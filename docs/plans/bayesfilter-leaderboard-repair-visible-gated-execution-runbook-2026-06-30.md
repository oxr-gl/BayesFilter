# BayesFilter leaderboard repair visible gated execution runbook

Date: 2026-06-30

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

If detached overnight execution is needed later, stop and write a separate detached-supervisor plan.

## Program

Master program:

- `docs/plans/bayesfilter-leaderboard-repair-master-program-2026-06-30.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-leaderboard-repair-claude-review-ledger-2026-06-30.md`

Execution ledger:

- `docs/plans/bayesfilter-leaderboard-repair-visible-execution-ledger-2026-06-30.md`

Stop handoff:

- `docs/plans/bayesfilter-leaderboard-repair-visible-stop-handoff-2026-06-30.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Contract audit and fail-closed schema | `docs/plans/bayesfilter-leaderboard-repair-phase0-contract-audit-subplan-2026-06-30.md` | `docs/plans/bayesfilter-leaderboard-repair-phase0-contract-audit-result-2026-06-30.md` |
| 1 | Actual-SV SGQF same-target value row | `docs/plans/bayesfilter-leaderboard-repair-phase1-actual-sv-sgqf-value-subplan-2026-06-30.md` | `docs/plans/bayesfilter-leaderboard-repair-phase1-actual-sv-sgqf-value-result-2026-06-30.md` |
| 2 | Actual-SV SGQF strict analytical score | `docs/plans/bayesfilter-leaderboard-repair-phase2-actual-sv-sgqf-score-subplan-2026-06-30.md` | `docs/plans/bayesfilter-leaderboard-repair-phase2-actual-sv-sgqf-score-result-2026-06-30.md` |
| 3 | Zhao-Cui LGSSM m3 evaluator adapter | `docs/plans/bayesfilter-leaderboard-repair-phase3-zhaocui-lgssm-adapter-subplan-2026-06-30.md` | `docs/plans/bayesfilter-leaderboard-repair-phase3-zhaocui-lgssm-adapter-result-2026-06-30.md` |
| 4 | Predator-prey SGQF/Zhao-Cui cells | `docs/plans/bayesfilter-leaderboard-repair-phase4-predator-prey-cells-subplan-2026-06-30.md` | `docs/plans/bayesfilter-leaderboard-repair-phase4-predator-prey-cells-result-2026-06-30.md` |
| 5 | Spatial SIR d18 parameterized observed-data row | `docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-subplan-2026-06-30.md` | `docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-result-2026-06-30.md` |
| 6 | Generalized SV target/evaluator repair | `docs/plans/bayesfilter-leaderboard-repair-phase6-generalized-sv-subplan-2026-06-30.md` | `docs/plans/bayesfilter-leaderboard-repair-phase6-generalized-sv-result-2026-06-30.md` |
| 7 | Batched CPU/GPU/XLA benchmarking | `docs/plans/bayesfilter-leaderboard-repair-phase7-batch-gpu-xla-subplan-2026-06-30.md` | `docs/plans/bayesfilter-leaderboard-repair-phase7-batch-gpu-xla-result-2026-06-30.md` |
| 8 | Final regeneration and release note | `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-subplan-2026-06-30.md` | `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-result-2026-06-30.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the highdim leaderboard be repaired to report value, strict analytical score, target, batch, and GPU/XLA status honestly? |
| Baseline/comparator | Current June 30 leaderboard artifacts, corrected actual-SV derivation note `docs/plans/bayesfilter-highdim-actual-sv-single-target-corrected-derivation-note-2026-06-29.md`, P91 SIR artifacts `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-result-2026-06-29.md`, `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-manifest-2026-06-29.json`, `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-manifest-2026-06-29.json`, and exact/Kalman references only for affine/Gaussian rows. |
| Primary pass criterion | Final leaderboard has no stale target blockers, no invalid analytical-score claims, and precise blockers for any remaining missing rows. |
| Veto diagnostics | Tape/autodiff analytical score; missing theta for score row; stale actual-SV `not_same_target`; GPU/XLA claim from non-trusted context; source-faithfulness claim without anchors. |
| Explanatory diagnostics | FD residuals, multi-replicate expected-score probes, timing, compile status, low-budget smoke tests. |
| Not concluded | Exact nonlinear likelihood, posterior correctness, HMC convergence, universal GPU speedup, or production readiness beyond recorded gates. |
| Artifacts | Phase results, regenerated leaderboard, review ledger, execution ledger, stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Strict analytical score excludes `GradientTape` | User directive and current leaderboard discussion | Prevents autodiff diagnostic from becoming analytical result | Valid score hidden as blocked | Provenance scan and code review | reviewed assumption |
| Direct actual-SV SGQF is same-target value route | Corrected derivation note 2026-06-29 | Old `not_same_target` label is stale for direct transformed route | Accidentally admit augmented-noise route | Function/provenance binding check | reviewed assumption |
| SIR score row requires free theta | Likelihood definition and user correction | No score without a parameterized likelihood | Complete-data component misreported as full likelihood | Parameter contract check | reviewed assumption |
| GPU/XLA evidence must be trusted-context | AGENTS.md GPU policy | Sandbox can hide GPU | False GPU failure or false claim | Escalated `nvidia-smi` and framework probe | policy |
| CPU-only framework checks must hide GPUs before import | AGENTS.md GPU policy | Avoid accidental GPU initialization in non-escalated context | Environment-sensitive artifacts | `CUDA_VISIBLE_DEVICES=-1` recorded in command/artifact | policy |

## Skeptical Plan Audit

Before executing each phase, Codex must record a skeptical audit in chat and the ledger.

Check:

- wrong baselines;
- proxy metrics treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If the audit finds a material flaw, revise the plan or write a blocker note before running that phase.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites.
   - Restate the phase evidence contract in chat.
   - Append a ledger entry.
2. `EXECUTE_MINIMAL`
   - Run only visible commands in the current conversation.
   - Prefer the smallest diagnostic or implementation needed to answer the phase question.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against the primary criterion and veto diagnostics.
   - Write or update the required phase result artifact.
4. `PASS_REVIEW`
   - Send material phase results, repairs, implementation diffs, or final decisions to Claude as read-only review.
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

Default first prompt:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the file itself explicitly asks you to inspect a cited line: <one path>. Do not edit, run commands, launch agents, or review the whole repo. Question: <one question>. Check wrong baseline, proxy metrics promoted to pass criteria, missing stop condition, unfair comparison, hidden assumption, stale context, environment mismatch, unsupported claim, and artifact mismatch. Findings first. End with exactly VERDICT: AGREE or VERDICT: REVISE.
```

If Claude does not respond, run a tiny read-only probe. If the probe responds, redesign the prompt to a smaller exact path.

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
