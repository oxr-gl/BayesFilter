# P8i Visible Stop Handoff

Date: 2026-06-16

Status: `P8I_CLOSED_REVIEWED`

## Current State

P8i has completed reviewed Phases 0-8 and is closed. P8h is closed through
Phase 10/11 and remains provenance baseline only through artifacts explicitly
inherited or re-tested by P8i.

## Active Route

- row alias: `actual_sv`;
- row ID: `zhao_cui_sv_actual_nongaussian_T1000`;
- algorithm ID: `ledh_pfpf_alg1_ukf_current`;
- route variant: `p8h_sv_scalar_graph_ot_resampled_alg1`;
- resampling route: `ot_sinkhorn_barycentric_covariance_carry`;
- coordinate: `canonical_unconstrained`;
- selected longer-prefix diagnostic count: `N=5` at horizons `16,32`, not
  full-horizon adequacy.

## Next Action

No next phase is authorized. Do not commit, push, merge, or stage files unless
the user gives a fresh explicit request.

## Not Concluded

P8i has not established production HMC readiness, posterior convergence, valid
tuning, NUTS readiness, stochastic PF marginal-gradient correctness,
full-horizon HMC feasibility, full GPU scaling law, exact nonlinear likelihood
correctness, generic high-dimensional LEDH readiness, filter ranking, or a
default sampler policy.
