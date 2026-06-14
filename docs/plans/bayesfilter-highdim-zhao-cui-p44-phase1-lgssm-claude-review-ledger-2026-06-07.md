# P44-M1 Claude Review Ledger: LGSSM Exact Baseline

metadata_date: 2026-06-08
phase: P44-M1
run_id: `p44-codex-supervised-20260608-013203`

p44_evidence_manifest: `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase1-lgssm-evidence-manifest-p44-codex-supervised-20260608-013203.json`
p44_claude_code_governance_verdict: `PASS_P44_M1_CODE_GOVERNANCE`
p44_claude_code_governance_iterations: `1`

## Repair Review Iteration 1

review_cycle: `1`
review_type: `repair`
review_iteration: `1`
status: `BLOCKED_P44_M1_REPAIR_REVIEW`

Scope:
- Read-only Claude review of the M1 CUT4 low-dimensional padding repair and
  Zhao--Cui artifact-lane boundary.
- Claude must not edit files, create artifacts, launch commands, or act as
  executor.

Reviewer/process summary:
- The first read-only repair review process ran silently long enough to be
  treated as an operational timeout and was stopped by Codex.
- No files were changed by the reviewer.
- This is not a substantive M1 repair blocker; Iteration 2 used a narrower
  read-only prompt.

## Repair Review Iteration 2

review_cycle: `1`
review_type: `repair`
review_iteration: `2`
status: `PASS_P44_M1_REPAIR_REVIEW`

Scope:
- Narrow read-only review of the dim-1 inert CUT4 padding repair, directional
  score coverage, Zhao--Cui artifact-lane nonclaim, and CPU-only logs.

Reviewer summary:
- The dim-1 padding is inert because the added innovation column is zero, so
  the physical process covariance remains unchanged.
- Dims 1, 2, and 3 are tested on value, full TensorFlow autodiff score, and
  seven deterministic directional residuals.
- The subplan honestly scopes the Zhao--Cui lane as fixed-design TT
  retained-density artifacts on the exact LGSSM path and does not promote the
  scalar TT propagation helper.
- The CPU-only pytest and compile logs are sufficient for the repair scope.

Decision:
- `PASS_P44_M1_REPAIR_REVIEW`

## Code/Governance Review Iteration 1

review_cycle: `1`
review_type: `code_governance`
review_iteration: `1`
status: `PASS_P44_M1_CODE_GOVERNANCE`

Scope:
- Read-only Claude review of the M1 subplan, focused test, result note,
  review ledger, evidence manifest, and CPU-only command logs.
- Claude must not edit files, create artifacts, launch commands, or act as
  executor.

Reviewer summary:
- Exact Kalman remains the governing baseline.
- CUT4 and the fixed-design TT artifact lane are compared against Kalman for
  dimensions 1, 2, and 3 on value, full TensorFlow autodiff score, and
  deterministic directional residuals.
- The dim-1 CUT4 padding repair is inert and reviewed.
- The scalar TT propagation helper mismatch is recorded as a nonclaim and
  guarded by a test.
- Manifest/result/ledger/logs are consistent apart from pending administrative
  closure fields, which this review authorizes Codex to update.

Decision:
- `PASS_P44_M1_CODE_GOVERNANCE`
