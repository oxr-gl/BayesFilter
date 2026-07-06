# P03 Paired Actual-SIR Ladder Subplan

Status: `DRAFT_FOR_REVIEW`

## Phase Objective

Run paired same-seed actual-SIR d18 streaming versus low-rank rows on feasible
particle counts to test validity, bounded comparability, and practical
resource evidence before large-N envelope runs.

## Entry Conditions Inherited From Previous Phase

- P02 smoke passed.
- Trusted GPU context is available for GPU claims.
- GPU1 is preferred via `CUDA_VISIBLE_DEVICES=1`; GPU0 may be used only if GPU1
  is busy/unavailable and the artifact records that fallback.
- Each paired row used for support must run streaming and low-rank on the same
  physical GPU UUID. If fallback changes the physical GPU between routes, that
  row is explanatory-only until rerun on one physical GPU.

## Required Artifacts

- Paired ladder JSON/Markdown aggregate:
  `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21.json`
  and `.md`
- Row JSON/Markdown sidecars.
- P03 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p03-paired-ladder-result-2026-06-21.md`
- Refreshed P04 subplan.

## Required Checks, Tests, Reviews

- GPU status check with `nvidia-smi`.
- Paired rows, subject to runtime budget:
  - `B=5,T=20,N=1024`
  - `B=5,T=20,N=4096`
  - `B=5,T=20,N=10000`
  - optional `N=20000` or `N=32768` only if earlier rows justify runtime.
- Same seeds: `81120,81121,81122,81123,81124`.
- Same observations, callbacks, dtype, TF32 mode, and physical GPU UUID for
  paired support rows.
- Exact timing protocol for rows used by the speed screen:
  `warmups=1`, `repeats=3`; compile/first call is recorded separately and is
  not counted in the warm-median speed screen.
- Streaming timing for the P03 speed screen must use the existing compiled
  streaming actual-SIR core via harness option
  `--streaming-timing-source compiled_core`; the owned streaming diagnostic loop
  remains route-fired/comparability evidence and its runtime is explanatory.
- Timeout-boundary commands use exact outer wall-clock timeout `3600s` per
  route-row command, measured from process launch and including TF import,
  compile/first call, warmups/repeats, diagnostics, and artifact writes.
  Timeout evidence is resource-boundary evidence only and is usable only after
  at least two adjacent smaller paired rows pass validity/comparability.
- GPU provenance manifest must record requested `CUDA_VISIBLE_DEVICES`,
  selected physical GPU index, GPU name, GPU UUID when available,
  `nvidia-smi` status, logical TensorFlow devices, and explicit fallback status.
- Claude review if the result supports a bounded efficiency claim or requires
  repairing thresholds/interpretation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | On feasible paired actual-SIR rows, does low-rank preserve validity/comparability and show practical runtime/timeout evidence versus streaming? |
| Baseline/comparator | Streaming actual-SIR route on the same seeds/rows. |
| Primary pass criterion | Paired rows used for support pass hard validity and predeclared engineering-comparability gates from the master program; at least two adjacent paired rows show streaming warm median / low-rank warm median `>= 1.25` under exact `warmups=1`, `repeats=3` on the same physical GPU UUID. Timeout-boundary evidence may support only a resource-boundary addendum after at least two adjacent smaller paired rows pass validity/comparability. |
| Veto diagnostics | Nonfinite outputs, GPU/TF32 mismatch, missing physical GPU provenance, route fallback, missing actual-SIR semantics, low-rank dense materialization, invalid factors, paired comparability failure for support rows. |
| Explanatory diagnostics | Runtime outside the predeclared warm-median screen, memory, compile time, ESS above the hard floor, log-likelihood delta below the paired veto threshold, filtered-summary deltas below the paired veto threshold, projection iterations. |
| Not concluded | No posterior correctness, no statistical ranking, no default readiness. |
| Artifact | Paired ladder aggregate, row sidecars, P03 result. |

## Forbidden Claims/Actions

- Do not rank methods statistically without uncertainty evidence.
- Do not use a row with failed comparability to support efficiency promotion.
- Do not use unpaired large-N low-rank-only rows as direct speed comparison.
- Do not count compile-inclusive timing as the warm-time speed screen.
- Do not use a paired row for promotion if streaming and low-rank ran on
  different physical GPU UUIDs.
- Do not use timeout evidence as same-row comparability evidence.

## Exact Next-Phase Handoff Conditions

Advance to P04 only if P03 produces a valid paired basis for deciding whether
large-N low-rank envelope runs are justified. If paired comparability fails but
the route runs, hand off as `TUNING_REQUIRED` unless a reviewed repair is
already in scope.

## Stop Conditions

- `TUNING_REQUIRED` if low-rank runs but paired comparability or practical
  resource evidence fails.
- `REJECT_CURRENT_ROUTE` if hard validity/factor diagnostics fail.
- Stop for human direction if large-N execution would exceed approved resource
  budget or require changing criteria after seeing results.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write the P03 phase result.
3. Draft or refresh P04.
4. Review P04 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
