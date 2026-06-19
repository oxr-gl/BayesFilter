# P75 Phase 1 Result: Stochastic Objective Design Contract

metadata_date: 2026-06-17
status: PHASE1_PASSED_CLAUDE_AGREE_READY_FOR_PHASE2
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase1-stochastic-objective-design-subplan-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase0-objective-boundary-result-2026-06-17.md
next_subplan: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase2-implementation-surface-subplan-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | What exact stochastic density objective should the first P75 pilot implement? |
| Exact baseline/comparator | P73 blocked diagnostic and Phase 0 objective-boundary result. |
| Primary criterion | Satisfied.  This result freezes one implementable objective, train/eval split, exact normalizer treatment, CPU-only pilot ladder, gates, nonclaims, and Phase 2 handoff without implementation edits. |
| Veto diagnostics | No implementation code was edited.  No training, validation, HMC, scaling, GPU, rank promotion, threshold change, or audit-holdout training was launched. |
| Explanatory only | Candidate batch sizes, optimizer choices, parameter counts, and training-loss diagnostics. |
| What is not concluded | No implementation correctness, pilot success, lower-gate repair, validation readiness, HMC readiness, scaling claim, rank/sample policy, or adaptive Zhao--Cui parity. |
| Artifact preserving result | This result, Phase 2 subplan, execution ledger, review ledger. |

## Skeptical Plan Audit

Phase 1 passed the skeptical audit before execution.  It uses the actual P73
blocked diagnostic as the comparator, keeps Phase 1 design-only, separates
fresh training batches from audit holdout and audit-line samples, and prevents
training loss or a KL proxy from becoming a validation or lower-gate promotion
criterion.

## Frozen Density Family

Let \(z\in[-1,1]^d\) denote the local fixed-variant coordinate and let
\(\mu\) be the product reference measure used by the local `ProductBasis`.
Let \(h_\theta\) be a fixed-degree, fixed-rank functional tensor train.  The
pilot density is

\[
\rho_\theta(z) = h_\theta(z)^2 + \tau q_0(z),
\qquad
Z_\theta = \int \rho_\theta(z)\,d\mu(z),
\qquad
p_\theta(z)=\rho_\theta(z)/Z_\theta.
\]

Here \(q_0\) is the tensor-product defensive reference density already used by
`TensorProductReferenceDensity`, and \(\tau>0\) is the fixed defensive mass from
the existing Zhao--Cui fixed-variant lane.  In code-facing names this is the
`rho_theta` family.

The first pilot requires \(q_0(z)>0\) on the training and audit support and
\(\tau>0\).  Then \(\rho_\theta(z)\ge \tau q_0(z)>0\), so
\(\log\rho_\theta(z)\) is well-defined even when \(h_\theta(z)=0\).  If a
future variant sets \(\tau=0\), it must add a separately reviewed positive
denominator floor and may not reuse this Phase 1 contract unchanged.

For the first pilot, \(Z_\theta\) is exact:

\[
Z_\theta =
\int h_\theta(z)^2\,d\mu(z)
+ \tau \int q_0(z)\,d\mu(z),
\]

where the first term is computed by paired TT-core mass-matrix contractions,
the same mathematical contraction as `SquaredTTDensity.sqrt_square_normalizer`.
No Monte Carlo normalizer estimator is used in the first pilot.

## Training Objective

Let a fresh training batch be
\[
B_b=\{(z_{b,i},g_{b,i},w_{b,i})\}_{i=1}^m,
\]
where \(z_{b,i}\) are local fixed-variant coordinates, \(g_{b,i}\) are the
existing shifted square-root target values, and \(w_{b,i}\ge0\) are the
source-route fit weights or proposal weights.  The batch defines the empirical
target measure

\[
\alpha_{b,i}
=
{w_{b,i}\{g_{b,i}^2+\tau q_0(z_{b,i})\}
\over
\sum_{j=1}^{m}w_{b,j}\{g_{b,j}^2+\tau q_0(z_{b,j})\}},
\qquad
\sum_i \alpha_{b,i}=1.
\]

This is the trainable analogue of the weighting rule already used by the P73
density-aware evaluator.  If a later generator truly samples exactly from the
normalized target law, the special case is \(\alpha_{b,i}=1/m\).  The first
pilot otherwise uses the weighted empirical cross-entropy

