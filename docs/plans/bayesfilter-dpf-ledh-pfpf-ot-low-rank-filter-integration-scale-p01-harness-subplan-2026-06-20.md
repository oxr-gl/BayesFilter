# P01 Harness Implementation And Small CPU Invariants Subplan

Status: `DRAFT_AFTER_P00`

## Phase Objective

Create a lane-owned TensorFlow benchmark harness that embeds the low-rank
solver route inside an LEDH/PFPF-OT filter-shaped loop, then validate small CPU
invariants without dense scale materialization.  The active-resampling row must
prove that the low-rank route actually fired inside the filter loop.

## Entry Conditions Inherited From Previous Phase

P00 must have passed plan/review gates.  Owned-file and non-claim boundaries
remain binding.  The integration harness must be lane-owned and must not change
BayesFilter public exports, defaults, shared schema, or shared ledger files.

## Required Artifacts

- Harness:
  `docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_integration_smoke.py`
- Tests:
  `tests/test_low_rank_ledh_pfpf_integration_smoke.py`
- Small JSON:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-small-2026-06-20.json`
- Small Markdown:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-small-2026-06-20.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p01-harness-result-2026-06-20.md`
- Log:
  `docs/benchmarks/logs/low-rank-ledh-pfpf-integration-p01-small.log`

## Required Checks, Tests, And Reviews

- `python -m py_compile docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_integration_smoke.py`
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_low_rank_ledh_pfpf_integration_smoke.py -q`
- Small CPU harness command in `--mode small`.
- Artifact inspection that active rows include
  `low_rank_resampling_invocations > 0` and
  `low_rank_resampling_invocations == active_resampling_mask_count`.
- Read-only Claude review if implementation or result has material boundary or evidence issues.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the owned harness faithfully exercise LEDH flow, log-density correction, ESS/moment output, and low-rank resampling while preserving lane boundaries? |
| Baseline/comparator | Existing LEDH/PFPF-OT LGSSM fixture shape and value recursion mechanics; no-resampling parity against the harness's no-transport branch. |
| Primary pass criterion | Tests pass; small active-resampling harness returns finite outputs, proves low-rank route execution with invocation count equal to active mask count, has no hard vetoes under the master fixed-threshold table, has valid low-rank factor diagnostics, has normalized log weights, and uses no scale-mode dense transport matrix. |
| Veto diagnostics | Import failure, shape mismatch, missing/zero low-rank invocation evidence for active rows, invocation count mismatch, nonfinite outputs, negative factors, nonpositive `g`, factor/induced residual above the master fixed thresholds, dense transport matrix materialized outside tiny invariant logic, missing artifacts, or forbidden shared edits. |
| Explanatory diagnostics | ESS, filtered mean/variance ranges, moment deltas, runtime, memory, and tiny materialized apply parity if used only at tiny scale. |
| Not concluded | No speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or TF32-help claim. |
| Artifact | P01 JSON/Markdown/result/log. |

## Forbidden Claims And Actions

- Do not edit public exports/defaults/package metadata.
- Do not use POT, external solvers, network, package installs, or positive-feature lane evidence.
- Do not claim dense Sinkhorn equivalence from small tests.
- Do not claim actual 50k/100k viability from P01.

## Exact Next-Phase Handoff Conditions

P02 may start only if the harness and tests exist, py_compile and pytest pass,
the small CPU active-resampling harness artifact reports `PASS`, records
`low_rank_resampling_invocations > 0`, records invocation count equal to active
mask count, and P01 result records the selected seed tuning grid for P02.

## Stop Conditions

- `LOW_RANK_FILTER_INTEGRATION_SCALE_BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED`
- `LOW_RANK_FILTER_INTEGRATION_SCALE_FAILED_TUNING_OR_VALIDITY`
- Harness cannot exercise LEDH flow/density loop without modifying shared contracts.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write the P01 result/close record.
3. Draft or refresh P02 subplan.
4. Review P02 for consistency, correctness, feasibility, artifact coverage, and boundary safety.
