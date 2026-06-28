# Low-Rank Residual Posterior-Gradient Calibration Visible Gated Execution Runbook

Date: 2026-06-24

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus/max is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

## Quiet Visible Execution Pattern

Full command output is an artifact, not chat content.

For long TensorFlow, CUDA, benchmark, sampler, or Claude review commands:

1. Predeclare log and structured artifact paths in the subplan or ledger.
2. Redirect full stdout/stderr to a log file where feasible.
3. Prefer commands that write JSON and Markdown artifacts directly.
4. Summarize only exit status, artifact paths, pass/fail fields, and failure
   tails in chat.
5. Treat excessive stdout/stderr as an execution-flow defect and repair the
   command pattern before continuing.

Log root:

- `docs/logs/low-rank-residual-posterior-gradient-calibration-2026-06-24/`

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-master-program-2026-06-24.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-claude-review-ledger-2026-06-24.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-visible-execution-ledger-2026-06-24.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-visible-stop-handoff-2026-06-24.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P00 | Governance and launch review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p00-governance-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p00-governance-result-2026-06-24.md` |
| P01 | Value/gradient instrumentation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p01-instrumentation-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p01-instrumentation-result-2026-06-24.md` |
| P02 | Three-seed reproduction and jitter | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p02-reproduction-determinism-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p02-reproduction-determinism-result-2026-06-24.md` |
| P03 | Residual-control calibration grid | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p03-grid-calibration-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p03-grid-calibration-result-2026-06-24.md` |
| P04 | Threshold freeze and rule selection | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p04-threshold-freeze-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p04-threshold-freeze-result-2026-06-24.md` |
| P05 | LGSSM heldout validation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p05-holdout-validation-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p05-holdout-validation-result-2026-06-24.md` |
| P06 | Actual-SIR d18 value/gradient probe | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p06-actual-sir-gradient-probe-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p06-actual-sir-gradient-probe-result-2026-06-24.md` |
| P07 | Closeout and recommendation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p07-closeout-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-result-2026-06-24.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the inherited low-rank residual threshold be calibrated against posterior value, posterior gradient, and peak-neighborhood behavior? |
| Baseline/comparator | LGSSM exact Kalman value/gradient oracle, streaming finite-particle comparator, and actual-SIR d18 streaming engineering comparator. |
| Primary pass criterion | P01-P05 valid artifacts exist, P04 freezes a candidate rule before holdout, P05 validates that frozen rule, and P07 review converges without unsupported claims. |
| Veto diagnostics | Active-path NumPy, nonfinite outputs/gradients, invalid factors, dense materialization, missing exact oracle where required, threshold changes after holdout, missing artifacts, failed local checks, unsupported claims, or review nonconvergence. |
| Explanatory diagnostics | Residual distributions, projection iterations, timing, memory, ESS, seed variation, gradient component summaries, and actual-SIR paired differences. |
| Not concluded | Statistical superiority, broad posterior correctness, dense equivalence, HMC readiness, product readiness, public API readiness, package default readiness, or scientific validity. |
| Artifacts | Per-phase subplans/results, JSON/Markdown benchmark artifacts, logs, ledgers, and final result. |

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

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run only visible commands in this conversation.
3. `ASSESS_GATE`: compare outputs against primary criterion and vetoes, then
   write result artifact.
4. `PASS_REVIEW`: send material plans/results/diffs to Claude as read-only
   review.
5. `REPAIR_LOOP`: patch fixable issues, rerun focused checks, and stop after
   five Claude rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after current phase gate passes.

## Claude Read-Only Review Template

Use Claude only as a reviewer. The prompt must say:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review the named artifacts by path. Do not require the entire file to be pasted
into this prompt. Prefer focused reads of relevant sections.

Check:
- wrong baseline;
- proxy metrics promoted to pass criteria;
- missing stop condition;
- unfair comparison;
- hidden assumption;
- stale context;
- environment mismatch;
- unsupported claim;
- artifact mismatch.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

Codex must preserve the review artifact and inspect whether Claude actually
remained read-only.

If Claude does not respond, Codex must send a small read-only probe through the
same wrapper. If the probe responds, Codex must redesign the review prompt
instead of treating Claude as unavailable.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing holdout results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- HMC/autodiff runtime not explicitly approved in a future plan;
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
