# P82 N1000 Central FD Sanity Result

Date: 2026-06-25
Status: COMPLETE_CENTRAL_FD_SUPPORTS_REGRESSION_FD_FOR_RATE_ROWS

## Question

For N1000, do simple central FD slopes in the three raw theta directions look
closer to the stored manual/reverse-gradient gradients or to the existing
13-point regression-FD slopes?

## Decision Table

| Field | Result |
|---|---|
| Decision | The central ±0.001 FD sanity check supports the regression-FD rate rows, not the manual/reverse-gradient rate rows. |
| Primary criterion status | PASS: JSON reports `status=pass`, GPU-visible route, N1000, five seeds, same theta/Sinkhorn/transport policy/dtype/TF32 settings, raw basis, seven accepted offsets, finite objective values, and finite slopes. |
| Veto diagnostic status | PASS: no OOM, timeout, missing JSON, nonfinite value, `transport_ad_mode=full`, route metadata violation, or central-FD promotion claim. |
| Main uncertainty | Central FD is intentionally noisy and extracted from ±0.001 inside a 7-point accepted-offset run. It is a sanity check only; the 13-point regression remains the stronger FD estimate. |
| Next justified action | Treat the kappa/nu mismatch as a manual-gradient route issue candidate. Audit the manual rate-parameter derivative route and route-decompose transition/flow/transport contributions. |
| Not concluded | This does not prove FD is an oracle, prove posterior correctness, certify HMC/default readiness, or use Zhao-Cui as a comparator. |

## Artifacts

| Artifact | Path |
|---|---|
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p82-n1000-central-fd-sanity-plan-2026-06-25.md` |
| Central FD JSON | `docs/plans/bayesfilter-highdim-zhao-cui-p82-n1000-central-fd-sanity-2026-06-25.json` |
| Progress JSON | `docs/plans/bayesfilter-highdim-zhao-cui-p82-n1000-central-fd-sanity-progress-2026-06-25.json` |
| Memory sidecar | `docs/plans/bayesfilter-highdim-zhao-cui-p82-n1000-central-fd-sanity-memory-samples-2026-06-25.json` |
| P8R 13-point comparator | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-n1000-xla-chunk500-gpu-tf32-2026-06-24.json` |
| Older reverse-gradient diagnostic | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-n1000-gpu-tf32-2026-06-23.json` |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `97ad05d40676f3fd15a2a2b4d45034ebb657ed97` |
| Conda env | `/home/chakwong/anaconda3/envs/tf-gpu` |
| TensorFlow | `2.19.1` |
| Device | GPU-visible, `/GPU:0` |
| Shape | N1000, five seeds, T3, state dim 18, obs dim 9 |
| Theta | `log_kappa_scale=0.02`, `log_nu_scale=-0.01`, `log_obs_noise_scale=0.01` |
| Seeds | `81120,81121,81122,81123,81124` |
| Route | `ad_evaluation_mode=manual-reverse`, XLA compiler, streaming transport |
| Transport | `gradient_mode=manual_streaming_finite_sinkhorn_stopped_scale_keys`, `transport_ad_mode=stabilized`, row/col chunks 500, particle chunk 512 |
| Sinkhorn | 10 iterations, epsilon 1.0 |
| Offsets | `-3,-2,-1,0,1,2,3` with no trimming; central slope extracted from `-1,+1` only |
| Wall time | `2182.439273854019` seconds |
| Peak TensorFlow allocator memory | `1189542912` bytes |
| XLA compile/first-call timings | `345.81`, `384.12`, `439.71`, `394.48`, `383.41` seconds |

## Central FD Comparison

| Direction | Manual gradient in this run | Older reverse-gradient diagnostic | Central ±0.001 FD | 7-point OLS FD | P8R 13-point FD |
|---|---:|---:|---:|---:|---:|
| `log_kappa_scale` | `-157.2984161376953` | `-157.03306579589844` | `-263.2484310998861` | `-263.1707763671875` | `-263.2330322265625` |
| `log_nu_scale` | `70.63054656982422` | `70.12858581542969` | `105.07964588789089` | `105.09571838378906` | `105.13096618652344` |
| `log_obs_noise_scale` | `46.88983154296875` | `47.451133728027344` | `46.57745140097102` | `46.83712387084961` | `46.83678436279297` |

## Central FD Objective Points

| Direction | `f(theta - h e_i)` | `f(theta + h e_i)` | `h` |
|---|---:|---:|---:|
| `log_kappa_scale` | `-125.33058166503906` | `-125.8570785522461` | `0.0010000000474974513` |
| `log_nu_scale` | `-125.69807434082031` | `-125.4879150390625` | `0.0010000000474974513` |
| `log_obs_noise_scale` | `-125.63905334472656` | `-125.5458984375` | `0.0010000000474974513` |

## Interpretation

The simple central ±0.001 check reproduces the FD side for the two rate
parameters:

- kappa central FD is `-263.25`, while manual/reverse-gradient are about
  `-157`;
- nu central FD is `105.08`, while manual/reverse-gradient are about `70`;
- obs-noise remains close enough that the more stable 7-point and 13-point OLS
  estimates agree with the manual route within the earlier tolerance.

This makes the current pattern exceedingly unlikely to be a 13-point regression
artifact.  The next diagnostic should inspect the manual rate-parameter
derivative path, not the FD regression protocol.

## Checks

- `python -m json.tool` on central FD JSON, progress JSON, and memory sidecar:
  passed.
- Extraction script for central ±0.001 slopes and comparator values: passed.
- `git diff --check` on the central FD plan: passed.
