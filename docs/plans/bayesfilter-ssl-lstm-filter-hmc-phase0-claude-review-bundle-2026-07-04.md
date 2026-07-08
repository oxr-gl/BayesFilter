# Claude Review Bundle: SSL-LSTM Filter-HMC Phase 0

Date: 2026-07-04

Status: `READY_FOR_READ_ONLY_REVIEW_AFTER_LOCAL_CHECKS`

## Review Role

READ-ONLY REVIEW ONLY.

Do not edit files, run mutating commands, launch agents, or approve boundary
crossings. Claude is a reviewer only. Codex is supervisor and executor.

## Objective

Review whether the Phase 0 planning artifacts are adequate to launch Phase 1
for HMC estimation of a Gaussian additive state-space LSTM using BayesFilter
filtering algorithms as deterministic value/score engines.

## Bounded Artifact Set

Review only these paths:

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-master-program-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-visible-gated-overnight-execution-plan-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-visible-execution-ledger-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-claude-review-ledger-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-visible-stop-handoff-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase0-planning-governance-subplan-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase1-ssl-model-estimand-subplan-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase2-value-score-protocol-subplan-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase3-sgqf-ukf-analytic-adapters-subplan-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase4-zhaocui-fixed-analytic-adapter-subplan-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase5-ledh-streaming-ot-manual-vjp-subplan-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase6-benchmark-runner-invariant-metrics-subplan-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase7-hmc-evidence-ladder-subplan-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase8-closeout-reset-boundary-subplan-2026-07-04.md`

Do not inspect unrelated repository files unless needed to verify that these
documents are not making an obvious unsupported claim about a named local path.

## Scope Summary

The planned program intentionally:

- uses HMC over parameters, not latent-path Particle Gibbs, conditional SMC, or
  Gibbs;
- estimates a filter-induced posterior for each declared filter likelihood;
- treats SSL-LSTM parameter recovery as non-identifiable and uses invariant
  predictive and latent-state metrics instead;
- requires analytic gradients for fixed SGQF, UKF, and fixed-variant Zhao-Cui;
- requires LEDH streaming-OT manual VJP, not ordinary autodiff through the
  transport solve;
- keeps SGQF and UKF in the same shared benchmark rather than assuming they are
  sufficient;
- keeps Zhao-Cui source-faithfulness claims blocked until paper and author-source
  anchors are inspected.

## Evidence Contract To Audit

| Field | Contract |
| --- | --- |
| Question | Are Phase 0 planning artifacts adequate and boundary-safe enough to start Phase 1? |
| Baseline/comparator | User request, BayesFilter AGENTS policy embedded in the conversation, and the visible gated execution template. |
| Primary pass criterion | Required artifacts and phase subplans exist, local checks pass, and the next phase has exact handoff conditions. |
| Veto diagnostics | Missing required subplan field, unsupported scientific claim, detached execution, Claude executor authority, unbounded review prompt, or no repair loop. |
| Explanatory diagnostics | Formatting, readability, and minor wording issues. |
| Not concluded | No implementation, no HMC readiness, no filter sufficiency, no posterior correctness, no ranking, no source-faithfulness. |

## Review Questions

Findings first. Check:

- wrong baseline or comparator;
- proxy metrics promoted to pass criteria;
- missing stop conditions;
- unfair comparisons among candidate filters;
- hidden assumptions about Gaussian additive noise, fixed randomness, XLA/GPU,
  or gradients;
- stale context or missing Phase 1 source-inspection gate;
- commands whose artifacts would not answer the stated phase question;
- unsupported claims about SSL-LSTM, HMC, SGQF, UKF, Zhao-Cui, or LEDH;
- Claude authority exceeding read-only review;
- missing artifact coverage or next-phase handoff conditions;
- evasive scientific language where direct `unsupported`, `not checked`, or
  `wrong relative to target` language is needed.

End with exactly:

`VERDICT: AGREE`

or

`VERDICT: REVISE`
