"""Tests for api/ai/multidisease_benchmarks.py."""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.ai.multidisease_benchmarks import BenchmarkResult, BenchmarkSuite

# ---------------------------------------------------------------------------
# BenchmarkResult tests
# ---------------------------------------------------------------------------


class TestBenchmarkResult:
    def test_instantiation(self):
        result = BenchmarkResult(
            test_name="my test",
            dataset_size=10,
            num_combinations=5,
            execution_time_ms=12.345,
            combinations_per_second=100.5,
        )
        assert result.test_name == "my test"
        assert result.dataset_size == 10
        assert result.num_combinations == 5
        assert result.execution_time_ms == pytest.approx(12.345)
        assert result.combinations_per_second == pytest.approx(100.5)

    def test_to_dict_keys(self):
        result = BenchmarkResult(
            test_name="x",
            dataset_size=1,
            num_combinations=2,
            execution_time_ms=3.1,
            combinations_per_second=4.2,
        )
        d = result.to_dict()
        assert set(d.keys()) == {
            "test_name",
            "dataset_size",
            "num_combinations",
            "execution_time_ms",
            "combinations_per_second",
        }

    def test_to_dict_values(self):
        result = BenchmarkResult(
            test_name="foo",
            dataset_size=50,
            num_combinations=20,
            execution_time_ms=99.999,
            combinations_per_second=200.123,
        )
        d = result.to_dict()
        assert d["test_name"] == "foo"
        assert d["dataset_size"] == 50
        assert d["num_combinations"] == 20
        # Values are rounded to 2 decimal places
        assert d["execution_time_ms"] == round(99.999, 2)
        assert d["combinations_per_second"] == round(200.123, 2)

    def test_to_dict_rounding(self):
        result = BenchmarkResult(
            test_name="r",
            dataset_size=1,
            num_combinations=1,
            execution_time_ms=1.2345678,
            combinations_per_second=9.8765432,
        )
        d = result.to_dict()
        assert d["execution_time_ms"] == 1.23
        assert d["combinations_per_second"] == 9.88


# ---------------------------------------------------------------------------
# BenchmarkSuite tests
# ---------------------------------------------------------------------------


