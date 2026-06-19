# P75 Phase 2 Result: Implementation Surface And Test Plan

metadata_date: 2026-06-17
status: PHASE2_PASSED_CLAUDE_AGREE_READY_FOR_PHASE3
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase2-implementation-surface-subplan-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase1-stochastic-objective-design-result-2026-06-17.md
next_subplan: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase3-optin-implementation-subplan-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | What minimal opt-in implementation surface can realize the Phase 1 objective without overclaiming? |
| Exact baseline/comparator | Phase 1 design result and current P73/P72 evaluator/gate surfaces. |
| Primary criterion | Satisfied.  This result maps the trainable variables, objective, exact normalizer, fresh-batch interface, audit exclusion, tests, command artifacts, and Phase 3 boundaries without code edits or training. |
| Veto diagnostics | No implementation code was edited.  No training, validation, HMC, scaling, GPU, rank promotion, threshold change, or package/network action was launched. |
| Explanatory only | Candidate file names, rough parameter count, and command shapes. |
| What is not concluded | No implementation correctness, pilot result, lower-gate repair, validation readiness, HMC readiness, scaling claim, or adaptive Zhao--Cui parity. |
| Artifact preserving result | This result, Phase 3 subplan, execution ledger, review ledger. |

## Skeptical Plan Audit

Phase 2 passed the skeptical audit before execution.  The planned artifacts
answer the phase question because they name concrete source, test, and runner
surfaces while keeping implementation and training out of this phase.  The
audit found no wrong baseline, proxy-metric promotion, missing stop condition,
unfair comparison, hidden GPU assumption, or command whose artifact would not
answer the planning question.

## Implementation Files

Phase 3 must create exactly these new implementation surfaces:

| Surface | Path | Role |
| --- | --- | --- |
| trainable objective module | `bayesfilter/highdim/stochastic_density_training.py` | Opt-in TensorFlow implementation of trainable TT density objective. |
| focused tests | `tests/highdim/test_p75_stochastic_density_training.py` | Unit tests and smoke tests for differentiability, objective terms, audit exclusion, and command schema. |
| visible pilot runner | `scripts/p75_stochastic_density_training_pilot.py` | CPU-only smoke and bounded-pilot command surface. |

Phase 3 must not modify top-level `bayesfilter.__all__`.  The first pass
should also avoid adding symbols to `bayesfilter.highdim.__all__`; tests may
import the new module directly as
`bayesfilter.highdim.stochastic_density_training`.  If Phase 3 discovers that
an internal export is necessary, it must document why and keep it
subpackage-scoped.

## Trainable API

The new module should define small, opt-in dataclasses or equivalent typed
helpers:

- `P75TrainableTTConfig`
  - `product_basis`;
  - `ranks`;
  - `tau`;
  - `normalizer_floor`;
  - `l2_weight`;
  - `logz_anchor_weight`;
  - `logz_reference`;
  - `learning_rate`;
  - `gradient_clip_norm`;
  - `seed`;
  - `metadata`.
- `P75ObjectiveBatch`
  - `points` with shape `[N, D]`;
  - `target_values` with shape `[N]`;
  - `weights` with shape `[N]`;
  - optional `point_records`;
  - optional `forbidden_audit_records`.
- `P75ObjectiveTerms`
  - scalar total loss;
  - weighted empirical cross-entropy;
  - exact `log Z`;
  - regularization;
  - normalizer;
  - alpha min/max/sum;
  - rho min/max;
  - gradient norm, when available;
  - status and nonclaims.
- `TrainableFunctionalTT`
  - persistent `tf.Variable` cores;
  - pure TensorFlow `evaluate(points)`;
  - pure TensorFlow `sqrt_square_normalizer()`;
  - pure TensorFlow `rho_theta(points)`;
  - pure TensorFlow `objective(batch)`;
  - `train_step(batch, optimizer)` with finite-gradient and clipping checks;
  - `snapshot_functional_tt()` and `snapshot_density()` for immutable
    evaluation/manifests.

The trainable path must not call `.numpy()` inside differentiable objective,
normalizer, `rho_theta`, or `log Z` functions.  `.numpy()` is allowed only
after a tape step for manifest/reporting serialization.

## Objective Contract

For a batch \(B=\{(z_i,g_i,w_i)\}_{i=1}^N\), the module must implement:

\[
\alpha_i =
{w_i(g_i^2+\tau q_0(z_i))
\over \sum_j w_j(g_j^2+\tau q_0(z_j))},
\qquad
\widehat L(\theta)
=-\sum_i\alpha_i\log\rho_\theta(z_i)+\log Z_\theta+R(\theta).
\]

The defensive reference for Phase 3 is `TensorProductReferenceDensity` on the
same `ProductBasis`; therefore \(q_0(z)=1\) under the reference-measure
convention used by the current local basis.  The implementation should still
call the defensive-density interface or an equivalent helper so the positivity
gate is explicit.

The exact normalizer is:

\[
Z_\theta=\int h_\theta(z)^2\,d\mu(z)+\tau\int q_0(z)\,d\mu(z).
\]

The first term must use paired-core mass contractions in TensorFlow, matching
`SquaredTTDensity.sqrt_square_normalizer()` after snapshot.  The second term
must use the defensive normalizer under the same `MassMeasure`.

## Audit Exclusion Contract

Phase 3 must implement a small provenance check for `P75ObjectiveBatch`:

- records with role `audit` or `audit_line` are rejected if they appear in
  training records;
