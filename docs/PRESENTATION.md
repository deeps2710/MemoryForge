# MemoryForge presentation

DataForge 2026 / PS-1 - Pathway. Team BitWise: **Ved Patel and Deepshikha Rani**.
The [role allocation](TEAM.md) records the user's authorization and distinguishes
assigned responsibilities from verified contribution history.

Open the [PowerPoint](../output/presentation/MemoryForge_DataForge2026_Presentation.pptx)
or its [PDF viewing copy](../output/pdf/MemoryForge_DataForge2026_Presentation.pdf).
The deck has ten slides, ending with THANK YOU:

1. DataForge-first cover with MemoryForge as the largest title, topic, track, team and role column.
2. Problem, working prototype and measured encoder/memory distinction.
3. Exact implemented S/c/M class-mean write and read equations.
4. Editable architecture with offline preparation, runtime path and tech stack.
5. Actual memory screenshot with Teach, Test Query and Clear Memory explanations.
6. Editable chart from the 50-seed evidence suite, with evaluation limits.
7. Actual conflict screenshot and the measured 27/30 to 26/30 failure.
8. Sourced BDH, BDH-CQ, DeltaNet and Titans distinctions; PS-1 alignment.
9. Reuse, scale limits, proposed experiments and a potential sustainability model.
10. THANK YOU, both team members, contact addresses and the live demonstration URL.

The [detailed DFD](DATA_FLOW.md) remains the complete four-view data-flow document.
The architecture slide summarizes it; the presentation does not claim a new
architecture or a BDH/CQ implementation. Future work is planning only.

## Evidence and assets

The original 1280 x 720 PNG screenshots in [assets/screenshots](../assets/screenshots)
were captured from the public application on 2026-09-08. The public preset was
inspected again before redesign and showed the same values, without owner login.

| File | State and use |
|---|---|
| guided-lab.png | Three-write preset, encoder delta 0 and memory delta 1.73205; slide 2, blog page 1 and README. |
| memory-and-retrieval.png | Six writes, 27/30 correct, actual matrix and scores; slide 5 and README. |
| conflict-outcome.png | Seven writes, 26/30 correct, five changed predictions; slide 7 and blog page 3. |
| research-evidence.png | Saved paired-suite chart and results; README. |

Captions identify each action, changed state and implication. Screenshot bytes
and aspect ratios are unchanged. The native chart reads phase3_evidence.json;
its embedded workbook rounds means to 0.01 percentage point, with visible labels
to 0.1. Primary paper identifiers appear beside claims and full URLs in notes.
Local evidence links pin the inspected implementation to revision 3751264.

Text, architecture connectors and chart are editable PowerPoint elements.
Screenshots and the logo are raster images. The ten-page PDF is a 192-dpi raster
viewing companion made from the finalized deck's renders; use the PPTX for
editing, text selection and speaker notes. Arial is referenced in the PPTX,
not embedded. No authoring-library code or font binaries are redistributed.

## Authoring and verification

The project script [build_presentation.mjs](../scripts/build_presentation.mjs)
requires the Codex Artifact Tool authoring runtime. Set `ARTIFACT_NODE_MODULES`
to its Node modules directory, `PRESENTATIONS_SKILL_DIR` to the installed
presentations skill directory, and `ARTIFACT_PYTHON` to its Python executable.
Set `DECK_REVISION` to a new revision identifier and run:

```sh
node scripts/build_presentation.mjs
```

The builder writes private candidates under `.local/redesign`, validates package,
geometry, font policy and chart workbook, imports the finalized file, and renders
ten slides at 2560 x 1440. Visually inspect them before copying the finalized
PPTX unchanged to the public output path. `build_pdfs.py --slide-render-dir`
creates the PDF viewing copy; see [PDF delivery](PDF_DELIVERY.md).

All ten final slides and all PDF pages received rendered visual review. Desktop
PowerPoint execution was not available and is not claimed. The authoring runtime
is optional; opening the deck and running the app do not require it.
The superseded eight-slide PPTX is retained in Git history, not the current ZIP.
