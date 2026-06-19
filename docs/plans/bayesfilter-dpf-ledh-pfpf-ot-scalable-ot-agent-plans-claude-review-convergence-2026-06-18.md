# Claude Review Convergence: Agent A/B Reduced-Rank Nystrom Plans

Date: 2026-06-18
Timestamp: 2026-06-18T16:49:00+08:00

## Scope

Claude reviewed these plans in a bounded read-only loop:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-agent-a-reduced-rank-nystrom-ladder-plan-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-agent-b-independent-test-review-harness-plan-2026-06-18.md`

The review was limited to plan adequacy.  No implementation, diagnostics,
package installs, network fetches, GPU execution, commits, or default-policy
changes were requested or performed.

## Review Loop

| Round | Outcome | Action |
| --- | --- | --- |
| Initial broad attempt | Stalled without usable verdict | Stopped and retried with a narrower prompt. |
| Round 1 | `VERDICT: REVISE` | Accepted material findings and patched both plans. |
| Round 2 | `VERDICT: AGREE` | Review converged; no material findings remained. |

## Round 1 Material Findings And Repairs

| Finding | Repair |
| --- | --- |
| Agent A comparator wording could allow schema-warning labels because Phase 3 expects `baseline_comparator` to start with `phase1_dense_streaming`. | Agent A now requires every nested `candidate_record.baseline_comparator` to begin `phase1_dense_streaming` and clarifies dense-reference errors are against the dense member of the local dense/streaming comparator pair. |
| Agent B independence was weakened by allowing Agent B to patch Agent A-owned files during the same review pass. | Agent B is now read-only on Agent A-owned implementation, diagnostic, JSON/Markdown, and result-note files during the initial independent review pass; repairs require a follow-up handoff/amendment after the independent verdict. |
| Agent B blocked-status naming had a shortened alias. | Agent B now consistently uses `PHASE_11_NYSTROM_INDEPENDENT_REVIEW_BLOCKED_WAITING_FOR_AGENT_A_ARTIFACTS` and forbids shortened aliases. |
| Agent B core command included Agent A's test file in the independent pass/fail gate. | Agent B's core independent gate now uses `tests/test_nystrom_transport_tf_independent.py` plus the independent review script; Agent A's test file is supplementary regression context only. |

## Open Questions Resolved In Plan Text

- Phase 11 JSON is now declared as a manifest containing one Phase 3-valid
  `candidate_record` per fixture/rank record plus a summary section.
- Dense-reference max/RMS error fields are required for every fixture/rank,
  including `high_dim_locality`, even when those fields are explanatory only.
- The `ledh_specific_smoke` fixture construction must be pinned in the
  diagnostic script and summarized in the result artifact.
- Agent B must not edit Agent A's result note before the initial independent
  verdict.

## Round 2 Verdict

Claude returned:

`VERDICT: AGREE`

No material findings remained.

## Residual Risks

- `high_dim_locality` dense-reference errors remain explanatory rather than a
  reduced-rank promotion threshold; this is intentional because Phase 8 already
  found locality issues on Phase 1 fixtures.  Future reviewers must not confuse
  explanatory role with optional emission.
- Agent B's review quality will depend on the independent review script
  actually checking the declared manifest invariants and
  `baseline_comparator` prefix rule.

## Status

`AGENT_A_B_REDUCED_RANK_NYSTROM_PLANS_CLAUDE_REVIEW_CONVERGED`

