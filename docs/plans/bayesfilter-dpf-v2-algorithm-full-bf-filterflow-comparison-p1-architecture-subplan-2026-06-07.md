# DPF V2 Algorithm Full Comparison P1 Architecture Subplan

metadata_date: 2026-06-07
phase: P1
status: REVIEWED_READY_FOR_PHASE_EXECUTION

## Question

Can BayesFilter and FilterFlow-side adapters host the two target algorithms over
all six V2 models without mutating `.localsource/filterflow`?

## Inputs

- P0 governance result.
- `common_model_suite_tf.py` V2 contracts.
- BayesFilter bootstrap-OT and LEDH-PFPF-OT code.
- Local FilterFlow SMC, proposal, transition, observation, criterion, and
  `RegularisedTransform` interfaces.

## Evidence Contract

Primary criterion:

- Freeze an architecture matrix with one row per V2 model and algorithm:
  bootstrap-OT BF, bootstrap-OT FF adapter, LEDH-PFPF-OT BF, LEDH-PFPF-OT FF
  adapter.
- For every cell, record implementation path, model equations source, proposal
  semantics, log-density route, OT route, gradient route, and readiness status.
- Confirm FilterFlow-side adapters live under BayesFilter-owned experiment code
  and import FilterFlow interfaces without modifying `.localsource/filterflow`.

Veto diagnostics:

- any planned adapter mutates `.localsource/filterflow`;
- LEDH proposal density or Jacobian/logdet semantics are not stated;
- FilterFlow adapter uses a different state convention, observation route,
  covariance, angle-wrap, RK4 step, structural completion, or parameterization;
- architecture matrix omits a V2 row;
- bootstrap-OT and LEDH-PFPF-OT surfaces are conflated.

Explanatory-only diagnostics:

- native FilterFlow support versus adapter-hosted support;
- expected implementation size;
- anticipated SIR/predator-prey Jacobian complexity.

Non-claims:

- P1 does not establish numerical agreement.

Artifacts:

- `experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_p1_architecture_2026-06-07.json`
- `experiments/dpf_implementation/reports/dpf-v2-algorithm-full-comparison-p1-architecture-2026-06-07.md`
- P1 result ledger under `docs/plans/`.

## Tasks

1. Inventory FilterFlow interfaces needed for bootstrap-OT and LEDH-PFPF-OT.
2. Specify BayesFilter-owned FilterFlow adapters:
   - generic V2 transition adapter;
   - generic V2 observation adapter;
   - bootstrap proposal adapter or native `BootstrapProposalModel` path;
   - LEDH proposal adapter implementing `propose` and `loglikelihood`;
   - branch-mask and fixed-noise replay adapter;
   - gradient tape wrapper.
3. Specify code paths for BF execution.
4. Specify exact fields in the architecture JSON matrix.
5. Run Claude architecture review.

## Exit Criteria

- P1 result declares `PASS_P1_ARCHITECTURE_READY_FOR_P2`.

## Stop Conditions

- Full comparison requires mutating `.localsource/filterflow`.
- LEDH proposal correction cannot be specified in the repo notation.
