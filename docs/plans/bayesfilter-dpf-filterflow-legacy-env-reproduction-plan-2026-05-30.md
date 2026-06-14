# Plan: Filterflow Legacy Environment Reproduction

## Decision

`PLAN_READY_FOR_EXECUTION`

## Evidence Contract

Question: can the external JTT94/filterflow LGSSM Section-5.1-style code be
run in an isolated local environment so BayesFilter can compare against an
executable original implementation rather than only source-level inspection?

Primary comparator: `.localsource/filterflow` at commit
`5d8300ba247c4c17e1a301a22560c24fd0670bfe`.

Primary success criterion: a local environment under `.localenv/` can import
`scripts.simple_linear_common`, construct the simple-linear LGSSM driver, and
run a bounded original-filterflow LGSSM command without modifying filterflow
source.

Veto diagnostics:

- environment writes outside `.localenv/`, `.cache/`, `docs/plans/`, or
  `experiments/dpf_implementation/reports/`;
- production `bayesfilter/`, `tests/`, vendored student code, monograph
  chapters, or high-dimensional lane edits;
- filterflow source modifications;
- TensorFlow/TFP import incompatibility that prevents original filterflow from
  importing;
- missing dependency cannot be installed in the isolated environment;
- bounded LGSSM smoke command fails before producing finite output.

Explanatory diagnostics: Python version, TensorFlow version, TensorFlow
Probability version, NumPy version, pykalman version, import warnings,
Matplotlib cache behavior, and whether the run uses current system packages or
fully local packages.

What will not be concluded: no BayesFilter OT-DPF correctness, no Section 5.1
full reproduction, no production readiness, no HMC readiness, and no claim that
filterflow or Corenflos is wrong.

## Allowed Write Set

- `.localenv/filterflow-py311/`
- `.cache/filterflow-mpl/`
- `docs/plans/bayesfilter-dpf-filterflow-legacy-env-reproduction-plan-2026-05-30.md`
- `docs/plans/bayesfilter-dpf-filterflow-legacy-env-reproduction-result-2026-05-30.md`
- `experiments/dpf_implementation/reports/filterflow-legacy-env-smoke-2026-05-30.md`
- `experiments/dpf_implementation/reports/outputs/filterflow_legacy_env_smoke_2026-05-30.json`

## Forbidden Write Set

- production `bayesfilter/`
- `tests/`
- vendored student code
- `.localsource/filterflow/` source files
- monograph chapters under `docs/chapters/`
- high-dimensional nonlinear filtering lane files
- global Python or conda package directories

## Method

1. Confirm filterflow checkout commit and clean status.
2. Create a local virtual environment at `.localenv/filterflow-py311` using
   `--system-site-packages` to reuse the existing TensorFlow/TFP stack while
   keeping new dependency writes local.
3. Install only the missing direct dependencies needed for the simple-linear
   driver, starting with `pykalman` and `attrs`, into that environment.
4. Record package versions from inside the environment.
5. Probe imports with:
   `PYTHONPATH=.localsource/filterflow python -c "from scripts.simple_linear_common import get_data"`.
6. Run a bounded original filterflow command for the simple-linear LGSSM without
   modifying filterflow source:
   call `scripts.simple_linear_comparison.main` with `T=150`, `batch_size=100`,
   `n_particles=25`, `data_seed=111`, `filter_seed=555`, and
   `RegularisedTransform` epsilon values where feasible.
7. If the full 3-by-3 grid is too slow or fails, record the first smallest
   failing command and stop with a structured blocker.
8. Write result artifacts with command, environment manifest, output excerpt,
   and blocker or success classification.

## Skeptical Pre-Execution Audit

| Risk | Status | Mitigation |
| --- | --- | --- |
| stale context | pass | Prior cross-audit result and filterflow dependency files were read. |
| wrong target | pass | Target is external filterflow execution only, not BayesFilter implementation. |
| environment contamination | watch | Use `.localenv/filterflow-py311`; do not install globally. |
| wrong backend policy | pass | This is external comparison code, not BayesFilter-owned implementation. |
| overclaiming smoke as reproduction | pass | Smoke success only means executable filterflow path exists. |
| hidden production drift | pass | Forbidden write set excludes `bayesfilter/` and `tests/`. |
| vendored/highdim/monograph drift | pass | Forbidden write set excludes those paths. |
| dependency resolver drift | watch | Record exact installed versions and stop on unresolved incompatibility. |

## Verification Commands

- `git -C .localsource/filterflow rev-parse HEAD`
- `git -C .localsource/filterflow status --short --branch`
- `.localenv/filterflow-py311/bin/python -c "import tensorflow as tf; import tensorflow_probability as tfp; import pykalman; print(tf.__version__, tfp.__version__, pykalman.__version__)"`
- `PYTHONPATH=.localsource/filterflow .localenv/filterflow-py311/bin/python -c "from scripts.simple_linear_common import get_data; print('ok')"`
- bounded `scripts.simple_linear_comparison.main` command
- `git status --short -- .localsource/filterflow bayesfilter tests docs/chapters`
- `git diff --check`
- `git status --short --branch`

## Stop Conditions

- local environment cannot be created;
- dependency install fails after one escalated retry;
- TensorFlow/TFP import cannot work in the environment;
- `pykalman` cannot import in the environment;
- original filterflow simple-linear imports fail after installing required
  missing dependencies;
- original filterflow bounded command fails due API incompatibility that would
  require modifying filterflow source;
- any forbidden write would be required.
