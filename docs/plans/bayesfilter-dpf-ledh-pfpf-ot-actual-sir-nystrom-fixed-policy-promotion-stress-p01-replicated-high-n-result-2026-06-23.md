# P01 Result: Replicated High-N Gate

Date: 2026-06-23

Status: `FAILED_OPTIONAL_HIGH_N_PAIRED_MEAN_VETO`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | P01 cannot pass because the launched optional `N=8192` row failed the predeclared paired mean log-likelihood threshold. |
| Primary criterion status | Mixed: required `N=2048` and `N=4096` replicated rows passed; launched optional `N=8192` row failed aggregate status. |
| Veto diagnostic status | `N=8192` fired `paired:paired_log_likelihood_mean_abs_delta` with mean/max delta `6.96771240234375`, exceeding the mean threshold `5.0` while remaining below max threshold `10.0`. |
| Main uncertainty | The failure is one seed at `N=8192`; it is a valid promotion-stress veto for this runbook, not statistical evidence of broad inferiority or a proof that the Nystrom route is unusable. |
| Next justified action | Route to P04 closeout classification or a separate reviewed repair/tuning plan; do not continue automatically to P02/P03 under this fixed-policy promotion-stress runbook. |
| What is not being concluded | No default readiness, no statistical ranking, no posterior correctness, no HMC readiness, no broad rank/epsilon robustness, no rejection of all Nystrom research directions. |

## Evidence Summary

Fixed policy for all rows:

- `rank=32`;
- `epsilon=0.5`;
- `kernel_mode=raw`;
- `scaling_normalization=none`;
- `core_solver=cholesky`;
- `float32`, TF32 enabled, JIT compiled;
- route `both`;
- history mode `value-only`;
- trusted GPU fallback to physical GPU0 because GPU1 was occupied at preflight.

Required rows:

| Row | Seeds | Status | Hard vetoes | Paired max delta | Paired mean delta | Row residual | Column residual | Wall seconds |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `N=2048,T=20` | `82921,82922,82923` | `PASS` | `[]` | `3.092529296875` | `2.1047770182291665` | `9.644031524658203e-05` | `2.384185791015625e-06` | `34.755391385173425` |
| `N=4096,T=20` | `82921,82922,82923` | `PASS` | `[]` | `4.99755859375` | `2.087646484375` | `9.953975677490234e-05` | `2.86102294921875e-06` | `35.88932419195771` |

Optional row:

| Row | Seeds | Status | Hard vetoes | Paired max delta | Paired mean delta | Row residual | Column residual | Wall seconds |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `N=8192,T=20` | `82921` | `FAIL` | `['paired:paired_log_likelihood_mean_abs_delta']` | `6.96771240234375` | `6.96771240234375` | `8.71419906616211e-05` | `4.291534423828125e-06` | `33.49705450399779` |

The optional `N=8192` row had finite route outputs and no per-route hard
vetoes. It failed only the paired mean threshold. Because P01 launched the
optional row under the predeclared entry conditions, that failed aggregate
artifact is binding for P01.

## Commands Actually Run

GPU preflight:

```bash
nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits
```

Required `N=2048` row:

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds 82921,82922,82923 --time-steps 20 --num-particles 2048 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --jit-compile --device-scope visible --cuda-visible-devices 0 --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu 0 --gpu-selection-note "GPU1 preferred but not selected: preflight showed GPU1 30749/32760 MiB used; GPU0 selected with 1494/32760 MiB used." --phase-id ACTUAL-SIR-NYSTROM-FIXED-POLICY-PROMOTION-STRESS-P01-N2048 --quiet --output docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n2048-r32-eps0p5-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n2048-r32-eps0p5-2026-06-23.md
```

Required `N=4096` row:

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds 82921,82922,82923 --time-steps 20 --num-particles 4096 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --jit-compile --device-scope visible --cuda-visible-devices 0 --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu 0 --gpu-selection-note "GPU1 preferred but not selected: preflight showed GPU1 30755/32760 MiB used; GPU0 selected with 1498/32760 MiB used." --phase-id ACTUAL-SIR-NYSTROM-FIXED-POLICY-PROMOTION-STRESS-P01-N4096 --quiet --output docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n4096-r32-eps0p5-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n4096-r32-eps0p5-2026-06-23.md
```

