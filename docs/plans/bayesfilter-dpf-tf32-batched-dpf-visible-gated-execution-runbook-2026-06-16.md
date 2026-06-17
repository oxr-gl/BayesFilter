# BayesFilter DPF TF32 Batched DPF Visible Gated Execution Runbook - 2026-06-16

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

## Quiet Visible Execution Pattern

Use this pattern for commands that may produce large stdout/stderr, including
TensorFlow, CUDA, benchmark, sampler, long test, or Claude review commands.

Principle: full output is an artifact, not chat content. The session window
gets bounded summaries only.

Required pattern:

1. Predeclare the log path and structured artifact path in the phase subplan or
   ledger before running the command.
2. Redirect full stdout/stderr to a log file. Do not mirror full output with
   `tee` unless the expected output is small.
3. Prefer commands that write JSON/Markdown/result artifacts directly.
4. After the command, print only a bounded summary to the session: exit status,
   artifact paths, pass/fail fields, and at most the last 20-40 log lines on
   failure.
5. If live monitoring is necessary, poll a bounded status command rather than
   streaming the full process output.
6. Treat excessive stdout/stderr as an execution-flow defect. If it destabilizes
   the session, write a stop handoff and resume with quieter redirection.

Recommended shell shape:

```bash
mkdir -p docs/benchmarks/logs
timeout <seconds> <command> > docs/benchmarks/logs/<run-name>.log 2>&1
```

Then inspect only bounded metadata, for example:

```bash
python <small-summary-script> <json-artifact>
tail -40 docs/benchmarks/logs/<run-name>.log
```

Do not use this as a way to hide failures. Logs and structured artifacts must
be preserved and referenced from the phase result.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-master-program-2026-06-16.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p0-claude-review-round-01-2026-06-16.md`
- Additional round files with incrementing round numbers when needed.

Execution ledger:

- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-visible-execution-ledger-2026-06-16.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-visible-stop-handoff-2026-06-16.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| ---: | --- | --- | --- |
| 0 | Governance And Runbook Lock | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p0-governance-runbook-lock-subplan-2026-06-16.md` | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p0-governance-runbook-lock-result-2026-06-16.md` |
| 1 | Implementation And Precision Inventory | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p1-implementation-precision-inventory-subplan-2026-06-16.md` | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p1-implementation-precision-inventory-result-2026-06-16.md` |
| 2 | Single-GPU Batched Value Runner | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p2-single-gpu-batched-value-subplan-2026-06-16.md` | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p2-single-gpu-batched-value-result-2026-06-16.md` |
| 3 | Two-GPU Row Splitting | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p3-two-gpu-row-splitting-subplan-2026-06-16.md` | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p3-two-gpu-row-splitting-result-2026-06-16.md` |
| 4 | JIT-Safe Score Path | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p4-jit-safe-score-path-subplan-2026-06-16.md` | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p4-jit-safe-score-path-result-2026-06-16.md` |
| 5 | HMC-Facing Diagnostics | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p5-hmc-facing-diagnostics-subplan-2026-06-16.md` | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p5-hmc-facing-diagnostics-result-2026-06-16.md` |
| 6 | Closeout And Guardrails | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p6-closeout-guardrails-subplan-2026-06-16.md` | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p6-closeout-guardrails-result-2026-06-16.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the TF32 batched DPF work proceed as visible foreground execution with clear gates, artifacts, and review boundaries? |
| Baseline/comparator | The 2026-06-16 reset memo, 2026-06-15 DPF reset memo, visible runbook template, and prior TF32 precision/capacity result notes. |
| Primary pass criterion | Each executed phase passes its subplan checks, writes a result artifact, refreshes the next subplan, and passes material read-only review. |
| Veto diagnostics | Detached execution; Claude acting as executor; missing stop condition; missing phase artifact; stale or wrong baseline; unsupported HMC/default-readiness claim; untrusted GPU interpretation; single-filter multi-GPU sharding claim. |
| Explanatory diagnostics | Runtime, compile time, memory, GPU placement, precision drift, and implementation complexity. |
| Not concluded | No production readiness, no public API readiness, no HMC posterior validity, no scientific correctness, no global dtype policy, and no particle-cloud sharding. |
| Artifacts | Master program, runbook, execution ledger, stop handoff, phase subplans/results, Claude review artifacts, and later benchmark artifacts. |

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
   - Use the quiet visible execution pattern for TensorFlow/CUDA/benchmark,
     sampler, long-test, and Claude-review commands.
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
### timestamp - Phase N - STATE

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

- commands, edits, reviews

Artifacts:

- paths

Gate status:

- PASSED, BLOCKED, FAILED, or IN_PROGRESS

Next action:

- next visible step
```

## Claude Read-Only Review Template

Use Claude only as a reviewer. The prompt must say:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review these named paths only.

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

Codex must preserve the review artifact and inspect whether Claude actually
remained read-only.

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
- tests and benchmarks actually run;
- unresolved blockers;
- what was not concluded;
- safest next human decision, if any.
