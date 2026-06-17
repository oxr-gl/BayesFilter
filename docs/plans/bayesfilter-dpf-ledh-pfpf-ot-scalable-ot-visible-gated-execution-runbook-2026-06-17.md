# Visible Gated Execution Runbook: Scalable OT for LEDH-PFPF-OT

Date: 2026-06-17

## Status

`PHASE_0_VISIBLE_RUNBOOK_READY_FOR_REVIEW`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

If detached overnight execution becomes necessary, stop and write a separate
detached-supervisor plan. This runbook is for visible, recoverable execution
inside the current conversation.

## Quiet Visible Execution Pattern

Full output is an artifact, not chat content.  The session window gets bounded
summaries only.

Required pattern:

1. Predeclare the log path and structured artifact path in the phase subplan or
   ledger before running the command.
2. Redirect full stdout/stderr to a log file for verbose commands.
3. Prefer commands that write JSON/Markdown/result artifacts directly.
4. After each command, report only bounded summary: exit status, artifact paths,
   pass/fail fields, and at most the last 20-40 log lines on failure.
5. If live monitoring is necessary, poll bounded status commands rather than
   streaming full output.
6. Treat excessive stdout/stderr as an execution-flow defect and repair the
   command shape before continuing.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-code-master-program-2026-06-17.md`

Source-lock result:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-source-lock-result-2026-06-17.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-visible-execution-ledger-2026-06-17.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-visible-stop-handoff-2026-06-17.md`

Claude review artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p00-claude-review-round-01-2026-06-17.md`
- Additional rounds use the same prefix with `round-02` through `round-05`.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| ---: | --- | --- | --- |
| 0 | Governance, Source Lock, And Runbook Gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p00-governance-source-lock-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p00-governance-source-lock-result-2026-06-17.md` |
| 1 | Baseline Fixture Contract | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p01-baseline-fixture-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p01-baseline-fixture-result-2026-06-17.md` |
| 2 | Candidate Audit Notes | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p02-candidate-audit-notes-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p02-candidate-audit-notes-result-2026-06-17.md` |
| 3 | Common Interface Harness | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p03-common-interface-harness-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p03-common-interface-harness-result-2026-06-17.md` |
| 4 | Nystrom Prototype | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p04-nystrom-prototype-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p04-nystrom-prototype-result-2026-06-17.md` |
| 5 | Positive-Feature Prototype | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p05-positive-feature-prototype-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p05-positive-feature-prototype-result-2026-06-17.md` |
| 6 | Low-Rank Coupling Prototype | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p06-low-rank-coupling-prototype-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p06-low-rank-coupling-prototype-result-2026-06-17.md` |
| 7 | Exact Online/GPU Reference Study | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p07-exact-online-gpu-reference-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p07-exact-online-gpu-reference-result-2026-06-17.md` |
| 8 | Sparse/Localized Diagnostic | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p08-sparse-localized-diagnostic-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p08-sparse-localized-diagnostic-result-2026-06-17.md` |
| 9 | Sliced/Subspace/Minibatch Exploratory Lane | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p09-sliced-subspace-minibatch-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p09-sliced-subspace-minibatch-result-2026-06-17.md` |
| 10 | Comparative Decision | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p10-comparative-decision-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p10-comparative-decision-result-2026-06-17.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which scalable OT schemes deserve implementation or deeper testing for LEDH-PFPF-OT after paper-note-code-execution comparison? |
| Baseline/comparator | Current TensorFlow dense/streaming FilterFlow-style transport in `annealed_transport_tf.py`, with deterministic fixtures created in Phase 1. |
| Primary pass criterion | Each advanced candidate has source-grounded audit, valid transport object or declared semantic replacement, small deterministic correctness evidence, and execution-value diagnostics before recommendation. |
| Veto diagnostics | Wrong baseline; scalar OT loss treated as transport; missing source anchors; unresolved paper-code mismatch; non-TensorFlow default route; nonfinite transport; invalid marginals; runtime-only promotion; Mini-batch source blocker ignored; one-seed stochastic ranking claim. |
| Explanatory diagnostics | Backend maturity, implementation effort, runtime, memory proxy, effective rank/features/sparsity, dense-reference discrepancy, downstream LGSSM value delta. |
| Not concluded | No production default, no posterior correctness, no HMC readiness, no public API readiness, no statistically supported ranking without uncertainty evidence. |
| Artifacts | Phase subplans/results, JSON diagnostics, logs, Claude review artifacts, execution ledger, stop handoff, final comparative result, reset memo. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| TensorFlow/TFP for BayesFilter-owned algorithmic code | Project AGENTS governance | Matches repository default backend. | Non-TF prototype silently becomes default. | Phase subplans require explicit backend classification. | baseline |
| Dense/streaming `annealed_transport_tf.py` as comparator | Current experimental implementation and source-lock result | It is the actual LEDH-PFPF-OT transport baseline. | External library compared against wrong object. | Phase 1 fixture contract. | baseline |
| Mini-batch/BoMb blocked for decision-grade use | Source-lock result and partial checkout | Checkout incomplete and inspected functions do not expose full deterministic plan. | Concept lane gets promoted from partial code. | Phase 2 audit keeps blocker unless clean source appears. | reviewed |
| Claude read-only reviewer only | User instruction and runbook template | Preserves Codex as supervisor/executor. | Claude becomes execution authority or hidden editor. | Review prompt and artifact inspection. | baseline |

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
   - Send material phase plans/results, repairs, implementation diffs, or final
     decisions to Claude as read-only review.
   - Treat `VERDICT: AGREE` as review-convergence evidence, not as
     authorization.  Continue only when Codex confirms that the phase gates,
     local checks, human-required boundaries, and review-convergence evidence
     all pass.
5. `REPAIR_LOOP`
   - For fixable blockers, patch the same artifact visibly.
   - Rerun focused local checks.
   - Retry focused Claude review for material blockers.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Ledger Entry Template

```markdown
### {timestamp} - Phase {N} - {STATE}

Evidence contract:

- Question:
- Baseline/comparator:
- Primary criterion:
- Veto diagnostics:
- Non-claims:

Actions:

- {commands/edits/reviews}

Artifacts:

- {paths}

Gate status:

- {PASSED/BLOCKED/FAILED/IN_PROGRESS}

Next action:

- {next visible step}
```

## Claude Read-Only Review Template

Use Claude only as a reviewer.  Prompts must be concise and path-based.  Do not
paste whole long files into Claude prompts.

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review these named artifacts in /home/ubuntu/python/BayesFilter:
- {artifact path 1}
- {artifact path 2}

Check:
- wrong baseline;
- proxy metrics promoted to pass criteria;
- missing stop condition;
- unfair comparison;
- hidden assumption;
- stale context;
- environment mismatch;
- unsupported claim;
- artifact mismatch;
- Claude being treated as executor or authority.

Findings first. The verdict is reviewer convergence evidence only; it does not
authorize phase advancement. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

If Claude does not respond to a review prompt, run a tiny probe:

```text
READ-ONLY PROBE ONLY. Reply exactly PROBE_OK.
```

If the probe responds, redesign the stalled review prompt to be narrower.  If
the probe does not respond, stop and ask for approval or environment help.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- unblocking Mini-batch/BoMb without clean source;
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
