# Clean XLA JIT Visible Gated Execution Runbook

Date: 2026-07-02

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus is a read-only reviewer only.  Claude must not edit files, run
experiments, launch agents, or change state.

This runbook must not launch a detached or nested agent.  Do not use
`codex exec`, detached supervisors, backgrounded phase runners, copied
workspaces, `setsid`, `nohup`, or detached `tmux`.

## Program

Master program:

- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-master-program-2026-07-02.md`

Claude review ledger:

- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-claude-review-ledger-2026-07-02.md`

Execution ledger:

- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-visible-execution-ledger-2026-07-02.md`

Stop handoff:

- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-visible-stop-handoff-2026-07-02.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Inventory And Target Freeze | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase0-inventory-target-freeze-subplan-2026-07-02.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase0-inventory-target-freeze-result-2026-07-02.md` |
| 1 | Static Guardrails | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-guardrails-subplan-2026-07-02.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase1-static-guardrails-result-2026-07-02.md` |
| 2 | Fixed Randomness Tensorization | Draft before execution | Draft before execution |
| 3 | RK4 Loop Hygiene | Draft before execution | Draft before execution |
| 4 | Manual Scan Hygiene | Draft before execution | Draft before execution |
| 5 | Streaming Sinkhorn Loop Hygiene | Draft before execution | Draft before execution |
| 6 | Compiler Metrics Gate | Draft before execution | Draft before execution |
| 7 | Numerical Validation | Draft before execution | Draft before execution |
| 8 | Closeout | Draft before execution | Draft before execution |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the corrected full total-derivative LEDH-PFPF-OT route be made mechanically clean for GPU/XLA compilation? |
| Baseline/comparator | Current corrected full route and current compiler-hygiene inventory. |
| Primary pass criterion | Static guardrails, HLO/compiler-size gates, GPU/XLA smoke, same-scalar FD sentinel, and validation gates pass under reviewed subplans. |
| Veto diagnostics | Hidden stopped partial derivative, Python-unrolled compiled loops, non-GPU or non-XLA GPU gates, HLO growth consistent with unrolling, nonfinite numerical output, same-scalar FD failure, or review nonconvergence. |
| Explanatory diagnostics | Cold compile time, warm call time, HLO while count, HLO size, memory, FD residuals, and MCSE. |
| Not concluded | No posterior correctness, exact nonlinear likelihood correctness, production HMC readiness, all-model validation, or validation of stopped partial derivatives. |
| Artifacts | Master program, phase subplans/results, ledgers, stop handoff, audit JSON, HLO JSON, validation JSON/markdown. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| GPU/XLA/TF32 route | `AGENTS.md` default target | This is the repository production direction for LEDH-PFPF-OT | CPU-only checks could hide GPU/XLA problems | trusted GPU smoke and HLO gate | reviewed default |
| Current corrected full route as numerical baseline | 2026-07-01 final decision artifact | It passed same-scalar raw-direction FD gate but has compiler hygiene problems | Numerical baseline could be mistaken for production readiness | nonclaim table in every result | frozen |
| Static audit before refactor | user request and global policy | Prevents vague "compiled" claims | Audit too broad or too narrow | Phase 0 inventory and Claude review | hypothesis |
| HLO size/while diagnostics | clean-XLA definition | Directly checks loop representation | HLO proxy could be over-promoted | explicit nonclaim: compiler hygiene only | hypothesis |

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run only scoped visible commands in this conversation.
3. `ASSESS_GATE`: compare outputs with the phase criterion and vetoes.
4. `PASS_REVIEW`: send material result or next subplan to Claude read-only
   review.
5. `REPAIR_LOOP`: patch visibly and rerun focused checks for fixable blockers.
6. `ADVANCE_OR_STOP`: advance only after the current phase gate passes.

## Plain-Language Gate

Before accepting any result, Codex must verify that the artifact:

- states the computed quantity separately from the claimed target;
- uses direct classifications: `correct`, `wrong relative to the stated
  target`, `unsupported`, `not checked`, or `heuristic only`;
- labels mismatches as wrong relative to the target;
- avoids unsupported soft language when deciding a scientific or engineering
  claim;
- states what remains unproved.

## Claude Review Prompt Skeleton

```text
READ-ONLY BOUNDED REVIEW.
Review exactly the named paths. Do not edit files, run commands, launch agents,
or review the whole repo.

Check: wrong baseline, proxy promotion, missing stop condition, unfair
comparison, hidden assumption, stale context, environment mismatch, unsupported
claim, artifact mismatch, evasive scientific language, and mismatch between
stated target and computed quantity.

End with exactly VERDICT: AGREE or VERDICT: REVISE.
```

## Human-Required Stop Conditions

Stop if continuing would require package installation, network data fetches,
credentials, destructive git or filesystem action, changing pass criteria after
seeing results, changing repository default policy, modifying unrelated dirty
work, detached execution, or continuing after five Claude review rounds for the
same blocker.
