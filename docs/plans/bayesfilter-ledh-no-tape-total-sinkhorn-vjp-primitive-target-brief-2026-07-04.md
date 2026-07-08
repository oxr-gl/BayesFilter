# Primitive Target Brief: No-Tape Total Finite Streaming Sinkhorn VJP

Date: 2026-07-04

Status: `PHASE0_DRAFT`

## Target Quantity

The target primitive is the finite streaming transport value currently computed
by:

- `_filterflow_manual_streaming_finite_transport_value_total_vjp`;
- `_filterflow_streaming_finite_sinkhorn_potentials_total_vjp`;
- `_filterflow_streaming_transport_from_potentials`.

In code variables, the forward primitive is:

```text
transported, row_residual =
  finite_transport_total_value(
    scaled_x, particles, logw, eps, epsilon0, scaling,
    steps, row_chunk_size, col_chunk_size)
```

The no-tape VJP must compute the derivative of this same finite scalar:

```text
scalar = reduce_sum(transported * upstream_transported)
```

with respect to the differentiated inputs:

- `scaled_x`;
- `particles`;
- `logw`;
- `epsilon0`.

The current custom-gradient signature also receives `eps` and `scaling`.
Phase 1 may keep those as constants, matching the current tape-backed helper,
only if the Phase 1 result states that `eps` and `scaling` are intentionally
constant for the primitive score route.  If a later row makes either depend on
model parameters, that row is not admitted until these derivatives are added or
the row target explicitly freezes them.

## Forward Equations

Let `N` be the number of particles and

```text
uniform_log_weight = -log(N)
```

The finite potential helper initializes four potential vectors with softmin
calls at `running = epsilon0`:

```text
a_y = softmin(running, x=scaled_x, key=scaled_x, values=logw)
b_x = softmin(running, x=scaled_x, key=scaled_x, values=uniform_log_weight)
a_x = softmin(running, x=scaled_x, key=scaled_x, values=logw)
b_y = softmin(running, x=scaled_x, key=scaled_x, values=uniform_log_weight)
```

For `steps` finite iterations, with

```text
eps_k = running
scaling_factor = scaling ** 2
```

the helper applies:

```text
at_y = softmin(eps_k, scaled_x, scaled_x, logw + b_x / eps_k)
bt_x = softmin(eps_k, scaled_x, scaled_x, uniform_log_weight + a_y / eps_k)
at_x = softmin(eps_k, scaled_x, scaled_x, logw + a_x / eps_k)
bt_y = softmin(eps_k, scaled_x, scaled_x, uniform_log_weight + b_y / eps_k)

a_y = 0.5 * (a_y + at_y)
b_x = 0.5 * (b_x + bt_x)
a_x = 0.5 * (a_x + at_x)
b_y = 0.5 * (b_y + bt_y)
running = max(running * scaling_factor, eps)
```

The final transport value uses the final `alpha/beta` potentials with the
streaming transport-from-potentials helper:

```text
alpha, beta = a_x, b_y  # names as returned by current helper
transported = transport_from_potentials(
  scaled_x, particles, alpha, beta, eps, logw, N)
```

The exact `alpha/beta` naming must be confirmed against current code before
Phase 1 implementation.  A name mismatch is a blocker, not an implementation
detail to guess.

## Reverse Obligations

The no-tape VJP must propagate the cotangent
`upstream_transported` backward through:

1. `transport_from_potentials`, producing cotangents for:
   - `scaled_x`;
   - `particles`;
   - `alpha`;
   - `beta`;
   - `logw`.
2. the finite Sinkhorn potential recursion, producing cotangents for:
   - initial and intermediate potentials;
   - `scaled_x` as both softmin query and key;
   - `logw`;
   - `epsilon0`.
3. every softmin call with both query and key differentiated.

The existing `_filterflow_streaming_softmin_vjp(..., stop_keys=False)` is a
candidate building block because it returns cotangents for query, key, and
values.  Phase 1 must verify whether it also needs explicit epsilon cotangent
support for `epsilon0` and intermediate `running` values.  If it does not
return epsilon cotangents, Phase 1 must add or separately derive them before
claiming total VJP for `epsilon0`.

## What Is Wrong Relative To This Target

The stopped-scale/key helpers are wrong relative to this unstopped target when
used as scores.  They intentionally detach key/scale dependencies and therefore
differentiate a different scalar.

The current total helper targets the correct finite scalar but is not a no-tape
implementation because its custom-gradient body opens `tf.GradientTape`.

## Implementation Boundary

Phase 1 may edit implementation and tests.  Phase 0 does not.

Phase 1 must not claim downstream score correctness.  It can only produce a
candidate no-tape primitive.  Correctness requires Phase 2 parity and finite
difference evidence.
