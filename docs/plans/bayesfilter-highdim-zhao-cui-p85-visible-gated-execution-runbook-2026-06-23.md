# P85 Visible Gated Execution Runbook

Date: 2026-06-23

Status: `DRAFT_VISIBLE_EXECUTION_RUNBOOK_PENDING_REVIEW`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

This is an overnight-ready gated plan in the sense that every phase, repair
loop, artifact, and stop condition is explicit. It is not a detached overnight
supervisor.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p85-configurable-basis-domain-master-program-2026-06-23.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p85-claude-review-ledger-2026-06-23.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p85-visible-execution-ledger-2026-06-23.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p85-visible-stop-handoff-2026-06-23.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
|---|---|---|---|
| 0 | Governance, scope, and XLA boundary freeze | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase0-governance-xla-freeze-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase0-governance-xla-freeze-result-2026-06-23.md` |
| 1 | Author basis/domain semantics inventory | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase1-author-basis-domain-inventory-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase1-author-basis-domain-inventory-result-2026-06-23.md` |
| 2 | Config interface and XLA contract design | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase2-config-interface-xla-contract-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase2-config-interface-xla-contract-result-2026-06-23.md` |
| 3 | Implementation and test matrix review | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase3-implementation-test-matrix-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase3-implementation-test-matrix-result-2026-06-23.md` |
| 4 | Minimal configurable basis/domain implementation | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase4-configurable-basis-domain-implementation-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase4-configurable-basis-domain-implementation-result-2026-06-23.md` |
| 5 | Manifest classification and regression checks | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase5-manifest-classification-regression-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase5-manifest-classification-regression-result-2026-06-23.md` |
| 6 | P84 handoff and reset memo | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase6-p84-handoff-reset-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase6-p84-handoff-reset-result-2026-06-23.md` |

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can P85 safely repair the P84 author-basis/domain blocker by making basis/domain explicit setup configuration? |
| Baseline/comparator | P84 Phase 1 blocker, author basis/domain anchors, and local Legendre-only code anchors. |
| Primary pass criterion | Reviewed configuration, implementation, and manifest/test artifacts distinguish author `Lagrangep(4,8)` plus `AlgebraicMapping(1)` from the legacy Legendre diagnostic route. |
| Veto diagnostics | Missing anchors; unsupported source-faithfulness claim; runtime basis switching inside compiled paths; production/fitting/correctness/scaling claims; unapproved GPU/fitting/HMC/LEDH/long commands. |
| Explanatory diagnostics | Source inventory, config schema, unit-test shapes, branch-manifest identity, CPU-hidden `tf.function` static behavior. |
| Not concluded | No production readiness or scientific validity beyond the P84 Phase 1 repair. |
| Artifacts | Master program, subplans/results, ledgers, optional implementation diff, handoff, reset memo. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
|---|---|---|---|---|---|
| Basis/domain as setup parameters | Author README and SIR main script | Author code exposes these as script configuration | Treating setup flexibility as proof of parity | Phase 1 source inventory | `hypothesis_pending_inventory` |
| XLA-static config | TensorFlow/XLA compilation model and project policy | Avoid runtime Python dispatch and dynamic basis cardinality | Recompile/retrace surprises or invalid graph assumptions | Phase 2 XLA contract | `hypothesis_pending_design` |
| CPU-hidden unit tests for implementation | Project GPU policy | Avoid accidental GPU evidence claims | TensorFlow import initializes GPU or artifact omits CPU-only status | Phase 4 command manifest | `pending_exact_command` |

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
     decisions to Claude as read-only one-path reviews.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, patch the same subplan or result visibly.
   - Rerun focused checks.
   - Repeat Claude review only for material issues.
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

Use the smallest exact path that can answer the gate:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: <one
question>. End with VERDICT: AGREE or VERDICT: REVISE.
```

If Claude does not respond, run a small read-only probe. If the probe responds,
the prompt is considered the problem; redesign the bounded prompt and retry.

## Human-Required Stop Conditions

Stop if continuing would require:

- a product or scientific claim not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- fitting, HMC, LEDH, d=50/d=100, or long runtime commands without exact
  approval;
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
