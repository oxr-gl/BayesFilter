# P57-M8 Subplan: Preconditioned Algorithm 5 Route

metadata_date: 2026-06-11
status: PLAN_REVIEW_CONVERGED

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter implement the paper/source preconditioned route needed by the spatial SIR example? |
| Baseline/comparator | Paper Algorithm 5, preconditioning equations, author `pre_sol.m`, SIR paper text saying linear preconditioning is used. |
| Primary pass criterion | A fixed-HMC version of the preconditioned route preserves source maps `Tu2x`/`Tx2u`, residual SIRT fit, retained marginal step, proposal correction, and frozen schedules. |
| Veto diagnostics | Preconditioning skipped for paper-scale SIR claim; local/operator route substituted; residual route lacks proposal correction or retained marginal. |
| Not concluded | No d=18 pass until M9 validates the full route. |

## Tasks

1. Re-open paper/source preconditioning anchors.
2. Implement or plan linear preconditioner construction in TensorFlow.
3. Connect residual SIRT transport to M2-M6 source-route interfaces.
4. Add low-dimensional preconditioned analytic tests before spatial SIR.
5. Write result artifact.

## Required Checks

- `rg -n "precondition|residual|Tu2x|Tx2u|Algorithm 5|linear" docs/plans bayesfilter/highdim tests/highdim third_party/audit/zhao_cui_tensor_ssm_p10/source`
- Claude review must verify preconditioning is source anchored, not merely a
  numerical convenience.
