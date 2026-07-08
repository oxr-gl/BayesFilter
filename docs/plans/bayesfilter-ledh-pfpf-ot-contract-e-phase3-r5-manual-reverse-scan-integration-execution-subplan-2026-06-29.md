# Phase R5 Subplan: Local Manual Reverse-Scan Integration

Date: 2026-06-29

Status: `CLAUDE_REVIEW_AGREED_EXECUTING`

## Phase Objective

Wire the R4 fixed-ridge Cholesky reset VJP into a local one-step manual
reverse-scan composition that includes:

- log-weight normalization and likelihood increment;
- fixed-branch floored normalized log weights;
- finite dense stopped-scale/key Sinkhorn transport matrix VJP;
- Cholesky-ridge Contract E reset VJP; and
- propagation of cotangents back to post-flow particles, corrected log
  weights, and residual reset noise.

R5 is a local integration gate only.  It must not remove or weaken the Phase 3
material blocker.

## Entry Conditions Inherited From R4

- R4 local fixed-ridge Cholesky reset VJP passed same-scalar central finite
  differences for `post_flow`, softmax-chart weights, `matrix`, and
  `residual_noise`.
- R4 fixed-chart tests asserted identical center/`+h`/`-h` realized ridge and
  ridge-attempt counts.
- Static reset-helper tests block hidden generic autodiff and eigensystem use
  in the Cholesky-ridge reset helper family.
- The material blocker remains active:
  `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`.

## Required Artifacts

- This executable R5 subplan.
- A local integration fixture, preferably in a focused test file, that defines:
  - the forward one-step scalar;
  - the manual composed VJP for the same scalar; and
  - central finite-difference checks on the same scalar.
- Static route audit covering the local R5 integration helpers and the Phase 3
  material blocker.
- Static transport-helper audit covering the full transitive manual dense
  finite stopped-scale/key transport-matrix helper family, including at least
  `_filterflow_manual_dense_finite_transport_matrix_vjp_stopped_scale_keys`,
  `_filterflow_manual_dense_finite_transport_matrix_value_stopped_scale_keys`,
  `_filterflow_manual_dense_finite_transport_matrix_stopped_scale_keys`,
  `_filterflow_manual_dense_finite_sinkhorn_outputs`,
  `_filterflow_manual_dense_finite_sinkhorn_vjp`,
  `_filterflow_manual_dense_finite_softmin_vjp`,
  `_filterflow_manual_transport_from_potentials_vjp`,
  `_filterflow_manual_same_particles_cost_vjp`,
  `_filterflow_exact_transport_from_potentials`,
  `_filterflow_exact_softmin`, and
  `_filterflow_exact_cost`.
- R5 result note that records the exact local scalar configuration:
  `epsilon`, replayed center, replayed scale, replayed transport key,
  replayed `epsilon0`, `scaling`, `steps`, floor value, fixed ridge, and
  center/`+h`/`-h` replay diagnostics for ridge and transport-side fixed-chart
  invariants.
- R5 result note that records the frozen upstream cotangents `U` and `u_inc`,
  finite-difference step size, parity tolerances, fixture dimensions, fixture
  seed or exact fixture source, and center/`+h`/`-h` floor-mask replay status.
- R5 result / close record.
- R6 handoff subplan only if the R5 local integration gate passes.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before implementation.
- Bounded Claude read-only review of this subplan before execution, looping up
  to five rounds for material issues.
- Focused CPU-hidden pytest for the R5 integration fixture and existing reset
  audit tests.
- Static audit that R5 local integration helpers do not use generic autodiff,
  `ForwardAccumulator`, `tf.gradients`, `tf.linalg.eigh`, or
  `transport_ad_mode="full"`.
- `py_compile` for touched Python modules.
- `git diff --check` on touched paths.
- Bounded Claude implementation/result review before advancing.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can the fixed-ridge reset VJP be composed with the existing manual finite dense transport matrix VJP and log-normalization VJP in a local one-step reverse-scan fixture without hidden autodiff? |
| Baseline/comparator | Central finite differences of the exact same local scalar used by the composed manual VJP. |
| Primary pass criterion | Manual VJP dot direction matches central finite difference for post-flow particles, corrected log weights, and residual reset noise within frozen tolerances. |
| Veto diagnostics | Nonfinite scalar or cotangents, ridge branch change in center/`+h`/`-h` branchy replay, floor-mask change in center/`+h`/`-h` replay, hidden autodiff token in local integration helpers, `tf.linalg.eigh` in the local fixed-ridge helper path, `transport_ad_mode="full"`, missing material blocker, or weakened forbidden-action text. |
| Explanatory diagnostics | Reset cotangent norms, transport cotangent norms, log-normalization cotangent norms, row/column transport residuals, realized ridge, and ridge-attempt count. |
| Not concluded | Full LGSSM gradient correctness, Kalman agreement, SIR/SV correctness, HMC readiness, production readiness, GPU/XLA readiness, or correctness across ridge branch changes. |
| Artifact preserving result | R5 result note and the focused R5 test output. |

## Forbidden Claims And Actions

- Do not remove or weaken the material blocker during R5.
- Do not run material Phase 3, full LGSSM finite differences, SIR, SV, GPU, or
  XLA jobs during R5.
- Do not claim full filter gradient correctness from the one-step local
  fixture.
- Do not differentiate through ridge branch selection.
- Do not use TensorFlow `GradientTape`, `.gradient`, `.jacobian`,
  `ForwardAccumulator`, `tf.gradients`, or `tf.compat.v1.gradients` as the
  material implementation.
- Do not use `transport_ad_mode="full"` or equivalent full transport autodiff.

