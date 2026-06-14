# P41 Result: Exact Transformed SV Zhao-Cui Ladder

metadata_date: 2026-06-07
phase: P41

Status: `PASS_P41_LOCAL_IMPLEMENTATION_AND_GOVERNANCE`.

## Decision Table

| Decision | Status |
| --- | --- |
| Add exact `z=log(y^2)` transformed SV model and density helpers | `PASS` |
| Add exact transformed dense references for dimensions 1, 2, 3 | `PASS` |
| Add factorized scalar Zhao--Cui/fixed-design TT panel lane | `PASS_WITH_SCOPE_LIMIT`: independent coordinate sum only |
| Tie exact transformed dense to raw native SV through Jacobian correction | `PASS` |
| Compare KSC mixture Kalman/CUT4 as approximation-only comparator | `PASS_WITH_SCOPE_LIMIT` |
| Claude plan review | `PASS_P41_PLAN_GOVERNANCE` |
| Claude code review | `PASS_P41_CODE_GOVERNANCE` |

## Implementation Summary

Changed files:

- `bayesfilter/highdim/sv_mixture_cut4.py`
- `bayesfilter/highdim/__init__.py`
- `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p41-exact-transformed-sv-zhaocui-ladder-plan-2026-06-07.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p41-exact-transformed-sv-zhaocui-claude-review-ledger-2026-06-07.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p41-exact-transformed-sv-zhaocui-ladder-result-2026-06-07.md`

Added implementation:

- `ExactTransformedSVSSM`
- `ExactTransformedSVPanelResult`
- `exact_log_chi_square_log_density`
- `exact_transformed_sv_observations`
- `exact_transformed_sv_jacobian_log_abs_det`
- `exact_transformed_sv_scalar_dense_reference`
- `exact_transformed_sv_independent_panel_dense_reference`
- `exact_transformed_sv_independent_panel_zhaocui_tt_filter`

## Numerical Evidence

Exact transformed dense versus factorized Zhao--Cui/fixed-design TT:

- dimension 1, 2, and 3 tests passed with `2e-8` log-likelihood and per-step
  log-normalizer tolerances.
- probe gaps before test finalization were about `1e-11` for the selected
  deterministic fixtures.

Exact transformed dense versus KSC mixture Kalman/CUT4 approximation:

| Dimension | Exact transformed dense | KSC mixture Kalman/CUT4 | KSC minus exact |
| --- | ---: | ---: | ---: |
| 1 | `-4.492112473834` | `-4.505481290078` | `-0.013368816244` |
| 2 | `-8.819168690843` | `-8.847218775872` | `-0.028050085029` |
| 3 | `-15.033778455609` | `-15.092459806873` | `-0.058681351263` |

These KSC gaps are finite approximation diagnostics, not failures and not exact
agreement claims.

## Test Evidence

Commands run:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py tests/highdim/test_p40_sv_kalman_cut4_zhaocui.py tests/highdim/test_p39_sv_mixture_cut4.py
```

Result: `26 passed, 2 warnings in 31.50s`.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py tests/highdim/test_p40_sv_kalman_cut4_zhaocui.py tests/highdim/test_p39_sv_mixture_cut4.py tests/highdim/test_p30_stochastic_volatility.py tests/highdim/test_p30_sv_short_sequential_tt_value_path.py tests/highdim/test_p30_cut4_statistical_comparators.py tests/highdim/test_public_api_highdim.py tests/test_v1_public_api.py
```

Result: `54 passed, 2 warnings in 37.44s`.

```bash
python -m compileall -q bayesfilter/highdim/sv_mixture_cut4.py bayesfilter/highdim/__init__.py tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py
```

Result: passed with no output.

Claude review:

```text
PASS_P41_PLAN_GOVERNANCE
PASS_P41_CODE_GOVERNANCE
```

## Boundaries

- No coupled multivariate Zhao--Cui TT implementation claim.
- No exact KSC mixture claim; KSC remains a Gaussian-mixture approximation.
- No generalized SV/CNS estimator claim.
- No nonlinear CUT4 accuracy claim.
- No derivative, HMC, DSGE, GPU, paper-scale, or production-default readiness
  claim.
