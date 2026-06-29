# Phase 1 Subplan: Single-Target Scalar Contract Freeze

Date: 2026-06-29

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Freeze the reviewed single-target scalar contract so later phases cannot start
from implementation inertia, old two-lane wording, or passing tests on the wrong
scalar.

## Entry Conditions Inherited From Previous Phase

- Phase 0 launch artifacts exist and passed review.
- The inherited actual-SV reset and derivation anchors are recorded in the
  master program.
- No implementation, test rewrite, or benchmark phase has started.

## Required Artifacts

- Phase 0 result:
  `docs/plans/bayesfilter-actual-sv-single-target-phase0-program-launch-result-2026-06-29.md`
- Single-target contract:
  `docs/plans/bayesfilter-actual-sv-single-target-contract-2026-06-29.md`
- Execution ledger:
  `docs/plans/bayesfilter-actual-sv-single-target-visible-execution-ledger-2026-06-29.md`
- Phase 1 result:
  `docs/plans/bayesfilter-actual-sv-single-target-phase1-single-target-contract-result-2026-06-29.md`
- Refreshed Phase 2 subplan:
  `docs/plans/bayesfilter-actual-sv-single-target-phase2-derivation-chapter-reconciliation-subplan-2026-06-29.md`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
rg -n "Governing Scalar|Same-Target Comparator Class|Surrogate / Diagnostic / Historical Class|Explicit Veto Conditions|TESTS_PASSED_BUT_WRONG_QUESTION|Comparator Separation Rule" docs/plans/bayesfilter-actual-sv-single-target-contract-2026-06-29.md
git diff --check -- docs/plans/bayesfilter-actual-sv-single-target-contract-2026-06-29.md docs/plans/bayesfilter-actual-sv-single-target-phase1-single-target-contract-*.md
```

Claude review is required for:

- the single-target contract,
- the Phase 1 result,
- the Phase 2 subplan.

No runtime or implementation command is authorized.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the single-target scalar contract explicit enough that future phases cannot honestly confuse same-target, surrogate, KSC-only, and diagnostic-only evidence? |
| Baseline/comparator | 2026-06-28 single-target reset memo, 2026-06-29 derivation note, corrected chapter statements, and the reviewed documentary authority set. Current code target labels are explanatory-only alignment evidence and may not override the contract. |
| Primary criterion | Contract passes only if it freezes one scalar, one comparator classification scheme, explicit veto tags, and explicit phase consequences, and Claude review returns `VERDICT: AGREE`. |
| Veto diagnostics | multiple-target wording, missing surrogate/KSC separation, absent tests-passed-but-wrong-question veto, absent blocked-status preservation rule, or implied same-target Lane B admission before a route decision phase. |
| Explanatory diagnostics | grep coverage and cross-artifact wording alignment. |
| Not concluded | No route-decision outcome, no code/test/benchmark classification, no value or gradient pass. |
| Artifact | Reviewed contract, execution-ledger authority update, and Phase 1 result. |

## Forbidden Claims/Actions

- Do not imply the current Gaussian-closure route is already a valid same-target
  Lane B.
- Do not let tests, wrappers, benchmark schemas, or code labels outrank the
  contract artifact.
- Do not start Phase 2 or later work before this contract passes.

## Exact Next-Phase Handoff Conditions

Phase 2 may start only if:

- the contract receives Claude `VERDICT: AGREE`;
- the Phase 1 result records any wording changes or remaining caveats;
- the Phase 2 subplan is refreshed and reviewed;
- the execution ledger records the contract as the active scalar authority.

## Stop Conditions

- The contract still allows plausible re-promotion of wrong-scalar evidence.
- Claude review does not converge after five rounds.
- Continuing would require implementation or runtime work before the contract is
  settled.

## End-Of-Phase Requirements

1. Run the local contract-shape checks.
2. Write the Phase 1 result.
3. Refresh the Phase 2 subplan.
4. Review the contract, the Phase 1 result, and the Phase 2 subplan for drift-prevention completeness.
