# Phase 4 Subplan: SIR Analytical Derivatives

status: REFRESHED_AFTER_P3_DRAFT_READY_FOR_REVIEW
date: 2026-06-23
phase: P4-SIR-ANALYTICAL-DERIVATIVES

## Phase Objective

Wire analytical SIR parameter derivatives into the no-autodiff route contract
and prove the production path does not ask TensorFlow to differentiate SIR
callbacks.

## Entry Conditions

- P3 derivation contract passed.
- P2 audit tool is available.
- P4 inherits
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-derivation-contract-2026-06-23.md`.
- P4 must restate and preserve the P3 theta order
  `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)`, model callback
  adjoint interfaces, and no-Zhao-Cui-comparator boundary before execution.
- P4 may edit only SIR derivative wiring and focused tests needed for this
  phase; transport repair, filter-level custom-gradient routing, GPU, FD, and
  actual-gradient validation remain forbidden.

## Required Artifacts

- Implementation diffs for analytical SIR derivative wiring.
- Focused tests for derivative route selection.
- P4 result artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase4-sir-analytical-derivatives-result-2026-06-23.md`.
- Refreshed P5 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase5-ledh-flow-logweight-adjoints-subplan-2026-06-23.md`.
- SIR derivative interface note or in-result section covering theta convention,
  RK4/RHS adjoint, observation gather VJP, and observation covariance
  parameter adjoint.

## Required Checks/Tests/Reviews

- CPU-hidden analytical derivative tests.
- Static audit proving no production SIR `GradientTape` is reached by the P4
  production candidate route.
- Diagnostic-only tiny autodiff comparison may be used but cannot promote.
- Bounded Claude review of implementation/result.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does SIR parameter sensitivity enter the LEDH gradient route analytically? |
| Baseline/comparator | Existing analytical derivative code and P3 obligations. |
| Primary criterion | Production route calls analytical SIR derivative functions for theta convention, RK4/RHS state sensitivities, observation gather, and observation covariance parameter adjoint; audit blocks autodiff fallback. |
| Veto diagnostics | Autodiff SIR callback in production; diagnostic parity treated as proof; missing theta-order contract; missing observation covariance adjoint; source-faithfulness claims without anchors. |
| Explanatory only | Tiny autodiff parity. |
| Not concluded | Full filter gradient correctness. |
| Preserved artifact | P4 result artifact path listed above. |

## Forbidden Claims/Actions

- Do not use Zhao-Cui as comparator for LEDH filter correctness.
- Do not rely on autodiff SIR derivatives in production.
- Do not run GPU/FD, actual-gradient validation, HMC, or posterior checks.
- Do not claim SIR derivative correctness certifies the full filter score.
- Do not edit transport custom-gradient bodies or route manifests in P4 unless
  only to block a forbidden production SIR autodiff fallback.

## Exact Next-Phase Handoff Conditions

Advance to P5 execution only if all P4 SIR derivative adjoint inputs/outputs
needed by downstream routing are implemented, tested, audited as no-production
autodiff, and recorded in the P4 result.

If P4 can only provide interface stubs or blocker placeholders, P4 must close
as `BLOCKED` or `FAILED` and may refresh only a non-execution remediation
subplan.  It must not authorize normal P5 implementation work.

The P5 subplan must inherit the P3/P4 interfaces for model callback cotangents
and theta-score accumulation after P4 passes.

## Stop Conditions

- Analytical derivative route cannot be found or safely wired.
- Audit fails and cannot be fixed within P4.
- Theta-order contract is ambiguous or not preserved.
- Source-faithfulness language is needed but cannot be anchored; otherwise P4
  must avoid source-faithfulness claims.
- Any required SIR adjoint piece named in the primary criterion is missing.
- Observation covariance parameter adjoint is missing.
- RK4/RHS, observation gather, or observation covariance adjoint cannot be
  specified without autodiff.
- Any needed comparison would require Zhao-Cui, FD, GPU, actual-gradient, or
  broad route repair evidence.
