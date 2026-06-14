# Result: Filterflow Transport Component Audit

## Decision

`transport_formula_mismatch_identified`

The component audit isolated the failed BayesFilter audit-only filterflow-style
transport mirror to a concrete formula mismatch.  The dominant issue is the
axis used when adding normalized log weights inside
`transport_from_potentials`.

Filterflow's transport matrix is an `N`-scaled barycentric transport operator:

- row sums are near one;
- column sums are near `N * source_weight`;
- transported particles are `transport_matrix @ particles`;
- `transport` and `transport_from_potentials` agree exactly on the frozen state.

The failed BayesFilter audit-only mirror added `logw` on the row/source axis.
Filterflow adds it on the column axis after the column normalization step.
That row-axis variant is off by order one in transport matrix and transported
particles.  The column-axis reconstruction matches filterflow to numerical
tolerance.

## Artifacts

- Plan:
  `docs/plans/bayesfilter-dpf-filterflow-transport-component-audit-plan-2026-05-30.md`
- Runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_transport_component_audit_tf.py`
- Report:
  `experiments/dpf_implementation/reports/dpf-filterflow-transport-component-audit-2026-05-30.md`
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_transport_component_audit_2026-05-30.json`

## Claude Review

Plan review:

| Iteration | Status | Codex audit |
| --- | --- | --- |
| 1 | `ACCEPT` | Accepted. Claude's watch item was to expose `transport_from_potentials` explicitly, which the runner/report now do. |

Result review:

| Iteration | Status | Codex audit |
| --- | --- | --- |
| 1 | `ACCEPT` | Accepted. Claude confirmed the component question is answered, `transport_from_potentials` is explicit, the row/column log-weight conclusion is supported, epsilon-start conclusions are limited, and no proxy overclaim or lane contamination was found. |

## Evidence Contract Status

Question: on one frozen LGSSM resampling state, does the BayesFilter
audit-only reconstruction of filterflow's annealed transport match the original
filterflow transport component?

Answer: the exact column-axis reconstruction matches; the previous row-axis
audit-only reconstruction fails.

Frozen state:

| Field | Value |
| --- | ---: |
| time index | `1` |
| batch index | `3` |
| selected ESS | `1.0999250411987305` |
| ESS threshold | `12.5` |
| triggered batches | `100` |

## Filterflow Internal Consistency

Filterflow `transport` versus direct `transport_from_potentials`:

| epsilon | matrix max diff | transported-particle max diff | row residual | column residual |
| --- | ---: | ---: | ---: | ---: |
| `0.25` | `0.0` | `0.0` | `1.372e-04` | `1.192e-07` |
| `0.50` | `0.0` | `0.0` | `1.329e-05` | `1.907e-06` |
| `0.75` | `0.0` | `0.0` | `3.457e-06` | `1.490e-07` |

This confirms the audit is comparing against the actual filterflow component,
not a separate inferred implementation.

## Candidate Variant Results

Summary across epsilons `0.25`, `0.5`, and `0.75`:

| Variant | Max matrix diff | Max particle diff | Status |
| --- | ---: | ---: | --- |
| `legacy_axis_row_epsilon0_max_cost` | `1.1361520290374756` | `5.1525678634643555` | fail |
| `axis_row_epsilon0_filterflow_range` | `1.1361525058746338` | `5.1525678634643555` | fail |
| `axis_column_epsilon0_max_cost` | `1.1026859283447266e-05` | `8.165836334228516e-06` | component match on transported particles |
| `axis_column_epsilon0_filterflow_range` | `4.172325134277344e-07` | `2.384185791015625e-07` | exact filterflow reconstruction |

The epsilon-start scale affects potentials and iteration count, but it is not
the order-one transported-particle failure on this frozen state.  The axis of
the `logw` term is the decisive mismatch.

## Interpretation

The earlier audit-only filterflow-style BayesFilter lane was not faithful to
filterflow's `transport_from_potentials`.  The mistake is mathematical/code
semantic rather than evidence that Corenflos/filterflow OT resampling fails on
LGSSM.

The filterflow transport matrix has row sums near one because each output
particle is a barycentric combination of the input particles.  Its column sums
carry the `N * source_weight` mass.  Adding `logw` on the row axis reverses
that mass placement, producing invalid row/column residuals and order-one
particle movement differences.

## Verification

Executed:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_transport_component_audit_tf.py
```

Status: pass.

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_transport_component_audit_tf
```

Output:

```text
transport_formula_mismatch_identified
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_transport_component_audit_tf --validate-only
```

Status: pass.

```bash
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_transport_component_audit_2026-05-30.json >/dev/null
```

Status: pass.

Import-boundary check:

```bash
rg -n "import numpy|from numpy|student_dpf_baselines|vendor|highdim|NAWM|DSGE" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_transport_component_audit_tf.py
```

Status: no matches.  The external filterflow subprocess dynamically imports
NumPy as reference/comparison code; the BayesFilter runner has no NumPy
algorithmic implementation import.

## What Is Not Concluded

- No production readiness.
- No public API readiness.
- No HMC readiness.
- No posterior correctness.
- No general nonlinear-SSM validity.
- No claim that finite relaxed OT is categorical PF.
- No claim that the BayesFilter outer matched audit runner is fixed.
- No claim that patched filterflow is untouched upstream code.

## Next Recommended Action

Patch only the experimental BayesFilter audit-only filterflow-style transport
mirror to use column-axis `logw` and filterflow's coordinate-range epsilon-start
schedule, then rerun the matched LGSSM cross-audit.  Do not change production
code or promote filterflow-style transport until that outer rerun passes.
