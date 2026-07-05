# Visible Gated Execution Runbook: Parameterized Zhao-Cui SIR Leaderboard Repair

Date: 2026-07-02

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

Claude review must be synchronous foreground work initiated by Codex in this
visible conversation. It must not launch detached agents, nested supervisors,
background review jobs, copied-workspace runs, or any Claude execution with
write/edit/bash authority. A small probe is allowed only as a foreground
read-only health check.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

This runbook is visible and recoverable inside the current conversation.

## Program

Master program:

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-master-program-2026-07-02.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-claude-review-ledger-2026-07-02.md`

Canonical semantic-binding artifact:

- `docs/plans/bayesfilter-parameterized-sir-semantic-binding-2026-07-02.md`

Execution ledger:

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-visible-execution-ledger-2026-07-02.md`

Stop handoff:

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-visible-stop-handoff-2026-07-02.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Baseline And Boundary Freeze | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase0-baseline-boundary-subplan-2026-07-02.md` | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase0-baseline-boundary-result-2026-07-02.md` |
| 1 | Source And Theta Contract | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase1-source-theta-contract-subplan-2026-07-02.md` | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase1-source-theta-contract-result-2026-07-02.md` |
| 2 | Dataset Row Contract Repair | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase2-dataset-row-contract-subplan-2026-07-02.md` | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase2-dataset-row-contract-result-2026-07-02.md` |
| 3 | Full Observed-Data Evaluator | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase3-full-evaluator-subplan-2026-07-02.md` | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase3-full-evaluator-result-2026-07-02.md` |
| 4 | Analytical Score Validation | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase4-score-validation-subplan-2026-07-02.md` | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase4-score-validation-result-2026-07-02.md` |
| 5 | Leaderboard Regeneration | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase5-leaderboard-regeneration-subplan-2026-07-02.md` | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase5-leaderboard-regeneration-result-2026-07-02.md` |
| 6 | Closeout And Release Note | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase6-closeout-subplan-2026-07-02.md` | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase6-closeout-result-2026-07-02.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the SIR leaderboard target be repaired from fixed/no-free-theta behavior to a reviewed parameterized observed-data filtering value and analytical-score target? |
| Baseline/comparator | Before-state commit `ef119f8bdb17b206339de92d722344a448eea745`; `scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py:208-214` with SHA256 `56f3f2bcada29447d580f2bca11746b4186ecdc2f2b045b9e16eeac16c8b995d`; current content snapshot `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.json` with SHA256 `4c3c63704cd25dd924ae9285a3a623e23b118847682f530b258b55bc392e92b5`; current content snapshot `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.md` with SHA256 `992d535ba28d1ec0bc955e206be30b43193fc43770cf7d57f73c14a502218a2b`. |
| Primary pass criterion | The final semantic-binding artifact and leaderboard artifact show a distinct parameterized SIR row with the reviewed row id, reviewed theta coordinate, reviewed truth theta, finite full observed-data/filtering value, finite admitted analytical/manual score, analytical/manual score provenance, and a derivation/source or local math-contract citation tying that score to the reviewed parameterized observed-data target; the fixed/no-free-theta row remains preserved as fixed-target evidence unless the human explicitly authorizes retirement in a later request. |
| Veto diagnostics | No reviewed theta contract; source-faithfulness claimed without source anchors; leaderboard score derived from autodiff or finite difference; branch or target mismatch; missing derivation/source/local-math binding for the admitted analytical/manual score; nonfinite value or score; full-row score route still blocked by complexity gate; final leaderboard still emits the wrong row id, theta coordinate, truth theta, or score provenance for the parameterized row. |
| Explanatory diagnostics | Diagnostic tape comparisons, finite-difference consistency, local complete-data score tests, runtime timing, GPU/XLA smoke. |
| Not concluded | No exact likelihood claim, no source-faithful inference parameterization claim unless anchored, no HMC readiness claim, no GPU production claim, no SGQF/UKF completion claim unless explicitly tested, and no claim that the fixed source-parity row and parameterized inference row are rank-comparable as the same target. |
| Artifacts | Master program, phase subplans/results, execution ledger, Claude review ledger, canonical semantic-binding artifact `docs/plans/bayesfilter-parameterized-sir-semantic-binding-2026-07-02.md`, final leaderboard JSON/MD if Phase 5 passes. |

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
- commands whose artifacts would not answer the phase question.

If the audit finds a material flaw, revise the plan or write a blocker note
before running the phase.

Initial audit: this runbook may launch Phase 0 only. Code changes are blocked
until Phase 1 reviews the theta contract and Phase 2 reviews row-contract
repair boundaries.

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
   - Apply the plain-language gate before accepting the result artifact.
   - Write or update the required phase result artifact.
4. `PASS_REVIEW`
   - Send material phase results, repairs, implementation diffs, or final
     decisions to Claude as foreground read-only review in this conversation.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, write a blocker plan.
   - Get Claude review when material.
   - Apply the repair visibly.
   - Rerun focused checks.
   - Write a blocker result.
   - Stop after five Claude review rounds for the same blocker.
   - Stop after three repeated local command/check retries for the same
     unchanged failure unless a new diagnostic changes the evidence.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Claude Read-Only Review Prompt Shape

Use one exact path first:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: check
wrong baseline, proxy promotion, missing stop condition, unfair comparison,
hidden assumption, stale context, environment mismatch, unsupported claim,
artifact mismatch, and boundary safety. End with VERDICT: AGREE or VERDICT:
REVISE.
```

If Claude does not respond, run a small foreground read-only probe. If the
probe responds, redesign the prompt by narrowing to a single path or line
range. If the foreground probe or narrowed foreground review still cannot
return a usable verdict, stop, write the visible stop handoff, and ask for
human direction. Do not use detached, nested, broader, or write-enabled review
as a workaround.

## Human-Required Stop Conditions

Stop if continuing would require:

- replacing or retiring the old fixed SIR row instead of adding a
  parameterized row without explicit human authorization;
- changing source-faithfulness classification without source anchors;
- claiming the fixed source-parity row and parameterized inference row are
  rank-comparable as the same target;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/XLA smoke results without trusted-context evidence;
- foreground Claude review remains unavailable after the probe and narrowed
  prompt path;
- continuing after Claude and Codex do not converge after five review rounds.

Each phase result must record CPU vs GPU, trusted/escalated vs sandboxed
context, TensorFlow dtype/TF32 policy when TensorFlow is used, command exit
status, and artifact paths before comparing or promoting numerical outputs.

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
