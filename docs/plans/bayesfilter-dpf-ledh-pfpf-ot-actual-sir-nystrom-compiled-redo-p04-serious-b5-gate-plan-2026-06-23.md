# Actual-SIR Nystrom Compiled Redo P04 Serious B5 Gate Plan

Date: 2026-06-23

Status: `READY_TO_LAUNCH`

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Does the repaired compiled Nystrom route pass a serious actual-SIR batched row after the P03B while-loop compile repair? |
| Candidate | Compiled tensor-only Nystrom route, `rank=32`, `epsilon=0.5`, `max_iterations=160`, with `tf.while_loop` time and Sinkhorn loops. |
| Baseline/comparator | Compiled production-style streaming TF32 actual-SIR value route, same process/device/shape/timing protocol. |
| Shape | `B=5,T=20,N=1024,D=18,M=9`, seeds `81120,81121,81122,81123,81124`. |
| Primary pass criterion | JSON `status=PASS`, hard vetoes `[]`, GPU output tensors, TF32 recorded enabled, `jit_compile=True`, paired log-likelihood thresholds pass, Nystrom residuals `<=5e-2`, finite outputs. |
| Promotion veto | Any hard veto, missing GPU/TF32 evidence, paired-threshold failure, nonfinite output, residual threshold failure, or artifact mismatch. |
| Continuation veto | Route execution error, timeout, GPU unavailability, missing artifact, or accidental use of the quarantined Python-loop benchmark. |
| Repair trigger | Compile regression, paired-delta increase near threshold, or residual degradation triggers protocol/candidate repair before replication. |
| Explanatory diagnostics | Compile plus first-call time, warm-call time, warm ratio, paired log-likelihood deltas, Nystrom residuals/iterations, GPU memory. |
| What must not be concluded | No default readiness, no statistical ranking, no posterior correctness, no HMC readiness, no superiority claim. |

## Evidence Contract

This row can advance the repaired compiled redo lane to a separate replicated
seed-batch gate if it passes.  It cannot by itself establish default readiness
or superiority.

## Skeptical Pre-Launch Audit

Status: `PASS_FOR_SERIOUS_B5_GATE`

The old Python-loop runtime artifacts remain quarantined.  This command uses
the repaired compiled redo harness and the same compiled route conditions for
streaming and Nystrom.  The baseline is not weak or convenient: it is the
compiled production-style streaming actual-SIR TF32 route.  Runtime and warm
ratio are explanatory because this is one batched row with one repeat.  The JSON
and Markdown artifacts answer the stated gate.

## Command

```bash
timeout 1800 python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 1024 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices <0-or-1> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <0-or-1> --gpu-selection-note '<preflight selection note>' --phase-id ACTUAL-SIR-NYSTROM-COMPILED-REDO-P04-SERIOUS-B5-T20-N1024 --quiet --output docs/benchmarks/actual-sir-nystrom-compiled-redo-p04-serious-b5-t20-n1024-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-nystrom-compiled-redo-p04-serious-b5-t20-n1024-2026-06-23.md
```
