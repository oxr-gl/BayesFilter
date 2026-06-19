# P70 Phase 6c Result: First-Row Condition-Veto Root-Cause Diagnostic

metadata_date: 2026-06-16
status: PHASE6C_DIAGNOSTIC_COMPLETED_CLAUDE_AGREE_PHASE7_BLOCKED
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 6c
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

Phase 6c executed the reviewed one-row diagnostic for
`rank_candidate_1_2_fit36`, time index \(1\), degree \(1\), rank \(2\), and
\(n_{\rm fit}=36\).  It did not run the four-row Phase 6 wrapper and did not
change thresholds, row count, rank, degree, ridge, sweep order, initializer, or
source-route semantics.

The proximate root cause is an unscaled ALS design/normal-equation conditioning
failure after earlier accepted core updates.  The actual ALS path accepts 23
updates, then vetoes at axis \(23\) with
\[
  \kappa(A^\top W A+\rho I)\approx 1.236\times 10^{17},
  \qquad \rho=10^{-10},
\]
exceeding the P70 veto threshold \(10^{14}\).

The result does not support clipping as the cause for this row: the measured
clip fraction and boundary fraction are both \(0\).

## Artifacts

- Plan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6c-first-row-root-cause-diagnostic-plan-2026-06-16.md`
- Script:
  `scripts/p70_phase6c_first_row_root_cause_diagnostic.py`
- JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6c-first-row-root-cause-diagnostic-2026-06-16.json`

## Run Manifest

| Field | Value |
| --- | --- |
| Command | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p70_phase6c_first_row_root_cause_diagnostic.py` |
| Exit status | `0` |
| CPU/GPU status | CPU-only intended with `CUDA_VISIBLE_DEVICES=-1`; TensorFlow still emitted CUDA plugin/cuInit messages as before. |
| Git HEAD recorded by artifact | `94069066a70df6f1f0f2b53d32b9d452bd67f891` |
| Dirty worktree | yes |
| Model seed | `5901` |
| Prior sample seed | `6301` |
| Process noise seed | `6401` |
| JSON size | about 248 KB |

## Root-Cause Ranking

1. Primary: unscaled ALS columns plus absolute normal-equation ridge.
   At the failing axis, the design has column-norm spread
   \(4.586\times 10^{11}\), \(\kappa(A)\approx 3.652\times 10^{12}\), and
   \(\kappa(A^\top W A+\rho I)\approx 1.236\times 10^{17}\).  As an
   explanatory-only check, column-normalizing the same design gives normal
   condition about \(7.72\times 10^2\), and trace-scaled ridge gives about
   \(7.60\times 10^{10}\).  These are diagnostics only, not repairs.

2. Primary contributor: ALS gauge/environment scale imbalance created during
   accepted updates.  Initial-axis diagnostics are already ill-conditioned but
   remain below the veto: maximum initial normal condition is about
   \(3.60\times 10^{11}\).  The veto appears only after 23 accepted updates,
   so the failing condition is path-created by the fitted environments.

3. Contributor: effective row and local-rank loss.  The resampled fit rows have
   26 unique source rows out of 36, with 10 duplicates and maximum duplicate
   multiplicity 3.  The centered local row rank is 25, not 35 or 36.

4. Background contributor: coordinate-frame rank boundary and jitter
   dependence.  The pre-jitter weighted covariance is singular, as expected at
   \(n_{\rm fit}=D=36\) after centering; one eigenvalue is jitter-dominated at
   the 10x diagnostic threshold.  The final frame matrix condition is about
   \(1.17\times 10^3\), so the frame is not the proximate explosion, but it
   contributes to the fragile data geometry.

5. Ruled out for this row: clipping/saturation.  Local maximum absolute value
   before clipping is about \(0.805\), with clip fraction \(0\) and boundary
   fraction \(0\).

6. Implementation smell, not this run's root cause: the helper accepts a
   `ridge` argument but constructs `FixedTTFitConfig(ridge=P70_FIT_RIDGE)`.
   In this diagnostic the supplied ridge equals `P70_FIT_RIDGE`, so this does
   not explain the observed veto, but it should be repaired or made explicit in
   a later implementation-cleanup phase.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Answered for the first failed row: why the first repaired fixed branch hits a condition-number veto. |
| Baseline/comparator | Exact Phase 6 first-row settings were reconstructed. |
| Primary criterion | Passed: JSON and result note rank the measured root-cause hypotheses. |
| Veto diagnostics | No four-row wrapper was run; failed fit remained failed; no transport was emitted; no tuning or threshold change occurred. |
| Explanatory-only diagnostics | Column-normalized and trace-scaled-ridge condition checks were recorded only as non-branch probes. |
| Not concluded | No fixed-variant repair, no Phase 6 pass, no validation, no rank/degree promotion, no scaling claim, no HMC readiness, no adaptive Zhao--Cui parity. |

## Decision Table

| Item | Status |
| --- | --- |
| Primary criterion | Passed for diagnostic scope. |
| Veto diagnostic status | Preserved: actual fitted branch still vetoes with `CONDITION_NUMBER_VETO`. |
| Main uncertainty | Whether the correct repair should be gauge/column normalization inside ALS, a scale-aware ridge, QR/SVD least squares, orthogonalized TT gauges, larger effective fit rows, or a combination. |
| Next justified action | Draft a focused repair-design plan for numerically stable fixed-variant ALS that preserves the fixed-HMC branch contract. |
| What is not concluded | The fixed variant is not repaired and Phase 7 remains blocked. |

## Checks Run

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p70_phase6c_first_row_root_cause_diagnostic.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p70_phase6c_first_row_root_cause_diagnostic.py
```

Both commands completed successfully.  TensorFlow emitted CUDA/cuInit messages
despite the CPU-only environment variable; this is consistent with previous
CPU-only artifacts and is not treated as GPU evidence.

## Next Handoff

Claude reviewed the Phase 6c execution/result and returned `VERDICT: AGREE`.
The next safe phase is a new repair-design subplan.  That plan should choose
among source-preserving numerical stabilizations such as gauge
normalization/orthogonalization, column-scaled normal equations, QR/SVD least
squares, and ridge scaling.  No repaired four-row diagnostic may run until a
new reviewed subplan and explicit user approval authorize it.
