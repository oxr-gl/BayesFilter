# P40 Result: SV Kalman--CUT4--Zhao-Cui Tests

metadata_date: 2026-06-07
phase: P40

Status: `PASS_P40_LOCAL_IMPLEMENTATION_AND_GOVERNANCE`.

## Decision Table

| Decision | Status |
| --- | --- |
| Add exact transformed-mixture SV Kalman oracle for dimensions 1, 2, 3 | `PASS` |
| Add CUT4 comparator for the same independent-product transformed-mixture target | `PASS` |
| Tie scalar transformed-mixture panel oracle to existing scalar P39 CUT4/dense references | `PASS` |
| Compare existing Zhao--Cui/BayesFilter SV lane honestly | `PASS_WITH_SCOPE_LIMIT`: scalar native SV only |
| Add generalized SV diagnostic coverage | `PASS_WITH_SCOPE_LIMIT`: finite diagnostic and moment-matched non-exact approximation only |
| Claude code governance review | `PASS_P40_CODE_GOVERNANCE` |

## Implementation Summary

Changed files:

- `bayesfilter/highdim/sv_mixture_cut4.py`
- `bayesfilter/highdim/__init__.py`
- `tests/highdim/test_p40_sv_kalman_cut4_zhaocui.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p40-sv-kalman-cut4-zhaocui-claude-review-ledger-2026-06-07.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p40-sv-kalman-cut4-zhaocui-test-result-2026-06-07.md`

Added implementation:

- `transformed_sv_panel_observations`
- `independent_panel_sv_mixture_kalman_filter`
- `independent_panel_sv_mixture_cut4_filter`
- `SVPanelMixtureFilterResult`

The Kalman oracle enumerates all KSC component tuples, `7**dim`, for tiny
deterministic `T=2` independent transformed-SV panel fixtures, then collapses
posterior Gaussian components by log-sum-exp weights and the law of total
covariance.

The CUT4 comparator enumerates the same component tuples and uses affine
structural CUT4 updates.  Because each conditional component is linear
Gaussian, this validates component-grid bookkeeping, Gaussian reduction, and
moment collapse.  It does not validate nonlinear CUT4 accuracy.

## Test Evidence

Commands run:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p40_sv_kalman_cut4_zhaocui.py tests/highdim/test_p39_sv_mixture_cut4.py
```

Result: `15 passed, 2 warnings in 16.71s`.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p40_sv_kalman_cut4_zhaocui.py tests/highdim/test_p39_sv_mixture_cut4.py tests/highdim/test_p30_stochastic_volatility.py tests/highdim/test_p30_sv_short_sequential_tt_value_path.py tests/highdim/test_p30_cut4_statistical_comparators.py tests/highdim/test_public_api_highdim.py tests/test_v1_public_api.py
```

Result: `43 passed, 2 warnings in 20.39s`.

```bash
python -m compileall -q bayesfilter/highdim/sv_mixture_cut4.py bayesfilter/highdim/__init__.py tests/highdim/test_p40_sv_kalman_cut4_zhaocui.py
```

Result: passed with no output.

Claude review:

```text
PASS_P40_CODE_GOVERNANCE
```

## Boundaries

- No exact native SV likelihood claim.
- No KSC importance-reweighting implementation.
- No multivariate Zhao--Cui TT implementation.
- No generalized CNS estimator.
- No generalized SV exact Kalman equivalence claim.
- No nonlinear CUT4 accuracy claim from the conditionally linear
  transformed-mixture fixtures.
- No production-default or derivative-readiness claim.
