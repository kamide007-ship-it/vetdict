"""
Genetic Score Estimation and Breeding Optimization System.

This module provides tools for pedigree analysis, inbreeding coefficient
calculation (Wright's COI), Expected Progeny Difference (EPD) estimation,
breeding pair compatibility scoring, and population genetics metrics.

All computations use only the Python standard library.

Classes:
    Dog: Data container for an individual dog's genetic and scoring info.
    PedigreeTree: Manages pedigree data and computes Wright's COI.
    GeneticScorer: Computes EPD values and per-axis breeding scores.
    BreedingOptimizer: Ranks candidate mates and provides recommendations.

Usage:
    from api.genetic_scoring import Dog, PedigreeTree, GeneticScorer, BreedingOptimizer
"""

import math
from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCORING_AXES = ("skeletal", "gait", "muscle", "coat", "temperament")

HERITABILITY_ESTIMATES: Dict[str, float] = {
    "skeletal": 0.45,
    "gait": 0.35,
    "muscle": 0.40,
    "coat": 0.55,
    "temperament": 0.25,
}

MAX_GENERATIONS = 10

# Common health-test genes mapped to popular breeds.
# Each entry: gene_name -> {"mode": "autosomal_recessive"|"autosomal_dominant",
#                            "breeds": [breed_ids]}
COMMON_HEALTH_GENES: Dict[str, Dict] = {
    "vWD1": {
        "mode": "autosomal_recessive",
        "description": "von Willebrand Disease Type 1",
        "breeds": [],  # applicable to many breeds
    },
    "PRA_prcd": {
        "mode": "autosomal_recessive",
        "description": "Progressive Retinal Atrophy (prcd)",
        "breeds": [],
    },
    "DM": {
        "mode": "autosomal_recessive",
        "description": "Degenerative Myelopathy",
        "breeds": [],
    },
    "EIC": {
        "mode": "autosomal_recessive",
        "description": "Exercise-Induced Collapse",
        "breeds": [],
    },
    "MDR1": {
        "mode": "autosomal_recessive",
        "description": "Multi-Drug Resistance 1",
        "breeds": [],
    },
    "HUU": {
        "mode": "autosomal_recessive",
        "description": "Hyperuricosuria",
        "breeds": [],
    },
    "DCM": {
        "mode": "autosomal_dominant",
        "description": "Dilated Cardiomyopathy (some forms)",
        "breeds": [],
    },
    "CEA": {
        "mode": "autosomal_recessive",
        "description": "Collie Eye Anomaly",
        "breeds": [],
    },
}

# Basic color genetics alleles (simplified Mendelian model).
# Loci: E (extension), B (brown), D (dilute), K (dominant black)
COLOR_LOCI = ("E", "B", "D", "K")


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------


class Dog:
    """Represents a single dog with pedigree and genetic information.

    Attributes:
        id: Unique identifier for this dog.
        name: Registered / call name.
        breed_id: Identifier for the breed (foreign key).
        sire_id: Father's dog id, or None if unknown.
        dam_id: Mother's dog id, or None if unknown.
        scores: Dict mapping each scoring axis to a numeric score (0-10).
        health_tests: List of dicts, each containing:
            - gene: str (e.g. "vWD1")
            - result: str ("clear", "carrier", "affected")
        color_genetics: Dict mapping locus name to a 2-tuple of alleles,
            e.g. {"E": ("E", "e"), "B": ("B", "B")}
    """

    __slots__ = (
        "id",
        "name",
        "breed_id",
        "sire_id",
        "dam_id",
        "scores",
        "health_tests",
        "color_genetics",
    )

    def __init__(
        self,
        dog_id: int,
        name: str,
        breed_id: int,
        sire_id: Optional[int] = None,
        dam_id: Optional[int] = None,
        scores: Optional[Dict[str, float]] = None,
        health_tests: Optional[List[Dict[str, str]]] = None,
        color_genetics: Optional[Dict[str, Tuple[str, str]]] = None,
    ) -> None:
        self.id = dog_id
        self.name = name
        self.breed_id = breed_id
        self.sire_id = sire_id
        self.dam_id = dam_id
        self.scores = scores or {}
        self.health_tests = health_tests or []
        self.color_genetics = color_genetics or {}

    def __repr__(self) -> str:
        return f"Dog(id={self.id}, name={self.name!r}, breed_id={self.breed_id})"

    def health_status(self, gene: str) -> Optional[str]:
        """Return the test result for *gene*, or None if untested.

        Args:
            gene: The gene identifier (e.g. "vWD1").

        Returns:
            "clear", "carrier", "affected", or None.
        """
        for test in self.health_tests:
            if test.get("gene") == gene:
                return test.get("result")
        return None


# ---------------------------------------------------------------------------
# Pedigree Tree
# ---------------------------------------------------------------------------


