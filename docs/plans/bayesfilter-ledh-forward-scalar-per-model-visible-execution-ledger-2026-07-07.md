# LEDH Forward Scalar Per-Model Visible Execution Ledger

Date: 2026-07-07

Status: `DRAFT_LAUNCH_PACKAGE_CREATED`

Master program:

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-master-program-2026-07-07.md`

Runbook:

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-visible-gated-execution-runbook-2026-07-07.md`

## Ledger

### 2026-07-07 - Launch Package - PRECHECK

Evidence contract:

- Question: Can each intended high-dimensional LEDH row produce an executable
  same-target observed-data log likelihood estimator artifact?
- Baseline/comparator: July 6 Phase 3 admitted/blocked result, July 6
  per-model amendment plan, current forward contract metadata, row datasets,
  and row-specific reference checks where available.
- Primary criterion: a row is value-admitted only when a validated executable
  artifact reports finite `log_likelihood` values from the row target
  correction at the required row scale.
- Veto diagnostics: metadata-only admission, callback-only admission,
  proposal/flow objective used as likelihood, wrong row target, actual-SV/KSC
  artifact borrowing, score implementation before scalar admission, or
  runtime/memory/finite output promoted as correctness.
- Nonclaims: no score correctness, score admission, HMC readiness, posterior
  correctness, scientific superiority, or fair runtime ranking.

Actions:

- Created draft master program, visible runbook, stop handoff, Phase 0 subplan,
  and launch review bundle.

Artifacts:

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-master-program-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-visible-gated-execution-runbook-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-visible-stop-handoff-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase0-baseline-guard-subplan-2026-07-07.md`
- `docs/reviews/bayesfilter-ledh-forward-scalar-per-model-launch-review-bundle-2026-07-07.md`

Gate status:

- `IN_PROGRESS_PENDING_LOCAL_CHECKS_AND_REVIEW`

Next action:

- Run launch package local checks, then bounded read-only review.

### 2026-07-07 - Launch Package - REVIEW_REPAIR_LOOP_1

Evidence contract:

- Question: Does the launch package prevent another bundled Phase 3 failure by
  making same-target scalar admission executable, row-specific, and
  forward-scalar-only?
- Primary criterion: review must agree that stop conditions cover the known
  failure modes before Phase 0 launches.
- Veto diagnostics: missing stop condition for callback-only evidence or
  actual-SV/KSC artifact borrowing.
- Nonclaims: no Phase 0 execution, model implementation, value admission, or
  score admission yet.

Actions:

- Ran bounded Claude read-only launch review.
- Review returned `VERDICT: REVISE`.
- Finding: high-level evidence contracts listed callback-only admission and
  actual-SV/KSC artifact borrowing as vetoes, but the concrete Phase 0 and stop
  handoff stop conditions omitted them.
- Patched Phase 0 stop conditions and visible stop handoff to make those
  blockers explicit.

Artifacts:

- Review run dir:
  `/home/chakwong/BayesFilter/.claude_reviews/20260707-022825-ledh-forward-scalar-per-model-launch`
- Patched:
  `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase0-baseline-guard-subplan-2026-07-07.md`
- Patched:
  `docs/plans/bayesfilter-ledh-forward-scalar-per-model-visible-stop-handoff-2026-07-07.md`

Gate status:

- `IN_PROGRESS_PENDING_REPAIR_CHECKS_AND_REVIEW`

Next action:

- Rerun launch package local checks and a focused read-only repair review.

### 2026-07-07 - Launch Package - REVIEW_REPAIR_ACCEPTED

Evidence contract:

- Question: Did the focused repair close the launch blocker?
- Primary criterion: review agrees the concrete stop surfaces now include
  callback-only evidence and actual-SV/KSC cross-use blockers.
- Nonclaims: no Phase 0 execution, model implementation, value admission, or
  score admission yet.

Actions:

- Ran focused local repair checks.
- Ran bounded Claude read-only repair review.

Artifacts:

- Review run dir:
  `/home/chakwong/BayesFilter/.claude_reviews/20260707-023901-ledh-forward-scalar-per-model-launch-repair1`
- Review status: `REVIEW_STATUS=agreed`, `VERDICT=AGREE`.

Gate status:

- `PASSED_LAUNCH_GATE_PHASE0_MAY_START`

Next action:

- Launch Phase 0 only.

### 2026-07-07 - Phase 0 - BASELINE_GUARD_PASSED

Evidence contract:

- Question: Does the current repo state distinguish metadata-only forward
  contracts from executable same-target scalar admission, and what is the exact
  admitted/blocked baseline?
- Target scalar: `observed_data_log_likelihood_estimator`, reported as
  `log_likelihood`.
- Primary criterion: local focused checks pass and Phase 0 records exactly two
  value-admitted rows and four value-blocked rows.
- Veto diagnostics: metadata-only row promotion, blocked-row promotion, score
  work, or target redefinition.
- Nonclaims: no new value admission, score admission, score correctness, GPU
  evidence, leaderboard rebuild, HMC readiness, posterior correctness,
  scientific superiority, or runtime ranking.

Actions:

- Ran focused local Phase 0 checks.
- Wrote Phase 0 result.
- Drafted Phase 1 shared runner schema subplan.
- Patched the Phase 0/Phase 1 review bundle so the bounded packet states the
  target scalar explicitly.
- Patched Phase 1 nonclaims to include score correctness explicitly.
- Ran bounded Claude read-only review of the Phase 0 result and Phase 1
  subplan handoff.

Artifacts:

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase0-baseline-guard-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase1-runner-schema-subplan-2026-07-07.md`
- `docs/reviews/bayesfilter-ledh-forward-scalar-per-model-phase0-result-phase1-subplan-review-bundle-2026-07-07.md`

