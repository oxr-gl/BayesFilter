# P69 Phase 5 Subplan: Fixed-Variant Repair Decision Or Adaptive-Reproduction Fork

metadata_date: 2026-06-15
status: READY_AFTER_PHASE4_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p69-remaining-gaps-master-program-2026-06-15.md
phase: 5
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Decide the next Zhao--Cui route after Phase 4:

- continue the fixed-HMC adaptation lane with a bounded repair/design
  diagnostic;
- open a separate adaptive Zhao--Cui reproduction lane;
- stop for human scientific direction.

The decision must preserve the distinction between the current
`fixed_hmc_adaptation` and any future adaptive-reproduction program.

## Entry Conditions Inherited From Phase 4

- Phase 4 result exists:
  `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase4-structural-diagnosis-result-2026-06-15.md`.
- Claude read-only review of Phase 4 returns `VERDICT: AGREE`.
- Phase 4 hypothesis classifications are explicit:
  - inactive rank channels: supported;
  - deterministic degeneracy: unresolved;
  - metric-insensitive comparison: weakened;
  - basis/domain sensitivity: supported;
  - design coverage insufficiency: supported;
  - overfitting: unresolved;
  - target scaling: unresolved;
  - structural sensitivity of the fixed variant: supported.
- Phase 3/4 do not establish d18 correctness, scaling, HMC readiness, or
  adaptive parity.

## Required Artifacts

- Phase 5 route-decision result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase5-route-decision-result-2026-06-15.md`.
- Updated P69 execution ledger and Claude review ledger.
- Refreshed next subplan:
  - either a bounded fixed-variant repair/design diagnostic subplan;
  - or an adaptive-reproduction fork subplan;
  - or a blocker/stop handoff.

## Required Checks/Tests/Reviews

This is a governance and scientific-boundary decision.  No code changes are
required unless a result artifact parser is added.

Required local text checks:

```bash
rg -n "fixed_hmc_adaptation|adaptive Zhao|d18 correctness|HMC|scaling|route decision|human direction" docs/plans/bayesfilter-highdim-zhao-cui-p69-phase4-structural-diagnosis-result-2026-06-15.md docs/plans/bayesfilter-highdim-zhao-cui-p69-phase5-route-decision-result-2026-06-15.md
rg -n "inactive rank channels|deterministic degeneracy|metric-insensitive comparison|basis/domain sensitivity|design coverage insufficiency|overfitting|target scaling|structural sensitivity" docs/plans/bayesfilter-highdim-zhao-cui-p69-phase4-structural-diagnosis-result-2026-06-15.md docs/plans/bayesfilter-highdim-zhao-cui-p69-phase5-route-decision-result-2026-06-15.md
```

Claude review must inspect:

- Phase 4 diagnosis result;
- Phase 5 route-decision result;
- refreshed next subplan or blocker handoff;
- claim-boundary language.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which route is justified by the fixed-variant evidence: repair/design diagnostic, adaptive-reproduction fork, or stop for human direction? |
| Baseline/comparator | Phase 4 structural diagnosis and the P69 source-governance boundary. |
| Primary criterion | Choose exactly one primary route and state what evidence supports it, what it does not authorize, and what artifact starts the next phase. |
| Veto diagnostics | Mixing fixed-HMC and adaptive claims; claiming d18 correctness; claiming scaling or HMC readiness; treating degree failure as paper failure; launching a new experiment without a subplan; skipping human direction when the target changes. |
| Explanatory diagnostics | Phase 3/4 hypothesis classifications, holdout/replay availability, rank zero-delta, degree threshold failures, fit and diagnostic residuals. |
| Not concluded | No correctness, scaling, HMC readiness, adaptive parity, or paper-failure claim. |
| Artifact preserving result | Phase 5 route-decision result. |

## Forbidden Claims/Actions

- Do not merge fixed-HMC adaptation and adaptive-reproduction claims.
- Do not authorize d18 validation, d50/d100 scaling, or HMC readiness from
  Phase 4 alone.
- Do not claim the fixed variant is source-faithful adaptive Zhao--Cui.
- Do not treat a route decision as a scientific validation.
- Do not launch new diagnostics or experiments in Phase 5.

## Exact Next-Phase Handoff Conditions

Phase 5 may hand off only if:

- one route is selected as primary;
- rejected/deferred routes are documented with reasons;
- the selected route has a next subplan or blocker handoff;
- claim boundaries and forbidden claims are restated;
- any need for human direction is explicit;
- Claude returns `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker result if:

- the route decision requires changing the scientific target without human
  direction;
- the evidence is insufficient to choose among repair/fork/stop;
- the next route would require GPU/HMC, long runs, model-file changes, or
  adaptive reproduction without a separate reviewed subplan;
- Claude and Codex do not converge after five review rounds.
