# P8p Phase 3c Subplan: Observation-Noise Gradient Diagnostics

Date: 2026-06-19

Status: `DRAFT_EXECUTABLE`

## Phase Objective

Diagnose why `log_obs_noise_scale` remains the suspicious P8p SIR d18 gradient
component after Phase 3b.  Separate three explanations:

- non-orthogonal or collinear parameter geometry;
- finite-difference step or TF32 precision sensitivity;
- a direct observation-covariance gradient wiring problem.

This phase is diagnostic only.  It does not promote the target to HMC readiness.

## Entry Conditions

- Phase 3 central finite-difference result is blocked.
- Phase 3b per-seed Jacobian noise result exists.
- The P8p harness compiles after adding per-seed Jacobian output.

## Required Artifacts

- GPU/TF32 JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3c-observation-noise-diagnostic-gpu-tf32-2026-06-19.json`
- GPU/TF32-disabled JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3c-observation-noise-diagnostic-gpu-no-tf32-2026-06-19.json`
- Result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3c-observation-noise-diagnostic-result-2026-06-19.md`

## Required Checks

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py
git diff --check -- docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3c-*
```

Trusted GPU diagnostics:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py \
  --device-scope visible \
  --expect-device-kind gpu \
  --device /GPU:0 \
  --time-steps 3 \
  --num-particles 16 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P8p Phase 3c obs-noise diagnostic GPU TF32" \
  --transport-policy active-all \
  --sinkhorn-iterations 10 \
  --sinkhorn-epsilon 1.0 \
  --row-chunk-size 16 \
  --col-chunk-size 16 \
  --particle-chunk-size 16 \
  --dtype float32 \
  --tf32-mode enabled \
  --fd-step 0.0005 \
  --fd-step-ladder 0.01,0.005,0.001,0.0005,0.0001 \
  --diagnostic-components obs-noise \
  --repeat-evaluations 1 \
  --check-isolated-observation-noise \
  --check-theta-zero-p8j-parity \
  --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3c-observation-noise-diagnostic-gpu-tf32-2026-06-19.json
```

Repeat with `--tf32-mode disabled` and the no-TF32 output artifact.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the `log_obs_noise_scale` AD/FD mismatch explained by parameter geometry, finite-difference/precision sensitivity, or a direct observation-covariance gradient wiring problem? |
| Baseline/comparator | Phase 3 and Phase 3b tiny SIR d18 diagnostics. |
| Primary diagnostics | Observation-noise FD step ladder; isolated Gaussian observation log-density AD/FD ladder; seed gradient covariance/correlation. |
| Veto diagnostics | Nonfinite value, AD gradient, or FD; disconnected `log_obs_noise_scale`; missing trusted GPU placement; broken theta-zero P8j parity; categorical resampling. |
| Explanatory diagnostics | Residual divided by five-seed MC standard error, TF32 enabled/disabled differences, parameter seed-gradient correlations. |
| Not concluded | Phase 3 pass, stochastic PF marginal-gradient correctness, exact likelihood correctness, full-horizon stability, HMC/NUTS readiness, posterior convergence, production/default readiness. |

## Stop Conditions

Stop before Phase 4 if:

- isolated observation-noise AD/FD fails across the step ladder;
- full-route observation-noise mismatch persists without step/precision
  convergence;
- route guarantees fail;
- interpreting the mismatch requires changing the target or making scientific
  claims beyond this diagnostic.

## Handoff Conditions

If isolated observation-noise AD/FD passes but full-route mismatch persists,
the next action is to inspect transport/flow covariance-gradient routing.  If
both isolated and full-route ladders converge, Phase 3 may be amended with a
reviewed MC-noise-aware validation rule.
