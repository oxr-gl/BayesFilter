# P12 Low-Rank Solver Route Claude Review Ledger

Date: 2026-06-19

## Status

`GOVERNANCE_REVIEW_AND_P12_HANDOFF_REVIEW_CONVERGED`

## Role Contract

Codex is supervisor and executor.

Claude Opus is a read-only reviewer only.  Claude may inspect bounded file
paths and report findings.  Claude may not edit files, run experiments, launch
agents, authorize boundary crossings, or decide scientific/product readiness.

## Review Loop

- Maximum five Claude rounds for the same material blocker.
- If Claude does not respond, Codex must run a tiny read-only probe after user
  approval.
- If the probe responds, Codex must redesign the review prompt rather than
  treating Claude as unavailable.
- Fixable P12-owned findings are patched visibly and followed by focused local
  checks.
- Shared-contract, other-lane, public-export, package-install, network, GPU,
  model-file, funding, product-capability, or scientific-claim boundary issues
  stop for human direction.

## Planned Review Rounds

| Round | Scope | Prompt artifact | Claude verdict | Codex action |
| --- | --- | --- | --- | --- |
| 1 | Master program, phase subplans, visible runbook | wrapper prompt, 2026-06-19 | `VERDICT: REVISE` | Patch stale launch status, Claude approval rule, CPU env commands, log write set, and pinned thresholds. |
| 2 | Focused repair review | `docs/benchmarks/logs/p12-low-rank-solver-route-claude-review-r2.log` | `VERDICT: REVISE` | Patch remaining stale Claude approval status, remove remaining deferral wording, and update this ledger. |
| 3 | Focused repair review | `docs/benchmarks/logs/p12-low-rank-solver-route-claude-review-r3.log` | `VERDICT: REVISE` | Patch stale live ledger status from round 1 to round 3 repair loop. |
| 4 | Focused convergence review | `docs/benchmarks/logs/p12-low-rank-solver-route-claude-review-r4.log` | `VERDICT: AGREE` | Governance review converged; proceed to P12-0 closeout and P12-1 intake. |
| 5 | Final retry for same governance blocker | N/A | N/A | Unused; governance converged at round 4. |

## Prompt Capsule

Do not paste whole files to Claude.  The prompt must provide bounded scope,
file paths, and required checks:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review the P12 low-rank solver route governance artifacts by path:
- <master program>
- <phase subplans>
- <visible runbook>

Check wrong baseline, proxy metrics promoted to pass criteria, missing stop
conditions, unfair comparisons, hidden assumptions, stale context, environment
mismatch, unsupported claims, artifact mismatch, and boundary safety.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

## Approval State

User approved Claude review on 2026-06-19.  Rounds 1, 2, and 3 completed with
`VERDICT: REVISE` on progressively narrower stale-governance findings.  Round
4 completed with `VERDICT: AGREE`; governance review converged within the
five-round limit.

## Round 1 Findings

Claude reported five material, fixable governance findings:

1. launched runbook status conflicted with stale "not launched" approval text
   and pending-approval statuses;
2. P12-0 allowed user deferral of Claude review while the master/P12-4 made
   Claude approval mandatory;
3. P12-2 replay commands omitted explicit `CUDA_VISIBLE_DEVICES=-1`;
4. P12 log output path was not in the owned write set;
5. replay thresholds were referenced but not pinned to concrete values/source.

Codex repaired the CPU environment commands, log-path ownership, and threshold
pinning before round 2.  Round 2 found two remaining stale approval/deferral
phrases plus this ledger's over-strong repair-complete wording.  Codex patched
those remaining P12-owned governance issues before round 3.

## P12-4/P12-5 Path-Only Review Addendum

After the user clarified that Claude should receive paths and bounded questions
only, Codex ran focused path-only review over the P12-4/P12-5 procedural
handoff scope.

| Round | Scope | Evidence artifact | Claude verdict | Codex action |
| --- | --- | --- | --- | --- |
| 1 | P12-4/P12-5 artifact review, path-only | wrapper output, 2026-06-19 | `VERDICT: REVISE` | Removed unsupported final-pass claim from local substitute review. |
| 2 | Focused repair review | wrapper output, 2026-06-19 | `VERDICT: REVISE` | Superseded stale ledger pass/complete wording and tightened finalization wording. |
| 3 | Focused repair review | wrapper output, 2026-06-19 | `VERDICT: REVISE` | Removed loose P12-5 subplan review-note wording. |
| 4 | Focused repair review | wrapper output, 2026-06-19 | `VERDICT: REVISE` | Added explicit P12-5 handoff condition requiring focused Claude `VERDICT: AGREE`. |
| 5 | Final focused repair review | `docs/benchmarks/logs/p12-low-rank-solver-route-claude-path-only-r5-final.log` | `VERDICT: AGREE` | Marked P12 lane-local handoff complete while preserving coordinator-merge deferral and non-claims. |

Round 5 reviewed only paths, not pasted file contents.  It confirmed that the
R4 handoff-condition issue was repaired, that stale shortcut language in the
reviewed scope is historical/problem-description text rather than live
completion criteria, and that no live P12 visible-execution complete claim
preceded the R5 agreement.
