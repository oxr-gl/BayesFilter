# DPF V2 Algorithm Full BF/FilterFlow Comparison P1 Architecture Result

metadata_date: 2026-06-07
visible_execution_timestamp: `2026-06-08T02:15:50+08:00`
phase: P1
execution_route: `VISIBLE_IN_DIALOGUE`
status: `PASS_P1_ARCHITECTURE_READY_FOR_P2`

## Question

Can BayesFilter and FilterFlow-side adapters host the two target algorithms over
all six V2 models without mutating `.localsource/filterflow`?

## Evidence Contract

Primary criterion:

- Freeze an architecture matrix with one row per V2 model and algorithm:
  bootstrap-OT BF, bootstrap-OT FF adapter, LEDH-PFPF-OT BF, LEDH-PFPF-OT FF
  adapter.
- For every cell, record implementation path, model equations source, proposal
  semantics, log-density route, OT route, gradient route, and readiness status.
- Confirm FilterFlow-side adapters live under BayesFilter-owned experiment code
  and import FilterFlow interfaces without modifying `.localsource/filterflow`.

Veto diagnostics:

- any planned adapter mutates `.localsource/filterflow`;
- LEDH proposal density or Jacobian/logdet semantics are not stated;
- FilterFlow adapter uses a different state convention, observation route,
  covariance, angle-wrap, RK4 step, structural completion, or parameterization;
- architecture matrix omits a V2 row;
- bootstrap-OT and LEDH-PFPF-OT surfaces are conflated.

Explanatory-only diagnostics:

- native FilterFlow support versus adapter-hosted support;
- expected implementation size;
- anticipated SIR/predator-prey Jacobian complexity.

Non-claims:

- P1 does not establish numerical agreement.

## Local Skeptical Phase Audit

Audit status: `PASS_LOCAL_PHASE_AUDIT`.

Wrong-baseline risk:

- Controlled. P1 freezes architecture for same-contract BF/FF execution and
  does not treat either implementation as an oracle.

Proxy-metric risk:

- Controlled. P1 records no value, gradient, ESS, RMSE, runtime, or finite
  difference promotion metric.

Missing stop-condition risk:

- Controlled. Any need to mutate `.localsource/filterflow`, omit a V2 row,
  conflate bootstrap and LEDH surfaces, or leave LEDH proposal correction
  semantics unstated remains a veto.

Unfair-comparison risk:

- Controlled for P1 by requiring shared V2 model sources, state conventions,
  observation routes, noise/covariance semantics, branch masks, OT route, and
  gradient-route descriptions in every architecture cell. P2 and P5 must still
  freeze executable contract bytes before value or gradient phases.

Hidden-assumption risk:

- Controlled. Local FilterFlow exposes generic SMC, state, proposal,
  transition, observation, resampling criterion, and RegularisedTransform
  interfaces. It does not provide native LEDH proposal support; LEDH-PFPF-OT is
  explicitly BayesFilter-owned FilterFlow-side adapter work.

Environment-mismatch risk:

- Controlled. P1 used source/document inspection only. No TensorFlow import,
  GPU command, student command, value computation, or gradient computation was
  run.

Audit decision:

- No material flaw was found for P1 architecture freeze after Claude read-only
  review returned `VERDICT: AGREE`.

## Architecture Summary

Required V2 rows are preserved in order:

1. `lgssm_2d_h25_rich`
2. `sv_1d_h18_rich`
3. `range_bearing_4d_h20_rich`
4. `structural_ar1_quadratic_h16`
5. `spatial_sir_j3_rk4`
6. `predator_prey_rk4`

For each row, P1 freezes four architecture cells:

- bootstrap-OT BayesFilter execution;
- bootstrap-OT FilterFlow-side adapter execution;
- LEDH-PFPF-OT BayesFilter execution;
- LEDH-PFPF-OT FilterFlow-side adapter execution.

All 24 cells are classified as `ARCHITECTURE_READY_FOR_CONTRACT_FREEZE`, not
as value-matched or gradient-matched.