class PedigreeTree:
    """Manages a collection of dogs and provides pedigree analysis.

    The tree supports Wright's path-coefficient method for computing the
    Coefficient of Inbreeding (COI) up to a configurable number of
    generations (default 10).

    Pedigree traversal results are memoized for performance.

    Usage:
        tree = PedigreeTree()
        tree.add_dog(Dog(1, "Alpha", breed_id=1, sire_id=2, dam_id=3))
        tree.add_dog(Dog(2, "Bravo", breed_id=1))
        tree.add_dog(Dog(3, "Charlie", breed_id=1))
        coi = tree.coi(1)
    """

    def __init__(self, max_generations: int = MAX_GENERATIONS) -> None:
        self._dogs: Dict[int, Dog] = {}
        self._max_gen = max_generations
        # Memoization caches
        self._ancestor_paths_cache: Dict[int, Dict[int, List[List[int]]]] = {}
        self._coi_cache: Dict[Tuple[int, int], float] = {}

    # -- Dog management -----------------------------------------------------

    def add_dog(self, dog: Dog) -> None:
        """Add a dog to the pedigree tree, clearing affected caches."""
        self._dogs[dog.id] = dog
        self._ancestor_paths_cache.clear()
        self._coi_cache.clear()

    def add_dogs(self, dogs: List[Dog]) -> None:
        """Add multiple dogs in bulk."""
        for dog in dogs:
            self._dogs[dog.id] = dog
        self._ancestor_paths_cache.clear()
        self._coi_cache.clear()

    def get_dog(self, dog_id: int) -> Optional[Dog]:
        """Retrieve a dog by id, or None if not present."""
        return self._dogs.get(dog_id)

    @property
    def all_dogs(self) -> List[Dog]:
        """Return a list of all dogs in the tree."""
        return list(self._dogs.values())

    def dogs_by_breed(self, breed_id: int) -> List[Dog]:
        """Return all dogs belonging to a specific breed."""
        return [d for d in self._dogs.values() if d.breed_id == breed_id]

    # -- Ancestor / path utilities ------------------------------------------

    def ancestors(self, dog_id: int, max_gen: Optional[int] = None) -> Set[int]:
        """Return the set of ancestor ids reachable within *max_gen* generations.

        Args:
            dog_id: The id of the dog whose ancestors to find.
            max_gen: Maximum number of generations to traverse.
                     Defaults to self._max_gen.

        Returns:
            A set of ancestor dog ids (not including the dog itself).
        """
        if max_gen is None:
            max_gen = self._max_gen
        result: Set[int] = set()
        self._collect_ancestors(dog_id, max_gen, 0, result)
        return result

    def _collect_ancestors(
        self, dog_id: int, max_gen: int, current_gen: int, acc: Set[int]
    ) -> None:
        if current_gen >= max_gen:
            return
        dog = self._dogs.get(dog_id)
        if dog is None:
            return
        for parent_id in (dog.sire_id, dog.dam_id):
            if parent_id is not None and parent_id in self._dogs:
                acc.add(parent_id)
                self._collect_ancestors(parent_id, max_gen, current_gen + 1, acc)

    def _all_paths_to_ancestor(
        self, dog_id: int, ancestor_id: int, max_gen: int
    ) -> List[List[int]]:
        """Find every path from *dog_id* up to *ancestor_id* within *max_gen*.

        Each path is a list of dog ids from dog_id (exclusive) to
        ancestor_id (inclusive).

        Returns:
            A list of paths (each path is a list of int ids).
        """
        results: List[List[int]] = []
        self._dfs_paths(dog_id, ancestor_id, max_gen, [], results)
        return results

    def _dfs_paths(
        self,
        current_id: int,
        target_id: int,
        remaining: int,
        path: List[int],
        results: List[List[int]],
    ) -> None:
        if remaining <= 0:
            return
        dog = self._dogs.get(current_id)
        if dog is None:
            return
        for parent_id in (dog.sire_id, dog.dam_id):
            if parent_id is None or parent_id not in self._dogs:
                continue
            new_path = path + [parent_id]
            if parent_id == target_id:
                results.append(new_path)
            # Keep searching further even if we found the target, because
            # the ancestor could appear at multiple depths.
            self._dfs_paths(parent_id, target_id, remaining - 1, new_path, results)

    # -- Wright's COI -------------------------------------------------------

    def coi(self, dog_id: int, max_gen: Optional[int] = None) -> float:
        """Compute Wright's Coefficient of Inbreeding for *dog_id*.

        Uses the path-coefficient method:
            COI = sum over each common ancestor A of
                  sum over each (sire_path, dam_path) pair through A of
                  (1/2)^(n1 + n2 + 1) * (1 + F_A)

        where n1 = length of path from sire to A, n2 = length of path from
        dam to A, and F_A = COI of ancestor A itself.

        Args:
            dog_id: The dog to compute COI for.
            max_gen: Maximum generations to traverse (default self._max_gen).

        Returns:
            COI as a float in [0.0, 1.0].
        """
        if max_gen is None:
            max_gen = self._max_gen

        cache_key = (dog_id, max_gen)
        if cache_key in self._coi_cache:
            return self._coi_cache[cache_key]

        dog = self._dogs.get(dog_id)
        if dog is None or dog.sire_id is None or dog.dam_id is None:
            self._coi_cache[cache_key] = 0.0
            return 0.0

        sire_id = dog.sire_id
        dam_id = dog.dam_id

        # Collect all ancestors reachable through sire and dam separately.
        sire_ancestors = self.ancestors(sire_id, max_gen - 1)
        sire_ancestors.add(sire_id)
        dam_ancestors = self.ancestors(dam_id, max_gen - 1)
        dam_ancestors.add(dam_id)

        common_ancestors = sire_ancestors & dam_ancestors

        if not common_ancestors:
            self._coi_cache[cache_key] = 0.0
            return 0.0

        total_coi = 0.0

        for anc_id in common_ancestors:
            # Paths from sire to ancestor
            sire_paths = self._all_paths_to_ancestor(sire_id, anc_id, max_gen - 1)
            # Paths from dam to ancestor
            dam_paths = self._all_paths_to_ancestor(dam_id, anc_id, max_gen - 1)

            # If ancestor IS the sire or dam directly, path length is 0.
            if anc_id == sire_id:
                sire_paths.append([sire_id])
            if anc_id == dam_id:
                dam_paths.append([dam_id])

            # F_A: the ancestor's own inbreeding coefficient (recursive,
            # but with reduced max_gen to avoid infinite recursion).
            f_a = self.coi(anc_id, max_gen - 1) if max_gen > 1 else 0.0

            for sp in sire_paths:
                for dp in dam_paths:
                    # Verify paths do not share intermediate nodes (true
                    # path-coefficient requirement: only the common ancestor
                    # itself should appear in both paths).
                    sp_intermediates = set(sp[:-1])  # exclude the ancestor
                    dp_intermediates = set(dp[:-1])
                    if sp_intermediates & dp_intermediates:
                        continue

                    n1 = len(sp)  # generations from sire to ancestor
                    n2 = len(dp)  # generations from dam to ancestor
                    contribution = (0.5 ** (n1 + n2 + 1)) * (1.0 + f_a)
                    total_coi += contribution

        # Clamp to [0, 1]
        total_coi = max(0.0, min(1.0, total_coi))
        self._coi_cache[cache_key] = total_coi
        return total_coi

    def hypothetical_coi(
        self, sire_id: int, dam_id: int, max_gen: Optional[int] = None
    ) -> float:
        """Estimate COI of a hypothetical offspring of *sire_id* x *dam_id*.

        Creates a temporary dog entry, computes COI, then removes it.

        Args:
            sire_id: Father's dog id.
            dam_id: Mother's dog id.

        Returns:
            Estimated COI for the hypothetical puppy.
        """
        temp_id = -999999
        sire = self._dogs.get(sire_id)
        dam = self._dogs.get(dam_id)
        if sire is None or dam is None:
            return 0.0

        temp_dog = Dog(
            dog_id=temp_id,
            name="__hypothetical__",
            breed_id=sire.breed_id,
            sire_id=sire_id,
            dam_id=dam_id,
        )
        self._dogs[temp_id] = temp_dog
        # Clear caches since we modified the tree
        self._ancestor_paths_cache.clear()
        self._coi_cache.clear()

        try:
            result = self.coi(temp_id, max_gen)
        finally:
            del self._dogs[temp_id]
            self._ancestor_paths_cache.clear()
            self._coi_cache.clear()

        return result


