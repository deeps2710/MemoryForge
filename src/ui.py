"""Streamlit presentation and callbacks; model computation stays in lab/core modules."""

import pandas as pd
import streamlit as st
import torch

from src.lab import LabResources, LabSession, MAX_SHOTS, N_WAY
from src.learning import QUIZ, quiz_feedback
from src.visualization import digit_image, embedding_figure, memory_figure, score_figure, shots_figure

CHART_CONFIG = {"displayModeBar": False, "responsive": True, "scrollZoom": False}


def chart(figure, key: str) -> None:
    st.plotly_chart(figure, use_container_width=True, theme=None, config=CHART_CONFIG, key=key)


def dispatch(action: str) -> None:
    """Callbacks complete before rerender, keeping widgets and derived views in sync."""
    lab: LabSession = st.session_state.lab
    try:
        if action == "new":
            st.session_state.lab = LabSession(lab.resources, seed=(lab.seed + 1) % 2**32)
        elif action == "teach":
            lab.teach_round()
        elif action == "query":
            lab.next_query()
        elif action == "conflict":
            lab.inject_conflict()
        elif action == "clear":
            lab.clear()
        elif action == "shots":
            lab.set_shots(int(st.session_state.shots_slider))
        else:
            raise ValueError("Unknown lab action")
        st.session_state.shots_slider = st.session_state.lab.shots
        st.session_state.matrix_view = "Current"
        st.session_state.ui_error = None
    except (ValueError, RuntimeError) as error:
        st.session_state.ui_error = str(error)


def navigate(page: str) -> None:
    st.session_state.workspace = page


def initialize(resources: LabResources, signature: tuple) -> None:
    if "lab" not in st.session_state or st.session_state.get("resource_signature") != signature:
        st.session_state.lab = LabSession(resources)
        st.session_state.resource_signature = signature
        st.session_state.shots_slider = 1
        st.session_state.matrix_view = "Current"
        st.session_state.ui_error = None


def sidebar(lab: LabSession) -> str:
    with st.sidebar:
        st.markdown('<div class="brand"><span class="brand-mark">M</span>MemoryForge</div>', unsafe_allow_html=True)
        st.caption("A small experiment in fast learning.")
        st.markdown("---")
        st.markdown('<div class="eyebrow">Your learning path</div>', unsafe_allow_html=True)
        page = st.radio("Workspace", ("Guided lab", "Playground", "Research & evidence", "60-second check"), key="workspace", label_visibility="collapsed")
        st.markdown("---")
        st.markdown('<span class="tag">ENCODER · FROZEN</span>', unsafe_allow_html=True)
        st.caption("Representations learned beforehand. No neural-network training during this experiment.")
        st.markdown(f"**Episode {lab.seed}**  \n3 temporary labels · CPU computation")
        st.caption("New Episode advances the seed by one. The same seed reproduces the same images and mapping.")
        st.markdown('<div class="rail-note"><strong>Made for curious ML learners.</strong><br>Bring an understanding of vectors, classification and basic neural networks.</div>', unsafe_allow_html=True)
        st.markdown('<div class="rail-note">MemoryForge is an educational fast-weight associative-memory model. It is not BDH or BDH-CQ.</div>', unsafe_allow_html=True)
        st.caption("DataForge 2026 · Associative Memory & Fast Weights")
    return page


def controls(lab: LabSession) -> None:
    specs = [
        ("New Episode", "new", False, "secondary", "Start a fresh seeded mapping with one real demonstration per class."),
        ("Teach demonstrations", "teach", lab.shots >= MAX_SHOTS, "primary", "Add one new held-out demonstration per class to actual memory."),
        ("Test Query", "query", False, "secondary", "Test the next distinct held-out image. No learning from queries."),
        ("Inject Conflict", "conflict", lab.shots == 0, "secondary", "Write a taught support image under a wrong label; measure the effect."),
        ("Clear Memory", "clear", False, "secondary", "Remove all temporary associations. Preserve the frozen encoder."),
    ]
    with st.container(key="controls"):
        for column, (label, action, disabled, kind, help_text) in zip(st.columns([1, 1.5, 1, 1.1, 1.1]), specs):
            column.button(label, key=action, disabled=disabled, type=kind, use_container_width=True, help=help_text, on_click=dispatch, args=(action,))


def what_changed(view: dict) -> None:
    with st.container(key="what_changed"):
        left, middle, right = st.columns([1, 1, 1])
        left.metric("Encoder parameter delta", f'{view["encoder_delta"]:.0f}')
        left.caption("Frozen · exact tensor equality verified")
        middle.metric("Fast-memory delta", f'{view["memory_delta"]:.5f}')
        middle.caption("Measured from the empty retrieval matrix")
        right.metric("Actual memory writes", str(view["statistics"]["writes"]))
        right.caption(f'{view["shots"]} clean demos/class · {view["conflicts"]} conflicting writes')


