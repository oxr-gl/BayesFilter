# LEDH Score And Memory Test Suite Result

Date: 2026-07-05

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Accept the `N=10000` LEDH score/memory tests as an executed regression suite for currently admitted score routes. | Passed for LGSSM compact score and parameterized SIR scoped manual score. One test exists for every highdim ledger row, plus an all-row integration status test. | No veto fired. Scores were finite, finite-difference checks passed, GPU was visible, and peak GPU memory stayed below the 12000 MiB budget. | Most highdim LEDH rows still do not have admitted score routes. Their tests correctly assert blocked status. | Keep this suite as the guardrail before leaderboard score promotion; add new admitted rows only after a same-target value route and no-autodiff total-derivative score route exist. | This does not prove score correctness for blocked rows, HMC/NUTS readiness, exact nonlinear likelihood score correctness, or LEDH superiority over other algorithms. |

## Run Manifest

- Git commit: `8e66819af4235d6a4a9c68eb49ce9eb9fdc9feef`
- Plan file: `docs/plans/ledh-score-memory-test-suite-plan-2026-07-05.md`
- Test file: `tests/test_ledh_score_memory_n10000.py`
- Command, light default run: `pytest -q tests/test_ledh_score_memory_n10000.py`
- Command, GPU opt-in run: `BAYESFILTER_RUN_LEDHD_SCORE_MEMORY_N10000=1 MPLCONFIGDIR=/tmp pytest -q tests/test_ledh_score_memory_n10000.py -s`
- Environment: TensorFlow/TFP repo environment, GPU trusted execution
- GPU: NVIDIA GeForce RTX 4080 SUPER, 16376 MiB, driver 591.86
- CPU/GPU status: light run intentionally hides GPU by default; opt-in run used visible GPU
- Random seeds: `81120` for the admitted score checks
- Wall time, GPU opt-in run: 946.89 seconds
- Result artifact: this file

## Local Check Results

- `python -m py_compile tests/test_ledh_score_memory_n10000.py`: passed
- `pytest -q tests/test_ledh_score_memory_n10000.py`: passed, `6 passed, 2 skipped`
- `BAYESFILTER_RUN_LEDHD_SCORE_MEMORY_N10000=1 MPLCONFIGDIR=/tmp pytest -q tests/test_ledh_score_memory_n10000.py -s`: passed, `8 passed`

TensorFlow emitted duplicate CUDA factory registration warnings during startup. They did not block GPU device creation or the tests.

## Admitted Score Route Evidence

| Row | Route | Particles | Correctness check | Peak GPU memory |
|---|---|---:|---|---:|
| `benchmark_lgssm_exact_oracle_m3_T50` | `compact_forward_sensitivity_no_autodiff_same_scalar_lgssm_ledh_pfpf_ot` | 10000 | Directional score `0.3782809953387445` vs same-scalar float64 central FD `0.378280994883795`; absolute error `4.5494946698809713e-10`, relative error `1.202675980538481e-09` | 197.2001953125 MiB |
| `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` | `manual_reverse_scan_no_autodiff` | 10000 | Directional score `-0.8572139739990234` vs same-route central FD `-0.8583068251609802`; absolute error `0.0010928511619567871`, relative error `0.00127326394431293` | 3169.22314453125 MiB |

The LGSSM correctness oracle is float64 same-scalar finite difference. Earlier float32/TF32 finite-difference evidence at `N=10000` was numerically unreliable for this check and is not used as the correctness oracle here.

## Blocked Row Evidence

The integration test still enumerates every highdim LEDH ledger row and refuses to silently pass blocked rows.

| Row | Test status |
|---|---|
| `zhao_cui_sv_actual_nongaussian_T1000` | Blocked: no reviewed current GPU/XLA same-target LEDH row adapter and no admitted score route. |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | Blocked: no LEDH KSC row adapter and no admitted score route. |
| `zhao_cui_spatial_sir_austria_j9_T20` | Blocked for full leaderboard score; fixed spatial SIR is still value-arm candidate only. |
| `zhao_cui_predator_prey_T20` | Blocked: no reviewed current GPU/XLA same-target LEDH row adapter and no admitted score route. |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | Blocked: no reviewed same-target LEDH row adapter and no admitted score route. |

## Post-Run Red-Team Note

The strongest alternative explanation for a false pass is that the finite-difference oracle checks the same implemented scalar, not an external exact likelihood for nonlinear rows. That is acceptable for this regression suite because the stated question is whether admitted LEDH implementation routes have score/memory guardrails at `N=10000`; it is not a proof of statistical correctness for nonlinear models.

The weakest part of the current evidence is model coverage: only LGSSM compact score and parameterized SIR scoped score are admitted. The other rows are correctly represented as blocked. A future result that implements same-target value routes and no-autodiff total-derivative score routes for those rows would overturn the current blocked-row status.
