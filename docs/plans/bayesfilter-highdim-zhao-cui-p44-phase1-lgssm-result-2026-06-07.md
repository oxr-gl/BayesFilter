# P44-M1 Result: LGSSM Exact Baseline

metadata_date: 2026-06-08
phase: P44-M1
run_id: `p44-codex-supervised-20260608-013203`
Status: `PASS_P44_M1_CODE_GOVERNANCE`

## Decision Table

| Field | Value |
| --- | --- |
| Decision | M1 exact LGSSM baseline passed final read-only Claude code/governance review. |
| Primary criterion status | Passed: local tests pass for dimensions 1, 2, and 3; exact Kalman, CUT4 structural value path, and fixed-design TT retained-density artifact lane agree on value and diagnostic score for the declared four-coordinate parameterization. |
| Veto diagnostic status | No value, score, covariance, or normalizer nonfinite was observed. The initial CUT4 dim-1 augmented-dimension blocker was repaired with inert padding and reviewed by Claude. |
| Main uncertainty | M1 still does not promote an independent TT-propagated LGSSM likelihood; it tests the current Zhao--Cui-style retained-density artifact lane on the exact LGSSM path. |
| Next justified action | Run the executable P44-M1 phase gate, then proceed to P44-M2 if the gate passes. |
| Not concluded | No HMC readiness, no production score API, no paper-scale Zhao--Cui reproduction, no independent TT-propagated LGSSM likelihood correctness. |

## Evidence Contract

Question: for an exact linear Gaussian state-space model in dimensions 1, 2,
and 3, do CUT4 and the current Zhao--Cui/fixed-design TT artifact lane agree
with the exact Kalman value and diagnostic score in the same declared
unconstrained parameter vector?

Baseline/comparator:

- Baseline: exact covariance-form Kalman value and score through
  `FixedBranchSquaredTTFilter(... fit_config=None ...)`.
- CUT4 comparator: `tf_svd_cut4_filter` on the same affine structural target.
- Zhao--Cui/fixed-design TT lane: exact highdim LGSSM value path with
  fixed-design TT retained-density artifacts enabled.

Primary promotion criterion:

- Dims 1, 2, and 3 all pass value equality, full TensorFlow autodiff score
  equality, and at least five deterministic directional score residual checks.

Veto diagnostics:

- likelihood convention mismatch;
- covariance or parameter transform mismatch;
- CUT4 padding that changes the LGSSM physical target;
- treating scalar TT propagation helper mismatch as promoted M1 evidence;
- nonfinite value, score, covariance, or normalizer.

Explanatory-only diagnostics:

- TT artifact fit residuals, TT density normalizers, point counts, warning
  logs, wall time, and compile success.

Nonclaims:

- no HMC readiness;
- no production analytic score API;
- no paper-scale Zhao--Cui reproduction;
- no adaptive MATLAB TT-cross/SIRT reproduction;
- no independent TT-propagated LGSSM likelihood correctness.

## Skeptical Audit

Status: `PASS_P44_M1_CODE_GOVERNANCE`.

- Wrong-baseline risk: exact Kalman remains the governing baseline; CUT4 is not
  treated as truth.
- Proxy-metric risk: TT artifact fit status is not used as the sole correctness
  criterion. The scalar likelihood and score are checked against Kalman.
- Target-mismatch risk: M1 now explicitly states that the Zhao--Cui lane is the
  retained-density artifact path on the exact LGSSM value path, not the scalar
  nonlinear TT propagation helper.
- Low-dimensional CUT4 risk: raw CUT4-G intentionally rejects augmented
  dimension 2. The M1 fixture pads dim 1 with one inert innovation coordinate;
  the process covariance remains `L L^T` because the padding column is zero.
- Fairness risk: all three evaluators rebuild the same physical LGSSM from the
  same four-coordinate vector `(rho_raw, log_q, log_r, mu_raw)`.
- Gradient risk: the test checks full TensorFlow autodiff scores and seven
  deterministic directional residuals per dimension.

## Implementation And Repair Notes

- Added `tests/highdim/test_p44_lgssm_exact_baseline.py`.
- Patched the M1 subplan to declare the parameterization, CUT4 padding repair,
  and Zhao--Cui artifact-lane boundary.
- Initial focused run failed because `tf_cut4g_sigma_point_rule` requires
  augmented dimension at least 3 and dim-1 LGSSM has raw augmented dimension 2.
- Repair: pad only the M1 dim-1 structural CUT4 fixture with one inert
  innovation coordinate. This follows the existing P39/P40 padding precedent
  and leaves the generic CUT4-G rule unchanged.
- Claude repair review Iteration 2 returned `PASS_P44_M1_REPAIR_REVIEW`.
- Claude final code/governance review Iteration 1 returned
  `PASS_P44_M1_CODE_GOVERNANCE`.

## Local Evidence

Commands:

1. `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p44_lgssm_exact_baseline.py`
2. `python -m compileall -q bayesfilter/highdim tests/highdim/test_p44_lgssm_exact_baseline.py`

Observed result:

- Focused pytest: `3 passed`, exit code 0.
- Compile check: exit code 0.
- CPU-only mode was deliberate; no GPU evidence is claimed.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `N/A - dirty worktree preserved; command manifest captures current files` |
| Command environment | CPU-only for pytest via `CUDA_VISIBLE_DEVICES=-1`; compile check CPU-only |
| Data version | deterministic in-test observations |
| Random seeds | deterministic branch seeds embedded in fixture config |
| Wall time | tiny local validation only |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase1-lgssm-subplan-2026-06-07.md` |
| Test file | `tests/highdim/test_p44_lgssm_exact_baseline.py` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase1-lgssm-result-2026-06-07.md` |

## Gate Markers

p44_evidence_manifest: `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase1-lgssm-evidence-manifest-p44-codex-supervised-20260608-013203.json`
p44_local_evidence_run: `COMPLETE`
p44_evidence_audit: `COMPLETE`
p44_result_note_substance: `COMPLETE`
p44_traceability_or_nonclaim: `COMPLETE`
p44_command_count: `2`
p44_long_run_used: `false`
