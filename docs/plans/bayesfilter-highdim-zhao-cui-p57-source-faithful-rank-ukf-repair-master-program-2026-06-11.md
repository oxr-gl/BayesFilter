# P57 Master Program: Source-Faithful Zhao-Cui Transport, Rank, And UKF Repair

metadata_date: 2026-06-11
program: P57-source-faithful-zhao-cui-rank-ukf-repair
status: PLAN_REVIEW_CONVERGED
supervisor: Codex
reviewer: Claude Code Opus max-effort read-only

## Objective

Close the P56 source-anchor gaps needed before BayesFilter can claim a
faithful fixed-HMC adaptation of the Zhao-Cui filtering route for paper-scale
spatial SIR.  This program also repairs the UKF/rank planning problem: P52/P53
implemented useful UKF scouting and rank/memory preflight code, but those
artifacts are tied to a local/operator route and cannot close a
source-faithfulness gap for the author SIRT/IRT retained-object route.

## Binding Source-Faithfulness Rule

`BLOCK_SOURCE_UNGROUNDED` is binding for every P57 phase.  Any implementation
choice must be checked against the Zhao-Cui paper and bundled author MATLAB
source before it is accepted as `source_faithful` or `fixed_hmc_adaptation`.

Adaptive Zhao-Cui parity, S&P 500 reproduction, and smoothing are not P57
requirements unless explicitly re-scoped.  Fixed-HMC adaptation is allowed only
when it preserves the author route while freezing ranks, bases, random draws,
sample schedules, ESS stop conditions, resampling policy, and other branch
choices before likelihood evaluation.

## What P57 Supersedes

P52/P53 UKF scouting, memory preflight, and route-rank selection remain useful
as diagnostics.  For source-faithful Zhao-Cui claims, however, P57 supersedes
any P52/P53 result that:

- uses `transition_route.py`, `rank_budget.py` `R_eff`, local-neighborhood
  transition metadata, or all-grid retained storage as the promoted route;
- treats UKF as a correctness oracle, rank selector, or likelihood comparator;
- budgets memory for a route other than fixed TT/SIRT transport cores,
  source-style marginalization/KR state, proposal-correction samples, and
  retained objects;
- runs d=18/d=50/d=100 spatial SIR without a source-route transport object.

These older artifacts may be used only as lower-rung diagnostics or scout
metadata unless a phase explicitly reclassifies them with paper/source anchors.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter repair the missing source-route transport, marginalization, proposal correction, sequential loop, rank protocol, and UKF boundary so fixed Zhao-Cui filtering can be tested on paper-scale spatial SIR without drifting into invented routes? |
| Baseline/comparator | P56 source-anchor audit; Zhao-Cui paper equations and algorithms; author MATLAB source in `third_party/audit/zhao_cui_tensor_ssm_p10/source`; existing P55 source-route substrate; P52/P53 UKF/rank artifacts as diagnostic-only prior work. |
| Primary pass criterion | Every phase has a source-anchored subplan, pass/block token, result artifact target, explicit nonclaims, and implementation/review gates preventing route drift. |
| Veto diagnostics | Missing paper/source anchor; local/operator or all-grid route promoted as source-faithful; UKF promoted to truth; rank selected from old `R_eff` route; proposal density uses base/reference density where source needs `eval_pdf`-equivalent density; sequential loop skips retained marginalization; rank adapts inside likelihood. |
| Explanatory diagnostics | UKF mean/covariance/effective-dimension summaries, memory forecasts, finite values/gradients, lower-rung dense checks, same-route rank self-convergence, wall time, and replay diagnostics. |
| Not concluded | This plan alone does not implement Zhao-Cui, prove HMC readiness, prove d=50/d=100 correctness, reproduce adaptive TT-cross, reproduce S&P 500, or implement smoothing. |
| Artifacts | P57 master program, phase subplans, Claude review ledger, phase result files, source-anchor ledgers, tests, code patches, manifests, and final integration closeout. |

## Skeptical Plan Audit

Status: CODEX_DRAFT_AUDIT_PASS_PENDING_CLAUDE.

- Wrong-baseline risk: P52/P53 route-rank metadata answered a different route
  question.  P57 requires source-route TT/SIRT rank evidence.
- Proxy-risk: UKF, memory feasibility, finite gradients, and self-convergence
  are not promoted beyond their declared role.
