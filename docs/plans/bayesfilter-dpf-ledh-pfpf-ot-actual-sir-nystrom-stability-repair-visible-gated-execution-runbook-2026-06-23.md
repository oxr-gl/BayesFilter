# Actual-SIR Nystrom Stability Repair Visible Gated Execution Runbook

Date: 2026-06-23

## Status

`READY_FOR_P00_VISIBLE_LAUNCH`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.  Claude is not an
execution authority and cannot authorize crossing human, runtime, model-file,
funding, product-capability, default-policy, or scientific-claim boundaries.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

Allowed exception: Codex may launch the local non-interactive Claude worker
wrapper only for bounded read-only review commands.  This is not execution
delegation; Claude may not edit files, run experiments, launch agents, or
change state.

Execution is visible and recoverable inside the current conversation.

## Quiet Visible Execution Pattern

For TensorFlow/CUDA, benchmark, and Claude review commands:

1. Predeclare log and structured artifact paths in the subplan or ledger.
2. Redirect full stdout/stderr to a log file.
3. Prefer commands that write JSON/Markdown result artifacts.
4. Print only bounded summaries in chat: exit status, artifact paths, pass/fail
   fields, and at most 20-40 log lines on failure.
5. If Claude does not respond, run a small Claude probe.  If the probe responds,
   redesign the prompt.  If it fails, write a blocker.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-master-program-2026-06-23.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-claude-review-ledger-2026-06-23.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-visible-execution-ledger-2026-06-23.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-visible-stop-handoff-2026-06-23.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P00 | Program review and launch gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p00-program-review-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p00-program-review-result-2026-06-23.md` |
| P01 | Instrumentation implementation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p01-instrumentation-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p01-instrumentation-result-2026-06-23.md` |
| P02 | Failure localization diagnostics | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p02-failure-localization-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p02-failure-localization-result-2026-06-23.md` |
| P03 | Minimal one-change ablations | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p03-minimal-ablations-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p03-minimal-ablations-result-2026-06-23.md` |
| P04 | Repair candidate selection | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p04-repair-selection-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p04-repair-selection-result-2026-06-23.md` |
| P05 | Focused repair implementation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p05-focused-repair-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p05-focused-repair-result-2026-06-23.md` |
| P06 | P09 repair gate and decision | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p06-p09-regate-decision-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p06-p09-regate-decision-result-2026-06-23.md` |
| P07 | Closeout handoff | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p07-closeout-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p07-closeout-result-2026-06-23.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can visible gated execution localize and repair the P09 Nystrom nonfinite failure without uncontrolled tuning? |
| Baseline/comparator | P09B/P09C/P09D artifacts and compiled streaming TF32 comparator for paired repair validation. |
| Primary pass criterion | Every phase reaches its exact handoff condition with required artifacts and no forbidden claims. |
| Veto diagnostics | Missing artifact, missing stop condition, unsupported claim, nonfinite repair-validation row, missing trusted GPU evidence, or Claude/Codex non-convergence after five rounds. |
| Explanatory diagnostics | Runtime, spectra, denominator stats, timing, memory, one-row diagnostic differences. |
| Not concluded | Default readiness, superiority, posterior correctness, dense equivalence, HMC readiness. |
| Artifacts | Master program, phase subplans/results, benchmark JSON/Markdown, logs, review ledger, execution ledger. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| GPU1 preferred, GPU0 fallback | Owner instruction | Keep consistent with prior runs while avoiding memory blocker | GPU1 memory pressure could look like algorithm failure | Trusted `nvidia-smi`, artifact GPU manifest | Reviewed assumption |
| Claude read-only review | User instruction and claudecodex skill | Independent plan audit without delegating execution | Claude edits/runs or overclaims | Read-only prompt, review ledger inspection | Required |
| No detached overnight launch | Visible template | Keeps state recoverable in current conversation | Lost artifacts/session disconnect | Visible ledger and bounded logs | Required |
| Start with diagnostics, not tuning | P09D result | SVD core solve did not rescue; failure source still unknown | More tuning hides failure mechanism | P02 first-nonfinite localization | Required |

## Skeptical Plan Audit

Before executing any phase, Codex records an audit checking wrong baselines,
proxy promotion, missing stop conditions, unfair comparisons, hidden
assumptions, stale context, environment mismatch, and artifacts that do not
answer the phase question.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run only visible commands needed for the phase.
3. `ASSESS_GATE`: compare outputs against criteria and write result.
4. `PASS_REVIEW`: send material phase docs/diffs/results to Claude read-only
   review and continue only after `VERDICT: AGREE`.
5. `REPAIR_LOOP`: patch fixable issues visibly, rerun focused checks, and stop
   after five Claude rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after handoff conditions; otherwise write
   stop handoff.

## Human-Required Stop Conditions

Stop if continuing would require a project-direction decision not already in
the reviewed plan, package installation, network fetch, credentials,
destructive filesystem/git action, changing criteria after results, changing
default policy, modifying unrelated dirty work, interpreting GPU results
without trusted evidence, or continuing after Claude/Codex do not converge
after five review rounds.

## Launch Instruction

Launch P00 visibly after local file checks.  If P00 passes and Claude review
converges, continue automatically to P01.  Do not stop between phases unless a
declared stop condition or true blocker fires.
