# DPF V2 Algorithm Full Comparison P6 LEDH-PFPF-OT Values Subplan

metadata_date: 2026-06-07
phase: P6
status: REVIEWED_READY_FOR_PHASE_EXECUTION_AFTER_P5_PASS

## Question

Do BayesFilter and FilterFlow-side adapters match LEDH-PFPF-OT fixed-branch
values and ledgers for all six V2 rows?

## Inputs

- P0 governance result.
- P1 architecture result.
- P5 LEDH-PFPF-OT contracts.

## Evidence Contract

Primary criterion:

- For every V2 row, BF and FF LEDH-PFPF-OT scalar values match within declared
  tolerance.
- Required ledgers match: pre-flow proposals, LEDH affine parameters,
  post-flow particles, pre-flow proposal log density, forward logdet, target
  transition log density, observation log density, PF-PF corrected log weights,
  ESS trigger masks, OT transport matrix summary/checksum, post-transport
  particles, incremental log normalizers, and final scalar.

Veto diagnostics:

- nonfinite proposal, logdet, corrected weight, scalar, or transport field;
- BF/FF scalar mismatch;
- PF-PF correction equation mismatch;
- runtime branch mask differs from P5;
- unclassified ledger mismatch.

Explanatory-only diagnostics:

- corrected-weight dispersion;
- LEDH local-linearization residuals;
- Jacobian condition numbers;
- ESS trajectories;
- transport residuals;
- runtime.

Non-claims:

- P6 does not establish LEDH-PFPF-OT gradient agreement.
- P6 does not prove LEDH proposal optimality or filtering correctness.

Artifacts:

- `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_values_2026-06-07.json`
- `experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-ot-values-2026-06-07.md`
- P6 result ledger under `docs/plans/`.

## Planned Command

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_ledh_pfpf_ot_values_tf
```

## Tasks

1. Run BF and FF LEDH-PFPF-OT fixed-branch value paths from P5 contracts.
2. Compare primary scalar and ledgers.
3. Classify every mismatch before any tolerance or contract change.
4. Run Claude result/governance review.

## Exit Criteria

- P6 result declares `PASS_P6_LEDH_PFPF_OT_VALUES_READY_FOR_P7`.

## Stop Conditions

- Any V2 row cannot execute without changing P5 contract semantics.
- Any unclassified value or ledger mismatch remains.
