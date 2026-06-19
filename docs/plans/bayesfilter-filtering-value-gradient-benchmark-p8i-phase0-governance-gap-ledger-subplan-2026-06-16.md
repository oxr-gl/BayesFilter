# P8i Phase 0 Subplan: Governance And Gap Ledger

Date: 2026-06-16

Status: `REVIEWED_EXECUTED`

## Phase Objective

Create the explicit P8i gap ledger and inherited-boundary contract before any
new numerical or HMC execution.

## Entry Conditions

- P8h Phase 11 closure sync is reviewed.
- P8i master/runbook planning gate is reviewed.
- No material P8i numerical command has been run.

## Required Artifacts

- P8i remaining-gap ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-remaining-gap-ledger-2026-06-16.md`.
- Phase 0 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase0-governance-gap-ledger-result-2026-06-16.md`.
- Refreshed Phase 1 subplan if review finds missing entry or stop conditions.

## Required Checks, Tests, Reviews

- `git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-* docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-*`
- Focused `rg` checks for all remaining-gap labels and forbidden-claim
  boundaries.
- Read-only Claude review of the gap ledger and Phase 1 subplan.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Are all remaining P8h limitations mapped to explicit P8i gates with nonclaim boundaries before execution? |
| Baseline/comparator | P8h Phase 11 closure result, P8h artifact index, and P8h Phase 5-8 results. |
| Primary criterion | A ledger maps each remaining gap to a planned P8i phase, required artifacts, promotion gate, veto diagnostics, and nonclaims. |
| Veto diagnostics | Missing any P8h nonclaim; treating planning as evidence; authorizing long GPU/HMC execution before its subplan; conflating relaxed-OT AD gradient with exact stochastic PF marginal score; reviving P8g no-resampling as serious route. |
| Explanatory diagnostics | Text search hits, review findings. |
| Not concluded | No numerical, GPU, gradient, HMC, NUTS, ranking, default-policy, or production-readiness claim. |

## Forbidden Claims And Actions

- Do not run GPU, HMC, NUTS, benchmark, or long numerical commands.
- Do not change implementation code.
- Do not commit or push.
- Do not claim that the gap ledger closes any scientific gap.

## Exact Next-Phase Handoff Conditions

Phase 1 may launch only if the Phase 0 result and refreshed Phase 1 subplan
are reviewed and preserve the longer-prefix/full-horizon boundary.

## Stop Conditions

- The gap list cannot be mapped to phase gates without human prioritization.
- Review finds that the planned Phase 1 would overclaim full-horizon adequacy
  or hide runtime risk.
