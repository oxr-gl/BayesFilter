# LEDH-PFPF-OT Autodiff-Free Adjoint Derivation Contract

date: 2026-06-23
phase: P3-DERIVATION-CONTRACT
status: P3_CONTRACT_DRAFT_FOR_REVIEW

## Purpose

This contract defines the manual adjoint obligations for the production
LEDH-PFPF-OT SIR gradient route.  Its job is to replace the current outer
`tf.GradientTape` gradient route and the current transport custom-gradient
`grad` body tape with explicit adjoint interfaces.

This is a derivation and implementation-boundary contract only.  It does not
implement the route, certify an implementation, run GPU, run finite
differences, produce an actual-gradient artifact, or make an HMC or scientific
validity claim.

## Inherited Gates

- P0 freezes the no-production-autodiff invariant.
- P1 pins the current leaking route and leak IDs.
- P2 audit tooling exists and intentionally returns `FAIL_CURRENT_ROUTE` for
  the current route.
- Production autodiff remains forbidden for the selected gradient route:
  `tf.GradientTape`, `tf.autodiff.ForwardAccumulator`, tape `.gradient`,
  tape `.jacobian`, `tf.gradients`, and custom-gradient `grad` bodies that open
  autodiff.
- Diagnostic autodiff is allowed only under exact whitelist and never as a
  production promotion criterion.
- `transport_ad_mode=full` is forbidden.
- FD remains forbidden until a later audited N10000 actual-gradient artifact
  exists.

## Source And Code Anchors

Mathematical anchors:

- `docs/chapters/ch32c2_ledh_pfpf_ot_custom_gradient.tex:140`,
  `prop:bf-ledh-ot-barycentric-vjp`.
- `docs/chapters/ch32c2_ledh_pfpf_ot_custom_gradient.tex:218`,
  `prop:bf-ledh-ot-normalized-transport-vjp`.
- `docs/chapters/ch32c2_ledh_pfpf_ot_custom_gradient.tex:310`,
  `prop:bf-ledh-ot-cost-vjp`.
- `docs/chapters/ch32c2_ledh_pfpf_ot_custom_gradient.tex:364`,
  `prop:bf-ledh-ot-softmin-vjp`.
- `docs/chapters/ch32c2_ledh_pfpf_ot_custom_gradient.tex:438`,
  `prop:bf-ledh-ot-finite-sinkhorn-vjp`.
- `docs/chapters/ch32c2_ledh_pfpf_ot_custom_gradient.tex:514`,
  `prop:bf-ledh-ot-filtering-loop-vjp`.

Current route anchors:

- Outer leaking objective gradient:
  `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:477`
  and `:485`.
- Objective/value wrapper:
  `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:535`.
- Streaming value recursion:
  `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py:256`.
- LEDH flow call:
  `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py:371`.
- Log-weight correction/normalization:
  `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py:407`
  and `:414`.
- Transport call:
  `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py:440`.
- Current blocked transport tape:
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:1988`
  and `:2003`.
- Candidate blockwise manual transport boundary:
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:2034`
  through `:2113`.

## Objective And Seed Aggregation

The production scalar is the same finite value currently returned by the
reviewed route:

```text
objective(theta) = seed_mean_s log_likelihood_s(theta)
```

For grouped seed contexts, the objective is the exact seed-weighted mean of
each fixed-seed value.  The manual gradient route must seed the reverse pass
with the same seed weights that `_objective_from_contexts` applies.  Replacing
P1-L001/P1-L003 requires a production function with this shape:

```text
manual_ledh_pfpf_ot_value_and_score(theta, route_manifest)
  -> objective, per_seed_log_likelihood, score_theta
```

The `score_theta` output must be produced by the manual reverse scan in this
contract, not by an outer TensorFlow tape, forward accumulator, or hidden
callback autodiff.

## Forward Step Contract

At each time step `t`, the executed forward map is:

```text
pre_flow_t = pre_flow_step(current_particles_t, t)

flow_t = ledh_flow(
    pre_flow_t,
    current_particles_t,
    observation_t,
    transition/observation callbacks and covariances,
)

post_flow_t = flow_t.post_flow_particles

corrected_logw_t =
    current_logw_t
    + transition_log_density(post_flow_t, current_particles_t, t)
    + observation_log_density(post_flow_t, observation_t, t)
    - flow_t.pre_flow_log_density
    + flow_t.forward_log_det

weights_t, incremental_t = normalize_log_weights(corrected_logw_t)
normalized_logw_t = log(max(weights_t, log_weight_floor))

if resampling mask is active:
    next_particles_t, next_logw_t =
        transport(post_flow_t, normalized_logw_t, mask_t)
else:
    next_particles_t, next_logw_t = post_flow_t, normalized_logw_t

log_likelihood += incremental_t
```

