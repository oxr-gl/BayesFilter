# P57-M7 Subplan: Source-Faithful Rank And UKF Calibration

metadata_date: 2026-06-11
status: PLAN_REVIEW_CONVERGED

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | How should rank be selected for the fixed TT/SIRT source route, and where can UKF help without becoming a false comparator? |
| Baseline/comparator | Author SIR rank ladder `{10,20,40}`, fixed TT/SIRT transport memory, same-route rank convergence, lower-rung dense references, P52 UKF scout as diagnostic-only. |
| Primary pass criterion | Rank selection is tied to fixed source-route transport cores and same-route evidence; UKF only proposes centers/scales/rank candidates and can veto nonsense, not certify correctness or final rank. A promoted rank must satisfy a declared comparator/tolerance rule before execution of the promoted spatial SIR row. |
| Veto diagnostics | Old local/operator `R_eff` rank budget used as final source-faithful rank selector; UKF promoted to truth; largest available rank selected without comparator; memory cap ignores TT/SIRT transport and KR state. |
| Not concluded | No d=18 spatial SIR success unless M9 passes; no d=50/d=100 correctness. |

## Tasks

1. Reclassify existing `rank_budget.py` and `ukf_scout.py` outputs as
   scout/preflight unless tied to fixed TT/SIRT route evidence.
2. Define memory budget terms for fixed TT/SIRT: TT cores, mass contractions,
   CDF/KR state, sample batches, autodiff workspace, and retained objects.
3. Use author d=18 rank ladder `{10,20,40}` as the first source anchor; justify
   any smaller practical ladder as a fixed-HMC approximation with evidence.
4. Define UKF outputs allowed to initialize centers, scales, covariance
   structure, preconditioner starting values, and candidate rank ranges.
5. Define pass/block rules for rank convergence, dense lower-rung tieout, and
   no-comparator cases. Default promotion rule:
   - if a dense/exact same-target lower-rung reference is available, promote the
     smallest feasible fixed TT/SIRT rank whose per-observation log-likelihood
     error is `<= 1e-3`, filtered mean scaled RMSE is `<= 5e-2`, covariance
     relative Frobenius error is `<= 1e-1`, and replay residual is zero within
     dtype-stable serialization;
   - if only same-route ranks are available, promote rank `r` only if a strictly
     higher feasible rank `r_hi` has run under the same frozen route and the
     same observable tolerances hold for `r` versus `r_hi`;
   - never promote the largest available feasible rank by self-convergence
     alone; emit `BLOCK_P57_M7_RANK_COMPARATOR_MISSING` if no higher-rank or
     dense comparator exists;
   - gradient promotion requires directional cosine `>= 0.995` and relative
     score error `<= 5e-2` where a reference score exists; finite gradients alone
     are explanatory only.

## Required Checks

- `pytest -q tests/highdim/test_p52_ukf_scout.py tests/highdim/test_p52_rank_budget.py tests/highdim/test_p53_m5_rank_selection_integration.py` only as regression/scout checks, not source-faithful proof.
- Claude review must verify the plan no longer lets P52/P53 old rank code close
  source-faithful spatial SIR.
