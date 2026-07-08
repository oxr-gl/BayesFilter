# Dense-IAF Frozen Transport Schema

Date: 2026-07-04

Status: `DENSE_IAF_SCHEMA_READY_FOR_SYNTHETIC_LOADER_IMPLEMENTATION`

## Schema ID

`bayesfilter.neutra.dense_iaf_frozen_transport.v1`

## Purpose

This schema represents a frozen dense-IAF NeuTra transport for a generic
BayesFilter nonlinear SSM target. It is a transport serialization schema only.
It does not train NeuTra, run HMC, prove posterior correctness, or certify
sampler convergence.

## Canonical Target Signature

`target_signature` is required and must be the stable hash produced by:

```text
bayesfilter.ssm.stable_ssm_target_signature(SSMTargetContract(..., frozen_transport=None))
```

The hashed payload is the canonical generic `SSMTargetContract` manifest:

- `problem`: static SSM shape, data signature, coordinate convention, and model
  manifest;
- `chart`: parameter names, unconstrained dimension, constrained shape,
  transform manifest, and log-Jacobian convention;
- `prior`: prior manifest, support policy, and log-density authority;
- `filter_program`: filter identity, required model capabilities,
  deterministic-target policy, approximation semantics, and filter manifest;
- `frozen_transport`: `None`.

Legacy target names, class paths, result-note labels, runtime object identities,
memory addresses, process-local ids, and unreviewed model instances are not
valid target signatures. A legacy artifact without this canonical signature is
reject-only until a later target-signature bridge supplies the exact generic
contract and proves the signature match.

## Top-Level Required Fields

| Field | Type | Rule |
| --- | --- | --- |
| `schema` | string | Must equal `bayesfilter.neutra.dense_iaf_frozen_transport.v1`. |
| `transport_id` | string | Stable nonempty id; must not contain process-local identity. |
| `dimension` | positive integer | Unconstrained parameter dimension. |
| `target_signature` | string | Canonical generic `SSMTargetContract` signature. |
| `log_jacobian_available` | boolean | Must be `true`. |
| `component_order` | list of strings | Ordered component ids in forward order. |
| `components` | list of component payloads | Every component id in `component_order` must appear exactly once. |
| `topology_hash` | SHA-256 string | Stable hash of schema, dimension, component order, component kinds, hidden layers, activation, masks/degrees policy, `s_max`, and tensor shapes, excluding tensor values. |
| `tensor_hash` | SHA-256 string | Stable hash of all tensor values in component order, with dtype and shape. |
| `transport_hash` | SHA-256 string | Stable hash of schema, transport id, dimension, target signature, topology hash, tensor hash, and logdet semantics. |
| `training_state_hash` | SHA-256 string or null | Optional hash of the original training-state payload, if preserved. |
| `source_artifact_hashes` | mapping | Optional mapping from source path role to SHA-256. |
| `nonclaims` | list of strings | Must include the nonclaims below. |

Required nonclaims:

- `frozen dense-IAF transport artifact loader only`;
- `no NeuTra training claim`;
- `no HMC tuning or sampling claim`;
- `no posterior convergence claim`;
- `no scientific validity claim`;
- `no default policy change`.

## Component Payloads

### `dense_autoregressive_iaf`

Represents the observed legacy MADE-style dense autoregressive IAF layer.

Required fields:

- `component_id`;
- `kind = "dense_autoregressive_iaf"`;
- `dim`;
- `hidden_layers`;
- `activation`;
- `s_max`;
- `masks_policy = "legacy_degree_masks_v1"`;
- `dtype`;
- `weights`;
- `biases`;
- `component_topology_hash`;
- `component_tensor_hash`.

Rules:

- `dim` must equal top-level `dimension`.
- `hidden_layers` must be positive integers.
- `activation` must be one of the reviewed activations implemented by the
  loader, initially `elu`, `tanh`, or `relu`.
- `weights` and `biases` lengths must match `len(hidden_layers) + 1`.
- Weight shapes must match `(layer_sizes[i], layer_sizes[i+1])` where
  `layer_sizes = [dim] + hidden_layers + [2 * dim]`.
- Bias shapes must match `(layer_sizes[i+1],)`.
- The output layer splits into scale logits and shifts of size `dim`.
- Forward semantics:

```text
h_0 = z
h_{j+1} = activation((h_j @ (W_j * mask_j)) + b_j) for hidden layers
raw = h_last @ (W_out * mask_out) + b_out
s, t = split(raw, 2)
s = s_max * tanh(s / s_max)
u = z * exp(s) + t
log_abs_det_jacobian = sum_i s_i
```

The exact mask generation is part of topology and must be deterministic:

- input degrees: `1, ..., dim`;
- hidden degrees: `1 + (arange(width) mod max(1, dim - 1))`;
- output degrees: two copies of `1, ..., dim`;
- hidden mask relation: `deg_in <= deg_out`;
- output mask relation: `deg_in < deg_out`.

