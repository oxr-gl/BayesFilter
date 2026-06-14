# Filterflow LGSSM Matched Cross-Audit

## Decision

`filterflow_style_transport_matched`

## Summary

This rerun uses the patched external filterflow branch and the same fixed
observation path for filterflow and BayesFilter.  Algorithmic random streams
are fixed but not bitwise matched.

## Filterflow

- Branch: `bayesfilter-py311-float64-reference`
- Commit: `ff0048060fd4cff43dbea606d14275e40e2ac084`
- Status: `## bayesfilter-py311-float64-reference`
- Diff summary: `clean`

## Kalman Alignment

- Max absolute log-likelihood delta: `2.274e-13`
- Within tolerance: `True`

## Comparison

| External | BayesFilter | eps | theta | filterflow mean | BayesFilter mean | delta | within 1 sd | status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| filterflow_pf | bayesfilter_pf | N/A | 0.25 | -1.03736 | -1.02157 | 0.0157965 | True | `executed` |
| filterflow_pf | bayesfilter_pf | N/A | 0.5 | -0.862022 | -0.866308 | -0.00428618 | True | `executed` |
| filterflow_pf | bayesfilter_pf | N/A | 0.75 | -0.912982 | -0.921244 | -0.00826177 | True | `executed` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.25 | 0.25 | -1.03963 | -1.04944 | -0.00981192 | True | `executed` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.25 | 0.5 | -0.864563 | -0.883816 | -0.0192528 | True | `executed` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.25 | 0.75 | -0.914135 | -0.957161 | -0.0430259 | True | `executed` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.5 | 0.25 | -1.03982 | -1.04961 | -0.00978671 | True | `executed` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.5 | 0.5 | -0.863701 | -0.884287 | -0.0205863 | True | `executed` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.5 | 0.75 | -0.91423 | -0.952295 | -0.0380643 | True | `executed` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.75 | 0.25 | -1.03987 | -1.04967 | -0.00979469 | True | `executed` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.75 | 0.5 | -0.862902 | -0.88429 | -0.0213879 | True | `executed` |
| filterflow_regularized | bayesfilter_scaled_fixed_sinkhorn_ess | 0.75 | 0.75 | -0.914533 | -0.952186 | -0.0376529 | True | `executed` |
| filterflow_regularized | bayesfilter_filterflow_style_transport_ess | 0.25 | 0.25 | -1.03963 | -1.04875 | -0.00912073 | True | `executed` |
| filterflow_regularized | bayesfilter_filterflow_style_transport_ess | 0.25 | 0.5 | -0.864563 | -0.874091 | -0.00952802 | True | `executed` |
| filterflow_regularized | bayesfilter_filterflow_style_transport_ess | 0.25 | 0.75 | -0.914135 | -0.944457 | -0.0303225 | True | `executed` |
| filterflow_regularized | bayesfilter_filterflow_style_transport_ess | 0.5 | 0.25 | -1.03982 | -1.04911 | -0.00929105 | True | `executed` |
| filterflow_regularized | bayesfilter_filterflow_style_transport_ess | 0.5 | 0.5 | -0.863701 | -0.876199 | -0.0124981 | True | `executed` |
| filterflow_regularized | bayesfilter_filterflow_style_transport_ess | 0.5 | 0.75 | -0.91423 | -0.945166 | -0.0309352 | True | `executed` |
| filterflow_regularized | bayesfilter_filterflow_style_transport_ess | 0.75 | 0.25 | -1.03987 | -1.04926 | -0.00939094 | True | `executed` |
| filterflow_regularized | bayesfilter_filterflow_style_transport_ess | 0.75 | 0.5 | -0.862902 | -0.876965 | -0.0140628 | True | `executed` |
| filterflow_regularized | bayesfilter_filterflow_style_transport_ess | 0.75 | 0.75 | -0.914533 | -0.948929 | -0.0343957 | True | `executed` |

## Discrepancies

| ID | Status | Detail |
| --- | --- | --- |
| `kalman_alignment` | `pass` | 2.2737367544323206e-13 |
| `fixed_sinkhorn_match` | `within_filterflow_mc_band` |  |
| `filterflow_style_transport_match` | `within_filterflow_mc_band` |  |
| `random_stream` | `not_bitwise_matched` | same observations and initial cloud; algorithmic random streams are fixed but independent |

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No HMC readiness is concluded.
- No posterior correctness is concluded.
- No general nonlinear-SSM validity is concluded.
- No claim that finite relaxed OT is categorical PF is concluded.
- No claim that patched filterflow is untouched upstream code is concluded.
