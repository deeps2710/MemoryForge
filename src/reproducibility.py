"""Explicit random seeds and deterministic CPU execution; no seed on import."""

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import platform
import random
from typing import Any

import joblib
import numpy as np
import scipy
import sklearn
import torch

from src.config import SeedConfig


def seed_everything(seeds: SeedConfig = SeedConfig()) -> dict[str, int]:
    random.seed(seeds.python)
    np.random.seed(seeds.numpy)
    torch.manual_seed(seeds.torch)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    return asdict(seeds)


def environment_info() -> dict[str, Any]:
    return {
        "python": platform.python_version(), "platform": platform.platform(),
        "numpy": np.__version__, "scikit_learn": sklearn.__version__,
        "scipy": scipy.__version__, "joblib": joblib.__version__,
        "torch": str(torch.__version__), "device": "cpu",
        "torch_threads": torch.get_num_threads(),
        "deterministic_algorithms": torch.are_deterministic_algorithms_enabled(),
    }


def tensor_digest(*tensors: torch.Tensor) -> str:
    digest = hashlib.sha256()
    for tensor in tensors:
        array = tensor.detach().cpu().contiguous().numpy()
        digest.update(str(array.shape).encode())
        digest.update(str(array.dtype).encode())
        digest.update(array.tobytes())
    return digest.hexdigest()


def save_json(path: str | Path, payload: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