The branch decisions, fixed random streams, fixed resampling masks, fixed
iteration budgets, chunk sizes, dtype/TF32 policy, and stopped-gradient policy
are part of the route manifest.  The backward pass must use the same route
identity.

## Forward Checkpoint Inventory

The primal route must retain or be able to replay, for each time step:

- `current_particles_t` and `current_logw_t`;
- `pre_flow_t`, or the fixed random stream and analytical transition map needed
  to replay it exactly;
- LEDH flow auxiliary data sufficient for a manual VJP of `post_flow_t`,
  `pre_flow_log_density_t`, and `forward_log_det_t`;
- transition and observation log-density inputs and model-callback auxiliary
  data needed for manual log-density VJPs;
- `corrected_logw_t`, normalized weights, and the fixed branch mask for
  `log(max(weights, floor))`;
- transport mask and transport auxiliary record, including finite Sinkhorn
  settings, stopped scale/key policy, chunk sizes, final potentials, and
  retained vector states needed for reverse replay;
- no full `[B,N,N]` cost, probability, or transport tensor retained in the
  large-N streaming production route.

If an implementation cannot either retain or replay one of these items without
autodiff, the corresponding phase must stop with a blocker.

## Reverse-Time Scan

The manual score is a reverse scan over time.  Let `bar_x_next` and
`bar_logw_next` be cotangents entering a time step from the future, and let
`bar_ll` be the cotangent of the accumulated log likelihood for that seed.

For each time step in reverse order:

1. Apply the fixed transport or skip branch VJP to map cotangents of
   `next_particles_t` and `next_logw_t` into cotangents of `post_flow_t` and
   `normalized_logw_t`.
2. Apply the `log(max(weights, floor))` fixed-branch VJP.  If floor activity is
   possible, the active floor mask must be recorded and the derivative is zero
   on floored entries.  If the floor mask is not stable or not recorded, stop
   rather than using autodiff.
3. Apply the log-normalization VJP:

```text
weights = softmax(corrected_logw)
incremental = logsumexp(corrected_logw)
normalized = corrected_logw - incremental

bar_corrected =
    bar_incremental * weights
    + bar_normalized
    - weights * sum_i bar_normalized_i
```

4. Distribute `bar_corrected` through the correction identity:

```text
bar_current_logw += bar_corrected
bar_transition_log_density += bar_corrected
bar_observation_log_density += bar_corrected
bar_pre_flow_log_density -= bar_corrected
bar_forward_log_det += bar_corrected
```

5. Apply manual VJPs for transition log density, observation log density, LEDH
   flow, and `pre_flow_step`.
6. Accumulate `score_theta` from every parameter-dependent primitive.
7. Pass cotangents to `current_particles_t` and `current_logw_t` to the next
   earlier time step.

The reverse scan is the replacement for the outer objective tape.  A phase may
use small diagnostic autodiff tests only outside the production route and under
the P2 whitelist.

## Outer Objective Adjoint Obligation

Replaces P1-L001/P1-L003.

Required production interface:

```text
manual_objective_score(
    contexts,
    theta_values,
    route_manifest,
) -> {
    objective,
    per_seed_log_likelihood,
    per_seed_score,
    score,
    audit_route_manifest,
}
```

Required behavior:

- compute the same scalar value as the route bound by the manifest;
- seed cotangents with exact context/seed weights;
- call a filter-level reverse scan, not `tf.GradientTape`;
- reject `ad_evaluation_mode=reverse-gradient` and `forward-jvp` for production
  promotion;
- reject any route manifest selecting `transport_ad_mode=full` or
  `filterflow_custom_op`;
- include the P2 no-autodiff sentinel and static audit result in any later
  certification artifact.

## Analytical SIR Derivative Obligation

P4 owns this obligation.

The SIR parameter vector is:

```text
theta = (
    log_kappa_scale,
    log_nu_scale,
    log_obs_noise_scale,
)
```

