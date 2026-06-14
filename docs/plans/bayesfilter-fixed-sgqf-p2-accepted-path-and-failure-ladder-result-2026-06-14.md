# Phase Result: Fixed-SGQF Accepted-Path and Failure Ladder

## Plan reference
- `docs/plans/bayesfilter-fixed-sgqf-p2-accepted-path-and-failure-ladder-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md`

## Status
- Outcome token: `PASS_P2_FIXED_SGQF_ACCEPTED_PATH_AND_FAILURE_LADDER_READY_FOR_P5`
- Decision class: `pass_with_recorded_limit`

## Command actually run
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_values_tf.py tests/test_fixed_sgqf_scores_tf.py tests/test_fixed_sgqf_branch_contract_tf.py tests/test_fixed_sgqf_audit_tf.py tests/test_fixed_sgqf_testing_integration_tf.py
CUDA_VISIBLE_DEVICES=-1 python - <<'PY'
# focused searches for carried-covariance and later-time failures
PY
```

## Run manifest
| Field | Value |
|---|---|
| git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| environment | `anaconda3/envs/tf-gpu` |
| CPU/GPU status | `CPU-only; CUDA_VISIBLE_DEVICES=-1` |
| code surfaces | `tests/test_fixed_sgqf_values_tf.py`, `tests/test_fixed_sgqf_scores_tf.py`, `bayesfilter/nonlinear/fixed_sgqf_tf.py` |
| plan path | `docs/plans/bayesfilter-fixed-sgqf-p2-accepted-path-and-failure-ladder-subplan-2026-06-14.md` |
| result path | `docs/plans/bayesfilter-fixed-sgqf-p2-accepted-path-and-failure-ladder-result-2026-06-14.md` |

## Result summary
P2 passed with a recorded limit.

New evidence now covers:
- clean accepted-path rows beyond the original single scalar one-step fixtures;
- explicit `carried_covariance` failure rows on both value and score paths;
- preservation of branch signature at the carried-covariance failure stage.

However, an attempted search for a deterministic failure with `time_index > 0`
did not find a clean local fixture in the scalar search box.  That subgap is not
closed; it is carried forward as a blocker-style limitation inside the phase
result.

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| accepted-path higher-dimensional evidence | `present` | 2D and 3D affine level-2 rows now pass cleanly |
| carried-covariance value failure row | `present` | level-3 scalar quadratic row blocks at carried covariance |
| carried-covariance score failure row | `present` | score path records same stage and same-branch signature |
| later-time failure search | `not found in scalar search box` | `time_index > 0` row remains open |

## Engineering observations
- A small implementation fix was required: `_symmetrize` in
  `bayesfilter/nonlinear/fixed_sgqf_tf.py` now uses
  `tf.linalg.matrix_transpose(...)` instead of `tf.transpose(...)`.  This makes
  the helper rank-safe for derivative arrays and prevents accidental axis
  reversal when symmetrizing batched covariance-derivative tensors.
- That fix was necessary to support broader score-path execution and not merely
  for test wording.

## Empirical evidence
- `carried_covariance` is now explicitly exercised and preserved in both value
  and score tests.
- No deterministic later-time failure fixture was found in the local two-step
  scalar search grid that preserved the phase’s contract requirements.

## Mathematical claims
- No new mathematical claim.
- This phase establishes contract coverage only: stage naming, failure staging,
  and branch-signature preservation on tested rows.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| pass P2 with recorded limit | satisfied for carried-covariance and accepted-path expansion | no hidden-label or hidden-stage veto triggered | a deterministic later-time failure fixture remains unfound | proceed, but keep the `time_index > 0` failure row listed as still open in P8 | no claim that every stage/time combination is now covered |

## Next step
- Continue to P1 and P3, while keeping the missing later-time deterministic
  failure row on the closeout checklist.
