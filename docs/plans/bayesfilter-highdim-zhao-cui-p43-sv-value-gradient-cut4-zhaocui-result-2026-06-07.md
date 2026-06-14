# P43 Result: SV Value and Gradient CUT4--Zhao-Cui Ladder

metadata_date: 2026-06-07
phase: P43

Status: `PASS_P43_LOCAL_IMPLEMENTATION_AND_GOVERNANCE`.

## Decision Table

| Item | Status |
| --- | --- |
| Decision | Keep P43 as a Tier-1 local diagnostic ladder for SV value/gradient tie-outs. |
| Primary criterion | Passed for same-target value and diagnostic score checks in dimensions 1, 2, and 3. |
| Veto diagnostics | Passed: no target-mismatch equality claim, no generalized-SV exactness claim, no coupled multivariate TT claim, and no HMC/Tier-2/Tier-3 promotion claim. |
| Main uncertainty | The scores are diagnostic autodiff-through-tiny-fixture scores, not a production analytic derivative API or long-horizon HMC validation. |
| Next justified action | Use this as a local correctness guardrail before any larger score-variance, HMC, or generalized-SV target implementation work. |
| Not concluded | No HMC readiness, no sampling-variance tolerance, no exact KSC claim, no coupled multivariate Zhao--Cui TT, and no exact generalized-SV filter. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `7ccb9c39883471c2d5ec2891cbf33b9ed436bada` |
| Timestamp | `2026-06-07T04:07:04+08:00` |
| Python | `Python 3.11.14` |
| CPU/GPU status | CPU-only by command: `CUDA_VISIBLE_DEVICES=-1`; TensorFlow still emitted CUDA registration chatter, but the run intentionally hid GPU devices. |
| Plan artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p43-sv-value-gradient-cut4-zhaocui-plan-2026-06-07.md` |
| Review ledger | `docs/plans/bayesfilter-highdim-zhao-cui-p43-sv-value-gradient-cut4-zhaocui-claude-review-ledger-2026-06-07.md` |
| Test artifact | `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py` |
| Seeds | Deterministic fixture seeds in the test file, including `p43-sv-gradient`, `dim-{1,2,3}`, and summary seeds. |
| Data | Tiny deterministic observations from `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`; no external data. |

## Commands And Results

- Focused P43:
  - `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
  - Result: `10 passed, 2 warnings in 32.55s`.
- Guardrail suite:
  - `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py tests/highdim/test_p40_sv_kalman_cut4_zhaocui.py tests/highdim/test_p39_sv_mixture_cut4.py tests/highdim/test_p30_stochastic_volatility.py tests/highdim/test_p30_sv_short_sequential_tt_value_path.py tests/highdim/test_p30_cut4_statistical_comparators.py tests/highdim/test_public_api_highdim.py tests/test_v1_public_api.py`
  - Result: `64 passed, 2 warnings in 78.49s`.
- Numeric summary:
  - `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python - <<'PY' ...`
  - Result summarized below.
- Claude code-governance review:
  - First worker attempt `p43-code-review-iter1` was stopped after a bounded
    no-output hang.
  - Narrowed worker attempt `p43-code-review-iter1b` returned
    `PASS_P43_CODE_GOVERNANCE`.

## Numeric Summary

Same-target KSC mixture CUT4 versus KSC Kalman:

| dim | value gap | max score gap | relative score gap |
| --- | ---: | ---: | ---: |
| 1 | `0.000e+00` | `2.220e-16` | `1.660e-16` |
| 2 | `0.000e+00` | `2.442e-15` | `1.215e-15` |
| 3 | `-5.329e-15` | `3.331e-15` | `1.290e-15` |

Same-target exact transformed factorized Zhao--Cui/fixed-design TT versus exact
dense:

| dim | value gap | max score gap | relative score gap |
| --- | ---: | ---: | ---: |
| 1 | `-4.006e-12` | `3.109e-15` | `2.523e-15` |
| 2 | `-8.011e-12` | `3.109e-15` | `1.731e-15` |
| 3 | `-1.202e-11` | `3.109e-15` | `1.287e-15` |

KSC mixture versus exact transformed SV is an approximation comparison only:

| dim | KSC minus exact value | KSC minus exact score norm |
| --- | ---: | ---: |
| 1 | `-0.013368816244` | `0.006470` |
| 2 | `-0.028050085029` | `0.006594` |
| 3 | `-0.058681351263` | `0.041374` |

## Interpretation

P43 gives a clean local answer to the user's question within the P42 rules:

- CUT4 matches the KSC Kalman-mixture target for SV dimensions 1, 2, and 3 in
  both value and diagnostic gradient on the tiny deterministic fixtures.
- The factorized Zhao--Cui/fixed-design TT lane matches the exact transformed
  dense target for SV dimensions 1, 2, and 3 in both value and diagnostic
  gradient on the same parameterization.
- CUT4/KSC and exact transformed Zhao--Cui are not the same target.  Their
  nonzero value and score gaps are recorded as approximation differences, not
  failures of either same-target check.
- The generalized SV case has only finite diagnostic coverage under an explicit
  transformed-residual non-claim label.

## Post-Run Red-Team Note

The strongest alternative explanation is that the fixtures are too small and
too deterministic to expose long-horizon numerical or HMC-relevant score
instability.  A larger result would need a new evidence contract with
multi-seed data-law/evaluator variance separation, score covariance diagnostics,
and HMC trajectory checks.  P43 intentionally does not provide that evidence.
