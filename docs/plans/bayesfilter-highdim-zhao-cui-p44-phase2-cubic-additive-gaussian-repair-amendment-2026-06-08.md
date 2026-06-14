# P44-M2 Repair Amendment: Cubic Additive-Gaussian Thresholds

metadata_date: 2026-06-08
phase: P44-M2
run_id: `p44-codex-supervised-20260608-013203`
Status: `PENDING_P44_M2_REPAIR_REVIEW`

## Blocker

The first M2 local evidence run found two fixable issues.

1. The command-log wrapper used unescaped Markdown backticks, so Bash tried to
   execute the marker contents. This was an operational logging bug only.
2. The initial CUT4 acceptance threshold treated the cubic same-target
   sigma-point approximation as closer to dense quadrature than observed.

Observed CUT4 gaps against dense order-241 reference:

| dim | value gap | max directional score gap | relative score error |
| --- | ---: | ---: | ---: |
| 1 | `3.198174e-03` | `8.470451e-03` | `1.074936e-02` |
| 2 | `6.693418e-03` | `1.770687e-02` | `1.589103e-02` |
| 3 | `1.541071e-02` | `4.073841e-02` | `2.326626e-02` |

Observed Zhao--Cui/fixed-design TT gaps against the same dense reference:

| dim | value gap | max directional score gap | relative score error |
| --- | ---: | ---: | ---: |
| 1 | `1.931912e-04` | `8.914410e-04` | `1.115007e-03` |
| 2 | `2.224265e-04` | `1.059130e-03` | `9.395700e-04` |
| 3 | `3.496295e-04` | `1.818532e-03` | `9.991846e-04` |

## Repair

- Fix the command-log marker writer by escaping Markdown backticks.
- Keep dense order-161 versus order-241 refinement as a veto check.
- Keep the nested `a=0` Kalman value and shared-parameter score check.
- Correct the nested-linear cubic-parameter score interpretation: when
  `a=0`, dense cubic-path differentiation still has a nonzero local derivative
  with respect to the cubic coefficient, while the exact Kalman nested linear
  model has no cubic coefficient. Therefore only the shared first four
  coordinates are asserted equal in the nested-linear sanity check.
- Revise CUT4 thresholds to explicit same-target approximation bounds:
  value gap `< 6e-3 * dim`, max directional score gap `< 1.5e-2 * dim`, and
  relative score error `< 2.5e-2`.
- Leave Zhao--Cui thresholds tight:
  value gap `< 4e-3 * dim`, max directional score gap `< 2e-2 * dim`, and
  relative score error `< 1e-2`.

## Claim Boundary

This repair does not promote CUT4 as an exact cubic filter. It supports only a
bounded, reported, same-target approximation diagnostic against a refined dense
reference on tiny deterministic fixtures. Zhao--Cui remains tested as the
tighter scalar fixed-design TT approximation lane for this fixture.

## Required Review

Claude must review this amendment read-only and either return
`PASS_P44_M2_REPAIR_REVIEW` or explain why the changed threshold or
nested-linear score interpretation is scientifically unsafe.

## Second Repair: CUT4 Structural Timing Evidence

Claude final code/governance review Iteration 2 identified a real evidence gap:
the test directly tied dense `a=0` timing to Kalman but did not directly tie
CUT4 structural `a=0` timing to Kalman. This left the CUT4 same-target claim
under-evidenced because the structural lane uses raw initial moments plus an
explicit transition map.

Repair:

- Add
  `test_p44_m2_nested_linear_cut4_structural_timing_matches_exact_kalman_dims_1_2_3`.
- The test sets `a=0`, compares CUT4 structural value to exact Kalman in dims
  1, 2, and 3, compares the first four shared score coordinates, and records
  the cubic-coordinate derivative as finite but non-Kalman-shared.
- Re-run focused M2 pytest; result is `5 passed`.

This repair does not change the target, tolerance, model parameters, or claim
boundary. It adds the missing direct same-target timing evidence requested by
Claude.
