# P5 Plan: TF/TFP LEDH Flow Implementation

Date: 2026-05-29

## Decision

`DRAFT_FOR_CLAUDE_REVIEW`

## Evidence Contract

Question: can a TF/TFP-only LEDH affine local Gaussian flow component be built
under `experiments/dpf_implementation/tf_tfp/flows/`?

Baseline/comparator: P1-P4 contracts and existing TF/TFP fixtures.

Pass criterion: implementation exposes local Gaussian map, range-bearing
Jacobian, Gaussian log-density helpers, log-det diagnostics, and finite checks
with no NumPy imports.

Veto diagnostics: NumPy import, non-TF implementation path, singular covariance
without structured blocker, missing log-det, or hidden production edits.

Not concluded: integrated filter validity, nonlinear correctness, production
readiness.

## Inputs

- P1-P4 result artifacts.
- `experiments/dpf_implementation/tf_tfp/fixtures/lgssm_tf.py`
- `experiments/dpf_implementation/tf_tfp/fixtures/range_bearing_tf.py`

## Outputs

- `experiments/dpf_implementation/tf_tfp/flows/__init__.py`
- `experiments/dpf_implementation/tf_tfp/flows/jacobians_tf.py`
- `experiments/dpf_implementation/tf_tfp/flows/ledh_tf.py`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p5-tf-tfp-ledh-flow-implementation-result-2026-05-29.md`

## Allowed Write Set

- listed output files;
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-*-2026-05-29.md`

## Forbidden Write Set

Production code, vendored code, monograph chapters, high-dimensional lane
artifacts, NumPy algorithm paths, and unrelated TF/TFP modules.

## Skeptical Audit Checklist

Check stale context, wrong default architecture, bootstrap-proposal overclaim,
OT-resampling overclaim, missing stop conditions, hidden production drift,
monograph drift, vendored-code contamination, high-dimensional-lane
contamination, and artifact fitness.

## Stop Conditions

Stop if TF/TFP cannot support the flow in eager mode, if Cholesky stabilization
would hide invalid covariance, or if implementation needs NumPy.

## Verification Commands

- `rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/flows`
- `python -m py_compile experiments/dpf_implementation/tf_tfp/flows/__init__.py experiments/dpf_implementation/tf_tfp/flows/jacobians_tf.py experiments/dpf_implementation/tf_tfp/flows/ledh_tf.py`

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to max five
iterations with Codex audit.

## What Must Not Be Concluded

No integrated filter, production, HMC, posterior, NAWM-scale, or monograph claim.
