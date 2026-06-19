# P69 Phase 2 Subplan: Holdout/Replay Implementation And Focused Tests

metadata_date: 2026-06-15
status: READY_FOR_PHASE2_TASK0_FEASIBILITY_CHECKPOINT
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p69-remaining-gaps-master-program-2026-06-15.md
phase: 2
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Implement the Phase 1 holdout/replay diagnostic design in the smallest
BayesFilter code surface needed.  The implementation must expose post-fit
diagnostic residuals and branch-identity invariants for the P59/P67/P68
Zhao--Cui SIR fixed-HMC adaptation path, without changing adjacent-ladder
thresholds or rerunning the ladder.

## Entry Conditions Inherited From Phase 1

- Phase 1 design result exists:
  `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase1-holdout-replay-design-result-2026-06-15.md`.
- Claude read-only review of the Phase 1 result and this subplan returns
  `VERDICT: AGREE`.
- The active lane remains `fixed_hmc_adaptation`, not adaptive Zhao--Cui parity.
- P68 remains the immediate predecessor: fit residual and condition diagnostics
  are exposed, but holdout/replay diagnostics are unavailable and the degree
  ladder exceeds thresholds.

## Required Artifacts

- Phase 2 result/close record:
  `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase2-holdout-replay-implementation-result-2026-06-15.md`.
- Code changes limited to:
  - `bayesfilter/highdim/source_route.py`;
  - `scripts/p67_author_sir_adjacent_ladder_diagnostics.py`;
  - focused tests under `tests/highdim/`.
- Refreshed Phase 3 adjacent-ladder rerun subplan.
- Updated P69 execution and Claude review ledgers.

## Implementation Tasks

0. Run the diagnostic-cloud feasibility checkpoint before broader edits.
   - Identify the concrete pre-fit source-route cloud available in code for
     each step: pushed augmented samples, local coordinates, target values,
     weights, coordinate frame, previous retained object, and deterministic
     seeds or index rules.
   - State the deterministic split/replay rule to be implemented.
   - Confirm whether the rule creates a diagnostic set disjoint from the fitted
     ALS rows without changing the current fitted branch route.
   - If this cannot be shown from current code, stop before implementation with
     `BLOCK_HOLDOUT_REPLAY_DESIGN_NEEDS_ROUTE_CHANGE`.

1. Add post-fit residual helpers.
   - Evaluate a fitted `FunctionalTT` on diagnostic local points after fitting.
   - Compute weighted RMS residuals against shifted square-root target values.
   - Do not pass these points into `FixedTTFitter.fit` as holdout points for
     P67/P68 rows.

2. Add deterministic diagnostic point construction for P59/P67 SIR.
   - Use the same local coordinate frame, shifted target convention,
     previous-retained object, and source target order as the fitted branch.
   - Record whether diagnostic points are disjoint from fit points.
   - If a disjoint diagnostic set cannot be made without changing the route,
     stop with `BLOCK_HOLDOUT_REPLAY_DESIGN_NEEDS_ROUTE_CHANGE`.

3. Add diagnostic hashes and branch invariants.
   - Record fit point/target/weight hashes.
   - Record holdout and replay point/target/weight hashes.
   - Record coordinate-frame, fit-branch, and density-branch hashes.
   - Verify `branch_identity_unchanged_by_diagnostics`.

4. Expose step-level manifest fields.
   - Add `holdout_replay_diagnostics_by_step`, or an equivalent sibling record
     with the exact Phase 1 fields.
   - Preserve existing `fit_quality_diagnostics_by_step` fields for backward
     compatibility unless a focused test proves the replacement is equivalent.

5. Update P67 budget diagnostics.
   - Missing post-fit holdout diagnostics keeps `holdout_unavailable_steps`.
   - Missing replay diagnostics keeps `replay_unavailable_steps`.
   - Finite post-fit holdout diagnostics can remove only the
     holdout-unavailable blocker.
   - Finite replay diagnostics can remove only the replay-unavailable blocker.
   - Nonfinite holdout diagnostics, nonfinite replay diagnostics, route mismatch,
     or branch identity drift blocks the row.
   - Do not change P67 threshold values.

6. Add focused tests.
   - P59 assembly exposes post-fit holdout/replay diagnostics for two steps.
   - Branch hashes are unchanged by diagnostics.
   - P67 budget logic treats finite holdout and replay diagnostics as separately
     available.
   - P67 budget logic treats missing holdout, missing replay, nonfinite holdout,
     nonfinite replay, and branch drift as distinct blockers or unresolved
     states.
   - Existing P66 validation-ladder schema tests still pass.

## Required Checks, Tests, And Reviews

