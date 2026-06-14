# P51 Visible Gated Execution Runbook

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

- `docs/plans/bayesfilter-highdim-zhao-cui-p51-gap-closure-master-program-2026-06-09.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p51-claude-review-ledger-2026-06-09.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p51-visible-execution-ledger-2026-06-09.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p51-visible-stop-handoff-2026-06-09.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact | Required manifest artifact | Required pass/block token |
| --- | --- | --- | --- | --- | --- |
| M0 | Gap Scope And Preflight Governance | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m0-gap-scope-preflight-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m0-gap-scope-preflight-result-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m0-gap-scope-preflight-manifest-2026-06-09.json` | `PASS_P51_M0_GAP_SCOPE_PREFLIGHT` or `BLOCK_P51_M0_GAP_SCOPE_PREFLIGHT` |
| M1 | Stable Score API Contract And Top-Level Gap Split | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m1-stable-score-api-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m1-stable-score-api-result-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m1-stable-score-api-manifest-2026-06-09.json` | `PASS_P51_M1_STABLE_SCORE_API` or `BLOCK_P51_M1_STABLE_SCORE_API` |
| M2 | Native Generalized SV Reference | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-result-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-manifest-2026-06-09.json` | `PASS_P51_M2_NATIVE_GENERALIZED_SV_REFERENCE` or `BLOCK_P51_M2_NATIVE_GENERALIZED_SV_REFERENCE` |
| M3 | Spatial SIR Production Route Architecture | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m3-spatial-sir-production-route-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m3-spatial-sir-production-route-result-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m3-spatial-sir-production-route-manifest-2026-06-09.json` | `PASS_P51_M3_SPATIAL_SIR_ROUTE_PREFLIGHT` or `BLOCK_P51_M3_SPATIAL_SIR_ROUTE_PREFLIGHT` |
| M4 | Predator-Prey Production Accuracy Tuning | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m4-predator-prey-production-tuning-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m4-predator-prey-production-tuning-result-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m4-predator-prey-production-tuning-manifest-2026-06-09.json` | `PASS_P51_M4_PREDATOR_PREY_PRODUCTION_TUNING` or `BLOCK_P51_M4_PREDATOR_PREY_PRODUCTION_TUNING` |
| M5 | HMC Tier 2 Leapfrog Diagnostics | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m5-hmc-tier2-leapfrog-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m5-hmc-tier2-leapfrog-result-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m5-hmc-tier2-leapfrog-manifest-2026-06-09.json` | `PASS_P51_M5_HMC_TIER2_LEAPFROG` or `BLOCK_P51_M5_HMC_TIER2_LEAPFROG` |
| M6 | HMC Tier 3 Short-Chain Diagnostics | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m6-hmc-tier3-short-chain-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m6-hmc-tier3-short-chain-result-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m6-hmc-tier3-short-chain-manifest-2026-06-09.json` | `PASS_P51_M6_HMC_TIER3_SHORT_CHAIN` or `BLOCK_P51_M6_HMC_TIER3_SHORT_CHAIN` |
| M7 | Smoothing Future-Target Decision | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m7-smoothing-future-target-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m7-smoothing-future-target-result-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m7-smoothing-future-target-manifest-2026-06-09.json` | `PASS_P51_M7_SMOOTHING_FUTURE_TARGET` or `BLOCK_P51_M7_SMOOTHING_FUTURE_TARGET` |
| M8 | Integration Closeout | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m8-integration-closeout-subplan-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m8-integration-closeout-result-2026-06-09.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p51-m8-integration-closeout-manifest-2026-06-09.json` | `PASS_P51_M8_INTEGRATION_CLOSEOUT` or `BLOCK_P51_M8_INTEGRATION_CLOSEOUT` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the actionable P50 remaining gaps be closed or narrowed under visible gated execution without reviving non-goals or overclaiming readiness? |
| Baseline/comparator | P50 M9 closeout, P50 M4 calibration rules, P50 HMC tier manifest, P50 smoothing boundary, existing model references, and current TensorFlow/TFP deterministic paths. |
| Primary pass criterion | All phases either pass with result artifacts, required token, and Claude review, or stop with a human-required blocker and handoff. |
| Veto diagnostics | Non-goals treated as gaps; proxy promotion; HMC readiness without Tier 2/3 evidence; production readiness from diagnostics; native generalized SV proxy treated as same-target; smoothing support without backward-conditionals. |
| Explanatory diagnostics | Unit tests, compile checks, static audits, dense references, route preflights, tuning ladders, leapfrog diagnostics, and short-chain diagnostics. |
| Not concluded | No production HMC readiness, production model readiness, root-level public API stability, or smoothing support unless the corresponding phase explicitly passes. |
| Artifacts | P51 phase results, review ledger, execution ledger, final handoff, tests/manifests, and local command outputs summarized in artifacts. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Codex is visible supervisor/executor | User instruction and claudecodex template | Keeps state recoverable and inspectable. | Detached execution hides failures. | No detached commands in runbook. | Required |
| Claude is read-only reviewer | User instruction | Independent critique without uncontrolled edits. | Claude edits or runs experiments. | Prompts say read-only; Codex inspects diffs/status. | Required |
| Adaptive TT/SIRT and S&P reproduction are non-goals | P50 M9 closeout | Avoids reviving already-removed gaps. | Scope drift. | M0 static governance audit. | Required |
| TF/TFP backend for implementation | AGENTS.md | Project default for differentiable algorithmic code. | NumPy prototype becomes implementation. | M0/M1 backend audit. | Required |
| CPU-only unless explicit GPU approval | AGENTS.md | Avoids sandbox GPU ambiguity. | GPU claims from untrusted context. | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`. | Required |
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
- a result artifact needs metadata, route labels, commands, tokens, or wording;
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

Use Claude only as reviewer. The prompt must say:

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

For smooth continuous execution of the whole P51 program, ask the user to
approve:

1. Escalated `claude -p` read-only review prompts for the master plan, each
   material phase, blocker repair plans, and closeout.
2. CPU-only local validation commands:
   - `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q ...`
   - `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q <focused tests>`
3. Narrow, reviewed, non-destructive CPU-only Python diagnostic scripts or
   modules created by P51 phases, with exact paths recorded before execution.
4. Static inspection commands such as `rg`, `sed`, `git diff --check`, and
   `git status`.

No anticipated approval is requested for network fetches, package
installation, GPU tests, detached execution, or destructive git commands. If
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
- safest next action.
