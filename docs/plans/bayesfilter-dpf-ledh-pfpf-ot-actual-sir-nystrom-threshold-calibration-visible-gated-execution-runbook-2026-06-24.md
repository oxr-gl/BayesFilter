# Actual-SIR Nystrom Threshold Calibration Visible Gated Execution Runbook

Date: 2026-06-24

Status: `P07_CLOSEOUT_READY_FOR_NEXT_MODEL_SUITE_OR_DEFAULT_GAP_PLAN`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus/max-effort is a read-only reviewer only.  Claude may review
material subplans, blocker plans, and final decisions, but cannot edit files,
run experiments, launch agents, authorize default promotion, choose thresholds
for Codex, or cross human/product/scientific boundaries.

This runbook must not launch detached execution with `codex exec`,
`overnight_gated_launch.sh`, `setsid`, `nohup`, detached `tmux`, backgrounded
phase runners, or copied-workspace execution.

## Quiet Visible Execution Pattern

For TensorFlow/GPU benchmark commands and Claude review commands:

1. predeclare JSON, Markdown, and log paths in the subplan or ledger;
2. redirect full stdout/stderr to a log file;
3. inspect structured JSON after each command;
4. report only exit status, artifact paths, pass/fail fields, and bounded log
   tails on failure;
5. stop on malformed or missing artifacts before interpreting metrics.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-master-program-2026-06-24.md`

Claude review ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-claude-review-ledger-2026-06-24.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-visible-execution-ledger-2026-06-24.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-visible-stop-handoff-2026-06-24.md`

## Phase Index

| Phase | Name | Status | Subplan | Required result artifact |
| --- | --- | --- | --- | --- |
| P0 | Governance/runbook lock | `PASSED` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p00-governance-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p00-governance-result-2026-06-24.md` |
| P1 | Existing-artifact scale extraction | `PASSED_LOCAL` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p01-artifact-scale-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p01-artifact-scale-result-2026-06-24.md` |
| P2 | Threshold principle and freeze | `PASSED` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p02-threshold-freeze-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p02-threshold-freeze-result-2026-06-24.md` |
| P3 | Frozen-threshold statistical validation and extension | `P3_INCONCLUSIVE_STOP_THRESHOLD_UNSUPPORTED_BY_PANEL` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p03-statistical-validation-subplan-2026-06-24.md`; `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p03-extension-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p03-statistical-validation-result-2026-06-24.md` |
| P4 | Threshold-support failure repair selection | `P04_HANDOFF_POLICY_TUNING` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p04-repair-selection-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p04-repair-selection-result-2026-06-24.md` |
| P5 | SVD core-solver focused tuning | `P05_NOMINATE_SVD_TO_P06` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-result-2026-06-24.md` |
| P6 | SVD fresh validation | `P06_PASS_TO_P07_EVIDENCE_PACKAGE` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p06-svd-fresh-validation-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p06-svd-fresh-validation-result-2026-06-24.md` |
| P7 | Evidence package closeout | `P07_CLOSEOUT_READY_FOR_NEXT_MODEL_SUITE_OR_DEFAULT_GAP_PLAN` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p07-evidence-package-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p07-evidence-package-result-2026-06-24.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the inherited threshold be replaced with a calibrated `tau_component` and then tested statistically under visible gated execution? |
| Baseline/comparator | Existing artifacts and future same-artifact compiled streaming TF32 actual-SIR comparator. |
| Primary pass criterion | Each phase passes local checks, material review converges, result artifacts are written, and the next subplan is ready before advancement. |
| Veto diagnostics | Wrong baseline, proxy threshold, missing stop condition, unfair comparison, hidden assumption, stale context, environment mismatch, unsupported claim, artifact mismatch, or post-hoc threshold change. |
| Explanatory diagnostics | Descriptive scale summaries, runtime, ESS, residual magnitudes below thresholds, reviewer suggestions. |
| Not concluded | Default readiness, posterior correctness, HMC readiness, statistical superiority, broad Nystrom rejection, or threshold validity beyond declared scope. |
| Artifacts | Master program, subplans/results, ledgers, logs, optional benchmark JSON/Markdown outputs. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Use normalized per-component log-likelihood error | User agreement and threshold calibration plan | Avoids raw total-threshold arbitrariness across `T,M` | Per-component tolerance still arbitrary if not tied to intended use | P2 threshold-freeze review | hypothesis |
| Treat legacy `5.0` as non-authoritative | Local provenance search and user correction | It was inherited, not MCSE-derived | Old artifacts misread as deterministic failures | P0/P1 claim scan | reviewed |
| Use streaming route as operational comparator | Existing compiled-redo harness | It is the current same-artifact baseline | Streaming is not truth oracle | Nonclaim in every phase | baseline |
| Use GPU1 if available, else GPU0 for GPU phases | User instruction and repo GPU policy | Matches prior lane policy | Mixed or untrusted GPU evidence | Trusted `nvidia-smi` preflight | P06 used GPU0 because GPU1 was saturated |
| Claude read-only review | User instruction and worker policy | Independent plan audit without execution authority | Claude prompt too broad or no response | Probe then prompt redesign | reviewed |

## Skeptical Plan Audit Requirement

Before each phase, Codex must record a skeptical audit in chat and, for material
phases, in the execution ledger:

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

1. `PRECHECK`: read phase subplan, confirm prerequisites, restate evidence
   contract, append ledger entry.
2. `EXECUTE_MINIMAL`: run only visible commands needed for the phase.
3. `ASSESS_GATE`: compare outputs to criteria, write phase result.
4. `PASS_REVIEW`: send material subplans/results to Claude read-only review.
5. `REPAIR_LOOP`: patch visibly, rerun focused checks/review, stop after five
   rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after current phase gate passes; otherwise
   write stop handoff.

Blocker identity rule: a blocker is the same blocker when it targets the same
phase, artifact set, evidence-contract field, or boundary condition.  Renaming
or rephrasing does not reset the five-round cap.

## Claude Read-Only Review Template

Claude prompts must say:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review bounded excerpts only. Check wrong baseline, proxy metrics promoted to
criteria, missing stop condition, unfair comparison, hidden assumption, stale
context, environment mismatch, unsupported claim, and artifact mismatch.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

## Human-Required Stop Conditions

Stop if continuing would require:

- default-policy change;
- HMC/posterior/scientific claim beyond this value-route threshold plan;
- changing pass/fail criteria after seeing validation outcomes;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- broad model-file changes;
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
