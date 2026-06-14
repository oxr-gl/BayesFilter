# P60 Visible Gated Execution Runbook

Date: 2026-06-12

## Status

`VISIBLE_EXECUTION_RUNBOOK_READY_TO_LAUNCH`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Code Opus max-effort is a read-only reviewer only.

This runbook must not launch a detached or nested agent.  Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

Execution stays visible and recoverable in the current conversation.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p60-rank-convergence-and-correctness-bridge-master-program-2026-06-12.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p60-plan-claude-review-ledger-2026-06-12.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p60-visible-execution-ledger-2026-06-12.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p60-visible-stop-handoff-2026-06-12.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P60-1 | Source Rank Knobs And Comparator Contract | `docs/plans/bayesfilter-highdim-zhao-cui-p60-1-source-rank-knobs-and-comparator-contract-subplan-2026-06-12.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p60-1-source-rank-knobs-and-comparator-contract-result-2026-06-12.md` |
| P60-2 | Same-Route Higher-Rank Comparator | `docs/plans/bayesfilter-highdim-zhao-cui-p60-2-same-route-higher-rank-comparator-subplan-2026-06-12.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p60-2-same-route-higher-rank-comparator-result-2026-06-12.md` |
| P60-3 | Same-Target Reference Or Bridge | `docs/plans/bayesfilter-highdim-zhao-cui-p60-3-same-target-reference-bridge-subplan-2026-06-12.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p60-3-same-target-reference-bridge-result-2026-06-12.md` |
| P60-4 | Validation Ladder Promotion Integration | `docs/plans/bayesfilter-highdim-zhao-cui-p60-4-validation-ladder-promotion-integration-subplan-2026-06-12.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p60-4-validation-ladder-promotion-integration-result-2026-06-12.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the author-SIR d=18 source-route implementation move from P59 execution-only evidence to rank-stable and then correctness-candidate evidence without drifting from Zhao-Cui `full_sol`? |
| Baseline/comparator | P59-9e execution-only result, Zhao-Cui `eg3_sir/mainscript.m`, Zhao-Cui `models/full_sol.m`, and a strictly stronger same-route fixed-TT/SIRT comparator. |
| Primary pass criterion | P60-1 through P60-4 pass in order.  Rank convergence requires P60-2.  Correctness-candidate status requires P60-2, P60-3, and P60-4. |
| Veto diagnostics | Source-route drift, nonempty theta block for the `d=0` author row, 18D target instead of realized 36D `[x_t, x_{t-1}]`, old all-grid/local route, UKF/memory/finite-value correctness proxy, missing rank comparator, missing reference/bridge, nonfinite diagnostics, memory breach, or post-hoc tolerance widening. |
| Explanatory diagnostics | Runtime, memory, ESS, correction-log-weight ranges, normalizer increments, probe-density deltas, lower-rung dense residuals, UKF scout summaries, and wall time. |
| Not concluded | P60 does not launch d=50/d=100, prove exact correctness, prove HMC production readiness, or reproduce adaptive Zhao-Cui parity. |
| Artifacts | P60 phase result files, manifests, tests, Claude review ledgers, this visible execution ledger, and stop handoff if needed. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Realized route is `[x_t, x_{t-1}]` | Zhao-Cui SIR has `d=0`, `m=18`; `full_sol` generic dimension is `d + 2m` | Prevents fake nonempty theta-block claims | Wrong 36D coordinate contract | P60-1 source audit | Reviewed by Claude |
| Same-route rank convergence before correctness | P59-9e nonclaims and P60 evidence ladder | Separates approximation stability from target correctness | Rank stability overclaimed as correctness | P60-2/P60-4 gates | Reviewed by Claude |
| Reference/bridge required for correctness | P60 master and P60-3 | Prevents proxy correctness claims | No same-target evidence | P60-3 gate | Reviewed by Claude |
| UKF is diagnostic-only | Prior governance and P60 plan | UKF can guide but not certify TT/SIRT correctness | Proxy metric promoted | P60-3/P60-4 tests | Reviewed by Claude |
| CPU-only visible diagnostics unless GPU is explicitly needed | AGENTS.md GPU policy | P60 planning/contract phases do not require GPU | Sandbox GPU false negatives | `CUDA_VISIBLE_DEVICES=-1` for CPU-only runs | Baseline |

## Skeptical Plan Audit

Status: `PASS_VISIBLE_LAUNCH_AFTER_CLAUDE_REVIEW`.

- Wrong-baseline risk: mitigated by using P59-9e plus Zhao-Cui `full_sol` as
  the baseline.
- Proxy-risk: UKF, memory, finite values, and wall time cannot promote
  correctness.
- Missing-stop risk: P60-2 cannot run before P60-1; P60-4 cannot pass before
  P60-2 and P60-3.
- Unfair-comparison risk: same-route comparator must preserve target,
  observations, route ordering, previous-marginal semantics, and correction
  formula.
- Hidden-assumption risk: fixed-HMC choices must be labeled as fixed-variant
  choices, not author-code facts.
- Stale-context risk: P59-9e is execution-only, not rank or correctness
  evidence.
- Environment mismatch risk: GPU/CUDA commands require escalation; CPU-only
  runs must record the choice.
- Artifact-risk: each phase has an explicit required result artifact and
  pass/block token.

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
- artifact mismatch.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

If Claude does not respond, Codex must run the minimal probe
`READ-ONLY PROBE. Reply with exactly: PROBE_OK`.  If the probe succeeds, Codex
must shorten or redesign the review prompt.

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

## Initial Launch Token

`RUNBOOK_P60_VISIBLE_GATED_EXECUTION_READY`
