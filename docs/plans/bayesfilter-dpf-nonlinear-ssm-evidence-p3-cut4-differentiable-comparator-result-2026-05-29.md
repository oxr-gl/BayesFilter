# P3 Result: CUT4 Differentiable Comparator

Date: 2026-05-29

## Decision

`ACCEPTED_EXECUTED`

## Evidence Contract Result

Added a TF-only one-dimensional CUT4-style symmetric Gaussian cubature component
under `experiments/dpf_implementation/tf_tfp/cubature/`.  The component returns
nodes `[-sqrt(3), 0, sqrt(3)]` and weights `[1/6, 2/3, 1/6]`, exact for
standard-normal moments through degree 5 in one dimension.  It is used as a
differentiable deterministic comparator, not ground truth.

## Artifacts

- `experiments/dpf_implementation/tf_tfp/cubature/__init__.py`
- `experiments/dpf_implementation/tf_tfp/cubature/cut4_tf.py`
- `experiments/dpf_implementation/tf_tfp/references/cut4_sv_tf.py`
- `experiments/dpf_implementation/tf_tfp/references/cut4_structural_tf.py`

## Verification

- `python -m py_compile` over touched CUT4/reference files: passed.
- NumPy import gate over `experiments/dpf_implementation/tf_tfp`: final P7 gate records status.
- SV and structural phases verified `tf.GradientTape` gradients through CUT4 same-scalar values.

## Caveats

CUT4 is a differentiable comparator, not ground truth.  It does not establish
posterior correctness, HMC readiness, production readiness, DSGE/NAWM
validation, or monograph claims.
