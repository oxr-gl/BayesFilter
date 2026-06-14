# Plan: Row 173 Time 93 Transport-Jacobian Probe

## Evidence Contract

- Question: under the frozen row-173/time-93 tensors, where do BayesFilter TF/TFP
  and the local float64 FilterFlow reference first differ in the implicit
  derivative of the annealed transport matrix with respect to input particles?
- Comparator: local executable float64 FilterFlow branch
  `bayesfilter-py311-float64-reference`.
- Primary criterion: compare `gradient(transport_matrix, particles,
  upstream_transport_matrix)` using the same frozen particles, log weights, and
  upstream transport-matrix adjoint.
- Veto diagnostics: FilterFlow reference drift, non-finite tensors, scalar/value
  mismatch in the frozen VJP source, or inability to run the CPU-only
  FilterFlow subprocess.
- Explanatory diagnostics: centered particles, scale, scaled particles,
  Sinkhorn potentials, raw/manual transport matrix, custom transport matrix,
  direct custom-gradient result, and manually reconstructed raw gradient under
  clipped upstream adjoint.
- Not concluded: correctness of either implementation, analytic gradient
  correctness, posterior correctness, production readiness, public API
  readiness, monograph claims, or nonlinear-SSM validity.
- Artifact: JSON and markdown report under
  `experiments/dpf_implementation/reports/outputs/`,
  `experiments/dpf_implementation/reports/`, and this result path.

## Inputs

- Row: `173`.
- Theta: `[0.9710526315789474, 0.9842105263157894]`.
- Time index: `93`.
- Frozen tensors are sourced from the existing row-173/time-93 VJP diagnostic:
  pre-resampling particles, pre-resampling log weights, and
  `gradient(target, transport_matrix)`.
- Transport settings: epsilon `0.25`, scaling `0.85`, threshold `1e-6`,
  max iterations `500`, `N=50`, dtype `float64`.

## Write Sets

Allowed:

- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-93-transport-jacobian-probe-plan-2026-06-03.md`
- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-time-93-transport-jacobian-probe-result-2026-06-03.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_time_93_transport_jacobian_probe_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-time-93-transport-jacobian-probe-2026-06-03.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_time_93_transport_jacobian_probe_2026-06-03.json`
- temporary JSON input under `experiments/dpf_implementation/reports/outputs/`

Forbidden:

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `.localsource/filterflow`
- high-dimensional nonlinear filtering lane
- vendored or student code
- DSGE/NAWM-specific code

## Skeptical Pre-Execution Audit

- Wrong baseline risk: use only the local float64 FilterFlow executable
  reference and validate its branch marker.
- Stale context risk: freeze tensors from the current row-173/time-93 VJP
  subprocess, not from handwritten state reconstruction.
- Proxy metric risk: finite gradients are smoke only; the pass/fail criterion is
  implementation agreement of the transport Jacobian under frozen inputs.
- Hidden topology risk: compare both FilterFlow custom-gradient output and a
  manually reconstructed raw-gradient path with clipped upstream.
- Threshold risk: report exact deltas; tolerances only classify localization,
  not correctness.
- Scope risk: no production/test/chapter/filterflow-source edits.

## Commands

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_time_93_transport_jacobian_probe_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_time_93_transport_jacobian_probe_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_time_93_transport_jacobian_probe_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_time_93_transport_jacobian_probe_2026-06-03.json
rg -n "^(import numpy|from numpy)" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_time_93_transport_jacobian_probe_tf.py
rg -n "student|controlled_dpf|highdim|DSGE|NAWM" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_time_93_transport_jacobian_probe_tf.py
git diff --check
git status --short -- bayesfilter tests docs/chapters
```
