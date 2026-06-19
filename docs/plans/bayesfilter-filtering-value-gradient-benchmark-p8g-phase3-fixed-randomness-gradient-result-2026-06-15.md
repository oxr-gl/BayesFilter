# P8g-G3 Result: Fixed-Randomness LEDH Gradient Objective

Date: 2026-06-15

Status: `PASS_P8G_G3_FIXED_RANDOMNESS_GRADIENT_REVIEWED`

## Phase Objective

Define and validate the no-resampling fixed-randomness LEDH objective needed for
gradient-bearing work, initially scoped to the actual scalar SV row covered by
the reviewed G2b graph route.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the fixed-randomness/no-resampling LEDH surrogate objective provide stable, finite, coordinate-consistent gradients? |
| Baseline/comparator | Reviewed G2b scalar-SV graph route and finite-difference checks on the same fixed random draws. |
| Primary criterion | Finite stable gradients pass repeatability, CPU/GPU parity, and directional finite-difference checks in `canonical_unconstrained` coordinate. |
| Veto diagnostics | Gradient through resampling branch; missing seed/salt contract; parameterization mismatch; finite value treated as gradient correctness; non-finite or unstable gradients. |
| Explanatory diagnostics | Gradient norms, finite-difference residuals, seed-variation spread, device placement. |
| Not concluded | Stochastic PF target gradient correctness, production HMC readiness, tuned particle count, generic high-dimensional Algorithm 1 gradient readiness, or filter ranking. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `eae3f22fb8fe4a7740d7dc67066522303aaaf083` |
| Worktree state | Dirty before/during G3; unrelated Zhao-Cui/SGQF changes preserved. |
| G2b result | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-repair-result-2026-06-15.md` |
| G3 subplan | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-subplan-2026-06-15.md` |
| G3 contract | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-contract-2026-06-15.md` |
| CPU gradient JSON/CSV | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-checks-cpu-2026-06-15.json`, `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-checks-cpu-2026-06-15.csv` |
| GPU gradient JSON/CSV | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-checks-gpu-2026-06-15.json`, `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-checks-gpu-2026-06-15.csv` |
| Result file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-result-2026-06-15.md` |

## Code Changes

- Added value-only scalar-SV graph objective
  `ledh_pfpf_alg1_scalar_sv_graph_log_likelihood_tf(...)`.
- Kept G2b XLA route for speed-oriented value profiles.
- Added non-XLA TensorFlow graph variant for reverse-mode gradients because
  reverse-mode through XLA `tf.while_loop` raised TensorList boundary errors.
- Added `--p8g-fixed-randomness-gradient-check`, `--route-variant`,
  `--coordinate`, and `--output-csv` runner support.
- Added focused G3 payload/guardrail test coverage.

## Commands Run

```bash
git diff --check
python -m py_compile experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py tests/test_ledh_pfpf_alg1_ukf_tf.py -q -k "p8g_fixed_randomness_gradient_check or p8g_profile or sv_scalar_graph or filter_bench_gradient_semantics or fixed_branch_gradient"

CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8g-fixed-randomness-gradient-check --rows actual_sv --horizon 10 --particles 8 --seeds 81120,81121 --route-variant p8g_sv_scalar_graph --coordinate canonical_unconstrained --device cpu --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-checks-cpu-2026-06-15.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-checks-cpu-2026-06-15.csv

MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8g-fixed-randomness-gradient-check --rows actual_sv --horizon 10 --particles 8 --seeds 81120,81121 --route-variant p8g_sv_scalar_graph --coordinate canonical_unconstrained --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-checks-gpu-2026-06-15.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-checks-gpu-2026-06-15.csv
```

## Check Results

- `git diff --check`: passed.
- `python -m py_compile ...`: passed.
- Focused pytest: `5 passed, 30 deselected, 2 warnings`.

## Gradient Results

Scope:

- row: `zhao_cui_sv_actual_nongaussian_T1000`;
- horizon prefix: `10`;
- particles: `8`;
- seeds: `81120,81121`;
- coordinate: `theta=(Phi^{-1}(gamma), log(beta))`;
- route variant: `p8g_sv_scalar_graph`;
- resampling route: `none`.

| Metric | CPU | GPU |
|---|---:|---:|
| Status | `executed_p8g_fixed_randomness_gradient_check` | `executed_p8g_fixed_randomness_gradient_check` |
| Mean log likelihood | `-8.028383010448087` | `-8.028383010448088` |
| Mean gradient | `[-1.8333640449046442, 0.8486277259462816]` | `[-1.833364044904644, 0.8486277259462812]` |
| Max finite-difference residual | `4.1930169336623635e-09` | `4.201898551325911e-09` |
| Max repeat gradient delta | `0.0` | `0.0` |
| Value tensor device | CPU | GPU |
| Gradient tensor device | CPU | GPU |

CPU/GPU parity:

- seed `81120`: value delta `-3.55e-15`, gradient deltas about
  `[4.44e-16, -6.66e-16]`;
- seed `81121`: value delta `0.0`, gradient deltas about
  `[2.22e-16, 1.67e-16]`.

## Gate Assessment

Decision: `PASS_P8G_G3_FIXED_RANDOMNESS_GRADIENT_REVIEWED`.

| Criterion | Status | Evidence |
|---|---|---|
| Fixed randomness/seed contract | Pass | Contract artifact records salts `110` and `1110 + t`; artifacts record the same randomness contract. |
| No resampling gradient | Pass | Route records `resampling_route=none`; no resampling randomness used. |
| Finite values and gradients | Pass | CPU/GPU artifacts have `all_values_finite=true` and `all_gradients_finite=true`. |
| Repeatability | Pass | Max repeat value and gradient deltas are `0.0`. |
| Finite-difference directional checks | Pass | Max residuals are about `4.2e-09` for the small diagnostic scope. |
| CPU/GPU parity | Pass | Values and gradients agree to floating precision. |
| Review gate | Pass | Claude read-only result review returned `VERDICT: AGREE` with one minor non-blocking note about JSON wording. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
|---|---|---|---|---|---|
| Mark G3 as reviewed pass | Passed for small actual-SV fixed-randomness diagnostic scope. | No finiteness, repeatability, coordinate, resampling, finite-difference, or CPU/GPU parity veto fired. | Whether this small-scope diagnostic should be broadened before particle tuning or HMC tiers. | Refresh G4 tuning subplan around reviewed scalar-SV route and existing nonclaims. | No stochastic PF marginal gradient, no HMC readiness, no tuned particle count, no generalized-SV/high-dimensional gradient evidence, no filter ranking. |

## Post-Run Red Team Note

Strongest alternative explanation: the diagnostic validates a fixed-randomness
conditional objective, not the gradient of the stochastic PF marginal
likelihood.

What would overturn this result: a seed/salt mismatch, a hidden resampling
branch, a coordinate transform error, nonfinite gradients at larger horizon or
particle count, or a Claude review finding that the non-XLA gradient route no
longer matches the reviewed scalar equations.

Weakest part of the evidence: the executed gradient validation is intentionally
small (`T=10`, `N=8`, two seeds). It is enough for a G3 gradient-wiring gate,
not enough for HMC readiness or production default selection.
