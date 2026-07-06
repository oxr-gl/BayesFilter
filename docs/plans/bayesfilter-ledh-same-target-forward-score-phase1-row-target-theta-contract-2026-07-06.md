# Phase 1 Contract: LEDH Row Target And Theta Freeze

Date: 2026-07-06

Status: `AMENDED_AFTER_HUMAN_DECISION`

## Purpose

This artifact freezes the row likelihood target, free parameter vector,
coordinate system, and score dimensionality for the LEDH same-target forward
scalar and score program.

No implementation phase may redefine these rows after seeing numerical results.

## Governing Rules

- The forward scalar for each row is the row observed-data log likelihood, or
  the finite-`N`, fixed-randomness LEDH estimator of that exact scalar.
- Proposal/flow observations may differ from the target observation density,
  but that does not change the target scalar.
- By explicit human amendment on 2026-07-06, the fixed SIR row
  `zhao_cui_spatial_sir_austria_j9_T20` is no longer treated as a
  no-free-theta score row for this LEDH score program. Its free theta is the
  reviewed BayesFilter log-scale model-parameter surface that reproduces the
  fixed source SIR base parameters at theta zero.
- The SIR log-scale surface is source-anchored in its fixed base formulas but
  remains `extension_or_invention` as an inference-theta parameterization. Do
  not call it author-source-faithful as a free-parameter inference model.
- Scoped or diagnostic rows must not be promoted into full observed-data rows.

## Frozen Row Contract Table

| Row | Frozen target scalar | Free theta / coordinate system | Score dimensionality | Notes |
| --- | --- | --- | ---: | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | exact-oracle LGSSM observed-data log likelihood for the admitted benchmark row | `physical_benchmark_exact_oracle`, theta = `(phi1, phi2, phi3, q_scale, r_scale)` | 5 | Reference same-target LEDH row already has compact no-tape score evidence. |
| `zhao_cui_sv_actual_nongaussian_T1000` | transformed actual-SV observed-data log likelihood with `z_t = log(y_t^2)` | `synthetic_unconstrained`, estimated parameters `(gamma, beta)`, fixed `sigma = 1.0` | 2 | Current same-target policy is transformed actual-SV only; raw Gaussian-closure routes are not same-target evidence. |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | KSC Gaussian-mixture surrogate observed-data log likelihood on the declared surrogate target | `synthetic_unconstrained`, estimated parameters `(gamma, beta)`, fixed `sigma = 1.0` | 2 | Same SV truth values as actual-SV, but this row remains a surrogate target, not the actual non-Gaussian target. |
| `zhao_cui_spatial_sir_austria_j9_T20` | spatial-SIR observed-data log likelihood using the source fixed-formula base model with free model-parameter log scales | `sir_log_scale_theta`, theta = `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)` with truth theta `[0,0,0]` | 3 | Human-amended fixed row: theta zero reproduces fixed source values `kappa_j=0.1`, `nu_j=18.0`, and observation sd `10`. Same-target observed-data value admission is still required before any score admission. |
| `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` | legacy/scoped diagnostic SIR component target only | `sir_log_scale_theta`, theta = `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)` | 3 | Historical diagnostic duplicate of the log-scale surface; it must not be used to bypass full observed-data fixed-row gates. |
| `zhao_cui_predator_prey_T20` | additive-Gaussian predator-prey observed-data log likelihood with source-paper T20 dataset | `physical`, theta = `(r, K, a, s, u, v)` | 6 | Use physical source-scope parameters; T25 tuned row remains outside this row identity. |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | source-scope generalized-SV observed-data log likelihood for the prior-mean synthetic row | `source_route_active_transformed_prior_mean`, active theta = `(gamma, tau, mu)` | 3 | Not actual-SV, not KSC, not native generalized-SV fixture, and not SP500 benchmark returns. |

## Explicit Nonclaims

- This contract does not admit any LEDH forward scalar yet.
- This contract does not admit any new score route yet.
- This contract does not admit the SIR same-target forward scalar or score.
- This contract does not resolve implementation correctness for current LEDH
  callbacks.
- This contract does not authorize leaderboard rebuild.
