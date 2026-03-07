"""
Judge Agreement Validation System
==================================

Compares AI-generated dog show scores with professional judges' ratings
using established inter-rater reliability statistics.

Statistical Methods Implemented
-------------------------------
1. Cohen's Kappa (k) -- chance-corrected agreement between two raters
   assigning categorical grades to the same set of dogs.

2. Weighted Cohen's Kappa -- extends kappa for ordinal grades where some
   disagreements are worse than others (e.g. S vs C is worse than A vs A+).
   Uses quadratic weights by default.

3. Intraclass Correlation Coefficient (ICC) -- two-way random, absolute
   agreement, single measures (ICC(2,1)).  Quantifies how consistently
   two raters assign *continuous* overall scores.

4. Bland-Altman Analysis -- plots the difference between raters against
   their mean.  Reports mean bias, 95% limits of agreement, and a simple
   bias detection test (whether the mean difference is significantly
   different from zero via a one-sample t-test).

5. Per-Axis Pearson Correlation -- Pearson r computed independently for
   each of the five scoring axes (skeletal, gait, muscle, coat,
   temperament).

6. Bootstrap Confidence Intervals -- non-parametric 95% CIs for kappa
   and ICC by resampling pairs with replacement.

7. Sample Size Recommendation -- approximates the number of dogs needed
   to estimate kappa or ICC within a desired half-width of the 95% CI,
   using the large-sample variance formula for kappa and a rule of thumb
   for ICC.

All calculations use only the Python standard library (math, statistics,
random) so the module works on constrained deployment targets such as
Render's ephemeral containers.

Grade Scale (ordinal, descending)
---------------------------------
S > A+ > A > B+ > B > C

Each result dict is expected to contain:
    skeletal        : float   (0-100)
    gait            : float   (0-100)
    muscle          : float   (0-100)
    coat            : float   (0-100)
    temperament     : float   (0-100)
    overall_score   : float   (0-100)
    grade           : str     one of S, A+, A, B+, B, C
"""

import logging
import math
import random

# -----------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------

GRADE_ORDER = ["C", "B", "B+", "A", "A+", "S"]
GRADE_INDEX = {g: i for i, g in enumerate(GRADE_ORDER)}
SCORING_AXES = ["skeletal", "gait", "muscle", "coat", "temperament"]


# -----------------------------------------------------------------------
# Helper: mean / variance / covariance (avoid numpy)
# -----------------------------------------------------------------------

def _mean(xs):
    """Arithmetic mean of a list of numbers."""
    if not xs:
        raise ValueError("Cannot compute mean of empty sequence")
    return sum(xs) / len(xs)


def _var(xs, ddof=0):
    """Variance with specified degrees-of-freedom correction.

    Parameters
    ----------
    xs : list[float]
    ddof : int
        Delta degrees of freedom.  0 = population variance,
        1 = sample (Bessel-corrected) variance.
    """
    if len(xs) < ddof + 1:
        raise ValueError("Not enough data points for requested ddof")
    m = _mean(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - ddof)


def _std(xs, ddof=0):
    """Standard deviation (square root of variance)."""
    return math.sqrt(_var(xs, ddof=ddof))


def _cov(xs, ys, ddof=0):
    """Covariance between two equal-length sequences.

    Parameters
    ----------
    xs, ys : list[float]
    ddof : int
        Delta degrees of freedom for the denominator.
    """
    if len(xs) != len(ys):
        raise ValueError("Sequences must have the same length")
    n = len(xs)
    if n < ddof + 1:
        raise ValueError("Not enough data points for requested ddof")
    mx = _mean(xs)
    my = _mean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (n - ddof)


def _pearson_r(xs, ys):
    """Pearson product-moment correlation coefficient.

    Returns
    -------
    float
        Correlation in [-1, 1].  Returns 0.0 if either variable has
        zero variance (constant).
    """
    sx = _std(xs)
    sy = _std(ys)
    if sx == 0.0 or sy == 0.0:
        return 0.0
    return _cov(xs, ys) / (sx * sy)


# -----------------------------------------------------------------------
# Cohen's Kappa (unweighted)
# -----------------------------------------------------------------------

def compute_cohens_kappa(grades_a, grades_b, categories=None):
    """Compute Cohen's Kappa for two lists of categorical grades.

    Cohen's Kappa measures agreement between two raters who each classify
    N items into C mutually exclusive categories.  It corrects for the
    amount of agreement expected by chance alone:

        k = (p_o - p_e) / (1 - p_e)

    where p_o is the observed proportion of agreement and p_e is the
    expected proportion of agreement under statistical independence.

    Interpretation (Landis & Koch, 1977):
        < 0.00   Poor
        0.00-0.20  Slight
        0.21-0.40  Fair
        0.41-0.60  Moderate
        0.61-0.80  Substantial
        0.81-1.00  Almost perfect

    Parameters
    ----------
    grades_a : list[str]
        Grades assigned by rater A (AI).
    grades_b : list[str]
        Grades assigned by rater B (judge).
    categories : list[str] or None
        Complete list of possible categories.  If None, the union of
        values seen in both lists is used.

    Returns
    -------
    dict
        kappa : float
        observed_agreement : float  (p_o)
        expected_agreement : float  (p_e)
        n : int
    """
    if len(grades_a) != len(grades_b):
        raise ValueError("Grade lists must have the same length")
    n = len(grades_a)
    if n == 0:
        raise ValueError("Cannot compute kappa on empty data")

    if categories is None:
        categories = sorted(set(grades_a) | set(grades_b))

    # Build confusion matrix counts
    counts_a = {c: 0 for c in categories}
    counts_b = {c: 0 for c in categories}
    agree = 0
    for a, b in zip(grades_a, grades_b):
        counts_a[a] = counts_a.get(a, 0) + 1
        counts_b[b] = counts_b.get(b, 0) + 1
        if a == b:
            agree += 1

    p_o = agree / n
    p_e = sum((counts_a.get(c, 0) / n) * (counts_b.get(c, 0) / n) for c in categories)

    kappa = 1.0 if p_e == 1.0 else (p_o - p_e) / (1.0 - p_e)

    return {
        "kappa": kappa,
        "observed_agreement": p_o,
        "expected_agreement": p_e,
        "n": n,
    }


