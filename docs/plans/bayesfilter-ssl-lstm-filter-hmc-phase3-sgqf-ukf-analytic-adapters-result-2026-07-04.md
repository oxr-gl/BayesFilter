# Phase 3 Result: Fixed SGQF And SVD-UKF Analytic Adapters

Date: 2026-07-04

Status: `LOCAL_CHECKS_PASSED_PENDING_REVIEW_DECISION`

## Phase Objective

Build or wire fixed SGQF and SVD-UKF analytic-gradient adapters for the
Gaussian additive SSL-LSTM target under the shared Phase 2 value/score protocol.

## Entry Conditions

- Phase 1 defined the Gaussian additive SSL-LSTM target with augmented state
  `[z, a, c]`.
- Phase 2 defined the fail-closed value/score protocol and artifact schema.
- Phase 2 was closed locally under user-directed no-export continuation.
- No Particle Gibbs, conditional SMC, Gibbs, or automatic-differentiation target
  gradient route is admitted.

## Implementation Summary

Added `bayesfilter/nonlinear/ssl_lstm_sgqf_ukf_adapters.py`.

The module implements a narrow adapter layer only. It does not export a public
API, does not run HMC, and does not claim SGQF/UKF sufficiency.

Implemented pieces:

- deterministic unpacking of the Phase 1 diagonal-covariance SSL-LSTM parameter
  vector;
- hand-coded SSL-LSTM transition, observation, state Jacobians, and parameter
  derivatives;
- Fixed-SGQF components using the full augmented state and the existing
  `tf_fixed_sgqf_score` analytic score path;
- SVD-UKF structural components with stochastic `z` and deterministic `[a, c]`,
  using the existing `tf_svd_ukf_score` analytic score path;
- Phase 2 protocol bindings for `fixed_sgqf` and `svd_ukf`;
- debug/reference artifact builder for the Phase 2 value/score schema.

Added `tests/test_ssl_lstm_sgqf_ukf_adapters.py`.

## Diagnostic Artifacts

The tiny deterministic value/score artifacts are debug/reference artifacts, not
production GPU/XLA evidence.

| Filter | Artifact | Role | FD max abs error |
| --- | --- | --- | --- |
| `fixed_sgqf` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase3-fixed-sgqf-debug-value-score-artifact-2026-07-04.json` | `debug_reference` | `6.08466610430014e-11` |
| `svd_ukf` | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase3-svd-ukf-debug-value-score-artifact-2026-07-04.json` | `debug_reference` | `6.731148971539369e-11` |

The finite-difference checks cover selected LSTM gate, latent map, observation
map, initial law, and process-noise parameters. They are adapter-admission
diagnostics only.

## Required Checks Run

All runtime checks below were CPU-hidden debug/protocol checks. They are not
production GPU evidence.

| Check | Command | Result |
| --- | --- | --- |
| Focused Phase 3 adapter tests | `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ssl_lstm_sgqf_ukf_adapters.py` | Passed: 6 tests |
| Compile check | `python -m compileall -q bayesfilter/nonlinear/ssl_lstm_protocol.py bayesfilter/nonlinear/ssl_lstm_sgqf_ukf_adapters.py tests/test_ssl_lstm_protocol.py tests/test_ssl_lstm_sgqf_ukf_adapters.py` | Passed |
| Forbidden target-path scan | `rg -n "GradientTape|gradient_tape|tf\\.py_function|numpy|np\\." bayesfilter/nonlinear/ssl_lstm_sgqf_ukf_adapters.py` | Passed: no hits |
| Diff whitespace hygiene | `git diff --check -- <Phase 2/3 code, tests, and governance docs>` | Passed |
| Phase 2 protocol plus Phase 3 adapters | `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ssl_lstm_protocol.py tests/test_ssl_lstm_sgqf_ukf_adapters.py` | Passed: 17 tests |
| Existing SGQF and sigma-point score suites | `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_scores_tf.py tests/test_nonlinear_sigma_point_scores_tf.py` | Passed: 23 tests |
| Debug value/score artifact generation | `CUDA_VISIBLE_DEVICES=-1 python - <<'PY' ...` | Passed; wrote both JSON artifacts and validated schema |

The XLA smoke in `tests/test_ssl_lstm_sgqf_ukf_adapters.py` compiles the
hand-coded transition/Jacobian/parameter-derivative block with
`tf.function(jit_compile=True)`. This is a core derivative smoke, not a full
filter target XLA artifact.

## Skeptical Plan Audit

| Risk | Phase 3 finding |
| --- | --- |
| Wrong baseline | Both adapters use the same Phase 1 `[z, a, c]` SSL-LSTM fixture and Phase 2 protocol. |
| Proxy metrics promoted | Finite-difference residuals are adapter-admission diagnostics only, not estimation or sufficiency evidence. |
| Missing stop conditions | The result remains pending material review decision before Phase 4 execution. |
| Unfair comparison | No SGQF/UKF ranking is made; both are only admitted to later shared benchmark work. |
| Hidden assumptions | Diagonal covariance, tiny static fixture, and hand-coded first-order derivatives are explicit. |
| Stale context | Phase 1 model, Phase 2 protocol, and existing analytic SGQF/UKF score modules were reread before implementation. |
| Environment mismatch | CPU-hidden checks and debug JSON artifacts are labeled as debug/reference only. |
| Artifact mismatch | Phase 3 wrote its own result artifact and two Phase 2-schema debug value/score JSON artifacts. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Phase 3 local adapter gate | Passed locally | No local finite, determinism, derivative, protocol, or forbidden-target-path veto fired | Material external review remains unresolved after earlier Claude export denial | Ask user for Phase 3 review decision before Phase 4 execution | No SGQF/UKF sufficiency, no HMC convergence, no exact SSL likelihood, no method ranking, no production/default readiness |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Local adapter hard-veto checks passed for tiny deterministic fixtures |
| Statistically supported ranking | Not applicable; no stochastic method comparison was run |
| Descriptive-only differences | FD residual magnitudes are descriptive adapter diagnostics after passing tolerances |
| Default-readiness | Not checked and not claimed |
| Next evidence needed | Material review decision, then Phase 4 Zhao-Cui fixed adapter source-anchor precheck |

## Phase 4 Subplan Review

Phase 4 remains feasible only under the Zhao-Cui source-anchor gate. Its
subplan has been refreshed to state that Phase 3 local checks passed but Phase 3
material review remains unresolved. Phase 4 must not implement source-route
behavior before inspecting and citing both Zhao-Cui paper/math anchors and local
author source file/line anchors.

## Review Boundary

No Claude review was attempted in Phase 3. Earlier Claude export was rejected
because it would send repo-local planning/workspace context to an external
Claude service. The user has not yet granted a Phase 3-specific external export
approval or Codex-only material review exception.

## Phase 3 Gate Status

`LOCAL_CHECKS_PASSED_PENDING_REVIEW_DECISION`

Phase 4 execution must not start until the user either:

- authorizes a Phase 3 Codex-only review exception;
- explicitly approves exporting a bounded Phase 3 review bundle to Claude; or
- changes the material review requirement.
