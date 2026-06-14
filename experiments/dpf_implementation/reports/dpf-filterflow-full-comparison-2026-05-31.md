# Filterflow Full Comparison For BayesFilter OT-DPF

## Decision

`full_comparison_filterflow_reference_matched_with_fixed_sinkhorn_diagnostic_gap`

## Scope

This result consolidates the matched executable-filterflow LGSSM audit and the
remaining final-gaps diagnostics into one full comparison artifact.  It uses the
patched local filterflow branch as external reference code and keeps BayesFilter
implementation evidence under the experimental TF/TFP DPF lane.

## Filterflow Reference

- Branch: `bayesfilter-py311-compat`
- Commit: `5d8300ba247c4c17e1a301a22560c24fd0670bfe`
- Upstream base: `5d8300ba247c4c17e1a301a22560c24fd0670bfe`
- Status: `## bayesfilter-py311-compat
 M scripts/base.py
 M scripts/simple_linear_common.py
 M scripts/simple_linear_smoothness.py`
- Diff summary: `scripts/base.py                     | 7 ++++---
 scripts/simple_linear_common.py     | 5 +++++
 scripts/simple_linear_smoothness.py | 6 ++++--
 3 files changed, 13 insertions(+), 5 deletions(-)`
- Reference status: patched local Python 3.11 compatibility branch, not pristine upstream source

## Comparison Matrix

| Lane | Source | Status | Primary scalar | Interpretation |
| --- | --- | --- | --- | --- |
| `paper_table_1` | Corenflos main paper | `context_only` | per_time_log_likelihood_error | published context, not sole authority for executable comparison |
| `exact_kalman` | filterflow_and_bayesfilter | `pass` | lgssm_log_likelihood |  |
| `filterflow_pf` | patched_filterflow | `executed` | per_time_log_likelihood_error | external classical baseline |
| `bayesfilter_pf` | tf_tfp | `within_filterflow_mc_band` | per_time_log_likelihood_error | internal bootstrap PF calibration against filterflow PF |
| `filterflow_regularised_transform` | patched_filterflow | `executed` | per_time_log_likelihood_error | external DPF reference |
| `bayesfilter_filterflow_style_transport` | tf_tfp_audit_mirror | `within_filterflow_mc_band` | per_time_log_likelihood_error | matched paper-style annealed regularized transport semantics |
| `bayesfilter_fixed_target_sinkhorn` | tf_tfp | `within_filterflow_mc_band` | per_time_log_likelihood_error_plus_sinkhorn_residuals | diagnostic branch, not filterflow-equivalent |
| `bayesfilter_ledh_pfpf_ot` | tf_tfp | `structured_not_run_as_matched_filterflow_table_lane` | not_available_under_matched_filterflow_protocol | Existing LEDH-PF-PF-OT LGSSM runner uses the repo fixture and proposal-correction diagnostics; it was not promoted into this filterflow table because this comparison requires the exact filterflow observation path, covariance convention, seed protocol, and per-time likelihood-error scalar. |
| `smoothness_gradient_contract` | patched_filterflow_and_kalman_fd_reference | `finite_gradient_smoke_with_severe_unreconciled_magnitude_mismatch` | bounded_gradient_smoke | finite-gradient smoke only; severe unresolved scalar/randomness/gradient-magnitude mismatch remains |

## Method Status Summary

| Key | Value |
| --- | --- |
| `matched_audit_decision` | `filterflow_style_transport_matched` |
| `final_gaps_decision` | `final_gaps_closed_unconditional_fixed_sinkhorn_compute_gap_identified` |
| `bayesfilter_pf_status` | `within_filterflow_mc_band` |
| `bayesfilter_filterflow_style_transport_status` | `within_filterflow_mc_band` |
| `bayesfilter_fixed_target_sinkhorn_status` | `within_filterflow_mc_band` |
| `fixed_target_sinkhorn_diagnostic_status` | `epsilon_0.25_unconditional_nontriggered_budget_gap` |
| `smoothness_gradient_status` | `finite_gradient_smoke_with_severe_unreconciled_magnitude_mismatch` |

## Matched LGSSM Table Comparison

