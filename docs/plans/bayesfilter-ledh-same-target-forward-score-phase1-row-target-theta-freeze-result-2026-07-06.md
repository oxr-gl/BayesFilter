# Phase 1 Result: Row Target And Theta Freeze

Date: 2026-07-06

Status: `AMENDED_PASSED_WITH_FIXED_SIR_FREE_MODEL_THETA`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Freeze the LEDH row targets and theta vectors exactly as documented in the amended Phase 1 contract. By explicit human decision on 2026-07-06, the fixed SIR row now uses model parameters as free parameters through the existing `sir_log_scale_theta` surface. |
| Primary criterion status | Passed after amendment: every row now has a frozen target scalar, free theta policy, coordinate system, and score dimensionality. |
| Veto diagnostic status | Passed: no raw/transformed actual-SV ambiguity remains; the SIR amendment is visible and does not promote scoped/local-complete-data score evidence as full observed-data evidence; no KSC/generalized-SV substitution was allowed. |
| Main uncertainty | The fixed SIR row now has a 3D free-theta target, but the full observed-data same-target LEDH forward scalar and no-tape score remain unadmitted until later phases. |
| Next justified action | Advance to Phase 2 common forward likelihood API, with fixed SIR included in nonempty score scope only after same-target forward scalar admission. |
| What is not concluded | No model forward scalar is admitted yet, no score route is admitted yet, and no leaderboard row is promoted. |

## Question Answered

Phase 1 asked:

- What exact `log p_theta(y_1:T)` target and theta vector must each LEDH row
  use?

Answer:

- The row targets and theta vectors are now frozen in
  `docs/plans/bayesfilter-ledh-same-target-forward-score-phase1-row-target-theta-contract-2026-07-06.md`.

Two important outcomes:

1. `zhao_cui_sv_actual_nongaussian_T1000` is frozen as the transformed
   actual-SV target only.
2. `zhao_cui_spatial_sir_austria_j9_T20` is amended to use
   `sir_log_scale_theta` with score dimensionality `3`, truth theta
   `[0, 0, 0]`, and the parameter order
   `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)`.

## Evidence

Fixed spatial SIR after the 2026-07-06 human amendment:

- Dataset generator and tests now bind the fixed row to
  `truth_theta_coordinate = sir_log_scale_theta` and
  `truth_theta = [0,0,0]`.
- Source-scope row contract records `theta_dimension = 0` for the fixed source
  row in the historical author fixed-parameter example; this amendment is a
  BayesFilter free-parameter benchmark surface, not an author inference-theta
  source-faithfulness claim:
  [bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json](/home/chakwong/BayesFilter/docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json)
- The parameterized SIR row is explicit and separate, with its own
  `sir_log_scale_theta`, but is now legacy/scoped diagnostic evidence rather
  than the path for the main fixed-row score gate.
- Existing local SIR score hooks and tests cover the same three log-scale
  model-parameter convention:
  [test_p81_analytical_sir_score.py](/home/chakwong/BayesFilter/tests/highdim/test_p81_analytical_sir_score.py:75)

Actual SV:

- The source-scope row is
  `stochastic_volatility_transformed_actual_nongaussian` with estimated
  parameters `(gamma, beta)` and fixed `sigma = 1.0`:
  [bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json](/home/chakwong/BayesFilter/docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json)
- The reviewed actual-SV single-target program and corrected derivation note
  freeze one transformed actual-SV target only:
  [bayesfilter-actual-sv-single-target-master-program-2026-06-29.md](/home/chakwong/BayesFilter/docs/plans/bayesfilter-actual-sv-single-target-master-program-2026-06-29.md)
  and
  [bayesfilter-highdim-actual-sv-single-target-corrected-derivation-note-2026-06-29.md](/home/chakwong/BayesFilter/docs/plans/bayesfilter-highdim-actual-sv-single-target-corrected-derivation-note-2026-06-29.md)

KSC SV:

- The KSC row is a declared Gaussian-mixture surrogate target with the same SV
  truth values as actual-SV but explicit surrogate-policy wording:
  [test_filtering_value_gradient_benchmark_source_paper_scope.py](/home/chakwong/BayesFilter/tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py:150)

Predator-prey:

