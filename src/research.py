"""Versioned research references and a read-only explanation of the live lab."""
import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import torch

from src.config import ROOT
from src.evidence import DEFAULT_EVIDENCE, load_evidence, report_digest
from src.visualization import _layout

SOURCE_FILE = ROOT / "docs" / "research_sources.json"


def sources() -> dict:
    return {item["id"]: item for item in json.loads(SOURCE_FILE.read_text(encoding="utf-8"))["sources"]}


def source_line(item: dict) -> str:
    return f'[{item["title"]}]({item["full_text"]}) · {item["reviewed_version"]} · {item["locator"]}'


def write_decomposition(lab, support_position: int) -> dict:
    """Inspect an actual possible write; never mutate the learner's memory."""
    key = lab.support_keys[support_position].to(torch.float64)
    key = key / torch.linalg.vector_norm(key)
    label = int(lab.episode.support_labels[support_position])
    value = torch.nn.functional.one_hot(torch.tensor(label), 3).to(torch.float64)
    q = lab.query_keys[lab.query_position].to(torch.float64)
    q = q / torch.linalg.vector_norm(q)
    matrix = lab.memory.state_snapshot().matrix
    return {"key": key, "value": value, "outer": torch.outer(value, key),
            "query": q, "matrix": matrix, "contributions": matrix * q,
            "scores": matrix @ q}


def evidence_figure(summary: list[dict]) -> go.Figure:
    fig = go.Figure()
    colors = ["#365C44", "#8D5228", "#515CAB"]
    for index, conflicts in enumerate(sorted({r["conflicts"] for r in summary})):
        rows = sorted((r for r in summary if r["conflicts"] == conflicts), key=lambda r: r["shots"])
        fig.add_trace(go.Scatter(
            x=[r["shots"] for r in rows], y=[100 * r["mean_accuracy"] for r in rows],
            error_y=dict(type="data", array=[100 * r["std_accuracy_population"] for r in rows], visible=True),
            mode="lines+markers", name="Clean" if conflicts == 0 else f"{conflicts} wrong-label writes",
            line=dict(color=colors[index % len(colors)], dash=["solid", "dash", "dot"][index % 3]),
            hovertemplate="%{x} demos/class<br>Mean %{y:.2f}%<extra>%{fullData.name}</extra>",
        ))
    chance = summary[0]["chance"]
    fig.add_hline(y=100 * chance, line_dash="dot", annotation_text=f"Chance {chance:.1%}")
    fig.update_xaxes(title="Clean demonstrations per class", dtick=1, fixedrange=True)
    fig.update_yaxes(title="Mean query accuracy (%)", range=[-5, 110], fixedrange=True)
    _layout(fig, 360)
    fig.update_layout(showlegend=True, legend=dict(orientation="h", y=1.28, x=0), margin=dict(t=65))
    return fig


@st.cache_data(show_spinner=False)
def cached_evidence(path: str, modified: int, size: int):
    return load_evidence(path)


def render_evidence(lab):
    st.subheader("Challenge the preset with 50 seeds")
    st.write("A single episode can improve or worsen when you add demonstrations. These saved experiments keep the query set fixed within each seed and compare clean memory with repeated wrong-label writes.")
    try:
        info = DEFAULT_EVIDENCE.stat()
        report = cached_evidence(str(DEFAULT_EVIDENCE), info.st_mtime_ns, info.st_size)
    except (OSError, ValueError, KeyError, TypeError) as error:
        st.warning(f"Saved evidence is unavailable: {error}")
        st.code("python scripts/evaluate_suite.py")
        return
    if report["encoder_sha256"] != lab.resources.encoder_sha256:
        st.warning("These saved results use a different encoder from the live lab. Regenerate evidence before comparing them.")
        return
    st.caption("Saved CPU computation, not a live rerun. Error bars show population standard deviation across episode accuracies, not confidence intervals. Lines connect measured counts.")
    st.plotly_chart(evidence_figure(report["summary"]), use_container_width=True,
                    theme=None, config={"displayModeBar": False}, key="evidence_summary")
    frame = pd.DataFrame(report["summary"])
    st.dataframe(frame[["shots", "conflicts", "episodes", "mean_accuracy", "std_accuracy_population",
                        "mean_accuracy_change_from_clean", "predictions_changed",
                        "memory_delta_min", "encoder_parameter_delta_max"]],
                 hide_index=True, use_container_width=True)
    total = sum(len(e["conditions"]) for e in report["episodes"])
    st.caption(f'{len(report["episodes"])} seeds · {total} condition evaluations · {total * 30:,} query outcomes. Conditions share images; these are not independent trials.')
    st.info("Zero shots means abstention. Conflicts append the same first support key under the next cyclic label. Three extra writes represent different contamination fractions at different clean shot counts.")
    with st.expander("Reproduce or inspect the saved evidence"):
        st.code("python scripts/evaluate_suite.py")
        st.write(report["protocol"])
        st.caption(f"Canonical report SHA-256: {report_digest(report)}")
        st.download_button("Download raw evidence JSON", DEFAULT_EVIDENCE.read_bytes(),
                           file_name="memoryforge-phase3-evidence.json", mime="application/json")
        st.markdown("[Experiment implementation](https://github.com/deeps2710/MemoryForge/blob/main/src/evidence.py) · [Memory implementation](https://github.com/deeps2710/MemoryForge/blob/main/src/fast_memory.py)")


