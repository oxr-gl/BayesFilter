# Actual-SIR Nystrom Compiled-Redo P09 Default-Neighborhood Repair Plan

Date: 2026-06-23

Status: `READY_TO_LAUNCH_SEQUENTIAL_GRID`

## Purpose

The full P09 grid stopped because `rank=16,epsilon=1.0` failed paired
thresholds.  This repair grid tests whether the intended default neighborhood
around `rank=32,epsilon=0.5` remains viable, or whether P09 exposes a blocker
near the candidate setting.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Does the Nystrom candidate remain paired-comparable across the intended default-neighborhood settings after the weak `rank=16,epsilon=1.0` setting failed? |
| Candidate family | Fixed-rank Nystrom with ranks `32,64` and epsilons `0.25,0.5,1.0`. |
| Baseline/comparator | Compiled streaming TF32 route in the same process and selected physical GPU. |
| Shape | `B=5,T=20,N=1024,D=18,M=9`, seeds `81920..81924`, same as P09 full grid. |
| Primary pass criterion | Every narrowed-grid row writes JSON/Markdown with `status=PASS`, `hard_vetoes=[]`, GPU/TF32/JIT evidence, finite outputs, residuals pass, and paired thresholds pass. |
| Promotion veto | Any failure at `rank=32,epsilon=0.5` or adjacent default-neighborhood settings blocks moving to P10 until repaired or reclassified. |
| Continuation veto | Timeout without artifact, GPU memory failure, artifact mismatch, or evidence that compiled-redo route did not run. |
| Repair trigger | Failure at `rank=32` or `rank=64` for any tested epsilon; this triggers candidate-policy narrowing or retuning. |
| Explanatory diagnostics | Runtime, warm ratio, residuals below threshold, per-seed deltas, and descriptively favorable settings. |
| What must not be concluded | No statistical ranking, no default readiness, no superiority, no posterior correctness, no HMC readiness. |

## Evidence Contract

Passing this narrowed grid permits classifying `rank=16,epsilon=1.0` as an
excluded weak setting and advancing to P10 stress testing.  Failing this grid
blocks default-readiness and requires candidate retuning.

## Skeptical Pre-Launch Audit

Status: `PASS_FOR_DEFAULT_NEIGHBORHOOD_REPAIR`

This repair does not move thresholds after seeing the failure.  It narrows the
candidate policy away from a weak low-rank/high-epsilon setting and tests the
intended default neighborhood using the same seeds, shape, comparator, dtype,
and thresholds as the full grid.  Timing remains descriptive only.

## Rows

| Row | Rank | Epsilon | Artifact suffix |
| --- | ---: | ---: | --- |
| 1 | `32` | `0.25` | `r32-eps0p25` |
| 2 | `32` | `0.5` | `r32-eps0p5` |
| 3 | `32` | `1.0` | `r32-eps1p0` |
| 4 | `64` | `0.25` | `r64-eps0p25` |
| 5 | `64` | `0.5` | `r64-eps0p5` |
| 6 | `64` | `1.0` | `r64-eps1p0` |

Output pattern:

- JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09-default-neighborhood-<suffix>-2026-06-23.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09-default-neighborhood-<suffix>-2026-06-23.md`

## Automatic Gated Execution Rule

After each row:

1. Read the JSON.
2. If `status=PASS` and `hard_vetoes=[]`, continue.
3. If a row fails, stop and write a repair result note.
4. Do not rank candidates by descriptive timing.
