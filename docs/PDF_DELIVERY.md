# Separate PDF delivery before Phase 4

The user explicitly requested these two documents while keeping Phase 4 unstarted.
This authorizes the documents only; it does not initiate deployment or the
remaining submission-hardening phase.

- [Project blog](../output/pdf/MemoryForge_Blog.pdf): four pages, about 1,816
  extracted words including headers/references; mechanism, actual failure example,
  measured vector chart, research connections and reproduction commands.
- [One-page concept summary](../output/pdf/MemoryForge_Concept_Summary.pdf): exactly
  one A4 page; 630 extracted words including headers/references, with 531 words
  in its Markdown text before the reference section. Main text is 10 pt, with
  12.2 pt line spacing; references are 8 pt. It is a self-contained briefing.

Both use the supplied logo and clickable citations. No application code, model,
experiment result or application dependency changed. The documents refer to the
verified implementation at f3ec52e and its existing measured evidence.

## Editable sources and reproduction

[BLOG.md](BLOG.md) and [CONCEPT_SUMMARY.md](CONCEPT_SUMMARY.md) are the editable
writing sources. [build_pdfs.py](../scripts/build_pdfs.py) typesets them with
ReportLab and builds the chart directly from phase3_evidence.json with Matplotlib.
It verifies the table's means/population deviations against the recorded rows.
The plot is merged as vector PDF content, retaining sharp text and lines.

Use a separate document-authoring environment:

```sh
python -m venv .local/pdf-env
# Activate it, or substitute its Python executable below.
python -m pip install -r requirements-pdf.txt
python scripts/build_pdfs.py
```

The default uses standard PDF fonts and was also successfully built. For the
delivered embedded typography, pass `--font-dir PATH` pointing to the four
LiberationSans-Regular/Bold/Italic/BoldItalic.ttf files. Font notices are in
[PDF_FONT_NOTICES.txt](PDF_FONT_NOTICES.txt); no standalone fonts are included.

Final outputs go to output/pdf/. Temporary layout and plot files go to tmp/pdfs/.
The builder checks page counts, word count, text extraction, citations and table
values. It does not replace rendered visual inspection after changing the text.

## Evidence and claim verification

The project's raw and replay artifacts remain unchanged. Their canonical digest
is 2a50066a46766a3ebe5e3ffda33e009200b5c15206104d10aa368d3bdd322eab.
Blog examples use the measured seed-1000 transitions; its chart uses all 50 seeds.
The two-dimensional dot-product example is explicitly hand-calculated rather
than described as a dataset observation.

Primary full text was rechecked on 2026-09-07:

| Claim used in the documents | Primary source / evidence location | Scope |
|---|---|---|
| Attention uses query-key affinity to combine values | [Vaswani et al.](https://arxiv.org/html/1706.03762v7), section 3.2 | Architecture definition |
| Retrieval-error update; MAD recall/memorization comparison | [Yang et al.](https://arxiv.org/html/2406.06484v3), section 2.2 and Table 1 | Author-reported synthetic benchmark; comparison baselines borrowed from earlier work |
| Fixed connections and changing Hebbian state | [BDH](https://arxiv.org/html/2509.26507v1), sections 1.2 and 2.2 | Published architecture, not the toy implementation |
| Context memory versus recurrent query workspace | [BDH-CQ](https://arxiv.org/html/2608.09888v1), section 3, equations 1-4 | Published interface; proprietary internals not inferred |
| Neural memory optimized at test time | [Titans](https://arxiv.org/html/2501.00663v1), section 3 | Distinct from the lab's gradient-free adaptation |

The external MAD comparison is never presented as MemoryForge's result or as a
deployment/independent reproduction. No external paper figure was copied.

## Quality and scope checks

[pdf_verification.json](../artifacts/pdf_verification.json) records final file
hashes, page/word counts, citation targets, text bounds and the visual review.
All five final pages were rendered with Poppler and inspected. No clipping,
overlap, broken symbols or table defects were observed. The one-page review
checked the central claim, mechanism, BDH/CQ distinction, evidence types and
limitations against the user's supplied criteria. It does not claim an
independent human comprehension study or completed team technical defense.

The concept PDF satisfies the requested one-page artifact requirement. The
separate blog PDF is also delivered. Actual portal acceptance, upload rules,
license choices and public deployment remain unverified later-phase work.
Phase 4 remains **NOT STARTED**.
