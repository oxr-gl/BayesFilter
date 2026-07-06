# P03 Conditional Microprobe Subplan

Status: `DRAFT_CONDITIONAL_NOT_LAUNCHED`

## Phase Objective

Run the smallest implementation-neutral microprobe only if P02 cannot classify
the route timing asymmetry from existing artifacts and source inspection.

## Entry Conditions Inherited From Previous Phase

P02 result must explicitly state `SOURCE_UNCLEAR_NEEDS_MICROPROBE`. P02 must
also state why artifact and source evidence are insufficient.

## Required Artifacts

- Optional P03 microprobe JSON:
  `docs/benchmarks/actual-sir-low-rank-repair-classification-p03-microprobe-2026-06-22.json`
- Optional P03 microprobe Markdown:
  `docs/benchmarks/actual-sir-low-rank-repair-classification-p03-microprobe-2026-06-22.md`
- Optional P03 log:
  `docs/benchmarks/logs/actual-sir-low-rank-repair-classification-p03-microprobe-2026-06-22.log`
- P03 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p03-conditional-microprobe-result-2026-06-22.md`

## Required Checks/Tests/Reviews

- Claude read-only review of this conditional subplan before execution.
- Trusted GPU precheck only if the microprobe uses GPU/CUDA.
- Exact command must be written into the P03 result before interpretation.
- The command must be bounded to one P03 comparable candidate, one seed, and
  smoke-size or existing P03 shape only.
- The command must not edit solver, streaming route, or wrapper code.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What one smallest runtime diagnostic separates timing-source asymmetry from artifact/source ambiguity? |
| Baseline/comparator | P03 comparable candidate and existing benchmark command shape. |
| Primary pass criterion | The microprobe answers only whether an implementation-neutral timing ambiguity remains. |
| Veto diagnostics | Need for source edit, package install, network, long benchmark, held-out support, untrusted GPU evidence, or missing artifact/log. |
| Explanatory diagnostics | First-call time, warm-call time, route selected, timing source, and bounded traceback if any. |
| Not concluded | No speedup, compile feasibility, route repair correctness, candidate freeze, or promotion. |
| Artifact | P03 microprobe artifact/log and P03 result. |

## Forbidden Claims/Actions

- Do not modify implementation.
- Do not run a tuning grid.
- Do not run held-out support.
- Do not claim performance improvement or route readiness.

## Exact Next-Phase Handoff Conditions

Advance to P04 only after P03 writes a bounded result classifying whether the
next repair should be route-performance-first, tuning-first, both, or blocked.

## Stop Conditions

- Stop if the microprobe would require implementation edits.
- Stop if trusted GPU is required but unavailable.
- Stop after five unresolved Claude review rounds for this microprobe blocker.

## End-Of-Subplan Duties

1. Run required local checks if P03 is launched.
2. Write the P03 phase result or a `NOT_LAUNCHED_NOT_NEEDED` result.
3. Draft or refresh P04.
4. Review P04 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
