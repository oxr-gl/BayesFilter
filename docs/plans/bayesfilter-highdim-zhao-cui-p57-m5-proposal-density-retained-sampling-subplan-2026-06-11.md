# P57-M5 Subplan: Proposal Density And Retained Sampling

metadata_date: 2026-06-11
status: PLAN_REVIEW_CONVERGED

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can retained sample generation and proposal correction match the author Algorithm 3 density semantics? |
| Baseline/comparator | Paper equations (21)--(23), Algorithm 3, author `full_sol.m:33-38`, `eval_irt`, and `eval_pdf`. |
| Primary pass criterion | Proposal correction divides by the same density represented by author `eval_pdf(sirt,r)` on local transported samples `r` after `eval_irt`, with any affine `x = mu + L r` determinant handled in the target/proposal coordinate convention; correction sign, determinant policy, and normalizer updates are tested. |
| Veto diagnostics | Real source-route transport uses `log_reference_density(reference)` alone as denominator; proposal correction sign untested; retained samples lack route manifest. |
| Not concluded | No full sequential filtering until M6 connects retained objects across time. |

## Tasks

1. Patch or plan the transport protocol so real transports expose
   `log_proposal_density(local_samples, reference_samples)` or `eval_pdf`.
   For a source-faithful real transport this must equal the author SIRT density
   in local `r` coordinates, not merely the base/reference density of the
   reference samples. Any Jacobian-aware wrapper must document exactly which
   coordinate measure it returns.
2. Preserve analytic test doubles where reference density is equivalent, but
   label that equivalence explicitly.
3. Add tests for proposal-density semantics, affine determinant handling,
   correction weights, and finite ESS.
4. Add a required identity check:
   `log_weight = -fun_post(local_r) - log_eval_pdf_sirt(local_r)` in the same
   coordinate convention as author `full_sol.m`; if BayesFilter evaluates the
   target in affine `x` coordinates, the result must show the matching
   `-log|det L|` placement.
5. Confirm the result remains differentiable under fixed draws.
6. Write result artifact.

## Required Checks

- `rg -n "source_route_generate_retained_samples|log_reference_density|proposal|eval_pdf|effective_sample" bayesfilter/highdim tests/highdim`
- Claude review must specifically answer whether the denominator matches the
  author `eval_pdf(sirt,r)` semantics.
