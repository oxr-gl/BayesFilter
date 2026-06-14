# Visible Gated Overnight Execution Plan: Li-Coates Algorithm 1 LEDH-PFPF UKF

Date: 2026-06-10

## Status

`DRAFT_NOT_LAUNCHED`

## Purpose

This plan turns the reviewed Li-Coates Algorithm 1 LEDH-PFPF UKF master program
into a visible, recoverable, gated overnight execution.  Codex remains the
supervisor and executor in the current dialogue.  Claude is a read-only
reviewer only.  The plan is written first and must not be launched until the
user explicitly approves launch.

The key operating principle is repair-loop persistence: do not stop merely
because a phase needs a fix, a test fails, Claude asks for revision, or a
diagnostic exposes an implementation gap.  Stop only for a reviewed veto, a
human-required decision, an approval/environment blocker, or five failed review
loops on the same blocker.

## Source Template

This plan follows:

- `/home/chakwong/python/claudecodex/docs/templates/visible-gated-execution-runbook-template.md`

It is an overnight-duration visible plan, not a detached supervisor plan.

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This plan must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

If the user later asks for detached overnight execution, stop and write a
separate detached-supervisor plan.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-master-program-2026-06-10.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-claude-review-ledger-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-gated-execution-runbook-2026-06-10.md`

This execution plan:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-gated-overnight-execution-plan-2026-06-10.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-overnight-execution-ledger-2026-06-10.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-overnight-stop-handoff-2026-06-10.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P0 | Governance and Evidence Quarantine | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p0-governance-quarantine-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p0-governance-quarantine-result-2026-06-10.md` |
| P1 | LaTeX Documentation Rewrite | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p1-documentation-rewrite-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p1-documentation-rewrite-result-2026-06-10.md` |
| P2 | UKF Covariance Lifecycle Design | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p2-ukf-covariance-design-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p2-ukf-covariance-design-result-2026-06-10.md` |
| P3 | Algorithm 1 Implementation | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p3-implementation-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p3-implementation-result-2026-06-10.md` |
| P4 | Faithfulness Audit | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p4-faithfulness-audit-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p4-faithfulness-audit-result-2026-06-10.md` |
| P5 | Test Rerun And Comparisons | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p5-rerun-comparison-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p5-rerun-comparison-result-2026-06-10.md` |
| P6 | Supersession Closeout | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p6-supersession-closeout-subplan-2026-06-10.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p6-supersession-closeout-result-2026-06-10.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the current dialogue visibly execute the reviewed program to replace old LEDH-PFPF-OT evidence with a Li-Coates Algorithm 1 implementation using per-particle UKF covariance prediction/update, then rerun all relevant tests and comparisons? |
| Baseline/comparator | Li-Coates Algorithm 1 source anchors; current BayesFilter docs and code; exact Kalman on LGSSM and applicable UKF/SVD/CUT4/Zhao-Cui comparators; old LEDH-PFPF-OT artifacts only as quarantined historical lineage. |
| Primary pass criterion | P4 faithfulness passes and P5 result artifacts report finite, reviewed value and fixed-branch gradient comparison rows for the new Algorithm 1 implementation, with old LEDH-PFPF-OT evidence superseded in P6. |
| Veto diagnostics | Missing per-particle covariance lifecycle; unsupported documentation claims; old LEDH-PFPF-OT route used as replacement; non-finite particles, weights, determinants, or UKF covariances; failed Claude convergence after five loops on the same gate; hidden detached execution; changing pass/fail criteria after seeing results. |
| Explanatory diagnostics | Runtime, ESS, covariance spectra, determinant ranges, Monte Carlo intervals, old-vs-new deltas, filter rankings on compatible model/filter pairs. |
| Not concluded | No production default, HMC readiness, universal superiority, full stochastic-resampling gradient correctness, or source-faithful status for OT resampling itself. |
| Artifacts | Execution ledger, phase result files, Claude review ledger, run manifests, JSON/Markdown comparison reports, final stop handoff if needed. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Visible overnight execution, not detached | User request and visible-runbook template | Keeps recovery and review in the dialogue box. | Long run may need continuation after context compaction. | Ledger and stop handoff updated after each phase. | reviewed plan choice |
| Claude read-only reviewer | User request and cross-agent policy | Provides adversarial review without allowing state changes. | Reviewer may hang, fail auth, or return `REVISE`. | Minimal Claude wrapper probe/review; max five loops. | approval needed before launch |
| UKF covariance lifecycle | User request and Li-Coates Algorithm 1 allows EKF/UKF prediction/update | Targets the missed Algorithm 1 obligation. | UKF parameters/stabilization could become hidden assumptions. | P2 design and LGSSM collapse tests. | reviewed plan choice |
| CPU-only TensorFlow by default | Project GPU policy and prior DPF CPU artifacts | Avoids GPU sandbox confusion and keeps reproducibility simple. | CPU runtime may be long. | Manifest records `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import. | approval needed for long runs |
| Quarantine, not deletion, of old results | Auditability requirement | Prevents accidental evidence reuse while preserving history. | Future artifacts may still cite old rows. | P0 inventory plus P4/P6 checks. | reviewed plan choice |
| OT resampling as extension | Li-Coates source boundary | Avoids claiming OT is Algorithm 1. | Extension rows might be mislabelled as source-faithful core. | Route identifiers and Claude review checks. | reviewed plan choice |

## Anticipated Approval Requests

Before launch, ask the user to approve these categories for the whole visible
overnight program:

