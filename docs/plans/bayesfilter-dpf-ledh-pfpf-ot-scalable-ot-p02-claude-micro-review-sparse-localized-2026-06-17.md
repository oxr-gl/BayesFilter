# Phase 2 Claude Micro Review: Sparse/Localized

Date: 2026-06-17

## Prompt Scope

One claim, no file reading:

Sparse/localized lane is `source_reference_only` and diagnostic-first; exact
only if certified sparse support/locality holds, otherwise approximate/reference.
Phase 1 dense baseline is used for locality/support diagnostics.  No sparse
implementation before locality and residuals pass; no speedup/ranking/default
claim.

## Claude Output

Boundary-safe: yes-this preserves the sparse/localized lane as
source-reference/diagnostic-first, uses Phase 1 dense only as a
locality/support diagnostic baseline, and blocks
implementation/promotion/speed/default claims until locality and residual gates
pass.

Small precision caveat: "exact" should mean exact only for the certified sparse
operator under the stated support/locality assumptions, not a broader
correctness or superiority claim.

VERDICT: AGREE

## Codex Disposition

Accepted as micro-review convergence for the sparse/localized lane.  The
precision caveat is already represented by the diagnostic-first wording and by
blocking sparse implementation until locality and residual gates pass.
