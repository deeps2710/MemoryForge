# Provenance — Phases 1 and 2

Evidence checked 2026-09-06 (core/data) and 2026-09-07 (UI dependencies/assets). This is an implementation provenance record, not
the Phase 3 research integration. No papers or figures are reused in this phase.

## Dataset

Alpaydin, E. and Kaynak, C. (1998), *Optical Recognition of Handwritten Digits*,
UCI Machine Learning Repository, DOI [10.24432/C50P49](https://doi.org/10.24432/C50P49).
The [original dataset page](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)
identifies the creators and lists **CC BY 4.0**; see the
[license](https://creativecommons.org/licenses/by/4.0/).

The [scikit-learn 1.6 dataset documentation](https://scikit-learn.org/1.6/datasets/toy_dataset.html#optical-recognition-of-handwritten-digits-dataset)
and installed `load_digits().DESCR` identify its bundled 1,797-row dataset as
a copy of the original UCI test partition. MemoryForge creates its own 1,347/450
split inside that bundled subset. Its metrics do not use the original UCI
training/test protocol and must not be described as such.

Modifications: float32 conversion, division by 16, deterministic stratified split,
embedding computation and seeded support/query sampling. Images are the dataset's
8×8 digit inputs; no external image assets are added. The original dataset is not
copied into this repository; it ships inside the scikit-learn dependency.

## Code, dependencies and model

| Item | Source/evidence | License/status | Modification/location |
|---|---|---|---|
| MemoryForge code | Original Phases 1–2 implementation with Codex assistance | Project license NOT SELECTED; team decision needed | `src/`, `scripts/`, `tests/` |
| Initial repository | Remote commit `fd433b4` from the user-designated repository | No license file present | Existing `html` preserved verbatim; README expanded |
| Encoder and head weights | Locally trained from seeded random initialization using this repository | Generated-weight license NOT SELECTED; training-data attribution above | `artifacts/encoder.pt`; no third-party pretrained weights |
| Evaluation evidence | Computed by this repository | Project-generated output; data attribution above | `artifacts/*.json` |
| PyTorch 2.6.0+cpu | Installed distribution metadata; [source](https://github.com/pytorch/pytorch/tree/v2.6.0) | BSD-3-Clause, package metadata | Imported dependency; unmodified |
| NumPy 2.2.6 | Installed distribution LICENSE metadata; [source](https://github.com/numpy/numpy/tree/v2.2.6) | Core BSD-3-Clause; wheel contains additional third-party notices | Imported dependency; unmodified |
| scikit-learn 1.6.1 | Installed distribution LICENSE metadata; [source](https://github.com/scikit-learn/scikit-learn/tree/1.6.1) | Core BSD-3-Clause; wheel includes runtime notices | Imported dependency; unmodified; dataset license tracked separately |
| pytest 8.3.5 | Installed distribution metadata; [source](https://github.com/pytest-dev/pytest/tree/8.3.5) | MIT | Test dependency; unmodified |
| SciPy, joblib, threadpoolctl | Installed dependencies recorded in `artifacts/environment.json` | Full transitive/wheel notice review deferred to Phase 4 | Imported numerical dependencies; unmodified |
| Streamlit 1.45.1 | Installed distribution metadata | Apache License 2.0 | Imported UI dependency; unmodified |
| Plotly 6.1.2 | Installed distribution metadata | MIT | Imported chart dependency; unmodified |
| pandas 2.2.3 | Installed distribution metadata | BSD-3-Clause | Imported table dependency; unmodified |
| UI CSS, brand mark and text | Original with Codex assistance | Project license NOT SELECTED | `assets/lab.css`, `src/ui.py`; no downloaded assets |
| Fonts and icons | Local system font stack; textual M/Unicode mark and native Streamlit controls | No font or icon files redistributed | System fonts and dependency rendering |
| Digit display images | Dataset above, nearest-neighbor enlargement | Dataset attribution above | `src/visualization.py`; no generated or external artwork |
| Research papers and figures | None reused yet | Phase 3 pending | Transition placeholder only |

Package metadata was read using `importlib.metadata`. Package license names do
not replace full wheel notices or determine dataset rights. No third-party
package source or wheels are vendored here. Final provenance review must cover
the dependencies/assets actually used by the finished product.

Phase 2 metadata and the installed package inventory are saved in
`artifacts/phase2_environment.json`. License names were read from installed
Streamlit, Plotly and pandas distributions. Full transitive and wheel notice
review remains a Phase 4 item. No image-generation model, remote font service,
third-party template or copied website was used for the UI.
