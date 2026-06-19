# P73 Visible Gated Execution Runbook

Date: 2026-06-17

## Status

`P73_PHASE6_PASSED_CLAUDE_AGREE_COMPLETE`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

Claude review is performed through the foreground wrapper
`/home/chakwong/python/claudecodex/scripts/claude_worker.sh` when a material
phase requires it.  That wrapper is a bounded read-only review mechanism, not
an executor, supervisor, detached phase runner, or authority to advance gates.
Codex must inspect the returned review in this conversation, patch or block
visibly, and record the outcome in the ledgers.

This runbook must not launch a detached or nested agent.  Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

"Overnight" means the phase ladder may contain long visible commands that
Codex monitors and records.  It does not mean hidden autonomous execution.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-master-program-2026-06-17.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p73-claude-review-ledger-2026-06-17.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-execution-ledger-2026-06-17.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p73-visible-stop-handoff-2026-06-17.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Proposal review and governance reset | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase0-proposal-review-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase0-proposal-review-result-2026-06-17.md` |
| 1 | Source, literature, and objective-boundary audit | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase1-source-literature-objective-boundary-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase1-source-literature-objective-boundary-result-2026-06-17.md` |
| 2 | Mathematical design contract | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase2-density-aware-renewal-design-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase2-density-aware-renewal-design-result-2026-06-17.md` |
| 3 | Implementation surface audit and focused test plan | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase3-implementation-surface-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase3-implementation-surface-result-2026-06-17.md` |
| 4 | Opt-in implementation and unit tests | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase4-optin-implementation-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase4-optin-implementation-result-2026-06-17.md` |
| 5 | Bounded renewal diagnostic | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase5-bounded-renewal-diagnostic-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase5-bounded-renewal-diagnostic-result-2026-06-17.md` |
| 6 | Result decision and next-root-cause handoff | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase6-result-decision-subplan-2026-06-17.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p73-phase6-result-decision-result-2026-06-17.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can P73 design, implement, and bounded-diagnose an opt-in density-aware renewed-support fixed fit that addresses the P72 blockers without overclaiming? |
| Baseline/comparator | P72 real Phase 5 blocked diagnostic. |
| Primary pass criterion | A phase advances only when its result artifact exists, required checks pass, material Claude review converges, the next subplan exists, and exact handoff conditions are met. |
| Veto diagnostics | NeuTra analogy treated as proof, audit points used for coefficient selection, certification on newly added training points, source-faithfulness overclaim, threshold changes after outputs, downstream validation/HMC/scaling launch before lower-gate pass. |
| Explanatory diagnostics | Residuals, line probes, normalizers, condition numbers, singular spectra, enrichment provenance, density-aware loss components, runtime. |
| Not concluded | No P72/P73 repair, no d18 validation, no HMC readiness, no scaling, no rank/degree promotion, no adaptive Zhao--Cui parity. |
| Artifacts | Master program, runbook, execution ledger, review ledger, phase subplans/results, implementation diffs if launched, diagnostic JSONs, stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| P72 blocked diagnostic is the comparator | P72 Phase 5 result and Claude review | It is the actual current failure, not a hypothetical baseline. | Comparing against stale schema/smoke result. | Phase 0 JSON/result checks. | reviewed |
| NeuTra analogy is context only | P73 proposal R1/R2/R3 review | Avoids importing unproved flow-training claims into TT/SIRT. | Treating renewal as proof. | Phase 1 boundary audit. | reviewed |
| Renewal cannot certify on newly added points | P73 proposal | Prevents guard/audit overfit. | Apparent pass from training-enriched support. | Phase 2 audit-split contract. | planned |
| Implementation is opt-in | BayesFilter backend and evidence policy | Avoids default-policy changes before evidence. | Accidental default change. | Phase 3/4 surface audit. | planned |

## Anticipated Approvals And Boundaries

The reviewed runbook approval covers visible execution of ordinary reviewed
phase transitions.  After a phase gate passes, Codex continues to the next
reviewed subplan without asking for another routine launch approval.  Codex
asks the user only when a human-required boundary below is reached.  A blocked
diagnostic is not itself a human-required boundary if the next reviewed phase
is a bounded result-decision or root-cause handoff phase.

Covered by the reviewed visible runbook:

- Claude Code read-only reviews through
  `/home/chakwong/python/claudecodex/scripts/claude_worker.sh` with Opus max
  effort, run in the foreground and used only for review;
- local documentation writes under `docs/plans`;
- visible source-code edits on implementation surfaces explicitly authorized
  by reviewed Phase 3 and Phase 4 subplans only;
- CPU-only Python/pytest diagnostics with `CUDA_VISIBLE_DEVICES=-1`;

Not approved by this runbook:

- destructive git or filesystem actions;
- package installation or dependency downloads;
- network fetches, credentials, or outside-repo writes;
- detached/background execution;
- threshold changes after outputs;
- downstream validation, HMC, scaling, or rank promotion during P73.
- escalated GPU, network, package-install, or outside-repo commands unless a
  later reviewed phase explicitly needs them and the user approves the
  boundary.

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and,
for material phases, in the execution ledger.

Check:

- wrong baselines;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If the audit finds a material flaw, revise the plan or write a blocker note
before running the phase.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites.
   - Restate the phase evidence contract in chat.
   - Append a ledger entry.
2. `EXECUTE_MINIMAL`
   - Run only visible commands in the current conversation.
   - Prefer the smallest diagnostic or implementation needed to answer the
     phase question.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against the primary criterion and veto diagnostics.
   - Write or update the required phase result artifact.
4. `DRAFT_NEXT`
   - Draft or refresh the next phase subplan.
   - Ensure the current result explicitly produces next-phase entry
     conditions.
5. `PASS_REVIEW`
   - Send material phase results, repairs, implementation diffs, or final
     decisions to Claude through the foreground read-only review wrapper.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
6. `REPAIR_LOOP`
   - For fixable blockers, patch the same artifact visibly.
   - Rerun focused checks.
   - Rereview material fixes.
   - Stop after five Claude review rounds for the same blocker.
7. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Continue automatically to the next reviewed subplan after the gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- continuing after Claude and Codex do not converge after five review rounds.

## Final Visible Handoff

When execution completes or stops, write:

- final phase reached;
- final status;
- result artifacts;
- Claude review trail;
- tests/benchmarks actually run;
- unresolved blockers;
- what was not concluded;
- safest next human decision, if any.