1. Repeated trusted Claude read-only review calls using:
   ```bash
   bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh ...
   ```
   Reason: project policy requires trusted/escalated context for Claude Code
   usage.  Claude remains read-only through wrapper tool restrictions.

2. Long CPU-only TensorFlow/Python/pytest execution for P3-P5, with
   `CUDA_VISIBLE_DEVICES=-1` set before TensorFlow import where TensorFlow runs
   are CPU-only.  Expected command families:
   ```bash
   python -m pytest ...
   python -m experiments...
   ```
   Reason: the comparison and repair loop may run for many minutes or hours.

3. LaTeX/documentation checks for P1 if the rewrite touches chapter files:
   ```bash
   latexmk ...
   ```
   Reason: documentation rewrite should be build-checked when feasible.

4. Non-destructive git inspection and staging/status commands:
   ```bash
   git status --short
   git diff -- ...
   git add ...
   ```
   Reason: phase manifests and handoff need exact changed-file state.  No commit
   or push will occur unless separately requested.

5. If a GPU/CUDA diagnostic becomes necessary, ask separately before any GPU
   command.  The current plan expects CPU-only runs; GPU use is not preapproved
   by this plan.

6. If package installation, network fetches, credential changes, destructive
   filesystem actions, default-policy changes, or detached/background execution
   become necessary, stop and ask separately.

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and in
the execution ledger.

Check:

- wrong baselines;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question;
- old LEDH-PFPF-OT evidence leaking into new claims;
- UKF being treated as paper-mandated rather than permitted/requested;
- OT being treated as source Algorithm 1 rather than a BayesFilter extension.

If the audit finds a material flaw, revise the plan or write a blocker note
before running the phase.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites.
   - Restate the phase evidence contract in chat.
   - Append a ledger entry.
   - Run the skeptical audit.
2. `EXECUTE_MINIMAL`
   - Run visible commands only in the current conversation.
   - Prefer the smallest diagnostic or implementation step that answers the
     phase question.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against the primary criterion and veto diagnostics.
   - Write or update the required phase result artifact.
   - For serious execution phases, include the full run manifest required by
     the master program.
4. `PASS_REVIEW`
   - Send material phase results, repairs, implementation diffs, or final
     decisions to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or enter `REPAIR_LOOP`.
5. `REPAIR_LOOP`
   - Classify the issue as implementation failure, documentation failure,
     tuning/numerical failure, evidence-contract failure, environment/approval
     blocker, or scientific negative result.
   - If fixable under the reviewed plan, write a bounded blocker/repair note in
     the execution ledger or a phase-specific amendment.
   - Get Claude read-only review when the repair is material.
   - Apply the repair visibly.
   - Rerun the smallest focused check that can clear the blocker.
   - Write a blocker result or append the phase result with the repair outcome.
   - Repeat until `VERDICT: AGREE`, a real veto is hit, or five Claude review
     rounds have occurred for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff only for a human-required blocker, an unresolved
     veto, or five failed review rounds on the same blocker.

## Repair Loop Non-Stop Rule

Do not stop for these non-terminal conditions:

- a failing unit test that points to a fixable implementation issue;
- a missing adapter or missing route identifier;
- a documentation gap that can be patched under P1/P4;
- Claude `VERDICT: REVISE` with actionable findings;
- a non-finite numerical diagnostic that can be localized by smaller tests;
- a comparison row marked `N/A` because an adapter is missing but in scope;
- a need to rerun a focused smoke/check after a repair.

Stop only for these valid reasons:

- the same blocker fails to converge after five Claude review loops;
- the next step requires user approval not already granted;
- the next step requires package/network/credential/environment setup;
- continuing would change the scientific question or pass/fail criteria;
- continuing would delete historical artifacts instead of superseding them;
- continuing would modify unrelated dirty user work;
- continuing would require destructive commands or detached/background launch;
- P4 faithfulness fails with an unfixable source mismatch under the current
  plan;
- P5 results are scientifically negative after P4 passes, in which case write a
  negative-result closeout rather than forcing success.

## Ledger Entry Template

```markdown
### <timestamp> - Phase <N> - <STATE>

Evidence contract:

- Question:
- Baseline/comparator:
- Primary criterion:
- Veto diagnostics:
- Non-claims:

Skeptical audit:

- Wrong baseline:
- Proxy metric risk:
- Stop conditions:
- Comparison fairness:
- Hidden assumptions:
- Environment:
- Artifact fit:

Actions:

- <commands/edits/reviews>

Artifacts:

- <paths>

Gate status:

- <PASSED/BLOCKED/FAILED/IN_PROGRESS>

Next action:

- <next visible step>
```

## Claude Read-Only Review Template

Use Claude only as a reviewer. The prompt must say:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review:
- <phase result / blocker plan / implementation diff / final decision>

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
- missing Li-Coates Algorithm 1 covariance lifecycle obligation;
- insufficient quarantine or supersession of previous LEDH-PFPF-OT evidence;
- UKF treated as paper-mandated rather than a permitted/requested Algorithm 1
  option;
- OT resampling treated as source Li-Coates Algorithm 1 rather than a
  BayesFilter extension;
- missing full run manifest for serious implementation or comparison runs;
- premature stop when a repair loop should continue.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

Codex must preserve the review artifact and inspect whether Claude actually
remained read-only.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/CUDA results without trusted-context evidence;
- deleting old LEDH-PFPF-OT artifacts instead of superseding them;
- detached/background execution;
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

## Launch Gate

This plan is not launched.  Launch requires explicit user approval after the
user reviews this file and approves the anticipated command categories above.
