# P84 Zhao-Cui Production Promotion Visible Gated Execution Runbook

Date: 2026-06-23

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK_PENDING_REVIEW`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook is based on
`/home/chakwong/python/claudecodex/docs/templates/visible-gated-execution-runbook-template.md`.
It is visible and recoverable inside the current conversation.  Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

If detached overnight execution is later required, stop and write a separate
detached-supervisor plan for human approval.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p84-production-promotion-master-program-2026-06-23.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p84-claude-review-ledger-2026-06-23.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p84-visible-execution-ledger-2026-06-23.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p84-visible-stop-handoff-2026-06-23.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
|---|---|---|---|
| P84-0 | Production target freeze | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase0-production-target-freeze-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase0-production-target-freeze-result-2026-06-23.md` |
| P84-1 | Author basis/domain parity | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase1-author-basis-domain-parity-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase1-author-basis-domain-parity-result-2026-06-23.md` |
| P84-2 | Budget-compliant fitting | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase2-budget-compliant-fitting-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase2-budget-compliant-fitting-result-2026-06-23.md` |
| P84-3 | Same-route rank/degree convergence | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase3-same-route-rank-convergence-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase3-same-route-rank-convergence-result-2026-06-23.md` |
| P84-4 | Correctness bridge | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase4-correctness-bridge-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase4-correctness-bridge-result-2026-06-23.md` |
| P84-5 | Production KR closure | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase5-production-kr-closure-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase5-production-kr-closure-result-2026-06-23.md` |
| P84-6 | Analytical derivative repair | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase6-analytical-derivative-repair-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase6-analytical-derivative-repair-result-2026-06-23.md` |
| P84-7 | HMC readiness | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase7-hmc-readiness-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase7-hmc-readiness-result-2026-06-23.md` |
| P84-8 | LEDH comparator | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase8-ledh-comparator-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase8-ledh-comparator-result-2026-06-23.md` |
| P84-9 | d50/d100 scale stress and uncertainty accounting | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase9-scale-stress-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase9-scale-stress-result-2026-06-23.md` |
| P84-10 | Production promotion decision | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase10-production-promotion-decision-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase10-production-promotion-decision-result-2026-06-23.md` |

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can visible execution close or precisely block every remaining production gap for Zhao-Cui SIR? |
| Baseline/comparator | P83 execution-only closeout and P84 master program. |
| Primary pass criterion | Every P84 phase writes a pass or blocker result under its subplan; production promotion only occurs after all mandatory gates pass. |
| Veto diagnostics | Proxy promotion, missing stop conditions, unapproved runtime boundary crossings, unsupported production claims, or treating Claude as execution authority. |
| Explanatory diagnostics | Local checks, source/code inventories, tests, benchmark manifests, review findings, and blocker ledgers. |
| Not concluded | Production readiness, default-policy change, correctness, HMC readiness, LEDH superiority, or scaling until their gates pass. |
| Artifacts | Master program, runbook, ledgers, phase subplans/results, JSON manifests, final reset memo. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
|---|---|---|---|---|---|
| Start from P83 execution-only | P83 final reset memo | Honest current evidence | Treat execution-only as correctness | P84-0 target freeze | binding |
| TensorFlow/TFP default backend | AGENTS.md | Project default | Non-default backend drift | Code review and imports | binding |
| GPU is default production target but not for planning | AGENTS.md | Avoid sandbox false negatives | CPU smoke promoted to production | Runtime posture field in artifacts | binding |
| Claude read-only only | User request and runbook | External review without authority drift | Claude treated as approver/executor | Review ledger | binding |

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

If the audit finds a material flaw, revise the plan or write a blocker before
running the phase.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run only visible commands in this conversation.
3. `ASSESS_GATE`: compare outputs against criteria and veto diagnostics.
4. `PASS_REVIEW`: use Claude read-only review for material phase decisions.
5. `REPAIR_LOOP`: patch fixable issues visibly, rerun checks, and stop after
   five Claude rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after the gate passes; otherwise write the
   handoff.

## Claude Read-Only Review Protocol

Use the trusted wrapper only with escalated permissions:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name <short-review-name> \
  --model opus \
  --effort max \
  "<bounded prompt>"
```

Prompt shape:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: <one
question>. End with VERDICT: AGREE or VERDICT: REVISE.
```

If Claude stalls, run:

```text
READ-ONLY PROBE. Reply exactly PROBE_OK.
```

If the probe responds, redesign the prompt.

## Human-Required Stops

Stop if continuing would require:

- package installation, network fetch, credentials, or environment setup;
- GPU/CUDA/NVIDIA execution without exact approved command;
- fitting, LEDH, HMC, MCMC, d=50/d=100, long, or production-promotion command
  without exact approved command;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- continuing after five Claude review rounds for the same blocker.

## Final Visible Handoff

When execution completes or stops, write:

- final phase reached;
- final status;
- result artifacts;
- Claude review trail;
- tests/benchmarks actually run;
- unresolved blockers;
- what was not concluded;
- safest next human decision.