\[
\widehat L_b(\theta)
=
-\sum_{i=1}^{m}\alpha_{b,i}\log \rho_\theta(z_{b,i})
+ \log Z_\theta
+ R(\theta).
\]

Equivalently, since
\(-\mathbb E_{\widehat q_b} \log p_\theta
=-\mathbb E_{\widehat q_b}\log\rho_\theta+\log Z_\theta\), this is a
stochastic forward-KL objective up to the entropy of the empirical target
measure, which is independent of \(\theta\).  The pilot therefore trains the
normalized density
\(p_\theta\), not a square-root regression fit to point values.

The initial regularizer is

\[
R(\theta)
=
\lambda_2 \sum_{k=1}^{d}\|G_k\|_F^2
+ \lambda_Z\{\log Z_\theta-\log Z_{\mathrm{ref}}\}^2,
\]

where \(G_k\) are the TT cores.  The first implementation may set
\(\lambda_Z=0\) by default and expose it as an opt-in stabilizer, but it must
record the value in the manifest.  If a normalizer anchoring term is enabled,
\(Z_{\mathrm{ref}}\) must be a predeclared initialization normalizer, not an
audit-derived quantity.

The regularization coefficients \(\lambda_2\), \(\lambda_Z\), and any future
penalty weights are part of model selection.  They must be predeclared in the
Phase 4 run contract or selected using training-only smoke evidence.  They
must not be tuned using audit holdout, audit replay, audit-line, validation,
HMC, or downstream sampler outcomes.

## Relation To P73 Evaluator

P73 already contains an explanatory evaluator,
`p73_density_aware_cross_entropy`, on a completed `SquaredTTDensity`.  That
function evaluates a cross-entropy-like term on an existing density and reports
`P73_B_OPTIMIZER_BLOCKED_NONLINEAR_OBJECTIVE_NOT_IMPLEMENTED`; it is not a
trainable optimizer.

P75 keeps the density objective but changes the implementation route.  It must
introduce an opt-in TensorFlow trainable adapter with persistent `tf.Variable`
TT cores.  The immutable `FunctionalTT`/`SquaredTTDensity` classes remain
evaluation and manifest surfaces, not the active training object.

## Training And Evaluation Split

Training samples:

- may use the existing fixed-variant diagnostic generator, frame, shift, and
  target-step construction;
- must be generated in fresh batches under training-specific seeds;
- must not reuse audit holdout, replay, or audit-line seeds;
- must not include any cloud declared as a certification or audit cloud.

Audit samples:

- remain held out from coefficient/parameter selection;
- are generated from the existing P72/P73 audit-holdout, audit-replay, and
  audit-line construction;
- are used only after training for fresh-audit residual and line gates;
- cannot be used for early stopping, model selection, learning-rate tuning, or
  threshold or regularization selection in the first pilot.

The no-audit rule is semantic as well as hash-based: an audit holdout point
must not influence trainable parameters even if it is regenerated under a
different label.

## First Pilot Ladder

The implementation should expose a small smoke rung before the larger user
target:

| Rung | Purpose | Degree/rank | Batch schedule | Pass role |
| --- | --- | --- | --- | --- |
| smoke | Verify finite TensorFlow objective, exact `log Z`, finite-gradient, update, manifest, and audit-separation plumbing | degree 1 or 2, rank 1 or 2 | very small CPU-only batches, at most a few steps | implementation mechanics only |
| target pilot | Test whether the intended sample scale can improve over the frozen P73 blocked diagnostic scale under the same fresh-audit gates | degree 2, rank 4 | CPU-only batch size 1024 for up to 500 fresh batches, stopping at the explicit Phase 4 wall-clock cap if reached first | bounded pilot evidence only |

The larger rung is not validation.  It can nominate the stochastic objective
for a larger reviewed plan only if finite-loss/gradient checks pass and fresh
audit diagnostics improve under frozen gates.

The frozen historical comparator is the P73 Phase 5 bounded diagnostic artifact
`docs/plans/bayesfilter-highdim-zhao-cui-p73-bounded-renewal-diagnostic-2026-06-17.json`,
especially row `rank_candidate_1_2_fit36` and the P73 Phase 6 handoff.  This
is a failed-scale comparator, not an apples-to-apples ALS superiority claim.
No "better than ALS" claim may be made unless Phase 4 also has a reviewed
same-degree/rank, same train/audit split, same-seed-family ALS comparator.

## Optimizer And Numerical Gates

