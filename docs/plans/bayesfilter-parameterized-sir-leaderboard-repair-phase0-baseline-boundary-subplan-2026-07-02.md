# Phase 0 Subplan: Baseline And Boundary Freeze

Date: 2026-07-02

Status: `DRAFT_PENDING_REVIEW`

## Phase Objective

Freeze the current SIR leaderboard state, confirm that the strange behavior is
a target/theta-contract issue, and preserve the boundary between the existing
fixed source-parity SIR row and the proposed parameterized inference row.

## Entry Conditions Inherited From Previous Phase

- Master program exists.
- No implementation changes for this program have been made yet.
- Current dirty worktree may contain unrelated user/agent work and must be
  preserved.

## Required Artifacts

- Phase 0 result:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase0-baseline-boundary-result-2026-07-02.md`
- Refreshed Phase 1 subplan:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase1-source-theta-contract-subplan-2026-07-02.md`
- Execution ledger update:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-visible-execution-ledger-2026-07-02.md`

## Required Checks/Tests/Reviews

- Inspect current dataset contract and model implementation with `rg`/`sed`.
- Run focused CPU-only local checks:
  - `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py::test_p8_dataset_manifest_generates_sir_raw_synthetic_but_not_source_route_success`
  - `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p81_analytical_sir_score.py::test_parameterized_zhao_cui_sir_matches_p8p_p79_theta_convention tests/highdim/test_p81_analytical_sir_score.py::test_parameterized_sir_log_density_parameter_scores_match_diagnostic_tape`
- Claude read-only review of Phase 0 result or Phase 1 subplan if the boundary
  classification is ambiguous.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the current SIR blocker caused by a fixed/no-free-theta row contract while parameterized local score math already exists? |
| Baseline/comparator | Current dataset generator, current P8 dataset tests, current `ParameterizedZhaoCuiSIRSSM`, current July 2 leaderboard result. |
| Primary pass criterion | Result artifact states the exact current blocker and distinguishes fixed row from parameterized candidate. |
| Veto diagnostics | Inability to find current row contract; missing parameterized model; test failure showing local score convention is absent. |
| Explanatory diagnostics | Existing source-parity notes, P91 local complete-data notes. |
| Not concluded | No full observed-data filtering score admission, no code repair, no source-faithful parameterization claim. |
| Artifact | Phase 0 result. |

## Forbidden Claims/Actions

- Do not change code in Phase 0.
- Do not claim the parameterized route is source-faithful.
- Do not treat P91 local complete-data evidence as full observed-data
  filtering evidence.
- Do not admit leaderboard score cells.

## Exact Next-Phase Handoff Conditions

Phase 1 may start only if Phase 0 records:

- current fixed row has `no_free_theta`;
- local parameterized SIR score components exist;
- the old fixed row and new parameterized candidate are separate targets;
- required focused checks pass or a precise blocker is written.

## Stop Conditions

Stop if local artifacts contradict the assumed current state, if focused tests
fail for reasons unrelated to Phase 0, or if current dirty work prevents
reading the required files safely.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 0 result or blocker.
3. Draft or refresh Phase 1 subplan.
4. Review Phase 1 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
