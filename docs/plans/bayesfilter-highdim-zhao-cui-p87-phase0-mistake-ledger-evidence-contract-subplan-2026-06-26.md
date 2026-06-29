# P87 Phase 0 Subplan: Mistake Ledger And Evidence Contract

Date: 2026-06-26

Status: `REVIEWED_READY_FOR_PHASE0_GOVERNANCE_EXECUTION`

## Phase Objective

Freeze the prior Zhao-Cui SIR d18 mistakes as binding blockers and write the
evidence contract for the rest of P87 before any implementation, experiment, or
long diagnostic run.

## Entry Conditions Inherited From Previous Phase

- P87 master program and visible runbook exist.
- No P87 phase has executed.
- Current known status includes P81 JVP-backed/horizon-0 limitations, P83
  source-route execution-only boundary, and P86 training-base/L1/rank-degree
  discipline.

## Required Artifacts

- Phase 0 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase0-mistake-ledger-evidence-contract-result-2026-06-26.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p87-visible-execution-ledger-2026-06-26.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p87-claude-review-ledger-2026-06-26.md`
- Phase 1 subplan, refreshed if Phase 0 changes the route audit scope:
  `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase1-current-route-audit-subplan-2026-06-26.md`

## Canonical Mistake Ledger

Phase 0 must preserve this table in its result. A phase cannot pass if any row
lacks a blocker, forbidden claim/action, artifact evidence, or downstream gate.

| Prior mistake | Blocker ID | Forbidden claim/action | Required Phase 0 evidence | Downstream gate |
| --- | --- | --- | --- | --- |
| Horizon-0 d18 smoke treated as full-history validation | `BLOCK_HORIZON0_OVERCLAIM` | Do not call one-row/horizon-0 evidence full filtering likelihood or full SIR d18 validation. | Cite P81 horizon-0 limitation and include blocker in result. | Phase 4 may say horizon-0 only; Phase 5 required before full-history tiny claim; Phase 6 required before d18 full-history route claim. |
| JVP/`ForwardAccumulator` treated as analytical Zhao-Cui gradient | `BLOCK_ANALYTICAL_ROUTE_HAS_JVP_COMPONENT` | Do not call a route analytical if promoted filter-score path still uses JVP/autodiff. | Cite current route-string audit requirement and include blocker in result. | Phase 1 route audit; Phase 2 repair/block before analytical-gradient promotion. |
| Dense all-pairs or streamed all-pairs treated as feasible d18 route | `BLOCK_D18_ALL_PAIRS_DRIFT` | Do not use dense all-pairs, streamed all-pairs, or "increase memory" as the d18 full-history solution. | Cite P81 Phase 9 scaling lesson and include blocker in result. | Phase 6 feasibility gate must select non-all-pairs route or block. |
| ESS, finite replay, fit loss, FD rows, or validation residuals treated as correctness | `BLOCK_PROXY_PROMOTION` | Do not promote proxy diagnostics to correctness, convergence, HMC readiness, or production readiness. | Include proxy/nonclaim rule in result. | Phases 4, 7, and 8 must preserve diagnostic-only roles unless a reference bridge exists. |
| Local/operator route treated as source-faithful Zhao-Cui | `BLOCK_SOURCE_CLAIM_UNGROUNDED` | Do not call local/operator/all-grid routes source-faithful without paper/source anchors and classification. | Include source-claim rule in result. | Phase 6 route classification; Phase 8 same-target source-backed bridge. |
| ALS training revived after training-base decision | `BLOCK_ALS_REVIVAL` | Do not use or revive historical ALS training for fixed-variant Zhao-Cui fitting. | Include ALS exclusion in result. | Phase 7 P86 training-base/L1 discipline. |
| Training run without L1 tuning, validation/holdout/audit split, scheduler, or sample-budget discipline | `BLOCK_TRAINING_DISCIPLINE_MISSING` | Do not run/interpret fitted source-route evidence without training-base, L1 tuning policy, holdout/audit separation, scheduler, sample budget, and no audit tuning. | Include training-discipline rule in result. | Phase 7 rank/degree gate and any later fit preflight. |

## Required Checks/Tests/Reviews

Pre-execution checks:

```bash
set -euo pipefail

