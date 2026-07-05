# P87 Master Program: SIR d18 Analytical-Gradient And Source-Route Gates

Date: 2026-06-26

Status: `P87_MASTER_PROGRAM_REVIEWED_CLAUDE_AGREE`

## Objective

Determine what the Zhao-Cui SIR d18 route can honestly claim for filtering
value and analytical gradient, while preventing the prior two-week mistakes
from recurring:

- horizon-0 evidence promoted to full-history validation;
- JVP/`ForwardAccumulator` promoted to analytical gradient;
- dense or streamed all-pairs transition promoted to a d18 route;
- execution-only, ESS, finite replay, or fit loss promoted to correctness;
- local/operator routes promoted to source-faithfulness;
- ALS training revived after training-base migration;
- training without L1 tuning, validation/holdout/audit separation, or plateau
  scheduler discipline.

## Governing Artifacts

- Runbook: `docs/plans/bayesfilter-highdim-zhao-cui-p87-visible-gated-overnight-execution-plan-2026-06-26.md`
- Execution ledger: `docs/plans/bayesfilter-highdim-zhao-cui-p87-visible-execution-ledger-2026-06-26.md`
- Claude review ledger: `docs/plans/bayesfilter-highdim-zhao-cui-p87-claude-review-ledger-2026-06-26.md`
- Stop handoff: `docs/plans/bayesfilter-highdim-zhao-cui-p87-visible-stop-handoff-2026-06-26.md`

## Phase Index

| Phase | Name | Subplan | Result |
| --- | --- | --- | --- |
| 0 | Mistake ledger and evidence contract | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase0-mistake-ledger-evidence-contract-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase0-mistake-ledger-evidence-contract-result-2026-06-26.md` |
| 1 | Current route audit | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase1-current-route-audit-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase1-current-route-audit-result-2026-06-26.md` |
| 2 | Analytical route repair | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase2-analytical-route-repair-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase2-analytical-route-repair-result-2026-06-26.md` |
| 3 | Local SIR algebra certification | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase3-local-sir-algebra-certification-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase3-local-sir-algebra-certification-result-2026-06-26.md` |
| 4 | Horizon-0 d18 value/gradient gate | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase4-horizon0-d18-value-gradient-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase4-horizon0-d18-value-gradient-result-2026-06-26.md` |
| 5 | Tiny full-history exact regression | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase5-tiny-full-history-regression-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase5-tiny-full-history-regression-result-2026-06-26.md` |
| 6 | d18 full-history feasibility gate | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase6-d18-full-history-feasibility-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase6-d18-full-history-feasibility-result-2026-06-26.md` |
| 7 | Source-route rank/degree gate | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase7-source-route-rank-degree-gate-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase7-source-route-rank-degree-gate-result-2026-06-26.md` |
| 8 | Correctness-candidate bridge gate | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase8-correctness-candidate-bridge-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase8-correctness-candidate-bridge-result-2026-06-26.md` |
| 9 | Final claim gate and handoff | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase9-final-claim-gate-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase9-final-claim-gate-result-2026-06-26.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which Zhao-Cui SIR d18 value/gradient claims are supported by current code after no-regression gates are applied? |
| Baseline/comparator | P81 route correction and phase results, P83 visible handoff/reset, P86 training-base/rank-degree artifacts, current `bayesfilter/highdim/filtering.py` and `models.py`. |
| Primary pass criterion | Each phase emits a result with explicit claim class, veto status, checks, artifacts, and next-phase handoff; analytical-gradient claims are allowed only after the promoted route is JVP-free. |
| Veto diagnostics | Horizon-0 overclaim, JVP promoted as analytical, all-pairs d18 route, proxy metric promotion, source-claim without anchors, ALS revival, missing training discipline, stale artifact status. |
| Explanatory diagnostics | FD residuals, branch hashes, ESS, fit/holdout residuals, validation scheduler events, rank/degree differences, runtime/memory. |
| Not concluded | Production readiness, HMC readiness, posterior correctness, d50/d100 scaling, LEDH superiority, source-faithful correctness, or default-policy change unless a later phase explicitly gates it. |
| Artifacts | P87 subplans/results, ledgers, review records, local test outputs, JSON manifests if a later phase runs numerical work. |

## Hard No-Regression Blockers

| Prior mistake | Binding blocker |
| --- | --- |
| Horizon-0 evidence called full-history validation | `BLOCK_HORIZON0_OVERCLAIM` |
| JVP/`ForwardAccumulator` called analytical Zhao-Cui gradient | `BLOCK_ANALYTICAL_ROUTE_HAS_JVP_COMPONENT` |
| Dense or streamed all-pairs used as the d18 solution | `BLOCK_D18_ALL_PAIRS_DRIFT` |
| Finite execution, ESS, fit loss, or replay promoted to correctness | `BLOCK_PROXY_PROMOTION` |
| Local/operator route used as source-faithful without anchors | `BLOCK_SOURCE_CLAIM_UNGROUNDED` |
| ALS training revived | `BLOCK_ALS_REVIVAL` |
| Missing L1 tuning or validation/holdout/audit split in fitted evidence | `BLOCK_TRAINING_DISCIPLINE_MISSING` |

## Claude Review Protocol

Claude is read-only reviewer only. Codex remains supervisor and executor.
Material subplans/results must be reviewed with bounded one-path prompts when
possible. Stop after five review rounds for the same blocker.

## Execution Rule

No phase may execute until its subplan exists, local plan checks pass, and the
runbook ledger records the phase evidence contract and skeptical audit. At the
end of each phase Codex must:

1. run required local checks;
2. write the phase result or blocker record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
5. use Claude read-only review for material crossings.
