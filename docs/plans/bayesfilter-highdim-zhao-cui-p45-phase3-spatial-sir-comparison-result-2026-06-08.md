# P45-M3 Result: Spatial SIR Comparison Gate

metadata_date: 2026-06-08
phase: P45-M3
run_id: `p45-codex-supervised-20260608-055034`
Status: `PASS_P45_M3_CODE_GOVERNANCE`

## Decision Table

| Field | Value |
| --- | --- |
| Decision | Spatial SIR remains closure/blocker/nonclaim for same-target CUT4--Zhao--Cui equality under current code. |
| Primary criterion status | Passed read-only Claude code/governance review at Iteration 1. |
| Veto diagnostic status | M3 does not treat finite CUT4 closure diagnostics as native SIR correctness or CUT4--Zhao--Cui equality. |
| Main uncertainty | A future phase could implement a dense closure reference and multistate/factorized Zhao--Cui adapter; native/non-Gaussian SIR also needs separate scientific target definition. |
| Next justified action | Proceed to P45-M4 as predator-prey blocker/nonclaim unless a reviewed multistate adapter amendment is introduced. |
| Not concluded | No native SIR filtering correctness, no production TT/SIRT SIR filtering, no CUT4--Zhao--Cui equality, no HMC readiness. |

## Evidence Contract

Question: can the declared spatial SIR target be evaluated by CUT4,
Zhao--Cui/fixed-design TT, and a reference route without changing the model or
parameterization?

M3 outcome:

- No same-target comparison is authorized under current code.
- The additive-Gaussian SIR row remains closure-only and blocked pending M1
  route support and dense/refined reference.
- The native/non-Gaussian SIR row remains blocked pending target definition,
  reference route, CUT4 route, and Zhao--Cui route.
- `J=2,3` rows remain factorized/replicated panels unless a coupled multistate
  TT route is separately implemented and reviewed.

## Local Evidence

| Command | Result |
| --- | --- |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p45_target_registry.py tests/highdim/test_p45_multistate_zhaocui_route.py tests/highdim/test_p45_generalized_sv_comparison_blocker.py tests/highdim/test_p45_spatial_sir_comparison_blocker.py` | 14 passed, 2 TFP deprecation warnings |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_p45_spatial_sir_comparison_blocker.py` | passed |
| `git diff --check -- tests/highdim/test_p45_spatial_sir_comparison_blocker.py` | passed |

## Claude Review

Iteration 1 returned `PASS_P45_M3_CODE_GOVERNANCE`.

Claude confirmed:

- M3 is framed as a blocker/nonclaim gate unless matched target, reference,
  value, and score evidence exist;
- closure-vs-native boundaries are preserved;
- factorized-vs-coupled panel boundaries are preserved;
- the current Zhao--Cui route rejects the `J=1`, `state_dim=2` SIR closure,
  consistent with M1.

## Gate Markers

p45_evidence_manifest: `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase3-spatial-sir-comparison-evidence-manifest-p45-codex-supervised-20260608-055034.json`
p45_local_evidence_run: `COMPLETE`
p45_evidence_audit: `COMPLETE`
p45_result_note_substance: `COMPLETE`
p45_traceability_or_nonclaim: `COMPLETE`
p45_command_count: `3`
p45_long_run_used: `false`
