# Phase Result: Fixed-SGQF Baseline Comparison Ladder

## Plan reference
- `docs/plans/bayesfilter-fixed-sgqf-p7-baseline-comparison-ladder-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md`
- superseding cloud-construction update:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p51-fixed-sgqf-merge-fix-result-2026-06-15.md`

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
| post-fix governing note | `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p51-fixed-sgqf-merge-fix-result-2026-06-15.md` |

## Result summary
P7 passed with explicit eligibility limits.

I built a same-target baseline panel on the scalar quadratic structural fixture:
- dense numerical reference,
- fixed-SGQF,
- UKF,
- cubature.

This panel should now be read as a result about the repaired, source-audited
merged-cloud fixed-SGQF lane. On that selected row, fixed-SGQF matches the
dense reference more closely than UKF or cubature in filtered mean. CUT4 was not
eligible on this 1D row because the current CUT4-G implementation requires
`dim >= 3`.

This remains selected-fixture positioning only. It is not a universal ranking.

## Comparator eligibility table
| Comparator | Eligibility | Reason |
|---|---|---|
| fixed-SGQF | `eligible_same_target` | same structural scalar, same dense reference row, repaired merged-cloud lane |
| UKF | `eligible_same_target` | same structural scalar through sigma-point backend |
| cubature | `eligible_same_target` | same structural scalar through sigma-point backend |
| CUT4 | `blocked_missing_surface` | current CUT4-G rule requires augmented dimension >= 3 on this 1D row |

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| dense filtered mean | `0.2454540` | same-target numerical anchor |
| fixed-SGQF filtered mean error | `< 1e-12` | best match on the tested row |
| UKF filtered mean error | `~9.6e-03` | same-target baseline but less accurate on this row |
| cubature filtered mean error | `~2.34e-01` | same-target baseline but much less accurate on this row |

## Engineering observations
- The baseline panel required no new comparator infrastructure because the repo
  already had same-target sigma-point backends for the structural fixture.
- The repaired cloud matters to interpretation: this panel should now be read as
  evidence about the corrected fixed-SGQF implementation, not about the
  previously corrupted higher-level cloud builder.
- Eligibility still matters: CUT4 is not missing in general, but it is not
  available for this particular low-dimensional row.

## Empirical evidence
- On the tested scalar quadratic row, fixed-SGQF is closer to the dense
  reference than UKF or cubature.
- That local ranking is useful positioning evidence for the repaired fixed-SGQF
  lane on this fixture only.

## Mathematical claims
- No universal ranking theorem.
- No claim that fixed-SGQF dominates those baselines outside the tested row.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| pass P7 with explicit limits | satisfied | no cross-target or hidden-eligibility veto triggered | broader baseline panels and higher-dimensional rows remain open | carry this selected-fixture panel into the final closeout as repaired-lane positioning evidence | no universal ranking or production-default claim |

## Next step
- Keep this panel in the closeout as selected-fixture evidence for the repaired
  merged-cloud implementation only.
