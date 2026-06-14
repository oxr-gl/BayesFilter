# P18 Zhao--Cui Eight-Issue Control Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- No claim that the P18 draft is final until Claude execution review accepts.
- No claim that equation surplus alone proves self-containedness.

## Controls

| Control | Status | Evidence |
|---|---|---|
| `SOURCE_ORDER` | `PASS_DRAFT` | P18 follows Sections 1, 2, 3, then 5 before fixed-branch extension. |
| `MISSING_DISPLAY_MATH` | `PASS_DRAFT` | Inventory maps Eqs. (1)--(26), (30)--(35), Algorithms 1--5, notation formulas, KR and preconditioning support formulas. |
| `SYMBOLS_MEASURES` | `PASS_DRAFT` | Reader contract defines dimensions, densities, measures; each source block adds local definitions. |
| `DERIVATION_GAPS` | `PASS_DRAFT_WITH_REVIEW_REQUIRED` | P18 adds derivations for joint density, recursion, TT contraction, squared mass, KR Jacobian, weights, preconditioning. Claude must spot-audit. |
| `IMPLEMENTATION_OBJECTS` | `PASS_DRAFT` | Each major source block has implementation contract or mini implementation contract. |
| `NUMERICAL_DIAGNOSTICS` | `PASS_DRAFT` | P18 lists positivity, finite normalizer, rank growth, condition number, mass matrix, Cholesky, CDF monotonicity, root residual, ESS, normalizer invariance, branch parity. |
| `CHEMISTRY_READER` | `PENDING_CLAUDE_PERSONA` | P18 adds low-dimensional analogies and after-math explanations; must be tested by Claude chemistry persona. |
| `FIXED_BRANCH_SEPARATION` | `PASS_DRAFT` | Exact hard boundary present; derivative material begins after it. |

Decision: `EIGHT_CONTROLS_READY_FOR_EXECUTION_REVIEW`.