# ---------------------------------------------------------------------------
# Genetic Scorer
# ---------------------------------------------------------------------------


class GeneticScorer:
    """Computes Expected Progeny Differences and per-axis breeding scores.

    EPD for a given axis:
        EPD = (own_score - breed_mean) * heritability / 2

    The breed mean is computed dynamically from all dogs of the same breed
    present in the PedigreeTree.

    Usage:
        scorer = GeneticScorer(tree)
        epd = scorer.epd(dog_id)
        # epd => {"skeletal": 0.12, "gait": -0.05, ...}
    """

    def __init__(self, tree: PedigreeTree) -> None:
        self._tree = tree
        self._breed_mean_cache: Dict[int, Dict[str, float]] = {}

    def invalidate_cache(self) -> None:
        """Clear cached breed means (call after adding/removing dogs)."""
        self._breed_mean_cache.clear()

    def breed_means(self, breed_id: int) -> Dict[str, float]:
        """Compute per-axis mean scores for all dogs of *breed_id*.

        Args:
            breed_id: The breed to compute means for.

        Returns:
            Dict mapping axis name to mean score. Axes with no data
            default to 5.0 (midpoint of 0-10 scale).
        """
        if breed_id in self._breed_mean_cache:
            return self._breed_mean_cache[breed_id]

        dogs = self._tree.dogs_by_breed(breed_id)
        if not dogs:
            means = {axis: 5.0 for axis in SCORING_AXES}
            self._breed_mean_cache[breed_id] = means
            return means

        sums: Dict[str, float] = defaultdict(float)
        counts: Dict[str, int] = defaultdict(int)

        for dog in dogs:
            for axis in SCORING_AXES:
                if axis in dog.scores:
                    sums[axis] += dog.scores[axis]
                    counts[axis] += 1

        means: Dict[str, float] = {}
        for axis in SCORING_AXES:
            if counts[axis] > 0:
                means[axis] = sums[axis] / counts[axis]
            else:
                means[axis] = 5.0

        self._breed_mean_cache[breed_id] = means
        return means

    def epd(self, dog_id: int) -> Dict[str, float]:
        """Compute Expected Progeny Differences for each scoring axis.

        EPD_axis = (score_axis - breed_mean_axis) * heritability_axis / 2

        Args:
            dog_id: The dog to compute EPDs for.

        Returns:
            Dict mapping axis name to EPD value. Missing axes yield 0.0.
        """
        dog = self._tree.get_dog(dog_id)
        if dog is None:
            return {axis: 0.0 for axis in SCORING_AXES}

        means = self.breed_means(dog.breed_id)
        result: Dict[str, float] = {}

        for axis in SCORING_AXES:
            own_score = dog.scores.get(axis)
            if own_score is None:
                result[axis] = 0.0
            else:
                h2 = HERITABILITY_ESTIMATES[axis]
                result[axis] = (own_score - means[axis]) * h2 / 2.0

        return result

    def combined_epd(self, sire_id: int, dam_id: int) -> Dict[str, float]:
        """Estimate combined EPD for a hypothetical mating.

        For each axis the combined EPD is the sum of sire and dam EPDs,
        giving an estimate of the offspring's expected deviation from the
        breed mean.

        Args:
            sire_id: Father's dog id.
            dam_id: Mother's dog id.

        Returns:
            Dict mapping axis to combined EPD.
        """
        sire_epd = self.epd(sire_id)
        dam_epd = self.epd(dam_id)
        return {axis: sire_epd[axis] + dam_epd[axis] for axis in SCORING_AXES}

    def complementarity_score(self, sire_id: int, dam_id: int) -> float:
        """Score how well sire and dam complement each other's weaknesses.

        For each axis, if one parent is below breed mean and the other is
        above, they complement. The magnitude of the compensation is
        weighted by heritability.

        Returns:
            A score in [0, 100] where higher means better complementarity.
        """
        sire = self._tree.get_dog(sire_id)
        dam = self._tree.get_dog(dam_id)
        if sire is None or dam is None:
            return 0.0

        # Use sire's breed for means (assumption: same breed pairing)
        means = self.breed_means(sire.breed_id)

        total_complement = 0.0
        total_weight = 0.0

        for axis in SCORING_AXES:
            h2 = HERITABILITY_ESTIMATES[axis]
            sire_score = sire.scores.get(axis, means[axis])
            dam_score = dam.scores.get(axis, means[axis])
            sire_dev = sire_score - means[axis]
            dam_dev = dam_score - means[axis]

            # Both above mean: good but not complementary
            # One above, one below: complementary if the strong one
            # compensates for the weak one.
            # Both below: poor.
            if sire_dev * dam_dev < 0:
                # They are on opposite sides of the mean -- complementary
                # Credit proportional to how well the strong side covers
                # the weak side.
                compensation = min(abs(sire_dev), abs(dam_dev))
                total_complement += compensation * h2
            elif sire_dev >= 0 and dam_dev >= 0:
                # Both above mean: moderate bonus
                total_complement += min(sire_dev, dam_dev) * h2 * 0.5
            else:
                # Both below mean: penalty (no complementarity)
                total_complement -= min(abs(sire_dev), abs(dam_dev)) * h2 * 0.3

            total_weight += h2

        if total_weight == 0:
            return 50.0

        # Normalize to 0-100 scale.  Raw complement is roughly in [-5, 5]
        # range for typical 0-10 scores.
        raw = total_complement / total_weight
        # Map [-5, 5] -> [0, 100]
        normalized = (raw + 5.0) / 10.0 * 100.0
        return max(0.0, min(100.0, normalized))

    def health_compatibility(self, sire_id: int, dam_id: int) -> Dict:
        """Assess health-test compatibility between sire and dam.

        Checks every gene for which both dogs have test results.
        Carrier x Carrier pairings are flagged as risks.

        Args:
            sire_id: Father's dog id.
            dam_id: Mother's dog id.

        Returns:
            Dict with keys:
                "score": float 0-100 (100 = no risks)
                "risks": list of dicts describing each flagged risk
                "tested_genes": list of genes both dogs were tested for
        """
        sire = self._tree.get_dog(sire_id)
        dam = self._tree.get_dog(dam_id)
        if sire is None or dam is None:
            return {"score": 50.0, "risks": [], "tested_genes": []}

        sire_genes = {t["gene"]: t["result"] for t in sire.health_tests}
        dam_genes = {t["gene"]: t["result"] for t in dam.health_tests}
        common_genes = set(sire_genes.keys()) & set(dam_genes.keys())

        risks: List[Dict] = []
        penalty = 0.0

        for gene in sorted(common_genes):
            sr = sire_genes[gene]
            dr = dam_genes[gene]
            mode = COMMON_HEALTH_GENES.get(gene, {}).get("mode", "autosomal_recessive")
            desc = COMMON_HEALTH_GENES.get(gene, {}).get("description", gene)

            if mode == "autosomal_recessive":
                if sr == "affected" or dr == "affected":
                    risks.append({
                        "gene": gene,
                        "description": desc,
                        "severity": "critical",
                        "detail": "One or both parents affected; all offspring at risk.",
                        "sire_status": sr,
                        "dam_status": dr,
                    })
                    penalty += 30.0
                elif sr == "carrier" and dr == "carrier":
                    risks.append({
                        "gene": gene,
                        "description": desc,
                        "severity": "high",
                        "detail": "Both parents are carriers; 25% of offspring expected affected.",
                        "sire_status": sr,
                        "dam_status": dr,
                    })
                    penalty += 20.0
                elif sr == "carrier" or dr == "carrier":
                    risks.append({
                        "gene": gene,
                        "description": desc,
                        "severity": "low",
                        "detail": "One parent is a carrier; no affected offspring expected but 50% carriers.",
                        "sire_status": sr,
                        "dam_status": dr,
                    })
                    penalty += 3.0
            elif mode == "autosomal_dominant":
                if sr == "affected" or dr == "affected":
                    risks.append({
                        "gene": gene,
                        "description": desc,
                        "severity": "critical",
                        "detail": "Dominant gene: affected parent will pass to ~50% of offspring.",
                        "sire_status": sr,
                        "dam_status": dr,
                    })
                    penalty += 30.0
                elif sr == "carrier" or dr == "carrier":
                    risks.append({
                        "gene": gene,
                        "description": desc,
                        "severity": "moderate",
                        "detail": "Carrier of dominant gene; variable expression possible.",
                        "sire_status": sr,
                        "dam_status": dr,
                    })
                    penalty += 10.0

        score = max(0.0, 100.0 - penalty)
        return {
            "score": score,
            "risks": risks,
            "tested_genes": sorted(common_genes),
        }

    def color_compatibility(
        self, sire_id: int, dam_id: int
    ) -> Dict[str, Dict[str, float]]:
        """Predict offspring color genotype probabilities (simplified Mendelian).

        For each locus present in both parents, computes the probability
        distribution of offspring genotypes using a basic Punnett square.

        Args:
            sire_id: Father's dog id.
            dam_id: Mother's dog id.

        Returns:
            Dict mapping locus name to a dict of {genotype: probability}.
            Genotypes are represented as sorted 2-character strings
            (e.g. "BB", "Bb", "bb").
        """
        sire = self._tree.get_dog(sire_id)
        dam = self._tree.get_dog(dam_id)
        if sire is None or dam is None:
            return {}

        results: Dict[str, Dict[str, float]] = {}
        common_loci = set(sire.color_genetics.keys()) & set(dam.color_genetics.keys())

        for locus in sorted(common_loci):
            sire_alleles = sire.color_genetics[locus]
            dam_alleles = dam.color_genetics[locus]

            # Punnett square: 4 combinations
            combos: Dict[str, float] = defaultdict(float)
            for s_allele in sire_alleles:
                for d_allele in dam_alleles:
                    # Canonical ordering: uppercase (dominant) first
                    pair = tuple(sorted([s_allele, d_allele], key=lambda a: (a.lower(), a)))
                    genotype = pair[0] + pair[1]
                    combos[genotype] += 0.25

            results[locus] = dict(combos)

        return results