def demonstrations(lab: LabSession) -> None:
    with st.container(border=True, key="demo_card"):
        st.subheader("01 / Teach an association")
        st.caption("These symbols belong to this episode. They are not digit-classifier outputs.")
        for column, class_index in zip(st.columns(N_WAY), range(N_WAY)):
            position = int(lab.support_grid[class_index, max(0, lab.shots - 1)])
            digit = int(lab.episode.support_digits[position])
            label = lab.episode.label_names[int(lab.episode.support_labels[position])]
            with column:
                st.image(digit_image(lab.episode.support_images[position]), width=80, clamp=True)
                st.markdown(f"**Digit {digit} → {label}**")
                st.caption(f"{lab.shots} taught · sample {int(lab.episode.support_ids[position])}" if lab.shots else f"Ready to teach · sample {int(lab.episode.support_ids[position])}")


def query_panel(lab: LabSession, view: dict) -> None:
    with st.container(border=True, key="query_card"):
        st.subheader("02 / Retrieve a new association")
        image_col, prediction_col, truth_col = st.columns([1, 1.15, 1.15])
        with image_col:
            st.image(digit_image(lab.episode.query_images[view["query_position"]]), width=96, clamp=True)
            st.caption(f'Digit {view["query_digit"]} · sample {view["query_id"]}')
        prediction = "Abstaining" if view["prediction"] == -1 else lab.episode.label_names[view["prediction"]]
        prediction_col.metric("Prediction", prediction)
        truth_col.metric("Ground truth", lab.episode.label_names[view["truth"]])
        if view["prediction"] == -1:
            st.info("Memory is empty. Teach demonstrations to create associations.")
        elif view["prediction"] == view["truth"]:
            st.success("Correct association")
        else:
            st.warning("Incorrect association — compare the scores below.")
        if view["prediction"] != -1 and bool(view["query_result"].ties[view["query_position"]]):
            st.caption("Exact tie: the first written label by index wins.")
        st.caption(f"Held-out image {lab.query_cursor + 1} of 30. This image was never a demonstration or encoder-training sample.")


def memory_panel(lab: LabSession) -> None:
    with st.container(border=True):
        heading, selector = st.columns([1.3, 1])
        heading.subheader("03 / Look inside fast memory")
        choices = ["Current", *lab.snapshots]
        selected = selector.selectbox("Memory snapshot", choices, key="matrix_view", label_visibility="collapsed")
        snapshot = lab.memory.state_snapshot() if selected == "Current" else lab.snapshots[selected]
        chart(memory_figure(snapshot, lab.episode.label_names), "memory_heatmap")
        st.caption(f"{selected} · {int(snapshot.counts.sum())} writes. Actual 3 × 16 retrieval matrix; fixed color scale −1 to +1.")
        with st.expander("Read the exact memory values"):
            st.dataframe(pd.DataFrame(snapshot.matrix.numpy(), index=lab.episode.label_names, columns=[f"k{i}" for i in range(1, 17)]), use_container_width=True)
            st.caption(f"Write counts: {snapshot.counts.tolist()}. Rows are class means of normalized demonstration embeddings.")


def retrieval_panel(lab: LabSession, view: dict) -> None:
    with st.container(border=True):
        st.subheader("Why this prediction?")
        chart(score_figure(view["query_result"], view["query_position"], lab.episode.label_names), "query_scores")
        st.caption("Each score is a memory-row dot product with the query key. Larger means stronger association; scores are not calibrated probabilities.")
        st.caption(f'Current episode: {round(view["accuracy"] * 30)}/30 query images correct ({view["accuracy"]:.1%}). Random-guess reference: {view["chance"]:.1%}.')
        if view["statistics"]["writes"] == 0:
            st.caption("Empty memory abstains on all queries; 0% here is abstention accuracy, not random guessing.")
        with st.expander("Read the association scores as a table"):
            result = view["query_result"]
            st.table(pd.DataFrame({"Label": lab.episode.label_names, "Raw score": result.scores[view["query_position"]].tolist()}))


def action_detail(lab: LabSession) -> None:
    transition = lab.last_transition
    if transition is None:
        return
    if transition.action == "After conflict":
        written = transition.writes[0]
        labels = lab.episode.label_names
        changed = int((transition.before_query.predictions != transition.after_query.predictions).sum())
        before, after = lab.accuracy(transition.before_query), lab.accuracy(transition.after_query)
        score_delta = float(torch.linalg.vector_norm(transition.after_query.scores - transition.before_query.scores))
        st.warning(f'Conflicting write: digit {written["digit"]} → {labels[written["written_label"]]} (true association: {labels[written["true_label"]]}).')
        st.write(f"Accuracy: **{before:.1%} → {after:.1%}** · **{changed}/30** predictions changed · score delta **{score_delta:.5f}**.")
        st.caption("Fast memory accepts the supplied label, even if it is wrong. A conflict need not reduce accuracy on every episode. Repeated clicks append the same wrong association.")
    elif transition.action == "After reset":
        st.info("Temporary associations cleared. The encoder is unchanged; queries now abstain. Teach again to rebuild memory.")
    with st.expander("Inspect the latest write and the update rule"):
        st.code("S ← S + v kᵀ\nc ← c + v\nM[i] = S[i] / c[i] for written labels\nscores = M q", language=None)
        st.caption("k = unit encoder embedding; v = one-hot episode label; S = raw sums; c = write counts; M = class-mean memory. No optimizer runs here.")
        st.markdown("[Implementation of this rule](https://github.com/deeps2710/MemoryForge/blob/main/src/fast_memory.py) · [Mathematical verification](https://github.com/deeps2710/MemoryForge/blob/main/tests/test_fast_memory.py)")
        if transition.writes:
            rows = [{"Sample": w["sample_id"], "Digit": w["digit"], "Written label": lab.episode.label_names[w["written_label"]], "One-hot value": str(w["value"])} for w in transition.writes]
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
            latest = transition.writes[-1]
            chart(embedding_figure(latest["key"]), "latest_key")
            st.caption(f'Actual encoder key for sample {latest["sample_id"]}. Full normalized key:')
            st.write(latest["key"])
        else:
            st.caption("The latest action made no write; sums and counts are zero after reset.")
        st.caption(f"Last update and integrity checks: {transition.elapsed_ms:.2f} ms on this server. Browser rendering is additional; this is not an end-to-end latency claim.")


