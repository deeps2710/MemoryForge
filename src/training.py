"""Ordinary supervised pretraining, performed only by an explicit training call."""

from dataclasses import asdict
from pathlib import Path
from typing import Any

import torch
from torch import nn

from src.config import DEFAULT_ARTIFACT, SeedConfig, TrainConfig
from src.data import load_digits_data
from src.encoder import DigitEncoder, freeze_encoder
from src.reproducibility import environment_info, save_json, seed_everything, tensor_digest


def train_encoder(
    config: TrainConfig = TrainConfig(), seeds: SeedConfig = SeedConfig(),
    artifact_path: str | Path = DEFAULT_ARTIFACT,
) -> dict[str, Any]:
    seed_everything(seeds)
    data = load_digits_data(seeds.split, config.test_size)
    encoder = DigitEncoder().cpu()
    head = nn.Linear(16, 10).cpu()
    optimizer = torch.optim.Adam(
        list(encoder.parameters()) + list(head.parameters()),
        lr=config.learning_rate, weight_decay=config.weight_decay,
    )
    features = torch.from_numpy(data.features[data.train_ids])
    targets = torch.from_numpy(data.targets[data.train_ids])
    generator = torch.Generator(device="cpu").manual_seed(seeds.torch)
    loss_history = []
    encoder.train()
    head.train()
    for _ in range(config.epochs):
        order = torch.randperm(len(targets), generator=generator)
        total_loss = 0.0
        for batch in order.split(config.batch_size):
            optimizer.zero_grad(set_to_none=True)
            logits = head(encoder(features[batch]))
            loss = nn.functional.cross_entropy(logits, targets[batch])
            loss.backward()
            optimizer.step()
            total_loss += float(loss.detach()) * len(batch)
        loss_history.append(total_loss / len(targets))

    encoder.eval()
    head.eval()
    with torch.no_grad():
        heldout_logits = head(encoder(torch.from_numpy(data.features[data.heldout_ids])))
        heldout_predictions = heldout_logits.argmax(dim=1)
        heldout_targets = torch.from_numpy(data.targets[data.heldout_ids])
        correct = int((heldout_predictions == heldout_targets).sum())
    freeze_encoder(encoder)
    report = {
        "architecture": [64, 32, 16, 10], "seeds": asdict(seeds), "config": asdict(config),
        "data": data.metadata, "environment": environment_info(), "loss_history": loss_history,
        "heldout_classification_correct": correct, "heldout_classification_total": len(data.heldout_ids),
        "heldout_classification_accuracy": correct / len(data.heldout_ids),
        "digit_classification_chance": 0.1,
        "encoder_sha256": tensor_digest(*encoder.state_dict().values()),
        "protocol": "Fixed-epoch training on train_ids only. Head used only for digit sanity evaluation.",
    }
    checkpoint = {
        "format_version": 1, "architecture": report["architecture"],
        "encoder_state": encoder.state_dict(), "head_state": head.state_dict(),
        "data": data.metadata, "train_ids": data.train_ids.tolist(),
        "heldout_ids": data.heldout_ids.tolist(), "training_report": report,
    }
    artifact_path = Path(artifact_path)
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(checkpoint, artifact_path)
    save_json(artifact_path.with_suffix(".training.json"), report)
    return report
