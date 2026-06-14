# DPF Common Model Suite V2 P3 No-Resampling Paths Subplan

metadata_date: 2026-06-07
phase: P3
status: REVIEWED_READY_FOR_PHASE_EXECUTION

## Question

Do BayesFilter and executable float64 FilterFlow match on deterministic
fixed-noise no-resampling filter-path values and ledgers for each non-blocked
v2 row?

## Inputs

- P0 governance result.
- P1 v2 manifest and path contracts.
- P2 density result.

## Evidence Contract

Primary criterion:

- For every non-blocked row, the scalar sum of per-step predictive
  log-normalizers and the per-step ledger match within declared tolerance.
- Execution only touches rows frozen ready by the prior reviewed
  classification table or amendment.

Veto diagnostics:

- hidden RNG use in transition propagation;
- stochastic resampling;
- changed initial particles, observations, innovations, scalar definition, or
  horizon after seeing results;
- nonfinite log weights or ledger values;
- treating ESS or filtered means as promotion criteria.
- any runner uses old v1 artifact names or the old three-row
  `common_model_specs()` API as its v2 source.

Non-claims:

- no stochastic resampling correctness, no random-number-generator equality,
  and no filtering correctness proof.

Artifacts:

- `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_noresampling_2026-06-07.json`
- `experiments/dpf_implementation/reports/dpf-common-model-suite-v2-noresampling-2026-06-07.md`
- P3 result ledger under `docs/plans/`.

Required artifact sections:

- `primary_criterion_fields`;
- `veto_diagnostics`;
- `explanatory_only_fields`;
- `review_round`;
- `open_material_blockers`;
- `repair_amendment_required`;
- `next_allowed_action`.

## Planned Command

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_noresampling_tf
```

## Tasks

1. Implement a v2 no-resampling runner that consumes only P1 path contracts.
2. Preflight fail if the runner imports the old three-row v1 API as its v2
   source or writes old 2026-06-06 artifact names.
3. Compare scalar, normalized log weights, unnormalized log weights,
   observation log densities, predicted particles, ESS, and filtered moments.
4. Treat ESS and moments as explanatory unless a finite-value veto fails.
5. Report primary, veto, and explanatory fields in distinct top-level sections.
6. Run Claude result/governance review.

## Exit Criteria

- All non-blocked rows match on primary scalar and ledger fields or receive an
  explicit reviewed classification.

## Stop Conditions

- The row cannot be represented by deterministic fixed innovations under the
  declared model without changing the model contract.
