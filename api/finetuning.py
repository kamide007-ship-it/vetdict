#!/usr/bin/env python3
"""
ShowDog Analysis Platform - Fine-Tuning Infrastructure

This module implements the infrastructure for training breed-specific evaluation
models on FCI show dog data. It provides:

  - Training data schema and dataset management (splits, augmentation, stats)
  - Model registry with version tracking, comparison, and selection
  - Training pipeline configuration with breed-specific overrides
  - Evaluation pipeline with full metric computation (MAE, accuracy, correlation,
    confusion matrix, statistical significance testing)
  - Inference wrapper with fallback chain (breed-specific -> universal -> prompt-based)
  - Data collection and validation utilities

IMPORTANT: This is the infrastructure layer only. Actual model training requires
an ML framework (PyTorch, TensorFlow, etc.) to be plugged in via the
TrainingPipeline.train() hook. All other components (data management, evaluation,
inference routing, metrics) are fully implemented using only the standard library.

Model metadata is persisted as JSON files under a configurable storage directory.
"""

import hashlib
import json
import logging
import math
import os
import random
import statistics
import time
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# =============================================================================
# CONSTANTS
# =============================================================================

SCORING_AXES = ["skeletal", "gait", "muscle", "coat", "temperament"]

# FCI grading scale (ordinal)
FCI_GRADES = ["Excellent", "Very Good", "Good", "Sufficient", "Disqualified"]
FCI_GRADE_TO_INT = {grade: i for i, grade in enumerate(FCI_GRADES)}
FCI_INT_TO_GRADE = {i: grade for i, grade in enumerate(FCI_GRADES)}

JUDGE_CERTIFICATION_LEVELS = ["Trainee", "National", "International", "FCI-All-Breed"]

DEFAULT_STORAGE_DIR = os.path.join(os.path.dirname(__file__), ".finetuning_data")

AUGMENTATION_DESCRIPTORS = [
    "rotation_-15_to_15",
    "brightness_0.7_to_1.3",
    "horizontal_flip",
    "crop_90_percent_center",
    "crop_85_percent_random",
    "gaussian_blur_sigma_0.5_to_1.5",
    "contrast_0.8_to_1.2",
    "saturation_0.8_to_1.2",
]


# =============================================================================
# TRAINING DATA SCHEMA
# =============================================================================

