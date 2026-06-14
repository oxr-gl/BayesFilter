# P50 Master Program: HMC-Compatible Deterministic Filtering

metadata_date: 2026-06-09
program: P50-hmc-deterministic-filtering
status: PLAN_REVIEW_CONVERGED
supervisor: Codex
reviewer: Claude Code read-only

## Objective

Build the next BayesFilter program around deterministic, differentiable
filtering suitable for HMC.  P50 uses the P49 route-governance work as guardrails
but does not pursue adaptive TT/SIRT source-faithful filtering as an
implementation target, because that route is not naturally gradient-bearing.

## Explicit Non-Goals

These are not gaps for P50:

- adaptive TT/SIRT source-faithful filtering;
- S&P 500 reproduction.

They may remain historical or source-audit context, but they must not appear as
P50 blockers, required deliverables, or pass criteria.

## Remaining Repair Targets

| Target | Issue to fix | Required outcome |
| --- | --- | --- |
| H1 | P49 helpers are scoped but not integrated into a full deterministic filter. | A documented full-loop contract and implementation path. |
| H2 | Recentring, Jacobian, proposal-correction, and normalizer accounting are not wired end to end. | One-step and sequential accounting tests. |
| H3 | Value and gradient correctness need HMC-grade criteria. | Quantitative value/gradient calibration rules and tests. |
| H4 | SV and generalized SV model comparisons need deterministic HMC-compatible value and gradient tests. | Dim 1/2/3 SV and generalized SV test ladder. |
| H5 | Spatial SIR and predator-prey comparisons need deterministic HMC-compatible value and gradient tests. | Model-specific test ladder with explicit non-production boundaries. |
| H6 | HMC readiness is not established by finite gradients alone. | Tiered HMC readiness gates, including local and short-chain diagnostics. |
| H7 | Smoothing/backward conditionals are separate from parameter HMC. | A boundary or implementation plan only if latent-path posterior inference is required. |
| H8 | Future artifacts may drift back into source-faithful/adaptive language. | Governance guards for HMC-compatible deterministic route labels. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter turn the P49 helper/governance scaffolding into a deterministic differentiable filter program whose value and gradient evidence can support HMC-facing work? |
| Baseline/comparator | P49 closeout and helper contracts; existing CUT4, Kalman, dense/exact, and model-specific references where applicable; current BayesFilter deterministic fixed branch. |
| Primary pass criterion | Every H1--H8 issue has a reviewed phase subplan, explicit pass/block token, result artifact path, local validation strategy, repair loop, and non-claims. |
| Veto diagnostics | Adaptive non-gradient filtering treated as a required target; S&P reproduction treated as a required target; proxy metrics promoted to HMC readiness; value-only agreement promoted to gradient correctness; stochastic/adaptive randomness promoted as differentiable without a reviewed contract; missing stop conditions. |
| Explanatory diagnostics | Unit tests, compile checks, small model ladders, directional-gradient diagnostics, likelihood-error calibration, short HMC smoke diagnostics, and static claim audits. |
| Not concluded | No HMC readiness, production model readiness, smoothing support, or full deterministic filter completion is concluded by this master plan alone. |
| Artifacts | This master program, phase subplans, visible execution runbook, visible execution ledger, phase result artifacts, Claude review ledger, and final handoff. |

## Skeptical Plan Audit

Status: REVIEWED.

- Wrong baseline risk: compare deterministic filter results against exact,
  dense, Kalman, CUT4, or existing deterministic references, not against
  adaptive source reproduction.
- Proxy promotion risk: value agreement, finite-difference checks, and short HMC
  runs are diagnostics unless a phase makes them primary criteria with explicit
  tolerances and veto conditions.
- Hidden assumption risk: a differentiable implementation can still have
  scientifically poor gradients; an accurate value path can still be unusable
  for HMC.
- Environment mismatch risk: validation is CPU-only by default; GPU claims need
  separate trusted-context approval.
- Stop-condition risk: every phase has pass, repair, and human-required stop
  conditions.
- Artifact adequacy risk: every phase has a required result artifact and one
  pass/block token before it can pass.

## Phase Index

