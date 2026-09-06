import numpy as np
import pytest
import torch

from src.data import load_digits_data
from src.encoder import (
    DigitEncoder, assert_frozen, embed, freeze_encoder, load_encoder,
    parameter_delta, parameter_snapshot, parameters_equal, validate_checkpoint_data,
)
from src.reproducibility import tensor_digest


def test_encoder_shape_normalization_freeze_and_no_grad(encoder, data):
    inputs = data.features[data.heldout_ids[:7]]
    assert encoder(torch.from_numpy(inputs)).shape == (7, 16)
    keys = embed(encoder, inputs)
    assert keys.shape == (7, 16) and keys.device.type == "cpu"
    assert not keys.requires_grad
    assert torch.allclose(torch.linalg.vector_norm(keys, dim=1), torch.ones(7))
    assert not encoder.training
    assert all(not p.requires_grad and p.grad is None for p in encoder.parameters())


def test_artifact_reproduces_embeddings_and_digit_sanity(encoder, data, trained_artifact):
    loaded, checkpoint = load_encoder(trained_artifact)
    validate_checkpoint_data(checkpoint, data)
    assert torch.equal(embed(encoder, data.features), embed(loaded, data.features))
    head = torch.nn.Linear(16, 10)
    head.load_state_dict(checkpoint["head_state"])
    with torch.no_grad():
        predictions = head(loaded(torch.from_numpy(data.features[data.heldout_ids]))).argmax(dim=1).numpy()
    accuracy = float((predictions == data.targets[data.heldout_ids]).mean())
    assert accuracy == checkpoint["training_report"]["heldout_classification_accuracy"]
    assert accuracy > 0.1 + 0.1  # Internal health check, not a competition target.
    assert tensor_digest(*loaded.state_dict().values()) == checkpoint["training_report"]["encoder_sha256"]


def test_loading_does_not_consume_torch_rng(trained_artifact):
    state = torch.get_rng_state().clone()
    load_encoder(trained_artifact)
    assert torch.equal(state, torch.get_rng_state())


def test_mismatched_checkpoint_split_is_rejected(trained_artifact):
    _, checkpoint = load_encoder(trained_artifact)
    with pytest.raises(ValueError, match="split mismatch"):
        validate_checkpoint_data(checkpoint, load_digits_data(43))


def test_actual_parameter_mutation_is_detected(encoder):
    before = parameter_snapshot(encoder)
    assert parameter_delta(encoder, before) == 0 and parameters_equal(encoder, before)
    with torch.no_grad():
        next(encoder.parameters()).flatten()[0] += 0.5
    assert parameter_delta(encoder, before) > 0
    assert not parameters_equal(encoder, before)


def test_unfrozen_or_training_encoder_is_rejected(data):
    encoder = DigitEncoder()
    with pytest.raises(ValueError, match="frozen"):
        embed(encoder, data.features[:1])
    freeze_encoder(encoder).train()
    with pytest.raises(ValueError):
        assert_frozen(encoder)


@pytest.mark.parametrize("inputs", [np.zeros(64), np.zeros((0, 64)), np.zeros((2, 63)), np.ones((1, 64)) * 2, np.ones((1, 64)) * -1, np.full((1, 64), np.nan)])
def test_bad_encoder_inputs_rejected(encoder, inputs):
    with pytest.raises(ValueError):
        embed(encoder, inputs)


def test_missing_or_wrong_artifact_has_actionable_error(tmp_path):
    with pytest.raises(FileNotFoundError, match="train_encoder.py"):
        load_encoder(tmp_path / "missing.pt")
    path = tmp_path / "invalid.pt"
    torch.save({"format_version": 999}, path)
    with pytest.raises(ValueError, match="format"):
        load_encoder(path)
