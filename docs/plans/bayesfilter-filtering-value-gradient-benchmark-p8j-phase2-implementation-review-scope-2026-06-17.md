# P8j Phase 2 Implementation Review Scope

metadata_date: 2026-06-17
status: ACTIVE_REVIEW_SCOPE_AFTER_CLAUDE_ITER1

## Purpose

The repository worktree contains substantial pre-existing dirty work in
`scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py` and
`tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py` from
P8g/P8h/P8i and other lanes.  Phase 2 must not claim ownership of that older
churn.

This scope note quarantines the P8j Phase 2 implementation review to the
SIR-specific route admission, callback, tests, smoke artifact, and P8j plan
records.

## In-Scope Phase 2 Code Surface

Review these local definitions and tests as the P8j implementation packet:

- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
  - `_dpf_sir_callbacks()`;
  - the `SIR_ROW` branch in `_dpf_route()`;
  - the inclusion of `SIR_ROW` in `_has_dpf_route()`.
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
  - `test_p8d_source_scope_and_route_policy_are_mechanical` only to the extent
    it now expects SIR DPF route admission;
  - `test_p8j_sir_dpf_callbacks_tie_out_to_author_sir_model`;
  - `test_p8j_sir_dpf_transition_sample_clips_only_susceptible`;
  - `test_p8j_sir_dpf_route_and_bootstrap_smoke_are_finite`.

Review these P8j artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-result-2026-06-17.md`;
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-2026-06-17.json`;
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase3-ledh-alg1-sir-smoke-subplan-2026-06-17.md`;
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md`;
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-claude-review-ledger-2026-06-17.md`;
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-stop-handoff-2026-06-17.md`.

## Explicitly Out Of Scope For Phase 2 Review

Do not treat the following as P8j Phase 2 changes or evidence:

- P8g/P8h/P8i constants, helper functions, CLI flags, HMC/gradient routines,
  particle-tuning routines, OT routes, scalar-SV graph routes, and their tests;
- SV or generalized-SV LEDH adapter changes;
- monograph, P70/P71, fixed-branch, Zhao-Cui TT/SIRT, or source-faithfulness
  artifacts outside this P8j packet;
- unrelated dirty tracked or untracked files in the working tree.

If an out-of-scope change appears to affect P8j behavior, report it as an
interaction risk.  Otherwise, exclude it from the Phase 2 verdict.

## Phase 2 Review Question

Within the in-scope surface above, does P8j Phase 2:

- implement the reviewed SIR callback contract;
- preserve the fixed SIR model/data definitions;
- preserve the clipped-transition adapter boundary;
- admit the SIR row to DPF only through the reviewed callback route;
- provide semantic tie-out tests rather than shape-only route admission;
- write one-seed/N=4 bootstrap smoke evidence without five-seed, tuning,
  leaderboard, gradient/HMC, or TT/SIRT claims?
