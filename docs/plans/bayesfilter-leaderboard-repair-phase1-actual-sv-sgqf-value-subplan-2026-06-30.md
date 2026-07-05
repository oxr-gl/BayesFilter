# Phase 1 subplan: actual-SV SGQF same-target value row

Date: 2026-06-30

Status: `DRAFT_REVIEW_READY`

## Phase Objective

Replace the stale SGQF actual-SV `blocked_not_same_target` leaderboard cell with an executed value-only direct exact-transformed SGQF row, if the existing route produces a finite value under the corrected single-target contract.

## Entry Conditions Inherited From Previous Phase

- Phase 0 passed.
- Fail-closed score contract is active.
- Corrected actual-SV derivation note remains the governing target artifact.
- Direct SGQF actual-SV value route exists in `bayesfilter/highdim/sv_mixture_cut4.py`.

## Required Artifacts

- Updated `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`.
- Regenerated:
  - `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
  - `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`
- Phase result:
  `docs/plans/bayesfilter-leaderboard-repair-phase1-actual-sv-sgqf-value-result-2026-06-30.md`
- Refreshed Phase 2 subplan.

## Required Checks, Tests, Reviews

- `python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
- CPU-only leaderboard regeneration with intentional `CUDA_VISIBLE_DEVICES=-1`.
- JSON check that `zhao_cui_sv_actual_nongaussian_T1000/fixed_sgqf` is same-target value-only, not `blocked_not_same_target`.
- JSON check that SGQF actual-SV score is not emitted unless strict analytical provenance exists.
- `git diff --check`.
- Claude read-only review of the Phase 1 result or focused diff.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the corrected direct actual-SV SGQF value route be represented honestly in the highdim leaderboard? |
| Baseline/comparator | Corrected actual-SV derivation note and existing direct SGQF filter function. |
| Primary criterion | The fixed SGQF actual-SV cell is finite `executed_value_only` with same-target direct transformed-SV target status. |
| Veto diagnostics | Any `blocked_not_same_target` reason for this direct route; any score emitted from `GradientTape`; any merged actual-SV and KSC-surrogate target. |
| Explanatory diagnostics | Value magnitude, average loglik, runtime if available. |
| Not concluded | No analytical SGQF score, no exact nonlinear likelihood, no GPU performance, no production readiness. |
| Artifact | Regenerated highdim leaderboard and Phase 1 result. |

## Forbidden Claims And Actions

- Do not claim SGQF actual-SV analytical score readiness.
- Do not use the augmented-noise Gaussian-closure route as same-target actual-SV evidence.
- Do not change the corrected actual-SV target contract after seeing values.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if:

- Actual-SV fixed SGQF value row is finite and same-target value-only, or a precise implementation blocker is recorded.
- The regenerated artifact preserves separate actual-SV and KSC-surrogate rows.
- Claude review agrees or all material review issues are repaired.

## Stop Conditions

Stop if:

- The direct value route fails numerically and the failure is not a small wiring issue.
- The only available value path is the rejected augmented-noise Gaussian-closure route.
- Implementing the value route would require changing target definitions.

## End-of-Subplan Protocol

1. Run required local checks.
2. Write Phase 1 result/close record.
3. Draft or refresh Phase 2 subplan.
4. Review Phase 2 subplan for analytical-score boundary safety.
