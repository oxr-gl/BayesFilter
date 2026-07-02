# Phase 0 Result: Route And Artifact Inventory

Date: 2026-07-01

Status: `PASS`

## Decision

Phase 0 passed.  The corrected total-derivative route artifacts are present,
the focused local checks pass, trusted GPU probes see the RTX 4080 SUPER, and
the Phase 1 selector pair is proven from code anchors to dispatch to the
total-derivative helper.

This phase does not prove GPU/XLA viability of the corrected route.  It only
proves that Phase 1 is allowed to test it.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Are the corrected total-derivative route artifacts present, locally checkable, and ready for a tiny trusted GPU/XLA smoke? |
| Primary criterion | Passed. |
| Veto diagnostics | No veto triggered. |
| Not concluded | No GPU/XLA full-route viability, no HMC readiness, no posterior correctness, no production promotion. |

## Local Checks

Compile check:

```bash
python -m py_compile \
  docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py \
  docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  docs/benchmarks/diagnose_p8p_sir_active_transport_comparator_contract.py \
  experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py \
  experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py
```

Result: passed.

Focused test check:

```bash
pytest -q \
  tests/test_p8p_sir_active_transport_comparator_contract.py \
  tests/test_ledh_pfpf_ot_p7_manual_score.py \
  tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
```

Result: `36 passed, 2 warnings`.

## Trusted GPU Probe

Command:

```bash
nvidia-smi
```

Result:

- GPU: NVIDIA GeForce RTX 4080 SUPER.
- Driver version: `591.86`.
- CUDA version: `13.1`.
- Memory: `16376 MiB`.

TensorFlow trusted GPU probe:

```bash
python - <<'PY'
import tensorflow as tf
print('physical', tf.config.list_physical_devices('GPU'))
print('logical', tf.config.list_logical_devices('GPU'))
print('tf32', tf.config.experimental.tensor_float_32_execution_enabled())
PY
```

Result:

- physical GPU list contains `/physical_device:GPU:0`;
- logical GPU list contains `/device:GPU:0`;
- TF32 execution enabled: `True`.

TensorFlow emitted repeated factory-registration warnings.  They did not block
device creation.

## Static Dispatch Proof

The Phase 1 command uses:

```text
--transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys
--transport-ad-mode full
```

The gradient-mode string is a legacy selector name.  The dispatch proof below
shows that the derivative branch is controlled by `transport_ad_mode="full"`.

1. `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:468-494`
   builds microbatch contexts by copying grouped `args` into each context.
   Therefore the Phase 1 `transport_ad_mode` flag reaches the context.

2. `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py:545-582`
   defines the manual-reverse diagnostic and calls
   `p8p._manual_value_and_score_from_components(context["tensors"],
   context["args"], ...)`.  Therefore the context `args.transport_ad_mode`
   reaches the P8p manual value/score route.

3. `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:587-626`
   checks that `args.transport_ad_mode` is either `stabilized` or `full`; when
   it is `full`, the manual transport VJP calls
   `annealed_transport_tf._filterflow_manual_streaming_finite_transport_total_vjp`.

4. `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py:703-746`
   checks the same `args.transport_ad_mode` in the manual forward transport.
   It stops center/scale/epsilon only for `stabilized`; when the mode is
   `full`, it calls
   `annealed_transport_tf._filterflow_manual_streaming_finite_transport_total_vjp`.

5. `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py:1394-1468`
   also allows `transport_ad_mode in {"stabilized", "full"}` for the manual
   streaming finite route.  For `stabilized`, it selects
   `_filterflow_manual_streaming_finite_transport_stopped_scale_keys`; otherwise
   it selects `_filterflow_manual_streaming_finite_transport_total_vjp`.

6. `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:2101-2189`
   defines `_filterflow_manual_streaming_finite_transport_total_vjp` as the
   streaming finite transport with total-derivative custom VJP.  Its docstring
   states that it differentiates the finite fixed-iteration transport value and
   intentionally does not use the historical stopped-scale/key derivative.

Conclusion:

The Phase 1 selector pair dispatches to the total-derivative helper.  Metadata
alone is not being used as the proof.

## Phase 1 Handoff

Phase 1 may launch after Claude reviews this result and the refreshed Phase 1
subplan.

Required Phase 1 veto remains:

- if output metadata does not record `transport_ad_mode="full"`, Phase 1 fails;
- if output tensors are not on GPU, Phase 1 fails;
- if XLA JIT is not used, Phase 1 fails;
- if objective or gradient is nonfinite, Phase 1 fails.

## Nonclaims

- No GPU/XLA viability of the corrected route has been tested yet.
- No HMC/NUTS readiness.
- No posterior correctness.
- No production/default promotion.
