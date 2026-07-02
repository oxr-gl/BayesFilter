# BayesFilter Agent Governance

## Default Implementation Backend

BayesFilter algorithmic implementation defaults to TensorFlow and TensorFlow
Probability.

## Default Execution Target

The BayesFilter repository default execution target is GPU.  CPU-only execution
is allowed for explicit reference checks, small smoke tests, debugging, and
sandbox-safe diagnostics, but it must not be described as the default
production target unless a reviewed plan explicitly changes this policy.

For DPF transport work, the default production algorithm target is the
GPU-oriented LEDH-PFPF-OT TF32 route: TensorFlow/TFP implementation, `float32`
tensors, TensorFlow TF32 execution enabled, streaming/chunked transport where
applicable, and explicit FP64 or FP32-no-TF32 only for reference/comparison
arms.  The historical module path under `experiments/dpf_implementation` is not
a reason to demote this route; future agents should treat the current owner
directive as the default production direction and should avoid reopening the
default-vs-experimental question without new evidence or human instruction.

This default-policy promotion is a product and engineering direction.  It does
not by itself certify posterior correctness, HMC readiness, statistical
superiority, dense Sinkhorn equivalence, or broad scientific validity.  Those
claims still require their stated evidence gates and artifacts.

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

GPU-oriented LEDH-PFPF-OT TF32 is now the default production target by owner
directive.  Evidence artifacts may still record unresolved scientific or HMC
gates, but they should not downgrade the default target back to "no production
default" merely because those separate gates remain open.

## Zhao-Cui Lane Source-Anchor Gate

For all Zhao-Cui high-dimensional filtering work, "faithful" has a binding
meaning: the agent must inspect and cite both the Zhao-Cui paper/math claim and
the local author source code before implementing, reviewing, or approving any
new source-route behavior.

## Zhao-Cui Production Route Boundary

For Zhao-Cui leaderboard and production work, the generic all-axes
multistate retained-grid route is diagnostic/historical only.  This includes
`bayesfilter/highdim/filtering.py::multistate_nonlinear_fixed_design_tt_value_path`
and `bayesfilter/highdim/filtering.py::multistate_nonlinear_fixed_design_tt_score_path`.
These routes may remain useful for tiny fixture diagnostics, lower-rung
tie-outs, and historical blocker preservation, but they must not be selected
as the production Zhao-Cui leaderboard evaluator.

The production-admissible Zhao-Cui direction is the fixed-variant source-route
path that avoids the generic full tensor-product retained-grid transition
route.  Do not revive the retained-grid path as a production candidate merely
because it emits a finite lower-rung value or score; use the fixed-variant
route for production planning and leaderboard wiring.

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

## Zhao-Cui Training Regularization Default

For Zhao-Cui training-base runs, L1 regularization with explicit L1 weight
tuning is the default procedure going forward.  This is a lane policy, not a
global `P75TrainableTTConfig` scalar default: `l1_weight=0.0` may remain an
allowed comparator arm inside a reviewed tuning grid, but fixed unreviewed
`l1_weight=0.0` training must not be treated as the default Zhao-Cui decision
path.

L1 weight tuning must preserve validation/audit separation.  Validation or
holdout data may nominate, select, or veto candidates only under a reviewed
plan; audit data remains reserved for final-only checks and must not be used
for tuning.  A selected L1 value requires a reviewed tuning/selection ledger
before it can support rank-convergence, HMC, production, or scientific claims.

The reviewed Phase 6T diagnostic showed lower LR plus L1 repaired a rank-5
training pathology, but that diagnostic does not by itself prove production
readiness, posterior correctness, HMC readiness, source-faithful TT-cross
training, or final rank convergence.

## Claude Review Prompt Shape

Claude review must start with the smallest exact path that can answer the gate.
The default prompt shape is:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: <one
question>. End with VERDICT: AGREE or VERDICT: REVISE.
```

Do not send artifact packets, broad path lists, pasted code chunks, whole-file
bundles, or repo-wide instructions as the first review attempt.  If Claude
needs more context, let Claude request the next exact path or line range, then
send only that bounded target.

This rule is deliberately operational.  It avoids repeated review stalls,
approval blocks, and over-broad external disclosure.  A review that can be
answered from a single result/subplan path should be asked as a one-path review.
