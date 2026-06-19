# Fixed-SGQF Structural Adapter Result

metadata_date: 2026-06-16
plan_reference: `docs/plans/bayesfilter-fixed-sgqf-structural-adapter-plan-2026-06-16.md`
status: EXECUTION_COMPLETE

## Question

Can we build an exact-gated same-target structural adapter that admits
Model-C-class fixtures into the current fixed-SGQF lane while honestly blocking
Model B under the present additive-state assumptions?

## Implemented result

### New adapter module
Created:
- `bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py`

This module now provides an exact-gated structural→fixed-SGQF adapter result
object and a conversion function:
- Model C (`model_c_autonomous_nonlinear_growth`) is admitted as exact-eligible
  for the current lane,
- Model B remains exact-ineligible with an explicit reason string.

### Primary implementation adjustment
Updated:
- `bayesfilter/nonlinear/fixed_sgqf_tf.py`

The state-covariance factorization gate is now semidefinite-capable in the sense
required by the structural adapter pass:
- strictly negative eigenvalues still veto,
- semidefinite directions can be carried by an eigen-factor when they are at or
  above zero but below the old positive-definite threshold.

This was necessary to admit Model C exactly without introducing a fake variance
floor on the deterministic phase coordinate.

### Tests added/updated
Updated:
- `tests/test_nonlinear_benchmark_models_tf.py`
  - Model B exact-ineligible adapter test
  - Model C exact-eligible adapter test
- `tests/test_fixed_sgqf_values_tf.py`
  - first-step structural Model C adapter row against dense reference
- `tests/test_fixed_sgqf_verification_tf.py`
  - adjusted the old large-threshold veto expectation to reflect semidefinite
    acceptance under the new exact adapter policy

### Benchmark harness integration
Updated:
- `docs/benchmarks/benchmark_bayesfilter_v1_nonlinear_filters.py`
  - fixed SGQF level-2 now:
    - runs on Model A,
    - remains explicitly blocked on Model B,
    - now runs on Model C.
- `docs/benchmarks/benchmark_highdim_nonlinear_filtering_smoke.py`
  - fixed SGQF still remains explicitly skipped there because the current smoke
    fixtures are not yet same-target adapter rows for the additive-state lane.

## Verification run

### Structural adapter / fixed SGQF regression subset
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/test_nonlinear_benchmark_models_tf.py \
  tests/test_fixed_sgqf_values_tf.py \
  tests/test_fixed_sgqf_tf.py \
  tests/test_fixed_sgqf_scores_tf.py \
  tests/test_fixed_sgqf_verification_tf.py
```

Observed:
- `39 passed, 2 warnings`

### Nonlinear benchmark harness rerun
```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_bayesfilter_v1_nonlinear_filters.py \
  --requested-device cpu --repeats 1 \
  --output /tmp/fixed_sgqf_nonlinear_benchmark.json \
  --markdown-output /tmp/fixed_sgqf_nonlinear_benchmark.md \
  --plan-path docs/plans/bayesfilter-fixed-sgqf-structural-adapter-plan-2026-06-16.md \
  --result-path docs/plans/bayesfilter-fixed-sgqf-structural-adapter-result-2026-06-16.md
```

Observed fixed-SGQF rows:
- **Model A**: admitted and executed
- **Model B**: explicitly blocked as exact-ineligible
- **Model C**: admitted and executed

### High-dimensional smoke harness rerun
```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_highdim_nonlinear_filtering_smoke.py \
  --output /tmp/fixed_sgqf_highdim_smoke.json \
  --markdown-output /tmp/fixed_sgqf_highdim_smoke.md
```

Observed fixed-SGQF rows:
- explicit skipped rows remain for the smoke fixtures, with same-target adapter
  scope reasons.

## Current adapter verdict by model

| Model | Adapter status | Reason |
| --- | --- | --- |
| Model A affine Gaussian oracle | admitted | already exact and unchanged |
| Model B nonlinear accumulation | blocked | innovation enters the deterministic block through nonlinear completion, so the current additive-state fixed-SGQF lane is not exact same-target |
| Model C autonomous nonlinear growth | admitted | additive noise only on the stochastic coordinate, deterministic phase coordinate carried exactly under semidefinite state handling |

## Interpretation

### What is now supported
1. The current fixed-SGQF lane has an exact-gated structural adapter path.
2. Model C can now be admitted into the nonlinear benchmark harness as a
   same-target fixed-SGQF comparison row.
3. Model B remains honestly blocked rather than being forced into a fake exact
   adapter.
4. The semidefinite deterministic phase coordinate in Model C can be handled
   without introducing an approximate variance floor.

### What remains outside scope
1. Model B exact same-target support is still not available in the current
   additive-state fixed-SGQF lane.
2. Fixed-SGQF score rows are still not integrated into the main nonlinear
   leaderboard artifact.
3. The high-dimensional smoke fixtures are still not exact same-target fixed-SGQF
   adapter rows.

## Diagnostics summary
| Item | Status | Interpretation |
| --- | --- | --- |
| Model A fixed-SGQF benchmark rows | admitted | unchanged exact-reference support |
| Model B fixed-SGQF benchmark rows | blocked | explicit exact-ineligible reason preserved |
| Model C fixed-SGQF benchmark rows | admitted | new structural adapter success |
| highdim smoke fixed-SGQF rows | skipped | still outside same-target adapter scope |
| regression subset | `39 passed, 2 warnings` | adapter integration did not break core fixed-SGQF rows |

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| close this structural-adapter pass as a successful exact-gated extension | satisfied | no fake Model B exactness; no hidden scope drift | how far the adapter should extend beyond Model C and whether score rows should join the benchmark next | use Model C as the first admitted structural nonlinear fixed-SGQF benchmark row; keep Model B and smoke rows explicitly blocked until a richer lane exists | no claim that fixed SGQF now exactly represents the whole nonlinear model suite |

## Recommended next step
If full nonlinear-suite coverage is still desired, the next major engineering
choice is not another small adapter tweak. It is deciding whether to build a
richer fixed-SGQF lane that integrates over structural state+innovation rather
than only over the current additive-state form. Until then:
- Model A: admitted,
- Model C: admitted,
- Model B: honestly blocked,
- smoke fixtures: honestly blocked.
