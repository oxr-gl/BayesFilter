# SSL-LSTM Filter-HMC Claude Review Ledger

Date: 2026-07-04

Status: `OPEN`

## Role Boundary

Codex is supervisor and executor. Claude is read-only reviewer only. Claude
cannot authorize boundary crossings or replace local checks.

## Planned Review Gates

| Gate | Review bundle | Scope | Max rounds for same blocker | Status |
| --- | --- | --- | --- | --- |
| Phase 0 plan review | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase0-claude-review-bundle-2026-07-04.md` | Master program, visible runbook, phase subplan coverage, Phase 1 handoff, boundary safety | 5 | `PENDING_LOCAL_CHECKS` |
| Material implementation phases | Phase-specific bounded bundles; Claude first, then one Codex read-only substitute review on the same bundle if Claude fails to return a material verdict | Diffs, result artifacts, and next subplans only | 5 | `NOT_STARTED` |

## Review Entry Template

| Round | Timestamp | Command/log artifact | Claude status | Codex classification | Action |
| --- | --- | --- | --- | --- | --- |
| `<n>` | `<timestamp>` | `<.claude_reviews/...>` | `<AGREE/REVISE/no_verdict/...>` | `<material/already-covered/out-of-scope/human-boundary>` | `<continue/patch/stop>` |

## Current Entries

| Round | Timestamp | Command/log artifact | Claude status | Codex classification | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | 2026-07-04T04:10:00+08:00 | Rejected before launch by approval reviewer; no `.claude_reviews` run directory created | `NOT_RUN_APPROVAL_REJECTED` | `human-boundary` | Stop and ask user whether to explicitly approve exporting bounded planning docs to Claude, or authorize a Codex-only review exception |
| Exception | 2026-07-04 user message | Conversation authorization | `USER_AUTHORIZED_CODEX_ONLY_PHASE0_EXCEPTION` | `human-authorized-review-exception` | Continue to Phase 1 without Claude review for Phase 0 only |
| Exception | 2026-07-04T11:49:20+08:00 user continuation | Conversation authorization | `USER_DIRECTED_CODEX_ONLY_PHASE2_CONTINUATION` | `human-authorized-review-exception` | Continue to Phase 3 without Claude review for Phase 2 only; no external export occurred |
| Pending | 2026-07-04T12:12:00+08:00 | No command run | `PHASE3_LOCAL_CHECKS_PASSED_PENDING_REVIEW_DECISION` | `human-boundary` | Stop before Phase 4 execution for Phase 3 Codex-only exception, bounded Claude export approval, or review requirement change |
| Fallback | 2026-07-04 user message | Conversation authorization | `USER_AUTHORIZED_CODEX_SUBSTITUTE_REVIEW_ON_CLAUDE_FAILURE` | `human-authorized-review-exception` | If a bounded Claude review gate fails to return a material verdict for Phases 3-8, run a separate Codex read-only substitute review on the same bounded bundle and record the result |
| Fallback | 2026-07-04T22:47:46+08:00 | `docs/reviews/ssl-lstm-phase4-blocked-codex-substitute-review.md` | `AGREE` | `material` | Continue to Phase 5 planning checks; review path fell back, phase blocker remained recorded |
| Fallback | 2026-07-05T02:12:24+08:00 | `docs/reviews/ssl-lstm-phase6-phase7-codex-substitute-review.md` | `AGREE` | `material` | Continue to Phase 7 planning checks; Claude gate did not return a material verdict and the authorized Codex substitute review agreed |
| Attempt | 2026-07-05T03:45:00+08:00 | No `.claude_reviews` run directory created | `NOT_RUN_APPROVAL_TIMEOUT` | `human-boundary` | Retry once because the automatic approval review timed out before Claude launched |
| Attempt | 2026-07-05T03:47:00+08:00 | No `.claude_reviews` run directory created | `NOT_RUN_APPROVAL_TIMEOUT` | `human-boundary` | Switch to user-authorized separate Codex read-only substitute review on the same bounded bundle |
| Fallback R1 | 2026-07-05T03:55:00+08:00 | `docs/reviews/ssl-lstm-phase7-phase8-codex-substitute-review.md` | `REVISE` | `material` | Patch Phase 8 reset-memo artifact coverage and rerun focused checks/review |
| Fallback R2 | 2026-07-05T03:59:00+08:00 | `docs/reviews/ssl-lstm-phase7-phase8-codex-substitute-review.md` | `AGREE` | `material` | Phase 7/8 closeout review converged; final boundary may close at launch-smoke evidence only |

## Blocker Detail

Attempted command:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/ubuntu/python/BayesFilter \
  --review-name ssl-lstm-filter-hmc-phase0-plan-review-r1 \
  --bundle docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase0-claude-review-bundle-2026-07-04.md \
  --model opus \
  --effort max \
  --probe-effort low \
  --timeout-seconds 180 \
  --probe-timeout 90 \
  --max-retries 1
```

The approval reviewer rejected the action because it would send repo-local
planning documents and possibly related workspace context to an external Claude
service. No Claude process was launched.

This was a human-boundary blocker, not a plan-convergence blocker. The user
authorized continuing without Claude review for Phase 0. Codex must not treat
this as a blanket exception for future material phases.

Phase 2 repeated the same external-export boundary. The user then directed
Codex to continue with the runbook after the Phase 2 handoff identified the
review decision. Codex treated that as a local no-export continuation for Phase
2 only. Future material Claude exports still require explicit approval or a
phase-specific no-export exception.

Phase 3 local checks passed, but no Phase 3 Claude review was attempted. Phase
4 execution is stopped at the same human/export boundary until the user makes a
Phase 3-specific review decision.

If Claude fails to return a material verdict for a later bounded review gate,
the user-authorized fallback is a separate Codex read-only substitute review on
the same bounded bundle. The fallback does not authorize scope expansion or
execution authority transfer.

The Phase 4 bounded Claude gate did not return a material verdict, so the
authorized Codex substitute review was executed on the same bounded bundle and
returned `VERDICT: AGREE`. The Phase 4 implementation blocker remains in force;
only the review path fell back.

The Phase 7/8 bounded Claude gate did not launch because the escalation
approval review timed out twice before any Claude process or `.claude_reviews`
run directory was created. Codex then used the user-authorized separate
read-only substitute review on the same bounded bundle. Round 1 returned
`VERDICT: REVISE` for a missing Phase 8 reset-memo artifact/path. Codex patched
the reset memo, Phase 8 closeout, and review bundle, reran focused checks, and
the substitute review returned `VERDICT: AGREE` in Round 2. This closeout is
still only launch-smoke evidence, not convergence, ranking, posterior
correctness, source-faithfulness, GPU readiness, or default-readiness evidence.
