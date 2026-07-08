# Phase 3-5 Closeout Result: Integration, Documentation, And Audit

Date: 2026-07-07
Status: `CLOSED_FOR_IMPLEMENTATION_AND_TESTS`

## Scope Completed

- BayesFilter owns the central HMC tuning budget/timing policy.
- MacroFinance CCMA calls BayesFilter and no longer owns a fallback staged-timeout policy for `phase4y`.
- BayesFilter LaTeX docs now describe the promoted fixed-trajectory HMC algorithm, the public/private final handoff split, geometry-scaled budgets, and emergency caps versus progress evidence.
- Public redaction for passed final handoffs was repaired after read-only review.

## Documentation Updated

- `docs/chapters/ch21_hmc_for_state_space.tex`
- `docs/chapters/ch22_mass_matrices.tex`

The docs explicitly state that fixed-trajectory HMC is the promoted route, NUTS is reference/diagnostic only, and the budget formulas are tuning-work allocation rules rather than posterior convergence criteria.

## Residual Issues

- `one_country_zlb_ns_estimation.py` still contains local staged HMC timing constants. This was reported by read-only review but is outside the CCMA promoted-default repair. It should be handled by a dedicated ZLB/BayesFilter integration plan.
- No long CCMA tuning run was executed. The implementation is ready for a small CCMA public-path smoke, not for posterior claims.

## Stop/Continuation Decision

Continue only with a reviewed execution plan. The next smallest justified run is a public-path CCMA smoke that confirms the promoted BayesFilter policy is actually used and that public artifacts remain redacted on the current CCMA target.
