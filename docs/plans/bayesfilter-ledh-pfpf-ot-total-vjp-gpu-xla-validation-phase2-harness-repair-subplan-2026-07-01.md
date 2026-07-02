# Phase 2 Subplan: Harness Repair If Needed

Date: 2026-07-01

Status: `DRAFT_CONDITIONAL`

## Phase Objective

If Phase 1 fails because no existing runner cleanly exercises the corrected
`transport_ad_mode="full"` route under GPU/XLA, implement the smallest harness
repair needed to run the Phase 1 smoke without changing the mathematical target.

## Entry Conditions Inherited From Previous Phase

- Phase 1 attempted and wrote a blocker result.
- The blocker is a harness or metadata issue, not evidence that the total
  derivative is mathematically unnecessary.

## Required Artifacts

- Phase 2 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase2-harness-repair-result-2026-07-01.md`.
- Any patched runner or wrapper script.
- Focused tests for changed runner behavior.
- Refreshed Phase 1 subplan if retrying the tiny smoke.

## Required Checks, Tests, Reviews

- `python -m py_compile` for any patched Python runner.
- Focused pytest for any added/changed test.
- Claude read-only review of the harness diff and result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the harness repair allow a faithful GPU/XLA full-route smoke without changing the finite scalar or derivative target? |
| Baseline/comparator | Phase 1 blocker and original CPU repair target. |
| Primary criterion | Patched harness records exact route metadata and can be used by Phase 1 retry. |
| Veto diagnostics | Repair changes mathematical target; hides stopped route as full route; lacks tests; broad refactor; output metadata insufficient. |
| Explanatory diagnostics | CLI parsing, route metadata, compile success. |
| Not concluded | No GPU viability until Phase 1 retry passes. |
| Artifact preserving result | Phase 2 result markdown and code diff. |

## Forbidden Claims And Actions

- Do not change derivative target.
- Do not remove route metadata.
- Do not introduce broad refactors.
- Do not proceed to ladder without rerunning Phase 1.

## Exact Next-Phase Handoff Conditions

Return to Phase 1 if:

- harness repair passes checks;
- Claude returns `VERDICT: AGREE`;
- Phase 1 command is refreshed with exact paths.

Stop if:

- repair requires changing the algorithmic target;
- XLA/GPU failure is not a harness problem;
- review fails to converge after five rounds.

## Stop Conditions

- Nonfixable XLA incompatibility in the current total-route implementation.
- Need for hand-coded total VJP beyond a small harness repair.
- User approval required for package/environment changes.
