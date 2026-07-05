# P90 Visible Gated Overnight Execution Runbook

Date: 2026-06-28

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK_PENDING_REVIEW`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus is a read-only reviewer only. Claude is not an execution authority
and cannot authorize crossing human, runtime, model-file, funding,
product-capability, default-policy, or scientific-claim boundaries.

This runbook is visible and recoverable inside the current conversation. It
must not launch a detached or nested agent. Do not use:

- `codex exec`;
- detached overnight launchers;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p90-source-route-value-derivative-repair-master-program-2026-06-28.md`

Claude review ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p90-claude-review-ledger-2026-06-28.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p90-visible-execution-ledger-2026-06-28.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p90-visible-stop-handoff-2026-06-28.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance bootstrap and blocker inheritance | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase0-governance-bootstrap-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase0-governance-bootstrap-result-2026-06-28.md` |
| 1 | Same-target value bridge contract | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase1-value-bridge-contract-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase1-value-bridge-contract-result-2026-06-28.md` |
| 2 | Value bridge implementation | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase2-value-bridge-implementation-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase2-value-bridge-implementation-result-2026-06-28.md` |
| 3 | Value bridge execution and correctness candidate | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase3-value-bridge-execution-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase3-value-bridge-execution-result-2026-06-28.md` |
| 4 | Source-route derivative-carry design | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase4-derivative-carry-design-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase4-derivative-carry-design-result-2026-06-28.md` |
| 5 | Source-route derivative implementation | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase5-derivative-implementation-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase5-derivative-implementation-result-2026-06-28.md` |
| 6 | Same-scalar FD gradient validation | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase6-fd-gradient-validation-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase6-fd-gradient-validation-result-2026-06-28.md` |
| 7 | HMC readiness | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase7-hmc-readiness-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase7-hmc-readiness-result-2026-06-28.md` |
| 8 | GPU/XLA production readiness | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase8-gpu-xla-production-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase8-gpu-xla-production-result-2026-06-28.md` |
| 9 | Packaging, CI, and default-readiness | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase9-packaging-default-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase9-packaging-default-result-2026-06-28.md` |
| 10 | Final production decision | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase10-final-decision-subplan-2026-06-28.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase10-final-decision-result-2026-06-28.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can visible gated execution safely begin a P90 repair program that closes the value bridge first and prevents downstream promotion before value/derivative gates pass? |
| Baseline/comparator | P89 blocked final decision, P89 target manifest, P89 value-bridge blocker, and P89 derivative inventory. |
| Primary pass criterion | Execution may advance only phase by phase, with reviewed subplans/results and exact upstream pass artifacts. |
| Veto diagnostics | Wrong baseline, proxy correctness, missing stop condition, unfair comparison, hidden assumption, stale context, environment mismatch, artifact mismatch, unreviewed runtime crossing, or unsupported claim. |
| Explanatory diagnostics | Local grep/source inventory, rank/degree stability, validation loss, holdout residuals, FD/compile/HMC smoke diagnostics when later authorized. |
| Not concluded | No production readiness, value correctness, analytical-gradient correctness, FD validation, HMC readiness, GPU/XLA readiness, packaging/default readiness, scale readiness, or default-policy change at launch. |
| Artifacts | P90 master, runbook, ledgers, subplans, phase results, bridge/derivative manifests, runtime manifests when later authorized. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| P89 exact target manifest is inherited | P89 target manifest | Prevents target drift. | Wrong scalar or branch used. | Phase 0 manifest/blocker grep. | baseline |
| Value bridge before derivative/FD/HMC/GPU | P89 final decision and reset memo | P89 identified missing bridge as first repair. | Proxy correctness jumps queue. | Phase 1 contract review. | baseline |
| Claude one-path read-only review | AGENTS.md and P89 review lessons | Avoids overbroad prompts and approval stalls. | Claude reviews whole repo or edits. | Prompt shape and review ledger. | reviewed rule |
| Runtime/GPU/HMC gated by exact subplan | AGENTS.md GPU/CUDA policy | Prevents sandbox/runtime misinterpretation. | Non-escalated GPU failure or unsupported runtime claim. | Phase-specific reviewed subplan. | reviewed rule |
| No ALS training revival | P89 reset memo | ALS is historical/buggy for fixed Zhao-Cui variant. | Old training path contaminates repair. | Phase 0/1 grep for forbidden route. | baseline |
| L1 tuning default for training | P86/P88/P89 lessons | Regularization is default when training is used. | Overfit rank/rich basis evidence. | Training manifest if a future phase trains. | baseline |

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
2. `REVIEW_SUBPLAN`
   - Confirm the current phase subplan has one-path Claude `VERDICT: AGREE`
     before any phase execution.
   - Confirm the exact upstream result artifacts required by the subplan exist
     and have the required reviewed pass status.
   - For phases already reviewed at launch, reuse the recorded review only if
     the subplan has not materially changed.
   - If the subplan changed materially, rerun one-path Claude review before
     execution.
