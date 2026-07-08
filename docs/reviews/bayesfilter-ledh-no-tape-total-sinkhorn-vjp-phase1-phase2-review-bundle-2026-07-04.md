# Claude Read-Only Review Bundle: LEDH No-Tape Sinkhorn VJP Phase 1/2 Gate

Date: 2026-07-04

## Role Contract

Codex is supervisor and executor.  Claude is a read-only reviewer only.  Do not
edit files, run commands, launch agents, or authorize crossing scientific,
runtime, product, or human-approval boundaries.

## Review Objective

Review whether Phase 1 can be accepted as a local implementation-existence
gate, and whether the refreshed Phase 2 subplan is adequate for primitive
correctness validation.

## Exact Artifacts To Inspect

- Phase 1 result:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase1-primitive-implementation-result-2026-07-04.md`
- Phase 2 subplan:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-primitive-validation-subplan-2026-07-04.md`
- Code paths:
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
  symbols only:
  - `_filterflow_streaming_softmin_vjp`
  - `_match_epsilon_cotangent_shape`
  - `_filterflow_streaming_finite_sinkhorn_potentials_vjp_total`
  - `_filterflow_manual_streaming_finite_transport_total_vjp`
- Tests:
  `tests/test_ledh_no_tape_total_sinkhorn_vjp_phase1.py`
  `tests/test_audit_ledh_clean_xla.py`

## Evidence Contract

Phase 1 question: Does the repository contain a candidate no-tape total
transport VJP implementation?

Phase 1 primary criterion: candidate compiles, has no tape or
forward-accumulator in the production helper, returns finite primitive
cotangents on tiny tensors, and has an explicit `epsilon0` total cotangent path.

Phase 1 nonclaims: no tape/FD parity, no P8p/LGSSM score admission, no GPU/XLA
claim, no HMC readiness.

Phase 2 question: Does the no-tape primitive compute the same total VJP as the
finite transport scalar?

Phase 2 must compare candidate VJP to the same finite scalar using tape and
finite differences on tiny tensors with predeclared tolerances.

## Commands Already Run By Codex

- `python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_no_tape_total_sinkhorn_vjp_phase1.py tests/test_audit_ledh_clean_xla.py` passed.
- Static source check found no `GradientTape`, `ForwardAccumulator`, or
  `.gradient(` in `_filterflow_manual_streaming_finite_transport_total_vjp` or
  `_filterflow_streaming_finite_sinkhorn_potentials_vjp_total`.
- `git diff --check` passed.
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ledh_no_tape_total_sinkhorn_vjp_phase1.py tests/test_audit_ledh_clean_xla.py::test_default_clean_xla_audit_reports_current_route_unclean_with_line_anchors tests/test_audit_ledh_clean_xla.py::test_phase5_sinkhorn_target_helpers_have_no_python_step_loop_or_state_list`
  passed: 6 tests.
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -k "streaming_softmin_vjp or streaming_transport_from_potentials_vjp"`
  passed: 5 tests.
- `CUDA_VISIBLE_DEVICES=-1 python scripts/audit_ledh_clean_xla.py` still reports
  `FAIL_CURRENT_ROUTE` because stopped-key helpers remain current vetoes; the
  old total-helper tape warning is absent.

## Review Questions

1. Does Phase 1 result avoid claiming correctness beyond implementation
   existence?
2. Do the named implementation symbols remove the local tape from the total
   production helper and include an explicit `epsilon0` cotangent path?
3. Does the Phase 2 subplan require the right next evidence: same-scalar tape
   parity, finite differences, fixed tolerances, and a negative stopped-route
   check?
4. Is there any material issue that should block moving to Phase 2?

## Required Verdict Format

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