| Phase | Name | Targets | Subplan | Required result artifact | Required pass/block token |
| --- | --- | --- | --- | --- | --- |
| P50-M0 | Scope And Claim Governance | H8 | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m0-scope-claim-governance-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m0-scope-claim-governance-result-2026-06-09.md` | `PASS_P50_M0_SCOPE_CLAIM_GOVERNANCE` or `BLOCK_P50_M0_SCOPE_CLAIM_GOVERNANCE` |
| P50-M1 | Deterministic Filter Loop Contract | H1, H2 | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m1-deterministic-filter-loop-contract-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m1-deterministic-filter-loop-contract-result-2026-06-09.md` | `PASS_P50_M1_DETERMINISTIC_FILTER_LOOP_CONTRACT` or `BLOCK_P50_M1_DETERMINISTIC_FILTER_LOOP_CONTRACT` |
| P50-M2 | One-Step Value Path Implementation | H1, H2 | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m2-one-step-value-path-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m2-one-step-value-path-result-2026-06-09.md` | `PASS_P50_M2_ONE_STEP_VALUE_PATH` or `BLOCK_P50_M2_ONE_STEP_VALUE_PATH` |
| P50-M3 | Sequential Likelihood Path | H1, H2 | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m3-sequential-likelihood-path-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m3-sequential-likelihood-path-result-2026-06-09.md` | `PASS_P50_M3_SEQUENTIAL_LIKELIHOOD_PATH` or `BLOCK_P50_M3_SEQUENTIAL_LIKELIHOOD_PATH` |
| P50-M4 | Value And Gradient Calibration Rules | H3 | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m4-value-gradient-calibration-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m4-value-gradient-calibration-result-2026-06-09.md` | `PASS_P50_M4_VALUE_GRADIENT_CALIBRATION` or `BLOCK_P50_M4_VALUE_GRADIENT_CALIBRATION` |
| P50-M5 | SV And Generalized SV Model Ladder | H4 | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m5-sv-generalized-sv-ladder-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m5-sv-generalized-sv-ladder-result-2026-06-09.md` | `PASS_P50_M5_SV_GENERALIZED_SV_LADDER` or `BLOCK_P50_M5_SV_GENERALIZED_SV_LADDER` |
| P50-M6 | Spatial SIR And Predator-Prey Ladder | H5 | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m6-spatial-sir-predator-prey-ladder-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m6-spatial-sir-predator-prey-ladder-result-2026-06-09.md` | `PASS_P50_M6_SPATIAL_SIR_PREDATOR_PREY_LADDER` or `BLOCK_P50_M6_SPATIAL_SIR_PREDATOR_PREY_LADDER` |
| P50-M7 | HMC Readiness Tiers | H6 | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m7-hmc-readiness-tiers-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m7-hmc-readiness-tiers-result-2026-06-09.md` | `PASS_P50_M7_HMC_READINESS_TIERS` or `BLOCK_P50_M7_HMC_READINESS_TIERS` |
| P50-M8 | Smoothing Boundary Or Latent-Path Plan | H7 | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m8-smoothing-boundary-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m8-smoothing-boundary-result-2026-06-09.md` | `PASS_P50_M8_SMOOTHING_BOUNDARY` or `BLOCK_P50_M8_SMOOTHING_BOUNDARY` |
| P50-M9 | Integration Closeout | H1--H8 | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m9-integration-closeout-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m9-integration-closeout-result-2026-06-09.md` | `PASS_P50_M9_INTEGRATION_CLOSEOUT` or `BLOCK_P50_M9_INTEGRATION_CLOSEOUT` |

## Repair Loop Rule

Codex must continue through fixable issues instead of stopping for no valid
reason.

Fixable issues include:

- focused tests failing with a clear code or artifact repair path;
- Claude `REVISE` findings that identify specific fixable flaws;
- result artifacts missing metadata, tokens, commands, or non-claims;
- stale route labels or unsupported HMC/source claims;
- wrong local command scope, import path, or test selection;
- numerical thresholds needing pre-declared calibration repairs before
  promotion.

Human-required blockers include:

- package installation, network fetch, credentials, or external runtime setup;
- destructive git or filesystem action;
- modifying unrelated dirty user work;
- changing pass/fail criteria after seeing results;
- changing default backend or numerical policy;
- GPU/special hardware claims without trusted-context approval;
- Codex/Claude non-convergence after five review rounds for the same blocker.

## Claude Review Loop

Claude is read-only reviewer only.  Use up to five iterations.  Stop early on:

```text
VERDICT: AGREE
```

If Claude returns `VERDICT: REVISE`, Codex patches the plan or runbook and
resubmits, unless the finding is a human-required blocker.  At iteration 5,
accept only if there is no major blocker; otherwise record
`BLOCKED_P50_PLAN_REVIEW_MAJOR_ISSUE`.

## Approval Needs For Execution

The visible runbook anticipates asking the user to approve:

1. escalated `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh`
   read-only Claude review prompts for the master plan, phase results, blocker
   plans, and closeout;
2. CPU-only local validation commands with
   `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`, including focused `pytest` and
   `python -m compileall`;
3. static inspection commands such as `rg`, `sed`, `git diff --check`, and
   `git status`.

No approval is anticipated for network fetches, package installation, GPU runs,
detached execution, or destructive git commands.  If any of those become
necessary, Codex must stop and ask separately.
