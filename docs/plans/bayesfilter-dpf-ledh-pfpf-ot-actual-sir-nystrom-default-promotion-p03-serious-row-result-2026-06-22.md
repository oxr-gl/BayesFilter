# Actual-SIR Nystrom Default-Promotion P03 Serious Row Result

Date: 2026-06-22

Status: `PASS_ADVANCE_TO_REPLICATED_LADDER`

## Question

Does fixed-rank Nystrom pass the first default-promotion-relevant actual-SIR d18
row against the current streaming TF32 route on the same callbacks, seeds,
dtype, TF32 state, and physical GPU?

## Artifacts

- Runbook: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-visible-gated-execution-runbook-2026-06-22.md`
- P03 JSON: `docs/benchmarks/actual-sir-nystrom-default-promotion-p03-serious-b5-t20-n1024-2026-06-22.json`
- P03 Markdown: `docs/benchmarks/actual-sir-nystrom-default-promotion-p03-serious-b5-t20-n1024-2026-06-22.md`

## Command

```bash
timeout 3600 python docs/benchmarks/benchmark_actual_sir_nystrom_default_promotion.py --route both --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 1024 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 0 --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu 0 --gpu-selection-note 'GPU1 unavailable for P03: 30799 MiB used and 3 percent utilization; fallback to GPU0 with 1266 MiB used and 31 percent utilization' --phase-id ACTUAL-SIR-NYSTROM-P03-SERIOUS-B5-T20-N1024 --quiet --output docs/benchmarks/actual-sir-nystrom-default-promotion-p03-serious-b5-t20-n1024-2026-06-22.json --markdown-output docs/benchmarks/actual-sir-nystrom-default-promotion-p03-serious-b5-t20-n1024-2026-06-22.md
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit in artifact | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Environment | Trusted/elevated GPU context |
| GPU preflight | GPU0: 1266 MiB, 31%; GPU1: 30799 MiB, 3% |
| Selected GPU | Physical GPU0 fallback; GPU1 was unsuitable due to memory pressure |
| Artifact selected GPU | GPU0, UUID `GPU-a008e90f-259e-df57-7988-63b6831fff68` |
| TensorFlow version | `2.19.0` |
| TF32 recorded | `True` |
| Serious model | `zhao_cui_spatial_sir_austria_j9_T20` |
| Shape | `B=5,T=20,N=1024,D=18,M=9` |
| Seeds | `81120,81121,81122,81123,81124` |
| Rank | `32` |
| Transport policy | `active-all` |
| Wall time | `1336.6070244549774` seconds |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to replicated actual-SIR ladder | Passed full P03 serious row with paired comparability | No hard vetoes; actual-SIR semantics, TF32, GPU, route-fired, ESS, logsumexp, and residual gates passed | One physical GPU fallback run, one five-seed batch, no uncertainty analysis | Run P05 replicated ladder with predeclared rows and uncertainty-aware interpretation | No default readiness, no statistical ranking, no posterior correctness, no HMC readiness |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS`; P03 JSON reports `hard_vetoes=[]` |
| Actual-SIR semantics | `PASS`; row id `zhao_cui_spatial_sir_austria_j9_T20`, `D=18`, `M=9` |
| Paired comparability | `PASS`; all deltas below thresholds |
| Descriptive timing | Nystrom warm median was lower in this row; this is descriptive only |
| Statistically supported ranking | `NO`; no replication/uncertainty model yet |
| Default-readiness | `NO`; P03 is necessary but not sufficient |
| Next evidence needed | Replicated actual-SIR ladder, then stress and gradient/HMC gates before default promotion |

## Route Summary

| Route | Status | Invocations | Warm median seconds | First call seconds | ESS fraction min | Final logsumexp residual | Row residual | Column residual |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `streaming` | `PASS` | `20` | `489.2099703249987` | `638.6572500199545` | `0.6536898016929626` | `0.0` | `7.641315460205078e-05` | `0.0` |
| `nystrom` | `PASS` | `20` | `104.42240847204812` | `104.30032387399115` | `0.6536898016929626` | `0.0` | `9.834766387939453e-05` | `4.76837158203125e-07` |

## Paired Comparability

| Metric | Value | Threshold |
| --- | ---: | ---: |
| Log-likelihood max absolute delta | `4.87078857421875` | `<= 10.0` |
| Log-likelihood mean absolute delta | `2.5714111328125` | `<= 5.0` |
| Filtered mean relative L2 | `0.0014205765845258954` | `<= 0.20` unless RMS passes |
| Filtered mean RMS | `0.2420245515078464` | `<= 2.5` unless relative L2 passes |
| Filtered variance relative L2 | `0.015914764790818416` | `<= 0.75` unless RMS passes |
| Filtered variance RMS | `0.020333283615234184` | `<= 25.0` unless relative L2 passes |
| Final particle mean relative L2 | `0.004265115345192201` | `<= 0.20` unless absolute L2 passes |
| Final particle mean absolute L2 | `1.1539638091744444` | `<= 25.0` unless relative L2 passes |
| Warm median streaming/Nystrom | `4.68491368359839` | descriptive only |

## Interpretation

Nystrom passed the first serious actual-SIR row.  This is a meaningful gate:
the same actual-SIR workload where the current low-rank route stopped as
`TUNING_REQUIRED` now has a Nystrom artifact with no hard vetoes and passing
paired comparability.

The result supports advancing to a replicated actual-SIR ladder.  It does not
support default promotion by itself.  Timing and memory remain descriptive
until the replicated ladder and uncertainty plan are run.

## Post-Run Red Team

| Check | Assessment |
| --- | --- |
| Strongest alternative explanation | This one GPU0 run may be favorable due to allocator/device state or this one seed batch; replication could weaken the timing signal or expose drift at larger `N`. |
| What would overturn the conclusion | Replicated rows fail comparability, Nystrom residuals, ESS/log-weight gates, or show no stable operational advantage. |
| Weakest evidence | GPU1 was unavailable, so this row ran on fallback GPU0; runtime is not yet uncertainty-supported. |

## Next Step

Skip P04 repair.  Continue to P05 replicated ladder with GPU1 preferred:
`N=[1024,2048,4096,8192]` if feasible, or a shorter reviewed ladder if GPU time
is constrained.  Keep ranking/default language blocked until uncertainty-aware
evidence is available.
