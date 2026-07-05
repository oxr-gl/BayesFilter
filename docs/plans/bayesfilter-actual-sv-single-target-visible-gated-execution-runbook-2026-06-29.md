# Actual-SV Single-Target Visible Gated Execution Runbook

Date: 2026-06-29

## Status

`ACTIVE_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- detached supervisors or copied-workspace execution;
- `setsid`, `nohup`, backgrounded phase runners, or hidden tmux loops.

If detached execution becomes necessary, stop and write a separate detached
execution plan for human approval. This runbook is for visible, recoverable
execution inside the current conversation.

## Program

Master program:

- `docs/plans/bayesfilter-actual-sv-single-target-master-program-2026-06-29.md`

Single-target contract:

- `docs/plans/bayesfilter-actual-sv-single-target-contract-2026-06-29.md`

Execution ledger:

- `docs/plans/bayesfilter-actual-sv-single-target-visible-execution-ledger-2026-06-29.md`

Claude review ledger:

- `docs/plans/bayesfilter-actual-sv-single-target-claude-review-ledger-2026-06-29.md`

Stop handoff:

- `docs/plans/bayesfilter-actual-sv-single-target-visible-stop-handoff-2026-06-29.md`

## Reviewed Revision Rule

Every review entry must record the artifact path and the reviewed revision marker.
For this visible document-only program, the minimum revision marker is the review
round timestamp plus a one-line summary of the last patch applied before review.
No artifact may be executed against or advanced from a reviewed path after that
path has changed without a fresh review entry.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| ---: | --- | --- | --- |
| 0 | Program launch and inherited-boundary freeze | `docs/plans/bayesfilter-actual-sv-single-target-phase0-program-launch-subplan-2026-06-29.md` | `docs/plans/bayesfilter-actual-sv-single-target-phase0-program-launch-result-2026-06-29.md` |
| 1 | Single-target scalar contract freeze | `docs/plans/bayesfilter-actual-sv-single-target-phase1-single-target-contract-subplan-2026-06-29.md` | `docs/plans/bayesfilter-actual-sv-single-target-phase1-single-target-contract-result-2026-06-29.md` |
| 2 | Derivation and chapter reconciliation | `docs/plans/bayesfilter-actual-sv-single-target-phase2-derivation-chapter-reconciliation-subplan-2026-06-29.md` | `docs/plans/bayesfilter-actual-sv-single-target-phase2-derivation-chapter-reconciliation-result-2026-06-29.md` |
| 3 | Code/test/benchmark boundary audit | `docs/plans/bayesfilter-actual-sv-single-target-phase3-code-test-benchmark-boundary-audit-subplan-2026-06-29.md` | `docs/plans/bayesfilter-actual-sv-single-target-phase3-code-test-benchmark-boundary-audit-result-2026-06-29.md` |
| 4 | Corrected Lane-B route decision | `docs/plans/bayesfilter-actual-sv-single-target-phase4-route-decision-subplan-2026-06-29.md` | `docs/plans/bayesfilter-actual-sv-single-target-phase4-route-decision-result-2026-06-29.md` |
| 5 | Same-target value validation | `docs/plans/bayesfilter-actual-sv-single-target-phase5-same-target-value-validation-subplan-2026-06-29.md` | `docs/plans/bayesfilter-actual-sv-single-target-phase5-same-target-value-validation-result-2026-06-29.md` |
| 6 | Same-target gradient validation | `docs/plans/bayesfilter-actual-sv-single-target-phase6-same-target-gradient-validation-subplan-2026-06-29.md` | `docs/plans/bayesfilter-actual-sv-single-target-phase6-same-target-gradient-validation-result-2026-06-29.md` |
| 7 | Final decision and documentation handoff | `docs/plans/bayesfilter-actual-sv-single-target-phase7-final-decision-handoff-subplan-2026-06-29.md` | `docs/plans/bayesfilter-actual-sv-single-target-phase7-final-decision-handoff-result-2026-06-29.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the actual-SV single-target correction be advanced through visible, gated, anti-drift phases without reintroducing the wrong scalar? |
| Baseline/comparator | Reviewed reset memos, single-target contract, derivation/chapter artifacts, current code/test/benchmark surfaces. |
| Primary pass criterion | Each phase passes its own reviewed subplan gate, writes its result artifact, refreshes the next subplan, and preserves the single-target contract. |
| Veto diagnostics | Wrong-scalar promotion, KSC/diagnostic evidence blending, phase advance without contract freeze, tests-passed-but-wrong-question, missing artifact, missing review convergence, runtime boundary violation. |
| Explanatory diagnostics | Dense gaps, gradient gaps, branch logs, benchmark timing, implementation complexity, review disagreement notes. |
| Not concluded | No corrected Lane-B implementation at launch, no same-target Lane-B admission, no HMC/default/production claim. |
| Artifacts | Master program, contract, subplans, results, runbook, ledgers, stop handoff, Claude reviews. |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and in
the execution ledger.

Check:

- wrong baseline;
- proxy metric being treated as promotion evidence;
- missing stop condition;
- unfair comparison;
- hidden surrogate substitution;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If the audit finds a material flaw, revise the plan or write a blocker note
before running the phase.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites and inherited artifacts exist.
   - Restate the phase evidence contract in chat.
   - Append a ledger entry.
2. `REVIEW_SUBPLAN`
   - Obtain bounded Claude review of the phase subplan before any execution.
3. `EXECUTE_MINIMAL`
   - Run only visible commands in the current conversation.
   - Prefer the smallest diagnostic or implementation step needed to answer the
     phase question.
   - If the current phase is Phase 0, 1, 2, 3, or 4, execution must remain
     document-only unless a reviewed subplan for that phase explicitly authorizes
     a read-only code/test inventory command.
   - If the current phase is Phase 5, 6, or 7, implementation, code mutation,
     test mutation, or benchmark mutation remains forbidden unless a reviewed
     subplan for that phase explicitly authorizes the exact mutation scope after
     Phase 4 has passed.
4. `ASSESS_GATE`
   - Compare outputs against the phase primary criterion and veto diagnostics.
   - Write or update the required phase result artifact.
5. `PASS_REVIEW`
   - Send phase results, repairs, or final decisions to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
6. `REPAIR_LOOP`
   - For fixable blockers, write a blocker plan/result, get review when material,
     apply the repair visibly, rerun focused checks, and stop after five review
     rounds for the same blocker.
7. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes, the next subplan exists,
     and the ledger records the review disposition.
   - Stop and write the handoff if a human-required or contract-required blocker
     appears.

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
- Hidden surrogate substitution:
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
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Reviewed
revision marker: <timestamp + last patch summary>. Do not edit, run commands,
launch agents, or review the whole repo. Question: <one question>. End with
VERDICT: AGREE or VERDICT: REVISE.
```

Codex must preserve the review artifact, record the reviewed revision marker,
and inspect whether Claude remained read-only.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already encoded in the reviewed program;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing a default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- continuing after Claude and Codex do not converge after five review rounds;
- continuing after discovering a new governing-scalar contradiction without first
  writing a reset memo or reviewed blocker artifact.

## Final Visible Handoff

When execution completes or stops, write:

- final phase reached;
- route statuses;
- result artifacts;
- Claude review trail;
- local tests/benchmarks actually run;
- unresolved math/implementation/benchmark/policy gaps;
- what was not concluded;
- exact next reviewed action required.
