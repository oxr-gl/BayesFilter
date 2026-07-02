# Phase 2 derivation: actual-SV SGQF manual score

Date: 2026-06-30

Status: `PHASE2_DERIVATION_REVIEW_READY`

## Scope

This note covers only the direct exact-transformed actual-SV fixed-SGQF row:

- model row: `zhao_cui_sv_actual_nongaussian_T1000`
- algorithm row: `fixed_sgqf`
- implementation path: `bayesfilter/highdim/sv_mixture_cut4.py`
- value function: `exact_transformed_sv_independent_panel_fixed_sgqf_filter`
- score function: `exact_transformed_sv_independent_panel_fixed_sgqf_score`

The score differentiates the fixed-SGQF approximate value recursion. It is not an exact-likelihood oracle, not a KSC Gaussian-mixture route, and not a coupled Zhao-Cui TT route.

## Target And Coordinates

The observation transform is

```text
z_t = log(y_t^2)
```

For each independent panel coordinate, the state recursion used by the fixed SGQF value route is

```text
h_t = gamma h_{t-1} + sigma eta_t
```

with fixed `sigma`, `gamma in (0, 1)` for this score coordinate, and parameter coordinate

```text
theta = [probit_gamma, log_beta]
gamma = Phi(probit_gamma)
beta = exp(log_beta)
```

At a predicted point `x_j`, the residual is

```text
r_j = z_t - 2 log_beta - x_j
```

and the exact log-chi-square observation log density is

```text
ell_j = 0.5 r_j - 0.5 exp(r_j) - 0.5 log(2 pi).
```

The derivative used by the implementation is

```text
d ell_j = 0.5 (1 - exp(r_j)) d r_j.
```

## Fixed SGQF Value Recursion

For fixed scalar SGQF nodes `xi_j` and weights `omega_j`, the predictive moments define deterministic quadrature points

```text
x_j = m_pred + sqrt(v_pred) xi_j.
```

The per-time normalizer is

```text
log Z_t = logsumexp_j(log omega_j + ell_j).
```

The normalized weights are

```text
a_j = exp(log omega_j + ell_j - log Z_t).
```

The filtered moments are

```text
m_filt = sum_j a_j x_j
s_filt = sum_j a_j x_j^2
v_filt = s_filt - m_filt^2.
```

The value route sums `log Z_t` over times and panel coordinates.

## Manual Forward Sensitivity

The implementation propagates first derivatives of `m`, `v`, predictive points, log normalizers, and filtered moments with respect to `[probit_gamma, log_beta]`.

At time 0:

```text
m = 0
v = sigma^2 / (1 - gamma^2)
d m = [0, 0]
d v / d probit_gamma = 2 sigma^2 gamma Phi'(probit_gamma) / (1 - gamma^2)^2
d v / d log_beta = 0
```

For `t > 0`:

```text
m_pred = gamma m
v_pred = gamma^2 v + sigma^2
d m_pred = d gamma * m + gamma * d m
d v_pred = 2 gamma d gamma * v + gamma^2 d v
```

where `d gamma / d probit_gamma = Phi'(probit_gamma)` and `d gamma / d log_beta = 0`.

The point derivatives are

```text
d x_j = d m_pred + 0.5 d v_pred / sqrt(v_pred) * xi_j.
```

The residual derivative is

```text
d r_j / d probit_gamma = -d x_j / d probit_gamma
d r_j / d log_beta = -2 - d x_j / d log_beta.
```

The normalizer derivative is

```text
d log Z_t = sum_j a_j d ell_j.
```

The normalized-weight sensitivity is represented by centering the derivative of the log terms:

```text
d a_j = a_j (d ell_j - d log Z_t).
```

The filtered moment derivatives are

```text
d m_filt = sum_j a_j (d x_j + (d ell_j - d log Z_t) x_j)
d s_filt = sum_j a_j (2 x_j d x_j + (d ell_j - d log Z_t) x_j^2)
d v_filt = d s_filt - 2 m_filt d m_filt.
```

These filtered moment sensitivities feed the next prediction step. The score vector is the sum of `d log Z_t` across times and panel coordinates, reshaped as `[probit_gamma_1, log_beta_1, ...]`.

## Implementation Mapping

| Derivation term | Implementation |
| --- | --- |
| `z_t = log(y_t^2)` | `exact_transformed_sv_observations(y)` |
| SGQF nodes/weights | `cloud.points`, `cloud.weights` |
| initial `m`, `v` | `current_mean`, `current_variance` |
| initial sensitivities | `current_d_mean`, `current_d_variance` |
| prediction sensitivities | `predicted_d_mean`, `predicted_d_variance` |
| points and point sensitivities | `predicted_points`, `d_predicted_points` |
| residual and log density | `residual`, `exact_log_chi_square_log_density(residual)` |
| `d ell` | `d_observation_log` |
| `d log Z_t` | `d_log_normalizer` |
| centered normalized-weight term | `centered_d_observation_log` |
| filtered moment sensitivities | `d_filtered_mean`, `d_filtered_variance` |
| emitted score | `score = tf.reshape(tf.stack(score_terms, axis=0), [-1])` |

## Checks And Evidence Boundaries

Implemented checks:

- route scan confirms the score function body contains no `GradientTape`, `.gradient(`, or `tape.watch`;
- focused unit test checks manual score against centered finite differences for dimensions 1, 2, and 3;
- leaderboard validator rejects fixed-SGQF score rows whose provenance contains tape/autodiff wording;
- regenerated leaderboard emits the actual-SV SGQF row as `executed_value_score` with finite score.

What this does not prove:

- it does not prove exact nonlinear likelihood correctness;
- it does not prove HMC posterior correctness;
- it does not prove GPU/XLA performance;
- it does not certify coupled high-dimensional Zhao-Cui TT source-faithfulness.
