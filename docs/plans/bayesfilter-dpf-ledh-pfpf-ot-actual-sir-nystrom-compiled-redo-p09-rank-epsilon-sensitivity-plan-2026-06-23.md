# Actual-SIR Nystrom Compiled-Redo P09 Rank/Epsilon Sensitivity Plan

Date: 2026-06-23

Status: `READY_TO_LAUNCH_SEQUENTIAL_GRID`

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Is the repaired compiled Nystrom candidate robust across nearby rank/epsilon settings, or is the apparent success brittle to the current `rank=32,epsilon=0.5` choice? |
| Candidate family | Compiled tensor-only Nystrom actual-SIR route with fixed rank and epsilon, TF32 enabled, JIT enabled. |
| Baseline/comparator | Compiled streaming TF32 actual-SIR route in the same process and selected physical GPU for each row. |
| Grid | ranks `16,32,64` crossed with epsilons `0.25,0.5,1.0`. |
| Shape | `B=5,T=20,N=1024,D=18,M=9`, seeds `81920,81921,81922,81923,81924`. |
| Primary pass criterion | Every grid row writes JSON/Markdown with `status=PASS`, `hard_vetoes=[]`, GPU/TF32/JIT evidence, finite outputs, Nystrom residuals pass, and paired log-likelihood thresholds pass. |
| Promotion veto | Any hard veto, paired max abs delta `>10.0`, paired mean abs delta `>5.0`, residual threshold failure, nonfinite output, route mismatch, missing GPU/TF32/JIT evidence, or artifact/schema mismatch. |
| Continuation veto | Timeout without artifact, GPU memory failure, evidence that the compiled-redo route did not run, or a failed row that shows a required candidate setting is invalid. |
| Repair trigger | One or more non-default grid rows fail while the default row passes; this triggers policy narrowing or sensitivity classification before default promotion. |
| Explanatory diagnostics | Runtime, warm ratio, residuals below threshold, iteration count, per-seed deltas, and which settings are descriptively favorable. |
| What must not be concluded | No statistical ranking, no default readiness, no superiority, no posterior correctness, no HMC readiness. Passing the grid means sensitivity viability only. |

## Evidence Contract

This phase is a brittleness screen.  It can keep the fixed `rank=32,epsilon=0.5`
candidate viable, narrow the acceptable policy, or trigger repair.  It cannot
rank candidates by timing or quality without a later uncertainty analysis.

## Skeptical Pre-Launch Audit

Status: `PASS_FOR_P09_GRID`

The grid uses the repaired compiled-redo harness, not quarantined Python-loop
artifacts.  The streaming comparator is the same compiled TF32 route used in
P04-P07.  Runtime and warm ratios are descriptive only.  The grid is sequential
and gated: if a row fails, stop before launching remaining rows unless the
failure is clearly an artifact-write issue that can be retried without changing
the scientific question.

## Grid Rows

All rows use:

```text
--route both
--batch-seeds 81920,81921,81922,81923,81924
--time-steps 20
--num-particles 1024
--transport-policy active-all
--sinkhorn-iterations 10
--sinkhorn-epsilon 1.0
--annealed-scaling 0.9
--annealed-convergence-threshold 0.001
--row-chunk-size 1024
--col-chunk-size 1024
--particle-chunk-size 1024
--nystrom-max-iterations 160
--nystrom-convergence-threshold 0.0001
--history-mode value-only
--warmups 0
--repeats 1
--dtype float32
--tf32-mode enabled
--device-scope visible
--device /GPU:0
--expect-device-kind gpu
--quiet
```

Rows:

| Row | Rank | Epsilon | Artifact suffix |
| --- | ---: | ---: | --- |
| 1 | `16` | `0.25` | `r16-eps0p25` |
| 2 | `16` | `0.5` | `r16-eps0p5` |
| 3 | `16` | `1.0` | `r16-eps1p0` |
| 4 | `32` | `0.25` | `r32-eps0p25` |
| 5 | `32` | `0.5` | `r32-eps0p5` |
| 6 | `32` | `1.0` | `r32-eps1p0` |
| 7 | `64` | `0.25` | `r64-eps0p25` |
| 8 | `64` | `0.5` | `r64-eps0p5` |
| 9 | `64` | `1.0` | `r64-eps1p0` |

Output pattern:

- JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09-sensitivity-<suffix>-2026-06-23.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09-sensitivity-<suffix>-2026-06-23.md`

## Automatic Gated Execution Rule

After each row:

1. Read the JSON.
2. If `status=PASS` and `hard_vetoes=[]`, continue to the next row.
3. If any row fails, stop the grid and write a P09 partial result note.
4. Do not reinterpret failed rows as timing evidence or rank candidates by
   descriptive metrics.
