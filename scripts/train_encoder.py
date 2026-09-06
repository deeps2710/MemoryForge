"""Explicit CPU pretraining: python scripts/train_encoder.py."""

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import DEFAULT_ARTIFACT, SeedConfig, TrainConfig
from src.training import train_encoder


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_ARTIFACT)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42, help="Python, NumPy and Torch seed")
    parser.add_argument("--split-seed", type=int, default=42)
    args = parser.parse_args()
    try:
        report = train_encoder(
            TrainConfig(epochs=args.epochs),
            SeedConfig(python=args.seed, numpy=args.seed, torch=args.seed, split=args.split_seed), args.output,
        )
    except (ValueError, OSError) as error:
        parser.exit(1, f"Training failed: {error}\n")
    print(json.dumps({
        "artifact": str(args.output), "heldout_accuracy": report["heldout_classification_accuracy"],
        "correct": report["heldout_classification_correct"], "total": report["heldout_classification_total"],
        "encoder_sha256": report["encoder_sha256"],
    }, indent=2))


if __name__ == "__main__":
    main()
