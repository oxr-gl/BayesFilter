# P8p Phase 1 Result: Parameterized SIR Objective Contract

Date: 2026-06-18

Status: `PASS_PHASE1_TARGET_CONTRACT_PHASE2_READY_REVIEWED`

## Phase Objective

Define the parameterized SIR d18 diagnostic objective before implementation.
The target remains a diagnostic fixed-randomness objective for gradient and
HMC-mechanics tests, not a scientific posterior target.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the proposed theta target differentiable, fixed-randomness, SIR d18-shaped, and narrow enough for diagnostic gradient/HMC-mechanics testing? |
| Baseline/comparator | Current fixed-parameter actual-SIR harness with P8o settings at theta zero. |
| Primary pass criterion | Phase 1 passes if the result specifies theta transforms, fixed observations, fixed initial/process random streams, differentiable relaxed OT, no categorical resampling, exact implementation surface, Phase 2 smoke sizes, and forbidden claims. |
| Veto diagnostics | Random streams depending on theta; stochastic categorical resampling; theta changes that alter state/observation dimensions; hidden NumPy implementation for differentiable path; missing fixed-seed contract; relying only on the zero-filled score helper for connectivity; missing exact theta-dependent edit points; claiming scientific posterior parameterization. |
| Not concluded | Gradient correctness, HMC readiness, exact likelihood correctness, posterior validity, or production/default readiness. |

## Target Contract

Diagnostic theta:

```text
theta = [
  log_kappa_scale,
  log_nu_scale,
  log_obs_noise_scale
]
```

Physical transforms:

```text
kappa(theta) = base_kappa * exp(log_kappa_scale)
nu(theta) = base_nu * exp(log_nu_scale)
observation_covariance(theta) =
    base_observation_covariance * exp(2 * log_obs_noise_scale)
```

At `theta = [0, 0, 0]`, the diagnostic target recovers the current
fixed-parameter SIR d18 settings used by the P8j/P8o value-only route.

Optional HMC-mechanics log target for Phase 7:

```text
log_target(theta) =
    mean_fixed_randomness_dpf_log_likelihood(theta)
    - 0.5 * sum(theta**2)
```

The standard-normal theta prior is allowed only as a diagnostic mechanics
stabilizer.  It is not a scientific prior and must not be represented as a
posterior validity claim.

## Fixed-Randomness Contract

Phase 2 and later phases must hold fixed across theta evaluations:

- SIR observations from `_sir_observations()`;
- batch seed list;
- initial particles sampled from the same fixed seeds;
- stateless process-noise draws indexed by batch seed and time index;
- fixed resampling mask and relaxed Sinkhorn OT settings;
- chunk sizes and precision settings for a given comparison arm.

Random streams must not depend on theta.  Any finite-difference diagnostic must
use the same fixed random streams for `theta + h e_j` and `theta - h e_j`.

## Exact Implementation Surface

Phase 2 should add a P8p-specific diagnostic harness rather than modifying the
P8j value-only leaderboard harness in place.  Proposed new file:

- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`

The harness may import helpers from:

- `docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py`
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`

Theta-dependent implementation points copied or wrapped from the current
actual-SIR harness:

- `docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py::_make_actual_sir_callbacks`
  currently captures fixed `kappa`, `nu`, `process_chol`, and
  `observation_covariance`;
- `transition_mean` and nested `sir_rhs` must take theta-dependent `kappa` and
  `nu`;
- `pre_flow_step` must use theta-dependent transition means while preserving
  fixed stateless process-noise draws;
- `transition_log_density_fn` must use the same theta-dependent transition mean
  as `pre_flow_step`;
- `observation_log_density_fn`, LEDH flow covariance inputs, and the tiled
  `observation_covariance` tensor must use theta-dependent observation
  covariance for `log_obs_noise_scale`;
- the identity `transition_matrix` remains a shape carrier for the LEDH core;
  nonlinear prior means are supplied through `prior_mean_fn`.

## Connectivity Diagnostic Contract

The existing helper
`streaming_batched_ledh_pfpf_ot_value_and_score_tf` is not sufficient for
connectivity certification because it zero-fills unconnected gradients.

Phase 2 must implement an explicit diagnostic that, for each theta component:

- computes an AD gradient with no silent success on `None` gradients;
- records whether each component is connected;
- records the absolute gradient component and gradient norm;
- runs same-randomness central finite differences as a diagnostic sensitivity
  check;
- blocks if a component is disconnected, nonfinite, or exactly zero without a
  reviewed structural explanation.

## Phase 2 Smoke Sizes

Initial Phase 2 smoke should be cheap and discriminating:

- horizon: `T=3`;
- particles: small, for example `N=8` or `N=16`;
- seeds: one or two seeds for implementation smoke;
- transport policy: `active-all`;
- Sinkhorn iterations: `10`;
- chunk sizes: small, for example `row=8`, `col=8`, `particle=8`;
- precision: start with `float32`/TF32 for GPU smoke and optionally CPU
  `float64` for a finite-difference diagnostic if the small fixture permits it.

GPU claims require trusted/escalated execution.

## Local Checks

Commands run:

```bash
python -m py_compile docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py
rg -n "transition_mean|pre_flow_step|observation_log_density_fn|process_chol|observation_covariance|kappa|nu" docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py bayesfilter/highdim/models.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-*
```

Results:

- `py_compile`: passed.
- Source-surface `rg`: found the required callback and model anchors.
- `git diff --check`: passed before this result was written; rerun after the
  Phase 2 subplan is added before review.

## Skeptical Audit

- Wrong baseline: theta zero is anchored to the current fixed SIR settings, but
  P8o remains value-only entry evidence, not gradient evidence.
- Proxy metrics: finite differences are a sensitivity diagnostic and can veto;
  they are not proof of stochastic PF marginal-gradient correctness.
- Hidden assumption: process covariance is kept fixed in Phase 2.  This is a
  deliberate initial target restriction; process-noise scaling would be a later
  target extension after the three-parameter target passes.
- Environment mismatch: GPU runs must be escalated/trusted; CPU-only runs must
  explicitly hide GPU if used.
- Artifact fitness: a new P8p harness avoids mutating P8j value-only artifacts
  and gives a clean diagnostic boundary.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Pass Phase 1 target contract. | Passed by contract design, source-surface checks, and Claude review after repair. | No Phase 1 veto active. | Phase 2 may find implementation or gradient-connectivity blockers in the actual graph. | Implement the P8p diagnostic harness under the reviewed Phase 2 subplan. | No gradient correctness, HMC readiness, posterior validity, exact likelihood correctness, or production/default readiness. |

## Handoff To Phase 2

Phase 2 must:

- implement `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`;
- preserve P8j value-only harness behavior;
- expose CLI arguments for theta, seeds, horizon, particles, chunks, precision,
  device, and output artifacts;
- include a theta-zero parity check against the current P8j fixed-parameter
  tiny-shape route before accepting gradient evidence;
- include repeated same-theta evaluation and artifact fields proving the fixed
  random streams, fixed resampling mask, relaxed Sinkhorn OT route, and absence
  of categorical resampling;
- run local compile/focused tests;
- run a tiny fixed-randomness gradient smoke;
- record explicit connectivity diagnostics and finite-difference sensitivity;
- stop on nonfinite, disconnected, masked-zero, or variable-randomness
  evidence.
