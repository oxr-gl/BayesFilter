# P50 Visible Gated Execution Runbook

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
recoverable in the current Codex conversation.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p50-hmc-deterministic-filtering-master-program-2026-06-09.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p50-claude-review-ledger-2026-06-09.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p50-visible-execution-ledger-2026-06-09.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p50-visible-stop-handoff-2026-06-09.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact | Required pass/block token |
| --- | --- | --- | --- | --- |
| M0 | Scope And Claim Governance | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m0-scope-claim-governance-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m0-scope-claim-governance-result-2026-06-09.md` | `PASS_P50_M0_SCOPE_CLAIM_GOVERNANCE` or `BLOCK_P50_M0_SCOPE_CLAIM_GOVERNANCE` |
| M1 | Deterministic Filter Loop Contract | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m1-deterministic-filter-loop-contract-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m1-deterministic-filter-loop-contract-result-2026-06-09.md` | `PASS_P50_M1_DETERMINISTIC_FILTER_LOOP_CONTRACT` or `BLOCK_P50_M1_DETERMINISTIC_FILTER_LOOP_CONTRACT` |
| M2 | One-Step Value Path Implementation | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m2-one-step-value-path-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m2-one-step-value-path-result-2026-06-09.md` | `PASS_P50_M2_ONE_STEP_VALUE_PATH` or `BLOCK_P50_M2_ONE_STEP_VALUE_PATH` |
| M3 | Sequential Likelihood Path | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m3-sequential-likelihood-path-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m3-sequential-likelihood-path-result-2026-06-09.md` | `PASS_P50_M3_SEQUENTIAL_LIKELIHOOD_PATH` or `BLOCK_P50_M3_SEQUENTIAL_LIKELIHOOD_PATH` |
| M4 | Value And Gradient Calibration Rules | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m4-value-gradient-calibration-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m4-value-gradient-calibration-result-2026-06-09.md` | `PASS_P50_M4_VALUE_GRADIENT_CALIBRATION` or `BLOCK_P50_M4_VALUE_GRADIENT_CALIBRATION` |
| M5 | SV And Generalized SV Model Ladder | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m5-sv-generalized-sv-ladder-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m5-sv-generalized-sv-ladder-result-2026-06-09.md` | `PASS_P50_M5_SV_GENERALIZED_SV_LADDER` or `BLOCK_P50_M5_SV_GENERALIZED_SV_LADDER` |
| M6 | Spatial SIR And Predator-Prey Ladder | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m6-spatial-sir-predator-prey-ladder-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m6-spatial-sir-predator-prey-ladder-result-2026-06-09.md` | `PASS_P50_M6_SPATIAL_SIR_PREDATOR_PREY_LADDER` or `BLOCK_P50_M6_SPATIAL_SIR_PREDATOR_PREY_LADDER` |
| M7 | HMC Readiness Tiers | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m7-hmc-readiness-tiers-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m7-hmc-readiness-tiers-result-2026-06-09.md` | `PASS_P50_M7_HMC_READINESS_TIERS` or `BLOCK_P50_M7_HMC_READINESS_TIERS` |
| M8 | Smoothing Boundary Or Latent-Path Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m8-smoothing-boundary-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m8-smoothing-boundary-result-2026-06-09.md` | `PASS_P50_M8_SMOOTHING_BOUNDARY` or `BLOCK_P50_M8_SMOOTHING_BOUNDARY` |
| M9 | Integration Closeout | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m9-integration-closeout-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p50-m9-integration-closeout-result-2026-06-09.md` | `PASS_P50_M9_INTEGRATION_CLOSEOUT` or `BLOCK_P50_M9_INTEGRATION_CLOSEOUT` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can P50 execute the remaining HMC-compatible deterministic filtering work without reviving non-gradient adaptive filtering or S&P reproduction as gaps? |
| Baseline/comparator | P49 closeout and helper contracts, exact/dense/Kalman/CUT4 references, existing deterministic BayesFilter branch, and model-specific diagnostics. |
| Primary pass criterion | All phases either pass their gate with result artifacts, required pass/block token, and Claude review, or stop with a human-required blocker and handoff. |
| Veto diagnostics | Adaptive source filtering or S&P reproduction treated as required; proxy promotion; value-only promotion to gradient correctness; HMC readiness without tier evidence; missing stop condition; unsupported model production claim. |
| Explanatory diagnostics | Unit tests, compile checks, static audits, low-dimensional reference comparisons, likelihood-variability calibration, directional-gradient diagnostics, and short HMC smoke diagnostics. |
| Not concluded | No HMC readiness, production model readiness, smoothing support, or full deterministic filter completion unless the corresponding phase explicitly passes. |
| Artifacts | P50 phase results, review ledger, execution ledger, final handoff, and local command outputs summarized in artifacts. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Codex is visible supervisor/executor | User instruction and template | Keeps execution recoverable and inspectable. | Detached agent hides state. | No detached commands in runbook. | Required |
| Claude is read-only reviewer | User instruction and template | Provides independent critique without uncontrolled edits. | Claude edits files or launches work. | Prompts say read-only; Codex inspects diff/status. | Required |
| Adaptive TT/SIRT filtering is a non-goal | User correction on 2026-06-09 | It is not naturally gradient-bearing for HMC. | Treating non-goal as blocker wastes execution. | M0 claim governance search. | Project direction |
| S&P reproduction is a non-goal | User correction on 2026-06-09 | It is not a target deliverable. | Treating non-goal as blocker distorts scope. | M0 claim governance search. | Project direction |
| TF/TFP backend for implementation | AGENTS.md | Project default for differentiable implementation. | NumPy prototype promoted to implementation. | Static backend checks in implementation phases. | Project policy |
| CPU-only unless explicit GPU approval | AGENTS.md | Avoids sandbox GPU ambiguity. | GPU claims from blocked sandbox. | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`. | Project policy |
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
   - Advance only after the current phase gate passes, the required phase pass
     token appears in the result artifact, and Claude returns
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

For smooth continuous execution of the whole P50 program, ask the user to
approve:

1. Escalated `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh`
   read-only review prompts for the master plan, each material phase, blocker
   repair plans, and closeout.
2. CPU-only local validation commands:
   - `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q ...`
   - `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q <focused tests>`
3. Static inspection commands such as `rg`, `sed`, `git diff --check`, and
   `git status`.

No anticipated approval is requested for network fetches, package
installation, GPU tests, detached execution, or destructive git commands.  If
any of those become necessary, Codex must stop and ask for separate approval.

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
