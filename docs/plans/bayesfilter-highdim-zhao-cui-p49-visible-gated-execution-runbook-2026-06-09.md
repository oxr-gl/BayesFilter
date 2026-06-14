# P49 Visible Gated Execution Runbook

Date: 2026-06-09

## Status

`PLAN_REVIEW_CONVERGED_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

This is an overnight-style gated plan, but execution remains visible and
recoverable in the current Codex conversation.  If the user requests detached
execution, stop and write a separate detached-supervisor plan.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p49-source-faithful-repair-master-program-2026-06-09.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p49-claude-review-ledger-2026-06-09.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p49-visible-execution-ledger-2026-06-09.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p49-visible-stop-handoff-2026-06-09.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact | Required pass/block token |
| --- | --- | --- | --- | --- |
| M0 | Route-Claim Governance | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m0-route-claim-governance-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m0-route-claim-governance-result-2026-06-09.md` | `PASS_P49_M0_ROUTE_CLAIM_GOVERNANCE` or `BLOCK_P49_M0_ROUTE_CLAIM_GOVERNANCE` |
| M1 | Source Route Contract | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m1-source-route-contract-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m1-source-route-contract-result-2026-06-09.md` | `PASS_P49_M1_SOURCE_ROUTE_CONTRACT` or `BLOCK_P49_M1_SOURCE_ROUTE_CONTRACT` |
| M2 | Retained TT/SIRT Object Skeleton | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m2-retained-transport-object-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m2-retained-transport-object-result-2026-06-09.md` | `PASS_P49_M2_RETAINED_TRANSPORT_OBJECT` or `BLOCK_P49_M2_RETAINED_TRANSPORT_OBJECT` |
| M3 | Sample Propagation, ESS, And Proposal Correction | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m3-sample-ess-proposal-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m3-sample-ess-proposal-result-2026-06-09.md` | `PASS_P49_M3_SAMPLE_ESS_PROPOSAL` or `BLOCK_P49_M3_SAMPLE_ESS_PROPOSAL` |
| M4 | Recentring, Jacobian, And Normalizer Accounting | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m4-recentering-normalizer-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m4-recentering-normalizer-result-2026-06-09.md` | `PASS_P49_M4_RECENTERING_NORMALIZER` or `BLOCK_P49_M4_RECENTERING_NORMALIZER` |
| M5 | Preconditioned Predator-Prey Repair | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m5-preconditioned-predator-prey-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m5-preconditioned-predator-prey-result-2026-06-09.md` | `PASS_P49_M5_PRECONDITIONED_PREDATOR_PREY` or `BLOCK_P49_M5_PRECONDITIONED_PREDATOR_PREY` |
| M6 | Smoothing Boundary And Backward Conditionals | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m6-smoothing-boundary-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m6-smoothing-boundary-result-2026-06-09.md` | `PASS_P49_M6_SMOOTHING_BOUNDARY` or `BLOCK_P49_M6_SMOOTHING_BOUNDARY` |
| M7 | Deterministic Gradient-Lane Contract | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m7-gradient-lane-boundary-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m7-gradient-lane-boundary-result-2026-06-09.md` | `PASS_P49_M7_GRADIENT_LANE_BOUNDARY` or `BLOCK_P49_M7_GRADIENT_LANE_BOUNDARY` |
| M8 | Integration Closeout | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m8-integration-closeout-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p49-m8-integration-closeout-result-2026-06-09.md` | `PASS_P49_M8_INTEGRATION_CLOSEOUT` or `BLOCK_P49_M8_INTEGRATION_CLOSEOUT` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can P49 repair the eight P48 route-fidelity errors without conflating source-faithful filtering and gradient-bearing adaptation? |
| Baseline/comparator | P48 discrepancy ledger, Zhao--Cui source snapshots, exact/dense/Kalman/CUT4 references, and current BayesFilter fixed branch. |
| Primary pass criterion | All phases either pass their gate with result artifacts, required pass/block token, and Claude review, or stop with a human-required blocker and handoff. |
| Veto diagnostics | Wrong baseline; proxy promotion; missing stop condition; unfair comparison; hidden assumption; stale context; environment mismatch; unsupported claim; artifact mismatch. |
| Explanatory diagnostics | Unit tests, static audits, preflight complexity checks, small numerical smoke tests, branch replay, likelihood/gradient calibration. |
| Not concluded | No source-faithful completion, HMC readiness, production SIR/predator-prey readiness, S&P 500 reproduction, or adaptive-route differentiability unless the corresponding phase explicitly passes. |
| Artifacts | P49 phase results, review ledger, execution ledger, stop handoff, local command outputs summarized in artifacts. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Codex is visible supervisor/executor | User instruction and template | Keeps execution recoverable and inspectable. | Detached agent hides state or cannot recover. | No detached commands in runbook. | Reviewed hypothesis |
| Claude is read-only reviewer | User instruction and template | Provides independent critique without uncontrolled edits. | Claude modifies files or launches work. | Prompts say read-only; Codex inspects artifacts after review. | Reviewed hypothesis |
| TF/TFP backend for BayesFilter code | AGENTS.md | Project default for differentiable implementation. | NumPy prototype promoted to implementation. | Static backend check in implementation phases. | Project policy |
| CPU-only unless explicit GPU approval | AGENTS.md | Avoids sandbox GPU ambiguity. | Non-escalated GPU errors misread. | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`. | Project policy |
| Source snapshots are audit references | P10/P34/P48 | License/runtime boundary prevents copying. | MATLAB code copied or source smoke treated as production. | License boundary row in every implementation phase. | Reviewed |
| Repair loop continues for fixable issues | User instruction | Avoids stopping for no valid reason. | Infinite churn or criterion drift. | Five Claude-review-round limit per blocker. | Required |

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

If the audit finds a material flaw, revise the phase plan or write a blocker
note before running the phase.

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
   - The result artifact must emit exactly one required pass or block token
     from the phase index.
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
   - Advance only after the current phase gate passes, the required phase
     pass token appears in the result artifact, and Claude returns
     `VERDICT: AGREE`.
   - If a block token appears, enter `REPAIR_LOOP` for fixable blockers or
     write the visible stop handoff for human-required blockers.
   - Stop and write the handoff if a human-required blocker appears.

## Invalid Stop Reasons

Codex must not stop merely because:

- a test failed but the failure is local and fixable;
- Claude requested a concrete revision;
- a result artifact needs metadata or wording repair;
- a command selected the wrong test subset;
- an unrelated dirty worktree file exists;
- a first Claude prompt stalls but a narrower read-only prompt can be tried.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default backend or numerical policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- continuing after Claude and Codex do not converge after five review rounds.

## Claude Read-Only Review Template

Use Claude only as reviewer.  The prompt must say:

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

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

## Anticipated Approval Requests

For smooth continuous execution of the whole P49 program, ask the user to
approve:

1. Direct escalated `claude -p` read-only review prompts for the master plan,
   each material phase, blocker repair plans, and closeout.
2. CPU-only local validation commands:
   - `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m json.tool ...`
   - `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q ...`
   - `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q <focused tests>`
3. Static inspection commands such as `rg`, `sed`, `git diff --check`, and
   `git status`.

No anticipated approval is requested for:

- network fetches;
- package installation;
- GPU tests;
- detached execution;
- destructive git commands.

If any of those become necessary, Codex must stop and ask for a separate
approval.

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
