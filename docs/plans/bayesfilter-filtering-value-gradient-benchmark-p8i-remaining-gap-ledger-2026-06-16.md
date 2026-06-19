# P8i Remaining Gap Ledger

Date: 2026-06-16

Status: `PHASE8_CLOSEOUT_READY`

## Scope

This ledger maps the limitations preserved by closed P8h into explicit P8i
phase gates. It is a governance artifact only; it does not close any
scientific gap by itself.

## Inherited Route

- row alias: `actual_sv`;
- row ID: `zhao_cui_sv_actual_nongaussian_T1000`;
- algorithm ID: `ledh_pfpf_alg1_ukf_current`;
- route variant: `p8h_sv_scalar_graph_ot_resampled_alg1`;
- resampling route: `ot_sinkhorn_barycentric_covariance_carry`;
- coordinate: `canonical_unconstrained`;
- inherited short-prefix count: `N=5`, diagnostic only.

## Gap Table

| Gap | P8h nonclaim | P8i phase | Required artifact | Promotion gate | Veto diagnostics | Status |
|---|---|---:|---|---|---|---|
| Longer-prefix particle/value adequacy | Not full-horizon particle-count adequacy | 1 | Longer-prefix JSON/CSV and result | Finite trusted-GPU values, transport/covariance carry pass, five fixed seeds, MCSE threshold, adjacent-rung stability, runtime budget | Nonfinite values, CPU fallback, transport failure, runtime over budget, post-hoc threshold change | planned |
| Longer-horizon gradient stability | Not stochastic PF marginal-gradient correctness and not HMC readiness | 2 | Gradient ladder JSON/CSV and result | Finite connected repeatable gradients, bounded FD residuals, trusted GPU, exact route/count | Disconnected/nonfinite gradient, CPU fallback, route mismatch, exact stochastic-gradient overclaim | planned |
| GPU scaling evidence | Not full GPU scaling law | 3 | GPU scaling JSON/CSV and result | Runtime/memory profile supports next HMC tier within budget | OOM, CPU fallback, nonfinite diagnostics, projection over budget | planned |
| HMC beyond Tier-0 | Not production HMC readiness, not posterior convergence, not valid tuning | 4 | HMC Tier-1/Tier-2 artifacts and result | Predeclared finite chain and integrator diagnostics pass without overclaim | Nonfinite samples/log prob, gradient failure, invalid integrator behavior, convergence overclaim | planned |
| NUTS readiness | Not NUTS readiness | 5 | NUTS readiness result and optional diagnostic artifact | Reviewed decision that NUTS is justified, diagnostic-only, or blocked | NUTS inferred from HMC alone, runtime infeasible, adaptive run without review | planned |
| Gradient and likelihood claim boundary | Not stochastic PF marginal-gradient correctness; not exact nonlinear likelihood correctness | 6 | Claim-boundary result | Each claim classified as passed, blocked, diagnostic-only, or out of scope | Relaxed-OT AD called exact stochastic PF marginal score without derivation; scalar surrogate called exact nonlinear likelihood without tieout | planned |
| High-dimensional scope, ranking, defaults | Not generic high-dimensional LEDH readiness; not filter ranking; not default sampler policy | 7 | Ranking/default-policy decision | Conservative decision table preserves missing evidence or justifies a narrow claim | Ranking without comparable baselines, default-policy change from diagnostic-only evidence | planned |
| Artifact and commit boundary | No remote sync, merge safety, bit-for-bit reproduction, or publish status | 8 | Artifact index, reset memo, boundary manifest | Intended P8i files separated from unrelated dirty lanes and blockers preserved | Unrelated Zhao-Cui/monograph/user work included, missing blockers, commit/push without request | planned |

## Cross-Gap Nonclaims

Until a named phase explicitly passes its higher evidence gate, P8i has not
established:

- production HMC readiness;
- posterior convergence;
- valid tuning;
- NUTS readiness;
- stochastic PF marginal-gradient correctness;
- full-horizon HMC feasibility;
- full GPU scaling law;
- exact nonlinear likelihood correctness;
- generic high-dimensional LEDH readiness;
- filter ranking;
- default sampler policy.

## Execution Boundary

Phase 1 may use the current `--p8h-particle-tuning-stage0` runner flag only as
a codepath selector for the OT-resampled Algorithm 1 tuning harness. P8i
provenance must be carried by P8i manifest phase names, P8i plan paths, P8i
output artifact paths, and P8i result notes.