## Source Surfaces

BayesFilter-owned implementation surfaces:

- bootstrap-OT execution:
  `experiments/dpf_implementation/tf_tfp/filters/dpf_ot_tf.py`;
- LEDH-PFPF-OT execution:
  `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py`;
- LEDH local affine flow:
  `experiments/dpf_implementation/tf_tfp/flows/ledh_tf.py`;
- FilterFlow-style annealed OT mirror:
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`;
- V2 model suite:
  `experiments/dpf_implementation/tf_tfp/fixtures/common_model_suite_tf.py`.

Local FilterFlow read-only interfaces:

- `filterflow.base.State`;
- `filterflow.smc.SMC`;
- `filterflow.proposal.base.ProposalModelBase`;
- `filterflow.proposal.bootstrap.BootstrapProposalModel`;
- `filterflow.transition.base.TransitionModelBase`;
- `filterflow.observation.base.ObservationModelBase`;
- `filterflow.resampling.criterion.NeffCriterion`;
- `filterflow.resampling.differentiable.biased.RegularisedTransform`;
- `filterflow.resampling.differentiable.regularized_transport.plan.transport`.

## Frozen Adapter Semantics

### Bootstrap-OT

Proposal semantics:

- proposal equals transition model;
- FF adapter can use `BootstrapProposalModel` with a V2 transition adapter;
- BF execution uses `run_ot_dpf_tf`.

Log-density route:

- transition log density plus observation log density under V2 fixture
  semantics;
- proposal log density equals transition log density for bootstrap proposal.

OT route:

- FilterFlow side uses `RegularisedTransform`;
- BayesFilter side mirrors the same mathematical route through
  `annealed_transport_resample_tf`;
- fixed-target Sinkhorn remains local comparator only, not this algorithm.

Gradient route:

- fixed-branch AD through differentiable value-path operations and deterministic
  OT under frozen trigger masks;
- no gradient claim through random seeds, random initial sampling, random
  transition sampling, Boolean trigger decisions, or discrete ancestor
  selection.

### LEDH-PFPF-OT

Proposal semantics:

- pre-flow particles are transition proposals from ancestors;
- LEDH local affine map sends pre-flow particles to post-flow particles;
- local observation Jacobian is held fixed per particle for the affine
  determinant.

PF-PF correction:

- corrected log weight is
  `previous_log_weight + target_transition + target_observation -
  pre_flow_log_density + forward_log_det`.

LEDH density/logdet route:

- `pre_flow_log_density` is transition-prior proposal density `q0`;
- `forward_log_det` is the frozen local-affine log absolute determinant from
  `ledh_flow_batch_tf`;
- nonfinite flow, logdet, target transition, target observation, or corrected
  log weights remain later-phase vetoes.

OT route:

- same FilterFlow-style annealed regularized transport route as bootstrap-OT,
  applied after PF-PF correction and fixed ESS trigger masks.

Gradient route:

- fixed-branch AD through LEDH flow, PF-PF correction, and deterministic OT
  under frozen branch masks;
- no gradient claim through random/discrete branch selection.

## Model-Specific Contract Notes

| Model id | State convention | Observation route | Special adapter requirement |
| --- | --- | --- | --- |
| `lgssm_2d_h25_rich` | 2D linear Gaussian state | linear Gaussian observation | preserve A/C/Q/R/m0/P0 semantics |
| `sv_1d_h18_rich` | 1D latent log-volatility | stochastic-volatility observation density | preserve AR(1) `mu,phi,sigma` route |
| `range_bearing_4d_h20_rich` | 4D constant-velocity state | range/bearing with angle wrap | preserve bearing wrap and R covariance |
| `structural_ar1_quadratic_h16` | state `(m,k)` with deterministic k completion | scalar structural observation | preserve singular completion density on m and deterministic k update |
| `spatial_sir_j3_rk4` | `(S_1,I_1,S_2,I_2,S_3,I_3)` | infectious-only observation | preserve RK4 step, neighbor coupling, domain policy, and note no P7 physical gradient knob currently included |
| `predator_prey_rk4` | `(prey,predator)` | direct noisy-state observation | preserve RK4 step, domain policy, and theta `(r,K,a,s,u,v)` parameterization |

## Primary Criterion Results

| Field | Status |
| --- | --- |
| 24-cell architecture matrix frozen | PASS |
| all six V2 rows included in order | PASS |
| bootstrap-OT BF and FF adapter surfaces separated | PASS |
| LEDH-PFPF-OT BF and FF adapter surfaces separated | PASS |
| FF adapters hosted under BayesFilter-owned experiment code | PASS |
| `.localsource/filterflow` mutation required | PASS: no mutation required |
| LEDH proposal density and logdet semantics stated | PASS |
| model-specific state/observation/covariance/angle/RK4/structural conventions recorded | PASS |
| no numerical agreement claim | PASS |

## Veto Diagnostics Result

| Veto | Status |
| --- | --- |
| planned adapter mutates `.localsource/filterflow` | PASS |
| LEDH proposal density/logdet semantics unstated | PASS |
| FF adapter uses different model convention | PASS |
| architecture matrix omits a V2 row | PASS |
| bootstrap-OT and LEDH-PFPF-OT surfaces conflated | PASS |

## Artifacts

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_p1_architecture_2026-06-07.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-v2-algorithm-full-comparison-p1-architecture-2026-06-07.md`
- Result ledger:
  `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p1-architecture-result-2026-06-07.md`

