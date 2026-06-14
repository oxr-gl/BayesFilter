# DPF1 Student Comparison Context Register

## Status

DPF1 execution artifact.  This register records frozen student and controlled
baseline artifacts that may inform comparison surfaces for the classical PF
baseline.  They are not authority and cannot satisfy acceptance criteria.

## Context Rows

| Source | Useful context | Allowed use | Forbidden use |
| --- | --- | --- | --- |
| `student-dpf-baseline-gap-closure-result-2026-05-10.md` | Student lane closeout/gap labels. | Identify caveats to preserve. | Certify BayesFilter correctness. |
| `student-dpf-baseline-linear-stress-result-2026-05-10.md` | Linear stress comparison surfaces. | Design analogous BayesFilter-owned stress rows. | Replace analytic LGSSM reference. |
| `student-dpf-baseline-nonlinear-smoke-result-2026-05-10.md` | Range-bearing smoke feasibility. | Identify proxy fields and runtime bounds. | Claim reference consistency. |
| `student-dpf-baseline-nonlinear-reference-panel-result-2026-05-10.md` | EKF/UKF/PF proxy spine and qualitative pressure points. | Inform DPF5 ladder design. | Promote RMSE/ESS to correctness. |
| `controlled-dpf-baseline-smoke-result.md` | Clean-room MP5 smoke row, no student import. | Inform bounded smoke size. | Claim correctness beyond one smoke row. |
| `controlled-dpf-baseline-fixed-grid-result.md` | Clean-room MP6 fixed-grid proxy rows. | Inform proxy fixture catalog. | Treat proxy RMSE as acceptance evidence. |
| `controlled-dpf-baseline-comparison-audit.md` | Same qualitative regime comparison under fixed 2.0x rule. | Qualitative comparison context only. | Treat student agreement as validation. |

## Carry-Forward Caveats

- Student implementation source is not imported or executed.
- Controlled fixed-grid metrics are proxy diagnostics, not correctness
  certificates.
- Same qualitative regime is a comparison label, not a promotion criterion.
- No production, HMC, posterior, banking, or model-risk claim follows.

## DPF1 Consequence

DPF1 must use independent BayesFilter-owned references for acceptance.  Student
and controlled context may shape artifact fields and proxy rows only after the
LGSSM/reference ladder is in place.
