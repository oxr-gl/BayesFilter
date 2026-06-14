# P45-M1 Result: Multistate Zhao-Cui Route Feasibility

metadata_date: 2026-06-08
phase: P45-M1
run_id: `p45-codex-supervised-20260608-055034`
Status: `PASS_P45_M1_CODE_GOVERNANCE`

## Decision Table

| Field | Value |
| --- | --- |
| Decision | Current nonlinear Zhao--Cui/fixed-design TT route remains scalar-only; P45-M1 passes as a governed implementation blocker, not as a multistate adapter implementation. |
| Primary criterion status | Passed read-only Claude code/governance review at Iteration 1. |
| Veto diagnostic status | No downstream generalized-SV, SIR, or predator-prey phase may claim CUT4--Zhao--Cui equality using the current scalar-only nonlinear route. |
| Main uncertainty | Whether to implement a reviewed multistate/factorized TT adapter in a future repair phase or keep M2--M4 as blocker/nonclaim phases. |
| Next justified action | Run the P45-M1 phase gate. Then M2--M4 must inherit this blocker unless they create a separately reviewed adapter amendment. |
| Not concluded | No multistate TT adapter, no generalized-SV/SIR/predator-prey equality, no HMC readiness, no production score API. |

## Evidence Contract

Question: can a reviewed fixed-design TT route evaluate the same tiny
multistate likelihood and score target as CUT4 and a dense/refined reference?

Baseline/comparator:

- Baseline route status is current code in `bayesfilter/highdim/filtering.py`.
- The route is judged against the P45-M1 subplan and M0 target registry.
- Because no multistate route is implemented in M1, the correct evidence is an
  executable blocker proving `state_dim != 1` nonlinear routes remain rejected.

Primary promotion criterion:

- Either implement and test a multistate/factorized fixed-design TT route, or
  record a blocker preventing M2--M4 equality promotion.

M1 outcome:

- The blocker route was selected.
- `FixedBranchSquaredTTFilter(...).log_likelihood` rejects a two-state
  nonlinear model with `scalar nonlinear dense value path requires state_dim ==
  1`.
- `scalar_nonlinear_fixed_design_tt_value_path` rejects a two-state nonlinear
  model with `scalar nonlinear fixed-design TT value path requires state_dim ==
  1`.
- The M0 target registry still marks generalized SV, spatial SIR closure, and
  predator-prey closure Zhao--Cui routes as
  `blocked_current_scalar_nonlinear_route_requires_state_dim_1`.

## Local Evidence

| Command | Result |
| --- | --- |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p45_target_registry.py tests/highdim/test_p45_multistate_zhaocui_route.py` | 8 passed, 2 TFP deprecation warnings |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p45_phase_gate.py tests/highdim/test_p45_target_registry.py tests/highdim/test_p45_multistate_zhaocui_route.py` | passed |
| `git diff --check -- tests/highdim/test_p45_multistate_zhaocui_route.py tests/highdim/test_p45_target_registry.py scripts/p45_phase_gate.py` | passed |

## Claude Review

Iteration 1 returned `PASS_P45_M1_CODE_GOVERNANCE`.

Claude confirmed:

- current nonlinear value paths hard-reject `state_dim != 1`;
- the new tests execute the blocker gate directly;
- the M0 registry keeps multistate generalized-SV, SIR, and predator-prey rows
  blocked;
- the subplan allows a blocker outcome and the artifacts do not claim a
  multistate TT adapter.

## Gate Markers

p45_evidence_manifest: `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase1-multistate-zhaocui-route-evidence-manifest-p45-codex-supervised-20260608-055034.json`
p45_local_evidence_run: `COMPLETE`
p45_evidence_audit: `COMPLETE`
p45_result_note_substance: `COMPLETE`
p45_traceability_or_nonclaim: `COMPLETE`
p45_command_count: `3`
p45_long_run_used: `false`
