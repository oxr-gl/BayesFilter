# P44-M4 Repair Amendment: Nonlinear Transition Horizon Scope

metadata_date: 2026-06-08
phase: P44-M4
run_id: `p44-codex-supervised-20260608-013203`
Status: `PENDING_P44_M4_REPAIR_REVIEW`

## Repair Target

The P44-M4 subplan requires dimensions 1, 2, and 3 value and diagnostic score
checks for CUT4 and Zhao--Cui against dense/sequential reference, and requires
two horizons before any error-accumulation statement.

Local implementation found a governed scope boundary: the current
`scalar_nonlinear_fixed_design_tt_value_path` helper is pinned to exactly two
observations. Extending it to horizon 4 would create a new Zhao--Cui helper
inside this phase rather than testing the already-governed artifact lane.

## Reviewed Scope Repair

M4 therefore uses the following repaired evidence ladder:

- `T=2`, dims 1, 2, and 3: dense/refined reference, CUT4, and
  Zhao--Cui/fixed-design scalar TT value and TensorFlow autodiff score checks.
- `T=4`, dims 1, 2, and 3: dense/refined reference and CUT4 value and
  TensorFlow autodiff score checks for accumulation diagnostics.
- `T=4` Zhao--Cui is an explicit nonclaim for this phase, not a pass condition
  and not evidence against Zhao--Cui.

## Why This Is Not A Tolerance Weakening

The repair does not relax any numerical threshold for observed Zhao--Cui
evidence. It prevents an unreviewed helper expansion from being smuggled into a
phase whose primary job is same-target nonlinear transition testing. The
T=2 Zhao--Cui checks still compare value and at least five deterministic
directional score residuals in dimensions 1, 2, and 3 against the dense
reference. The T=4 statement is limited to CUT4 accumulation.

## Stop Condition

If read-only Claude review rejects this scope boundary, P44-M4 must stop before
phase pass and either:

- implement a separately reviewed horizon-4 Zhao--Cui helper; or
- rewrite M4 as a narrower diagnostic-only phase without a Zhao--Cui
  accumulation claim.
