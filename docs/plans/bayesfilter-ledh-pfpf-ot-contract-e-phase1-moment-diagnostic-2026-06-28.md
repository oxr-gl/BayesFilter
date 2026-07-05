# Contract E Moment Diagnostic

Status: `passed`

| Case | Expected | Status | Mean residual | Cov residual | Rank | Cond |
| --- | --- | --- | --- | --- | --- | --- |
| 1d_strict_gap_pass | pass | pass | 0.000e+00 | 1.205e-16 | 1/1 | 1.000e+00 |
| 2d_full_rank_strict_gap_pass | pass | pass | 5.551e-17 | 6.117e-16 | 2/2 | 2.849e+00 |
| 2d_rank_deficient_support_repair_pass | pass | pass | 1.388e-16 | 2.120e-16 | 1/1 | 1.000e+00 |
| 2d_conditioning_expected_veto | veto | expected_veto | 4.547e-13 | 2.898e-16 | 2/2 | 3.494e+13 |

## Nonclaims

This diagnostic does not certify LEDH filtering correctness, gradients, LGSSM Kalman agreement, production readiness, posterior correctness, or GPU/XLA performance.