## Claude Read-Only Review

Review timestamp: `2026-06-08T02:26:36+08:00`.

Verdict: `VERDICT: AGREE`.

Claude agreed that:

- P1 is architecture-only and does not promote numerical evidence;
- all six V2 rows and all four architecture surfaces are present;
- LEDH-PFPF-OT FilterFlow support is honestly classified as
  BayesFilter-owned adapter-hosted work, not native FilterFlow support;
- LEDH proposal density, forward-logdet, and PF-PF correction semantics are
  stated clearly enough for P2/P5 contract freeze;
- P2 advancement was correctly blocked until review agreement.

Non-blocking note:

- The visible ledger entries are not strictly monotone by timestamp in file
  order. This does not affect the P1 gate because the top-level state and
  handoff are consistent.

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `PASS_P1_ARCHITECTURE_READY_FOR_P2` | 24-cell architecture matrix and adapter semantics frozen | all local P1 veto diagnostics pass and Claude agreed | P2/P5 still must freeze executable contracts | begin P2 `PRECHECK` visibly | no value match, gradient match, filtering correctness, implementation correctness, scientific correctness, student, TT/SIRT, dense quadrature, paper-table, simulated-truth, GPU, HMC, DSGE, scalability, deployment, or production-readiness claim |

## Post-Run Red Team

Strongest alternative explanation:

- P1 can pass while P2/P5 contract freeze or P3/P6/P4/P7 execution still fail.
  Architecture readiness is not executable numerical agreement.

Result that would overturn the local decision:

- A reviewer finds a missing V2 row, a FilterFlow mutation need, conflated
  bootstrap/LEDH surfaces, a model-convention mismatch, or an unstated LEDH
  proposal correction/logdet route.

Weakest evidence link:

- LEDH-PFPF-OT FilterFlow-side support is adapter-hosted and not native
  FilterFlow functionality. This is explicitly frozen as BayesFilter-owned
  adapter work and remains subject to P5 contract review.

## Non-Claims

- No BayesFilter correctness proof.
- No FilterFlow correctness proof.
- No proof that bootstrap-OT or LEDH-PFPF-OT is scientifically correct.
- No stochastic resampling distribution correctness claim.
- No value or gradient match.
- No gradient-through-random/discrete-branch claim.
- No student implementation claim.
- No TT/SIRT, dense quadrature, paper-table, simulated-truth, GPU, HMC, DSGE,
  scalability, deployment, or production-readiness claim.
