# P2 Result: Range-Bearing Fixture And UKF Reference

Date: 2026-05-28

## Decision

`P2_RANGE_BEARING_UKF_REFERENCE_ACCEPTED`

## Skeptical Pre-Execution Audit

| Check | Status | Evidence |
| --- | --- | --- |
| stale context | pass | DPF5 calls for a controlled nonlinear range-bearing rung. |
| wrong baseline | pass | UKF is approximate reference; not student or ground truth. |
| proxy overclaim | pass | RMSE is reserved for P7 proxy diagnostics only. |
| missing stop conditions | pass | Non-finite UKF, covariance failure, or missing caveat blocks movement. |
| hidden production drift | pass | Wrote only experimental DPF files. |
| monograph drift | pass | No chapter edits. |
| vendored-code contamination | pass | Fixture is local clean-room code and imports no student/vendor paths. |
| high-dimensional-lane contamination | pass | No high-dimensional artifacts used. |
| artifact fitness | pass | Fixture and UKF reference answer the P2 question. |

## Artifacts

- `experiments/dpf_implementation/fixtures/range_bearing.py`
- `experiments/dpf_implementation/references/ukf.py`

## Verification

- `python -m py_compile ... range_bearing.py ... ukf.py`: pass.
- Import probe printed horizon `20`, filtered mean shape `(20, 4)`,
  `approximate_reference=True`, and `finite=True`.

## Non-Implications

UKF is approximate for the nonlinear range-bearing fixture.  It is not ground
truth and does not validate posterior correctness, HMC, production, or monograph
claims.
