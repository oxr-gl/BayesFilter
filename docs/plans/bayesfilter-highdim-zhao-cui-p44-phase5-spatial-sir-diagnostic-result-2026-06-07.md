# P44-M5 Result: Spatial SIR Diagnostic Closure

metadata_date: 2026-06-08
phase: P44-M5
run_id: `p44-codex-supervised-20260608-013203`
Status: `PASS_P44_M5_CODE_GOVERNANCE`

## Decision Table

| Field | Value |
| --- | --- |
| Decision | M5 spatial SIR diagnostic closure passed final read-only Claude code/governance review. |
| Primary criterion status | Passed locally as diagnostic-only: SIR model-contract anchor, negative-domain diagnostic, finite CUT4 value and diagnostic TensorFlow autodiff score, CUT4 metadata boundary, and executable no-Zhao--Cui-equality route. |
| Veto diagnostic status | No negative-population, native-SIR-overclaim, equality-overclaim, missing model-contract, nonfinite, point-cap, or compile veto fired. |
| Main uncertainty | This is not a native SIR likelihood or TT/SIRT result; no matched Zhao--Cui SIR equality target exists in this phase. |
| Next justified action | Run the P44-M5 executable phase gate, then proceed to P44-M6 if the gate passes. |
| Not concluded | No native SIR filtering correctness, no CUT4-vs-Zhao--Cui equality, no production TT/SIRT SIR filtering, no paper-scale SIR validation, no HMC readiness, no GPU readiness, and no stable score API readiness. |

## Evidence Contract

Question: for the smallest spatial-SIR diagnostic closure (`J=1`), can CUT4
evaluate a finite additive-Gaussian closure value and diagnostic score while
preserving model-contract anchors and explicit nonclaims?

Baseline/comparator:

- Governing baseline: SIR model-contract tests from `SpatialSIRSSM`, including
  RK4 transition source anchors, infectious-only observation convention, and
  negative-state domain diagnostics.
- CUT4 diagnostic closure: `tf_svd_cut4_filter` on a clean-room
  additive-Gaussian structural closure with `J=1`, horizon 2, augmented
  dimension 4, and point count 24.
- Zhao--Cui route: no matched non-scalar SIR equality target exists in this
  phase; the fixed-branch highdim value route rejects the non-scalar SIR model,
  and this is recorded as diagnostic-only nonclaim evidence.

Primary promotion criterion:

- `SpatialSIRSSM` source/model-contract metadata is present;
- negative populations are surfaced by domain diagnostics, not silently
  accepted as native correctness;
- CUT4 closure value and diagnostic TensorFlow autodiff score are finite;
- CUT4 metadata records diagnostic closure, point count, polynomial degree, and
  no innovation-floor events;
- the absence of a matched Zhao--Cui equality route is executable;
- diagnostic manifest blocks equivalence metrics and records nonclaims.

Veto diagnostics:

- negative populations silently accepted;
- closure diagnostics described as native SIR filtering;
- observed-only accuracy promoted as full state recovery;
- no source/model-contract anchor;
- CUT4-vs-Zhao--Cui equality claimed without a matched shared closure target;
- any finite diagnostic is promoted as production score API readiness.

Explanatory-only diagnostics:

- TensorFlow warning logs, wall time, CUT4 point count, polynomial degree,
  diagnostic score norm, and manifest schema checks.

Nonclaims:

- no native SIR filtering correctness;
- no production TT/SIRT SIR filtering;
- no CUT4-vs-Zhao--Cui equality;
- no paper-scale SIR validation;
- no adaptive MATLAB behavior;
- no GPU readiness;
- no HMC readiness;
- no DSGE readiness;
- no stable public API or score API readiness.

Artifact preserving the result:

- Result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase5-spatial-sir-diagnostic-result-2026-06-07.md`
- Evidence manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase5-spatial-sir-diagnostic-evidence-manifest-p44-codex-supervised-20260608-013203.json`
- Command logs:
  `docs/plans/logs/p44-codex-supervised-20260608-013203-P44-M5-command0.log`
  and
  `docs/plans/logs/p44-codex-supervised-20260608-013203-P44-M5-command1.log`

## Skeptical Audit

Status: `PASS_P44_M5_CODE_GOVERNANCE`.

- Wrong-baseline risk: there is no dense or Kalman baseline for native SIR in
  M5; the phase is therefore explicitly diagnostic-only.
- Proxy-metric risk: finite CUT4 value and score are not promoted to native
  correctness, equality, HMC readiness, or score API readiness.
- Target-mismatch risk: the test records that the current highdim fixed-branch
  route rejects non-scalar SIR, so no Zhao--Cui equality row is run.
- Negative-domain risk: a negative-state path is passed through domain
  diagnostics and checked as surfaced evidence.
- Resource risk: fixture is `J=1`, horizon 2, CPU-only, augmented dimension 4,
  and point count 24, within the phase cap.
- Hidden-assumption risk: the closure is named and labeled as additive-Gaussian
  diagnostic closure, not native SIR filtering.

## Local Evidence

Commands:

1. `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q -s tests/highdim/test_p44_spatial_sir_diagnostic.py`
2. `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p44_spatial_sir_diagnostic.py`

Observed result:

- Focused pytest: `5 passed`, exit code 0.
- Compile check: exit code 0.
- CUT4 diagnostic value: `-1.152078e+01`.
- CUT4 diagnostic score norm: `3.580805e+00`.
- CPU-only mode was deliberate; no GPU evidence is claimed. TensorFlow emitted
  CUDA initialization warnings despite `CUDA_VISIBLE_DEVICES=-1`; these are
  treated as explanatory-only because the phase is CPU-only.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `N/A - dirty worktree preserved; command manifest captures current files` |
| Command environment | CPU-only via `CUDA_VISIBLE_DEVICES=-1` and `MPLCONFIGDIR=/tmp` |
| Data version | deterministic in-test observations |
| Random seeds | deterministic fixture only; no stochastic run promotion |
| Wall time | tiny local validation only |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase5-spatial-sir-diagnostic-subplan-2026-06-07.md` |
| Test file | `tests/highdim/test_p44_spatial_sir_diagnostic.py` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase5-spatial-sir-diagnostic-result-2026-06-07.md` |

## Gate Markers

p44_evidence_manifest: `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase5-spatial-sir-diagnostic-evidence-manifest-p44-codex-supervised-20260608-013203.json`
p44_local_evidence_run: `COMPLETE`
p44_evidence_audit: `COMPLETE`
p44_result_note_substance: `COMPLETE`
p44_traceability_or_nonclaim: `COMPLETE`
p44_command_count: `2`
p44_long_run_used: `false`
