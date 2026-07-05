# LEDH Leaderboard Score Repair Visible Gated Execution Runbook

Date: 2026-07-03

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK_PENDING_CLAUDE_REVIEW`

## Resume Amendment

Execution resumes after Phase 2 retracted the tape-gradient LGSSM score route.
The active phase is Phase 3 manual-VJP LGSSM score repair.  Equivalently,
Phase 3 must implement a manual VJP route or a documented analytical
equivalent, not an autodiff tape score.

Additional hard gates for all resumed work:

- `GradientTape` and `ForwardAccumulator` are forbidden in production LEDH
  score computation.
- Admitted value+score rows must report one scalar route for both quantities:
  `value_route_id == score_route_id` and
  `value_score_route_status == same_route_value_score`.
- Same-scalar finite differences must perturb the exact scalar whose value is
  reported.
- CPU-hidden diagnostics are debugging only, not material GPU/XLA/TF32 score
  evidence.

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent.  Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

Commands that use Claude Code or GPU/CUDA/TensorFlow/XLA must run in trusted or
escalated context.

## Quiet Visible Execution Pattern

Full stdout/stderr is an artifact, not chat content.

For large commands:

1. predeclare the log path and structured artifact path;
2. redirect full stdout/stderr to the log path;
3. print only exit status, artifact paths, key pass/fail fields, and at most
   the last 40 log lines on failure;
4. preserve logs under `docs/plans/logs/`.

## Program

Master program:

- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-master-program-2026-07-03.md`

Reviewed plan artifacts:

- `docs/reviews/bayesfilter-ledh-leaderboard-score-repair-plan-review-bundle-2026-07-03.md`

Execution ledger:

- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-visible-execution-ledger-2026-07-03.md`

Stop handoff:

- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-visible-stop-handoff-2026-07-03.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Launch Boundary And Score Meaning Freeze | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase0-launch-boundary-score-meaning-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase0-launch-boundary-score-meaning-result-2026-07-03.md` |
| 1 | Row Score Inventory | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase1-row-score-inventory-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase1-row-score-inventory-result-2026-07-03.md` |
| 2 | Same-Target LGSSM Score Repair | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase2-lgssm-score-repair-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase2-lgssm-score-repair-result-2026-07-03.md` |
| 3 | Memory-Safe GPU/XLA Score Scaling | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase3-memory-safe-gpu-xla-score-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase3-memory-safe-gpu-xla-score-result-2026-07-03.md` |
| 4 | Fixed SIR Score Target Decision | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase4-fixed-sir-score-target-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase4-fixed-sir-score-target-result-2026-07-03.md` |
| 5 | Nonlinear Row Adapter Admission | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase5-nonlinear-adapter-admission-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase5-nonlinear-adapter-admission-result-2026-07-03.md` |
| 6 | Admitted Nonlinear Score Repair | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase6-nonlinear-score-repair-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase6-nonlinear-score-repair-result-2026-07-03.md` |
| 7 | Leaderboard Merge | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase7-leaderboard-merge-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase7-leaderboard-merge-result-2026-07-03.md` |
| 8 | Closeout And Reset Memo | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase8-closeout-reset-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase8-closeout-reset-result-2026-07-03.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can LEDH compute total-derivative score rows for the existing highdim leaderboard targets? |
| Baseline/comparator | July 3 LEDH-inclusive leaderboard for current status; row-specific exact score or same-scalar finite differences for score checks. |
| Primary pass criterion | Rows are promoted only when same-target value and total-derivative score checks pass; otherwise they remain plainly blocked with reason. |
| Veto diagnostics | Wrong target, value/score route mismatch, tape/autodiff score computation, partial derivative admitted as score, missing parameter dependency, nonfinite score, missing MCSE/FD/exact evidence, missing GPU/XLA evidence for production route, hidden failed row. |
| Explanatory diagnostics | Compile time, runtime, memory, ESS, per-seed dispersion, score covariance conditioning, particle trend. |
| Not concluded | HMC readiness, posterior correctness, scientific superiority, and runtime ranking are not concluded. |
| Artifacts | Master program, phase subplans/results, row inventory JSON/MD, score diagnostic JSON/MD, merged leaderboard JSON/MD, review records, logs. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Score means total derivative | User direction and July 1 repair result | MLE/HMC need derivative of the stated log likelihood | Partial derivative is incorrectly admitted | Phase 0 score meaning freeze | planned |
| Value and score use the same scalar route | Current leaderboard admission guard and owner direction | Prevents reporting one algorithm's value with another route's derivative | Mixed-route row is incorrectly admitted | `value_route_id == score_route_id` validation before merge | active |
| Baseline is July 3 LEDH-inclusive leaderboard | Existing closeout and reset memo | It is the current LEDH row-status ledger | Contract E or P8p diagnostic reused as row score | Phase 1 row inventory | planned |
| LEDH production route is GPU/XLA/TF32 | `AGENTS.md` | Matches repository default for LEDH transport | CPU-only diagnostic used as production evidence | Trusted GPU probe before material score runs | planned |
| First score target is same-target LGSSM | Exact Kalman comparator exists | Smallest row with exact value and score | Contract E mistakenly substituted | Phase 2 target manifest | planned |
| Nonlinear rows require adapter admission first | Current leaderboard has blocked adapters | Prevents wrong-target score repair | Diagnostic route promoted to row route | Phase 5 adapter admission | planned |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in the execution
ledger and in chat for material phases.

Check:

- wrong baseline;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If the audit finds a material flaw, revise the plan or write a blocker note
before running the phase.

Current runbook audit: `PASS_TO_CLAUDE_REVIEW`.  This runbook is allowed to go
to Claude review.  It is not yet a score result.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites.
   - Restate the phase evidence contract.
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
   - Send material phase plans/results to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or patch and retry.
5. `REPAIR_LOOP`
   - Patch fixable blockers visibly.
   - Rerun focused checks.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Plain-Language Gate

Before accepting a phase result, blocker result, or final decision, Codex must
verify that the artifact:

- states the claimed target and computed quantity separately;
- uses direct classifications such as `correct`, `wrong relative to the stated
  target`, `unsupported`, `not checked`, or `heuristic only`;
- labels unsupported claims as `unsupported` or `not checked`;
- labels mismatches as `wrong relative to the stated target`;
- states what remains unproved or unevaluated.

## Claude Review Gate

Use `bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh`
for material review gates.  Use exact paths and compact review bundles.

Review command shape:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/chakwong/BayesFilter \
  --review-name ledh-score-repair-plan-review \
  --bundle /home/chakwong/BayesFilter/docs/reviews/bayesfilter-ledh-leaderboard-score-repair-plan-review-bundle-2026-07-03.md \
  --probe-timeout 90 \
  --timeout-seconds 180 \
  --max-retries 1 \
  --allow-bounded-fallback
```

This command requires trusted/escalated execution because Claude Code may need
network, auth, process, and workspace access outside the sandbox.

If the review hangs:

- run the small probe through the review gate or `claude_worker.sh`;
- if the probe works, reduce the bundle and retry with exact paths;
- if the probe fails, record reviewer unavailability and stop or ask the user.

## Human-Required Stop Conditions

Stop if continuing would require:

- changing pass/fail criteria after seeing results;
- new package installation or network data fetch;
- destructive git or filesystem action;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU results without trusted execution;
- continuing after five unresolved Claude review rounds for the same blocker.

## Final Visible Handoff

When execution completes or stops, write:

- latest phase reached;
- accepted rows and blocked rows;
- exact artifact paths;
- local checks and Claude review status;
- unresolved blockers;
- next smallest justified action.
