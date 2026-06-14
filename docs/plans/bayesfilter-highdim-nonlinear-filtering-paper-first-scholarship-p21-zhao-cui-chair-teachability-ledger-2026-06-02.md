# P21 Zhao--Cui Chair Teachability Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- P20 integrated Zhao--Cui companion and fixed-branch gradient note.

what_is_not_concluded:
- No claim of actual panel-chair endorsement.
- No executable prototype claim.
- No exact posterior accuracy claim.
- No HMC convergence claim.
- No production implementation readiness claim.

## Teach-Back Targets

| Target | P21 anchors | Intended chair teach-back |
|---|---|---|
| normalizer derivative | P21-13--P21-23 | differentiate mass, then use \(\dot Z/Z\) |
| squared-density derivative | P21-24--P21-30a | square gives nonnegative density; derivative is \(2\phi\dot\phi\) |
| mass contraction derivative | P21-31--P21-39a | integrate by contracting one-dimensional mass matrices; differentiate every factor once |
| fixed solve derivative | P21-40--P21-50a | frozen solve rule gives \(N\dot g=\dot d-\dot N g\) |
| carried-filter quotient | P21-51--P21-57i | next filter is \(a/Z\), derivative is quotient rule; carried object is \(P_t,\dot P_t:(p,p)\) |
| next-step target derivative | P21-58--P21-63 | target derivative needs previous filter derivative plus model derivatives |
| same-branch finite difference | P21-82--P21-87 | branch choices fixed, fitted cores recomputed |
| plausibility argument | P21-88--P21-90 | nonnegative approximation plus computable mass plus marginal gives normalized approximate filter |

## Current Self-Audit

Decision: `READY_FOR_CLAUDE_CHAIR_PERSONA_REVIEW_AFTER_ITERATION_1_PATCH`.

Codex believes P21 is more teachable than P20 for the gradient path because it
uses repeated scalar, two-coordinate, TT, and filtering interpretations before
the implementation-ready specification.

Post-Claude-iteration-1 controls added:

- Added teach-back checkpoint for squared-density derivative at P21-30a.
- Added teach-back checkpoint for mass-contraction derivative at P21-39a.
- Added teach-back checkpoint for fixed-solve derivative at P21-50a.
- Added carried-filter storage and quotient checkpoint at P21-57a--P21-57i.
