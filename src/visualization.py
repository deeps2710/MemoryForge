"""Plotly figures built only from the tensors used by the interactive lab."""

import numpy as np
import plotly.graph_objects as go

from src.fast_memory import MemorySnapshot, QueryResult

LABEL_COLORS = ["#365C44", "#8D5228", "#515CAB"]
TEXT = "#202B24"
MUTED = "#5D695E"


def _layout(fig: go.Figure, height: int) -> go.Figure:
    fig.update_layout(
        height=height, margin=dict(l=66, r=48, t=12, b=52),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", color=TEXT, size=12),
        showlegend=False, dragmode=False,
    )
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
    return fig


def memory_figure(snapshot: MemorySnapshot, labels: tuple[str, ...]) -> go.Figure:
    """Fixed [-1,1] color scale permits honest before/after visual comparison."""
    matrix = snapshot.matrix.detach().cpu().numpy()
    fig = go.Figure(go.Heatmap(
        z=matrix.tolist(), x=list(range(1, matrix.shape[1] + 1)), y=list(labels),
        zmin=-1, zmax=1, zmid=0, xgap=3, ygap=5,
        colorscale=[[0, "#9B542C"], [0.5, "#F3F2E9"], [1, "#365C44"]],
        colorbar=dict(title="Weight", thickness=9, len=0.9),
        hovertemplate="%{y} · dimension %{x}<br>Actual weight: %{z:.5f}<extra></extra>",
    ))
    fig.update_xaxes(title="Embedding dimension", dtick=1, fixedrange=True, showgrid=False)
    fig.update_yaxes(autorange="reversed", fixedrange=True, showgrid=False)
    return _layout(fig, 225)


def score_figure(result: QueryResult, position: int, labels: tuple[str, ...]) -> go.Figure:
    scores = result.scores[position].tolist()
    fig = go.Figure(go.Bar(
        x=scores, y=list(labels), orientation="h", marker_color=LABEL_COLORS[:len(labels)],
        text=[f"{score:+.3f}" for score in scores], textposition="outside", cliponaxis=False,
        hovertemplate="%{y}: %{x:.5f}<extra></extra>",
    ))
    fig.update_xaxes(range=[-1.12, 1.15], title="Raw association score", fixedrange=True, zeroline=True, zerolinecolor="#C2C8BC")
    fig.update_yaxes(autorange="reversed", fixedrange=True)
    return _layout(fig, 195)


def embedding_figure(key: list[float]) -> go.Figure:
    fig = go.Figure(go.Bar(x=list(range(1, len(key) + 1)), y=list(key), marker_color="#365C44"))
    fig.update_xaxes(title="Embedding dimension", dtick=1, fixedrange=True)
    fig.update_yaxes(title="Unit key", range=[-1, 1], fixedrange=True)
    return _layout(fig, 180)


def shots_figure(observed: dict[int, float], chance: float) -> go.Figure:
    shots = sorted(observed)
    fig = go.Figure(go.Scatter(
        x=shots, y=[observed[n] * 100 for n in shots], mode="lines+markers",
        line=dict(color="#365C44", width=2), marker=dict(size=8),
        hovertemplate="%{x} demos/class<br>%{y:.1f}% correct<extra></extra>",
    ))
    fig.add_hline(y=chance * 100, line_dash="dot", line_color="#8D5228", annotation_text="Chance 33.3%")
    fig.update_xaxes(title="Demonstrations per class", range=[-0.25, 10.5], dtick=1, fixedrange=True)
    fig.update_yaxes(title="Query accuracy (%)", range=[-5, 105], fixedrange=True)
    return _layout(fig, 240)


def digit_image(pixels: np.ndarray, scale: int = 12) -> np.ndarray:
    """Enlarge the real 8x8 input with nearest-neighbor repetition, never synthesize."""
    image = pixels.reshape(8, 8)
    return np.repeat(np.repeat(image, scale, axis=0), scale, axis=1)
