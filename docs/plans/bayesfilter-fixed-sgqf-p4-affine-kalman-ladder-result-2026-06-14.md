# Phase Result: Fixed-SGQF Affine Kalman Ladder

## Plan reference
- `docs/plans/bayesfilter-fixed-sgqf-p4-affine-kalman-ladder-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md`

## Status
- Outcome token: `PASS_P4_FIXED_SGQF_AFFINE_KALMAN_LADDER_READY_FOR_P7`
- Decision class: `pass`

## Command actually run
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_values_tf.py tests/test_fixed_sgqf_verification_tf.py
CUDA_VISIBLE_DEVICES=-1 python - <<'PY'
# focused affine probes for 2D/3D exact-vs-Kalman parity and higher-level failure checks
PY
```

## Run manifest
| Field | Value |
|---|---|
| git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| environment | `anaconda3/envs/tf-gpu` |
| CPU/GPU status | `CPU-only; CUDA_VISIBLE_DEVICES=-1` |
| code surfaces | `tests/test_fixed_sgqf_values_tf.py` |
| plan path | `docs/plans/bayesfilter-fixed-sgqf-p4-affine-kalman-ladder-subplan-2026-06-14.md` |
| result path | `docs/plans/bayesfilter-fixed-sgqf-p4-affine-kalman-ladder-result-2026-06-14.md` |

## Result summary
P4 passed. I extended affine exact-vs-Kalman parity from the existing 1D row to
new 2D and 3D level-2 rows.  Both new rows matched exact Kalman likelihood and
filtered-path outputs to tight numerical tolerance.

A focused 3D level-3 probe did not extend the ladder: the SGQF route blocked at
`carried_covariance`.  That does not invalidate the new level-2 exact rows, but
it does limit the higher-level affine ladder.

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| 2D level-2 log-likelihood error | `1.33e-15` | exact-reference parity within floating-point noise |
| 2D level-2 max filtered-mean error | `8.05e-16` | exact-reference parity |
| 2D level-2 max filtered-covariance error | `1.17e-15` | exact-reference parity |
| 3D level-2 log-likelihood error | `2.66e-15` | exact-reference parity within floating-point noise |
| 3D level-2 max filtered-mean error | `4.30e-16` | exact-reference parity |
| 3D level-2 max filtered-covariance error | `1.17e-15` | exact-reference parity |
| 3D level-3 status | `carried_covariance veto` | higher-level affine extension blocked |

## Engineering observations
- The current fixed-SGQF affine implementation is exact on the tested 2D and 3D
  level-2 rows.
- The main limitation is not the multidimensional affine surface itself; it is
  the higher sparse-level behavior once the cloud changes.

## Empirical evidence
- New 2D and 3D level-2 tests pass against exact Kalman references.
- The exact-reference lane is therefore broader than the original 1D-only
  coverage.

## Mathematical claims
- No new general theorem is claimed.
- On the tested affine Gaussian rows, Kalman remains the exact reference, and
  the fixed-SGQF level-2 implementation matches it numerically.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| pass P4 | satisfied | no same-target or exactness-label veto triggered | higher sparse levels block even on affine rows | use these rows as exact anchors for later comparison phases | no claim that higher levels or nonlinear rows inherit the same exactness |

## Next step
- Continue to P2 and P1, using the new 2D/3D affine rows as exact-reference
  anchors while keeping the higher-level affine extension explicitly blocked.
