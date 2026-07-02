# LEDH-PFPF-OT Streaming Manual VJP Visible Gated Execution Runbook

Date: 2026-06-23

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK_READY_FOR_REVIEW`

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

- `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-master-program-2026-06-23.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-claude-review-ledger-2026-06-23.md`

Execution ledger:

- `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-visible-execution-ledger-2026-06-23.md`

Stop handoff:

- `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-visible-stop-handoff-2026-06-23.md`

## Inherited Master-Program Invariants

This runbook inherits the following non-overridable constraints from the master
program.  It may not change baselines, promotion criteria, phase gates, default
policy, GPU/trusted-execution boundaries, or P82 FD entry conditions.

- No implementation changes before S1 closes with a reviewed derivation
  contract and S2 entry conditions are satisfied.
- No GPU work before S7, and S7 GPU evidence must be trusted/escalated.
- No S8/P82 handoff unless S7 produces a valid `N=10000` actual-gradient
  artifact for the new blockwise manual VJP route.
- Any S7 failure must write an S7 blocker result, update the visible stop
  handoff with failure status, blocking reason, artifact paths, and explicit
  prohibition on S8/P82 advancement, then stop or proceed only to S9 blocker
  closeout.
- No `transport_ad_mode=full` governed `N=10000` route.
- No Zhao-Cui comparator in this program.
- Tiny autodiff is diagnostic only and cannot promote large-N correctness.
- P82 FD remains downstream and cannot run until the actual-gradient side
  passes.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
|---|---|---|---|
| S0 | Governance and inventory | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase0-governance-inventory-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase0-governance-inventory-result-2026-06-23.md` |
| S1 | Derivation contract | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase1-derivation-contract-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase1-derivation-contract-result-2026-06-23.md` |
| S2 | Blockwise softmin VJP | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase2-softmin-vjp-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase2-softmin-vjp-result-2026-06-23.md` |
| S3 | Transport-from-potentials VJP | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase3-transport-vjp-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase3-transport-vjp-result-2026-06-23.md` |
| S4 | Sinkhorn recursion VJP | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase4-sinkhorn-recursion-vjp-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase4-sinkhorn-recursion-vjp-result-2026-06-23.md` |
| S5 | Custom-gradient wiring | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase5-custom-gradient-wiring-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase5-custom-gradient-wiring-result-2026-06-23.md` |
| S6 | Local parity ladder | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase6-local-parity-ladder-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase6-local-parity-ladder-result-2026-06-23.md` |
| S7 | GPU memory ladder | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-gpu-memory-ladder-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-gpu-memory-ladder-result-2026-06-23.md` |
| S8 | P82 handoff | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase8-p82-handoff-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase8-p82-handoff-result-2026-06-23.md` |
| S9 | Closeout | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase9-closeout-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase9-closeout-result-2026-06-23.md` |

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the current streaming replay-gradient blocker be replaced by a reviewed blockwise manual VJP route and carried through local and GPU gates before P82 resumes? |
| Baseline/comparator | Prior dense manual VJP, prior streaming replay route, P82 P7 OOM, tiny autodiff diagnostics, and later same-scalar FD only after S7. |
| Primary pass criterion | Each phase passes its artifact, local check, review, and handoff gates; S7 must produce a valid `N=10000` actual-gradient artifact before S8 may authorize P82 FD. |
| Veto diagnostics | Wrong baseline, `GradientTape` in new streaming backward, dense `[B,N,N]` retained state in large-N route, missing stop condition, unsupported mode accepted, untrusted GPU evidence, FD protocol drift. |
| Explanatory diagnostics | Runtime, memory, chunk sizes, warnings, parity errors, MCSE, review notes. |
| Not concluded | FD agreement, posterior correctness, HMC/default readiness, production readiness, scientific superiority, or Zhao-Cui source-faithfulness. |
| Artifacts | Master program, subplans/results, review ledger, execution ledger, implementation diffs, tests, JSON outputs, GPU logs, final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
|---|---|---|---|---|---|
| New route remains opt-in | Prior manual-adjoint governance | Prevents accidental default route changes | Default/public behavior changes silently | S5 route tests and source scan | binding |
| Tiny autodiff is diagnostic only | User correction and scientific policy | Avoids oracle overclaim | Tiny parity promoted to large-N proof | Evidence contract in every phase | binding |
| FD waits until actual-gradient artifact exists | P82 closeout | Avoids comparing against missing or failed gradient side | P8 launched prematurely | S8 entry gate | binding |
| GPU commands require trusted execution | AGENTS.md GPU policy | Non-escalated GPU evidence can be false | Sandbox GPU failure misread | S7 preflight | binding |
| Claude is reviewer only | User directive and runbook template | Keeps execution authority with Codex/human | Claude authorizes boundary crossing | Review prompt and ledger audit | binding |

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
   - Send material phase results or next subplans to Claude as one-exact-path
     read-only reviews.
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

Use the one-exact-path pattern from `memory.md`.

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: <one
question>. End with VERDICT: AGREE or VERDICT: REVISE.
```

If Claude stalls, probe with:

```text
READ-ONLY PROBE. Reply exactly PROBE_OK.
```

If the probe works, redesign the prompt into a smaller exact-path review.  Do
not send pasted code chunks or artifact packets.

## S7 Operational GPU Gate

S7 is the first phase allowed to run GPU work.  Codex must not treat any
non-trusted GPU result as evidence and must not enter S8 from non-trusted GPU
evidence.  Every S7 rung must record route metadata, device visibility, required
finite outputs, and artifact paths.  If a rung OOMs, writes no JSON, records
nonfinite required outputs, records wrong route metadata, or lacks trusted GPU
evidence, S7 is blocked and the visible stop handoff must be updated before
stopping or entering S9 blocker closeout.

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
