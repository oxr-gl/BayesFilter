# P53 Visible Gated Execution Runbook

Date: 2026-06-10

## Status

`RUNBOOK_AMENDMENT_REVIEW_CONVERGED`

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
- If Claude does not respond, Codex must run a minimal probe.  If the probe
  responds, Codex must treat the original prompt as the problem, split it, and
  retry a smaller read-only review.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p53-factorized-transition-repair-master-program-2026-06-10.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p53-claude-review-ledger-2026-06-10.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p53-visible-execution-ledger-2026-06-10.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p53-visible-stop-handoff-2026-06-10.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact | Required token |
| --- | --- | --- | --- | --- |
| P53-M0 | Planning Failure Lock And Prerequisite DAG | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m0-planning-failure-lock-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m0-planning-failure-lock-result-2026-06-10.md` | `PASS_P53_M0_PLANNING_FAILURE_LOCK` or `BLOCK_P53_M0_PLANNING_FAILURE_LOCK` |
| P53-M1 | Route Design, Math, And P30 Amendment | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m1-route-design-math-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m1-route-design-math-result-2026-06-10.md` | `PASS_P53_M1_ROUTE_DESIGN_MATH` or `BLOCK_P53_M1_ROUTE_DESIGN_MATH` |
| P53-M2 | Lower-Rung TensorFlow Route Implementation | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m2-route-implementation-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m2-route-implementation-result-2026-06-10.md` | `PASS_P53_M2_ROUTE_IMPLEMENTATION` or `BLOCK_P53_M2_ROUTE_IMPLEMENTATION` |
| P53-M3 | Lower-Rung Dense Tie-Out | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m3-lower-rung-dense-tieout-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m3-lower-rung-dense-tieout-result-2026-06-10.md` | `PASS_P53_M3_LOWER_RUNG_DENSE_TIEOUT` or `BLOCK_P53_M3_LOWER_RUNG_DENSE_TIEOUT` |
| P53-M4A | Scaling Route Choice And Derivation | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4a-scaling-route-choice-derivation-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4a-scaling-route-choice-derivation-result-2026-06-10.md` | `PASS_P53_M4A_SCALING_ROUTE_DERIVATION` or `BLOCK_P53_M4A_SCALING_ROUTE_DERIVATION` |
| P53-M4B | Scaling Route TensorFlow Implementation | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4b-scaling-route-implementation-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4b-scaling-route-implementation-result-2026-06-10.md` | `PASS_P53_M4B_SCALING_ROUTE_IMPLEMENTATION` or `BLOCK_P53_M4B_SCALING_ROUTE_IMPLEMENTATION` |
| P53-M4C | Scaling Route Lower-Rung Tie-Out | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4c-scaling-route-tieout-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4c-scaling-route-tieout-result-2026-06-10.md` | `PASS_P53_M4C_SCALING_ROUTE_TIEOUT` or `BLOCK_P53_M4C_SCALING_ROUTE_TIEOUT` |
| P53-M4D | Scaling Route Admission Gate | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4d-scaling-route-admission-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4d-scaling-route-admission-result-2026-06-10.md` | `PASS_P53_M4D_SCALING_ROUTE_ADMISSION` or `BLOCK_P53_M4D_SCALING_ROUTE_ADMISSION` |
| P53-M5 | Rank Selection Integration | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m5-rank-selection-integration-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m5-rank-selection-integration-result-2026-06-10.md` | `PASS_P53_M5_RANK_SELECTION_INTEGRATION` or `BLOCK_P53_M5_RANK_SELECTION_INTEGRATION` |
| P53-M6 | Spatial SIR d=18 Calibration Row | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m6-spatial-sir-d18-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m6-spatial-sir-d18-result-2026-06-10.md` | `PASS_P53_M6_SPATIAL_SIR_D18` or `BLOCK_P53_M6_SPATIAL_SIR_D18` |
| P53-M7 | Spatial SIR d=50/d=100 Scaling Policy | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m7-spatial-sir-d50-d100-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m7-spatial-sir-d50-d100-result-2026-06-10.md` | `PASS_P53_M7_SPATIAL_SIR_D50_D100` or `BLOCK_P53_M7_SPATIAL_SIR_D50_D100` |
| P53-M8 | Integration Closeout | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m8-integration-closeout-subplan-2026-06-10.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m8-integration-closeout-result-2026-06-10.md` | `PASS_P53_M8_INTEGRATION_CLOSEOUT` or `BLOCK_P53_M8_INTEGRATION_CLOSEOUT` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the corrected P53 program repair the P52 planning error, implement and validate lower-rung and scaling transition routes separately, and only then resume rank/scaling work? |
| Baseline/comparator | P52 stop handoff, P52-M4 blocker, current dense `filtering.py` route, lower-rung dense spatial SIR references, P30 notation, and P52 rank/UKF artifacts. |
| Primary pass criterion | Every phase either emits its required pass/block token with result artifacts and Claude read-only review, or stops with a human-required blocker after the repair loop.  P53-M5 through P53-M8 may not start until `PASS_P53_M4D_SCALING_ROUTE_ADMISSION` exists. |
| Veto diagnostics | Contract-only artifact treated as implementation; route design deferred to code; lower-rung dense tie-out skipped; streaming dense-equivalent route promoted to scaling route; dense all-pairs route used as production path; rank/scaling phases run before scaling-route gate; UKF promoted to truth; d=100 overclaimed. |
| Explanatory diagnostics | Static audits, focused CPU-only pytest, compile checks, dense lower-rung tie-outs, route metadata, memory forecasts, UKF scout manifests, gradient finite checks, deterministic replay, and Claude reviews. |
| Not concluded | No production HMC readiness, no exact d=50/d=100 posterior correctness, no GPU readiness, no S&P 500 reproduction, and no adaptive filtering path. |
| Artifacts | P53 visible execution ledger, phase results, manifests, implementation diffs, P30 amendment, Claude review ledger, stop handoff, and closeout. |

