# Phase 4 Result: Transport Adjoint And Stopped-Scale-Key Audit

Date: 2026-07-01

Status: `PASSED`

## Decision

Phase 4 passes as a local transport-algebra audit.  The P8p manual transport
VJP wrapper matches TensorFlow autodiff through the pinned non-custom-gradient
stopped-scale-key forward helper on active-all, inactive-all, and mixed masks.

This clears the local transport wrapper boundary tested here.  It does not
establish full SIR score correctness, GPU/TF32 material correctness, HMC
readiness, or that non-centered/process-noise representation is irrelevant.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the P8p manual transport VJP wrapper match autodiff for the same stopped-scale-key forward transport before full-filter score assembly? |
| Baseline/comparator | TensorFlow autodiff of identical fixed tensors through `annealed_transport_tf._filterflow_manual_streaming_finite_transport_value_stopped_scale_keys`, wrapped to reproduce P8p stopped center/scale, stopped `epsilon0`, mask, and uniform reset semantics. |
| Primary criterion | For each active-all, inactive-all, and mixed mask case, `bar_post_flow` and `bar_normalized_log_weights` residuals must satisfy max absolute residual `<= 1.0e-8` and relative L2 residual `<= 1.0e-7`. |
| Veto diagnostics | Comparator using the same custom-gradient route being tested, missing mask cases, CPU result claimed as material GPU/TF32 evidence, unsupported full-filter correctness claim. |
| Not concluded | Full SIR score correctness, GPU/TF32 runtime correctness, HMC readiness, or that non-centered process noise is irrelevant. |

## Commands Run

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/diagnose_p8p_sir_transport_adjoint_vjp.py
pytest -q tests/test_p8p_sir_transport_adjoint_vjp.py
python docs/benchmarks/diagnose_p8p_sir_transport_adjoint_vjp.py --output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase4-transport-adjoint-2026-07-01.json
```

## Artifacts

- Diagnostic:
  `docs/benchmarks/diagnose_p8p_sir_transport_adjoint_vjp.py`
- Tests:
  `tests/test_p8p_sir_transport_adjoint_vjp.py`
- JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase4-transport-adjoint-2026-07-01.json`

## Local Check Results

- Compile check: passed.
- `pytest -q tests/test_p8p_sir_transport_adjoint_vjp.py`: `3 passed`.
- Diagnostic status: `PASS`.
- Failure localization: `pass`.
- Artifact CPU boundary: `CUDA_VISIBLE_DEVICES=-1`; recorded tensor devices
  were CPU only.
- Comparator guard: passed with zero calls to the forbidden custom-gradient
  transport routes:
  - `_filterflow_manual_streaming_finite_transport_stopped_scale_keys`: `0`
  - `_filterflow_manual_streaming_blockwise_vjp_finite_transport_stopped_scale_keys`: `0`

TensorFlow printed CUDA plugin registration and `cuInit` messages during import.
Those messages are not material GPU evidence because this diagnostic explicitly
hid CUDA devices and recorded CPU-only tensors.

## Numerical Summary

All comparisons passed.

| Case | Tensor | Max absolute residual | Relative L2 residual |
| --- | --- | ---: | ---: |
| active-all transport contribution | `bar_post_flow` | `2.3314683517128287e-15` | `7.470158257190283e-16` |
| active-all transport contribution | `bar_normalized_log_weights` | `8.881784197001252e-16` | `2.7871604591149337e-16` |
| inactive-all transport contribution | `bar_post_flow` | `0.0` | `0.0` |
| inactive-all transport contribution | `bar_normalized_log_weights` | `0.0` | `0.0` |
| mixed transport contribution | `bar_post_flow` | `5.551115123125783e-16` | `3.120057523897156e-16` |
| mixed transport contribution | `bar_normalized_log_weights` | `5.551115123125783e-17` | `8.326672684688674e-17` |
| active-all caller masked step | `bar_post_flow` | `2.3314683517128287e-15` | `7.470158257190283e-16` |
| active-all caller masked step | `bar_normalized_log_weights` | `8.881784197001252e-16` | `2.7871604591149337e-16` |
| inactive-all caller masked step | `bar_post_flow` | `0.0` | `0.0` |
| inactive-all caller masked step | `bar_normalized_log_weights` | `0.0` | `0.0` |
| mixed caller masked step | `bar_post_flow` | `5.551115123125783e-16` | `1.7616294983476283e-16` |
| mixed caller masked step | `bar_normalized_log_weights` | `5.551115123125783e-17` | `8.326672684688674e-17` |

## Interpretation

The local transport-adjoint wrapper is not the observed SIR gradient failure by
itself.  Together with Phase 3, this means the two obvious local VJP suspects
are clean under independent float64 CPU algebra:

- RHS/RK4 transition VJP: passed in Phase 3.
- Stopped-scale-key transport VJP wrapper: passed in Phase 4.

The remaining discrepancy must be investigated at a broader boundary:
full-filter score assembly, material GPU/TF32 route behavior, finite-N /
finite-difference noise in the budget-10 diagnostic, or a representation /
parameterization issue that does not reduce to the isolated transition or
transport primitives tested here.

## Decision Table

| Item | Status |
| --- | --- |
| Primary criterion | Passed. |
| Veto diagnostics | No veto. |
| Main uncertainty | Full-route score mismatch remains unresolved. |
| Next justified action | Phase 5 synthesis should classify local transition and transport wrapper bugs as weakened explanations and propose the next discriminating full-route diagnostic. |
| Not concluded | No full SIR score correctness, GPU/TF32 material correctness, or HMC readiness claim. |
