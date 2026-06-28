# Actual-SIR Nystrom Compiled-Redo P08 High-N Nystrom-Only Envelope Plan

Date: 2026-06-23

Status: `READY_TO_LAUNCH_SEQUENTIAL_ROWS`

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Does the repaired compiled Nystrom route remain finite and residual-valid at higher particle counts when run without the streaming comparator? |
| Candidate | Compiled tensor-only Nystrom route, `rank=32`, `epsilon=0.5`, `max_iterations=160`, `convergence_threshold=1e-4`, TF32 enabled. |
| Baseline/comparator | None inside P08 rows. P07 paired rows through `N=8192` are prior context; P08 tests Nystrom-only feasibility and shape/memory envelope. |
| Shapes | Prior lower-envelope evidence: `N=4096,8192` from P07 paired diagnostics. New P08 rows: `B=1,T=20,N=16384,32768,65536,D=18,M=9`, one seed each. |
| Primary pass criterion | Each row writes JSON/Markdown with `status=PASS`, `hard_vetoes=[]`, GPU/TF32/JIT evidence, finite outputs, Nystrom residuals within thresholds, and route invocations present. |
| Promotion veto | Any hard veto blocks using that row as high-N feasibility support. |
| Continuation veto | Timeout without artifact, GPU memory failure, artifact mismatch, nonfinite route output, residual threshold failure, or evidence that compiled-redo Nystrom route did not run. |
| Repair trigger | Memory pressure, compile/runtime regression, residual degradation, route invocation mismatch, or high-N row failure. |
| Explanatory diagnostics | Runtime, memory before/after, warm time, residuals, iterations, route invocations. |
| What must not be concluded | No paired quality beyond P07, no default readiness, no statistical ranking, no superiority, no posterior correctness, no HMC readiness. |

## Evidence Contract

This phase is Nystrom-only feasibility evidence.  Passing the envelope can
support continuing to rank/epsilon sensitivity and stress testing.  It cannot
establish dense equivalence, posterior correctness, paired comparability at
these high-N rows, or default promotion.

## Skeptical Pre-Launch Audit

Status: `PASS_FOR_SEQUENTIAL_P08_ROWS`

The phase does not use quarantined Python-loop timing artifacts.  It does not
pretend Nystrom-only rows are paired-quality evidence.  Runtime and memory are
descriptive feasibility diagnostics.  Rows are sequential with stop conditions:
if a row fails, do not continue to larger rows until a result note classifies
the failure and repair option.

## Row Commands

Use trusted GPU preflight before launch and prefer physical GPU1 if available,
otherwise GPU0.  Record the selected device in each artifact.

### N16384

```bash
timeout 2400 python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route nystrom --batch-seeds 81620 --time-steps 20 --num-particles 16384 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices <0-or-1> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <0-or-1> --gpu-selection-note '<preflight selection note>' --phase-id ACTUAL-SIR-NYSTROM-COMPILED-REDO-P08-NYSTROM-ONLY-N16384 --quiet --output docs/benchmarks/actual-sir-nystrom-compiled-redo-p08-nystrom-only-n16384-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-nystrom-compiled-redo-p08-nystrom-only-n16384-2026-06-23.md
```

### N32768

```bash
timeout 2400 python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route nystrom --batch-seeds 81720 --time-steps 20 --num-particles 32768 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices <0-or-1> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <0-or-1> --gpu-selection-note '<preflight selection note>' --phase-id ACTUAL-SIR-NYSTROM-COMPILED-REDO-P08-NYSTROM-ONLY-N32768 --quiet --output docs/benchmarks/actual-sir-nystrom-compiled-redo-p08-nystrom-only-n32768-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-nystrom-compiled-redo-p08-nystrom-only-n32768-2026-06-23.md
```

### N65536

```bash
timeout 2400 python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route nystrom --batch-seeds 81820 --time-steps 20 --num-particles 65536 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices <0-or-1> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <0-or-1> --gpu-selection-note '<preflight selection note>' --phase-id ACTUAL-SIR-NYSTROM-COMPILED-REDO-P08-NYSTROM-ONLY-N65536 --quiet --output docs/benchmarks/actual-sir-nystrom-compiled-redo-p08-nystrom-only-n65536-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-nystrom-compiled-redo-p08-nystrom-only-n65536-2026-06-23.md
```
