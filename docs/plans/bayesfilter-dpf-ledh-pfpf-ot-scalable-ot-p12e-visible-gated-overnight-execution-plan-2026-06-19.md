# P12E Visible Gated Overnight Execution Plan

Date: 2026-06-19

## Status

`REVIEWED_VISIBLE_GATED_EXECUTION_PLAN_NOT_LAUNCHED_PENDING_USER_APPROVALS`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

These are execution/review roles, not additional active Wave 1 agents.  The
only active Wave 1 agents remain `peer agent` and `current agent`.

This runbook must not launch a detached or nested agent.  Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

This plan is visible, gated, and recoverable inside the current conversation.
It must not execute until the user explicitly approves launch and anticipated
command classes.

## Quiet Visible Execution Pattern

Full command output is an artifact, not chat content.  The session receives
bounded summaries only.

Required pattern:

1. Predeclare log paths and structured artifact paths in the phase subplan or
   ledger before commands run.
2. Redirect full stdout/stderr for noisy TensorFlow/diagnostic/Claude commands
   to logs.
3. Prefer commands that write JSON/Markdown/result artifacts directly.
4. After commands, print only a bounded summary: exit status, artifact paths,
   pass/fail fields, and at most the last 20-40 log lines on failure.
5. If live monitoring is needed, poll bounded status commands.
6. Treat excessive stdout/stderr as an execution-flow defect and repair with
   quieter redirection.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-ledh-sparse-locality-screen-master-program-2026-06-19.md`

Review artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-master-program-review-packet-2026-06-19.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-master-program-claude-review-ledger-2026-06-19.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-visible-execution-ledger-2026-06-19.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-visible-stop-handoff-2026-06-19.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P12E-0 | Intake, Governance, And First Checks | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p0-first-checks-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p0-first-checks-result-2026-06-19.md` |
| P12E-1 | Diagnostic Implementation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p1-diagnostic-implementation-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p1-diagnostic-implementation-result-2026-06-19.md` |
| P12E-2 | Smoke Diagnostic And Artifact Validation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p2-smoke-diagnostic-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p2-smoke-diagnostic-result-2026-06-19.md` |
| P12E-3 | Official Diagnostic | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p3-official-diagnostic-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p3-official-diagnostic-result-2026-06-19.md` |
| P12E-4 | Result Closeout And Coordinator Handoff | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p4-closeout-handoff-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p4-closeout-handoff-result-2026-06-19.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a deterministic, CPU-scoped TensorFlow LEDH-like locality diagnostic produce valid evidence on whether sparse/localized OT work should be reopened for LEDH post-flow particles? |
| Baseline/comparator | Dense TensorFlow transport on the same deterministic LEDH-like post-flow particles, preserving Phase 1/Phase 8 orientation and truncation conventions. |
| Primary pass criterion | P12E writes valid JSON/Markdown/result artifacts recording deterministic fixture provenance, finite dense plans, support curves, nearest-neighbor mass, 99% truncation residuals, transported-particle errors, decisions, and non-claims. |
| Veto diagnostics | Missing deterministic provenance, non-finite LEDH/dense/truncated artifacts, orientation mismatch, threshold/reporting mismatch, package/network/GPU/external-solver need, shared-file edit need, or unsupported claim. |
| Explanatory diagnostics | Runtime, memory, 90/95/99.9% support curves, nearest-neighbor mass, LEDH log-det ranges, and descriptive Phase 8 context. |
| Not concluded | No sparse solver validity, speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, or broad sparse-OT validation/rejection. |
| Artifacts | Phase result notes, official JSON/Markdown diagnostic artifacts, review ledger, execution ledger, and stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| CPU-only TensorFlow | Wave 1 coordinator and P12E subplans | Avoids unstable GPU evidence and satisfies governance. | Script imports TensorFlow before hiding GPU. | P12E-1 review plus import check. | reviewed requirement |
| Deterministic synthetic LEDH-like fixtures | Coordinator input-data rule | No actual LEDH artifact is frozen. | Fixture discretion after seeing results. | Code/JSON must record seeds, grids, maps, digests. | reviewed requirement |
| Phase 8 locality thresholds | Phase 8 reviewed result/subplan | Keeps sparse reopen criterion comparable to prior blocker. | Threshold drift after seeing results. | Static review and artifact validation. | reviewed requirement |
| Dense TensorFlow comparator | Phase 1/Phase 8 convention | Sparse locality is screened from dense transport support. | Orientation/scaling mismatch. | P12E-1/P12E-2 artifact checks. | reviewed requirement |

## Skeptical Plan Audit

Before each phase, Codex must record a skeptical audit in chat and, for
material phases, in the execution ledger.

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
   - Restate the phase evidence contract.
   - Append a ledger entry.
2. `EXECUTE_MINIMAL`
   - Run only visible commands in the current conversation.
   - Prefer the smallest diagnostic or implementation needed to answer the
     phase question.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against primary criterion and veto diagnostics.
   - Write/update required phase result artifact.
4. `PASS_REVIEW`
   - Send material phase plans, implementation diffs, result packets, or final
     decisions to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, patch lane-owned files visibly.
   - Rerun focused checks.
   - Get Claude review when material.
   - Write repair evidence in the phase result.
   - Stop after five Claude review rounds for the same material blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Claude Read-Only Review Template

Use Claude only as a reviewer.  Do not paste whole files.  Use the review
packet and targeted excerpts/diffs.

Prompt form:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review the P12E packet and targeted snippets/diff paths:
- <paths>

Check wrong baseline, proxy metrics as pass criteria, missing stop conditions,
unfair comparison, hidden assumptions, stale context, environment mismatch,
unsupported claim, artifact mismatch, two-agent boundary, and forbidden actions.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

If Claude does not respond, run the tiny probe:

```text
READ-ONLY PROBE ONLY. Reply with exactly: PROBE_OK
```

If the probe responds, redesign the original prompt.  If the probe fails, write
an external-review blocker and ask the user for direction.

## Anticipated Approvals Required Before Launch

Ask the user to approve these before visible execution starts:

- Claude Code read-only review via
  `bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh --model opus --effort max`
  using narrow wrapper-script approval.
- Local Python checks:
  `python -m py_compile ...`
- CPU-scoped TensorFlow import checks:
  `CUDA_VISIBLE_DEVICES=-1 python -c ...`
- Lane-owned diagnostic smoke and official runs:
  `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_p12e_ledh_sparse_locality_screen.py ...`
- Writing lane-owned artifacts listed in the master program.

No approval is requested for package installation, network fetch, GPU evidence,
external solver execution, destructive filesystem/git action, default-policy
change, shared ledger/stop-handoff edit, or peer-agent file edit; those remain
stop conditions.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- editing coordinator-owned or peer-owned artifacts;
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

## Launch Status

`NOT_LAUNCHED_PENDING_USER_APPROVALS`
