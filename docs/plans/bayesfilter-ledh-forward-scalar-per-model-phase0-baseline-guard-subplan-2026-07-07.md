# Phase 0 Subplan: Baseline And Admission Guard

metadata_date: 2026-07-07
status: `DRAFT_LAUNCH_REVIEW_PENDING`
master_program: `docs/plans/bayesfilter-ledh-forward-scalar-per-model-master-program-2026-07-07.md`
phase: 0

## Phase Objective

Freeze the current admitted/blocked baseline and verify that local tests
distinguish metadata-only forward contracts from executable same-target
forward scalar evidence.

The target scalar is `observed_data_log_likelihood_estimator`, reported as
`log_likelihood`.

This phase is forward-scalar-only. It must not implement model-specific
adapters, run long GPU jobs, implement scores, admit scores, or rebuild the
leaderboard.

## Entry Conditions Inherited From Previous Phase

There is no previous phase in this program. The inherited baseline comes from:

- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase3-model-forward-admission-result-2026-07-06.md`;
- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase3-remaining-row-forward-blockers-result-2026-07-06.md`;
- `docs/plans/bayesfilter-ledh-same-target-forward-scalar-per-model-amendment-plan-2026-07-06.md`.

The expected baseline is:

- value-admitted rows:
  - `benchmark_lgssm_exact_oracle_m3_T50`;
  - `zhao_cui_spatial_sir_austria_j9_T20`;
- value-blocked rows:
  - `zhao_cui_predator_prey_T20`;
  - `zhao_cui_sv_actual_nongaussian_T1000`;
  - `zhao_cui_generalized_sv_synthetic_from_estimated_values`;
  - `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`.

## Required Artifacts

- Phase 0 result:
  `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase0-baseline-guard-result-2026-07-07.md`
- Refreshed Phase 1 subplan:
  `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase1-runner-schema-subplan-2026-07-07.md`
- Optional focused guard test if existing tests do not cover the baseline:
  `tests/highdim/test_ledh_forward_scalar_admission_guard.py`
- Phase 0 review bundle if material changes are made:
  `docs/reviews/bayesfilter-ledh-forward-scalar-per-model-phase0-review-bundle-2026-07-07.md`

## Required Checks/Tests/Reviews

Local checks:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py -q
```

If a new guard test is added, include it in the focused test command.

Review:

- Launch package must receive bounded read-only review before Phase 0 starts.
- Phase 0 result and Phase 1 subplan must receive bounded read-only review if
  Phase 0 changes tests, code, or row baseline status.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the current repo state distinguish metadata-only forward contracts from executable same-target scalar admission, and what is the exact admitted/blocked baseline? |
| Target scalar | `observed_data_log_likelihood_estimator`, reported as `log_likelihood`. |
| Baseline/comparator | July 6 Phase 3 admitted/blocked result and remaining-row blocker result. |
| Primary criterion | Phase 0 passes only if local checks enforce metadata-only as non-admission and the result records exactly two admitted rows and four blocked rows. |
| Veto diagnostics | Any metadata-only row treated as admitted; any blocked row silently promoted; any score work; any target redefinition; any proposal/flow objective treated as likelihood. |
| Explanatory diagnostics | Existing tiny artifacts, old N=10000 artifacts, and prior review status. |
| Not concluded | No new value admission, score admission, score correctness, HMC readiness, posterior correctness, scientific superiority, or runtime ranking. |
| Artifact | Phase 0 result and refreshed Phase 1 subplan. |

## Forbidden Claims/Actions

- Do not admit a new row.
- Do not run long GPU/XLA jobs.
- Do not implement model-specific forward adapters.
- Do not implement or admit scores.
- Do not rebuild the leaderboard.
- Do not change row targets or pass/fail criteria.

## Exact Next-Phase Handoff Conditions

Phase 1 may begin only if:

- the Phase 0 result records exactly the two admitted rows and four blocked
  rows listed above;
- local checks pass;
- any added guard test passes;
- the Phase 1 subplan is drafted or refreshed;
- review, if required, returns `VERDICT: AGREE` or a documented fallback Codex
  review accepts the boundary.

## Stop Conditions

Stop and write/update the visible stop handoff if:

- current tests cannot distinguish metadata-only contracts from executable
  scalar evidence;
- current tests cannot distinguish callback-only evidence from executable
  same-target scalar evidence;
- current tests cannot prevent actual-SV and KSC-SV artifacts, callbacks, or
  target densities from being cross-used as admission evidence;
- the admitted/blocked baseline differs from the July 6 result without a
  reviewed explanation;
- Phase 0 would need model-specific adapter implementation;
- any score work becomes necessary;
- a human approval boundary is reached.

## Skeptical Plan Audit

| Risk | Control |
| --- | --- |
| Wrong baseline | Phase 0 reads the July 6 result files and records the exact baseline. |
| Proxy metrics | Runtime, memory, finite output, and review status cannot admit rows. |
| Missing stop conditions | Stop conditions above block target changes, score work, and baseline ambiguity. |
| Hidden assumptions | Phase 0 makes no model-specific implementation changes. |
| Artifact mismatch | The required result must answer baseline and admission-guard status only. |

Audit status: passed for Phase 0 subplan draft.