Local checks:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py -q
```

Result:

```text
12 passed, 2 warnings in 2.74s
```

Review:

- Run dir:
  `/home/chakwong/BayesFilter/.claude_reviews/20260707-025112-ledh-forward-scalar-per-model-phase0-phase1-handoff`
- `REVIEW_STATUS=agreed`, `VERDICT=AGREE`.

Gate status:

- `PASSED_PHASE0_PHASE1_HANDOFF_PHASE1_MAY_START`

Next action:

- Execute Phase 1 shared executable artifact schema guard.

### 2026-07-07 - Phase 1 - SCHEMA_GUARD_PASSED

Evidence contract:

- Question: Is there a shared executable artifact schema/validator that
  prevents metadata-only, callback-only, wrong-target, and actual-SV/KSC
  cross-use admission?
- Target scalar: `observed_data_log_likelihood_estimator`, reported as
  `log_likelihood`.
- Primary criterion: local validator/tests reject artifacts without executable
  `log_likelihood` evidence and reject target/flow ambiguity before row
  admission.
- Veto diagnostics: metadata-only contract passes; callback-only evidence
  passes; proposal scalar passes; target density correction missing; tiny
  artifact is admitted; actual-SV/KSC cross-use passes; theta mismatch passes.
- Nonclaims: no model row admission, score admission, score correctness, GPU
  evidence, leaderboard rebuild, HMC readiness, posterior correctness,
  scientific superiority, or runtime ranking.

Actions:

- Added `validate_ledh_forward_scalar_artifact(...)`.
- Added canonical executable schema version:
  `bayesfilter.highdim.ledh_forward_scalar_artifact.v1`.
- Added focused schema/admission guard tests.
- Ran Phase 1 required local checks.
- Wrote Phase 1 result.
- Drafted Phase 2 LGSSM subplan.
- Ran bounded Claude read-only Phase 1 handoff review.
- Review returned `VERDICT=REVISE` because theta values were not enforced
  against forward-contract `truth_theta`.
- Patched validator, tests, Phase 1 result, and Phase 2 stop conditions.
- Reran focused and required Phase 1 checks.
- Ran bounded Claude read-only repair review.

Artifacts:

- `bayesfilter/highdim/ledh_forward_contract.py`
- `tests/highdim/test_ledh_forward_scalar_admission_guard.py`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase1-runner-schema-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase2-lgssm-subplan-2026-07-07.md`
- `docs/reviews/bayesfilter-ledh-forward-scalar-per-model-phase1-review-bundle-2026-07-07.md`
- `docs/reviews/bayesfilter-ledh-forward-scalar-per-model-phase1-repair1-review-bundle-2026-07-07.md`

Local checks:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py -q
```

Result:

```text
12 passed, 2 warnings in 3.23s
```

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py -q
```

