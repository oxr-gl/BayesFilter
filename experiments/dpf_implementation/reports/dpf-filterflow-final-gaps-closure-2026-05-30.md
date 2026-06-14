# Filterflow Final Gaps Closure

## Decision

`final_gaps_closed_unconditional_fixed_sinkhorn_compute_gap_identified`

## Gap Ledger

| Gap | Status | Primary risk |
| --- | --- | --- |
| `paper_code_section_5_1_settings` | `closed_with_transition_covariance_ambiguity_recorded` | transition covariance paper/code ambiguity remains explicit |
| `filterflow_smoothness_gradient` | `closed_bounded_gradient_smoke_with_severe_unreconciled_magnitude_risk` | finite gradients only; severe scalar/randomness/gradient-magnitude mismatch remains unresolved and full Figure 1/Table 4 reproduction remains future work |
| `bayesfilter_fixed_target_sinkhorn_epsilon_0.25` | `epsilon_0.25_unconditional_nontriggered_budget_gap` | diagnostic only; not filterflow annealed transport equivalence |

## Paper/Code Settings

Status: `closed_with_transition_covariance_ambiguity_recorded`

| Item | Paper | Filterflow code | Status |
| --- | --- | --- | --- |
| `state_dimension` | 2 | 2 | `matched` |
| `transition_mean` | diag(theta_1, theta_2) x | diag(theta_1, theta_2) x | `matched` |
| `transition_covariance` | 0.5 I_2 | I_2 | `mismatch_or_version_ambiguity` |
| `observation_covariance` | 0.1 I_2 | 0.1 I_2 | `matched` |
| `horizon` | T=150 | T=150 | `matched` |
| `particle_count` | N=25 | N=25 in primary table loop | `matched` |
| `realizations` | 100 realizations | batch_size=100 in script main loop | `matched` |
| `epsilon_grid` | 0.25, 0.5, 0.75 | 0.25, 0.5, 0.75 | `matched` |
| `resampling_rule` | not fully specified in main text | NeffCriterion(0.5, True) | `code_specific` |
| `regularized_transport_scaling` | not fully specified in main text | scaling=0.9, convergence_threshold=1e-3 | `code_specific` |

Interpretation: The executable filterflow Section-5.1-style script matches most reported settings, but its transition covariance is I_2 while the main paper and supplement text state 0.5 I_2. A direct bounded rerun showed the published Table 1 scale is consistent with the executable filterflow I_2 convention and not with 0.5 I_2, so this is likely a paper typo or notation mismatch. BayesFilter reproduction audits use the executable filterflow I_2 convention, while recording the paper-text discrepancy explicitly.

## Smoothness Gradient

Status: `executed`

| Metric | Value |
| --- | ---: |
| `finite_likelihoods` | True |
| `finite_gradients` | True |
| `likelihood_rmse` | 323944 |
| `gradient_rmse` | 1.44488e+08 |
| `gradient_max_abs_delta` | 5.11229e+08 |
| `gradient_cosine_vs_kalman_fd` | 0.889557 |
| `gradient_sign_agreement` | 0.9375 |

## Fixed-Target Sinkhorn

Status: `epsilon_0.25_unconditional_nontriggered_budget_gap`

| epsilon | budget | max residual | median residual | below tol |
| ---: | ---: | ---: | ---: | --- |
| 0.25 | 25 | 0.000420767 | 3.0789e-06 | False |
| 0.25 | 50 | 0.000192996 | 2.04749e-09 | False |
| 0.25 | 100 | 0.000123991 | 1.15186e-15 | False |
| 0.25 | 200 | 5.47407e-05 | 4.16334e-17 | False |
| 0.25 | 500 | 5.13809e-06 | 4.16334e-17 | True |
| 0.25 | 1000 | 1.00979e-07 | 4.16334e-17 | True |
| 0.5 | 25 | 0.000141796 | 8.45478e-11 | False |
| 0.5 | 50 | 3.58369e-06 | 4.16334e-17 | True |
| 0.5 | 100 | 2.2936e-09 | 4.16334e-17 | True |
| 0.5 | 200 | 9.22873e-16 | 4.16334e-17 | True |
| 0.5 | 500 | 5.55112e-17 | 4.16334e-17 | True |
| 0.5 | 1000 | 5.55112e-17 | 4.16334e-17 | True |
| 0.75 | 25 | 2.80186e-07 | 2.01922e-15 | True |
| 0.75 | 50 | 4.84226e-12 | 4.16334e-17 | True |
| 0.75 | 100 | 5.55112e-17 | 4.16334e-17 | True |
| 0.75 | 200 | 5.55112e-17 | 4.16334e-17 | True |
| 0.75 | 500 | 5.55112e-17 | 4.16334e-17 | True |
| 0.75 | 1000 | 5.55112e-17 | 4.16334e-17 | True |

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

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No general nonlinear-SSM validity is concluded.
- No full paper figure or Table 4 reproduction is concluded.
- No claim that fixed-target Sinkhorn is filterflow paper-equivalent is concluded.
