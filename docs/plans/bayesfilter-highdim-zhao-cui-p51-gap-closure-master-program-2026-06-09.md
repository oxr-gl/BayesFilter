# P51 Master Program: HMC Gap Closure After P50

metadata_date: 2026-06-09
program: P51-hmc-gap-closure-after-p50
status: PLAN_REVIEW_CONVERGED
supervisor: Codex
reviewer: Claude Code read-only

## Objective

Close the actionable P50 remaining gaps without reviving explicit P50 non-goals
or promoting diagnostics into HMC, smoothing, or production readiness.

P51 addresses only the P50 gaps that were explicitly left actionable:

- native generalized SV same-target reference;
- spatial SIR production route architecture;
- predator-prey production accuracy/tuning;
- HMC Tier 2 Hamiltonian/leapfrog diagnostics;
- HMC Tier 3 short-chain sampler diagnostics;
- original P50 `stable_top_level_score_api` gap, split explicitly into:
  - stable `bayesfilter.highdim` score API contract work; and
  - a root-level `bayesfilter` public export decision that must either pass by
    reviewed policy/implementation or remain blocked as a public-API decision;
- smoothing only as a scoped decision boundary if latent-path inference becomes
  an explicit future target.

These remain non-goals, not gaps:

- adaptive TT/SIRT source-faithful filtering;
- S&P 500 reproduction.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the P50 remaining gaps be closed or converted into narrower reviewed blockers without overclaiming HMC, production, smoothing, or source-faithful reproduction? |
| Baseline/comparator | P50 closeout, P50 M4 calibration rules, P50 HMC tier manifest, P50 smoothing boundary, existing SV/generalized-SV/spatial-SIR/predator-prey tests, and TensorFlow/TFP deterministic score paths. |
| Primary pass criterion | Each P51 phase either emits its required pass/block token with result and manifest artifacts plus Claude review, or stops with a human-required blocker after the repair loop. |
| Veto diagnostics | Non-goals treated as gaps; diagnostic rows promoted to production readiness; finite gradients promoted to HMC readiness; native generalized SV compared to a proxy as if same-target; smoothing support claimed without backward conditionals; GPU claims from CPU-only runs. |
| Explanatory diagnostics | Unit tests, compile checks, low-dimensional dense references, route preflight checks, tuning sweeps, leapfrog energy/reversibility checks, short-chain sampler diagnostics, and static claim audits. |
| Not concluded | No production HMC readiness, model production readiness, native generalized SV correctness, stable public API, or smoothing support unless the corresponding P51 phase explicitly passes. |
| Artifacts | P51 master program, phase subplans, visible runbook, review ledger, execution ledger, phase results, phase manifests, tests, and final handoff. |

## Skeptical Plan Audit

Status: REVIEWED.

- Wrong baseline risk: P51 must use same-target references, production
  criteria, and HMC tier criteria from P50 rather than convenient proxy metrics.
- Proxy promotion risk: finite values, finite scores, low-rung diagnostics, and
  short CPU tests cannot imply production or HMC readiness unless their phase
  criteria explicitly require the missing diagnostics.
- Hidden assumption risk: native generalized SV may require a new exact/dense
  reference rather than adaptation of transformed-residual diagnostics.
- Stop-condition risk: production-scale nonlinear rows may remain blocked; the
  repair loop must narrow or document blockers rather than fabricate passes.
- Environment mismatch risk: CPU-only default; GPU claims require trusted GPU
  approval and separate evidence.
- Artifact adequacy risk: every phase has one result artifact and one required
  pass/block token before advancement.

## Phase Index

