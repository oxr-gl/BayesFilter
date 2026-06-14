# P24 Zhao--Cui Claude Review Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports."
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific
  Computing, 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.

what_is_not_concluded:
- No claim that the P24 note has been executed or accepted.
- No claim that the Zhao--Cui literature coverage is complete.
- No claim that the fixed-branch derivative is the derivative of the adaptive
  Zhao--Cui algorithm.
- No production implementation claim.
- No exact posterior accuracy claim.

## Plan Review Iteration 1

reviewer: Claude Code bounded hostile reviewer

command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p24-zhao-cui-human-facing-plan-review-iter1 \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt>"
```

decision: `REJECT`

### Finding 1

Claude finding:

Missing the policy-mandated literature ledgers: the plan required cleanup,
chair-gap, implementation, citation, review, and discrepancy artifacts, but not
the separate scholarly-audit ledgers required by policy.

Codex classification: `ACCEPT`

Codex audit:

Materially correct.  A polished P24 human-facing note still needs a separate
audit trail for source support, citation/venue metadata, backward snowballing,
forward snowballing, claim support, and omitted-paper risk.

Control added:

- Added the six required scholarly-audit ledgers to `Required Outputs`.
- Added source-provenance pass criteria and veto diagnostics.
- Added validation gates requiring all six ledgers and required provenance
  fields.

### Finding 2

Claude finding:

No explicit retraction, quarantine, erratum, or version-conflict control.

Codex classification: `ACCEPT`

Codex audit:

Materially correct.  Citation style alone does not establish source reliability.

Control added:

- Added required source-support ledger fields for publication status,
  full-text status, local artifact path, retraction/withdrawal/expression of
  concern, erratum, quarantine, and version-consistency status.
- Added veto diagnostics for missing source-status checks or recorded blockers.

### Finding 3

Claude finding:

No mandatory backward/forward snowballing or omission-risk register.

Codex classification: `ACCEPT`

Codex audit:

Materially correct under the scholarly literature audit policy.  P24 can remain
human-facing while the review substrate records omission risk separately.

Control added:

- Added required backward-snowball, forward-snowball, and omitted-paper-risk
  ledger fields.
- Added execution steps to inspect prior ledgers, record snowballing results,
  and record metadata blockers rather than invent unavailable metadata.
- Added validation gates for actioned snowballing entries or explicit blockers.

### Finding 4

Claude finding:

Claim-support discipline is too coarse: citation style is enforced, but exact
technical anchor mapping is not.

Codex classification: `ACCEPT`

Codex audit:

Materially correct.  A generic `\cite{...}` is insufficient for a mathematical
or algorithmic claim unless the relevant source section/equation/algorithm or
project derivation is recorded.

Control added:

- Added claim-support ledger fields mapping P24 claims to exact source anchors
  or explicit P24 derivation labels.
- Added execution-review and validation rejection criteria for major technical
  claims lacking exact source anchors or derivation support.

## Plan Review Iteration 2

reviewer: Claude Code bounded hostile reviewer

command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p24-zhao-cui-human-facing-plan-review-iter2 \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt with iteration-1 rejection summary>"
```

decision: `ACCEPT`

Claude summary:

- The patched plan now includes the six required scholarly-audit ledgers with
  concrete fields.
- Source reliability, version, retraction, quarantine, and erratum controls are
  explicit.
- Backward/forward snowballing and omission-risk controls are explicit and
  blocker-aware.
- Exact claim-to-anchor mapping is required, not only citation style.
- Human-facing note constraints remain strong.
- Chair and implementation gaps are controlled with enough mathematical
  specificity for plan stage.
- Allowed writes, validation gates, and veto diagnostics are concrete enough
  for execution review to have real blocking authority.

Codex classification: `ACCEPT`

Codex audit:

The acceptance is independently supported by the patched plan.  The plan now
separates the chair-facing note from the scholarly-audit substrate: P24 must
read as a normal mathematical note, while the ledgers carry source reliability,
claim support, snowballing, and omission-risk evidence.  No unresolved Claude
findings remain at plan-review stage.

Residual risks:

- Plan acceptance is not execution acceptance.
- Length guards can be gamed by filler, so execution review must judge
  mathematical substance and source anchoring, not only line/page counts.
