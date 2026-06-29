# P87 Phase 0 Result: Mistake Ledger And Evidence Contract

Date: 2026-06-26

Status: `P87_PHASE0_MISTAKE_LEDGER_EVIDENCE_CONTRACT_PASSED_REVIEWED`

## Decision

Phase 0 passes as a governance-only closeout after the human-directed blocker
repair cycle.

This phase did not edit algorithmic code, run GPU commands, run long fits, run
HMC, run LEDH, or execute source-route validation. It only froze the prior
Zhao-Cui SIR d18 mistakes as explicit no-regression blockers and preserved the
evidence contract for later phases.

## Blocker Repair History

The original Phase 0 subplan review reached five `VERDICT: REVISE` rounds
because the check snippets were not fail-closed and the review-verdict checks
were not exact-line anchored.

After the user directed continuation, Codex patched the subplan so:

- pre-execution and closeout check blocks begin with `set -euo pipefail`;
- blocker checks iterate over exact artifact paths and exact blocker tokens;
- Phase 0 subplan/result review checks require exact-line anchored
  `VERDICT: AGREE` tokens;
- the stale iteration-4 status was removed.

Claude reviewed only this repair and returned `VERDICT: AGREE` in Phase 0
Subplan Review Iteration 6.

## Canonical Mistake Ledger

| Prior mistake | Blocker ID | Forbidden claim/action | Required downstream gate |
| --- | --- | --- | --- |
| Horizon-0 d18 smoke treated as full-history validation | `BLOCK_HORIZON0_OVERCLAIM` | Do not call one-row or horizon-0 evidence full filtering likelihood or full SIR d18 validation. | Phase 4 may claim horizon-0 only; Phase 5 is required before tiny full-history claim; Phase 6 is required before d18 full-history route claim. |
| JVP/`ForwardAccumulator` treated as analytical Zhao-Cui gradient | `BLOCK_ANALYTICAL_ROUTE_HAS_JVP_COMPONENT` | Do not call a route analytical if the promoted filter-score path still uses JVP/autodiff. | Phase 1 route audit and Phase 2 repair/block before analytical-gradient promotion. |
| Dense or streamed all-pairs treated as feasible d18 route | `BLOCK_D18_ALL_PAIRS_DRIFT` | Do not use dense all-pairs, streamed all-pairs, or "increase memory" as the d18 full-history solution. | Phase 6 feasibility gate must select a non-all-pairs route or block. |
| ESS, finite replay, fit loss, FD rows, or validation residuals treated as correctness | `BLOCK_PROXY_PROMOTION` | Do not promote proxy diagnostics to correctness, convergence, HMC readiness, or production readiness. | Phases 4, 7, and 8 must preserve diagnostic-only roles unless a reference bridge exists. |
| Local/operator route treated as source-faithful Zhao-Cui | `BLOCK_SOURCE_CLAIM_UNGROUNDED` | Do not call local/operator/all-grid routes source-faithful without paper/source anchors and classification. | Phase 6 route classification and Phase 8 same-target source-backed bridge. |
| ALS training revived after training-base decision | `BLOCK_ALS_REVIVAL` | Do not use or revive historical ALS training for fixed-variant Zhao-Cui fitting. | Phase 7 must inherit P86 training-base/L1 discipline. |
| Training run without L1 tuning, validation/holdout/audit split, scheduler, or sample-budget discipline | `BLOCK_TRAINING_DISCIPLINE_MISSING` | Do not run or interpret fitted source-route evidence without training-base, L1 tuning, holdout/audit separation, scheduler, sample budget, and no audit tuning. | Phase 7 rank/degree gate and any later fit preflight. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does P87 correctly freeze the old mistakes as blockers before execution? |
| Baseline/comparator | P81 route correction, P81 Phase 3/5/9 notes, P83 reset/visible handoff, P86 Phase 6T/6Y results, and current code route strings. |
| Primary criterion | Met: every canonical mistake-ledger row has a named blocker, forbidden promotion, artifact evidence, and downstream phase gate. |
| Veto diagnostics | Missing JVP blocker, missing all-pairs blocker, stale Phase 7 execution-only status, proxy metrics as correctness, non-fail-closed checks, or non-exact review verdict checks. |
| Explanatory diagnostics | Artifact inventory, grep hits, current code route strings, all-pairs/scaling blocker hits. |
| Not concluded | No analytical-gradient correctness, source-route correctness, full-history feasibility, HMC readiness, production readiness, LEDH comparison, GPU performance, d50/d100 scaling, or default-policy change. |
| Artifact | This result, execution ledger, Claude review ledger, and Phase 1 read-only route-audit subplan. |

## Checks Run

Pre-execution checks passed in fail-closed form:

- exact-file existence checks for the P87 master and visible runbook;
- exact blocker-token checks across the P87 master, visible runbook, and Phase
  0 subplan;
- current JVP-route hazard grep:
  `ForwardAccumulator|target_derivative_backend|tensorflow_forward_accumulator_for_model_log_density`;
- current all-pairs/complexity hazard grep:
  `streamed all-pairs|all-pairs|quadratic|COMPLEXITY_GATE`;
- Phase 1 read-only boundary phrase checks;
- `git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p87*.md`.

## Phase 1 Handoff

Phase 1 may begin only as a read-only current-route audit. It may write its
result, ledgers, and refreshed subplan documentation, but it may not edit code,
run long tests, run GPU commands, or call the current JVP-backed route
analytical.

Required Phase 1 first action:

- run the local route audit greps in
  `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase1-current-route-audit-subplan-2026-06-26.md`;
- classify every derivative component before any repair or analytical-gradient
  claim.

## What Is Not Concluded

No Zhao-Cui SIR d18 analytical-gradient correctness, full-history feasibility,
source-route correctness, HMC readiness, production readiness, LEDH comparison,
GPU claim, d50/d100 scaling claim, or default-policy change is authorized by
Phase 0.
