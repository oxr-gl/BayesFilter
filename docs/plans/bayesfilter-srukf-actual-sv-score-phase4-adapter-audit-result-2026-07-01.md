# Phase 4 Result: Adapter Derivation Audit

Date: 2026-07-01

Status: PASSED_TO_PHASE_5_IMPLEMENTATION_SCOPE

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Advance to Phase 5 implementation-scope preparation after bounded Claude result review. |
| Primary criterion status | Met locally: adapter labels are present, key derivatives passed symbolic checks, target/nonclaim boundaries are visible, and the Phase 3 variance-vs-factor caveat was resolved with an explicit factor derivative label. |
| Veto diagnostic status | No local veto remains.  Claude result review remains the final Phase 4 convergence check before Phase 5 execution. |
| Main uncertainty | MathDevMCP could not formalize every displayed equation as a proof obligation; some label lookups used fallback/stale-cache context before the new factor label indexed cleanly. |
| Next justified action | Run bounded Claude review of this Phase 4 result, then refresh Phase 5 implementation subplan to match audited labels. |
| Not concluded | No implementation, numerical accuracy, HMC readiness, leaderboard admission, exact actual-SV likelihood, or same-target transformed actual-SV likelihood is concluded. |

## Evidence Contract Outcome

Question:

- Does the actual-SV adapter derivation survive audit for target law,
  dimensions, derivatives, and nonclaim boundaries?

Outcome:

- Yes for the Phase 4 local audit.  The adapter remains a raw actual-SV
  Gaussian-closure surrogate route and does not admit exact/same-target
  transformed actual-SV claims.

## Labels Audited

- `sec:bf-hd-actual-sv-srukf-augmented-adapter`
- `eq:bf-hd-actual-sv-srukf-model`
- `eq:bf-hd-actual-sv-srukf-parameterization`
- `eq:bf-hd-actual-sv-srukf-parameter-derivatives`
- `eq:bf-hd-actual-sv-srukf-augmented-variable`
- `eq:bf-hd-actual-sv-srukf-augmented-law`
- `eq:bf-hd-actual-sv-srukf-transition-map`
- `eq:bf-hd-actual-sv-srukf-observation-map`
- `eq:bf-hd-actual-sv-srukf-transition-derivatives`
- `eq:bf-hd-actual-sv-srukf-observation-state-derivative`
- `eq:bf-hd-actual-sv-srukf-observation-parameter-derivatives`
- `eq:bf-hd-actual-sv-srukf-initial-law`
- `eq:bf-hd-actual-sv-srukf-initial-derivatives`
- `eq:bf-hd-actual-sv-srukf-initial-factor-derivatives`
- `eq:bf-hd-actual-sv-srukf-surrogate-loglik`
- `eq:bf-hd-actual-sv-srukf-score-handoff`
- `eq:bf-hd-actual-sv-srukf-collapsed-law-equivalence`
- `eq:bf-hd-actual-sv-srukf-nonclaims`

## MathDevMCP And Symbolic Checks

MathDevMCP:

- `latex_label_lookup` found
  `sec:bf-hd-actual-sv-srukf-augmented-adapter` by fallback text context and
  reported stale-cache/index warnings.
- `extract_latex_context` found
  `eq:bf-hd-actual-sv-srukf-observation-parameter-derivatives` by fallback text
  context with stale-cache/index warnings.
- `extract_latex_context` found
  `eq:bf-hd-actual-sv-srukf-initial-factor-derivatives` as an indexed equation
  in section `Actual-SV SR-UKF Augmented-Noise Adapter`.
- `check_equality` verified the stationary variance derivative algebra:
  `2*sigma**2*gamma*gd/(1-gamma**2)**2` equals
  `gd*(2*gamma*sigma**2/(1-gamma**2)**2)`.
- An attempted MCP `diff(...)` observation-derivative check was inconclusive
  because the backend could not encode the expression; this is recorded as a
  parser limitation, not a mathematical pass.

Local symbolic sanity checks:

- A deterministic SymPy script simplified all of the following residuals to
  zero:
  - `dZ_dgamma_chain`;
  - `dZ_dbeta_log_chain`;
  - `dX_dgamma_chain`;
  - `d_var_dgamma_chain`;
  - `d_factor_dgamma_chain`.

## Local Text Checks

Commands run:

- `git diff --check -- docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex docs/plans/bayesfilter-srukf-actual-sv-score-phase3-adapter-derivation-review-excerpt-2026-07-01.md docs/plans/bayesfilter-srukf-actual-sv-score-phase3-augmented-adapter-derivation-result-2026-07-01.md docs/plans/bayesfilter-srukf-actual-sv-score-phase4-adapter-audit-subplan-2026-07-01.md docs/plans/bayesfilter-srukf-actual-sv-score-visible-execution-ledger-2026-07-01.md`
- Fixed-string `rg` checks for `initial-factor-derivatives`,
  `scalar stationary factor`, `variance derivative and scalar factor
  derivative`, and `variance-vs-factor`.
- Label-presence `rg` checks for the adapter equations listed above.

## Boundary Audit

The derivation states:

- the default augmented variable is `(H_{t-1}, U_t, E_t)`;
- the observation shock is part of the default sigma-point variable;
- `theta=(theta_gamma, theta_beta)` with fixed `sigma`;
- the raw observation map is not the transformed datum `z_t=log(y_t^2)`;
- the score is for the raw Gaussian-closure surrogate scalar;
- a two-coordinate collapsed route requires law and derivative equivalence;
- exact actual-SV, same-target transformed-likelihood, `GradientTape`,
  historical SVD/eigenderivative, and strict-SPD principal-root admissions are
  explicitly excluded.

## Implementation-Facing Handoff

Phase 5 must implement the factor-propagating backend against these exact
objects:

- placed points from `eq:bf-hd-actual-sv-srukf-augmented-law`;
- map derivatives from
  `eq:bf-hd-actual-sv-srukf-transition-derivatives`,
  `eq:bf-hd-actual-sv-srukf-observation-state-derivative`, and
  `eq:bf-hd-actual-sv-srukf-observation-parameter-derivatives`;
- initial variance and scalar factor derivatives from
  `eq:bf-hd-actual-sv-srukf-initial-derivatives` and
  `eq:bf-hd-actual-sv-srukf-initial-factor-derivatives`;
- score handoff from `eq:bf-hd-actual-sv-srukf-surrogate-loglik` and
  `eq:bf-hd-actual-sv-srukf-score-handoff`;
- nonclaim boundary from `eq:bf-hd-actual-sv-srukf-nonclaims`.

Phase 5 must not wire the historical `tf_svd_sigma_point_filter` value route,
any `GradientTape` score route, or a strict-SPD principal-root derivative route
as the admitted analytical score implementation.
