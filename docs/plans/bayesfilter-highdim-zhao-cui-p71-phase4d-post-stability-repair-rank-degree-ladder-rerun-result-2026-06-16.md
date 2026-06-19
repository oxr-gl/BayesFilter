# P71 Phase 4d Result: Post-Stability-Repair Rank/Degree Ladder Rerun

metadata_date: 2026-06-16
status: BLOCKED_MULTIPLE_ROW_ADMISSIONS_PHASE5_NOT_AUTHORIZED
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-subplan-2026-06-16.md
artifact: docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-2026-06-16.json

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | After the Phase 4c objective-preserving scaled ALS repair, does the same source-route d18 branch pass the frozen Phase 4d structural row and ladder gate with exactly one admitted d18 configuration? |
| Baseline/comparator | Original blocked Phase 4 artifact, Phase 4c implementation result, and the same five P67 row specs and thresholds. |
| Primary criterion | Valid JSON plus frozen-contract validation with exactly one admitted d18 configuration. |
| Veto diagnostics | Failed fit, budget-limited row, source-route invariant drift, changed row specs, changed thresholds, zero admitted rows, multiple admitted rows, incomplete ladder comparison, or scientific-claim leakage. |
| Explanatory diagnostics | Sentinel status, row statuses, condition warnings/vetoes, source-invariant payloads, holdout/replay diagnostic availability, and validator blocker details. |
| Not concluded | No d18 filtering accuracy, no rank/degree convergence proof, no d50/d100 scaling, no HMC readiness, and no adaptive Zhao-Cui parity claim. |
| Artifact | Phase 4d JSON artifact and this result note. |

## Commands Run

Initial stale-invariant run:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p67_author_sir_adjacent_ladder_diagnostics.py --output docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-2026-06-16.json
```

Focused stale-invariant repair checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p67_author_sir_adjacent_ladder_diagnostics.py scripts/p71_phase4d_validate_ladder_artifact.py tests/highdim/test_p59_author_sir_step_spec_assembly.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_step_spec_assembly.py::test_p67_source_invariant_accepts_p70_seeded_channel_initializer tests/highdim/test_p59_author_sir_step_spec_assembly.py::test_phase4d_validator_enforces_frozen_rows_thresholds_and_single_admission tests/highdim/test_p59_author_sir_step_spec_assembly.py::test_p67_failed_fit_row_payload_preserves_p70_diagnostics
git diff --check -- scripts/p67_author_sir_adjacent_ladder_diagnostics.py tests/highdim/test_p59_author_sir_step_spec_assembly.py
```

Repaired rerun:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p67_author_sir_adjacent_ladder_diagnostics.py --output docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-2026-06-16.json
```

Post-rerun checks:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-2026-06-16.json /tmp/p71_phase4d_post_stability_rerun_pretty.json
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p71_phase4d_validate_ladder_artifact.py --artifact docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-2026-06-16.json
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p67_author_sir_adjacent_ladder_diagnostics.py scripts/p71_phase4d_validate_ladder_artifact.py bayesfilter/highdim/fitting.py bayesfilter/highdim/source_route.py tests/highdim/test_fixed_branch_fit.py tests/highdim/test_p59_author_sir_step_spec_assembly.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_fixed_branch_fit.py tests/highdim/test_p59_author_sir_step_spec_assembly.py::test_p67_failed_fit_row_payload_preserves_p70_diagnostics tests/highdim/test_p59_author_sir_step_spec_assembly.py::test_p67_source_invariant_accepts_p70_seeded_channel_initializer tests/highdim/test_p59_author_sir_step_spec_assembly.py::test_phase4d_validator_enforces_frozen_rows_thresholds_and_single_admission
git diff --check -- scripts/p67_author_sir_adjacent_ladder_diagnostics.py scripts/p71_phase4d_validate_ladder_artifact.py bayesfilter/highdim/fitting.py bayesfilter/highdim/source_route.py tests/highdim/test_fixed_branch_fit.py tests/highdim/test_p59_author_sir_step_spec_assembly.py docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-subplan-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-result-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-2026-06-16.json docs/plans/bayesfilter-highdim-zhao-cui-p71-visible-execution-ledger-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-runbook-claude-review-ledger-2026-06-16.md
```

## Run Manifest

| Field | Value |
| --- | --- |
| git commit | `9406906` |
| environment | conda `tf-gpu` as invoked by current shell |
| CPU/GPU status | CPU-only intent: `CUDA_VISIBLE_DEVICES=-1`; TensorFlow emitted CUDA/cuInit import warnings, treated as CPU-only import noise. |
| random seeds | Project/script defaults; no new seed sweep in Phase 4d. |
| wall time | Final repaired ladder artifact records about `1004.724` seconds. |
| output artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-2026-06-16.json` |
| plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-subplan-2026-06-16.md` |
| result file | this file |

