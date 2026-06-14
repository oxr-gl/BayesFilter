# P47 Overnight Gated Self-Recovery Runbook

metadata_date: 2026-06-08
phase: P47-overnight
status: `DRAFT_FOR_CLAUDE_RUNBOOK_REVIEW`

## Purpose

Govern a supervised P47 overnight run for the remaining Zhao--Cui filtering
program.  Codex is the supervisor and execution agent.  Claude is a read-only
reviewer only and must not edit files, run experiments, launch agents, or
change state.

This runbook begins with the repair of the prior P47 plan-governance blocker:
spatial SIR and predator-prey now have separate lower-rung and production
tokens, and M6 depends on the correct evidence class.

## Governing Sources

- P47 master:
  `docs/plans/bayesfilter-highdim-zhao-cui-p47-remaining-filtering-completion-master-program-2026-06-08.md`
- P47 Claude plan review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p47-remaining-filtering-completion-claude-review-ledger-2026-06-08.md`
- P47 phase subplans M0--M7:
  `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase*-2026-06-08.md`
- P42 gradient/likelihood validation rules:
  `docs/plans/bayesfilter-highdim-zhao-cui-p42-gradient-likelihood-validation-rules-2026-06-07.md`
- P45 closeout:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-overnight-gated-self-recovery-execution-result-2026-06-08.md`
- P46 multistate adapter and resume governance:
  `docs/plans/bayesfilter-highdim-zhao-cui-p46-multistate-zhaocui-adapter-result-2026-06-08.md`
  and
  `docs/plans/bayesfilter-highdim-zhao-cui-p46-resume-governance-result-2026-06-08.md`

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_RUNBOOK_REVIEW_WITH_PRELAUNCH_REPAIR_GATE`.

The main risk is repeating the prior P47 failure mode: a lower-rung fixture,
feasibility manifest, or proposal diagnostic could be promoted as production
filtering, score API readiness, or HMC readiness.  The repaired P47 packet
therefore splits M4 and M5 into lower-rung and production tokens:

- `PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY`
- `PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING`
- `PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING`
- `PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING`

M6 must label each API/HMC row as lower-rung or production and may not promote
production API/HMC readiness from lower-rung tokens.

No material flaw remains in using this as an execution runbook if Claude
confirms the split-token repair and the self-recovery controls.

## Evidence Contract

Question: can Codex supervise and execute P47 overnight, repairing fixable
issues through bounded reviewed amendments, while preserving target identity,
source governance, same-target comparison discipline, and P42 gradient/HMC
standards?

Baseline/comparator:

- phase-specific exact, dense/refined, Kalman, CUT4, Zhao--Cui retained-grid,
  and production-scale baselines declared by each subplan;
- P45/P46 blockers as historical constraints, not artifacts to overwrite;
- P42 Tier 1/2/3 validation rules for any score or HMC-readiness claim.

Primary promotion criterion:

- each phase emits only the pass token whose evidence class it actually
  satisfies, with a result artifact, command manifest, nonclaims, and read-only
  Claude review.

Veto diagnostics:

- S&P 500 reproduction is reintroduced;
- MATLAB code is copied, line-translated, or used as production structure;
- CUT4 and Zhao--Cui evaluate different targets;
- gradients are compared in different parameterizations;
- finite outputs, fit residuals, resource manifests, proposal metrics, or
  lower-rung tests are promoted as production correctness;
- M4/M5 production tokens emit without M2 readiness and lower-rung tokens;
- M6 production API/HMC readiness emits from lower-rung tokens;
- Claude returns a material blocker after five repair-review iterations;
- a decision requires human scientific judgment rather than a fixable
  engineering/governance repair.

Explanatory-only diagnostics:

- wall time, memory, TT rank, point count, resource usage, fit residual,
  holdout residual, branch hash, ESS-like metric, trajectory plot, and smoke
  timing unless a phase-specific plan explicitly makes one a narrow stress
  criterion.

What will not be concluded:

- no S&P 500 reproduction;
- no adaptive MATLAB TT-cross/SIRT reproduction from M1 route-label evidence;
- no production spatial SIR or predator-prey filtering from lower-rung tokens;
- no production API or HMC readiness without the matching P42 evidence class;
- no high-dimensional scalability claim from tiny retained-grid fixtures.

Artifact preserving the result:

- this runbook;
- `docs/plans/bayesfilter-highdim-zhao-cui-p47-overnight-gated-self-recovery-claude-review-ledger-2026-06-08.md`;
- `docs/plans/bayesfilter-highdim-zhao-cui-p47-overnight-gated-self-recovery-execution-result-2026-06-08.md`;
- phase result ledgers and phase Claude ledgers created during execution.

## Launch Preconditions

Execution may launch only after all preconditions hold:

1. `git diff --check` passes for P47 plan artifacts.
2. Claude read-only review returns `PASS_P47_OVERNIGHT_RUNBOOK`.
3. The execution result artifact records `LAUNCHED_BY_CODEX_SUPERVISOR`.
4. No detached Claude executor is started.  Claude is used only for bounded
   read-only reviews.
5. GPU/CUDA work is skipped unless a phase-specific trusted execution plan is
   written and reviewed.  Default launch is CPU-only with
   `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`.

## Phase State Machine

Each phase runs:

```text
READY
  -> SKEPTICAL_PHASE_AUDIT
  -> IMPLEMENT_OR_REPAIR
  -> LOCAL_EVIDENCE_RUN
  -> EVIDENCE_AUDIT
  -> RESULT_LEDGER_WRITTEN
  -> CLAUDE_READ_ONLY_REVIEW
  -> TRACEABILITY_UPDATED
  -> PHASE_PASS_OR_BLOCK
