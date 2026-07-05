# P83 Zhao-Cui Source-Route Reset Visible Gated Execution Runbook

Date: 2026-06-22

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK_READY_FOR_PHASE0`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook is based on
`/home/chakwong/python/claudecodex/docs/templates/visible-gated-execution-runbook-template.md`.
It is visible and recoverable inside the current conversation.  Do not use:

- `codex exec`;
- detached `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

The user asked for a gated overnight execution plan, but also required Codex in
this conversation to be supervisor/executor and Claude to be read-only reviewer.
Therefore this is the visible gated plan for the whole master program.  If a
detached supervisor is later required, stop and write a separate detached plan
for human approval.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p83-source-route-reset-master-program-2026-06-22.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-execution-ledger-2026-06-22.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-stop-handoff-2026-06-22.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
|---|---|---|---|
| P83-0 | Governance reset | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase0-governance-reset-subplan-2026-06-22.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase0-governance-reset-result-2026-06-22.md` |
| P83-1 | Anchored source-route inventory | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase1-source-route-inventory-subplan-2026-06-22.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase1-source-route-inventory-result-2026-06-22.md` |
| P83-2 | Transport and Proposition-2 repair design | To be drafted/refreshed at P83-1 close | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase2-transport-marginalization-design-result-2026-06-22.md` |
| P83-3 | Minimal transport slice | To be drafted after P83-2 | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase3-minimal-transport-slice-result-2026-06-22.md` |
| P83-4 | Analytical fixed-branch derivative audit | To be drafted after P83-3 | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase4-analytical-derivative-audit-result-2026-06-22.md` |
| P83-5 | Tiny source-route mechanics smoke | To be drafted after P83-4 | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase5-mechanics-smoke-result-2026-06-22.md` |
| P83-6 | Fitting budget design | To be drafted after P83-5 | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase6-fitting-budget-design-result-2026-06-22.md` |
| P83-7 | SIR d=18 source-route validation | To be drafted after P83-6 | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-result-2026-06-22.md` |
| P83-8 | Scale/stress closeout | To be drafted after P83-7 | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase8-scale-stress-closeout-result-2026-06-22.md` |

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can visible execution reset the Zhao-Cui lane to source-route governance and anchored inventory before any implementation or numerical validation? |
| Baseline/comparator | P83 master program, reset memo, P56 source-anchor audit, P57/P58 source-route artifacts, and author source. |
| Primary pass criterion | Each phase follows its dedicated subplan, passes required local checks/reviews, writes a result/close record, drafts or refreshes the next subplan, and preserves route boundaries. |
| Veto diagnostics | Local/operator route promoted as source-faithful; UKF/FD/validation CE/JVP promoted as truth; missing anchors; missing stop conditions; d=18/LEDH launched early; Claude treated as executor or authority. |
| Explanatory diagnostics | `rg` inventories, markdown scans, code/source anchors, focused pytest/compile checks in implementation phases, and Claude read-only findings. |
| Not concluded | No source-route numerical correctness, no d=18 SIR validation, no LEDH agreement, no posterior correctness, no HMC readiness, no production default change. |
| Artifacts | Master program, runbook, execution ledger, Claude review ledger, phase subplans/results, blocker result if needed, and final stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
|---|---|---|---|---|---|
| Source route means fixed-TTSIRT retained-object route | Reset memo and P56 | Restores the documented Zhao-Cui target | Accidentally validating all-grid/operator route | P83-0/P83-1 scans and veto language | binding |
| Local all-grid/operator route is `extension_or_invention` | P56 and reset memo | It is not author retained-object TTSIRT/KR route | Old evidence reused as proof | Inventory table requires classification | binding |
| UKF is scout only | Reset memo and P57-M7 | Useful for centers/rank hints but not target measure | UKF agreement promoted as correctness | P83-0 forbidden claims | binding |
| JVP/ForwardAccumulator is diagnostic only | P82 and reset memo | Not the analytical fixed-branch source comparator | FD/JVP promoted as analytical route | P83-4 stop condition | binding |
| Phase 0/1 are documentation/inventory only | User request and evidence discipline | Avoids premature implementation | Numerical claims made from governance work | Local markdown scans and review | active |
| GPU/LEDH later require trusted execution | AGENTS policy | Sandbox can hide GPU devices | CPU or sandbox failure misread | Trusted GPU preflight in later subplan | deferred |

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
   - Send material phase fact packets to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, patch the same artifact visibly.
   - Rerun focused checks.
   - Review again when material.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Required Per-Phase Close

Each phase close must:

- run required local checks;
- write the phase result or blocker record;
- draft or refresh the next subplan;
- perform Codex consistency review of the next subplan for correctness,
  feasibility, artifact coverage, boundary safety, and stop conditions;
- use Claude read-only review for material subplans or material blockers.

## Claude Read-Only Review Protocol

Use the trusted Claude wrapper only after requesting escalated permissions:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name <short-review-name> \
  --model opus \
  --effort max \
  "<bounded prompt>"
```

Do not send whole files.  Send compact path-anchored fact packets and one
focused question.

Required prompt shape:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review the P83 fact packet below for:
- wrong baseline;
- proxy metrics promoted to pass criteria;
- missing stop condition;
- unfair comparison;
- hidden assumption;
- stale context;
- environment mismatch;
- unsupported claim;
- artifact mismatch;
- route-boundary violation.

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
- launching d=18/LEDH before source-route gates;
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
