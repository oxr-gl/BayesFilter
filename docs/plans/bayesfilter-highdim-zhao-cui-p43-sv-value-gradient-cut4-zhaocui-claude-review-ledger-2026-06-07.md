# P43 Claude Review Ledger: SV Value and Gradient CUT4--Zhao-Cui Ladder

metadata_date: 2026-06-07
phase: P43

## Plan Review Iteration 1

status: `PASS_P43_PLAN_GOVERNANCE`

Reviewer summary:
- P43 stays within P42 guardrails as Tier-1 local diagnostics and disclaims HMC,
  Tier-2, and Tier-3 readiness.
- Autodiff is labeled diagnostic-only for tiny fixed fixtures; finite
  differences remain optional and governed rather than authoritative.
- Same-target evidence is separated from cross-target approximation evidence:
  CUT4 versus KSC Kalman-mixture, Zhao--Cui versus exact transformed dense, and
  KSC versus exact transformed as approximation-only.
- KSC-versus-exact mismatch is explicit.
- Dimension 2/3 Zhao--Cui is factorized scalar TT, not coupled multivariate TT.
- Generalized SV remains finite diagnostic coverage with explicit non-claims.

## Code Review Iteration 1

status: `PASS_P43_CODE_GOVERNANCE`

Execution note:
- The first worker attempt, `p43-code-review-iter1`, stayed alive without
  returning review output after a bounded wait and was stopped as an execution
  issue rather than a substantive governance block.
- The narrowed worker attempt, `p43-code-review-iter1b`, reviewed only the P43
  test, plan, and result artifacts and returned no blockers.

Reviewer summary:
- The same unconstrained parameterization is used for same-target score
  comparisons: per-coordinate `theta=(Phi^{-1}(gamma_i), log beta_i)` with
  fixed `sigma`.
- Same-target evidence is separated correctly:
  - KSC mixture CUT4 versus KSC Kalman;
  - exact transformed factorized Zhao--Cui/fixed-design TT versus exact dense;
  - KSC versus exact transformed as approximation-only.
- Autodiff is confined to tiny fixtures and described as diagnostic-only, not
  as a production analytic-score API.
- Each dimension has at least five deterministic score-difference directional
  residual checks.
- The generalized SV check is explicitly finite diagnostic/non-exact and uses
  the non-claim label
  `p43_generalized_sv_cut4_gradient_diagnostic_not_exact`.

Verdict: `PASS_P43_CODE_GOVERNANCE`
