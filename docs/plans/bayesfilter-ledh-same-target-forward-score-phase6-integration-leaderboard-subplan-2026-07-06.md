# Phase 6 Subplan: Integration And Leaderboard Rebuild

metadata_date: 2026-07-06
status: DRAFT_AFTER_PHASE5_PASS
master_program: docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md
phase: 6

## Phase Objective

Add all-model LEDH integration tests and rebuild the LEDH-inclusive leaderboard
only with rows that passed same-target value, no-tape score, and `N=10000`
gates.

## Entry Conditions Inherited From Previous Phase

- Phase 5 lists rows with passing per-model score/memory tests.
- Blocked rows remain explicitly blocked.
- Phase 5 passing full-row score/memory rows:
  - `benchmark_lgssm_exact_oracle_m3_T50`
  - `zhao_cui_spatial_sir_austria_j9_T20`
- Rows that remain blocked:
  - `zhao_cui_sv_actual_nongaussian_T1000`
  - `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`
  - `zhao_cui_predator_prey_T20`
  - `zhao_cui_generalized_sv_synthetic_from_estimated_values`
- The scoped `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`
  diagnostic remains non-full-row evidence.

## Required Artifacts

- Phase 6 result:
  `docs/plans/bayesfilter-ledh-same-target-forward-score-phase6-integration-leaderboard-result-2026-07-06.md`
- All-model integration test.
- Updated leaderboard JSON/Markdown artifacts if and only if row gates pass.
- Final review bundle.

## Required Checks/Tests/Reviews

- Integration test that value and score use the same LEDH algorithm id for
  LGSSM and fixed SIR.
- Check that no row is silently skipped.
- Leaderboard JSON content checks.
- `git diff --check` on updated artifacts.
- Claude read-only final review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the LEDH-inclusive leaderboard truthfully report all admitted LEDH values and scores? |
| Baseline/comparator | Phase 5 per-model tests and existing July 3/July 5 leaderboard artifacts. |
| Primary criterion | The leaderboard includes only rows whose row gates passed and preserves blocked statuses for all others. |
| Veto diagnostics | Value/score algorithm mismatch; blocked row promoted; scoped row promoted; runtime ranking against frozen rows; unsupported scientific claim. |
| Explanatory diagnostics | Runtime, memory, compile status, and non-LEDH frozen comparator context. |
| Not concluded | HMC readiness, posterior correctness, and scientific superiority unless separately gated. |

## Forbidden Claims/Actions

- Do not rebuild the leaderboard with rows that lack Phase 5 pass artifacts.
- Do not runtime-rank fresh LEDH against frozen non-LEDH rows.
- Do not claim full all-model score readiness unless every model row passes or
  has an explicit blocked status. Fixed SIR no longer has a no-free-theta
  exemption under the 2026-07-06 amendment.
- Do not promote scoped parameterized SIR as a full observed-data row.

## Allowed Operations

- Edit tests and leaderboard artifacts.
- Run trusted GPU/XLA integration tests.
- Use Claude read-only final review.

## Exact Next-Phase Handoff Conditions

There is no next phase. Final closeout must state:

- admitted rows;
- blocked rows;
- artifact support for each admitted row;
- remaining blockers and nonclaims.

## Stop Conditions

Stop if the leaderboard cannot truthfully represent the admitted/blocked split
or if any row lacks required evidence.