class TrainingExample:
    """
    A single training example pairing an image with judge evaluation data.

    Attributes:
        example_id:                 Unique identifier (auto-generated UUID).
        image_path:                 Path to the image file on disk.
        breed_id:                   Breed key from breeds.py (e.g. '172d_poodle_toy').
        judge_scores:               Dict mapping each of the 5 scoring axes to a
                                    float score in [0, 100].
        judge_grade:                FCI grade string (one of FCI_GRADES).
        show_name:                  Name of the dog show where judging took place.
        show_date:                  ISO-8601 date string (YYYY-MM-DD).
        judge_name:                 Name of the judge who provided the scores.
        judge_certification_level:  One of JUDGE_CERTIFICATION_LEVELS.
        augmentations:              List of augmentation descriptors applied.
        metadata:                   Arbitrary extra metadata dict.
    """

    __slots__ = (
        "example_id", "image_path", "breed_id", "judge_scores", "judge_grade",
        "show_name", "show_date", "judge_name", "judge_certification_level",
        "augmentations", "metadata",
    )

    def __init__(
        self,
        image_path: str,
        breed_id: str,
        judge_scores: Dict[str, float],
        judge_grade: str,
        show_name: str = "",
        show_date: str = "",
        judge_name: str = "",
        judge_certification_level: str = "National",
        augmentations: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        example_id: Optional[str] = None,
    ):
        self.example_id = example_id or uuid.uuid4().hex[:12]
        self.image_path = image_path
        self.breed_id = breed_id

        # Validate scores
        for axis in SCORING_AXES:
            if axis not in judge_scores:
                raise ValueError(f"Missing score for axis '{axis}'")
            val = judge_scores[axis]
            if not isinstance(val, (int, float)) or val < 0 or val > 100:
                raise ValueError(
                    f"Score for '{axis}' must be a number in [0, 100], got {val}"
                )
        self.judge_scores = dict(judge_scores)

        if judge_grade not in FCI_GRADES:
            raise ValueError(
                f"Invalid grade '{judge_grade}'. Must be one of {FCI_GRADES}"
            )
        self.judge_grade = judge_grade

        self.show_name = show_name
        self.show_date = show_date
        self.judge_name = judge_name

        if judge_certification_level not in JUDGE_CERTIFICATION_LEVELS:
            raise ValueError(
                f"Invalid certification level '{judge_certification_level}'. "
                f"Must be one of {JUDGE_CERTIFICATION_LEVELS}"
            )
        self.judge_certification_level = judge_certification_level

        self.augmentations = list(augmentations) if augmentations else []
        self.metadata = dict(metadata) if metadata else {}

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a JSON-compatible dictionary."""
        return {
            "example_id": self.example_id,
            "image_path": self.image_path,
            "breed_id": self.breed_id,
            "judge_scores": self.judge_scores,
            "judge_grade": self.judge_grade,
            "show_name": self.show_name,
            "show_date": self.show_date,
            "judge_name": self.judge_name,
            "judge_certification_level": self.judge_certification_level,
            "augmentations": self.augmentations,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TrainingExample":
        """Deserialize from a dictionary."""
        return cls(
            image_path=d["image_path"],
            breed_id=d["breed_id"],
            judge_scores=d["judge_scores"],
            judge_grade=d["judge_grade"],
            show_name=d.get("show_name", ""),
            show_date=d.get("show_date", ""),
            judge_name=d.get("judge_name", ""),
            judge_certification_level=d.get("judge_certification_level", "National"),
            augmentations=d.get("augmentations"),
            metadata=d.get("metadata"),
            example_id=d.get("example_id"),
        )

    def __repr__(self) -> str:
        return (
            f"TrainingExample(id={self.example_id}, breed={self.breed_id}, "
            f"grade={self.judge_grade})"
        )


# =============================================================================
# DATASET MANAGER
# =============================================================================

class DatasetSplit:
    """
    Named container for a train/validation/test split.

    Attributes:
        name:      Split name ('train', 'validation', or 'test').
        examples:  List of TrainingExample in this split.
    """

    def __init__(self, name: str, examples: Optional[List[TrainingExample]] = None):
        if name not in ("train", "validation", "test"):
            raise ValueError(f"Split name must be train/validation/test, got '{name}'")
        self.name = name
        self.examples: List[TrainingExample] = list(examples) if examples else []

    def __len__(self) -> int:
        return len(self.examples)

    def __repr__(self) -> str:
        return f"DatasetSplit(name={self.name}, n={len(self.examples)})"


class DatasetManager:
    """
    Manages training data: storage, splitting, augmentation descriptors, and
    dataset-level statistics.

    The manager keeps an in-memory list of all examples and can persist them to
    a JSON file.  Splits are created on demand via stratified sampling keyed on
    (breed_id, judge_grade).

    Args:
        storage_dir:  Directory where dataset JSON files are written.
    """

    def __init__(self, storage_dir: str = DEFAULT_STORAGE_DIR):
        self.storage_dir = storage_dir
        self.examples: List[TrainingExample] = []
        self._ensure_dir(self.storage_dir)

    # -- persistence ----------------------------------------------------------

    @staticmethod
    def _ensure_dir(path: str) -> None:
        os.makedirs(path, exist_ok=True)

    def save(self, filename: str = "dataset.json") -> str:
        """Save all examples to a JSON file. Returns the file path."""
        path = os.path.join(self.storage_dir, filename)
        data = {
            "version": "1.0",
            "created": datetime.now(timezone.utc).isoformat(),
            "count": len(self.examples),
            "examples": [ex.to_dict() for ex in self.examples],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info("Dataset saved to %s (%d examples)", path, len(self.examples))
        return path

    def load(self, filename: str = "dataset.json") -> int:
        """Load examples from a JSON file. Returns the number loaded."""
        path = os.path.join(self.storage_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.examples = [TrainingExample.from_dict(d) for d in data["examples"]]
        logger.info("Dataset loaded from %s (%d examples)", path, len(self.examples))
        return len(self.examples)

    # -- data collection ------------------------------------------------------

    def add_example(self, example: TrainingExample) -> None:
        """Add a single training example after validation."""
        self.examples.append(example)

    def add_examples(self, examples: List[TrainingExample]) -> int:
        """Add multiple examples. Returns count added."""
        self.examples.extend(examples)
        return len(examples)

    # -- stratified splitting -------------------------------------------------

    def create_splits(
        self,
        train_ratio: float = 0.7,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        seed: int = 42,
    ) -> Tuple[DatasetSplit, DatasetSplit, DatasetSplit]:
        """
        Create stratified train/validation/test splits.

        Stratification key is (breed_id, judge_grade) so that every stratum is
        represented proportionally in each split.  When a stratum has fewer than
        3 examples, all go to the training set to avoid empty strata.

        Args:
            train_ratio:  Fraction for training (default 0.70).
            val_ratio:    Fraction for validation (default 0.15).
            test_ratio:   Fraction for test (default 0.15).
            seed:         Random seed for reproducibility.

        Returns:
            Tuple of (train_split, val_split, test_split).
        """
        total = train_ratio + val_ratio + test_ratio
        if abs(total - 1.0) > 0.001:
            raise ValueError(
                f"Split ratios must sum to 1.0, got {total:.4f}"
            )

        rng = random.Random(seed)

        # Group by stratification key
        strata: Dict[Tuple[str, str], List[TrainingExample]] = defaultdict(list)
        for ex in self.examples:
            key = (ex.breed_id, ex.judge_grade)
            strata[key].append(ex)

        train_ex: List[TrainingExample] = []
        val_ex: List[TrainingExample] = []
        test_ex: List[TrainingExample] = []

        for _key, group in sorted(strata.items()):
            rng.shuffle(group)
            n = len(group)

            if n < 3:
                # Too few to split meaningfully; keep all for training
                train_ex.extend(group)
                continue

            n_train = max(1, round(n * train_ratio))
            n_val = max(1, round(n * val_ratio))
            # Remainder goes to test
            n_test = n - n_train - n_val
            if n_test < 0:
                n_test = 0
                n_val = n - n_train

            train_ex.extend(group[:n_train])
            val_ex.extend(group[n_train: n_train + n_val])
            test_ex.extend(group[n_train + n_val:])

        # Final shuffle within each split
        rng.shuffle(train_ex)
        rng.shuffle(val_ex)
        rng.shuffle(test_ex)

        logger.info(
            "Splits created: train=%d, val=%d, test=%d",
            len(train_ex), len(val_ex), len(test_ex),
        )
        return (
            DatasetSplit("train", train_ex),
            DatasetSplit("validation", val_ex),
            DatasetSplit("test", test_ex),
        )

    # -- augmentation descriptors ---------------------------------------------

    @staticmethod
    def augmentation_descriptors(
        include: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Return the list of data augmentation descriptors to be applied during
        training.  These are *descriptors* -- actual augmentation is performed
        by the training framework.

        Args:
            include:  Subset of AUGMENTATION_DESCRIPTORS to use.  If None, all
                      are returned.
        """
        if include is not None:
            unknown = set(include) - set(AUGMENTATION_DESCRIPTORS)
            if unknown:
                raise ValueError(f"Unknown augmentation descriptors: {unknown}")
            return list(include)
        return list(AUGMENTATION_DESCRIPTORS)

    # -- dataset statistics ---------------------------------------------------

    def compute_statistics(self) -> Dict[str, Any]:
        """
        Compute dataset-level statistics.

        Returns a dict with:
          - total_examples
          - samples_per_breed        : {breed_id: count}
          - grade_distribution       : {grade: count}
          - judge_diversity          : {judge_name: count}
          - certification_distribution: {level: count}
          - per_axis_score_stats     : {axis: {mean, std, min, max}}
          - shows                    : list of unique show names
        """
        stats: Dict[str, Any] = {
            "total_examples": len(self.examples),
            "samples_per_breed": defaultdict(int),
            "grade_distribution": defaultdict(int),
            "judge_diversity": defaultdict(int),
            "certification_distribution": defaultdict(int),
            "per_axis_score_stats": {},
            "shows": set(),
        }

        axis_values: Dict[str, List[float]] = {ax: [] for ax in SCORING_AXES}

        for ex in self.examples:
            stats["samples_per_breed"][ex.breed_id] += 1
            stats["grade_distribution"][ex.judge_grade] += 1
            if ex.judge_name:
                stats["judge_diversity"][ex.judge_name] += 1
            stats["certification_distribution"][ex.judge_certification_level] += 1
            if ex.show_name:
                stats["shows"].add(ex.show_name)
            for axis in SCORING_AXES:
                axis_values[axis].append(ex.judge_scores[axis])

        for axis in SCORING_AXES:
            vals = axis_values[axis]
            if vals:
                stats["per_axis_score_stats"][axis] = {
                    "mean": statistics.mean(vals),
                    "std": statistics.pstdev(vals) if len(vals) > 1 else 0.0,
                    "min": min(vals),
                    "max": max(vals),
                }
            else:
                stats["per_axis_score_stats"][axis] = {
                    "mean": 0, "std": 0, "min": 0, "max": 0,
                }

        # Convert defaultdicts and sets for JSON serialisation
        stats["samples_per_breed"] = dict(stats["samples_per_breed"])
        stats["grade_distribution"] = dict(stats["grade_distribution"])
        stats["judge_diversity"] = dict(stats["judge_diversity"])
        stats["certification_distribution"] = dict(stats["certification_distribution"])
        stats["shows"] = sorted(stats["shows"])

        return stats

    # -- data quality validation ----------------------------------------------

    def validate_quality(self) -> Dict[str, Any]:
        """
        Check training data for quality issues.

        Returns a report dict with:
          - missing_fields   : list of (example_id, field_name)
          - outlier_scores   : list of (example_id, axis, value) for |z|>3
          - duplicate_images : list of image_path that appear more than once
          - total_issues     : int
        """
        report: Dict[str, Any] = {
            "missing_fields": [],
            "outlier_scores": [],
            "duplicate_images": [],
            "total_issues": 0,
        }

        # Check missing fields
        for ex in self.examples:
            if not ex.image_path:
                report["missing_fields"].append((ex.example_id, "image_path"))
            if not ex.breed_id:
                report["missing_fields"].append((ex.example_id, "breed_id"))
            if not ex.show_name:
                report["missing_fields"].append((ex.example_id, "show_name"))
            if not ex.show_date:
                report["missing_fields"].append((ex.example_id, "show_date"))
            if not ex.judge_name:
                report["missing_fields"].append((ex.example_id, "judge_name"))

        # Outlier detection: z-score > 3 per axis
        axis_values: Dict[str, List[float]] = {ax: [] for ax in SCORING_AXES}
        for ex in self.examples:
            for ax in SCORING_AXES:
                axis_values[ax].append(ex.judge_scores[ax])

        axis_stats: Dict[str, Tuple[float, float]] = {}
        for ax in SCORING_AXES:
            vals = axis_values[ax]
            if len(vals) > 1:
                mu = statistics.mean(vals)
                sd = statistics.pstdev(vals)
                axis_stats[ax] = (mu, sd)
            else:
                axis_stats[ax] = (0.0, 0.0)

        for ex in self.examples:
            for ax in SCORING_AXES:
                mu, sd = axis_stats[ax]
                if sd > 0:
                    z = abs(ex.judge_scores[ax] - mu) / sd
                    if z > 3.0:
                        report["outlier_scores"].append(
                            (ex.example_id, ax, ex.judge_scores[ax])
                        )

        # Duplicate images
        image_counts: Dict[str, int] = defaultdict(int)
        for ex in self.examples:
            image_counts[ex.image_path] += 1
        report["duplicate_images"] = [
            path for path, cnt in image_counts.items() if cnt > 1
        ]

        report["total_issues"] = (
            len(report["missing_fields"])
            + len(report["outlier_scores"])
            + len(report["duplicate_images"])
        )
        return report


# =============================================================================
# MODEL REGISTRY
# =============================================================================

class ModelVersion:
    """
    Represents a single version of a fine-tuned model.

    Attributes:
        version_id:            Unique version identifier (auto-generated).
        base_model:            Name/ID of the base model fine-tuned from.
        breed_id:              Breed key, or None for a universal model.
        training_date:         ISO-8601 datetime of training completion.
        metrics:               Dict of evaluation metrics.
        status:                One of 'training', 'validated', 'production',
                               'deprecated'.
        hyperparameters:       Dict of training hyperparameters used.
        dataset_version:       Identifier/hash of the dataset used for training.
        notes:                 Free-text notes.
    """

    VALID_STATUSES = ("training", "validated", "production", "deprecated")

    def __init__(
        self,
        base_model: str,
        breed_id: Optional[str] = None,
        metrics: Optional[Dict[str, Any]] = None,
        status: str = "training",
        hyperparameters: Optional[Dict[str, Any]] = None,
        dataset_version: str = "",
        notes: str = "",
        version_id: Optional[str] = None,
        training_date: Optional[str] = None,
    ):
        self.version_id = version_id or f"v-{uuid.uuid4().hex[:8]}"
        self.base_model = base_model
        self.breed_id = breed_id
        self.training_date = training_date or datetime.now(timezone.utc).isoformat()
        self.metrics = dict(metrics) if metrics else {}
        if status not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid status '{status}'. Must be one of {self.VALID_STATUSES}"
            )
        self.status = status
        self.hyperparameters = dict(hyperparameters) if hyperparameters else {}
        self.dataset_version = dataset_version
        self.notes = notes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version_id": self.version_id,
            "base_model": self.base_model,
            "breed_id": self.breed_id,
            "training_date": self.training_date,
            "metrics": self.metrics,
            "status": self.status,
            "hyperparameters": self.hyperparameters,
            "dataset_version": self.dataset_version,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ModelVersion":
        return cls(
            base_model=d["base_model"],
            breed_id=d.get("breed_id"),
            metrics=d.get("metrics"),
            status=d.get("status", "training"),
            hyperparameters=d.get("hyperparameters"),
            dataset_version=d.get("dataset_version", ""),
            notes=d.get("notes", ""),
            version_id=d.get("version_id"),
            training_date=d.get("training_date"),
        )

    def __repr__(self) -> str:
        breed = self.breed_id or "universal"
        return (
            f"ModelVersion({self.version_id}, base={self.base_model}, "
            f"breed={breed}, status={self.status})"
        )


