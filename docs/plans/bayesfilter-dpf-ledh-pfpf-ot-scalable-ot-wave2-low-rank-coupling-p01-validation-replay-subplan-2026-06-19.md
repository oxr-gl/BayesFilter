# W2-LR-1 Subplan: Validation Implementation And Replay

Date: 2026-06-19
Owner: peer agent

## Status

`DRAFT_READY_AFTER_P00`

## Phase Objective

Implement and run a Wave 2 lane-owned validation diagnostic for the existing
TensorFlow low-rank coupling solver-route candidate, then run focused tests and
artifact checks.

## Entry Conditions Inherited From Previous Phase

- W2-LR-0 passed governance/intake.
- Peer-agent write set is lane-local and excludes positive-feature artifacts.
- P12 low-rank solver-route implementation exists as the algorithm under
  validation.
- Non-claims and source-route classification boundaries are fixed.

## Required Artifacts

- `docs/benchmarks/scalable_ot_wave2_low_rank_coupling_validation.py`
- `tests/test_wave2_low_rank_coupling_validation.py`
- `docs/benchmarks/scalable-ot-wave2-low-rank-coupling-validation-2026-06-19.json`
- `docs/benchmarks/scalable-ot-wave2-low-rank-coupling-validation-2026-06-19.md`
- W2-LR-1 result/close record.

## Required Checks, Tests, And Reviews

- `CUDA_VISIBLE_DEVICES=-1 python -m py_compile ...`
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_low_rank_coupling_solver_tf.py tests/test_wave2_low_rank_coupling_validation.py`
- `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_wave2_low_rank_coupling_validation.py ...`
- JSON schema and status check.
- Forbidden claim/action scan over Wave 2 low-rank artifacts.

Claude review is optional read-only review only.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the low-rank coupling solver-route candidate pass a Wave 2 hard-veto validation screen under CPU-only TensorFlow replay? |
| Baseline/comparator | P12 diagnostic result is entry context; Phase 1 dense/streaming baseline is context only and not a promotion comparator. |
| Primary pass criterion | Validation JSON status is `PASS`; hard vetoes are empty; candidate record validates under Phase 3 schema; fixture rows have finite particles/factors, nonnegative `Q,R`, positive `g`, residuals below `5e-3`, and materialized apply parity below `1e-10`; source-route classification remains weakest-route `extension_or_invention`. |
| Veto diagnostics | Compile/test/diagnostic failure, invalid JSON/schema, nonfinite values, negative factors, nonpositive `g`, residual/parity failure, source-route overclaim, positive-feature evidence use, external solver execution, GPU evidence, package/network requirement, or public/shared edit. |
| Explanatory diagnostics | Rank, fixture shape, projection iterations, projection error, floor hits, factor minima, runtime, and memory proxy. |
| Not concluded | No speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or full solver fidelity. |

## Forbidden Claims And Actions

- Do not edit the solver implementation unless validation exposes a peer-lane
  hard issue requiring a focused fix.
- Do not import or execute POT/OTT/external solvers.
- Do not use GPU evidence or package/network operations.
- Do not edit positive-feature lane files, shared schema, public exports, or
  coordinator records.

## Exact Next-Phase Handoff Conditions

Advance to W2-LR-2 only if W2-LR-1 checks pass, JSON/Markdown diagnostics exist,
the result record is written, and no unresolved hard veto or shared-boundary
blocker remains.

## Stop Conditions

Stop with `LOW_RANK_COUPLING_VALIDATION_BLOCKED` if the validation cannot
produce finite nonnegative `Q,R,g` and transported particles without forbidden
actions.  Stop with `BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED` if a shared
schema, baseline, public export/default, or coordinator contract must change.
