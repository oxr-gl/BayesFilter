# Visible Gated Overnight Execution Plan: P12 Low-Rank Solver Route

Date: 2026-06-19

## Status

`VISIBLE_EXECUTION_LAUNCHED`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus is a read-only reviewer only.

This plan is based on
`/home/ubuntu/python/claudecodex/docs/templates/visible-gated-execution-runbook-template.md`.
It is a visible, foreground, recoverable overnight plan.  It must not launch a
detached or nested agent.  Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-master-program-2026-06-19.md`

Claude review ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-claude-review-ledger-2026-06-19.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-visible-execution-ledger-2026-06-19.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-visible-stop-handoff-2026-06-19.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P12-0 | Governance, Source Anchors, And Review Gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p00-governance-source-lock-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p00-governance-source-lock-result-2026-06-19.md` |
| P12-1 | Intake And Artifact Baseline | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p01-intake-artifact-baseline-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p01-intake-artifact-baseline-result-2026-06-19.md` |
| P12-2 | Implementation And Diagnostic Replay | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p02-implementation-diagnostic-replay-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p02-implementation-diagnostic-replay-result-2026-06-19.md` |
| P12-3 | Result Closeout And Status Sync | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p03-result-closeout-status-sync-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p03-result-closeout-status-sync-result-2026-06-19.md` |
| P12-4 | Read-Only Independent Review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p04-readonly-independent-review-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p04-readonly-independent-review-result-2026-06-19.md` |
| P12-5 | Coordinator Handoff Readiness | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p05-coordinator-handoff-readiness-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p05-coordinator-handoff-readiness-result-2026-06-19.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the P12 peer-agent lane be governed, replayed, reviewed, and handed off without crossing Wave 1 boundaries or overstating diagnostic evidence? |
| Baseline/comparator | Wave 1 coordinator plus Phase 1 dense/streaming baseline as descriptive comparator only. |
| Primary pass criterion | All P12 phases write required results, local checks pass or blockers are recorded, Claude read-only review converges for material subplans/results, and final handoff waits for coordinator merge. |
| Veto diagnostics | Shared contract drift, forbidden file edit, external solver/package/network/GPU use, unsupported claim, missing result artifact, Claude non-read-only behavior, or five failed review rounds on same blocker. |
| Explanatory diagnostics | Dense-reference deltas, runtime/memory proxies, review round counts, nonblocking wording findings. |
| Not concluded | No speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or coordinator merge. |
| Artifacts | Master program, phase subplans/results, Claude review ledger, visible execution ledger, stop handoff, P12 implementation/test/diagnostic/result/status artifacts. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| CPU-only replay | Wave 1 coordinator | P12 does not need GPU evidence. | TensorFlow emits CUDA/no-device logs. | Record `CUDA_VISIBLE_DEVICES=-1`; treat logs as environment noise. | Locked |
| TensorFlow implementation backend | BayesFilter governance | BayesFilter-owned algorithmic code defaults to TensorFlow/TFP. | NumPy/POT route silently becomes implementation backend. | Code import/source scan. | Locked |
| Diagnostic-only interpretation | P12 subplan/result | P12 route includes extension components. | Result wording implies solver fidelity or dense equivalence. | Claim scan and Claude review. | Locked |
| Claude read-only reviewer | User instruction and 2026-06-19 user approval | Keeps Codex accountable and bounded. | Claude edits or authorizes boundary crossing. | Wrapper prompt says read-only; Codex inspects output. | Approved and active |

## Quiet Visible Execution Pattern

Commands that may produce large TensorFlow or Claude output must write logs
under a P12-owned log path before launch, for example:

```bash
mkdir -p docs/benchmarks/logs
timeout 300 <command> > docs/benchmarks/logs/p12-low-rank-solver-route-<phase>.log 2>&1
```

The chat should show only exit status, artifact paths, pass/fail fields, and
bounded failure tails.

## Skeptical Plan Audit

Before each phase, Codex must record a skeptical audit covering:

- wrong baseline;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If the audit finds a material flaw, revise the plan or write a blocker before
running the phase.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run only visible commands in this conversation.
3. `ASSESS_GATE`: compare outputs to criteria and write/update phase result.
4. `PASS_REVIEW`: send material results or repairs to Claude as read-only
   review after approval.
5. `REPAIR_LOOP`: patch fixable P12-owned issues, rerun focused checks, and
   stop after five Claude rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after gate passes; otherwise write handoff.

## Repair Loop And No-Invalid-Stop Rule

The repair loop is mandatory for fixable P12-owned issues:

1. identify the smallest focused repair;
2. patch visibly inside the P12-owned write set;
3. rerun focused checks;
4. refresh the phase result;
5. resend material repairs to Claude read-only review after approval;
6. stop after five review rounds for the same blocker.

Do not stop merely because a phase is tedious, output is noisy, Claude reports
nonblocking wording findings, or the diagnostic remains diagnostic-only.  Stop
only for a declared stop condition, missing human approval, forbidden boundary
crossing, or nonconvergence after the five-round blocker limit.

## Claude Read-Only Review Command Shape

Requires explicit user approval before use:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh --cwd /home/ubuntu/python/BayesFilter --name p12-low-rank-solver-review-r1 --model opus --effort max "READ-ONLY REVIEW ONLY. Do not edit files, run experiments, launch agents, or change state. Review the P12 low-rank solver route governance artifacts by path. Findings first. End with exactly VERDICT: AGREE or VERDICT: REVISE."
```

If Claude does not respond, also only after user approval:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh --cwd /home/ubuntu/python/BayesFilter --name p12-low-rank-solver-probe --model opus --effort max "READ-ONLY PROBE ONLY. Reply with VERDICT: AGREE if you can read this prompt."
```

Do not paste whole files to Claude.  Provide paths and bounded review
questions.

## Human-Required Stop Conditions

Stop if continuing would require:

- Claude Code usage without approval;
- package installation, network fetch, credentials, or environment setup;
- destructive git/filesystem action;
- changing pass/fail criteria after seeing results;
- modifying unrelated dirty worktree changes;
- shared contract or current-agent file edits;
- changing default policy;
- interpreting GPU/special hardware results;
- continuing after five nonconvergent Claude rounds.

## Launch Approval State

User approval was granted on 2026-06-19 for:

1. running Claude Code read-only review/probe commands;
2. running the visible phase execution sequence;
3. applying focused P12-owned repairs discovered during review.

This plan is now launched visibly in the current conversation.  Additional
human approval remains required for any action outside the approved scope,
including package installation, network fetch, GPU evidence, external solver
execution, destructive git/filesystem action, shared contract edits,
current-agent file edits, public export changes, or scientific-claim boundary
changes.

## Final Visible Handoff

When complete or stopped, write:

- final phase reached;
- final status;
- result artifacts;
- Claude review trail;
- tests/checks actually run;
- unresolved blockers;
- what was not concluded;
- safest next human decision.
