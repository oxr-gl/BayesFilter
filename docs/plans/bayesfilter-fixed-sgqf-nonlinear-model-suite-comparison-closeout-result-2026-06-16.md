# Phase Result: Fixed-SGQF Nonlinear Model Suite Comparison Closeout

metadata_date: 2026-06-16
plan_reference: `docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-master-program-2026-06-15.md`
status: EXECUTION_COMPLETE

## Executed phases
| Phase | Result | Notes |
| --- | --- | --- |
| P0 governance and eligibility | passed | fixed SGQF level-2 frozen as the first comparison variant |
| P1 Model A exact baseline integration | passed | fixed SGQF rows emitted in the nonlinear benchmark harness on Model A |
| P2 Model B/C value panel | partial / blocked by eligibility | fixed SGQF rows are now represented explicitly as skipped with same-target scope reasons |
| P3 high-dimensional smoke integration | partial / blocked by eligibility | fixed SGQF rows are now represented explicitly as skipped with same-target scope reasons |
| P4 score panel scope audit | classified | score rows remain outside the main leaderboard for fixed SGQF at this time |
| P5 closeout | passed | current supported comparison claims recorded below |

## What was implemented

### 1. Comparison program docs
Created:
- `docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-master-program-2026-06-15.md`
- `docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-p0-governance-and-eligibility-subplan-2026-06-15.md`
- `docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-p1-model-a-exact-baseline-subplan-2026-06-15.md`
- `docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-p2-model-bc-value-panel-subplan-2026-06-15.md`
- `docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-p3-highdim-smoke-integration-subplan-2026-06-15.md`
- `docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-p4-score-panel-scope-audit-subplan-2026-06-15.md`
- `docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-p5-closeout-subplan-2026-06-15.md`

### 2. Nonlinear benchmark harness integration
Edited:
- `docs/benchmarks/benchmark_bayesfilter_v1_nonlinear_filters.py`

Implemented:
- added `tf_fixed_sgqf_level_2` as a value-backend participant,
- added exact-reference Model A rows for fixed SGQF,
- added explicit branch-precheck / skip semantics for ineligible Model B/C rows,
- preserved current score-row scope by leaving fixed SGQF score out of the main
  leaderboard,
- emitted clear same-target skip reasons for unsupported structural-model rows.

### 3. High-dimensional smoke integration
Edited:
- `docs/benchmarks/benchmark_highdim_nonlinear_filtering_smoke.py`

Implemented:
- added `tf_fixed_sgqf_level_2` rows to the smoke harness,
- represented current structural incompatibility explicitly as skipped diagnostic
  rows rather than silent omission or broken execution.

## Verification run

### Benchmark harness run
```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_bayesfilter_v1_nonlinear_filters.py \
  --requested-device cpu --repeats 1 \
  --output /tmp/fixed_sgqf_nonlinear_benchmark.json \
  --markdown-output /tmp/fixed_sgqf_nonlinear_benchmark.md \
  --plan-path docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-master-program-2026-06-15.md \
  --result-path docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-p5-closeout-subplan-2026-06-15.md
```

Observed fixed SGQF benchmark rows:
- **Model A** fixed SGQF rows execute and match the exact Kalman reference with
  tiny log-likelihood and first-step errors.
- **Model B/C** fixed SGQF rows are now present in the artifact as explicit
  skipped rows with the reason:
  - current fixed SGQF implementation is an additive-state lane and is not yet a
    same-target adapter for the structural Model B/C benchmark fixtures.

### High-dimensional smoke harness run
```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_highdim_nonlinear_filtering_smoke.py \
  --output /tmp/fixed_sgqf_highdim_smoke.json \
  --markdown-output /tmp/fixed_sgqf_highdim_smoke.md
```

Observed fixed SGQF smoke rows:
- fixed SGQF rows are present as explicit skipped rows for `model_b` and
  `block_model_b` cases with the reason:
  - current fixed SGQF implementation is an additive-state lane and is not yet a
    same-target adapter for the structural high-dimensional smoke fixtures.

### Regression check
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/test_fixed_sgqf_tf.py \
  tests/test_fixed_sgqf_values_tf.py \
  tests/test_fixed_sgqf_scores_tf.py \
  tests/test_fixed_sgqf_verification_tf.py
```

Observed:
- `33 passed, 2 warnings`

## Current supported comparison claims

### Supported now
1. Fixed SGQF is integrated into the existing nonlinear comparison program at the
   governance/eligibility level.
2. Fixed SGQF participates as an executed benchmark peer on **Model A** under an
   exact-reference Kalman row.
3. Fixed SGQF is represented explicitly — not silently omitted — on **Model B/C**
   and on high-dimensional smoke rows, with an honest same-target eligibility
   blocker message.
4. The comparison program now makes clear that fixed SGQF level 2 is the first
   declared leaderboard variant.

### Not supported yet
1. No value-leaderboard comparison for fixed SGQF on Models B/C, because the
   current fixed SGQF implementation is not yet a same-target adapter for those
   structural fixtures.
2. No fixed SGQF participation in the high-dimensional smoke rows beyond explicit
   skip diagnostics for the same reason.
3. No fixed SGQF score rows in the main nonlinear leaderboard yet; score remains
   separately supported only by its own accepted-branch tests.
4. No universal ranking claim for fixed SGQF against cubature / UKF / CUT4.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| close this comparison implementation pass as partial-but-correct integration | satisfied for governance and Model A, explicitly blocked for Model B/C and highdim smoke | no silent comparator drift; no hidden omission | same-target structural adapters for Models B/C and smoke rows do not yet exist | build an explicit structural-to-fixed-SGQF adapter if the user wants full leaderboard presence | no claim that fixed SGQF has been fully benchmarked on the whole nonlinear suite |

## Recommended next step
If the goal is full leaderboard presence, the next concrete engineering task is:
- design and implement a **same-target structural adapter** from the existing
  nonlinear structural fixture suite (especially Models B/C) into the current
  fixed SGQF additive-state lane, or explicitly define a fixed-SGQF-specific
  comparison fixture family that is semantically aligned with the current
  benchmark models.

Until that adapter exists, the current state is the correct one:
- Model A: real benchmark participation,
- Models B/C + smoke: explicit scope block rather than misleading comparison.
