"""
Longitudinal Growth Prediction System for Show Dogs.

Uses historical analysis data (age and scores over time) to predict future
scores, growth trajectories, and optimal show ages. Implements multiple
curve-fitting models (Modified Gompertz, Polynomial, Von Bertalanffy) and
selects the best fit using information criteria (AIC/BIC).

All numerical work uses only the Python standard library (math, statistics).
Nonlinear curve fitting is performed via a simplified Levenberg-Marquardt
algorithm implemented from scratch. Linear least-squares uses explicit
matrix algebra helpers also included in this module.

Classes:
    GrowthCurveModel  -- fits a single growth curve to (age, score) data.
    GrowthPredictor   -- higher-level manager for per-dog, per-axis predictions.

Typical usage:
    history = [
        (0.5, {"balance": 60, "coat": 55, "structure": 58, "gait": 50, "temperament": 65}),
        (1.0, {"balance": 72, "coat": 68, "structure": 70, "gait": 66, "temperament": 74}),
        ...
    ]
    predictor = GrowthPredictor(breed="Labrador Retriever")
    predictor.fit(history)
    future = predictor.predict(target_age=3.0)
    peak   = predictor.predict_peak_age()
    phase  = predictor.get_growth_phase(age=2.0)
    anomalies = predictor.detect_anomalies()
    trajectory = predictor.get_trajectory(age_range=(0.5, 8.0), step=0.25)
"""

import logging
import math
import statistics
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AXES: List[str] = ["balance", "coat", "structure", "gait", "temperament"]

# Default breed-specific expectations (age in years).  Users may override
# by passing their own dict to GrowthPredictor.
DEFAULT_BREED_EXPECTATIONS: Dict[str, Dict[str, float]] = {
    "default": {
        "puppy_peak_age": 1.5,
        "adult_peak_start": 2.0,
        "adult_peak_end": 5.0,
        "senior_onset": 7.0,
    },
    "Labrador Retriever": {
        "puppy_peak_age": 1.5,
        "adult_peak_start": 2.0,
        "adult_peak_end": 5.5,
        "senior_onset": 7.0,
    },
    "German Shepherd": {
        "puppy_peak_age": 1.8,
        "adult_peak_start": 2.5,
        "adult_peak_end": 5.0,
        "senior_onset": 7.0,
    },
    "Toy Poodle": {
        "puppy_peak_age": 1.2,
        "adult_peak_start": 1.5,
        "adult_peak_end": 6.0,
        "senior_onset": 9.0,
    },
    "Great Dane": {
        "puppy_peak_age": 1.5,
        "adult_peak_start": 2.0,
        "adult_peak_end": 4.0,
        "senior_onset": 5.5,
    },
    "Shiba Inu": {
        "puppy_peak_age": 1.3,
        "adult_peak_start": 1.8,
        "adult_peak_end": 6.0,
        "senior_onset": 8.0,
    },
    "Golden Retriever": {
        "puppy_peak_age": 1.5,
        "adult_peak_start": 2.0,
        "adult_peak_end": 5.5,
        "senior_onset": 7.0,
    },
    "French Bulldog": {
        "puppy_peak_age": 1.2,
        "adult_peak_start": 1.5,
        "adult_peak_end": 5.0,
        "senior_onset": 7.5,
    },
    "Border Collie": {
        "puppy_peak_age": 1.5,
        "adult_peak_start": 2.0,
        "adult_peak_end": 6.0,
        "senior_onset": 8.0,
    },
}

# Minimum data points required to attempt nonlinear curve fitting.
MIN_POINTS_NONLINEAR = 4
# Minimum data points required for any prediction at all.
MIN_POINTS_ANY = 3

# Anomaly detection threshold (number of standard deviations).
ANOMALY_SD_THRESHOLD = 2.0


# ============================================================================
# Matrix helpers  (pure-Python, no numpy)
# ============================================================================

def _mat_zeros(rows: int, cols: int) -> List[List[float]]:
    """Return a *rows x cols* matrix of zeros."""
    return [[0.0] * cols for _ in range(rows)]


def _mat_identity(n: int) -> List[List[float]]:
    """Return an *n x n* identity matrix."""
    m = _mat_zeros(n, n)
    for i in range(n):
        m[i][i] = 1.0
    return m


def _mat_transpose(A: List[List[float]]) -> List[List[float]]:
    """Transpose matrix *A*."""
    rows = len(A)
    cols = len(A[0])
    T = _mat_zeros(cols, rows)
    for i in range(rows):
        for j in range(cols):
            T[j][i] = A[i][j]
    return T


