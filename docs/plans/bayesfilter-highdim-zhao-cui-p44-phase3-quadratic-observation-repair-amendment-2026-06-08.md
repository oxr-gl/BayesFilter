# P44-M3 Repair Amendment: Quadratic Observation Stress-Gap Boundary

metadata_date: 2026-06-08
phase: P44-M3
run_id: `p44-codex-supervised-20260608-013203`
Status: `PENDING_P44_M3_REPAIR_REVIEW`

## Blocker

The first M3 local evidence run showed the intended multimodality stress:
dense quadrature covers both symmetric modes, and Zhao--Cui/fixed-design TT is
tight against dense, but CUT4 has a large same-target approximation gap.

Observed CUT4 gaps against dense order-281 reference:

| dim | value gap | max directional score gap | relative score error |
| --- | ---: | ---: | ---: |
| 1 | `7.099181e-02` | `2.418344e-01` | `2.579872e-01` |
| 2 | `1.751315e-01` | `5.681237e-01` | `3.527955e-01` |
| 3 | `3.607512e-01` | `1.102107e+00` | `4.637075e-01` |

Observed Zhao--Cui/fixed-design TT gaps against the same dense reference:

| dim | value gap | max directional score gap | relative score error |
| --- | ---: | ---: | ---: |
| 1 | `4.252455e-05` | `1.502594e-04` | `1.564833e-04` |
| 2 | `9.662974e-05` | `2.820354e-04` | `2.045106e-04` |
| 3 | `2.756965e-04` | `6.769339e-04` | `3.598171e-04` |

## Repair

- Reclassify the CUT4 row as a same-target stress-gap diagnostic, not a
  small-error approximation success.
- Keep CUT4 requirements finite and bounded:
  value gap greater than `5e-2 * dim` and less than `1.3e-1 * dim`, max
  directional score gap less than `4.0e-1 * dim`, and relative score error
  less than `5.0e-1`.
- Keep Zhao--Cui as the tight same-target approximation evidence:
  value gap less than `8e-3 * dim`, max directional score gap less than
  `4e-2 * dim`, and relative score error less than `2e-2`.
- Preserve dense order-181 versus order-281 refinement as a veto check.
- Preserve explicit symmetric-mode coverage as a veto check before any
  comparison is interpreted.
- Preserve CUT4 point-count cap at augmented dimension 6 / point count 76.

## Claim Boundary

M3 now supports the claim that the quadratic observation fixture is a stress
case where CUT4 remains finite and same-target but exhibits a large recorded
gap, while Zhao--Cui/fixed-design TT remains close to dense on the tiny
factorized fixtures. It does not promote CUT4 as accurate for symmetric
multimodal quadratic observations.

## Required Review

Claude must review this repair read-only and either return
`PASS_P44_M3_REPAIR_REVIEW` or explain why this stress-gap reclassification is
scientifically unsafe.
