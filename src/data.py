"""Bundled digits, fixed input scaling and an auditable train/held-out split."""

from dataclasses import dataclass
import hashlib
from typing import Any

import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

from src.config import require_int


@dataclass(frozen=True)
class DigitsData:
    features: np.ndarray
    targets: np.ndarray
    train_ids: np.ndarray
    heldout_ids: np.ndarray
    metadata: dict[str, Any]

    @property
    def fingerprint(self) -> str:
        return self.metadata["fingerprint_sha256"]


def load_digits_data(split_seed: int = 42, test_size: float = 0.25) -> DigitsData:
    require_int("split_seed", split_seed, 0, 2**32 - 1)
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1")
    dataset = load_digits()
    features = np.asarray(dataset.data, dtype=np.float32) / np.float32(16.0)
    targets = np.asarray(dataset.target, dtype=np.int64)
    ids = np.arange(len(targets), dtype=np.int64)
    train_ids, heldout_ids = train_test_split(
        ids, test_size=test_size, random_state=split_seed, stratify=targets,
    )
    train_ids, heldout_ids = np.sort(train_ids), np.sort(heldout_ids)
    digest = hashlib.sha256(features.tobytes() + targets.tobytes()).hexdigest()
    metadata = {
        "name": "sklearn.datasets.load_digits", "samples": len(targets),
        "features": 64, "image_shape": [8, 8], "classes": list(range(10)),
        "raw_pixel_range": [0, 16], "normalization": "float32 pixels / 16",
        "train_count": len(train_ids), "heldout_count": len(heldout_ids),
        "split_seed": split_seed, "test_size": test_size,
        "fingerprint_sha256": digest,
        "source": "https://scikit-learn.org/1.6/datasets/toy_dataset.html#optical-recognition-of-handwritten-digits-dataset",
        "dataset_license": "CC BY 4.0 (UCI dataset page, verified 2026-09-06)",
    }
    return DigitsData(features, targets, train_ids, heldout_ids, metadata)
