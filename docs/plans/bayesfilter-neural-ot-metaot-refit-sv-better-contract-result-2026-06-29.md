# Experiment result: Meta OT-aligned retained-Sinkhorn SV evaluation under a better evidence contract

## Plan reference
- `docs/plans/bayesfilter-neural-ot-metaot-refit-better-evidence-contract-plan-2026-06-28.md`

## Command actually run
```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_teacher_data_sv_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_low_budget_eval_sv_calibrated_tf
```

## Result summary
- The donor-aligned SV teacher-data artifact regenerated successfully.
- The donor-aligned calibrated SV evaluation completed successfully.
- Decision: `RETAINED_TEACHER_SINKHORN_SV_HELDOUT_LOCAL_USEFULNESS_ON_DISCRIMINATING_BUDGETS`
- The local usefulness signal survives the SV envelope shift at the discriminating primary budget.

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| Initial train loss | `6.141e+00` | Donor-aligned objective starts finite on the SV artifact |
| Final train loss | `-8.417e-01` | Donor-aligned objective improves strongly during training |
| Heldout log_u loss | `5.974e-02` | One-half heldout fit is finite; not a promotion criterion by itself |
| Budget 10 regime | `discriminating` | This remains the calibrated primary SV budget and is still informative |
| Budget 10 student mean RMSE | `6.030e-06` | Better than zero-init on the donor-aligned SV primary rung |
| Budget 10 zero-init mean RMSE | `5.098e-05` | Baseline is not saturated, so this supports a local usefulness claim |
| Budget 10 better-or-equal count | `4/4` | The donor-aligned route wins on all heldout SV examples at the discriminating rung |
| Budget 20 regime | `saturated_zero_init` | Explanatory only; not valid as algorithm-failure evidence |
| Budget 20 student mean RMSE | `6.620e-09` | Student remains near-teacher but does not beat an exact/saturated baseline |
| Budget 20 zero-init mean RMSE | `0.000e+00` | Saturated zero-init baseline |

## Engineering observations
- The SV teacher-data runner was updated to carry the same donor-aligned route metadata as the LGSSM refit artifacts:
  - `meta_ot_refit_target_half = canonical_log_u`
  - `meta_ot_refit_complementary_recovery = teacher_side_sinkhorn_update`
  - `route_family = meta_ot_aligned_fixed_target_retained_sinkhorn_refit`
- The calibrated SV evaluation runner was updated to use:
  - `prediction_head = meta_ot_log_u`
  - `loss_route = meta_ot_log_u_dual_objective_plus_teacher_log_u`
  - explicit discriminating-versus-saturated budget interpretation
- The resulting SV artifact stays semantically aligned with the donor-aligned retained-Sinkhorn refit and no longer inherits the old pair-regression framing.

## Empirical evidence
- The donor-aligned one-half route now shows local usefulness on:
  - expanded LGSSM discriminating budgets,
  - calibrated SV discriminating budget 10.
- The usefulness signal therefore survives at least one nontrivial envelope shift, not just the original LGSSM family.
- The saturated budget-20 rung remains explanatory only and should not be used as a headline failure signal.

## Mathematical claims
- None beyond the already-audited donor-aligned retained-teacher route definition. This result is empirical and contract-framed.

## Decision
- The donor-aligned retained-Sinkhorn route now has local usefulness evidence on:
  - broader LGSSM heldout coverage,
  - and calibrated SV heldout evaluation.
- This strengthens the case that the route is genuinely useful in correction-limited, discriminating regimes rather than only on one narrow artifact family.
- It still does not justify broad success claims, but it materially strengthens the route beyond the earlier “tiny local artifact” interpretation.

## Next step
- The next discriminating test is the harder envelope: range-bearing or another stress slice, keeping the same donor-aligned route and the same “discriminating budgets only” interpretation rule.
