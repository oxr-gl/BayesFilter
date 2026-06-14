# DPF Common Model Suite V2 P4 Fixed-Ancestor Paths Subplan

metadata_date: 2026-06-07
phase: P4
status: REVIEWED_READY_FOR_PHASE_EXECUTION

## Question

Do BayesFilter and executable float64 FilterFlow match on fixed-ancestor replay
filter-path values and ledgers for each non-blocked v2 row?

## Inputs

- P0 governance result.
- P1 v2 manifest and fixed-ancestor contracts.
- P2 density result.
- P3 no-resampling path result.

## Evidence Contract

Primary criterion:

- For every non-blocked row, fixed-ancestor branch replay scalars and ledgers
  match within declared tolerance.
- Execution only touches rows frozen ready by the prior reviewed
  classification table or amendment.

Veto diagnostics:

- ancestor arrays or resampling flags changed after seeing results;
- gradient through random or discrete ancestor selection is implied;
- nonfinite scalar or ledger;
- hidden stochastic resampling;
- branch replay differs across BF and FF.
- any runner uses old v1 artifact names or the old three-row
  `common_model_specs()` API as its v2 source.

Non-claims:

- no claim about stochastic ancestor distribution, differentiable resampler
  correctness, or random resampling gradients.

Artifacts:

- `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_fixed_resampling_2026-06-07.json`
- `experiments/dpf_implementation/reports/dpf-common-model-suite-v2-fixed-resampling-2026-06-07.md`
- P4 result ledger under `docs/plans/`.

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
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_fixed_resampling_tf
```

## Pre-Execution Skeptical Audit

Audit status before launch: PASS.

The planned P4 evidence answers only the fixed-ancestor replay question:
whether BayesFilter and the executable local float64 FilterFlow-side adapter
produce matching scalars and primary ledgers under the same frozen P1 v2
contracts. The baseline is the paired implementation output under identical
fixtures, not a correctness oracle. ESS and moments are explanatory only.
The run remains vetoed by any stale v1 fixture leakage, old artifact names,
hidden stochastic resampling, changed ancestor flags or indices, nonfinite
ledger values, missing FilterFlow environment, or mismatch that is not
classified before promotion. This phase does not test gradients, stochastic
resampling distributions, student repositories, TT/SIRT, dense quadrature, or
paper-table correctness.

## Tasks

1. Implement fixed-ancestor replay from declarative v2 contracts.
2. Preflight fail if the runner imports the old three-row v1 API as its v2
   source or writes old 2026-06-06 artifact names.
3. Compare branch-specific particles, weights, scalar increments, and ledgers.
4. Keep ESS/moments explanatory only if reported.
5. Record branch checksums in JSON.
6. Run Claude result/governance review.

## Exit Criteria

- All non-blocked rows match or receive a reviewed classification.

## Stop Conditions

- A row requires stochastic branch semantics rather than fixed branch replay.
