# Provenance — submission release

Evidence checked 2026-09-06 (core/data) and 2026-09-07 (UI, dependencies, fonts and release). Phase 3 source verification is recorded in RESEARCH_NOTES.md and the versioned
research_sources.json ledger. No paper figures or full texts are redistributed.

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
8×8 digit inputs; the separate user-supplied logo is recorded below. The original dataset is not
copied into this repository; it ships inside the scikit-learn dependency.

## Code, dependencies and model

| Item | Source/evidence | License/status | Modification/location |
|---|---|---|---|
| MemoryForge code, original docs/figures | Original Phases 1–4 implementation with Codex assistance | MIT, explicitly selected by owner on 2026-09-07; see root LICENSE and LICENSE_PROPOSAL.md | `src/`, `scripts/`, `tests/`, original documentation |
| Initial repository | Remote commit `fd433b4` from the user-designated repository | No license file present | Existing `html` preserved verbatim; README expanded |
| Encoder and head weights | Locally trained from seeded random initialization using this repository | Scoped MIT selected by owner; training-data attribution above | `artifacts/encoder.pt`; no third-party pretrained weights |
| Evaluation evidence | Computed by this repository | Project-generated output; data attribution above | `artifacts/*.json` |
| PyTorch 2.6.0+cpu | Installed distribution metadata; [source](https://github.com/pytorch/pytorch/tree/v2.6.0) | BSD-3-Clause, package metadata | Imported dependency; unmodified |
| NumPy 2.2.6 | Installed distribution LICENSE metadata; [source](https://github.com/numpy/numpy/tree/v2.2.6) | Core BSD-3-Clause; wheel contains additional third-party notices | Imported dependency; unmodified |
| scikit-learn 1.6.1 | Installed distribution LICENSE metadata; [source](https://github.com/scikit-learn/scikit-learn/tree/1.6.1) | Core BSD-3-Clause; wheel includes runtime notices | Imported dependency; unmodified; dataset license tracked separately |
| pytest 8.3.5 | Installed distribution metadata; [source](https://github.com/pytest-dev/pytest/tree/8.3.5) | MIT | Test dependency; unmodified |
| SciPy 1.15.3, joblib 1.4.2, threadpoolctl 3.6.0 | Installed package metadata and notice files in dependency_provenance.json | BSD-3-Clause cores; SciPy wheel includes separate runtime notices retained in DEPENDENCY_NOTICES.txt | Imported numerical dependencies; unmodified |
| Streamlit 1.45.1 | Installed metadata and version-tagged upstream LICENSE/NOTICES | Apache-2.0 core; bundled components have separate notices in STREAMLIT_NOTICES.txt | Imported UI dependency; unmodified |
| Plotly 6.1.2 | Installed distribution metadata | MIT | Imported chart dependency; unmodified |
| pandas 2.2.3 | Installed distribution metadata | BSD-3-Clause | Imported table dependency; unmodified |
| UI CSS and text | Original with Codex assistance | Scoped MIT | `assets/lab.css`, `src/ui.py` |
| Application logo | User-supplied PNG, added at the user's request after Phase 3 | Supplied for application use; no separate license inferred | `assets/memoryforge-logo.png`; original bytes preserved, displayed in sidebar and browser icon |
| App fonts and interface icons | System font stack plus Streamlit's bundled Adobe Source Sans/Code/Serif Pro, KaTeX fonts and Material Symbols | Adobe fonts: SIL OFL 1.1; Material icons: Apache-2.0; KaTeX license/notices retained upstream. Exact version-tagged text in STREAMLIT_NOTICES.txt | Dependency serves bundled font assets unmodified; not copied to assets/ |
| Digit display images | Dataset above, nearest-neighbor enlargement | Dataset attribution above | `src/visualization.py`; no generated or external artwork |
| Research sources | Four primary papers/reports and official BDH code, versioned in research_sources.json | Linked and paraphrased; no figures/full texts/source code copied | src/research.py; docs/RESEARCH_NOTES.md |

Package metadata was read using `importlib.metadata`. Package license names do
not replace full wheel notices or determine dataset rights. No third-party
package source or wheels are vendored here. Only their notice text is retained.

Phase 2 metadata and the installed package inventory are saved in
`artifacts/phase2_environment.json`. License names were read from installed
Streamlit, Plotly and pandas distributions. Phase 4's full installed inventory
and exact wheel notices supersede the earlier deferred review. The original Phase 2 UI used no image-generation
model, remote font service, third-party template or copied website. The later
user-supplied logo is recorded separately above.

Phase 3 adds original evidence/derivation code and reuses the existing dependency
stack. Official BDH code at 2b0d7a45b058d4309c84a10e0768d541fe18bdc2 was inspected
read-only; it is not a project dependency or vendored implementation. Sources'
licenses do not become the project license. The fresh installed package inventory
is captured in artifacts/phase3_robustness.json. Phase 4 adds the explicit MIT
choice, version constraints and notice inventory without changing the ML core.

The separately requested PDFs use original explanatory text and diagrams,
the supplied logo, and a Matplotlib plot of the existing Phase 3 observations.
No paper figure is reused. PDF text embeds Liberation Sans subsets (SIL Open
Font License 1.1); the plot embeds DejaVu Sans subsets with the distribution's
Bitstream/Arev notices. Exact notices are in PDF_FONT_NOTICES.txt. Optional PDF
authoring dependencies are isolated in requirements-pdf.txt and do not change
the application dependency set. The owner later selected scoped MIT for original
project material; third-party font rights remain separate.

## Installed dependency and asset record

`artifacts/dependency_provenance.json` records the 54 distributions in the
inspected Windows CPU environment: package name/version, upstream URLs, license
metadata/classifiers, modification status, and relative paths/hashes for 85
license/notice files. `docs/DEPENDENCY_NOTICES.txt` retains their exact text.
This includes dependency build tools and bundled runtime notices, not only the
ten direct application requirements. The lone distribution without a local
notice file was Streamlit; its version-tagged upstream LICENSE and NOTICES are
retained in `docs/STREAMLIT_NOTICES.txt`, with source URLs and hashes in
`artifacts/streamlit_notice_sources.json`. The upstream frontend record also
covers JavaScript dependencies used inside Streamlit controls.

Representative transitive terms include MIT, BSD, Apache-2.0, certifi's MPL-2.0,
Pillow's MIT-CMU, Python typing extensions' PSF-2.0 and numerical-library runtime
exceptions/notices. Do not replace these with the project's MIT label. A wheel
for another operating system can contain different bundled code; inspect that
wheel before claiming its notice inventory matches this Windows record.

The optional PDF authoring tools are ReportLab 4.4.9 (BSD), Matplotlib 3.11.1
(Matplotlib/PSF-based terms), and pypdf 6.10.0 (BSD-3-Clause), from their installed
package metadata. Their output contains original text/diagrams, the user logo,
the measured chart and the explicitly recorded embedded fonts. The tools' code
and wheels are not embedded in the PDF or vendored. The two PDF font notices
are included alongside the PDFs in the submission ZIP.

The supplied logo's original filename indicates a ChatGPT image. The team
provided the PNG and authorized application use; its generation history and
general reuse license have not been independently established. The MIT grant
explicitly excludes it. The pre-existing `html` file also has no identified
license, remains unchanged in the repository, is not executed by the app and
is excluded from the submission ZIP. No paper figures, checkpoints or code
from BDH/BDH-CQ are redistributed. Research is linked and paraphrased.

2026-09-08 release addendum: the installed inventory was refreshed after changing
PyArrow from 25.0.1 to 24.0.0 to match Community Cloud's observed compatibility
override. It still describes 54 Windows distributions and 85 notice files.
The hosted Linux install and app behavior were checked, but the complete Linux
wheel notice inventory was not downloaded or claimed equivalent. Community
Cloud additionally installs logging tools (rich, markdown-it-py, mdurl and
pygments); these provider-installed packages are not vendored in the ZIP.
