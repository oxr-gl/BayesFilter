# Actual-SIR Low-Rank Route-Performance Repair Subplan

Status: `DRAFT_NEXT_PROGRAM_NOT_LAUNCHED`

## Phase Objective

Design and execute the smallest route-performance repair that can separate
diagnostic-loop/eager overhead from low-rank solver math for actual-SIR
comparable candidates, without changing scientific gates or making promotion
claims.

## Entry Conditions Inherited From Previous Phase

The repair-classification program ended with `BOTH_REPAIRS` and
`ROUTE_TIMING_ASYMMETRY_SUPPORTED`. P03 tuning artifacts remain no-freeze:
Stage B, P04, P05, and P06 from the earlier tuning master are still forbidden.

## Required Artifacts

- Route-performance repair result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-route-performance-repair-result-2026-06-22.md`
- Optional implementation diff, only inside this reviewed write set:
  `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py`
  and focused tests under `tests/`.
- Optional microbenchmark JSON/Markdown:
  `docs/benchmarks/actual-sir-low-rank-route-performance-repair-*.json`
  and `.md`
- Optional logs:
  `docs/benchmarks/logs/actual-sir-low-rank-route-performance-repair-*.log`

## Required Checks/Tests/Reviews

- Read and restate the P01/P02 classification results before edits.
- If implementing, add the smallest benchmark-only path or probe; do not edit
  low-rank solver internals unless a later reviewed implementation subplan
  explicitly permits it.
- Run focused tests for any changed benchmark/wrapper code.
- If any GPU/CUDA timing evidence is needed, run in trusted/elevated context and
  record physical GPU UUID, TF32 mode, dtype, shape, seed, command, and wall
  time.
- Claude read-only review before interpreting any implementation result as a
  repair outcome.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can benchmark-level route-performance repair remove or isolate diagnostic-loop/eager timing overhead for the low-rank route? |
| Baseline/comparator | P03 comparable candidate artifacts and current compiled streaming timing source. |
| Primary pass criterion | A bounded implementation/probe result records one of: `OVERHEAD_REDUCED`, `OVERHEAD_ISOLATED_NOT_REDUCED`, `OVERHEAD_STILL_PRESENT`, or `BLOCKED`, with the command, artifact path, focused checks, and next branch. |
| Veto diagnostics | Source edit outside write set, solver semantic change without authorization, missing artifact, untrusted GPU timing, comparability gates ignored, or speedup/default claim. |
| Explanatory diagnostics | First-call time, warm-call time, route invocations, host-sync barriers removed or remaining, source anchors, and compile/probe failure mode. |
| Not concluded | No candidate freeze, held-out support, posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, broad speedup claim, or statistical ranking. |
| Artifact | Route-performance repair result, optional benchmark artifacts/logs, and Claude review ledger. |

## Forbidden Claims/Actions

- Do not claim low-rank is faster or default-ready from this subplan.
- Do not run held-out support or large-N promotion rows.
- Do not erase the tuning/comparability/ESS repair lane.
- Do not edit the low-rank solver internals without a separate reviewed
  implementation subplan.
- Do not alter gates after seeing results.

## Exact Next-Phase Handoff Conditions

Handoff depends on the recorded result:

- `OVERHEAD_REDUCED`: write the route-performance repair result and hand off to
  a dedicated tuning/comparability/ESS repair subplan before any candidate
  freeze or held-out support.
- `OVERHEAD_ISOLATED_NOT_REDUCED`: write the route-performance repair result
  and hand off to a narrower route implementation subplan that may request
  solver-internal authorization if needed.
- `OVERHEAD_STILL_PRESENT`: write the route-performance repair result and stop
  for a narrower implementation plan or human direction.
- `BLOCKED`: write a blocker result and stop for clarification or approval.

## Stop Conditions

- Stop if the smallest repair requires solver-internal semantic changes.
- Stop if trusted GPU evidence is required but unavailable.
- Stop if focused tests fail and the failure cannot be isolated to the planned
  repair.
- Stop after five unresolved Claude review rounds for the same blocker.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write a phase result or blocker result.
3. Draft or refresh the next tuning/comparability/ESS subplan only if route
   performance repair produces a usable next artifact.
4. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
