# Result: Filterflow Legacy Environment Reproduction

## Decision

`EXECUTED_WITH_PARTIAL_BLOCKER`

The external JTT94/filterflow simple-linear LGSSM particle-filter path now runs
from an isolated local environment without modifying filterflow source.  The
original filterflow Kalman helper branch remains blocked by a Python
3.11/modern SciPy compatibility issue in filterflow's pykalman wrapper.

## Evidence Contract Status

Question: can the external JTT94/filterflow LGSSM Section-5.1-style code be run
locally enough to support a later BayesFilter cross-implementation comparison?

Primary comparator: `.localsource/filterflow` commit
`5d8300ba247c4c17e1a301a22560c24fd0670bfe`.

Primary success criterion: an isolated environment under
`.localenv/filterflow-py311/` can import and run the simple-linear particle
filter and regularized transform commands without modifying filterflow source.

Status: pass for original PF and regularized transform paths; blocked for
filterflow's own Kalman helper branch.

What is not concluded: this is not a full Section 5.1 reproduction, not a
BayesFilter correctness result, not a posterior-correctness result, and not
production readiness.

## Run Manifest

| Field | Value |
| --- | --- |
| Date | 2026-05-30 |
| Repo | `/home/chakwong/BayesFilter` |
| Filterflow path | `.localsource/filterflow` |
| Filterflow commit | `5d8300ba247c4c17e1a301a22560c24fd0670bfe` |
| Filterflow status | `## master...origin/master` |
| Environment | `.localenv/filterflow-py311` |
| Python | `3.11.14` |
| CPU/GPU status | CPU-only requested with `CUDA_VISIBLE_DEVICES=-1` |
| Matplotlib cache | `MPLCONFIGDIR=.cache/filterflow-mpl` |
| Source mutation | none in `.localsource/filterflow` |

Selected package versions recorded from inside `.localenv/filterflow-py311`:

| Package | Version |
| --- | --- |
| numpy | `1.26.4` |
| scipy | `1.17.1` |
| tensorflow | `2.19.1` |
| tensorflow_probability | `0.25.0` |
| pandas | `3.0.2` |
| matplotlib | `3.10.8` |
| pykalman | `0.9.5` |
| dm-sonnet | `2.0.2` |
| sonnet | `0.1.6` |
| tensorflow-estimator | `2.15.0` |
| graphs | `0.1.3` |
| gast | `0.3.3` |
| tqdm | `4.67.3` |
| seaborn | `0.13.2` |

Runtime shim used for Python 3.11 compatibility:

```python
import inspect
inspect.getargspec = getattr(inspect, "getargspec", inspect.getfullargspec)
```

## Commands And Results

Import probe:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=.cache/filterflow-mpl \
PYTHONPATH=.localsource/filterflow \
.localenv/filterflow-py311/bin/python -c \
"import inspect; inspect.getargspec = getattr(inspect, 'getargspec', inspect.getfullargspec); from scripts.simple_linear_common import get_data; from scripts.simple_linear_comparison import main; print('filterflow_simple_linear_import_ok')"
```

Result: `filterflow_simple_linear_import_ok`.

The original simple-linear settings recovered from
`.localsource/filterflow/scripts/simple_linear_comparison.py` are:

| Setting | Value |
| --- | --- |
| State dimension | `2` |
| Observation dimension | `2` |
| True transition matrix | `0.5 * I_2` |
| Transition covariance | `I_2` |
| Observation matrix | `I_2` |
| Observation covariance | `0.1 * I_2` |
| Section-style theta grid | `(0.25, 0.25)`, `(0.5, 0.5)`, `(0.75, 0.75)` |
| Default resampling threshold in executed commands | `NeffCriterion(0.5, True)` |
| Regularized transform settings | `scaling=0.9`, `convergence_threshold=1e-3` |

Bounded Section-5.1-style commands were run with:

| Field | Value |
| --- | --- |
| `T` | `150` |
| `batch_size` | `100` |
| `n_particles` | `25` |
| `data_seed` | `111` |
| `filter_seed` | `555` |
| Output scalar | `final_state.log_likelihoods / T` printed by filterflow |

Multinomial PF output:

| theta | mean | std |
| --- | ---: | ---: |
| 0.250 | -4.077 | 0.176 |
| 0.500 | -3.818 | 0.153 |
| 0.750 | -3.938 | 0.198 |

Regularized transform output with `epsilon=0.25`:

| theta | mean | std |
| --- | ---: | ---: |
| 0.250 | -4.077 | 0.179 |
| 0.500 | -3.815 | 0.155 |
| 0.750 | -3.930 | 0.193 |

Regularized transform output with `epsilon=0.5`:

| theta | mean | std |
| --- | ---: | ---: |
| 0.250 | -4.078 | 0.179 |
| 0.500 | -3.817 | 0.154 |
| 0.750 | -3.938 | 0.190 |

Regularized transform output with `epsilon=0.75`:

| theta | mean | std |
| --- | ---: | ---: |
| 0.250 | -4.078 | 0.178 |
| 0.500 | -3.818 | 0.154 |
| 0.750 | -3.943 | 0.189 |

These are filterflow's raw printed per-time log-likelihood summaries, not
errors relative to Kalman.  The next comparison step must subtract or otherwise
align against an exact Kalman reference.

## Structured Blocker: Filterflow Kalman Branch

The filterflow particle-filter paths run, but this command fails:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=.cache/filterflow-mpl \
PYTHONPATH=.localsource/filterflow \
.localenv/filterflow-py311/bin/python -c \
"import inspect; inspect.getargspec = getattr(inspect, 'getargspec', inspect.getfullargspec); from scripts.simple_linear_comparison import main; from scripts.simple_linear_common import ResamplingMethodsEnum; main(ResamplingMethodsEnum.KALMAN, 0.5, T=20, batch_size=5, n_particles=10, data_seed=111, filter_seed=555, savefig=False)"
```

Failure:

```text
TypeError: solve_triangular() takes from 2 to 7 positional arguments but 8 were given
```

Cause: `.localsource/filterflow/scripts/base.py` monkey-patches
`pykalman.utils.linalg.solve_triangular` and forwards `debug` as a positional
argument to the modern SciPy `solve_triangular` signature.  Fixing this inside
filterflow would mutate external source, so this result records it as a
structured blocker rather than patching the checkout.

## Decision Table

| Decision | Status |
| --- | --- |
| Isolated filterflow environment exists | pass |
| Original simple-linear import works | pass |
| Original PF path runs | pass |
| Original regularized transform path runs | pass |
| Filterflow source remains unmodified | pass |
| Filterflow Kalman helper branch runs | blocker |
| Full Section 5.1 reproduction | not yet claimed |

## Next Justified Action

Use this environment for the cross-implementation audit, but compute the exact
Kalman reference outside filterflow's blocked helper path unless we explicitly
approve a non-mutating runtime shim or an external-source patch.  The next audit
should compare filterflow PF/regularized outputs against BayesFilter using the
same LGSSM, theta grid, particle count, resampling threshold, `epsilon`,
`scaling`, Sinkhorn stopping rule, and seed protocol.
