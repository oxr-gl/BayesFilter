# P52 Visible Gated Execution Runbook

Date: 2026-06-10

## Status

`RUNBOOK_REVIEW_CONVERGED`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

Allowed reviewer tool exception:

- Codex may invoke the bounded non-interactive Claude worker wrapper only for
  read-only review prompts.
- Claude worker calls must not execute phases, edit files, run experiments, or
  supervise recovery.
- A Claude worker process is a reviewer tool invocation, not a detached
  executor.  If a Claude response attempts to execute or mutate state, discard
  it as invalid review output and retry with a stricter prompt or stop.

If detached overnight execution becomes necessary, stop and write a separate
detached-supervisor plan. This runbook is for visible, recoverable execution
inside the current conversation.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p52-rank-calibrated-spatial-sir-master-program-2026-06-10.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p52-claude-review-ledger-2026-06-10.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p52-visible-execution-ledger-2026-06-10.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p52-visible-stop-handoff-2026-06-10.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact | Required token |
| --- | --- | --- | --- | --- |
| P52-M0 | Governance, Target Lock, And Claim Boundaries | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m0-governance-target-lock-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m0-governance-target-lock-result-2026-06-10.md` | `PASS_P52_M0_GOVERNANCE_TARGET_LOCK` or `BLOCK_P52_M0_GOVERNANCE_TARGET_LOCK` |
| P52-M1 | P30 LaTeX Rank-Calibrated Route Update | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m1-p30-latex-rank-calibration-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m1-p30-latex-rank-calibration-result-2026-06-10.md` | `PASS_P52_M1_P30_LATEX_RANK_CALIBRATION` or `BLOCK_P52_M1_P30_LATEX_RANK_CALIBRATION` |
| P52-M2 | Memory-Bounded Rank Ceiling Protocol | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m2-memory-rank-ceiling-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m2-memory-rank-ceiling-result-2026-06-10.md` | `PASS_P52_M2_MEMORY_RANK_CEILING` or `BLOCK_P52_M2_MEMORY_RANK_CEILING` |
| P52-M3 | UKF Scouting And Centering Protocol | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m3-ukf-scouting-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m3-ukf-scouting-result-2026-06-10.md` | `PASS_P52_M3_UKF_SCOUTING` or `BLOCK_P52_M3_UKF_SCOUTING` |
| P52-M4 | Factorized Transition Route Contract | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m4-factorized-transition-route-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m4-factorized-transition-route-result-2026-06-10.md` | `PASS_P52_M4_FACTORIZED_TRANSITION_ROUTE` or `BLOCK_P52_M4_FACTORIZED_TRANSITION_ROUTE` |
| P52-M5 | Rank Selection Implementation And Tests | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m5-rank-selection-implementation-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m5-rank-selection-implementation-result-2026-06-10.md` | `PASS_P52_M5_RANK_SELECTION_IMPLEMENTATION` or `BLOCK_P52_M5_RANK_SELECTION_IMPLEMENTATION` |
| P52-M6 | Spatial SIR d=18 Calibration Row | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m6-spatial-sir-d18-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m6-spatial-sir-d18-result-2026-06-10.md` | `PASS_P52_M6_SPATIAL_SIR_D18` or `BLOCK_P52_M6_SPATIAL_SIR_D18` |
| P52-M7 | Spatial SIR d=50/d=100 Scaling Policy | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m7-spatial-sir-d50-d100-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m7-spatial-sir-d50-d100-result-2026-06-10.md` | `PASS_P52_M7_SPATIAL_SIR_D50_D100` or `BLOCK_P52_M7_SPATIAL_SIR_D50_D100` |
| P52-M8 | Integration Closeout | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m8-integration-closeout-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p52-m8-integration-closeout-result-2026-06-10.md` | `PASS_P52_M8_INTEGRATION_CLOSEOUT` or `BLOCK_P52_M8_INTEGRATION_CLOSEOUT` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the reviewed P52 program be executed visibly to replace the dense spatial SIR route with a documented, memory-bounded fixed-rank calibration protocol and bounded spatial SIR scaling evidence? |
| Baseline/comparator | P51-M3 route blocker, P52 master program, P52 phase subplans, existing P30 LaTeX note, existing highdim TensorFlow/TFP implementation, existing lower-rung spatial SIR tests, UKF scout diagnostics, and higher-rank same-route diagnostics when feasible. |
| Primary pass criterion | Every P52 phase either emits its required pass/block token with result artifacts and read-only Claude review, or stops with a human-required blocker after the repair loop. |
| Veto diagnostics | Dense all-pairs route retained as production path; UKF promoted to truth; rank chosen adaptively inside HMC likelihood; d=100 promoted to correctness; memory cap ignored; finite gradients promoted to HMC readiness; implementation drifts from P30 documentation without amendment; any source-faithfulness claim lacks paper and author-source anchors. |
| Explanatory diagnostics | Static audits, focused CPU-only pytest, compile checks, rank-budget manifests, UKF scout manifests, memory forecasts, lower-rung reference checks, deterministic replay checks, and Claude read-only reviews. |
| Not concluded | No production HMC readiness, no exact spatial SIR posterior correctness at d=50/d=100, no GPU readiness, no S&P 500 reproduction, no adaptive TT/SIRT source-faithful filtering. |
| Artifacts | P52 visible execution ledger, phase results, phase manifests, implementation diffs, P30 LaTeX patch, Claude review ledger, stop handoff, and closeout result. |

## Binding Source-Anchor Gate

Any Zhao--Cui lane phase that proposes, implements, or reviews source-route
behavior must first inspect and cite:

1. the relevant Zhao--Cui paper section/equation or reviewed paper note; and
2. the relevant author source file and line-level operation under
   `third_party/audit/zhao_cui_tensor_ssm_p10/source`.

Each implementation choice must be classified as:

- `source_faithful`: matches the cited paper/source operation;
- `fixed_hmc_adaptation`: preserves the author's algorithmic route but freezes
  randomness, ranks, bases, schedules, or samples for differentiability;
- `extension_or_invention`: not in the author paper/source and not allowed to
  close source-faithfulness gaps without explicit user approval.

If the anchors are missing, or if Claude approves without checking them, the
phase must emit `BLOCK_SOURCE_UNGROUNDED` and stop or repair the plan before
implementation.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Codex is supervisor/executor | User request and template | Keeps execution visible and recoverable | Claude accidentally becomes executor | Claude prompts say read-only only; inspect outputs | reviewed |
| Claude is read-only reviewer | User request and P52 plan | Independent critique without hidden mutation | Claude edits/runs commands | Use worker prompt with explicit read-only role; review output | reviewed |
| CPU-only default | BayesFilter AGENTS policy and P52 plan | Avoid GPU claims and sandbox ambiguity | Slow run or no GPU scaling evidence | Set `CUDA_VISIBLE_DEVICES=-1`; record CPU-only | reviewed |
| TensorFlow/TFP backend | BayesFilter governance | Required backend for gradient-bearing implementation | NumPy implementation becomes default path | Static tests and code review | reviewed |
| d=50 first full filtering stress max | P52 Claude-reviewed dimension policy | d=100 should start as scout/preflight | d=100 overclaim | Claim-class manifest in M7/M8 | reviewed |
| Rank candidates `{2,4,8,16,32}` | P52 master plan | Keeps ladder memory bounded | Rank grows until it passes | Rank-budget tests and stop rules | reviewed |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and, for
material phases, in the execution ledger.

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

Initial audit status: reviewed.  The highest-risk points are P52-M4
factorized-route design and P52-M6/M7 claim discipline.  The runbook keeps those
as gates and allows blocker results instead of fabricated passes.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites.
   - Restate the phase evidence contract in chat.
   - For source-route or paper-scale Zhao--Cui claims, cite paper/source
     anchors and classify the change as `source_faithful`,
     `fixed_hmc_adaptation`, or `extension_or_invention`.
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
   - Send material phase results, repairs, implementation diffs, or final
     decisions to Claude as read-only review.
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

## Repair Loop Protocol

The repair loop must continue through fixable issues and must not stop for no
valid reason.

Fixable issues:

- local test failures with clear code or artifact repair path;
- result artifacts missing metadata, commands, pass/block token, nonclaims, or
  manifests;
- Claude `REVISE` findings with specific repairs;
- stale claim language;
- implementation drift that can be repaired or documented in a P30 amendment;
- missing paper/source anchors for a source-route claim, if repairable by
  re-reading the paper and author source before implementation;
- rank-budget arithmetic or static-route bugs;
- missing focused tests for a just-added protocol object.

Human-required blockers:

- project-direction decision not already in the reviewed P52 plan or this
  runbook;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing default backend or scientific pass/fail criteria;
- implementing an `extension_or_invention` as if it were source-faithful
  without explicit user approval;
- changing default policy;
- modifying unrelated dirty user work;
- GPU execution or GPU claims without trusted-context approval;
- d=100 filtering-correctness claim without reviewed reference strategy;
- Codex/Claude non-convergence after five iterations on the same major issue.

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

When a human-required stop condition appears, Codex must write or update the
stop handoff before final response.

## Claude Read-Only Review Template

Use Claude only as a reviewer.  Use Opus with maximum available effort for
material reviews when the local worker accepts those options.  If Claude does
not respond, run a minimal probe.  If the probe responds, treat the original
prompt as the problem, split it, and retry a smaller read-only review.

The prompt must say:

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
- artifact mismatch.
- missing Zhao-Cui paper/source anchors for any source-faithfulness claim;
- route replacement disguised as fixed-HMC adaptation.  A fixed-HMC adaptation
  may freeze the author's route, but replacing the route is
  extension/invention unless explicitly approved.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

Codex must preserve the review artifact and inspect whether Claude actually
remained read-only.

## Anticipated Approvals

The user has requested this execution and Claude review loop.  Smooth execution
anticipates these approvals:

1. Escalated/trusted Claude Code worker calls:
   `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --model opus --effort max`
   or the closest supported Opus/max-effort equivalent.
2. If an Opus/max-effort Claude prompt stalls, a small escalated Claude probe
   through the same worker wrapper.
3. CPU-only local validation commands, including focused `pytest`,
   `python -m compileall`, `git diff --check`, `rg`, and `sed`.
4. Non-destructive file edits in the BayesFilter workspace using `apply_patch`.

No approval is requested in advance for package installation, network fetches,
GPU execution, detached/background supervisors, destructive git commands, or
modifying unrelated dirty work.  If any of those become necessary, Codex must
stop and ask separately.

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