def render_derivation(lab):
    st.subheader("Follow one key through the equation")
    st.write("This calculation uses an actual support image embedding and the current query. Inspecting a write does not apply it.")
    positions = lab.support_grid[:, 0].tolist()
    position = st.selectbox("Inspect support sample", positions, format_func=lambda p: f'Digit {lab.episode.support_digits[p]} → {lab.episode.label_names[lab.episode.support_labels[p]]} · row {lab.episode.support_ids[p]}', key="derive_support")
    data = write_decomposition(lab, position)
    st.code("k = encoder(image) / ||encoder(image)||₂\nv = one_hot(episode_label)\nS ← S + v kᵀ\nc ← c + v\nM[i] = S[i] / c[i] if c[i] > 0, else 0\nscores = M q", language=None)
    st.write("k and q have 16 components and unit length; v has 3 components. S and M have shape 3×16. A one-hot v adds k to just one row of S. Counts c make retrieval average demonstrations within each label; class means are not normalized again.")
    st.caption(f'Inspected key norm: {torch.linalg.vector_norm(data["key"]):.8f} · value: {data["value"].to(torch.int64).tolist()}')
    st.dataframe(pd.DataFrame(data["outer"].numpy(), index=lab.episode.label_names,
                             columns=[f"k{i}" for i in range(1,17)]), use_container_width=True)
    st.caption("Actual outer-product increment ΔS for the selected support; it is not the complete current memory.")
    st.latex(r"\mathrm{score}_i = \sum_{d=1}^{16} M_{i,d}q_d = \frac{1}{c_i}\sum_{j:\,y_j=i} k_j^\top q\quad(c_i>0)")
    st.write("Each stored key contributes its dot product with the query, divided by the number of writes to that label. A conflicting write enters the wrong row. Similar keys can therefore compete even though the encoder stays fixed.")
    st.table(pd.DataFrame({"Label": lab.episode.label_names,
                          "Sum of dimension contributions": data["contributions"].sum(dim=1).tolist(),
                          "Current M @ q": data["scores"].tolist()}))
    st.caption("Empty memory abstains; unwritten labels cannot win. Scores are not calibrated probabilities. The source below is the implementation authority for these equations.")
    st.markdown("[MemoryForge memory rule](https://github.com/deeps2710/MemoryForge/blob/main/src/fast_memory.py) · [Independent mathematical tests](https://github.com/deeps2710/MemoryForge/blob/main/tests/test_fast_memory.py)")


def render_research(lab):
    from src.ui import navigate  # Avoid module-level circular dependency.
    catalog = sources()
    st.markdown('<div class="eyebrow">Connect / Research & evidence</div>', unsafe_allow_html=True)
    st.title("From a writable matrix to research")
    view = lab.state_view()
    st.write(f'Your episode {lab.seed}: **{view["statistics"]["writes"]} memory writes**, encoder parameter delta **{view["encoder_delta"]:.0f}**. Keep that distinction in mind as the architectures become more complex.')
    st.caption("This page inspects your experiment without changing it. Published claims below are separate from measurements made by MemoryForge.")
    bridge, equations, evidence = st.tabs(["BDH connection", "Memory rule", "Evidence"])
    with bridge:
        st.subheader("What you observed")
        st.write("The encoder supplies a learned representation. Demonstrations alter a separate store; queries read it. Clearing the store removes the episode associations. This is the limited result the toy makes directly testable.")
        for key, heading in [("bdh", "What genuinely connects to BDH"), ("bdh-cq", "Where BDH-CQ adds another stage")]:
            item = catalog[key]
            st.subheader(heading)
            st.write(item["claim"])
            st.markdown(source_line(item))
            st.write(item["relevance"])
            st.info(item["limits"])
        st.subheader("Keep the roles separate")
        st.table(pd.DataFrame({
            "Role": ["Previously learned structure", "Writable association", "Answer computation"],
            "MemoryForge": ["Frozen 64→32→16 digit encoder", "Supervised symbol writes to a 3×16 class-mean matrix", "One matrix–query product, then argmax"],
            "What this toy cannot establish": ["BDH's full architecture or biological interpretation", "A language model's memory capacity or learned update behavior", "BDH-CQ's iterative latent reasoning or ARC results"],
        }))
        item = catalog["bdh-code"]
        with st.expander("Inspect the official baseline boundary"):
            st.write(item["claim"])
            st.markdown(source_line(item))
            st.caption(item["limits"])
        st.subheader("Two other directions for associative memory")
        for key in ("delta", "titans"):
            item = catalog[key]
            with st.container(border=True):
                st.markdown(f'**{item["title"]}**')
                st.write(item["claim"])
                st.markdown(source_line(item))
                st.caption(item["relevance"] + " " + item["limits"])
        answer = st.radio("Does a zero encoder delta prove that this lab reproduces BDH-CQ?",
                          ["Yes", "No"], index=None, key="research_check")
        if answer:
            (st.success if answer == "No" else st.info)("A shared separation of fixed parameters and temporary state does not establish architectural equivalence. The lab has no iterative latent workspace.")
        with st.expander("Source ledger: versions, evidence and limitations"):
            for item in catalog.values():
                st.markdown(source_line(item))
                st.caption(f'{", ".join(item["authors"])} · first public date {item["first_public_date"]} · {item["kind"]} · {item["evidence_type"]}')
            st.caption("Verified 2026-09-07. Four research papers/reports fall within 2022–2026. Titans first appeared on 2024-12-31 despite its 2501 arXiv identifier. Preprints and code inspection are not independent reproductions.")
    with equations:
        render_derivation(lab)
    with evidence:
        render_evidence(lab)
    st.button("Return to your experiment", on_click=navigate, args=("Guided lab",))
