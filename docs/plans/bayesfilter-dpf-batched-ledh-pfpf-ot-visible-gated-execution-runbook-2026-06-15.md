# Batched LEDH-PFPF-OT Visible Gated Execution Runbook

Date: 2026-06-15

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

If detached overnight execution becomes necessary, stop and write a separate
detached-supervisor plan for human approval. This runbook is for visible,
recoverable execution inside the current conversation.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-master-program-2026-06-15.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-claude-review-round-01-2026-06-15.md`
- Additional round files with incrementing round numbers when needed.

Execution ledger:

- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-visible-execution-ledger-2026-06-15.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-visible-stop-handoff-2026-06-15.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| ---: | --- | --- | --- |
| 0 | Inventory And Contract Lock | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p0-inventory-contract-subplan-2026-06-15.md` | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p0-inventory-contract-result-2026-06-15.md` |
| 1 | Batched Callback And Shape Contract | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p1-shape-contract-subplan-2026-06-15.md` | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p1-shape-contract-result-2026-06-15.md` |
| 2 | Batched LEDH Flow And Transport Core | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p2-flow-transport-core-subplan-2026-06-15.md` | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p2-flow-transport-core-result-2026-06-15.md` |
| 3 | Batched Value Recursion And Parity | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p3-value-parity-subplan-2026-06-15.md` | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p3-value-parity-result-2026-06-15.md` |
| 4 | Batched Value+Score | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p4-value-score-subplan-2026-06-15.md` | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p4-value-score-result-2026-06-15.md` |
| 5 | Compiled Benchmark Ladder | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p5-compiled-benchmark-subplan-2026-06-15.md` | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p5-compiled-benchmark-result-2026-06-15.md` |
| 6 | Closeout And Promotion Boundary | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p6-closeout-subplan-2026-06-15.md` | `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p6-closeout-result-2026-06-15.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a new experimental LEDH-PFPF-OT tensor core batch independent parameter proposals and later expose value+score for the relaxed objective? |
| Baseline/comparator | Existing scalar `run_ledh_pfpf_ot_tf`, scalar LEDH flow, existing annealed transport, and scalar-stack parity. |
| Primary pass criterion | Each phase passes its subplan checks, writes a result artifact, refreshes the next subplan, and receives read-only review when material. |
| Veto diagnostics | Wrong baseline; missing deterministic parity contract; row cross-talk; scalar parity failure; nonfinite score; unsupported categorical PF gradient claim; uncompiled GPU comparison; Claude nonconvergence after five rounds. |
| Explanatory diagnostics | Runtime, compile time, ESS, transport residuals, log-det/Jacobian ranges, memory estimates. |
| Not concluded | No production default, no categorical PF gradient, no posterior correctness, no HMC/NeuTra readiness, no broad GPU speedup. |
| Artifacts | Master program, subplans, results, Claude reviews, benchmark JSON/MD outputs when applicable, ledger, stop handoff. |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and, for
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
4. `PASS_REVIEW`
   - Send material phase results, repairs, implementation diffs, or final
     decisions to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, write a blocker plan.
   - Get Claude review when material.
   - Apply the repair visibly.
   - Rerun focused checks.
   - Write a blocker result.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Ledger Entry Template

```markdown
### <timestamp> - Phase <N> - <STATE>

Evidence contract:

- Question:
- Baseline/comparator:
- Primary criterion:
- Veto diagnostics:
- Non-claims:

Skeptical audit:

- Wrong baseline:
- Proxy metric risk:
- Missing stop condition:
- Unfair comparison:
- Hidden assumption:
- Stale context:
- Environment mismatch:
- Artifact adequacy:

Actions:

- <commands/edits/reviews>

Artifacts:

- <paths>

Gate status:

- <PASSED/BLOCKED/FAILED/IN_PROGRESS>

Next action:

- <next visible step>
```

## Claude Read-Only Review Template

Use Claude only as a reviewer. The prompt must say:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review these paths only:
- <path>

Check:
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

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

Codex must preserve the review artifact and inspect whether Claude remained
read-only.

## Claude Nonresponse Protocol

If a material Claude review does not return a usable answer:

1. Run a small read-only probe asking Claude to answer exactly `PROBE_OK`.
2. If the probe responds, treat the failed review as a prompt-design problem.
   Shorten and narrow the prompt, then retry the same review round.
3. If the probe does not respond in trusted context, write a blocker result and
   stop for human direction.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing a production default or public API;
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