### `mixing_linear`

Required fields:

- `component_id`;
- `kind = "mixing_linear"`;
- `dim`;
- `matrix`;
- `dtype`;
- `component_topology_hash`;
- `component_tensor_hash`.

Forward semantics:

```text
u = z @ matrix
log_abs_det_jacobian = slogdet(matrix)
```

The matrix must be square `[dim, dim]` and finite. A singular or nonfinite
matrix is reject-only.

### `affine`

Required fields:

- `component_id`;
- `kind = "affine"`;
- `dim`;
- one of `scale` or `L_np`;
- `offset`;
- `dtype`;
- `component_topology_hash`;
- `component_tensor_hash`.

Forward semantics:

```text
u = offset + z * scale
```

or

```text
u = offset + z @ transpose(L_np)
```

depending on which payload is present. Logdet is the sum of log absolute scales
or `slogdet(L_np)`.

### `affine_dense`

`affine_dense` is accepted only when its payload is reducible to the `affine`
semantics above with explicit dense matrix and offset. Otherwise it is
reject-only as `unsupported_transport_kind`.

### `composed`

Required fields:

- `component_id`;
- `kind = "composed"`;
- `children`;
- `component_topology_hash`;
- `component_tensor_hash`.

Forward semantics:

```text
u = child_k(...child_2(child_1(z))...)
log_abs_det_jacobian = sum_j child_j_log_abs_det_jacobian
```

The top-level `component_order` must be the flattened forward execution order.

## Hash Rules

All hashes use SHA-256 over JSON normalized with sorted keys and compact
separators. Tensors are hashed with explicit dtype, shape, and nested finite
numeric values. Hash payloads must reject process-local identity strings before
hashing.

`topology_hash` excludes tensor numeric values. `tensor_hash` excludes target
identity and nonclaims. `transport_hash` binds topology, tensors, target
signature, dimension, and logdet semantics.

## Mapping/Rejection Table

| Phase 1 class or observed payload | Schema coverage | Target-signature handling | Status before Phase 4 bridge |
| --- | --- | --- | --- |
| Embedded `transport_state` with `composed`, `mixing_linear`, `affine`, `affine_dense`, `dense_autoregressive_iaf` | Representable if all tensors are finite and shapes match component rules. | Requires canonical generic `SSMTargetContract` signature. Legacy target metadata is insufficient. | Reject-only as `missing_target_signature`. |
| Embedded replay `transport` with same component kinds | Representable if replay payload maps to component rules. | Requires canonical generic `SSMTargetContract` signature. | Reject-only as `missing_target_signature`. |
| Summary/latest JSON with `replay_state_path` or `training_state_path` | Not a transport payload by itself. May point to another artifact. | Target signature must be taken from canonical bridge, not the summary name. | Reject-only as `missing_payload` unless referenced payload is separately admitted. |
| Per-parameter statistics JSON | No frozen transport tensors. | Not applicable. | `not_migration_candidate`. |
| Markdown result note from prior inventory | Provenance only. | Not a generic signature source. | `missing_payload` or `missing_target_signature` per prior inventory. |
| Candidate freeze/tuning summary without dense-IAF tensors | No dense-IAF transport payload. | Not applicable. | `not_migration_candidate`. |
| Any payload with process-local identity | Forbidden. | Forbidden. | `unsafe_identity`. |
| Any payload requiring execution of legacy model code to identify target | Not admitted by schema alone. | Requires later reviewed target bridge. | Reject-only until bridge. |

## Loader Rejection Requirements

A loader for this schema must reject:

- unsupported schema id;
- missing or mismatched canonical `target_signature`;
- `log_jacobian_available != true`;
- dimension mismatch between top-level dimension and components;
- unknown component kind;
- nonfinite tensor;
- invalid tensor shape;
- missing topology hash, tensor hash, or transport hash;
- hash mismatch;
- process-local identity;
- summary/latest/result artifacts that do not contain a transport payload;
- legacy target names or class paths offered as generic signatures.

## What Is Correct, Unsupported, And Not Checked

| Statement | Classification |
| --- | --- |
| The schema can represent the observed legacy dense-IAF topology classes if tensor shapes are finite and explicit. | `correct` |
| A historical artifact with embedded dense-IAF tensors is loadable without a generic target signature. | `wrong relative to the stated target` |
| Legacy target names or runtime class paths are equivalent to `SSMTargetContract` signatures. | `unsupported` |
| HMC convergence or posterior correctness follows from this schema. | `unsupported` |
| Numerical parity between a future BayesFilter loader and legacy source code. | `not checked` |

`DENSE_IAF_SCHEMA_READY_FOR_SYNTHETIC_LOADER_IMPLEMENTATION`
