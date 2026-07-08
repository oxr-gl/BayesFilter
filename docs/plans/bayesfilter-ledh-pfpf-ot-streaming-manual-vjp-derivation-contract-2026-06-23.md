# LEDH-PFPF-OT Streaming Manual VJP Derivation Contract

date: 2026-06-23
phase: S1-DERIVATION-CONTRACT
status: DRAFT_FOR_LOCAL_CHECK_AND_REVIEW

## Scope

This contract defines the blockwise manual VJP for the
`manual_streaming_finite_sinkhorn_stopped_scale_keys` route.  It covers:

- the softmin VJP;
- the transport-from-potentials VJP;
- the finite Sinkhorn recursion VJP;
- stopped keys and stopped scale semantics;
- block accumulation and padding/mask policy;
- retained quantities and forbidden dense retained state;
- implementation exclusions, including no `GradientTape` in streaming backward.

Static acceptance terms are intentionally literal in this artifact: softmin,
transport-from-potentials, finite Sinkhorn recursion, column normalizer,
cost-to-query/key handling, block accumulation, retained quantities, stopped
keys, stopped scale, exact scalar, padding/mask policy, no hidden dense
retained state, exact comparators, implementation exclusions, and no
`GradientTape` in streaming backward.

The contract is for the transport core in
`experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.
It does not make a P82, HMC, posterior-correctness, default-route, or
production-readiness claim.

## Exact Comparators And Forward Routes

Dense/manual comparators:

- `_filterflow_manual_dense_finite_softmin_vjp`
- `_filterflow_manual_dense_finite_sinkhorn_vjp`
- `_filterflow_manual_dense_finite_transport_matrix_vjp_stopped_scale_keys`

Streaming forward routes:

- `_filterflow_streaming_softmin`
- `_filterflow_streaming_transport_from_potentials`
- `_filterflow_streaming_finite_sinkhorn_potentials_stopped_scale_keys`
- `manual_streaming_finite_sinkhorn_stopped_scale_keys`

The new streaming backward must agree with these routes only within the scope
of their code-defined scalar and stopped/frozen boundaries.  Dense/manual
comparators are tiny-fixture diagnostics, not a large-N oracle.

## Exact Scalar And Differentiated Inputs

For the core custom-gradient route, the exact scalar is the cotangent
contraction with the transported particle output:

```text
L = sum_{b,i,d} U[b,i,d] * transported[b,i,d]
```

where `U` is the upstream cotangent supplied to the custom gradient.  The
`row_residual` output is a diagnostic output; its cotangent is ignored in this
route, matching the current custom-gradient wrapper behavior.

The differentiable inputs for this route are:

- `scaled_x`;
- `particles`;
- `logw`.

The frozen or stopped inputs are:

- `eps`;
- `epsilon0`;
- `scaling`;
- `steps`;
- chunk sizes;
- `float_n`;
- Sinkhorn keys inside the finite Sinkhorn recursion.

No derivative is returned for `eps`, `epsilon0`, or `scaling`.  Their numeric
values still appear in local VJP formulas as fixed coefficients.

## Softmin VJP

Forward softmin, for batch `b`, query row `i`, and key/value column `j`:

```text
C[b,i,j] = 0.5 * ||query[b,i,:] - key[b,j,:]||^2
Z[b,i,j] = values[b,j] - C[b,i,j] / epsilon[b]
s[b,i] = -epsilon[b] * logsumexp_j Z[b,i,j]
P[b,i,j] = softmax_j Z[b,i,j]
```

For upstream `u[b,i] = dL / ds[b,i]`:

```text
d_values[b,j] += -epsilon[b] * sum_i u[b,i] * P[b,i,j]
dC[b,i,j] += u[b,i] * P[b,i,j]
```

Cost-to-query/key handling:

```text
d_query[b,i,:] += sum_j dC[b,i,j] * (query[b,i,:] - key[b,j,:])
d_key[b,j,:]   += sum_i dC[b,i,j] * (key[b,j,:] - query[b,i,:])
```

For stopped keys, `d_key` is omitted and only `d_query` is accumulated.  The
finite Sinkhorn recursion uses stopped keys, so its softmin VJPs must not return
a key-side contribution.  Any helper that supports key gradients must expose the
choice explicitly.

Block accumulation rules:

- process row blocks and column blocks matching the streaming forward chunking;
- recompute only the current block logits/probabilities;
- accumulate `d_values` across row blocks;
- accumulate `d_query` for the current row block;
- optionally accumulate `d_key` across row blocks only when the caller has not
  requested stopped-key semantics.

No softmin VJP may retain or return a full `[B,N,N]` probability, cost, or
transport tensor in the large-N streaming route.

## Transport-From-Potentials VJP

Forward route:

```text
A[b,i,j] = (f[b,i] + g[b,j] - C[b,i,j]) / eps[b]
M[b,j]   = logsumexp_i A[b,i,j]
T[b,i,j] = exp(A[b,i,j] - M[b,j] + log(float_n) + logw[b,j])
transported[b,i,d] = sum_j T[b,i,j] * particles[b,j,d]
```

with:

```text
C[b,i,j] = 0.5 * ||scaled_x[b,i,:] - scaled_x[b,j,:]||^2
```

Column normalizer contract:

- `M[b,j]` is the column normalizer.
- Because `g[b,j] / eps[b]` appears in every row of the same column and also in
  `M[b,j]`, `g` cancels from the code-defined `T`.
- Therefore `d_g` for the exact code-defined scalar is zero, up to floating
  point roundoff if a diagnostic implementation computes it indirectly.
- S3 must still include an explicit column normalizer adjoint check.  A missing
  normalizer adjoint is a veto because it would produce the wrong `d_f`,
  `d_scaled_x`, and `d_logw`.

Direct barycentric adjoints for upstream `U[b,i,d]`:

```text
dT[b,i,j] += sum_d U[b,i,d] * particles[b,j,d]
d_particles[b,j,d] += sum_i T[b,i,j] * U[b,i,d]
```

For each column `j`, define:

```text
P[b,i,j] = exp(A[b,i,j] - M[b,j])
R[b,i,j] = dT[b,i,j] * T[b,i,j]
S[b,j]   = sum_i R[b,i,j]
dA[b,i,j] = R[b,i,j] - P[b,i,j] * S[b,j]
```

Then:

```text
d_logw[b,j] += S[b,j]
d_f[b,i]    += sum_j dA[b,i,j] / eps[b]
d_g[b,j]    += sum_i dA[b,i,j] / eps[b] = 0
dC[b,i,j]   += -dA[b,i,j] / eps[b]
```

Final transport cost-to-state handling is not stopped-key handling.  The final
transport cost uses `scaled_x` as both query and key, so both sides contribute:

```text
d_scaled_x_query[b,i,:] += sum_j dC[b,i,j] * (scaled_x[b,i,:] - scaled_x[b,j,:])
d_scaled_x_key[b,j,:]   += sum_i dC[b,i,j] * (scaled_x[b,j,:] - scaled_x[b,i,:])
d_scaled_x += d_scaled_x_query + d_scaled_x_key
```

Block accumulation rules:

- use column blocks as the outer unit when convenient because the normalizer is
  column-wise;
- for each column block, either retain only block-sized `S[b,j]` or recompute a
  first pass over row blocks to get it;
- use a second pass over row blocks to accumulate `d_f`, `d_scaled_x`, and any
  block-local diagnostics;
- accumulate `d_particles` and `d_logw` by column block;
- never retain a full `[B,N,N]` `T`, `P`, `A`, or `C`.

The transport-from-potentials VJP may use a two-pass or recompute design.  The
contract requirement is bounded retained state, not single-pass execution.

## Finite Sinkhorn Recursion VJP

Forward recursion for stopped-scale/key route:

```text
key_x = stop_gradient(x)
running = epsilon0
eps = epsilon
scaling_factor = scaling^2

