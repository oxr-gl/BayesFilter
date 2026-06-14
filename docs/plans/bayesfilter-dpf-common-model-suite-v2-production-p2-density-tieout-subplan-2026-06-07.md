# DPF Common Model Suite V2 P2 Density Tie-Out Subplan

metadata_date: 2026-06-07
phase: P2
status: REVIEWED_READY_FOR_PHASE_EXECUTION

## Question

Do BayesFilter and executable float64 FilterFlow evaluate the same v2 initial,
transition, observation, and scalar density components for each non-blocked row?

## Inputs

- P0 governance result.
- P1 v2 manifest and declarative specs.
- FilterFlow reference policy and branch marker.

## Evidence Contract

Primary criterion:

- For every non-blocked v2 row, BayesFilter and FilterFlow density components
  match within the P1-declared tolerance.
- Execution only touches rows frozen as `READY_FOR_P2` in the P1 pre-run row
  classification table.

Veto diagnostics:

- missing FilterFlow subprocess environment;
- FilterFlow adapter implements a different equation than the v2 spec;
- any nonfinite density component;
- any density probe changed after seeing results without reviewed amendment;
- any v2 row silently omitted from the report.
- any SIR or predator-prey FilterFlow adapter cannot certify exact equality to
  the P1 no-lookup adapter semantics before execution;
- any runner uses old v1 artifact names or the old three-row
  `common_model_specs()` API as its v2 source.

Non-claims:

- density agreement is not full filter-path agreement and is not correctness
  proof.

Artifacts:

- `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_density_2026-06-07.json`
- `experiments/dpf_implementation/reports/dpf-common-model-suite-v2-density-2026-06-07.md`
- P2 result ledger under `docs/plans/`.

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
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_density_tf
```

## Tasks

1. Implement a v2 density runner using the P1 declarative contracts.
2. Preflight fail if the runner imports the old three-row v1 API as its v2
   source or writes old 2026-06-06 artifact names.
3. Run BayesFilter density evaluation from the v2 model adapter.
4. Run FilterFlow density evaluation in a CPU-only subprocess without mutating
   `.localsource/filterflow`.
5. Classify each row as `MATCHED`, `EXPLAINED_MISMATCH`,
   `INTERFACE_BLOCKED`, `CONTRACT_BLOCKED`, or
   `SCIENTIFIC_CONTRACT_BLOCKED`.
6. Run Claude result/governance review.

## Exit Criteria

- All required non-blocked rows match or every non-match is scientifically
  classified with evidence.
- No row status changed after P1 classification without reviewed amendment.
- Claude review returns PASS or convergence.

## Stop Conditions

- A required row needs `.localsource/filterflow` mutation.
- A mismatch requires changing the scientific contract rather than fixing an
  implementation/adapter error.
