# Claude Review Ledger: N8192 Paired-Drift Diagnostic

Date: 2026-06-23

Status: `PENDING_P00_REVIEW`

Claude is read-only reviewer only.

## Reviews

### P00 Review Round 1

Reviewer: Claude Opus max effort, read-only through
`/home/ubuntu/python/claudecodex/scripts/claude_worker.sh`.

Verdict: `VERDICT: REVISE`

Findings:

- P01 declared `REPRODUCED_DRIFT` but had no handoff rule.
- P01 allowed P02 repair selection if any two of three rows failed, even if
  the original failed seed did not reproduce.
- P02 repair selection was underdetermined and exposed to ad hoc tuning.
- GPU fallback/provenance was acceptable but threshold-sensitive replay should
  be interpreted carefully.
- Fifteen-minute timeout needed justification.

Repair action:

- Replace P01 classification with:
  - `NON_REPRODUCED_OR_INCONCLUSIVE`;
  - `REPLAYED_SINGLE_SEED_DRIFT`;
  - `REPRODUCED_AND_REPEATED_DRIFT`;
  - `HARNESS_OR_NUMERICAL_INVALID`.
- Permit P02 only for `REPRODUCED_AND_REPEATED_DRIFT`.
- Add P02 predeclared routing rules for rank, epsilon, or solver repair.
- Record that the 15-minute timeout is conservative relative to the previous
  `N=8192` row's roughly 33.5 second runtime.

### P00 Review Round 2

Reviewer: Claude Opus max effort, read-only through
`/home/ubuntu/python/claudecodex/scripts/claude_worker.sh`.

Note: the approval reviewer blocked the first round-2 attempt as data export
risk. The user explicitly approved the bounded local plan review before this
round was rerun.

Verdict: `VERDICT: AGREE`

Findings:

- Round-1 gating blocker fixed.
- Original failed seed must now reproduce before repair can open.
- P02 repair selection underdetermination fixed by predeclared routing rules.
- Timeout justification fixed.
- No remaining material governance blocker to P01 launch.
