# BayesFilter Quadratic MAP-Covariance Initializer Visible Gated Execution Runbook

Date: 2026-07-08

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook is an overnight-capable visible runbook, not a detached launcher.
It must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

If detached overnight execution is later required, stop and write a separate
detached-supervisor plan.

## Quiet Visible Execution Pattern

Full stdout/stderr from long commands is an artifact, not chat content. For
commands expected to produce large output, predeclare a log path, redirect full
stdout/stderr to that log, and summarize only exit status, artifact paths,
pass/fail fields, and bounded failure tails.

## Program

Master program:

- `docs/plans/bayesfilter-quadratic-map-covariance-initializer-master-program-2026-07-08.md`

Reviewed plan artifacts:

- `docs/reviews/bayesfilter-quadratic-map-covariance-initializer-phase0-review-bundle-2026-07-08.md`

Execution ledger:

- `docs/plans/bayesfilter-quadratic-map-covariance-initializer-visible-execution-ledger-2026-07-08.md`

Stop handoff:

- `docs/plans/bayesfilter-quadratic-map-covariance-initializer-visible-stop-handoff-2026-07-08.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and API boundary | `docs/plans/bayesfilter-quadratic-map-covariance-initializer-phase0-governance-subplan-2026-07-08.md` | `docs/plans/bayesfilter-quadratic-map-covariance-initializer-phase0-governance-result-2026-07-08.md` |
| 1 | Reusable initializer implementation | `docs/plans/bayesfilter-quadratic-map-covariance-initializer-phase1-implementation-subplan-2026-07-08.md` | `docs/plans/bayesfilter-quadratic-map-covariance-initializer-phase1-implementation-result-2026-07-08.md` |
| 2 | Focused unit validation | `docs/plans/bayesfilter-quadratic-map-covariance-initializer-phase2-validation-subplan-2026-07-08.md` | `docs/plans/bayesfilter-quadratic-map-covariance-initializer-phase2-validation-result-2026-07-08.md` |
| 3 | Benchmark adoption smoke | `docs/plans/bayesfilter-quadratic-map-covariance-initializer-phase3-benchmark-smoke-subplan-2026-07-08.md` | `docs/plans/bayesfilter-quadratic-map-covariance-initializer-phase3-benchmark-smoke-result-2026-07-08.md` |
| 4 | Closeout and handoff | `docs/plans/bayesfilter-quadratic-map-covariance-initializer-phase4-closeout-subplan-2026-07-08.md` | `docs/plans/bayesfilter-quadratic-map-covariance-initializer-phase4-closeout-result-2026-07-08.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter gain a reusable diagnostic initializer where a local optimizer finds a neighborhood and constrained SPD quadratic geometry provides the covariance candidate? |
| Baseline/comparator | Current benchmark-local helpers and existing reusable `fit_low_rank_spd_quadratic_geometry` plus `mass_matrix.py` regularization helpers. |
| Primary pass criterion | Focused tests pass for controlled targets, fail-closed cases, payload nonclaims, and public exports; result artifacts preserve boundaries. |
| Veto diagnostics | Nonfinite accepted covariance, non-SPD accepted precision, sign convention failure, insufficient sample guard failure, BFGS curvature used as covariance authority, unsupported MAP/HMC claim, or review nonconvergence. |
| Explanatory diagnostics | Locator status, finite sample count, fit/holdout residuals, eigen summaries, condition number, trust-region displacement, gradient norm, and benchmark smoke metadata. |
| Not concluded | Global MAP, true posterior covariance, HMC readiness, sampler convergence, statistical superiority, default readiness, or Zhao-Cui source faithfulness. |
| Artifacts | Master program, phase subplans/results, review bundles, logs under `docs/plans/artifacts/bayesfilter-quadratic-map-covariance-initializer-2026-07-08/`, source/tests diff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Reusable API in `bayesfilter/inference` | Existing geometry and mass-matrix APIs live there | Keeps initializer with inference utilities | Public surface grows before tests | Phase 1/2 export tests | hypothesis until tested |
| BFGS locator optional/fallback | User directive and current benchmark helper pattern | Good local center can improve design cloud | Optimizer failure blocks useful covariance fit | Locator result must be non-authoritative and fallback-capable | reviewed |
| Quadratic SPD fit as covariance authority | Existing `fit_low_rank_spd_quadratic_geometry` | Produces explicit precision with SPD/condition diagnostics | Fit residuals poor or mode outside trust region | Holdout/trust/eigen gates | reviewed |
| CPU-safe focused tests | BayesFilter policy allows small smoke/debug CPU checks | No GPU/HMC evidence needed for reusable API unit correctness | Mistaken production-readiness claim | Nonclaims in result notes | reviewed |
| Claude review gate | User instruction and local guide | Provides bounded external read-only review | Timeout/no-verdict treated as correctness | Gate status recorded; fallback labeled weaker | reviewed |

## Skeptical Plan Audit

Before executing each phase, Codex must record a skeptical audit in chat and in
the ledger for material phases.

Check:

- wrong baselines;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

Initial audit status: `PASSED_FOR_PHASE_0_REVIEW`.

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
   - For fixable blockers, patch visibly, rerun focused checks, and preserve
     repair evidence.
   - Stop after five review rounds for the same blocker.
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

## Claude Read-Only Review Template

Use Claude only as a reviewer. The prompt must say:

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
- artifact mismatch;
- evasive scientific language;
- unsupported soft terms;
- mismatch between stated target and computed quantity without a direct verdict.

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
- package installation, network fetch, credentials, or environment setup outside
  the Claude review call;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- continuing after Claude and Codex do not converge after five review rounds.
