# Filterflow Float64 Reference Probe Plan

## Goal

Test whether an experimental float64 filterflow variant preserves the
Section-5.1-style LGSSM table scale closely enough to be useful as a debugging
reference for BayesFilter/filterflow difference audits.

## Evidence Contract

- Question: does a float64 execution variant of the local executable filterflow
  LGSSM table preserve the canonical float32 filterflow paper-table-scale
  outputs for Kalman, PF, and RegularisedTransform?
- Comparator: canonical local executable filterflow float32 run on the same
  Section-5.1-style settings and fixed seeds.
- Primary criterion: every float64 PF and RegularisedTransform epsilon/theta
  cell has per-time mean-error delta within one canonical float32 Monte Carlo
  standard deviation, and Kalman per-time log-likelihoods differ by less than
  `1e-6`.
- Veto diagnostics: float64 variant cannot run without mutating
  `.localsource/filterflow`; non-finite log likelihoods; dtype-mixing errors;
  missing fixed seed controls; float64 table rows outside the canonical
  float32 Monte Carlo band.
- Explanatory diagnostics: per-cell mean-error deltas, per-cell standard
  deviations, max absolute deltas, package versions, filterflow commit, and
  whether the float64 variant required in-memory monkeypatches.
- Not concluded: paper correctness, production readiness, posterior
  correctness, gradient correctness, or that float64 is pristine upstream
  filterflow.
- Artifact: result JSON under
  `experiments/dpf_implementation/reports/outputs/` and result note under
  `docs/plans/`.

## Exact Settings

- Local executable filterflow checkout: `.localsource/filterflow`.
- Environment: `.localenv/filterflow-py311/bin/python`.
- CPU-only: `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import.
- LGSSM: transition matrix `0.5 I_2` for data generation, transition
  covariance executable `I_2`, observation matrix `I_2`, observation
  covariance `0.1 I_2`.
- Horizon `T=150`, particles `N=25`, realizations `100`.
- Theta grid: `0.25`, `0.5`, `0.75`.
- Epsilon grid: `0.25`, `0.5`, `0.75`.
- Seeds: `data_seed=111`, `filter_seed=555`.
- RegularisedTransform kwargs: `scaling=0.9`,
  `convergence_threshold=1e-3`, `max_iter=100`.

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-filterflow-float64-reference-probe-plan-2026-06-03.md`
- `docs/plans/bayesfilter-dpf-filterflow-float64-reference-probe-result-2026-06-03.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_reference_probe_tf.py`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_reference_probe_2026-06-03.json`

## Forbidden Write Set

- Production `bayesfilter/`.
- `tests/`.
- Monograph chapters under `docs/chapters/`.
- High-dimensional nonlinear filtering lane.
- Vendored student code.
- `.localsource/filterflow` source files.

## Skeptical Pre-Execution Audit

| Risk | Control |
| --- | --- |
| Wrong baseline | Compare float64 only against canonical local executable filterflow float32, not against BayesFilter or paper table alone. |
| Dtype wrapper overclaims upstream status | Label float64 as an experimental in-memory execution variant. |
| Seed drift mistaken for dtype drift | Use the same `data_seed` and `filter_seed`; record the seeds. |
| Bitwise equality overrequired | Use table-scale Monte Carlo-band agreement, not per-realization equality. |
| Hidden source contamination | Do not edit `.localsource/filterflow`; run patches only in the subprocess. |
| Float64 random stream differs | Treat PF/RegularisedTransform as Monte Carlo comparison; Kalman is the deterministic tight check. |
| Artifact would not answer question | Emit float32 rows, float64 rows, per-cell deltas, decision, and manifest. |

The plan passes the skeptical audit because it directly tests the proposed
policy change under the same table settings while preserving the canonical
float32 reference.

## Phase Order

1. Implement a bounded runner that executes canonical float32 filterflow and an
   experimental float64 filterflow variant.
2. Keep all float64 changes in-memory inside the subprocess.
3. Compare deterministic Kalman rows and stochastic PF/RegularisedTransform
   rows against the canonical float32 Monte Carlo band.
4. Write JSON and result note.
5. Run verification commands.

## Stop Conditions

- Missing `.localenv/filterflow-py311/bin/python`.
- Float64 execution requires editing `.localsource/filterflow`.
- TensorFlow/TFP or filterflow import failure.
- Non-finite outputs.
- Float64 output falls outside the canonical float32 Monte Carlo band.

## Verification Commands

- `python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_reference_probe_tf.py`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_reference_probe_tf`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_reference_probe_tf --validate-only`
- JSON parse/schema check for the output file.
- NumPy import gate over touched BayesFilter TF/TFP file allowing external
  filterflow subprocess/reporting exceptions only.
- Import-boundary search for student/vendored/highdim/DSGE/NAWM imports.
- Lane-scoped trailing whitespace check.
- `git diff --check`.
- `git status --short -- bayesfilter tests docs/chapters`.
- `git status --short --branch`.
