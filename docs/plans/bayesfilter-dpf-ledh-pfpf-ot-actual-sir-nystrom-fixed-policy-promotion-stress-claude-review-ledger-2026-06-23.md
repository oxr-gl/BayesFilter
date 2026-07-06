# Claude Review Ledger: Fixed-Policy Promotion-Stress

Date: 2026-06-23

Status: `PENDING_P00_REVIEW`

Claude is read-only reviewer only. Claude is not an execution authority and
cannot authorize human, runtime, model-file, funding, product-capability,
default-policy, or scientific-claim boundary crossings.

## Reviews

### P00 Review Round 1

Reviewer: Claude Opus max effort, read-only through
`/home/ubuntu/python/claudecodex/scripts/claude_worker.sh`.

Verdict: `VERDICT: REVISE`

Findings:

- Boundary inconsistency: the runbook forbade nested agents while the program
  anticipated Claude review through the wrapper.
- P03 artifact/question mismatch: the planned tiny CPU-hidden HMC fixture could
  pass without exercising the fixed actual-SIR Nystrom route.
- Review-flow inconsistency: the runbook implied every phase required Claude
  review while P01/P02 made it conditional.
- Optional row thresholds used vague "reasonable" / "acceptable" language.
- P02 history-payload audit did not name concrete artifact fields.

Repair action:

- Patch the plan/runbook/subplans to allow only bounded read-only Claude
  review, make P03 Nystrom-specific, make review requirements phase-specific,
  predeclare optional-row thresholds, and name concrete P02 history fields.

### P00 Review Round 2

Reviewer: Claude Opus max effort, read-only through
`/home/ubuntu/python/claudecodex/scripts/claude_worker.sh`.

Verdict: `VERDICT: AGREE`

Findings:

- Prior boundary inconsistency fixed.
- Prior P03 artifact/question mismatch fixed.
- Prior review-flow inconsistency fixed.
- Prior optional-row threshold ambiguity fixed.
- Prior P02 history-payload ambiguity fixed.
- No remaining material blocker to P01 launch.

### Final Closeout Review

Reviewer: Claude Opus max effort, read-only through
`/home/ubuntu/python/claudecodex/scripts/claude_worker.sh`.

Verdict: `VERDICT: AGREE`

Findings:

- P01 result values match inspected JSON artifacts.
- P01 failure classification is correct: launched optional `N=8192` failed the
  aggregate paired mean log-likelihood threshold.
- P02/P03 should be skipped under the documented lane logic.
- No unsupported default/HMC/posterior/superiority claims found.
- No statistical overclaiming found.
- Recommended next action is boundary-safe.