- overlap between training cloud hashes and forbidden audit cloud hashes is a
  hard block;
- if no records are supplied, synthetic/unit tests may proceed but the manifest
  must mark provenance as `unrecorded_test_only`.

The runner must keep training seeds separate from P72/P73 audit seeds.  Audit
holdout, audit replay, and audit-line samples may be evaluated only after
training and may not select learning rate, regularization coefficients,
stopping point, rank, or degree.

## Runner Contract

`scripts/p75_stochastic_density_training_pilot.py` must support at least:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_stochastic_density_training_pilot.py --schema-only
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_stochastic_density_training_pilot.py --smoke-only --output docs/plans/bayesfilter-highdim-zhao-cui-p75-smoke-2026-06-17.json
```

Phase 3 may implement `--pilot` or `--target-pilot` as a schema-ready option,
but Phase 4 controls whether it is executed.  The runner must record:

- command;
- git state;
- CPU/GPU status with `CUDA_VISIBLE_DEVICES`;
- objective coefficients;
- optimizer settings;
- batch sizes and step counts;
- seeds;
- exact pilot-halting conditions;
- output paths;
- nonclaims.

## Test Plan

Phase 3 must run CPU-only focused tests:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p75_stochastic_density_training.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_stochastic_density_training_pilot.py --schema-only --output /tmp/p75-schema.json
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_stochastic_density_training_pilot.py --smoke-only --output /tmp/p75-smoke.json
```

Required test assertions:

- `tf.Variable` cores are watched by `GradientTape`;
- exact trainable normalizer equals immutable `SquaredTTDensity.normalizer`
  on a tiny one- or two-dimensional TT after snapshot;
- trainable `rho_theta(points)` equals immutable
  `snapshot_density().unnormalized_density(points)` on the same tiny points;
- trainable normalized log-density,
  `log rho_theta(points) - log Z`, equals immutable
  `snapshot_density().log_density(points)` on the same tiny points;
- weighted empirical cross-entropy normalizes
  \(\alpha_i\propto w_i(g_i^2+\tau q_0(z_i))\);
- uniform weights and constant target produce the expected unweighted special
  case;
- objective returns finite loss, exact `log Z`, and finite gradients;
- one optimizer step changes at least one core by a finite amount;
- audit records or overlapping audit hashes are rejected;
- the P75 runner records CPU-only status and nonclaims;
- P73-B remains blocked and distinct from P75;
- P72/P73 regression assertions pass:
  `p73_density_aware_optimizer_status()["status"]` remains
  `P73_B_OPTIMIZER_BLOCKED_NONLINEAR_OBJECTIVE_NOT_IMPLEMENTED`, P72/P73
  runner import paths still load, and no P75 code is imported by default P72
  or P73 entrypoints.

Phase 3 smoke is operationally bounded:

- synthetic fixture only;
- no Zhao--Cui target-generated fresh batches;
- at most 2 optimizer steps;
- tiny dimension at most 2, degree at most 2, rank at most 2;
- batch size at most 8;
- no audit gate, validation, HMC, scaling, GPU, rank promotion, or target
  pilot;
- smoke manifest must state `smoke_only_not_pilot_evidence`.

## Phase 3 Boundaries

Phase 3 may:

- create the three P75 files listed above;
- add narrowly necessary imports inside the new files;
- use TensorFlow/TensorFlow Probability only for differentiable
  implementation;
- use Python/JSON utilities for manifests and reporting;
- run the focused CPU-only tests and runner smoke commands.

Phase 3 must not:

- change default P72/P73 behavior;
- change `FixedTTFitter` or `SquaredTTDensity` unless a focused test proves
  the new adapter cannot be implemented separately;
- use NumPy as the differentiable backend;
- run the degree 2/rank 4/1024/500 target pilot;
- run validation, HMC, scaling, GPU, or rank promotion;
- claim lower-gate repair from training loss or smoke success.
- thread P75 into default P72/P73 code.  If Phase 3 needs to modify P72/P73
  entrypoints, it must stop and write a blocker instead.

## Phase 3 Handoff

Phase 3 may begin only after this result, the Phase 3 subplan, local checks,
and Claude review pass.  Phase 3 is the first phase allowed to edit
implementation code, and only the opt-in P75 surfaces described here are in
scope.

## Local Checks

Phase 2 local checks passed:

```text
test -s docs/plans/bayesfilter-highdim-zhao-cui-p75-phase1-stochastic-objective-design-result-2026-06-17.md
rg -n "rho_theta|log Z|KL|cross-entropy|audit holdout|finite-gradient|CPU-only|not validation" ...
rg -n "Trainable|tf.Variable|GradientTape|normalizer|Adam|audit exclusion|CPU-only|pytest|no training" ...
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p75-phase2-implementation-surface-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase3-optin-implementation-subplan-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-claude-review-ledger-2026-06-17.md
```

## Claude Review

Claude R1 returned `VERDICT: REVISE`.

Accepted repairs:

- added required `rho_theta` and normalized log-density equality tests against
  immutable `SquaredTTDensity`;
- bounded Phase 3 smoke as synthetic-only, at most 2 steps, tiny dimension,
  tiny batch, and not pilot evidence;
- added explicit P72/P73 regression checks and a stop rule forbidding P75
  threading into default P72/P73 entrypoints.

Claude R2 returned:

```text
VERDICT: AGREE
```

Claude agreed the R1 blockers were repaired: direct `rho_theta` and
log-density equality tests, bounded synthetic smoke, and explicit P72/P73
regression checks plus stop rule.
