"""Session-local interactive experiments built on the unchanged Phase 1 engine."""

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Any

import numpy as np
import torch

from src.config import DEFAULT_ARTIFACT, require_int
from src.data import DigitsData, load_digits_data
from src.encoder import (
    DigitEncoder, assert_frozen, embed, load_encoder, parameter_delta,
    parameter_snapshot, parameters_equal, validate_checkpoint_data,
)
from src.episodes import generate_episode
from src.fast_memory import FastMemory, MemorySnapshot, QueryResult
from src.reproducibility import tensor_digest

MAX_SHOTS = 10
N_WAY = 3
QUERIES_PER_CLASS = 10
PRESET_SEED = 1000


@dataclass(frozen=True)
class LabResources:
    encoder: DigitEncoder
    data: DigitsData
    heldout_keys: torch.Tensor
    key_offsets: dict[int, int]
    original_parameters: dict[str, torch.Tensor]
    encoder_sha256: str

    def keys(self, row_ids: np.ndarray) -> torch.Tensor:
        # Reject training rows: only held-out IDs are present in this lookup.
        return self.heldout_keys[[self.key_offsets[int(row)] for row in row_ids]].clone()


def load_lab_resources(path: str | Path = DEFAULT_ARTIFACT) -> LabResources:
    """Load once and cache representations only. No training or memory is cached."""
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    encoder, checkpoint = load_encoder(path)
    data = load_digits_data(checkpoint["data"]["split_seed"], checkpoint["data"]["test_size"])
    validate_checkpoint_data(checkpoint, data)
    keys = embed(encoder, data.features[data.heldout_ids])
    return LabResources(
        encoder, data, keys, {int(row): i for i, row in enumerate(data.heldout_ids)},
        parameter_snapshot(encoder), tensor_digest(*encoder.state_dict().values()),
    )


@dataclass(frozen=True)
class Transition:
    action: str
    before: MemorySnapshot
    after: MemorySnapshot
    before_query: QueryResult
    after_query: QueryResult
    writes: tuple[dict[str, Any], ...]
    elapsed_ms: float


