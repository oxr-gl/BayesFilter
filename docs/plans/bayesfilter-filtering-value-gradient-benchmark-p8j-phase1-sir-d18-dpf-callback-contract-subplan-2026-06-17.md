# P8j Phase 1 Subplan: SIR d18 DPF Callback Contract

metadata_date: 2026-06-17
status: DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md
phase: 1
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Specify the exact callback contract required to admit
`zhao_cui_spatial_sir_austria_j9_T20` into the P8d DPF route table without
executing DPF numerics yet.

The contract must support:

- `bootstrap_dpf_current`;
- `ledh_pfpf_alg1_ukf_current`;
- later OT-resampled LEDH-PFPF-OT through the inherited covariance-carry route.

## Entry Conditions Inherited From Previous Phase

- Phase 0 passed and recorded that SIR d18 DPF callbacks remain missing.
- P8d reset/current runner/tests are the primary missing-route baseline.
- P8g/P8h/P8i are historical non-SIR DPF/LEDH/OT provenance only.
- Fixed-parameter SIR has no free theta; score/Hessian/theta-gradient/HMC/NUTS
  claims remain forbidden.

## Required Artifacts

- Phase 1 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase1-sir-d18-dpf-callback-contract-result-2026-06-17.md`
- Updated P8j execution ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md`
- Updated P8j Claude review ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-claude-review-ledger-2026-06-17.md`
- Draft Phase 2 subplan, only if Phase 1 passes:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-subplan-2026-06-17.md`

## Required Checks/Tests/Reviews

Local contract-surface checks:

```bash
rg -n "def _dpf_.*callbacks|def _dpf_route|def _has_dpf_route|def _sir_structural|SIR_ROW|DPF_SEEDS|DPF_PARTICLE_COUNT" scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py
rg -n "zhao_cui_sir_austria_model|transition_mean|transition_log_density|observation_log_density|infectious_components|_apply_process_noise_policy" bayesfilter/highdim/models.py
rg -n "assert not p8d._has_dpf_route\\(SIR_ROW\\)|test_p8d_spatial_sir_value_only_cell_preserves_no_free_theta|test_p57_m1_author_sir" tests/highdim
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase1-sir-d18-dpf-callback-contract-subplan-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase1-sir-d18-dpf-callback-contract-result-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-claude-review-ledger-2026-06-17.md
```

Claude read-only review of this subplan and the Phase 1 result is required
before Phase 2 implementation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact TensorFlow callbacks must be added so SIR d18 can enter the DPF route table without changing the model, observations, or fixed-parameter claim boundary? |
| Baseline/comparator | Existing DPF callback dictionaries for LGSSM/SV/predator-prey/generalized-SV; `highdim.zhao_cui_sir_austria_model()`; deterministic `_sir_structural()` route; tests preserving no-free-theta SIR semantics. |
| Primary criterion | Phase 1 result specifies each required callback, shape, density, metadata field, and test update needed for SIR d18 DPF admission; no DPF numerical run is launched. |
| Veto diagnostics | Contract changes SIR model/data definitions; omits clipping/process-noise policy; treats Gaussian transition density after clipping as exact target density; omits observation Jacobian; fabricates theta/score/HMC semantics; treats callbacks as Zhao-Cui TT/SIRT source-faithfulness; authorizes implementation before review. |
| Explanatory diagnostics | Existing callback keys, SIR model methods, author-source parity tests, deterministic SIR value-only route, route-table tests. |
| Not concluded | Callback implementation correctness, finite DPF execution, LEDH/OT quality, particle-count adequacy, leaderboard completion, gradient/HMC readiness. |

## Required Callback Contract

Phase 2 implementation must add a `_dpf_sir_callbacks()` route with these
TensorFlow callbacks and metadata:

- `initial_sample(num_particles, seed)`:
  sample from `model.initial_mean + Normal(0, I_18)` using stateless seeds and
  `tf.linalg.cholesky(model.initial_covariance)`.
- `transition_mean_fn(points, time_index)`:
  call `model.transition_mean(points)`; `time_index` is ignored because the row
  is time-homogeneous.
- `transition_sample(particles, seed, time_index)`:
  sample additive process noise with covariance `model.process_covariance`,
  add it to `transition_mean_fn`, then apply
  `model._apply_process_noise_policy(...)` exactly as `_sir_structural()` and
  the model simulation path do.
- `transition_log_density_fn(next_particles, previous_particles, time_index)`:
  call `model.transition_log_density(tf.zeros([0], tf.float64), previous,
  next, time_index)`.  This is the Gaussian additive-noise transition density
  associated with the pre-projection RK4 mean.  Because `transition_sample`
  applies `clip_susceptible_after_noise`, this callback must be recorded as a
  reviewed BayesFilter correction adapter for the clipped SIR propagation path,
  not as the exact density of the clipped pushforward state and not as exact
  source-filter proof.
