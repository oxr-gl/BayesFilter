# DPF V2 Algorithm Full Comparison P5 LEDH-PFPF-OT Contracts Subplan

metadata_date: 2026-06-07
phase: P5
status: REVIEWED_READY_FOR_PHASE_EXECUTION_AFTER_P4_PASS

## Question

Can we freeze executable LEDH-PFPF-OT contracts for all six V2 rows, including
proposal-flow, PF-PF correction, Jacobian/logdet, and OT semantics, before
seeing value or gradient results?

## Inputs

- P0 governance result.
- P1 architecture result.
- P4 bootstrap-OT gradient result.
- V2 common model contracts.
- BayesFilter LEDH-PFPF-OT implementation.
- FilterFlow proposal/resampling interfaces.

## Evidence Contract

Primary criterion:

- Write one frozen LEDH-PFPF-OT contract per V2 row.
- Each contract states:
  - pre-flow transition proposal;
  - LEDH linearization point and Jacobian function;
  - LEDH affine map and forward log-determinant convention;
  - proposal log density route;
  - target transition density route;
  - observation density route;
  - PF-PF corrected log-weight equation;
  - fixed ESS trigger mask and OT settings;
  - physical gradient knobs and parameterization.

Veto diagnostics:

- any LEDH map is not differentiable for a required row without reviewed
  classification;
- any proposal log density or logdet convention is ambiguous;
- FF adapter cannot implement `ProposalModelBase.propose` and `loglikelihood`
  semantics without mutating `.localsource/filterflow`;
- any row missing;
- contracts generated after inspecting LEDH value or gradient results;
- any row relies on bootstrap-OT contracts without recording LEDH-specific
  fields.

Explanatory-only diagnostics:

- local linearization residuals;
- Jacobian condition numbers;
- expected corrected-weight dispersion;
- expected transport residual envelope.

Non-claims:

- P5 freezes contracts only; it does not validate LEDH-PFPF-OT values or
  gradients.

Artifacts:

- `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_contracts_2026-06-07.json`
- `experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-ot-contracts-2026-06-07.md`
- P5 result ledger under `docs/plans/`.

## Planned Command

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_ledh_pfpf_ot_contracts_tf
```

## Tasks

1. Derive the LEDH/PF-PF correction equation in repo notation.
2. Implement or inspect FF-side LEDH proposal adapter design.
3. Freeze row contracts and checksums.
4. Validate all six rows have explicit readiness or a stop blocker.
5. Run Claude contract review.

## Exit Criteria

- P5 result declares `PASS_P5_LEDH_PFPF_OT_CONTRACTS_READY_FOR_P6`.

## Stop Conditions

- Any required row cannot state a mathematically unambiguous LEDH/PF-PF
  contract.
- Any required adapter requires `.localsource/filterflow` mutation.