Result:

```text
24 passed, 2 warnings in 2.72s
```

Review:

- Initial review run dir:
  `/home/chakwong/BayesFilter/.claude_reviews/20260707-032055-ledh-forward-scalar-per-model-phase1-phase2-handoff`
- Initial status: `REVIEW_STATUS=revise`, `VERDICT=REVISE`.
- Repair review run dir:
  `/home/chakwong/BayesFilter/.claude_reviews/20260707-033721-ledh-forward-scalar-per-model-phase1-repair1`
- Repair status: `REVIEW_STATUS=agreed`, `VERDICT=AGREE`.

Gate status:

- `PASSED_PHASE1_PHASE2_HANDOFF_PHASE2_MAY_START`

Next action:

- Execute Phase 2 LGSSM forward scalar reconfirmation.

### 2026-07-07 - Phase 2 - LGSSM_FORWARD_SCALAR_LOCAL_PASS

Evidence contract:

- Question: Can the LGSSM row produce or preserve an executable same-target
  observed-data log likelihood artifact under the shared schema?
- Target scalar: `observed_data_log_likelihood_estimator`, reported as
  `log_likelihood`.
- Primary criterion: canonical LGSSM artifact validates with
  `require_admitted=True`, finite `log_likelihood_by_seed`, full-row scale, and
  exact Kalman target identity.
- Veto diagnostics: missing likelihood vector, wrong target scalar, wrong
  exact comparator, theta mismatch, failed schema validation, score evidence
  used for value admission, or runtime-only admission.
- Nonclaims: not nonlinear-row evidence, no score admission, no score
  correctness, no leaderboard rebuild, no new GPU model evidence, no HMC
  readiness, no posterior correctness, no scientific superiority, and no
  runtime ranking.

Actions:

- Normalized the existing LGSSM N=10000 value artifact into the Phase 1
  canonical executable artifact schema.
- Validated the canonical artifact with
  `validate_ledh_forward_scalar_artifact(..., require_admitted=True)`.
- Added Phase 2 LGSSM artifact replay tests.
- Ran focused and combined local checks.
- Wrote Phase 2 result.
- Drafted Phase 3 fixed SIR subplan.

Artifacts:

- `docs/plans/ledh-phase2-lgssm-forward-scalar-artifact-2026-07-07.json`
- `docs/plans/ledh-phase2-lgssm-forward-scalar-artifact-2026-07-07.md`
- `tests/highdim/test_ledh_phase2_lgssm_forward_scalar_artifact.py`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase2-lgssm-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase3-fixed-sir-subplan-2026-07-07.md`

Local checks:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase2_lgssm_forward_scalar_artifact.py -q
```

Result:

```text
2 passed, 2 warnings in 2.55s
```

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py \
  tests/highdim/test_ledh_phase2_lgssm_forward_scalar_artifact.py -q
```

Result:

```text
26 passed, 2 warnings in 2.77s
```

Gate status:

- `IN_PROGRESS_PENDING_PHASE2_PHASE3_REVIEW`

Next action:

- Run bounded read-only review of Phase 2 result and Phase 3 fixed SIR
  subplan.

### 2026-07-07 - Phase 2 - REVIEW_REPAIR_ACCEPTED

Evidence contract:

- Question: Did the Phase 2/3 handoff repair make fixed SIR replay mandatory?
- Primary criterion: read-only review agrees the Phase 3 fixed SIR subplan
  requires a replay test that reads the actual Phase 3 canonical JSON artifact
  and validates it with `require_admitted=True`.
- Nonclaims: no Phase 3 execution yet, no new model row beyond LGSSM
  reconfirmation, no score admission, no score correctness, no leaderboard
  rebuild, no new GPU model evidence, and no scientific conclusion.

Actions:

- Ran bounded Claude read-only review of Phase 2 result and Phase 3 subplan.
- Review returned `VERDICT=REVISE` because fixed SIR artifact replay was
  optional.
- Patched Phase 3 subplan so
  `tests/highdim/test_ledh_phase3_fixed_sir_forward_scalar_artifact.py` is
  mandatory and appears in required checks and handoff conditions.
- Patched Phase 2 result to record the repair.
- Ran bounded Claude read-only repair review.

Artifacts:

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase2-lgssm-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase3-fixed-sir-subplan-2026-07-07.md`
- `docs/reviews/bayesfilter-ledh-forward-scalar-per-model-phase2-review-bundle-2026-07-07.md`
- `docs/reviews/bayesfilter-ledh-forward-scalar-per-model-phase2-repair1-review-bundle-2026-07-07.md`

