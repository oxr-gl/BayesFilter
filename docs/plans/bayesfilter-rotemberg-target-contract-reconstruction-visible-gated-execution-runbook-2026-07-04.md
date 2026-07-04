# BayesFilter Rotemberg Target-Contract Reconstruction Visible Gated Execution Runbook

Date: 2026-07-04

Status: `VISIBLE_EXECUTION_RUNBOOK_DRAFT`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus at max effort is a read-only reviewer only. Claude must not edit
files, run experiments, launch agents, or change state. Claude cannot
authorize crossing human, runtime, model-file, funding, product-capability, or
scientific-claim boundaries.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

## Quiet Visible Execution Pattern

Use bounded summaries for commands that may produce large output. Full output
is an artifact, not chat content.

Required pattern:

1. Predeclare log and structured artifact paths in the phase subplan or
   ledger.
2. Redirect large stdout/stderr to a log file.
3. Prefer commands that write JSON/Markdown artifacts directly.
4. Print only exit status, artifact paths, pass/fail fields, and short failure
   tails.
5. If live monitoring is necessary, poll bounded status commands.
6. Treat excessive stdout/stderr as an execution-flow defect.

## Program

Master program:

- `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-master-program-2026-07-04.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-claude-review-ledger-2026-07-04.md`

Execution ledger:

- `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-visible-execution-ledger-2026-07-04.md`

Stop handoff:

- `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-visible-stop-handoff-2026-07-04.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and reconstruction boundary | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase0-governance-subplan-2026-07-04.md` | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase0-governance-result-2026-07-04.md` |
| 1 | Metadata-source inventory | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-subplan-2026-07-04.md` | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-result-2026-07-04.md` |
| 2 | Canonical contract manifest draft | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase2-contract-manifest-subplan-2026-07-04.md` | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase2-contract-manifest-result-2026-07-04.md` |
| 3 | Local `SSMTargetContract` validation | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase3-contract-validation-subplan-2026-07-04.md` | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase3-contract-validation-result-2026-07-04.md` |
| 4 | Bridge rerun and payload boundary decision | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-subplan-2026-07-04.md` | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-result-2026-07-04.md` |
| 5 | Closeout or handoff to a separate payload program | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase5-closeout-subplan-2026-07-04.md` | `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase5-closeout-result-2026-07-04.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can one historical Rotemberg dense-IAF target cell be reconstructed into a canonical BayesFilter `SSMTargetContract` manifest without inventing fields? |
| Baseline/comparator | Dense-IAF Phase 4 stop handoff and the exact local Rotemberg result/source artifacts identified by Phase 1. |
| Primary pass criterion | A reviewed manifest is complete enough for local `SSMTargetContract` validation and bridge rerun, or the program writes exact fail-closed blockers. |
| Veto diagnostics | Unsupported field, legacy-name-only identity, process-local identity, unresolved payload presence, failed local validation, or Claude/Codex nonconvergence. |
| Explanatory diagnostics | Source hashes, line anchors, historical HMC metrics, artifact existence, and payload sizes. |
| Not concluded | Real payload reuse, HMC convergence, posterior correctness, sampler superiority, GPU readiness, and default-policy change. |
| Artifacts | Master, subplans/results, inventory JSON, manifest JSON if created, review ledger, execution ledger, stop handoff. |

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites.
   - Restate the phase evidence contract in chat.
   - Append a ledger entry.
2. `EXECUTE_MINIMAL`
   - Run only visible commands in the current conversation.
   - Prefer the smallest diagnostic or implementation needed.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against the primary criterion and veto diagnostics.
   - Write or update the required phase result artifact.
4. `PASS_REVIEW`
   - Send material next subplans or results to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - Patch fixable blockers visibly.
   - Rerun focused checks.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write handoff if a human-required blocker appears.

## Claude Prompt Shape

Use the smallest exact path that can answer the gate:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: <one
question>. End with VERDICT: AGREE or VERDICT: REVISE.
```

Run Claude in trusted/elevated context with noninteractive print mode, Opus,
and max effort. If Claude returns no output or times out, probe with:

```text
Return exactly CLAUDE_PROBE_OK.
```

If the probe responds, narrow or redesign the review prompt.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying `/home/chakwong/python`;
- copying large historical artifacts into BayesFilter;
- interpreting GPU/special hardware results without trusted-context evidence;
- continuing after Claude and Codex do not converge after five review rounds.

`VISIBLE_EXECUTION_RUNBOOK_DRAFT`
