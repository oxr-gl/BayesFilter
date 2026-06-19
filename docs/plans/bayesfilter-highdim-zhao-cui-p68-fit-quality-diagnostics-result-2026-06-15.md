# P68 Result: Fixed-TTSIRT Fit-Quality Diagnostics

metadata_date: 2026-06-15
status: P68_FIT_QUALITY_DIAGNOSTICS_EXPOSED_LADDER_STILL_INCONCLUSIVE
parent_plan: docs/plans/bayesfilter-highdim-zhao-cui-p68-fit-quality-diagnostics-plan-2026-06-15.md
parent_result: docs/plans/bayesfilter-highdim-zhao-cui-p67-adjacent-ladder-execution-result-2026-06-15.md
json_artifact: docs/plans/bayesfilter-highdim-zhao-cui-p68-fit-quality-adjacent-ladder-diagnostics-2026-06-15.json
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

P68 repaired the P67 diagnostic-exposure gap, but the adjacent ladder still did
not pass.

The P59/P67 artifacts now expose step-level fixed-TTSIRT fit-quality
diagnostics: fit status, termination reason, stop condition, fit residual,
holdout availability/status, per-core update records, and condition-number
summaries.  In the P68 rerun, every row had `missing_fit_resolution_fields = []`.

The rerun remains `P67_ADJACENT_FIXED_BUDGET_SCREEN_INCONCLUSIVE` because
holdout diagnostics are explicitly not supplied for every row.  The degree
ladder also still exceeds all declared P67 delta thresholds.  No threshold,
row, fit-sample budget, or fixed-branch algorithm was changed.

## Decision Table

| Field | Result |
| --- | --- |
| Decision | `P68_FIT_QUALITY_DIAGNOSTICS_EXPOSED_LADDER_STILL_INCONCLUSIVE`. |
| Primary criterion status | Partially passed: condition and fit-residual diagnostics are now exposed; not promoted because holdout is unavailable and degree-ladder thresholds fail. |
| Veto diagnostic status | No source-invariant drift, no defensive-only row, no near-zero core collapse, no non-OK fit status, no nonfinite fit residual, no condition warning/veto. Holdout unavailable for both step fits in every row. Degree-ladder threshold blockers remain. |
| Main uncertainty | Whether the observed adjacent-ladder deltas reflect unresolved fit generalization or structural branch instability; the current run has no holdout fit-quality evidence. |
| Next justified action | If holdout validation is required, write a separate plan to construct source-route-consistent holdout/replay diagnostics without changing thresholds after seeing data. |
| Not concluded | No structural rank/degree convergence proof, no d18 correctness, no d50/d100 scaling, no adaptive Zhao--Cui parity, no HMC readiness. |

## Implementation Summary

Changed artifacts:

- `bayesfilter/highdim/source_route.py`
  - Added `_p59_fixed_ttsirt_fit_quality_diagnostics`.
  - Added `fit_quality_diagnostics` to the P59-9a preparation manifest.
  - Added `fit_quality_diagnostics_by_step` to the P59-9b assembly manifest.
- `scripts/p67_author_sir_adjacent_ladder_diagnostics.py`
  - Reads exposed fit-quality diagnostics.
  - No longer reports condition/residual diagnostics as missing when present.
  - Still marks rows unresolved for non-OK fit status, unavailable/nonfinite fit
    residual, unavailable holdout, or condition warning/veto.
- `tests/highdim/test_p59_author_sir_step_spec_assembly.py`
  - Checks that P59-9b exposes fit-quality diagnostics.
  - Checks that P67 budget diagnostics treat exposed condition/residual fields
    as present while preserving holdout-unavailable as unresolved.

## Checks

Compile:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py scripts/p67_author_sir_adjacent_ladder_diagnostics.py tests/highdim/test_p59_author_sir_step_spec_assembly.py
```

Focused tests:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_step_spec_assembly.py tests/highdim/test_p66_author_sir_fixed_branch_validation_ladder.py
```

```text
16 passed, 2 warnings in 331.52s
```

