# Claude Read-Only Review Bundle

Date: 2026-07-03
Review name: `bayesfilter-ledh-leaderboard-score-repair-phase3-closeout`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

READ-ONLY REVIEW ONLY.  Do not edit files, run commands, launch agents, or
change state.

Claude is not execution authority and cannot approve scientific-claim,
runtime, GPU, model-file, product, funding, or human-boundary crossings.

## Objective

Review the Phase 3 closeout decision for the LEDH leaderboard score-repair
runbook.

The closeout says the same-target LGSSM LEDH score is still blocked.  It does
not admit an LEDH score row.  The exact blocker token is
`blocked_total_transport_vjp_needs_no_tape_repair`.

## Artifacts To Inspect

Inspect only these bounded local paths:

- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase3-memory-safe-gpu-xla-score-result-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase4-fixed-sir-score-target-subplan-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-visible-execution-ledger-2026-07-03.md`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py`

Relevant line anchors recorded in the result:

- dense public value+score wrapper opens `tf.GradientTape` at
  `experimental_batched_ledh_pfpf_ot_tf.py:1762`;
- streaming public value+score wrapper opens `tf.GradientTape` at
  `experimental_batched_ledh_pfpf_ot_streaming_tf.py:691`;
- closest no-tape LGSSM route uses stopped transport center/scale/epsilon0 and
  stopped-scale/key transport primitives in
  `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py:165-250`;
- total transport helper opens `tf.GradientTape` inside its custom-gradient
  body in `annealed_transport_tf.py:2393`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is Phase 3 correct to block LGSSM LEDH score admission rather than proceed to a GPU/XLA score run? |
| Baseline/comparator | Phase 3 rules: same-target total derivative, no `GradientTape`, no `ForwardAccumulator`, same scalar value/score route. |
| Primary criterion | If current code lacks a route satisfying both total derivative and no-tape/manual VJP, the result must block score admission. |
| Veto diagnostics | Any admitted LEDH score row, any claim that stopped-scale/key derivative is the unstopped total derivative, any claim that `GradientTape` total transport route is allowed, any Phase 4 text that assumes LGSSM score is solved. |
| Explanatory diagnostics | Whether the next repair target is well named and bounded. |
| Not concluded | Code implementation correctness for a future repair, GPU feasibility, HMC readiness, nonlinear score readiness. |

## Pass Criteria

Return `VERDICT: AGREE` only if all are true:

- Phase 3 result does not admit an LEDH score row.
- The result plainly says stopped-scale/key derivative is not the total
  derivative of the unstopped leaderboard scalar.
- The result plainly says the current total-transport helper is blocked because
  it uses `GradientTape`.
- The result identifies the next required repair as no-tape total VJP for
  finite streaming Sinkhorn transport.
- Phase 4 subplan preserves the Phase 3 LGSSM blocker and does not claim any
  LEDH `executed_value_score` row.

Return `VERDICT: REVISE` if any item fails.

## Required Output

Findings first, concise.  End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