Review:

- Initial review run dir:
  `/home/chakwong/BayesFilter/.claude_reviews/20260707-040054-ledh-forward-scalar-per-model-phase2-phase3-handoff`
- Initial status: `REVIEW_STATUS=revise`, `VERDICT=REVISE`.
- Repair review run dir:
  `/home/chakwong/BayesFilter/.claude_reviews/20260707-040534-ledh-forward-scalar-per-model-phase2-repair1`
- Repair status: `REVIEW_STATUS=agreed`, `VERDICT=AGREE`.

Gate status:

- `PASSED_PHASE2_PHASE3_HANDOFF_PHASE3_MAY_START`

Next action:

- Execute Phase 3 fixed SIR forward scalar reconfirmation.

### 2026-07-07 - Phase 3 - FIXED_SIR_FORWARD_SCALAR_LOCAL_PASS

Evidence contract:

- Question: Can the fixed SIR row produce or preserve an executable same-target
  observed-data log likelihood artifact under the shared schema and amended
  free-parameter target?
- Target scalar: `observed_data_log_likelihood_estimator`, reported as
  `log_likelihood`.
- Primary criterion: canonical fixed SIR artifact validates with
  `require_admitted=True`, finite `log_likelihood_by_seed`, full-row scale,
  `sir_log_scale_theta`, theta `[0,0,0]`, and target-density correction.
- Veto diagnostics: old `no_free_theta` admission, missing likelihood vector,
  theta mismatch, missing target-density correction, score evidence used for
  value admission, or runtime-only admission.
- Nonclaims: not old `no_free_theta` admission, not predator-prey/SV evidence,
  no score admission, no score correctness, no leaderboard rebuild, no new GPU
  model evidence, no exact nonlinear likelihood correctness, no Zhao-Cui
  TT/SIRT source-faithfulness, no HMC readiness, no posterior correctness, no
  scientific superiority, and no runtime ranking.

Actions:

- Normalized the existing fixed SIR N=10000 value artifact into the Phase 1
  canonical executable artifact schema.
- Validated the canonical artifact with
  `validate_ledh_forward_scalar_artifact(..., require_admitted=True)`.
- Added mandatory fixed SIR artifact replay tests.
- Ran focused and combined local checks.
- Wrote Phase 3 result.
- Drafted Phase 4 predator-prey subplan.

Artifacts:

- `docs/plans/ledh-phase3-fixed-sir-forward-scalar-artifact-2026-07-07.json`
- `docs/plans/ledh-phase3-fixed-sir-forward-scalar-artifact-2026-07-07.md`
- `tests/highdim/test_ledh_phase3_fixed_sir_forward_scalar_artifact.py`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase3-fixed-sir-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase4-predator-prey-subplan-2026-07-07.md`

Local checks:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_fixed_sir_forward_scalar_artifact.py -q
```

Result:

```text
2 passed, 2 warnings in 2.50s
```

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py \
  tests/highdim/test_ledh_phase2_lgssm_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase3_fixed_sir_forward_scalar_artifact.py -q
```

Result:

```text
28 passed, 2 warnings in 2.57s
```

Gate status:

- `IN_PROGRESS_PENDING_PHASE3_PHASE4_REVIEW`

Next action:

- Run bounded read-only review of Phase 3 result and Phase 4 predator-prey
  subplan.

### 2026-07-07 - Phase 3 - REVIEW_ACCEPTED

Evidence contract:

- Question: Did Phase 3 correctly close fixed SIR scalar reconfirmation and
  safely hand off to predator-prey as the first previously blocked model?
- Primary criterion: read-only review agrees Phase 3 stays within fixed SIR
  scalar scope and Phase 4 has safe predator-prey stop/handoff conditions.
- Nonclaims: no predator-prey execution yet, no score admission, no score
  correctness, no leaderboard rebuild, no new GPU model evidence, and no
  scientific conclusion.

Actions:

- Ran bounded Claude read-only review of Phase 3 result and Phase 4 subplan.

Artifacts:

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase3-fixed-sir-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase4-predator-prey-subplan-2026-07-07.md`
- `docs/reviews/bayesfilter-ledh-forward-scalar-per-model-phase3-review-bundle-2026-07-07.md`

