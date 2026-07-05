# Visible Stop Handoff: Parameterized Zhao-Cui SIR Leaderboard Repair

Date: 2026-07-02

## Status

`STOPPED_AT_PHASE3_FULL_EVALUATOR_COMPLEXITY_GATE`

## Current Phase

Phase 3: Full Observed-Data Evaluator.

## Current Artifacts

- Master program:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-master-program-2026-07-02.md`
- Runbook:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-visible-gated-execution-runbook-2026-07-02.md`
- Ledger:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-visible-execution-ledger-2026-07-02.md`
- Claude review ledger:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-claude-review-ledger-2026-07-02.md`
- Phase 1 result:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase1-source-theta-contract-result-2026-07-02.md`
- Phase 2 result:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase2-dataset-row-contract-result-2026-07-02.md`
- Phase 3 result:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase3-full-evaluator-result-2026-07-02.md`
- Phase 3 blocker JSON:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase3-full-evaluator-blocker-2026-07-02.json`
- Canonical semantic binding:
  `docs/plans/bayesfilter-parameterized-sir-semantic-binding-2026-07-02.md`

## Last Known State

Plan/runbook Claude review converged. Phase 0 checks passed. Phase 1 target
contract review converged. Phase 2 added the distinct parameterized SIR row
`zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` with
`truth_theta_coordinate = sir_log_scale_theta` and
`truth_theta = [0.0, 0.0, 0.0]`, while preserving the fixed
`zhao_cui_spatial_sir_austria_j9_T20` row as `no_free_theta`.

Phase 3 blocked on the then-current candidate Zhao-Cui full observed-data route:
`bayesfilter/highdim/filtering.py::multistate_nonlinear_fixed_design_tt_score_path`.
The lower-rung horizon-0 SIR `d=18` score path runs, but the two-row transition
rung remains blocked by retained full tensor-product grid complexity. The
minimum retained grid at order 2 is `2^18 = 262144` points; the current
streaming transition fallback would need `2097152` chunk products under the
default gate before reaching full `T=20`.

Owner-directive update: this generic multistate retained-grid route is now
diagnostic/historical only.  It should not be repaired or selected as the
production Zhao-Cui leaderboard route.  Production leaderboard work should wire
the fixed-variant Zhao-Cui source-route path instead.

Claude reviewed the Phase 3 blocker after a probe/narrowed line-range path and
returned `VERDICT: AGREE`.

## Tests/Checks Run

- Phase 0 dataset no-free-theta check: passed.
- Phase 0 parameterized SIR local analytical tests: passed.
- Phase 2 focused dataset row tests: `4 passed`.
- Phase 3 focused lower-rung evaluator tests: `2 passed, 2 warnings`.
- JSON syntax checks for dataset manifest and Phase 3 blocker: passed.
- Focused `git diff --check` on touched artifacts: passed.

## Not Concluded

- No full observed-data/filtering SIR score has been admitted.
- No Phase 4 score-at-true, FD, or GPU/XLA validation has run.
- No final leaderboard regeneration has run for the parameterized SIR row.
- No source-faithful parameterized SIR inference claim has been made.
- No permission is granted to substitute the P8p LEDH-PFPF-OT manual score as
  the Zhao-Cui full observed-data leaderboard score.
- No HMC readiness or GPU production readiness claim has been made.

## Remaining Blocker

`BLOCK_PHASE3_FULL_EVALUATOR_COMPLEXITY_GATE`: the historical Zhao-Cui
fixed-design TT multistate retained-grid route does not admit a full T20 SIR
d18 value/analytical-score row under the reviewed Phase 1 contract, and is now
demoted to diagnostic/historical evidence.

## Next Safe Action

Supersede the generic retained-grid candidate and wire the fixed-variant
Zhao-Cui source-route evaluator while preserving analytical/manual score
provenance. Any new route behavior must be classified under the Zhao-Cui
source-anchor gate before code admission.