# -----------------------------------------------------------------------
# Weighted Cohen's Kappa (quadratic weights, ordinal)
# -----------------------------------------------------------------------

def compute_weighted_kappa(grades_a, grades_b, categories=None, weight_type="quadratic"):
    """Compute Weighted Cohen's Kappa for ordinal grade data.

    When categories have a natural ordering (S > A+ > A > B+ > B > C),
    not all disagreements are equally serious.  Weighted kappa assigns
    a weight w_ij to each cell of the confusion matrix reflecting the
    severity of the disagreement.

    Quadratic weights (default):
        w_ij = 1 - ((i - j) / (k - 1))^2

    where k is the number of categories and i, j are the ordinal
    positions.  This gives full credit (1) for exact agreement and
    decreasing credit as the distance increases.

    Linear weights:
        w_ij = 1 - |i - j| / (k - 1)

    The weighted kappa formula:

        k_w = 1 - ( sum_ij w_ij^d * o_ij ) / ( sum_ij w_ij^d * e_ij )

    where w_ij^d = 1 - w_ij are *disagreement* weights, o_ij are
    observed counts, and e_ij are expected counts.

    Parameters
    ----------
    grades_a, grades_b : list[str]
    categories : list[str] or None
        Ordered from lowest to highest.  Defaults to GRADE_ORDER.
    weight_type : str
        "quadratic" or "linear".

    Returns
    -------
    dict
        weighted_kappa : float
        weight_type : str
        n : int
    """
    if len(grades_a) != len(grades_b):
        raise ValueError("Grade lists must have the same length")
    n = len(grades_a)
    if n == 0:
        raise ValueError("Cannot compute weighted kappa on empty data")

    if categories is None:
        categories = list(GRADE_ORDER)

    k = len(categories)
    cat_idx = {c: i for i, c in enumerate(categories)}

    # Build observed confusion matrix
    observed = [[0] * k for _ in range(k)]
    for a, b in zip(grades_a, grades_b):
        i = cat_idx[a]
        j = cat_idx[b]
        observed[i][j] += 1

    # Marginals
    row_totals = [sum(observed[i]) for i in range(k)]
    col_totals = [sum(observed[i][j] for i in range(k)) for j in range(k)]

    # Expected matrix under independence
    expected = [[(row_totals[i] * col_totals[j]) / n for j in range(k)] for i in range(k)]

    # Weight matrix (disagreement weights: 0 = perfect agreement)
    if k <= 1:
        return {"weighted_kappa": 1.0, "weight_type": weight_type, "n": n}

    w_disagree = [[0.0] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            if weight_type == "quadratic":
                w_disagree[i][j] = ((i - j) / (k - 1)) ** 2
            elif weight_type == "linear":
                w_disagree[i][j] = abs(i - j) / (k - 1)
            else:
                raise ValueError(f"Unknown weight_type: {weight_type}")

    # Weighted observed and expected disagreement
    num = sum(w_disagree[i][j] * observed[i][j] for i in range(k) for j in range(k))
    den = sum(w_disagree[i][j] * expected[i][j] for i in range(k) for j in range(k))

    weighted_kappa = 1.0 if den == 0.0 else 1.0 - num / den

    return {
        "weighted_kappa": weighted_kappa,
        "weight_type": weight_type,
        "n": n,
    }


# -----------------------------------------------------------------------
# Intraclass Correlation Coefficient  ICC(2,1)
# -----------------------------------------------------------------------

def compute_icc(scores_a, scores_b):
    """Compute ICC(2,1) -- two-way random, absolute agreement, single measures.

    The Intraclass Correlation Coefficient quantifies how much of the
    total variance in continuous scores is attributable to true
    differences between dogs (subjects), as opposed to systematic or
    random differences between raters.

    Model: two-way random effects
        X_ij = mu + s_i + r_j + e_ij

    where s_i ~ N(0, sigma_s^2)  (subject effect)
          r_j ~ N(0, sigma_r^2)  (rater effect)
          e_ij ~ N(0, sigma_e^2) (residual)

    ICC(2,1) = (MS_S - MS_E) / (MS_S + MS_E + 2*(MS_R - MS_E)/n)

    where MS_S = mean square for subjects (between-dog variance)
          MS_R = mean square for raters (between-rater variance)
          MS_E = mean square error (residual variance)
          n = number of subjects (dogs)

    Interpretation:
        < 0.50   Poor
        0.50-0.75  Moderate
        0.75-0.90  Good
        > 0.90   Excellent

    Parameters
    ----------
    scores_a, scores_b : list[float]
        Continuous overall scores from rater A (AI) and rater B (judge).

    Returns
    -------
    dict
        icc : float
        ms_subjects : float
        ms_raters : float
        ms_error : float
        n : int
    """
    if len(scores_a) != len(scores_b):
        raise ValueError("Score lists must have the same length")
    n = len(scores_a)
    if n < 2:
        raise ValueError("Need at least 2 subjects for ICC")

    k = 2  # number of raters

    # Grand mean
    grand_mean = (sum(scores_a) + sum(scores_b)) / (n * k)

    # Subject means (mean of both raters for each dog)
    subject_means = [(a + b) / k for a, b in zip(scores_a, scores_b)]

    # Rater means
    rater_means = [_mean(scores_a), _mean(scores_b)]

    # Sum of squares -- subjects (between-dog)
    ss_subjects = k * sum((sm - grand_mean) ** 2 for sm in subject_means)

    # Sum of squares -- raters (between-rater)
    ss_raters = n * sum((rm - grand_mean) ** 2 for rm in rater_means)

    # Total sum of squares
    ss_total = sum((x - grand_mean) ** 2 for x in scores_a) + \
               sum((x - grand_mean) ** 2 for x in scores_b)

    # Residual (error) sum of squares
    ss_error = ss_total - ss_subjects - ss_raters

    # Degrees of freedom
    df_subjects = n - 1
    df_raters = k - 1
    df_error = (n - 1) * (k - 1)

    # Mean squares
    ms_subjects = ss_subjects / df_subjects if df_subjects > 0 else 0.0
    ms_raters = ss_raters / df_raters if df_raters > 0 else 0.0
    ms_error = ss_error / df_error if df_error > 0 else 0.0

    # ICC(2,1) formula
    denominator = ms_subjects + ms_error + k * (ms_raters - ms_error) / n
    icc = 0.0 if denominator == 0.0 else (ms_subjects - ms_error) / denominator

    return {
        "icc": icc,
        "ms_subjects": ms_subjects,
        "ms_raters": ms_raters,
        "ms_error": ms_error,
        "n": n,
    }


# -----------------------------------------------------------------------
# Bland-Altman Analysis
# -----------------------------------------------------------------------

def compute_bland_altman(scores_a, scores_b, confidence=0.95):
    """Bland-Altman analysis for method comparison.

    The Bland-Altman plot (also called a Tukey mean-difference plot)
    assesses the agreement between two measurement methods by plotting
    the difference (A - B) against the mean ((A + B)/2) for each subject.

    Key outputs:

    * **Mean difference (bias)**: the average of (AI - Judge).  A value
      near zero suggests no systematic bias.

    * **Limits of agreement (LoA)**: mean_diff +/- z * sd_diff, where
      z is the standard normal quantile for the requested confidence
      level (1.96 for 95%).  Approximately 95% of differences are
      expected to fall within these limits.

    * **Bias detection**: a one-sample t-test on the differences with
      H0: mean_diff = 0.  If the p-value is below 0.05 the bias is
      considered statistically significant.

    The p-value is approximated using the survival function of the
    t-distribution via a continued-fraction expansion (no scipy needed).

    Parameters
    ----------
    scores_a, scores_b : list[float]
    confidence : float
        Confidence level for limits of agreement (default 0.95).

    Returns
    -------
    dict
        mean_diff : float
        sd_diff : float
        upper_loa : float
        lower_loa : float
        bias_significant : bool
        t_statistic : float
        p_value : float
        n : int
        pairs : list[dict]   each with 'mean' and 'diff'
    """
    if len(scores_a) != len(scores_b):
        raise ValueError("Score lists must have the same length")
    n = len(scores_a)
    if n < 2:
        raise ValueError("Need at least 2 pairs for Bland-Altman analysis")

    diffs = [a - b for a, b in zip(scores_a, scores_b)]
    means = [(a + b) / 2.0 for a, b in zip(scores_a, scores_b)]

    mean_diff = _mean(diffs)
    sd_diff = _std(diffs, ddof=1)

    # z multiplier for confidence level (use normal approx for large n)
    z = _normal_quantile((1.0 + confidence) / 2.0)

    upper_loa = mean_diff + z * sd_diff
    lower_loa = mean_diff - z * sd_diff

    # One-sample t-test: H0: mean_diff = 0
    se = sd_diff / math.sqrt(n) if n > 0 else 0.0
    if se == 0.0:
        # If all differences are identical: either all zero (no bias,
        # p=1) or all equal to some nonzero constant (perfect bias, p=0).
        if mean_diff == 0.0:
            t_stat = 0.0
            p_value = 1.0
        else:
            t_stat = float("inf")
            p_value = 0.0
    else:
        t_stat = mean_diff / se
        df = n - 1
        p_value = _t_test_two_tailed_p(t_stat, df)

    bias_significant = p_value < 0.05

    pairs = [{"mean": m, "diff": d} for m, d in zip(means, diffs)]

    return {
        "mean_diff": mean_diff,
        "sd_diff": sd_diff,
        "upper_loa": upper_loa,
        "lower_loa": lower_loa,
        "bias_significant": bias_significant,
        "t_statistic": t_stat,
        "p_value": p_value,
        "n": n,
        "pairs": pairs,
    }


# -----------------------------------------------------------------------
# Per-Axis Pearson Correlation
# -----------------------------------------------------------------------

def compute_per_axis_correlation(results_a, results_b):
    """Compute Pearson r for each scoring axis between two raters.

    Pearson r measures the linear association between two variables.
    Values close to +1 indicate strong positive linear relationship;
    close to 0 indicates no linear relationship.

    For dog show judging, high per-axis correlations (r > 0.7) suggest
    that the AI and human judge are evaluating the same underlying
    qualities in each axis.

    Parameters
    ----------
    results_a : list[dict]
        AI results for each dog, each containing keys for all 5 axes.
    results_b : list[dict]
        Judge results for each dog, same structure.

    Returns
    -------
    dict
        Keys are axis names; values are dicts with 'r' and 'n'.
    """
    if len(results_a) != len(results_b):
        raise ValueError("Result lists must have the same length")
    n = len(results_a)
    if n < 2:
        raise ValueError("Need at least 2 pairs for correlation")

    report = {}
    for axis in SCORING_AXES:
        xs = [r[axis] for r in results_a]
        ys = [r[axis] for r in results_b]
        r = _pearson_r(xs, ys)
        report[axis] = {"r": r, "n": n}

    return report


# -----------------------------------------------------------------------
# Bootstrap Confidence Intervals
# -----------------------------------------------------------------------

def _bootstrap_ci(pair_indices, stat_fn, n_boot=2000, confidence=0.95, seed=42):
    """Compute a bootstrap confidence interval for a statistic.

    Resamples the pair indices with replacement `n_boot` times, computes
    the statistic for each resample, and returns the percentile-based CI.

    Parameters
    ----------
    pair_indices : list[int]
        Indices into the original paired data (0 .. n-1).
    stat_fn : callable(list[int]) -> float
        Function that takes a list of indices and returns the statistic.
    n_boot : int
        Number of bootstrap replicates.
    confidence : float
        Confidence level.
    seed : int or None
        Random seed for reproducibility.

    Returns
    -------
    dict
        ci_lower : float
        ci_upper : float
        se : float  (bootstrap standard error)
        n_boot : int
    """
    _logger = logging.getLogger(__name__)
    rng = random.Random(seed)
    n = len(pair_indices)
    boot_stats = []
    _skipped = 0
    for _ in range(n_boot):
        sample = [rng.choice(pair_indices) for _ in range(n)]
        try:
            boot_stats.append(stat_fn(sample))
        except (ValueError, ZeroDivisionError):
            _skipped += 1
            continue
    if _skipped > 0:
        _logger.debug(
            "Bootstrap: %d/%d iterations skipped due to numerical errors",
            _skipped, n_boot,
        )

    if len(boot_stats) < 10:
        return {"ci_lower": float("nan"), "ci_upper": float("nan"), "se": float("nan"), "n_boot": len(boot_stats)}

    boot_stats.sort()
    alpha = 1.0 - confidence
    lower_idx = int(math.floor((alpha / 2.0) * len(boot_stats)))
    upper_idx = int(math.ceil((1.0 - alpha / 2.0) * len(boot_stats))) - 1
    lower_idx = max(0, min(lower_idx, len(boot_stats) - 1))
    upper_idx = max(0, min(upper_idx, len(boot_stats) - 1))

    return {
        "ci_lower": boot_stats[lower_idx],
        "ci_upper": boot_stats[upper_idx],
        "se": _std(boot_stats, ddof=1) if len(boot_stats) > 1 else 0.0,
        "n_boot": len(boot_stats),
    }


# -----------------------------------------------------------------------
# Sample Size Recommendation (power analysis approximation)
# -----------------------------------------------------------------------

def get_sample_size_recommendation(target_kappa=0.7, desired_half_width=0.1,
                                   confidence=0.95, target_icc=0.8,
                                   desired_icc_half_width=0.1):
    """Recommend minimum sample sizes for kappa and ICC estimation.

    Kappa sample size
    -----------------
    Uses the large-sample variance approximation for kappa under the
    null hypothesis of the target value:

        Var(k) ~ 1 / n  (simplified)

    A more precise formula (Fleiss, 1981) depends on the marginal
    proportions, but as a conservative rule of thumb:

        n >= (z / desired_half_width)^2 * pe_factor

    where pe_factor accounts for expected agreement by chance.  We use
    pe_factor = 2 as a moderately conservative default.

    ICC sample size
    ---------------
    For ICC(2,1) the required sample size can be approximated (Bonett,
    2002) as:

        n >= 8 * (1 - target_icc)^2 * (1 + target_icc)^2
             / (desired_icc_half_width^2) + 2

    Parameters
    ----------
    target_kappa : float
        Expected kappa value to plan around.
    desired_half_width : float
        Desired half-width of the 95% CI for kappa.
    confidence : float
        Confidence level.
    target_icc : float
        Expected ICC value.
    desired_icc_half_width : float
        Desired half-width of the 95% CI for ICC.

    Returns
    -------
    dict
        kappa_n : int   recommended n for kappa
        icc_n : int     recommended n for ICC
        recommended_n : int  max of the two (conservative)
        notes : str
    """
    z = _normal_quantile((1.0 + confidence) / 2.0)

    # Kappa sample size (conservative approximation)
    pe_factor = 2.0  # conservative multiplier
    kappa_n_raw = (z / desired_half_width) ** 2 * pe_factor
    kappa_n = int(math.ceil(kappa_n_raw))

    # ICC sample size (Bonett 2002 approximation)
    icc_n_raw = (8.0 * (1.0 - target_icc) ** 2 * (1.0 + target_icc) ** 2
                 / (desired_icc_half_width ** 2)) + 2
    icc_n = int(math.ceil(icc_n_raw))

    recommended = max(kappa_n, icc_n)

    return {
        "kappa_n": kappa_n,
        "icc_n": icc_n,
        "recommended_n": recommended,
        "notes": (
            f"To estimate kappa within +/-{desired_half_width} at "
            f"{confidence*100:.0f}% confidence, need >= {kappa_n} dogs. "
            f"To estimate ICC within +/-{desired_icc_half_width} at "
            f"{confidence*100:.0f}% confidence, need >= {icc_n} dogs. "
            f"Recommended minimum: {recommended} dogs."
        ),
    }


# -----------------------------------------------------------------------
# Approximate normal quantile (inverse CDF) -- no scipy
# -----------------------------------------------------------------------

def _normal_quantile(p):
    """Approximate inverse of the standard normal CDF.

    Uses the rational approximation by Peter Acklam (relative error
    < 1.15e-9 across the full range).

    Parameters
    ----------
    p : float
        Probability in (0, 1).

    Returns
    -------
    float
        z such that Phi(z) = p.
    """
    if p <= 0.0 or p >= 1.0:
        raise ValueError("p must be in (0, 1)")

    # Coefficients
    a = [
        -3.969683028665376e+01,
         2.209460984245205e+02,
        -2.759285104469687e+02,
         1.383577518672690e+02,
        -3.066479806614716e+01,
         2.506628277459239e+00,
    ]
    b = [
        -5.447609879822406e+01,
         1.615858368580409e+02,
        -1.556989798598866e+02,
         6.680131188771972e+01,
        -1.328068155288572e+01,
    ]
    c = [
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e+00,
        -2.549732539343734e+00,
         4.374664141464968e+00,
         2.938163982698783e+00,
    ]
    d = [
         7.784695709041462e-03,
         3.224671290700398e-01,
         2.445134137142996e+00,
         3.754408661907416e+00,
    ]

    p_low = 0.02425
    p_high = 1.0 - p_low

    if p < p_low:
        q = math.sqrt(-2.0 * math.log(p))
        z = (((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / \
            ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1.0)
    elif p <= p_high:
        q = p - 0.5
        r = q * q
        z = (((((a[0]*r + a[1])*r + a[2])*r + a[3])*r + a[4])*r + a[5]) * q / \
            (((((b[0]*r + b[1])*r + b[2])*r + b[3])*r + b[4])*r + 1.0)
    else:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        z = -(((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / \
             ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1.0)

    return z


# -----------------------------------------------------------------------
# Approximate t-distribution p-value (two-tailed) -- no scipy
# -----------------------------------------------------------------------

def _t_test_two_tailed_p(t_stat, df):
    """Two-tailed p-value for Student's t-distribution.

    Uses the regularised incomplete beta function relationship:

        p = I_{df/(df+t^2)}(df/2, 1/2)

    The regularised incomplete beta function is computed via a
    continued-fraction expansion (Lentz's method).

    Parameters
    ----------
    t_stat : float
        Observed t statistic.
    df : int or float
        Degrees of freedom (> 0).

    Returns
    -------
    float
        Two-tailed p-value in [0, 1].
    """
    if df <= 0:
        return float("nan")
    x = df / (df + t_stat ** 2)
    a = df / 2.0
    b = 0.5
    p = _regularized_incomplete_beta(x, a, b)
    return max(0.0, min(1.0, p))


def _regularized_incomplete_beta(x, a, b):
    """Regularised incomplete beta function I_x(a, b).

    Uses the continued-fraction representation (Lentz's modified method)
    for numerical stability.

    Parameters
    ----------
    x : float in [0, 1]
    a, b : float > 0

    Returns
    -------
    float
        I_x(a, b) in [0, 1].
    """
    if x < 0.0 or x > 1.0:
        raise ValueError("x must be in [0, 1]")
    if x == 0.0:
        return 0.0
    if x == 1.0:
        return 1.0

    # Use symmetry relation if x > (a+1)/(a+b+2) for better convergence
    if x > (a + 1.0) / (a + b + 2.0):
        return 1.0 - _regularized_incomplete_beta(1.0 - x, b, a)

    # Log of the front factor: x^a * (1-x)^b / (a * Beta(a,b))
    lbeta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    front = math.exp(a * math.log(x) + b * math.log(1.0 - x) - lbeta - math.log(a))

    # Continued fraction (Lentz's method)
    TINY = 1e-30
    MAX_ITER = 200
    EPS = 1e-12

    f = 1.0 + TINY
    c = f
    d = 0.0

    for m in range(0, MAX_ITER):
        if m == 0:
            numerator = 1.0
        elif m % 2 == 1:
            k = (m - 1) // 2 + 1
            numerator = -(a + k) * (a + b + k) * x / ((a + 2*k) * (a + 2*k + 1))
        else:
            k = m // 2
            numerator = k * (b - k) * x / ((a + 2*k - 1) * (a + 2*k))

        d = 1.0 + numerator * d
        if abs(d) < TINY:
            d = TINY
        d = 1.0 / d

        c = 1.0 + numerator / c
        if abs(c) < TINY:
            c = TINY

        delta = c * d
        f *= delta

        if abs(delta - 1.0) < EPS:
            break

    return max(0.0, min(1.0, front * (f - 1.0)))


# =======================================================================
# JudgeValidationSession
# =======================================================================

class JudgeValidationSession:
    """Manages a set of (AI result, Judge result) pairs and computes
    comprehensive inter-rater agreement statistics.

    Usage
    -----
    >>> session = JudgeValidationSession()
    >>> session.add_pair(ai_result, judge_result)   # for each dog
    >>> report = session.compute_full_report()

    Each result dict must contain:
        skeletal        : float (0-100)
        gait            : float (0-100)
        muscle          : float (0-100)
        coat            : float (0-100)
        temperament     : float (0-100)
        overall_score   : float (0-100)
        grade           : str   one of S, A+, A, B+, B, C
    """

    REQUIRED_KEYS = {"skeletal", "gait", "muscle", "coat", "temperament",
                     "overall_score", "grade"}

    def __init__(self):
        """Initialise an empty validation session."""
        self._pairs = []  # list of (ai_result, judge_result) tuples

    # -------------------------------------------------------------------
    # Data management
    # -------------------------------------------------------------------

    def add_pair(self, ai_result, judge_result):
        """Add a paired observation for one dog.

        Parameters
        ----------
        ai_result : dict
            AI scoring result.
        judge_result : dict
            Professional judge scoring result (same structure).

        Raises
        ------
        ValueError
            If required keys are missing or grade is invalid.
        """
        for label, result in [("ai_result", ai_result), ("judge_result", judge_result)]:
            missing = self.REQUIRED_KEYS - set(result.keys())
            if missing:
                raise ValueError(f"{label} is missing keys: {missing}")
            if result["grade"] not in GRADE_INDEX:
                raise ValueError(
                    f"{label} has invalid grade '{result['grade']}'. "
                    f"Must be one of {GRADE_ORDER}"
                )

        self._pairs.append((dict(ai_result), dict(judge_result)))

    @property
    def n(self):
        """Number of paired observations currently stored."""
        return len(self._pairs)

    # -------------------------------------------------------------------
    # Individual statistics
    # -------------------------------------------------------------------

    def compute_cohens_kappa(self):
        """Compute unweighted Cohen's Kappa on grades.

        Returns
        -------
        dict   (see module-level compute_cohens_kappa docstring)
        """
        grades_a = [p[0]["grade"] for p in self._pairs]
        grades_b = [p[1]["grade"] for p in self._pairs]
        return compute_cohens_kappa(grades_a, grades_b, categories=GRADE_ORDER)

    def compute_weighted_kappa(self, weight_type="quadratic"):
        """Compute weighted Cohen's Kappa on ordinal grades.

        Parameters
        ----------
        weight_type : str   "quadratic" or "linear"

        Returns
        -------
        dict   (see module-level compute_weighted_kappa docstring)
        """
        grades_a = [p[0]["grade"] for p in self._pairs]
        grades_b = [p[1]["grade"] for p in self._pairs]
        return compute_weighted_kappa(grades_a, grades_b,
                                      categories=GRADE_ORDER,
                                      weight_type=weight_type)

    def compute_icc(self):
        """Compute ICC(2,1) on overall_score.

        Returns
        -------
        dict   (see module-level compute_icc docstring)
        """
        scores_a = [p[0]["overall_score"] for p in self._pairs]
        scores_b = [p[1]["overall_score"] for p in self._pairs]
        return compute_icc(scores_a, scores_b)

    def compute_bland_altman(self):
        """Run Bland-Altman analysis on overall_score.

        Returns
        -------
        dict   (see module-level compute_bland_altman docstring)
        """
        scores_a = [p[0]["overall_score"] for p in self._pairs]
        scores_b = [p[1]["overall_score"] for p in self._pairs]
        return compute_bland_altman(scores_a, scores_b)

    def compute_per_axis_correlation(self):
        """Pearson r for each scoring axis.

        Returns
        -------
        dict   (see module-level compute_per_axis_correlation docstring)
        """
        results_a = [p[0] for p in self._pairs]
        results_b = [p[1] for p in self._pairs]
        return compute_per_axis_correlation(results_a, results_b)

    # -------------------------------------------------------------------
    # Bootstrap CIs
    # -------------------------------------------------------------------

    def _bootstrap_kappa_ci(self, n_boot=2000, confidence=0.95, seed=42):
        """Bootstrap 95% CI for unweighted Cohen's Kappa.

        Resamples pairs with replacement and recomputes kappa for each
        bootstrap sample to estimate the sampling distribution.

        Returns
        -------
        dict with ci_lower, ci_upper, se, n_boot
        """
        grades_a = [p[0]["grade"] for p in self._pairs]
        grades_b = [p[1]["grade"] for p in self._pairs]
        indices = list(range(self.n))

        def stat_fn(idx_sample):
            ga = [grades_a[i] for i in idx_sample]
            gb = [grades_b[i] for i in idx_sample]
            return compute_cohens_kappa(ga, gb, categories=GRADE_ORDER)["kappa"]

        return _bootstrap_ci(indices, stat_fn, n_boot=n_boot,
                             confidence=confidence, seed=seed)

    def _bootstrap_icc_ci(self, n_boot=2000, confidence=0.95, seed=42):
        """Bootstrap 95% CI for ICC(2,1).

        Returns
        -------
        dict with ci_lower, ci_upper, se, n_boot
        """
        scores_a = [p[0]["overall_score"] for p in self._pairs]
        scores_b = [p[1]["overall_score"] for p in self._pairs]
        indices = list(range(self.n))

        def stat_fn(idx_sample):
            sa = [scores_a[i] for i in idx_sample]
            sb = [scores_b[i] for i in idx_sample]
            return compute_icc(sa, sb)["icc"]

        return _bootstrap_ci(indices, stat_fn, n_boot=n_boot,
                             confidence=confidence, seed=seed)

    # -------------------------------------------------------------------
    # Sample size recommendation
    # -------------------------------------------------------------------

    def get_sample_size_recommendation(self, **kwargs):
        """Return sample size recommendations.

        Delegates to the module-level function.  If kappa and ICC have
        already been computed on current data, their point estimates are
        used as planning values; otherwise the defaults are used.

        Returns
        -------
        dict   (see module-level get_sample_size_recommendation docstring)
        """
        # Attempt to use current estimates as planning values
        defaults = {}
        try:
            kappa_result = self.compute_cohens_kappa()
            defaults["target_kappa"] = kappa_result["kappa"]
        except (ValueError, ZeroDivisionError) as e:
            logging.getLogger(__name__).debug(
                "Could not compute kappa for sample-size defaults: %s", e,
            )
        try:
            icc_result = self.compute_icc()
            defaults["target_icc"] = icc_result["icc"]
        except (ValueError, ZeroDivisionError) as e:
            logging.getLogger(__name__).debug(
                "Could not compute ICC for sample-size defaults: %s", e,
            )

        # Caller kwargs override
        defaults.update(kwargs)
        return get_sample_size_recommendation(**defaults)

    # -------------------------------------------------------------------
    # Full report
    # -------------------------------------------------------------------

    def compute_full_report(self, include_bootstrap=True, n_boot=2000):
        """Generate a comprehensive validation report.

        Computes every available statistic and assembles them into a
        single nested dictionary for downstream consumption (API
        response, logging, display).

        Parameters
        ----------
        include_bootstrap : bool
            Whether to compute bootstrap CIs (can be slow for large n).
        n_boot : int
            Number of bootstrap replicates.

        Returns
        -------
        dict
            n : int
            cohens_kappa : dict
            weighted_kappa : dict
            icc : dict
            bland_altman : dict  (pairs list omitted for brevity)
            per_axis_correlation : dict
            bootstrap_ci : dict  (only if include_bootstrap)
            sample_size_recommendation : dict
            interpretation : dict   human-readable quality labels
        """
        if self.n < 2:
            raise ValueError(
                f"Need at least 2 paired observations; currently have {self.n}"
            )

        kappa = self.compute_cohens_kappa()
        w_kappa = self.compute_weighted_kappa()
        icc = self.compute_icc()
        ba = self.compute_bland_altman()
        per_axis = self.compute_per_axis_correlation()
        sample_rec = self.get_sample_size_recommendation()

        # Strip verbose pairs from Bland-Altman for the summary report
        ba_summary = {k: v for k, v in ba.items() if k != "pairs"}

        report = {
            "n": self.n,
            "cohens_kappa": kappa,
            "weighted_kappa": w_kappa,
            "icc": icc,
            "bland_altman": ba_summary,
            "per_axis_correlation": per_axis,
            "sample_size_recommendation": sample_rec,
            "interpretation": self._interpret(kappa, w_kappa, icc, ba, per_axis),
        }

        if include_bootstrap:
            report["bootstrap_ci"] = {
                "kappa_95ci": self._bootstrap_kappa_ci(n_boot=n_boot),
                "icc_95ci": self._bootstrap_icc_ci(n_boot=n_boot),
            }

        return report

    # -------------------------------------------------------------------
    # Interpretation helper
    # -------------------------------------------------------------------

    @staticmethod
    def _interpret(kappa, w_kappa, icc, ba, per_axis):
        """Generate human-readable quality labels for each statistic.

        Returns
        -------
        dict with string labels.
        """
        def kappa_label(k):
            if k < 0.0:
                return "Poor (less than chance)"
            elif k < 0.21:
                return "Slight"
            elif k < 0.41:
                return "Fair"
            elif k < 0.61:
                return "Moderate"
            elif k < 0.81:
                return "Substantial"
            else:
                return "Almost Perfect"

        def icc_label(v):
            if v < 0.50:
                return "Poor"
            elif v < 0.75:
                return "Moderate"
            elif v < 0.90:
                return "Good"
            else:
                return "Excellent"

        def r_label(r):
            ar = abs(r)
            if ar < 0.30:
                return "Weak"
            elif ar < 0.50:
                return "Low-Moderate"
            elif ar < 0.70:
                return "Moderate"
            elif ar < 0.90:
                return "Strong"
            else:
                return "Very Strong"

        interp = {
            "cohens_kappa": kappa_label(kappa["kappa"]),
            "weighted_kappa": kappa_label(w_kappa["weighted_kappa"]),
            "icc": icc_label(icc["icc"]),
            "bias": "Significant systematic bias detected" if ba["bias_significant"]
                    else "No significant systematic bias",
            "per_axis": {axis: r_label(data["r"]) for axis, data in per_axis.items()},
        }
        return interp


# =======================================================================
# Self-test
# =======================================================================

def _self_test():
    """Run a battery of self-tests to verify correctness.

    This function creates synthetic data with known properties and
    checks that the computed statistics are within expected ranges.
    It prints PASS/FAIL for each test.

    Can be executed directly:
        python -m api.judge_validation
    """
    print("=" * 60)
    print("Judge Validation Module -- Self Test")
    print("=" * 60)

    passed = 0
    failed = 0

    def check(name, condition):
        nonlocal passed, failed
        if condition:
            print(f"  PASS: {name}")
            passed += 1
        else:
            print(f"  FAIL: {name}")
            failed += 1

    # ----- Test 1: Perfect agreement kappa = 1.0 -----------------------
    print("\n[Test 1] Perfect agreement -> kappa = 1.0")
    grades = ["S", "A+", "A", "B+", "B", "C", "S", "A"]
    result = compute_cohens_kappa(grades, grades)
    check("kappa == 1.0", abs(result["kappa"] - 1.0) < 1e-9)
    check("observed_agreement == 1.0", abs(result["observed_agreement"] - 1.0) < 1e-9)

    # ----- Test 2: Known kappa value -----------------------------------
    print("\n[Test 2] Known disagreement pattern")
    g_a = ["A", "A", "A", "B", "B", "B"]
    g_b = ["A", "B", "A", "B", "A", "B"]
    result = compute_cohens_kappa(g_a, g_b, categories=["A", "B"])
    # p_o = 4/6 = 0.6667, p_e = (3/6)*(3/6) + (3/6)*(3/6) = 0.5
    # kappa = (0.6667 - 0.5) / (1 - 0.5) = 0.3333
    check("kappa ~ 0.333", abs(result["kappa"] - 1.0/3.0) < 0.01)

    # ----- Test 3: Weighted kappa with perfect agreement ---------------
    print("\n[Test 3] Weighted kappa with perfect agreement")
    grades = ["S", "A+", "A", "B+", "B", "C"]
    result = compute_weighted_kappa(grades, grades)
    check("weighted_kappa == 1.0", abs(result["weighted_kappa"] - 1.0) < 1e-9)

    # ----- Test 4: Weighted kappa < unweighted when ordinal close ------
    print("\n[Test 4] Weighted kappa > unweighted for near-miss ordinal")
    g_a = ["S",  "A+", "A",  "B+", "B",  "C"]
    g_b = ["A+", "A",  "B+", "B",  "C",  "C"]  # one step off each
    uw = compute_cohens_kappa(g_a, g_b, categories=GRADE_ORDER)
    wk = compute_weighted_kappa(g_a, g_b)
    check("weighted > unweighted for near-misses",
          wk["weighted_kappa"] > uw["kappa"])

    # ----- Test 5: ICC with identical scores = 1.0 ---------------------
    print("\n[Test 5] ICC with identical scores -> 1.0")
    scores = [90.0, 85.0, 70.0, 60.0, 95.0]
    result = compute_icc(scores, scores)
    check("icc == 1.0", abs(result["icc"] - 1.0) < 1e-6)

    # ----- Test 6: ICC with random noise < 1.0 -------------------------
    print("\n[Test 6] ICC with added noise < 1.0")
    rng = random.Random(123)
    base = [rng.gauss(75, 10) for _ in range(50)]
    noisy = [s + rng.gauss(0, 5) for s in base]
    result = compute_icc(base, noisy)
    check("0 < icc < 1", 0.0 < result["icc"] < 1.0)

    # ----- Test 7: Bland-Altman with zero bias -------------------------
    print("\n[Test 7] Bland-Altman no-bias scenario")
    rng = random.Random(456)
    n = 100
    sa = [rng.gauss(75, 10) for _ in range(n)]
    sb = [s + rng.gauss(0, 2) for s in sa]  # small symmetric noise
    result = compute_bland_altman(sa, sb)
    check("mean_diff near 0", abs(result["mean_diff"]) < 2.0)
    check("lower_loa < 0 < upper_loa",
          result["lower_loa"] < 0 < result["upper_loa"])

    # ----- Test 8: Bland-Altman with known bias ------------------------
    print("\n[Test 8] Bland-Altman with systematic +10 bias")
    sa = [70.0, 80.0, 90.0, 60.0, 75.0, 85.0, 65.0, 95.0, 55.0, 72.0]
    sb = [s - 10.0 for s in sa]  # judge consistently 10 lower
    result = compute_bland_altman(sa, sb)
    check("mean_diff ~ 10", abs(result["mean_diff"] - 10.0) < 0.01)
    check("bias_significant is True", result["bias_significant"])

    # ----- Test 9: Per-axis correlation with perfect linear data -------
    print("\n[Test 9] Per-axis Pearson r with perfect correlation")
    results_a = [{"skeletal": i*10.0, "gait": i*5.0, "muscle": i*8.0,
                  "coat": i*3.0, "temperament": i*7.0} for i in range(1, 11)]
    results_b = [{"skeletal": i*10.0, "gait": i*5.0, "muscle": i*8.0,
                  "coat": i*3.0, "temperament": i*7.0} for i in range(1, 11)]
    result = compute_per_axis_correlation(results_a, results_b)
    for axis in SCORING_AXES:
        check(f"r({axis}) == 1.0", abs(result[axis]["r"] - 1.0) < 1e-9)

    # ----- Test 10: JudgeValidationSession full report -----------------
    print("\n[Test 10] JudgeValidationSession full workflow")
    session = JudgeValidationSession()
    rng = random.Random(789)
    for _ in range(30):
        base_score = rng.gauss(75, 12)
        base_score = max(10, min(100, base_score))
        ai_axes = {ax: max(0, min(100, base_score + rng.gauss(0, 5)))
                   for ax in SCORING_AXES}
        judge_axes = {ax: max(0, min(100, base_score + rng.gauss(0, 5)))
                      for ax in SCORING_AXES}
        ai_overall = max(0, min(100, base_score + rng.gauss(0, 3)))
        judge_overall = max(0, min(100, base_score + rng.gauss(0, 3)))

        # Assign grade based on overall score (both use similar thresholds)
        def score_to_grade(s):
            if s >= 92:
                return "S"
            elif s >= 84:
                return "A+"
            elif s >= 76:
                return "A"
            elif s >= 68:
                return "B+"
            elif s >= 60:
                return "B"
            else:
                return "C"

        ai_result = {**ai_axes, "overall_score": ai_overall,
                     "grade": score_to_grade(ai_overall)}
        judge_result = {**judge_axes, "overall_score": judge_overall,
                        "grade": score_to_grade(judge_overall)}
        session.add_pair(ai_result, judge_result)

    check("session.n == 30", session.n == 30)

    report = session.compute_full_report(include_bootstrap=True, n_boot=500)
    check("report has 'cohens_kappa'", "cohens_kappa" in report)
    check("report has 'weighted_kappa'", "weighted_kappa" in report)
    check("report has 'icc'", "icc" in report)
    check("report has 'bland_altman'", "bland_altman" in report)
    check("report has 'per_axis_correlation'", "per_axis_correlation" in report)
    check("report has 'bootstrap_ci'", "bootstrap_ci" in report)
    check("report has 'interpretation'", "interpretation" in report)
    check("report has 'sample_size_recommendation'", "sample_size_recommendation" in report)

    # Kappa should be reasonable (not perfect, not zero) for this data
    k = report["cohens_kappa"]["kappa"]
    check(f"kappa in plausible range (got {k:.3f})", -0.5 < k < 1.0)

    wk = report["weighted_kappa"]["weighted_kappa"]
    check(f"weighted_kappa in plausible range (got {wk:.3f})", -0.5 < wk < 1.0)

    icc_val = report["icc"]["icc"]
    check(f"icc in plausible range (got {icc_val:.3f})", 0.0 < icc_val < 1.0)

    # Bootstrap CIs should contain the point estimates
    kci = report["bootstrap_ci"]["kappa_95ci"]
    check("kappa CI contains point estimate",
          kci["ci_lower"] <= k <= kci["ci_upper"])

    icci = report["bootstrap_ci"]["icc_95ci"]
    check("ICC CI contains point estimate",
          icci["ci_lower"] <= icc_val <= icci["ci_upper"])

    # ----- Test 11: Sample size recommendation -------------------------
    print("\n[Test 11] Sample size recommendation")
    rec = get_sample_size_recommendation()
    check("kappa_n > 0", rec["kappa_n"] > 0)
    check("icc_n > 0", rec["icc_n"] > 0)
    check("recommended_n >= max(kappa_n, icc_n)",
          rec["recommended_n"] >= max(rec["kappa_n"], rec["icc_n"]))

    # ----- Test 12: Edge case - add_pair validation --------------------
    print("\n[Test 12] Input validation")
    session2 = JudgeValidationSession()
    try:
        session2.add_pair({"skeletal": 80}, {"skeletal": 80})
        check("missing keys raises ValueError", False)
    except ValueError:
        check("missing keys raises ValueError", True)

    try:
        bad = {"skeletal": 80, "gait": 80, "muscle": 80, "coat": 80,
               "temperament": 80, "overall_score": 80, "grade": "X"}
        good = {"skeletal": 80, "gait": 80, "muscle": 80, "coat": 80,
                "temperament": 80, "overall_score": 80, "grade": "A"}
        session2.add_pair(bad, good)
        check("invalid grade raises ValueError", False)
    except ValueError:
        check("invalid grade raises ValueError", True)

    # ----- Test 13: Normal quantile sanity check -----------------------
    print("\n[Test 13] Normal quantile approximation")
    z95 = _normal_quantile(0.975)
    check(f"z(0.975) ~ 1.96 (got {z95:.4f})", abs(z95 - 1.96) < 0.001)
    z50 = _normal_quantile(0.5)
    check(f"z(0.5) ~ 0.0 (got {z50:.6f})", abs(z50) < 0.001)

    # ----- Test 14: t-test p-value sanity check ------------------------
    print("\n[Test 14] t-test p-value")
    p_zero = _t_test_two_tailed_p(0.0, 10)
    check(f"t=0, df=10 -> p~1.0 (got {p_zero:.4f})", abs(p_zero - 1.0) < 0.05)
    p_large = _t_test_two_tailed_p(10.0, 30)
    check(f"t=10, df=30 -> p~0.0 (got {p_large:.6f})", p_large < 0.001)

    # ----- Summary -----------------------------------------------------
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed out of {passed + failed}")
    print("=" * 60)

    return failed == 0


# -----------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------

if __name__ == "__main__":
    success = _self_test()
    raise SystemExit(0 if success else 1)
