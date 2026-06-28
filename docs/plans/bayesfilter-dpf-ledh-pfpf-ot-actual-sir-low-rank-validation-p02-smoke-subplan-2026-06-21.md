# P02 Tiny Actual-SIR Route Smoke Subplan

Status: `DRAFT_FOR_REVIEW`

## Phase Objective

Run the smallest actual-SIR route diagnostics that can prove both streaming and
low-rank paths execute on the real workload before expensive paired ladders.

## Entry Conditions Inherited From Previous Phase

- P01 harness result passed.
- Harness and focused tests exist and pass.
- No shared contract/API/export change is required.

## Required Artifacts

- Smoke JSON/Markdown aggregate:
  `docs/benchmarks/actual-sir-low-rank-route-validation-smoke-2026-06-21.json`
  and `.md`
- Row sidecars written by the harness if row subprocesses are used.
- P02 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p02-smoke-result-2026-06-21.md`
- Refreshed P03 subplan.

## Required Checks, Tests, Reviews

- CPU-hidden or trusted GPU smoke, explicitly recorded.
- Suggested rows:
  - `B=1,T=3,N=128`, both routes.
  - `B=1,T=20,N=256`, both routes.
- Validate finite log likelihood, filtered means/variances, ESS, route
  invocations, low-rank nonmaterialization, and low-rank factor diagnostics.
- Claude review only if smoke result changes planned thresholds or exposes a
  material boundary issue.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do both route implementations execute on tiny actual-SIR rows and emit required validity/diagnostic artifacts? |
| Baseline/comparator | Streaming route on the same actual-SIR rows. |
| Primary pass criterion | Both routes pass tiny rows with finite outputs, route-fired evidence, and no hard vetoes. |
| Veto diagnostics | Nonfinite outputs, missing route invocation, low-rank dense materialization, invalid low-rank factors, missing actual-SIR semantics. |
| Explanatory diagnostics | Runtime, memory, ESS, log-likelihood/filtered-summary deltas. |
| Not concluded | No large-N performance claim, no posterior correctness, no promotion. |
| Artifact | Smoke JSON/Markdown and P02 result. |

## Forbidden Claims/Actions

- Do not interpret tiny smoke speed as promotion evidence.
- Do not change thresholds after seeing smoke results without a repair result.
- Do not proceed to large-N if smoke fails hard validity.

## Exact Next-Phase Handoff Conditions

Advance to P03 only if smoke passes for both routes and P03 paired rows/timeout
budget are still feasible under current GPU/resource status.

## Stop Conditions

- `TUNING_REQUIRED` if low-rank runs but fails factor or predeclared
  engineering-comparability thresholds in a way a planned tuning repair can
  address. P02 smoke does not support promotion even if timing looks favorable.
- `REJECT_CURRENT_ROUTE` if low-rank emits nonfinite values or invalid factors
  after focused repair.
- Stop for human direction if GPU/resource constraints invalidate P03.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write the P02 phase result.
3. Draft or refresh P03.
4. Review P03 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
