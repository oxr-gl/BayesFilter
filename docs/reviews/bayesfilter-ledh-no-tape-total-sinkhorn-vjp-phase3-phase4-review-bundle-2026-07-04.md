# Claude Read-Only Review Bundle: LEDH No-Tape Sinkhorn VJP Phase 3/4 Gate

Date: 2026-07-04

## Role Contract

Codex is supervisor and executor.  Claude is a read-only reviewer only.  Do not
edit files, run commands, launch agents, or authorize crossing scientific,
runtime, product, or human-approval boundaries.

## Review Objective

Review whether Phase 3 can be accepted as scoped P8p SIR regression integration
and whether the refreshed Phase 4 subplan is adequate for LGSSM same-target
score admission.

## Exact Artifacts To Inspect

- Phase 3 result:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-p8p-sir-regression-result-2026-07-04.md`
- Phase 3 JSON:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-p8p-sir-regression-2026-07-04.json`
- Phase 4 subplan:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-lgssm-score-admission-subplan-2026-07-04.md`
- Code paths:
  `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
  symbol only: `_manual_transport_vjp_tf`
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
  symbols only:
  - `_filterflow_manual_streaming_finite_transport_total_pullback`
  - `_filterflow_manual_streaming_finite_transport_total_vjp`
- Tests:
  `tests/test_ledh_pfpf_ot_p7_manual_score.py`

## Evidence Contract

Phase 3 question: Does the no-tape primitive preserve the scoped P8p SIR
total-derivative behavior?

Phase 3 primary criterion: P8p same-scalar total-derivative checks pass with
route metadata proving no-tape total VJP use.

Phase 3 vetoes: P8p route falls back to tape; stopped partial derivative used
as score; value/score algorithm mismatch; scoped diagnostic promoted to full
leaderboard row; same-scalar check fails.

Phase 4 question: Does LEDH compute the total derivative of the same LGSSM
leaderboard scalar without tape?

Phase 4 must separately prove same-route/no-tape LGSSM score admission with
exact Kalman or same-scalar FD comparison and must not reuse scoped P8p evidence
as LGSSM score evidence.

## Commands Already Run By Codex

- `python -m py_compile ...` passed for edited Python files.
- Focused P8p full/stabilized no-autodiff sentinel and tiny autodiff tests
  passed.
- Phase 1/2 no-tape primitive tests still passed.
- Existing P8p manual scan baseline/reference checks passed.
- Static AST/source check found no `GradientTape`, `ForwardAccumulator`, or
  `.gradient(` in `_manual_transport_vjp_tf`,
  `_filterflow_manual_streaming_finite_transport_total_pullback`, and
  `_filterflow_manual_streaming_finite_transport_total_vjp`.
- Phase 3 JSON generation passed.
- `git diff --check` passed for edited Phase 3 files/artifacts.

## Key Numerical Evidence

- Tiny P8p full-mode max log-likelihood gap versus raw autodiff: `0.0`.
- Tiny P8p full-mode max gradient gap versus raw autodiff:
  `7.62939453125e-06`.
- Predeclared tolerance: `1.0e-05`.
- Full-mode runtime no-autodiff sentinel test passed.

## Review Questions

1. Does Phase 3 avoid claiming more than scoped P8p regression?
2. Does the P8p full-mode route now avoid local tape in the score path?
3. Is the tiny autodiff comparison plus runtime sentinel adequate for Phase 3
   handoff, given that Phase 4 remains a separate LGSSM gate?
4. Does the Phase 4 subplan require same-route, same-algorithm, no-tape, and
   exact/FD evidence before LGSSM score admission?
5. Is there any material issue that should block moving to Phase 4?

## Required Verdict Format

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```

