# Visible Gated Overnight Execution Plan: Agent B Independent Review

Date: 2026-06-18

## Status

`DRAFT_VISIBLE_GATED_OVERNIGHT_EXECUTION_PLAN`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus/max effort is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

This is a visible, recoverable execution plan in the current conversation.

## Quiet Visible Execution Pattern

Commands that may produce large output must write full output to artifacts or
logs. Chat updates should report only bounded summaries: exit status, artifact
paths, pass/fail fields, and at most the last 20-40 log lines on failure.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-agent-b-independent-review-master-program-2026-06-18.md`

Required context to load before independent tests or artifact judgments:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-reboot-reset-memo-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p10-comparative-decision-result-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-agent-a-reduced-rank-nystrom-ladder-plan-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p04-nystrom-prototype-result-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p01-baseline-fixture-spec-2026-06-17.md`
- `docs/benchmarks/scalable_ot_candidate_result_schema.py`
- `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`
- `tests/test_nystrom_transport_tf.py`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-agent-b-independent-test-review-harness-plan-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-agent-plans-claude-review-convergence-2026-06-18.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-visible-execution-ledger-2026-06-18.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-visible-stop-handoff-2026-06-18.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| B0 | Intake and readiness gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p00-intake-readiness-subplan-2026-06-18.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p00-intake-readiness-result-2026-06-18.md` |
| B1 | Independent unit-test harness | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p01-independent-unit-test-harness-subplan-2026-06-18.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p01-independent-unit-test-harness-result-2026-06-18.md` |
| B2 | Independent artifact review script | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p02-artifact-review-script-subplan-2026-06-18.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p02-artifact-review-script-result-2026-06-18.md` |
| B3 | Independent review execution | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p03-independent-review-execution-subplan-2026-06-18.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p03-independent-review-execution-result-2026-06-18.md` |
| B4 | Closeout and decision | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p04-closeout-decision-subplan-2026-06-18.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p04-closeout-decision-result-2026-06-18.md` |

B4 also writes the parent-required standalone Agent B review result:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p11-nystrom-independent-review-result-2026-06-18.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do Agent A's reduced-rank Nystrom artifacts satisfy their declared Phase 11 evidence contract without unsupported claims, unfair comparisons, schema drift, or boundary violations? |
| Baseline/comparator | Agent A's Phase 11 artifacts against the Phase 1 dense/streaming comparator convention, with every direct top-level `candidate_records` entry's `baseline_comparator` beginning `phase1_dense_streaming`, required `diagnostics.dense_reference_max_abs_particle_error` and `diagnostics.dense_reference_rms_particle_error` fields present, and Phase 3 schema validation. |
| Primary pass criterion | B0-B4 execute visibly, produce required artifacts, and reach an evidence-class-aware Agent B decision. |
| Veto diagnostics | Missing artifacts, failed independent tests, failed artifact review, unsupported claims, Agent B mutation of Agent A files, or Claude/Codex nonconvergence after five rounds. |
| Explanatory diagnostics | Test timings, review findings, coverage tables, residual risks, and Claude read-only review outcomes. |
| Not concluded | No speedup, no default readiness, no posterior correctness, no HMC readiness, no ranking, no production readiness. |
| Artifacts | Master program, B0-B4 subplans/results, standalone parent-required review result, independent tests, review script, review JSON/Markdown, ledger, stop handoff. |

## Skeptical Plan Audit

Before executing any phase, Codex must check:

- wrong baselines;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If the audit finds a material flaw, revise the plan or write a blocker before
running the phase.

## Visible State Machine

For each phase:

1. `PRECHECK`: read the phase subplan, confirm prerequisites, restate evidence
   contract, and append a ledger entry.
2. `EXECUTE_MINIMAL`: run only visible commands in this conversation.
3. `ASSESS_GATE`: compare outputs to primary criterion and veto diagnostics.
4. `PASS_REVIEW`: use Claude read-only review for material subplans/results.
5. `REPAIR_LOOP`: patch Agent B-owned fixable problems, rerun focused checks,
   and stop after five Claude rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after the phase gate passes.

## Claude Read-Only Review Template

Use Claude only as reviewer. Prompts must be compact and must not include whole
large files. Prompt text must say:

```text
READ-ONLY REVIEW ONLY.
Do not edit files, run experiments, launch agents, or change state.
Review the compact phase summary and listed artifact paths.
Check wrong baseline, proxy metric promotion, missing stop condition, unfair
comparison, hidden assumption, stale context, environment mismatch,
unsupported claim, and artifact mismatch.
End with exactly VERDICT: AGREE or VERDICT: REVISE.
```

If Claude does not respond, run a small read-only probe.  If the probe responds,
the original prompt is considered the problem; redesign the prompt into a
smaller focused review.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- modifying Agent A-owned files before the first independent verdict;
- interpreting GPU/special hardware results without trusted-context evidence;
- continuing after Claude and Codex do not converge after five review rounds.

## Final Visible Handoff

When execution completes or stops, write:

- final phase reached;
- final status;
- result artifacts;
- Claude review trail;
- tests/checks actually run;
- unresolved blockers;
- what was not concluded;
- safest next human decision, if any.
