"""Slow representation plus exact parameter audit and safe checkpoint loading."""

from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

from src.config import DEFAULT_ARTIFACT
from src.data import DigitsData


class DigitEncoder(nn.Module):
    embedding_dim = 16

    def __init__(self) -> None:
        super().__init__()
        self.layers = nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 16))

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        return self.layers(inputs)


def freeze_encoder(encoder: DigitEncoder) -> DigitEncoder:
    encoder.cpu().eval()
    for parameter in encoder.parameters():
        parameter.requires_grad_(False)
        parameter.grad = None
    return encoder


def assert_frozen(encoder: DigitEncoder) -> None:
    if encoder.training or any(p.requires_grad or p.grad is not None for p in encoder.parameters()):
        raise ValueError("Episode adaptation requires a frozen encoder in eval mode")
    if any(p.device.type != "cpu" for p in encoder.parameters()):
        raise ValueError("MemoryForge Phase 1 uses CPU execution")


def parameter_snapshot(encoder: DigitEncoder) -> dict[str, torch.Tensor]:
    return {name: value.detach().cpu().clone() for name, value in encoder.named_parameters()}


def parameter_delta(encoder: DigitEncoder, before: dict[str, torch.Tensor]) -> float:
    current = dict(encoder.named_parameters())
    if current.keys() != before.keys():
        raise ValueError("Parameter snapshot has different parameter names")
    squared = 0.0
    for name, value in current.items():
        if value.shape != before[name].shape:
            raise ValueError("Parameter snapshot has different shapes")
        difference = value.detach().cpu().double() - before[name].double()
        squared += float(torch.sum(difference.square()))
    return squared**0.5


def parameters_equal(encoder: DigitEncoder, before: dict[str, torch.Tensor]) -> bool:
    current = parameter_snapshot(encoder)
    return current.keys() == before.keys() and all(torch.equal(current[k], before[k]) for k in current)


def embed(encoder: DigitEncoder, inputs: np.ndarray | torch.Tensor) -> torch.Tensor:
    """Produce detached, normalized CPU keys without changing slow parameters."""
    assert_frozen(encoder)
    values = torch.as_tensor(inputs, dtype=torch.float32, device="cpu")
    if values.ndim != 2 or values.shape[1] != 64 or values.shape[0] == 0:
        raise ValueError("inputs must have nonempty shape (samples, 64)")
    if not torch.isfinite(values).all() or torch.any(values < 0) or torch.any(values > 1):
        raise ValueError("inputs must contain finite pixels normalized to [0, 1]")
    with torch.no_grad():
        encoded = encoder(values)
        if not torch.isfinite(encoded).all() or torch.any(torch.linalg.vector_norm(encoded, dim=1) <= 1e-12):
            raise ValueError("Encoder produced a nonfinite or zero embedding")
        return F.normalize(encoded, p=2, dim=1).detach()


def load_encoder(path: str | Path = DEFAULT_ARTIFACT) -> tuple[DigitEncoder, dict[str, Any]]:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Encoder artifact missing: {path}. Run python scripts/train_encoder.py")
    checkpoint = torch.load(path, map_location="cpu", weights_only=True)
    if not isinstance(checkpoint, dict) or checkpoint.get("format_version") != 1:
        raise ValueError("Unsupported MemoryForge checkpoint format")
    if checkpoint.get("architecture") != [64, 32, 16, 10]:
        raise ValueError("Checkpoint architecture does not match DigitEncoder")
    # Loading must not consume the caller's random state during module initialization.
    with torch.random.fork_rng(devices=[]):
        encoder = DigitEncoder()
    encoder.load_state_dict(checkpoint["encoder_state"], strict=True)
    if not all(torch.isfinite(p).all() for p in encoder.parameters()):
        raise ValueError("Checkpoint contains nonfinite encoder weights")
    return freeze_encoder(encoder), checkpoint


def validate_checkpoint_data(checkpoint: dict[str, Any], data: DigitsData) -> None:
    """Reject a mismatched split instead of accidentally evaluating training rows."""
    if checkpoint["data"]["fingerprint_sha256"] != data.fingerprint:
        raise ValueError("Checkpoint dataset fingerprint mismatch")
    if checkpoint["train_ids"] != data.train_ids.tolist() or checkpoint["heldout_ids"] != data.heldout_ids.tolist():
        raise ValueError("Checkpoint/data split mismatch: would invalidate held-out evaluation")