## Implementation Design

The local fixture will define a matrix-based same-route scalar.  For a fixed
batch fixture, let

```text
increment_b = logsumexp_j(corrected_log_weights_{b,j}),
weights_{b,j} = exp(corrected_log_weights_{b,j} - increment_b),
transport_logw_{b,j} = log(max(weights_{b,j}, floor)).
```

No renormalization is applied after flooring; this intentionally matches the
existing fixed-branch route under test.  The fixed floor chart is the active
mask

```text
floor_active_{b,j} = [weights_{b,j} > floor].
```

For every central finite-difference comparison, center/`+h`/`-h` replay must
preserve exactly the same `floor_active` mask.  Any floor-mask change is a
veto and stop condition.  Because finite differences do not understand
`stop_gradient`, the fixed-chart finite-difference comparator records the base
transport chart and replays it:

```text
center^0_b = mean_j post_flow^0_{b,j},
scale^0_b = filterflow_scale(post_flow^0)_b,
x^0_{b,j} = (post_flow^0_{b,j} - center^0_b) / scale^0_b,
key^0 = x^0,
epsilon0^0_b = filterflow_epsilon_start(x^0)_b,
x_{b,j} = (post_flow_{b,j} - center^0_b) / scale^0_b.
```

With frozen `epsilon`, replayed `epsilon0^0`, `scaling`, and integer `steps`,
define the dense finite stopped-scale/key transport matrix

```text
M = T_matrix(x, key^0, transport_logw; epsilon, epsilon0^0, scaling, steps),
```

where `T_matrix` is the value route paired with
`_filterflow_manual_dense_finite_transport_matrix_vjp_stopped_scale_keys`.
The Sinkhorn potential costs use the replayed key `key^0`, matching the
stopped-key derivative.  The final transport-from-potentials matrix keeps the
same center value and the same local derivative as the existing paired manual
VJP helper at the base point.
The one-step scalar is then

```text
S(post_flow, corrected_log_weights, residual_noise)
  = <Reset_fixed_ridge(post_flow, weights, M, residual_noise; ridge), U>
    + <increment, u_inc>.
```

- `Reset_fixed_ridge` is the R4 fixed-ridge Cholesky reset route.
- `<.,.>` denotes the scalar contraction with frozen upstream cotangents.
- The manual VJP target is the derivative of this exact map, not a nearby
  surrogate.

The manual reverse composition will:

1. call `contract_e_cholesky_ridge_reset_fixed_ridge_vjp`;
2. send the returned matrix cotangent through
   `_filterflow_manual_dense_finite_transport_matrix_vjp_stopped_scale_keys`;
3. propagate scaled-particle cotangents through the replayed
   stopped-center/stopped-scale chart, so `d post_flow = d x / scale^0`;
4. combine direct reset weight cotangents, floored-log-weight cotangents, and
   likelihood-increment cotangents through the log-normalization VJP; and
5. compare the resulting cotangents with central finite differences of `S`.

## Skeptical Plan Audit

- Wrong baseline risk: avoided by comparing against the exact same scalar, not
  against Kalman, a full-filter proxy, or a different reset route.
- Proxy promotion risk: the one-step fixture is not a material Phase 3 pass
  criterion and cannot unblock material mode.
- Missing stop conditions: branch changes, hidden autodiff, nonfinite values,
  and parity failure all stop R5.
- Unfair comparison risk: finite differences and manual VJP share fixed
  residual noise, fixed ridge, fixed Sinkhorn hyperparameters, and fixed
  upstream cotangents.  The R5 result must record those values and the
  center/`+h`/`-h` branch replay diagnostics, including the floor mask.
- Environment mismatch risk: checks are CPU-hidden local tests only; no GPU,
  XLA, or production-target claim is made.
- Artifact relevance risk: the test explicitly composes normalization,
  transport matrix VJP, and reset VJP, which are the R5 boundaries under test.

Audit decision: proceed to Claude review before implementation.

## Claude Plan Review

- Round 1: `VERDICT: REVISE`.  The scalar had to be made explicitly
  matrix-based and the normalization/floor map had to be fully specified.
- Round 2: `VERDICT: REVISE`.  Floor-mask replay, transitive transport-helper
  audit, and result reproducibility fields were required.
- Round 3: `VERDICT: AGREE`.
- Round 4 delta review: `VERDICT: AGREE` for replaying base center, scale, and
  `epsilon0` in finite-difference parity.
- Round 5 stopped-key delta review: `VERDICT: AGREE` for replaying `key^0` in
  the Sinkhorn-potential costs while keeping the final transport-from-potentials
  local derivative matched to the paired manual VJP.

## Exact Next-Phase Handoff Conditions

Advance to R6 only if:

- the R5 one-step integrated manual VJP matches same-scalar finite differences;
- static hidden-autodiff/full-transport/eigh audit passes for the R5 helpers;
- ridge branch replay is stable for parity probes;
- floor-mask replay is stable for parity probes;
- focused local checks pass;
- R5 result is written;
- bounded Claude implementation/result review converges; and
- the Phase 3 material blocker remains active unless R6 is explicitly reviewed
  to replace it with a narrower material gate.

## Stop Conditions

Stop and write an R5 blocker result if:

- Claude plan review does not converge after five rounds for the same blocker;
- local integrated parity fails after one focused repair attempt;
- ridge branch changes appear on parity probes;
- floor-mask changes appear on parity probes;
- the local route requires generic autodiff or full transport autodiff to pass;
- static audit detects hidden `eigh` use in the fixed-ridge R5 path; or
- any required artifact cannot be produced without crossing the forbidden
  action boundary.
