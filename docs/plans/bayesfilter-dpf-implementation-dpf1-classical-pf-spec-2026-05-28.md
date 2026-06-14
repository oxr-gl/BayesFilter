# DPF1 Classical Bootstrap/SIR PF Specification

## Status

DPF1 execution artifact.  This specification defines the BayesFilter-owned
classical bootstrap/SIR particle-filter baseline required before differentiable
resampling, PF-PF, learned, or HMC-facing variants can be evaluated.

## Scope And Boundary

- Authority inputs: DPF0 obligations, `ch19_particle_filters.tex`, IE3
  linear-Gaussian recovery evidence, and the production checklist.
- Student and controlled-baseline reports are comparison context only.
- No production `bayesfilter/` code, vendored student code, monograph chapter,
  or high-dimensional lane artifact is edited or imported.

## Skeptical Plan Audit

| Check | Status | Notes |
| --- | --- | --- |
| Stale context | pass | DPF0 result records `DPF1 may start: yes` after Claude acceptance. |
| Wrong baseline | pass | Baseline is classical bootstrap/SIR PF with Kalman LGSSM reference, not student PF output. |
| Proxy overclaim | pass | Student/controlled RMSE, ESS, runtime, and same-regime rows remain explanatory only. |
| Missing stop conditions | pass | Ambiguous likelihood semantics or lack of independent reference blocks implementation promotion. |
| Hidden production/monograph drift | pass | DPF1 writes plan artifacts only. |
| Vendored-code contamination | pass | No student code is copied, executed, edited, or imported. |
| High-dimensional-lane contamination | pass | The separate high-dimensional nonlinear filtering lane is not used. |
| Artifact fitness | pass | This spec directly answers what classical baseline must exist before DPF components. |

## Required Algorithm Contract

| Field | Requirement |
| --- | --- |
| Model interface | Initial sampler/density, transition sampler/density, observation log-density, observation sequence, parameter object, and optional proposal object. |
| Default proposal | Bootstrap proposal `q_t(x_t|x_{t-1}, y_t) = p_theta(x_t|x_{t-1})`. |
| Weight update | For bootstrap PF, unnormalized log weight at time `t` is the observation log-density at the propagated particle. |
| Normalization | Normalize log weights with a stable log-sum-exp path; never normalize by raw exponentiation without finite checks. |
| Likelihood estimator | Record incremental average weight `Z_t^N` and product/sum-log normalizer as the PF likelihood estimator. |
| Log likelihood | Record `sum_t log Z_t^N` as the log of the estimator, not an unbiased estimator of log likelihood. |
| ESS | `1 / sum_i (w_i^2)` for normalized weights, with optional ratio `ESS/N`. |
| Resampling trigger | Configurable trigger, default `ESS/N < tau`, with `tau` recorded in artifacts. |
| Resampling methods | Start with multinomial/systematic/stratified only if their conditional-unbiasedness status and seed behavior are documented. |
| Randomness | Explicit RNG key/seed policy; every run artifact records seed list, particle count, horizon, dtype, and device. |
| Shapes | Particles have shape `(T or current, N, state_dim)` in artifacts or a documented streaming equivalent. |
| Dtype | Float dtype is explicit; mixed precision is disallowed in first-rung validation unless separately planned. |
| Failure handling | Non-finite log weights, zero total mass, invalid observations, or unsupported target/proposal support emit structured failure rows. |

## Output Artifact Schema

Every future classical PF result row should include:

| Field | Meaning |
| --- | --- |
| `model_id` | Fixture or model name. |
| `method_id` | `bootstrap_sir_pf` or later named proposal. |
| `seed` | RNG seed or deterministic marker. |
| `num_particles` | Particle count. |
| `horizon` | Number of observations. |
| `resampling_method` | Named method and trigger. |
| `dtype` | Numeric dtype. |
| `device` | CPU/GPU plus GPU hiding/trusted-status note. |
| `log_likelihood_estimate` | Log of PF likelihood estimator. |
| `likelihood_estimator_status` | Value-side estimator status and assumptions. |
| `mean_or_state_summary` | Reference-comparable summaries where available. |
| `ess_summary` | min/mean/final ESS and resampling count. |
| `finite_checks` | Value, weight, normalizer, and summary finiteness. |
| `reference_comparison` | Reference id, residuals, tolerances, and pass/fail. |
| `non_implications` | Explicit note that DPF/HMC/production validity is not concluded. |

## Required Non-Implications

- Classical bootstrap/SIR PF does not provide a pathwise differentiable
  likelihood map through resampling.
- Likelihood-estimator unbiasedness does not imply unbiased log likelihood or
  unbiased score.
- Passing LGSSM recovery does not validate nonlinear flow, relaxed resampling,
  HMC, or production behavior.
- Student agreement or same qualitative regime is not acceptance evidence.
