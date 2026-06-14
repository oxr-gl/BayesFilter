# Plan: 1D LGSSM Horizon Ladder

## Scope

Extend the controlled scalar-state LGSSM diagnostic from `T=2` to `T=4`,
without changing production code or the prior `T=2` result artifact. This stays
inside the BayesFilter-owned experimental DPF lane.

Forbidden edits:

- production `bayesfilter/`;
- `tests/`;
- monograph chapters under `docs/chapters/`;
- high-dimensional nonlinear filtering lane artifacts;
- vendored student code;
- DSGE/NAWM artifacts;
- `.localsource/filterflow` source.

## Evidence Contract

Question: as the controlled 1D scalar-state fixture moves from `T=2` to `T=4`,
do BayesFilter TF/TFP annealed transport and the current local patched
filterflow executable still agree on the forward scalar ledger?

Primary comparator: current local patched `.localsource/filterflow` executable
reference on branch `bayesfilter-py311-compat`.

Primary pass criterion: for each horizon, BayesFilter and filterflow agree on:

- resampling trigger pattern;
- predicted particles;
- observation log likelihoods;
- normalized log weights;
- transport cost matrix and transport matrix;
- post-transport particles;
- per-step log normalizers;
- total scalar;
- absolute row/column residual bounds.

Gradient diagnostics are recorded but are not promotion criteria. AD-vs-FD
mismatch remains diagnostic only.

Veto diagnostics:

- filterflow subprocess cannot run;
- non-finite scalar or gradient;
- BayesFilter/filterflow trigger mismatch;
- forward ledger exceeds predeclared tolerances;
- absolute transport residuals exceed tolerance.

Explanatory diagnostics:

- observed trigger pattern;
- AD gradient, finite-difference gradient, and AD-vs-FD deltas;
- BayesFilter iteration counts where available;
- filterflow checkout provenance.

Not concluded:

- production readiness;
- public API readiness;
- posterior correctness;
- HMC readiness;
- general nonlinear-SSM validity;
- smoothness-surface gradient agreement;
- transport-map derivative correctness.

## Fixed Fixtures

Common settings:

- `theta0 = 0.7`;
- `Q = 0.04`;
- `R = 0.04`;
- `N = 4`;
- initial particles `[-1.5, -0.2, 0.4, 1.2]`;
- ESS threshold `0.9999 * N`;
- epsilon `0.25`;
- scaling `0.9`;
- convergence threshold `1e-6`;
- max iterations `200`;
- finite-difference step `1e-4`.

Horizon ladder:

| Scenario | Horizon | Observations | Transition noises |
| --- | ---: | --- | --- |
| `T2_anchor` | 2 | `[0.05, -0.1]` | `[[0.0, 0.1, -0.2, 0.3], [0.2, -0.1, 0.0, -0.3]]` |
| `T4_extension` | 4 | `[0.05, -0.1, 0.08, -0.04]` | T2 noises plus `[[-0.1, 0.0, 0.25, -0.15], [0.15, -0.25, 0.05, 0.1]]` |

## Outputs

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_lgssm_horizon_ladder_tf.py`;
- `experiments/dpf_implementation/reports/dpf-filterflow-1d-lgssm-horizon-ladder-2026-06-01.md`;
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_1d_lgssm_horizon_ladder_2026-06-01.json`;
- `docs/plans/bayesfilter-dpf-1d-lgssm-horizon-ladder-result-2026-06-01.md`.

## Skeptical Audit

- This does not answer the full smoothness LGSSM failure; it only extends the
  scalar-state microscope one step toward longer horizon behavior.
- Trigger pattern is observed and compared, not pre-promoted.
- Finite gradients do not establish gradient correctness.
- Agreement with current patched filterflow is executable-reference agreement,
  not pristine upstream proof.
- The T4 fixture is hand-written and diagnostic; it is not a tuned benchmark.

Audit status: proceed with a bounded CPU-only runner and record any mismatch as
diagnostic, not as production evidence.

## Verification

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_lgssm_horizon_ladder_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_lgssm_horizon_ladder_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_lgssm_horizon_ladder_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_1d_lgssm_horizon_ladder_2026-06-01.json >/dev/null
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_lgssm_horizon_ladder_tf.py
rg -n "^\\s*(from|import)\\s+.*(student|vendored|vendor|highdim|dsge|DSGE|nawm|NAWM)" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_lgssm_horizon_ladder_tf.py
rg -n "[ \t]$" docs/plans/bayesfilter-dpf-1d-lgssm-horizon-ladder-*.md experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_lgssm_horizon_ladder_tf.py experiments/dpf_implementation/reports/dpf-filterflow-1d-lgssm-horizon-ladder-2026-06-01.md
git diff --check
git status --short -- bayesfilter tests docs/chapters
```
