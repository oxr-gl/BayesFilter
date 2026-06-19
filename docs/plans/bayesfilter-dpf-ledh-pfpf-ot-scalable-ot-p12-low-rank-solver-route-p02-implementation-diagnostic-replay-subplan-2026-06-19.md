# P12-2 Subplan: Implementation And Diagnostic Replay

Date: 2026-06-19

## Status

`DRAFT_PENDING_PHASE_P12_1_GATE`

## Phase Objective

Replay the P12 implementation checks and diagnostic command under the locked
evidence contract, preserving the diagnostic-only interpretation.

## Entry Conditions Inherited From Previous Phase

- P12-1 confirmed artifact presence and consistency.
- P12-owned write set remains the only writable surface.
- CPU-only diagnostics and non-claims remain active.

## Required Artifacts

- `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`
- `tests/test_low_rank_coupling_solver_tf.py`
- `docs/benchmarks/scalable_ot_p12_low_rank_solver_route_diagnostics.py`
- refreshed P12 diagnostic JSON/Markdown.
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p02-implementation-diagnostic-replay-result-2026-06-19.md`
- Full command logs under a P12-owned log location if a visible runbook launch
  is later approved.

## Required Checks, Tests, And Reviews

```bash
CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py tests/test_low_rank_coupling_solver_tf.py docs/benchmarks/scalable_ot_p12_low_rank_solver_route_diagnostics.py
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_low_rank_coupling_solver_tf.py
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_p12_low_rank_solver_route_diagnostics.py --output docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.json --markdown-output docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.md
```

Claude read-only review is required for material implementation or diagnostic
diffs after user approval.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the P12 implementation replay still produce finite, nonnegative, Phase 3-valid low-rank factors and transported particles? |
| Baseline/comparator | Phase 1 dense/streaming baseline remains descriptive only; P12 fixture checks are the hard validity gate. |
| Primary pass criterion | Compile passes, unit tests pass, diagnostic command exits 0, JSON validates, hard vetoes are empty, factors/particles are finite, `Q,R >= 0`, `g > 0`, residuals pass thresholds, and tiny apply parity passes. |
| Veto diagnostics | Compile/test/diagnostic failure, invalid JSON, nonfinite or negative factors, nonpositive `g`, invalid transported particles, residual threshold failure, external solver use, GPU evidence, or unsupported claim. |
| Explanatory diagnostics | Dense-reference deltas, runtime, memory, rank, projection iterations, TensorFlow environment warnings. |
| Not concluded | No speedup, ranking, dense Sinkhorn equivalence, posterior correctness, HMC readiness, public API readiness, production/default readiness, or full solver fidelity for extension components. |

Pinned thresholds:

- factor marginal residual `<= 5.0e-3`;
- induced row residual `<= 5.0e-3`;
- induced column residual `<= 5.0e-3`;
- materialized tiny apply parity `<= 1.0e-10`.

These thresholds are inherited from the existing P12 subplan and from
`VALIDITY_THRESHOLD` and `MATERIALIZED_PARITY_THRESHOLD` in
`docs/benchmarks/scalable_ot_p12_low_rank_solver_route_diagnostics.py`.
They must not be changed after seeing replay results.

## Forbidden Claims And Actions

- Do not execute POT/OTT or any external solver.
- Do not install packages, use network, collect GPU evidence, or alter public
  exports.
- Do not promote runtime/memory or dense-reference deltas into pass criteria.
- Do not change thresholds after seeing results.

## Exact Next-Phase Handoff Conditions

Advance to P12-3 only if:

- all local implementation checks pass;
- refreshed diagnostic artifacts preserve diagnostic-only status;
- no hard vetoes fire;
- any repair is P12-owned, visible, and followed by focused reruns.

## Stop Conditions

Stop with `LOW_RANK_SOLVER_ROUTE_BLOCKED` if valid finite nonnegative factors
and transported particles cannot be produced without forbidden actions.

Stop with `BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED` if passing requires a
shared schema, comparator, public API, or other-lane artifact change.

## End-Of-Phase Protocol

At phase end:

1. run required local checks;
2. write the P12-2 result/close record;
3. draft or refresh the P12-3 subplan;
4. review the P12-3 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
