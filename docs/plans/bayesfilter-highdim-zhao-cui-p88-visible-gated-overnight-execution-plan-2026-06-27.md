# P88 Visible Gated Overnight Execution Plan

Date: 2026-06-27

## Status

`P88_VISIBLE_EXECUTION_RUNBOOK_REVIEWED_CLAUDE_AGREE`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus is a read-only reviewer only. Claude is not an execution authority
and cannot authorize human, runtime, model-file, funding, product-capability,
or scientific-claim boundaries.

This is an overnight-style gated plan in artifact naming only. It follows the
visible gated execution template and must not launch detached or nested agents.
Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, detached `tmux`, or background phase runners;
- copied-workspace execution.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p88-sir-d18-promotion-master-program-2026-06-27.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p88-claude-review-ledger-2026-06-27.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p88-visible-execution-ledger-2026-06-27.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p88-visible-stop-handoff-2026-06-27.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance bootstrap and P87 inheritance | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase0-governance-bootstrap-subplan-2026-06-27.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase0-governance-bootstrap-result-2026-06-27.md` |
| 1 | Degree-convergence protocol freeze | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase1-degree-convergence-protocol-subplan-2026-06-27.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase1-degree-convergence-protocol-result-2026-06-27.md` |
| 2 | Degree-convergence execution and evaluation | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-convergence-execution-subplan-2026-06-27.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-convergence-execution-result-2026-06-27.md` |
| 3 | Same-target reference bridge design | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase3-same-target-bridge-design-subplan-2026-06-27.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase3-same-target-bridge-design-result-2026-06-27.md` |
| 4 | Correctness-candidate bridge execution | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase4-correctness-bridge-execution-subplan-2026-06-27.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase4-correctness-bridge-execution-result-2026-06-27.md` |
| 5 | Source-route analytical derivative design | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase5-source-route-derivative-design-subplan-2026-06-27.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase5-source-route-derivative-design-result-2026-06-27.md` |
| 6 | HMC and production readiness gate | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase6-hmc-production-readiness-subplan-2026-06-27.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase6-hmc-production-readiness-result-2026-06-27.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can P88 promote Zhao-Cui SIR d18 beyond P87 execution-only evidence through reviewed degree, bridge, derivative, and readiness gates? |
| Baseline/comparator | P87 final label `D18_SOURCE_ROUTE_EXECUTION_ONLY`; P86 L1/rank/degree artifacts; current code/source-route constraints. |
| Primary pass criterion | A phase can pass only with exact artifacts, local checks, no veto diagnostics, and explicit claim/nonclaim language. |
| Veto diagnostics | Proxy promotion, degree-comparator overclaim, ALS revival, audit tuning, missing L1 tuning, missing source anchors, wrong target, missing bridge tolerances, JVP analytical overclaim, GPU/HMC/production drift. |
| Explanatory diagnostics | Fit/holdout/audit residuals, validation/LR events, rank/degree differences, bridge provenance, derivative route inventory, runtime/memory. |
| Not concluded | Any stronger claim not explicitly passed by its phase gate. |
| Artifacts | P88 master, subplans/results, ledgers, review records, fit/bridge manifests if later phases run. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| P88 starts from P87 final label | P87 reviewed stop handoff | Avoids reopening closed execution-only evidence | Stronger claim silently assumed | Phase 0 exact grep checks | binding |
| Degree convergence is first stronger lane | P87 successor recommendation | It is the nearest blocker to rank/degree-stable label | Correctness bridge bypasses degree blocker | Phase 1 handoff must preserve blocker | binding |
| Training-base/L1 only | P86 Phase 6U/6V/6W | Prevents ALS and unregularized drift | ALS revival or audit tuning | Phase 1 protocol checks | binding |
| Claude read-only review | User request and repo policy | Independent review without execution authority | Claude edits/runs/broad review | One-path bounded prompts | binding |
| Visible execution only | Template | Recoverable and auditable | Hidden detached work | No detached launch commands | binding |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and the
execution ledger for material phases.

Check:

- wrong baselines;
- proxy metrics promoted to pass criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If a material flaw is found, revise the plan or write a blocker note before
running that phase.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites.
   - Restate the phase evidence contract in chat.
   - Append a ledger entry.
2. `EXECUTE_MINIMAL`
   - Run only visible commands in the current conversation.
   - Prefer the smallest diagnostic or implementation needed.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against primary criterion and veto diagnostics.
   - Write/update the phase result.
4. `PASS_REVIEW`
   - Use Claude read-only review for material crossings.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, patch the same subplan/result visibly.
   - Rerun focused checks.
   - Retry Claude review only for material issues.
   - Stop after five Claude rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write handoff if a true human-required blocker appears.

## Claude Read-Only Review Template

Use bounded prompts:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <path>. Do not edit,
run commands, launch agents, or review the whole repo. Question: <one question>.
End with VERDICT: AGREE or VERDICT: REVISE.
```

If Claude does not respond, Codex may run a tiny escalated probe. If the probe
responds, the prompt must be redesigned narrower before retrying. Record every
Claude nonresponse, probe command, probe outcome, and prompt redesign in both
ledgers before retrying the material review.

## Anticipated Approval / Escalation Needs

- Claude Code read-only reviews require escalated sandbox permissions because
  they use external model/API access. The user's request authorizes Claude as
  read-only reviewer; no additional human approval is expected for bounded
  review prompts.
- Local doc/artifact checks require no human approval.
- CPU-only TensorFlow/Python checks must set `CUDA_VISIBLE_DEVICES=-1` before
  TensorFlow import and record the CPU-only posture.
- GPU/CUDA commands require escalated permissions and are not authorized until
  the relevant phase is visibly refreshed with exact commands, runtime budget,
  device target, stop conditions, and review evidence. None are planned for
  Phases 0-1.
- Long fitting/training commands are not authorized by this runbook until
  Phase 1 refreshes Phase 2 with exact commands, budgets, stop conditions, and
  review evidence.
- HMC commands are not authorized by this runbook until Phase 6 is visibly
  refreshed with exact commands, target contract, runtime budget, sampler
  diagnostics, stop conditions, and review evidence.
- Production-readiness commands, benchmarks, default-policy changes, release
  gates, or product-capability claims are not authorized by this runbook until
  Phase 6 is visibly refreshed with exact commands, evidence contract, stop
  conditions, and review evidence.
- Human approval is required only for true blockers that cross human, runtime,
  model-file, funding, product-capability, default-policy, destructive-action,
  or scientific-claim boundaries not already covered by a reviewed subplan.

## Human-Required Stop Conditions

Stop if continuing would require:

- changing pass/fail criteria after seeing results;
- destructive git/filesystem actions;
- package installation, network fetch, credentials, or environment setup beyond
  Claude review;
- broad default-policy changes;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted evidence;
- continuing after five non-convergent Claude review rounds.

## Final Visible Handoff

When execution completes or stops, write:

- final phase reached;
- final status;
- result artifacts;
- Claude review trail;
- tests actually run;
- unresolved blockers;
- what was not concluded;
- safest next decision.