- Hidden-assumption risk: fixed-rank ALS, grid KR, and local transition
  operators are not automatically fixed-HMC adaptations.  They must prove or
  relinquish source equivalence.
- Missing-stop risk: if a phase cannot cite author paper/source anchors, it
  blocks with `BLOCK_SOURCE_UNGROUNDED` instead of inventing a substitute.
- Artifact-risk: every phase must produce a result file even when blocked, so a
  later agent can resume from evidence rather than memory.
- Drift-risk: Claude review must explicitly check paper/source anchors and
  reject plans that only repair governance while leaving implementation gaps
  untouched.

## Source Anchors From P56

P57 starts from the anchors already audited in P56:

- paper equations (9)--(11): adjacent-state posterior recursion and
  marginalization;
- Algorithm 1 and Algorithm 2: TT/SIRT sequential filtering;
- equation (13), Proposition 2, and equation (14): squared TT defensive
  density, mass/QR marginalization, and normalizer;
- conditional KR maps and inverse maps;
- Algorithm 3: proposal sampling and correction with `eval_pdf`;
- Algorithm 5: preconditioned route and retained marginal step;
- author `full_sol.m`, `pre_sol.m`, `ssmodel.m`, `SIRT.m`,
  `AbstractIRT.m`, and `@TTSIRT/marginalise.m`.

Every implementation phase must re-open the specific source files it relies on
and preserve line references in its result artifact.

## Phase Index

| Phase | Name | Subplan | Required result artifact | Required token |
| --- | --- | --- | --- | --- |
| P57-M0 | Governance And Source-Anchor Lock | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-result-2026-06-11.md` | `PASS_P57_M0_GOVERNANCE_SOURCE_ANCHOR` or `BLOCK_P57_M0_GOVERNANCE_SOURCE_ANCHOR` |
| P57-M1 | Author Model Callback Parity | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m1-author-model-callback-parity-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m1-author-model-callback-parity-result-2026-06-11.md` | `PASS_P57_M1_AUTHOR_MODEL_CALLBACK_PARITY` or `BLOCK_P57_M1_AUTHOR_MODEL_CALLBACK_PARITY` |
| P57-M2 | FixedTTSIRT Transport Contract | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m2-fixed-ttsirt-transport-contract-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m2-fixed-ttsirt-transport-contract-result-2026-06-11.md` | `PASS_P57_M2_FIXED_TTSIRT_TRANSPORT_CONTRACT` or `BLOCK_P57_M2_FIXED_TTSIRT_TRANSPORT_CONTRACT` |
| P57-M3 | Proposition-2 Marginalization | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m3-proposition2-marginalization-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m3-proposition2-marginalization-result-2026-06-11.md` | `PASS_P57_M3_PROPOSITION2_MARGINALIZATION` or `BLOCK_P57_M3_PROPOSITION2_MARGINALIZATION` |
| P57-M4 | Source KR/CDF Maps | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m4-source-kr-cdf-maps-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m4-source-kr-cdf-maps-result-2026-06-11.md` | `PASS_P57_M4_SOURCE_KR_CDF_MAPS` or `BLOCK_P57_M4_SOURCE_KR_CDF_MAPS` |
| P57-M5 | Proposal Density And Retained Sampling | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m5-proposal-density-retained-sampling-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m5-proposal-density-retained-sampling-result-2026-06-11.md` | `PASS_P57_M5_PROPOSAL_DENSITY_RETAINED_SAMPLING` or `BLOCK_P57_M5_PROPOSAL_DENSITY_RETAINED_SAMPLING` |
| P57-M6 | Full Sequential Fixed-HMC Source Loop | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m6-sequential-fixed-hmc-source-loop-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m6-sequential-fixed-hmc-source-loop-result-2026-06-11.md` | `PASS_P57_M6_SEQUENTIAL_FIXED_HMC_SOURCE_LOOP` or `BLOCK_P57_M6_SEQUENTIAL_FIXED_HMC_SOURCE_LOOP` |
| P57-M7 | Source-Faithful Rank And UKF Calibration | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m7-source-faithful-rank-ukf-calibration-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m7-source-faithful-rank-ukf-calibration-result-2026-06-11.md` | `PASS_P57_M7_SOURCE_FAITHFUL_RANK_UKF_CALIBRATION` or `BLOCK_P57_M7_SOURCE_FAITHFUL_RANK_UKF_CALIBRATION` |
| P57-M8 | Preconditioned Algorithm 5 Route | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m8-preconditioned-algorithm5-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m8-preconditioned-algorithm5-result-2026-06-11.md` | `PASS_P57_M8_PRECONDITIONED_ALGORITHM5` or `BLOCK_P57_M8_PRECONDITIONED_ALGORITHM5` |
| P57-M9 | Spatial SIR Validation Ladder | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m9-spatial-sir-validation-ladder-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m9-spatial-sir-validation-ladder-result-2026-06-11.md` | `PASS_P57_M9_SPATIAL_SIR_VALIDATION_LADDER` or `BLOCK_P57_M9_SPATIAL_SIR_VALIDATION_LADDER` |
| P57-M10 | P30 Documentation And Claim Reconciliation | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m10-p30-doc-claim-reconciliation-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m10-p30-doc-claim-reconciliation-result-2026-06-11.md` | `PASS_P57_M10_P30_DOC_CLAIM_RECONCILIATION` or `BLOCK_P57_M10_P30_DOC_CLAIM_RECONCILIATION` |
| P57-M11 | Integration Closeout | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m11-integration-closeout-subplan-2026-06-11.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p57-m11-integration-closeout-result-2026-06-11.md` | `PASS_P57_M11_INTEGRATION_CLOSEOUT` or `BLOCK_P57_M11_INTEGRATION_CLOSEOUT` |