| External | BayesFilter | eps | theta | filterflow mean | BayesFilter mean | delta | within 1 sd | status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| filterflow_pf | bayesfilter_pf | N/A | 0.25 | -1.02587 | -1.02157 | 0.00430025 | True | `executed` |
| filterflow_pf | bayesfilter_pf | N/A | 0.5 | -0.862692 | -0.866308 | -0.00361567 | True | `executed` |
| filterflow_pf | bayesfilter_pf | N/A | 0.75 | -0.939249 | -0.921244 | 0.0180054 | True | `executed` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.25 | 0.25 | -1.02566 | -1.04944 | -0.023776 | True | `executed` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.25 | 0.5 | -0.857608 | -0.883816 | -0.0262082 | True | `executed` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.25 | 0.75 | -0.91767 | -0.957161 | -0.0394903 | True | `executed` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.5 | 0.25 | -1.02654 | -1.04961 | -0.0230692 | True | `executed` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.5 | 0.5 | -0.860413 | -0.884287 | -0.0238741 | True | `executed` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.5 | 0.75 | -0.925254 | -0.952295 | -0.0270404 | True | `executed` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.75 | 0.25 | -1.02692 | -1.04967 | -0.022749 | True | `executed` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.75 | 0.5 | -0.860785 | -0.88429 | -0.0235046 | True | `executed` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.75 | 0.75 | -0.930679 | -0.952186 | -0.0215067 | True | `executed` |
| filterflow_regularized | bayesfilter_filterflow_style_transport_ess | 0.25 | 0.25 | -1.02566 | -1.04875 | -0.0230848 | True | `executed` |
| filterflow_regularized | bayesfilter_filterflow_style_transport_ess | 0.25 | 0.5 | -0.857608 | -0.874091 | -0.0164834 | True | `executed` |
| filterflow_regularized | bayesfilter_filterflow_style_transport_ess | 0.25 | 0.75 | -0.91767 | -0.944457 | -0.0267869 | True | `executed` |
| filterflow_regularized | bayesfilter_filterflow_style_transport_ess | 0.5 | 0.25 | -1.02654 | -1.04911 | -0.0225735 | True | `executed` |
| filterflow_regularized | bayesfilter_filterflow_style_transport_ess | 0.5 | 0.5 | -0.860413 | -0.876199 | -0.0157859 | True | `executed` |
| filterflow_regularized | bayesfilter_filterflow_style_transport_ess | 0.5 | 0.75 | -0.925254 | -0.945166 | -0.0199113 | True | `executed` |
| filterflow_regularized | bayesfilter_filterflow_style_transport_ess | 0.75 | 0.25 | -1.02692 | -1.04926 | -0.0223452 | True | `executed` |
| filterflow_regularized | bayesfilter_filterflow_style_transport_ess | 0.75 | 0.5 | -0.860785 | -0.876965 | -0.0161795 | True | `executed` |
| filterflow_regularized | bayesfilter_filterflow_style_transport_ess | 0.75 | 0.75 | -0.930679 | -0.948929 | -0.0182495 | True | `executed` |

## Red Flags

| ID | Severity | Status | Detail |
| --- | --- | --- | --- |
| `paper_transition_covariance_ambiguity` | `medium` | `recorded_and_controlled` | Paper/supplement text says 0.5 I_2; executable filterflow uses I_2 and prior bounded rerun showed Table 1 scale matches executable I_2. |
| `patched_filterflow_not_pristine` | `medium` | `recorded` | Local filterflow is a Python 3.11 compatibility branch. |
| `fixed_target_sinkhorn_not_paper_equivalent` | `medium` | `epsilon_0.25_unconditional_nontriggered_budget_gap` | BayesFilter fixed-target Sinkhorn remains a diagnostic branch and must not be read as Corenflos/filterflow annealed regularized transport. |
| `smoothness_gradient_severe_unreconciled_magnitude_mismatch` | `high` | `finite_gradient_smoke_with_severe_unreconciled_magnitude_mismatch` | Bounded smoothness run produced finite gradients, but severe scalar/randomness/gradient-magnitude reconciliation gaps against Kalman finite-difference diagnostics remain. |

## Discrepancy Ledger

| ID | Status | Detail |
| --- | --- | --- |
| `kalman_alignment` | `pass` | max_abs_delta=7.26172e-08 |
| `pf_calibration` | `within_filterflow_mc_band` | BayesFilter PF versus filterflow PF under matched LGSSM protocol. |
| `paper_style_transport_match` | `within_filterflow_mc_band` | BayesFilter audit mirror versus filterflow RegularisedTransform. |
| `fixed_target_sinkhorn_branch` | `within_filterflow_mc_band` | epsilon_0.25_unconditional_nontriggered_budget_gap |
| `gradient_smoothness` | `finite_gradient_smoke_with_severe_unreconciled_magnitude_mismatch` | Finite-gradient smoke only; severe scalar/randomness/gradient-magnitude mismatch remains unreconciled. |
| `ledh_pfpf_ot_matched_table` | `not_run_structured_scope_limit` | No matched filterflow-table scalar was promoted for LEDH-PF-PF-OT in this audit. |

## Smoothness Gradient Diagnostics

- Status: `finite_gradient_smoke_with_severe_unreconciled_magnitude_mismatch`
- Finite likelihoods: `True`
- Finite gradients: `True`
- Likelihood RMSE: `323943.654172315`
- Gradient RMSE: `144487904.8897196`
- Gradient max absolute delta: `511228982.96222275`
- Gradient cosine vs Kalman finite difference: `0.8895568190836275`
- Gradient sign agreement: `0.9375`

## Fixed-Target Sinkhorn Diagnostics

- Status: `epsilon_0.25_unconditional_nontriggered_budget_gap`
- Diagnostic scope: This diagnoses the BayesFilter fixed-target Sinkhorn lane only. The old veto can occur on non-triggered rows because the diagnostic path computed Sinkhorn before masking by ESS. It is not paper-equivalence evidence for filterflow's annealed transport.
- Epsilon 0.25 budget 100 max residual: `0.00012399118874682064`
- Epsilon 0.25 budget 500 max residual: `5.138093904899499e-06`

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No general nonlinear-SSM validity is concluded.
- No external macro-model validation is concluded.
- No banking/model-risk claim is concluded.
- No monograph claim is concluded.
- No claim that patched filterflow is pristine upstream source is concluded.
- No claim that fixed-target Sinkhorn is filterflow-equivalent is concluded.
- No full supplement figure or learning-table reproduction is concluded.