3. `EXECUTE_MINIMAL`
   - Run only commands authorized by that reviewed subplan.
   - Prefer the smallest diagnostic or implementation needed to answer the
     phase question.
   - Preserve unrelated dirty worktree changes.
4. `ASSESS_GATE`
   - Compare outputs against the primary criterion and veto diagnostics.
   - Write or update the required phase result artifact.
5. `PASS_REVIEW`
   - Send material phase results, repairs, implementation summaries, or final
     decisions to Claude as one-path read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
6. `REPAIR_LOOP`
   - For fixable blockers, write a visible repair patch or blocker plan.
   - Get Claude review when material.
   - Apply the repair visibly.
   - Rerun focused checks.
   - Write a blocker result if the repair cannot proceed.
   - Stop after five Claude review rounds for the same blocker.
7. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a true blocker appears.

Later phases cannot start unless the current phase subplan has one-path Claude
`VERDICT: AGREE` and the exact upstream result artifact required by that
subplan exists with reviewed pass status. If an upstream phase closed as a
blocker, later phases may only write blocker closeouts or a final blocked
decision unless a reviewed successor subplan repairs the blocked prerequisite.

## Claude Read-Only Review Template

Use this one-path prompt shape:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: Check
consistency, correctness, feasibility, artifact coverage, boundary safety, and
whether this artifact repeats P89 mistakes. End with VERDICT: AGREE or
VERDICT: REVISE.
```

If Claude does not respond, Codex may run a tiny read-only responsiveness probe
through the same worker. If the probe succeeds, Codex must narrow or redesign
the material prompt. The probe is not substantive review and cannot widen
context.

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

Human approval is not required for ordinary reviewed document repairs, local
artifact checks, or bounded Claude agreement loops. Claude agreement is enough
for document-only subplan/result review, but Claude cannot authorize runtime,
scientific, product, funding, model-file, or default-policy boundaries.

Phase 9 packaging/CI/default-readiness and Phase 10 final-decision artifacts are
recommendation/evidence artifacts by default. Actual package installation,
network fetch, release, CI service mutation, publishing, or default-policy
change stops for human authorization unless a prior human decision explicitly
granted that exact boundary crossing and the reviewed subplan records it.

## Launch Steps

1. Run local artifact checks over P90 master/runbook/subplans.
2. Review master with Claude until `VERDICT: AGREE` or five rounds.
3. Review runbook with Claude until `VERDICT: AGREE` or five rounds.
4. Review Phase 0 subplan with Claude until `VERDICT: AGREE` or five rounds.
5. Launch Phase 0 in visible mode.
6. At end of Phase 0, write result, refresh Phase 1 subplan if needed, run
   local checks, and review the result and next subplan.

## Final Visible Handoff

When execution completes or stops, write:

- final phase reached;
- final status;
- result artifacts;
- Claude review trail;
- checks/benchmarks actually run;
- unresolved blockers;
- what was not concluded;
- safest next action.