class TestBenchmarkSuite:
    def setup_method(self):
        self.suite = BenchmarkSuite()

    def test_init_empty_results(self):
        assert self.suite.results == []

    # ------------------------------------------------------------------
    # generate_disease_interactions
    # ------------------------------------------------------------------

    def test_generate_disease_interactions_count(self):
        interactions = self.suite.generate_disease_interactions(5)
        # 5 diseases → C(5,2) = 10 pairs
        assert len(interactions) == 10

    def test_generate_disease_interactions_zero(self):
        interactions = self.suite.generate_disease_interactions(0)
        assert interactions == {}

    def test_generate_disease_interactions_one(self):
        interactions = self.suite.generate_disease_interactions(1)
        assert interactions == {}

    def test_generate_disease_interactions_keys_are_tuples(self):
        interactions = self.suite.generate_disease_interactions(3)
        for key in interactions:
            assert isinstance(key, tuple)
            assert len(key) == 2

    def test_generate_disease_interactions_disease_names(self):
        interactions = self.suite.generate_disease_interactions(4)
        all_names = set()
        for d1, d2 in interactions:
            all_names.add(d1)
            all_names.add(d2)
        assert all_names == {"Disease_0", "Disease_1", "Disease_2", "Disease_3"}

    def test_generate_disease_interactions_values(self):
        from api.ai.multidisease_expander import DiseaseInteraction

        interactions = self.suite.generate_disease_interactions(3)
        for value in interactions.values():
            assert isinstance(value, DiseaseInteraction)
            assert 0.0 <= value.base_probability <= 1.0

    def test_generate_disease_interactions_interaction_types(self):
        from api.ai.multidisease_expander import InteractionType

        interactions = self.suite.generate_disease_interactions(10)
        found_types = {v.interaction_type for v in interactions.values()}
        valid_types = {
            InteractionType.CASCADE,
            InteractionType.SYNERGISTIC,
            InteractionType.SECONDARY,
            InteractionType.SHARED_PATHWAY,
            InteractionType.INDEPENDENT,
        }
        assert found_types.issubset(valid_types)

    # ------------------------------------------------------------------
    # benchmark_expansion_by_dataset_size
    # ------------------------------------------------------------------

    def test_benchmark_expansion_appends_results(self, capsys):
        self.suite.benchmark_expansion_by_dataset_size()
        # 6 size values
        assert len(self.suite.results) == 6

    def test_benchmark_expansion_result_names(self, capsys):
        self.suite.benchmark_expansion_by_dataset_size()
        for r in self.suite.results:
            assert r.test_name.startswith("Expansion (size=")

    # ------------------------------------------------------------------
    # benchmark_complexity_calculation
    # ------------------------------------------------------------------

    def test_benchmark_complexity_appends_results(self, capsys):
        self.suite.benchmark_complexity_calculation()
        # 5 combo sizes
        assert len(self.suite.results) == 5

    def test_benchmark_complexity_result_names(self, capsys):
        self.suite.benchmark_complexity_calculation()
        for r in self.suite.results:
            assert r.test_name.startswith("Complexity (size=")

    # ------------------------------------------------------------------
    # benchmark_rule_mining
    # ------------------------------------------------------------------

    def test_benchmark_rule_mining_appends_results(self, capsys):
        self.suite.benchmark_rule_mining()
        # 5 pattern counts
        assert len(self.suite.results) == 5

    def test_benchmark_rule_mining_result_names(self, capsys):
        self.suite.benchmark_rule_mining()
        for r in self.suite.results:
            assert r.test_name.startswith("Rule Mining (patterns=")

    # ------------------------------------------------------------------
    # benchmark_clustering
    # ------------------------------------------------------------------

    def test_benchmark_clustering_appends_results(self, capsys):
        self.suite.benchmark_clustering()
        assert len(self.suite.results) == 5

    def test_benchmark_clustering_result_names(self, capsys):
        self.suite.benchmark_clustering()
        for r in self.suite.results:
            assert r.test_name.startswith("Clustering (diseases=")

    # ------------------------------------------------------------------
    # benchmark_network_analysis
    # ------------------------------------------------------------------

    def test_benchmark_network_analysis_appends_one_result(self, capsys):
        self.suite.benchmark_network_analysis()
        assert len(self.suite.results) == 1
        assert self.suite.results[0].test_name == "Network Analysis"

    # ------------------------------------------------------------------
    # benchmark_memory_usage
    # ------------------------------------------------------------------

    def test_benchmark_memory_usage_runs_without_error(self, capsys):
        # Does not append to self.results; just prints
        self.suite.benchmark_memory_usage()
        captured = capsys.readouterr()
        assert "Size:" in captured.out

    # ------------------------------------------------------------------
    # print_summary
    # ------------------------------------------------------------------

    def test_print_summary_no_results(self, capsys):
        self.suite.print_summary()
        captured = capsys.readouterr()
        assert "No results collected" in captured.out

    def test_print_summary_with_results(self, capsys):
        self.suite.results = [
            BenchmarkResult("Alpha", 10, 5, 1.0, 5000.0),
            BenchmarkResult("Beta", 20, 10, 2.0, 5000.0),
        ]
        self.suite.print_summary()
        captured = capsys.readouterr()
        assert "Total benchmarks run: 2" in captured.out
        assert "Fastest" in captured.out
        assert "Slowest" in captured.out
        # JSON output
        assert "Alpha" in captured.out
        assert "Beta" in captured.out

    def test_print_summary_json_output(self, capsys):
        self.suite.results = [
            BenchmarkResult("Only", 5, 3, 10.0, 300.0),
        ]
        self.suite.print_summary()
        captured = capsys.readouterr()
        # Verify valid JSON block is present
        lines = captured.out.splitlines()
        json_start = next(i for i, l in enumerate(lines) if l.strip().startswith("["))
        json_text = "\n".join(lines[json_start:])
        parsed = json.loads(json_text)
        assert isinstance(parsed, list)
        assert parsed[0]["test_name"] == "Only"

    # ------------------------------------------------------------------
    # run_all_benchmarks (smoke test – just confirm it doesn't crash)
    # ------------------------------------------------------------------

    def test_run_all_benchmarks_populates_results(self, capsys):
        self.suite.run_all_benchmarks()
        # Should have results from all benchmark methods
        assert len(self.suite.results) > 0
