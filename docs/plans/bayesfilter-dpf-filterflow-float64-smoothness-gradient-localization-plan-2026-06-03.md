# FilterFlow Float64 Smoothness Gradient Localization Plan

## Question

Where does the BayesFilter TF/TFP gradient path first diverge from the local
float64 FilterFlow executable on the first failing `simple_linear_smoothness`
row, `theta=[0.95, 0.95]`?

This is a cross-implementation difference audit only.  It does not assert that
either implementation is mathematically correct.

## Evidence Contract

- Comparator: local executable FilterFlow checkout on branch
  `bayesfilter-py311-float64-reference`.
- BayesFilter backend: TensorFlow / TensorFlow Probability only.
- Primary artifact: per-time cumulative scalar and diagonal-gradient ledger for
  the first failing smoothness row.
- Primary success criterion: identify the first cumulative time index where the
  BayesFilter raw gradient diverges from FilterFlow while the scalar path
  remains aligned.
- Veto diagnostics: FilterFlow reference drift, scalar mismatch before gradient
  comparison, non-finite scalar, non-finite gradient, GPU visibility in a
  deliberate CPU-only run, protected-path mutation.
- Explanatory diagnostics: ablations for FilterFlow-style transport custom
  gradient clipping, stopped transport-matrix gradient, stopped resampled-state
  gradient, stopped proposal log-probability gradient, stopped proposal mean
  gradient, stopped transition log-probability gradient, and stopped normalized
  weight gradient.
- Not concluded: correctness of either implementation, analytic-gradient
  correctness, posterior correctness, production readiness, public API
  readiness, HMC readiness, nonlinear-SSM validity, DSGE/NAWM validation, or
  monograph claims.

## Inputs

- `docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-surface-result-2026-06-03.md`
- `docs/plans/bayesfilter-dpf-filterflow-r3-float64-trace-replay-result-2026-06-03.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_surface_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r3_float64_trace_replay_tf.py`
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- `.localsource/filterflow/scripts/simple_linear_smoothness.py`
- `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/plan.py`
- `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/sinkhorn.py`

## Outputs

- Runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_localization_tf.py`
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_smoothness_gradient_localization_2026-06-03.json`
- Report:
  `experiments/dpf_implementation/reports/dpf-filterflow-float64-smoothness-gradient-localization-2026-06-03.md`
- Result:
  `docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-localization-result-2026-06-03.md`

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-localization-plan-2026-06-03.md`
- `docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-localization-result-2026-06-03.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_localization_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-smoothness-gradient-localization-2026-06-03.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_smoothness_gradient_localization_2026-06-03.json`

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- high-dimensional nonlinear filtering lane artifacts
- vendored student code
- `.localsource/filterflow`
- DSGE/NAWM-specific models or artifacts

## Skeptical Pre-Execution Audit

- Wrong baseline: use the local float64 FilterFlow executable only.
- Wrong objective: localize implementation differences, not correctness.
- Hidden scalar failure: compare cumulative scalar deltas before interpreting
  gradients.
- Gradient overclaim: finite gradients are smoke evidence only.
- Transport backward mismatch: explicitly test FilterFlow-style custom-gradient
  clipping because FilterFlow clips upstream transport-matrix gradients.
- Arbitrary thresholds: use the previous gradient-surface tolerances for
  within-row checks and report scale ratios as explanatory.
- Production drift: do not edit production code.
- Comparator drift: fingerprint FilterFlow before and after the run.

## Phase Order

1. Generate FilterFlow per-time cumulative scalar and gradient ledger for
   `theta=[0.95, 0.95]`.
2. Generate BayesFilter raw per-time ledger for the same fixed data, particles,
   seeds, dtype, and scalar.
3. Generate BayesFilter ablation ledgers.
4. Compare first scalar and gradient divergence times.
5. Record which ablation, if any, collapses the BayesFilter final-gradient scale
   toward FilterFlow.
6. Run verification.

## Stop Conditions

- FilterFlow reference status fails branch/marker validation.
- FilterFlow subprocess cannot run.
- Scalar mismatch appears before gradient localization.
- Required CPU-only manifest fails.
- Any required verification fails.
- Protected paths are modified by this task.

## Verification Commands

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_localization_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_smoothness_gradient_localization_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_smoothness_gradient_localization_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_smoothness_gradient_localization_2026-06-03.json >/tmp/dpf_filterflow_float64_smoothness_gradient_localization.json
rg -n "^(import numpy|from numpy)" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_localization_tf.py
rg -n "student|controlled_dpf|highdim|DSGE|NAWM|\\.localsource/filterflow" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_localization_tf.py
git diff --check
git status --short -- bayesfilter tests docs/chapters
git status --short --branch
```
