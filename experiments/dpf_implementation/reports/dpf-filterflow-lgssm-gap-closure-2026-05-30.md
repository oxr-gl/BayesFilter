# Filterflow LGSSM Gap-Closure Rerun

## Decision

`filterflow_style_transport_matched`

## Summary

This rerun uses the patched external filterflow branch and the corrected
BayesFilter experimental filterflow-style transport mirror.  It is a
Section-5.1-style executable-code match, not an exact paper-table claim.

## Gap-Closure Ledger

| ID | Status | Detail |
| --- | --- | --- |
| `filterflow_executable` | `bayesfilter-py311-compat` | 5d8300ba247c4c17e1a301a22560c24fd0670bfe |
| `paper_code_setting_ledger` | `section_5_1_style_not_exact_paper_table_claim` | Matched to executable filterflow simple_linear_comparison settings: transition covariance I_2, observation covariance 0.1 I_2, T=150, N=25, theta grid 0.25/0.5/0.75, RegularisedTransform scaling=0.9 and convergence_threshold=1e-3. Earlier audit recorded a paper/code covariance ambiguity, so exact paper-table reproduction is not claimed here. |
| `kalman_alignment` | `pass` | 7.26172402210068e-08 |
| `pf_calibration` | `within_filterflow_mc_band` |  |
| `corrected_filterflow_style_transport` | `within_filterflow_mc_band` |  |
| `fixed_sinkhorn_small_epsilon` | `veto_or_missing` |  |
| `gradient_smoothness_replication` | `not_run_separate_gap` | This gap closure reruns LGSSM likelihood behavior only; gradient/smoothness replication remains separate. |

## Filterflow

- Branch: `bayesfilter-py311-compat`
- Commit: `5d8300ba247c4c17e1a301a22560c24fd0670bfe`
- Status: `## bayesfilter-py311-compat
 M scripts/base.py
 M scripts/simple_linear_common.py
 M scripts/simple_linear_smoothness.py`
- Diff summary: `scripts/base.py                     | 7 ++++---
 scripts/simple_linear_common.py     | 5 +++++
 scripts/simple_linear_smoothness.py | 6 ++++--
 3 files changed, 13 insertions(+), 5 deletions(-)`

## Comparison

| External | BayesFilter | eps | theta | filterflow mean | BayesFilter mean | delta | within 1 sd | status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| filterflow_pf | bayesfilter_pf | N/A | 0.25 | -1.02587 | -1.02157 | 0.00430025 | True | `executed` |
| filterflow_pf | bayesfilter_pf | N/A | 0.5 | -0.862692 | -0.866308 | -0.00361567 | True | `executed` |
| filterflow_pf | bayesfilter_pf | N/A | 0.75 | -0.939249 | -0.921244 | 0.0180054 | True | `executed` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.25 | 0.25 | -1.02566 | N/A | N/A | None | `veto` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.25 | 0.5 | -0.857608 | N/A | N/A | None | `veto` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.25 | 0.75 | -0.91767 | N/A | N/A | None | `veto` |
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

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No HMC readiness is concluded.
- No posterior correctness is concluded.
- No general nonlinear-SSM validity is concluded.
- No claim that finite relaxed OT is categorical PF is concluded.
- No claim that patched filterflow is untouched upstream code is concluded.
- No gradient/smoothness replication is concluded.
- No exact paper-table reproduction is concluded.
