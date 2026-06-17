# Phase 1 Baseline Fixture Spec: Scalable OT Transport Baseline

Date: 2026-06-17

## Purpose

Define deterministic fixtures for the current TensorFlow dense/streaming
FilterFlow-style annealed transport baseline.  These fixtures are comparator
artifacts for later scalable OT candidates.

## Baseline Function

- Module: `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- Function: `annealed_transport_resample_tf`
- Dense mode: `transport_plan_mode="dense"` returns a materialized transport
  matrix.
- Streaming mode: `transport_plan_mode="streaming"` applies the transport
  without returning a dense matrix; the transport object is represented by the
  explicit non-materialization reason `streaming_no_dense_matrix`.

## Shared Settings

| Field | Value |
| --- | --- |
| Backend | TensorFlow |
| Device policy | CPU-only (`CUDA_VISIBLE_DEVICES=-1`) |
| Dtype | `tf.float64` |
| Transport gradient mode | `raw` |
| Epsilon | `0.5` |
| Scaling | `0.9` |
| Convergence threshold | `1e-3` |
| Max iterations | `12` |
| Row/column chunk size | `4` unless overridden by fixture |
| Randomness | No runtime random draws; all fixtures are deterministic formulas |

## Fixtures

| Fixture | Shape | Intent | Construction |
| --- | --- | --- | --- |
| `tiny_manual` | `B=1,N=6,D=3` | Manually inspectable transport fixture. | Fixed low-dimensional grid plus deterministic unequal log weights. |
| `small_parity` | `B=2,N=16,D=5` | Dense-vs-streaming transported-particle parity. | Smooth deterministic sine/cosine particle coordinates and fixed batch-dependent log weights. |
| `high_dim_low_rank` | `B=1,N=64,D=32` | High-dimensional but intrinsically low-rank transport baseline diagnostic. | Particles lie in a deterministic rank-4 subspace embedded into 32 dimensions. |
| `high_dim_locality` | `B=1,N=64,D=32` | Locality/sparsity pre-diagnostic for later sparse lane. | Particles form deterministic ordered clusters with small within-cluster offsets. |

## Required Diagnostics

For each fixture and transport mode:

- finite particles and log weights;
- output particle shape;
- log-weight normalization residual;
- transported-particle norm;
- wall time;
- row residual and column residual reported by baseline diagnostics;
- materialized transport matrix shape for dense mode;
- `not_materialized_reason` for streaming mode.

For dense mode only:

- row residual recomputed from the materialized matrix;
- column residual recomputed from the materialized matrix;
- transport mass;
- finite transport matrix.

For dense-vs-streaming comparison:

- max absolute transported-particle difference;
- RMS transported-particle difference;
- dense and streaming diagnostic residuals side by side.

## Pass/Fail Rules

Hard vetoes:

- any nonfinite particles or log weights;
- dense transport matrix missing in dense mode;
- streaming transported particles missing;
- dense recomputed row residual is nonfinite;
- dense recomputed column residual is nonfinite;
- dense-vs-streaming transported-particle max error is nonfinite;
- required JSON artifact is missing.

Promotion/pass for Phase 1:

- all required fixtures run on CPU;
- dense and streaming modes emit finite transported particles;
- dense-vs-streaming transported-particle differences are recorded;
- diagnostics are written to JSON and summarized in the Phase 1 result.

## Non-Claims

- No scalable candidate correctness.
- No speedup claim.
- No posterior validity claim.
- No production default change.
- No statistical ranking.
- No GPU performance claim.
