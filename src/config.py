"""Small immutable configurations shared by training, evaluation and tests."""

from dataclasses import dataclass
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARTIFACT = ROOT / "artifacts" / "encoder.pt"
LABELS = ("ALPHA", "BETA", "GAMMA", "DELTA", "EPSILON", "ZETA", "ETA", "THETA", "IOTA", "KAPPA")


def require_int(name: str, value: int, minimum: int, maximum: int | None = None) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    if maximum is not None and value > maximum:
        raise ValueError(f"{name} must be <= {maximum}")


@dataclass(frozen=True)
class SeedConfig:
    python: int = 42
    numpy: int = 42
    torch: int = 42
    split: int = 42
    episode: int = 1000

    def __post_init__(self) -> None:
        for name, value in vars(self).items():
            require_int(name, value, 0, 2**32 - 1)


@dataclass(frozen=True)
class TrainConfig:
    epochs: int = 100
    batch_size: int = 64
    learning_rate: float = 0.003
    weight_decay: float = 0.0001
    test_size: float = 0.25

    def __post_init__(self) -> None:
        require_int("epochs", self.epochs, 1)
        require_int("batch_size", self.batch_size, 1)
        if not math.isfinite(self.learning_rate) or self.learning_rate <= 0:
            raise ValueError("learning_rate must be finite and positive")
        if not math.isfinite(self.weight_decay) or self.weight_decay < 0:
            raise ValueError("weight_decay must be finite and nonnegative")
        if not 0 < self.test_size < 1:
            raise ValueError("test_size must be between 0 and 1")


@dataclass(frozen=True)
class EpisodeConfig:
    n_way: int = 3
    shots_per_class: int = 5
    queries_per_class: int = 10

    def __post_init__(self) -> None:
        require_int("n_way", self.n_way, 2, len(LABELS))
        require_int("shots_per_class", self.shots_per_class, 1)
        require_int("queries_per_class", self.queries_per_class, 1)