Review:

- Run dir:
  `/home/chakwong/BayesFilter/.claude_reviews/20260707-041754-ledh-forward-scalar-per-model-phase3-phase4-handoff`
- `REVIEW_STATUS=agreed`, `VERDICT=AGREE`.

Gate status:

- `PASSED_PHASE3_PHASE4_HANDOFF_PHASE4_MAY_START`

Next action:

- Execute Phase 4 predator-prey inventory and forward scalar build/blocker
  path.

### 2026-07-07 - Phase 4 - PREDATOR_PREY_FORWARD_SCALAR_LOCAL_PASS

Evidence contract:

- Question: Can the predator-prey row produce an executable same-target
  observed-data log likelihood artifact under the shared schema?
- Target scalar: `observed_data_log_likelihood_estimator`, reported as
  `log_likelihood`.
- Primary criterion: canonical predator-prey artifact validates with
  `require_admitted=True`, finite `log_likelihood_by_seed`, full-row scale,
  physical theta `(0.6,114,25,0.3,0.5,0.5)`, and target-density correction.
- Veto diagnostics: LGSSM/SIR evidence borrowing, metadata-only evidence,
  callback-only evidence, missing likelihood vector, wrong theta, missing
  target correction, score evidence used for value admission, or runtime-only
  admission.
- Nonclaims: no score admission, no score correctness, no exact nonlinear
  likelihood correctness, no Zhao-Cui TT/SIRT source-faithfulness, no HMC
  readiness, no posterior correctness, no scientific superiority, and no
  runtime ranking.

Actions:

- Inventoried predator-prey row callbacks and prior blocker records.
- Added a current-route streaming LEDH-PFPF-OT predator-prey forward scalar
  runner.
- Ran a tiny CPU-hidden smoke artifact.
- Ran the trusted GPU/XLA full-row N=10000 artifact.
- Added mandatory predator-prey artifact replay tests.
- Ran the required local check set.
- Wrote Phase 4 result.
- Drafted Phase 5 actual-SV subplan.

Artifacts:

- `docs/benchmarks/benchmark_ledh_same_target_predator_prey_value.py`
- `docs/plans/ledh-phase4-predator-prey-forward-scalar-artifact-2026-07-07.json`
- `docs/plans/ledh-phase4-predator-prey-forward-scalar-artifact-2026-07-07.md`
- `tests/highdim/test_ledh_phase4_predator_prey_forward_scalar_artifact.py`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase4-predator-prey-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-subplan-2026-07-07.md`

Full-row trusted GPU command:

```text
MPLCONFIGDIR=/tmp python \
  docs/benchmarks/benchmark_ledh_same_target_predator_prey_value.py \
  --device-scope visible --device /GPU:0 --expect-device-kind gpu \
  --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 \
  --num-particles 10000 --transport-policy active-all \
  --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 \
  --history-mode value-only --warmups 0 --repeats 1 \
  --output docs/plans/ledh-phase4-predator-prey-forward-scalar-artifact-2026-07-07.json \
  --markdown-output docs/plans/ledh-phase4-predator-prey-forward-scalar-artifact-2026-07-07.md
```

Full-row result:

- `admission_status = n10000_same_target_value_admitted`;
- `log_likelihood_by_seed =
  [-169.6912841796875, -169.636962890625, -169.46498107910156,
  -171.49961853027344, -169.044677734375]`;
- output tensor device `/job:localhost/replica:0/task:0/device:GPU:0`;
- compile plus first call `34.134711731923744` seconds;
- warm call `19.095908388961107` seconds;
- finite output and schema validation passed.

Local checks:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py \
  tests/highdim/test_ledh_phase2_lgssm_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase3_fixed_sir_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase4_predator_prey_forward_scalar_artifact.py -q
```

Result:

```text
30 passed, 2 warnings in 2.79s
```

Gate status:

- `IN_PROGRESS_PENDING_PHASE4_PHASE5_REVIEW`

Next action:

- Run bounded read-only review of Phase 4 result and Phase 5 actual-SV
  subplan.
