# Phase Result: Fixed-SGQF Multistep Dense-Reference Ladder

## Plan reference
- `docs/plans/bayesfilter-fixed-sgqf-p1-multistep-dense-reference-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md`
- superseding cloud-construction update:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p51-fixed-sgqf-merge-fix-result-2026-06-15.md`

## Status
- Outcome token: `PASS_P1_FIXED_SGQF_MULTISTEP_DENSE_REFERENCE_READY_FOR_P3_P5_P6`
- Decision class: `pass`

## Command actually run
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_values_tf.py tests/test_fixed_sgqf_verification_tf.py
CUDA_VISIBLE_DEVICES=-1 python - <<'PY'
# recursive dense-reference probe for the scalar quadratic fixture over three observations
PY
```

## Run manifest
| Field | Value |
|---|---|
| git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| environment | `anaconda3/envs/tf-gpu` |
| CPU/GPU status | `CPU-only; CUDA_VISIBLE_DEVICES=-1` |
| code surfaces | `tests/test_fixed_sgqf_values_tf.py` |
| plan path | `docs/plans/bayesfilter-fixed-sgqf-p1-multistep-dense-reference-subplan-2026-06-14.md` |
| result path | `docs/plans/bayesfilter-fixed-sgqf-p1-multistep-dense-reference-result-2026-06-14.md` |
| post-fix governing note | `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p51-fixed-sgqf-merge-fix-result-2026-06-15.md` |

## Result summary
P1 passed.

I extended the scalar quadratic dense-reference evidence from one step to a
three-step recursive ladder. On the chosen 1D nonlinear fixture, fixed-SGQF
matches the recursively updated dense numerical reference in total log
likelihood, filtered means, and filtered covariances to floating-point
precision.

This result should now be read through the repaired merged-cloud lane described
in the p51 merge-fix result. The old pre-fix interpretation already established
a strong level-2 row; the post-fix state strengthens the reading by showing that
higher-level cloud corruption was not contaminating this dense-reference lane.

This remains local dense-reference evidence on a selected low-dimensional
fixture. It is not a general nonlinear exactness claim.

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| horizon | `3` | multistep evidence extends beyond one-step only |
| total dense-reference log-likelihood mismatch | `< 1e-10` | selected-fixture agreement is numerically exact at this rung |
| max filtered-mean mismatch | `< 1e-10` | selected-fixture agreement |
| max filtered-covariance mismatch | `< 1e-10` | selected-fixture agreement |
| dense-reference class | `dense_numerical_reference` | comparator remains numerical, not analytic truth |
| current cloud lane status | `repaired and audited` | multistep reading is conditioned on the repaired merged-cloud implementation |

## Engineering observations
- The recursive dense-reference ladder could be built without adding a new
  reference helper by iterating the current one-step dense projection surface.
- The governing interpretation is now explicitly tied to the repaired
  merged-cloud implementation rather than to an underspecified pre-fix lane.
- This selected scalar quadratic row remains unusually favorable and should not
  be promoted into a broader nonlinear-exactness story.

## Empirical evidence
- Three-step scalar quadratic fixed-SGQF and recursive dense reference agree to
  floating-point tolerance on the tested row.
- After the merge fix, the lane remains coherent and this row should be read as a
  result of the repaired, source-audited cloud implementation.
- G1 is therefore closed at the selected 1D fixture scope.

## Mathematical claims
- No general nonlinear exactness claim.
- Only the selected fixture/horizon row is certified by this phase.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| pass P1 | satisfied | no same-target or exactness-label veto triggered | agreement may not transfer to higher dimension or harder nonlinear rows | use this row as a dense-reference anchor under the repaired merged-cloud lane | no claim beyond the tested 1D fixture/horizon |

## Next step
- Continue to later phases using this row as dense-reference evidence for the
  repaired fixed-SGQF lane, not as a cloud-agnostic SGQF theorem.
