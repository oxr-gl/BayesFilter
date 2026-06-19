# P8p Phase 3i Result: Transport Stop-Gradient Ablation

Date: 2026-06-19

Status: `CLOSED_DIAGNOSTIC_FULL_MODE_PASSES_LOCAL_GATE`

## Question

Which stopped-gradient component explains the active transport AD/FD mismatch
for the parameterized SIR d18 LEDH-PFPF-OT diagnostic?

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Localize the active transport AD/FD mismatch under dense active transport. |
| Baseline/comparator | Phase 3h dense `stabilized` transport. |
| Primary criterion | Directional AD/FD agreement with usable 9-point regression slope plateaus in the semantic-orthogonal basis. |
| Veto diagnostics | Nonfinite objective/gradient/slope, missing GPU placement, TF32 disabled, missing artifact, or no usable slope plateau. |
| Explanatory diagnostics | Per-mode gradient, seed-gradient covariance/correlation, adaptive steps, objective line values, and per-direction residuals. |
| Not concluded | HMC/NUTS readiness, full-horizon stability, exact likelihood correctness, posterior validity, production/default readiness, or leaderboard ranking. |
| Preserved artifacts | Per-mode JSON outputs listed below. |

## Artifacts

| Mode | Artifact |
| --- | --- |
| `stabilized` baseline | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3h-dense-transport-ad-contract-n64-gpu-tf32-2026-06-19.json` |
| `diff-scale` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3i-transport-ad-diff-scale-n64-gpu-tf32-2026-06-19.json` |
| `diff-keys` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3i-transport-ad-diff-keys-n64-gpu-tf32-2026-06-19.json` |
| `diff-potentials` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3i-transport-ad-diff-potentials-n64-gpu-tf32-2026-06-19.json` |
| `full` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3i-transport-ad-full-n64-gpu-tf32-2026-06-19.json` |

All runs used trusted GPU execution on `/GPU:0`, TensorFlow 2.19.1, float32
with TF32 enabled, `T=3`, `N=64`, five fixed seeds
`81120,81121,81122,81123,81124`, dense transport plan mode, active-all
transport, Sinkhorn epsilon `1.0`, Sinkhorn iterations `10`, and 9-point
ordinary least squares finite-difference lines.

## Mode Comparison

| Mode | Gradient `(log_kappa, log_nu, log_obs_noise)` | Directional AD/FD result |
| --- | --- | --- |
| `stabilized` | `(-192.4062, 80.9372, 47.5070)` | Fails. Stable FD slopes but large AD gaps: rho about `+1.95`, tau about `-8.1` to `-8.8`, omega about `-1.8` to `-2.2`. |
| `diff-scale` | `(-263.3574, 105.1482, 46.4131)` | Partial. Rho and omega mostly align, but tau has no usable plateau: slopes `32.8804, 13.7578, 6.0183` versus AD `2.3726`. |
| `diff-keys` | `(-263.2769, 105.1616, 46.4159)` | Partial. Rho and omega mostly align, but tau still narrows from `12.2278` to `7.5078` versus AD `6.9501`; this is not a clean close. |
| `diff-potentials` | `(-203.5673, 84.3286, 47.3649)` | Fails. Rho and tau retain stable FD slopes but large AD gaps; omega is close. |
| `full` | `(-263.1447, 105.1307, 46.4017)` | Passes this local diagnostic. Rho slopes `-57.6018, -57.9043, -58.0358` versus AD `-57.6938`; tau slopes `18.7392, 18.3903, 17.6307` versus AD `18.3065`; omega slopes `-60.1683, -60.4279, -60.3241` versus AD `-60.5091`. |

## Interpretation

The failure is not explained by dense-vs-streaming chunking, and it is not
repaired by differentiating only one stopped component.  The smallest tested
contract that closes the local Phase 3i gate is the combined `full` transport
AD mode: differentiable scale/centering, differentiable Sinkhorn cost keys, and
differentiable converged potentials.

This strongly suggests the previous active transport gradient mismatch came
from an inconsistent stabilized surrogate-gradient contract: the forward value
was computed with active transport, while the AD path omitted enough transport
dependence that the gradient no longer matched local finite-difference slopes.

The result does not prove that `full` should become the default.  It only says
that, at this local SIR d18 checkpoint, the fully differentiable transport
contract is the first tested AD contract whose gradient agrees with regression
finite differences.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Use `full` as the candidate transport AD contract for the next validation phase. | Passed locally at `T=3`, `N=64`, active-all, dense plan, TF32 enabled. | No nonfinite values; GPU placement present; TF32 enabled; artifacts written. | Whether the full AD contract remains stable and performant under streaming transport, larger `N`, longer horizon, and HMC-style repeated gradients. | Run a focused Phase 3j validation of `transport_ad_mode=full`: streaming-vs-dense parity, higher-particle smoke, and targeted gradient regression with the same semantic-orthogonal FD protocol. | No HMC/NUTS readiness, no posterior validity, no leaderboard claim, no production/default promotion. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `9bcad31f0d9b21731b3915083d86834b43730f51` |
| Host | `DESKTOP-RF1Q5IJ` |
| Device | `/GPU:0`, NVIDIA GeForce RTX 4080 SUPER reported by TensorFlow logical GPU placement |
| Environment | Python 3.11.14, TensorFlow 2.19.1 |
| Precision | float32, TF32 enabled |
| Seeds | `81120,81121,81122,81123,81124` |
| State/observation dimension | SIR d18, obs dim 9 |
| Time steps / particles | `T=3`, `N=64` |
| Transport settings | active-all, dense, Sinkhorn epsilon `1.0`, iterations `10`, row/col/particle chunks `64` |
| FD protocol | Semantic-orthogonal basis, 9 offsets `-4..4`, adaptive base-step factors `1.0,0.5,0.25`, target objective delta `0.15` |
| Wall times | stabilized `109.97s`, diff-scale `106.54s`, diff-keys `105.44s`, diff-potentials `131.18s`, full `134.53s` |

## Close Conditions

- Required Phase 3i JSON artifacts exist.
- The diagnostic ladder was completed through `full`.
- The default transport AD mode remains `stabilized`; Phase 3i made no
  production/default promotion.
- Next phase should validate `full` in the operational streaming path before
  using it for HMC-facing conclusions.

## Boundary Notes

- This is DPF/SIR d18 work only.
- This is not Zhao-Cui source-faithfulness evidence.
- This is not a monograph rewrite artifact.
- This result does not authorize crossing model-file, funding, product,
  runtime, or scientific-claim boundaries.
