import random

import numpy as np
import torch

from src.config import SeedConfig, TrainConfig
from src.encoder import load_encoder
from src.evaluation import evaluate_core
from src.reproducibility import seed_everything
from src.training import train_encoder


def test_central_seed_controls_python_numpy_and_torch():
    seeds = SeedConfig(python=12, numpy=23, torch=34, split=45, episode=56)
    assert seed_everything(seeds) == {"python": 12, "numpy": 23, "torch": 34, "split": 45, "episode": 56}
    first = random.random(), np.random.random(), torch.rand(3)
    seed_everything(seeds)
    second = random.random(), np.random.random(), torch.rand(3)
    assert first[:2] == second[:2] and torch.equal(first[2], second[2])


def test_two_full_evaluations_match_all_evidence(trained_artifact):
    a = evaluate_core(trained_artifact, episodes=8)
    random.random()
    np.random.random(12)
    torch.rand(50)
    b = evaluate_core(trained_artifact, episodes=8)
    # Includes label mappings, sampled IDs, metrics, scores and every memory tensor.
    assert a == b


def test_training_replay_reproduces_weights_losses_and_metrics(tmp_path):
    config = TrainConfig(epochs=4)
    first_path, second_path = tmp_path / "first.pt", tmp_path / "second.pt"
    first = train_encoder(config, artifact_path=first_path)
    second = train_encoder(config, artifact_path=second_path)
    assert first == second
    first_model, first_checkpoint = load_encoder(first_path)
    second_model, second_checkpoint = load_encoder(second_path)
    for key in first_model.state_dict():
        assert torch.equal(first_model.state_dict()[key], second_model.state_dict()[key])
    for key in first_checkpoint["head_state"]:
        assert torch.equal(first_checkpoint["head_state"][key], second_checkpoint["head_state"][key])
