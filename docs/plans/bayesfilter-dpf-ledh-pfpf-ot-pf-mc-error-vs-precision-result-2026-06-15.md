# BayesFilter DPF LEDH-PFPF-OT PF MC Error vs Precision Result - 2026-06-15

## Question

Can we calculate the Monte Carlo error of the PF value and PF gradient from the
paired precision diagnostic, and compare FP32/TF32 precision drift to that PF
noise floor?

## Evidence Contract Check

- Baseline: FP64 `streaming_streaming_tensor` value and score across six
  independent PF seeds.
- Precision drift: same-seed FP32-no-TF32 and FP32+TF32 values/scores minus
  same-seed FP64 values/scores.
- Primary diagnostic: precision RMS error divided by FP64 seed-to-seed sample
  SD.
- Veto diagnostics: non-finite value/score, missing paired artifacts, or
  precision drift near/above one FP64 sample SD.
- Explanatory diagnostics: signed mean drift, max absolute drift, and score
  L2 ratios.
- Nonclaims: no HMC readiness claim, no posterior validity claim, no default
  precision-policy change, and no statistically supported ranking from six
  seeds.

The parent aggregate artifact reported `overall_passed: false` because each
TF32 child exceeded the child script's strict FP64 structural tolerance and
returned nonzero. The child JSON artifacts were still written and finite. For
this question, that tolerance failure is the measurement, not a reason to
discard the finite TF32 values. The aggregate harness was patched so future
MC-noise runs treat finite target artifacts as usable even when the child
strict-tolerance screen fails.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `70ab32644cedeb95d4b56e096448f3bb2c908763` |
| Command | `timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_pf_mc_error_vs_precision.py --device-scope visible --cuda-visible-devices 0 --device /GPU:0 --expect-device-kind gpu --num-seeds 6 --base-seed 20260615 --seed-stride 1009 --batch-size 1 --time-steps 5 --num-particles 32 --state-dim 4 --obs-dim 4 --transport-policy active-odd --sinkhorn-iterations 3 --row-chunk-size 16 --col-chunk-size 16 --particle-chunk-size 16 --child-timeout-seconds 180 --artifact-dir docs/benchmarks/experimental-batched-ledh-pfpf-ot-pf-mc-error-vs-precision-gpu0-b1-t5-np32-d4-m4-seeds6-children-2026-06-15 --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-pf-mc-error-vs-precision-gpu0-b1-t5-np32-d4-m4-seeds6-2026-06-15.json --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-pf-mc-error-vs-precision-gpu0-b1-t5-np32-d4-m4-seeds6-2026-06-15.md` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13`, TensorFlow `2.20.0` |
| GPU | `NVIDIA GeForce RTX 4080 SUPER`, CUDA device `/GPU:0`, driver `580.159.03` |
| Seeds | `20260615, 20261624, 20262633, 20263642, 20264651, 20265660` |
| Shape | `B=1, T=5, N=32, state_dim=4, obs_dim=4, parameter_dim=3` |
| Transport | `active-odd`, `sinkhorn_iterations=3`, row/col/particle chunks `16/16/16` |
| Main artifact | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-pf-mc-error-vs-precision-gpu0-b1-t5-np32-d4-m4-seeds6-2026-06-15.json` |
| Child artifacts | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-pf-mc-error-vs-precision-gpu0-b1-t5-np32-d4-m4-seeds6-children-2026-06-15/` |

## FP64 PF Monte Carlo Error Estimate

For this diagnostic, the single-run PF MC noise proxy is the FP64
seed-to-seed sample SD. The MC error of the six-seed mean is the sample SD
divided by `sqrt(6)`.

| Quantity | Mean | Sample SD | SE of 6-seed mean | Relative sample SD |
| --- | ---: | ---: | ---: | ---: |
| value | `3.9461303145` | `0.0200362968` | `0.0081797839` | `0.00507745` |
| score[0] | `-0.5671159316` | `0.0594481650` | `0.0242696117` | `0.104825` |
| score[1] | `-3.8484223261` | `0.0128803278` | `0.0052583718` | `0.00334691` |
| score[2] | `-5.9403616231` | `0.0062079331` | `0.0025343781` | `0.00104504` |

Score-vector norm diagnostics:

- `||mean score||_2 = 7.1006951134`
- `||component sample SD||_2 = 0.0611434837`
- `||component sample SD||_2 / ||mean score||_2 = 0.00861092`
- `||component SE||_2 / ||mean score||_2 = 0.00351539`

## Precision Drift Relative To PF MC Noise

| Precision arm | Value RMS error | Value RMS / value SD | Score RMS error by component | Score RMS / score SD by component | Max score ratio | Score L2 RMS / score-SD L2 |
| --- | ---: | ---: | --- | --- | ---: | ---: |
| FP32, TF32 disabled | `1.08223e-6` | `5.40133e-5` | `[6.75763e-8, 2.60257e-7, 5.21296e-7]` | `[1.13673e-6, 2.02058e-5, 8.39725e-5]` | `8.39725e-5` | `9.59313e-6` |
| FP32, TF32 enabled | `2.11529e-4` | `0.0105573` | `[6.94376e-5, 0.00371724, 0.00141984]` | `[0.00116804, 0.288598, 0.228714]` | `0.288598` | `0.0650892` |

Signed same-seed mean drift, useful only as an explanatory diagnostic:

| Precision arm | Value mean drift | Score mean drift |
| --- | ---: | --- |
| FP32, TF32 disabled | `1.07384e-6` | `[-6.06593e-8, 7.69015e-8, 4.41249e-7]` |
| FP32, TF32 enabled | `2.10167e-4` | `[-4.02342e-5, 0.00368225, 0.00138534]` |

## Decision Table

| Decision field | Status |
| --- | --- |
| Can we calculate PF MC error here? | Yes. FP64 seed-to-seed SD gives a focused practical MC noise proxy for this deterministic benchmark fixture. |
| Primary criterion | Passed descriptively. Both FP32-no-TF32 and TF32 precision drifts are below one FP64 PF sample SD for value and all score components. |
| Veto diagnostic status | No non-finite target values/scores. Parent aggregate failed only because TF32 violated strict FP64 tolerance, not because the target artifact was unusable. |
| Main uncertainty | Six seeds and a small `T=5,N=32,D=4` fixture. This is a noise-floor diagnostic, not a production uncertainty interval. |
| Next justified action | Run the same finite-artifact aggregation on a larger HMC-relevant fixture after the score path is made JIT-safe, then check HMC energy/acceptance diagnostics. |
| What is not concluded | TF32 is not yet promoted as a default; HMC correctness, posterior validity, and production-scale gradient behavior are not established. |

## Inference Status

| Evidence class | Interpretation |
| --- | --- |
| Hard veto screen | No finite-output veto fired for the target arm. |
| Statistically supported ranking | None. Six seeds are descriptive only. |
| Descriptive-only differences | FP32-no-TF32 drift is negligible relative to PF MC noise. TF32 value drift is about `1.06%` of value PF SD; TF32 score drift is about `6.51%` of score-SD L2, with max component ratio about `28.9%`. |
| Default-readiness | Not default-ready. The gradient path still needs a JIT-safe implementation and HMC-level energy/acceptance validation. |
| Next evidence needed | Larger-seed/larger-shape MC-noise comparison and downstream HMC diagnostics, especially whether TF32 drift creates persistent energy error or only small efficiency changes. |

## Interpretation

For the value, TF32 drift is tiny compared with PF MC variability in this
fixture: about `0.0106` PF sample SD. FP32 without TF32 is effectively
invisible at this scale.

For the gradient, FP32 without TF32 is also effectively invisible. TF32 is more
interesting: it is still below one PF sample SD in every score component, but
two score components have ratios around `0.23` to `0.29` of the FP64 PF
seed-to-seed SD. On the score-vector L2 diagnostic, TF32 drift is about `0.065`
of the FP64 PF score-SD vector norm.

This supports the user's framing: pointwise TF32 drift is not obviously
mathematically disqualifying when compared with the PF approximation noise
floor. The remaining question is not "is TF32 exactly FP64?", because it is not.
The right next question is whether TF32's deterministic arithmetic drift causes
systematic HMC energy/acceptance degradation at realistic shape and tuning. That
requires HMC-level diagnostics, not just pointwise loglik/score comparison.

## Post-Run Red-Team Note

- Strongest alternative explanation: this small fixture underestimates TF32
  accumulation error in longer time series, larger state dimension, sharper
  likelihoods, or more Sinkhorn iterations.
- Result that would overturn this interpretation: TF32 score drift near or
  above one PF MC SD on a realistic JIT-safe fixture, or HMC diagnostics showing
  persistent energy error, degraded acceptance, or biased accepted samples.
- Weakest evidence: only six seeds and no downstream HMC validation.
- Repair trigger: once the score path is JIT-safe, repeat this comparison at a
  larger `T,N,D` and pair it with HMC acceptance/energy diagnostics.
