# P82 Active Transport Contract Diagnostic Result

Date: 2026-06-26

## Question

Why do the P82 active-all SIR LEDH-PFPF-OT diagnostics show manual/reverse
gradients around `[-157, 70, 47]`, while central and 13-point finite
differences give approximately `[-263, 105, 46.8]`?

## Decision Table

| Field | Result |
|---|---|
| Decision | The leading hypothesis is an active-transport stopped-geometry gradient contract mismatch. |
| Primary criterion status | PASS: a small T-ladder reproduces the mismatch only when active transport feeds future steps. |
| Veto diagnostic status | PASS: no `transport_ad_mode=full`, no Zhao-Cui comparator/oracle use, and CPU-only diagnostics were deliberately small local checks. |
| Main uncertainty | These are discriminating diagnostics, not a repaired implementation or a full production proof. |
| Next justified action | Audit and decide the intended gradient contract for active transport: stopped-key surrogate gradient versus finite-difference gradient of the recomputed transport map. |
| Not concluded | No HMC readiness claim, no posterior correctness claim, no FD-as-oracle claim, no broad LEDH correctness claim. |

## Evidence Contract

The baseline question was whether the large kappa/nu discrepancy is caused by
the SIR transition derivative, the one-step LEDH primitive, or active transport
feeding future particles.  The primary discriminator was whether the
manual-versus-FD mismatch appears at `T=1` or only after transported particles
become ancestors for later time steps.  Diagnostics are explanatory only.

All runs below were deliberate CPU-only local diagnostics with
`CUDA_VISIBLE_DEVICES=-1`; they are not GPU performance evidence.

## T-Ladder Result

Command shape:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp TF_CPP_MIN_LOG_LEVEL=2 python - <<'PY'
# imported docs.benchmarks.benchmark_p8p_parameterized_sir_gradient
# compared manual reverse score to central FD at theta [0.02, -0.01, 0.01]
# for N=64, seeds 81120..81124, T=1,2,3, active-all and no-resampling
PY
```

| Policy | T | Manual gradient | Central FD | FD minus manual |
|---|---:|---:|---:|---:|
| active-all | 1 | `[-9.5703, 3.5054, 4.6988]` | `[-9.5673, 3.5057, 4.6997]` | `[0.0030, 0.0003, 0.0010]` |
| active-all | 2 | `[-37.3474, 14.1829, 4.9730]` | `[-38.8336, 14.6065, 4.9820]` | `[-1.4863, 0.4235, 0.0090]` |
| active-all | 3 | `[-205.2538, 84.6428, 47.3322]` | `[-263.1416, 105.3543, 46.5431]` | `[-57.8878, 20.7115, -0.7890]` |
| no-resampling | 1 | `[-9.5703, 3.5054, 4.6988]` | `[-9.5673, 3.5057, 4.6997]` | `[0.0030, 0.0003, 0.0010]` |
| no-resampling | 2 | `[-35.2167, 13.2270, 3.9050]` | `[-35.2173, 13.2256, 3.9063]` | `[-0.0006, -0.0015, 0.0012]` |
| no-resampling | 3 | `[-218.4986, 87.0989, 35.5406]` | `[-218.5059, 87.0972, 35.5415]` | `[-0.0072, -0.0018, 0.0010]` |

Interpretation: the discrepancy is absent at `T=1`, appears under active-all at
`T=2`, and becomes large under active-all at `T=3`.  The same local setup
matches under no-resampling through `T=3`.  This strongly points to active
transport feeding future particles rather than a standalone SIR transition
VJP, one-step LEDH flow, or observation-noise path.

## Local Transport VJP Check

Command shape:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp TF_CPP_MIN_LOG_LEVEL=2 python - <<'PY'
# built a small B=2, N=16, D=3 transport problem
# compared manual stopped-key transport VJP, autodiff of the same surrogate,
# and finite difference of the recomputed transport map
PY
```

| Quantity | Value |
|---|---:|
| Manual stopped-key directional derivative | `-1.4269537925720215` |
| Autodiff stopped-key directional derivative | `-1.4269537925720215` |
| FD recomputed-transport directional derivative | `-1.0449886322021484` |
| FD minus manual | `0.38196516036987305` |
| Autodiff minus manual | `0.0` |

Interpretation: manual transport VJP and autodiff agree exactly for the
stopped-key surrogate contract, while FD of the recomputed transport map differs.
This matches the full-filter symptom: manual/reverse agree with each other, but
finite differences see a different derivative once transport affects later
states.

## SIR Transition VJP Control

Command shape:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp TF_CPP_MIN_LOG_LEVEL=2 python - <<'PY'
# compared _sir_transition_mean_vjp_tf against
# ParameterizedZhaoCuiSIRSSM.transition_mean_parameter_jacobian
PY
```

| Quantity | Value |
|---|---:|
| Transition mean max absolute delta versus model route | `6.103515625e-05` |
| Parameter-score max absolute delta versus analytic Jacobian | `1.1444091796875e-05` |

Interpretation: the manual SIR transition VJP agrees with the implemented
analytic transition-mean parameter Jacobian to float32 tolerance.  This demotes
the RK4/SIR transition derivative as a root cause for the large active-all
discrepancy.

## Ranked Hypotheses After Diagnostics

1. Active transport stopped-geometry contract mismatch.  The implementation
   differentiates a stopped-key/stopped-scale surrogate, while FD perturbs theta
   and recomputes the transport geometry.
2. Transport-origin cotangents are being reported as transition-mean channels
   because transported particles become future ancestors.  The decomposition is
   a landing-location diagnostic, not necessarily the origin of the error.
3. LEDH flow `prior_means` contract remains relevant but is no longer the top
   root-cause candidate by itself, because the discrepancy is absent at `T=1`.
4. SIR transition VJP/RK4 analytical derivative is unlikely as the primary
   cause, given the analytic-Jacobian control check.
5. Clamp nonsmoothness remains a secondary caveat, but the no-resampling match
   and active-only onset make it less likely to explain the main discrepancy.

## Next Action

Decide and document the intended active-transport gradient contract:

- If the target is the stopped-key surrogate gradient, then FD diagnostics must
  compare against a surrogate FD that holds transport geometry fixed, not against
  recomputed-geometry FD.
- If the target is the recomputed transport-map derivative, the manual transport
  VJP must include the missing center/scale/key/epsilon-start dependencies, or
  the route must stop claiming agreement with recomputed FD.