Run before Phase 2 Claude review:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py scripts/p67_author_sir_adjacent_ladder_diagnostics.py tests/highdim/test_p59_author_sir_step_spec_assembly.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_step_spec_assembly.py tests/highdim/test_p66_author_sir_fixed_branch_validation_ladder.py
```

The pytest command must include every touched holdout/replay/P67-focused test
file, even if the tests are added to an existing file.  At minimum, if
`scripts/p67_author_sir_adjacent_ladder_diagnostics.py` changes, run the test
file containing the new P67 budget-diagnostic assertions.  A valid Phase 2
result must name the exact test functions or files that exercise:

- finite holdout diagnostics;
- finite replay diagnostics;
- missing holdout diagnostics;
- missing replay diagnostics;
- nonfinite holdout diagnostics;
- nonfinite replay diagnostics;
- branch identity drift.

Run local text checks:

```bash
rg -n "post_fit_diagnostic_only|BLOCK_BRANCH_IDENTITY_DRIFT|diagnostic_only_unless_predeclared|fixed_hmc_adaptation" bayesfilter/highdim/source_route.py scripts/p67_author_sir_adjacent_ladder_diagnostics.py tests/highdim docs/plans/bayesfilter-highdim-zhao-cui-p69-phase2-holdout-replay-implementation-result-2026-06-15.md
rg -n "log_marginal_abs_delta|normalizer_increment_abs_delta|probe_log_density_median_abs_delta|retained_log_density_median_abs_delta" scripts/p67_author_sir_adjacent_ladder_diagnostics.py
```

Claude read-only review must inspect:

- implementation diff summary;
- Phase 2 result;
- focused test output;
- preservation of Phase 1 forbidden claims/actions.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the code expose reviewed post-fit holdout/replay diagnostics without changing fixed-branch fitting, row thresholds, or ladder execution? |
| Baseline/comparator | P68 manifest behavior and Phase 1 design contract. |
| Primary pass criterion | The Task 0 feasibility checkpoint passes; focused tests pass; P59/P67 manifests expose the reviewed holdout and replay fields; P67 budget logic distinguishes missing, finite, nonfinite, and branch-drift diagnostics separately for holdout and replay. |
| Veto diagnostics | Changed P67 thresholds; passed diagnostic points into `FixedTTFitter.fit` for ladder rows; branch hash drift; adaptive source-faithful claim; ladder rerun; long experiment; GPU/HMC command. |
| Explanatory diagnostics | Holdout/replay residuals, point hashes, target hashes, weight hashes, frame hash, branch hashes, condition numbers, fit residuals. |
| Not concluded | No adjacent-ladder stability, no rank-channel activity conclusion, no degree-instability diagnosis, no d18 correctness, no d50/d100 scaling, no HMC readiness. |
| Artifact preserving result | Phase 2 result/close record. |

## Forbidden Claims And Actions

- Do not rerun P67/P68 adjacent ladders in Phase 2.
- Do not change P67 thresholds.
- Do not use `FixedTTFitSampleBatch.holdout_points` for the ladder-row
  diagnostic unless a reviewed amendment explains the changed status semantics.
- Do not call finite holdout/replay residuals filtering correctness.
- Do not call this adaptive source-faithful Zhao--Cui.
- Do not run GPU/CUDA/HMC commands.
- Do not change default backend policy.

## Exact Next-Phase Handoff Conditions

Phase 2 may hand off to Phase 3 only if:

- the diagnostic-cloud feasibility checkpoint identifies the exact source-route
  cloud and deterministic split/replay rule used in implementation;
- focused compile and pytest checks pass;
- post-fit holdout diagnostics and replay diagnostics are both present in
  P59/P67 manifests;
- branch-identity invariants pass in tests;
- P67 budget diagnostics remove the holdout-unavailable marker only when finite
  post-fit holdout diagnostics are present;
- P67 budget diagnostics remove the replay-unavailable marker only when finite
  replay diagnostics are present;
- P67 budget diagnostics preserve distinct blockers for missing holdout, missing
  replay, nonfinite holdout, nonfinite replay, route mismatch, and branch drift;
- Phase 2 result is written;
- Claude returns `VERDICT: AGREE`;
- Phase 3 rerun subplan is refreshed with exact commands, thresholds, evidence
  contract, and stop conditions.

## Stop Conditions

Stop and write a blocker result if:

- diagnostic point construction requires changing the fitted branch route;
- diagnostic points cannot be separated from fitting points or clearly labeled
  as replay-only;
- branch hashes change after diagnostics;
- nonfinite diagnostic values appear in focused tests;
- implementation requires threshold changes;
- implementation requires long ladder reruns;
- Claude and Codex do not converge after five review rounds.
