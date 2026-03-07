"""
Comprehensive tests for the genetic scoring and breeding optimization system.

Tests cover:
- Dog data structure
- PedigreeTree operations
- Wright's COI calculation
- GeneticScorer EPD estimation
- BreedingOptimizer compatibility
- Color genetics
- Health gene analysis
- Edge cases
"""

from api.genetic_scoring import (
    COMMON_HEALTH_GENES,
    HERITABILITY_ESTIMATES,
    SCORING_AXES,
    Dog,
    PedigreeTree,
    GeneticScorer,
    BreedingOptimizer,
)


# ============================================================================
# Dog Data Structure
# ============================================================================


class TestDog:
    """Verify Dog data container."""

    def test_create_basic_dog(self):
        dog = Dog(1, "Alpha", breed_id=1)
        assert dog.id == 1
        assert dog.name == "Alpha"
        assert dog.breed_id == 1
        assert dog.sire_id is None
        assert dog.dam_id is None

    def test_create_dog_with_parents(self):
        dog = Dog(1, "Alpha", breed_id=1, sire_id=2, dam_id=3)
        assert dog.sire_id == 2
        assert dog.dam_id == 3

    def test_default_scores_empty(self):
        dog = Dog(1, "Alpha", breed_id=1)
        assert dog.scores == {}

    def test_default_health_tests_empty(self):
        dog = Dog(1, "Alpha", breed_id=1)
        assert dog.health_tests == []

    def test_health_status_clear(self):
        dog = Dog(
            1, "Alpha", breed_id=1,
            health_tests=[{"gene": "vWD1", "result": "clear"}],
        )
        assert dog.health_status("vWD1") == "clear"

    def test_health_status_untested(self):
        dog = Dog(1, "Alpha", breed_id=1)
        assert dog.health_status("vWD1") is None

    def test_health_status_carrier(self):
        dog = Dog(
            1, "Alpha", breed_id=1,
            health_tests=[{"gene": "PRA_prcd", "result": "carrier"}],
        )
        assert dog.health_status("PRA_prcd") == "carrier"

    def test_repr(self):
        dog = Dog(1, "Alpha", breed_id=1)
        r = repr(dog)
        assert "Alpha" in r
        assert "1" in r

    def test_color_genetics(self):
        dog = Dog(
            1, "Alpha", breed_id=1,
            color_genetics={"E": ("E", "e"), "B": ("B", "B")},
        )
        assert dog.color_genetics["E"] == ("E", "e")
        assert dog.color_genetics["B"] == ("B", "B")


# ============================================================================
# PedigreeTree
# ============================================================================


class TestPedigreeTree:
    """Verify pedigree tree operations and COI calculation."""

    def _make_simple_tree(self):
        """Create a simple 3-generation pedigree."""
        tree = PedigreeTree()
        # Grandparents
        tree.add_dog(Dog(10, "GrandSire", breed_id=1))
        tree.add_dog(Dog(11, "GrandDam", breed_id=1))
        tree.add_dog(Dog(12, "GrandSire2", breed_id=1))
        tree.add_dog(Dog(13, "GrandDam2", breed_id=1))
        # Parents
        tree.add_dog(Dog(2, "Sire", breed_id=1, sire_id=10, dam_id=11))
        tree.add_dog(Dog(3, "Dam", breed_id=1, sire_id=12, dam_id=13))
        # Offspring
        tree.add_dog(Dog(1, "Puppy", breed_id=1, sire_id=2, dam_id=3))
        return tree

    def test_add_and_retrieve_dog(self):
        tree = PedigreeTree()
        dog = Dog(1, "Alpha", breed_id=1)
        tree.add_dog(dog)
        assert tree.get_dog(1) is dog

    def test_get_nonexistent_dog(self):
        tree = PedigreeTree()
        assert tree.get_dog(999) is None

    def test_all_dogs(self):
        tree = self._make_simple_tree()
        assert len(tree.all_dogs) == 7

    def test_dogs_by_breed(self):
        tree = PedigreeTree()
        tree.add_dog(Dog(1, "A", breed_id=1))
        tree.add_dog(Dog(2, "B", breed_id=2))
        tree.add_dog(Dog(3, "C", breed_id=1))
        assert len(tree.dogs_by_breed(1)) == 2
        assert len(tree.dogs_by_breed(2)) == 1

    def test_ancestors(self):
        tree = self._make_simple_tree()
        ancestors = tree.ancestors(1)
        # Should include parents and grandparents
        assert 2 in ancestors  # Sire
        assert 3 in ancestors  # Dam
        assert 10 in ancestors  # GrandSire
        assert 11 in ancestors  # GrandDam

    def test_coi_unrelated_parents(self):
        """COI should be 0 when parents are completely unrelated."""
        tree = self._make_simple_tree()
        coi = tree.coi(1)
        assert coi == 0.0

    def test_coi_half_sibling_mating(self):
        """Half-sibling mating (shared sire) should produce COI = 0.125.

        Wright's formula: COI = sum of (1/2)^(n1+n2+1) * (1+F_A)
        Common ancestor = CommonSire (F_A=0)
        Path from sire side: Sire -> CommonSire (n1=1)
        Path from dam side: Dam -> CommonSire (n2=1)
        COI = (1/2)^(1+1+1) * (1+0) = 1/8 = 0.125
        """
        tree = PedigreeTree()
        tree.add_dog(Dog(10, "CommonSire", breed_id=1))
        tree.add_dog(Dog(11, "Dam1", breed_id=1))
        tree.add_dog(Dog(12, "Dam2", breed_id=1))
        # Half-siblings (same sire, different dam)
        tree.add_dog(Dog(2, "Sire", breed_id=1, sire_id=10, dam_id=11))
        tree.add_dog(Dog(3, "Dam", breed_id=1, sire_id=10, dam_id=12))
        # Offspring of half-siblings
        tree.add_dog(Dog(1, "Offspring", breed_id=1, sire_id=2, dam_id=3))
        coi = tree.coi(1)
        assert abs(coi - 0.125) < 0.01

    def test_coi_no_parents(self):
        """Dog with no parents should have COI = 0."""
        tree = PedigreeTree()
        tree.add_dog(Dog(1, "Orphan", breed_id=1))
        assert tree.coi(1) == 0.0

    def test_coi_one_parent_missing(self):
        """Dog with only one parent known should have COI = 0."""
        tree = PedigreeTree()
        tree.add_dog(Dog(2, "Sire", breed_id=1))
        tree.add_dog(Dog(1, "Puppy", breed_id=1, sire_id=2))
        assert tree.coi(1) == 0.0

    def test_coi_cached(self):
        """Second call should use cache."""
        tree = self._make_simple_tree()
        coi1 = tree.coi(1)
        coi2 = tree.coi(1)
        assert coi1 == coi2

    def test_add_bulk_dogs(self):
        tree = PedigreeTree()
        dogs = [Dog(i, f"Dog{i}", breed_id=1) for i in range(10)]
        tree.add_dogs(dogs)
        assert len(tree.all_dogs) == 10


