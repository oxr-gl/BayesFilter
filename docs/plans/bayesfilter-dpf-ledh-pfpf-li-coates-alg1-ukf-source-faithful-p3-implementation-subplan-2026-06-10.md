# P3 Subplan: Algorithm 1 Implementation

Date: 2026-06-10

## Status

`DRAFT_FOR_CLAUDE_REVIEW`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter implement Li-Coates Algorithm 1 with UKF prediction/update covariance state in TensorFlow/TFP? |
| Baseline/comparator | P1 documentation, P2 UKF design, Algorithm 1 obligation table in the master program, existing DPF runner architecture only as scaffolding. |
| Primary pass criterion | A TensorFlow/TFP implementation carries per-particle `P_{k-1}^i`, predicts `P^i`, uses `P^i` in LEDH coefficients, updates `P_k^i`, and resamples covariance state consistently. |
| Veto diagnostics | NumPy in differentiable algorithmic path; old auxiliary-flow-only implementation reused as final path; missing route identifiers; covariance not used in coefficients; covariance dropped during resampling; non-finite determinant, weights, particles, or covariances. |
| Explanatory diagnostics | Runtime, ESS, determinant ranges, covariance spectra, old-vs-new row deltas. |
| Not concluded | P3 does not certify faithfulness by itself and does not promote performance tables. |
| Required artifact | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p3-implementation-result-2026-06-10.md` |

## Implementation Scope

Implement in BayesFilter-owned TensorFlow/TFP code.  Use float64 for the
research-grade route unless P2 explicitly justifies another dtype.

The core implementation must be a source-faithful Algorithm 1 filter without OT
first.  If an OT-resampling version is added, it is a BayesFilter extension and
must be labelled separately from the Li-Coates core.

## Required Route Identifiers

Every result row must record:

- `method_generation = li_coates_algorithm1_ukf_covariance_lifecycle`;
- `flow_source_route = li_coates_2017_algorithm1_ledh_pfpf`;
- `covariance_route = per_particle_ukf_prediction_update`;
- `flow_anchor_route = zero_noise_transition` unless a reviewed extension is
  used;
- `resampling_route = none`, `classical_resampling`, or a named BayesFilter OT
  extension;
- `previous_ledh_pfpf_ot_evidence_status = quarantined`.

## Required Tests

1. Import and shape smoke test.
2. Linear-Gaussian collapse for UKF covariance prediction/update.
3. Scalar determinant hand-check for the LEDH pseudo-time product.
4. Nonlinear small fixture proving particle-indexed covariance variation.
5. Resampling ancestry test proving `P_k^i` moves with `x_k^i`.
6. Fixed-branch gradient smoke test, labelled as fixed-branch only.
7. Regression test that the old collapsed/auxiliary-flow-only route cannot be
   selected when `method_generation` claims Algorithm 1.

## Gate

P3 passes only when implementation diffs, test commands, diagnostics, and
Claude read-only review are recorded in the result artifact.

Because P3 is a serious implementation phase, the result artifact must also
include a run manifest with git branch/commit, exact commands, environment,
CPU/GPU status, `CUDA_VISIBLE_DEVICES` status before TensorFlow import, seeds
where applicable, route identifiers, test output paths, plan/result paths, and
wall time.
