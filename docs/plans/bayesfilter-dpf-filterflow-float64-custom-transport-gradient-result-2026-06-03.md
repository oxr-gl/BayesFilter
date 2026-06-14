# FilterFlow Float64 Custom Transport Gradient Patch Result

## Decision

`filterflow_float64_custom_transport_gradient_patch_closed_surface_gap`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `filterflow_float64_custom_transport_gradient_patch_closed_surface_gap` | Bounded float64 smoothness gradient surface now passes: 16/16 scalar rows and 16/16 gradient rows within tolerance. | No scalar, finiteness, CPU-only, or comparator-drift veto fired. | Bounded 4x4 mesh only; this is agreement with the local executable FilterFlow reference, not analytic-gradient correctness. | Rerun the larger/full smoothness mesh or integrate the same clipped-backward contract into any remaining comparison runners that rely on annealed transport gradients. | Correctness of either implementation, posterior correctness, production readiness, public API readiness, HMC readiness, nonlinear-SSM validity, DSGE/NAWM validation, monograph claims. |

## Files Changed

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_localization_tf.py`
- `docs/plans/bayesfilter-dpf-filterflow-float64-custom-transport-gradient-plan-2026-06-03.md`
- `docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-surface-result-2026-06-03.md`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-smoothness-gradient-surface-2026-06-03.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_smoothness_gradient_surface_2026-06-03.json`
- `docs/plans/bayesfilter-dpf-filterflow-float64-custom-transport-gradient-result-2026-06-03.md`

## Patch Summary

- Added `transport_gradient_mode` to the experimental annealed transport
  component.
- Defaulted `transport_gradient_mode` to `filterflow_clipped`.
- Added a TensorFlow custom-gradient wrapper that leaves the forward transport
  matrix unchanged and clips upstream `d_transport` to `[-1, 1]`, mirroring the
  local FilterFlow `RegularisedTransform` executable behavior.
- Preserved a labelled `raw` transport-gradient mode for future difference
  audits.
- Updated the localization runner so its `raw` diagnostic explicitly requests
  raw TensorFlow transport gradients after the component default changed.

## Evidence

Targeted runner:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_smoothness_gradient_surface_tf
```

Decision:

`filterflow_float64_smoothness_gradient_surface_pass`

Comparison summary:

```json
{
  "finite_rows": 16,
  "first_failure": {
    "status": "no_failure"
  },
  "gradient_rows_within_tolerance": 16,
  "implementation_agreement": true,
  "max_abs_gradient_delta": 0.1233334128792194,
  "max_relative_gradient_delta": 1.4123389604429983e-05,
  "max_scalar_delta": 1.4924950164640904e-08,
  "rmse_max_abs_gradient_delta": 0.031213201130162273,
  "rmse_scalar_delta": 8.905779290840865e-09,
  "row_count": 16,
  "scalar_rows_within_tolerance": 16
}
```

First mesh row after patch:

```json
{
  "filterflow_gradient_diag": [
    18935.6850725171,
    2073.5151524806142
  ],
  "bayesfilter_gradient_diag": [
    18935.685049167038,
    2073.51515897136
  ],
  "filterflow_mean_log_likelihood": -258.58524847172157,
  "bayesfilter_mean_log_likelihood": -258.5852484624214
}
```

The previous raw-gradient failure was localized to the first resampling step
and to FilterFlow's transport custom-gradient clipping. The patched component
now mirrors that executable backward contract by default.

## Verification

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_surface_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_localization_tf.py
```

Passed.

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_smoothness_gradient_surface_tf
```

Passed with decision `filterflow_float64_smoothness_gradient_surface_pass`.

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_smoothness_gradient_surface_tf --validate-only
```

Passed.

```bash
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_smoothness_gradient_surface_2026-06-03.json >/tmp/dpf_filterflow_float64_smoothness_gradient_surface.json
```

Passed.

CPU-only manifest recorded `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import
and `gpu_devices_visible=[]`.

FilterFlow reference drift was false. The FilterFlow checkout remained on
`bayesfilter-py311-float64-reference`.

## Caveats

- This is not production readiness.
- This is not public API readiness.
- This is not posterior correctness.
- This is not HMC readiness.
- This is not general nonlinear-SSM validity.
- This is not DSGE/NAWM validation.
- This is not a banking/model-risk claim.
- This is not a monograph claim.
- Finite gradients alone are not gradient correctness.
- Agreement here is against the local float64 FilterFlow executable reference,
  not pristine upstream source and not an analytic Kalman gradient.
