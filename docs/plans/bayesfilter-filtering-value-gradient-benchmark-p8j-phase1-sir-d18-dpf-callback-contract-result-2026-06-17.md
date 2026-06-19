# P8j Phase 1 Result: SIR d18 DPF Callback Contract

metadata_date: 2026-06-17
status: PASS
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md
phase: 1
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Advance to Phase 2 bootstrap SIR smoke implementation. |
| Primary criterion status | Passed.  The callback contract states required keys, shapes, semantic tie-outs, metadata, and tests without launching numerics. |
| Veto diagnostic status | No veto fired after revision.  The clipped SIR transition density is explicitly an adapter boundary, not exact clipped-pushforward density or source-filter proof. |
| Main uncertainty | The callbacks are not implemented yet; finite bootstrap DPF execution remains unproven. |
| Next justified action | Implement `_dpf_sir_callbacks()`, route admission, focused callback tests, and a minimal bootstrap smoke in Phase 2. |
| What is not concluded | No LEDH/OT SIR result, no particle-count adequacy, no leaderboard refresh, no score/Hessian/theta-gradient/HMC/NUTS readiness. |

## Contract Closed

Phase 1 specifies that `_dpf_sir_callbacks()` must provide:

- stateless Gaussian initial sample from the fixed SIR initial distribution;
- transition mean equal to `highdim.zhao_cui_sir_austria_model().transition_mean`;
- transition sample using additive process noise and
  `clip_susceptible_after_noise`;
- Gaussian pre-projection transition log density as a reviewed clipped-path
  adapter boundary;
- observation mean equal to infectious components;
- constant 9x18 infectious-coordinate selector Jacobian;
- observation log density equal to the fixed SIR Gaussian observation density;
- process and observation covariance callbacks;
- initial covariance;
- metadata identifying the fixed-parameter SIR row and forbidding TT/SIRT,
  exact source-filter, gradient, HMC, and production claims.

## Review And Repair

Claude review iteration 1 returned `VERDICT: REVISE` for two fixable issues:

- transition-density wording needed to state that `model.transition_log_density`
  is pre-projection Gaussian density for a reviewed clipped-path adapter, not
  exact clipped-pushforward density;
- Phase 2 tests needed semantic tie-outs against
  `highdim.zhao_cui_sir_austria_model()`, not only shape checks.

The Phase 1 subplan was patched.  Claude review iteration 2 returned
`VERDICT: AGREE`.

## Required Phase 2 Handoff

Phase 2 may implement only:

- `_dpf_sir_callbacks()`;
- `_dpf_route(SIR_ROW)` route admission;
- `_has_dpf_route(SIR_ROW)` update;
- focused callback and bootstrap smoke tests;
- a minimal bootstrap SIR smoke artifact.

Phase 2 must not implement LEDH/OT SIR claims beyond preserving callback
surface compatibility for later phases.  Phase 2 must not claim particle-count
adequacy or leaderboard completion.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Recorded by later compute artifacts; Phase 1 used local source inspection only. |
| Dirty state | Repository had substantial pre-existing dirty/untracked work outside P8j; Phase 1 edited only P8j plan artifacts. |
| Commands | Local `rg`, `sed`, `git diff --check`, and Claude read-only worker review. |
| Environment | Local repo, no GPU command, no DPF numerical run. |
| CPU/GPU status | N/A; no compute run. |
| Data version | Current local P8d source-scope and adapter matrix. |
| Seeds | N/A; no stochastic run. |
| Wall time | N/A. |
| Output artifacts | This result, updated execution ledger, updated Claude review ledger, updated stop handoff, Phase 2 subplan. |
| Plan file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase1-sir-d18-dpf-callback-contract-subplan-2026-06-17.md` |
| Result file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase1-sir-d18-dpf-callback-contract-result-2026-06-17.md` |
