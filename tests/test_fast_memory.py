import math

import pytest
import torch

from src.fast_memory import FastMemory


def test_empty_abstention_then_identity_retrieval_and_reset():
    memory = FastMemory(2, 2)
    before = memory.state_snapshot()
    empty = memory.query([1, 0])
    assert empty.predictions.tolist() == [-1] and not empty.has_memory
    assert empty.scores.tolist() == [[0, 0]]
    assert empty.display_scores.tolist() == [[0.5, 0.5]]
    memory.write([3, 0], [1, 0])  # Nonunit input normalized to (1,0).
    memory.write([0, 2], [0, 1])
    assert torch.equal(memory.state_snapshot().matrix, torch.eye(2, dtype=torch.float64))
    result = memory.query([[5, 0], [0, 7]])
    assert result.predictions.tolist() == [0, 1]
    assert result.scores.tolist() == [[1, 0], [0, 1]]
    assert memory.memory_delta(before) == pytest.approx(math.sqrt(2))
    assert memory.statistics()["writes"] == 2
    memory.reset()
    memory.reset()
    assert memory.memory_delta(before) == 0
    assert memory.statistics()["writes"] == 0
    assert memory.statistics()["memory_norm"] == 0
    assert memory.query([1, 0]).predictions.tolist() == [-1]


def test_handcrafted_outer_product_and_class_averaging():
    memory = FastMemory(2, 2)
    memory.write_batch([[1, 0], [0, 1], [-1, 0]], [[1, 0], [1, 0], [0, 1]])
    state = memory.state_snapshot()
    assert state.sums.tolist() == [[1, 1], [-1, 0]]
    assert state.counts.tolist() == [2, 1]
    assert state.matrix.tolist() == [[0.5, 0.5], [-1, 0]]
    result = memory.query([1, 1])
    expected = torch.tensor([[1 / math.sqrt(2), -1 / math.sqrt(2)]], dtype=torch.float64)
    assert torch.allclose(result.scores, expected, atol=1e-14)
    assert torch.allclose(result.display_scores, torch.softmax(expected, dim=1))
    assert result.predictions.tolist() == [0]


def test_more_duplicate_shots_do_not_bias_class_scores():
    memory = FastMemory(2, 2)
    memory.write_batch([[1, 0], [0, 1]], [[1, 0], [0, 1]])
    before = memory.state_snapshot()
    memory.write_batch([[1, 0]] * 4, [[1, 0]] * 4)
    assert torch.equal(memory.state_snapshot().matrix, before.matrix)
    assert memory.statistics()["counts"] == [5, 1]


def test_batch_matches_sequential_writes_exactly():
    keys = [[3, 4], [2, -3], [0, -2]]
    labels = [[1, 0], [1, 0], [0, 1]]
    batch, sequential = FastMemory(2, 2), FastMemory(2, 2)
    batch.write_batch(keys, labels)
    for k, v in zip(keys, labels):
        sequential.write(k, v)
    assert batch.state_snapshot().as_dict() == sequential.state_snapshot().as_dict()


def test_conflict_changes_exact_scores_and_exposes_tie():
    memory = FastMemory(2, 2)
    memory.write_batch([[1, 0], [0, 1]], [[1, 0], [0, 1]])
    before = memory.state_snapshot()
    memory.write([1, 0], [0, 1])
    assert memory.state_snapshot().matrix.tolist() == [[1, 0], [0.5, 0.5]]
    assert memory.query([1, 0]).scores.tolist() == [[1, 0.5]]
    assert memory.memory_delta(before) == pytest.approx(math.sqrt(0.5))
    result = memory.query([1, 1])
    assert result.ties.tolist() == [True]
    assert result.predictions.tolist() == [0]


def test_unwritten_label_cannot_win_against_negative_similarity():
    memory = FastMemory(2, 3)
    memory.write([1, 0], [0, 1, 0])
    result = memory.query([-1, 0])
    assert result.scores.tolist() == [[0, -1, 0]]
    assert result.predictions.tolist() == [1]
    assert result.display_scores.tolist() == [[0, 1, 0]]


def test_snapshot_and_inputs_cannot_mutate_internal_state():
    key = torch.tensor([3.0, 4.0], requires_grad=True)
    value = torch.tensor([1.0, 0.0], requires_grad=True)
    memory = FastMemory(2, 2)
    memory.write(key, value)
    state = memory.state_snapshot()
    assert not state.matrix.requires_grad and not state.sums.requires_grad
    assert key.grad is None and value.grad is None
    original = memory.statistics()["state_sha256"]
    state.sums.fill_(99)
    state.counts.fill_(99)
    state.matrix.fill_(99)
    with torch.no_grad():
        key.fill_(99)
        value.fill_(99)
    assert memory.statistics()["state_sha256"] == original


@pytest.mark.parametrize("keys,values", [
    ([[1, 0], [0, 0]], [[1, 0], [0, 1]]),
    ([[1, 0], [0, 1]], [[1, 0], [0.5, 0.5]]),
    ([[1, 0]], [[1, 1]]), ([[1, 0]], [[0, 0]]),
    ([[1, 0]], [[-1, 2]]), ([[1, 0]], [[1, 0, 0]]),
    ([[1, 0]], [[float("nan"), 0]]),
    ([[float("inf"), 0]], [[1, 0]]),
    ([[1, 0, 0]], [[1, 0]]), ([], []),
])
def test_invalid_batch_rejected_atomically(keys, values):
    memory = FastMemory(2, 2)
    memory.write([1, 0], [1, 0])
    before = memory.state_snapshot().as_dict()
    with pytest.raises(ValueError):
        memory.write_batch(keys, values)
    assert memory.state_snapshot().as_dict() == before


@pytest.mark.parametrize("query", [[0, 0], [1, 2, 3], [float("nan"), 0], [], "bad"])
def test_invalid_queries_rejected(query):
    with pytest.raises(ValueError):
        FastMemory(2, 2).query(query)


@pytest.mark.parametrize("temperature", [0, -1, float("nan"), float("inf")])
def test_invalid_temperature_rejected(temperature):
    with pytest.raises(ValueError):
        FastMemory(2, 2).query([1, 0], temperature=temperature)


def test_extreme_temperature_is_finite_and_does_not_change_prediction():
    memory = FastMemory(2, 2)
    memory.write_batch([[1, 0], [0, 1]], [[1, 0], [0, 1]])
    a, b = memory.query([1, 0]), memory.query([1, 0], temperature=1e-300)
    assert torch.equal(a.predictions, b.predictions)
    assert torch.isfinite(b.display_scores).all()
    assert b.display_scores.sum() == 1


@pytest.mark.parametrize("dims", [(0, 2), (2, 1), (True, 2), (2.5, 3)])
def test_invalid_dimensions_rejected(dims):
    with pytest.raises(ValueError):
        FastMemory(*dims)
