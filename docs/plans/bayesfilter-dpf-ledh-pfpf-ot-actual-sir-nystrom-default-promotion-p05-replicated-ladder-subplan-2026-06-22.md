# Actual-SIR Nystrom Default-Promotion P05 Replicated Ladder Subplan

Date: 2026-06-22

Status: `READY_TO_LAUNCH_STAGE_A`

## Purpose

Extend the passed P03 serious row into a replicated actual-SIR ladder without
turning a single successful row into a default-promotion claim.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does fixed-rank Nystrom keep passing actual-SIR d18 validity and paired comparability across additional seed batches and larger particle counts? |
| Comparator | Streaming TF32 actual-SIR route, same P8j callbacks, same observations, same dtype, same TF32 state, same physical GPU within each paired artifact. |
| Candidate | Nystrom `rank=32`, `epsilon=0.5`, `max_iterations=160`, active-all resampling. |
| Accepted prior evidence | P03 `B=5,T=20,N=1024`, seeds `81120..81124`, passed with `hard_vetoes=[]`; use as seed batch S0 evidence. |
| Stage A row | `B=5,T=20,N=1024`, seeds `81220,81221,81222,81223,81224`; tests seed-batch replication at the P03 particle count. |
| Stage B row | `B=5,T=20,N=2048`, seeds `81120..81124`; run only if Stage A passes. |
| Stage C row | `B=5,T=20,N=4096`, seeds `81120..81124`; run only if Stage B passes and GPU/runtime budget is still reasonable. |
| Primary pass/fail criterion | Each launched row must report JSON `status=PASS`, `hard_vetoes=[]`, actual-SIR semantics pass, TF32/GPU provenance, and paired comparability pass. |
| Veto diagnostics | Nonfinite outputs; actual-SIR semantics missing; route invocation mismatch; dense transport materialization; Nystrom residual `>5e-2`; final log-sum-exp residual `>1e-5`; ESS fraction `<0.01`; paired comparability failure; GPU/TF32 mismatch; mixed GPU within one paired artifact. |
| Explanatory diagnostics | Runtime, memory, warm-time ratios, residual magnitudes below thresholds, ESS above threshold, rank, landmarks. |
| Statistical interpretation | Stage A plus P03 gives two seed batches at `N=1024`; continuous differences remain descriptive unless an uncertainty note is written from row-level evidence. Larger-N rows are ladder viability evidence, not default readiness. |
| Not concluded | No default readiness, no posterior correctness, no HMC readiness, no public API readiness, no dense Sinkhorn equivalence, no statistical superiority. |

## Stop Rules

- Stop if Stage A fails; write `SEED_REPLICATION_FAILED`.
- Stop if Stage B fails; write `N2048_LADDER_FAILED`.
- Stop if a GPU row times out under its fixed timeout; write timeout-boundary
  blocker/result before continuing.
- Stop if GPU1 and GPU0 are both unsuitable in trusted preflight.
- Stop before changing thresholds, seeds, comparator, SIR model, dtype, or
  default/public API behavior.

## Stage A Command Template

Use trusted GPU preflight first. Prefer physical GPU1 if usable, otherwise GPU0.

```bash
timeout 3600 python docs/benchmarks/benchmark_actual_sir_nystrom_default_promotion.py --route both --batch-seeds 81220,81221,81222,81223,81224 --time-steps 20 --num-particles 1024 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices <0-or-1> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <0-or-1> --gpu-selection-note '<preflight selection note>' --phase-id ACTUAL-SIR-NYSTROM-P05A-SEED-REPL-B5-T20-N1024 --quiet --output docs/benchmarks/actual-sir-nystrom-default-promotion-p05a-seed-repl-b5-t20-n1024-2026-06-22.json --markdown-output docs/benchmarks/actual-sir-nystrom-default-promotion-p05a-seed-repl-b5-t20-n1024-2026-06-22.md
```

## Stage B Command Template

Run only if Stage A passes.

```bash
timeout 7200 python docs/benchmarks/benchmark_actual_sir_nystrom_default_promotion.py --route both --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 2048 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices <0-or-1> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <0-or-1> --gpu-selection-note '<preflight selection note>' --phase-id ACTUAL-SIR-NYSTROM-P05B-LADDER-B5-T20-N2048 --quiet --output docs/benchmarks/actual-sir-nystrom-default-promotion-p05b-ladder-b5-t20-n2048-2026-06-22.json --markdown-output docs/benchmarks/actual-sir-nystrom-default-promotion-p05b-ladder-b5-t20-n2048-2026-06-22.md
```
