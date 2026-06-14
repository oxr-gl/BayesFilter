# TF/TFP OT-DPF Rewrite Plan

Date: 2026-05-28

## Decision

`PLAN_DRAFT_FOR_REVIEW`

## Purpose

Build the actual BayesFilter-owned experimental OT-DPF implementation path in
TensorFlow / TensorFlow Probability.  The existing NumPy artifacts under
`experiments/dpf_implementation/` are prototype/reference/comparison smoke
evidence only and are not the default implementation.

Implementation gap addressed by this plan:
`TF_TFP_OT_DPF_IMPLEMENTATION_NOT_BUILT`.

## Evidence Contract

Question: can a TF/TFP finite-Sinkhorn relaxed OT-DPF value and gradient path
reproduce the bounded LGSSM and range-bearing smoke contracts while preserving
same-scalar autodiff gradient checks?

Baseline and comparators:

- LGSSM: Kalman reference for filtered means and log likelihood.
- Range-bearing Gaussian: UKF approximate reference and classical bootstrap PF
  comparator.
- Gradient: same scalar evaluated by `tf.GradientTape` and finite differences
  with fixed observations and common random numbers.

Primary pass criteria:

- algorithmic implementation modules use TensorFlow / TensorFlow Probability,
  not NumPy;
- finite Sinkhorn/entropic OT is implemented in TensorFlow with declared
  epsilon, iteration budget, stabilization mode, tolerance, cost function, and
  target marginal;
- LGSSM and range-bearing runners produce finite JSON outputs and preserve
  reference/comparator checksums;
- Sinkhorn marginal residuals and nonnegativity checks pass stated tolerances;
- `tf.GradientTape` gradient and finite-difference comparator target the same
  named scalar and agree within a reviewed smoke tolerance.

Veto diagnostics:

- any algorithmic implementation file imports NumPy without a reviewed
  exception;
- TensorFlow is imported before the CPU-only device policy is applied in
  CPU-only runners;
- Kalman, UKF, or fixture checksums do not match the result artifact;
- value and gradient paths target different scalars;
- NaN, infinite weights, negative transport mass beyond tolerance, or failed
  marginal residuals appear;
- result text promotes smoke evidence to production, posterior, HMC,
  monograph, banking/model-risk, or public API readiness.

What will not be concluded:

- no production readiness;
- no public API readiness;
- no HMC readiness;
- no posterior correctness;
- no learned/neural OT promotion;
- no banking/model-risk claim;
- no monograph claim without separate review.

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-ot-tf-tfp-*-2026-05-28.md`
- `experiments/dpf_implementation/README.md`
- `experiments/dpf_implementation/tf_tfp/`
- `experiments/dpf_implementation/reports/dpf-ot-tf-tfp-*-2026-05-28.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_*.json`

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `docs/references.bib`
- high-dimensional nonlinear filtering plans, reports, chapters, or sources;
- vendored student code;
- existing NumPy prototype modules except README/report classification updates;
- production API files.

## Implementation Scope

Create a new TF/TFP implementation subtree rather than mutating the NumPy
prototype path:

- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/dpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/bootstrap_pf_tf.py`
- `experiments/dpf_implementation/tf_tfp/fixtures/lgssm_tf.py`
- `experiments/dpf_implementation/tf_tfp/fixtures/range_bearing_tf.py`
- `experiments/dpf_implementation/tf_tfp/references/kalman_lgssm_tf.py`
- `experiments/dpf_implementation/tf_tfp/references/ukf_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_lgssm_ot_dpf_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_range_bearing_ot_dpf_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_gradient_checks_tf.py`

Reference/comparison files may use NumPy only when the file name, module
docstring, and result note label the use as reference/comparator/reporting and
not implementation.

## NumPy Import Gate

Before result acceptance, run:

```bash
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp
```

Expected result: no matches in implementation modules.  Any match is a blocker
unless a reviewed exception explicitly classifies the file as reference,
comparison, closed-form sanity check, serialization, or reporting.

## Runtime Policy

Start CPU-only.  Every CPU-only runner must set `CUDA_VISIBLE_DEVICES=-1`
before importing TensorFlow or TensorFlow Probability, and the result artifact
must record that choice.  GPU/CUDA probes or runs require trusted/escalated
permissions under repo policy.

## Verification Commands

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_ot_dpf_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_range_bearing_ot_dpf_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_gradient_checks_tf
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp
python -m py_compile $(git diff --name-only -- '*.py' | rg '^experiments/dpf_implementation/tf_tfp/')
git diff --check -- docs/plans/bayesfilter-dpf-ot-tf-tfp-*.md experiments/dpf_implementation/README.md experiments/dpf_implementation/tf_tfp experiments/dpf_implementation/reports/dpf-ot-tf-tfp-*.md
git status --short --branch
```

If shell expansion makes `py_compile` ambiguous, replace it with an explicit
list of touched Python files.

## Stop Conditions

Stop and write a structured blocker if:

- TensorFlow / TensorFlow Probability is unavailable in the target environment;
- CPU-only import discipline cannot be enforced;
- the implementation requires NumPy algorithmic code;
- LGSSM, UKF, or fixture references cannot be independently reproduced;
- finite Sinkhorn residuals fail the stated tolerance;
- `tf.GradientTape` cannot target the same scalar as the finite-difference
  comparator;
- any forbidden write set would need edits.

## Review Protocol

Use exactly:

```bash
claude -p --model claude-opus-4-7 --effort max
```

If that command/model/effort is unavailable, stop and report a blocker.  Claude
reviews read-only and returns `ACCEPT` or `REJECT` with findings.  Codex audits
Claude's findings.  If rejected and Codex agrees, patch and resubmit up to five
iterations.  On iteration 5, accept only for user inspection unless a major
blocker remains.  Unresolved objections are risks, not validation.

## Result Artifacts

- `docs/plans/bayesfilter-dpf-ot-tf-tfp-rewrite-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/dpf-ot-tf-tfp-lgssm-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/dpf-ot-tf-tfp-range-bearing-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/dpf-ot-tf-tfp-gradient-check-result-2026-05-28.md`
- JSON outputs under `experiments/dpf_implementation/reports/outputs/`
