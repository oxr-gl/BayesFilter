# Actual-SIR Nystrom Fixed-Policy Promotion-Stress Visible Gated Execution Runbook

Date: 2026-06-23

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested execution agent. The only
allowed cross-agent action is bounded read-only Claude review through
`bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh` when a subplan
requires it.

Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

If detached overnight execution becomes necessary, stop and write a separate
detached-supervisor plan.

## Quiet Visible Execution Pattern

Full stdout/stderr is an artifact, not chat content. For TensorFlow/CUDA,
benchmark, HMC, and Claude review commands:

1. Predeclare the log path and structured artifact path in the phase subplan.
2. Redirect full stdout/stderr to the log path.
3. Prefer commands that write JSON/Markdown/result artifacts directly.
4. After the command, print only bounded summaries: exit status, artifact
   paths, pass/fail fields, and at most the last 40 log lines on failure.
5. If live monitoring is necessary, poll bounded process/status commands.
6. Treat excessive stdout/stderr as an execution-flow defect and write a stop
   handoff if quiet execution fails repeatedly.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-master-program-2026-06-23.md`

Claude review ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-claude-review-ledger-2026-06-23.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-visible-execution-ledger-2026-06-23.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-visible-stop-handoff-2026-06-23.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P00 | Governance, local audit, and Claude review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p00-governance-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p00-governance-result-2026-06-23.md` |
| P01 | Replicated high-N gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p01-replicated-high-n-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p01-replicated-high-n-result-2026-06-23.md` |
| P02 | Full-history/memory gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p02-history-memory-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p02-history-memory-result-2026-06-23.md` |
| P03 | Nystrom-specific gradient mechanics gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p03-hmc-gradient-mechanics-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p03-hmc-gradient-mechanics-result-2026-06-23.md` |
| P04 | Closeout and default-review classification | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p04-closeout-subplan-2026-06-23.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p04-closeout-result-2026-06-23.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the fixed Nystrom policy survive replicated high-N, full-history/memory, and Nystrom-specific gradient mechanics gates? |
| Baseline/comparator | Compiled streaming TF32 actual-SIR route in paired artifacts. |
| Primary pass criterion | Every phase writes required artifacts and passes hard-veto screens without changing criteria or fixed policy. |
| Veto diagnostics | Aggregate hard vetoes, nonfinite outputs, residual threshold failure, paired threshold failure, missing GPU/TF32 provenance, missing fixed-policy metadata, malformed/missing artifacts, runtime timeout, missing or nonfinite Nystrom gradient, unsupported claim. |
| Explanatory diagnostics | Runtime, memory snapshots, ESS, residual magnitudes below threshold, factor/scaling ranges, gradient norm and tiny gradient-smoke shape. |
| Not concluded | No default change, no posterior correctness, no HMC readiness, no statistical superiority, no broad rank/epsilon robustness. |
| Artifacts | Program/runbook/ledger/subplan/result files plus benchmark JSON/Markdown/log files. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Fixed `rank=32,epsilon=0.5,raw,none` | Closed fixed-policy validation/stress artifacts | This was the viable restricted policy after brittle nearby settings failed | Overfitting to observed seeds or brittle neighborhood | Replicated high-N P01 | `hypothesis` |
| Streaming TF32 comparator | Current compiled benchmark harness | Same artifact comparator avoids stale cross-run comparison | Comparator path changes or missing paired data | P01/P02 route `both`, paired JSON audit | `baseline` |
| GPU1 preferred, GPU0 fallback | Owner instruction and repo GPU policy | Matches user preference and trusted GPU policy | Wrong or mixed physical GPU evidence | `nvidia-smi` preflight and artifact GPU fields | `reviewed` |
| Full history is required before promotion review | Prior closeout next-evidence list | Value-only artifacts may miss downstream memory/history issues | History storage path fails after value-only pass | P02 `--history-mode full` | `hypothesis` |
| Gradient gate is Nystrom-specific | Claude P00 review and promotion-boundary audit | Avoids passing P03 with an unrelated tiny HMC fixture | Generic HMC smoke says nothing about the fixed Nystrom route | P03 route-invocation and finite-gradient audit | `reviewed` |

## Skeptical Plan Audit

Before executing each phase, Codex must record a skeptical audit in chat and in
the execution ledger for material phases.

Check:

- wrong baselines;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

Current audit: this runbook avoids wrong baselines by using paired artifacts,
avoids proxy-promotion by reserving default decisions for human review, avoids
unfair comparison by freezing the fixed policy, and includes stop conditions
for artifact, GPU, threshold, runtime, and unsupported-claim failures.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites.
   - Restate the phase evidence contract in chat.
   - Append a ledger entry.
2. `EXECUTE_MINIMAL`
   - Run only visible commands in the current conversation.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against the primary criterion and veto diagnostics.
   - Write or update the required phase result artifact.
4. `PASS_REVIEW`
   - Send material phase plans, blocker decisions, HMC/gradient-boundary
     interpretations, or final classifications to Claude as read-only review
     only when required by the active subplan.
   - For mandatory review phases, continue only after `VERDICT: AGREE`, or
     revise and retry up to five rounds for the same blocker.
5. `REPAIR_LOOP`
   - For fixable plan/report blockers, patch the same artifact visibly and
     rerun focused checks/review.
   - For fixed-policy candidate failures, do not retune in this lane; write a
     result and stop or route to closeout classification.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction or default-policy decision;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- tuning or changing the fixed Nystrom policy;
- modifying unrelated dirty user work;
- interpreting GPU results without trusted-context evidence;
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
