# Actual-SIR Nystrom Compiled-Redo P07 N8192 Diagnostic Result

Date: 2026-06-23

Status: `PASS_P07_PAIRED_DIAGNOSTIC_LADDER`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Close P07 paired diagnostic ladder as passed and advance to P08 Nystrom-only high-N envelope planning | `PASS`: one-seed `B=1,T=20,N=8192` paired diagnostic wrote artifact with `status=PASS` | No hard vetoes; paired threshold passed; GPU/TF32/JIT evidence present | One seed only; batch size `B=1`; timing is descriptive despite large observed ratio | Start P08 Nystrom-only envelope with sequential rows and stop conditions | No rigorous promotion evidence, no default readiness, no statistical ranking, no superiority, no posterior correctness, no HMC readiness |

## Artifacts

- Plan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p07-n8192-diagnostic-plan-2026-06-23.md`
- JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-n8192-diagnostic-2026-06-23.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-n8192-diagnostic-2026-06-23.md`

## Result Summary

| Field | Value |
| --- | --- |
| Status | `PASS` |
| Hard vetoes | `[]` |
| Shape | `B=1,T=20,N=8192,D=18,M=9` |
| Seed | `81520` |
| GPU | Physical GPU0 |
| GPU selection | GPU1 unavailable: `30755 MiB` already used; fallback to GPU0 |
| TF32 | enabled |
| JIT compile | `True` |
| Wall time | `64.03262791316956s` |

## Route Summary

| Route | Status | Compile plus first call | Warm median | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `33.77408173913136s` | `17.025218456983566s` | `[]` |
| nystrom | `PASS` | `11.30258442601189s` | `0.8690328011289239s` | `[]` |

## Nystrom Diagnostics

| Diagnostic | Value |
| --- | ---: |
| Final logsumexp residual | `9.5367431640625e-07` |
| Max row residual | `6.80685043334961e-05` |
| Max column residual | `3.337860107421875e-06` |
| Route invocations | `20` |
| Iterations used max | `3` |
| Finite factors | `True` |
| Finite particles | `True` |

## Paired Comparability

| Metric | Value | Threshold | Status |
| --- | ---: | ---: | --- |
| Log-likelihood max abs delta | `0.0142822265625` | `<=10.0` | `PASS` |
| Log-likelihood mean abs delta | `0.0142822265625` | `<=5.0` | `PASS` |
| Warm median streaming/Nystrom | `19.59099637535755` | descriptive only | N/A |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | `timeout 2400 python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds 81520 --time-steps 20 --num-particles 8192 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 0 --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu 0 --gpu-selection-note 'GPU1 unavailable for P07 N8192 diagnostic: 30755 MiB already used; fallback to GPU0 with 1198 MiB used and 34 percent utilization' --phase-id ACTUAL-SIR-NYSTROM-COMPILED-REDO-P07-N8192-DIAGNOSTIC --quiet --output docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-n8192-diagnostic-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-n8192-diagnostic-2026-06-23.md` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13`, TensorFlow `2.20.0` |
| GPU status | Trusted preflight; physical GPU0 selected because GPU1 was memory-busy |
| Data/model | Actual-SIR `zhao_cui_spatial_sir_austria_j9_T20`, `D=18,M=9,T=20` |
| Random seed | `81520` |
| Wall time | `64.03262791316956s` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p07-n8192-diagnostic-plan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p07-n8192-diagnostic-result-2026-06-23.md` |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS` |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Runtime, warm ratio, single-seed paired delta, and memory |
| Default-readiness | `NO` |
| Next evidence needed | P08 Nystrom-only high-N envelope, then P09 rank/epsilon sensitivity |

## Post-Run Red Team

Strongest alternative explanation: the route may pass one-seed `B=1` paired
rows while still failing higher batch sizes, other seeds, full-history mode, or
gradient/HMC use.

What would overturn continuation: P08 high-N envelope memory failure, P09
sensitivity brittleness, or P10/P11 stress and gradient failures.

## Next Action

Plan and launch P08 Nystrom-only high-N envelope sequentially, with explicit
stop conditions.  These rows remain feasibility evidence only.
