# P8k Phase 4 Result: Inactive-Transport Skip Path

metadata_date: 2026-06-18
status: PASS_INACTIVE_TRANSPORT_SKIP
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-generic-batched-dpf-optimization-master-program-2026-06-17.md
phase: 4
executor: Codex
reviewer: Claude Opus max effort, read-only

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | The streaming core now honors the already-advertised `skip_transport_when_no_active=True` semantics for dynamic all-inactive masks, while preserving transport calls for mixed active/inactive masks. |
| Primary criterion status | Passed.  Focused sentinel tests proved the transport core is not called for all-inactive dynamic masks and is called when any batch row is active. |
| Veto diagnostic status | No active veto.  Focused tests passed; no default-policy broadening, GPU profiling, speed claim, or particle-adequacy claim was made. |
| Main uncertainty | No trusted-GPU runtime benefit has been measured yet; Phase 5 owns profiling. |
| Next justified action | Review and launch Phase 5 trusted-GPU profiling ladder. |
| What is not concluded | No GPU speedup, no memory improvement, no particle adequacy, no leaderboard completion, no production/default readiness. |

## Implementation

Changed generic streaming core:

- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`

Change:

- dynamic per-time mask now computes `tf.logical_not(tf.reduce_any(mask))`;
- if `skip_transport_when_no_active=True` and no row is active, the core skips
  `batched_annealed_transport_core_tf`;
- if any row is active, the core still calls transport with the row mask.

Changed tests:

- `tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py`

New tests:

- `test_inactive_transport_dynamic_mask_skips_transport_core`;
- `test_mixed_active_transport_dynamic_mask_calls_transport_core`.

## Checks Run

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py
git diff --check -- experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-*
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py -q -k "inactive_transport or mixed_active_transport or transport or streaming or nonlinear_prior_mean"
```

Results:

- pycompile: passed;
- `git diff --check`: passed;
- focused pytest: `12 passed`.

## Boundary

This phase repairs and verifies existing function-argument semantics.  It does
not introduce a new default policy and does not claim GPU speedup.  All checks
were CPU-only with CUDA intentionally hidden.

## Post-Run Red Team

Strongest alternative explanation:

- The sentinel tests prove call/no-call control flow but do not quantify speed
  benefit.

What would overturn the Phase 4 conclusion:

- A future graph/XLA-only path showing `tf.cond` retraces or executes transport
  unexpectedly under all-inactive masks, or a larger benchmark where the skip
  path changes log likelihood.

Weakest part of the evidence:

- These are focused CPU tests.  GPU profiling is still required before any
  runtime claim.

## Handoff

Phase 5 may proceed after Claude review of this result and the Phase 5
profiling subplan.  Phase 5 must run all GPU/CUDA/TensorFlow GPU commands in
trusted/escalated context.
