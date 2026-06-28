# Low-Rank LEDH-PFPF-OT Model-Suite Promotion Visible Gated Execution Runbook

Date: 2026-06-24

## Status

`REVIEW_CONVERGED_READY_FOR_P00`

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

For long TensorFlow, CUDA, benchmark, HMC, or Claude review commands:

1. Predeclare log and structured artifact paths in the subplan or ledger.
2. Redirect full stdout/stderr to a log file where feasible.
3. Prefer commands that write JSON and Markdown artifacts directly.
4. Summarize only exit status, artifact paths, pass/fail fields, and failure
   tails in chat.
5. Treat excessive stdout/stderr as an execution-flow defect and repair the
   command pattern before continuing.

Log root:

- `docs/logs/low-rank-ledh-model-suite-promotion-2026-06-24/`

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-master-program-2026-06-24.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-claude-review-ledger-2026-06-24.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-visible-execution-ledger-2026-06-24.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-visible-stop-handoff-2026-06-24.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P00 | Governance and launch review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p00-governance-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p00-governance-result-2026-06-24.md` |
| P01 | LGSSM exact-Kalman gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p01-lgssm-kalman-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p01-lgssm-kalman-result-2026-06-24.md` |
| P02 | Actual-SIR stress extension | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p02-actual-sir-stress-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p02-actual-sir-stress-result-2026-06-24.md` |
| P03 | Nonlinear Gaussian gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p03-nonlinear-gaussian-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p03-nonlinear-gaussian-result-2026-06-24.md` |
| P04 | Stochastic-volatility and heavy-tail gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p04-sv-heavy-tail-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p04-sv-heavy-tail-result-2026-06-24.md` |
| P05 | Stiff nonlinear dynamics gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p05-stiff-nonlinear-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p05-stiff-nonlinear-result-2026-06-24.md` |
| P06 | Large-N and long-T resource envelope | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p06-resource-envelope-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p06-resource-envelope-result-2026-06-24.md` |
| P07 | HMC/autodiff mechanics | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p07-hmc-autodiff-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p07-hmc-autodiff-result-2026-06-24.md` |
| P08 | Final promotion decision | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p08-closeout-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-result-2026-06-24.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can locked low-rank LEDH-PFPF-OT be promoted beyond actual-SIR d18 into a bounded model-suite engineering recommendation? |
| Baseline/comparator | Streaming GPU/TF32 LEDH-PFPF-OT and LGSSM exact Kalman where declared. |
| Primary pass criterion | Required model gates pass hard validity and quality screens, with final review convergence and no unsupported claims. |
| Veto diagnostics | Active-path NumPy, exact-reference failure, untrusted GPU evidence for GPU claims, nonfinite outputs, route mismatch, dense materialization, missing artifacts, failed checks, or review nonconvergence. |
| Explanatory diagnostics | Timing, memory, ESS, tail diagnostics, Jacobian summaries, and per-seed descriptive differences. |
| Not concluded | Statistical superiority, posterior correctness outside declared references, dense equivalence, HMC readiness unless P07 passes, public API readiness, package-level or public default-policy change, or broad scientific validity. |
| Artifacts | Per-phase subplans/results, JSON/Markdown benchmark artifacts, logs, ledgers, and final result. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Locked candidate `r16_eps0p25_alpha1em08_it120` | Actual-SIR d18 certification result | Prevents post-hoc tuning during promotion testing | May overfit actual-SIR d18 | P01 exact-reference gate | baseline |
| LGSSM exact-Kalman first | Local Kalman/LGSSM fixtures and prior result | Gives an exact quality oracle before nonlinear stress | Synthetic linear success may not generalize | P02/P03/P04/P05 later gates | planned |
| Streaming comparator preserved | BayesFilter default DPF policy | Keeps fallback and paired comparison available | Comparator may itself fail a stress case | Route-fired and hard-veto checks | required |
| GPU/TF32/XLA default | Project policy | Matches production direction | Sandbox or CPU fallback could mislead | Trusted GPU probes and manifests | required |

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

Codex must preserve the review artifact and inspect whether Claude remained
read-only.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- HMC/autodiff runtime without explicit P07 approval;
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