The first optimizer is TensorFlow Adam in float64, with:

- fixed predeclared learning rate;
- fixed gradient global-norm clip;
- finite loss and finite-gradient checks before each update;
- finite exact normalizer and finite `log Z` checks;
- parameter-norm and gradient-norm logging;
- CPU-only execution with `CUDA_VISIBLE_DEVICES=-1` unless a later reviewed
  phase reaches a trusted GPU boundary.

Mechanics pass criteria:

- all objective components are finite;
- the gradient exists for every trainable core;
- at least one smoke update changes a core by a finite amount;
- the exact normalizer remains positive and above its predeclared floor;
- the result manifest records seeds, batch schedule, objective coefficients,
  optimizer settings, CPU/GPU status, and nonclaims.

Mandatory pilot-halting conditions:

- stop immediately on nonfinite loss, \(\rho_\theta\), `log Z`, regularizer,
  gradient, or parameter value;
- stop immediately if \(Z_\theta\) is nonpositive or at/below the normalizer
  floor;
- stop immediately if any trainable core has a missing gradient in the smoke
  rung;
- stop immediately if audit provenance or training/audit separation checks
  fail;
- stop the smoke rung after 5 CPU minutes or the predeclared smoke step count,
  whichever comes first;
- stop the target pilot after 500 batches, the Phase 4 predeclared wall-clock
  cap, or any veto above, whichever comes first.

Fresh-audit evidence criteria:

- audit holdout, audit replay, and audit-line samples are generated after or
  outside training from nontraining seeds;
- the same frozen P72/P73 residual and line gates are evaluated;
- audit diagnostics are primary for lower-gate evidence, while training loss,
  empirical KL/cross-entropy, and normalizer trajectories are explanatory.

## Nonclaims

- This is `extension_or_invention`, not source-faithful Zhao--Cui.
- The objective is not equivalent to Zhao--Cui adaptive ALS.
- A finite training loss is not validation.
- A decreasing cross-entropy estimate is not lower-gate repair.
- The smoke rung is not evidence for degree/rank/sample adequacy.
- The target pilot is not HMC, scaling, validation, or rank-promotion
  evidence.
- The frozen P73 comparator is not an apples-to-apples ALS win/loss baseline
  unless a later reviewed phase creates or identifies a same-schedule ALS row.

## Phase 2 Handoff

Phase 2 must map this design to concrete implementation surfaces and tests.
It must specify:

- the trainable TT adapter API;
- exact differentiable `rho_theta`, `log Z`, and objective functions;
- training-batch generation and provenance records;
- audit exclusion checks;
- smoke and target-pilot command surfaces;
- focused unit tests for finite-gradient behavior and exact-normalizer
  consistency;
- reviewed Phase 3 implementation boundaries.

Phase 2 remains planning-only.  It must not edit implementation code or run
training.

## Local Checks

Phase 1 local checks passed:

```text
test -s docs/plans/bayesfilter-highdim-zhao-cui-p75-phase0-objective-boundary-result-2026-06-17.md
rg -n "extension_or_invention|SquaredTTDensity|FixedTTFitter|P73_B_OPTIMIZER_BLOCKED|No training was run" ...
rg -n "rho_theta|log Z|KL|cross-entropy|audit holdout|finite-gradient|CPU-only|not validation" ...
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p75-phase1-stochastic-objective-design-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase2-implementation-surface-subplan-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-claude-review-ledger-2026-06-17.md
```

## Claude Review

Claude R1 returned `VERDICT: REVISE`.

Accepted repairs:

- froze the P73 blocked diagnostic as the historical comparator and barred
  same-schedule ALS superiority claims unless a later reviewed comparator is
  created;
- added explicit pilot-halting conditions;
- extended the no-audit rule to regularization coefficients;
- stated the positivity condition \(q_0>0,\tau>0\) needed for
  \(\log\rho_\theta\);
- changed the objective from an implicit unweighted average to the weighted
  empirical cross-entropy matching the current P73 density-aware evaluator,
  with the unweighted case only as an exact-target-sampler special case.

Claude R2 returned:

```text
VERDICT: AGREE
```

Claude agreed that the R1 blockers were repaired: frozen P73 comparator,
explicit halts, audit-free regularization selection, positivity/finiteness
for `log rho_theta`, required P75 runner surface, and weighted empirical
cross-entropy with exact `log Z`.
