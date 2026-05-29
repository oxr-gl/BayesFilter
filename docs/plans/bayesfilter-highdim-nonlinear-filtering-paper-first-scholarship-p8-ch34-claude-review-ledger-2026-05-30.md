# P8 Ch34 Claude Review Ledger

Date: 2026-05-30

metadata_date: 2026-05-30

seed_papers: P8 plan, Claude plan reviews, rewritten `ch34`, P8 ledgers, and
the scholarly literature audit policy.

what_is_not_concluded: Claude is a bounded hostile reviewer, not final
authority.  Claude review does not prove mathematical correctness, source
completeness, HMC convergence, posterior accuracy, production readiness, or PDF
quality by itself.

## Plan Review

| Iteration | Worker name | Decision | Codex audit/action |
|---|---|---|---|
| 1 | `highdim-p8-ch34-plan-review-iter1` | `REJECT` | Codex agreed.  Claude found the plan needed explicit source-support, claim-support, omission-risk, snowball, quarantine, and gradient support-class ledgers.  Codex patched the plan. |
| 2 | `highdim-p8-ch34-plan-review-iter2` | `ACCEPT` | Accepted.  Residual risks: forward snowballing remains inherited/no-new-network; execution must not drift into hidden authority or audit prose. |

## Execution Review

| Iteration | Worker name | Decision | Codex audit/action |
|---|---|---|---|
| 1 | `highdim-p8-ch34-exec-review-iter1` | `REJECT` | Codex agreed with the actionable findings.  Repairs applied: method headings now spell out acronyms before abbreviations; high-degree CKF, tensor-product GHQF, SGQF, and ASGHF sections now include explicit exact-versus-approximate paragraphs and method-local limitations; the gradient section now states that \(\xi^{(r)}\) and weights must be constant in the differentiated parameter unless extra derivative terms are included; the HMC table now names scalar \(\widehat\ell_t\) in its header and reasons; the stale boundary label was removed; source-support taxonomy was normalized. |
| 2 | `highdim-p8-ch34-exec-review-iter2` | `REJECT` | Codex agreed that the remaining issues were artifact-consistency repairs, not chapter-substance blockers.  Repairs applied: result note no longer says iteration 2 is pending; source-reconstruction ledger normalized `ch18` to `PROJECT_DERIVATION`; EKF/IEKF HMC table rows now explicitly tie labels to \(\widehat\ell_t\). |
| 3 | `highdim-p8-ch34-exec-review-iter3` | `REJECT` | Codex agreed that the result artifact still had stale current-decision text.  Repair applied: result note now records iteration 3 as rejected and sets the current decision to iteration-3-repaired/pending-iteration-4, not pending iteration 3. |
| 4 | `highdim-p8-ch34-exec-review-iter4` | `ACCEPT` | Accepted.  Claude found the iteration-3 artifact-consistency blocker repaired, support classes normalized, EKF/IEKF scalar wording fixed, and no remaining major P8 blocker.  Limits: PDF/citation validation was not part of Claude's review. |