class LabSession:
    """One learner's temporary state; never share/cache this object across sessions.

    Generate a full fixed support pool once. Changing shots selects nested prefixes
    while preserving query rows and symbolic mappings. Phase 1 sampling stays intact.
    """

    def __init__(self, resources: LabResources, seed: int = PRESET_SEED, preset_shots: int = 1) -> None:
        require_int("preset_shots", preset_shots, 0, MAX_SHOTS)
        self.resources = resources
        self.episode = generate_episode(N_WAY, MAX_SHOTS, QUERIES_PER_CLASS, seed, data=resources.data)
        self.support_keys = resources.keys(self.episode.support_ids)
        self.query_keys = resources.keys(self.episode.query_ids)
        self.memory = FastMemory(resources.encoder.embedding_dim, N_WAY)
        self.support_grid = np.arange(N_WAY * MAX_SHOTS).reshape(N_WAY, MAX_SHOTS)
        self.query_order = np.arange(N_WAY * QUERIES_PER_CLASS).reshape(N_WAY, QUERIES_PER_CLASS).T.flatten()
        self.query_cursor = 0
        self.shots = 0
        self.conflicts = 0
        self.snapshots: dict[str, MemorySnapshot] = {"Before teaching": self.memory.state_snapshot()}
        self.shot_accuracies: dict[int, float] = {}
        self.last_transition: Transition | None = None
        self.last_query_ms = 0.0
        self.set_shots(preset_shots)

    @property
    def seed(self) -> int:
        return self.episode.seed

    @property
    def query_position(self) -> int:
        return int(self.query_order[self.query_cursor])

    def audit(self) -> float:
        assert_frozen(self.resources.encoder)
        delta = parameter_delta(self.resources.encoder, self.resources.original_parameters)
        if delta != 0 or not parameters_equal(self.resources.encoder, self.resources.original_parameters):
            raise RuntimeError("Encoder integrity check failed: permanent weights changed. Reload the model before continuing.")
        return delta

    def query_all(self) -> QueryResult:
        return self.memory.query(self.query_keys)

    def accuracy(self, result: QueryResult | None = None) -> float:
        result = self.query_all() if result is None else result
        return float((result.predictions.numpy() == self.episode.query_labels).mean())

    def _begin(self) -> tuple[float, MemorySnapshot, QueryResult]:
        start = perf_counter()
        self.audit()
        return start, self.memory.state_snapshot(), self.query_all()

    def _write_rows(self, positions: np.ndarray, wrong_label: int | None = None) -> tuple[dict[str, Any], ...]:
        if not len(positions):
            return ()
        labels = self.episode.support_labels[positions].copy()
        if wrong_label is not None:
            labels[:] = wrong_label
        values = torch.nn.functional.one_hot(torch.from_numpy(labels), N_WAY)
        self.memory.write_batch(self.support_keys[positions], values)
        return tuple({
            "support_position": int(pos), "sample_id": int(self.episode.support_ids[pos]),
            "digit": int(self.episode.support_digits[pos]),
            "true_label": int(self.episode.support_labels[pos]), "written_label": int(label),
            "key": self.support_keys[pos].tolist(), "value": value.tolist(),
        } for pos, label, value in zip(positions, labels, values))

    def _finish(self, action: str, started: tuple, writes: tuple[dict[str, Any], ...]) -> None:
        start, before, before_query = started
        after_query = self.query_all()
        self.audit()
        after = self.memory.state_snapshot()
        self.last_transition = Transition(action, before, after, before_query, after_query, writes, (perf_counter() - start) * 1000)
        self.snapshots["Before latest action"] = before
        self.snapshots[action] = after
        if not self.conflicts:
            self.shot_accuracies[self.shots] = self.accuracy(after_query)

    def teach_round(self) -> None:
        if self.shots >= MAX_SHOTS:
            raise ValueError(f"All {MAX_SHOTS} available demonstrations per class are already taught")
        started = self._begin()
        writes = self._write_rows(self.support_grid[:, self.shots])
        self.shots += 1
        self._finish("After teaching", started, writes)

    def set_shots(self, shots: int) -> None:
        """Rebuild clean temporary memory; keep the same query set and nested supports."""
        require_int("shots", shots, 0, MAX_SHOTS)
        started = self._begin()
        self.memory.reset()
        self.conflicts = 0
        self.shots = shots
        writes = self._write_rows(self.support_grid[:, :shots].T.flatten())
        self._finish("After teaching" if shots else "After reset", started, writes)

    def inject_conflict(self) -> None:
        if self.shots == 0:
            raise ValueError("Teach at least one demonstration per class before injecting a conflict")
        started = self._begin()
        wrong = (int(self.episode.support_labels[0]) + 1) % N_WAY
        writes = self._write_rows(np.asarray([0]), wrong_label=wrong)
        self.conflicts += 1
        self._finish("After conflict", started, writes)

    def clear(self) -> None:
        started = self._begin()
        self.memory.reset()
        self.shots = 0
        self.conflicts = 0
        self._finish("After reset", started, ())

    def next_query(self) -> QueryResult:
        start = perf_counter()
        self.audit()
        self.query_cursor = (self.query_cursor + 1) % len(self.query_order)
        result = self.memory.query(self.query_keys[self.query_position])
        self.last_query_ms = (perf_counter() - start) * 1000
        return result

    def state_view(self) -> dict[str, Any]:
        """A fresh measured view, including real truth/prediction and tensor deltas."""
        delta = self.audit()
        result = self.query_all()
        pos = self.query_position
        transition = self.last_transition
        return {
            "seed": self.seed, "shots": self.shots, "conflicts": self.conflicts,
            "encoder_delta": delta, "encoder_parameters_equal": True,
            "memory_delta": self.memory.memory_delta(self.snapshots["Before teaching"]),
            "last_memory_delta": self.memory.memory_delta(transition.before) if transition else 0.0,
            "accuracy": self.accuracy(result), "chance": 1 / N_WAY,
            "prediction": int(result.predictions[pos]), "truth": int(self.episode.query_labels[pos]),
            "query_id": int(self.episode.query_ids[pos]), "query_digit": int(self.episode.query_digits[pos]),
            "query_position": pos, "query_result": result, "statistics": self.memory.statistics(),
            "last_action": transition.action if transition else "Before teaching",
            "last_action_ms": transition.elapsed_ms if transition else 0.0,
        }
