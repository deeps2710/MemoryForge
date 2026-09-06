"""Tests train their own artifact; no hidden dependency on checked-in weights."""

import pytest

from src.config import SeedConfig, TrainConfig
from src.data import load_digits_data
from src.encoder import load_encoder
from src.reproducibility import seed_everything
from src.training import train_encoder


@pytest.fixture(scope="session")
def data():
    return load_digits_data()


@pytest.fixture(scope="session")
def trained_artifact(tmp_path_factory):
    path = tmp_path_factory.mktemp("model") / "encoder.pt"
    train_encoder(TrainConfig(), SeedConfig(), path)
    return path


@pytest.fixture
def encoder(trained_artifact):
    seed_everything()
    return load_encoder(trained_artifact)[0]