## Skeptical Plan Audit

Initial audit status: REVIEWED_BY_CODEX_AND_CLAUDE.

The explicit P53 repair for the P52 planning error is that route design,
lower-rung implementation, lower-rung tie-out, and a separately derived,
implemented, tied-out, and admitted scaling route are prerequisites for rank
selection and dimension scaling.  A contract-only artifact cannot pass an
implementation gate, and a streaming dense-equivalent route cannot pass the
scaling-route admission gate by itself.

After the first visible run reached `BLOCK_P53_M4_SCALING_ROUTE_GATE`, Codex
and the user identified a second planning error: P53-M4 had combined route
choice, mathematical derivation, implementation, tie-out, and admission into
one overloaded phase.  This amended runbook replaces that overloaded phase with
P53-M4A through P53-M4D.  The historical P53-M4 blocker remains evidence for
why the amended phase split is necessary, but it is not the active resume
target.

Claude Opus read-only review iteration 2 returned `VERDICT: AGREE`.  Claude
found the route-class loophole materially closed and the runbook safe to launch
visibly, with one nonblocking wording ambiguity about d=100 claim scope.  The
master program now uses dimension-specific claim classes for d=18/d=50/d=100.

Before executing any phase, Codex must check:

- wrong baselines;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites and dependency DAG.
   - Restate the phase evidence contract in chat and ledger.
2. `EXECUTE_MINIMAL`
   - Run only visible commands in the current conversation.
   - Prefer the smallest diagnostic or implementation needed.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against primary criterion and veto diagnostics.
   - Write or update the result artifact.
4. `PASS_REVIEW`
   - Send material phase results, repairs, implementation diffs, or final
     decisions to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, write a blocker plan.
   - Get Claude review when material.
   - Apply the repair visibly.
   - Rerun focused checks.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Continuation Rule

A clean phase boundary is not a stop condition.  After a phase passes focused
validation and Claude read-only review, Codex must immediately advance to the
next unpassed phase in this same visible supervisor/executor conversation.

Routine phase completion must update the execution ledger, but it must not be
recorded as a stop.  The stop handoff is reserved for true stop states:

- a human-required blocker from the stop-condition list;
- Claude/Codex non-convergence after five review rounds for the same blocker;
- a context or tool interruption that prevents safe continuation;
- an explicit user pause/stop request;
- a required approval that was not already anticipated in this runbook;
- final completion of P53-M8.

If no true stop state exists, the correct behavior is to continue the phase
index in order.  For amended P53 this means P53-M0 -> P53-M1 -> P53-M2 ->
P53-M3 -> P53-M4A -> P53-M4B -> P53-M4C -> P53-M4D -> P53-M5 -> P53-M6 ->
P53-M7 -> P53-M8, while preserving all prerequisite gates, especially the rule
that P53-M5 through P53-M8 cannot run until
`PASS_P53_M4D_SCALING_ROUTE_ADMISSION` exists.

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

## Anticipated Approvals

The user requested this execution and Claude review loop.  Smooth execution
anticipates these approvals:

1. Escalated/trusted Claude worker calls through
   `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh` with Opus
   and maximum available effort.
2. Escalated small Claude probes if a review prompt stalls.
3. CPU-only local validation commands, including focused `pytest`,
   `python -m compileall`, `git diff --check`, `rg`, and `sed`.  CPU-only
   scientific validation must set `CUDA_VISIBLE_DEVICES=-1` before framework
   import and record that CPU-only choice in the phase result.
4. Non-destructive file edits in the BayesFilter workspace using `apply_patch`.

No approval is requested in advance for package installation, network fetches,
GPU execution, detached/background supervisors, destructive git commands, or
modifying unrelated dirty work.

## Required Run Manifest Fields

Every material phase result must record:

- git commit or dirty-worktree note;
- exact command;
- environment or conda environment when known;
- CPU/GPU status, including `CUDA_VISIBLE_DEVICES=-1` for deliberate CPU-only
  runs;
- random seeds or `N/A`;
- wall time or `N/A` for static-only phases;
- output artifact paths;
- plan and result file paths;
- nonclaims.

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
