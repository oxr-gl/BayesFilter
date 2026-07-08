# Phase 5 Subplan: Per-Model Score And Memory Tests

metadata_date: 2026-07-06
status: DRAFT_AFTER_PHASE4_LOCAL_PASS
master_program: docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md
phase: 5

## Phase Objective

Write and run one score correctness/memory test per admitted model, including
tiny correctness and trusted GPU `N=10000` checks.

## Entry Conditions Inherited From Previous Phase

- Phase 4 lists rows with passing tiny no-tape score checks.
- Rows without Phase 4 score implementation remain blocked.
- Phase 4 admitted tiny no-tape score rows:
  - `benchmark_lgssm_exact_oracle_m3_T50`
  - `zhao_cui_spatial_sir_austria_j9_T20`
- The scoped `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`
  diagnostic is not an admitted full-row score target.

## Required Artifacts

- Phase 5 result:
  `docs/plans/bayesfilter-ledh-same-target-forward-score-phase5-per-model-score-tests-result-2026-07-06.md`
- Test files under `tests/`.
- Per-row JSON/Markdown output artifacts for `N=10000` checks.
- Refreshed Phase 6 integration/leaderboard subplan.

## Required Checks/Tests/Reviews

- One per-model score test for each admitted row:
  - LGSSM compact no-tape score;
  - fixed SIR full-row `sir_log_scale_theta` no-tape score.
- `N=10000` trusted GPU memory check for each admitted row.
- No-autodiff runtime sentinel in every score test.
- XLA compile test when the production route is XLA-targeted.
- Claude read-only review of test coverage and result interpretation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do admitted LEDH score routes remain correct and memory-bounded at `N=10000`? |
| Baseline/comparator | Phase 4 tiny score checks and same-scalar finite-difference or analytic references. |
| Primary criterion | Every admitted row passes correctness, no-autodiff, finite-score, reproducibility, and memory gates. |
| Veto diagnostics | OOM; hidden autodiff; wrong scalar FD; nonfinite score; value/score algorithm mismatch; row silently skipped. |
| Explanatory diagnostics | Runtime, compile time, memory headroom, and FD noise. |
| Not concluded | Scientific superiority, HMC readiness, and fair runtime ranking. |

## Forbidden Claims/Actions

- Do not lower thresholds after seeing results without human direction.
- Do not treat skipped tests as pass.
- Do not hide GPU unintentionally in `N=10000` tests.
- Do not count the scoped parameterized SIR diagnostic as the fixed-SIR
  full-row `N=10000` score test.

## Allowed Operations

- Edit tests and result artifacts.
- Run trusted GPU/CUDA/XLA TensorFlow checks.
- Run long `N=10000` tests using bounded logs.
- Use Claude read-only test/result review.

## Exact Next-Phase Handoff Conditions

Advance to Phase 6 only if all admitted rows have passing per-model tests or
are explicitly removed from the admitted set with a result artifact.

## Stop Conditions

Stop if an admitted row fails correctness or memory gates and cannot be fixed
within the phase repair loop.
