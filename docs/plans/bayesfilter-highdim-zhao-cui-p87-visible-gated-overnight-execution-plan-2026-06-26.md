# P87 Visible Gated Overnight Execution Plan

Date: 2026-06-26

## Status

`P87_VISIBLE_EXECUTION_RUNBOOK_REVIEWED_CLAUDE_AGREE`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus is a read-only reviewer only. Claude is not an execution authority
and cannot authorize human, runtime, model-file, funding, product-capability,
or scientific-claim boundaries.

This is an overnight-style gated plan in artifact naming only. It follows the
visible gated execution template and must not launch detached or nested agents.
Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, detached `tmux`, or background phase runners;
- copied-workspace execution.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p87-sir-d18-analytical-gradient-source-route-master-program-2026-06-26.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p87-claude-review-ledger-2026-06-26.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p87-visible-execution-ledger-2026-06-26.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p87-visible-stop-handoff-2026-06-26.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Mistake ledger and evidence contract | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase0-mistake-ledger-evidence-contract-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase0-mistake-ledger-evidence-contract-result-2026-06-26.md` |
| 1 | Current route audit | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase1-current-route-audit-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase1-current-route-audit-result-2026-06-26.md` |
| 2 | Analytical route repair | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase2-analytical-route-repair-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase2-analytical-route-repair-result-2026-06-26.md` |
| 3 | Local SIR algebra certification | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase3-local-sir-algebra-certification-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase3-local-sir-algebra-certification-result-2026-06-26.md` |
| 4 | Horizon-0 d18 value/gradient gate | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase4-horizon0-d18-value-gradient-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase4-horizon0-d18-value-gradient-result-2026-06-26.md` |
| 5 | Tiny full-history exact regression | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase5-tiny-full-history-regression-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase5-tiny-full-history-regression-result-2026-06-26.md` |
| 6 | d18 full-history feasibility gate | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase6-d18-full-history-feasibility-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase6-d18-full-history-feasibility-result-2026-06-26.md` |
| 7 | Source-route rank/degree gate | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase7-source-route-rank-degree-gate-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase7-source-route-rank-degree-gate-result-2026-06-26.md` |
| 8 | Correctness-candidate bridge gate | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase8-correctness-candidate-bridge-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase8-correctness-candidate-bridge-result-2026-06-26.md` |
| 9 | Final claim gate and handoff | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase9-final-claim-gate-subplan-2026-06-26.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase9-final-claim-gate-result-2026-06-26.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What Zhao-Cui SIR d18 value/gradient claim level is supported after applying no-regression gates from P81/P83/P86? |
| Baseline/comparator | P81 route correction and full-history notes; P83 execution-only/source-route handoff; P86 training-base/L1/rank-degree evidence; current code audit. |
| Primary pass criterion | A phase can pass only with exact artifacts, local checks, no veto diagnostics, and explicit claim/nonclaim language. |
| Veto diagnostics | `BLOCK_HORIZON0_OVERCLAIM`, `BLOCK_ANALYTICAL_ROUTE_HAS_JVP_COMPONENT`, `BLOCK_D18_ALL_PAIRS_DRIFT`, `BLOCK_PROXY_PROMOTION`, `BLOCK_SOURCE_CLAIM_UNGROUNDED`, `BLOCK_ALS_REVIVAL`, `BLOCK_TRAINING_DISCIPLINE_MISSING`. |
| Explanatory diagnostics | Branch hashes, FD rows, route backend strings, model-score comparisons, fit/holdout residuals, validation events, ESS, runtime/memory. |
| Not concluded | Production, HMC, posterior correctness, d50/d100 scaling, source-route correctness, or LEDH superiority unless separately gated. |
| Artifacts | P87 master, subplans, results, ledgers, review records, and any phase JSON manifests. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Visible execution only | Runbook template | Recoverable and avoids hidden detached agents | Hidden state or unreviewed actions | No detached launch scripts | reviewed by template |
| CPU-only for local doc/test phases | Repo GPU policy | Phases 0-3 do not require GPU; GPU use needs trusted escalation | Mistaking CPU-only for production target | Record `CUDA_VISIBLE_DEVICES=-1` when used | baseline |
| Claude as read-only reviewer | User request and AGENTS policy | Independent plan audit without execution authority | Claude edits/runs/overbroad review | One-path bounded prompts, review ledger | baseline |
| Analytical route must be JVP-free | P81 route correction | Prevents the main prior mistake | JVP drift into promoted comparator | `rg ForwardAccumulator target_derivative_backend` | binding |
| Source-route claim requires anchors | AGENTS Zhao-Cui gate | Prevents local diagnostic source-faithfulness overclaim | Unanchored faithful claim | source anchor audit | binding |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and the
execution ledger for material phases.

Check:

- wrong baselines;
- proxy metrics promoted to pass criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If a material flaw is found, revise the plan or write a blocker note before
running that phase.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites.
   - Restate the phase evidence contract in chat.
   - Append a ledger entry.
2. `EXECUTE_MINIMAL`
   - Run only visible commands in the current conversation.
   - Prefer the smallest diagnostic or implementation needed.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against primary criterion and veto diagnostics.
   - Write/update the phase result.
4. `PASS_REVIEW`
   - Use Claude read-only review for material crossings.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, write a blocker plan, review if material, repair
     visibly, rerun focused checks, and record the blocker result.
   - Stop after five Claude rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write handoff if a human-required blocker appears.

## Claude Read-Only Review Template

Use bounded prompts:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <path>. Do not edit,
run commands, launch agents, or review the whole repo. Question: <one question>.
End with VERDICT: AGREE or VERDICT: REVISE.
```

If Claude does not respond, Codex may run a tiny escalated probe. If the probe
responds, the prompt must be redesigned narrower before retrying.
Record every Claude nonresponse, probe command, probe outcome, and prompt
redesign in the execution ledger and Claude review ledger before retrying the
material review.

## Anticipated Escalation/Approval Needs

- Claude Code read-only reviews through
  `/home/chakwong/python/claudecodex/scripts/claude_worker.sh`, escalated
  because Claude uses external model/API access.
- GPU/CUDA commands only if a later phase explicitly requires GPU evidence.
  None are needed for Phases 0-3 as drafted.
- Long training or benchmark commands only after their exact subplan/result
  artifacts and evidence contract are frozen and reviewed.

## Human-Required Stop Conditions

Stop if continuing would require:

- changing pass/fail criteria after seeing results;
- destructive git/filesystem actions;
- package installation, network fetch, credentials, or environment setup beyond
  Claude review;
- broad default-policy changes;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted evidence;
- continuing after five non-convergent Claude review rounds.

## Final Visible Handoff

When execution completes or stops, write:

- final phase reached;
- final status;
- result artifacts;
- Claude review trail;
- tests actually run;
- unresolved blockers;
- what was not concluded;
- safest next decision.
