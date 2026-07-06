# Actual-SIR Nystrom Less-Intrusive Stability Visible Gated Execution Runbook

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
5. If live monitoring is necessary, poll bounded status instead of streaming
   full output.
6. Treat excessive stdout/stderr as an execution-flow defect.  If it
   destabilizes the session, write a stop handoff and resume quieter.

If Claude does not respond, run a small Claude probe.  If the probe responds,
redesign the prompt.  If the probe fails, write a blocker.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-master-program-2026-06-23.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-claude-review-ledger-2026-06-23.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-visible-execution-ledger-2026-06-23.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-visible-stop-handoff-2026-06-23.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P00 | Program review and launch gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p00-program-review-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p00-program-review-result-2026-06-23.md` |
| P01 | Diagnostic adequacy and missing-instrumentation gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p01-diagnostic-adequacy-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p01-diagnostic-adequacy-result-2026-06-23.md` |
| P02 | Less-intrusive repair selection | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p02-repair-selection-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p02-repair-selection-result-2026-06-23.md` |
| P03 | Focused implementation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p03-focused-implementation-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p03-focused-implementation-result-2026-06-23.md` |
| P04 | Known brittle row repair gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p04-brittle-row-repair-gate-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p04-brittle-row-repair-gate-result-2026-06-23.md` |
| P05 | Neighborhood and control gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p05-neighborhood-control-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p05-neighborhood-control-result-2026-06-23.md` |
| P06 | Promotion-readiness decision gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p06-promotion-readiness-decision-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p06-promotion-readiness-decision-result-2026-06-23.md` |
| P07 | Closeout handoff | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p07-closeout-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p07-closeout-result-2026-06-23.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a less-intrusive Nystrom stabilization repair the brittle actual-SIR row without breaking paired comparability? |
| Baseline/comparator | Compiled production-style streaming TF32 actual-SIR route; raw Nystrom brittle artifacts; positive projection as diagnostic-only rescue evidence. |
| Primary pass criterion | Each phase reaches exact handoff conditions with required artifacts and no forbidden claims; P04 repair gate requires finite/residual pass, paired max delta <= `10.0`, and paired mean delta <= `5.0`. |
| Veto diagnostics | Missing artifact, missing stop condition, unsupported claim, nonfinite repair-validation row, Nystrom residual veto, paired threshold veto, missing trusted GPU evidence, or Claude/Codex non-convergence after five rounds. |
| Explanatory diagnostics | Kernel negativity, factor diagonal error, scaling ranges, denominator floor hits, runtime, spectra, prefix behavior. |
| Not concluded | Default readiness, superiority/ranking, posterior correctness, dense equivalence, HMC readiness, scalable high-N readiness, broad robustness/unusability. |
| Artifacts | Master program, phase subplans/results, benchmark JSON/Markdown, logs, review ledger, execution ledger, stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| GPU1 preferred, GPU0 fallback | Owner instruction | Consistent with prior runs and current owner preference | GPU1 memory pressure could masquerade as algorithm failure | Trusted `nvidia-smi`, artifact GPU manifest | Required |
| Same brittle row first | Prior closeout and P09 artifacts | Tests repair without tuning target after the fact | A new row could hide original failure | P04 exact shape/seeds/rank/epsilon | Required |
| Same paired thresholds | Prior evidence contract | Prevents threshold drift after seeing results | Finite repair could be overclaimed | P04/P05 paired hard vetoes | Required |
| Claude read-only review | User instruction and claudecodex skill | Independent audit without execution delegation | Claude edits/runs or overclaims | Bounded prompt, review ledger inspection | Required |
| No detached launch | Visible template | Keeps state recoverable in current conversation | Lost context or uncontrolled process | Visible ledger and bounded logs | Required |
| Positive projection diagnostic-only | Prior closeout | It rescued finite behavior but failed paired threshold | Reusing it as promotion repair would repeat known failure | Forbidden claims/actions in every material phase | Required |

## Skeptical Plan Audit

Before executing any phase, Codex records an audit checking:

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

Initial audit status: `PASS_FOR_P00_ONLY`.  No code/GPU phase may execute until
P00 local checks and Claude review converge.

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
   - Send material phase results, repair selections, implementation diffs, or
     final decisions to Claude as read-only review.
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
   - Stop and write the handoff if a human-required blocker appears.

## Claude Read-Only Review Template

Use Claude only as a reviewer.  The prompt must say:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review:
- <bounded paths and context>

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
- boundary safety.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

Do not send whole files when a bounded path-and-question prompt is enough.
If review finds a fixable problem, patch the same subplan visibly and rerun
focused checks.  Loop Claude review at high/max effort only for material issues,
stopping after five rounds for the same blocker.

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

## Launch Instruction

Launch P00 visibly after local file checks.  If P00 passes and Claude review
converges, continue automatically to P01.  Do not stop between phases unless a
declared stop condition or true blocker fires.
