# Limitations

- The encoder learns digit representations by supervised training before fast
  adaptation. Fast memory learns arbitrary episode labels, not vision from scratch.
- sklearn digits is a small, simple 8x8 dataset. Held-out rows are unseen but their
  digit classes occur in encoder training. Results do not establish transfer to
  novel visual classes, language models or large-scale continual learning.
- MemoryForge is an educational fast-weight associative-memory model used to
  demonstrate the concept. It does not implement or reproduce BDH or BDH-CQ.
- Memory consists of class means of normalized keys. It has no learned memory
  rule, explicit decay, capacity parameter, meta-training or consolidation.
- Conflicting labels can interfere; the measured accuracy need not decrease on
  every episode. A single appended wrong-label write is the Phase 1 experiment.
- Softmax-normalized similarity scores are not calibrated probabilities. An empty
  memory abstains; 1/N is a theoretical random-guess reference, not its accuracy.
- Held-out examples may recur across episodes. Episode standard deviation describes
  this fixed benchmark; it is not a confidence interval over independent datasets.
- CPU deterministic replay is tested on the recorded environment. Bitwise equality
  across other operating systems, BLAS builds or library versions is not promised.
- Phases 2–3 provide the interactive UI, sourced research and evidence. Both
  requested PDFs are delivered. Phase 4 verifies deployment and submission
  packaging; see SUBMISSION_READINESS_REPORT.md for the actual release status.
- The lab fixes 3 classes, 30 queries and a support pool of 10 images/class; it
  starts at one shot/class. Its nested-prefix sampling differs from the Phase 1
  five-shot benchmark. Adding shots need not monotonically improve accuracy.
- The shot slider rebuilds clean memory, removing conflicts. Teach retains existing
  conflicts; repeated conflict clicks append the same wrong-label association.
  This is a controlled interference example, not a comprehensive robustness study.
- Browser reload discards temporary state. Shared cached embeddings/model are
  read-only application resources; session memory is isolated. No persistence,
  accounts or multi-worker load testing is implemented.
- Historical matrix snapshots are explicitly labelled and may differ from the
  current query scores. Actions switch the matrix view back to Current.
- Local core/AppTest timings and three browser observations are recorded separately.
  No remote latency, cold-start deployment guarantee or universal subsecond claim
  is made. AppTest excludes browser rendering and network transport.
- Text labels, numeric alternatives, keyboard slider/controls and 390 px responsive
  layout were checked. Full screen-reader/WCAG conformance and learning outcomes
  with human participants have not been established.
- Dataset attribution/license is recorded from the original UCI source. The owner
  selected scoped MIT for original project code, documents and generated weights.
  The supplied logo and pre-existing html retain separate, unresolved general
  reuse rights. The portal requires a ZIP; the organizer has not specified a
  separate blog format. Its four-page blog remains a submission-format draft.

- The Phase 3 suite uses 50 fixed seeds, nested shots and repeated corruption of
  one support key. Absolute conflict counts are not equal corruption rates across
  shot counts. Conditions share queries; the 19,500 outcomes are not independent.
- Error bars are population standard deviations, not confidence intervals or
  guarantees for another dataset. No held-out score selects new training settings.
- Research claims are version-specific primary-source paraphrases. Paper/code
  inspection does not reproduce published results. Proprietary BDH-CQ details
  are not inferred; no language, ARC, capacity or biological claim is validated
  by this digit toy.
- Offline tests deny socket connections after installation with fresh app caches;
  this is not a complete air-gapped browser audit. External source links need
  connectivity when opened. Phase 4 adds transitive version constraints from the
  verified environment; these are not hashes of platform-specific wheels.
