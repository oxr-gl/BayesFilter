# DPF V2 Algorithm Full Comparison P3 Bootstrap-OT Values Subplan

metadata_date: 2026-06-07
phase: P3
status: REVIEWED_READY_FOR_PHASE_EXECUTION_AFTER_P2_PASS

## Question

Do BayesFilter and FilterFlow-side adapters match bootstrap-OT fixed-branch
values and ledgers for all six V2 rows?

## Inputs

- P0 governance result.
- P1 architecture result.
- P2 bootstrap-OT frozen contracts.

## Evidence Contract

Primary criterion:

- For every V2 row, BF and FF bootstrap-OT scalar values match within declared
  tolerance.
- Required ledgers match: initial particles, predicted particles,
  observation log densities, unnormalized log weights, normalized log weights,
  ESS trigger masks, OT transport matrix summary/checksum, post-transport
  particles, incremental log normalizers, and final scalar.

Veto diagnostics:

- nonfinite scalar or ledger field;
- runtime branch mask differs from the frozen P2 mask;
- transport settings differ from P2;
- BF/FF value delta exceeds tolerance;
- unclassified ledger mismatch.

Explanatory-only diagnostics:

- ESS trajectories;
- filtered mean/variance;
- transport residuals;
- runtime;
- optional stochastic smoke values.

Non-claims:

- P3 does not establish bootstrap-OT gradient agreement.
- P3 does not establish stochastic resampling distribution correctness.

Artifacts:

- `experiments/dpf_implementation/reports/outputs/dpf_v2_bootstrap_ot_values_2026-06-07.json`
- `experiments/dpf_implementation/reports/dpf-v2-bootstrap-ot-values-2026-06-07.md`
- P3 result ledger under `docs/plans/`.

## Planned Command

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_bootstrap_ot_values_tf
```

## Tasks

1. Run BF and FF bootstrap-OT fixed-branch value paths from P2 contracts.
2. Compare primary scalar and ledgers.
3. Classify every mismatch before any tolerance or contract change.
4. Run Claude result/governance review.

## Exit Criteria

- P3 result declares `PASS_P3_BOOTSTRAP_OT_VALUES_READY_FOR_P4`.

## Stop Conditions

- Any V2 row cannot execute without changing V2 semantics.
- Any unclassified value or ledger mismatch remains.
