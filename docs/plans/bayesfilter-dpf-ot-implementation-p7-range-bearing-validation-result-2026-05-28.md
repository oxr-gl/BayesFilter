# P7 Result: Range-Bearing Validation

Date: 2026-05-28

## Decision

`P7_RANGE_BEARING_VALIDATION_PASSED`

## Skeptical Pre-Execution Audit

| Check | Status | Evidence |
| --- | --- | --- |
| stale context | pass | P2/P3/P4 artifacts exist and compile. |
| wrong baseline | pass | UKF is approximate reference; bootstrap PF is comparator. |
| proxy overclaim | pass | RMSE metrics are proxy-only and not correctness evidence. |
| missing stop conditions | pass | UKF caveat, schema, checksums, finite values, Sinkhorn residuals, and reproducibility are enforced. |
| hidden production drift | pass | No production writes. |
| monograph drift | pass | No chapter edits. |
| vendored-code contamination | pass | No student/vendored imports. |
| high-dimensional-lane contamination | pass | No high-dimensional artifacts used. |
| artifact fitness | pass | Result answers nonlinear smoke evidence question. |

## Metrics

| Metric | Value |
| --- | ---: |
| median bootstrap state RMSE to UKF | `0.042616` |
| median OT-DPF state RMSE to UKF | `0.071249` |
| median bootstrap latent position RMSE | `0.064388` |
| median OT-DPF latent position RMSE | `0.074433` |
| median bootstrap observation proxy RMSE | `0.079780` |
| median OT-DPF observation proxy RMSE | `0.105909` |
| max OT Sinkhorn residual | `2.220e-16` |

## Artifacts

- `experiments/dpf_implementation/reports/dpf-ot-range-bearing-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ot_range_bearing_2026-05-28.json`

## Verification

- `python -m experiments.dpf_implementation.runners.run_range_bearing_ot_dpf`: pass.
- `python -m experiments.dpf_implementation.runners.run_range_bearing_ot_dpf --validate-only`: pass.
- `python -m experiments.dpf_implementation.runners.run_range_bearing_ot_dpf --check-reproducibility`: pass.

## Non-Implications

UKF is approximate and proxy RMSE is not posterior correctness.  This pass does
not validate HMC, production, exact categorical PF equivalence, learned/neural
OT, banking/model-risk, or monograph claims.
