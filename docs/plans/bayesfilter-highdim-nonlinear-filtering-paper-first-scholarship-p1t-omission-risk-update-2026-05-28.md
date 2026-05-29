# P1T Omission-Risk Update

Date: 2026-05-28

metadata_date: 2026-05-28

seed_papers: five user-supplied blocker PDFs in `.local_sources/highdim_nonlinear_filtering/`.

what_is_not_concluded: see section "What Is Not Concluded".

## Purpose

Update the P1S omission-risk register after the user supplied the five blocker
PDFs.  This file records only risk movement caused by P1T source inspection.

## Updated Risk Rows

| p1s_risk | p1s_status | p1t_evidence | p1t_adjudication | reviewer_answer | remaining_action |
| --- | --- | --- | --- | --- | --- |
| Arasaratnam--Haykin CKF primary paper | `REMAINS_SOURCE_BLOCKED` | Local IEEE PDF validated and text-extracted; Sections II--VI and Appendices A--B checked. | `CLOSED` | The CKF baseline can now be cited and derived from the primary paper, with Gaussian/additive-noise scope and no high-dimensional overclaim. | Use in Ch34; still cite Jia separately for high-degree CKF. |
| Girolami--Calderhead RMHMC primary paper | `REMAINS_SOURCE_BLOCKED` | Local JRSS B PDF validated and text-extracted; Sections 2--6 and examples/cost caveats checked. | `CLOSED` | RMHMC can now be treated as a primary geometry-aware MCMC competitor/substrate. | Use in Ch36; derive only under stated metric assumptions. |
| High-dimensional PF collapse papers by Bengtsson--Bickel--Li and Snyder et al. | `REMAINS_SOURCE_BLOCKED` | Both local PDFs validated and text-extracted; Snyder `tau^2` heuristic/asymptotic discussion and Bengtsson--Bickel--Li formal propositions checked. | `CLOSED` | The chapter can now include a careful proposition/proof-sketch treatment of prior-proposal PF weight collapse under source-stated assumptions. | Use in Ch33/Ch35/Ch37; avoid universal PF impossibility claims. |
| Gordon--Salmond--Smith bootstrap PF original | `DEFER_TO_CHAPTER_REWRITE_WITH_EXPLICIT_SCOPE` / original detail blocked | Local IEE PDF validated; scan-only, OCR created; Sections 2--3 and conclusion checked. | `CLOSED_WITH_OCR_CAVEAT` | Original bootstrap filter history and algorithm can be cited, but exact formulas should be visually checked before final typesetting because the local PDF is image-only. | Use Gordon for origin, Arulampalam/Chopin for clean modern notation. |

## Remaining Reviewer Risks After P1T

- TT-cross/maxvol primary foundations remain source-blocked.
- Robust/pathwise DMZ transformations remain source-blocked.
- Broad Smolyak/Stroud/Genz sparse-grid/cubature foundations remain scoped or
  source-blocked if Ch34 goes beyond Jia/Arasaratnam source-local derivations.
- Rosenblatt/Knothe historical foundations remain source-local through modern
  transport papers unless primary/standard references are inspected.
- Complete forward-snowball coverage is still incomplete for many seed papers.
- Derivations in BayesFilter notation have not yet been MathDevMCP-audited.

## What Is Not Concluded

P1T does not make the survey comprehensive or chapters review-ready.  It closes
five source-access blockers and reduces the immediate reviewer risk around CKF,
RMHMC, bootstrap PF, and high-dimensional PF collapse.
