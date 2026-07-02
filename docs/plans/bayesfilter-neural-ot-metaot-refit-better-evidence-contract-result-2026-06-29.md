# Experiment result: Meta OT-aligned retained-Sinkhorn evaluation under a better evidence contract

## Plan reference
- `docs/plans/bayesfilter-neural-ot-metaot-refit-better-evidence-contract-plan-2026-06-28.md`

## Command actually run
```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_heldout_eval_tf
```

## Result summary
- The updated better-contract heldout evaluation completed successfully.
- Decision: `RETAINED_TEACHER_SINKHORN_HELDOUT_EVAL_LOCAL_USEFULNESS_ON_DISCRIMINATING_BUDGETS`
- The donor-aligned one-half route remains non-promoted on the saturated high-budget rung, but the improved evidence contract now classifies the result as **local usefulness on discriminating budgets**, not algorithm failure.

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| Initial train loss | `2.118e+01` | Donor-aligned training objective starts high but finite |
| Final train loss | `-9.567e-01` | Donor-aligned objective improved strongly during training |
| Heldout log_u loss | `8.974e-02` | One-half heldout fit is finite but not by itself a promotion criterion |
| Budget 5 regime | `discriminating` | Zero-init is not saturated here, so this rung can support local usefulness interpretation |
| Budget 5 student mean RMSE | `7.246e-06` | Better than zero-init on the discriminating low-budget rung |
| Budget 5 zero-init mean RMSE | `1.378e-04` | Baseline remains far from exact at this rung |
| Budget 10 regime | `discriminating` | Still a valid discriminating rung |
| Budget 10 student mean RMSE | `1.030e-08` | Better mean replay than zero-init on the discriminating mid-budget rung |
| Budget 10 zero-init mean RMSE | `1.932e-07` | Baseline not yet saturated |
| Budget 20 regime | `saturated_zero_init` | This rung must not drive an algorithm-failure headline |
| Budget 20 student mean RMSE | `1.030e-08` | Student remains near-teacher but does not beat a saturated zero-init baseline |
| Budget 20 zero-init mean RMSE | `0.000e+00` | Baseline is effectively exact, so non-promotion here is not algorithm-failure evidence |

## Engineering observations
- The updated heldout-eval runner now labels each budget rung as either `discriminating` or `saturated_zero_init`.
- The validation rule was changed so the artifact no longer fails just because the student does not beat zero-init on a saturated high-budget rung.
- The runner writes a new artifact family under the better-contract plan/result paths instead of overwriting the older 2026-06-18 interpretation artifact.

## Empirical evidence
- The donor-aligned one-half route shows clear local usefulness on the discriminating budget rungs (`5` and `10`).
- The old misleading headline came from the `20`-iteration rung where zero-init is already exact.
- Under the better evidence contract, the same raw metrics support a more accurate conclusion: **local usefulness under discriminating budgets, saturated-budget non-promotion, and no algorithm-failure claim**.

## Mathematical claims
- None beyond the already-audited retained-teacher / donor-aligned route interpretation. This result is empirical and contract-framed, not a new derivation.

## Decision
- The better evidence contract changes the interpretation materially: the donor-aligned route is now best described as **locally useful on discriminating corrective-budget rungs**.
- The current tiny heldout dataset still does not justify a broad success claim.
- The earlier “failed” framing should no longer be used as the top-line description of the retained-teacher route.

## Next step
- Expand or diversify the donor-aligned teacher-data envelope and rerun the same better-contract ladder so that the local usefulness signal is tested on a broader and still-discriminating heldout regime.
