# P45-M5 Result: Cross-Model Error Calibration

metadata_date: 2026-06-08
phase: P45-M5
run_id: `p45-codex-supervised-20260608-055034`
Status: `PASS_P45_M5_CODE_GOVERNANCE`

## Decision Table

| Field | Value |
| --- | --- |
| Decision | No P45-M2--M4 same-target comparison rows were promoted, so no value/gradient error calibration is interpretable yet. |
| Primary criterion status | Passed read-only Claude code/governance review at Iteration 1. |
| Veto diagnostic status | M5 does not invent value gaps, score gaps, directional residuals, or likelihood-variance tolerances for blocked/nonclaim rows. |
| Main uncertainty | Error calibration can become meaningful only after a future phase implements matched reference, CUT4, and Zhao--Cui routes for at least one target. |
| Next justified action | Proceed to P45-M6 integration closeout. |
| Not concluded | No CUT4--Zhao--Cui equality, no gradient agreement, no HMC readiness, no production score API, no long/high-dimensional conclusion. |

## Calibration Ledger

Machine-readable ledger:

`docs/plans/bayesfilter-highdim-zhao-cui-p45-cross-model-error-calibration-2026-06-08.json`

Summary:

| Phase | Model | Same-target comparison reached? | Calibration result |
| --- | --- | --- | --- |
| P45-M2 | generalized SV | no | equality metrics absent due to missing native reference, native CUT4 route, and multistate Zhao--Cui route |
| P45-M3 | spatial SIR | no | equality metrics absent due to missing dense closure reference and multistate Zhao--Cui route |
| P45-M4 | predator-prey | no | equality metrics absent due to missing dense closure reference and multistate Zhao--Cui route |

## Local Evidence

| Command | Result |
| --- | --- |
| `python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p45-cross-model-error-calibration-2026-06-08.json` | passed |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p45_target_registry.py tests/highdim/test_p45_multistate_zhaocui_route.py tests/highdim/test_p45_generalized_sv_comparison_blocker.py tests/highdim/test_p45_spatial_sir_comparison_blocker.py tests/highdim/test_p45_predator_prey_comparison_blocker.py tests/highdim/test_p45_cross_model_error_calibration.py` | 20 passed, 2 TFP deprecation warnings |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_p45_cross_model_error_calibration.py` | passed |
| `git diff --check -- tests/highdim/test_p45_cross_model_error_calibration.py docs/plans/bayesfilter-highdim-zhao-cui-p45-cross-model-error-calibration-2026-06-08.json` | passed |

## Claude Review

Iteration 1 returned `PASS_P45_M5_CODE_GOVERNANCE`.

Claude confirmed:

- M5's empty promoted-row list is consistent with upstream M2--M4 gates;
- blocked rows carry no fabricated value or gradient metrics;
- likelihood variance remains explanatory only and is not used to excuse bias;
- tests enforce absent equality metrics and nonclaims.

## Gate Markers

p45_evidence_manifest: `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase5-cross-model-error-calibration-evidence-manifest-p45-codex-supervised-20260608-055034.json`
p45_local_evidence_run: `COMPLETE`
p45_evidence_audit: `COMPLETE`
p45_result_note_substance: `COMPLETE`
p45_traceability_or_nonclaim: `COMPLETE`
p45_command_count: `4`
p45_long_run_used: `false`
