# Actual-SIR Nystrom Compiled-Redo P07 N4096 Diagnostic Result

Date: 2026-06-23

Status: `PASS_DIAGNOSTIC_ADVANCE_OPTIONAL_N8192`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Keep the repaired compiled Nystrom candidate viable and allow the optional `N=8192` paired diagnostic or P08 high-N envelope | `PASS`: one-seed `B=1,T=20,N=4096` paired diagnostic wrote artifact with `status=PASS` | No hard vetoes; paired threshold passed; GPU/TF32/JIT evidence present | One seed only; batch size reduced to `B=1`; timing is descriptive | Continue with optional `N=8192` paired diagnostic or move to P08 Nystrom-only envelope under a new launch note | No rigorous promotion evidence, no default readiness, no statistical ranking, no superiority, no posterior correctness, no HMC readiness |

## Artifacts

- Plan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p07-n4096-diagnostic-plan-2026-06-23.md`
- JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-n4096-diagnostic-2026-06-23.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-n4096-diagnostic-2026-06-23.md`

## Result Summary

| Field | Value |
| --- | --- |
| Status | `PASS` |
| Hard vetoes | `[]` |
| Shape | `B=1,T=20,N=4096,D=18,M=9` |
| Seed | `81420` |
| GPU | Physical GPU0 |
| GPU selection | GPU1 unavailable: `30881 MiB` already used; fallback to GPU0 |
| TF32 | enabled |
| JIT compile | `True` |
| Wall time | `31.468154155882075s` |

## Route Summary

| Route | Status | Compile plus first call | Warm median | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `17.963599339826033s` | `1.5411376350093633s` | `[]` |
| nystrom | `PASS` | `10.773117518983781s` | `0.14315718389116228s` | `[]` |

## Nystrom Diagnostics

| Diagnostic | Value |
| --- | ---: |
| Final logsumexp residual | `0.0` |
| Max row residual | `9.85860824584961e-05` |
| Max column residual | `3.337860107421875e-06` |
| Route invocations | `20` |
| Iterations used max | `3` |
| Finite factors | `True` |
| Finite particles | `True` |

## Paired Comparability

| Metric | Value | Threshold | Status |
| --- | ---: | ---: | --- |
| Log-likelihood max abs delta | `0.57757568359375` | `<=10.0` | `PASS` |
| Log-likelihood mean abs delta | `0.57757568359375` | `<=5.0` | `PASS` |
| Warm median streaming/Nystrom | `10.765353111311828` | descriptive only | N/A |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | `timeout 2400 python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds 81420 --time-steps 20 --num-particles 4096 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 0 --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu 0 --gpu-selection-note 'GPU1 unavailable for P07 N4096 diagnostic: 30881 MiB already used; fallback to GPU0 with 1280 MiB used and 27 percent utilization' --phase-id ACTUAL-SIR-NYSTROM-COMPILED-REDO-P07-N4096-DIAGNOSTIC --quiet --output docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-n4096-diagnostic-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-n4096-diagnostic-2026-06-23.md` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13`, TensorFlow `2.20.0` |
| GPU status | Trusted preflight; physical GPU0 selected because GPU1 was memory-busy |
| Data/model | Actual-SIR `zhao_cui_spatial_sir_austria_j9_T20`, `D=18,M=9,T=20` |
| Random seed | `81420` |
| Wall time | `31.468154155882075s` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p07-n4096-diagnostic-plan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p07-n4096-diagnostic-result-2026-06-23.md` |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS` |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Runtime, warm ratio, single-seed paired delta, and memory |
| Default-readiness | `NO` |
| Next evidence needed | Optional `N=8192` paired diagnostic or P08 Nystrom-only high-N envelope |

## Post-Run Red Team

Strongest alternative explanation: this pass may depend on the single seed and
`B=1`; it does not rule out instability at other seeds, larger batch size, full
history, or gradient/HMC use.

What would overturn continuation: failure at `N=8192`, a Nystrom-only high-N
envelope memory failure, or sensitivity/stress gates showing brittleness.

## Next Action

Run either the optional one-seed paired `N=8192` diagnostic or start P08
Nystrom-only high-N envelope.  Both remain feasibility/repair evidence, not
promotion-grade statistical evidence.