def _mat_mul(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """Multiply matrices *A* (m x n) and *B* (n x p)."""
    m = len(A)
    n = len(A[0])
    p = len(B[0])
    C = _mat_zeros(m, p)
    for i in range(m):
        for j in range(p):
            s = 0.0
            for k in range(n):
                s += A[i][k] * B[k][j]
            C[i][j] = s
    return C


def _mat_vec_mul(A: List[List[float]], v: List[float]) -> List[float]:
    """Multiply matrix *A* (m x n) by column vector *v* (length n)."""
    m = len(A)
    n = len(A[0])
    result = [0.0] * m
    for i in range(m):
        s = 0.0
        for j in range(n):
            s += A[i][j] * v[j]
        result[i] = s
    return result


def _mat_add(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """Element-wise addition of two matrices of equal shape."""
    rows = len(A)
    cols = len(A[0])
    C = _mat_zeros(rows, cols)
    for i in range(rows):
        for j in range(cols):
            C[i][j] = A[i][j] + B[i][j]
    return C


def _mat_scale(A: List[List[float]], s: float) -> List[List[float]]:
    """Multiply every element of *A* by scalar *s*."""
    rows = len(A)
    cols = len(A[0])
    C = _mat_zeros(rows, cols)
    for i in range(rows):
        for j in range(cols):
            C[i][j] = A[i][j] * s
    return C


def _mat_inverse(A: List[List[float]]) -> List[List[float]]:
    """Invert a square matrix via Gauss-Jordan elimination.

    Raises ``ValueError`` if the matrix is singular.
    """
    n = len(A)
    # Augment with identity.
    aug = _mat_zeros(n, 2 * n)
    for i in range(n):
        for j in range(n):
            aug[i][j] = A[i][j]
        aug[i][n + i] = 1.0

    for col in range(n):
        # Partial pivoting.
        max_row = col
        max_val = abs(aug[col][col])
        for row in range(col + 1, n):
            if abs(aug[row][col]) > max_val:
                max_val = abs(aug[row][col])
                max_row = row
        aug[col], aug[max_row] = aug[max_row], aug[col]

        pivot = aug[col][col]
        if abs(pivot) < 1e-14:
            raise ValueError("Singular matrix -- cannot invert.")
        for j in range(2 * n):
            aug[col][j] /= pivot
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            for j in range(2 * n):
                aug[row][j] -= factor * aug[col][j]

    inv = _mat_zeros(n, n)
    for i in range(n):
        for j in range(n):
            inv[i][j] = aug[i][n + j]
    return inv


def _least_squares(X: List[List[float]], y: List[float]) -> List[float]:
    """Ordinary least-squares: solve X @ beta = y  ->  beta = (XtX)^-1 Xt y.

    Parameters
    ----------
    X : list[list[float]]
        Design matrix, shape (n_samples, n_features).
    y : list[float]
        Response vector, length n_samples.

    Returns
    -------
    list[float]
        Coefficient vector *beta*.
    """
    Xt = _mat_transpose(X)
    XtX = _mat_mul(Xt, X)
    XtX_inv = _mat_inverse(XtX)
    Xty = _mat_vec_mul(Xt, y)
    beta = _mat_vec_mul(XtX_inv, Xty)
    return beta


# ============================================================================
# Nonlinear curve fitting -- simplified Levenberg-Marquardt
# ============================================================================

def _numerical_jacobian(
    func: Callable[[float, List[float]], float],
    x_data: List[float],
    params: List[float],
    eps: float = 1e-7,
) -> List[List[float]]:
    """Compute the Jacobian of *func* w.r.t. *params* at every point in *x_data*.

    Returns a matrix of shape (len(x_data), len(params)).
    """
    n = len(x_data)
    p = len(params)
    J = _mat_zeros(n, p)
    for j in range(p):
        params_up = list(params)
        params_down = list(params)
        h = max(abs(params[j]) * eps, eps)
        params_up[j] += h
        params_down[j] -= h
        for i in range(n):
            f_up = func(x_data[i], params_up)
            f_down = func(x_data[i], params_down)
            J[i][j] = (f_up - f_down) / (2.0 * h)
    return J


def _levenberg_marquardt(
    func: Callable[[float, List[float]], float],
    x_data: List[float],
    y_data: List[float],
    params0: List[float],
    max_iter: int = 200,
    tol: float = 1e-10,
    lambda_init: float = 1e-3,
    lambda_factor: float = 10.0,
) -> Tuple[List[float], float]:
    """Fit *func(x, params)* to *(x_data, y_data)* using Levenberg-Marquardt.

    Parameters
    ----------
    func : callable
        Model function with signature ``func(x, params) -> y``.
    x_data, y_data : lists of floats
        Observed data.
    params0 : list of float
        Initial parameter guess.
    max_iter : int
        Maximum number of iterations.
    tol : float
        Convergence tolerance on relative change of sum-of-squares.
    lambda_init : float
        Initial damping parameter.
    lambda_factor : float
        Factor to increase/decrease lambda.

    Returns
    -------
    (params, residual_ss) : (list[float], float)
        Best-fit parameters and residual sum of squares.
    """
    params = list(params0)
    n = len(x_data)
    p = len(params)
    lam = lambda_init

    def _residuals(par: List[float]) -> List[float]:
        return [y_data[i] - func(x_data[i], par) for i in range(n)]

    def _ss(residuals: List[float]) -> float:
        return sum(r * r for r in residuals)

    res = _residuals(params)
    ss = _ss(res)

    for _ in range(max_iter):
        J = _numerical_jacobian(func, x_data, params)
        Jt = _mat_transpose(J)
        JtJ = _mat_mul(Jt, J)

        # Damping: (JtJ + lambda * diag(JtJ)) delta = Jt * r
        diag_JtJ = _mat_zeros(p, p)
        for i in range(p):
            diag_JtJ[i][i] = JtJ[i][i] if abs(JtJ[i][i]) > 1e-14 else 1e-6

        A = _mat_add(JtJ, _mat_scale(diag_JtJ, lam))
        g = _mat_vec_mul(Jt, res)

        try:
            A_inv = _mat_inverse(A)
        except ValueError:
            lam *= lambda_factor
            continue

        delta = _mat_vec_mul(A_inv, g)

        new_params = [params[i] + delta[i] for i in range(p)]
        new_res = _residuals(new_params)
        new_ss = _ss(new_res)

        if new_ss < ss:
            # Accept step.
            relative_change = abs(ss - new_ss) / max(ss, 1e-14)
            params = new_params
            res = new_res
            ss = new_ss
            lam = max(lam / lambda_factor, 1e-12)
            if relative_change < tol:
                break
        else:
            lam *= lambda_factor
            if lam > 1e16:
                break

    return params, ss


# ============================================================================
# Curve model definitions
# ============================================================================

def _gompertz(x: float, params: List[float]) -> float:
    """Modified Gompertz growth curve.

    y = a * exp(-b * exp(-c * x))

    Parameters: [a, b, c]
        a -- asymptote (maximum score)
        b -- displacement along x
        c -- growth rate
    """
    a, b, c = params
    try:
        inner = -c * x
        inner = max(min(inner, 500.0), -500.0)
        outer = -b * math.exp(inner)
        outer = max(min(outer, 500.0), -500.0)
        return a * math.exp(outer)
    except (OverflowError, ValueError):
        return a


def _von_bertalanffy(x: float, params: List[float]) -> float:
    """Von Bertalanffy growth model.

    y = L_inf * (1 - exp(-k * (x - t0)))^3

    Parameters: [L_inf, k, t0]
        L_inf -- asymptotic maximum
        k     -- growth coefficient
        t0    -- theoretical age at zero size
    """
    L_inf, k, t0 = params
    try:
        exponent = -k * (x - t0)
        exponent = max(min(exponent, 500.0), -500.0)
        base = 1.0 - math.exp(exponent)
        if base < 0:
            return 0.0
        return L_inf * (base ** 3)
    except (OverflowError, ValueError):
        return L_inf


# ============================================================================
# GrowthCurveModel
# ============================================================================

class GrowthCurveModel:
    """Fits and predicts a single growth curve for one scoring axis.

    Tries multiple model families (Gompertz, Von Bertalanffy, polynomial),
    selects the best one by AIC, and uses it for predictions.

    Parameters
    ----------
    model_type : str or None
        Force a specific model (``"gompertz"``, ``"vonbert"``, ``"poly2"``,
        ``"poly3"``).  If ``None``, automatic selection is used.

    Attributes (set after ``fit``):
        best_model : str          -- name of the selected model
        params     : list[float]  -- fitted parameters
        residual_ss: float        -- residual sum of squares
        aic        : float        -- Akaike Information Criterion
        bic        : float        -- Bayesian Information Criterion
        rse        : float        -- residual standard error
    """

    # Map of model name -> (function, param_count)
    MODELS: Dict[str, Tuple[Callable, int]] = {
        "gompertz": (_gompertz, 3),
        "vonbert": (_von_bertalanffy, 3),
    }

    def __init__(self, model_type: Optional[str] = None) -> None:
        self.forced_model = model_type
        self.best_model: Optional[str] = None
        self.params: List[float] = []
        self.residual_ss: float = float("inf")
        self.aic: float = float("inf")
        self.bic: float = float("inf")
        self.rse: float = 0.0
        self._x_data: List[float] = []
        self._y_data: List[float] = []
        self._predict_func: Optional[Callable[[float], float]] = None

    # ------------------------------------------------------------------
    # Information criteria
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_aic(n: int, k: int, ss: float) -> float:
        """Akaike Information Criterion (AIC).

        AIC = n * ln(ss / n) + 2 * k
        where *n* = number of observations, *k* = number of parameters,
        *ss* = residual sum of squares.

        A near-zero *ss* indicates a near-perfect fit and yields a very
        negative (i.e. excellent) AIC.  Negative *ss* values (which should
        not occur) are treated as invalid.
        """
        if n <= 0:
            return float("inf")
        if ss < 0:
            return float("inf")
        # Floor ss to a tiny positive value to avoid log(0).
        ss = max(ss, 1e-300)
        return n * math.log(ss / n) + 2 * k

    @staticmethod
    def _compute_bic(n: int, k: int, ss: float) -> float:
        """Bayesian Information Criterion (BIC).

        BIC = n * ln(ss / n) + k * ln(n)
        """
        if n <= 0:
            return float("inf")
        if ss < 0:
            return float("inf")
        ss = max(ss, 1e-300)
        return n * math.log(ss / n) + k * math.log(n)

    # ------------------------------------------------------------------
    # Polynomial fitting helpers
    # ------------------------------------------------------------------

    def _fit_poly(self, x: List[float], y: List[float], degree: int) -> Tuple[List[float], float]:
        """Fit a polynomial of given *degree* by least squares.

        Returns (coefficients, residual_ss).
        Coefficients are in order [c0, c1, ..., cd] so that
        y = c0 + c1*x + c2*x^2 + ...
        """
        n = len(x)
        # Build design matrix.
        X = _mat_zeros(n, degree + 1)
        for i in range(n):
            for j in range(degree + 1):
                X[i][j] = x[i] ** j
        beta = _least_squares(X, y)
        # Compute residual SS.
        ss = 0.0
        for i in range(n):
            pred = sum(beta[j] * (x[i] ** j) for j in range(degree + 1))
            ss += (y[i] - pred) ** 2
        return beta, ss

    def _poly_predict(self, coeffs: List[float], x: float) -> float:
        """Evaluate a polynomial with coefficients *coeffs* at *x*."""
        return sum(c * (x ** j) for j, c in enumerate(coeffs))

    # ------------------------------------------------------------------
    # Initial parameter guesses
    # ------------------------------------------------------------------

    @staticmethod
    def _guess_gompertz(x: List[float], y: List[float]) -> List[float]:
        """Heuristic initial guess for Gompertz parameters [a, b, c]."""
        y_max = max(y) if y else 80.0
        a = y_max * 1.15  # asymptote slightly above max observed
        b = 3.0
        # Rough growth rate from data range.
        x_range = max(x) - min(x) if len(x) > 1 else 1.0
        c = 1.0 / max(x_range, 0.1)
        return [a, b, c]

    @staticmethod
    def _guess_vonbert(x: List[float], y: List[float]) -> List[float]:
        """Heuristic initial guess for Von Bertalanffy parameters [L_inf, k, t0]."""
        y_max = max(y) if y else 80.0
        L_inf = y_max * 1.2
        k = 0.5
        t0 = min(x) - 0.5 if x else -0.5
        return [L_inf, k, t0]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def fit(self, x_data: List[float], y_data: List[float]) -> "GrowthCurveModel":
        """Fit the model to observed data.

        Parameters
        ----------
        x_data : list[float]
            Ages (in years).
        y_data : list[float]
            Scores corresponding to each age.

        Returns
        -------
        GrowthCurveModel
            ``self`` (for chaining).

        Raises
        ------
        ValueError
            If fewer than ``MIN_POINTS_ANY`` data points are provided.
        """
        if len(x_data) < MIN_POINTS_ANY:
            raise ValueError(
                f"At least {MIN_POINTS_ANY} data points are required for fitting "
                f"(got {len(x_data)})."
            )
        if len(x_data) != len(y_data):
            raise ValueError("x_data and y_data must have the same length.")

        self._x_data = list(x_data)
        self._y_data = list(y_data)
        n = len(x_data)

        candidates: List[Tuple[str, List[float], float, Callable[[float], float]]] = []

        # --- Polynomial degree 2 ---
        try:
            coeffs2, ss2 = self._fit_poly(x_data, y_data, 2)
            candidates.append(("poly2", coeffs2, ss2, lambda x, c=coeffs2: self._poly_predict(c, x)))
        except (ValueError, ZeroDivisionError) as e:
            logging.getLogger(__name__).debug(
                "Poly2 model fit failed (non-fatal, trying others): %s", e
            )

        # --- Polynomial degree 3 (need >= 4 points) ---
        if n >= 4:
            try:
                coeffs3, ss3 = self._fit_poly(x_data, y_data, 3)
                candidates.append(("poly3", coeffs3, ss3, lambda x, c=coeffs3: self._poly_predict(c, x)))
            except (ValueError, ZeroDivisionError) as e:
                logging.getLogger(__name__).debug(
                    "Poly3 model fit failed (non-fatal, trying others): %s", e
                )

        # --- Nonlinear models (need >= MIN_POINTS_NONLINEAR) ---
        if n >= MIN_POINTS_NONLINEAR:
            # Gompertz
            if self.forced_model is None or self.forced_model == "gompertz":
                try:
                    guess_g = self._guess_gompertz(x_data, y_data)
                    params_g, ss_g = _levenberg_marquardt(_gompertz, x_data, y_data, guess_g)
                    candidates.append(("gompertz", params_g, ss_g, lambda x, p=params_g: _gompertz(x, p)))
                except Exception as e:
                    logging.getLogger(__name__).debug(f"Gompertz model fit failed (non-fatal, trying others): {e}")

            # Von Bertalanffy
            if self.forced_model is None or self.forced_model == "vonbert":
                try:
                    guess_v = self._guess_vonbert(x_data, y_data)
                    params_v, ss_v = _levenberg_marquardt(_von_bertalanffy, x_data, y_data, guess_v)
                    candidates.append(("vonbert", params_v, ss_v, lambda x, p=params_v: _von_bertalanffy(x, p)))
                except Exception as e:
                    logging.getLogger(__name__).debug(f"Von Bertalanffy model fit failed (non-fatal, trying others): {e}")

        # --- Select best by AIC (or forced model) ---
        if self.forced_model:
            candidates = [c for c in candidates if c[0] == self.forced_model]

        if not candidates:
            raise ValueError("Could not fit any model to the provided data.")

        best = None
        best_aic = float("inf")
        for name, params, ss, pred_fn in candidates:
            k = len(params)
            aic_val = self._compute_aic(n, k, ss)
            if aic_val < best_aic:
                best_aic = aic_val
                best = (name, params, ss, pred_fn)

        assert best is not None
        self.best_model = best[0]
        self.params = best[1]
        self.residual_ss = best[2]
        self._predict_func = best[3]

        k = len(self.params)
        self.aic = self._compute_aic(n, k, self.residual_ss)
        self.bic = self._compute_bic(n, k, self.residual_ss)

        # Residual standard error.
        dof = max(n - k, 1)
        self.rse = math.sqrt(self.residual_ss / dof)

        return self

    def predict(self, x: float) -> float:
        """Predict the score at age *x*.

        Raises ``RuntimeError`` if the model has not been fitted yet.
        """
        if self._predict_func is None:
            raise RuntimeError("Model has not been fitted. Call fit() first.")
        return self._predict_func(x)

    def predict_with_ci(
        self, x: float, confidence: float = 0.95
    ) -> Tuple[float, float, float]:
        """Predict with an approximate confidence interval.

        Uses a simple approach: prediction +/- z * RSE, where *z* is
        derived from the requested confidence level assuming a normal
        distribution.  This is an approximation suitable for showing
        directional uncertainty.

        Parameters
        ----------
        x : float
            Age at which to predict.
        confidence : float
            Confidence level (e.g. 0.95 for 95%).

        Returns
        -------
        (predicted, lower, upper) : tuple of floats
        """
        pred = self.predict(x)
        # Approximate z-value using the rational approximation of the
        # inverse normal CDF (Abramowitz & Stegun 26.2.23).
        alpha = 1.0 - confidence
        p = 1.0 - alpha / 2.0
        z = self._approx_z(p)
        margin = z * self.rse
        return pred, pred - margin, pred + margin

    @staticmethod
    def _approx_z(p: float) -> float:
        """Approximate the z-value for cumulative probability *p*.

        Uses the rational approximation from Abramowitz & Stegun (26.2.23).
        Accurate to about 4.5e-4 for 0.5 < p < 1.
        """
        if p <= 0.5:
            return -GrowthCurveModel._approx_z(1.0 - p)
        t = math.sqrt(-2.0 * math.log(1.0 - p))
        # Coefficients from A&S.
        c0, c1, c2 = 2.515517, 0.802853, 0.010328
        d1, d2, d3 = 1.432788, 0.189269, 0.001308
        z = t - (c0 + c1 * t + c2 * t * t) / (1.0 + d1 * t + d2 * t * t + d3 * t * t * t)
        return z

    def derivative(self, x: float, h: float = 0.01) -> float:
        """Numerical first derivative of the fitted curve at *x*.

        Uses central differences.
        """
        return (self.predict(x + h) - self.predict(x - h)) / (2.0 * h)

    def second_derivative(self, x: float, h: float = 0.01) -> float:
        """Numerical second derivative of the fitted curve at *x*."""
        return (self.predict(x + h) - 2.0 * self.predict(x) + self.predict(x - h)) / (h * h)


# ============================================================================
# GrowthPredictor -- per-dog, per-axis manager
# ============================================================================

class GrowthPredictor:
    """High-level growth prediction manager for a single dog.

    Maintains independent ``GrowthCurveModel`` instances for each scoring
    axis and provides aggregate predictions, growth-phase detection,
    anomaly detection, and trajectory generation.

    Parameters
    ----------
    breed : str
        Breed name used to look up breed-specific expectations.
        Falls back to ``"default"`` if the breed is not found.
    breed_expectations : dict, optional
        Override the default breed expectations dict.

    Example
    -------
    >>> history = [
    ...     (0.5, {"balance": 55, "coat": 50, "structure": 52, "gait": 48, "temperament": 60}),
    ...     (1.0, {"balance": 70, "coat": 65, "structure": 68, "gait": 64, "temperament": 73}),
    ...     (2.0, {"balance": 82, "coat": 78, "structure": 80, "gait": 77, "temperament": 84}),
    ...     (3.0, {"balance": 85, "coat": 82, "structure": 84, "gait": 81, "temperament": 87}),
    ... ]
    >>> gp = GrowthPredictor(breed="Labrador Retriever")
    >>> gp.fit(history)
    >>> gp.predict(target_age=4.0)
    {...}
    """

    def __init__(
        self,
        breed: str = "default",
        breed_expectations: Optional[Dict[str, Dict[str, float]]] = None,
    ) -> None:
        self.breed = breed
        expectations_db = breed_expectations or DEFAULT_BREED_EXPECTATIONS
        self.expectations: Dict[str, float] = expectations_db.get(
            breed, expectations_db.get("default", {})
        )
        self.models: Dict[str, GrowthCurveModel] = {}
        self._history: List[Tuple[float, Dict[str, float]]] = []
        self._fitted = False

    # ------------------------------------------------------------------
    # fit
    # ------------------------------------------------------------------

    def fit(
        self,
        history: List[Tuple[float, Dict[str, float]]],
        model_type: Optional[str] = None,
    ) -> "GrowthPredictor":
        """Fit growth models to historical analysis data.

        Parameters
        ----------
        history : list of (age_years, scores_dict)
            Each element is a tuple of the dog's age in years and a dict
            mapping axis names to numeric scores.  Must be sorted by age
            (the method will sort internally if not).
        model_type : str or None
            Force a specific model type for all axes.

        Returns
        -------
        GrowthPredictor
            ``self`` (for chaining).

        Raises
        ------
        ValueError
            If not enough data points are supplied.
        """
        if len(history) < MIN_POINTS_ANY:
            raise ValueError(
                f"Need at least {MIN_POINTS_ANY} historical analyses, got {len(history)}."
            )

        # Sort by age.
        self._history = sorted(history, key=lambda h: h[0])

        ages = [h[0] for h in self._history]

        for axis in AXES:
            scores = [h[1].get(axis, 0.0) for h in self._history]
            model = GrowthCurveModel(model_type=model_type)
            try:
                model.fit(ages, scores)
            except ValueError as e:
                # If a specific model fails, try automatic.
                logging.getLogger(__name__).debug(
                    "Model %s failed for axis '%s', falling back to auto: %s",
                    model_type, axis, e,
                )
                model = GrowthCurveModel(model_type=None)
                model.fit(ages, scores)
            self.models[axis] = model

        self._fitted = True
        return self

    # ------------------------------------------------------------------
    # predict
    # ------------------------------------------------------------------

    def predict(
        self,
        target_age: float,
        confidence: float = 0.95,
    ) -> Dict[str, Any]:
        """Predict scores at *target_age* for all axes.

        Parameters
        ----------
        target_age : float
            Age in years to predict.
        confidence : float
            Confidence level for intervals.

        Returns
        -------
        dict
            Keys: ``"age"``, ``"scores"`` (dict axis->predicted), ``"ci_lower"``,
            ``"ci_upper"``, ``"model_info"`` (per-axis model name).
        """
        self._check_fitted()
        scores: Dict[str, float] = {}
        ci_lower: Dict[str, float] = {}
        ci_upper: Dict[str, float] = {}
        model_info: Dict[str, str] = {}

        for axis in AXES:
            model = self.models[axis]
            pred, lo, hi = model.predict_with_ci(target_age, confidence)
            scores[axis] = round(pred, 2)
            ci_lower[axis] = round(lo, 2)
            ci_upper[axis] = round(hi, 2)
            model_info[axis] = model.best_model or "unknown"

        overall = round(sum(scores.values()) / len(scores), 2)
        return {
            "age": target_age,
            "scores": scores,
            "overall": overall,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "model_info": model_info,
        }

    # ------------------------------------------------------------------
    # predict_peak_age
    # ------------------------------------------------------------------

    def predict_peak_age(
        self,
        search_range: Optional[Tuple[float, float]] = None,
        step: float = 0.1,
    ) -> Dict[str, Any]:
        """Estimate the age at which the dog will achieve its peak overall score.

        Searches over *search_range* in increments of *step*.  If no range
        is provided, the method uses a breed-aware heuristic: from the
        earliest observed age to 1.5x the breed's expected senior onset
        (or 10.0 years as a fallback).

        For monotonic models (Gompertz, Von Bertalanffy) that never decline,
        the method also considers the derivative: if the curve is still
        rising at the end of the search range but has flattened to near-zero
        slope (< 0.5 score-units/year), it reports the age where the slope
        first dropped below that threshold as the practical peak.

        Returns
        -------
        dict
            ``"peak_age"``, ``"peak_overall"``, ``"per_axis_peak_ages"``.
        """
        self._check_fitted()

        # Determine search bounds.
        if search_range is None:
            min_age = min(h[0] for h in self._history) if self._history else 0.5
            senior_onset = self.expectations.get("senior_onset", 7.0)
            max_age = senior_onset * 1.5
            search_range = (min_age, max_age)

        best_age = search_range[0]
        best_overall = -float("inf")

        per_axis_peaks: Dict[str, Dict[str, float]] = {}
        for axis in AXES:
            per_axis_peaks[axis] = {"age": search_range[0], "score": -float("inf")}

        age = search_range[0]
        while age <= search_range[1]:
            total = 0.0
            for axis in AXES:
                s = self.models[axis].predict(age)
                total += s
                if s > per_axis_peaks[axis]["score"]:
                    per_axis_peaks[axis] = {"age": round(age, 2), "score": round(s, 2)}
            overall = total / len(AXES)
            if overall > best_overall:
                best_overall = overall
                best_age = age
            age += step

        # For monotonic models whose peak is at the edge of the search
        # range, find the "practical peak" -- the age where the average
        # derivative drops below a small threshold (the curve has
        # effectively plateaued).
        if abs(best_age - search_range[1]) < step * 1.5:
            practical_peak_age = search_range[0]
            plateau_threshold = 0.5  # score-units per year
            age = search_range[0]
            while age <= search_range[1]:
                avg_deriv = sum(
                    self.models[axis].derivative(age) for axis in AXES
                ) / len(AXES)
                if avg_deriv < plateau_threshold:
                    practical_peak_age = age
                    break
                age += step
            else:
                # Never plateaued; report the breed's expected adult peak end.
                practical_peak_age = self.expectations.get("adult_peak_end", best_age)

            if practical_peak_age < best_age:
                best_age = practical_peak_age
                total = sum(self.models[axis].predict(best_age) for axis in AXES)
                best_overall = total / len(AXES)

        return {
            "peak_age": round(best_age, 2),
            "peak_overall": round(best_overall, 2),
            "per_axis_peak_ages": per_axis_peaks,
        }

    # ------------------------------------------------------------------
    # get_growth_phase
    # ------------------------------------------------------------------

    def get_growth_phase(self, age: float) -> Dict[str, str]:
        """Detect the growth phase at a given *age* for each axis.

        Growth phases:
            - ``"rapid_growth"`` -- first derivative > 5 and second derivative >= 0
            - ``"plateau"``      -- |first derivative| <= 5
            - ``"peak"``         -- first derivative near zero and second derivative < 0
            - ``"decline"``      -- first derivative < -5

        The thresholds are absolute score-units per year.

        Returns
        -------
        dict
            Mapping axis name -> phase string.
        """
        self._check_fitted()
        phases: Dict[str, str] = {}

        for axis in AXES:
            model = self.models[axis]
            d1 = model.derivative(age)
            d2 = model.second_derivative(age)

            if d1 > 5.0:
                phases[axis] = "rapid_growth"
            elif d1 < -5.0:
                phases[axis] = "decline"
            elif abs(d1) <= 5.0 and d2 < -1.0:
                phases[axis] = "peak"
            else:
                phases[axis] = "plateau"

        return phases

    # ------------------------------------------------------------------
    # detect_anomalies
    # ------------------------------------------------------------------

    def detect_anomalies(self) -> List[Dict[str, Any]]:
        """Flag unusually large score changes between consecutive analyses.

        A change is flagged as anomalous if its magnitude exceeds
        ``ANOMALY_SD_THRESHOLD`` standard deviations of the observed
        inter-analysis changes for that axis.

        Returns
        -------
        list of dict
            Each dict: ``{"axis", "from_age", "to_age", "change", "mean_change",
            "sd_change", "z_score"}``.
        """
        self._check_fitted()
        anomalies: List[Dict[str, Any]] = []

        if len(self._history) < 3:
            return anomalies

        for axis in AXES:
            changes: List[float] = []
            for i in range(1, len(self._history)):
                prev_score = self._history[i - 1][1].get(axis, 0.0)
                curr_score = self._history[i][1].get(axis, 0.0)
                changes.append(curr_score - prev_score)

            if len(changes) < 2:
                continue

            mean_c = statistics.mean(changes)
            sd_c = statistics.stdev(changes)

            if sd_c < 1e-9:
                continue

            for i, change in enumerate(changes):
                z = abs(change - mean_c) / sd_c
                if z > ANOMALY_SD_THRESHOLD:
                    anomalies.append({
                        "axis": axis,
                        "from_age": self._history[i][0],
                        "to_age": self._history[i + 1][0],
                        "change": round(change, 2),
                        "mean_change": round(mean_c, 2),
                        "sd_change": round(sd_c, 2),
                        "z_score": round(z, 2),
                    })

        return anomalies

    # ------------------------------------------------------------------
    # get_trajectory
    # ------------------------------------------------------------------

    def get_trajectory(
        self,
        age_range: Tuple[float, float] = (0.5, 8.0),
        step: float = 0.25,
        confidence: float = 0.95,
    ) -> List[Dict[str, Any]]:
        """Generate a predicted trajectory over an age range.

        Parameters
        ----------
        age_range : (float, float)
            Start and end ages.
        step : float
            Increment between prediction points.
        confidence : float
            Confidence level for intervals.

        Returns
        -------
        list of dict
            Each element is the output of ``predict()`` at that age,
            augmented with ``"phase"`` information.
        """
        self._check_fitted()
        trajectory: List[Dict[str, Any]] = []

        age = age_range[0]
        while age <= age_range[1] + 1e-9:
            point = self.predict(target_age=age, confidence=confidence)
            point["phase"] = self.get_growth_phase(age)
            trajectory.append(point)
            age += step

        return trajectory

    # ------------------------------------------------------------------
    # Breed expectation helpers
    # ------------------------------------------------------------------

    def get_breed_expectations(self) -> Dict[str, float]:
        """Return breed-specific age expectations.

        Returns
        -------
        dict
            ``"puppy_peak_age"``, ``"adult_peak_start"``,
            ``"adult_peak_end"``, ``"senior_onset"``.
        """
        return dict(self.expectations)

    def compare_to_expectations(self, age: float) -> Dict[str, Any]:
        """Compare a dog's predicted scores to breed-typical expectations.

        Provides a simple categorical label for the dog's current stage
        relative to the breed standard.

        Returns
        -------
        dict
            ``"life_stage"`` (puppy / adult_rising / adult_peak / senior),
            ``"predicted_scores"``, ``"breed_expectations"``.
        """
        self._check_fitted()
        exp = self.expectations
        if age < exp.get("puppy_peak_age", 1.5):
            stage = "puppy"
        elif age < exp.get("adult_peak_start", 2.0):
            stage = "adult_rising"
        elif age <= exp.get("adult_peak_end", 5.0):
            stage = "adult_peak"
        else:
            stage = "senior"

        return {
            "life_stage": stage,
            "predicted_scores": self.predict(age)["scores"],
            "breed_expectations": self.get_breed_expectations(),
        }

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def summary(self) -> Dict[str, Any]:
        """Return a comprehensive summary of the fitted models and predictions.

        Returns
        -------
        dict
            ``"breed"``, ``"n_observations"``, ``"age_range"``,
            ``"per_axis_models"``, ``"peak_prediction"``,
            ``"anomalies"``.
        """
        self._check_fitted()
        ages = [h[0] for h in self._history]

        per_axis: Dict[str, Dict[str, Any]] = {}
        for axis in AXES:
            m = self.models[axis]
            per_axis[axis] = {
                "model": m.best_model,
                "aic": round(m.aic, 2),
                "bic": round(m.bic, 2),
                "rse": round(m.rse, 2),
                "params": [round(p, 6) for p in m.params],
            }

        return {
            "breed": self.breed,
            "n_observations": len(self._history),
            "age_range": (round(min(ages), 2), round(max(ages), 2)),
            "per_axis_models": per_axis,
            "peak_prediction": self.predict_peak_age(),
            "anomalies": self.detect_anomalies(),
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _check_fitted(self) -> None:
        if not self._fitted:
            raise RuntimeError(
                "GrowthPredictor has not been fitted. Call fit() first."
            )


# ============================================================================
# Self-test
# ============================================================================

def _self_test() -> None:
    """Run internal self-tests to verify correctness of the module.

    Tests matrix helpers, curve fitting, prediction, anomaly detection,
    and trajectory generation.  Prints results to stdout.  Raises
    ``AssertionError`` on failure.
    """
    print("=" * 70)
    print("growth_prediction.py -- self-test")
    print("=" * 70)

    # ------------------------------------------------------------------
    # 1. Matrix helpers
    # ------------------------------------------------------------------
    print("\n[1] Matrix helpers...")

    # Identity inverse should be identity.
    I3 = _mat_identity(3)
    I3_inv = _mat_inverse(I3)
    for i in range(3):
        for j in range(3):
            expected = 1.0 if i == j else 0.0
            assert abs(I3_inv[i][j] - expected) < 1e-10, f"Identity inverse failed at ({i},{j})"

    # 2x2 inverse.
    A = [[4.0, 7.0], [2.0, 6.0]]
    A_inv = _mat_inverse(A)
    product = _mat_mul(A, A_inv)
    for i in range(2):
        for j in range(2):
            expected = 1.0 if i == j else 0.0
            assert abs(product[i][j] - expected) < 1e-10, f"2x2 inverse failed at ({i},{j})"

    # Transpose.
    B = [[1, 2, 3], [4, 5, 6]]
    Bt = _mat_transpose(B)
    assert len(Bt) == 3 and len(Bt[0]) == 2
    assert Bt[0][0] == 1 and Bt[2][1] == 6

    print("  Matrix helpers: PASSED")

    # ------------------------------------------------------------------
    # 2. Least squares (polynomial fit to known data)
    # ------------------------------------------------------------------
    print("\n[2] Least-squares polynomial fit...")

    # y = 3 + 2x  (linear)
    x_ls = [0.0, 1.0, 2.0, 3.0, 4.0]
    y_ls = [3.0, 5.0, 7.0, 9.0, 11.0]
    X_ls = [[1.0, xi] for xi in x_ls]
    beta = _least_squares(X_ls, y_ls)
    assert abs(beta[0] - 3.0) < 1e-8, f"Intercept wrong: {beta[0]}"
    assert abs(beta[1] - 2.0) < 1e-8, f"Slope wrong: {beta[1]}"

    print("  Least squares: PASSED")

    # ------------------------------------------------------------------
    # 3. GrowthCurveModel -- polynomial
    # ------------------------------------------------------------------
    print("\n[3] GrowthCurveModel (polynomial)...")

    # Quadratic: y = 10 + 20x - 2x^2
    x_poly = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]
    y_poly = [10 + 20 * x - 2 * x * x for x in x_poly]

    gcm_poly = GrowthCurveModel(model_type="poly2")
    gcm_poly.fit(x_poly, y_poly)
    assert gcm_poly.best_model == "poly2"
    pred_3 = gcm_poly.predict(3.0)
    expected_3 = 10 + 20 * 3.0 - 2 * 9.0  # = 52
    assert abs(pred_3 - expected_3) < 0.5, f"Poly2 prediction off: {pred_3} vs {expected_3}"

    # Confidence interval.
    pred_val, lo, hi = gcm_poly.predict_with_ci(3.0, 0.95)
    assert lo <= pred_val <= hi, "CI bounds incorrect"

    print(f"  Poly2 model: PASSED (predicted {pred_3:.2f}, expected {expected_3:.2f})")

    # ------------------------------------------------------------------
    # 4. GrowthCurveModel -- Gompertz
    # ------------------------------------------------------------------
    print("\n[4] GrowthCurveModel (Gompertz)...")

    # Generate data from a known Gompertz curve: y = 90 * exp(-3 * exp(-0.8 * x))
    true_a, true_b, true_c = 90.0, 3.0, 0.8
    x_gomp = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0]
    y_gomp = [_gompertz(x, [true_a, true_b, true_c]) for x in x_gomp]

    gcm_gomp = GrowthCurveModel(model_type="gompertz")
    gcm_gomp.fit(x_gomp, y_gomp)
    assert gcm_gomp.best_model == "gompertz"

    # Check prediction at x = 4.0 is close to true value.
    pred_g4 = gcm_gomp.predict(4.0)
    true_g4 = _gompertz(4.0, [true_a, true_b, true_c])
    assert abs(pred_g4 - true_g4) < 2.0, (
        f"Gompertz prediction off: {pred_g4:.2f} vs {true_g4:.2f}"
    )

    print(f"  Gompertz model: PASSED (predicted {pred_g4:.2f}, true {true_g4:.2f})")

    # ------------------------------------------------------------------
    # 5. GrowthCurveModel -- Von Bertalanffy
    # ------------------------------------------------------------------
    print("\n[5] GrowthCurveModel (Von Bertalanffy)...")

    true_L, true_k, true_t0 = 95.0, 0.6, -0.5
    x_vb = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    y_vb = [_von_bertalanffy(x, [true_L, true_k, true_t0]) for x in x_vb]

    gcm_vb = GrowthCurveModel(model_type="vonbert")
    gcm_vb.fit(x_vb, y_vb)
    assert gcm_vb.best_model == "vonbert"

    pred_v5 = gcm_vb.predict(5.0)
    true_v5 = _von_bertalanffy(5.0, [true_L, true_k, true_t0])
    assert abs(pred_v5 - true_v5) < 3.0, (
        f"VonBert prediction off: {pred_v5:.2f} vs {true_v5:.2f}"
    )

    print(f"  Von Bertalanffy model: PASSED (predicted {pred_v5:.2f}, true {true_v5:.2f})")

    # ------------------------------------------------------------------
    # 6. GrowthCurveModel -- auto model selection
    # ------------------------------------------------------------------
    print("\n[6] Automatic model selection...")

    gcm_auto = GrowthCurveModel()
    gcm_auto.fit(x_gomp, y_gomp)
    print(f"  Auto-selected model: {gcm_auto.best_model} (AIC={gcm_auto.aic:.2f})")
    assert gcm_auto.best_model is not None, "No model selected"

    # ------------------------------------------------------------------
    # 7. GrowthPredictor -- full workflow
    # ------------------------------------------------------------------
    print("\n[7] GrowthPredictor -- full workflow...")

    history = [
        (0.5, {"balance": 45, "coat": 42, "structure": 44, "gait": 40, "temperament": 50}),
        (1.0, {"balance": 62, "coat": 58, "structure": 60, "gait": 55, "temperament": 66}),
        (1.5, {"balance": 73, "coat": 69, "structure": 72, "gait": 67, "temperament": 76}),
        (2.0, {"balance": 80, "coat": 76, "structure": 79, "gait": 75, "temperament": 83}),
        (3.0, {"balance": 85, "coat": 82, "structure": 84, "gait": 81, "temperament": 87}),
        (4.0, {"balance": 87, "coat": 84, "structure": 86, "gait": 83, "temperament": 88}),
        (5.0, {"balance": 86, "coat": 83, "structure": 85, "gait": 82, "temperament": 87}),
        (6.0, {"balance": 84, "coat": 80, "structure": 82, "gait": 79, "temperament": 85}),
    ]

    gp = GrowthPredictor(breed="Labrador Retriever")
    gp.fit(history)

    # predict
    result = gp.predict(target_age=3.5)
    assert "scores" in result
    assert "ci_lower" in result
    assert "ci_upper" in result
    assert all(axis in result["scores"] for axis in AXES)
    print(f"  Prediction at 3.5yr: overall={result['overall']}, scores={result['scores']}")

    # predict_peak_age
    peak = gp.predict_peak_age()
    assert "peak_age" in peak
    assert 2.0 <= peak["peak_age"] <= 10.0, f"Peak age out of expected range: {peak['peak_age']}"
    print(f"  Predicted peak age: {peak['peak_age']}yr (overall={peak['peak_overall']})")

    # get_growth_phase
    phase_1 = gp.get_growth_phase(age=0.8)
    phase_4 = gp.get_growth_phase(age=4.0)
    print(f"  Phase at 0.8yr: {phase_1}")
    print(f"  Phase at 4.0yr: {phase_4}")
    assert all(v in ("rapid_growth", "plateau", "peak", "decline") for v in phase_1.values())
    assert all(v in ("rapid_growth", "plateau", "peak", "decline") for v in phase_4.values())

    # detect_anomalies
    anomalies = gp.detect_anomalies()
    print(f"  Anomalies detected: {len(anomalies)}")

    # get_trajectory
    traj = gp.get_trajectory(age_range=(0.5, 6.0), step=0.5)
    assert len(traj) > 0
    assert "phase" in traj[0]
    print(f"  Trajectory points: {len(traj)}")

    # breed expectations
    expectations = gp.get_breed_expectations()
    assert "puppy_peak_age" in expectations
    print(f"  Breed expectations: {expectations}")

    # compare_to_expectations
    comp = gp.compare_to_expectations(age=3.0)
    assert comp["life_stage"] == "adult_peak"
    print(f"  Life stage at 3.0yr: {comp['life_stage']}")

    # summary
    s = gp.summary()
    assert "per_axis_models" in s
    assert "peak_prediction" in s
    print(f"  Summary breed: {s['breed']}, observations: {s['n_observations']}")

    # ------------------------------------------------------------------
    # 8. Anomaly detection with injected anomaly
    # ------------------------------------------------------------------
    print("\n[8] Anomaly detection with injected anomaly...")

    # Use many data points with consistent small changes, then one large anomaly.
    # Coat changes: +5, +5, +5, +5, +5, -35, +5 -- the -35 stands out at > 2 SD.
    history_anom = [
        (0.5, {"balance": 45, "coat": 42, "structure": 44, "gait": 40, "temperament": 50}),
        (1.0, {"balance": 50, "coat": 47, "structure": 49, "gait": 45, "temperament": 55}),
        (1.5, {"balance": 55, "coat": 52, "structure": 54, "gait": 50, "temperament": 60}),
        (2.0, {"balance": 60, "coat": 57, "structure": 59, "gait": 55, "temperament": 65}),
        (2.5, {"balance": 65, "coat": 62, "structure": 64, "gait": 60, "temperament": 70}),
        (3.0, {"balance": 70, "coat": 67, "structure": 69, "gait": 65, "temperament": 75}),
        # Injected anomaly: coat drops dramatically while others continue
        (3.5, {"balance": 75, "coat": 32, "structure": 74, "gait": 70, "temperament": 80}),
        (4.0, {"balance": 80, "coat": 37, "structure": 79, "gait": 75, "temperament": 85}),
    ]

    gp_anom = GrowthPredictor(breed="Labrador Retriever")
    gp_anom.fit(history_anom)
    anomalies_found = gp_anom.detect_anomalies()
    coat_anomalies = [a for a in anomalies_found if a["axis"] == "coat"]
    assert len(coat_anomalies) > 0, "Expected to detect coat anomaly"
    print(f"  Coat anomalies found: {len(coat_anomalies)}")
    for a in coat_anomalies:
        print(f"    age {a['from_age']}->{a['to_age']}: change={a['change']}, z={a['z_score']}")

    # ------------------------------------------------------------------
    # 9. Edge cases
    # ------------------------------------------------------------------
    print("\n[9] Edge cases...")

    # Too few data points.
    try:
        GrowthPredictor().fit([
            (1.0, {"balance": 50, "coat": 50, "structure": 50, "gait": 50, "temperament": 50}),
        ])
        raise AssertionError("Should have raised ValueError")
    except ValueError as e:
        print(f"  Too few points: correctly raised ValueError: {e}")

    # Predict before fit.
    try:
        GrowthPredictor().predict(target_age=3.0)
        raise AssertionError("Should have raised RuntimeError")
    except RuntimeError as e:
        print(f"  Predict before fit: correctly raised RuntimeError: {e}")

    # Derivative computation.
    print("\n[10] Derivative computation...")
    model_d = GrowthCurveModel(model_type="poly2")
    x_d = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    y_d = [x * x for x in x_d]  # y = x^2, dy/dx = 2x
    model_d.fit(x_d, y_d)
    d_at_3 = model_d.derivative(3.0)
    assert abs(d_at_3 - 6.0) < 0.5, f"Derivative at x=3 should be ~6.0, got {d_at_3:.2f}"
    print(f"  Derivative of x^2 at x=3: {d_at_3:.2f} (expected ~6.0)")

    # Second derivative should be ~2.0.
    d2_at_3 = model_d.second_derivative(3.0)
    assert abs(d2_at_3 - 2.0) < 0.5, f"Second derivative should be ~2.0, got {d2_at_3:.2f}"
    print(f"  Second derivative of x^2 at x=3: {d2_at_3:.2f} (expected ~2.0)")

    # ------------------------------------------------------------------
    # 11. AIC / BIC sanity
    # ------------------------------------------------------------------
    print("\n[11] AIC / BIC sanity...")
    aic_val = GrowthCurveModel._compute_aic(n=20, k=3, ss=10.0)
    bic_val = GrowthCurveModel._compute_bic(n=20, k=3, ss=10.0)
    assert True  # Just check they're finite.
    assert math.isfinite(aic_val), "AIC should be finite"
    assert math.isfinite(bic_val), "BIC should be finite"
    print(f"  AIC(n=20, k=3, ss=10) = {aic_val:.4f}")
    print(f"  BIC(n=20, k=3, ss=10) = {bic_val:.4f}")

    # ------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("All self-tests PASSED.")
    print("=" * 70)


if __name__ == "__main__":
    _self_test()
