# P50-M4 Value And Gradient Calibration Result

metadata_date: 2026-06-09
phase: P50-M4
status: PASS_P50_M4_VALUE_GRADIENT_CALIBRATION

## Decision Table

| Field | Decision |
| --- | --- |
| Gate decision | Pass M4 for predeclared value and gradient calibration rules before running P50-M5 and P50-M6 model ladders. |
| Primary criterion status | Passed: the calibration artifacts define value error, gradient norm error, directional residual/cosine diagnostics, likelihood variability normalization, finite-difference boundaries, autodiff fragility checks, veto diagnostics, pass classes, and non-promotions. |
| Veto diagnostic status | Passed: the rules forbid single finite-difference truth, value-only promotion to gradient correctness, post-hoc threshold loosening, likelihood-variability excuses for same-data bias, hidden stochastic/adaptive gradient branches, and unsupported HMC-readiness claims. |
| Main uncertainty | M4 is a rules and governance gate.  It does not execute SV, generalized SV, spatial SIR, predator-prey, or HMC sampler comparisons. |
| Next justified action | Advance to M5 SV and generalized SV ladder, using these rules as the comparison contract. |
| Not concluded | No model-suite pass, no HMC readiness, no production readiness, no smoothing support, no source-faithful adaptive TT/SIRT filtering, and no S&P 500 reproduction. |

## Artifacts

- `docs/plans/bayesfilter-highdim-zhao-cui-p50-value-gradient-calibration-rules-2026-06-09.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p50-value-gradient-calibration-rules-2026-06-09.json`
- `tests/highdim/test_p50_value_gradient_calibration.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p50-m4-value-gradient-calibration-result-2026-06-09.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p50-visible-execution-ledger-2026-06-09.md`

## Rules Added

M4 records these rules before the model ladders consume them:

- same-target value metrics: absolute, relative, per-step, paired same-data,
  and likelihood-variability-normalized gaps;
- same-target gradient metrics: norm error, relative norm error, deterministic
  directional residuals, scaled directional residuals, directional cosine, and
  componentwise finite checks;
- default small-fixture same-target gates: `1e-6` absolute value error,
  `1e-8` relative value error, `1e-7` per-step value error, `1e-5` gradient
  relative norm error, `1e-5` directional scaled residual, and directional
  cosine at least `0.999999` when defined;
- generated-data likelihood variability is explanatory only and cannot excuse
  failed paired same-data value or gradient gates;
- finite differences require a stable multi-step window and remain diagnostic
  rather than sole truth;
- autodiff gradients require finite checks, branch/replay checks where
  applicable, and a paired same-target reference before promoted claims.

## Local Validation

Commands run CPU-only:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p50_value_gradient_calibration.py tests/highdim/test_p45_cross_model_error_calibration.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_p50_value_gradient_calibration.py
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p50-value-gradient-calibration-rules-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p50-value-gradient-calibration-rules-2026-06-09.json tests/highdim/test_p50_value_gradient_calibration.py docs/plans/bayesfilter-highdim-zhao-cui-p50-m4-value-gradient-calibration-result-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p50-visible-execution-ledger-2026-06-09.md
```

Observed results:

- `10 passed`;
- compileall passed with no output;
- `git diff --check` passed.

## Non-Claims

M4 does not claim:

- any SV, generalized SV, spatial SIR, or predator-prey comparison has passed;
- finite differences are ground truth;
- autodiff is correct without evidence;
- likelihood variability can justify systematic same-data bias;
- HMC readiness;
- production readiness;
- smoothing support.
