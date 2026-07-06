# Nystrom Algorithm-Complete Claude Review Ledger

Date: 2026-06-21

Status: `CLOSED_FINAL_REVIEW_PASSED_AFTER_R5_REPAIR`

Claude is read-only reviewer only. Codex is supervisor/executor.

## Review Entries

### R1 - Master/Runbook/Subplan Packet

Reviewer: Claude read-only worker `nystrom-plan-review-r1`

Verdict: `VERDICT: REVISE`

Findings accepted by Codex:

- P02 had thresholds/ranks/fixtures implied rather than predeclared.
- P03 had ESS, residual, and normalization vetoes without exact thresholds or
  smoke shape/budget.
- P04 had required GPU rows, timeout budget, contamination rule, and
  busy/unsuitable GPU rule underdeclared.
- P01 did not explicitly require source-route/provenance schema fields despite
  the master program treating them as veto-relevant.
- Executable phases lacked exact commands/environment.

Repair action: patch the same master/subplan artifacts before execution and
rerun focused local checks plus a compact R2 read-only review.

### R2 - Repaired Packet

Reviewer: Claude read-only worker `nystrom-plan-review-r2`

Verdict: `VERDICT: AGREE`

Accepted findings:

- P02 fixtures, ranks, and thresholds are now predeclared.
- P03 smoke rows and thresholds are now predeclared.
- P04 GPU ladder, optional row, budgets, and GPU busy/unsuitable rule are now
  predeclared.
- Required schema fields are now explicit in master program and P01.
- Exact execution commands/environment are now present for executable phases.
- Boundary safety is consistent with `AGENTS.md`.

### R3 - Final Closeout Draft

Reviewer: Claude read-only worker `nystrom-closeout-review-r1`

Verdict: `VERDICT: REVISE`

Findings accepted by Codex:

- Final result was internally inconsistent: the evidence-contract row described
  final Claude review as clean while the local closeout table still marked the
  review as `PENDING`.
- P05 was not fully reflected in closeout bookkeeping: the execution ledger
  still had `Status: OPEN` and its next action still said to execute P05, while
  the stop handoff was already closed.

Non-findings recorded by reviewer:

- P01-P04 result artifacts and P02-P04 benchmark JSON artifacts were present.
- P02 fixture-level gate was interpreted correctly; the `high_dim_low_rank`
  rank-2 miss was row-level only.
- No unsupported positive ranking/default/posterior/HMC/API/speedup claim was
  found in the final result or benchmark JSON summaries.
- GPU selection was consistent: physical GPU1 selected, with logical
  `/device:GPU:0` explained by `CUDA_VISIBLE_DEVICES=1` visibility remapping.

Repair action: patch final result, review ledger, and execution ledger to remove
pending/open contradictions, then run a focused R4 read-only review.

### R4 - Focused Closeout Bookkeeping Re-Review

Reviewer: Claude read-only worker `nystrom-closeout-review-r4`

Verdict: `VERDICT: REVISE`

Findings accepted by Codex:

- The R3 `PENDING` contradiction was repaired in the final result.
- The execution ledger was no longer `OPEN` and had a P05 closeout entry.
- The stop handoff was consistent with the execution ledger closed state.
- No new unsupported positive ranking/default/posterior/HMC/API/speedup claim
  was found in the checked closeout files.
- Remaining finding: the review ledger did not yet include the R4 record, while
  the execution ledger and final result implied final review convergence.

Repair action: record this R4 entry and run one final focused verification.

### R5 - Final Verification

Reviewer: Claude read-only worker `nystrom-closeout-review-r5`

Verdict: `VERDICT: REVISE`

Findings accepted by Codex:

- R4 was now recorded and the R4 finding was repaired.
- The earlier final-result `PENDING` contradiction was repaired.
- No unsupported positive ranking/default/posterior/HMC/API/speedup claim was
  found.
- Remaining finding: this review ledger header still said
  `PENDING_R5_FINAL_VERIFICATION` while final result and execution ledger
  described convergence.

Repair action: record this R5 entry and set the review ledger status to
`CLOSED_FINAL_REVIEW_PASSED_AFTER_R5_REPAIR`.  No further Claude loop is needed
because the only R5 finding is repaired by this entry and status update.
