import numpy as np
import pytest

from src.data import load_digits_data


def test_dataset_shapes_ranges_and_metadata(data):
    assert data.features.shape == (1797, 64)
    assert data.features.dtype == np.float32
    assert data.targets.shape == (1797,)
    assert set(data.targets) == set(range(10))
    assert np.isfinite(data.features).all()
    assert data.features.min() == 0 and data.features.max() == 1
    assert np.array_equal(data.features * 16, (data.features * 16).round())
    assert data.metadata["image_shape"] == [8, 8]
    assert len(data.fingerprint) == 64


def test_split_deterministic_disjoint_and_complete(data):
    replay = load_digits_data()
    assert np.array_equal(data.train_ids, replay.train_ids)
    assert np.array_equal(data.heldout_ids, replay.heldout_ids)
    assert len(data.train_ids) == 1347 and len(data.heldout_ids) == 450
    assert not set(data.train_ids) & set(data.heldout_ids)
    assert set(data.train_ids) | set(data.heldout_ids) == set(range(1797))
    assert data.fingerprint == replay.fingerprint
    for digit in range(10):
        proportion = (data.targets[data.heldout_ids] == digit).mean()
        assert abs(proportion - (data.targets == digit).mean()) < 0.005


def test_different_split_seed_changes_rows_not_dataset(data):
    other = load_digits_data(split_seed=43)
    assert not np.array_equal(other.heldout_ids, data.heldout_ids)
    assert other.fingerprint == data.fingerprint


@pytest.mark.parametrize("kwargs", [{"split_seed": -1}, {"split_seed": True}, {"test_size": 0}, {"test_size": 1}, {"test_size": float("nan")}])
def test_bad_split_rejected(kwargs):
    with pytest.raises(ValueError):
        load_digits_data(**kwargs)
