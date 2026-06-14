# P1 Result: LGSSM Fixture And Kalman Reference

Date: 2026-05-28

## Decision

`P1_LGSSM_KALMAN_REFERENCE_ACCEPTED`

## Skeptical Pre-Execution Audit

| Check | Status | Evidence |
| --- | --- | --- |
| stale context | pass | DPF1/DPF5 require Kalman LGSSM reference before DPF comparisons. |
| wrong baseline | pass | Reference is analytic Kalman, not student or controlled output. |
| proxy overclaim | pass | P1 creates reference only; no particle or proxy claim. |
| missing stop conditions | pass | Non-finite Kalman outputs or production imports block movement. |
| hidden production drift | pass | Wrote only `experiments/dpf_implementation/` and DPF OT plan result. |
| monograph drift | pass | No chapter edits. |
| vendored-code contamination | pass | No student/vendored imports. |
| high-dimensional-lane contamination | pass | No high-dimensional artifacts used. |
| artifact fitness | pass | Fixture and Kalman reference answer the P1 question. |

## Artifacts

- `experiments/dpf_implementation/fixtures/lgssm.py`
- `experiments/dpf_implementation/references/kalman_lgssm.py`
- `experiments/dpf_implementation/references/__init__.py`

## Verification

- `python -m py_compile ... lgssm.py ... kalman_lgssm.py`: pass.
- Import probe printed horizon `25`, finite Kalman log likelihood
  `-24.245777`, and `finite=True`.

## Non-Implications

This reference is exact only for the local LGSSM fixture.  It does not validate
OT-DPF, nonlinear filtering, gradients, HMC, production, or monograph claims.
