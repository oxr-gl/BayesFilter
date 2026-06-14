# DPF V2 Algorithm Full Comparison P7 LEDH-PFPF-OT Gradients Subplan

metadata_date: 2026-06-07
phase: P7
status: REVIEWED_READY_FOR_PHASE_EXECUTION_AFTER_P6_PASS

## Question

Do BayesFilter and FilterFlow-side adapters match LEDH-PFPF-OT fixed-branch AD
gradients for all required physical knobs across all six V2 rows?

## Inputs

- P0 governance result.
- P1 architecture result.
- P5 LEDH-PFPF-OT contracts.
- P6 LEDH-PFPF-OT value result.

## Evidence Contract

Primary criterion:

- For every required physical knob in every V2 row, BF and FF scalar values and
  AD gradients match within declared tolerance.
- Gradients are through the deterministic fixed-branch LEDH proposal, PF-PF
  correction, and FilterFlow-style OT transport when triggered.
- Gradients do not pass through random seeds, random sampling, Boolean trigger
  decisions, or any discrete ancestor choice.

Veto diagnostics:

- nonfinite scalar or gradient;
- BF/FF scalar mismatch;
- BF/FF AD-gradient mismatch;
- logdet/proposal-density gradient route mismatch;
- gradient knob changed after seeing results;
- FD used as promotion gate;
- value agreement used to excuse derivative mismatch.

Explanatory-only diagnostics:

- FD ladders and AD-vs-FD deltas;
- gradient norm summaries;
- per-component VJP summaries for LEDH map, PF-PF correction, and OT transport;
- local linearization residuals.

Finite differences are diagnostic-only. A row cannot pass because FD is close,
and a row cannot fail solely because FD is noisy, unless a reviewed amendment
defines a specific implementation-health veto before result inspection.

Non-claims:

- P7 does not establish gradients through stochastic resampling distribution or
  random/discrete branch selection.

Artifacts:

- `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_gradients_2026-06-07.json`
- `experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-ot-gradients-2026-06-07.md`
- P7 result ledger under `docs/plans/`.

## Planned Command

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_ledh_pfpf_ot_gradients_tf
```

## Tasks

1. Load P5 contracts and P6 matched value ledgers.
2. Run BF and FF gradient tapes over the same fixed branch.
3. Compare scalars and AD gradients.
4. Record FD and VJP diagnostics separately.
5. Run Claude result/governance review.

## Exit Criteria

- P7 result declares `PASS_P7_LEDH_PFPF_OT_GRADIENTS_READY_FOR_P8`.

## Stop Conditions

- Correct gradient semantics require changing LEDH proposal, PF-PF correction,
  branch, scalar, model, or OT contract.
