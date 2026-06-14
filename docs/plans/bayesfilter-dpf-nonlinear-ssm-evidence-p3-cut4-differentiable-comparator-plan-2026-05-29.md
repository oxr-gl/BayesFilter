# P3 Plan: CUT4 Differentiable Comparator

Date: 2026-05-29

## Decision

`ACCEPTED_BY_CLAUDE_REVIEW_ITERATION_1`

## Evidence Contract

Question: can BayesFilter expose a TF/TFP differentiable CUT4-style deterministic
comparator for one-dimensional innovation filtering?

Comparator: internal finite-difference self-checks and same-scalar GradientTape
contract.

Pass criterion: TF/TFP-only CUT4 component emits deterministic weighted
standard-normal nodes, same-scalar log-normalizer values, and finite gradients
for SV and structural fixtures.

Veto diagnostics: NumPy implementation, non-differentiable scalar, missing
gradient, CUT4 called ground truth, or hidden arbitrary thresholds.

## Inputs

- Current TF/TFP DPF lane.

## Outputs

- `experiments/dpf_implementation/tf_tfp/cubature/__init__.py`
- `experiments/dpf_implementation/tf_tfp/cubature/cut4_tf.py`
- `docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-p3-cut4-differentiable-comparator-result-2026-05-29.md`

## Allowed Write Set

Listed outputs and DPF nonlinear-SSM plan/result artifacts.

## Forbidden Write Set

Production code, tests, monograph chapters, vendored code, high-dimensional
lane, DSGE/NAWM files, NumPy implementation.

## Skeptical Audit Checklist

Use the master checklist.  Pay special attention to CUT4-not-ground-truth
caveat and gradient evidence.

## Stop Conditions

Stop if the component cannot remain TF/TFP-only or cannot support
`tf.GradientTape`.

## Verification Commands

- `rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/cubature`
- `python -m py_compile experiments/dpf_implementation/tf_tfp/cubature/__init__.py experiments/dpf_implementation/tf_tfp/cubature/cut4_tf.py`

## Claude Review Protocol

Use exact Claude command and loop.

## What Must Not Be Concluded

CUT4 is not ground truth; no production, HMC, posterior, DSGE/NAWM, or monograph
claim.
