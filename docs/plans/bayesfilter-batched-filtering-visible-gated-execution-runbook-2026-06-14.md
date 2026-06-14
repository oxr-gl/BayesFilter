# Batched Filtering Visible Gated Execution Runbook

Date: 2026-06-14

## Status

`ACTIVE_VISIBLE_EXECUTION_RUNBOOK`

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
detached-supervisor plan for human approval.  This runbook is for visible,
recoverable execution inside the current conversation.

## Program

Master program:

- `docs/plans/bayesfilter-batched-filtering-production-default-master-program-2026-06-14.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-batched-filtering-claude-review-round-01-2026-06-14.md`
- Additional round files with incrementing round numbers when needed.

Execution ledger:

- `docs/plans/bayesfilter-batched-filtering-visible-execution-ledger-2026-06-14.md`

Stop handoff:

- `docs/plans/bayesfilter-batched-filtering-visible-stop-handoff-2026-06-14.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| ---: | --- | --- | --- |
| 0 | Inventory And Boundary Audit | `docs/plans/bayesfilter-batched-filtering-phase-0-inventory-boundary-subplan-2026-06-14.md` | `docs/plans/bayesfilter-batched-filtering-phase-0-inventory-boundary-result-2026-06-14.md` |
| 1 | Test Stabilization | `docs/plans/bayesfilter-batched-filtering-phase-1-test-stabilization-subplan-2026-06-14.md` | `docs/plans/bayesfilter-batched-filtering-phase-1-test-stabilization-result-2026-06-14.md` |
| 2 | Nonlinear Branch Coverage | `docs/plans/bayesfilter-batched-filtering-phase-2-nonlinear-branch-coverage-subplan-2026-06-14.md` | `docs/plans/bayesfilter-batched-filtering-phase-2-nonlinear-branch-coverage-result-2026-06-14.md` |
| 3 | Production Interface Candidate | `docs/plans/bayesfilter-batched-filtering-phase-3-interface-candidate-subplan-2026-06-14.md` | `docs/plans/bayesfilter-batched-filtering-phase-3-interface-candidate-result-2026-06-14.md` |
| 4 | Compiled Benchmark Ladder | `docs/plans/bayesfilter-batched-filtering-phase-4-compiled-benchmark-ladder-subplan-2026-06-14.md` | `docs/plans/bayesfilter-batched-filtering-phase-4-compiled-benchmark-ladder-result-2026-06-14.md` |
| 5 | Downstream HMC/NeuTra Harness | `docs/plans/bayesfilter-batched-filtering-phase-5-downstream-harness-subplan-2026-06-14.md` | `docs/plans/bayesfilter-batched-filtering-phase-5-downstream-harness-result-2026-06-14.md` |
| 6 | Default-Readiness Decision | `docs/plans/bayesfilter-batched-filtering-phase-6-default-readiness-subplan-2026-06-14.md` | `docs/plans/bayesfilter-batched-filtering-phase-6-default-readiness-result-2026-06-14.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the experimental batched filtering value+score work be advanced through visible gated evidence toward a conditional production-default candidate? |
| Baseline/comparator | Existing scalar production APIs, current experimental artifacts, and scalar-loop benchmarks where performance is tested. |
| Primary pass criterion | Each phase passes its subplan checks, writes a result artifact, refreshes the next subplan, and receives read-only review when material. |
| Veto diagnostics | Missing artifact; scalar parity failure; nonfinite outputs; JIT failure for supported benchmark targets; wrong trusted-device placement; unsupported default claim; Claude/Codex nonconvergence after five rounds. |
| Explanatory diagnostics | Compile time, warm-call time, memory/capacity, branch summaries, smoke throughput, and implementation complexity. |
| Not concluded | No unconditional default, no CUT4 readiness, no broad posterior quality claim, no downstream sampler convergence claim without a separate sampler-validity plan. |
| Artifacts | Master program, subplans, results, Claude reviews, benchmark JSON/MD outputs, ledger, stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Visible execution in current conversation | User requested Codex supervisor/executor | Preserves recoverability and prevents hidden detached state | Long GPU phase may exceed practical interactive time | Stop before Phase 4 if trusted approvals or runtime are unavailable | reviewed |
| Claude as reviewer only | User instruction | Keeps execution authority with Codex and human | Reviewer may attempt edits or broad claims | Preserve review transcript and check git status after review | reviewed |
| Phase-by-phase subplans | User instruction | Prevents stale plan drift | Subplan may not match previous result | End every phase by refreshing/reviewing next subplan | reviewed |
| Repair loop before stop | User instruction | Avoids stopping for fixable issues | Could chase non-material issues | Five-round cap per same blocker and materiality screen | reviewed |

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
   - Confirm the declared interpreter, TensorFlow environment, and required
     local artifact paths exist; class missing or mismatched environment as a
     blocker unless the subplan gives a safe fallback.
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

Use Claude only as a reviewer.  The prompt must say:

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

Codex must preserve the review artifact and inspect whether Claude actually
remained read-only.

## Claude Nonresponse Protocol

If a material Claude review does not return a usable answer:

1. Run a small read-only probe asking Claude to answer a one-line readiness
   question.
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
- changing a production default;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- continuing after Claude and Codex do not converge after five review rounds.

Also stop and write a blocker if the active Python/TensorFlow environment is
missing, inconsistent with the subplan, or unable to import the required
experimental modules, unless the phase subplan explicitly provides a reviewed
local fallback.

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
