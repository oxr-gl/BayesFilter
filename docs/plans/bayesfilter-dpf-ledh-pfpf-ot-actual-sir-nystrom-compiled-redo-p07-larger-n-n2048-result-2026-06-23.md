# Actual-SIR Nystrom Compiled-Redo P07 Larger-N N2048 Result

Date: 2026-06-23

Status: `PASS_ADVANCE_TO_N4096_DIAGNOSTIC`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to the P07 one-seed `N=4096` paired diagnostic | `PASS`: `B=5,T=20,N=2048` paired row wrote artifact with `status=PASS` | No hard vetoes; paired log-likelihood thresholds passed; GPU/TF32/JIT evidence present | One five-seed larger-N row only; timing is one-repeat descriptive evidence | Run the cheap one-seed `N=4096` paired probe before any high-N envelope | No default readiness, no statistical ranking, no superiority, no posterior correctness, no HMC readiness, no dense equivalence |

## Artifacts

- Plan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p07-larger-n-n2048-plan-2026-06-23.md`
- JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-larger-n-b5-t20-n2048-2026-06-23.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-larger-n-b5-t20-n2048-2026-06-23.md`

## Result Summary

| Field | Value |
| --- | --- |
| Status | `PASS` |
| Hard vetoes | `[]` |
| Shape | `B=5,T=20,N=2048,D=18,M=9` |
| Seeds | `81320,81321,81322,81323,81324` |
| GPU | Physical GPU0 |
| GPU selection | GPU1 unavailable: `30755 MiB` already used; fallback to GPU0 |
| TF32 | enabled |
| JIT compile | `True` |
| Wall time | `37.534399644937366s` |

## Route Summary

| Route | Status | Compile plus first call | Warm median | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `20.986187719972804s` | `0.41184131195768714s` | `[]` |
| nystrom | `PASS` | `14.94269566400908s` | `0.1320293180178851s` | `[]` |

## Nystrom Diagnostics

| Diagnostic | Value |
| --- | ---: |
| Final logsumexp residual | `0.0` |
| Max row residual | `9.632110595703125e-05` |
| Max column residual | `2.86102294921875e-06` |
| Route invocations | `20` |
| Iterations used max | `3` |
| Finite factors | `True` |
| Finite particles | `True` |

## Paired Comparability

| Metric | Value | Threshold | Status |
| --- | ---: | ---: | --- |
| Log-likelihood max abs delta | `4.65521240234375` | `<=10.0` | `PASS` |
| Log-likelihood mean abs delta | `2.67186279296875` | `<=5.0` | `PASS` |
| Warm median streaming/Nystrom | `3.1193171194135676` | descriptive only | N/A |

Per-seed paired log-likelihood deltas:

| Seed | Nystrom minus streaming |
| ---: | ---: |
| `81320` | `-3.32830810546875` |
| `81321` | `4.65521240234375` |
| `81322` | `-0.67596435546875` |
| `81323` | `-0.77166748046875` |
| `81324` | `3.92816162109375` |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | `timeout 2400 python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds 81320,81321,81322,81323,81324 --time-steps 20 --num-particles 2048 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 0 --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu 0 --gpu-selection-note 'GPU1 unavailable for P07 N2048: 30755 MiB already used; fallback to GPU0 with 1199 MiB used and 28 percent utilization' --phase-id ACTUAL-SIR-NYSTROM-COMPILED-REDO-P07-LARGER-N-B5-T20-N2048 --quiet --output docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-larger-n-b5-t20-n2048-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-larger-n-b5-t20-n2048-2026-06-23.md` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13`, TensorFlow `2.20.0` |
| GPU status | Trusted preflight; physical GPU0 selected because GPU1 was memory-busy |
| Data/model | Actual-SIR `zhao_cui_spatial_sir_austria_j9_T20`, `D=18,M=9,T=20` |
| Random seeds | `81320,81321,81322,81323,81324` |
| Wall time | `37.534399644937366s` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p07-larger-n-n2048-plan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p07-larger-n-n2048-result-2026-06-23.md` |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS` |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Runtime, warm ratio, per-seed deltas, and residual magnitudes below threshold |
| Default-readiness | `NO` |
| Next evidence needed | One-seed paired `N=4096` diagnostic |

## Post-Run Red Team

Strongest alternative explanation: `N=2048` may still be below the particle
regime where the approximation or memory profile breaks, and this row has no
replicated uncertainty model for timing.

What would overturn continuation: `N=4096` paired diagnostic failing thresholds,
timing out without an artifact, or exposing a GPU memory/runtime blocker.

## Next Action

Run the one-seed paired `N=4096` diagnostic under the repaired compiled-redo
harness.  Treat the result as diagnostic feasibility evidence only.
