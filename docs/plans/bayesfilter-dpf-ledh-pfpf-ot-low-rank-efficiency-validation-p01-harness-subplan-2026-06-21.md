# P01 Common Efficiency Harness And Small Sanity Checks Subplan

Status: `DRAFT_AFTER_P00_ROUND_2`

## Phase Objective

Create a lane-owned common efficiency harness that can run the existing
streaming LEDH/PFPF-OT route and the low-rank route on comparable LGSSM-shaped
settings, then validate small route-fired, TF32-state, timing/memory, and
bounded output-comparability sanity checks.

## Entry Conditions Inherited From Previous Phase

P00 must pass.  GPU selection and fixed criteria remain binding.  The harness
must be lane-owned and must not alter public exports/defaults or shared
contracts.

## Required Artifacts

- Harness:
  `docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py`
- Tests:
  `tests/test_low_rank_ledh_pfpf_efficiency.py`
- Small sanity JSON:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-small-2026-06-21.json`
- Small sanity Markdown:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-small-2026-06-21.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p01-harness-result-2026-06-21.md`
- Log:
  `docs/benchmarks/logs/low-rank-ledh-pfpf-efficiency-p01-small.log`

## Required Checks, Tests, And Reviews

- `python -m py_compile docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py`
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_low_rank_ledh_pfpf_efficiency.py -q`
- Small CPU sanity command that runs both routes at tiny `N`.
- JSON inspection for finite outputs, low-rank route-fired evidence, TF32 state
  field, physical/logical GPU fields, timeout fields, output-comparability
  fields, and timing/memory metric fields.
- Claude review only if material harness boundary issues appear.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the common harness produce comparable artifacts for streaming and low-rank routes and prove low-rank route execution? |
| Baseline/comparator | Existing streaming route and low-rank route under a common harness wrapper. |
| Primary pass criterion | Harness/tests pass; both routes produce finite small outputs; low-rank records route invocations equal to active mask count; required TF32, same-GPU, timeout, output-comparability, timing, and memory fields exist. |
| Veto diagnostics | Import failure, shape mismatch, nonfinite output, missing low-rank invocation evidence, missing TF32/GPU/timeout/output-comparability/timing/memory fields, dense materialization in low-rank scale path, or shared/public edit. |
| Explanatory diagnostics | Small runtime/memory values and output previews. |
| Not concluded | No efficiency, speedup, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, or broad scalable-OT selection. |
| Artifact | P01 JSON/Markdown/result/log. |

## Forbidden Claims And Actions

- Do not claim efficiency from small sanity checks.
- Do not modify the existing streaming implementation.
- Do not widen fixed thresholds.
- Do not use network, package installs, POT, or external solvers.

## Exact Next-Phase Handoff Conditions

P02 may start only if P01 passes and the harness records all fields needed for
paired feasible-N efficiency: route, N, physical GPU, logical device,
`CUDA_VISIBLE_DEVICES`, TF32 state, timeout status, finite output, bounded
output-comparability summaries, warm-call timings, GPU memory before/after, and
low-rank route-fired evidence.

## Stop Conditions

- `LOW_RANK_LEDH_EFFICIENCY_BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED`
- `LOW_RANK_LEDH_EFFICIENCY_NOT_SUPPORTED_CURRENT_EVIDENCE`
- Harness cannot fairly run both routes at small sanity size.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write the P01 result/close record.
3. Draft or refresh P02 subplan.
4. Review P02 for consistency, correctness, feasibility, artifact coverage, and boundary safety.