- Forward-snowballing may remain limited if metadata access is unavailable;
  the plan requires recording that blocker rather than inventing coverage.

## Execution Review Attempts

reviewer: Claude Code bounded hostile reviewer

status: `TOOL_STALLED_FOR_FILE_REVIEW`

### Attempt 1

command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p24-zhao-cui-human-facing-exec-review-iter1 \
  --model sonnet --effort high \
  "<full bounded hostile execution review prompt>"
```

outcome:

- No review output was returned after repeated polling.
- The worker was stopped with `pkill -f
  highdim-p24-zhao-cui-human-facing-exec-review-iter1`.

### Attempt 2

command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p24-zhao-cui-human-facing-exec-review-iter1b \
  --model sonnet --effort high \
  "<narrowed section-targeted execution review prompt>"
```

outcome:

- No review output was returned after repeated polling.
- The worker was stopped with `pkill -f
  highdim-p24-zhao-cui-human-facing-exec-review-iter1b`.

### Claude Worker Smoke Test

command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p24-zhao-cui-human-facing-claude-smoke \
  --model sonnet --effort high \
  "First line exactly ACCEPT. Second line: smoke test complete. Do not edit files."
```

outcome:

```text
ACCEPT
smoke test complete
```

Interpretation:

- Claude worker authentication and minimal prompt execution worked.
- File-reading execution-review prompts stalled, so no substantive Claude
  execution-review findings were produced.

### Attempt 3

command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p24-zhao-cui-human-facing-exec-review-iter1c \
  --model sonnet --effort high \
  "<compact five-file top-blocker execution review prompt>"
```

outcome:

- No review output was returned after repeated polling.
- The worker was stopped with `pkill -f
  highdim-p24-zhao-cui-human-facing-exec-review-iter1c`.

Codex classification: `CLARIFY`

Codex audit:

Claude did not provide substantive execution-review findings to classify.  The
tooling failure blocks the plan's intended Claude execution-review acceptance.
Codex therefore performed a local supervisor audit and records the resulting
findings below, but this is not a substitute for completed Claude execution
review.

## Codex Supervisor Execution Audit Findings

### Finding C1

Codex finding:

The P24 main note cites Oseledets and Rosenblatt, but the source-support ledger
only listed Zhao--Cui, Cui--Dolgov, and the companion code snapshot.

Codex classification: `ACCEPT`

Control added:

- Added Oseledets 2011 and Rosenblatt 1952 rows to
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-source-support-ledger-2026-06-02.md`.
- Recorded local artifact paths, bibliography/status notes, inspected-use
  scope, allowed claims, and forbidden claims.

### Finding C2

Codex finding:

The source-support and metadata ledgers over-compressed version/status
provenance for Cui--Dolgov and Zhao--Cui.  In particular, P24 should not imply
fresh exhaustive live retraction or publisher-version reconciliation when the
note relies mainly on local full text and prior ledgers.

Codex classification: `ACCEPT`

Control added:

- Rewrote Zhao--Cui source status to state local full-text status and local
  quarantine/withdrawal/retraction/erratum/version-conflict checks, while
  forbidding a broad live-database conclusion.
- Rewrote Cui--Dolgov source status to distinguish the local arXiv artifact
  from prior-ledger FoCM status and to block claims depending on exact
  published-version wording without fresh reconciliation.
- Updated the citation/venue metadata ledger to record metadata blockers and
  not use citation counts as evidence.

### Finding C3

Codex finding:

The forward-snowball ledger said forward snowballing was "not required" too
flatly.  The plan allows blocker-aware scope control, but the ledger should
make clear that no literature-completeness or absence-of-follow-up claim is
being made.

Codex classification: `ACCEPT`

Control added:

- Rewrote the forward-snowball ledger to record a scope-limited blocker table
  for Zhao--Cui and Cui--Dolgov.
- Changed the decision to `FORWARD_SNOWBALL_SCOPE_LIMIT_RECORDED`.

Execution-review decision after Codex audit: `BLOCKED_BY_CLAUDE_REVIEW_TOOLING`

No Claude execution-review acceptance exists for P24.  Local validation and
Codex audit patches passed, but downstream acceptance should remain conditional
on either a successful later Claude execution review or explicit human
decision.
