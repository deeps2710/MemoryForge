import numpy as np

from src.fast_memory import FastMemory
from src.learning import QUIZ, quiz_feedback
from src.visualization import digit_image, embedding_figure, memory_figure, score_figure, shots_figure


def test_heatmap_is_actual_matrix_and_fixed_scale_after_every_action():
    memory = FastMemory(2, 3)
    for action in [lambda: None, lambda: memory.write([1, 0], [1, 0, 0]), lambda: memory.write([1, 0], [0, 1, 0]), memory.reset]:
        action()
        snapshot = memory.state_snapshot()
        fig = memory_figure(snapshot, ("ALPHA", "BETA", "GAMMA"))
        assert np.array_equal(fig.data[0].z, snapshot.matrix.numpy())
        assert fig.data[0].zmin == -1 and fig.data[0].zmax == 1


def test_score_and_embedding_figures_use_actual_values():
    memory = FastMemory(2, 3)
    memory.write([1, 0], [1, 0, 0])
    result = memory.query([[1, 0], [0, 1]])
    fig = score_figure(result, 1, ("ALPHA", "BETA", "GAMMA"))
    assert list(fig.data[0].x) == result.scores[1].tolist()
    key = [0.1, -0.2, 0.3]
    assert list(embedding_figure(key).data[0].y) == key


def test_shots_plot_only_contains_observed_points():
    fig = shots_figure({1: 0.6, 5: 0.9}, 1 / 3)
    assert list(fig.data[0].x) == [1, 5]
    assert list(fig.data[0].y) == [60, 90]


def test_digit_image_is_nearest_neighbor_copy_of_real_pixels():
    pixels = np.arange(64, dtype=np.float32) / 64
    image = digit_image(pixels, scale=3)
    assert image.shape == (24, 24)
    assert np.array_equal(image[::3, ::3].flatten(), pixels)


def test_quiz_feedback_checks_central_concepts_and_every_option():
    for i, question in enumerate(QUIZ):
        for option in question["options"]:
            correct, explanation = quiz_feedback(i, option)
            assert correct == (option == question["answer"])
            assert explanation == question["explanation"]