# ---------------------------------------------------------------------------
# Breeding Optimizer
# ---------------------------------------------------------------------------


class BreedingOptimizer:
    """Ranks candidate mates for a target dog and provides recommendations.

    The overall compatibility score (0-100) is a weighted combination of:
        - Genetic diversity (lower offspring COI = better):  weight 0.30
        - Scoring complementarity:                          weight 0.30
        - Health test compatibility:                        weight 0.30
        - Color genetics compatibility (bonus, not penalty): weight 0.10

    Usage:
        optimizer = BreedingOptimizer(tree)
        results = optimizer.rank_candidates(target_id, candidate_ids)
        for r in results:
            print(r["candidate_name"], r["overall_score"])
    """

    # Weights for sub-scores
    W_DIVERSITY = 0.30
    W_COMPLEMENT = 0.30
    W_HEALTH = 0.30
    W_COLOR = 0.10

    def __init__(self, tree: PedigreeTree) -> None:
        self._tree = tree
        self._scorer = GeneticScorer(tree)

    @property
    def scorer(self) -> GeneticScorer:
        """Access the underlying GeneticScorer."""
        return self._scorer

    def compatibility_score(self, sire_id: int, dam_id: int) -> Dict:
        """Compute a detailed compatibility report for a sire x dam pairing.

        Args:
            sire_id: Father's dog id.
            dam_id: Mother's dog id.

        Returns:
            Dict with keys:
                overall_score: float 0-100
                diversity_score: float 0-100
                complementarity_score: float 0-100
                health_score: float 0-100
                color_score: float 0-100
                offspring_coi: float
                combined_epd: dict
                health_details: dict (from health_compatibility)
                color_details: dict (from color_compatibility)
                risks: list of flagged health risks
        """
        # 1. Genetic diversity: lower COI -> higher score
        offspring_coi = self._tree.hypothetical_coi(sire_id, dam_id)
        # COI of 0 -> 100, COI of 0.25 -> 0 (linear mapping)
        diversity_score = max(0.0, min(100.0, (1.0 - offspring_coi / 0.25) * 100.0))

        # 2. Complementarity
        complement_score = self._scorer.complementarity_score(sire_id, dam_id)

        # 3. Health compatibility
        health_info = self._scorer.health_compatibility(sire_id, dam_id)
        health_score = health_info["score"]

        # 4. Color genetics -- we give a bonus for genetic diversity at
        #    color loci (more heterozygosity = more diversity = small bonus).
        color_details = self._scorer.color_compatibility(sire_id, dam_id)
        color_score = self._color_diversity_score(color_details)

        # 5. Combined EPD
        combined_epd = self._scorer.combined_epd(sire_id, dam_id)

        # Overall weighted score
        overall = (
            self.W_DIVERSITY * diversity_score
            + self.W_COMPLEMENT * complement_score
            + self.W_HEALTH * health_score
            + self.W_COLOR * color_score
        )
        overall = max(0.0, min(100.0, overall))

        return {
            "overall_score": round(overall, 2),
            "diversity_score": round(diversity_score, 2),
            "complementarity_score": round(complement_score, 2),
            "health_score": round(health_score, 2),
            "color_score": round(color_score, 2),
            "offspring_coi": round(offspring_coi, 6),
            "combined_epd": {k: round(v, 4) for k, v in combined_epd.items()},
            "health_details": health_info,
            "color_details": color_details,
            "risks": health_info["risks"],
        }

    def _color_diversity_score(
        self, color_details: Dict[str, Dict[str, float]]
    ) -> float:
        """Score color-locus genetic diversity in offspring.

        Higher heterozygosity probability at each locus yields a higher
        score.  100 = maximum heterozygosity across all loci.

        Args:
            color_details: Output of GeneticScorer.color_compatibility().

        Returns:
            Score in [0, 100].
        """
        if not color_details:
            return 50.0  # Neutral if no color data

        hetero_sum = 0.0
        locus_count = 0

        for _locus, genotype_probs in color_details.items():
            locus_count += 1
            for genotype, prob in genotype_probs.items():
                # A genotype is heterozygous if the two alleles differ
                if len(genotype) == 2 and genotype[0] != genotype[1]:
                    hetero_sum += prob

        if locus_count == 0:
            return 50.0

        avg_hetero = hetero_sum / locus_count  # in [0, 1]
        return avg_hetero * 100.0

    def rank_candidates(
        self,
        target_id: int,
        candidate_ids: List[int],
        top_n: Optional[int] = None,
    ) -> List[Dict]:
        """Rank candidate mates by compatibility score.

        Args:
            target_id: The dog seeking a mate.
            candidate_ids: List of potential mate dog ids.
            top_n: If set, return only the top N candidates.

        Returns:
            List of dicts sorted by overall_score descending.  Each dict
            contains:
                candidate_id, candidate_name, and all fields from
                compatibility_score().
        """
        results: List[Dict] = []
        target = self._tree.get_dog(target_id)
        if target is None:
            return results

        for cid in candidate_ids:
            candidate = self._tree.get_dog(cid)
            if candidate is None:
                continue
            if candidate.breed_id != target.breed_id:
                continue  # Only same-breed pairings

            report = self.compatibility_score(target_id, cid)
            report["candidate_id"] = cid
            report["candidate_name"] = candidate.name
            results.append(report)

        results.sort(key=lambda r: r["overall_score"], reverse=True)

        if top_n is not None:
            results = results[:top_n]

        return results

    def recommend(
        self,
        target_id: int,
        candidate_ids: List[int],
        top_n: int = 3,
    ) -> Dict:
        """Generate a breeding recommendation report.

        Args:
            target_id: The dog seeking a mate.
            candidate_ids: List of candidate mate ids.
            top_n: Number of top candidates to include in detailed breakdown.

        Returns:
            Dict with:
                target: Dog info
                recommendations: list of top_n ranked candidates with
                    detailed breakdowns
                health_warnings: list of any carrier x carrier pairings
                    across ALL candidates (not just top_n)
                summary_stats: dict with average COI, score ranges, etc.
        """
        target = self._tree.get_dog(target_id)
        if target is None:
            return {"error": "Target dog not found"}

        all_ranked = self.rank_candidates(target_id, candidate_ids)
        top_candidates = all_ranked[:top_n]

        # Collect all health warnings across every candidate
        health_warnings: List[Dict] = []
        scores_list: List[float] = []
        coi_list: List[float] = []

        for report in all_ranked:
            scores_list.append(report["overall_score"])
            coi_list.append(report["offspring_coi"])
            for risk in report.get("risks", []):
                if risk["severity"] in ("high", "critical"):
                    health_warnings.append({
                        "candidate_id": report["candidate_id"],
                        "candidate_name": report["candidate_name"],
                        **risk,
                    })

        summary_stats = {}
        if scores_list:
            summary_stats = {
                "candidates_evaluated": len(all_ranked),
                "avg_score": round(sum(scores_list) / len(scores_list), 2),
                "max_score": round(max(scores_list), 2),
                "min_score": round(min(scores_list), 2),
                "avg_offspring_coi": round(
                    sum(coi_list) / len(coi_list), 6
                ),
                "min_offspring_coi": round(min(coi_list), 6),
                "max_offspring_coi": round(max(coi_list), 6),
            }

        return {
            "target": {
                "id": target.id,
                "name": target.name,
                "breed_id": target.breed_id,
            },
            "recommendations": top_candidates,
            "health_warnings": health_warnings,
            "summary_stats": summary_stats,
        }


