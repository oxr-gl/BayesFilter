# Actual-SIR Nystrom Default-Promotion Pilot Result

Date: 2026-06-22

Status: `ACTUAL_SIR_NYSTROM_P02_PASSED_READY_FOR_SERIOUS_ROW`

## Question

Can the fixed-rank Nystrom route pass actual-SIR d18 validity and paired
comparability against the current streaming TF32 route on the same serious SIR
workload?

## Artifacts

- Plan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-plan-2026-06-22.md`
- Harness: `docs/benchmarks/benchmark_actual_sir_nystrom_default_promotion.py`
- Tests: `tests/test_actual_sir_nystrom_default_promotion.py`
- P02 GPU pilot JSON: `docs/benchmarks/actual-sir-nystrom-default-promotion-p02-gpu-pilot-2026-06-22.json`
- P02 GPU pilot Markdown: `docs/benchmarks/actual-sir-nystrom-default-promotion-p02-gpu-pilot-2026-06-22.md`

## Commands

```bash
python -m py_compile docs/benchmarks/benchmark_actual_sir_nystrom_default_promotion.py tests/test_actual_sir_nystrom_default_promotion.py
pytest -q tests/test_actual_sir_nystrom_default_promotion.py
nvidia-smi --query-gpu=index,memory.used,utilization.gpu,name --format=csv,noheader,nounits
timeout 1200 python docs/benchmarks/benchmark_actual_sir_nystrom_default_promotion.py --route both --batch-seeds 81120 --time-steps 3 --num-particles 128 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 0 --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu 0 --gpu-selection-note 'GPU1 unavailable for pilot: 30799 MiB used and 15 percent utilization; fallback to GPU0 with 1239 MiB used and 34 percent utilization' --phase-id ACTUAL-SIR-NYSTROM-P02-GPU0-FALLBACK-B1-T3-N128 --quiet --output docs/benchmarks/actual-sir-nystrom-default-promotion-p02-gpu-pilot-2026-06-22.json --markdown-output docs/benchmarks/actual-sir-nystrom-default-promotion-p02-gpu-pilot-2026-06-22.md
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `9e905273fa9219fa5d2d9ca670212cb86a31aeb8` |
| Environment | Trusted/elevated GPU context |
| GPU preflight | GPU0: 1239 MiB, 34%; GPU1: 30799 MiB, 15% |
| Selected GPU | Physical GPU0 fallback; GPU1 was unsuitable |
| Recorded selected GPU in artifact | GPU0, UUID `GPU-a008e90f-259e-df57-7988-63b6831fff68` |
| TensorFlow version | `2.19.0` |
| TF32 recorded | `True` |
| Serious model | `zhao_cui_spatial_sir_austria_j9_T20` |
| Shape | `B=1,T=3,N=128,D=18,M=9` |
| Seed | `81120` |
| Rank | `32` |
| Transport policy | `active-all` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Advance Nystrom to the first serious actual-SIR row | P02 GPU pilot passed both routes and paired comparability | No hard vetoes; SIR semantics passed; GPU/TF32 evidence present | One seed, short horizon, fallback GPU0, no replication | Run `B=5,T=20,N=1024` actual-SIR row with GPU1 preferred, same thresholds, and compiled/diagnostic timing separation if needed | No default readiness, no posterior correctness, no HMC readiness, no statistical ranking |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS`; JSON reports `hard_vetoes=[]` |
| Actual-SIR semantics | `PASS`; row id `zhao_cui_spatial_sir_austria_j9_T20`, `D=18`, `M=9` |
| Paired comparability | `PASS` under predeclared thresholds |
| Statistical ranking | `NO`; single short pilot only |
| Default-readiness | `NO`; this is the gate before the first serious row |
| Next evidence needed | Full `B=5,T=20,N=1024` actual-SIR paired row, then replicated ladder if it passes |

## Row Summary

| Route | Status | Warm median seconds | First call seconds | ESS fraction min | Final logsumexp residual | Row residual | Column residual |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `streaming` | `PASS` | `3.5849189849104732` | `6.972060945117846` | `0.677178680896759` | `0.0` | `3.457069396972656e-05` | `0.0` |
| `nystrom` | `PASS` | `1.0852115859743208` | `1.9543134530540556` | `0.677178680896759` | `0.0` | `9.739398956298828e-05` | `2.384185791015625e-07` |

## Paired Comparability

| Metric | Value | Threshold |
| --- | ---: | ---: |
| Log-likelihood max absolute delta | `0.00679779052734375` | `<= 10.0` |
| Log-likelihood mean absolute delta | `0.00679779052734375` | `<= 5.0` |
| Filtered mean relative L2 | `3.9791576582646976e-05` | `<= 0.20` unless RMS passes |
| Filtered mean RMS | `0.012853146001979234` | `<= 2.5` unless relative L2 passes |
| Filtered variance relative L2 | `0.04104982135193494` | `<= 0.75` unless RMS passes |
| Filtered variance RMS | `0.09175880070111714` | `<= 25.0` unless relative L2 passes |
| Final particle mean relative L2 | `6.274204511133432e-05` | `<= 0.20` unless absolute L2 passes |
| Final particle mean absolute L2 | `0.08081171095793331` | `<= 25.0` unless relative L2 passes |
| Warm median streaming/Nystrom | `3.3034285951636555` | descriptive in this pilot |

## Interpretation

Nystrom passed the first serious-model gate on the actual-SIR d18 workload.  The
important result is not the descriptive timing ratio; it is that the route
preserved actual-SIR semantics, fired on every active resampling step, produced
finite outputs, kept log weights normalized, passed Nystrom residual gates, and
matched the streaming route under the paired actual-SIR comparability thresholds.

This is meaningfully stronger than the synthetic LGSSM pilot, but it is still
not default-promotion evidence.  The pilot has one seed, a short horizon, and a
small particle count.  It authorizes the first serious actual-SIR row, not a
default change.

## Post-Run Red Team

| Check | Assessment |
| --- | --- |
| Strongest alternative explanation | The short `B=1,T=3,N=128` row may be too easy; the full `B=5,T=20,N=1024` row could reveal drift or runtime issues. |
| What would overturn the conclusion | Full SIR row fails paired log-likelihood/filter comparability, residuals, ESS, or route-fired evidence. |
| Weakest evidence | Fallback GPU0 was used because GPU1 was busy; timing is descriptive and not comparable to prior GPU1 rows. |

## Next Step

Run the first serious actual-SIR default-promotion-relevant row:
`B=5,T=20,N=1024`, seeds `81120,81121,81122,81123,81124`, `rank=32` first
unless a reviewed tuning note chooses `rank=64`, GPU1 preferred otherwise GPU0,
same paired thresholds, and a fixed outer timeout.  If that passes, then move to
a replicated actual-SIR ladder; if it fails, classify whether the failure is
rank/tuning, route validity, or evidence against Nystrom for actual-SIR default
promotion.
