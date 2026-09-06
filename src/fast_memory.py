"""Hebbian sums and class-mean retrieval, using detached float64 CPU tensors.

Unit keys k, one-hot values v: S <- S + v k^T, c <- c + v.
Effective memory: M_i = S_i / c_i (zero for unwritten rows).
Unit query q: scores = M q. No optimizer or autograd participates.
"""

from dataclasses import dataclass
import math
from typing import Any

import numpy as np
import torch

from src.config import require_int
from src.reproducibility import tensor_digest

ArrayLike = torch.Tensor | np.ndarray | list[float]


def _tensor(value: ArrayLike) -> torch.Tensor:
    try:
        result = torch.as_tensor(value, dtype=torch.float64, device="cpu").detach().clone()
    except (TypeError, ValueError, RuntimeError) as error:
        raise ValueError("Expected a numeric tensor or array") from error
    if not torch.isfinite(result).all():
        raise ValueError("Memory inputs must be finite")
    return result


@dataclass(frozen=True)
class MemorySnapshot:
    sums: torch.Tensor
    counts: torch.Tensor
    matrix: torch.Tensor

    def as_dict(self) -> dict[str, Any]:
        return {
            "sums": self.sums.tolist(), "counts": self.counts.tolist(),
            "matrix": self.matrix.tolist(),
            "sha256": tensor_digest(self.sums, self.counts, self.matrix),
        }


@dataclass(frozen=True)
class QueryResult:
    scores: torch.Tensor
    display_scores: torch.Tensor
    predictions: torch.Tensor
    ties: torch.Tensor
    has_memory: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "scores": self.scores.tolist(), "display_scores": self.display_scores.tolist(),
            "predictions": self.predictions.tolist(), "ties": self.ties.tolist(),
            "has_memory": self.has_memory,
        }


class FastMemory:
    def __init__(self, key_dim: int, n_labels: int) -> None:
        require_int("key_dim", key_dim, 1)
        require_int("n_labels", n_labels, 2)
        self.key_dim = key_dim
        self.n_labels = n_labels
        self._sums = torch.zeros(n_labels, key_dim, dtype=torch.float64)
        self._counts = torch.zeros(n_labels, dtype=torch.float64)

    def reset(self) -> None:
        self._sums.zero_()
        self._counts.zero_()

    def _keys(self, keys: ArrayLike) -> torch.Tensor:
        values = _tensor(keys)
        if values.ndim != 2 or values.shape[1] != self.key_dim or values.shape[0] == 0:
            raise ValueError(f"keys must have nonempty shape (samples, {self.key_dim})")
        norms = torch.linalg.vector_norm(values, dim=1, keepdim=True)
        if torch.any(norms <= 1e-12) or not torch.isfinite(norms).all():
            raise ValueError("Keys must have finite, nonzero norms")
        return values / norms

    def _matrix(self) -> torch.Tensor:
        return self._sums / self._counts.clamp_min(1).unsqueeze(1)

    def write(self, key: ArrayLike, value: ArrayLike) -> None:
        key_tensor, value_tensor = _tensor(key), _tensor(value)
        if key_tensor.ndim != 1 or value_tensor.ndim != 1:
            raise ValueError("write expects one key vector and one one-hot value vector")
        self.write_batch(key_tensor.unsqueeze(0), value_tensor.unsqueeze(0))

    def write_batch(self, keys: ArrayLike, values: ArrayLike) -> None:
        """Validate the entire batch before applying any update (atomic on error)."""
        normalized = self._keys(keys)
        labels = _tensor(values)
        if labels.shape != (len(normalized), self.n_labels):
            raise ValueError(f"values must have shape (samples, {self.n_labels})")
        if not torch.all((labels == 0) | (labels == 1)) or not torch.all(labels.sum(dim=1) == 1):
            raise ValueError("Each value must be exactly one-hot")
        for key, value in zip(normalized, labels):
            self._sums += torch.outer(value, key)
            self._counts += value

    def query(self, queries: ArrayLike, temperature: float = 1.0) -> QueryResult:
        """Retrieve raw similarities and uncalibrated softmax display scores.

        Unwritten labels cannot win. Empty memory abstains with prediction -1;
        uniform display scores in that state are not an actual random guess.
        """
        if not math.isfinite(temperature) or temperature <= 0:
            raise ValueError("temperature must be finite and positive")
        inputs = _tensor(queries)
        if inputs.ndim == 1:
            inputs = inputs.unsqueeze(0)
        normalized = self._keys(inputs)
        scores = normalized @ self._matrix().T
        occupied = self._counts > 0
        if not occupied.any():
            return QueryResult(
                scores, torch.full_like(scores, 1 / self.n_labels),
                torch.full((len(normalized),), -1, dtype=torch.int64),
                torch.ones(len(normalized), dtype=torch.bool), False,
            )
        masked = scores.masked_fill(~occupied.unsqueeze(0), -torch.inf)
        maxima = masked.max(dim=1, keepdim=True).values
        # Subtract before division for stability even with a tiny positive temperature.
        display = torch.softmax((masked - maxima) / temperature, dim=1)
        predictions = masked.argmax(dim=1)
        ties = (masked == maxima).sum(dim=1) > 1
        return QueryResult(scores, display, predictions, ties, True)

    def state_snapshot(self) -> MemorySnapshot:
        return MemorySnapshot(self._sums.clone(), self._counts.clone(), self._matrix().clone())

    def memory_delta(self, before: MemorySnapshot) -> float:
        """Frobenius delta of the effective retrieval matrix, not parameter drift."""
        if before.matrix.shape != self._sums.shape or not torch.isfinite(before.matrix).all():
            raise ValueError("Snapshot matrix shape/values do not match this memory")
        return float(torch.linalg.vector_norm(self._matrix() - before.matrix))

    def statistics(self) -> dict[str, Any]:
        return {
            "writes": int(self._counts.sum()), "occupied_labels": int((self._counts > 0).sum()),
            "counts": self._counts.tolist(), "memory_norm": float(torch.linalg.vector_norm(self._matrix())),
            "sum_norm": float(torch.linalg.vector_norm(self._sums)),
            "state_sha256": tensor_digest(self._sums, self._counts, self._matrix()),
        }
