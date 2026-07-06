# Actual-SIR Nystrom Stability Repair Claude Review Ledger

Date: 2026-06-23

Status: `P04_SELECTION_REVIEW_CONVERGED`

## Review Protocol

Claude Opus max effort is read-only reviewer only.  Prompts must provide a
bounded target list and ask Claude to inspect local files.  Do not paste whole
files into the prompt.

Each material review must check:

- wrong baseline;
- proxy metrics promoted to pass criteria;
- missing stop condition;
- unfair comparison;
- hidden assumption;
- stale context;
- environment mismatch;
- unsupported claim;
- artifact mismatch;
- boundary safety.

Claude must end with exactly `VERDICT: AGREE` or `VERDICT: REVISE`.

## Reviews

### P00 Round 1

- Log: `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p00-claude-review-r1-2026-06-23.log`
- Verdict: `REVISE`
- Material fixes requested: Claude wrapper exception, GPU run manifest
  requirements, P01 write boundary, fixed-policy branch scoping.

### P00 Round 2

- Log: `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p00-claude-review-r2-2026-06-23.log`
- Verdict: `REVISE`
- Material fix requested: P04 optional confirmation row must require exact
  artifact/log/run-manifest details before execution.

### P00 Round 3

- Log: `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p00-claude-review-r3-2026-06-23.log`
- Verdict: `AGREE`
- Result: no material remaining plan-level finding.

### P03 Round 1

- Log: `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p03-subplan-claude-review-r1-2026-06-23.log`
- Verdict: `REVISE`
- Material fixes requested: bracket both failing rows, specify exact
  commands/environment/artifact/log details, add prefix-specific stop
  conditions, and align P04 handoff with blocker-classification path.

### P03 Round 2

- Log: `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p03-subplan-claude-review-r2-2026-06-23.log`
- Verdict: `NO_OUTPUT_INTERRUPTED_AFTER_PROBE_DECISION`
- Result: interrupted after repeated empty polls; a small Claude probe returned
  `CLAUDE_PROBE_OK`, so the prompt was treated as too broad rather than Claude
  availability failure.

### P03 Round 2 Redesigned

- Log: `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p03-subplan-claude-review-r2-redesigned-2026-06-23.log`
- Verdict: `AGREE`
- Result: launch-safety review converged for the refreshed P03 prefix
  localization subplan.

### P04 Round 1

- Log: `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p04-selection-claude-review-r1-2026-06-23.log`
- Verdict: `REVISE`
- Material fixes requested: make the proposed repair behavior distinct from the
  already-floored raw Sinkhorn update denominators; require a discriminating
  raw-vs-repair fixture so a no-op implementation cannot pass; carry P06
  paired-comparison invariants into the P05 handoff.

### P04 Round 2

- Log: `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p04-selection-claude-review-r2-2026-06-23.log`
- Verdict: `AGREE`
- Result: focused re-review converged after P04/P05 were revised to select an
  opt-in `positive_projected` Nystrom kernel diagnostic and require projection
  floor-hit evidence.