Optional `N=8192` row:

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds 82921 --time-steps 20 --num-particles 8192 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-diagnostics --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --nystrom-kernel-mode raw --nystrom-scaling-normalization none --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --jit-compile --device-scope visible --cuda-visible-devices 0 --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu 0 --gpu-selection-note "GPU1 preferred but not selected: optional preflight showed GPU1 30887/32760 MiB used; GPU0 selected with 1500/32760 MiB used and >8 GiB free." --phase-id ACTUAL-SIR-NYSTROM-FIXED-POLICY-PROMOTION-STRESS-P01-N8192 --quiet --output docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n8192-r32-eps0p5-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n8192-r32-eps0p5-2026-06-23.md
```

## Artifacts

- `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n2048-r32-eps0p5-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n2048-r32-eps0p5-2026-06-23.md`
- `docs/plans/logs/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n2048-r32-eps0p5-2026-06-23.log`
- `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n4096-r32-eps0p5-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n4096-r32-eps0p5-2026-06-23.md`
- `docs/plans/logs/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n4096-r32-eps0p5-2026-06-23.log`
- `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n8192-r32-eps0p5-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n8192-r32-eps0p5-2026-06-23.md`
- `docs/plans/logs/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n8192-r32-eps0p5-2026-06-23.log`

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, TensorFlow `2.20.0` |
| CPU/GPU status | Trusted GPU run; GPU1 preferred but occupied during P01 preflights; GPU0 selected and recorded in every artifact. |
| Random seeds | Required rows: `82921,82922,82923`; optional row: `82921`. |
| Wall time | `34.76s`, `35.89s`, `33.50s` for `N=2048`, `N=4096`, `N=8192`. |
| Output artifacts | Listed above. |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p01-replicated-high-n-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p01-replicated-high-n-result-2026-06-23.md` |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Required replicated rows passed; launched optional `N=8192` failed aggregate hard screen by paired mean likelihood threshold. |
| Statistically supported ranking | None. One optional seed failure is a hard-screen veto for this lane, not a statistical ranking. |
| Descriptive-only differences | Runtime, warm timing ratio, ESS, and residual magnitudes below thresholds are descriptive only. |
| Default-readiness | No. P01 failed after launching the optional `N=8192` row. |
| Next evidence needed | Separate reviewed closeout and, if desired, a repair/tuning plan that explains the paired mean drift at `N=8192`. |

## Interpretation

The required replicated high-N evidence improved on the previous one-seed
ladder at `N=2048` and `N=4096`: both required rows passed with no hard vetoes.

The optional `N=8192` row was launched because its predeclared entry conditions
were met. It produced a valid artifact with finite route outputs and acceptable
Nystrom residuals, but failed the aggregate paired mean log-likelihood
threshold. Under this runbook, that is a promotion-stress veto for the fixed
policy. It does not classify the harness as invalid and does not by itself
reject the broader Nystrom research direction.

## Post-Run Red-Team Note

Strongest alternative explanation: the single optional `N=8192` seed may be an
unlucky paired-drift draw or may reveal a scale-specific comparability issue
that was hidden at lower N.

What would overturn this result: discovering that the `N=8192` paired artifact
used a different comparator, fixed policy, seed, GPU/TF32 state, or threshold
than recorded; or a reviewed plan declaring the optional row non-binding before
launch, which did not happen.

Weakest part of the evidence: `N=8192` has only one seed, so it is a hard-screen
veto rather than statistical evidence about tail behavior or superiority.
