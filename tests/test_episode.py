from dataclasses import asdict

import numpy as np
import pytest

from src.config import EpisodeConfig
from src.episodes import generate_episode


def test_episode_is_seeded_and_replayable(data):
    a = generate_episode(data=data)
    b = generate_episode(data=data)
    assert a.description() == b.description()
    assert np.array_equal(a.support_images, b.support_images)
    assert np.array_equal(a.query_images, b.query_images)


@pytest.mark.parametrize("seed", [0, 42, 1000, 1001, 2026])
def test_support_query_train_disjoint_and_ground_truth_preserved(data, seed):
    episode = generate_episode(seed=seed, data=data)
    support, query = set(episode.support_ids), set(episode.query_ids)
    assert len(support) == 15 and len(query) == 30
    assert not support & query
    assert (support | query) <= set(data.heldout_ids)
    assert not (support | query) & set(data.train_ids)
    assert np.array_equal(episode.support_images, data.features[episode.support_ids])
    assert np.array_equal(episode.query_images, data.features[episode.query_ids])
    for digits, labels in [(episode.support_digits, episode.support_labels), (episode.query_digits, episode.query_labels)]:
        assert labels.tolist() == [episode.digit_to_label[int(d)] for d in digits]
    assert set(episode.digit_to_label.values()) == {0, 1, 2}
    assert episode.label_names == ("ALPHA", "BETA", "GAMMA")


def test_label_permutation_changes_independently_of_selected_digits(data):
    episodes = [generate_episode(seed=i, data=data) for i in range(30)]
    assert len({tuple(e.digit_to_label.values()) for e in episodes}) > 1
    assert len({tuple(e.support_ids) for e in episodes}) > 1
    # No assertion that every pair must differ: random collisions are legitimate.
    assert any(list(e.digit_to_label.values()) != [0, 1, 2] for e in episodes)


@pytest.mark.parametrize("config", [EpisodeConfig(2, 1, 1), EpisodeConfig(10, 2, 3)])
def test_supported_episode_sizes(data, config):
    episode = generate_episode(**asdict(config), data=data)
    assert len(episode.support_ids) == config.n_way * config.shots_per_class
    assert len(episode.query_ids) == config.n_way * config.queries_per_class


@pytest.mark.parametrize("kwargs", [{"n_way": 1}, {"n_way": 11}, {"shots_per_class": 0}, {"queries_per_class": -1}, {"seed": -1}, {"shots_per_class": 100}, {"n_way": 3.5}])
def test_invalid_or_impossible_episode_rejected(data, kwargs):
    with pytest.raises(ValueError):
        generate_episode(data=data, **kwargs)