## UKF And Rank Rule

UKF can scout centers, scales, covariance structure, local correlation, and
effective dimension.  UKF can propose candidate rank ranges, preconditioner
initialization, and grid/basis scale choices.  UKF cannot certify likelihood,
filtering correctness, source faithfulness, HMC readiness, or final rank.

Source-faithful rank selection must be tied to the fixed TT/SIRT transport
object.  The first source anchor is the paper/author spatial SIR rank ladder
`{10, 20, 40}` for d=18.  Any smaller practical rank such as `{2,4,8,16,32}`
must be justified as a fixed-HMC approximation to that route through source
transport memory budgets and rank-convergence evidence, not through the old
local/operator `R_eff` route alone.

## Repair Loop

Codex must handle fixable issues instead of stopping for no valid reason.
Fixable issues include missing source anchors, stale nonclaims, failing tests
with clear local repairs, outdated route classification, missing result tokens,
or Claude review findings that identify concrete corrections.

Stop only if:

- author source or paper anchors cannot be located after a documented search;
- an implementation choice requires human approval because it is not source
  grounded and no fixed-HMC adaptation can be defended;
- dependencies or trusted permissions needed for implementation are unavailable;
- Claude and Codex both identify the same unresolved major blocker after the
  allowed repair loop.

## Claude Review Protocol

Run Claude Code Opus max-effort read-only review up to five iterations.
Claude must check:

1. whether every phase is source anchored;
2. whether P52/P53 UKF/rank work is correctly demoted to scout/preflight unless
   tied to fixed TT/SIRT;
3. whether the plan would actually lead to implementation rather than only
   governance documents;
4. whether proposal density and retained marginalization are treated as hard
   blockers;
5. whether the plan preserves fixed-HMC differentiability without inventing a
   new route.

Converged means Claude returns no material blockers.  If the fifth review still
contains only minor editorial issues, accept the fifth version and record the
residuals.  If it contains a major source-faithfulness blocker, keep status
blocked rather than launching implementation from an unsound plan.

## Iteration-1 Review Corrections

Claude iteration 1 accepted the master-program direction but found material
subplan gaps. Draft 2 tightens:

- M0 durable checked-in governance over mutable memory;
- M1 spatial SIR scope and mismatch blockers;
- M3 pass-only-with-implementation semantics;
- M4 exact KR/CDF source anchors;
- M5 exact `eval_pdf(sirt,r)` denominator identity;
- M6 branch-by-branch source/adaptation ledger;
- M7 concrete rank-promotion comparator/tolerance rules;
- M9 d=18 claim tiers and non-proxy comparator strategy;
- M10 exact P30 LaTeX file binding;
- M11 claim-to-phase gate matrix.

Claude iteration 2 accepted M0-M9 and M11. It found one residual blocker in
M10: the P30 target was still ambiguous because the subplan mentioned a P40
draft as a possible superseding file. Draft 3 binds M10 to the exact P30 LaTeX
file and requires any other LaTeX reconciliation to be a separate reviewed
amendment.