- `observation_mean_fn(points, time_index)`:
  return `model.infectious_components(points)`.
- `observation_jacobian_fn(point, time_index)`:
  return a constant 9x18 selector matrix with ones at infectious coordinates
  `1, 3, ..., 17`.
- `observation_log_density_fn(points, observation, time_index)`:
  call `model.observation_log_density(tf.zeros([0], tf.float64), points,
  observation, time_index)`.
- `process_noise_covariance_fn(point, time_index)`:
  return `model.process_covariance`.
- `observation_covariance_fn(time_index)`:
  return `model.observation_covariance`.
- `initial_covariance`:
  `model.initial_covariance`.
- `ledh_observation_adapter` metadata:
  classify the SIR LEDH route as same-observation Gaussian flow/correction,
  with `target_density_used_for_correction=True`,
  `surrogate_target_claim=False`, and
  `adapter_classification="BayesFilter DPF adapter for fixed-parameter SIR; not Zhao-Cui TT/SIRT source-faithfulness evidence"`.

`_dpf_route(SIR_ROW)` must then return:

- callbacks from `_dpf_sir_callbacks()`;
- `_sir_observations()`;
- route label `"spatial_sir_austria_j9_T20"`;
- horizon `20`.

`_has_dpf_route(SIR_ROW)` must become true only after tests verify the callback
contract.

## Required Tests For Phase 2

Phase 2 must add focused tests before or with implementation:

- callback dictionary has all required keys and SIR metadata;
- initial samples shape `[N, 18]`;
- transition samples shape `[N, 18]` and finite values;
- observation means shape `[N, 9]`;
- observation Jacobian shape `[9, 18]` and equals the infectious selector;
- observation log density shape `[N]` and finite values for model observations;
- process and observation covariance shapes are `[18, 18]` and `[9, 9]`;
- `_has_dpf_route(SIR_ROW)` becomes true;
- `_dpf_route(SIR_ROW)` returns horizon `20` and route label containing
  `spatial_sir`;
- deterministic SIR no-free-theta tests continue to pass.

Phase 2 must also add semantic tie-out tests against
`highdim.zhao_cui_sir_austria_model()`:

- `transition_mean_fn(points, t)` equals `model.transition_mean(points)` for a
  nontrivial state batch;
- `observation_mean_fn(points, t)` equals `model.infectious_components(points)`;
- `observation_jacobian_fn(point, t)` equals the infectious-coordinate selector
  implied by `model.observed_state_indices()`;
- `transition_log_density_fn(next, previous, t)` has finite `[N]` values and is
  explicitly identified in metadata as the Gaussian pre-projection density used
  by the reviewed clipped-path adapter;
- `transition_sample(...)` clips only susceptible coordinates after process
  noise, matching the model policy and the author-source parity test, while
  leaving infectious coordinates unclipped;
- callback model identity/metadata records
  `zhao_cui_spatial_sir_austria_j9_T20`,
  `rk4_variant="zhao_cui_sir_step"`,
  `process_noise_policy="clip_susceptible_after_noise"`, state dimension `18`,
  and observation dimension `9`.

## Forbidden Claims/Actions

- Do not edit implementation code in Phase 1.
- Do not run bootstrap, LEDH, OT, tuning, or leaderboard numerics in Phase 1.
- Do not claim SIR DPF is implemented or finite.
- Do not claim exact nonlinear filtering correctness, Zhao-Cui TT/SIRT
  source-faithfulness, score/Hessian/theta-gradient/HMC/NUTS readiness, or
  production readiness.
- Do not stage, commit, merge, or push.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if:

- Phase 1 result records the callback contract above;
- local checks pass;
- Claude returns `VERDICT: AGREE` on the Phase 1 contract/result packet;
- Phase 2 subplan is drafted and reviewed;
- no DPF numerical run was launched during Phase 1.

## Stop Conditions

Stop and write a blocker if:

- local code shows SIR model semantics differ from this contract;
- observation Jacobian or transition density cannot be represented in the
  existing callback interface;
- the reviewed contract would require changing SIR data/model definitions;
- Claude review does not converge after five rounds for the same blocker.

## Skeptical Plan Audit

This phase could pass while misleading us if it quietly treats callback
admission as numerical validation.  It therefore produces a contract only and
keeps implementation, smoke, tuning, and leaderboard gates in later phases.
The contract uses the existing SIR model source and deterministic structural
route, not P71 fixed-branch artifacts or scalar-SV P8h/P8i evidence.
