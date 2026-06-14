# DPF Structural-SSM Interface Result

Date: 2026-05-29

## Decision

`EXECUTED_WITH_LINEAR_POLICY_FIX_AND_NONLINEAR_CUT4_MISMATCH_REMAINING`

## Evidence Contract Result

Implemented an experimental TF/TFP structural SSM interface under
`experiments/dpf_implementation/tf_tfp/structural/`.  The interface separates
the stochastic/exogenous block `z_t` from the deterministic/endogenous
completion block `s_t`, evaluates target/proposal densities over `z_t` only,
evaluates observation likelihood on completed state `(z_t, s_t)`, and records
completion residuals as veto diagnostics.

## Files Changed

- `experiments/dpf_implementation/tf_tfp/structural/__init__.py`
- `experiments/dpf_implementation/tf_tfp/structural/contracts_tf.py`
- `experiments/dpf_implementation/tf_tfp/structural/particle_state_tf.py`
- `experiments/dpf_implementation/tf_tfp/structural/resampling_policies_tf.py`
- `experiments/dpf_implementation/tf_tfp/structural/structural_filter_tf.py`
- `experiments/dpf_implementation/tf_tfp/structural/models/structural_ar1_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_structural_interface_linear_ar1_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_structural_interface_nonlinear_ar1_tf.py`

## Structural Contract Implemented

| Contract item | Status |
| --- | --- |
| stochastic block `z_t` declared | implemented for `m_t` |
| deterministic completion block `s_t` declared | implemented for `k_t` |
| transition target density | stochastic `z_t` only |
| proposal density | stochastic `z_t` only |
| flow log-det | stochastic `z_t` block only |
| observation likelihood | completed `(z_t, s_t)` state |
| deterministic residual | recorded before and after resampling policy |
| no density on deterministic block | recorded in diagnostics |

## Resampling Policies Tested

- `none`
- `categorical_ancestor`
- `sinkhorn_current_z`
- `sinkhorn_full_context`, labelled as the old/ad hoc full-context relaxed
  comparator.

## Linear Structural AR(1), `c=d=0`

Comparator: exact TF Kalman.  Kalman grid MLE for `b`: `0.65`.

| Policy | DPF median grid MLE `b` | SE-scaled distance | DPF gradient at true `b` | max residual |
| --- | ---: | ---: | ---: | ---: |
| `none` | 0.65 | 0.0 | 0.633403472425357 | 0.0 |
| `categorical_ancestor` | 0.65 | 0.0 | -0.014472143449953068 | 0.0 |
| `sinkhorn_current_z` | 0.8 | 0.62877289267674 | -4.100836252821147 | 0.0 |
| `sinkhorn_full_context` | 0.8 | 0.62877289267674 | -4.133094039750198 | 0.0 |

Interpretation: the structural interface isolates the previous linear MLE shift
to relaxed Sinkhorn resampling policies.  No-resampling and categorical
ancestor policies match the exact Kalman grid MLE at smoke scale.  This is not
production validation; it is a strong debugging result for the structural DPF
lane.

JSON: `experiments/dpf_implementation/reports/outputs/dpf_structural_interface_linear_ar1_2026-05-29.json`.

## Nonlinear Structural AR(1)

Comparator: differentiable TF/TFP CUT4, not ground truth.  CUT4 grid MLE for
`b`: `0.65`.

| Policy | DPF median grid MLE `b` | SE-scaled distance | DPF gradient at true `b` | max residual |
| --- | ---: | ---: | ---: | ---: |
| `none` | 0.35 | 1.196399784219709 | 4.063071730686302 | 0.0 |
| `categorical_ancestor` | 0.35 | 1.196399784219709 | 4.386400293173679 | 0.0 |
| `sinkhorn_current_z` | 0.35 | 1.196399784219709 | 4.1679224978955345 | 0.0 |
| `sinkhorn_full_context` | 0.35 | 1.196399784219709 | 4.109861800494036 | 0.0 |

Interpretation: the nonlinear CUT4-vs-DPF mismatch remains across all tested
policies.  Because CUT4 is a comparator, not ground truth, this is not evidence
against the DPF idea by itself.  It is evidence that the next nonlinear step
needs a stronger comparator/self-consistency check or a finer particle/seed
ladder before estimator-equivalence language is used.

JSON: `experiments/dpf_implementation/reports/outputs/dpf_structural_interface_nonlinear_ar1_2026-05-29.json`.

## Verification Run

- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_interface_linear_ar1_tf`: passed.
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_interface_linear_ar1_tf --validate-only`: passed.
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_interface_linear_ar1_tf --check-reproducibility`: passed.
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_interface_nonlinear_ar1_tf`: passed.
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_interface_nonlinear_ar1_tf --validate-only`: passed.
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_interface_nonlinear_ar1_tf --check-reproducibility`: passed.
- `python -m py_compile` over touched structural/runners files: passed.

TensorFlow emitted CUDA plugin/cuInit startup messages despite CPU hiding; the
runner manifests record CPU-only execution, `CUDA_VISIBLE_DEVICES=-1` before
TensorFlow import, and no visible GPUs.

## Claude Review Record

- Plan iteration 1: `ACCEPT`.
- Result iteration 1: `ACCEPT`.

## Caveats

No production readiness, public API readiness, HMC readiness, posterior
correctness, DSGE/NAWM validation, banking/model-risk claim, or monograph claim
is concluded.  CUT4 is a differentiable comparator, not ground truth.  Exact
Kalman validates only the `c=d=0` structural toy fixture.

## Next Justified Action

For the linear structural path, promote `categorical_ancestor` as the baseline
structural resampling policy and treat relaxed Sinkhorn policies as requiring a
separate bias-correction design before estimator use.  For the nonlinear path,
run a reviewed comparator-strengthening plan: CUT4 self-consistency, finer
`b` grid, particle-count/seed ladder, and if possible an independent
high-accuracy one-dimensional reference before interpreting the DPF/CUT4 MLE
gap.
