# DPF Structural AR(1) Linear MLE Test Result

Date: 2026-05-29

## Decision

`DPF_STRUCTURAL_AR1_LINEAR_MLE_ESTIMATION_CALIBRATION_WARNING`

## Evidence Contract Result

The `c=d=0` structural AR(1) completion model was tested as a linear-Gaussian
SSM with an exact TF Kalman comparator.  This is the right first check before
interpreting the nonlinear structural CUT4 discrepancy.

Model:

- `m_t = rho m_{t-1} + sigma eps_t`
- `k_t = a k_{t-1} + b m_t`
- `y_t = k_t + lambda m_t + eta_t`

The exact Kalman comparator and LEDH-PF-PF-OT DPF evaluated the same fixed
observations and the same named scalar:
`structural_ar1_linear_negative_log_likelihood_b_parameter_tf`.

## Decision Table

| Check | Status | Evidence |
| --- | --- | --- |
| exact Kalman comparator available | pass | finite value and gradient |
| DPF same-scalar path available | pass | finite value and gradient |
| deterministic completion residual | pass | max residual `0.0` |
| Sinkhorn residual | pass | max residual `2.7479581110601004e-12` |
| MLE agreement | warning | Kalman grid MLE `0.65`; DPF median grid MLE `0.8` |
| SE-scaled MLE distance | calibration | `0.62877289267674` |

## Metrics

| Diagnostic | Kalman | DPF |
| --- | ---: | ---: |
| value at true `b=0.65` | 7.099395386722153 | 7.693164860550011 |
| GradientTape gradient at true `b` | -0.35086306423226066 | -4.04235916084723 |
| grid MLE `b` | 0.65 | 0.8 median over seeds |

DPF seed grid MLEs were `[0.8, 0.8, 0.8]`.  Kalman grid values over
`[0.35, 0.50, 0.65, 0.80, 0.95]` were
`[8.697582312501545, 7.4125848592667865, 7.099395386722153, 7.202733825788014, 7.508262328050101]`.

## Interpretation

The simple linear structural case does not yet show MLE agreement between exact
Kalman and the current finite-particle LEDH-PF-PF-OT path.  Because the
deterministic residual and Sinkhorn residual checks pass, the discrepancy is
not explained by silently breaking the structural completion equation.  The
next debugging target is the DPF proposal/resampling/correction path in this
linear structural setting, especially finite-Sinkhorn relaxed resampling and
whether the PF-PF correction remains unbiased after structural-context
barycentric recompletion.

## Run Manifest

- Command: `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_ar1_linear_kalman_ledh_mle_tf`
- Validate command: `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_ar1_linear_kalman_ledh_mle_tf --validate-only`
- Reproducibility command: `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_ar1_linear_kalman_ledh_mle_tf --check-reproducibility`
- CPU-only status: `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import; runner manifest records no visible GPUs.
- JSON output: `experiments/dpf_implementation/reports/outputs/dpf_structural_ar1_linear_mle_2026-05-29.json`
- Report output: `experiments/dpf_implementation/reports/dpf-structural-ar1-linear-mle-result-2026-05-29.md`

TensorFlow emitted CUDA plugin/cuInit startup messages despite CPU hiding; the
run manifest records CPU-only execution.

## What This Does Not Conclude

No nonlinear structural equivalence, DSGE/NAWM validation, production
readiness, public API readiness, HMC readiness, posterior correctness,
banking/model-risk claim, or monograph claim is concluded.

## Next Justified Action

Before increasing nonlinear structural particle-count ladders, run a linear
structural ablation ladder: exact Kalman vs DPF with no resampling, categorical
resampling, and finite-Sinkhorn relaxed resampling at increasing particle
counts.  The goal is to isolate whether the MLE shift comes from the local flow,
PF-PF correction, finite particles, or relaxed OT structural recompletion.
