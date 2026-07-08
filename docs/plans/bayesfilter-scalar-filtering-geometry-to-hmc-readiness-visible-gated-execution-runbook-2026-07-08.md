# Scalar Filtering Geometry To HMC Readiness Visible Gated Execution Runbook

Date: 2026-07-08
Status: `DRAFT_VISIBLE_EXECUTION_RUNBOOK_READY_FOR_PHASE0_REVIEW`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only. Claude must not edit files, run mutating commands, launch agents, approve boundary crossings, or act as execution authority.

This is a visible, recoverable runbook inside the current conversation. It must not launch detached or nested execution. Do not use `codex exec`, `overnight_gated_launch.sh`, `setsid`, `nohup`, detached `tmux`, background phase runners, or copied-workspace execution.

## Program

Master program:

- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md`

Execution ledger:

- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-visible-execution-ledger-2026-07-08.md`

Stop handoff:

- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-visible-stop-handoff-2026-07-08.md`

Phase 0 review bundle:

- `docs/reviews/scalar-filtering-geometry-hmc-phase0-review-bundle-2026-07-08.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and review gate | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase0-governance-subplan-2026-07-08.md` | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase0-governance-result-2026-07-08.md` |
| 1 | Scalar filtering-likelihood geometry target | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-filtering-geometry-subplan-2026-07-08.md` | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-filtering-geometry-result-2026-07-08.md` |
| 2 | Geometry-to-mass handoff | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase2-mass-handoff-subplan-2026-07-08.md` | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase2-mass-handoff-result-2026-07-08.md` |
| 3 | HMC mechanics canary | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase3-mechanics-canary-subplan-2026-07-08.md` | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase3-mechanics-canary-result-2026-07-08.md` |
| 4 | Short HMC smoke | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase4-short-hmc-smoke-subplan-2026-07-08.md` | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase4-short-hmc-smoke-result-2026-07-08.md` |
| 5 | Replicated scalar HMC diagnostic | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase5-replicated-scalar-hmc-subplan-2026-07-08.md` | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase5-replicated-scalar-hmc-result-2026-07-08.md` |
| 6 | Closeout and next-dimensional handoff | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase6-closeout-subplan-2026-07-08.md` | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase6-closeout-result-2026-07-08.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the scalar filtering-likelihood SSL-LSTM target pass geometry, mass, and short HMC mechanics readiness gates after the complete-data oracle geometry pass? |
| Baseline/comparator | Passed identifiable complete-data oracle geometry result and current TensorFlow/TFP filtering score helpers. |
| Primary pass criterion | Every phase writes the required artifact and passes hard validity checks for that phase without unsupported claims. |
| Veto diagnostics | Nonfinite accepted quantity, non-SPD or over-conditioned accepted matrix, coordinate mismatch, failed tests, invalid artifact, unresolved review `REVISE`, hidden default/scientific claim. |
| Explanatory diagnostics | Residuals, score norm, eigen summaries, `L * epsilon`, acceptance, ESS/R-hat, runtime, and finite sample ratios unless a phase explicitly classifies one as a hard check. |
| Not concluded | Posterior correctness, HMC convergence, zero divergences, sampler superiority, default readiness, GPU/XLA production readiness, package readiness, public API readiness, or Zhao-Cui source-faithfulness. |
| Artifacts | Master/runbook/ledger/stop handoff, phase subplans/results, review bundles/status, benchmark JSON/Markdown/log artifacts. |

## Quiet Visible Execution Pattern

Commands that may produce large stdout/stderr, including TensorFlow/TFP, CUDA, HMC, benchmark, or Claude review commands, must preserve full output in a log artifact and show only a bounded summary in chat.

Required pattern:

1. Predeclare log and structured artifact paths in the subplan or ledger.
2. Redirect full stdout/stderr to the log file.
3. Prefer scripts that write JSON/Markdown result artifacts directly.
4. After completion, summarize exit status, artifact paths, pass/fail fields, and at most 20-40 failure log lines.
5. Treat excessive stdout/stderr as an execution-flow defect and repair with quieter redirection.

## Default And Assumption Audit

| Choice | Provenance | Classification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Visible execution only | User prompt plus template | Binding governance choice | Detached state cannot be supervised or recovered | No detached launch commands in runbook | Active |
| Claude review gate | Local claudecodex guide | Binding for material review if available | Review timeout or no verdict | Gate status plus probe/fallback status | Pending Phase 0 |
| CPU-hidden early diagnostics | BayesFilter policy | Debug/reference exception | Mistaken for production GPU evidence | Artifact field `CUDA_VISIBLE_DEVICES=-1` | Active |
| Scalar four-parameter target | Passed oracle diagnostic | Narrow inherited scope | Over-generalization | Non-claims in every result | Active |
| Whitened coordinate geometry | `quadratic_geometry.py` utility contract | Binding coordinate convention | Wrong mass in HMC | Phase 2 coordinate audit | Pending |

## Skeptical Plan Audit

Before each phase, Codex must record a skeptical audit in the ledger and check:

- wrong baselines;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons or ranking claims;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

Current audit status: `PASS_WITH_BOUNDARIES` for Phase 0 governance. Later phases remain `PENDING_SUBPLAN_AUDIT`.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract, append ledger entry.
2. `EXECUTE_MINIMAL`: run only visible commands in the current conversation.
3. `ASSESS_GATE`: compare outputs against criteria and vetoes; write or update result artifact.
4. `PASS_REVIEW`: send material result/subplan/repair bundle to Claude review gate.
5. `REPAIR_LOOP`: patch fixable blockers visibly, rerun focused checks, and stop after five review rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after the current phase gate passes; otherwise write stop handoff.

## Review Gate Command

Material review uses:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/ubuntu/python/BayesFilter \
  --review-name scalar-filtering-geometry-hmc-phase0 \
  --bundle /home/ubuntu/python/BayesFilter/docs/reviews/scalar-filtering-geometry-hmc-phase0-review-bundle-2026-07-08.md \
  --probe-timeout 90 \
  --timeout-seconds 120 \
  --max-retries 1 \
  --allow-bounded-fallback
```

The command must run with trusted/escalated permissions because it invokes Claude Code model/API work. If the material review fails but the tiny probe succeeds, revise the bundle/prompt and retry. If the probe shows Claude is unavailable or transport-blocked, write a Codex substitute review and label it weaker than full external review.

If the trusted-context reviewer blocks Claude review because the bundle would transfer private repository context to an external service, do not work around the block. Record `CLAUDE_REVIEW_POLICY_BLOCKED`, write a fresh Codex substitute review over the same required governance artifacts, and label it weaker than full external review.

## Human-Required Stop Conditions

Stop if continuing would require:

- project-direction change not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- model-file edits;
- interpreting GPU/special-hardware results without trusted-context evidence;
- continuing after Claude and Codex do not converge after five review rounds.

## Plain-Language Gate

Before accepting a phase result, blocker result, or final decision, Codex must verify that the artifact states the claimed target and computed quantity separately, labels unsupported claims as `unsupported` or `not checked`, labels mismatches as `wrong relative to the stated target`, and states what remains unproved or unevaluated.