test -f docs/plans/bayesfilter-highdim-zhao-cui-p87-sir-d18-analytical-gradient-source-route-master-program-2026-06-26.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p87-visible-gated-overnight-execution-plan-2026-06-26.md
for path in \
  docs/plans/bayesfilter-highdim-zhao-cui-p87-sir-d18-analytical-gradient-source-route-master-program-2026-06-26.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p87-visible-gated-overnight-execution-plan-2026-06-26.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p87-phase0-mistake-ledger-evidence-contract-subplan-2026-06-26.md; do \
  for token in \
    BLOCK_HORIZON0_OVERCLAIM \
    BLOCK_ANALYTICAL_ROUTE_HAS_JVP_COMPONENT \
    BLOCK_D18_ALL_PAIRS_DRIFT \
    BLOCK_PROXY_PROMOTION \
    BLOCK_SOURCE_CLAIM_UNGROUNDED \
    BLOCK_ALS_REVIVAL \
    BLOCK_TRAINING_DISCIPLINE_MISSING; do \
    rg -n "$token" "$path"; \
  done; \
done
rg -n "ForwardAccumulator|target_derivative_backend|tensorflow_forward_accumulator_for_model_log_density" bayesfilter/highdim/filtering.py docs/plans/bayesfilter-highdim-zhao-cui-p81-analytical-derivative-route-correction-2026-06-22.md
rg -n "streamed all-pairs|all-pairs|quadratic|COMPLEXITY_GATE" docs/plans/bayesfilter-highdim-zhao-cui-p81-phase9-representation-scaling-result-2026-06-21.md tests/highdim/test_p81_analytical_sir_score.py bayesfilter/highdim/filtering.py
rg -n "Phase 1 is read-only except result/ledger/subplan documentation" docs/plans/bayesfilter-highdim-zhao-cui-p87-phase1-current-route-audit-subplan-2026-06-26.md
rg -n "Do not edit code in Phase 1" docs/plans/bayesfilter-highdim-zhao-cui-p87-phase1-current-route-audit-subplan-2026-06-26.md
rg -n "Do not run long tests or GPU commands" docs/plans/bayesfilter-highdim-zhao-cui-p87-phase1-current-route-audit-subplan-2026-06-26.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p87*.md
```

Closeout checks after writing the Phase 0 result:

```bash
set -euo pipefail

test -f docs/plans/bayesfilter-highdim-zhao-cui-p87-phase0-mistake-ledger-evidence-contract-result-2026-06-26.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p87-visible-execution-ledger-2026-06-26.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p87-claude-review-ledger-2026-06-26.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p87-phase1-current-route-audit-subplan-2026-06-26.md
for token in \
  BLOCK_HORIZON0_OVERCLAIM \
  BLOCK_ANALYTICAL_ROUTE_HAS_JVP_COMPONENT \
  BLOCK_D18_ALL_PAIRS_DRIFT \
  BLOCK_PROXY_PROMOTION \
  BLOCK_SOURCE_CLAIM_UNGROUNDED \
  BLOCK_ALS_REVIVAL \
  BLOCK_TRAINING_DISCIPLINE_MISSING; do \
  rg -n "$token" docs/plans/bayesfilter-highdim-zhao-cui-p87-phase0-mistake-ledger-evidence-contract-result-2026-06-26.md; \
