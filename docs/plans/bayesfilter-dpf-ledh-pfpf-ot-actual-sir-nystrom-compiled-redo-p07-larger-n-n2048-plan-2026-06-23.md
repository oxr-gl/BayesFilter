# Actual-SIR Nystrom Compiled-Redo P07 Larger-N N2048 Plan

Date: 2026-06-23

Status: `READY_TO_LAUNCH`

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Does the repaired compiled Nystrom route continue to pass actual-SIR paired validity/comparability at `N=2048` after P04/P05 same-shape replication passed at `N=1024`? |
| Candidate | Compiled tensor-only Nystrom route, `rank=32`, `epsilon=0.5`, `max_iterations=160`, `convergence_threshold=1e-4`, TF32 enabled. |
| Baseline/comparator | Compiled streaming TF32 actual-SIR route in the same process, same GPU, same seeds, same dtype, same transport policy, and same timing protocol. |
| Shape | `B=5,T=20,N=2048,D=18,M=9`, seeds `81320,81321,81322,81323,81324`. |
| Primary pass criterion | JSON `status=PASS`, `hard_vetoes=[]`, GPU/TF32/JIT evidence present, finite outputs, Nystrom residuals pass, and paired log-likelihood thresholds pass. |
| Promotion veto | Any hard veto, paired log-likelihood max abs delta `>10.0`, paired mean abs delta `>5.0`, missing GPU/TF32/JIT evidence, nonfinite output, residual threshold failure, route mismatch, or stale artifact support. |
| Continuation veto | Timeout without artifact, GPU unavailable in trusted context, artifact/schema mismatch, or evidence that the repaired compiled route is not being used. |
| Repair trigger | Residual degradation, paired deltas near or above threshold, compile/runtime regression that threatens completion, or memory pressure. |
| Explanatory diagnostics | Compile plus first-call time, warm-call time, warm ratio, residuals, iterations, GPU memory, per-seed deltas. |
| What must not be concluded | No default readiness, no statistical ranking, no superiority claim, no posterior correctness, no HMC readiness, no dense Sinkhorn equivalence. |

## Evidence Contract

This phase can advance the runbook to the one-seed higher-N paired probes only
if it passes.  It cannot by itself establish promotion or speed superiority.

## Skeptical Pre-Launch Audit

Status: `PASS_FOR_P07_N2048`

The plan uses the repaired compiled-redo harness, not quarantined Python-loop
runtime artifacts.  The comparator is the production-style compiled streaming
TF32 actual-SIR route, not a weak baseline.  The row uses the same serious SIR
model and five-seed batch structure as P04/P05, with only `N` increased to
`2048`.  Runtime and memory remain explanatory because the phase has one repeat
and no uncertainty model.  The JSON and Markdown artifacts directly answer the
larger-N paired validity/comparability question.

## Command Template

```bash
timeout 2400 python docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py --route both --batch-seeds 81320,81321,81322,81323,81324 --time-steps 20 --num-particles 2048 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --history-mode value-only --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices <0-or-1> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <0-or-1> --gpu-selection-note '<preflight selection note>' --phase-id ACTUAL-SIR-NYSTROM-COMPILED-REDO-P07-LARGER-N-B5-T20-N2048 --quiet --output docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-larger-n-b5-t20-n2048-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-nystrom-compiled-redo-p07-larger-n-b5-t20-n2048-2026-06-23.md
```