```

Fixable failure loop:

```text
BLOCKER_CLASSIFIED
  -> REPAIR_PLAN_AMENDMENT
  -> CLAUDE_REPAIR_REVIEW_TO_PASS_OR_MAX_5
  -> REPAIR_IMPLEMENTED
  -> LOCAL_EVIDENCE_RUN
```

Stop conditions:

- same material blocker remains after five Claude repair reviews;
- required human interpretation, licensing, data access, or infrastructure
  choice is encountered;
- a veto diagnostic fails and fixing it would weaken the evidence contract.

## Phase Gates

| Phase | Gate | Required token(s) |
| --- | --- | --- |
| G0 | repaired governance packet and runbook accepted | `PASS_P47_OVERNIGHT_RUNBOOK` |
| M0 | target registry and S&P 500 exclusion | `PASS_P47_M0_GOVERNANCE` |
| M1 | route-label governance | `PASS_P47_M1_ADAPTIVE_ROUTE` |
| M2 | paper-scale readiness only | `PASS_P47_M2_PAPER_SCALE_READINESS` |
| M3 | generalized SV same-target value/gradient | `PASS_P47_M3_GENERALIZED_SV_EQUALITY` |
| M4a | spatial SIR lower-rung reference/equality | `PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY` |
| M4b | spatial SIR production filtering | `PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING` |
| M5a | predator-prey lower-rung reference filtering | `PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING` |
| M5b | predator-prey production filtering | `PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING` |
| M6 | score API/HMC readiness by evidence class | `PASS_P47_M6_SCORE_HMC_READINESS` |
| M7 | closeout and nonclaim reconciliation | `PASS_P47_M7_CLOSEOUT` |

M4b cannot run before M2 and M4a.  M5b cannot run before M2 and M5a.  M6
production rows cannot run before the corresponding production token.

## Default Local Gates

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim
git diff --check -- bayesfilter/highdim tests/highdim docs/plans
```

If a phase-specific test named in a subplan does not exist, the phase begins by
creating the missing test under the same evidence contract rather than skipping
the gate.

## Claude Review Prompt

```text
READ-ONLY REVIEW ONLY. Do not edit files, run experiments, launch agents, or
change state. Review the P47 overnight runbook plus the repaired P47 master
and M0--M7 subplans. Check the split M4/M5 token repair, M6 dependency repair,
Codex-as-supervisor/Claude-read-only role split, evidence contract, stop
conditions, CPU/GPU policy, S&P 500 exclusion, proxy-vs-correctness discipline,
and whether launch is safe after PASS. Findings first, at most 8 bullets. End
with exactly PASS_P47_OVERNIGHT_RUNBOOK or BLOCK_P47_OVERNIGHT_RUNBOOK.
```