done
rg -n "P87_PHASE0_MISTAKE_LEDGER_EVIDENCE_CONTRACT_PASSED" docs/plans/bayesfilter-highdim-zhao-cui-p87-visible-execution-ledger-2026-06-26.md
rg -n "Phase 0 blocker ledger/check summary" docs/plans/bayesfilter-highdim-zhao-cui-p87-visible-execution-ledger-2026-06-26.md
rg -n "Phase 1 handoff" docs/plans/bayesfilter-highdim-zhao-cui-p87-visible-execution-ledger-2026-06-26.md
rg -n "^Phase 0 Subplan Review - Iteration [0-9]+ Verdict: VERDICT: AGREE$" docs/plans/bayesfilter-highdim-zhao-cui-p87-claude-review-ledger-2026-06-26.md
rg -n "^Phase 0 Result Review - Iteration [0-9]+ Verdict: VERDICT: AGREE$" docs/plans/bayesfilter-highdim-zhao-cui-p87-claude-review-ledger-2026-06-26.md
rg -n "Phase 1 is read-only except result/ledger/subplan documentation" docs/plans/bayesfilter-highdim-zhao-cui-p87-phase1-current-route-audit-subplan-2026-06-26.md
rg -n "Do not edit code in Phase 1" docs/plans/bayesfilter-highdim-zhao-cui-p87-phase1-current-route-audit-subplan-2026-06-26.md
rg -n "Do not run long tests or GPU commands" docs/plans/bayesfilter-highdim-zhao-cui-p87-phase1-current-route-audit-subplan-2026-06-26.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p87*.md
```

Review:

- Claude read-only bounded review of this subplan is required before Phase 0
  execution.
- Claude read-only bounded review of the Phase 0 result is required before
  Phase 1 execution.
- The only review pass token is `VERDICT: AGREE`.
- Any `VERDICT: REVISE`, missing verdict, or ambiguous verdict blocks
  progression until the issue is patched, focused checks are rerun, and bounded
  review is repeated.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does P87 correctly freeze the old mistakes as blockers before execution? |
| Baseline/comparator | P81 route correction, P81 Phase 3/5/9 notes, P83 reset/visible handoff, P86 Phase 6T/6Y results, current code route strings. |
| Primary criterion | Every canonical mistake-ledger row has a named blocker, forbidden promotion, artifact evidence, and downstream phase gate. |
| Veto diagnostics | Missing JVP blocker, missing all-pairs blocker, stale Phase 7 execution-only status, or allowing proxy metrics as correctness. |
| Explanatory diagnostics | Artifact inventory, grep hits, current code route strings, all-pairs/scaling blocker hits. |
| Not concluded | No analytical-gradient correctness, no source-route correctness, no full-history feasibility, no production readiness. |
| Artifact | Phase 0 result and ledger update. |

## Forbidden Claims/Actions

- Do not edit algorithmic code.
- Do not run GPU, long fits, HMC, LEDH, or source-route validation.
- Do not claim current analytical-gradient readiness.
- Do not treat this governance phase as scientific evidence.

## Exact Next-Phase Handoff Conditions

Phase 1 may start only if:

- Phase 0 result records the blocker ledger and evidence contract;
- pre-execution and closeout checks pass;
- Phase 0 subplan and Phase 0 result reviews converge or any review issue is
  patched visibly;
- `docs/plans/bayesfilter-highdim-zhao-cui-p87-visible-execution-ledger-2026-06-26.md`
  records the Phase 0 blocker ledger/check summary and Phase 1 handoff;
- `docs/plans/bayesfilter-highdim-zhao-cui-p87-claude-review-ledger-2026-06-26.md`
  records the Phase 0 subplan and result review outcomes;
- Phase 1 subplan still targets a read-only route audit.

## Stop Conditions

- Any prior mistake lacks a blocker or forbidden-claim rule.
- Any canonical mistake-ledger row lacks artifact evidence or downstream gate.
- Current status cannot distinguish execution-only from correctness.
- Claude review does not converge after five rounds for the same issue.

## Repair Loop

If a local check or Claude review fails:

1. Record the failure in the Claude review ledger or execution ledger.
2. Patch the smallest affected artifact, usually this subplan or the Phase 0
   result.
3. Rerun the focused failed local check plus `git diff --check`.
4. Resubmit the same bounded review question with an incremented iteration
   number.
5. Stop with a blocker result after five review rounds for the same issue.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write the Phase 0 result/close record.
3. Draft or refresh the Phase 1 subplan.
4. Review Phase 1 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
