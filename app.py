"""MemoryForge Phase 2. Run: python -m streamlit run app.py"""

from pathlib import Path

import streamlit as st

from src.config import DEFAULT_ARTIFACT, ROOT
from src.lab import load_lab_resources
from src.ui import initialize, learning_check, render_lab, sidebar

st.set_page_config(page_title="MemoryForge · Learn without retraining", page_icon="◈", layout="wide", initial_sidebar_state="expanded")
st.html(f"<style>{(ROOT / 'assets' / 'lab.css').read_text(encoding='utf-8')}</style>")


@st.cache_resource(show_spinner="Loading the frozen encoder and digit representations…")
def cached_resources(path: str, signature: tuple[int, int]):
    return load_lab_resources(path)


def main() -> None:
    try:
        artifact = Path(DEFAULT_ARTIFACT)
        if not artifact.is_file():
            raise FileNotFoundError("Encoder artifact is missing. Run python scripts/train_encoder.py, then reload this page.")
        info = artifact.stat()
        signature = (info.st_mtime_ns, info.st_size)
        resources = cached_resources(str(artifact), signature)
        initialize(resources, (str(artifact), *signature))
        lab = st.session_state.lab
        lab.audit()
        page = sidebar(lab)
        if page == "60-second check":
            learning_check()
        else:
            render_lab(lab, page)
    except (OSError, ValueError, RuntimeError, KeyError) as error:
        st.error(f"The lab could not continue: {error}")
        st.caption("No training was triggered. Fix the artifact or input issue, then reload the page.")


main()
