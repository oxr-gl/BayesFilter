# Result: 1D LGSSM Horizon Ladder

## Decision

`one_d_lgssm_horizon_ladder_agreement_residual_veto`

## Scope

This result extends the controlled scalar-state LGSSM microscope from `T=2` to
`T=4`. It compares BayesFilter TF/TFP annealed transport against the current
local patched filterflow executable on fixed numeric fixtures. This is not a
smoothness-surface reproduction and does not promote gradient correctness.

Plan:
`docs/plans/bayesfilter-dpf-1d-lgssm-horizon-ladder-plan-2026-06-01.md`

Artifacts:

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_lgssm_horizon_ladder_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-1d-lgssm-horizon-ladder-2026-06-01.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_1d_lgssm_horizon_ladder_2026-06-01.json`

## Findings

| Scenario | T | Trigger flags | Scalar delta | Ledger match | Residual veto | BayesFilter FD | filterflow FD |
| --- | ---: | --- | ---: | --- | --- | ---: | ---: |
| `T2_anchor` | 2 | `[False, True]` | `6.20155775621356e-08` | pass | pass | `-1.6753548204218038` | `-1.6754865646362305` |
| `T4_extension` | 4 | `[False, True, True, True]` | `1.731355947498514e-07` | pass | fail | `-1.9368130259955763` | `-1.9371509552001953` |

The important distinction is that `T4_extension` did **not** show a
BayesFilter/filterflow forward-ledger disagreement. It showed implementation
agreement but failed the predeclared absolute row-residual tolerance:

| Scenario | BayesFilter max row residual | filterflow max row residual | tolerance |
| --- | ---: | ---: | ---: |
| `T2_anchor` | `3.7740217395665354e-06` | `3.6954879760742188e-06` | `1e-04` |
| `T4_extension` | `0.0005233019270021178` | `0.0005233287811279297` | `1e-04` |

Gradient diagnostics remain non-promotional. Finite-difference gradients remain
close across implementations at both horizons, while AD gradients continue to
disagree with finite differences.

## Interpretation

The scalar-state ladder supports the user's intuition: BayesFilter and
filterflow continue to agree as the toy scalar-state horizon is extended to
`T=4`, at least for forward scalar and ledger values. The first issue that
appears is not a cross-implementation mismatch; it is a shared transport
residual-quality veto under the strict `1e-4` row-residual bound.

The next step should not jump to the full smoothness LGSSM yet. It should first
run a `T=4` residual ladder over Sinkhorn settings, especially
`convergence_threshold` and `max_iterations`, to determine whether the shared
row residual is a tolerance/iteration issue or a structural consequence of the
annealed transform at repeated resampling steps.

## Verification

| Command | Result |
| --- | --- |
| `python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_lgssm_horizon_ladder_tf.py` | pass |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_lgssm_horizon_ladder_tf` | pass; decision `one_d_lgssm_horizon_ladder_agreement_residual_veto` |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_lgssm_horizon_ladder_tf --validate-only` | pass |
| `python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_1d_lgssm_horizon_ladder_2026-06-01.json >/dev/null` | pass |
| schema/decision invariant check on JSON output | pass |
| NumPy import gate on touched BayesFilter TF/TFP runner | pass; no module-scope NumPy import |
| forbidden import-boundary search for student/vendored/highdim/DSGE/NAWM imports | pass; no matches |
| lane-scoped trailing whitespace check | pass |
| `git diff --check` | pass |
| `git status --short -- bayesfilter tests docs/chapters` | pass; no output |

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No general nonlinear-SSM validity is concluded.
- No smoothness-surface gradient agreement is concluded.
- No transport-map derivative correctness is concluded.
