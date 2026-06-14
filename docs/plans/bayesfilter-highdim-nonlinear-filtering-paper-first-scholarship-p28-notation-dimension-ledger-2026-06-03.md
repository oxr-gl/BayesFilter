# P28 Notation And Dimension Ledger

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

audit_scope:
- Notation, dimension, measure, and coordinate-system consistency audit for P27.

what_is_not_concluded:
- This pass does not prove all formulas correct.
- This pass does not certify all basis and quadrature choices as numerically optimal.

## Object Audit

| object family | P27 anchor | status | comments |
|---|---|---|---|
| physical states and parameter `x_t, theta` | Sections 5--7 | PASS_WITH_REVIEW_RISK | The density factorization is clear; final visual check should ensure `theta` as integration variable vs differentiated parameter is never confused. |
| coordinate systems `r,z,u,z_t` | Sections 11--12 | PASS_WITH_REVIEW_RISK | Coordinate walk is present and human-facing. High-risk because Jacobians and retained coordinates recur throughout. |
| TT cores and ranks | Sections 8, 15, 31--33 | PASS_WITH_REVIEW_RISK | Shapes are stated in many places; equation inventory flags all shape formulas for deep check. |
| basis vectors and mass matrices | Sections 13, 18, 33 | PASS_WITH_REVIEW_RISK | Mass matrices defined; need deep check for all index conventions and transposes. |
| normalizers, shifts, floors | Sections 17, 33, 35, 52 | PASS_WITH_REVIEW_RISK | Stabilization defaults and normalizer identities included. Need careful audit for where tau/lambda integrate to one. |
| KR maps and preconditioning | Sections 19, 24 | HUMAN_REVIEW_REQUIRED | Most likely chair-reader and notation risk; local formulas present, but full teach-back and Jacobian signs require review. |
| fixed-branch derivative objects | Sections 32--51 | HUMAN_REVIEW_REQUIRED | The branch/narrowness story is good, but derivative dependency graph is dense and contains many critical equations. |
| validation model symbols | Sections 55--61 | PASS_WITH_REVIEW_RISK | Models and metrics are explicit; empirical settings must still be checked against Zhao--Cui visually. |

## Cross-Ledger Issues

| issue id | issue | affected ledgers | status |
|---|---|---|---|
| P28-I012 | Distinguish `theta` as Zhao--Cui parameter coordinate from `beta` as fixed-branch derivative parameter. | equation, notation, implementation, chair | REVIEW_REQUIRED |
| P28-I013 | Confirm every coordinate transform includes the correct Jacobian direction. | equation, source, MathDevMCP, chair | HUMAN_REVIEW_REQUIRED |
| P28-I014 | Confirm TT core index ordering matches implementation storage conventions throughout derivative sweeps. | equation, implementation | HUMAN_REVIEW_REQUIRED |

## Verdict

notation_dimension_verdict: `NOT_READY_FOR_FLAWLESS_CLAIM`

No obvious global notation collapse was found in this pass, but central objects remain high-risk and require detailed human review before submission as mathematically flawless.
