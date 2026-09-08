# MemoryForge presentation

DataForge 2026, Pathway track. **Team BitWise: Deepshikha Rani and Ved Patel.**

Open [the PowerPoint](../output/presentation/MemoryForge_BitWise_DataForge.pptx)
in a compatible slide viewer; running the application is not required to view it.
The deck contains exactly eight slides:

1. MemoryForge, its central claim and team.
2. Actual guided-lab screenshot with unchanged encoder weights.
3. Editable offline model-preparation DFD.
4. Editable session memory, retrieval and audit DFD, with the write/read equations.
5. Actual memory and conflict screenshots with measured outcomes.
6. Editable accuracy chart and the distinct roles of BDH, BDH-CQ, DeltaNet and Titans.
7. Deployment, reproducibility and limitations.
8. THANK YOU, both team members and their user-supplied contact addresses.

The [detailed DFD](DATA_FLOW.md) expands the two slide views into system context,
offline training/evaluation, runtime initialization and session adaptation, with
a data dictionary and code links. These describe implemented data flows.

## Evidence and assets

Four original 1280 x 720 PNG screenshots are in
[assets/screenshots](../assets/screenshots), captured from the public
[MemoryForge application](https://memoryforge.streamlit.app/) on 2026-09-08:

| File | Observed state and use |
|---|---|
| guided-lab.png | Seed 1000, three-write preset; slide 2 and README. |
| memory-and-retrieval.png | Six writes, 27/30 correct, actual matrix and scores; slide 5 and README. |
| conflict-outcome.png | Seven writes, 26/30 correct, five changed predictions; slide 5. |
| research-evidence.png | Saved paired-suite chart and results; README. |

These are browser captures, not generated interface mockups. The slides preserve
their aspect ratios; the original full-resolution files remain in the ZIP.
The chart uses [saved Phase 3 evidence](../artifacts/phase3_evidence.json), with
mean percentages rounded to two decimals in its embedded workbook and one
decimal in the visible labels. The full precision results remain in the JSON.
Primary citations are beside the research claims and full URLs are in speaker notes.
Deployment measurements are dated observations, not performance guarantees.

Text, DFD shapes/connectors and the evidence chart are native editable PowerPoint
elements. Screenshots and the user logo are raster images. Arial is referenced,
not embedded; no font files or authoring-library code are distributed with the
presentation. See [provenance](PROVENANCE.md) and [AI assistance](AI_ASSISTANCE.md)
for original-content licensing, separate logo/frontend rights and authoring disclosure.

## Authoring and verification

[build_presentation.mjs](../scripts/build_presentation.mjs) uses the Codex
Artifact Tool runtime, not the application Python environment. To regenerate,
set `ARTIFACT_NODE_MODULES` to the bundled Node modules directory,
`PRESENTATIONS_SKILL_DIR` to the installed presentations skill directory, and
`ARTIFACT_PYTHON` to its bundled Python executable. Set `DECK_REVISION` to a fresh
identifier, then run `node scripts/build_presentation.mjs` from the repository.
This optional toolchain is not needed to run MemoryForge or open the supplied PPTX.

The builder exports and finalizes a candidate under `.local/presentation-build`,
validates package structure, geometry, fonts and the chart workbook, imports the
final file and renders all eight slides. Inspect each rendered slide before
copying that finalized PPTX to the public `output/presentation` path. Private
drafts and validation scratch files are excluded from the submission ZIP.
The delivered eight-slide file received those checks and full-size visual review.
It was not opened in the desktop Microsoft PowerPoint application.

Run `python scripts/build_submission.py` after committing the reviewed files.
The ZIP builder requires the presentation, both PDFs, DFD, screenshot files and
application deliverables, then verifies every archived byte against its source.
