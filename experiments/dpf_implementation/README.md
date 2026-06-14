# Experimental DPF Implementation

This directory contains BayesFilter-owned experimental DPF evidence artifacts
and NumPy prototype/reference/comparison smoke code.  It is not production
`bayesfilter` code and does not define a public API.

## Backend Status

BayesFilter's default algorithmic implementation backend is TensorFlow /
TensorFlow Probability.  The current OT-DPF Python artifacts in this directory
use NumPy and are therefore classified as prototype/reference/comparison smoke
evidence only.  They are not the BayesFilter-owned default implementation.

Actual implementation gap: `TF_TFP_OT_DPF_IMPLEMENTATION_NOT_BUILT`.

Future DPF implementation work must build the finite-Sinkhorn OT-DPF path in
TF/TFP and must keep NumPy limited to reference solutions, comparison fixtures,
closed-form sanity checks, serialization/reporting, or reviewed exceptions.

Update: the experimental TF/TFP OT-DPF implementation path now lives under
`experiments/dpf_implementation/tf_tfp/`.  It is still experimental and not
production `bayesfilter` code, but it is the BayesFilter-owned backend-compliant
implementation lane for the current OT-DPF evidence.

Current artifacts:

- stochastic-volatility smoke fixture and classical bootstrap/SIR PF runner;
- LGSSM fixture with Kalman reference;
- Gaussian range-bearing fixture with UKF approximate reference;
- classical bootstrap/SIR PF and finite-Sinkhorn relaxed OT-DPF NumPy prototype
  runners;
- TF/TFP classical bootstrap PF and finite-Sinkhorn relaxed OT-DPF runners under
  `tf_tfp/`;
- finite-difference same-scalar gradient check for a named relaxed OT-DPF
  proxy scalar;
- JSON and markdown reports under `reports/`.

The first stochastic-volatility smoke test is CPU-only, uses fixed seeds, and
compares a small candidate bootstrap PF panel against a high-particle bootstrap
PF engineering reference.  The reference is not exact posterior truth.

No HMC, posterior correctness, learned resampling, neural OT, banking,
model-risk, production, or monograph-validity claim follows from this directory.

The finite-Sinkhorn OT-DPF path is a relaxed finite-budget entropic transport
diagnostic.  It is not exact categorical resampling and not exact unregularized
optimal transport.
