# P22 Zhao--Cui Integrated Readable Companion Result

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P20 integrated Zhao--Cui companion and fixed-branch gradient note.
- P21 chair guide and implementation-ready mathematical specification.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive branch choices.
- No HMC convergence claim.
- No production implementation readiness claim.
- No executable prototype claim.

## Status

Decision: `ACCEPTED_AFTER_EXECUTION_REVIEW_ITERATION_5`.

Draft outputs created:

- P22 integrated readable companion note and PDF.
- P22 integration ledger with carry-forward map and size guardrail.
- P22 readable orientation ledger.
- P22 implementation specification ledger.
- P22 discrepancy report.
- P22 Claude review ledger.

## Current Draft Summary

P22 was produced by copying P20 as the spine and adding P21-derived material:

- non-summary contract;
- five-object reader orientation;
- neutral fixed-branch orientation blocks;
- carried-filter representation contract;
- finite-difference report schema.

Current size:

- P20: 4295 TeX lines, 50 PDF pages.
- P22: 4815 TeX lines, 55 PDF pages.

## Review History

Plan review:

- Iteration 1: Claude `REJECT`; Codex accepted all findings and patched plan.
- Iteration 2: Claude `ACCEPT`.

Execution review:

- Iteration 1: Claude `REJECT` for runnable/script framing, residual
  audience-coaching tone, and finite-difference ledger anchor inconsistency.
- Codex audit: all three findings classified `ACCEPT`.
- Patch applied: non-executable object-flow/example language, neutral titles,
  and P22-local finite-difference anchors P22-FD0a--P22-FD0e.
- Iteration 2: Claude `REJECT` for documentation/control consistency:
  lingering P19 FD ledger anchors, stale line counts, and stale pending-status
  artifacts.
- Codex audit: all three findings classified `ACCEPT`.
- Patch applied: implementation ledger now uses P22-local anchors for affected
  rows, size metrics are current, and status artifacts record iteration-2.
- Iteration 3: Claude `REJECT` for remaining code-like finite-difference
  vocabulary, stale post-iteration status language, and a branch-identity
  statement that was not local enough to the P22 scalar.
- Codex audit: all three findings classified `ACCEPT`.
- Patch applied: finite-difference status labels now use mathematical prose
  rather than typewriter/code labels, P22-FD6 states the local branch identity
  condition, stale status language was advanced to iteration-3, and size
  metrics were updated to the current TeX count.
- Iteration 4: Claude `REJECT` for exact-anchor incompleteness in three
  finite-difference implementation-ledger rows.
- Codex audit: the finding classified `ACCEPT`.
- Patch applied: added P22-FD7, P22-FD8, and P22-FD9 and updated the
  implementation ledger to cite those exact anchors. Current size after this
  patch is 4815 TeX lines and 55 PDF pages.
- Iteration 5: Claude `ACCEPT`.
- Codex audit: Codex independently agrees with acceptance.  Residual risks are
  recorded in the review ledger and discrepancy report.

No executable code was created.  P20 and P21 artifacts were not edited.

## Final Validation Summary

- PDF build: `PASS`, 55 pages.
- Anti-summary size guardrail: `PASS`, P22 is 4815 TeX lines and 55 pages
  versus P20's 4295 TeX lines and 50 pages.
- P20 carry-forward map: `PASS`, no failure flags recorded.
- P21 field-level controls: `PASS`, carried-filter anchors P22-K1--P22-K8 and
  finite-difference anchors P22-FD1--P22-FD9 are recorded.
- Claude review: `ACCEPTED_AFTER_EXECUTION_REVIEW_ITERATION_5`.
- Remaining limitation: P22 is still a mathematical document, not executable
  code, empirical validation, or proof that the adaptive Zhao--Cui branch is
  globally differentiable.
