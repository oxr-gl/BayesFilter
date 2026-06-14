# BayesFilter Agent Governance

## Default Implementation Backend

BayesFilter algorithmic implementation defaults to TensorFlow and TensorFlow
Probability.

New BayesFilter-owned algorithmic code must not use NumPy as its implementation
backend.  NumPy is allowed only for:

- independent reference solutions;
- comparison fixtures;
- closed-form sanity checks;
- serialization, reporting, and lightweight data inspection;
- narrowly reviewed exceptions recorded in a plan or result artifact.

Differentiable or gradient-bearing implementation paths must use TensorFlow /
TensorFlow Probability unless a reviewed plan explicitly authorizes another
autodiff backend.

PyTorch and JAX are non-default backends for this repository.  They require a
reviewed exception before use in BayesFilter-owned algorithmic implementation
paths.

## Evidence Discipline

Reference, comparison, prototype, smoke, and reporting code must not be
represented as the BayesFilter default implementation.  If an experimental lane
uses NumPy for a prototype or comparator, the artifact must say so explicitly
and must preserve the gap to a TensorFlow / TensorFlow Probability
implementation.

## Zhao-Cui Lane Source-Anchor Gate

For all Zhao-Cui high-dimensional filtering work, "faithful" has a binding
meaning: the agent must inspect and cite both the Zhao-Cui paper/math claim and
the local author source code before implementing, reviewing, or approving any
new source-route behavior.

Every proposed Zhao-Cui implementation choice must be classified before code is
written:

- `source_faithful`: matches a cited author paper/source operation, with
  source file and line anchors.
- `fixed_hmc_adaptation`: preserves the author's algorithmic route but freezes
  randomness, ranks, bases, schedules, or samples for differentiability/HMC.
  The frozen operation must still cite the author source route it adapts.
- `extension_or_invention`: not present in the author paper/source. It may be
  useful, but it must not close a Zhao-Cui source-faithfulness gap unless the
  user explicitly approves that extension as the target.

Veto rule: if a plan, implementation, result, or Claude review uses
"faithful", "source-faithful", "paper-scale Zhao-Cui", or equivalent language
without paper anchors and author source file/line anchors, block with
`BLOCK_SOURCE_UNGROUNDED`.  If a fixed-gradient need changes the route rather
than merely freezing the author's route, classify it as `extension_or_invention`
unless explicitly approved otherwise.

Claude/Codex review loops for this lane must verify anchors, not merely
internal consistency.  A review that does not inspect the cited paper/source
anchors cannot emit a valid `VERDICT: AGREE` for source-faithfulness.
