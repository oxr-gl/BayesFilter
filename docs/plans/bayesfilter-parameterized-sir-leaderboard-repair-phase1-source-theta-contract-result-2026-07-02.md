# Phase 1 Result: Source And Theta Contract

Date: 2026-07-02

Status: `PASS_PHASE1_TARGET_CONTRACT_REVIEWED`

## Objective

Define the reviewed parameterized SIR target contract before any dataset or
leaderboard implementation change.

## Entry Evidence

- Phase 0 result confirmed the current fixed SIR dataset row remains
  `truth_theta_coordinate = no_free_theta` with `truth_theta = []`.
- Phase 0 result confirmed `ParameterizedZhaoCuiSIRSSM` exists and focused
  local analytical score tests pass.
- Phase 1 did not change implementation code or regenerate leaderboard
  artifacts.

## Artifacts

- Target contract:
  `docs/plans/bayesfilter-parameterized-sir-target-contract-2026-07-02.md`
- Semantic binding draft:
  `docs/plans/bayesfilter-parameterized-sir-semantic-binding-2026-07-02.md`
- Claude review ledger:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-claude-review-ledger-2026-07-02.md`
- Execution ledger:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-visible-execution-ledger-2026-07-02.md`

## Decisions

| Field | Decision |
| --- | --- |
| New row id | `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` |
| Fixed row preservation | Preserve `zhao_cui_spatial_sir_austria_j9_T20` as fixed/no-free-theta evidence. |
| Theta coordinate | `sir_log_scale_theta` |
| Truth theta | `[0.0, 0.0, 0.0]` |
| Truth semantics | Log-scale origin reproducing the fixed source SIR base values. |
| Parameter order | `log_kappa_scale`, `log_nu_scale`, `log_obs_noise_scale` |
| Theta domain | `[-0.5, 0.5]^3` for admission diagnostics. |
| Classification | Fixed base formulas are source-anchored; the free-theta log-scale surface is `extension_or_invention` as an inference parameterization. |
| Historical candidate evaluator route | `bayesfilter/highdim/filtering.py::multistate_nonlinear_fixed_design_tt_score_path`, now demoted to diagnostic/historical retained-grid evidence and not admitted for production leaderboard wiring. |
| Production evaluator direction | Fixed-variant Zhao-Cui source-route path. |
| Published score provenance | Analytical/manual derivative returned as `FixedBranchScoreResult.score`; autodiff and finite difference are diagnostics only. |

## Review Evidence

Claude target-contract review converged on iteration 5 with
`VERDICT: AGREE`.

The final repair specifically addressed:

- explicit boundary/corner admission diagnostic over truth plus all eight
  corners of `[-0.5, 0.5]^3`;
- local score-route math-contract citations for
  `bayesfilter/highdim/filtering.py:1392`-`1709`,
  `bayesfilter/highdim/models.py:1034`-`1110`, and
  `tests/highdim/test_p81_analytical_sir_score.py:132`-`268`;
- preservation of the Phase 3 full-`T=20` admission boundary.

## Local Checks

- `git diff --check -- docs/plans/bayesfilter-parameterized-sir-target-contract-2026-07-02.md docs/plans/bayesfilter-parameterized-sir-semantic-binding-2026-07-02.md docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-visible-execution-ledger-2026-07-02.md docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-claude-review-ledger-2026-07-02.md`
  passed.
- Focused `rg` checks confirmed the new boundary/corner and score-route
  contract fields are present.

## Environment

- Phase 1 checks were document/static checks only.
- GPU/CUDA was not used.
- Claude review was run through trusted/escalated
  `bash scripts/claude_worker.sh` as a foreground read-only review.

## Stop Conditions Assessed

- No source-faithful inference-theta claim was made.
- No old fixed row retirement was authorized or performed.
- No exact likelihood, exact-gradient, HMC-readiness, GPU-readiness, or
  leaderboard-rank claim was made.

## Next Handoff

Phase 2 may start. It must add or repair a distinct parameterized dataset row
with the reviewed row id, theta coordinate, truth theta, and truth semantics,
while preserving the old fixed/no-free-theta row unless the human explicitly
authorizes retirement.
