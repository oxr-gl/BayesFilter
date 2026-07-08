# Phase 4 Subplan: Transport Adjoint And Stopped-Scale-Key Audit

Date: 2026-07-01

Status: `REFRESHED_AFTER_PHASE3_PENDING_REVIEW`

## Phase Objective

Audit the manual transport reverse wrapper used by the P8p SIR score route
against TensorFlow autodiff of the same stopped-scale-key forward transport on
tiny fixed tensors before returning to material GPU/TF32 SIR score evidence.

## Entry Conditions Inherited From Previous Phase

- Phase 1 ruled out scalar-to-regional kappa aggregation failure.
- Phase 2 localized the largest mismatch to regional infection-vs-recovery
  (`rho`) and secondary common-rate (`tau`) directions.
- Phase 3 passed the RHS/RK4 transition-only VJP audit at machine precision.
- Because Phase 3 passed, a local transition derivative bug is no longer the
  next smallest explanation.
- Transport-adjoint and stopped-scale-key routes remain live alternatives.

## Required Artifacts

- Transport adjoint diagnostic:
  `docs/benchmarks/diagnose_p8p_sir_transport_adjoint_vjp.py`
- Unit/smoke tests:
  `tests/test_p8p_sir_transport_adjoint_vjp.py`
- Phase 4 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase4-transport-adjoint-result-2026-07-01.md`
- Optional JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase4-transport-adjoint-2026-07-01.json`

## Required Checks, Tests, Reviews

- Compare `p8p._manual_transport_vjp_tf` against TensorFlow autodiff of a
  matching stopped-scale-key forward wrapper that uses the exact
  non-custom-gradient comparator helper
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py::_filterflow_manual_streaming_finite_transport_value_stopped_scale_keys`.
- The comparator wrapper must reproduce the P8p stopped-center/stopped-scale
  normalization, stopped `epsilon0`, uniform-log-weight reset, active/inactive
  mask semantics, and scalar epsilon/finite Sinkhorn step count.
- The diagnostic must record and assert that the autodiff comparator path does
  not call
  `annealed_transport_tf._filterflow_manual_streaming_finite_transport_stopped_scale_keys`
  or
  `annealed_transport_tf._filterflow_manual_streaming_blockwise_vjp_finite_transport_stopped_scale_keys`,
  because those are custom-gradient routes being tested rather than the
  comparator.
- Cover active-all, inactive-all, and mixed masks.
- Cover `post_flow` and `normalized_log_weights` cotangents.
- Syntax/compile checks for touched files.
- Run this local check on CPU only; record it as transport algebra evidence,
  not material GPU/TF32 SIR evidence.
- Claude read-only review for the refreshed Phase 4 subplan before execution.
- Claude read-only review for any result that changes the root-cause target.

Exact local command templates:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/diagnose_p8p_sir_transport_adjoint_vjp.py
pytest -q tests/test_p8p_sir_transport_adjoint_vjp.py
```

Exact diagnostic command:

```bash
python docs/benchmarks/diagnose_p8p_sir_transport_adjoint_vjp.py --output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase4-transport-adjoint-2026-07-01.json
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the P8p manual transport VJP wrapper match autodiff for the same stopped-scale-key forward transport before full-filter score assembly? |
| Baseline/comparator | TensorFlow autodiff of identical fixed tensors through `annealed_transport_tf._filterflow_manual_streaming_finite_transport_value_stopped_scale_keys` in float64 CPU algebra, wrapped only to reproduce P8p stopped center/scale, stopped `epsilon0`, mask, and uniform reset semantics. |
| Primary pass criterion | For each mask case and each checked tensor family (`bar_post_flow`, `bar_normalized_log_weights`), manual VJP vs autodiff comparator must satisfy max absolute residual `<= 1.0e-8` and relative L2 residual `<= 1.0e-7`, denominator `max(norm(comparator), 1.0)`. If this fails, localize the mismatch to active mask handling, inactive mask handling, scaled-particle cotangent, particle cotangent, log-weight cotangent, or classify it as `diffuse_transport_mismatch` without repair. |
| Veto diagnostics | Comparator uses `_filterflow_manual_streaming_finite_transport_stopped_scale_keys`, `_filterflow_manual_streaming_blockwise_vjp_finite_transport_stopped_scale_keys`, or any route with a custom transport gradient; missing inactive/mixed mask case; CPU result claimed as material GPU/TF32 SIR evidence; unsupported full-filter correctness claim. |
| Explanatory diagnostics | Per-mask residual table, value parity, tensor devices, route names. |
| Not concluded | Full SIR score correctness, GPU/TF32 runtime correctness, HMC readiness, or that non-centered process noise is irrelevant. |

## Forbidden Claims And Actions

- Do not use the custom-gradient transport wrapper as the autodiff comparator.
- Do not infer full filter score correctness from local transport agreement.
- Do not run CPU-only material SIR comparisons.
- Do not change production transport semantics.
- Do not claim non-centered/process-noise representation has been ruled out.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 synthesis if:

- Phase 4 transport adjoint passes and the result explicitly preserves
  full-filter score-assembly and non-centered/process-noise routes as possible
  residual explanations; or
- Phase 4 fails and localizes the mismatch to a named transport wrapper term,
  in which case Phase 5 must classify this as an implementation repair target
  rather than a production reparameterization result.
- Phase 4 fails with a clean independent comparator but does not localize
  confidently; then write the result as `diffuse_transport_mismatch`, do not
  patch production code, and draft Phase 5 as a blocker/synthesis step that
  proposes the next smallest localizing diagnostic.

Draft a repair subplan instead of advancing if:

- The comparator cannot avoid the custom-gradient path.
- The failure is local but the repair would change production transport
  semantics.

## Stop Conditions

- The non-custom-gradient stopped-scale-key comparator cannot be made
  semantically identical to the manual route.
- The comparator is clean and residuals fail, but the diagnostic cannot
  distinguish a localized transport-wrapper term from a broader assembly issue;
  in that case stop Phase 4 with `diffuse_transport_mismatch`.
- The same Claude review blocker does not converge after five rounds.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write Phase 4 result / close record.
3. Draft or refresh Phase 5 subplan.
4. Review Phase 5 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
