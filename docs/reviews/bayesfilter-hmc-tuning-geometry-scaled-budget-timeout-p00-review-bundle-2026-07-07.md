# Claude Read-Only Review Bundle

Date: 2026-07-07
Review name: `bayesfilter-hmc-tuning-geometry-scaled-budget-timeout-p00`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, approve
boundary crossings, or act as execution authority.

## Objective

Review whether the BayesFilter master program, visible runbook, and Phase 0
inventory subplan are sufficient and safe before Codex executes the inventory
and implementation phases for HMC tuning sample/time budget repair.

## Artifacts To Inspect

- `docs/plans/bayesfilter-hmc-tuning-geometry-scaled-budget-timeout-master-program-2026-07-07.md`
- `docs/plans/bayesfilter-hmc-tuning-geometry-scaled-budget-timeout-visible-gated-execution-runbook-2026-07-07.md`
- `docs/plans/bayesfilter-hmc-tuning-geometry-scaled-budget-timeout-p00-inventory-subplan-2026-07-07.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is this gated program/subplan safe and complete enough to start Phase 0 inventory? |
| Baseline/comparator | User directive: BayesFilter owns generic HMC tuning repair/docs, MacroFinance only integrates CCMA, no NUTS, no magic timeout/sample constants. |
| Primary criterion | Plan has explicit phases, artifacts, checks, evidence contract, forbidden claims/actions, handoff conditions, stop conditions, Claude read-only boundary, and no documentation-location error. |
| Veto diagnostics | Plan sends generic docs to MacroFinance; Claude given execution authority; missing BayesFilter usage audit; missing no-NUTS audit; no magic-number audit; no stop condition for active NUTS or MacroFinance-local HMC tuning; no Phase 0 result artifact. |
| Explanatory diagnostics | Whether phase sequence is overly broad, whether review bundles are bounded, whether Phase 0 inventory scope is too narrow or too wide. |
| Numeric provenance | No new tuning numeric default is authorized by Phase 0. Any numbers mentioned are inventory targets, not accepted defaults. |
| Not concluded | No implementation correctness, no tuning readiness, no posterior convergence, no sampler superiority, no CCMA result validity. |

## Review Questions

1. Is there a material correctness or boundary issue in the master program,
   runbook, or Phase 0 subplan?
2. Is the evidence contract internally consistent with the user's directive?
3. Are required Phase 0 artifacts and checks sufficient to identify active
   sample/time/attempt constants before implementation?
4. Are there unsupported claims or hidden authority transfers?
5. Are there unsupported numeric defaults introduced by the plan?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
