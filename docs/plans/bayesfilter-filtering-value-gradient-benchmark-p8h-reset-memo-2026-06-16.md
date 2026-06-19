# P8h Reset Memo: OT-Resampled Algorithm 1 LEDH Repair

Date: 2026-06-16

Status: `CLOSED_PHASE10_BOUNDARY_REVIEWED`

## Scope

This memo resets the active DPF/LEDH lane after P8h Phases 0-8. Zhao-Cui
high-dimensional fixed-branch work and the broader monograph rewrite are out
of scope here.

## Current Route

The active P8h serious-candidate route is:

`Li-Coates Algorithm 1 UKF LEDH + PF-PF correction + Corenflos-style relaxed Sinkhorn OT resampling + same-transport barycentric covariance carry`.

Exact identifiers:

- row alias: `actual_sv`;
- resolved row ID: `zhao_cui_sv_actual_nongaussian_T1000`;
- algorithm ID: `ledh_pfpf_alg1_ukf_current`;
- route variant: `p8h_sv_scalar_graph_ot_resampled_alg1`;
- resampling route: `ot_sinkhorn_barycentric_covariance_carry`;
- canonical transport convention: `target_by_source_row_stochastic`;
- selected Stage 0 particle count: `N=5`;
- coordinate: `canonical_unconstrained`, meaning
  `theta=(Phi^{-1}(gamma), log(beta))`, sigma fixed at `1.0`.

P8g no-resampling/fixed-randomness artifacts are historical graph/kernel/shape
and diagnostic context only. They are not the current serious DPF route and do
not provide HMC entry authority.

## Phase Status

| Phase | Status | Meaning |
|---:|---|---|
| 0 | `PASS_REVIEWED` | Documentation/governance corrected the Algorithm 1 covariance-state and OT-resampling relationship. |
| 1 | `PASS_REVIEWED` | Route roles reset: P8h is the active serious-candidate lane; P8g no-resampling is historical context. |
| 2 | `PASS_REVIEWED` | Design contract fixed canonical `A[target, source]` transport convention and covariance carry. |
| 3 | `PASS_REVIEWED` | Scalar-SV OT implementation passed CPU/GPU smoke after fail-closed transport validation repair. |
| 4 | `PASS_REVIEWED` | Local integration diagnostics passed for exact P8h route. |
| 5 | `PASS_STAGE0_PREFIX_SELECTED_REVIEWED` | Stage 0 prefix tuning selected `N=5` for diagnostic use only. |
| 6 | `PASS_OT_GRADIENT_REVIEWED` | Relaxed Sinkhorn OT route has finite connected repeatable AD gradients on trusted GPU for the short diagnostic. |
| 7 | `PASS_SMALL_HMC_FEASIBILITY_REVIEWED` | Short-prefix trusted-GPU profile supports attempting a tiny HMC smoke. |
| 8 | `PASS_TIER0_HMC_EXECUTION_REVIEWED` | Tiny fixed-kernel TFP HMC execution smoke ran on trusted GPU with finite value/gradient/samples/trace quantities. |
| 9 | `PASS_CLOSEOUT_REVIEWED` | Closeout artifacts preserved route, count, Phase 8 boundary, nonclaims, and handoff state. |
| 10 | `PASS_BOUNDARY_REVIEWED` | Repo-hygiene manifest isolated P8h code/test/docs/results from unrelated dirty lanes; no commit or push performed. |
| 11 | `STATUS_SYNC_ONLY` | Terminal summary fields were synchronized to Phase 10 closure without adding scientific evidence. |

## Phase 8 HMC Smoke Boundary

Phase 8 used:

- HMC kernel: `tfp.mcmc.HamiltonianMonteCarlo`;
- PF seed: `81120`;
- HMC seed: `[81120, 82120]`;
- horizon: `4`;
- particles: `5`;
- `num_results=2`;
- `num_burnin_steps=1`;
- `step_size=0.005`;
- `num_leapfrog_steps=1`;
- trusted GPU tensor evidence: `/device:GPU:0`.

The result proves only that the selected short-prefix P8h value/gradient graph
can execute inside a tiny fixed-kernel HMC chain on trusted GPU with finite
initial value/gradient, finite samples, finite target log probabilities, and
finite log-accept ratios.

The acceptance rate `1.0` is explanatory trace data only. It is not tuning
quality or convergence evidence.

## Remaining Limitations

Do not claim:

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

## Active Files To Preserve

The closeout artifact index is:

`docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-artifact-index-2026-06-16.json`.

It lists P8h implementation files, tests, documents, subplans/results,
diagnostic JSON/CSV artifacts, and nonclaim boundaries for Phase 10 repo
hygiene.

## Next Step

P8h is closed. Do not commit or push unless the user explicitly requests that
git operation after reviewing the Phase 10 boundary. Remaining scientific gaps
must be handled in a new gated follow-on program, not by retroactively widening
P8h.
