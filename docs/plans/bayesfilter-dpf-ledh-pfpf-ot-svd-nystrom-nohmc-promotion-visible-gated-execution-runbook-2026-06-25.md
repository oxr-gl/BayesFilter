# SVD-Nystrom No-HMC Promotion Visible Gated Execution Runbook

Date: 2026-06-25

## Status

`P04C_BLOCKED_INVALID_CALIBRATION_ARTIFACT`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus/max-effort is a read-only reviewer only.

This runbook must not launch detached execution with `codex exec`,
`overnight_gated_launch.sh`, `setsid`, `nohup`, detached `tmux`, backgrounded
phase runners, or copied-workspace execution.

## Quiet Visible Execution Pattern

Full command output is an artifact, not chat content.

1. predeclare JSON, Markdown, and log paths in the subplan or ledger;
2. redirect full stdout/stderr to a log file for long TensorFlow/GPU/Claude
   commands;
3. inspect structured JSON after each command;
4. report only exit status, artifact paths, gate fields, and bounded failure
   tails;
5. stop on malformed/missing artifacts before interpreting metrics.

Log root:

- `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/`

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-master-program-2026-06-25.md`

Claude review ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-claude-review-ledger-2026-06-25.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-visible-execution-ledger-2026-06-25.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-visible-stop-handoff-2026-06-25.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P00 | Governance and runbook lock | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p00-governance-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p00-governance-result-2026-06-25.md` |
| P01 | Scope, inventory, and harness readiness | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p01-scope-inventory-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p01-scope-inventory-result-2026-06-25.md` |
| P02 | LGSSM exact-reference gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p02-lgssm-reference-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p02-lgssm-reference-result-2026-06-25.md` |
| P03 | Actual-SIR stress replication | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p03-actual-sir-stress-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p03-actual-sir-stress-result-2026-06-25.md` |
| P04 | Nonlinear Gaussian gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04-nonlinear-gaussian-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04-nonlinear-gaussian-result-2026-06-25.md` |
| P04B | Nonlinear threshold governance repair | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04b-threshold-governance-repair-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04b-threshold-governance-repair-result-2026-06-25.md` |
| P04C0 | Harness threshold-control repair | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c-nonlinear-threshold-scale-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c0-harness-threshold-control-result-2026-06-26.md` |
| P04C | Nonlinear threshold scale extraction | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c-nonlinear-threshold-scale-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c-nonlinear-threshold-scale-result-2026-06-25.md` |
| P05 | Stochastic-volatility/heavy-tail gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p05-sv-heavy-tail-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p05-sv-heavy-tail-result-2026-06-25.md` |
| P06 | Stiff nonlinear dynamics gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p06-stiff-nonlinear-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p06-stiff-nonlinear-result-2026-06-25.md` |
| P07 | Resource and default-integration gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p07-resource-default-integration-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p07-resource-default-integration-result-2026-06-25.md` |
| P08 | Final scoped promotion decision | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p08-final-decision-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-result-2026-06-25.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can fixed SVD-Nystrom be promoted to a bounded internal default-candidate recommendation after exact-reference LGSSM validation and no-regression/operational-viability checks, without HMC readiness? |
| Baseline/comparator | Exact Kalman for LGSSM; compiled streaming TF32 DPF route for stochastic model-suite/resource no-regression and operational-viability comparisons. |
| Primary pass criterion | P01-P07 pass hard gates; P08 review converges without unsupported claims. |
| Veto diagnostics | Wrong baseline, active-path NumPy, dense materialization, invalid artifacts, deterministic invalidity, GPU/TF32 mismatch, exact-reference failure, missing uncertainty where required, unsupported claim, or review nonconvergence. |
| Explanatory diagnostics | Runtime, memory, residuals, ESS/tails, seed variation, Nystrom core/factor diagnostics. |
| Not concluded | HMC readiness, statistical superiority, posterior correctness beyond references, dense Sinkhorn equivalence, public API/package release readiness, broad scientific validity. |
| Artifacts | Per-phase subplans/results, JSON/Markdown benchmark artifacts, logs, ledgers, and final result. |

Non-LGSSM model-suite phases are no-regression and bounded
operational-viability checks against the declared compiled streaming TF32
route. They must not be interpreted as absolute correctness, posterior
correctness beyond declared references, statistical superiority, or broad
scientific validity.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Candidate `r32_eps0p5_raw_none_svd_rcond1e-6` | P05/P06 SVD threshold-calibration lane | Prevents post-hoc tuning during promotion testing | Actual-SIR overfit | P02/P04/P05/P06 model gates | baseline |
| HMC readiness excluded | User instruction | Promotion target is non-HMC value-route/default-candidate evidence | Accidental HMC claim | P00/P08 boundary review | owner-scoped |
| Exact Kalman first | LGSSM exact reference | Catches basic quality failure before stochastic stress | Linear success may not generalize | Later nonlinear/SV/stiff gates | planned |
| GPU1 if suitable else GPU0 | User instruction and repo GPU policy | Maintains GPU provenance | Mixed or untrusted GPU evidence | Trusted `nvidia-smi` preflight | required |

## Skeptical Plan Audit Requirement

Before executing any phase, Codex must record a skeptical audit in chat and, for
material phases, in the execution ledger:

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

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run only visible commands needed for the phase.
3. `ASSESS_GATE`: compare outputs to criteria and write result.
4. `PASS_REVIEW`: send material subplans/results to Claude as exact-path
   read-only review.
5. `REPAIR_LOOP`: patch visibly, rerun focused checks/review, stop after five
   rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after current phase gate passes.

Execution is strictly predecessor-gated. A downstream experiment or benchmark
phase must not run unless the previous phase has emitted its exact pass handoff
state. If the current phase emits repair or blocker status, the supervisor may
write or refresh the next subplan for handoff purposes, but must not execute the
downstream phase.

Program-level artifacts are phase-owned:

- P00 owns the master program, runbook, Claude review ledger, execution ledger,
  stop handoff, and P01 subplan.
- P01-P07 own their phase result, structured benchmark or inventory artifacts,
  logs, next-subplan refresh/review, and in-flight maintenance of the execution
  ledger and stop handoff for the current phase. When a material review occurs,
  the current phase also owns updating the Claude review ledger for that round.
- P08 owns final consistency across all phase results, ledgers, stop handoff,
  and the final verdict.

Missing or malformed owned artifacts are hard gate failures for the owning
phase.

## Claude Read-Only Review Template

Use exact-path bounded prompts. Do not paste whole files.

```text
READ-ONLY REVIEW ONLY.
Inspect only <exact absolute path> and same-prefix docs/plans paths named in it.
Do not inspect the repo broadly, run commands, edit files, or launch agents.
Review only the plan consistency and boundary safety. Findings first. End with
VERDICT: AGREE or VERDICT: REVISE.
```

If a prompt is blocked, first narrow it to a named heading or checklist at the
same exact path. Use multiple narrower prompts before asking the user for
explicit path/content export approval.

## Human-Required Stop Conditions

Stop if continuing would require:

- package installation, network fetches, credentials, commits, pushes, or
  destructive actions;
- changing thresholds/pass criteria after seeing results;
- changing default policy in code;
- model-file changes;
- public API/package release claims;
- HMC readiness claims;
- continuing after five unresolved Claude review rounds for the same blocker.

## Final Handoff

When execution completes or stops, write final phase reached, status, result
artifacts, Claude review trail, tests/benchmarks run, unresolved blockers, what
was not concluded, and the safest next human decision.
