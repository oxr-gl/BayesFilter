# P08 Final Promotion Decision Subplan

Date: 2026-06-24

Status: `PROVISIONAL_PENDING_P07_RESULT_AND_REFRESH`

## Phase Objective

Synthesize P01-P07 evidence into one scoped final promotion decision without
overclaiming beyond the tested model suite and approved boundaries.

## Entry Conditions Inherited From Previous Phase

- P00 through P07 results or blocker/skip records exist.
- Candidate lock history is recorded.
- All material Claude reviews are recorded.
- No unresolved hard veto is hidden.

## Required Artifacts

- Final result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-result-2026-06-24.md`
- Updated execution ledger.
- Updated Claude review ledger.
- Updated stop handoff.

## Required Checks, Tests, And Reviews

- Phase artifact existence scan.
- Boundary scan for unsupported claims.
- Review all phase result decision tables and inference-status tables.
- Confirm whether P07 was skipped or passed before any HMC wording.
- Claude Opus/max read-only final review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What scoped promotion verdict is justified by the completed model-suite evidence? |
| Baseline/comparator | P01-P07 phase-local comparators and exact references. |
| Primary pass criterion | Final result accurately reflects passed/failed/skipped phases, preserves nonclaims, and Claude final review returns `VERDICT: AGREE`. |
| Veto diagnostics | Missing phase result, unsupported claim, hidden failed gate, inflated HMC/API/default/scientific claim, or review nonconvergence. |
| Explanatory diagnostics | Phase metrics and descriptive timings summarized with statistical humility. |
| Not concluded | Anything not explicitly passed by phase gates, especially statistical superiority, broad scientific validity, public API readiness, package default readiness, and HMC readiness if P07 skipped. |
| Artifact | Final result, ledgers, stop handoff. |

## Forbidden Claims And Actions

- Do not promote beyond evidence.
- Do not claim HMC readiness unless P07 approved runtime passed.
- Do not claim package/public API readiness unless a separate public/API phase
  exists and passed.
- Do not claim statistical superiority without uncertainty evidence.
- Do not change code, defaults, package metadata, model files, or dependencies
  in P08.

## Exact Next-Phase Handoff Conditions

This is the terminal phase. The final handoff must state:

- final phase reached;
- final status;
- result artifacts;
- Claude review trail;
- tests/benchmarks actually run;
- unresolved blockers;
- what was not concluded;
- safest next human decision.

## Stop Conditions

- Missing required phase artifacts.
- Any hard veto unresolved.
- Claude final review does not converge within five rounds for the same
  blocker.
- Final result would need to cross a default/API/package/HMC/scientific boundary
  not authorized by passed phase evidence.

## End-Of-Subplan Procedure

1. Run required final local checks.
2. Write final result or blocker result.
3. Update stop handoff.
4. Run Claude final read-only review and repair if needed.