Rerun:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p67_author_sir_adjacent_ladder_diagnostics.py --output docs/plans/bayesfilter-highdim-zhao-cui-p68-fit-quality-adjacent-ladder-diagnostics-2026-06-15.json
```

```text
artifact_check: PASS
status: P67_ADJACENT_FIXED_BUDGET_SCREEN_INCONCLUSIVE
elapsed_seconds: 1442.404
```

Self-check:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p67_author_sir_adjacent_ladder_diagnostics.py --check-only --output docs/plans/bayesfilter-highdim-zhao-cui-p68-fit-quality-adjacent-ladder-diagnostics-2026-06-15.json
```

```text
artifact_check: PASS
status: P67_ADJACENT_FIXED_BUDGET_SCREEN_INCONCLUSIVE
```

TensorFlow emitted CUDA plugin/cuInit chatter despite `CUDA_VISIBLE_DEVICES=-1`.
This is recorded as CPU-only intent and is not GPU evidence.

## Row Fit Diagnostics

Every row has:

- `missing_fit_resolution_fields = []`;
- `non_ok_fit_steps = []`;
- `fit_residual_unavailable_steps = []`;
- `nonfinite_fit_residual_steps = []`;
- `condition_warning_steps = []`;
- `condition_veto_steps = []`;
- `holdout_unavailable_steps = [1, 2]`.

| Row | Step 1 fit residual | Step 2 fit residual | Step 1 max condition | Step 2 max condition | Holdout status |
| --- | ---: | ---: | ---: | ---: | --- |
| `base_candidate_1_2_fit16` | `0.03695360167840636` | `0.10825979689029418` | `1606443606.5391824` | `1605908773.1174378` | not supplied |
| `rank_candidate_1_2_fit36` | `0.09573780350980712` | `0.04261274001476897` | `3604749582.0605702` | `3600070649.2720394` | not supplied |
| `rank_stronger_1_3_fit36` | `0.09573780350980712` | `0.04261274001476897` | `3604749582.0605702` | `3600070649.2720394` | not supplied |
| `degree_candidate_1_2_fit24` | `0.08234689014371575` | `0.10990965252882855` | `2401780042.1106615` | `2400656610.4544387` | not supplied |
| `degree_stronger_2_2_fit24` | `0.040451316910524164` | `0.0024177977036540545` | `4452608164.547448` | `4217720578.7897215` | not supplied |

The condition values are below the configured warning threshold `1e12` and veto
threshold `1e16`.  These facts are diagnostic only; they do not establish
filtering correctness or structural rank/degree convergence.

## Ladder Results

| Ladder | Compared rows | Unauthorized differences | Deltas | Threshold blockers | Status |
| --- | --- | --- | --- | --- | --- |
| rank | `(1,2,36)` vs `(1,3,36)` | none | log marginal `0.0`; normalizer increments `[0.0, 0.0]`; probe median `0.0`; retained median `0.0` | none | `P67_ADJACENT_FIXED_BUDGET_SCREEN_INCONCLUSIVE` because holdout is unavailable for both rows |
| degree | `(1,2,24)` vs `(2,2,24)` | none | log marginal `39.90354896700583`; normalizer increments `[59.54048065746218, 19.636931690456336]`; probe median `21.25481599004719`; retained median `335.22761346150156` | log marginal, normalizer increment, probe density, retained density | `P67_ADJACENT_FIXED_BUDGET_SCREEN_INCONCLUSIVE` with threshold failures |

The old P60 `(degree=0, rank=1)` versus `(degree=1, rank=2)` sentinel remains
explanatory only.

## Review Trail

- P68 plan review R1: `VERDICT: AGREE`.
- P68 implementation review R1: `VERDICT: AGREE`.

## Interpretation

P68 closes the narrow manifest problem found in P67: condition-number and
fit-residual diagnostics are now visible in the row artifacts.  It does not
make the fixed branch ready for promotion.

The rank ladder remains non-promotional because both rows lack holdout
fit-quality evidence.  The degree ladder gives stronger negative evidence:
even after exposing diagnostics, it exceeds all declared delta thresholds under
the same fixed-budget comparison.  The correct next step is not to tune the
thresholds, but to decide whether we need a separate reviewed holdout/replay
diagnostic plan or whether the degree-ladder failure is already sufficient to
redirect the fixed-variant repair.
