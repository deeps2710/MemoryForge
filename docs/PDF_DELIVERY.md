# MemoryForge PDF delivery

Redesigned on 2026-09-08 after inspecting the actual code, existing documents,
README, app screenshots, raw evaluations, research ledger and public prototype.
No application code, checkpoint or numerical evaluation changed.

- [Blog](../output/pdf/MemoryForge_Blog.pdf): six A4 pages with MemoryForge as the
  main title, two explained app screenshots, a vector architecture, exact
  equations, measured chart/table, failure analysis, research, limitations,
  proposed future work, potential sustainability and primary references.
- [One-page summary](../output/pdf/MemoryForge_OnePage_Summary.pdf): exactly one
  A4 page, about 526 extracted words including references, with MemoryForge as
  the main title. Body text is 10.8 pt. It defines the claim, mechanism,
  contribution, developer evidence, research boundaries and missing evidence.
- [Presentation viewing PDF](../output/pdf/MemoryForge_DataForge2026_Presentation.pdf):
  ten landscape pages rendered from the finalized PPTX. Its pages are raster
  images; the PPTX retains editable text, architecture and chart plus source notes.

`MemoryForge_Concept_Summary.pdf` is a byte-identical compatibility alias of the
new one-page summary for existing application links. It is not an older summary.
The older eight-slide deck and original PDF designs remain in Git history.

## Editable sources and reproduction

[BLOG.md](BLOG.md) and [CONCEPT_SUMMARY.md](CONCEPT_SUMMARY.md) are editable Markdown
writing sources. [build_pdfs.py](../scripts/build_pdfs.py) typesets them using
ReportLab, builds vector charts/tables from phase3_evidence.json and embeds the
unaltered supplied screenshot/logo files. It asserts page counts, content bounds,
mean reconstruction, extraction and the five expected citation targets.

Use an isolated authoring environment, separate from the application:

```sh
python -m venv .local/pdf-env
# Activate the environment or invoke its Python executable directly.
python -m pip install -r requirements-pdf.txt
python scripts/build_pdfs.py --font-dir PATH_TO_LIBERATION_SANS
```

The font directory must contain LiberationSans-Regular/Bold/Italic/BoldItalic.ttf.
The supplied documents use the Codex bundled PDF.js font files. Omitting
`--font-dir` uses standard PDF fonts and requires renewed visual review; the
published layout checks concern the embedded-font output. Font notices are in
[PDF_FONT_NOTICES.txt](PDF_FONT_NOTICES.txt). No standalone fonts are distributed.

To include the presentation PDF, first finalize/render the PPTX using the
[presentation instructions](PRESENTATION.md), then append
`--slide-render-dir .local/redesign/slides` to the PDF build command.
Copy the completed one-page file to the compatibility alias after verification.
This optional authoring step is not needed to launch the application.

## Verification and source scope

The primary full text for BDH, BDH-CQ, DeltaNet and Titans was rechecked on
2026-09-08. Version-specific links appear beside claims through numbered PDF
hyperlinks and in the sources. The MemoryForge citation pins revision 3751264,
whose application and evidence bytes match the inspected implementation.
DeltaNet's MAD comparison is a developer-reported synthetic benchmark with
borrowed baselines; it is not a MemoryForge result or external reproduction.

[PDF verification](../artifacts/pdf_verification.json) records final file hashes,
page/word counts, source hashes and visual checks. All seventeen PDF pages
(six blog, one summary and ten presentation) were rendered and inspected. The
presentation's ten finalized slides were also checked. This verifies the files,
not human comprehension or native desktop PowerPoint behavior.

These documents describe a functional public CPU prototype. Future work and
sustainability are proposals. [TEAM.md](TEAM.md) records newly assigned roles;
[AI_ASSISTANCE.md](AI_ASSISTANCE.md) and [PROVENANCE.md](PROVENANCE.md) disclose
assistance and separate asset rights. The separate blog's organizer-specific
format remains unspecified. Packaging does not submit a competition entry.