# ---------------------------------------------------------------------------
# Population Genetics Metrics
# ---------------------------------------------------------------------------


def effective_population_size(coi_values: List[float]) -> float:
    """Estimate effective population size (Ne) from individual COI values.

    Uses the relationship: Ne ~ 1 / (2 * mean_COI)

    This is a simplified estimator. When mean COI is zero (no inbreeding
    detected), returns infinity.

    Args:
        coi_values: List of COI values for individuals in the population.

    Returns:
        Estimated Ne. Returns float('inf') if mean COI is 0.
    """
    if not coi_values:
        return float("inf")
    mean_coi = sum(coi_values) / len(coi_values)
    if mean_coi <= 0:
        return float("inf")
    return 1.0 / (2.0 * mean_coi)


def average_coi(tree: PedigreeTree, breed_id: int) -> float:
    """Compute the average COI for all dogs of a breed in the tree.

    Args:
        tree: The PedigreeTree containing the dogs.
        breed_id: The breed to compute average COI for.

    Returns:
        Mean COI, or 0.0 if no dogs of that breed exist.
    """
    dogs = tree.dogs_by_breed(breed_id)
    if not dogs:
        return 0.0
    coi_values = [tree.coi(d.id) for d in dogs]
    return sum(coi_values) / len(coi_values)


