# Judging rubric audit

The weights below are from physical page 11 of the inspected organizer PDF.
They are maxima, not predicted or guaranteed scores. This is an agent review
of the submission and recorded evidence, not an external evaluation.

| Criterion / weight | Strength and evidence | Weakness / remaining uncertainty | Worthwhile final action |
|---|---|---|---|
| Technical correctness and depth /25 | Independently constructed-vector tests validate outer products, means and retrieval; exact encoder equality and disjoint sample IDs are checked. 650 saved conditions replay; equations and source claims are traceable in TECHNICAL_WALKTHROUGH.md and research_sources.json. | Toy class means are not BDH, language reasoning or new-category few-shot learning; overlapping episodes limit statistical inference. | Team traces one raw write and query and explains the different Phase 1/UI samplers. Do not add a new architecture before submission. |
| Technical ownership and live defense /15 | Code, evidence and 12 defense questions have a detailed walkthrough; AI assistance and original versus reused material are disclosed. | Human review, comprehension and live defense are UNVERIFIED. Agent-generated explanations cannot establish team ownership. | Rehearse DEMO_SCRIPT.md and explain each major component without reading generated prose verbatim. |
| Learning effectiveness /15 | One falsifiable claim, explicit audience/prerequisites, guided preset then playground, immediate-feedback quiz, truthful failure and reset. Browser/AppTest evidence in Phase 2/3 reports. | No human learner study; a one-minute script is not proof that unfamiliar learners finish in one minute. | Have an average data scientist use the resource and explain what changed; record feedback only if it occurs. |
| Interactive substrate and honesty /15 | Real writes/queries and exact matrices; truth beside predictions; live versus saved labels; local latency measurements and non-monotonic failures retained. | Public cold-start/network latency and multi-user load are not established by local timings. | Verify the deployed URL in a browser without an owner session and replay the demo. |
| BDH/CQ integration and evidence discipline /10 | Substantial module connects current state and equations to four recent primary papers; BDH versus CQ workspace/parameter distinctions are explicit. Sources are versioned and adjacent. | No official checkpoint run or external paper reproduction; CQ details remain proprietary. | Keep the “not an implementation” boundary explicit in the live defense; do not infer proprietary updates. |
| Craft, robustness, accessibility and provenance /10 | Logo, responsive 390 px checks, numeric alternatives, dependency constraints, exact notices, MIT scope and reproducible package. Final clean-install evidence is recorded in phase4_robustness.json when complete. | No full WCAG audit, concurrent load test or proof of downstream logo rights. Deployment/account steps remain external dependencies. | Finish actual public-access checks and review separate asset notices; retain those limits in the README. |
| One-page concept summary /10 | One A4 page; 630 extracted words; central claim, mechanism, architecture comparison, local evidence, correctly labelled MAD benchmark, BDH/CQ roles and primary citations. PDF_DELIVERY.md and pdf_verification.json contain visual/content evidence. | No independent human comprehension review; it cannot establish production maturity for a toy. The separate blog's format remains unspecified. | Read the summary without the app and explain the state/update distinction and strongest missing evidence. Confirm any later organizer upload guidance. |

The most valuable remaining work is public deployment verification and human
technical rehearsal. More charts, new datasets or larger models would add scope
without resolving those two gaps. The one-page summary is distinct from the
blog; the portal accepts one ZIP, and the ZIP must still contain the required
links and supporting materials.