## Repairs During Phase 4d

Two fixable gate defects were found during closeout and patched visibly before
the final result decision:

- `scripts/p67_author_sir_adjacent_ladder_diagnostics.py` expected the old
  P65 initializer `fixed_hmc_constant_path_weighted_mean` even though the P70
  source route now manifests `fixed_hmc_seeded_channel_paths_v1`.  The P67
  source-invariant expectation was updated to `P70_FIXED_BRANCH_INITIALIZATION_RULE`.
- `scripts/p71_phase4d_validate_ladder_artifact.py` counted admissions using
  the top-level P67 pass status instead of the row execution pass status
  `PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY`.  The validator now counts
  executed non-budget-limited rows with passing source invariants.

Focused tests were added/updated so the seeded-channel initializer is accepted
and multiple row admissions remain a validator failure.

## Result Summary

Final repaired artifact top-level status:

`P67_ADJACENT_FIXED_BUDGET_SCREEN_BLOCKED`

Validator output after the repaired rerun:

```json
{
  "blockers": [
    "admitted_configuration_count_mismatch:4"
  ],
  "phase4d_artifact_contract": "FAIL"
}
```

Row-level summary from the repaired artifact:

| Row | Degree | Rank | Fit count | Status | Budget limited | Source invariants | Phase 4d admission role |
| --- | ---: | ---: | ---: | --- | --- | --- | --- |
| `base_candidate_1_2_fit16` | 1 | 2 | 16 | `PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY` | false | pass | admitted by row-level contract |
| `rank_candidate_1_2_fit36` | 1 | 2 | 36 | `PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY` | false | pass | admitted by row-level contract |
| `rank_stronger_1_3_fit36` | 1 | 3 | 36 | `P67_ROW_BLOCKED_ON_FAILED_FIT` | true | fail before capture | inadmissible |
| `degree_candidate_1_2_fit24` | 1 | 2 | 24 | `PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY` | false | pass | admitted by row-level contract |
| `degree_stronger_2_2_fit24` | 2 | 2 | 24 | `PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY` | false | pass | admitted by row-level contract |

The rank-3 stronger row still failed with:

`fixed_ttsirt_fit_status_CONDITION_NUMBER_VETO`

Because the runner records any row exception as a top-level blocker, it returns
before computing the rank and degree ladder comparison payloads.  The final
artifact therefore preserves `rank_ladder` and `degree_ladder` as
`P67_ROW_NOT_EXECUTED` with `ladder_not_executed_yet`.

## Local Check Status

| Check | Status |
| --- | --- |
| JSON parse via `python -m json.tool` | PASS |
| Phase 4d validator | FAIL by intended gate: `admitted_configuration_count_mismatch:4` |
| compileall focused files | PASS |
| focused pytest bundle | PASS, `37 passed, 2 warnings` |
| focused invariant/validator pytest | PASS, `3 passed, 2 warnings` |
| `git diff --check` focused files | PASS |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Block Phase 5 | FAIL: exactly-one admitted d18 configuration was not met | VETO: four row-level admissions; rank-3 row condition-vetoed; ladder comparisons not executed | Whether Phase 4d should choose a canonical row by predeclared rule, expand comparison logic after a failed stronger-rank row, or revise the structural gate | Stop for human/plan direction after Claude review; do not launch Phase 5 from this result | No d18 filtering accuracy, no structural convergence proof, no HMC readiness |

## Interpretation

Phase 4c did repair the original all-row condition-veto failure for the rank-2
and degree-2 bounded rows: four rows now execute through step-spec assembly with
non-budget-limited payloads and passing source invariants.  That is real
engineering progress.

It does not close Phase 4d.  The Phase 4d subplan required exactly one admitted
d18 configuration and made multiple admissions an unconditional blocker.  The
repaired validator now reports four admitted row-level configurations.  The
rank-3 stronger row still condition-vetoes, and the runner does not compute the
ladder comparison payloads once any row exception is recorded.  Therefore Phase
5 remains blocked.

## Nonclaims

- This is not d18 filtering accuracy evidence.
- This is not a rank/degree convergence proof.
- This is not a d50/d100 scaling result.
- This is not HMC readiness evidence.
- This does not claim adaptive Zhao-Cui source-faithfulness for the fixed-HMC
  seeded-channel stabilization.

## Handoff

Phase 5 is not authorized.  A next subplan, if approved, should decide one of
the following before any accuracy gate:

- predeclare a canonical single admitted row selection rule and rerun the
  validator under that rule;
- revise P67 so ladder comparisons can still be computed when the rank-3
  stronger row condition-vetoes, without hiding that failure;
- design a new structural discrimination gate for the four admitted row-level
  configurations.
