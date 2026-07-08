# Phase 1 Result: Fixed-Variant Design And Classification Ledger

Date: 2026-07-05

Status: `PASSED_DESIGN_LEDGER_PENDING_PHASE2_REVIEW`

## Phase Objective

Design the first admissible `zhaocui_fixed` SSL-LSTM route as a deterministic,
fixed-branch, analytic-score adapter candidate, without claiming source-faithful
SSL-LSTM Zhao-Cui parity or writing adapter code.

## Entry Conditions

- Phase 0 passed through local Codex substitute review.
- The route is bounded as a clean-room fixed variant with source-anchored
  recentering/replay inspiration.
- LEDH remains out of scope.
- The existing Phase 4 blocker remains true until Phase 2 implements a real
  adapter.

## Source And Local-Code Re-Inspection

| Item | Anchor | Phase 1 use |
| --- | --- | --- |
| Author sequential loop | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-43` | Source anchor for replaying a fixed sequence of push/reapprox/sample/correction operations. |
| Author reapproximation | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:46-124` | Source anchor for fixed recentering, shifted target construction, fit-data split, transport fit, and log-normalizer update. |
| Author local target formula | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:132-135` | Source anchor for distinguishing prior/previous term, transition density, likelihood density, and nonfinite rejection. |
| Weighted affine recentering | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m:24-47` | Bounded source anchor for weighted mean/covariance/scale frame metadata. |
| SSL-LSTM protocol | `bayesfilter/nonlinear/ssl_lstm_protocol.py:30-84`, `:186-210` | Local contract for filter names, gradient paths, forbidden target authorities, required artifact fields, and `zhaocui_fixed` metadata. |
| SSL-LSTM parameter layout | `bayesfilter/nonlinear/ssl_lstm_protocol.py:91-171`, `bayesfilter/nonlinear/ssl_lstm_sgqf_ukf_adapters.py:123-286` | Local substrate for static shape, parameter slices, constrained transforms, and covariance derivative tensors. |
| SSL-LSTM hand derivatives | `bayesfilter/nonlinear/ssl_lstm_sgqf_ukf_adapters.py:505-729` | Local substrate for transition/observation means, state Jacobians, and direct parameter derivatives. |
| Existing adapter tests | `tests/test_ssl_lstm_sgqf_ukf_adapters.py:94-177`, `:180-260` | Test style for finite-difference subset checks, determinism checks, and schema admission. |

## Fixed-Variant Design

The first `zhaocui_fixed` implementation should be a deterministic replay
adapter over the existing Gaussian additive SSL-LSTM target. It is a clean-room
fixed-HMC approximation, not a source-faithful reproduction of the Zhao-Cui
paper route.

The target path should evaluate a fixed approximation to the SSL-LSTM filtering
log likelihood and analytic score with these components:

1. SSL-LSTM parameter unpacking uses the existing `SSLLSTMStaticConfig` and
   `unpack_ssl_lstm_parameters` layout.
2. State transition and observation means use the existing hand-coded
   TensorFlow functions and derivative tensors.
3. A manifest fixes all branch choices before target evaluation:
   reference noise, reference state sample count, resampling quantiles if used,
   affine recentering policy, support/ridge constants, horizon, dimensions,
   and finite-difference test indices.
4. The value path propagates deterministic reference samples through the
   SSL-LSTM transition mean plus fixed process-noise draws, evaluates Gaussian
   observation densities, and accumulates a log-mean-exp style filtering
   likelihood with deterministic stabilizers.
5. The score path uses manual chain rule through the existing SSL-LSTM
   derivative functions and analytic Gaussian log-density derivatives.
6. `computeL`-style weighted recentering may be computed and recorded as
   branch metadata. For Phase 2, it should not be required as a differentiable
   transformation inside the score path unless Phase 2 explicitly derives the
   derivative of the frame and passes finite-difference checks.

## Route-Classification Ledger

| Design choice | Classification | Required Phase 2 handling |
| --- | --- | --- |
| Fixed reference-noise replay before target evaluation | `fixed_hmc_adaptation` | Store stateless seeds or literal fixed tensors in a manifest; repeated evaluation must be bitwise or tolerance deterministic. |
| Weighted affine recentering diagnostic modeled on `computeL` | `fixed_hmc_adaptation` | Compute weighted mean/covariance/scale with fixed weights; record frame metadata; do not claim full TTSIRT parity. |
| Deterministic resampling quantiles, if used | `fixed_hmc_adaptation` | Quantiles must be fixed in manifest; no random draw or adaptive resampling inside target evaluation. |
| SSL-LSTM transition, observation, parameter derivatives | local SSL-LSTM implementation substrate | Reuse existing hand-coded derivative functions; cite as local BayesFilter code, not Zhao-Cui source. |
| Deterministic particle/proposal log-mean-exp likelihood | `extension_or_invention` | It is the first clean-room `zhaocui_fixed` route; validate as HMC-compatible approximation only. |
| TTSIRT/TTIRT, KR maps, marginalization parity | not implemented in this design | Phase 2 must not claim these; later source-route work would need a separate plan. |
| SGQF/UKF comparator status | comparator only | Phase 2 may reuse testing style, not promote comparator success into Zhao-Cui success. |
| LEDH/manual VJP streaming OT | out of scope | No Phase 2 file should implement or test LEDH. |

