"""Performance benchmarks for MultiDiseaseExpander.

Measures execution time, memory usage, and scalability across different
dataset sizes and combination complexities.
"""

import time
import sys
import os
from typing import Dict, List, Tuple
from dataclasses import dataclass
import json

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from api.ai.multidisease_expander import (
    MultiDiseaseExpander,
    DiseaseInteraction,
    InteractionType,
    InteractionRuleMiner,
)


@dataclass
class BenchmarkResult:
    """Result of a single benchmark."""
    test_name: str
    dataset_size: int
    num_combinations: int
    execution_time_ms: float
    combinations_per_second: float

    def to_dict(self):
        return {
            "test_name": self.test_name,
            "dataset_size": self.dataset_size,
            "num_combinations": self.num_combinations,
            "execution_time_ms": round(self.execution_time_ms, 2),
            "combinations_per_second": round(self.combinations_per_second, 2),
        }


class BenchmarkSuite:
    """Suite of performance benchmarks."""

    def __init__(self):
        self.results: List[BenchmarkResult] = []

    def generate_disease_interactions(self,
                                     num_diseases: int) -> Dict[Tuple[str, str], DiseaseInteraction]:
        """Generate synthetic disease interaction matrix.

        Args:
            num_diseases: Number of diseases to generate

        Returns:
            Dict of disease interactions
        """
        interactions = {}
        diseases = [f"Disease_{i}" for i in range(num_diseases)]

        for i in range(len(diseases)):
            for j in range(i + 1, len(diseases)):
                d1, d2 = diseases[i], diseases[j]

                # Assign interaction type probabilistically
                interaction_type = [
                    InteractionType.CASCADE,
                    InteractionType.SYNERGISTIC,
                    InteractionType.SECONDARY,
                    InteractionType.SHARED_PATHWAY,
                    InteractionType.INDEPENDENT,
                ][i % 5]

                interactions[(d1, d2)] = DiseaseInteraction(
                    disease_a=d1,
                    disease_b=d2,
                    interaction_type=interaction_type,
                    base_probability=0.3 + (i * j % 100) / 200,  # 0.3-0.8
                    mechanism=f"mechanism_{i}_{j}",
                    age_factor=0.9 + (i % 5) * 0.1,
                    severity_factor=0.8 + (j % 5) * 0.1,
                )

        return interactions

    def benchmark_expansion_by_dataset_size(self):
        """Benchmark expansion with varying dataset sizes."""
        print("\n📊 Benchmark: Expansion by Dataset Size")
        print("-" * 60)

        sizes = [10, 20, 30, 50, 75, 100]

        for size in sizes:
            interactions = self.generate_disease_interactions(size)
            expander = MultiDiseaseExpander(interactions)

            # Select subset for expansion
            all_diseases = []
            for (d1, d2) in interactions.keys():
                if d1 not in all_diseases:
                    all_diseases.append(d1)
                if d2 not in all_diseases:
                    all_diseases.append(d2)

            expand_diseases = all_diseases[:min(6, len(all_diseases))]

            start_time = time.time()
            patterns = expander.expand_combinations(expand_diseases, min_combined_prob=0.1)
            elapsed_ms = (time.time() - start_time) * 1000

            num_combinations = len(patterns)
            cps = num_combinations / (elapsed_ms / 1000) if elapsed_ms > 0 else 0

            result = BenchmarkResult(
                test_name=f"Expansion (size={size})",
                dataset_size=size,
                num_combinations=num_combinations,
                execution_time_ms=elapsed_ms,
                combinations_per_second=cps,
            )

            self.results.append(result)
            print(f"Size: {size:3d} | Time: {elapsed_ms:8.2f}ms | "
                  f"Combos: {num_combinations:4d} | Speed: {cps:8.1f} combos/sec")

    def benchmark_complexity_calculation(self):
        """Benchmark complexity score calculation."""
        print("\n📊 Benchmark: Complexity Calculation")
        print("-" * 60)

        interactions = self.generate_disease_interactions(30)
        expander = MultiDiseaseExpander(interactions)

        # Create test combinations of varying sizes
        sizes = [2, 3, 4, 5, 6]
        all_diseases = list(set(
            d for pair in interactions.keys()
            for d in pair
        ))[:15]

        for size in sizes:
            test_combos = [tuple(all_diseases[i:i+size]) for i in range(5)]

            start_time = time.time()
            for combo in test_combos:
                pattern = expander._score_combination(combo)
            elapsed_ms = (time.time() - start_time) * 1000

            cps = len(test_combos) / (elapsed_ms / 1000) if elapsed_ms > 0 else 0

            result = BenchmarkResult(
                test_name=f"Complexity (size={size})",
                dataset_size=len(interactions),
                num_combinations=len(test_combos),
                execution_time_ms=elapsed_ms,
                combinations_per_second=cps,
            )

            self.results.append(result)
            print(f"Combo Size: {size} | Time: {elapsed_ms:8.2f}ms | "
                  f"Calcs: {len(test_combos):4d} | Speed: {cps:8.1f} calcs/sec")

    def benchmark_rule_mining(self):
        """Benchmark association rule mining."""
        print("\n📊 Benchmark: Rule Mining")
        print("-" * 60)

        pattern_counts = [10, 25, 50, 100, 200]

        for count in pattern_counts:
            interactions = self.generate_disease_interactions(20)
            expander = MultiDiseaseExpander(interactions)

            # Generate patterns
            all_diseases = list(set(
                d for pair in interactions.keys()
                for d in pair
            ))[:12]

            patterns = []
            for i in range(0, min(count, len(all_diseases) - 2)):
                diseases = tuple(all_diseases[i:i+3])
                pattern = expander._score_combination(diseases)
                if pattern:
                    patterns.append(pattern)

            # Benchmark mining
            miner = InteractionRuleMiner(min_support=0.1, min_confidence=0.3)

            start_time = time.time()
            rules = miner.mine_rules(patterns)
            elapsed_ms = (time.time() - start_time) * 1000

            rps = len(rules) / (elapsed_ms / 1000) if elapsed_ms > 0 else 0

            result = BenchmarkResult(
                test_name=f"Rule Mining (patterns={len(patterns)})",
                dataset_size=len(patterns),
                num_combinations=len(rules),
                execution_time_ms=elapsed_ms,
                combinations_per_second=rps,
            )

            self.results.append(result)
            print(f"Patterns: {len(patterns):3d} | Time: {elapsed_ms:8.2f}ms | "
                  f"Rules: {len(rules):4d} | Speed: {rps:8.1f} rules/sec")

    def benchmark_clustering(self):
        """Benchmark disease clustering."""
        print("\n📊 Benchmark: Disease Clustering")
        print("-" * 60)

        sizes = [20, 50, 100, 150, 200]

        for size in sizes:
            interactions = self.generate_disease_interactions(size)

            start_time = time.time()
            expander = MultiDiseaseExpander(interactions)
            elapsed_ms = (time.time() - start_time) * 1000

            num_clusters = len(expander.disease_clusters)
            cps = size / (elapsed_ms / 1000) if elapsed_ms > 0 else 0

            result = BenchmarkResult(
                test_name=f"Clustering (diseases={size})",
                dataset_size=size,
                num_combinations=num_clusters,
                execution_time_ms=elapsed_ms,
                combinations_per_second=cps,
            )

            self.results.append(result)
            print(f"Diseases: {size:3d} | Time: {elapsed_ms:8.2f}ms | "
                  f"Clusters: {num_clusters:3d} | Speed: {cps:8.1f} diseases/sec")

    def benchmark_network_analysis(self):
        """Benchmark network analysis."""
        print("\n📊 Benchmark: Network Analysis")
        print("-" * 60)

        interactions = self.generate_disease_interactions(50)
        expander = MultiDiseaseExpander(interactions)

        # Generate patterns first
        all_diseases = list(set(
            d for pair in interactions.keys()
            for d in pair
        ))[:12]

        for i in range(0, len(all_diseases) - 2):
            diseases = tuple(all_diseases[i:i+3])
            expander._score_combination(diseases)

        # Benchmark analysis
        start_time = time.time()
        network = expander.analyze_disease_network()
        elapsed_ms = (time.time() - start_time) * 1000

        result = BenchmarkResult(
            test_name="Network Analysis",
            dataset_size=len(expander.combination_patterns),
            num_combinations=network.get("total_combinations", 0),
            execution_time_ms=elapsed_ms,
            combinations_per_second=0,
        )

        self.results.append(result)
        print(f"Time: {elapsed_ms:8.2f}ms")
        print(f"Network Stats: {json.dumps(network, indent=2)}")

    def benchmark_memory_usage(self):
        """Benchmark memory usage for different dataset sizes."""
        print("\n📊 Benchmark: Memory Usage")
        print("-" * 60)

        import sys

        sizes = [10, 20, 50, 100]

        for size in sizes:
            interactions = self.generate_disease_interactions(size)

            # Measure size of interaction matrix
            matrix_size = sys.getsizeof(interactions)
            for key, value in interactions.items():
                matrix_size += sys.getsizeof(key) + sys.getsizeof(value)

            expander = MultiDiseaseExpander(interactions)

            # Measure expander memory
            expander_size = sys.getsizeof(expander)
            expander_size += sys.getsizeof(expander.combination_patterns)

            total_mb = (matrix_size + expander_size) / (1024 * 1024)

            print(f"Size: {size:3d} | Matrix: {matrix_size:10d} bytes | "
                  f"Expander: {expander_size:10d} bytes | "
                  f"Total: {total_mb:6.2f} MB")

    def run_all_benchmarks(self):
        """Run all benchmarks."""
        print("=" * 60)
        print("🚀 MultiDiseaseExpander Performance Benchmarks")
        print("=" * 60)

        self.benchmark_expansion_by_dataset_size()
        self.benchmark_complexity_calculation()
        self.benchmark_rule_mining()
        self.benchmark_clustering()
        self.benchmark_network_analysis()
        self.benchmark_memory_usage()

        self.print_summary()

    def print_summary(self):
        """Print benchmark summary."""
        print("\n" + "=" * 60)
        print("📈 Summary")
        print("=" * 60)

        if not self.results:
            print("No results collected")
            return

        print(f"Total benchmarks run: {len(self.results)}")
        print(f"Average execution time: {sum(r.execution_time_ms for r in self.results) / len(self.results):.2f}ms")

        fastest = min(self.results, key=lambda r: r.execution_time_ms)
        slowest = max(self.results, key=lambda r: r.execution_time_ms)

        print(f"\nFastest: {fastest.test_name} ({fastest.execution_time_ms:.2f}ms)")
        print(f"Slowest: {slowest.test_name} ({slowest.execution_time_ms:.2f}ms)")

        # Print results in JSON
        print("\nDetailed Results (JSON):")
        results_json = [r.to_dict() for r in self.results]
        print(json.dumps(results_json, indent=2))


def main():
    """Run benchmark suite."""
    suite = BenchmarkSuite()
    suite.run_all_benchmarks()


if __name__ == "__main__":
    main()