- The row is source-scope T20 additive-Gaussian predator-prey with physical
  parameters `(r, K, a, s, u, v)`:
  [test_filtering_value_gradient_benchmark_source_paper_scope.py](/home/chakwong/BayesFilter/tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py:170)
  and
  [test_filtering_value_gradient_benchmark_p8_datasets.py](/home/chakwong/BayesFilter/tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py:170)

Generalized SV:

- The frozen target contract says the active row is the source-scope
  generalized-SV prior-mean synthetic row, not actual-SV, not KSC, not native
  generalized-SV fixture:
  [bayesfilter-generalized-sv-target-truth-source-scope-contract-2026-06-29.md](/home/chakwong/BayesFilter/docs/plans/bayesfilter-generalized-sv-target-truth-source-scope-contract-2026-06-29.md)
- Dataset/tests freeze the active transformed prior-mean coordinate system with
  `truth_theta = [1.0824113944610982, -2.076793740349318, 0.0]`:
  [test_filtering_value_gradient_benchmark_p8_datasets.py](/home/chakwong/BayesFilter/tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py:194)

LGSSM:

- The same-target LGSSM runner already freezes the benchmark row and five
  physical benchmark parameters:
  [benchmark_ledh_same_target_lgssm_m3_t50_value.py](/home/chakwong/BayesFilter/docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py:1)

## Plain Scientific Classification

- The fixed spatial SIR leaderboard row now has free model theta
  `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)` under the human
  amendment.
- The parameterized SIR row is now legacy/scoped diagnostic evidence for the
  same log-scale surface. It must not be promoted as full observed-data score
  evidence unless the Phase 3/4 same-target gates pass for the fixed row.
- Actual-SV is frozen as the transformed actual-SV target.
- KSC is frozen as the surrogate mixture target.
- Predator-prey and generalized-SV are frozen as their source-scope row
  likelihood targets.

Phase 1 therefore converges after changing the fixed SIR row's theta contract
under explicit human direction, while preserving that full observed-data SIR
score admission still requires later same-target value and no-tape score gates.

## Checks Run

```bash
rg -n "no_free_theta|sir_log_scale_theta|truth_theta_coordinate|transformed_actual_nongaussian|gaussian_mixture_surrogate|predator_prey_additive_gaussian|source_route_active_transformed_prior_mean" tests/highdim docs/plans docs/benchmarks scripts -g '!*.pyc'
```

Result: passed.

```bash
git diff --check -- \
  docs/plans/bayesfilter-ledh-same-target-forward-score-phase1-row-target-theta-contract-2026-07-06.md \
  docs/plans/bayesfilter-ledh-same-target-forward-score-phase1-row-target-theta-freeze-result-2026-07-06.md \
  docs/plans/bayesfilter-ledh-same-target-forward-score-phase2-common-forward-api-subplan-2026-07-06.md \
  docs/reviews/ledh-same-target-forward-score-phase1-review-bundle-2026-07-06.md \
  docs/plans/bayesfilter-ledh-same-target-forward-score-visible-execution-ledger-2026-07-06.md
```

Result: pending until this phase-close patch is complete, then rerun.

## Evidence Contract Result

| Field | Status |
| --- | --- |
| Question | Answered directly: each row now has a frozen target scalar and theta vector. |
| Baseline/comparator | Passed: source-scope contracts, dataset tests, actual-SV and generalized-SV governing contracts, and current benchmark artifacts agree on the frozen row identities. |
| Primary criterion | Passed: target scalar, theta, coordinate system, and score dimensionality are frozen for every row. |
| Veto diagnostics | Passed: no target substitution and no silent row redefinition occurred. |
| Explanatory diagnostics | Current callback routes remain implementation context only; they do not override the frozen targets. |
| Not concluded | No forward scalar admission, no score implementation, and no leaderboard promotion. |

## Next-Phase Handoff

Phase 2 must build the common forward API under these hard constraints:

- fixed SIR uses `sir_log_scale_theta` and must be supported by the common
  forward API as a 3D model-parameter row;
- parameterized SIR remains scoped/legacy diagnostic only and must not be used
  as a shortcut around the fixed-row full observed-data gates;
- actual-SV target density must be the transformed actual-SV target, not a raw
  Gaussian-closure substitute;
- generalized-SV and KSC must preserve their own row identities and target
  families.
