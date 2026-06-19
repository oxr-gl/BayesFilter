# P70 Phase 6g Result: Gate Schema And Blocker Analysis

metadata_date: 2026-06-17
status: PHASE6G_REPORTING_REPAIR_PASSED_TRUE_BLOCKERS_REMAIN
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6g-gate-schema-blocker-analysis-subplan-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

Phase 6g repaired the P70 diagnostic gate/reporting schema defects identified
in the Phase 6f result audit.  The repaired gate now:

- accepts the source-route normalizer field `sqrt_square_normalizer` as the
  square-root tensor-train normalizer used by the gate;
- accepts finite scalar TensorFlow/NumPy numeric values in `_finite_float`;
- preserves the Phase 6 thresholds and all row/rank/degree/model choices.

The saved Phase 6f artifact was re-gated without rerunning the diagnostic.  The
result still fails, but now for the substantive reasons:

- `rank_candidate_1_2_fit36` fails by holdout/replay normalized residual veto;
- `rank_stronger_1_3_fit36` fails by captured `CONDITION_NUMBER_VETO`.

Phase 7 remains blocked.

## Code And Test Changes

Changed:

- `scripts/p70_phase6_rank_channel_normalizer_diagnostic.py`
- `tests/highdim/test_p70_phase6_diagnostic_script.py`

The code change is limited to gate/reporting logic.  It does not rerun the
diagnostic, loosen thresholds, alter row specifications, or change the fitting
algorithm.

Added regression tests for:

- accepting `sqrt_square_normalizer` from the source-route normalizer payload;
- accepting finite NumPy scalar residuals before JSON serialization.

## Checks Run

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p70_phase6_diagnostic_script.py
```

Result:

```text
10 passed, 2 warnings in 2.91s
```

```bash
git diff --check -- scripts/p70_phase6_rank_channel_normalizer_diagnostic.py tests/highdim/test_p70_phase6_diagnostic_script.py docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6g-gate-schema-blocker-analysis-subplan-2026-06-17.md
```

Result: passed.

## Saved Phase 6f Re-Gate

The saved Phase 6f JSON was re-gated by importing the repaired P70 gate and
applying it to the existing saved rows.  This was a reporting check only, not a
diagnostic rerun.

Output:

`docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6g-saved-phase6f-regate-2026-06-17.json`

Compact re-gate summary:

```json
{
  "failed_row_labels": [
    "rank_candidate_1_2_fit36",
    "rank_stronger_1_3_fit36"
  ],
  "has_missing_sqrt_tt_normalizer": false,
  "has_residual_nonfinite": false,
  "overall_status": "fail",
  "row0_holdout_normalized": [
    63609553179.463104,
    147485186405.4084
  ],
  "row0_replay_normalized": [
    235033845830.0373,
    568980270393.0525
  ],
  "row0_step_reasons": [
    [
      "holdout_normalized_residual_veto",
      "replay_normalized_residual_veto"
    ],
    [
      "holdout_normalized_residual_veto",
      "replay_normalized_residual_veto"
    ]
  ],
  "row1_fit_status": "CONDITION_NUMBER_VETO",
  "row1_reasons": [
    "row_assembly_status_not_pass",
    "captured_failed_fit",
    "CONDITION_NUMBER_VETO"
  ]
}
```

## Interpretation

Phase 6g fixes the gate's description of the failed Phase 6f result.  It does
not fix the fixed-variant algorithm.  The first row remains a serious
generalization failure: the fit residual is small on the fitted cloud, while
holdout and replay residuals are enormous relative to the target scale.  The
rank-3 row remains numerically fragile enough to hit the scaled augmented
condition-number veto.

The remaining blocker is therefore not a reporting bug.  It is a mathematical
or numerical problem in the fixed-branch approximation route: the current
fixed-cloud fit can interpolate the selected fit rows while failing badly on
diagnostic clouds, and the higher-rank row still has unstable local solved
systems.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the P70 gate correctly read the existing row schema and finite scalar residuals, so that the saved Phase 6f artifact fails for the actual lower-gate reasons rather than reporting artifacts? |
| Primary criterion | Passed for reporting repair: focused tests passed; saved re-gate removed `missing_sqrt_tt_normalizer` and false residual-nonfinite labels; saved artifact still fails by true blockers. |
| Veto diagnostics | Passed: no threshold change, no diagnostic rerun, no row/rank/degree/ridge/sweep/initializer/model change, no Phase 7 command, no fixed-variant success claim. |
| Explanatory only | Large residual magnitudes and condition summaries explain the blocker but do not prove a repair route. |
| Not concluded | No d18 correctness, no rank/degree promotion, no scaling claim, no HMC readiness, no adaptive Zhao--Cui parity, no author-code failure claim, no claim that the original bug is fixed. |
| Artifact preserving result | This result note and `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6g-saved-phase6f-regate-2026-06-17.json`. |

## Next Justified Action

Draft a Phase 6h root-cause subplan before any further diagnostic run.  Phase
6h should test the residual explosion and rank-3 conditioning hypotheses with
small, predeclared probes, not by loosening gates or rerunning the full
diagnostic blindly.