class ModelRegistry:
    """
    Tracks all model versions, supports comparison, and selects the best model
    for a given breed based on validation metrics.

    Model metadata is stored as a single JSON file (registry.json) inside the
    storage directory.

    Args:
        storage_dir:  Directory for persisting registry data.
    """

    def __init__(self, storage_dir: str = DEFAULT_STORAGE_DIR):
        self.storage_dir = storage_dir
        self.models: Dict[str, ModelVersion] = {}
        os.makedirs(self.storage_dir, exist_ok=True)

    # -- persistence ----------------------------------------------------------

    def save(self, filename: str = "registry.json") -> str:
        path = os.path.join(self.storage_dir, filename)
        data = {
            "version": "1.0",
            "updated": datetime.now(timezone.utc).isoformat(),
            "models": {vid: mv.to_dict() for vid, mv in self.models.items()},
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path

    def load(self, filename: str = "registry.json") -> int:
        path = os.path.join(self.storage_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.models = {
            vid: ModelVersion.from_dict(md)
            for vid, md in data["models"].items()
        }
        return len(self.models)

    # -- registration ---------------------------------------------------------

    def register(self, model: ModelVersion) -> str:
        """Register a new model version. Returns the version_id."""
        if model.version_id in self.models:
            raise ValueError(f"Model version '{model.version_id}' already registered")
        self.models[model.version_id] = model
        logger.info("Registered model %s", model.version_id)
        return model.version_id

    def update_status(self, version_id: str, new_status: str) -> None:
        """Update the status of a registered model."""
        if version_id not in self.models:
            raise KeyError(f"Model version '{version_id}' not found")
        if new_status not in ModelVersion.VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'")
        old = self.models[version_id].status
        self.models[version_id].status = new_status
        logger.info(
            "Model %s status: %s -> %s", version_id, old, new_status
        )

    def update_metrics(self, version_id: str, metrics: Dict[str, Any]) -> None:
        """Update metrics for a registered model."""
        if version_id not in self.models:
            raise KeyError(f"Model version '{version_id}' not found")
        self.models[version_id].metrics.update(metrics)

    # -- querying -------------------------------------------------------------

    def get(self, version_id: str) -> ModelVersion:
        if version_id not in self.models:
            raise KeyError(f"Model version '{version_id}' not found")
        return self.models[version_id]

    def list_models(
        self,
        breed_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[ModelVersion]:
        """List models, optionally filtered by breed and/or status."""
        result = list(self.models.values())
        if breed_id is not None:
            result = [m for m in result if m.breed_id == breed_id]
        if status is not None:
            result = [m for m in result if m.status == status]
        return sorted(result, key=lambda m: m.training_date, reverse=True)

    # -- comparison and selection ---------------------------------------------

    def compare(
        self, version_a: str, version_b: str
    ) -> Dict[str, Any]:
        """
        A/B comparison between two model versions based on their stored metrics.

        Returns a dict with each metric key and which version is better
        (lower MAE is better; higher accuracy / correlation is better).
        """
        ma = self.get(version_a)
        mb = self.get(version_b)

        # Metrics where lower is better
        lower_is_better = {"mae_overall"}
        for ax in SCORING_AXES:
            lower_is_better.add(f"mae_{ax}")

        comparison: Dict[str, Any] = {"version_a": version_a, "version_b": version_b}
        all_keys = set(ma.metrics.keys()) | set(mb.metrics.keys())

        for key in sorted(all_keys):
            val_a = ma.metrics.get(key)
            val_b = mb.metrics.get(key)
            if val_a is None or val_b is None:
                comparison[key] = {
                    "a": val_a, "b": val_b, "winner": None, "note": "metric missing",
                }
                continue
            if not isinstance(val_a, (int, float)) or not isinstance(val_b, (int, float)):
                comparison[key] = {"a": val_a, "b": val_b, "winner": None}
                continue

            if key in lower_is_better:
                winner = version_a if val_a < val_b else version_b
            else:
                winner = version_a if val_a > val_b else version_b

            comparison[key] = {
                "a": val_a,
                "b": val_b,
                "diff": round(val_a - val_b, 6),
                "winner": winner,
            }

        return comparison

    def select_best(
        self,
        breed_id: Optional[str] = None,
        primary_metric: str = "mae_overall",
        lower_is_better: bool = True,
    ) -> Optional[ModelVersion]:
        """
        Automatically select the best validated/production model for a breed
        based on a primary validation metric.

        Args:
            breed_id:        Breed to select for (None = universal).
            primary_metric:  Metric key to rank by.
            lower_is_better: If True, lower metric value wins.

        Returns:
            The best ModelVersion, or None if no candidate exists.
        """
        candidates = [
            m for m in self.models.values()
            if m.breed_id == breed_id
            and m.status in ("validated", "production")
            and primary_metric in m.metrics
        ]
        if not candidates:
            return None

        candidates.sort(
            key=lambda m: m.metrics[primary_metric],
            reverse=not lower_is_better,
        )
        return candidates[0]

    def promote_to_production(self, version_id: str) -> None:
        """
        Promote a model to production status.  Any previously active production
        model for the same breed is deprecated.
        """
        model = self.get(version_id)
        if model.status not in ("validated", "production"):
            raise ValueError(
                f"Can only promote validated models, current status: {model.status}"
            )

        # Deprecate existing production models for this breed
        for m in self.models.values():
            if (
                m.breed_id == model.breed_id
                and m.status == "production"
                and m.version_id != version_id
            ):
                m.status = "deprecated"
                logger.info("Deprecated model %s (replaced by %s)", m.version_id, version_id)

        model.status = "production"
        logger.info("Promoted model %s to production", version_id)


# =============================================================================
# TRAINING PIPELINE CONFIGURATION
# =============================================================================

class FineTuningConfig:
    """
    Configuration for a fine-tuning training run.

    Attributes:
        base_model:     Name/path of the pretrained model to fine-tune.
        learning_rate:  Initial learning rate.
        epochs:         Number of training epochs.
        batch_size:     Training batch size.
        warmup_steps:   Number of LR warmup steps.
        weight_decay:   L2 regularisation coefficient.
        breed_id:       If set, this is a breed-specific config.
        augmentations:  List of augmentation descriptors to apply.
        kfold:          Number of cross-validation folds (0 = no CV).
        extra:          Arbitrary extra parameters.
    """

    def __init__(
        self,
        base_model: str = "showdog-base-v1",
        learning_rate: float = 2e-5,
        epochs: int = 10,
        batch_size: int = 16,
        warmup_steps: int = 100,
        weight_decay: float = 0.01,
        breed_id: Optional[str] = None,
        augmentations: Optional[List[str]] = None,
        kfold: int = 0,
        extra: Optional[Dict[str, Any]] = None,
    ):
        self.base_model = base_model
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size
        self.warmup_steps = warmup_steps
        self.weight_decay = weight_decay
        self.breed_id = breed_id
        self.augmentations = augmentations or list(AUGMENTATION_DESCRIPTORS)
        self.kfold = kfold
        self.extra = extra or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "base_model": self.base_model,
            "learning_rate": self.learning_rate,
            "epochs": self.epochs,
            "batch_size": self.batch_size,
            "warmup_steps": self.warmup_steps,
            "weight_decay": self.weight_decay,
            "breed_id": self.breed_id,
            "augmentations": self.augmentations,
            "kfold": self.kfold,
            "extra": self.extra,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "FineTuningConfig":
        return cls(**d)

    @classmethod
    def breed_specific(cls, breed_id: str, **overrides) -> "FineTuningConfig":
        """
        Create a breed-specific config with sensible defaults and optional
        overrides.  Breed-specific configs use a lower learning rate and more
        epochs by default (transfer learning from universal model).
        """
        defaults = {
            "base_model": "showdog-universal-v1",
            "learning_rate": 1e-5,
            "epochs": 20,
            "batch_size": 8,
            "warmup_steps": 50,
            "weight_decay": 0.01,
            "breed_id": breed_id,
            "kfold": 5,
        }
        defaults.update(overrides)
        return cls(**defaults)

    def __repr__(self) -> str:
        breed = self.breed_id or "universal"
        return (
            f"FineTuningConfig(base={self.base_model}, breed={breed}, "
            f"lr={self.learning_rate}, epochs={self.epochs})"
        )


class TrainingPipeline:
    """
    Orchestrates a fine-tuning run.

    This class defines the execution flow.  Actual model training is delegated
    to a pluggable ``train_fn`` callback.  If no callback is provided, a mock
    training function is used that simulates metrics.

    Usage::

        pipeline = TrainingPipeline(config, dataset_manager, registry)
        version_id = pipeline.run()

    Args:
        config:           FineTuningConfig for this run.
        dataset_manager:  DatasetManager with loaded training data.
        registry:         ModelRegistry to record results.
        train_fn:         Optional callable(config, train_split, val_split) ->
                          Dict[str, float] of metrics.  If None, mock training
                          is used.
    """

    def __init__(
        self,
        config: FineTuningConfig,
        dataset_manager: DatasetManager,
        registry: ModelRegistry,
        train_fn: Optional[Callable] = None,
    ):
        self.config = config
        self.dataset_manager = dataset_manager
        self.registry = registry
        self.train_fn = train_fn or self._mock_train

    # -- mock training --------------------------------------------------------

    @staticmethod
    def _mock_train(
        config: FineTuningConfig,
        train_split: DatasetSplit,
        val_split: DatasetSplit,
    ) -> Dict[str, float]:
        """
        Simulate a training run.  Produces plausible metrics based on dataset
        size -- larger datasets yield slightly better scores.

        Returns:
            Dict of metric_name -> value.
        """
        rng = random.Random(hash(config.base_model) + len(train_split))
        n = len(train_split)
        # More data -> lower MAE (with noise)
        base_mae = max(2.0, 8.0 - math.log2(max(n, 1)) * 0.5)

        metrics: Dict[str, float] = {}
        for axis in SCORING_AXES:
            noise = rng.uniform(-0.5, 0.5)
            metrics[f"mae_{axis}"] = round(base_mae + noise, 4)

        metrics["mae_overall"] = round(
            statistics.mean(metrics[f"mae_{ax}"] for ax in SCORING_AXES), 4
        )
        metrics["grade_accuracy_exact"] = round(
            min(0.95, 0.4 + math.log2(max(n, 1)) * 0.05 + rng.uniform(-0.02, 0.02)), 4
        )
        metrics["grade_accuracy_pm1"] = round(
            min(0.99, metrics["grade_accuracy_exact"] + 0.15 + rng.uniform(0, 0.05)), 4
        )
        for axis in SCORING_AXES:
            metrics[f"pearson_{axis}"] = round(
                min(0.99, 0.5 + math.log2(max(n, 1)) * 0.04 + rng.uniform(-0.03, 0.03)), 4
            )

        logger.info(
            "Mock training complete: MAE=%.4f, grade_acc=%.4f",
            metrics["mae_overall"], metrics["grade_accuracy_exact"],
        )
        return metrics

    # -- pipeline execution ---------------------------------------------------

    def run(self) -> str:
        """
        Execute the full training pipeline:

        1. Create dataset splits (or k-fold if configured).
        2. Run training (real or mock).
        3. Register the resulting model version.
        4. Return the version_id.

        For k-fold cross-validation, metrics are averaged across folds.
        """
        logger.info("Starting training pipeline: %s", self.config)

        # Create dataset hash for provenance
        dataset_hash = hashlib.sha256(
            json.dumps(
                [ex.example_id for ex in self.dataset_manager.examples],
                sort_keys=True,
            ).encode()
        ).hexdigest()[:12]

        if self.config.kfold > 1:
            metrics = self._run_kfold(self.config.kfold)
        else:
            train_split, val_split, _test_split = (
                self.dataset_manager.create_splits()
            )
            metrics = self.train_fn(self.config, train_split, val_split)

        # Register model
        model = ModelVersion(
            base_model=self.config.base_model,
            breed_id=self.config.breed_id,
            metrics=metrics,
            status="validated",
            hyperparameters=self.config.to_dict(),
            dataset_version=dataset_hash,
        )
        self.registry.register(model)
        logger.info("Pipeline complete. Model registered: %s", model.version_id)
        return model.version_id

    def _run_kfold(self, k: int) -> Dict[str, float]:
        """
        Run k-fold cross-validation by creating k different splits and
        averaging metrics across folds.
        """
        all_fold_metrics: List[Dict[str, float]] = []

        for fold in range(k):
            seed = 42 + fold
            train_split, val_split, _ = self.dataset_manager.create_splits(
                train_ratio=0.8, val_ratio=0.2, test_ratio=0.0, seed=seed,
            )
            fold_metrics = self.train_fn(self.config, train_split, val_split)
            all_fold_metrics.append(fold_metrics)
            logger.info("Fold %d/%d complete: MAE=%.4f",
                        fold + 1, k, fold_metrics.get("mae_overall", -1))

        # Average metrics across folds
        averaged: Dict[str, float] = {}
        all_keys = set()
        for fm in all_fold_metrics:
            all_keys.update(fm.keys())

        for key in all_keys:
            values = [fm[key] for fm in all_fold_metrics if key in fm]
            if values and all(isinstance(v, (int, float)) for v in values):
                averaged[key] = round(statistics.mean(values), 4)

        averaged["kfold_std_mae_overall"] = round(
            statistics.pstdev(
                [fm["mae_overall"] for fm in all_fold_metrics if "mae_overall" in fm]
            ), 4
        ) if len(all_fold_metrics) > 1 else 0.0

        return averaged


# =============================================================================
# EVALUATION PIPELINE
# =============================================================================

class EvaluationPipeline:
    """
    Fully implemented evaluation pipeline that computes metrics comparing
    model predictions against ground-truth judge evaluations.

    All metric computations use only the standard library.

    Metrics computed:
      - MAE (Mean Absolute Error) per axis and overall
      - Grade accuracy (exact match)
      - Grade accuracy +/- 1 (within one grade step)
      - Pearson correlation per axis
      - Confusion matrix for grade prediction
      - Statistical significance tests (paired t-test, McNemar's test)
    """

    def __init__(self):
        pass

    # -- core metrics ---------------------------------------------------------

    @staticmethod
    def mean_absolute_error(
        predictions: List[float], targets: List[float]
    ) -> float:
        """Compute Mean Absolute Error between predictions and targets."""
        if len(predictions) != len(targets):
            raise ValueError("predictions and targets must have the same length")
        if not predictions:
            return 0.0
        return sum(abs(p - t) for p, t in zip(predictions, targets)) / len(predictions)

    @staticmethod
    def pearson_correlation(
        predictions: List[float], targets: List[float]
    ) -> float:
        """
        Compute Pearson correlation coefficient.

        Returns 0.0 if either series has zero variance (all identical values).
        """
        n = len(predictions)
        if n != len(targets):
            raise ValueError("predictions and targets must have the same length")
        if n < 2:
            return 0.0

        mean_p = sum(predictions) / n
        mean_t = sum(targets) / n

        cov = sum((p - mean_p) * (t - mean_t) for p, t in zip(predictions, targets))
        var_p = sum((p - mean_p) ** 2 for p in predictions)
        var_t = sum((t - mean_t) ** 2 for t in targets)

        denom = math.sqrt(var_p * var_t)
        if denom == 0:
            return 0.0
        return cov / denom

    @staticmethod
    def grade_accuracy(
        predicted_grades: List[str], true_grades: List[str]
    ) -> float:
        """Exact-match grade accuracy."""
        if len(predicted_grades) != len(true_grades):
            raise ValueError("Lists must have the same length")
        if not predicted_grades:
            return 0.0
        correct = sum(1 for p, t in zip(predicted_grades, true_grades) if p == t)
        return correct / len(predicted_grades)

    @staticmethod
    def grade_accuracy_pm1(
        predicted_grades: List[str], true_grades: List[str]
    ) -> float:
        """
        Grade accuracy allowing +/- 1 grade step.

        Uses the ordinal FCI grade ordering:
        Excellent(0) > Very Good(1) > Good(2) > Sufficient(3) > Disqualified(4)
        """
        if len(predicted_grades) != len(true_grades):
            raise ValueError("Lists must have the same length")
        if not predicted_grades:
            return 0.0
        correct = 0
        for p, t in zip(predicted_grades, true_grades):
            pi = FCI_GRADE_TO_INT.get(p)
            ti = FCI_GRADE_TO_INT.get(t)
            if pi is not None and ti is not None and abs(pi - ti) <= 1:
                correct += 1
        return correct / len(predicted_grades)

    @staticmethod
    def confusion_matrix(
        predicted_grades: List[str], true_grades: List[str]
    ) -> Dict[str, Any]:
        """
        Compute a confusion matrix for grade predictions.

        Returns:
            Dict with:
              - 'labels': list of grade labels (FCI_GRADES)
              - 'matrix': 2D list where matrix[true_idx][pred_idx] = count
              - 'per_class': {grade: {precision, recall, f1, support}}
        """
        n_classes = len(FCI_GRADES)
        matrix = [[0] * n_classes for _ in range(n_classes)]

        for p, t in zip(predicted_grades, true_grades):
            pi = FCI_GRADE_TO_INT.get(p)
            ti = FCI_GRADE_TO_INT.get(t)
            if pi is not None and ti is not None:
                matrix[ti][pi] += 1

        # Per-class precision, recall, F1
        per_class: Dict[str, Dict[str, float]] = {}
        for i, grade in enumerate(FCI_GRADES):
            tp = matrix[i][i]
            # Support = total actual instances of this class
            support = sum(matrix[i])
            # Predicted as this class
            pred_total = sum(matrix[row][i] for row in range(n_classes))

            precision = tp / pred_total if pred_total > 0 else 0.0
            recall = tp / support if support > 0 else 0.0
            f1 = (
                2 * precision * recall / (precision + recall)
                if (precision + recall) > 0
                else 0.0
            )
            per_class[grade] = {
                "precision": round(precision, 4),
                "recall": round(recall, 4),
                "f1": round(f1, 4),
                "support": support,
            }

        return {
            "labels": list(FCI_GRADES),
            "matrix": matrix,
            "per_class": per_class,
        }

    # -- statistical significance ---------------------------------------------

    @staticmethod
    def paired_t_test(
        errors_a: List[float], errors_b: List[float]
    ) -> Dict[str, float]:
        """
        Paired t-test to determine whether the mean difference between two sets
        of paired error measurements is statistically significant.

        Uses a two-tailed test.  Computes the t-statistic and an approximate
        p-value from the t-distribution using the standard library only
        (numerical approximation of the incomplete beta function).

        Args:
            errors_a:  Absolute errors from model A.
            errors_b:  Absolute errors from model B.

        Returns:
            Dict with 't_statistic', 'degrees_of_freedom', 'p_value',
            'mean_diff', 'significant_at_005'.
        """
        n = len(errors_a)
        if n != len(errors_b):
            raise ValueError("Both error lists must have the same length")
        if n < 2:
            return {
                "t_statistic": 0.0,
                "degrees_of_freedom": 0,
                "p_value": 1.0,
                "mean_diff": 0.0,
                "significant_at_005": False,
            }

        diffs = [a - b for a, b in zip(errors_a, errors_b)]
        mean_d = sum(diffs) / n
        var_d = sum((d - mean_d) ** 2 for d in diffs) / (n - 1)
        se = math.sqrt(var_d / n) if var_d > 0 else 0.0

        t_stat = 0.0 if se == 0 else mean_d / se

        df = n - 1
        p_value = EvaluationPipeline._t_distribution_p_value(t_stat, df)

        return {
            "t_statistic": round(t_stat, 6),
            "degrees_of_freedom": df,
            "p_value": round(p_value, 6),
            "mean_diff": round(mean_d, 6),
            "significant_at_005": p_value < 0.05,
        }

    @staticmethod
    def _t_distribution_p_value(t: float, df: int) -> float:
        """
        Approximate two-tailed p-value for a t-distribution using the
        regularised incomplete beta function.

        Uses the continued-fraction expansion of the incomplete beta function
        for numerical stability.
        """
        if df <= 0:
            return 1.0
        x = df / (df + t * t)
        p = EvaluationPipeline._regularized_incomplete_beta(
            df / 2.0, 0.5, x
        )
        return min(1.0, max(0.0, p))

    @staticmethod
    def _regularized_incomplete_beta(a: float, b: float, x: float) -> float:
        """
        Compute the regularised incomplete beta function I_x(a, b) using a
        continued fraction expansion (Lentz's algorithm).

        This is sufficient for computing t-distribution p-values.
        """
        if x < 0 or x > 1:
            return 0.0
        if x == 0:
            return 0.0
        if x == 1:
            return 1.0

        # Use symmetry relation if needed for convergence
        if x > (a + 1) / (a + b + 2):
            return 1.0 - EvaluationPipeline._regularized_incomplete_beta(b, a, 1.0 - x)

        # Log-beta for the prefactor
        ln_prefactor = (
            EvaluationPipeline._log_gamma(a + b)
            - EvaluationPipeline._log_gamma(a)
            - EvaluationPipeline._log_gamma(b)
            + a * math.log(x)
            + b * math.log(1.0 - x)
        )

        # Continued fraction (Lentz's method)
        eps = 1e-30
        max_iter = 200

        f = 1.0 + eps
        c = f
        d = 0.0

        for m in range(max_iter):
            if m == 0:
                numerator = 1.0
            elif m % 2 == 1:
                k = (m - 1) // 2 + 1
                numerator = -(a + k - 1 + k) * (a + k) * x / (
                    (a + 2 * k - 1) * (a + 2 * k)
                )  # odd term
                # Correction: use standard DLMF formula
                k_idx = (m + 1) // 2
                numerator = (
                    k_idx * (b - k_idx) * x
                    / ((a + 2 * k_idx - 1) * (a + 2 * k_idx))
                )
            else:
                k_idx = m // 2
                numerator = -(
                    (a + k_idx) * (a + b + k_idx) * x
                    / ((a + 2 * k_idx) * (a + 2 * k_idx + 1))
                )

            d = 1.0 + numerator * d
            if abs(d) < eps:
                d = eps
            d = 1.0 / d

            c = 1.0 + numerator / c
            if abs(c) < eps:
                c = eps

            delta = c * d
            f *= delta

            if abs(delta - 1.0) < 1e-10:
                break

        try:
            result = math.exp(ln_prefactor) * (f - 1.0) / a
        except (OverflowError, ValueError):
            result = 0.5

        return max(0.0, min(1.0, result))

    @staticmethod
    def _log_gamma(x: float) -> float:
        """Lanczos approximation to the log-gamma function."""
        if x <= 0:
            return 0.0
        coefficients = [
            76.18009172947146,
            -86.50532032941677,
            24.01409824083091,
            -1.231739572450155,
            0.1208650973866179e-2,
            -0.5395239384953e-5,
        ]
        y = x
        tmp = x + 5.5
        tmp -= (x - 0.5) * math.log(tmp)
        ser = 1.000000000190015
        for c in coefficients:
            y += 1
            ser += c / y
        return -tmp + math.log(2.5066282746310005 * ser / x)

    @staticmethod
    def mcnemars_test(
        correct_a: List[bool], correct_b: List[bool]
    ) -> Dict[str, Any]:
        """
        McNemar's test for paired nominal data -- tests whether two models
        differ in their classification accuracy on the same test set.

        Args:
            correct_a:  List of booleans (True = model A correct).
            correct_b:  List of booleans (True = model B correct).

        Returns:
            Dict with 'b_count' (A wrong, B right), 'c_count' (A right, B wrong),
            'chi2_statistic', 'p_value', 'significant_at_005'.
        """
        if len(correct_a) != len(correct_b):
            raise ValueError("Both lists must have the same length")

        # b = A wrong & B right, c = A right & B wrong
        b_count = sum(
            1 for a, b in zip(correct_a, correct_b) if not a and b
        )
        c_count = sum(
            1 for a, b in zip(correct_a, correct_b) if a and not b
        )

        total_discordant = b_count + c_count
        if total_discordant == 0:
            return {
                "b_count": b_count,
                "c_count": c_count,
                "chi2_statistic": 0.0,
                "p_value": 1.0,
                "significant_at_005": False,
            }

        # McNemar's chi-squared statistic (with continuity correction)
        chi2 = (abs(b_count - c_count) - 1) ** 2 / total_discordant

        # Approximate p-value from chi-squared distribution with 1 df
        # Using the complementary error function relation
        p_value = EvaluationPipeline._chi2_p_value_1df(chi2)

        return {
            "b_count": b_count,
            "c_count": c_count,
            "chi2_statistic": round(chi2, 6),
            "p_value": round(p_value, 6),
            "significant_at_005": p_value < 0.05,
        }

    @staticmethod
    def _chi2_p_value_1df(chi2: float) -> float:
        """
        Approximate p-value for chi-squared distribution with 1 degree of
        freedom using the complementary error function.

        P(X > chi2) = erfc(sqrt(chi2/2))  (for 1 df)
        """
        if chi2 <= 0:
            return 1.0
        return math.erfc(math.sqrt(chi2 / 2.0))

    # -- full evaluation run --------------------------------------------------

    def evaluate(
        self,
        predicted_scores: List[Dict[str, float]],
        true_scores: List[Dict[str, float]],
        predicted_grades: List[str],
        true_grades: List[str],
    ) -> Dict[str, Any]:
        """
        Run full evaluation and return all metrics.

        Args:
            predicted_scores:  List of dicts {axis: score} from the model.
            true_scores:       List of dicts {axis: score} from judges.
            predicted_grades:  List of predicted FCI grade strings.
            true_grades:       List of true FCI grade strings.

        Returns:
            Comprehensive metrics dict including per-axis MAE, correlations,
            grade accuracies, and confusion matrix.
        """
        n = len(predicted_scores)
        if n != len(true_scores) or n != len(predicted_grades) or n != len(true_grades):
            raise ValueError("All input lists must have the same length")

        results: Dict[str, Any] = {"n_samples": n}

        # Per-axis MAE and Pearson correlation
        all_pred_flat: List[float] = []
        all_true_flat: List[float] = []

        for axis in SCORING_AXES:
            preds = [s[axis] for s in predicted_scores]
            trues = [s[axis] for s in true_scores]
            results[f"mae_{axis}"] = round(self.mean_absolute_error(preds, trues), 4)
            results[f"pearson_{axis}"] = round(self.pearson_correlation(preds, trues), 4)
            all_pred_flat.extend(preds)
            all_true_flat.extend(trues)

        results["mae_overall"] = round(
            self.mean_absolute_error(all_pred_flat, all_true_flat), 4
        )
        results["pearson_overall"] = round(
            self.pearson_correlation(all_pred_flat, all_true_flat), 4
        )

        # Grade metrics
        results["grade_accuracy_exact"] = round(
            self.grade_accuracy(predicted_grades, true_grades), 4
        )
        results["grade_accuracy_pm1"] = round(
            self.grade_accuracy_pm1(predicted_grades, true_grades), 4
        )

        # Confusion matrix
        results["confusion_matrix"] = self.confusion_matrix(
            predicted_grades, true_grades
        )

        return results

    def compare_models(
        self,
        scores_a: List[Dict[str, float]],
        scores_b: List[Dict[str, float]],
        true_scores: List[Dict[str, float]],
        grades_a: List[str],
        grades_b: List[str],
        true_grades: List[str],
    ) -> Dict[str, Any]:
        """
        Compare two models (A = baseline/prompt-based, B = fine-tuned) with
        statistical significance testing.

        Returns:
            Dict with per-model metrics and significance tests.
        """
        eval_a = self.evaluate(scores_a, true_scores, grades_a, true_grades)
        eval_b = self.evaluate(scores_b, true_scores, grades_b, true_grades)

        # Paired t-test on overall absolute errors
        errors_a: List[float] = []
        errors_b: List[float] = []
        for sa, sb, st in zip(scores_a, scores_b, true_scores):
            ea = statistics.mean(abs(sa[ax] - st[ax]) for ax in SCORING_AXES)
            eb = statistics.mean(abs(sb[ax] - st[ax]) for ax in SCORING_AXES)
            errors_a.append(ea)
            errors_b.append(eb)

        t_test = self.paired_t_test(errors_a, errors_b)

        # McNemar's test on grade accuracy
        correct_a = [p == t for p, t in zip(grades_a, true_grades)]
        correct_b = [p == t for p, t in zip(grades_b, true_grades)]
        mcnemar = self.mcnemars_test(correct_a, correct_b)

        return {
            "model_a_metrics": eval_a,
            "model_b_metrics": eval_b,
            "paired_t_test": t_test,
            "mcnemars_test": mcnemar,
        }


# =============================================================================
# INFERENCE WRAPPER
# =============================================================================

class FineTunedInference:
    """
    Inference wrapper with a three-level fallback chain:

    1. Breed-specific fine-tuned model (if available and in production).
    2. Universal fine-tuned model (if available and in production).
    3. Prompt-based analysis (the current system -- always available).

    The wrapper returns scores in the same format as the existing AI analysis
    system (dict with axis scores and a grade), and tracks inference latency
    and the method used.

    Args:
        registry:           ModelRegistry to look up models.
        prompt_based_fn:    Callable that performs the current prompt-based
                            analysis.  Signature: (image_path, breed_id) ->
                            Dict with 'scores' and 'grade'.
        model_inference_fn: Optional callable for actual model inference.
                            Signature: (model_version, image_path) -> Dict
                            with 'scores' and 'grade'.  If None, mock
                            inference is used.
    """

    def __init__(
        self,
        registry: ModelRegistry,
        prompt_based_fn: Optional[Callable] = None,
        model_inference_fn: Optional[Callable] = None,
    ):
        self.registry = registry
        self.prompt_based_fn = prompt_based_fn or self._default_prompt_based
        self.model_inference_fn = model_inference_fn or self._mock_model_inference
        self._latency_log: List[Dict[str, Any]] = []

    # -- fallback functions ---------------------------------------------------

    @staticmethod
    def _default_prompt_based(
        image_path: str, breed_id: str
    ) -> Dict[str, Any]:
        """
        Default prompt-based fallback that returns mid-range scores.
        In production this would call the actual Vision API analysis.
        """
        return {
            "scores": {axis: 75.0 for axis in SCORING_AXES},
            "grade": "Very Good",
            "method": "prompt_based",
            "confidence": 0.5,
        }

    @staticmethod
    def _mock_model_inference(
        model_version: ModelVersion, image_path: str
    ) -> Dict[str, Any]:
        """
        Mock model inference that returns slightly randomised scores.
        In production this would load the actual model weights and run
        forward inference.
        """
        rng = random.Random(hash(image_path) + hash(model_version.version_id))
        scores = {}
        for axis in SCORING_AXES:
            scores[axis] = round(70.0 + rng.uniform(-10, 15), 1)

        # Derive grade from average score
        avg = statistics.mean(scores.values())
        if avg >= 90:
            grade = "Excellent"
        elif avg >= 80:
            grade = "Very Good"
        elif avg >= 70:
            grade = "Good"
        elif avg >= 60:
            grade = "Sufficient"
        else:
            grade = "Disqualified"

        return {
            "scores": scores,
            "grade": grade,
            "method": "fine_tuned",
            "confidence": round(0.7 + rng.uniform(0, 0.25), 3),
        }

    # -- main inference -------------------------------------------------------

    def predict(
        self, image_path: str, breed_id: str
    ) -> Dict[str, Any]:
        """
        Run inference using the best available model with fallback chain.

        Fallback order:
          1. Breed-specific production model
          2. Universal production model
          3. Prompt-based analysis

        Returns:
            Dict with:
              - scores:       {axis: float} for each scoring axis
              - grade:        FCI grade string
              - method:       'fine_tuned_breed', 'fine_tuned_universal',
                              or 'prompt_based'
              - model_version: version_id or None
              - confidence:   float in [0, 1]
              - latency_ms:   inference time in milliseconds
        """
        start = time.monotonic()

        result = None
        method = "prompt_based"
        model_version_id = None
        fallback_errors: List[str] = []

        # 1. Try breed-specific model
        breed_model = self.registry.select_best(breed_id=breed_id)
        if breed_model and breed_model.status == "production":
            try:
                result = self.model_inference_fn(breed_model, image_path)
                method = "fine_tuned_breed"
                model_version_id = breed_model.version_id
            except Exception as e:
                logger.warning(
                    "Breed-specific inference failed for %s: %s", breed_id, e
                )
                fallback_errors.append(f"breed({breed_id}): {e}")
                result = None

        # 2. Try universal model
        if result is None:
            universal_model = self.registry.select_best(breed_id=None)
            if universal_model and universal_model.status == "production":
                try:
                    result = self.model_inference_fn(universal_model, image_path)
                    method = "fine_tuned_universal"
                    model_version_id = universal_model.version_id
                except Exception as e:
                    logger.warning("Universal inference failed: %s", e)
                    fallback_errors.append(f"universal: {e}")
                    result = None

        # 3. Fallback to prompt-based
        if result is None:
            if fallback_errors:
                logger.warning(
                    "All fine-tuned models failed, falling back to prompt-based. "
                    "Errors: %s", "; ".join(fallback_errors),
                )
            result = self.prompt_based_fn(image_path, breed_id)
            method = "prompt_based"
            model_version_id = None

        elapsed_ms = round((time.monotonic() - start) * 1000, 2)

        output = {
            "scores": result.get("scores", {}) if result is not None else {},
            "grade": result.get("grade", "Good") if result is not None else "Good",
            "method": method,
            "model_version": model_version_id,
            "confidence": result.get("confidence", 0.5) if result is not None else 0.5,
            "latency_ms": elapsed_ms,
            "fallback_errors": fallback_errors if fallback_errors else None,
        }

        self._latency_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "breed_id": breed_id,
            "method": method,
            "latency_ms": elapsed_ms,
        })

        return output

    # -- latency tracking -----------------------------------------------------

    def get_latency_stats(self) -> Dict[str, Any]:
        """
        Return latency statistics grouped by inference method.
        """
        if not self._latency_log:
            return {"total_inferences": 0}

        by_method: Dict[str, List[float]] = defaultdict(list)
        for entry in self._latency_log:
            by_method[entry["method"]].append(entry["latency_ms"])

        stats: Dict[str, Any] = {"total_inferences": len(self._latency_log)}
        for method, latencies in by_method.items():
            stats[method] = {
                "count": len(latencies),
                "mean_ms": round(statistics.mean(latencies), 2),
                "median_ms": round(statistics.median(latencies), 2),
                "min_ms": round(min(latencies), 2),
                "max_ms": round(max(latencies), 2),
            }
        return stats

    def clear_latency_log(self) -> None:
        """Clear the latency tracking log."""
        self._latency_log.clear()


# =============================================================================
# DATA COLLECTION HELPERS
# =============================================================================

def format_judge_evaluation(
    image_path: str,
    breed_id: str,
    skeletal: float,
    gait: float,
    muscle: float,
    coat: float,
    temperament: float,
    grade: str,
    show_name: str = "",
    show_date: str = "",
    judge_name: str = "",
    judge_certification_level: str = "National",
) -> TrainingExample:
    """
    Convenience function to create a TrainingExample from individual judge
    evaluation fields.

    This is the primary interface for the data collection pipeline: when a
    judge submits an evaluation through the app, call this function to produce
    a training-ready example.

    Args:
        image_path:                 Path to the dog image.
        breed_id:                   Breed key.
        skeletal .. temperament:    Scores (0-100) for each axis.
        grade:                      FCI grade string.
        show_name:                  Show name.
        show_date:                  ISO date string.
        judge_name:                 Judge name.
        judge_certification_level:  Certification level.

    Returns:
        A validated TrainingExample instance.
    """
    scores = {
        "skeletal": float(skeletal),
        "gait": float(gait),
        "muscle": float(muscle),
        "coat": float(coat),
        "temperament": float(temperament),
    }
    return TrainingExample(
        image_path=image_path,
        breed_id=breed_id,
        judge_scores=scores,
        judge_grade=grade,
        show_name=show_name,
        show_date=show_date,
        judge_name=judge_name,
        judge_certification_level=judge_certification_level,
    )


def validate_training_batch(
    examples: List[TrainingExample],
) -> Dict[str, Any]:
    """
    Validate a batch of training examples before ingestion.

    Checks:
      - All required fields are present and non-empty.
      - Scores are in valid range.
      - Grades are valid FCI grades.
      - No duplicate image paths within the batch.

    Returns:
        Dict with 'valid' (bool), 'errors' (list of error strings),
        'warnings' (list), and 'accepted_count' / 'rejected_count'.
    """
    errors: List[str] = []
    warnings: List[str] = []
    seen_images: set = set()
    rejected = 0

    for i, ex in enumerate(examples):
        prefix = f"Example {i} ({ex.example_id})"

        # Required fields
        if not ex.image_path:
            errors.append(f"{prefix}: missing image_path")
            rejected += 1
            continue
        if not ex.breed_id:
            errors.append(f"{prefix}: missing breed_id")
            rejected += 1
            continue

        # Duplicate check
        if ex.image_path in seen_images:
            warnings.append(f"{prefix}: duplicate image_path '{ex.image_path}'")
        seen_images.add(ex.image_path)

        # Score range
        for axis in SCORING_AXES:
            val = ex.judge_scores.get(axis, -1)
            if not (0 <= val <= 100):
                errors.append(f"{prefix}: {axis} score out of range: {val}")

        # Optional but recommended
        if not ex.show_name:
            warnings.append(f"{prefix}: missing show_name")
        if not ex.judge_name:
            warnings.append(f"{prefix}: missing judge_name")

    accepted = len(examples) - rejected
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "accepted_count": accepted,
        "rejected_count": rejected,
    }


