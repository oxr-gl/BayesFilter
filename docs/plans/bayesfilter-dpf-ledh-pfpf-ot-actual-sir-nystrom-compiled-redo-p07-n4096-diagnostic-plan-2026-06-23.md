# Actual-SIR Nystrom Compiled-Redo P07 N4096 Diagnostic Plan

Date: 2026-06-23

Status: `READY_TO_LAUNCH`

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Does the repaired compiled Nystrom route remain feasible and paired-comparable in a one-seed actual-SIR diagnostic at `N=4096`? |
| Candidate | Compiled tensor-only Nystrom route, `rank=32`, `epsilon=0.5`, `max_iterations=160`, `convergence_threshold=1e-4`, TF32 enabled. |
| Baseline/comparator | Compiled streaming TF32 actual-SIR route in the same process and selected physical GPU. |
| Shape | `B=1,T=20,N=4096,D=18,M=9`, seed `81420`. |
| Primary pass criterion | JSON `status=PASS`, `hard_vetoes=[]`, GPU/TF32/JIT evidence present, finite outputs, residuals pass, and paired log-likelihood thresholds pass. |
| Promotion veto | Any hard veto blocks using this row as scale-support evidence. |
| Continuation veto | Timeout without artifact, GPU memory failure, artifact mismatch, or evidence that compiled-redo route did not run. |
| Repair trigger | Threshold failure, residual degradation, memory pressure, or compile/runtime regression. |
| Explanatory diagnostics | Runtime, memory, warm ratio, residuals, iterations, single-seed paired delta. |
| What must not be concluded | No rigorous promotion evidence, no statistical ranking, no default readiness, no superiority, no posterior correctness, no HMC readiness. |

## Evidence Contract

This is a one-seed diagnostic requested to avoid over-spending on high-N seed
replication.  Passing can justify the next diagnostic row or high-N envelope;
failing triggers repair classification.  It cannot establish default readiness
or superiority.

## Skeptical Pre-Launch Audit

Status: `PASS_FOR_N4096_DIAGNOSTIC`

The command uses the repaired compiled-redo harness and same-process compiled
streaming comparator.  It does not reuse quarantined Python-loop timing
artifacts.  The row is explicitly one-seed diagnostic evidence, so proxy
metrics and single-seed deltas will not be promoted into statistical claims.

## Command Template

```bash
timeout 2400 python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds 81420 --time-steps 20 --num-particles 4096 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices <0-or-1> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <0-or-1> --gpu-selection-note '<preflight selection note>' --phase-id ACTUAL-SIR-NYSTROM-COMPILED-REDO-P07-N4096-DIAGNOSTIC --quiet --output docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-n4096-diagnostic-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-n4096-diagnostic-2026-06-23.md
```
