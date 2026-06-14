# P45-M4 Result: Predator-Prey Comparison Gate

metadata_date: 2026-06-08
phase: P45-M4
run_id: `p45-codex-supervised-20260608-055034`
Status: `PASS_P45_M4_CODE_GOVERNANCE`

## Decision Table

| Field | Value |
| --- | --- |
| Decision | Predator-prey remains RK4-closure/blocker/nonclaim for same-target CUT4--Zhao--Cui equality under current code. |
| Primary criterion status | Passed read-only Claude code/governance review at Iteration 1. |
| Veto diagnostic status | M4 does not treat finite CUT4 closure diagnostics as paper-scale predator-prey validation or CUT4--Zhao--Cui equality. |
| Main uncertainty | A future phase could implement a dense closure reference and multistate/factorized Zhao--Cui adapter; native/non-Gaussian predator-prey also needs separate scientific target definition. |
| Next justified action | Proceed to P45-M5 cross-model error calibration, which should calibrate only actual same-target rows and preserve blocker/nonclaim statuses for M2--M4. |
| Not concluded | No native predator-prey filtering correctness, no nonlinear preconditioning usefulness claim, no CUT4--Zhao--Cui equality, no HMC readiness. |

## Evidence Contract

Question: can the declared predator-prey target be evaluated by CUT4,
Zhao--Cui/fixed-design TT, and a reference route without changing the ODE
transition, parameterization, or observation model?

M4 outcome:

- No same-target comparison is authorized under current code.
- The additive-Gaussian RK4 predator-prey row remains closure-only and blocked
  pending M1 route support and dense/refined reference.
- The native/non-Gaussian predator-prey row remains blocked pending target
  definition, reference route, CUT4 route, and Zhao--Cui route.
- Replicated panels remain factorized unless a coupled multistate TT route is
  separately implemented and reviewed.

## Local Evidence

| Command | Result |
| --- | --- |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p45_target_registry.py tests/highdim/test_p45_multistate_zhaocui_route.py tests/highdim/test_p45_generalized_sv_comparison_blocker.py tests/highdim/test_p45_spatial_sir_comparison_blocker.py tests/highdim/test_p45_predator_prey_comparison_blocker.py` | 17 passed, 2 TFP deprecation warnings |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_p45_predator_prey_comparison_blocker.py` | passed |
| `git diff --check -- tests/highdim/test_p45_predator_prey_comparison_blocker.py` | passed |

## Claude Review

Iteration 1 returned `PASS_P45_M4_CODE_GOVERNANCE`.

Claude confirmed:

- predator-prey stays on the additive-Gaussian RK4 closure row while
  native/non-Gaussian predator-prey is separately blocked;
- RK4 convention and factorized replicated-panel governance are preserved;
- equality promotion remains blocked;
- the tests use the actual predator-prey fixture with `state_dim() == 2` to
  confirm current Zhao--Cui rejection.

## Gate Markers

p45_evidence_manifest: `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase4-predator-prey-comparison-evidence-manifest-p45-codex-supervised-20260608-055034.json`
p45_local_evidence_run: `COMPLETE`
p45_evidence_audit: `COMPLETE`
p45_result_note_substance: `COMPLETE`
p45_traceability_or_nonclaim: `COMPLETE`
p45_command_count: `3`
p45_long_run_used: `false`
