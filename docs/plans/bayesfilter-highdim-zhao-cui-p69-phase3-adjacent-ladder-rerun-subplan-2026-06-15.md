# P69 Phase 3 Subplan: Adjacent Ladder Rerun With Holdout/Replay Evidence

metadata_date: 2026-06-15
status: READY_AFTER_PHASE2_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p69-remaining-gaps-master-program-2026-06-15.md
phase: 3
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Rerun the P67 adjacent rank and degree ladders under the reviewed P69
holdout/replay diagnostic contract, with thresholds frozen and with
holdout/replay diagnostics treated as veto or explanatory evidence rather than
as correctness evidence.

## Entry Conditions Inherited From Phase 2

- Phase 2 result exists:
  `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase2-holdout-replay-implementation-result-2026-06-15.md`.
- Claude read-only review of Phase 2 returns `VERDICT: AGREE`.
- CPU-only focused checks from Phase 2 pass:
  `22 passed, 2 warnings in 333.84s`.
- `holdout_replay_diagnostics_by_step` is exposed by P59/P67 rows.
- P67 budget diagnostics distinguish:
  finite holdout, finite replay, missing holdout, missing replay, nonfinite
  holdout, nonfinite replay, route mismatch, and branch identity drift.
- P67 thresholds remain:
  `log_marginal_abs_delta = 5.0`,
  `normalizer_increment_abs_delta = 5.0`,
  `probe_log_density_median_abs_delta = 10.0`,
  `retained_log_density_median_abs_delta = 10.0`.

## Required Artifacts

- Phase 3 execution result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase3-adjacent-ladder-rerun-result-2026-06-15.md`.
- Adjacent-ladder JSON result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase3-adjacent-ladder-diagnostics-2026-06-15.json`.
- Updated P69 execution ledger and Claude review ledger.
- Refreshed Phase 4 structural-diagnosis subplan.

## Required Commands

Pre-run local checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py scripts/p67_author_sir_adjacent_ladder_diagnostics.py tests/highdim/test_p59_author_sir_step_spec_assembly.py tests/highdim/test_p66_author_sir_fixed_branch_validation_ladder.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_step_spec_assembly.py tests/highdim/test_p66_author_sir_fixed_branch_validation_ladder.py
rg -n "log_marginal_abs_delta|normalizer_increment_abs_delta|probe_log_density_median_abs_delta|retained_log_density_median_abs_delta" scripts/p67_author_sir_adjacent_ladder_diagnostics.py
```

Adjacent-ladder rerun:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p67_author_sir_adjacent_ladder_diagnostics.py --output docs/plans/bayesfilter-highdim-zhao-cui-p69-phase3-adjacent-ladder-diagnostics-2026-06-15.json
```

The rerun is CPU-only unless a later reviewed subplan explicitly authorizes GPU
or HMC work.

## Required Checks/Tests/Reviews

- Confirm every executed row contains `budget_limitation_diagnostics`.
- Confirm every executed row contains
  `holdout_replay_diagnostics_by_step` under
  `budget_limitation_diagnostics`.
- Confirm `holdout_replay_resolution_status` is present for every executed row.
- Confirm `branch_identity_drift_steps` and `route_mismatch_steps` are empty
  before interpreting row metric comparisons.
- Confirm `holdout_unavailable_steps`, `replay_unavailable_steps`,
  `holdout_nonfinite_steps`, and `replay_nonfinite_steps` are empty before
  treating a row as interpretable.
- Confirm old P67 thresholds in the JSON match the source thresholds above.
- Claude read-only review must inspect the Phase 3 result, JSON summary,
  threshold evidence, and stop-condition decisions.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | With post-fit holdout/replay diagnostics available, what does the adjacent rank/degree ladder say about the fixed-HMC adaptation branch? |
| Baseline/comparator | P68 adjacent-ladder result without post-fit holdout/replay diagnostics. |
| Primary pass/fail criterion | Rows are interpretable only if source invariants pass, fit diagnostics pass, post-fit holdout/replay diagnostics are available and finite, branch identity does not drift, and P67 thresholds are unchanged. |
| Veto diagnostics | Source-route invariant drift; branch identity drift; route mismatch; missing/nonfinite holdout or replay diagnostics; missing fit-quality diagnostics; non-OK fit status; nonfinite fit residual; condition-number warning/veto; defensive-only TT branch; threshold changes. |
| Explanatory diagnostics | Log-marginal delta, normalizer increment deltas, probe/retained log-density median deltas, holdout/replay residual values, condition numbers, point/target/weight hashes. |
| Not concluded | No d18 correctness, no d50/d100 scaling, no HMC readiness, no adaptive Zhao--Cui parity, no theorem-level convergence result. |
| Artifact preserving result | Phase 3 result and adjacent-ladder JSON. |

## Forbidden Claims/Actions

- Do not change P67 thresholds.
- Do not tune degree/rank/sample counts after seeing Phase 3 results.
- Do not call finite holdout/replay residuals filtering correctness.
- Do not call an interpretable row a scientific success if any veto diagnostic
  fires.
- Do not run GPU/CUDA/HMC commands.
- Do not claim adaptive Zhao--Cui source-faithful parity.
- Do not edit model, author-source route, or fit semantics in Phase 3.

## Exact Next-Phase Handoff Conditions

Phase 3 may hand off to Phase 4 only if:

- the pre-run compile, pytest, and threshold text checks pass;
- the adjacent ladder command completes or writes a clear blocker artifact;
- the JSON result is preserved at the required path;
- every row is classified as interpretable, blocked, or inconclusive under the
  evidence contract;
- the Phase 3 result records the row table, veto diagnostics, and nonclaims;
- Claude returns `VERDICT: AGREE`;
- Phase 4 structural-diagnosis subplan is refreshed with exact unresolved
  questions from the Phase 3 row table.

## Stop Conditions

Stop and write a blocker result if:

- any threshold changes are required or discovered;
- source-route invariant drift appears;
- branch identity drifts after diagnostics;
- holdout/replay diagnostics are missing or nonfinite for the rows needed to
  interpret the ladder;
- the rerun would require GPU/HMC or a long unreviewed experiment;
- Claude and Codex do not converge after five review rounds.