a_y = softmin(running, x, key_x, log_alpha)
b_x = softmin(running, x, key_x, log_beta)
a_x = softmin(running, x, key_x, log_alpha)
b_y = softmin(running, x, key_x, log_beta)

repeat steps times:
    running_ = reshape(running, [-1, 1])
    at_y = softmin(running, x, key_x, log_alpha + b_x / running_)
    bt_x = softmin(running, x, key_x, log_beta  + a_y / running_)
    at_x = softmin(running, x, key_x, log_alpha + a_x / running_)
    bt_y = softmin(running, x, key_x, log_beta  + b_y / running_)
    a_y = 0.5 * (a_y + at_y)
    b_x = 0.5 * (b_x + bt_x)
    a_x = 0.5 * (a_x + at_x)
    b_y = 0.5 * (b_y + bt_y)
    running = max(running * scaling_factor, eps)

alpha = softmin(eps, x, key_x, log_alpha + b_x / eps)
beta  = softmin(eps, x, key_x, log_beta  + a_y / eps)
```

The streaming implementation returns only `alpha` and `beta` for this finite
route.  The dense comparator also computes `a_x` and `b_y`; these are internal
states for the recursion and can be useful for parity diagnostics, but they are
not extra public outputs of the streaming transport route.

Reverse recursion mirrors `_filterflow_manual_dense_finite_sinkhorn_vjp` with
the dense softmin VJP replaced by the blockwise softmin VJP:

1. Seed upstreams from the final transport VJP:
   - `d_alpha` from transport `d_f`;
   - `d_beta` from transport `d_g`, which should be zero for the code-defined
     transport scalar but must still be accepted by the recursion API;
   - zero upstreams for internal `a_x` and `b_y` unless a diagnostic route asks
     for them.
2. Run the final `alpha` and `beta` softmin VJPs:
   - add `d_values` from `alpha` to `d_log_alpha`;
   - add `d_values / eps` from `alpha` to `d_b_x`;
   - add `d_values` from `beta` to `d_log_beta`;
   - add `d_values / eps` from `beta` to `d_a_y`;
   - add each softmin `d_query` to `d_x_from_sinkhorn_cost`.
3. Traverse saved vector states in reverse.  For each saved state
   `(running, old_a_y, old_b_x, old_a_x, old_b_y)`:
   - split each averaging adjoint by `0.5`;
   - run four blockwise softmin VJPs at fixed `running`;
   - add `d_values` to `d_log_alpha` or `d_log_beta`;
   - add `d_values / running` to the corresponding old potential adjoint;
   - add each softmin `d_query` to `d_x_from_sinkhorn_cost`;
   - replace current potential adjoints with the old potential adjoints.
4. Run the four initial softmin VJPs at fixed `epsilon0`:
   - two contribute to `d_log_alpha`;
   - two contribute to `d_log_beta`;
   - all contribute stopped-key `d_query` to `d_x_from_sinkhorn_cost`.

Stopped keys and stopped scale:

- every recursion softmin uses `key_x = stop_gradient(x)`, so its cost VJP
  contributes only to the query side of `x`;
- `running`, `eps`, `epsilon0`, and `scaling_factor` are fixed coefficients;
- no adjoint is propagated into `running`, `eps`, `epsilon0`, or `scaling`;
- the `max(running * scaling_factor, eps)` branch is not differentiated in this
  route.

Retained quantities:

- allowed: `running`, `a_y`, `b_x`, `a_x`, and `b_y` vectors per iteration;
- allowed: scalar/static metadata such as `steps`, chunk sizes, and dtype;
- allowed: block-sized temporaries inside the current loop body;
- forbidden: retained full `[B,N,N]` costs, logits, probabilities, transports,
  normalizers expanded over rows, or dense transport matrices.

## Padding/Mask Policy

All blockwise helpers must implement an explicit padding/mask policy:

- valid row mask: `row_start + arange(row_chunk_size) < num_rows`;
- valid column mask: `col_start + arange(col_chunk_size) < num_cols`;
- padded output rows are discarded and their upstreams are treated as zero;
- padded columns use log-zero values, log-zero weights, or an explicit mask so
  their softmax probability and transport contribution are zero;
- padded query/key coordinates may have arbitrary padded numeric values, but
  masked probabilities or transports must prevent any contribution from leaking;
- accumulated gradients are written only to valid slices;
- `row_residual` and other diagnostics must not use padded rows or columns as
  evidence.

Exact-chunk and padded-chunk fixtures are both required.  A helper that passes
only when `N` is divisible by both chunk sizes is not acceptable.

## Implementation Exclusions

The new streaming backward must not use:

- `GradientTape` in streaming backward;
- dense `[B,N,N]` retained state in the large-N route;
- `transport_ad_mode=full` as a governed `N=10000` path;
- Zhao-Cui as a comparator;
- finite differences as an implementation oracle;
- tiny autodiff diagnostics as evidence of large-N memory success.

Autodiff may appear only in tiny diagnostic tests or existing comparator code
outside the new streaming backward.  It must not be the mechanism that computes
the production candidate streaming gradient.

## Layer Coverage Checklist

Softmin VJP:

- inputs: `epsilon`, `query`, `key`, `values`, `upstream`, chunk sizes, stopped
  key flag;
- outputs: `d_query`, optional `d_key`, `d_values`;
- block accumulation: row/column block recomputation, no dense retained state;
- stopped quantities: optional stopped key, fixed epsilon;
- exact scalar: upstream contraction with softmin output;
- padding/mask policy: valid row/column masks and log-zero padded columns;
- comparators: `_filterflow_manual_dense_finite_softmin_vjp`,
  `_filterflow_streaming_softmin`.

Transport-from-potentials VJP:

- inputs: `scaled_x`, `particles`, `f`, `g`, `eps`, `logw`, `float_n`,
  `upstream`, chunk sizes;
- outputs: `d_scaled_x`, `d_particles`, `d_f`, `d_g` equal to zero for the
  code-defined scalar, and `d_logw`;
- block accumulation: column normalizer plus two-pass/recompute column-block
  adjoint;
- stopped quantities: fixed `eps` and `float_n`;
- exact scalar: upstream contraction with `transported`;
- padding/mask policy: valid row/column masks and no padded mass leakage;
- comparators: `_filterflow_manual_dense_finite_transport_matrix_vjp_stopped_scale_keys`,
  `_filterflow_streaming_transport_from_potentials`.

Finite Sinkhorn recursion VJP:

- inputs: `log_alpha`, `log_beta`, `x`, `epsilon`, `epsilon0`, `scaling`,
  `steps`, upstreams for `alpha` and `beta`, chunk sizes;
- outputs: `d_log_alpha`, `d_log_beta`, `d_x_from_sinkhorn_cost`;
- block accumulation: reverse recursion over vector states with blockwise
  softmin VJPs;
- stopped quantities: stopped keys and stopped scale;
- exact scalar: upstream contractions through final `alpha` and `beta`;
- padding/mask policy: inherited from softmin VJP;
- comparators: `_filterflow_manual_dense_finite_sinkhorn_vjp`,
  `_filterflow_streaming_finite_sinkhorn_potentials_stopped_scale_keys`,
  `manual_streaming_finite_sinkhorn_stopped_scale_keys`.

## S2 Handoff

S2 may implement only the first primitive slice, the blockwise softmin VJP, but
it must preserve the full S1 contract.  A successful S2 cannot narrow the
program to softmin-only correctness.  S3 remains responsible for the column
normalizer and transport-from-potentials VJP, and S4 remains responsible for the
finite Sinkhorn recursion VJP.
