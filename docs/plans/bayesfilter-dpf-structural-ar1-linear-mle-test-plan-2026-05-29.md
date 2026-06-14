# DPF Structural AR(1) Linear MLE Test Plan

Date: 2026-05-29

## Decision

`EXECUTE_NARROW_LINEAR_MLE_TEST`

## Evidence Contract

Question: when `c = d = 0`, so the structural AR(1) completion model is
linear-Gaussian with singular process noise, do the TF/TFP LEDH-PF-PF-OT path
and an exact Kalman comparator agree on the one-parameter MLE/gradient evidence
for `b` at smoke scale?

Model:

- `m_t = rho m_{t-1} + sigma eps_t`
- `k_t = a k_{t-1} + b m_t`
- `y_t = k_t + lambda m_t + eta_t`

Comparator: exact TF Kalman likelihood for the two-dimensional linear Gaussian
state, with process covariance induced by the single `eps_t` shock.  The Kalman
path is the reference for this linear fixture only.

Primary criterion: record same-scalar negative log-likelihood values,
`tf.GradientTape` gradients, coarse-grid MLEs for `b`, observed-information SE,
and standard-error scaled MLE distance.  This is a smoke-scale test, not a
final universal equivalence threshold.

Veto diagnostics: non-finite Kalman/DPF scalar or gradient, invalid observed
information, nonzero structural deterministic residual, invalid Sinkhorn
residual, CPU-only manifest missing, NumPy implementation backend, or any
production/vendored/high-dimensional/DSGE/NAWM drift.

## Inputs

- Existing structural AR(1) fixture helpers.
- Existing LEDH-PF-PF-OT structural runner logic.
- Existing TF/TFP DPF lane policy and nonlinear-SSM evidence ladder.

## Outputs

- `experiments/dpf_implementation/tf_tfp/references/kalman_structural_ar1_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_structural_ar1_linear_kalman_ledh_mle_tf.py`
- `experiments/dpf_implementation/reports/dpf-structural-ar1-linear-mle-result-2026-05-29.md`
- `experiments/dpf_implementation/reports/outputs/dpf_structural_ar1_linear_mle_2026-05-29.json`
- `docs/plans/bayesfilter-dpf-structural-ar1-linear-mle-test-result-2026-05-29.md`

## Allowed Write Set

- Listed outputs.
- Existing experimental TF/TFP DPF lane files only if a small helper extension
  is required.

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- high-dimensional nonlinear filtering lane artifacts;
- vendored student code;
- DSGE/NAWM model implementations;
- production API files;
- NumPy implementation backend.

## Skeptical Audit

| Check | Status | Notes |
| --- | --- | --- |
| stale context | pass | Uses current TF/TFP LEDH-PF-PF-OT structural artifacts and the P6 blocker. |
| wrong comparator | pass | Exact Kalman is the right comparator once `c=d=0`; CUT4 is not primary here. |
| proxy overclaim | pass | MLE/gradient is central; RMSE is not used as promotion evidence. |
| arbitrary threshold | pass | SE-scaled distance is reported for calibration, not final universal threshold. |
| missing stop conditions | pass | Veto diagnostics cover scalar/gradient/information/residual/OT failures. |
| production drift | pass | Production writes forbidden. |
| monograph drift | pass | No chapter edits. |
| vendored/highdim drift | pass | No student/highdim sources used. |
| DSGE/NAWM drift | pass | Toy structural model only. |
| artifact fitness | pass | Linear case directly tests the simpler MLE agreement question. |

## Verification Commands

- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_ar1_linear_kalman_ledh_mle_tf`
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_ar1_linear_kalman_ledh_mle_tf --validate-only`
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_ar1_linear_kalman_ledh_mle_tf --check-reproducibility`
- `python -m py_compile` over touched Python files.
- `python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_structural_ar1_linear_mle_2026-05-29.json`
- `rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp`
- `git diff --check`
- `git status --short -- bayesfilter tests`

## What Must Not Be Concluded

No nonlinear structural equivalence, DSGE/NAWM validation, production readiness,
public API readiness, HMC readiness, posterior correctness, banking/model-risk
claim, or monograph claim is concluded.
