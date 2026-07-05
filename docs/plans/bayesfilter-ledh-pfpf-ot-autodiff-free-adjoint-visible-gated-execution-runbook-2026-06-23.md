# LEDH-PFPF-OT Autodiff-Free Adjoint Visible Gated Execution Runbook

Date: 2026-06-23

## Status

`REVIEWED_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

This is visible, recoverable execution inside the current conversation.

## Program

Master program:

- `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-master-program-2026-06-23.md`

Claude review ledger:

- `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-claude-review-ledger-2026-06-23.md`

Execution ledger:

- `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-visible-execution-ledger-2026-06-23.md`

Stop handoff:

- `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-visible-stop-handoff-2026-06-23.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Contract Freeze | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase0-contract-freeze-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase0-contract-freeze-result-2026-06-23.md` |
| 1 | Callgraph Leak Inventory | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase1-callgraph-leak-inventory-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase1-callgraph-leak-inventory-result-2026-06-23.md` |
| 2 | Audit Tooling | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-audit-tooling-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-audit-tooling-result-2026-06-23.md` |
| 3 | Derivation Contract | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase3-derivation-contract-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase3-derivation-contract-result-2026-06-23.md` |
| 4 | SIR Analytical Derivatives | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase4-sir-analytical-derivatives-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase4-sir-analytical-derivatives-result-2026-06-23.md` |
| 5 | LEDH Flow And Log-Weight Adjoints | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase5-ledh-flow-logweight-adjoints-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase5-ledh-flow-logweight-adjoints-result-2026-06-23.md` |
| 6 | Transport No-Autodiff Audit/Repair | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase6-transport-noautodiff-audit-repair-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase6-transport-noautodiff-audit-repair-result-2026-06-23.md` |
| 7 | Filter-Level Custom Gradient | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase7-filter-custom-gradient-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase7-filter-custom-gradient-result-2026-06-23.md` |
| 8 | Certification Tests | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-certification-tests-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-certification-tests-result-2026-06-23.md` |
| 9 | Trusted GPU Ladder | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-gpu-ladder-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-gpu-ladder-result-2026-06-23.md` |
| 10 | Closeout And FD Handoff | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase10-closeout-fd-handoff-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase10-closeout-fd-handoff-result-2026-06-23.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can LEDH-PFPF-OT SIR gradients run through a production route that contains no autodiff in the production gradient path? |
| Baseline/comparator | Reviewed S7R blocker: partial manual transport VJP, outer `GradientTape`, valid N100/N1000, N2500 GPU OOM. |
| Primary pass criterion | Phase 8 audit passes for the exact route manifest and Phase 9 N10000 JSON validates against that same manifest and audit artifact. |
| Veto diagnostics | Forbidden autodiff in production path; Phase 8/9 route manifest mismatch; broad whitelist; custom-gradient `grad` body with autodiff; GPU ladder before audit; any Phase 9 higher rung after the first non-`PASSED` rung; FD before valid N10000; `transport_ad_mode=full`; unsupported scientific/default claims. |
| Explanatory diagnostics | Tiny autodiff parity, local FD checks, N100/N1000 trends, allocator warnings. |
| Not concluded | Posterior correctness, HMC readiness, production default promotion, scientific superiority, Zhao-Cui source-faithfulness, FD agreement. |
| Artifacts | Master, subplans/results, audit scripts/results, ledgers, Claude reviews, GPU JSONs, stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| TensorFlow/TFP implementation | `AGENTS.md` | BayesFilter default backend | Accidental NumPy/JAX/PyTorch route | Phase 1 source inventory | reviewed policy |
| GPU TF32 target | `AGENTS.md` | BayesFilter DPF default target | CPU-only evidence misreported as GPU | Phase 9 trusted preflight | reviewed policy |
| No-autodiff binary gate | Owner request and S7R blocker | Prevents fifth partial manual route | Whitelist hides production autodiff | Phase 2 audit tooling | program invariant |
| Claude exact-path review | Owner instruction and prior blockers | Avoids approval blocks and artifact floods | Claude reviews wrong scope | Review ledger prompt capture | program invariant |

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
   - Ensure every result includes the master-program required phase result
     schema: objective/question, entry conditions, decision, evidence, commands,
     skeptical audit, evidence-contract outcome, veto status, carry-forward
     blockers, run manifest when applicable, nonclaims, and next gate.
4. `PASS_REVIEW`
   - Send material phase results, repairs, implementation diffs, or final
     decisions to Claude as read-only exact-path review.
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
   - Treat any phase decision other than `PASSED` as a stop until a reviewed
     remediation plan exists and passes.
   - Stop and write the handoff if a human-required blocker appears.

## Phase 9 Ordered Rung Rule

For Phase 9, Codex must run rungs sequentially and stop at the first
non-`PASSED` rung, including either `BLOCKED` or `FAILED`.  The Phase 9 result
must include an ordered rung ledger with attempted rung, decision, first
non-`PASSED` rung if any, and confirmation that no higher rung was launched
after that point.

## Claude Exact-Path Review Template

Use this pattern only:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <path>. Do not edit,
run commands, launch agents, or review the whole repo. Use highest-effort
review. Question: <bounded question>. End with VERDICT: AGREE or VERDICT:
REVISE.
```

If Claude does not respond, run only this probe:

```text
READ-ONLY PROBE. Reply exactly PROBE_OK.
```

If the probe works, redesign the prompt smaller.  Do not send large code or
artifact bundles to Claude.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU results without trusted-context evidence;
- continuing after Claude and Codex do not converge after five review rounds.

## Final Visible Handoff

When execution completes or stops, write:

- final phase reached;
- final status;
- result artifacts;
- Claude review trail;
- checks/benchmarks actually run;
- unresolved blockers;
- what was not concluded;
- safest next human decision, if any.
