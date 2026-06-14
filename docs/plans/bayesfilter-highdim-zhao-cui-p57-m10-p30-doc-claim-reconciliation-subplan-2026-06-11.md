# P57-M10 Subplan: P30 Documentation And Claim Reconciliation

metadata_date: 2026-06-11
status: PLAN_REVIEW_CONVERGED

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the P30 LaTeX companion note describe the repaired source-route rank and UKF policy accurately? |
| Baseline/comparator | P30 LaTeX companion note at `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`, P56 audit, and P57 implemented result artifacts. |
| Primary pass criterion | The LaTeX text distinguishes source-faithful route, fixed-HMC adaptation, UKF scout, rank selection, and extension routes without overclaiming. |
| Veto diagnostics | P30 still describes old local/operator route as Zhao-Cui source-faithful; UKF or rank preflight language implies correctness; implementation deviates from documented math. |
| Not concluded | Documentation pass does not substitute for code tests. |

## Tasks

1. Update P30 equations/pseudocode only after implementation phases are
   sufficiently settled.
2. Mark P52/P53 local/operator rank route as extension/scout context.
3. Add source-route rank selection and UKF policy language from P57-M7.
4. Build or syntax-check the document if feasible.
5. If another LaTeX draft such as a P40 companion also needs reconciliation,
   create a separate reviewed amendment after the P30 target is handled. Do not
   treat any other file as an alternative P30 target for this phase.
6. Write result artifact.

## Required Checks

- `rg -n "UKF|rank|Zhao|SIRT|source|spatial SIR|operator route" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex docs/plans/*.md`
- Claude review must inspect the actual edited LaTeX, not just the result note.
