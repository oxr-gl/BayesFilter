# Phase Result: Fixed-SGQF Cloud Exactness Ladder

## Plan reference
- `docs/plans/bayesfilter-fixed-sgqf-p3-cloud-exactness-ladder-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md`
- superseding cloud-construction update:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p51-fixed-sgqf-merge-fix-result-2026-06-15.md`

## Status
- Outcome token: `PASS_P3_FIXED_SGQF_CLOUD_EXACTNESS_READY_FOR_P6_P7`
- Decision class: `pass`

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
| code surfaces | `tests/test_fixed_sgqf_tf.py`, `bayesfilter/nonlinear/fixed_sgqf_tf.py` |
| plan path | `docs/plans/bayesfilter-fixed-sgqf-p3-cloud-exactness-ladder-subplan-2026-06-14.md` |
| result path | `docs/plans/bayesfilter-fixed-sgqf-p3-cloud-exactness-ladder-result-2026-06-14.md` |
| post-fix governing note | `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p51-fixed-sgqf-merge-fix-result-2026-06-15.md` |

## Result summary
P3 passed.

This result is revised by the post-fix merged-cloud audit and rerun. The earlier
pre-fix interpretation that the 2D level-3 cloud was a local covariance-limit
row is now superseded: that mismatch was caused by the higher-level merge bug.

Current construction evidence now covers:
- 2D level-2 covariance and selected moment rows;
- 3D level-2 preview cloud and signed-coefficient structure;
- 4D level-2 covariance recovery;
- 1D level-3/4/5 higher-order GHQ point-count preservation;
- 2D level-3 Jia-consistent 17-point cloud with correct covariance behavior.

This is still tested-moment and tested-cloud evidence, not an all-level or
all-moment theorem.

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| 2D level-2 point count | `5` | small nontrivial cloud rung |
| 2D level-2 max covariance error | `< 1e-12` | covariance exactness on tested row |
| 2D level-2 x^4 moment | `3.0` | matches standard-normal target on tested coordinate row |
| 2D level-2 x^2 y^2 moment | `0.0` | selected mixed-moment behavior recorded explicitly |
| 4D level-2 point count | `9` | higher-dimensional level-2 rung covered |
| 4D level-2 max covariance error | `< 1e-12` | covariance exactness on tested row |
| 1D level-3 / 4 / 5 point counts | `5 / 7 / 9` | repaired higher-level GHQ clouds no longer collapse |
| 2D level-3 point count | `17` | Jia-consistent higher-level cloud restored |
| 2D level-3 covariance error | `~0` | pre-fix `~0.4` mismatch was a merge-bug artifact |

## Engineering observations
- The repaired cloud builder now preserves distinct higher-level GHQ nodes and
  only merges nodes that actually satisfy the declared sup-norm tolerance.
- The most important change in interpretation is negative: the earlier 2D
  level-3 covariance mismatch should no longer be treated as evidence of an
  intrinsic SGQF limit on that tested row.
- Cloud evidence is still best described by tested point-count/moment/covariance
  rows rather than by a blanket exactness slogan.

## Empirical evidence
- The higher-level cloud collapse bug was real and is now repaired.
- 2D level-3 cloud behavior now matches the Jia-style construction on the tested
  row instead of the old collapsed 9-point artifact.
- G3 is therefore closed at the tested-cloud scope of this program.

## Mathematical claims
- No all-moment theorem is claimed.
- Only the named tested point-count, moment, and covariance rows are supported.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| pass P3 | satisfied | no overclaiming veto triggered | broader higher-level clouds beyond the tested rows still need case-specific evidence | use the repaired level-2 and level-3 cloud rows as the current construction anchor | no blanket claim for all dimensions, all moments, or all higher levels |

## Next step
- Use the repaired cloud ladder as the construction anchor for later fixed-SGQF
  interpretation, and treat the old pre-fix 2D level-3 mismatch as superseded by
  the merge-fix rerun.
