# P8h Visible Stop Handoff

Date: 2026-06-16

Status: `CLOSED_PHASE10_BOUNDARY_REVIEWED`

## Current State

P8h is the active DPF/LEDH repair lane. It supersedes the P8g
no-resampling-centered path for serious value, gradient, GPU, and HMC-smoke
work. Zhao-Cui high-dimensional fixed-branch work and the broader monograph
rewrite are out of scope for this lane.

Phases 0-10 have completed with reviewed results. The active route preserved
by P8h is:

`Li-Coates Algorithm 1 UKF LEDH + PF-PF correction + Corenflos-style relaxed Sinkhorn OT resampling + same-transport barycentric covariance carry`.

Exact current route/configuration:

- row alias: `actual_sv`;
- resolved row ID: `zhao_cui_sv_actual_nongaussian_T1000`;
- algorithm ID: `ledh_pfpf_alg1_ukf_current`;
- route variant: `p8h_sv_scalar_graph_ot_resampled_alg1`;
- resampling route: `ot_sinkhorn_barycentric_covariance_carry`;
- canonical transport convention: `target_by_source_row_stochastic`;
- selected Stage 0 particle count: `N=5`;
- coordinate: `theta=(Phi^{-1}(gamma), log(beta))`, sigma fixed at `1.0`;
- GPU context: trusted TensorFlow GPU evidence was required for GPU artifacts.

## Last Completed Gate

Phase 10 passed as a repo-hygiene and commit-boundary review:

- result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase10-repo-hygiene-result-2026-06-16.md`;
- boundary manifest:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase10-commit-boundary-manifest-2026-06-16.json`;
- status: `PASS_BOUNDARY_REVIEWED`;
- commit/push status: no commit or push was performed.

The last numerical gate remains Phase 8:

Phase 8 passed as a Tier-0 fixed-kernel HMC execution smoke only:

- artifact:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase8-hmc-tier0-smoke-result-2026-06-16.md`;
- JSON/CSV:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase8-hmc-tier0-smoke-gpu-2026-06-16.json`,
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase8-hmc-tier0-smoke-gpu-2026-06-16.csv`;
- HMC kernel: `tfp.mcmc.HamiltonianMonteCarlo`;
- HMC settings: `num_results=2`, `num_burnin_steps=1`,
  `step_size=0.005`, `num_leapfrog_steps=1`;
- pass basis: trusted GPU tensor placement, finite initial value/gradient,
  connected gradient, finite samples, finite target log probabilities, finite
  log-accept ratios, no blocker.

The acceptance rate `1.0` is explanatory trace data only. It is not tuning
quality or convergence evidence.

## Next Action

P8h is closed. Remaining scientific gaps require a new gated follow-on program.
Commit or push remains forbidden unless the user explicitly requests it after
reviewing the Phase 10 boundary.

## Not Concluded

P8h has not established production HMC readiness, posterior convergence, valid
tuning, NUTS readiness, stochastic PF marginal-gradient correctness,
full-horizon HMC feasibility, full GPU scaling law, exact nonlinear likelihood
correctness, generic high-dimensional LEDH readiness, filter ranking, or a
default sampler policy.

## Key Artifacts

- Artifact index:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-artifact-index-2026-06-16.json`;
- Master program:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-ot-resampled-alg1-ledh-master-program-2026-06-15.md`;
- Runbook:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-visible-gated-execution-runbook-2026-06-15.md`;
- Execution ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-visible-execution-ledger-2026-06-15.md`;
- Claude review ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-claude-review-ledger-2026-06-15.md`;
- Phase 9 subplan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase9-closeout-artifact-refresh-subplan-2026-06-15.md`;
- Phase 10 subplan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase10-repo-hygiene-subplan-2026-06-16.md`.
- Phase 10 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase10-repo-hygiene-result-2026-06-16.md`;
- Phase 10 boundary manifest:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase10-commit-boundary-manifest-2026-06-16.json`;
- Phase 11 status-sync subplan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase11-closure-sync-subplan-2026-06-16.md`.