The current parameterization is:

```text
kappa(theta) = base_kappa * exp(theta[0])
nu(theta) = base_nu * exp(theta[1])
R(theta) = base_observation_covariance * exp(2 * theta[2])
```

Therefore P4 must provide manual parameter adjoints:

```text
d theta[0] += sum_regions d_kappa * kappa
d theta[1] += sum_regions d_nu * nu
d theta[2] += <d_R, 2 * R>
```

For each RK4 substep in `transition_mean`, P4 must provide either:

- a reverse-mode manual VJP for the SIR RHS and RK4 stages; or
- an analytically propagated sensitivity state with a documented equivalence to
  the required VJP for this scalar.

The SIR RHS obligations are:

```text
infection = kappa * susceptible * infectious
d_susceptible = -infection + 0.5 * susceptible_neighbor
d_infectious = infection - nu * infectious + 0.5 * infectious_neighbor
```

The manual route must account for adjoints to susceptible, infectious, `kappa`,
and `nu`, including spatial-neighbor matrix multiplications.  The observation
map is a fixed gather of infectious components; its VJP is scatter-add into the
infectious coordinates.  The observation residual VJP is the negative of the
observation-function VJP with respect to the state.

P4 must not use Zhao-Cui as the LEDH comparator and must not use TensorFlow
autodiff as the production derivative mechanism.  Tiny autodiff checks may
remain diagnostic-only.

## Log-Density And Log-Weight Obligation

P5 owns this obligation.

For a Gaussian log density

```text
ell(r, Sigma) =
    -0.5 * (dim * log(2*pi) + logdet(Sigma) + r^T Sigma^{-1} r),
```

the manual VJP must provide:

```text
d_r += -bar_ell * Sigma^{-1} r
d_Sigma += 0.5 * bar_ell *
    (Sigma^{-1} r r^T Sigma^{-1} - Sigma^{-1})
```

with the correct batch and particle reductions.  Transition covariance is
constant for the current P8p route unless a later reviewed plan changes it.
Observation covariance depends on `theta[2]` and must feed the P4/P5 parameter
score.

The log-normalization VJP is the formula in the reverse-time scan section.
The floor in `log(max(weights, floor))` is a fixed-branch operation.  Later
implementation phases must either prove no entry is floored for the certified
route, or record the floor mask and use the fixed-branch VJP.  They must not
let TensorFlow silently differentiate through the floor.

## LEDH Flow Adjoint Obligation

P5 owns this obligation.

The LEDH flow primitive maps:

```text
(pre_flow_particles, ancestors, observation, model callbacks, covariances)
  -> (post_flow_particles, pre_flow_log_density, forward_log_det)
```

The required manual VJP interface is:

```text
ledh_flow_vjp(
    flow_aux,
    bar_post_flow_particles,
    bar_pre_flow_log_density,
    bar_forward_log_det,
) -> {
    bar_pre_flow_particles,
    bar_ancestors,
    bar_observation_callback_inputs,
    bar_transition_callback_inputs,
    bar_covariances,
    score_theta_contribution,
}
```

The implementation phase must account for the affine transform, posterior mean
and covariance construction, Cholesky/log-determinant terms, triangular solves,
proposal pre-flow log density, and observation residual/Jacobian callbacks.
Each primitive may use TensorFlow tensor math in forward and manual backward
code, but the backward path must not rely on TensorFlow autodiff.  If a matrix
primitive VJP is not derived and tested, P5 must stop instead of leaving a
hidden tape.

## Transport And Sinkhorn Obligation

P6 owns this obligation.

Replaces P1-L013/P1-L015.

The current route
`manual_streaming_finite_sinkhorn_stopped_scale_keys` is blocked because its
custom-gradient `grad` body opens `tf.GradientTape`.  P6 must either replace
that body with the blockwise manual VJP or route production to an audited
manual blockwise VJP mode.

The candidate route
`manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys` must be
audited; it is not certified by name alone.

Required transport VJP layers:

- barycentric product VJP from `prop:bf-ledh-ot-barycentric-vjp`;
- normalized transport output VJP from
  `prop:bf-ledh-ot-normalized-transport-vjp`;