# ============================================================================
# GeneticScorer
# ============================================================================


class TestGeneticScorer:
    """Verify EPD estimation and scoring."""

    def _make_scored_dogs(self):
        tree = PedigreeTree()
        scores_a = {axis: 85.0 for axis in SCORING_AXES}
        scores_b = {axis: 75.0 for axis in SCORING_AXES}
        dog_a = Dog(1, "Alpha", breed_id=1, scores=scores_a)
        dog_b = Dog(2, "Beta", breed_id=1, scores=scores_b)
        tree.add_dog(dog_a)
        tree.add_dog(dog_b)
        return tree

    def test_heritability_estimates_valid(self):
        for axis in SCORING_AXES:
            assert axis in HERITABILITY_ESTIMATES
            h = HERITABILITY_ESTIMATES[axis]
            assert 0.0 <= h <= 1.0

    def test_scorer_creation(self):
        tree = self._make_scored_dogs()
        scorer = GeneticScorer(tree)
        assert scorer is not None

    def test_epd_estimation(self):
        tree = self._make_scored_dogs()
        scorer = GeneticScorer(tree)
        epd = scorer.epd(1)
        assert isinstance(epd, dict)
        for axis in SCORING_AXES:
            assert axis in epd

    def test_epd_higher_score_gives_positive_epd(self):
        """Dog with above-average scores should have positive EPDs."""
        tree = PedigreeTree()
        scores_high = {axis: 95.0 for axis in SCORING_AXES}
        scores_avg = {axis: 75.0 for axis in SCORING_AXES}
        tree.add_dog(Dog(1, "High", breed_id=1, scores=scores_high))
        tree.add_dog(Dog(2, "Avg", breed_id=1, scores=scores_avg))
        scorer = GeneticScorer(tree)
        epd = scorer.epd(1)
        for axis in SCORING_AXES:
            assert epd[axis] >= 0.0


# ============================================================================
# BreedingOptimizer
# ============================================================================


class TestBreedingOptimizer:
    """Verify breeding pair optimization."""

    def _make_breeding_pool(self):
        tree = PedigreeTree()
        for i in range(5):
            scores = {axis: 70 + i * 5 for axis in SCORING_AXES}
            tree.add_dog(Dog(i + 1, f"Dog{i+1}", breed_id=1, scores=scores))
        return tree

    def test_optimizer_creation(self):
        tree = self._make_breeding_pool()
        optimizer = BreedingOptimizer(tree)
        assert optimizer is not None
        assert optimizer.scorer is not None

    def test_compatibility_score(self):
        tree = self._make_breeding_pool()
        optimizer = BreedingOptimizer(tree)
        result = optimizer.compatibility_score(1, 2)
        assert "overall_score" in result
        assert 0 <= result["overall_score"] <= 100

    def test_rank_candidates(self):
        tree = self._make_breeding_pool()
        optimizer = BreedingOptimizer(tree)
        ranked = optimizer.rank_candidates(1, [2, 3, 4, 5])
        assert len(ranked) > 0
        # Results should be sorted by overall_score descending
        scores = [r["overall_score"] for r in ranked]
        assert scores == sorted(scores, reverse=True)


# ============================================================================
# Health Genes
# ============================================================================


class TestHealthGenes:
    """Verify health gene configuration."""

    def test_all_genes_have_mode(self):
        for gene, info in COMMON_HEALTH_GENES.items():
            assert "mode" in info, f"Gene {gene} missing 'mode'"
            assert info["mode"] in ("autosomal_recessive", "autosomal_dominant")

    def test_all_genes_have_description(self):
        for gene, info in COMMON_HEALTH_GENES.items():
            assert "description" in info, f"Gene {gene} missing 'description'"
            assert len(info["description"]) > 0

    def test_expected_genes_present(self):
        expected = {"vWD1", "PRA_prcd", "DM", "EIC", "MDR1", "HUU", "DCM", "CEA"}
        assert set(COMMON_HEALTH_GENES.keys()) == expected
