# P8h Phase 1 Subplan: Governance Reset

Date: 2026-06-15

Status: `PASS_REVIEWED`

## Phase Objective

Reset P8 governance so no-resampling is graph/kernel sanity only, classical
resampling is ESS/debug comparator only, and Corenflos OT-resampled Algorithm 1
LEDH is the default serious candidate.

## Entry Conditions

- Phase 0 documentation/governance correction passed and wrote its result.

## Required Artifacts

- Phase 1 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase1-governance-reset-result-2026-06-15.md`.
- Updated P8h ledger and any affected P8g/P8h status notes.

## Required Checks, Tests, Reviews

- `git diff --check`.
- Focused text search proving no P8h artifact promotes no-resampling as serious.
- Claude read-only review if governance language changes materially.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Are the route roles and claim boundaries reset before implementation? |
| Baseline/comparator | P8g stop handoff, G4 blocker, Phase 0 result. |
| Primary criterion | Governance artifacts clearly assign route roles and stop unsupported claims. |
| Veto diagnostics | No-resampling promoted; classical multinomial promoted for gradients; OT route treated as already validated. |
| Explanatory diagnostics | Search hits and review findings. |
| Not concluded | Implementation, value, gradient, GPU scaling, or HMC readiness. |

## Forbidden Claims And Actions

- Do not run implementation or benchmarks in Phase 1.
- Do not change pass/fail criteria after seeing results.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 2 only after Phase 1 result records the route-role reset and
review status.

## Stop Conditions

- Human direction is needed to choose a different default serious route.
- Review finds unfixable conflict with existing evidence boundaries.