- quadratic cost VJP from `prop:bf-ledh-ot-cost-vjp`;
- log-scale softmin VJP from `prop:bf-ledh-ot-softmin-vjp`;
- finite Sinkhorn reverse scan from `prop:bf-ledh-ot-finite-sinkhorn-vjp`;
- composition with stopped scale, stopped keys, fixed epsilon/epsilon0,
  fixed scaling, fixed steps, padding masks, and chunk sizes.

Required production behavior:

- no `GradientTape` in the transport `grad` body;
- no dense `[B,N,N]` retained transport, cost, probability, or normalizer in
  large-N streaming mode;
- no derivative returned for `eps`, `epsilon0`, or `scaling` in the stopped
  route;
- row residual cotangent ignored or explicitly documented as diagnostic-only;
- padded rows/columns contribute zero cotangent;
- exact same scalar as the manifest-bound forward route.

## Audit Crosswalk

| Leak ID | Current leak | Required P3 obligation | Owner phase | Handoff condition |
|---|---|---|---|---|
| P1-L001 | Outer `tf.GradientTape` around objective | Manual objective score interface and reverse-time scan | P7, with P4-P6 primitive inputs | No production objective tape remains; audit blocks reverse-gradient route. |
| P1-L003 | Outer tape `.gradient` | Manual seed-weighted score aggregation | P7 | Score returned by manual scan, not tape gradient. |
| P1-L004 | Forward accumulator selectable route | Production manifest rejects forward-JVP promotion route | P7/P8 | Forward-JVP stays diagnostic-only or blocked. |
| P1-L005-P1-L008 | P8p `_gradient_diagnostic` tape/jacobian helper | Exact whitelist or removal from production callgraph | P4/P7/P8 | Production route cannot call helper. |
| P1-L013 | Transport `grad` body opens `tf.GradientTape` | Blockwise manual transport VJP | P6 | Transport grad body has no forbidden autodiff. |
| P1-L015 | Transport `tape.gradient` | Manual VJP returns `d_scaled_x`, `d_particles`, `d_logw` | P6 | P2/P6 audit passes grad-body scan. |
| P1-L021-P1-L023 | Streaming score helper tape | Exact diagnostic whitelist or production block | P7/P8 | Helper cannot be production gradient route. |
| P1-L026-P1-L028 | Dense score helper tape | Exact diagnostic whitelist or production block | P7/P8 | Helper cannot be production gradient route. |

## Required Downstream Tests

Later phases must add focused tests before any GPU ladder:

- P4 analytical SIR derivative tests for theta convention and shape/sign
  obligations.
- P5 primitive tests for Gaussian log-density, log-normalization, floor-mask,
  LEDH flow primitive adjoints, and shape contracts.
- P6 transport tests for softmin, transport-from-potentials, finite Sinkhorn
  reverse scan, padding/mask behavior, and no dense retained state in the
  streaming route.
- P7 filter-level manual score tests on tiny fixed-seed cases.
- P8 static and runtime no-autodiff audit bound to the exact route manifest.

Tiny autodiff parity tests may explain local implementation mistakes, but only
the no-autodiff audit and later route-bound artifacts can promote the
production route.

## Next-Phase Handoff

P4 may start only if it accepts this contract and implements or blocks the
analytical SIR derivative obligations.  P4 must not claim that analytical SIR
derivatives certify the full filter score.  P5 and P6 remain separately gated.

P5 may start only after P4 has either implemented the SIR derivative route or
written a blocker that explicitly says which derivative input is missing.

P6 may start only after P5 has bounded non-transport primitive adjoints well
enough to compose with transport, or after a reviewed remediation plan narrows
P6 to transport-only repair without claiming filter-level completion.

## Stop Conditions

Stop the program and write a blocker if:

- any production gradient still requires TensorFlow autodiff;
- any P1/P2 leak class has no owner;
- the floor, mask, random stream, or transport branch cannot be treated as a
  fixed branch under the route manifest;
- a matrix or model primitive VJP is needed but not derived or tested;
- transport repair would require `transport_ad_mode=full`;
- FD, GPU ladder, or actual-gradient validation is needed before P8/P9
  authorization;
- a downstream phase tries to promote tiny autodiff parity, Zhao-Cui, or FD as
  the production oracle.

## Nonclaims

This contract does not conclude no-autodiff certification, implementation
correctness, GPU feasibility, N10000 feasibility, FD agreement, posterior
correctness, HMC readiness, default-route promotion, Zhao-Cui
source-faithfulness, or scientific superiority.
