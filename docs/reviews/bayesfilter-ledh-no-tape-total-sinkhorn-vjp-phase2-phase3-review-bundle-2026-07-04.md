# Claude Read-Only Review Bundle: LEDH No-Tape Sinkhorn VJP Phase 2/3 Gate

Date: 2026-07-04

## Role Contract

Codex is supervisor and executor.  Claude is a read-only reviewer only.  Do not
edit files, run commands, launch agents, or authorize crossing scientific,
runtime, product, or human-approval boundaries.

## Review Objective

Review whether Phase 2 can be accepted as primitive correctness validation on
the tiny same-scalar fixture, and whether the refreshed Phase 3 subplan is
adequate for P8p SIR regression integration.

## Exact Artifacts To Inspect

- Phase 2 result:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-primitive-validation-result-2026-07-04.md`
- Phase 2 validation JSON:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-primitive-validation-2026-07-04.json`
- Phase 3 subplan:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-p8p-sir-regression-subplan-2026-07-04.md`
- Test:
  `tests/test_ledh_no_tape_total_sinkhorn_vjp_phase2.py`
- Code symbols only:
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
  - `_filterflow_manual_streaming_finite_transport_value_total_vjp`
  - `_filterflow_manual_streaming_finite_transport_total_vjp`
  - `_filterflow_manual_streaming_finite_transport_stopped_scale_keys`

## Evidence Contract

Phase 2 question: Does the no-tape primitive compute the same total VJP as the
finite transport scalar?

Phase 2 primary criterion: candidate VJP matches raw tape and central finite
differences within predeclared tiny-tensor tolerances for `scaled_x`,
`particles`, `logw`, and `epsilon0`.

Phase 2 vetoes: candidate matches stopped route but not total route; FD mismatch
beyond tolerance; nonfinite cotangent; tape found in production helper; wrong
scalar; tolerance changed after seeing failures.

Phase 3 question: Does the no-tape primitive preserve the scoped P8p SIR
same-scalar total-derivative behavior?

Phase 3 must prove the P8p value and score use the same transport algorithm and
must not use stopped partial derivatives as scores.

## Commands Already Run By Codex

- `python -m py_compile tests/test_ledh_no_tape_total_sinkhorn_vjp_phase2.py`
  passed.
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ledh_no_tape_total_sinkhorn_vjp_phase2.py`
  passed: 2 tests.
- `PYTHONPATH=/home/chakwong/BayesFilter CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python tests/test_ledh_no_tape_total_sinkhorn_vjp_phase2.py > docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-primitive-validation-2026-07-04.json`
  passed.
- `python -m json.tool docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-primitive-validation-2026-07-04.json`
  passed.
- `git diff --check -- tests/test_ledh_no_tape_total_sinkhorn_vjp_phase2.py docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-primitive-validation-2026-07-04.json`
  passed.

## Key Numerical Evidence

- same-scalar value gap: `0.0`;
- maximum tape parity error: `5.204170427930421e-18`;
- maximum FD directional error: `2.5253430770906966e-13`;
- maximum stopped-route gap versus total tape: `0.002199091916697652`;
- total `epsilon0` tape gradient: `4.113532015233492e-05`;
- no-tape custom `epsilon0` gradient: `4.113532015233463e-05`;
- stopped-route `epsilon0` gradient: `0.0`.

## Review Questions

1. Does Phase 2 compare the no-tape candidate to the same finite scalar rather
   than to the stopped partial derivative?
2. Are the tolerances and negative stopped-route check adequate for a tiny
   primitive validation gate?
3. Does Phase 2 avoid overclaiming downstream score, GPU/XLA, or HMC readiness?
4. Does the Phase 3 subplan carry the correct next boundary: P8p same-scalar
   route regression with value/score algorithm identity and no stopped partial
   derivative as score?
5. Is there any material issue that should block moving to Phase 3?

## Required Verdict Format

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
