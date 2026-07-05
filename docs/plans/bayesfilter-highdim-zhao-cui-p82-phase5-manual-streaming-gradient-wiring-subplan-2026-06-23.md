# P82 Phase 5 Subplan: Manual Streaming Transport-Gradient Wiring

status: DRAFT_READY_FOR_LOCAL_EXECUTION
date: 2026-06-23
phase: P5-MANUAL-STREAMING-WIRING

## Phase Objective

Wire the reviewed manual streaming transport-gradient route through the P82 SIR
d18 benchmark path without running P82 validation.

The only intended behavioral surface is route selection and metadata:

```text
transport_gradient_mode=manual_streaming_finite_sinkhorn_stopped_scale_keys
```

## Entry Conditions

- Manual-adjoint M8 closeout status is
  `MANUAL_ADJOINT_LOCAL_ROUTE_PASSED_P82_WIRING_BLOCKED`.
- P82 FD-only comparator contract remains unchanged.
- Raw/full AD through the whole Sinkhorn transport solve remains forbidden for
  governed `N=10000`.
- No P82 validation or GPU run is authorized in this phase.

## Required Artifacts

- Code diff:
  - `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
  - `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
  - `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`
- Focused tests:
  - `tests/highdim/test_p82_regression_fd_harness_protocol.py`
  - additional route-forwarding coverage where appropriate.
- Phase result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase5-manual-streaming-gradient-wiring-result-2026-06-23.md`
- Updated P82 ledger/stop handoff if present.

## Required Checks / Tests / Reviews

- CPU-hidden parser/metadata tests proving `--transport-gradient-mode` is
  accepted and recorded.
- CPU-hidden route-forwarding test proving the streaming value core forwards
  the requested mode to `batched_annealed_transport_core_tf`.
- `python -m py_compile` for edited Python files.
- `git diff --check` on touched code/tests/plans.
- One-path Claude read-only review of the P5 result.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can P82 select and record the manual streaming transport-gradient route through the SIR d18 benchmark path? |
| Baseline/comparator | Prior P82 path hard-wired `transport_gradient_mode="raw"`; M6 manual route exists in `batched_annealed_transport_core_tf`. |
| Primary criterion | CLI/API wiring and metadata tests pass locally, without launching P82 validation. |
| Veto diagnostics | P82 validation launched; GPU evidence claimed; FD protocol changed; raw full-AD N10000 route reintroduced; route metadata still says `"raw"` when manual route requested; unsupported mode accepted silently. |
| Explanatory diagnostics | Parser choices, forwarded mode captured by test double, metadata field value, and focused test list. |
| Not concluded | No P82 FD agreement, no N10000 feasibility, no GPU/TF32 success, no HMC/default/posterior/scientific-superiority readiness, no Zhao-Cui source-faithfulness. |

## Planned Edits

1. Add `transport_gradient_mode` parameter to
   `streaming_batched_ledh_pfpf_ot_value_core_tf`, defaulting to `"raw"` to
   preserve existing behavior.
2. Forward that parameter into `batched_annealed_transport_core_tf`.
3. Add `--transport-gradient-mode` CLI option to both P8p benchmark entry
   points, defaulting to `"raw"` for backward compatibility.
4. Pass `args.transport_gradient_mode` into the streaming value core call sites.
5. Record `gradient_mode: args.transport_gradient_mode` in output metadata.

## Forbidden Claims / Actions

- Do not run GPU commands.
- Do not run P82 `N=10000` actual gradient.
- Do not run P82 `N=1000` regression FD.
- Do not change the 13-point regression-FD protocol.
- Do not promote this wiring to P82 validation success.
- Do not change defaults.

## Stop Conditions

Stop and write a blocker if:

- route forwarding cannot be tested without GPU/P82 validation;
- the streaming value core cannot safely preserve default `"raw"` behavior;
- tests would require changing P82 FD semantics;
- review finds a material route/metadata mismatch.

## Next-Phase Handoff Conditions

If this phase passes, P82 may plan a tiny trusted GPU smoke in a separate
reviewed subplan.  P82 validation remains blocked until that later smoke passes.
