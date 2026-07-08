# Actual-SIR Nystrom Compiled Redo P03 Moderate Gate Plan

Date: 2026-06-22

Status: `READY_TO_LAUNCH`

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Does the repaired compiled route protocol remain valid on a moderate actual-SIR row before any serious default-promotion ladder is relaunched? |
| Candidate | Compiled tensor-only Nystrom route, `rank=32`, `epsilon=0.5`, `max_iterations=160`. |
| Baseline/comparator | Compiled production-style streaming TF32 actual-SIR value route, same process/device/shape/timing protocol. |
| Shape | `B=1,T=20,N=1024,D=18,M=9`, seed `81120`. |
| Primary pass criterion | JSON `status=PASS`, hard vetoes `[]`, GPU output tensors, TF32 recorded enabled, both routes compiled under `jit_compile=True`, paired log-likelihood thresholds pass, Nystrom residuals `<=5e-2`, finite outputs. |
| Promotion veto | Any hard veto, missing GPU/TF32 evidence, failed paired threshold, nonfinite output, Nystrom residual threshold failure, or artifact mismatch. |
| Continuation veto | Route execution error, timeout, GPU unavailability, missing artifact, or a benchmark path that is not the compiled redo harness. |
| Repair trigger | Failure caused by compile incompatibility, threshold mismatch, or artifact/schema issue triggers protocol repair rather than default-lane rejection. |
| Explanatory diagnostics | Compile plus first-call time, warm-call time, warm ratio, Nystrom iterations, residual values, GPU memory. |
| What must not be concluded | No default readiness, no statistical ranking, no posterior correctness, no HMC readiness, no superiority claim. |

## Evidence Contract

This is a protocol/effectiveness gate only.  It can advance the compiled redo
to a serious replicated row if it passes.  It cannot promote Nystrom to default
and cannot resurrect the old Python-loop timing artifacts.

## Skeptical Pre-Launch Audit

Status: `PASS_FOR_MODERATE_GATE`

The baseline is now the compiled streaming actual-SIR route, not the
contaminated Python-loop streaming timing from the prior harness.  The candidate
uses the new graph-compatible Nystrom tensor core.  Runtime is descriptive
because this is one seed and one repeat; hard vetoes and paired diagnostics are
the decision criteria.  The command writes a JSON/Markdown artifact that answers
the stated question, and the old benchmark path is not used.

## Command

```bash
timeout 1800 python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds 81120 --time-steps 20 --num-particles 1024 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices <0-or-1> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <0-or-1> --gpu-selection-note '<preflight selection note>' --phase-id ACTUAL-SIR-NYSTROM-COMPILED-REDO-P03-MODERATE-B1-T20-N1024 --quiet --output docs/benchmarks/actual-sir-nystrom-compiled-redo-p03-moderate-b1-t20-n1024-2026-06-22.json --markdown-output docs/benchmarks/actual-sir-nystrom-compiled-redo-p03-moderate-b1-t20-n1024-2026-06-22.md
```
