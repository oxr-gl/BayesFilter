# P71 Visible Gated Overnight Execution Runbook

Date: 2026-06-16

## Status

`PHASE4_BLOCKED_CLAUDE_REVIEW_AGREE_STOPPED_BEFORE_PHASE5`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook must not launch a detached or nested agent.  Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

"Overnight" means the phase ladder may contain long visible commands that
Codex monitors and records.  It does not mean hidden autonomous execution.
If a long command is needed, Codex launches it visibly in this conversation,
polls it, records the command and output artifact, and stops only at real
phase gates or human-required boundaries.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p71-claude-review-ledger-2026-06-16.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p71-runbook-claude-review-ledger-2026-06-16.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p71-visible-execution-ledger-2026-06-16.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p71-visible-stop-handoff-2026-06-16.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and current-evidence reset | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase0-governance-current-evidence-reset-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase0-governance-current-evidence-reset-result-2026-06-16.md` |
| 1 | Condition-veto capture and repair gate | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase1-condition-veto-capture-repair-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase1-condition-veto-capture-repair-result-2026-06-16.md` |
| 2 | d18 execution-only reproduction | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase2-execution-only-reproduction-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase2-execution-only-reproduction-result-2026-06-16.md` |
| 3 | Numeric evaluator and value-finite gate | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase3-numeric-evaluator-value-finite-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase3-numeric-evaluator-value-finite-result-2026-06-16.md` |
| 4 | Same-route rank and degree ladder | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4-same-route-rank-degree-ladder-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4-same-route-rank-degree-ladder-result-2026-06-16.md` |
| 5 | Filtering accuracy and reference gate | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase5-filtering-accuracy-reference-gate-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase5-filtering-accuracy-reference-gate-result-2026-06-16.md` |
| 6 | Five-seed robustness and performance | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase6-five-seed-robustness-and-performance-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase6-five-seed-robustness-and-performance-result-2026-06-16.md` |
| 7 | Value-gradient and HMC diagnostic readiness | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase7-value-gradient-hmc-readiness-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase7-value-gradient-hmc-readiness-result-2026-06-16.md` |
| 8 | Closeout and scaling-decision boundary | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase8-closeout-claim-boundary-scaling-decision-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase8-closeout-claim-boundary-scaling-decision-result-2026-06-16.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the P71 SIR d=18 validation ladder be executed visibly, phase by phase, without overclaiming accuracy, scaling, source-faithfulness, or HMC readiness? |
| Baseline/comparator | P59/P60/P66/P70 fixed route, P8-B6 execution-only closure, P70 Phase 5 unit tests, P70 Phase 6 condition-number veto, and Zhao-Cui source anchors. |
| Primary pass criterion | A phase advances only when its result artifact exists, local checks pass, material Claude review converges when required, the next phase subplan is current, and exact handoff conditions are met. |
| Veto diagnostics | Wrong baseline; execution-only evidence promoted to accuracy; P70 condition-number veto ignored; token-only source-anchor verification; same-route replay promoted to accuracy; thresholds/seeds/budgets changed after output; GPU sandbox evidence treated as trusted; HMC smoke promoted to production readiness; detached execution. |
| Explanatory diagnostics | Source-anchor table, commit/worktree drift table, fit residuals, holdout/replay residuals, condition numbers, channel norms, ESS, normalizer increments, correction weights, runtime, memory, seed spread, gradient checks. |
| Not concluded | No d18 accuracy until Phase 5 passes, no five-seed robustness until Phase 6 passes, no d50/d100 scaling, no adaptive Zhao-Cui parity, no author-code failure claim, no HMC production readiness. |
| Artifacts | Master program, runbook, execution ledger, stop handoff, phase subplans/results, machine-readable run artifacts, and Claude review ledgers. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Visible execution only | User request and visible runbook template | Keeps long work recoverable and inspectable. | Hidden detached state or missed blocker. | This runbook forbids detached/nested execution. | planned |
| P70 condition veto is active blocker | P71 master program and P70 Phase 6 result | Full d18 validation is unsafe while the first repaired row condition-veto is unresolved or unreconciled. | Treating a failed diagnostic as a nuisance. | Phase 0 drift reconciliation and Phase 1 capture/repair gate. | planned |
| Read-level source-anchor verification | AGENTS.md and P71 Claude review | Zhao-Cui source claims require actual source/local anchor verification. | Token search masquerades as source verification. | Phase 0 anchor-read table. | planned |
| Independent reference for accuracy | P71 Claude review iteration 2 | Same-route replay is consistency-only. | Self-consistency promoted to accuracy. | Phase 5 reference eligibility gate. | planned |
| Five fixed seeds for robustness | P71 Phase 6 subplan | Average is meaningful only if every seed passes vetoes and spread is reported. | Failed seed hidden by mean. | Phase 6 seed table and per-seed vetoes. | planned |
| Trusted GPU context for GPU/HMC | AGENTS.md GPU policy | Non-escalated GPU failures can be sandbox artifacts. | GPU failure or success misinterpreted. | Escalated GPU probe before GPU interpretation. | planned |

