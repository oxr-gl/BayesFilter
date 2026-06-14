# Phase Result: Fixed-SGQF Cloud Exactness Ladder

## Plan reference
- `docs/plans/bayesfilter-fixed-sgqf-p3-cloud-exactness-ladder-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md`

## Status
- Outcome token: `PASS_P3_FIXED_SGQF_CLOUD_EXACTNESS_READY_FOR_P6_P7`
- Decision class: `pass_with_recorded_limit`

## Command actually run
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_tf.py
CUDA_VISIBLE_DEVICES=-1 python - <<'PY'
# direct cloud-moment probes for (2,2), (2,3), and (4,2)
PY
```

## Run manifest
| Field | Value |
|---|---|
| git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| environment | `anaconda3/envs/tf-gpu` |
| CPU/GPU status | `CPU-only; CUDA_VISIBLE_DEVICES=-1` |
| code surfaces | `tests/test_fixed_sgqf_tf.py` |
| plan path | `docs/plans/bayesfilter-fixed-sgqf-p3-cloud-exactness-ladder-subplan-2026-06-14.md` |
| result path | `docs/plans/bayesfilter-fixed-sgqf-p3-cloud-exactness-ladder-result-2026-06-14.md` |

## Result summary
P3 passed with a recorded limit.

New construction evidence now covers:
- 2D level-2 covariance and selected moment rows;
- 4D level-2 covariance recovery;
- the existing 3D level-2 preview remains intact.

A direct 2D level-3 probe was informative but not promotable as a covariance
exactness row: it preserved centering but produced a covariance mismatch around
`0.4` relative to the identity target.  That row is recorded as a limitation,
not as a passing exactness extension.

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| 2D level-2 point count | `5` | small nontrivial cloud rung |
| 2D level-2 max covariance error | `< 1e-12` | covariance exactness on tested row |
| 2D level-2 x^4 moment | `3.0` | matches standard-normal target on tested coordinate row |
| 2D level-2 x^2 y^2 moment | `0.0` | selected mixed-moment behavior recorded explicitly |
| 4D level-2 point count | `9` | higher-dimensional level-2 rung covered |
| 4D level-2 max covariance error | `< 1e-12` | covariance exactness on tested row |
| 2D level-3 max covariance error | `~0.4` | not promotable as covariance-exactness extension |

## Engineering observations
- The cloud ladder is better described by tested moment rows than by generic
  “exactness” language.
- Level-2 rows are robust across the newly tested dimensions, but the simple
  level-3 2D extension is not a monotone improvement in the covariance target.

## Empirical evidence
- New level-2 moment/covariance rows passed in 2D and 4D.
- The attempted 2D level-3 covariance extension did not pass and should remain a
  recorded limit.

## Mathematical claims
- No all-moment theorem is claimed.
- Only the named tested moments and covariance rows are supported.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| pass P3 with recorded limit | satisfied for tested level-2 rows | no overclaiming veto triggered | higher-level cloud behavior is not uniformly better on the tested 2D row | use level-2 cloud rows as the stable construction anchor for later phases | no blanket claim for all dimensions, all moments, or all higher levels |

## Next step
- Continue to P5 and P6, using level-2 cloud evidence as the stable anchor and
  keeping the 2D level-3 covariance mismatch listed as a limitation.
