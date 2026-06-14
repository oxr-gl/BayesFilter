# P30 Algorithm 5(c.2) Expansion And Audit Plan

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Rosenblatt, "Remarks on a Multivariate Transformation," Annals of Mathematical Statistics 1952.

audit_scope:
- Close P29-I001 by expanding and auditing Zhao--Cui Algorithm 5(c.2), the retained physical marginal derivation.
- Preserve P27 content and patch only the Algorithm 5(c.2) explanation in a P30 copy.

what_is_not_concluded:
- P30 does not certify all equations in the 103-page note.
- P30 does not prove empirical validation or production implementation readiness.
- P30 does not differentiate the adaptive Zhao--Cui algorithm.

## Evidence Contract

Question:
- Does the expanded Algorithm 5(c.2) derivation correctly transform the preconditioned residual marginal back into the retained physical-coordinate filter?

Pass criterion:
- The derivation states the source formula, defines the two-block variables, derives the formula step by step by conditional change of variables, and passes focused Claude review.

Veto diagnostics:
- wrong Jacobian direction;
- missing bridge marginal factor;
- denominator uses the wrong reference marginal;
- notation conflict between \(T_t^\ell\), \(S_t^\ell\), \(\widehat\rho_t\), and \(\widehat\nu_t^\sharp\);
- Claude accepted finding remains unpatched.

## Planned Files

- `...p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`
- compiled PDF beside it
- `...p30-alg5c2-source-ledger-2026-06-03.md`
- `...p30-alg5c2-mathdevmcp-ledger-2026-06-03.md`
- `...p30-alg5c2-claude-review-ledger-2026-06-03.md`
- `...p30-alg5c2-result-2026-06-03.md`

## Review Protocol

- Use MathDevMCP only for scalar ratio/cancellation identities.
- Use Claude Code as a hostile focused reviewer.
- Codex classifies every Claude finding as `ACCEPT`, `PARTIAL`, `DISPUTE`, or `CLARIFY`.

