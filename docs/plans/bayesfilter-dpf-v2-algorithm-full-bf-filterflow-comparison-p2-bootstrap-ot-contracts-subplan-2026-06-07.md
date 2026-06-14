# DPF V2 Algorithm Full Comparison P2 Bootstrap-OT Contracts Subplan

metadata_date: 2026-06-07
phase: P2
status: REVIEWED_READY_FOR_PHASE_EXECUTION_AFTER_P1_PASS

## Question

Can we freeze executable bootstrap-OT comparison contracts for all six V2
models before seeing value or gradient results?

## Inputs

- P0 governance result.
- P1 architecture result.
- V2 common model manifest.

## Evidence Contract

Primary criterion:

- Write one frozen bootstrap-OT contract per V2 row.
- Each contract includes model parameters, observations, initial particles,
  transition innovations, fixed ESS trigger mask, OT settings, scalar
  definition, gradient knobs, dtype, tolerance, and checksums.
- Both BF and FF execution paths must consume the same contract bytes.

Veto diagnostics:

- any contract generated after inspecting bootstrap-OT value or gradient
  results;
- any row missing;
- any stochastic sampling not represented by fixed initial particles or fixed
  additive innovations;
- any Boolean trigger decision left to runtime in primary fixed-branch evidence;
- any tolerance or gradient knob inherited without being recorded.

Explanatory-only diagnostics:

- expected ESS levels under the frozen branch;
- expected transport residual envelopes;
- optional stochastic smoke commands for later diagnostics.

Non-claims:

- P2 freezes contracts only; it does not validate values or gradients.

Artifacts:

- `experiments/dpf_implementation/reports/outputs/dpf_v2_bootstrap_ot_contracts_2026-06-07.json`
- `experiments/dpf_implementation/reports/dpf-v2-bootstrap-ot-contracts-2026-06-07.md`
- P2 result ledger under `docs/plans/`.

## Planned Command

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_bootstrap_ot_contracts_tf
```

## Tasks

1. Implement or run a contract-freezing runner.
2. Ensure it fails if any V2 row is absent.
3. Ensure it fails if old v1 artifact names are used.
4. Validate contract checksums are stable across reruns.
5. Run Claude contract review.

## Exit Criteria

- P2 result declares `PASS_P2_BOOTSTRAP_OT_CONTRACTS_READY_FOR_P3`.

## Stop Conditions

- A row cannot be given a fixed-branch bootstrap-OT contract without changing
  the V2 model semantics.
