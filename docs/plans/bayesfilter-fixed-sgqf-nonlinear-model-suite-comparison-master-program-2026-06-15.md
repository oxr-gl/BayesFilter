# Master Program: Fixed-SGQF Nonlinear Model Suite Comparison

metadata_date: 2026-06-15
program_id: fixed-sgqf-nonlinear-model-suite-comparison
status: EXECUTION_READY

## Date

2026-06-15

## Status

`EXECUTION_READY`

## Purpose

This program integrates the repaired fixed-SGQF lane into the existing
BayesFilter nonlinear model suite and leaderboard-style benchmark
infrastructure.  The goal is to position fixed SGQF against the existing
BayesFilter nonlinear algorithms on the repo's established fixtures and reference
policy.

This is a governed comparison program, not an ad hoc benchmark patch.

## Governing Constraints

1. Reuse the existing model suite and benchmark conventions wherever possible.
2. Do not silently change reference policy between algorithms.
3. Model A uses exact Kalman as the exact reference.
4. Models B/C use dense one-step Gaussian projection references only in the
   existing benchmark stack; that is not a full exact multi-step nonlinear
   oracle.
5. Do not imply universal ranking from selected benchmark models.
6. Start with one declared fixed-SGQF comparison level: `fixed_sgqf_level_2`.
   Higher-level ladders remain separate evidence, not the first leaderboard row.
7. Score comparison must preserve accepted-branch / same-scalar discipline.  If
   that cannot be harmonized cleanly with the existing value harness, keep score
   comparison as a scope-audit or diagnostic-only artifact.

## Existing Infrastructure

### Shared model fixtures
- `bayesfilter/testing/nonlinear_models_tf.py`
  - Model A affine Gaussian oracle
  - Model B nonlinear accumulation
  - Model C univariate nonlinear growth
  - dense one-step projection oracle

### Existing BayesFilter-native nonlinear benchmark harness
- `docs/benchmarks/benchmark_bayesfilter_v1_nonlinear_filters.py`
  - currently compares:
    - `tf_svd_cubature`
    - `tf_svd_ukf`
    - `tf_svd_cut4`
  - reports value rows, branch prechecks, score rows, timing, first-step dense
    projection errors, and exact affine parity where available.

### Existing high-dimensional smoke harness
- `docs/benchmarks/benchmark_highdim_nonlinear_filtering_smoke.py`
  - currently compares cubature / UKF / CUT4
  - records point count, timing, residuals, and skip behavior under a point cap.

### Existing fixed SGQF surfaces
- `bayesfilter/nonlinear/fixed_sgqf_tf.py`
- `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`
- `bayesfilter/testing/fixed_sgqf_diagnostics_tf.py`
- `tests/test_fixed_sgqf_*.py`

## Comparator Eligibility Rules

### Exact-reference rows
Allowed when:
- the model is Model A affine Gaussian,
- the compared scalar is the same full filter value,
- exact Kalman remains authoritative.

### Dense-reference rows
Allowed when:
- the model is Model B or Model C,
- the compared quantity is the same first-step Gaussian projection quantity
  already used by the benchmark harness,
- the row is labeled as dense one-step projection only.

### Baseline-only rows
Allowed when:
- the row compares fixed SGQF level 2 against cubature / UKF / CUT4 under the
  same fixture and same benchmark schema,
- no exact claim is inferred beyond the declared reference policy.

### Score rows
Allowed only if:
- same-scalar / accepted-branch comparability is preserved,
- the benchmark artifact makes score-scope limitations explicit.

## Evidence Contract

Question:

How does the repaired fixed SGQF lane compare against the existing nonlinear
BayesFilter algorithms on the established model suite and benchmark
infrastructure?

Primary pass criterion:
- fixed SGQF is added to the existing nonlinear benchmark rows while preserving
  comparator eligibility and current reference policy;
- benchmark outputs show where fixed SGQF fits relative to cubature, UKF, and
  CUT4 on Models A/B/C and on the high-dimensional smoke ladder;
- unsupported claims remain explicit.

Veto diagnostics:
- reference policies silently change between algorithms;
- higher SGQF levels are introduced without a declared level policy;
- score rows overclaim beyond accepted-branch same-scalar evidence;
- benchmark outputs imply universal superiority or full exact nonlinear
  likelihood certification for Models B/C.

Explanatory-only diagnostics:
- point count,
- timing,
- memory,
- branch diagnostics,
- CUT4 skip behavior,
- fixed SGQF cloud/branch metadata.

## Phase Map

| Phase | Subplan | Purpose | Required outcome token |
| --- | --- | --- | --- |
| P0 | `docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-p0-governance-and-eligibility-subplan-2026-06-15.md` | freeze comparator eligibility, SGQF level policy, and artifact schema | `PASS_P0_FIXED_SGQF_SUITE_COMPARISON_READY_FOR_P1` |
| P1 | `docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-p1-model-a-exact-baseline-subplan-2026-06-15.md` | add fixed SGQF to Model A exact-reference benchmark rows | `PASS_P1_FIXED_SGQF_MODEL_A_INTEGRATED` |
| P2 | `docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-p2-model-bc-value-panel-subplan-2026-06-15.md` | add fixed SGQF to Model B/C value panel under dense one-step reference policy | `PASS_P2_FIXED_SGQF_MODEL_BC_VALUE_PANEL_INTEGRATED` |
| P3 | `docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-p3-highdim-smoke-integration-subplan-2026-06-15.md` | add fixed SGQF to the high-dimensional smoke harness | `PASS_P3_FIXED_SGQF_HIGHDIM_SMOKE_INTEGRATED` |
| P4 | `docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-p4-score-panel-scope-audit-subplan-2026-06-15.md` | decide whether score rows belong in the main leaderboard or a separate diagnostic artifact | `PASS_P4_FIXED_SGQF_SCORE_SCOPE_CLASSIFIED` |
| P5 | `docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-p5-closeout-subplan-2026-06-15.md` | summarize supported comparison claims and remaining scope limits | `PASS_P5_FIXED_SGQF_SUITE_COMPARISON_CLOSEOUT` |

## Artifact Contract

Each phase must write, or explicitly block:
- a phase result note,
- a phase review ledger if needed,
- updated benchmark markdown/json artifacts where benchmark code is exercised.

Expected comparison outputs include refreshed benchmark artifacts under
`docs/benchmarks/` rather than a disconnected ad hoc output format.

## Stop Rules

Stop if:
1. fixed SGQF cannot be placed into the current benchmark schema without
   breaking comparator meaning;
2. Model B/C rows require changing the dense one-step reference policy;
3. score rows cannot be integrated without violating accepted-branch
   same-scalar discipline;
4. benchmark output wording starts to imply more than selected-model evidence.

## Exit Criteria

The program exits successfully only if:
- fixed SGQF appears as a governed comparator in the nonlinear benchmark
  infrastructure where eligible;
- the benchmark outputs clearly distinguish exact, dense, and baseline-only
  rows;
- the closeout states what fixed SGQF adds to the model suite comparison and
  what remains outside scope.
