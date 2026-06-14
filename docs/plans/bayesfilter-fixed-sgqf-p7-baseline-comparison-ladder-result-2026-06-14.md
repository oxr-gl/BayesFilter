# Phase Result: Fixed-SGQF Baseline Comparison Ladder

## Plan reference
- `docs/plans/bayesfilter-fixed-sgqf-p7-baseline-comparison-ladder-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md`

## Status
- Outcome token: `PASS_P7_FIXED_SGQF_BASELINE_COMPARISON_READY_FOR_P8`
- Decision class: `pass_with_explicit_eligibility_limits`

## Command actually run
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_verification_tf.py
CUDA_VISIBLE_DEVICES=-1 python - <<'PY'
# same-target scalar quadratic comparison against dense reference, UKF, and cubature
PY
```

## Run manifest
| Field | Value |
|---|---|
| git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| environment | `anaconda3/envs/tf-gpu` |
| CPU/GPU status | `CPU-only; CUDA_VISIBLE_DEVICES=-1` |
| code surfaces | `tests/test_fixed_sgqf_verification_tf.py` |
| plan path | `docs/plans/bayesfilter-fixed-sgqf-p7-baseline-comparison-ladder-subplan-2026-06-14.md` |
| result path | `docs/plans/bayesfilter-fixed-sgqf-p7-baseline-comparison-ladder-result-2026-06-14.md` |

## Result summary
P7 passed with explicit eligibility limits.

I built a same-target baseline panel on the scalar quadratic structural fixture:
- dense numerical reference,
- fixed-SGQF level 2,
- UKF,
- cubature.

On that selected row, fixed-SGQF level 2 matched the dense reference more
closely than UKF or cubature in filtered mean.  CUT4 was not eligible on this
1D row because the current CUT4-G implementation requires `dim >= 3`.

This is selected-fixture positioning only.  It is not a universal ranking.

## Comparator eligibility table
| Comparator | Eligibility | Reason |
|---|---|---|
| fixed-SGQF level 2 | `eligible_same_target` | same structural scalar, same dense reference row |
| UKF | `eligible_same_target` | same structural scalar through sigma-point backend |
| cubature | `eligible_same_target` | same structural scalar through sigma-point backend |
| CUT4 | `blocked_missing_surface` | current CUT4-G rule requires augmented dimension >= 3 on this 1D row |

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| dense filtered mean | `0.2454540` | same-target numerical anchor |
| SGQF level-2 filtered mean error | `< 1e-12` | best match on the tested row |
| UKF filtered mean error | `~9.6e-03` | same-target baseline but less accurate on this row |
| cubature filtered mean error | `~2.34e-01` | same-target baseline but much less accurate on this row |

## Engineering observations
- The baseline panel required no new comparator infrastructure because the repo
  already had same-target sigma-point backends for the structural fixture.
- Eligibility matters: the CUT4 route is not missing in general, but it is not
  available for this particular low-dimensional row.

## Empirical evidence
- On the tested scalar quadratic row, fixed-SGQF level 2 is closer to the dense
  reference than UKF or cubature.
- That local ranking is useful positioning evidence for this fixture only.

## Mathematical claims
- No universal ranking theorem.
- No claim that fixed-SGQF dominates those baselines outside the tested row.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| pass P7 with explicit limits | satisfied | no cross-target or hidden-eligibility veto triggered | broader baseline panels and higher-dimensional rows remain open | carry this selected-fixture panel into P8 as local positioning evidence | no universal ranking or production-default claim |

## Next step
- Continue to P8 and classify this panel explicitly as selected-fixture,
  same-target baseline evidence only.
