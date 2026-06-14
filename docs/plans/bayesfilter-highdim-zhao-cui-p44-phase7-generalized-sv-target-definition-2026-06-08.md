# P44-M7 Generalized SV Target Definition

metadata_date: 2026-06-08
phase: P44-M7
run_id: `p44-codex-supervised-20260608-013203`
Status: `PASS_P44_M7_CODE_GOVERNANCE`

## Target-Definition Table

| Field | Decision |
| --- | --- |
| `state_law_s` | `s_t = phi_s s_{t-1} + sigma_s eta_{s,t}`, Gaussian innovation, stationary Gaussian initial law. P44 diagnostic fixture fixes `phi_s=0.55`, `sigma_s=0.30`; no estimated `s` parameters in this phase. |
| `state_law_h` | `h_t = phi_h h_{t-1} + sigma_h eta_{h,t}`, Gaussian innovation, stationary Gaussian initial law. P44 diagnostic fixture fixes `phi_h=0.65`, `sigma_h=0.45`; no estimated `h` parameters in this phase. |
| `state_dependence` | `s_t` and `h_t` are independent a priori in the diagnostic fixture; the native observation law couples them through `y_t | s_t,h_t`. |
| `observation_law` | Native generalized SV: `y_t | s_t,h_t,beta ~ N(beta s_t, exp(h_t))`. This native density is not made additive-Gaussian by `log(y_t^2)` because the residual `y_t - beta s_t` depends on the latent state `s_t`. |
| `target_route` | `diagnostic-only` for P44-M7. Existing code supports transformed-residual and moment-matched diagnostics, plus exact/KSC transformed routes for simple SV. P44-M7 does not approve a native generalized-SV same-target CUT4/Zhao--Cui equality route. |
| `parameterization` | Diagnostic fixture uses scalar `theta = log(beta)` only for the finite gradient check, with `beta=exp(theta)`. State-law parameters are fixed as above. |
| `jacobian_terms` | Native route: none because raw `y_t` density would be evaluated directly. Transformed-residual route: blocked as exact likelihood because `r_t=y_t-beta s_t` is state-dependent; any exact transformed route would need conditional transform accounting and a reviewed reference. P44-M7 diagnostic uses no exact transform claim. |
| `reference_route` | `blocked` for native same-target equality. Tiny finite diagnostics may use CUT4 transformed-residual and moment-matched approximations only as non-exact checks. Any native dense, SMC, mixture, or long-horizon route requires a separate reviewed experiment plan. |
| `claim_class` | `P42 Class D diagnostic only`. Possible Class B/A route is deferred until a shared target and reference are separately reviewed. |

## Decision

Generalized SV remains diagnostic-only in P44-M7. The phase may run tiny
finite checks that ensure existing diagnostic code is not broken, but it must
not run or claim a CUT4-versus-Zhao--Cui same-target equality test.

## Required Nonclaims

- transformed residual is not the exact native generalized-SV likelihood;
- Gaussian mixture approximation is not exact native likelihood;
- moment-matched Kalman is diagnostic only;
- independent prior states become coupled in the native observation density;
- no same-target CUT4/Zhao--Cui equality is approved in P44-M7;
- no HMC readiness, paper-scale CNS reproduction, or production score API
  readiness is claimed.
