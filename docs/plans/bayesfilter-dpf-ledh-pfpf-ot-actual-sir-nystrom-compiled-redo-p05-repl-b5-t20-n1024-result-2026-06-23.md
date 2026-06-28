# Actual-SIR Nystrom Compiled-Redo P05 Replication Result

Date: 2026-06-23

Status: `PASS_REPLICATION_GATE`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to P06 same-shape replication summary | `PASS`: disjoint `B=5,T=20,N=1024` seed batch wrote artifact with `status=PASS` | No hard vetoes; paired thresholds passed; GPU/TF32/JIT evidence present | One additional five-seed batch only; P04 and P05 used different physical GPUs, so timing remains descriptive | Combine P04 and P05 into the required 10-seed same-shape summary before larger-N | No default readiness, no posterior correctness, no HMC readiness, no dense equivalence, no statistical ranking, no superiority claim |

## Artifacts

- Runbook: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-promotion-or-rejection-runbook-2026-06-23.md`
- JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p05-repl-b5-t20-n1024-2026-06-23.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p05-repl-b5-t20-n1024-2026-06-23.md`

## Result Summary

| Field | Value |
| --- | --- |
| Status | `PASS` |
| Hard vetoes | `[]` |
| Shape | `B=5,T=20,N=1024,D=18,M=9` |
| Seeds | `81220,81221,81222,81223,81224` |
| GPU | Physical GPU0 |
| GPU selection | GPU1 unavailable: `30755 MiB` already used; fallback to GPU0 |
| TF32 | enabled |
| JIT compile | `True` |
| Wall time | `35.06056473799981s` |

## Route Summary

| Route | Status | Compile plus first call | Warm median | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `19.843501010909677s` | `0.1679728280287236s` | `[]` |
| nystrom | `PASS` | `13.852564461063594s` | `0.07246675505302846s` | `[]` |

## Nystrom Diagnostics

| Diagnostic | Value |
| --- | ---: |
| Final logsumexp residual | `0.0` |
| Max row residual | `9.381771087646484e-05` |
| Max column residual | `2.86102294921875e-06` |
| Route invocations | `20` |
| Iterations used max | `3` |
| Finite factors | `True` |
| Finite particles | `True` |

## Paired Comparability

| Metric | Value | Threshold | Status |
| --- | ---: | ---: | --- |
| Log-likelihood max abs delta | `7.10369873046875` | `<=10.0` | `PASS` |
| Log-likelihood mean abs delta | `3.2791748046875` | `<=5.0` | `PASS` |
| Warm median streaming/Nystrom | `2.317929482364808` | descriptive only | N/A |

Per-seed paired log-likelihood deltas:

| Seed | Nystrom minus streaming |
| ---: | ---: |
| `81220` | `7.10369873046875` |
| `81221` | `-1.2872314453125` |
| `81222` | `3.412841796875` |
| `81223` | `-1.021484375` |
| `81224` | `-3.57061767578125` |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | `timeout 1800 python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds 81220,81221,81222,81223,81224 --time-steps 20 --num-particles 1024 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 0 --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu 0 --gpu-selection-note 'GPU1 unavailable for P05: 30755 MiB already used; fallback to GPU0 with 1217 MiB used and 25 percent utilization' --phase-id ACTUAL-SIR-NYSTROM-COMPILED-REDO-P05-REPL-B5-T20-N1024 --quiet --output docs/benchmarks/actual-sir-nystrom-compiled-redo-p05-repl-b5-t20-n1024-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-nystrom-compiled-redo-p05-repl-b5-t20-n1024-2026-06-23.md` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13`, TensorFlow `2.20.0` |
| GPU status | Trusted preflight; physical GPU0 selected because GPU1 was memory-busy |
| Data/model | Actual-SIR `zhao_cui_spatial_sir_austria_j9_T20`, `D=18,M=9,T=20` |
| Random seeds | `81220,81221,81222,81223,81224` |
| Wall time | `35.06056473799981s` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-promotion-or-rejection-runbook-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p05-repl-b5-t20-n1024-result-2026-06-23.md` |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS` |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Timing ratio and per-batch timing remain descriptive |
| Default-readiness | `NO` |
| Next evidence needed | P06 combined same-shape replication summary |

## Post-Run Red Team

Strongest alternative explanation: P05 may pass because the selected rank and
thresholds are adequate only at `N=1024`; larger particle counts, different
transport policies, full-history mode, or gradient use may still fail.

Weakest evidence: timing uses one repeat and P04/P05 ran on different physical
GPUs, so it cannot support a speed ranking.

What would overturn continuation: a combined P06 audit finding a hidden artifact
mismatch, stale harness support, or a paired-threshold violation.
