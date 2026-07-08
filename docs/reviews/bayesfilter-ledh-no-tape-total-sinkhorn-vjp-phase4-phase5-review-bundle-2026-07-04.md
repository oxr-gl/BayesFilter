# Claude Read-Only Review Bundle: LEDH No-Tape Sinkhorn VJP Phase 4/5 Gate

Date: 2026-07-04

## Role Contract

Codex is supervisor and executor.  Claude is a read-only reviewer only.  Do not
edit files, run commands, launch agents, or authorize crossing scientific,
runtime, product, or human-approval boundaries.

## Review Objective

Review whether Phase 4 can be accepted as a local LGSSM tiny-prefix score
validation while keeping full T50 leaderboard score admission blocked, and
whether the refreshed Phase 5 closeout subplan preserves that boundary.

## Exact Artifacts To Inspect

- Phase 4 result:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-lgssm-score-admission-result-2026-07-04.md`
- Phase 4 JSON:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-lgssm-score-admission-tiny-prefix-2026-07-04.json`
- Phase 5 subplan:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase5-closeout-subplan-2026-07-04.md`
- Code paths:
  `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`
  symbols only:
  - `_manual_value_and_score_from_components`
  - `_manual_score_diagnostic`
  - `_manual_transport_vjp_tf`
  - `_manual_forward_transport_tf`
- Tests:
  `tests/test_ledh_lgssm_manual_score_phase4.py`

## Evidence Contract

Phase 4 question: Does LEDH compute the total derivative of the same LGSSM
LEDH scalar without tape for the fixed tiny prefix fixture?

Phase 4 primary criterion: local prefix route is same-route, same-algorithm,
no-tape, and same-scalar finite-difference pass.

Phase 4 vetoes: tape route; stopped partial derivative used as score;
value/score route mismatch; value/score transport mismatch; nonfinite score;
FD mismatch; full leaderboard score admission from prefix/CPU evidence.

Phase 5 question: Does closeout preserve the exact implemented/validated/
blocked statuses without overclaiming?

## Commands Already Run By Codex

- `python -m py_compile docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py` passed.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_ledh_lgssm_manual_score_phase4.py` passed: 3 tests.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_ledh_lgssm_manual_score_phase4.py tests/test_ledh_pfpf_ot_p7_manual_score.py tests/test_ledh_no_tape_total_sinkhorn_vjp_phase1.py tests/test_ledh_no_tape_total_sinkhorn_vjp_phase2.py` passed: 15 tests.
- `python -m json.tool docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-lgssm-score-admission-tiny-prefix-2026-07-04.json` passed.
- Local content check passed: Phase 4/5 artifacts state full T50 score remains blocked and do not contain `admitted_same_target_manual_total_score`.
- `git diff --check` passed for the touched Phase 4/5 files.

## Key Numerical Evidence

- Tiny prefix time steps: `2`; particles: `4`; seed: `81120`.
- Transport: streaming manual finite total VJP, `transport_ad_mode=full`.
- Same-scalar FD status: `pass`.
- Max absolute score error: `9.465646044759524e-09`.
- Max relative score error: `8.792013654782173e-10`.
- Manual score:
  `[4.6517339713326, -2.2383309550434705, 0.6785225994442738, 8.17939757825367, 10.766186687265593]`.
- Full row admission status: `blocked_material_gate_not_full_gpu_row`.

## Known Limitation

The successful score evidence is CPU-hidden and prefix-only.  It is not full
T50 trusted GPU/XLA material evidence.  It must not be used to admit a full
leaderboard score.

## Review Questions

1. Does Phase 4 avoid claiming more than local tiny-prefix same-scalar score
   validation?
2. Does the new LGSSM score route avoid `GradientTape`/`ForwardAccumulator` in
   the production score helpers under review?
3. Does the result correctly keep the full T50 leaderboard score blocked?
4. Does Phase 5 preserve the correct closeout boundary and nonclaims?
5. Is there any material issue that should block moving to Phase 5?

## Required Verdict Format

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
