# P6 Result: LGSSM Validation

Date: 2026-05-28

## Decision

`P6_LGSSM_VALIDATION_PASSED`

## Skeptical Pre-Execution Audit

| Check | Status | Evidence |
| --- | --- | --- |
| stale context | pass | P1/P3/P4 artifacts exist and compile. |
| wrong baseline | pass | Kalman is exact LGSSM reference; bootstrap PF is comparator. |
| proxy overclaim | pass | OT-DPF is labeled relaxed finite-Sinkhorn path. |
| missing stop conditions | pass | Schema, checksums, finite values, Sinkhorn residuals, and reproducibility are enforced. |
| hidden production drift | pass | No production writes. |
| monograph drift | pass | No chapter edits. |
| vendored-code contamination | pass | No student/vendored imports. |
| high-dimensional-lane contamination | pass | No high-dimensional artifacts used. |
| artifact fitness | pass | Result answers LGSSM evidence question. |

## Metrics

| Metric | Value |
| --- | ---: |
| median bootstrap mean RMSE to Kalman | `0.045212` |
| median OT-DPF mean RMSE to Kalman | `0.051936` |
| median bootstrap log-likelihood delta to Kalman | `0.057763` |
| median OT-DPF log-likelihood delta to Kalman | `0.334682` |
| max OT Sinkhorn residual | `9.832e-09` |

## Artifacts

- `experiments/dpf_implementation/reports/dpf-ot-lgssm-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ot_lgssm_2026-05-28.json`

## Verification

- `python -m experiments.dpf_implementation.runners.run_lgssm_ot_dpf`: pass.
- `python -m experiments.dpf_implementation.runners.run_lgssm_ot_dpf --validate-only`: pass.
- `python -m experiments.dpf_implementation.runners.run_lgssm_ot_dpf --check-reproducibility`: pass.

## Non-Implications

LGSSM pass does not validate nonlinear filtering, exact DPF likelihood,
posterior correctness, HMC, production, learned/neural OT, banking/model-risk,
or monograph claims.
