# Active Transport Loop Bound Audit - 2026-06-17

## Status

`LOOP_BOUND_AUDIT_PASSED_FOR_PLANNED_TINY_ACTIVE_ODD_FIXTURE`

## Scope

This audit covers TensorList-producing constructs reachable from the Phase 4
active-transport score/JIT repair path for the planned tiny fixture:

- batch size `B=1`;
- time steps `T=3`;
- particles `N=8`;
- state dimension `D=2`;
- observation dimension `M=2`;
- transport policy `active-odd`;
- Sinkhorn iterations `3`;
- default row/column chunk sizes from the harness: `32`.

## Source Search Evidence

Searched:

```bash
rg -n "tf\\.while_loop\\(|maximum_iterations=|TensorArray|tf\\.scan|tf\\.map_fn|for .* in" \
  experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py
```

Findings:

- `tf.while_loop`: present and now bounded with `maximum_iterations`.
- `tf.TensorArray`: present in streaming chunk accumulator helpers.
- `tf.scan`: absent.
- `tf.map_fn`: absent.
- Python `for` loops in active transport helpers: absent.

## Bound Derivation Convention

For chunk loops, the iteration variable starts at `0` and updates by
`start += chunk_size`. The loop condition is `start < extent`.

The exact number of iterations is:

```text
ceil(extent / chunk_size) = (extent + chunk_size - 1) // chunk_size
```

For zero extent, the convention is `ceil(0 / chunk_size) = 0`; the condition
`start < extent` is false initially, so the cap is non-binding.

For the planned active-odd fixture, particle extents are `8` and chunk sizes are
`32`, so chunk-loop realized iterations are `ceil(8 / 32) = 1`.

For Sinkhorn loops, the added cap is the existing user-specified
`max_iterations`; the original stopping condition still controls the loop.
With `max_iterations = 3`, the original condition `i < max_iter - 1` allows at
most two body executions before the condition becomes false. The cap of `3` is
therefore non-binding for the original condition.

## Candidate Source Table

| id | source location | construct | dynamic extent | chunk size | derived cap | realized iterations / proof | cap_bound |
| --- | --- | --- | --- | --- | --- | --- | --- |
| streaming_softmin_outer_rows | `annealed_transport_tf.py:367-411` | `TensorArray` + outer `tf.while_loop` | `num_rows`; for active transport calls, `8` | `row_chunk_size=32` | `ceil(num_rows / row_chunk_size)`; fixture `1` | `start=0`, one update to `32`, then `32 < 8` false | `false` |
| streaming_softmin_inner_cols | `annealed_transport_tf.py:380-400` | inner `tf.while_loop` | `num_cols`; for active transport calls, `8` | `col_chunk_size=32` | `ceil(num_cols / col_chunk_size)`; fixture `1` | `start=0`, one update to `32`, then `32 < 8` false | `false` |
| streaming_sinkhorn_loop | `annealed_transport_tf.py:537-557` | `tf.while_loop` | `max_iter` | N/A | existing `max_iter`; fixture `3` | original condition includes `i < max_iter - 1`, so body count is at most `2`; cap `3` cannot bind first | `false` |
| column_normalizer_outer_cols | `annealed_transport_tf.py:621-674` | `TensorArray` + outer `tf.while_loop` | `num_particles=8` | `col_chunk_size=32` | `ceil(num_particles / col_chunk_size)`; fixture `1` | `start=0`, one update to `32`, then `32 < 8` false | `false` |
| column_normalizer_inner_rows | `annealed_transport_tf.py:640-664` | inner `tf.while_loop` | `num_particles=8` | `row_chunk_size=32` | `ceil(num_particles / row_chunk_size)`; fixture `1` | `start=0`, one update to `32`, then `32 < 8` false | `false` |
| transport_from_potentials_outer_rows | `annealed_transport_tf.py:712-793` | `TensorArray` + outer `tf.while_loop` | `num_particles=8` | `row_chunk_size=32` | `ceil(num_particles / row_chunk_size)`; fixture `1` | `start=0`, one update to `32`, then `32 < 8` false | `false` |
| transport_from_potentials_inner_cols | `annealed_transport_tf.py:737-782` | inner `tf.while_loop` | `num_particles=8` | `col_chunk_size=32` | `ceil(num_particles / col_chunk_size)`; fixture `1` | `start=0`, one update to `32`, then `32 < 8` false | `false` |
| exact_sinkhorn_loop | `annealed_transport_tf.py:1102-1123` | `tf.while_loop` | `max_iter` | N/A | existing `max_iter`; fixture `3` | original condition includes `i < max_iter - 1`, so body count is at most `2`; cap `3` cannot bind first | `false` |

## Absent Or Uncapped Constructs

| construct | search result | reason no cap is needed |
| --- | --- | --- |
| `tf.scan` | no occurrence in `annealed_transport_tf.py` | absent from active transport helper path |
| `tf.map_fn` | no occurrence in `annealed_transport_tf.py` | absent from active transport helper path |
| AutoGraph-lowered Python loops | no active-helper Python `for` loop found in `annealed_transport_tf.py` | absent from active transport helper path |
| public `annealed_transport_resample_tf` eager active-row branch | `.numpy()`/`bool(...)` diagnostics exist in public eager wrapper | not reached by the streaming filter's JIT path, which uses `batched_annealed_transport_core_tf` and imports the lower-level helpers directly |

## Decision

All active-path TensorList candidates currently in the allowed repair surface
are explicit `tf.while_loop` / `tf.TensorArray` constructs in
`annealed_transport_tf.py`. Every added cap is derived from the original loop
extent or existing `max_iter`, and every audited row has `cap_bound=false` for
the planned tiny active-odd fixture.

## Nonclaims

This audit is a loop-bound and JIT-structure artifact only. It does not prove
active-transport score correctness, finite-difference correctness, HMC
readiness, posterior validity, production readiness, or performance
improvement.