| Phase | Name | Gap Target | Subplan | Required result artifact | Required manifest artifact | Required token |
| --- | --- | --- | --- | --- | --- | --- |
| P51-M0 | Gap Scope And Preflight Governance | All | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m0-gap-scope-preflight-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m0-gap-scope-preflight-result-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m0-gap-scope-preflight-manifest-2026-06-09.json` | `PASS_P51_M0_GAP_SCOPE_PREFLIGHT` or `BLOCK_P51_M0_GAP_SCOPE_PREFLIGHT` |
| P51-M1 | Stable Score API Contract | original `stable_top_level_score_api` row, with subpackage/root-level split | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m1-stable-score-api-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m1-stable-score-api-result-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m1-stable-score-api-manifest-2026-06-09.json` | `PASS_P51_M1_STABLE_SCORE_API` or `BLOCK_P51_M1_STABLE_SCORE_API` |
| P51-M2 | Native Generalized SV Reference | generalized SV | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-result-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-manifest-2026-06-09.json` | `PASS_P51_M2_NATIVE_GENERALIZED_SV_REFERENCE` or `BLOCK_P51_M2_NATIVE_GENERALIZED_SV_REFERENCE` |
| P51-M3 | Spatial SIR Production Route Architecture | spatial SIR | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m3-spatial-sir-production-route-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m3-spatial-sir-production-route-result-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m3-spatial-sir-production-route-manifest-2026-06-09.json` | `PASS_P51_M3_SPATIAL_SIR_ROUTE_PREFLIGHT` or `BLOCK_P51_M3_SPATIAL_SIR_ROUTE_PREFLIGHT` |
| P51-M4 | Predator-Prey Production Accuracy Tuning | predator-prey | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m4-predator-prey-production-tuning-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m4-predator-prey-production-tuning-result-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m4-predator-prey-production-tuning-manifest-2026-06-09.json` | `PASS_P51_M4_PREDATOR_PREY_PRODUCTION_TUNING` or `BLOCK_P51_M4_PREDATOR_PREY_PRODUCTION_TUNING` |
| P51-M5 | HMC Tier 2 Leapfrog Diagnostics | HMC Tier 2 | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m5-hmc-tier2-leapfrog-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m5-hmc-tier2-leapfrog-result-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m5-hmc-tier2-leapfrog-manifest-2026-06-09.json` | `PASS_P51_M5_HMC_TIER2_LEAPFROG` or `BLOCK_P51_M5_HMC_TIER2_LEAPFROG` |
| P51-M6 | HMC Tier 3 Short-Chain Diagnostics | HMC Tier 3 | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m6-hmc-tier3-short-chain-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m6-hmc-tier3-short-chain-result-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m6-hmc-tier3-short-chain-manifest-2026-06-09.json` | `PASS_P51_M6_HMC_TIER3_SHORT_CHAIN` or `BLOCK_P51_M6_HMC_TIER3_SHORT_CHAIN` |
| P51-M7 | Smoothing Future-Target Decision | smoothing deferral | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m7-smoothing-future-target-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m7-smoothing-future-target-result-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m7-smoothing-future-target-manifest-2026-06-09.json` | `PASS_P51_M7_SMOOTHING_FUTURE_TARGET` or `BLOCK_P51_M7_SMOOTHING_FUTURE_TARGET` |
| P51-M8 | Integration Closeout | all | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m8-integration-closeout-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m8-integration-closeout-result-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m8-integration-closeout-manifest-2026-06-09.json` | `PASS_P51_M8_INTEGRATION_CLOSEOUT` or `BLOCK_P51_M8_INTEGRATION_CLOSEOUT` |

## Repair Loop Rule

Codex must continue through fixable issues instead of stopping for no valid
reason.

Fixable issues include:

- local test failures with a clear code or artifact repair path;
- Claude `REVISE` findings that identify concrete flaws;
- result artifacts missing metadata, tokens, commands, non-claims, or route
  labels;
- wrong local command scope, import path, or test selection;
- insufficient guard tests for non-goals or overclaim prevention;
- a phase needing to narrow from pass to a reviewed blocker while preserving
  valid lower-rung evidence.

Human-required blockers include:

- package installation, network fetch, credentials, or external runtime setup;
- destructive git or filesystem action;
- modifying unrelated dirty user work;
- changing pass/fail criteria after seeing results;
- changing default backend or numerical policy;
- GPU/special hardware claims without trusted-context approval;
- continuing after Claude and Codex do not converge after five review rounds
  for the same blocker.

## Approval Needs For Execution

For smooth visible execution, the user should approve:

1. escalated `claude -p` read-only review prompts for the master plan, material
   phase results, repair plans, and closeout;
2. CPU-only validation commands with `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`,
   including focused `pytest` and `python -m compileall`;
3. narrow, reviewed, non-destructive CPU-only Python diagnostic scripts or
   modules created by P51 phases, with exact paths recorded before execution;
4. static inspection commands such as `rg`, `sed`, `git diff --check`, and
   `git status`.

No approval is anticipated for network fetches, package installation, GPU runs,
detached execution, or destructive git commands. If any of those become
necessary, Codex must stop and ask separately.
