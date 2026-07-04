# BayesFilter Dense-IAF Migration Visible Gated Execution Runbook

Date: 2026-07-04

Status: `VISIBLE_EXECUTION_RUNBOOK_READY`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus at max effort is a read-only reviewer only. Claude must not edit
files, run experiments, launch agents, or change state. Claude cannot authorize
crossing human, runtime, model-file, funding, product-capability, or
scientific-claim boundaries.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

## Quiet Visible Execution Pattern

Use bounded summaries for commands that may produce large output. Full output is
an artifact, not chat content.

Required pattern:

1. Predeclare log and structured artifact paths in the phase subplan or ledger.
2. Redirect large stdout/stderr to a log file.
3. Prefer commands that write JSON/Markdown artifacts directly.
4. Print only exit status, artifact paths, pass/fail fields, and short failure
   tails.
5. If live monitoring is necessary, poll bounded status commands.
6. Treat excessive stdout/stderr as an execution-flow defect.

Claude review prompts must use exact paths. Do not paste whole files into
Claude.

## Program

Master program:

- `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-master-program-2026-07-04.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-claude-review-ledger-2026-07-04.md`

Execution ledger:

- `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-visible-execution-ledger-2026-07-04.md`

Stop handoff:

- `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-visible-stop-handoff-2026-07-04.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and boundary freeze | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase0-governance-boundary-freeze-subplan-2026-07-04.md` | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase0-governance-boundary-freeze-result-2026-07-04.md` |
| 1 | Historical artifact taxonomy | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase1-historical-artifact-taxonomy-subplan-2026-07-04.md` | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase1-historical-artifact-taxonomy-result-2026-07-04.md` |
| 2 | Dense-IAF frozen schema | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase2-dense-iaf-schema-subplan-2026-07-04.md` | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase2-dense-iaf-schema-result-2026-07-04.md` |
| 3 | TensorFlow/TFP loader implementation | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase3-tf-loader-implementation-subplan-2026-07-04.md` | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase3-tf-loader-implementation-result-2026-07-04.md` |
| 4 | Target-signature bridge | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-subplan-2026-07-04.md` | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase4-target-signature-bridge-result-2026-07-04.md` |
| 5 | Payload restoration or export | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase5-payload-export-subplan-2026-07-04.md` | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase5-payload-export-result-2026-07-04.md` |
| 6 | One real-artifact load canary | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase6-real-artifact-load-canary-subplan-2026-07-04.md` | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase6-real-artifact-load-canary-result-2026-07-04.md` |
| 7 | Mechanics canary and closeout | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase7-mechanics-closeout-subplan-2026-07-04.md` | `docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-phase7-mechanics-closeout-result-2026-07-04.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can dense-IAF NeuTra artifacts be migrated into a stable BayesFilter frozen-transport schema for generic nonlinear SSM targets and filters? |
| Baseline/comparator | Prior generic SSM interface closeout and Phase 6 artifact inventory from 2026-07-03. |
| Primary pass criterion | A reviewed loader schema and implementation can load at least one schema-valid, target-signature-matched dense-IAF artifact or write a precise fail-closed blocker explaining why no such artifact exists. |
| Veto diagnostics | Missing payload, missing or mismatched target signature, process-local identity, nonfinite tensor, invalid shape, unsupported schema, unreviewed copy/runtime boundary, or failed focused tests. |
| Explanatory diagnostics | Candidate IDs, topology, tensor counts, source paths, SHA-256 hashes, step sizes, leapfrog counts, R-hat values where source artifacts provide them. |
| Not concluded | HMC convergence, posterior correctness, sampler superiority, all-filter readiness, production default change, and scientific claims. |
| Artifacts | Master program, phase subplans/results, inventory JSON, schema doc or code, tests, review ledger, execution ledger, stop handoff. |

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
   - Compare outputs against primary criterion and veto diagnostics.
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

Run Claude in trusted/elevated context with noninteractive print mode, Opus, and
max effort. If Claude returns no output or times out, probe with:

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
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- copying large historical artifacts into BayesFilter without explicit approval;
- continuing after Claude and Codex do not converge after five review rounds.

`VISIBLE_EXECUTION_RUNBOOK_READY`
