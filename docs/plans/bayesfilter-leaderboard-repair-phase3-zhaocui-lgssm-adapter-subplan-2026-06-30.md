# Phase 3 subplan: Zhao-Cui LGSSM m3 evaluator adapter

Date: 2026-06-30

Status: `DRAFT_REVIEW_READY`

## Phase Objective

Wire the Zhao-Cui evaluator adapter for `benchmark_lgssm_exact_oracle_m3_T50` so the row no longer blocks solely on `P8D_MODEL_SPECIFIC_NUMERIC_EVALUATOR_ADAPTER_REQUIRED`.

## Entry Conditions Inherited From Previous Phase

- Phase 2 has either resolved or explicitly deferred SGQF actual-SV score.
- Leaderboard schema can distinguish source-faithful, fixed-HMC adaptation, and extension/invention claims.
- Zhao-Cui training must use the training-base route, not historical ALS.

## Required Artifacts

- Narrow evaluator adapter code and tests.
- Source-anchor ledger for Zhao-Cui route classification if any Zhao-Cui source-faithfulness language is used.
- Regenerated highdim leaderboard.
- Phase result:
  `docs/plans/bayesfilter-leaderboard-repair-phase3-zhaocui-lgssm-adapter-result-2026-06-30.md`
- Refreshed Phase 4 subplan.

## Required Checks, Tests, Reviews

- Value check against exact Kalman reference.
- Score check against Kalman analytical score if available, otherwise FD and score consistency.
- XLA compile smoke if cheap and CPU-only; GPU XLA deferred to Phase 7.
- Guard that ALS training is not reintroduced.
- Claude review of Zhao-Cui adapter plan/result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Zhao-Cui evaluate the affine LGSSM m3 row with value and score rather than an adapter blocker? |
| Baseline/comparator | Exact Kalman log likelihood and differentiated Kalman score for the same row. |
| Primary criterion | Finite Zhao-Cui value, target-compatible status, and score status that matches actual derivative provenance. |
| Veto diagnostics | ALS fallback; target mismatch; source-faithfulness claim without anchors; nonfinite value/score; score coordinate mismatch. |
| Explanatory diagnostics | Value error to Kalman, score norm/error, runtime. |
| Not concluded | No nonlinear Zhao-Cui production readiness, no broad source-faithful claim beyond this adapter. |
| Artifact | Regenerated leaderboard and Phase 3 result. |

## Forbidden Claims And Actions

- Do not describe the adapter as paper-scale Zhao-Cui unless source anchors support it.
- Do not use historical ALS training.
- Do not make production readiness claims from this affine row.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 if:

- The LGSSM m3 Zhao-Cui row is executed or has a precise remaining blocker.
- Any score claim identifies coordinate system and derivative provenance.

## Stop Conditions

Stop if:

- The adapter requires a new Zhao-Cui algorithmic route not approved by the target classification.
- Kalman comparison fails outside a diagnosed numerical/tuning reason.
- Review flags source-faithfulness violations that cannot be repaired.

## End-of-Subplan Protocol

1. Run required local checks.
2. Write Phase 3 result/close record.
3. Draft or refresh Phase 4 subplan.
4. Review Phase 4 subplan for predator-prey target and analytical-score boundaries.