## Anticipated Approvals And Boundaries

Approved or requested for smooth visible execution:

- Claude Code read-only reviews through
  `/home/chakwong/python/claudecodex/scripts/claude_worker.sh` with Opus max
  effort.  Claude is not allowed to edit, execute experiments, or authorize
  boundary crossings.
- Local read-only shell checks: `sed`, `rg`, `git status`, `git diff`,
  `git show`, `git log`.
- Local documentation writes under `docs/plans` for runbook, ledger, phase
  result, review, and stop-handoff artifacts.
- CPU-only local Python/pytest/compile checks for focused implementation
  phases, with `CUDA_VISIBLE_DEVICES=-1` recorded when CPU-only is intended.
- Trusted/escalated GPU commands only when a reviewed phase contract requires
  GPU evidence.  The exact command must be written in the phase subplan/result
  before it is interpreted.

Not approved by this runbook:

- package installation or dependency downloads;
- funding/product-capability changes;
- destructive git or filesystem actions;
- editing unrelated dirty user work;
- changing pass/fail thresholds after seeing outputs;
- d50/d100 scaling execution before P71 closeout supports a separate plan;
- HMC production-readiness claims.

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and in
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

If the audit finds a material flaw, revise the plan or write a blocker note
before running the phase.  Execution begins only after the phase survives this
audit.

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
4. `DRAFT_NEXT`
   - Draft or refresh the next phase subplan.
   - Ensure the current result explicitly produces next-phase entry
     conditions.
5. `PASS_REVIEW`
   - Send material phase results, repairs, implementation diffs, or final
     decisions to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
6. `REPAIR_LOOP`
   - For fixable blockers, write a blocker plan.
   - Get Claude review when material.
   - Apply the repair visibly.
   - Rerun focused checks.
   - Write a blocker result.
   - Stop after five Claude review rounds for the same blocker.
7. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Ledger Entry Template

```markdown
### <timestamp> - Phase <N> - <STATE>

Evidence contract:

- Question:
- Baseline/comparator:
- Primary criterion:
- Veto diagnostics:
- Non-claims:

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

Use Claude only as a reviewer.  The prompt must say:

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
- source-anchor gap.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

Codex must preserve the review artifact and inspect whether Claude actually
remained read-only.

Claude transport/no-response handling:

1. Use the trusted wrapper
   `/home/chakwong/python/claudecodex/scripts/claude_worker.sh` for all
   non-interactive Claude review.
2. If a material Claude review does not respond, monitor the worker process
   before assuming a model or prompt failure.
3. If the worker appears stalled or exits without a usable verdict, run a tiny
   trusted-context read-only probe through the same wrapper.
4. If the probe responds, treat the original prompt as the problem: redesign
   the prompt to be smaller and path-bounded, then retry.
5. If the trusted probe also fails, treat that as a Claude transport/auth/tool
   blocker, write a blocker handoff, and stop for human direction.

Do not stop merely because one broad Claude prompt stalls while the trusted
probe succeeds.  That is a prompt-design problem, not a phase blocker.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- using Claude as executor or authority rather than read-only reviewer;
- continuing after Claude and Codex do not converge after five review rounds.

## Launch Rule

This runbook may be launched after:

- local runbook checks pass;
- Claude read-only runbook review returns `VERDICT: AGREE`;
- the execution ledger records `PHASE0_PRECHECK_READY`.

Launch means starting Phase 0 visibly in the current conversation.  Phase 0 may
run read-level anchor and drift checks and write its result artifact.  Later
phases advance only through their own gates.

## Prelaunch Checklist

Before recording `PHASE0_PRECHECK_READY`, Codex must verify and record:

- `git diff --check` passes for the runbook packet;
- required role/repair-loop/no-detached tokens are present in the runbook;
- Claude runbook review returned `VERDICT: AGREE`;
- the runbook review ledger records the final verdict and any repairs;
- the execution ledger records the local checks and review status;
- no Phase 0 command has run before those checks;
- remaining dirty worktree entries are unrelated and unstaged unless the phase
  explicitly touches them.

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