def playground(lab: LabSession) -> None:
    st.subheader("Your measured shot experiment")
    chart(shots_figure(lab.shot_accuracies, 1 / N_WAY), "shots_experiment")
    st.caption("Only counts you have actually tried are plotted. Lines connect measured points; they are not predictions for untested counts. More demonstrations need not always help.")


def learning_check() -> None:
    st.markdown('<div class="eyebrow">Reflect / 60-second check</div>', unsafe_allow_html=True)
    st.title("What actually learned?")
    st.write("Three questions to connect what you saw to the mechanism. Choose an answer to get immediate feedback.")
    for index, question in enumerate(QUIZ):
        with st.container(border=True):
            st.subheader(f'{index + 1:02d} / {question["question"]}')
            answer = st.radio(f"Answer {index + 1}", question["options"], index=None, key=f"quiz_{index}", label_visibility="collapsed")
            if answer is not None:
                correct, explanation = quiz_feedback(index, answer)
                (st.success if correct else st.info)(("Correct. " if correct else "Try that reasoning again. ") + explanation)
    st.button("Back to the lab", on_click=navigate, args=("Guided lab",))


def render_lab(lab: LabSession, page: str) -> None:
    view = lab.state_view()
    st.markdown('<div class="eyebrow">Interactive learning lab / Fast-weight associative memory</div>', unsafe_allow_html=True)
    st.title("New associations. Same neural weights.")
    st.write("Can an AI learn a new association without changing its neural-network weights? Teach this memory, query it, then clear it to find out.")
    if page == "Guided lab":
        steps = [("01 · Represent", "A frozen encoder turns a digit into a vector."), ("02 · Associate", "Demonstrations write new symbol associations."), ("03 · Retrieve", "Unseen images read the temporary memory.")]
        for column, (title, description) in zip(st.columns(3), steps):
            column.markdown(f'<div class="path-step"><strong>{title}</strong>{description}</div>', unsafe_allow_html=True)
    else:
        st.slider("Demonstrations per class", min_value=0, max_value=MAX_SHOTS, key="shots_slider", on_change=dispatch, args=("shots",))
        st.caption("This control rebuilds clean memory and clears conflicts. The mapping, query images and ordered demonstration pool stay fixed. Zero demonstrations means abstention.")
    controls(lab)
    if st.session_state.get("ui_error"):
        st.error(st.session_state.ui_error)
    what_changed(view)
    with st.container(key="lab_grid"):
        left, right = st.columns([1, 1.1], gap="medium")
        with left:
            demonstrations(lab)
            memory_panel(lab)
        with right:
            query_panel(lab, view)
            retrieval_panel(lab, view)
    action_detail(lab)
    if page == "Playground":
        playground(lab)
    else:
        st.caption("The preset starts with one real demonstration per class. Teach adds one more per class; Test Query advances to another held-out image.")
        st.button("Explore the playground", on_click=navigate, args=("Playground",))
    with st.expander("What this teaches — and how it connects to research"):
        st.write("A frozen representation and writable temporary memory play different roles. You just changed associations without changing the encoder. Reset shows why that adaptation is temporary.")
        st.write("Follow the research lesson to compare this experiment with published BDH, BDH-CQ, DeltaNet and Titans work. Each connection includes its primary source and the limits of the comparison.")
        st.caption("Limits: supervised digit representations, tiny 8×8 data, known digit identities, uncalibrated scores, and possible interference. Held-out embeddings are precomputed once; writes, queries, matrices and comparisons are computed live.")
    st.button("Connect this experiment to research", on_click=navigate, args=("Research & evidence",))
    st.button("Take the 60-second check", on_click=navigate, args=("60-second check",))
    st.markdown('<div class="small-rule">One claim, made testable: temporary fast memory can acquire new associations while long-term model parameters remain unchanged.<br>AI assistance: Codex assisted implementation and verification; the team remains responsible for technical understanding. Data attribution and sources are recorded in the repository.</div>', unsafe_allow_html=True)
