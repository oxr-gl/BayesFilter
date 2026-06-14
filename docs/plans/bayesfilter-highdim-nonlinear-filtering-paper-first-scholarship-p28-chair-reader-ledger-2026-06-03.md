# P28 Chair-Reader Ledger

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

audit_scope:
- Decision-relevant chair-reader audit from the viewpoint of an educated former chemistry academic with mathematical seriousness but no tensor-train background.

what_is_not_concluded:
- This is not a prose-polish pass.
- This does not replace mathematical equation audit.

## Chair-Reader Findings

| issue id | finding | severity | satisfying change |
|---|---|---|---|
| P28-I015 | The broad story is now understandable: high-dimensional Bayesian density, TT low-rank interactions, squared TT nonnegativity, fixed branch for differentiability. | positive | Keep this narrative intact. |
| P28-I016 | KR maps and preconditioning remain the hardest conceptual sections for a non-TT chair. | medium | Before submission, visually check that the worked 2D KR example and preconditioning density walk are free of sign/Jacobian errors. |
| P28-I017 | Proposition 2 and the fixed-branch derivative are still the highest trust-risk sections. | high | Deep-check every display in Sections 45--51 and consider a one-page dependency diagram in the talk/slides even if P27 remains unchanged. |
| P28-I018 | The 103-page length is appropriate for an annotated companion, but only if the title/abstract do not imply empirical success. | low | P27 already states validation protocol, not outcomes. |
| P28-I019 | A single small equation error in KR or derivative sections would disproportionately damage trust. | high | Treat KR Jacobian/change-of-variable and derivative quotient/solve equations as mandatory deep-check items. |

## Verdict

chair_reader_verdict: `PERSUASIVE_WITH_HIGH_RISK_SECTIONS`

A chemist chair can likely understand the method narrative and why it is plausible, but the KR/preconditioning and fixed-branch derivative sections still need targeted equation-level scrutiny before submission.