def genetic_diversity_index(tree: PedigreeTree, breed_id: int) -> float:
    """Compute a genetic diversity index for a breed population.

    The index is defined as:
        GDI = 1 - average_COI

    Values closer to 1.0 indicate greater genetic diversity.
    Values closer to 0.0 indicate severe inbreeding.

    Args:
        tree: The PedigreeTree containing the dogs.
        breed_id: The breed to assess.

    Returns:
        Diversity index in [0.0, 1.0].
    """
    avg = average_coi(tree, breed_id)
    return 1.0 - avg


def population_metrics(tree: PedigreeTree, breed_id: int) -> Dict:
    """Compute a full suite of population genetics metrics for a breed.

    Args:
        tree: The PedigreeTree.
        breed_id: The breed to assess.

    Returns:
        Dict with:
            breed_id: int
            population_size: int (number of dogs in tree)
            average_coi: float
            genetic_diversity_index: float
            effective_population_size: float
            coi_distribution: dict with min, max, median, q1, q3
    """
    dogs = tree.dogs_by_breed(breed_id)
    n = len(dogs)
    if n == 0:
        return {
            "breed_id": breed_id,
            "population_size": 0,
            "average_coi": 0.0,
            "genetic_diversity_index": 1.0,
            "effective_population_size": float("inf"),
            "coi_distribution": {},
        }

    coi_values = sorted([tree.coi(d.id) for d in dogs])
    mean_coi = sum(coi_values) / n
    ne = effective_population_size(coi_values)
    gdi = 1.0 - mean_coi

    def percentile(data: List[float], p: float) -> float:
        """Compute the p-th percentile (0-100) of sorted data."""
        if not data:
            return 0.0
        k = (len(data) - 1) * (p / 100.0)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return data[int(k)]
        return data[f] * (c - k) + data[c] * (k - f)

    distribution = {
        "min": round(coi_values[0], 6),
        "max": round(coi_values[-1], 6),
        "median": round(percentile(coi_values, 50), 6),
        "q1": round(percentile(coi_values, 25), 6),
        "q3": round(percentile(coi_values, 75), 6),
    }

    return {
        "breed_id": breed_id,
        "population_size": n,
        "average_coi": round(mean_coi, 6),
        "genetic_diversity_index": round(gdi, 6),
        "effective_population_size": round(ne, 2) if ne != float("inf") else float("inf"),
        "coi_distribution": distribution,
    }


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def _self_test() -> None:
    """Run built-in tests to verify module correctness.

    Constructs a small pedigree with known structure and validates:
    - COI computation for a simple half-sibling mating
    - EPD calculation against manual values
    - Health compatibility scoring
    - Color genetics Punnett square
    - Breeding optimizer ranking
    - Population metrics

    Raises AssertionError on any failure.
    """
    print("=== genetic_scoring self-test ===")

    # ---- Build a small pedigree ----
    #
    #  Grandpa (10)
    #    |          \
    #  Sire_A (20)   Dam_B (30)   <- half siblings (same sire = Grandpa)
    #    |     \       |      \
    #  (via different dams)
    #
    # More specifically:
    #   Grandpa (10): no parents known
    #   Grandma_1 (11): no parents known
    #   Grandma_2 (12): no parents known
    #   Sire_A (20): sire=10, dam=11
    #   Dam_B (30): sire=10, dam=12
    #   Puppy (40): sire=20, dam=30  <- inbred (half-sibling mating)

    grandpa = Dog(10, "Grandpa", breed_id=1, scores={
        "skeletal": 8.0, "gait": 7.0, "muscle": 6.0, "coat": 9.0, "temperament": 7.5,
    })
    grandma1 = Dog(11, "Grandma1", breed_id=1, scores={
        "skeletal": 7.0, "gait": 8.0, "muscle": 7.0, "coat": 6.0, "temperament": 8.0,
    })
    grandma2 = Dog(12, "Grandma2", breed_id=1, scores={
        "skeletal": 6.0, "gait": 6.0, "muscle": 8.0, "coat": 7.0, "temperament": 6.5,
    })

    sire_a = Dog(
        20, "Sire_A", breed_id=1, sire_id=10, dam_id=11,
        scores={
            "skeletal": 9.0, "gait": 7.5, "muscle": 6.5, "coat": 8.0, "temperament": 7.0,
        },
        health_tests=[
            {"gene": "vWD1", "result": "carrier"},
            {"gene": "PRA_prcd", "result": "clear"},
            {"gene": "DM", "result": "clear"},
        ],
        color_genetics={"E": ("E", "e"), "B": ("B", "b")},
    )

    dam_b = Dog(
        30, "Dam_B", breed_id=1, sire_id=10, dam_id=12,
        scores={
            "skeletal": 5.0, "gait": 8.5, "muscle": 7.5, "coat": 7.0, "temperament": 8.5,
        },
        health_tests=[
            {"gene": "vWD1", "result": "carrier"},
            {"gene": "PRA_prcd", "result": "clear"},
            {"gene": "DM", "result": "carrier"},
        ],
        color_genetics={"E": ("E", "E"), "B": ("B", "B")},
    )

    puppy = Dog(
        40, "Puppy", breed_id=1, sire_id=20, dam_id=30,
        scores={
            "skeletal": 7.0, "gait": 8.0, "muscle": 7.0, "coat": 7.5, "temperament": 7.5,
        },
    )

    # Unrelated dog for comparison
    outsider = Dog(
        50, "Outsider", breed_id=1,
        scores={
            "skeletal": 7.0, "gait": 7.0, "muscle": 7.0, "coat": 7.0, "temperament": 7.0,
        },
        health_tests=[
            {"gene": "vWD1", "result": "clear"},
            {"gene": "PRA_prcd", "result": "clear"},
            {"gene": "DM", "result": "clear"},
        ],
        color_genetics={"E": ("e", "e"), "B": ("B", "b")},
    )

    # Different breed dog (should be excluded from same-breed ranking)
    diff_breed = Dog(
        60, "DiffBreed", breed_id=2,
        scores={
            "skeletal": 9.0, "gait": 9.0, "muscle": 9.0, "coat": 9.0, "temperament": 9.0,
        },
    )

    tree = PedigreeTree()
    tree.add_dogs([grandpa, grandma1, grandma2, sire_a, dam_b, puppy, outsider, diff_breed])

    # ---- Test 1: COI of Puppy (half-sibling mating) ----
    puppy_coi = tree.coi(40)
    print(f"  Puppy COI = {puppy_coi:.6f}")
    # Half-sibling mating with one common ancestor (Grandpa, id=10):
    # Path through sire: 20 -> 10 (n1 = 1)
    # Path through dam: 30 -> 10 (n2 = 1)
    # COI = (1/2)^(1+1+1) * (1 + F_grandpa) = (1/2)^3 * 1.0 = 0.125
    assert abs(puppy_coi - 0.125) < 0.01, f"Expected ~0.125, got {puppy_coi}"
    print("  [PASS] COI for half-sibling mating")

    # ---- Test 2: COI of unrelated dog ----
    outsider_coi = tree.coi(50)
    assert outsider_coi == 0.0, f"Expected 0.0, got {outsider_coi}"
    print("  [PASS] COI for unrelated dog is 0")

    # ---- Test 3: Hypothetical COI ----
    hyp_coi = tree.hypothetical_coi(20, 30)
    assert abs(hyp_coi - 0.125) < 0.01, f"Expected ~0.125, got {hyp_coi}"
    print("  [PASS] Hypothetical COI matches actual puppy COI")

    # ---- Test 4: EPD computation ----
    scorer = GeneticScorer(tree)
    means = scorer.breed_means(1)
    print(f"  Breed 1 means: { {k: round(v, 2) for k, v in means.items()} }")

    sire_epd = scorer.epd(20)
    print(f"  Sire_A EPD: { {k: round(v, 4) for k, v in sire_epd.items()} }")
    # Manual check for skeletal: (9.0 - mean_skeletal) * 0.45 / 2
    expected_skeletal_epd = (9.0 - means["skeletal"]) * 0.45 / 2.0
    assert abs(sire_epd["skeletal"] - expected_skeletal_epd) < 0.001, (
        f"EPD skeletal mismatch: {sire_epd['skeletal']} vs {expected_skeletal_epd}"
    )
    print("  [PASS] EPD computation")

    # ---- Test 5: Health compatibility ----
    health = scorer.health_compatibility(20, 30)
    print(f"  Health score (Sire_A x Dam_B): {health['score']}")
    # vWD1: carrier x carrier -> high risk, -20
    # PRA_prcd: clear x clear -> no risk
    # DM: clear x carrier -> low risk, -3
    # Expected score: 100 - 20 - 3 = 77
    assert abs(health["score"] - 77.0) < 0.01, f"Expected 77.0, got {health['score']}"
    assert len(health["risks"]) == 2, f"Expected 2 risks, got {len(health['risks'])}"
    print("  [PASS] Health compatibility scoring")

    # ---- Test 6: Color genetics ----
    colors = scorer.color_compatibility(20, 30)
    print(f"  Color compatibility: {colors}")
    # Sire E locus: (E, e), Dam E locus: (E, E)
    # Punnett: EE=0.5, Ee=0.5
    e_locus = colors.get("E", {})
    assert abs(e_locus.get("EE", 0) - 0.5) < 0.01
    assert abs(e_locus.get("Ee", 0) - 0.5) < 0.01
    # Sire B locus: (B, b), Dam B locus: (B, B)
    # Punnett: BB=0.5, Bb=0.5
    b_locus = colors.get("B", {})
    assert abs(b_locus.get("BB", 0) - 0.5) < 0.01
    assert abs(b_locus.get("Bb", 0) - 0.5) < 0.01
    print("  [PASS] Color genetics Punnett square")

    # ---- Test 7: Breeding optimizer ranking ----
    optimizer = BreedingOptimizer(tree)
    # Rank candidates for Sire_A: candidates = Dam_B, Outsider, DiffBreed
    ranked = optimizer.rank_candidates(20, [30, 50, 60])
    print(f"  Candidates ranked: {len(ranked)}")
    # DiffBreed (breed_id=2) should be excluded
    assert len(ranked) == 2, f"Expected 2 same-breed candidates, got {len(ranked)}"
    for r in ranked:
        print(f"    {r['candidate_name']}: overall={r['overall_score']}")
    # Outsider should score higher than Dam_B (lower COI, no carrier x carrier)
    outsider_rank = [r for r in ranked if r["candidate_id"] == 50]
    dam_b_rank = [r for r in ranked if r["candidate_id"] == 30]
    assert outsider_rank and dam_b_rank
    assert outsider_rank[0]["overall_score"] > dam_b_rank[0]["overall_score"], (
        "Outsider should rank above Dam_B due to lower COI and better health"
    )
    print("  [PASS] Breeding optimizer ranking")

    # ---- Test 8: Recommendation report ----
    report = optimizer.recommend(20, [30, 50, 60], top_n=2)
    assert report["target"]["id"] == 20
    assert len(report["recommendations"]) == 2
    assert report["summary_stats"]["candidates_evaluated"] == 2
    assert len(report["health_warnings"]) > 0  # carrier x carrier flagged
    print(f"  Recommendation report: {report['summary_stats']}")
    print("  [PASS] Recommendation engine")

    # ---- Test 9: Population metrics ----
    metrics = population_metrics(tree, breed_id=1)
    print(f"  Population metrics for breed 1: {metrics}")
    assert metrics["population_size"] == 7  # all breed_id=1 dogs
    assert metrics["average_coi"] >= 0
    assert 0 <= metrics["genetic_diversity_index"] <= 1.0
    print("  [PASS] Population metrics")

    # ---- Test 10: Edge cases ----
    # Dog with no parents
    assert tree.coi(10) == 0.0
    # Non-existent dog
    assert tree.coi(9999) == 0.0
    # EPD of non-existent dog
    epd_none = scorer.epd(9999)
    assert all(v == 0.0 for v in epd_none.values())
    # Effective population size with no inbreeding
    assert effective_population_size([0.0, 0.0, 0.0]) == float("inf")
    # Effective population size with known COI
    ne = effective_population_size([0.125])
    assert abs(ne - 4.0) < 0.01  # Ne = 1/(2*0.125) = 4
    # Empty population
    empty_metrics = population_metrics(tree, breed_id=999)
    assert empty_metrics["population_size"] == 0
    print("  [PASS] Edge cases")

    print("=== All self-tests passed ===")


if __name__ == "__main__":
    _self_test()
