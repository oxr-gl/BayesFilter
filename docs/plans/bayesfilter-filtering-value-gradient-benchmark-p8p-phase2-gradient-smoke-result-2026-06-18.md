# P8p Phase 2 Result: Fixed-Randomness Gradient Smoke Implementation

Date: 2026-06-18

Status: `PASS_PHASE2_TINY_GRADIENT_SMOKE`

## Phase Objective

Implement and smoke-test a P8p-specific parameterized SIR d18 gradient harness
for:

```text
theta = [log_kappa_scale, log_nu_scale, log_obs_noise_scale]
```

This phase tests a tiny fixed-randomness SIR d18 LEDH-PFPF-OT graph for finite
values and explicit per-theta connected gradients.  It is not full-horizon
adequacy or HMC readiness.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the tiny P8p parameterized SIR d18 fixed-randomness graph produce finite values and explicit connected gradients for all three theta components? |
| Baseline/comparator | Phase 1 theta-zero contract and current P8j fixed-parameter route at the same tiny shape. |
| Primary pass criterion | Theta-zero P8j tiny-shape parity checked and within declared tolerance; value finite; AD gradient finite; every theta component explicitly connected; no component exactly zero without reviewed structural explanation; repeated same-theta evaluation repeatable; same-randomness finite-difference sensitivity finite for each component; artifact proves fixed random streams, fixed resampling mask, relaxed Sinkhorn OT, and no categorical resampling; GPU placement trusted. |
| Veto diagnostics | Missing or failed theta-zero P8j parity; nonfinite value/gradient; disconnected theta component; masked zero-gradient success; stochastic categorical resampling; missing fixed-mask/relaxed-OT artifact fields; random streams vary across repeated theta; CPU fallback for GPU claim. |
| Not concluded | Full-horizon gradient correctness, stochastic PF marginal-gradient correctness, exact likelihood correctness, HMC/NUTS readiness, posterior convergence, production/default readiness, or filter ranking. |

## Implementation

Added:

- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`

The harness:

- keeps the P8j value-only harness intact;
- threads theta through `kappa`, `nu`, and observation covariance;
- keeps initial particles and stateless process noise fixed across theta;
- uses fixed resampling masks and relaxed Sinkhorn OT;
- checks theta-zero parity against the current tiny-shape P8j fixed route;
- records explicit per-theta connectivity diagnostics rather than relying on
  the zero-filled streaming score helper alone;
- emits JSON fields required by the Phase 2 subplan.

## Checks

Local checks:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py
git diff --check -- docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-*
```

Both passed.

Debug CPU-only smoke:

```bash
python docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py \
  --device-scope cpu \
  --expect-device-kind cpu \
  --device /CPU:0 \
  --time-steps 3 \
  --num-particles 8 \
  --batch-seeds 81120 \
  --theta 0,0,0 \
  --transport-policy active-all \
  --sinkhorn-iterations 10 \
  --sinkhorn-epsilon 1.0 \
  --row-chunk-size 8 \
  --col-chunk-size 8 \
  --particle-chunk-size 8 \
  --dtype float32 \
  --tf32-mode disabled \
  --fd-step 0.001 \
  --repeat-evaluations 2 \
  --check-theta-zero-p8j-parity \
  --output /tmp/p8p_phase2_cpu_smoke.json \
  --no-fail-on-veto
```

CPU debug status: passed.  This was implementation debugging evidence only.

Trusted GPU smoke:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py \
  --device-scope visible \
  --expect-device-kind gpu \
  --device /GPU:0 \
  --time-steps 3 \
  --num-particles 8 \
  --batch-seeds 81120 \
  --theta 0,0,0 \
  --transport-policy active-all \
  --sinkhorn-iterations 10 \
  --sinkhorn-epsilon 1.0 \
  --row-chunk-size 8 \
  --col-chunk-size 8 \
  --particle-chunk-size 8 \
  --dtype float32 \
  --tf32-mode enabled \
  --fd-step 0.001 \
  --repeat-evaluations 2 \
  --check-theta-zero-p8j-parity \
  --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase2-gradient-smoke-2026-06-18.json
```

Trusted GPU status: passed.

JSON gate validation:

```bash
python - <<'PY'
# validated required fields and gate booleans from the Phase 2 JSON
PY
```

Result: `P8P_PHASE2_JSON_PASS`.

## Trusted GPU Diagnostic Summary

Artifact:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase2-gradient-smoke-2026-06-18.json`

Key fields:

| Field | Value |
| --- | --- |
| Primary pass | `true` |
| Device | `/GPU:0` |
| Output devices | GPU tensors |
| Shape | `B=1`, `T=3`, `N=8`, `D=18`, `M=9`, `P=3` |
| Theta | `[0.0, 0.0, 0.0]` |
| Theta-zero P8j parity checked | `true` |
| Theta-zero max abs value delta | `0.0` |
| Value finite | `true` |
| Gradient finite | `true` |
| Connectivity | all three theta components connected |
| Gradient | `[-215.0961151123047, 81.67037200927734, 35.681541442871094]` |
| Gradient norm | `232.8294677734375` |
| Repeat value max abs delta | `0.0` |
| Repeat gradient max abs delta | `0.0` |
| Finite differences finite | `true` |
| Relaxed Sinkhorn OT used | `true` |
| Categorical resampling used | `false` |
| Random streams fixed across theta | `true` |
| Resampling mask fixed | `true` |

Finite-difference diagnostics:

| Parameter | Central difference |
| --- | ---: |
| `log_kappa_scale` | `-212.20396423339844` |
| `log_nu_scale` | `86.98271942138672` |
| `log_obs_noise_scale` | `36.23199462890625` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Pass Phase 2 tiny gradient smoke. | Passed on trusted GPU. | No Phase 2 veto fired. | This is a tiny `T=3`, `N=8`, one-seed smoke; FD residuals are only sensitivity diagnostics and not a proof of stochastic PF score correctness. | Proceed to Phase 3 central finite-difference validation with a more deliberate tolerance and artifact contract. | No full-horizon gradient correctness, stochastic PF marginal-gradient correctness, exact likelihood correctness, HMC/NUTS readiness, posterior convergence, production/default readiness, or filter ranking. |

## Post-Run Red Team

Strongest alternative explanation:

- The graph can be connected and finite on a tiny fixed-randomness target while
  still failing at longer horizon, larger particles, different precision, or
  under HMC dynamics.

What would overturn this result:

- A reviewed rerun showing theta-zero parity failure, disconnected theta
  components, nonfinite gradients, variable random streams, categorical
  resampling, or silent CPU fallback for the GPU claim.

Weakest part of evidence:

- The finite-difference diagnostic is close in sign and scale but not yet a
  calibrated finite-difference validation gate.  That is Phase 3.

## Handoff To Phase 3

Phase 3 must:

- use the same P8p harness;
- focus on central finite-difference validation with explicit tolerances;
- use fixed random streams and theta-zero parity checks;
- keep finite differences as a computational diagnostic, not a stochastic PF
  score proof;
- write a Phase 3 result before any full-horizon gradient probe.
