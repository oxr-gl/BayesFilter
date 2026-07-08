# LEDH-PFPF-OT Manual Adjoint Visible Gated Execution Runbook

Date: 2026-06-22

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK_READY_FOR_M1`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus is a read-only reviewer only.

This runbook must not launch a detached or nested agent.  Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

Visible execution stays in the current conversation.  If detached overnight
execution is desired later, write a separate detached-supervisor plan and stop.

## Program

Master program:

- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-master-program-2026-06-22.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-claude-review-ledger-2026-06-22.md`

Execution ledger:

- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-visible-execution-ledger-2026-06-22.md`

Stop handoff:

- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-visible-stop-handoff-2026-06-22.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
|---|---|---|---|
| M0 | Re-entry and boundary lock | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase0-reentry-subplan-2026-06-22.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase0-reentry-result-2026-06-22.md` |
| M1 | Derivation and chapter contract | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase1-derivation-subplan-2026-06-22.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase1-derivation-result-2026-06-22.md` |
| M2 | Primitive dense VJP parity | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase2-primitive-vjp-subplan-2026-06-22.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase2-primitive-vjp-result-2026-06-22.md` |
| M3 | Dense custom-gradient prototype | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase3-dense-custom-gradient-subplan-2026-06-22.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase3-dense-custom-gradient-result-2026-06-22.md` |
| M4 | Loop-adjoint integration design | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase4-loop-adjoint-integration-design-subplan-2026-06-22.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase4-loop-adjoint-integration-design-result-2026-06-22.md` |
| M5 | Opt-in integration and small SIR smoke | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase5-small-sir-smoke-subplan-2026-06-22.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase5-small-sir-smoke-result-2026-06-22.md` |
| M6 | Streaming/chunked memory route | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase6-streaming-memory-route-subplan-2026-06-22.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase6-streaming-memory-route-result-2026-06-22.md` |
| M7 | Return-to-P82 validation handoff | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase7-p82-validation-handoff-subplan-2026-06-22.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase7-p82-validation-handoff-result-2026-06-22.md` |
| M8 | Closeout and code-doc audit | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase8-closeout-code-doc-audit-subplan-2026-06-22.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase8-closeout-code-doc-audit-result-2026-06-22.md` |

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can BayesFilter obtain a memory-disciplined LEDH-PFPF-OT transport-gradient route whose primitive adjoints, opt-in integration, and memory behavior are checked before returning to P82 FD validation? |
| Baseline/comparator | Tiny dense TensorFlow autodiff and finite differences for primitives; dense-vs-streaming parity for memory route; same-scalar regression FD only after P82 resumes. |
| Primary pass criterion | Each phase produces required artifacts, passes local checks/reviews, preserves default-route boundaries, and blocks unsupported claims. |
| Veto diagnostics | Raw full-AD N10000 route reintroduced; missing primitive parity; hidden scalar mismatch; missing stopped/frozen policy; unsupported mode accepted; untrusted GPU evidence; HMC/default/posterior overclaims. |
| Explanatory diagnostics | Runtime, memory, device placement, parity errors, FD residuals, route metadata, seed manifests, and review notes. |
| Not concluded | P82 FD agreement, HMC/NUTS readiness, posterior correctness, exact likelihood correctness, default-gradient readiness, production readiness, or scientific superiority unless separately proven. |
| Artifacts | Master program, runbook, ledgers, subplans, results, implementation diffs, tests, review notes, and final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
|---|---|---|---|---|---|
| Raw full AD is not the N10000 route | P8p Phase 3j and P82 correction | Avoids repeating known runtime/memory explosion | Accidentally rerunning a known-bad route | M0 route-lock scan | binding |
| Start with dense tiny primitives | Reset memo and engineering discipline | Smallest check that can validate adjoint equations | Passing tiny primitives but failing filter-loop integration | M4/M5 gates | planned |
| Keep route opt-in | BayesFilter default-policy discipline | Prevents accidental default-gradient claim | Public/default behavior changes silently | M5 route/default tests | planned |
| Streaming claim deferred to M6 | Reset memo | Dense parity must precede memory claim | Overclaiming memory improvement from derivation | M6 memory ladder | planned |
| P82 resumes only after reviewed handoff | P82 correction | Keeps FD validation downstream of actual-gradient route | FD comparison launched without usable gradient side | M7 handoff review | binding |

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
4. `PASS_REVIEW`
   - Send material phase fact packets to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, patch visibly.
   - Rerun focused checks.
   - Review again when material.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Claude Read-Only Review Protocol

Use Claude only as a reviewer.  Send compact path-anchored fact packets and one
focused question unless a narrow source/code anchor audit requires direct
inspection.

Required prompt shape:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review the manual-adjoint fact packet below for:
- wrong baseline;
- proxy metrics promoted to pass criteria;
- missing stop condition;
- unfair comparison;
- hidden assumption;
- stale context;
- environment mismatch;
- unsupported claim;
- artifact mismatch.

Findings first. End with exactly one final line:
VERDICT: AGREE
or
VERDICT: REVISE
```

If Claude stalls, probe:

```text
READ-ONLY PROBE. Reply exactly PROBE_OK.
```

If the probe works, redesign the prompt.

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
