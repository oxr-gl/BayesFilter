# P8j Visible Gated Execution Runbook

Date: 2026-06-17

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent.  Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

If the user wants detached overnight execution, stop and write a separate
detached-supervisor plan.  This runbook is for visible, recoverable execution
inside the current conversation.

## Program

Master program:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-claude-review-ledger-2026-06-17.md`

Execution ledger:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md`

Stop handoff:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-stop-handoff-2026-06-17.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and current evidence audit | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase0-governance-current-evidence-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase0-governance-current-evidence-result-2026-06-17.md` |
| 1 | SIR d18 DPF callback contract | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase1-sir-d18-dpf-callback-contract-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase1-sir-d18-dpf-callback-contract-result-2026-06-17.md` |
| 2 | Bootstrap DPF SIR smoke implementation | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-result-2026-06-17.md` |
| 3 | Algorithm 1 UKF LEDH SIR smoke | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase3-ledh-alg1-sir-smoke-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase3-ledh-alg1-sir-smoke-result-2026-06-17.md` |
| 4 | OT-resampled LEDH-PFPF-OT SIR smoke | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase4-ot-ledh-sir-smoke-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase4-ot-ledh-sir-smoke-result-2026-06-17.md` |
| 5 | SIR d18 particle-count tuning | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-result-2026-06-17.md` |
| 6 | SIR d18 leaderboard refresh | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase6-sir-leaderboard-refresh-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase6-sir-leaderboard-refresh-result-2026-06-17.md` |
| 7 | Closeout, artifact index, and repo boundary | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase7-closeout-boundary-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase7-closeout-boundary-result-2026-06-17.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter complete the missing DPF leaderboard cells for Zhao-Cui spatial SIR d18 with reviewed callback, smoke, tuning, and artifact gates? |
| Baseline/comparator | P8d reset memo, current P8d runner route table and route tests, P8 source-paper scope and adapter matrices, deterministic SIR value-only route, and existing DPF callbacks for non-SIR rows.  P8g/P8h/P8i are historical non-SIR DPF/LEDH/OT provenance only. |
| Primary pass criterion | Each phase passes its declared gate with artifacts and review, or writes a blocker preserving exact SIR d18 DPF boundary state.  Phase 6 leaderboard refresh may pass only with the Phase 5-reviewed selected SIR d18 particle count plus five fixed seeds; five seeds are necessary but not sufficient. |
| Veto diagnostics | Wrong lane/P71 drift; fabricated SIR DPF callback; P8h actual-SV evidence treated as SIR evidence; fewer than five DPF seeds for value evidence; GPU outside trusted context; score/Hessian/theta-gradient/HMC claim for fixed-parameter SIR; source-faithful TT/SIRT claim from DPF evidence. |
| Explanatory diagnostics | ESS, MC SE, runtime, per-seed log likelihood, transport residuals, covariance carry diagnostics, finite flags, source/adapter search hits. |
| Not concluded | Zhao-Cui TT/SIRT parity, exact nonlinear likelihood correctness, stochastic PF marginal-gradient correctness, theta-gradient correctness, posterior convergence, HMC/NUTS readiness, production readiness, or final default ranking. |
| Artifacts | P8j master program, subplans/results, execution ledger, Claude review ledger, stop handoff, and any JSON/CSV leaderboard outputs. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Treat SIR d18 row as fixed-parameter/no-free-theta | P8 source-paper scope and current P8d tests | Prevents score/Hessian/HMC overclaim | Accidental parameterized target claim | Phase 0 route/test audit | baseline |
| Require five fixed DPF seeds for value evidence | P8d/P8h DPF contracts | Preserves MC uncertainty accounting; necessary but not sufficient for leaderboard completion | One-seed smoke or untuned particle count promoted to leaderboard | Phase 1 contract and Phase 5 tuning checks | baseline |
| Use P8h OT covariance-carry route for serious LEDH SIR route | P8h reviewed design contract | Keeps DPF route aligned with repaired serious candidate | SIR adapter exposes shape/numerical failure | Phase 4 smoke diagnostics | hypothesis |
| Start with bootstrap DPF before LEDH/OT | Engineering risk ladder | Separates target callback errors from LEDH/OT errors | Bootstrap pass could be overread as LEDH pass | Phase 2 nonclaims and Phase 3 handoff | reviewed-after-Phase0 |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and,
for material phases, in the execution ledger.

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

Codex must preserve the review artifact and inspect whether Claude actually
remained read-only.

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
