# P87 Phase 9 Subplan: Final Claim Gate And Handoff

Date: 2026-06-26

Status: `REVIEWED_READY_FOR_PHASE9_EXECUTION`

## Phase Objective

Close P87 with one honest final claim level and a reset/handoff.

The expected final-claim decision must inherit:

- Phase 4 passed only a bounded horizon-0 SIR d18 fixed-branch value/gradient
  gate;
- Phase 5 passed only tiny d2 multistate full-history fixed-branch regression;
- Phase 7 blocked `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE` because degree
  convergence remains unresolved;
- Phase 8 blocked `D18_CORRECTNESS_CANDIDATE` because no same-target
  source-backed reference bridge exists in the audited artifacts.

Final-label selection is not a single total ordering because the labels mix
local fixed-branch analytical coverage and source-route execution coverage. The
Phase 9 result must therefore select exactly one headline label using this
tie-break rule:

1. If `D18_CORRECTNESS_CANDIDATE` passes, choose it.
2. Else if `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE` passes, choose it.
3. Else if `D18_SOURCE_ROUTE_EXECUTION_ONLY` is reviewed-supported, choose it
   as the headline d18 source-route label, while also preserving Phase 4/5
   fixed-branch analytical evidence in a separate secondary-evidence row.
4. Else if `FIXED_BRANCH_ANALYTICAL_TINY_FULL_HISTORY_ONLY` passes, choose it.
5. Else if `FIXED_BRANCH_ANALYTICAL_HORIZON0_ONLY` passes, choose it.
6. Else choose `JVP_BACKED_DIAGNOSTIC_ONLY`.

Given the reviewed Phase 7/8 blockers, Phase 9 is expected to select
`D18_SOURCE_ROUTE_EXECUTION_ONLY` unless a local check finds stale or
unreviewed evidence.

## Entry Conditions Inherited From Previous Phase

- Phases 0-8 have either passed or produced explicit blocker results.
- No final claim is selected until evidence is mapped to allowed labels.
- Phase 9 starts only after the Phase 8 result and this refreshed Phase 9
  subplan receive read-only review.

## Required Artifacts

- Phase 9 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase9-final-claim-gate-result-2026-06-26.md`
- Updated visible stop handoff:
  `docs/plans/bayesfilter-highdim-zhao-cui-p87-visible-stop-handoff-2026-06-26.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p87-visible-execution-ledger-2026-06-26.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p87-claude-review-ledger-2026-06-26.md`
- Decision table section embedded in the Phase 9 result, mapping every allowed
  label to pass/block status, blocker, and evidence anchor.
- Run/check manifest section embedded in the Phase 9 result.
- Final stop-handoff section embedded in the visible stop handoff, preserving
  the selected headline label, secondary fixed-branch evidence, blocked
  stronger labels, successor-program recommendations, and nonclaims.

## Required Checks/Tests/Reviews

Pre-write checks:

```bash
set -euo pipefail
rg -n "JVP_BACKED_DIAGNOSTIC_ONLY|FIXED_BRANCH_ANALYTICAL_HORIZON0_ONLY|FIXED_BRANCH_ANALYTICAL_TINY_FULL_HISTORY_ONLY|D18_SOURCE_ROUTE_EXECUTION_ONLY|D18_SOURCE_ROUTE_RANK_DEGREE_STABLE|D18_CORRECTNESS_CANDIDATE" docs/plans/bayesfilter-highdim-zhao-cui-p87*.md
rg -n "P87_PHASE4_HORIZON0_D18_VALUE_GRADIENT_PASS_REVIEWED_CLOSED|P87_PHASE5_TINY_FULL_HISTORY_PASS_REVIEWED_CLOSED|P87_PHASE7_BLOCKS_D18_SOURCE_ROUTE_RANK_DEGREE_STABLE_REVIEWED_CLOSED|P87_PHASE8_BLOCK_SOURCE_ROUTE_REFERENCE_BRIDGE_MISSING" docs/plans/bayesfilter-highdim-zhao-cui-p87*.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p87*.md
```

Post-write checks:

```bash
set -euo pipefail
rg -n "selected_headline_label|blocked_stronger_labels|secondary_fixed_branch_evidence|D18_SOURCE_ROUTE_EXECUTION_ONLY|D18_SOURCE_ROUTE_RANK_DEGREE_STABLE|D18_CORRECTNESS_CANDIDATE" docs/plans/bayesfilter-highdim-zhao-cui-p87-phase9-final-claim-gate-result-2026-06-26.md docs/plans/bayesfilter-highdim-zhao-cui-p87-visible-stop-handoff-2026-06-26.md
rg -n "Phase 9|P87_PHASE9|selected_headline_label|VERDICT: AGREE|VERDICT: REVISE" docs/plans/bayesfilter-highdim-zhao-cui-p87-visible-execution-ledger-2026-06-26.md docs/plans/bayesfilter-highdim-zhao-cui-p87-claude-review-ledger-2026-06-26.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p87*.md
```

Claude review required for final claim gate.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the strongest honest Zhao-Cui SIR d18 value/gradient/source-route claim supported by P87? |
| Baseline/comparator | P87 phase results and prior P81/P83/P86 blockers, especially Phase 7 rank/degree blocker and Phase 8 missing-bridge blocker. |
| Primary criterion | Exactly one headline final label is selected by the tie-break rule, every allowed label has an explicit pass/block row, and all nonclaims/blockers are preserved. |
| Veto diagnostics | Stronger label than evidence, missing unresolved blocker, unreviewed claim, stale artifact, Phase 7/8 blocker bypass, local fixed-branch evidence promoted to source-route correctness. |
| Explanatory diagnostics | Phase ledger and review trail. |
| Not concluded | Any claim not listed in the final label and nonclaim table. |
| Artifact | Final result, stop handoff, execution ledger, and Claude review ledger. |

## Allowed Final Labels

- `JVP_BACKED_DIAGNOSTIC_ONLY`
- `FIXED_BRANCH_ANALYTICAL_HORIZON0_ONLY`
- `FIXED_BRANCH_ANALYTICAL_TINY_FULL_HISTORY_ONLY`
- `D18_SOURCE_ROUTE_EXECUTION_ONLY`
- `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE`
- `D18_CORRECTNESS_CANDIDATE`

## Forbidden Claims/Actions

- Do not introduce new experiments in closeout.
- Do not promote unresolved blockers.
- Do not make production/HMC/posterior/default-readiness claims.
- Do not use Phase 4/5 local fixed-branch evidence as source-route correctness.
- Do not use P86 favorable degree-comparator evidence as degree convergence.
- Do not use P83/P87 execution-only evidence as correctness.

## Exact Next-Phase Handoff Conditions

No next P87 phase. The result must state any recommended successor program.
The stop handoff must preserve the selected final label, all blocked stronger
labels, and the evidence needed for a successor program.

## Stop Conditions

- Final label cannot be chosen without changing criteria.
- Phase 8 result remains unreviewed.
- More than one headline label is selected, or the selected headline label
  conflicts with the decision table.
- Stop handoff does not preserve blocked stronger labels or secondary
  fixed-branch evidence.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Run pre-write local checks.
2. Write Phase 9 result/close record.
3. Update final stop handoff.
4. Update execution ledger and Claude review ledger.
5. Run post-write structural/local checks.
6. Review closeout for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
