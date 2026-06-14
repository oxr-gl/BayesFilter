# DPF V2 Algorithm Full Comparison P4 Bootstrap-OT Gradients Subplan

metadata_date: 2026-06-07
phase: P4
status: REVIEWED_READY_FOR_PHASE_EXECUTION_AFTER_P3_PASS

## Question

Do BayesFilter and FilterFlow-side adapters match bootstrap-OT fixed-branch AD
gradients for all required physical knobs across all six V2 rows?

## Inputs

- P0 governance result.
- P1 architecture result.
- P2 bootstrap-OT contracts.
- P3 bootstrap-OT value result.

## Evidence Contract

Primary criterion:

- For every required physical knob in every V2 row, BF and FF scalar values and
  AD gradients match within declared tolerance.
- Gradients are through the deterministic fixed-branch value path, including
  FilterFlow-style OT transport when triggered, but excluding random seeds,
  random sampling, and Boolean trigger decisions.

Veto diagnostics:

- nonfinite scalar or gradient;
- BF/FF scalar mismatch;
- BF/FF AD-gradient mismatch;
- gradient knob changed after seeing results;
- FD used as promotion gate;
- disconnected gradient classified after result inspection rather than through
  predeclared contract logic.

Explanatory-only diagnostics:

- central FD ladders;
- AD-vs-FD deltas within each implementation;
- gradient norm summaries;
- transport-gradient upstream summaries.

Finite differences are diagnostic-only and cannot promote or fail a row unless
the phase has a separate reviewed amendment making a specific FD pathology a
veto for implementation-health reasons.

Non-claims:

- P4 does not establish full stochastic-filter gradient correctness.

Artifacts:

- `experiments/dpf_implementation/reports/outputs/dpf_v2_bootstrap_ot_gradients_2026-06-07.json`
- `experiments/dpf_implementation/reports/dpf-v2-bootstrap-ot-gradients-2026-06-07.md`
- P4 result ledger under `docs/plans/`.

## Planned Command

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_bootstrap_ot_gradients_tf
```

## Tasks

1. Load P2 contracts and P3 matched value ledgers.
2. Run BF and FF gradient tapes over the same fixed branch.
3. Compare scalars and AD gradients.
4. Record FD diagnostics separately.
5. Run Claude result/governance review.

## Exit Criteria

- P4 result declares `PASS_P4_BOOTSTRAP_OT_GRADIENTS_READY_FOR_P5`.

## Stop Conditions

- Correct gradient semantics require changing branch, scalar, model, or OT
  contract.
