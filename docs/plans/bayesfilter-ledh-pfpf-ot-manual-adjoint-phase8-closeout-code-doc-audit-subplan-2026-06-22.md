# Manual Adjoint Phase 8 Subplan: Closeout And Code-Doc Audit

status: DRAFT_READY_AFTER_M7_BLOCKER_RESULT
date: 2026-06-22
phase: M8-CLOSEOUT

## Phase Objective

Close the manual-adjoint/custom-gradient program with a code-doc consistency
audit, limitations ledger, and final handoff to either P82 validation or a
specific blocker.

## Entry Conditions

- M7 result is complete.
- P82 return is explicitly blocked by benchmark wiring.
- All implementation phases have written results and checks.

## Required Artifacts

- Closeout result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase8-closeout-code-doc-audit-result-2026-06-22.md`
- Final visible stop handoff update:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-visible-stop-handoff-2026-06-22.md`
- Code-doc consistency audit note if implementation/chapter files changed.

## Required Checks / Tests / Reviews

- Run final focused tests identified by M7.
- Run `git diff --check` on touched files.
- If docs/chapter files changed, run the reviewed document build/check
  specified by the phase result.
- Review unsupported claims across new artifacts.
- Claude one-path read-only final review if implementation or scientific
  handoff claims changed materially.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Are the manual-adjoint artifacts, code, tests, docs, limitations, and downstream handoff internally consistent? |
| Baseline/comparator | M0-M7 phase results, implementation diffs, tests, and documentation artifacts. |
| Primary criterion | Closeout records final status, tests actually run, supported/unsupported modes, unresolved blockers, and what downstream P82 may or may not do. |
| Veto diagnostics | Unsupported claims; missing tests; code-doc mismatch; stale runbook status; missing handoff; overclaiming HMC/default/posterior readiness. |
| Explanatory diagnostics | Test list, review trail, code paths, doc paths, and limitation table. |
| Not concluded | Any claim not explicitly supported by phase evidence remains forbidden. |

## Forbidden Claims / Actions

- Do not broaden supported modes at closeout.
- Do not claim P82 passed unless P82 actually ran and passed separately.
- Do not claim HMC/default/posterior readiness without separate evidence.
- Do not hide blockers.

## Next-Phase Handoff Conditions

Final handoff must state one of:

- `MANUAL_ADJOINT_READY_FOR_P82`;
- `MANUAL_ADJOINT_BLOCKED`;
- `MANUAL_ADJOINT_PARTIAL_PRIMITIVE_ONLY`.

For the current M7 outcome, the expected final status is:

- `MANUAL_ADJOINT_LOCAL_ROUTE_PASSED_P82_WIRING_BLOCKED`.

It must include exact next action and stop conditions.

## Stop Conditions

Stop if code-doc consistency cannot be checked, if final tests fail, if review
finds unsupported claims that cannot be fixed safely, or if downstream P82
instructions would require human approval.
