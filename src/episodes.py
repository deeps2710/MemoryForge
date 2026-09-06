"""Seeded temporary label mappings with support/query disjointness by row ID."""

from dataclasses import dataclass
from typing import Any

import numpy as np

from src.config import EpisodeConfig, LABELS, require_int
from src.data import DigitsData, load_digits_data


@dataclass(frozen=True)
class Episode:
    seed: int
    config: EpisodeConfig
    digit_to_label: dict[int, int]
    support_ids: np.ndarray
    support_images: np.ndarray
    support_digits: np.ndarray
    support_labels: np.ndarray
    query_ids: np.ndarray
    query_images: np.ndarray
    query_digits: np.ndarray
    query_labels: np.ndarray

    @property
    def label_names(self) -> tuple[str, ...]:
        return LABELS[:self.config.n_way]

    def description(self) -> dict[str, Any]:
        return {
            "seed": self.seed,
            "digit_to_label": {str(digit): LABELS[label] for digit, label in self.digit_to_label.items()},
            "support_ids": self.support_ids.tolist(), "support_digits": self.support_digits.tolist(),
            "support_labels": self.support_labels.tolist(), "query_ids": self.query_ids.tolist(),
            "query_digits": self.query_digits.tolist(), "query_labels": self.query_labels.tolist(),
            "label_names": list(self.label_names),
        }


def generate_episode(
    n_way: int = 3, shots_per_class: int = 5, queries_per_class: int = 10,
    seed: int = 1000, *, data: DigitsData | None = None,
) -> Episode:
    config = EpisodeConfig(n_way, shots_per_class, queries_per_class)
    require_int("episode seed", seed, 0, 2**32 - 1)
    data = load_digits_data() if data is None else data
    rng = np.random.default_rng(seed)
    classes = np.sort(rng.choice(np.unique(data.targets[data.heldout_ids]), n_way, replace=False))
    labels = rng.permutation(n_way)
    mapping = {int(digit): int(label) for digit, label in zip(classes, labels)}
    support_ids, query_ids = [], []
    for digit in classes:
        candidates = data.heldout_ids[data.targets[data.heldout_ids] == digit]
        required = shots_per_class + queries_per_class
        if len(candidates) < required:
            raise ValueError(f"Digit {digit} has {len(candidates)} held-out rows; need {required}")
        chosen = rng.choice(candidates, required, replace=False)
        support_ids.extend(chosen[:shots_per_class].tolist())
        query_ids.extend(chosen[shots_per_class:].tolist())
    support = np.asarray(support_ids, dtype=np.int64)
    query = np.asarray(query_ids, dtype=np.int64)
    return Episode(
        seed, config, mapping, support, data.features[support], data.targets[support],
        np.asarray([mapping[int(d)] for d in data.targets[support]], dtype=np.int64),
        query, data.features[query], data.targets[query],
        np.asarray([mapping[int(d)] for d in data.targets[query]], dtype=np.int64),
    )
