# P88 Master Program: Zhao-Cui SIR d18 Promotion Successor

Date: 2026-06-27

Status: `P88_MASTER_REVIEWED_AGREE`

## Objective

Start a new successor program after P87. P87 closed with:

```text
selected_headline_label: D18_SOURCE_ROUTE_EXECUTION_ONLY
```

P88 may promote stronger Zhao-Cui SIR d18 claims only through reviewed gates,
in this order:

1. close degree convergence and, if justified, promote
   `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE`;
2. build or block a same-target source-backed reference bridge for
   `D18_CORRECTNESS_CANDIDATE`;
3. design source-route full-history analytical derivative wiring with
   paper/source anchors;
4. evaluate HMC/production readiness only after correctness, derivative, and
   route gates close.

## Governing Artifacts

- Runbook:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-visible-gated-overnight-execution-plan-2026-06-27.md`
- Execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-visible-execution-ledger-2026-06-27.md`
- Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-claude-review-ledger-2026-06-27.md`
- Stop handoff:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-visible-stop-handoff-2026-06-27.md`

## Phase Index

| Phase | Name | Subplan | Result |
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
| Question | Can P88 justifiably promote Zhao-Cui SIR d18 beyond P87 execution-only evidence without repeating prior mistakes? |
| Baseline/comparator | P87 final handoff/result; P86 L1 tuning, rank pass, degree blocked, configurable-basis repair, and order-3 comparator evidence. |
| Primary pass criterion | Each stronger label passes only through its reviewed phase gate with exact artifacts, pass/fail criteria, veto diagnostics, and no unsupported claim leakage. |
| Veto diagnostics | Degree evidence treated as correctness; favorable comparator treated as convergence; execution-only treated as correctness; local fixed-branch evidence treated as source-route correctness; ALS revival; audit tuning; missing L1 tuning; unanchored source-faithful claim; JVP/autodiff promoted as analytical derivative; GPU/HMC/production claims before correctness and derivative gates. |
| Explanatory diagnostics | Fit/holdout/audit residuals, validation curves, LR-drop events, rank/degree deltas, bridge provenance, derivative route inventory, runtime/memory. |
| Not concluded | Production readiness, HMC readiness, posterior correctness, source-route correctness, full-history analytical-gradient correctness, GPU readiness, LEDH agreement, d50/d100 scaling, or default-policy change unless the relevant phase explicitly gates it. |
| Artifacts | P88 master, runbook, subplans/results, ledgers, reviewed command manifests, and final stop handoff. |

## Claim Ladder

| Claim | Current inherited status | P88 gate |
| --- | --- | --- |
| `D18_SOURCE_ROUTE_EXECUTION_ONLY` | Passed/reviewed in P87 | Inherited baseline; not re-proved. |
| `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE` | Blocked by unresolved degree convergence | Phases 1-2. |
| `D18_CORRECTNESS_CANDIDATE` | Blocked by missing same-target source-backed bridge | Phases 3-4, only after Phase 2 passes or explicitly records a scoped alternative. |
| Source-route full-history analytical-gradient readiness | Not established | Phase 5. |
| HMC/production readiness | Not established | Phase 6, only after correctness and derivative gates. |

## Mandatory Training Discipline

All future fitted Zhao-Cui source-route evidence must preserve:

- training-base optimizer only;
- L1 weight tuning as the default procedure;
- zero-L1 as an allowed comparator arm, not a universal scalar default;
- validation/holdout/audit separation;
- no audit tuning;
- plateau scheduler with LR drops and early stop only after LR drops stop
  helping or a reviewed max budget is reached;
- sample budget scaled to parameter count;
- no ALS training revival.

## Claude Review Protocol

Claude is read-only reviewer only. Codex is supervisor and executor.
Material subplans/results use one-path bounded prompts and stop after five
review rounds for the same blocker.

## Launch Rule

P88 launches with Phase 0 only after this master, the visible runbook, and the
Phase 0 subplan pass local artifact checks and Claude read-only review.
