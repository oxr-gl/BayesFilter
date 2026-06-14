# P5 Result: Gradient Contract And Same-Scalar Check

Date: 2026-05-28

## Decision

`P5_GRADIENT_FINITE_DIFFERENCE_SAME_SCALAR_PASSED`

## Skeptical Pre-Execution Audit

| Check | Status | Evidence |
| --- | --- | --- |
| stale context | pass | DPF4 authorizes same-scalar G1/G2-style checks only. |
| wrong baseline | pass | Comparator is central finite differences for the same scalar. |
| proxy overclaim | pass | Gradient is for a relaxed proxy scalar only. |
| missing stop conditions | pass | Non-finite scalar, unstable finite differences, or scalar mismatch would fail. |
| hidden production drift | pass | Wrote only experimental runner/report artifacts. |
| monograph drift | pass | No chapter edits. |
| vendored-code contamination | pass | No student/vendored imports. |
| high-dimensional-lane contamination | pass | No high-dimensional artifacts used. |
| artifact fitness | pass | Same-scalar finite-difference artifact answers P5. |

## Result

- Scalar: `lgssm_relaxed_ot_log_normalizer_proxy`.
- Gradient path: `central_finite_difference_only`.
- Autodiff status: `autodiff_not_tested`.
- Finite-difference gradient: `-0.566919`.
- Half-step stability residual: `1.483e-09`.
- Decision: `DPF_OT_GRADIENT_FD_PASSED`.

## Artifacts

- `experiments/dpf_implementation/runners/run_gradient_checks.py`
- `experiments/dpf_implementation/reports/dpf-ot-gradient-check-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ot_gradient_check_2026-05-28.json`

## Verification

- `python -m experiments.dpf_implementation.runners.run_gradient_checks`: pass.
- `python -m experiments.dpf_implementation.runners.run_gradient_checks --validate-only`: pass.
- `python -m experiments.dpf_implementation.runners.run_gradient_checks --check-reproducibility`: pass.

## Non-Implications

This is finite-difference-only same-scalar evidence.  It is not autodiff
validation, likelihood-score validation, HMC readiness, posterior correctness,
production readiness, or monograph validation.