## Analytic Gradient Obligations

Phase 2 must implement the `zhaocui_fixed` score without `GradientTape`,
`tf.py_function`, NumPy implementation logic, or finite-difference target
gradients.

Required analytic derivatives:

- direct parameter derivatives for SSL-LSTM transition mean from
  `ssl_lstm_transition_parameter_derivative`;
- transition state Jacobians from `ssl_lstm_transition_state_jacobian`;
- observation mean parameter derivatives from
  `ssl_lstm_observation_parameter_derivative`;
- observation state Jacobians from `ssl_lstm_observation_state_jacobian`;
- covariance derivatives already produced by `unpack_ssl_lstm_parameters`;
- Gaussian log-density derivatives for observation and process-noise terms;
- log-mean-exp weight derivatives using normalized deterministic weights.

Finite differences are required as tests only.

## Manifest And Artifact Contract

Phase 2 should introduce a narrow manifest, most likely in a new module
`bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py`, with fields including:

- `source_route_classification`;
- `source_anchor_summary`;
- `reference_seed_policy`;
- `reference_noise_shape`;
- `reference_sample_count`;
- `resampling_policy`;
- `recenter_policy`;
- `score_path`;
- `forbidden_authorities`;
- `nonclaims`.

The value/score artifact must validate against
`SSL_LSTM_VALUE_SCORE_SCHEMA_VERSION` and record:

- `filter_name = zhaocui_fixed`;
- `gradient_path = analytic_first_order_zhaocui_fixed`;
- `value_score_authority` that is not any forbidden target authority;
- `seed_policy = stateless_required` or an explicitly fixed literal tensor
  policy;
- `branch_or_randomness_policy = fixed_hmc_adaptation_manifest`;
- nonclaims denying source-faithful parity, HMC convergence, posterior
  correctness, method superiority, and default readiness.

## Testing Plan For Phase 2/3

Phase 2 must add or prepare focused tests for:

- repeated evaluation determinism;
- finite scalar log likelihood and finite score vector;
- protocol metadata validation for `zhaocui_fixed`;
- branch/manifest stability under repeated construction;
- finite-difference subset agreement for representative LSTM gate, latent map,
  observation map, initial law, process-noise, and observation-noise parameters;
- forbidden target-path scan for `GradientTape`, `tf.py_function`, `np.`, and
  `numpy` in the target adapter module;
- negative test that the adapter does not claim source-faithful parity.

## Skeptical Plan Audit

| Risk | Phase 1 finding |
| --- | --- |
| Wrong baseline | Passed: baseline remains SGQF/UKF comparators plus Zhao-Cui source anchors, not SGQF/UKF proof. |
| Proxy metrics promoted | Passed: finite differences and smoke metrics are adapter-admission checks only. |
| Missing stop conditions | Passed: Phase 2 blocks on autodiff, randomness, nonfinite score, schema invalidity, or unclassified route choices. |
| Unfair comparison | Passed: no ranking or sufficiency claim is made. |
| Hidden assumptions | Recorded: deterministic particle/proposal approximation is `extension_or_invention`, not source-faithful route parity. |
| Stale context | Required source and local code surfaces were reopened during Phase 1. |
| Environment mismatch | No runtime/GPU evidence is used. |
| Artifact mismatch | Phase 1 writes a design ledger and Phase 2 subplan only, as required. |

## Required Checks Run

| Check | Result |
| --- | --- |
| Source anchor re-open | Passed: `full_sol.m` and `computeL.m` anchors inspected. |
| Local protocol/scaffold re-open | Passed: `ssl_lstm_protocol.py` and `ssl_lstm_sgqf_ukf_adapters.py` inspected. |
| Implementation boundary | Passed: no adapter code written in Phase 1. |
| Phase 2 subplan | Written as `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase2-zhaocui-fixed-adapter-implementation-subplan-2026-07-05.md`. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Phase 1 design gate | Passed locally pending Phase 2 subplan review | No design veto fired | Whether the deterministic clean-room approximation will pass finite/FD/schema tests when implemented | Review Phase 2 subplan, then implement the narrow adapter | No implementation success, HMC readiness, source-faithful SSL-LSTM parity, posterior correctness, or method ranking |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | No design hard veto found. |
| Statistically supported ranking | Not applicable. |
| Descriptive-only differences | Design choices and comparator roles are planning evidence only. |
| Default-readiness | Not checked and not claimed. |
| Next evidence needed | Phase 2 implementation with deterministic, finite, schema-valid analytic score tests. |

## Next-Phase Handoff

Phase 2 may start only after the Phase 2 implementation subplan is reviewed for
consistency, feasibility, artifact coverage, and boundary safety. Phase 2 must
not implement a broad TTSIRT/KR source route, public API, LEDH path, or any
target-gradient autodiff fallback.
