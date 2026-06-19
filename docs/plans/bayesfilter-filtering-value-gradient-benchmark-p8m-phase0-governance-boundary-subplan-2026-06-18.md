# P8m Phase 0 Subplan: Governance And Generic Boundary Contract

metadata_date: 2026-06-18
status: DRAFT
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-generic-transport-core-optimization-master-program-2026-06-18.md
phase: 0

## Phase Objective

Establish that P8m is a generic transport-core optimization lane and that SIR
d18 is only a stress fixture.

## Entry Conditions Inherited From Previous Phase

- P8l result exists and states active transport dominates the coarse trusted-GPU
  profile.
- No P8m implementation has started.

## Required Artifacts

- Phase 0 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase0-governance-boundary-result-2026-06-18.md`

## Required Checks/Tests/Reviews

```bash
test -f docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-transport-core-profiling-result-2026-06-18.md
rg -n "SIR d18 is only a stress fixture|SIR-specific|lower Sinkhorn" docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-*
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-*
```

Claude review is required before Phase 0 closes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is P8m scoped as generic transport-core work rather than SIR d18 specialization? |
| Baseline/comparator | P8l result and current transport code anchors. |
| Primary criterion | P8m artifacts explicitly forbid SIR-specific generic-engine changes and separate exact implementation from tuning/extension claims. |
| Veto diagnostics | Missing SIR-specific stop condition, lower-iteration promotion, GPU trust gap, or hidden default-policy change. |
| Explanatory diagnostics | Text anchors and phase structure. |
| Not concluded | No implementation success, runtime improvement, particle adequacy, or default readiness. |

## Forbidden Claims/Actions

- Do not edit algorithm code in Phase 0.
- Do not run GPU benchmarks in Phase 0.
- Do not claim P8m has optimized anything yet.

## Exact Next-Phase Handoff Conditions

Phase 1 may proceed only after local checks pass and Claude agrees the generic
boundary is explicit.

## Stop Conditions

Stop if the plan cannot prevent SIR-specific shortcuts from being labeled
generic, or if Claude finds a material boundary issue that does not converge.
