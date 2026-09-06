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
- Phase 1 has no interactive UI, latency guarantee, research integration, public
  deployment or submission PDFs. These remain explicitly gated future phases.
- Dataset attribution/license is recorded from the original UCI source. The team
  has not selected a license for project code or generated model weights.
  Final provenance review and the portal's blog-PDF versus concept-summary-PDF
  distinction remain unresolved.