# =============================================================================
# SELF-TEST
# =============================================================================

def _self_test() -> None:
    """
    Comprehensive self-test exercising all major components.

    This function is designed to be run standalone or via ``python -m
    api.finetuning``.  It uses a temporary directory for storage and cleans up
    after itself.
    """
    import shutil
    import tempfile

    print("=" * 70)
    print("Fine-Tuning Infrastructure -- Self-Test")
    print("=" * 70)

    tmp_dir = tempfile.mkdtemp(prefix="showdog_ft_test_")
    try:
        _run_all_tests(tmp_dir)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    print("\n" + "=" * 70)
    print("ALL TESTS PASSED")
    print("=" * 70)


def _run_all_tests(tmp_dir: str) -> None:
    rng = random.Random(42)

    # ---- 1. TrainingExample -------------------------------------------------
    print("\n[1/8] TrainingExample schema ...")

    ex = TrainingExample(
        image_path="/tmp/img_001.jpg",
        breed_id="172d_poodle_toy",
        judge_scores={
            "skeletal": 85.0, "gait": 80.0, "muscle": 78.0,
            "coat": 90.0, "temperament": 88.0,
        },
        judge_grade="Very Good",
        show_name="Tokyo International",
        show_date="2025-11-15",
        judge_name="Tanaka Ichiro",
        judge_certification_level="International",
    )
    d = ex.to_dict()
    ex2 = TrainingExample.from_dict(d)
    assert ex2.breed_id == ex.breed_id
    assert ex2.judge_scores == ex.judge_scores
    assert ex2.judge_grade == ex.judge_grade
    print("  OK: creation, serialisation, deserialisation")

    # Validation errors
    try:
        TrainingExample(
            image_path="/tmp/x.jpg", breed_id="test",
            judge_scores={"skeletal": 85}, judge_grade="Very Good",
        )
        raise AssertionError("Should have raised ValueError for missing axes")
    except ValueError:
        pass

    try:
        TrainingExample(
            image_path="/tmp/x.jpg", breed_id="test",
            judge_scores={ax: 50 for ax in SCORING_AXES},
            judge_grade="InvalidGrade",
        )
        raise AssertionError("Should have raised ValueError for bad grade")
    except ValueError:
        pass
    print("  OK: validation rejects bad data")

    # ---- 2. DatasetManager --------------------------------------------------
    print("\n[2/8] DatasetManager ...")

    dm = DatasetManager(storage_dir=tmp_dir)

    # Generate synthetic examples
    breeds = ["172d_poodle_toy", "122_labrador_retriever", "166_german_shepherd"]
    grades = ["Excellent", "Very Good", "Good", "Sufficient"]
    generated: List[TrainingExample] = []

    for i in range(60):
        breed = breeds[i % len(breeds)]
        grade = grades[i % len(grades)]
        scores = {
            ax: round(rng.uniform(60, 98), 1) for ax in SCORING_AXES
        }
        generated.append(TrainingExample(
            image_path=f"/tmp/img_{i:04d}.jpg",
            breed_id=breed,
            judge_scores=scores,
            judge_grade=grade,
            show_name="Test Show" if i % 3 != 0 else "",
            show_date="2025-01-01",
            judge_name=f"Judge_{i % 5}" if i % 4 != 0 else "",
            judge_certification_level="National",
        ))

    dm.add_examples(generated)
    assert len(dm.examples) == 60
    print(f"  OK: added {len(dm.examples)} examples")

    # Save and reload
    dm.save("test_dataset.json")
    dm2 = DatasetManager(storage_dir=tmp_dir)
    n = dm2.load("test_dataset.json")
    assert n == 60
    print(f"  OK: save/load roundtrip ({n} examples)")

    # Statistics
    stats = dm.compute_statistics()
    assert stats["total_examples"] == 60
    assert len(stats["samples_per_breed"]) == 3
    assert all(ax in stats["per_axis_score_stats"] for ax in SCORING_AXES)
    print(f"  OK: statistics computed (breeds={len(stats['samples_per_breed'])})")

    # Quality validation
    report = dm.validate_quality()
    assert isinstance(report["total_issues"], int)
    print(f"  OK: quality check (issues={report['total_issues']})")

    # Splits
    train, val, test = dm.create_splits(seed=42)
    total_split = len(train) + len(val) + len(test)
    assert total_split == 60, f"Split total {total_split} != 60"
    print(f"  OK: splits train={len(train)}, val={len(val)}, test={len(test)}")

    # Augmentation descriptors
    augs = DatasetManager.augmentation_descriptors()
    assert len(augs) == len(AUGMENTATION_DESCRIPTORS)
    subset = DatasetManager.augmentation_descriptors(include=["horizontal_flip"])
    assert subset == ["horizontal_flip"]
    print(f"  OK: augmentation descriptors ({len(augs)} available)")

    # ---- 3. ModelRegistry ---------------------------------------------------
    print("\n[3/8] ModelRegistry ...")

    reg = ModelRegistry(storage_dir=tmp_dir)

    m1 = ModelVersion(
        base_model="showdog-base-v1",
        breed_id=None,
        metrics={"mae_overall": 5.2, "grade_accuracy_exact": 0.65},
        status="validated",
    )
    m2 = ModelVersion(
        base_model="showdog-base-v1",
        breed_id=None,
        metrics={"mae_overall": 4.8, "grade_accuracy_exact": 0.70},
        status="validated",
    )
    m3 = ModelVersion(
        base_model="showdog-universal-v1",
        breed_id="172d_poodle_toy",
        metrics={"mae_overall": 3.5, "grade_accuracy_exact": 0.78},
        status="validated",
    )

    reg.register(m1)
    reg.register(m2)
    reg.register(m3)
    assert len(reg.models) == 3
    print("  OK: registered 3 models")

    # Save and reload
    reg.save("test_registry.json")
    reg2 = ModelRegistry(storage_dir=tmp_dir)
    reg2.load("test_registry.json")
    assert len(reg2.models) == 3
    print("  OK: registry save/load roundtrip")

    # Comparison
    comp = reg.compare(m1.version_id, m2.version_id)
    assert comp["mae_overall"]["winner"] == m2.version_id  # lower MAE
    assert comp["grade_accuracy_exact"]["winner"] == m2.version_id  # higher acc
    print("  OK: A/B comparison")

    # Selection
    best_universal = reg.select_best(breed_id=None)
    assert best_universal is not None
    assert best_universal.version_id == m2.version_id  # lower MAE
    print(f"  OK: auto-selection (best universal = {best_universal.version_id})")

    # Promotion
    reg.promote_to_production(m2.version_id)
    assert reg.get(m2.version_id).status == "production"
    print("  OK: model promotion")

    # Promote another -> old one deprecated
    reg.update_status(m1.version_id, "validated")
    reg.promote_to_production(m1.version_id)
    assert reg.get(m2.version_id).status == "deprecated"
    assert reg.get(m1.version_id).status == "production"
    print("  OK: old production model auto-deprecated")

    # ---- 4. FineTuningConfig ------------------------------------------------
    print("\n[4/8] FineTuningConfig ...")

    cfg = FineTuningConfig(epochs=15, learning_rate=3e-5)
    assert cfg.epochs == 15
    d = cfg.to_dict()
    cfg2 = FineTuningConfig.from_dict(d)
    assert cfg2.learning_rate == cfg.learning_rate
    print("  OK: config creation and serialisation")

    breed_cfg = FineTuningConfig.breed_specific("172d_poodle_toy", epochs=30)
    assert breed_cfg.breed_id == "172d_poodle_toy"
    assert breed_cfg.epochs == 30
    assert breed_cfg.learning_rate == 1e-5  # breed-specific default
    print("  OK: breed-specific config")

    # ---- 5. TrainingPipeline ------------------------------------------------
    print("\n[5/8] TrainingPipeline ...")

    pipeline_reg = ModelRegistry(storage_dir=tmp_dir)
    pipeline_cfg = FineTuningConfig(base_model="test-base", epochs=5)
    pipeline = TrainingPipeline(pipeline_cfg, dm, pipeline_reg)

    vid = pipeline.run()
    assert vid in pipeline_reg.models
    model = pipeline_reg.get(vid)
    assert model.status == "validated"
    assert "mae_overall" in model.metrics
    print(f"  OK: pipeline run (version={vid}, MAE={model.metrics['mae_overall']})")

    # k-fold
    kfold_cfg = FineTuningConfig(base_model="test-kfold", kfold=3)
    kfold_pipe = TrainingPipeline(kfold_cfg, dm, pipeline_reg)
    vid2 = kfold_pipe.run()
    model2 = pipeline_reg.get(vid2)
    assert "kfold_std_mae_overall" in model2.metrics
    print(f"  OK: k-fold pipeline (version={vid2}, k=3)")

    # ---- 6. EvaluationPipeline ----------------------------------------------
    print("\n[6/8] EvaluationPipeline ...")

    evl = EvaluationPipeline()

    # MAE
    mae = evl.mean_absolute_error([80, 85, 90], [82, 83, 88])
    assert abs(mae - 2.0) < 0.001
    print(f"  OK: MAE = {mae}")

    # Pearson correlation
    r = evl.pearson_correlation([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])
    assert abs(r - 1.0) < 0.001, f"Expected r=1.0, got {r}"
    print(f"  OK: Pearson r = {r}")

    r_neg = evl.pearson_correlation([1, 2, 3, 4, 5], [10, 8, 6, 4, 2])
    assert abs(r_neg - (-1.0)) < 0.001
    print(f"  OK: Pearson r (negative) = {r_neg}")

    # Grade accuracy
    acc = evl.grade_accuracy(
        ["Excellent", "Very Good", "Good"], ["Excellent", "Good", "Good"]
    )
    assert abs(acc - 2 / 3) < 0.001
    print(f"  OK: grade accuracy = {acc:.4f}")

    # Grade accuracy +/- 1
    acc_pm1 = evl.grade_accuracy_pm1(
        ["Excellent", "Very Good", "Good"], ["Very Good", "Good", "Sufficient"]
    )
    assert abs(acc_pm1 - 1.0) < 0.001  # all within 1 step
    print(f"  OK: grade accuracy +/-1 = {acc_pm1:.4f}")

    # Confusion matrix
    pred_g = ["Excellent", "Very Good", "Good", "Good", "Sufficient"]
    true_g = ["Excellent", "Very Good", "Very Good", "Good", "Sufficient"]
    cm = evl.confusion_matrix(pred_g, true_g)
    assert cm["matrix"][0][0] == 1  # Excellent correct
    assert cm["labels"] == FCI_GRADES
    assert "per_class" in cm
    print("  OK: confusion matrix computed")

    # Paired t-test
    errs_a = [3.0, 4.0, 5.0, 6.0, 7.0, 3.5, 4.5, 5.5]
    errs_b = [2.0, 3.0, 3.5, 4.0, 5.0, 2.5, 3.5, 4.0]
    t_result = evl.paired_t_test(errs_a, errs_b)
    assert "t_statistic" in t_result
    assert "p_value" in t_result
    assert t_result["mean_diff"] > 0  # A has higher errors
    print(f"  OK: paired t-test (t={t_result['t_statistic']}, p={t_result['p_value']})")

    # McNemar's test
    cor_a = [True, True, False, False, True, True, False, True, True, False]
    cor_b = [True, False, True, False, True, True, True, True, False, True]
    mcn = evl.mcnemars_test(cor_a, cor_b)
    assert "chi2_statistic" in mcn
    assert "p_value" in mcn
    print(f"  OK: McNemar's test (chi2={mcn['chi2_statistic']}, p={mcn['p_value']})")

    # Full evaluation
    n_eval = 20
    pred_scores = []
    true_scores = []
    pred_grades_list = []
    true_grades_list = []
    for i in range(n_eval):
        ps = {ax: round(rng.uniform(65, 95), 1) for ax in SCORING_AXES}
        ts = {ax: round(ps[ax] + rng.uniform(-5, 5), 1) for ax in SCORING_AXES}
        pred_scores.append(ps)
        true_scores.append(ts)
        g_idx = i % len(FCI_GRADES[:-1])  # skip Disqualified for realism
        pred_grades_list.append(FCI_GRADES[g_idx])
        # Slightly offset true grade
        true_idx = min(len(FCI_GRADES) - 1, max(0, g_idx + rng.choice([-1, 0, 0, 1])))
        true_grades_list.append(FCI_GRADES[true_idx])

    full = evl.evaluate(pred_scores, true_scores, pred_grades_list, true_grades_list)
    assert "mae_overall" in full
    assert "pearson_overall" in full
    assert "grade_accuracy_exact" in full
    assert "confusion_matrix" in full
    print(f"  OK: full evaluation (MAE={full['mae_overall']}, "
          f"grade_acc={full['grade_accuracy_exact']})")

    # Model comparison
    pred_scores_b = []
    grades_b = []
    for ps in pred_scores:
        # Slightly better model B
        improved = {ax: round(ps[ax] + rng.uniform(-1, 2), 1) for ax in SCORING_AXES}
        pred_scores_b.append(improved)
    for g in pred_grades_list:
        grades_b.append(g)  # same grades for simplicity

    comparison = evl.compare_models(
        pred_scores, pred_scores_b, true_scores,
        pred_grades_list, grades_b, true_grades_list,
    )
    assert "model_a_metrics" in comparison
    assert "model_b_metrics" in comparison
    assert "paired_t_test" in comparison
    assert "mcnemars_test" in comparison
    print("  OK: model comparison with significance tests")

    # ---- 7. FineTunedInference ----------------------------------------------
    print("\n[7/8] FineTunedInference ...")

    inf_reg = ModelRegistry(storage_dir=tmp_dir)

    # No models -> falls back to prompt-based
    inference = FineTunedInference(inf_reg)
    result = inference.predict("/tmp/test.jpg", "172d_poodle_toy")
    assert result["method"] == "prompt_based"
    assert all(ax in result["scores"] for ax in SCORING_AXES)
    assert result["model_version"] is None
    print(f"  OK: prompt-based fallback (method={result['method']})")

    # Add universal production model
    univ = ModelVersion(
        base_model="test", breed_id=None,
        metrics={"mae_overall": 4.0}, status="production",
    )
    inf_reg.register(univ)

    result2 = inference.predict("/tmp/test.jpg", "999_unknown_breed")
    assert result2["method"] == "fine_tuned_universal"
    assert result2["model_version"] == univ.version_id
    print(f"  OK: universal fallback (method={result2['method']})")

    # Add breed-specific production model
    breed_m = ModelVersion(
        base_model="test", breed_id="172d_poodle_toy",
        metrics={"mae_overall": 3.0}, status="production",
    )
    inf_reg.register(breed_m)

    result3 = inference.predict("/tmp/test.jpg", "172d_poodle_toy")
    assert result3["method"] == "fine_tuned_breed"
    assert result3["model_version"] == breed_m.version_id
    print(f"  OK: breed-specific model (method={result3['method']})")

    # Latency stats
    for _ in range(5):
        inference.predict("/tmp/test.jpg", "172d_poodle_toy")
    lat = inference.get_latency_stats()
    assert lat["total_inferences"] == 8  # 3 above + 5 here
    assert "fine_tuned_breed" in lat
    print(f"  OK: latency tracking ({lat['total_inferences']} inferences logged)")

    inference.clear_latency_log()
    assert inference.get_latency_stats()["total_inferences"] == 0
    print("  OK: latency log cleared")

    # ---- 8. Data collection helpers -----------------------------------------
    print("\n[8/8] Data collection helpers ...")

    ex = format_judge_evaluation(
        image_path="/tmp/photo.jpg",
        breed_id="122_labrador_retriever",
        skeletal=88.0, gait=82.0, muscle=85.0, coat=90.0, temperament=92.0,
        grade="Excellent",
        show_name="Osaka FCI Show",
        show_date="2025-06-20",
        judge_name="Yamamoto Kenji",
        judge_certification_level="FCI-All-Breed",
    )
    assert ex.breed_id == "122_labrador_retriever"
    assert ex.judge_scores["skeletal"] == 88.0
    print("  OK: format_judge_evaluation")

    # Batch validation
    good_batch = [ex]
    bad_ex = TrainingExample(
        image_path="", breed_id="test",
        judge_scores={ax: 50 for ax in SCORING_AXES},
        judge_grade="Good",
    )
    mixed_batch = [ex, bad_ex]

    v1 = validate_training_batch(good_batch)
    assert v1["valid"] is True
    assert v1["accepted_count"] == 1
    print(f"  OK: valid batch (accepted={v1['accepted_count']})")

    v2 = validate_training_batch(mixed_batch)
    assert v2["valid"] is False
    assert v2["rejected_count"] == 1
    print(f"  OK: mixed batch (errors={len(v2['errors'])}, rejected={v2['rejected_count']})")


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    _self_test()
