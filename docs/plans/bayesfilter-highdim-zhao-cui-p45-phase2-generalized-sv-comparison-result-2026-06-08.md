# P45-M2 Result: Generalized SV Comparison Gate

metadata_date: 2026-06-08
phase: P45-M2
run_id: `p45-codex-supervised-20260608-055034`
Status: `PASS_P45_M2_CODE_GOVERNANCE`

## Decision Table

| Field | Value |
| --- | --- |
| Decision | Generalized SV remains blocker/nonclaim for same-target CUT4--Zhao--Cui equality under current code. |
| Primary criterion status | Passed read-only Claude code/governance review at Iteration 1. |
| Veto diagnostic status | M2 does not compare unmatched native, transformed, approximation, CUT4, and Zhao--Cui targets. |
| Main uncertainty | A future phase could implement a native dense reference and multistate/factorized Zhao--Cui adapter, but P45-M2 did not do so. |
| Next justified action | Proceed to P45-M3 as spatial-SIR blocker/nonclaim unless a reviewed multistate adapter amendment is introduced. |
| Not concluded | No native generalized-SV likelihood correctness, no CUT4--Zhao--Cui equality, no HMC readiness, no production score API, no CNS paper-scale reproduction. |

## Evidence Contract

Question: for generalized SV
`y_t = beta s_t + exp(h_t / 2) epsilon_t` with states `(s_t,h_t)`, can CUT4
and Zhao--Cui evaluate the same likelihood and score target?

M2 outcome:

- No. Under P45-M1, the current nonlinear Zhao--Cui route is scalar-only.
- The native raw-observation target remains blocked because native dense
  reference, CUT4 native route, and Zhao--Cui multistate route are not all
  available.
- The transformed-residual route remains diagnostic-only because conditioning
  and Jacobian issues prevent treating it as exact native likelihood.
- Gaussian-mixture and moment-matched routes remain approximation-only.

## Local Evidence

| Command | Result |
| --- | --- |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p45_target_registry.py tests/highdim/test_p45_multistate_zhaocui_route.py tests/highdim/test_p45_generalized_sv_comparison_blocker.py` | 11 passed, 2 TFP deprecation warnings |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_p45_generalized_sv_comparison_blocker.py` | passed |
| `git diff --check -- tests/highdim/test_p45_generalized_sv_comparison_blocker.py` | passed |

## Claude Review

Iteration 1 returned `PASS_P45_M2_CODE_GOVERNANCE`.

Claude confirmed:

- M2 correctly inherits the M1 scalar-only blocker;
- native, transformed, and approximation distinctions are preserved;
- two-state generalized-SV Zhao--Cui rejection is exercised by code-level
  tests;
- the subplan and artifacts do not overclaim CUT4--Zhao--Cui equality.

## Gate Markers

p45_evidence_manifest: `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase2-generalized-sv-comparison-evidence-manifest-p45-codex-supervised-20260608-055034.json`
p45_local_evidence_run: `COMPLETE`
p45_evidence_audit: `COMPLETE`
p45_result_note_substance: `COMPLETE`
p45_traceability_or_nonclaim: `COMPLETE`
p45_command_count: `3`
p45_long_run_used: `false`
