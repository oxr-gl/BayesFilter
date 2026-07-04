# Phase 2 Result: Same-Target LGSSM Score Repair

Date: 2026-07-03

Status: `RETRACTED_TAPE_SCORE_ROUTE_INVALID`

## Decision

Phase 2 is retracted as a valid score-repair implementation.

The runner I added used TensorFlow `GradientTape` to compute the LEDH score.
That is the wrong implementation route for this program.  LEDH score repair is
supposed to use the manual VJP route developed earlier, not automatic
differentiation through the whole filter.

Plainly: using tape-gradient score computation for LEDH was a planning and
implementation error.  The LEDH LGSSM leaderboard score remains blocked.

## Files Removed After Retraction

The invalid tape-gradient runner and its tests were removed:

- `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_score.py`
- `tests/test_ledh_same_target_lgssm_score_runner.py`

## Correct Target

The correct future runner must target:

- row id: `benchmark_lgssm_exact_oracle_m3_T50`;
- `D=3`, `T=50`, dataset seed `81100`;
- theta `[0.72, 0.55, 0.35, 0.35, 0.45]`;
- parameter coordinates `p8d_lgssm_theta=[phi_1,phi_2,phi_3,q_scale,r_scale]`.

The correct score target is:

- total derivative of the executed finite-particle LEDH scalar with fixed
  standard-normal draws, computed by manual VJP.

The exact Kalman score is a comparator only:

```text
[5.655446876369503, -3.83505645148858, 0.3023616684162056,
 -1.9171806685717399, 4.354265155260018]
```

Contract E is not used.

## Checks Run Before Retraction

Static checks on the now-removed invalid runner:

```text
python -m py_compile \
  docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_score.py \
  tests/test_ledh_same_target_lgssm_score_runner.py
```

Result: passed, but this does not rescue the route because the score method was
wrong.

Focused tests on the now-removed invalid runner:

```text
pytest -q tests/test_ledh_same_target_lgssm_score_runner.py
```

Result: `5 passed`, but this only tested metadata around the invalid route.

Eager CPU-hidden tiny diagnostic from the invalid route:

```text
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_score.py \
  --device-scope cpu --device /CPU:0 --expect-device-kind cpu \
  --dtype float64 --tf32-mode disabled --tf-function disabled --xla disabled \
  --time-steps 1 --num-particles 4 --batch-seeds 81120,81121 \
  --sinkhorn-iterations 1 --row-chunk-size 4 --col-chunk-size 4 \
  --particle-chunk-size 4 \
  --output /tmp/ledh_lgssm_score_cpu_eager_smoke.json \
  --markdown-output /tmp/ledh_lgssm_score_cpu_eager_smoke.md
```

Result summary:

```text
status score_diagnostic_not_admitted
finite True
score_shape [2, 5]
score_mean [3.262953491960977, -1.4227587268553914,
            0.3456230133298378, 5.8383903871150515,
            14.276269971620469]
tf_function False jit False
```

Graph CPU-hidden tiny diagnostic from the invalid route:

```text
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_score.py \
  --device-scope cpu --device /CPU:0 --expect-device-kind cpu \
  --dtype float64 --tf32-mode disabled --tf-function enabled --xla disabled \
  --time-steps 1 --num-particles 4 --batch-seeds 81120,81121 \
  --sinkhorn-iterations 1 --row-chunk-size 4 --col-chunk-size 4 \
  --particle-chunk-size 4 \
  --output /tmp/ledh_lgssm_score_cpu_graph_smoke.json \
  --markdown-output /tmp/ledh_lgssm_score_cpu_graph_smoke.md
```

Result: failed at `tape.gradient` inside `tf.function` with TensorFlow
`AssertionError`.

These diagnostics are not LEDH score evidence because they used tape-gradient
score computation.

## Evidence Contract Result

| Field | Status |
| --- | --- |
| Question | Does LEDH compute a total-derivative score for the same LGSSM leaderboard row target? |
| Primary criterion | Not met.  The attempted implementation used tape-gradient score computation, which is forbidden for this LEDH score-repair program. |
| Veto diagnostics | Tape-gradient score route triggered a veto.  No wrong-target or partial-derivative score was admitted. |
| Explanatory diagnostics | The failed attempt showed why the next implementation must be manual VJP only. |
| Not concluded | No leaderboard score admission, no HMC readiness, no GPU/XLA score correctness. |

## Root Cause Classification

The real root cause of this Phase 2 failure is not merely graph/XLA mechanics.
It is that the implementation used the wrong class of method:

- LEDH score computation must use manual VJP.
- Tape-gradient score computation is banned for this repair route.
- The existing SIR GPU/XLA route that passed earlier uses a manual score
  function, which is the model to follow.

Therefore the next repair must implement or adapt a manual LGSSM score route.
It must not try to make the tape-gradient runner work.

## Phase 3 Handoff

Advance to Phase 3 as a manual-VJP repair phase, not a scaling phase.

Phase 3 must:

- keep the same LGSSM row target;
- remove tape-gradient score computation from the LEDH score path;
- implement manual VJP for the same-target LGSSM finite-particle scalar;
- compare manual VJP against exact Kalman and same-scalar finite differences
  on small fixed-randomness diagnostics;
- only then run trusted GPU/XLA smoke.

## Nonclaims

- This does not admit an LEDH LGSSM leaderboard score.
- This does not prove the score agrees with exact Kalman at `T=50`.
- This does not certify GPU/XLA score execution.
- This does not certify HMC readiness.
- This does not repair nonlinear rows.
- The removed tape-gradient runner is not LEDH score evidence.
