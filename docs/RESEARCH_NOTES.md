# Research verification and claim ledger

Verified 2026-09-07 from primary full text and official author-maintained code.
The [machine-readable claim ledger](research_sources.json) records authors,
claim, first public date, reviewed version, primary-source type, exact section,
evidence type, relevance and limitations for every research claim. The app reads
this same file and places each citation beside the claim.

| ID | Primary source | First public date | Inspected version | Evidence location |
|---|---|---|---|---|
| bdh | [The Dragon Hatchling: The Missing Link between the Transformer and Models of the Brain](https://arxiv.org/html/2509.26507v1) | 2025-09-30 | arXiv:2509.26507v1 | §1.2–1.3, §2.2 and §3 |
| delta | [Parallelizing Linear Transformers with the Delta Rule over Sequence Length](https://arxiv.org/html/2406.06484v3) | 2024-06-10 | arXiv:2406.06484v3 | §2.1–2.2; §3 |
| titans | [Titans: Learning to Memorize at Test Time](https://arxiv.org/html/2501.00663v1) | 2024-12-31 | arXiv:2501.00663v1 | §3.1–3.3, especially associative-memory objective and §3.2 |
| bdh-cq | [BDH-CQ: In-Context Learning with Recurrent Latent Reasoning](https://arxiv.org/html/2608.09888v1) | 2026-08-10 | arXiv:2608.09888v1 | §3.1–3.3, equations (1)–(4) |
| bdh-code | [Pathway official BDH baseline implementation](https://github.com/pathwaycom/bdh/blob/2b0d7a45b058d4309c84a10e0768d541fe18bdc2/bdh.py) | 2025-09-30 | 2b0d7a45b058d4309c84a10e0768d541fe18bdc2 | bdh.py: Attention.forward and BDH.forward; README baseline scope |

Four entries qualify as research papers/reports within 2022–2026. The official
code is additional primary evidence, not a fifth paper. The
[NeurIPS 2024 proceedings](https://proceedings.neurips.cc/paper_files/paper/2024/file/d13a3eae72366e61dfdc7eea82eeb685-Paper-Conference.pdf)
verify the DeltaNet paper's venue. Other papers are identified as preprints or
technical reports. Titans' first submission is 2024-12-31 despite its 2501
identifier. Publication does not establish independent reproduction.

The BDH connection is conceptual, not architectural equivalence. The ledger
separates the official baseline from BDH-CQ. For BDH-CQ, only the published
system-level interface is explained; proprietary dimensions and update rules
are not guessed. No ARC, language-model, biological, scaling or interpretability
benchmark claim is transferred to MemoryForge. DeltaNet and Titans motivate
questions about write mechanisms but are not implemented here.

Sources were read, not executed. No full paper, figure, external code or weights
are redistributed. The competition rules remain those in the user-supplied
brief; portal verification belongs to Phase 4.

## Local technical claims

| Claim | Evidence type | Authority | Limit |
|---|---|---|---|
| Encoder unchanged during adaptation | Exact tensor comparison | src/lab.py audit; tests/test_lab.py | Recorded model/environment |
| Scores equal class-mean memory times normalized query | Code and independent reconstruction | src/fast_memory.py; tests/test_evidence.py; tests/test_research.py | Uncalibrated scores |
| More support can help without monotonic improvement per seed | Paired observations | artifacts/phase3_evidence.json | 50 overlapping held-out episodes |
| Conflicts change actual state/predictions | Actual wrong-label writes | Same artifact's clean/corrupted conditions | Targeted repeated-first-key corruption |
| Charts use measured means and population deviations | Summary reconstruction and chart tests | src/evidence.py and src/research.py | Descriptive, not independent-sample intervals |
| Runtime works offline after installation | Blocked socket-connect tests | tests/test_research.py | Opening external sources still needs connectivity |

Local measurements use code/tests as their authority rather than borrowing
external paper results. See the [technical walkthrough](TECHNICAL_WALKTHROUGH.md).
