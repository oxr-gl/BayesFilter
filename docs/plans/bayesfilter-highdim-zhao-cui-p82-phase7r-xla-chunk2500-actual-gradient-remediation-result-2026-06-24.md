# P82 Phase 7R Result: XLA Chunk2500 Actual-Gradient Remediation

status: COMPLETE_PASSED_READY_FOR_P8R_SUBPLAN_REVIEW
date: 2026-06-24
phase: P7R-XLA-CHUNK2500-ACTUAL-GRADIENT-REMEDIATION

## Question

Can the reviewed manual score route produce finite five-seed SIR d18 actual
gradients at N10000 under GPU/TF32 with XLA and chunk `2500 x 2500`, without
the known-bad full-AD route?

## Decision

Yes.  P7R produced the required N10000 five-seed actual-gradient JSON with
GPU-visible outputs, finite objective, finite gradient components, finite seed
MCSE, `manual-reverse` XLA metadata, and the expected streaming transport route.

This clears the old P7 blocker for purposes of moving to P8R.  It does not
claim FD agreement or scientific correctness.

## Decision Table

| Field | Result |
|---|---|
| Decision | P7R passes and may hand off to P8R governed FD consistency. |
| Primary criterion status | PASS: JSON reports `status=pass`, `primary_pass=true`, GPU output devices, five seeds, `N=10000`, `seed_microbatch_size=1`, `ad_evaluation_mode=manual-reverse`, `compiler.mode=xla`, `jit_compile=true`, streaming transport, manual finite Sinkhorn gradient mode, `transport_ad_mode=stabilized`, chunks `2500/2500/512`, finite objective, finite gradients, and finite seed MCSE. |
| Veto diagnostic status | PASS: no FD launched, no `transport_ad_mode=full`, no timeout/OOM, no missing artifact, and no nonfinite objective/gradient/MCSE. |
| Main uncertainty | The run spent most wall time in repeated XLA compile/retrace across seed microbatches; this is a performance issue, not a P7R validity blocker. |
| Next justified action | Draft/review P8R against the P7R JSON path and then run the governed N1000 five-seed 13-point FD comparison if P8R review passes. |
| Not concluded | FD agreement, posterior correctness, HMC/default readiness, scientific superiority, calibrated uncertainty, or production readiness. |

## Artifact Summary

| Artifact | Path |
|---|---|
| P7R subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-xla-chunk2500-actual-gradient-remediation-subplan-2026-06-24.md` |
| P7R JSON | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-actual-gradient-n10000-xla-chunk2500-gpu-tf32-2026-06-24.json` |
| P7R progress JSON | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-actual-gradient-n10000-xla-chunk2500-progress-2026-06-24.json` |
| P7R memory sidecar | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-actual-gradient-n10000-xla-chunk2500-memory-samples-2026-06-24.json` |
| Chunk-sizing reset memo | `docs/plans/bayesfilter-ledh-pfpf-ot-n10000-chunk-sizing-reset-memo-2026-06-24.md` |

## Run Manifest

| Field | Value |
|---|---|
| Command | P7R command from subplan, run with trusted GPU permissions. |
| Git commit recorded by benchmark | `97ad05d40676f3fd15a2a2b4d45034ebb657ed97` |
| Host | `DESKTOP-RF1Q5IJ` |
| TensorFlow | `2.19.1` |
| Device | `/GPU:0`, NVIDIA GeForce RTX 4080 SUPER |
| Seeds | `81120,81121,81122,81123,81124` |
| Shape | `N=10000`, `T=3`, `state_dim=18`, `obs_dim=9`, `parameter_dim=3` |
| Precision | `float32`, TF32 enabled |
| AD route | `manual-reverse`, `manual_reverse_compiler=xla` |
| Transport | streaming, `manual_streaming_finite_sinkhorn_stopped_scale_keys`, `transport_ad_mode=stabilized`, `sinkhorn_iterations=10`, `sinkhorn_epsilon=1.0`, chunks `2500/2500/512` |
| Wall time | `2026.6537902009732` seconds |
| TF allocator peak | `0.3189578056335449` GiB |

## Actual Gradient Result

| Parameter | Mean gradient | Seed SD | Seed SE |
|---|---:|---:|---:|
| `log_kappa_scale` | `-156.6765899658203` | `11.319337844848633` | `5.062162399291992` |
| `log_nu_scale` | `70.43897247314453` | `2.6886048316955566` | `1.2023807764053345` |
| `log_obs_noise_scale` | `46.97493362426758` | `0.08519520610570908` | `0.038100458681583405` |

Per-seed gradient contributions:

| Seed | `log_kappa_scale` | `log_nu_scale` | `log_obs_noise_scale` |
|---:|---:|---:|---:|
| 81120 | `-142.94125366210938` | `67.23486328125` | `47.04758834838867` |
| 81121 | `-149.0147705078125` | `68.3528823852539` | `47.03822708129883` |
| 81122 | `-166.98550415039062` | `72.87738800048828` | `46.874595642089844` |
| 81123 | `-169.19918823242188` | `73.32843780517578` | `46.889869689941406` |
| 81124 | `-155.24217224121094` | `70.40130615234375` | `47.024375915527344` |

## Compiler / Runtime Notes

P7R succeeded on the memory axis that blocked old P7.  TensorFlow allocator
peak was only about `0.319` GiB.

The cost was repeated XLA compilation/retracing across seed microbatch
contexts.  Compile plus first call timings were:

```text
[361.10041873998125, 400.70206240200787, 429.63548234599875, 407.8259952100052, 404.0149232200056]
```

Warm-call timings by context were:

```text
[[2.013194803002989], [1.933327926992206], [2.0409954299975652], [12.8699653520016], [2.2520743870118167]]
```

This should be treated as a performance follow-up, not a reason to block P8R.

## Checks

- `CUDA_VISIBLE_DEVICES=-1 /home/chakwong/anaconda3/envs/tf-gpu/bin/python -m pytest tests/highdim/test_p82_regression_fd_harness_protocol.py -q`: `16 passed, 2 warnings`.
- `CUDA_VISIBLE_DEVICES=-1 /home/chakwong/anaconda3/envs/tf-gpu/bin/python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`: passed.
- `git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py tests/highdim/test_p82_regression_fd_harness_protocol.py docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-xla-chunk2500-actual-gradient-remediation-subplan-2026-06-24.md`: passed.
- Trusted `nvidia-smi`: GPU visible.
- Trusted TensorFlow GPU probe: TensorFlow `2.19.1`, GPU visible.
- P7R JSON contract validation script: passed.
- `python -m json.tool` on P7R JSON, progress JSON, and memory sidecar: passed.

## Non-Claims

P7R does not claim FD agreement, P82 validation, posterior correctness,
HMC/default readiness, production readiness, scientific superiority, or
Zhao-Cui comparator readiness.

## Handoff

P8R may now be drafted/reviewed.  It must consume:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-actual-gradient-n10000-xla-chunk2500-gpu-tf32-2026-06-24.json
```

It must not use the old blocked P7 path.
