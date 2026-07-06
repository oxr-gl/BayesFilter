# Phase 3 Row Result: Fixed SIR Forward Value Admission

metadata_date: 2026-07-06
status: VALUE_ADMITTED_WITH_EXPLICIT_NONCLAIMS
master_program: docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md
phase: 3
row_id: zhao_cui_spatial_sir_austria_j9_T20

## Question

Does the fixed spatial SIR row now have a same-target LEDH observed-data
likelihood value route under the amended 3D `sir_log_scale_theta` contract?

## Decision

Admitted for Phase 3 value execution and forward-contract identity only.

The row may proceed to Phase 4 as value-admitted for manual no-tape score
implementation work. The score remains blocked until the derivative of exactly
this executed scalar is implemented and checked.

## Evidence Components

| Component | Artifact | Role |
| --- | --- | --- |
| Existing N=10000 GPU/XLA value execution | `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-fixed-sir-value-ladder-N10000-2026-07-03.json` | Finite trusted-GPU SIR LEDH execution with target-density correction. |
| Current amended contract smoke | `docs/plans/ledh-phase3-fixed-sir-forward-contract-tiny-2026-07-06.json` | Confirms the current runner emits the Phase 2 forward contract and amended 3D theta metadata. |
| Admission tests | `tests/highdim/test_ledh_phase3_forward_admission.py` | Makes the old/new evidence boundary executable. |

## Existing N=10000 GPU/XLA Evidence

The July 3 artifact records:

- `primary_pass_5x_runtime_gate = true`
- `runtime_gate_applicable = true`
- `finite_output = true`
- `sir_semantics.row_id = zhao_cui_spatial_sir_austria_j9_T20`
- `sir_semantics.target_density_used_for_correction = true`
- `shape.num_particles = 10000`
- `shape.time_steps = 20`
- batch seeds `[81120,81121,81122,81123,81124]`

This artifact also records nonclaims including `not exact likelihood
correctness`, `not DPF gradient correctness`, and `not HMC/NUTS readiness`.

## Current Contract Smoke

The tiny CPU-hidden diagnostic run:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python \
  docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py \
  --device-scope cpu --device /CPU:0 --expect-device-kind cpu \
  --batch-seeds 81120 --num-particles 4 --time-steps 1 \
  --sinkhorn-iterations 1 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 4 --col-chunk-size 4 --particle-chunk-size 4 \
  --history-mode value-only --warmups 0 --repeats 1 \
  --dtype float32 --tf32-mode disabled \
  --output docs/plans/ledh-phase3-fixed-sir-forward-contract-tiny-2026-07-06.json \
  --markdown-output docs/plans/ledh-phase3-fixed-sir-forward-contract-tiny-2026-07-06.md
```

Result: passed as a tiny prefix diagnostic and emitted:

- `target_scalar = observed_data_log_likelihood_estimator`
- `target_output_tensor_field = log_likelihood`
- target density fields `transition_log_density`, `observation_log_density`
- proposal/flow fields `pre_flow_log_density`, `forward_log_det`,
  `proposal_observation_surface`
- correction formula
  `transition_log_density + observation_log_density - pre_flow_log_density + forward_log_det`
- theta contract:
  - `theta_coordinate_system = sir_log_scale_theta`
  - `theta_dimension = 3`
  - parameter order `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)`
  - truth theta `[0,0,0]`

This tiny CPU-hidden run is not production GPU evidence and is not score
evidence.

## Local Checks

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/test_ledh_score_memory_n10000.py::test_fixed_spatial_sir_ledh_full_row_score_remains_blocked -q
```

Result: `12 passed, 2 warnings`.

```text
python -m py_compile \
  docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py \
  tests/highdim/test_ledh_phase3_forward_admission.py
```

Result: passed.

```text
git diff --check -- \
  docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  docs/plans/bayesfilter-ledh-same-target-forward-score-phase3-lgssm-value-admission-result-2026-07-06.md \
  docs/plans/bayesfilter-ledh-same-target-forward-score-phase3-fixed-sir-forward-contract-blocker-result-2026-07-06.md \
  docs/plans/ledh-phase3-fixed-sir-forward-contract-tiny-2026-07-06.json \
  docs/plans/ledh-phase3-fixed-sir-forward-contract-tiny-2026-07-06.md
```

Result: passed.

## Boundary Safety

- The scoped parameterized-SIR diagnostic is not used for this admission.
- The fixed SIR score remains blocked.
- The log-scale theta surface is classified as a BayesFilter inference-theta
  extension over source-anchored fixed formulas, not as Zhao-Cui author-source
  free-theta faithfulness.
- Exact nonlinear likelihood correctness is not claimed from the old value
  artifact.
- HMC readiness, posterior correctness, scientific superiority, and fair
  runtime ranking are not claimed.
