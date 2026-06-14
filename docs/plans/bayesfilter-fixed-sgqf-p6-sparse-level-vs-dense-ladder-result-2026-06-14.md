# Phase Result: Fixed-SGQF Sparse-Level Versus Dense Ladder

## Plan reference
- `docs/plans/bayesfilter-fixed-sgqf-p6-sparse-level-vs-dense-ladder-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md`

## Status
- Outcome token: `PASS_P6_FIXED_SGQF_SPARSE_LEVEL_LADDER_READY_FOR_P8`
- Decision class: `pass_with_recorded_limit`

## Command actually run
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_values_tf.py
CUDA_VISIBLE_DEVICES=-1 python - <<'PY'
# sparse-level probes for the scalar quadratic dense-reference fixture
PY
```

## Run manifest
| Field | Value |
|---|---|
| git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| environment | `anaconda3/envs/tf-gpu` |
| CPU/GPU status | `CPU-only; CUDA_VISIBLE_DEVICES=-1` |
| code surfaces | `tests/test_fixed_sgqf_values_tf.py` |
| plan path | `docs/plans/bayesfilter-fixed-sgqf-p6-sparse-level-vs-dense-ladder-subplan-2026-06-14.md` |
| result path | `docs/plans/bayesfilter-fixed-sgqf-p6-sparse-level-vs-dense-ladder-result-2026-06-14.md` |

## Result summary
P6 passed with a recorded limit.

On the selected scalar quadratic fixture against the same dense numerical
reference:
- level 1 was substantially less accurate than level 2;
- level 2 matched the dense reference essentially exactly on the tested row;
- levels 3-5 did not continue the ladder and instead blocked at
  `carried_covariance`.

This is a local sparse-level ladder.  It is not a general convergence result,
and the non-monotone extension beyond level 2 is itself part of the evidence.

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| level-1 observation-mean error | `> 0.9` | coarse rung is poor on this fixture |
| level-2 observation-mean error | `< 1e-12` | selected-fixture dense-reference match |
| level-3 status | `carried_covariance veto` | ladder does not extend smoothly upward |
| level-4 status | `carried_covariance veto` | same limitation |
| level-5 status | `carried_covariance veto` | same limitation |

## Engineering observations
- This lane does not support a simplistic “higher sparse level is always better”
  story.
- The stable recommendation from the tested fixture is narrower: level 2 is a
  strong local rung, and higher levels may block because of covariance-carriage
  behavior.

## Empirical evidence
- The sparse-level ladder is informative even though it is not monotone beyond
  level 2.
- The phase therefore closes G8 at the selected-fixture scope while preserving a
  recorded higher-level limit.

## Mathematical claims
- No general sparse-level convergence claim.
- Only the tested fixture ladder is supported.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| pass P6 with recorded limit | satisfied | no comparator-mixing or hidden-rung veto triggered | behavior beyond level 2 is blocked on the tested fixture | carry the non-monotone/blocked ladder explicitly into P8 | no theorem that sparse level should improve monotonically or generally |

## Next step
- Continue to P7 and P8, using the level-2 row as the stable dense-reference
  anchor and treating higher levels as an explicit limit rather than a silent
  omission.
