# DPF Common Model Suite V2 P5 Fixed-Branch Gradients Subplan

metadata_date: 2026-06-07
phase: P5
status: REVIEWED_READY_FOR_PHASE_EXECUTION_WITH_FD_DIAGNOSTIC_ONLY_AMENDMENT

## Question

Do BayesFilter and executable float64 FilterFlow match fixed-branch physical
gradients for each non-blocked v2 row, with same-implementation
finite-difference diagnostics?

## Inputs

- P0 governance result.
- P1 v2 manifest and gradient contracts.
- P2 density result.
- P3 no-resampling path result.
- P4 fixed-ancestor path result.

## Evidence Contract

Primary criterion:

- For every required non-blocked gradient knob, BF and FF scalar values and
  AD gradients match within declared tolerance.
- Execution only touches knobs frozen ready by the prior reviewed gradient
  classification table or amendment.

Veto diagnostics:

- gradient knob changed after seeing results;
- parameterization mismatch between BF and FF;
- nonfinite gradient or scalar;
- gradient through random ancestor selection is claimed;
- a value match is used to excuse a derivative mismatch.
- any runner uses old v1 artifact names or the old three-row
  `common_model_specs()` API as its v2 source;
- any SIR or predator-prey gradient adapter cannot certify exact equality to
  the P1 no-lookup semantics before execution.

Explanatory-only diagnostics:

- central finite-difference gradients, AD-vs-FD deltas, and FD ladders;
- FD pass/fail booleans retained for historical interpretability;
- historical disconnected-zero-gradient FD guard records.

Finite differences are numerically fragile and are not a P5 promotion gate.
Row status depends only on BF/FF scalar equality, BF/FF AD-gradient equality,
and finiteness of executed scalar/AD values; FD is retained only for diagnosis
and explanation.

Non-claims:

- fixed-branch gradient agreement is not a full stochastic-filter gradient
  correctness proof and not proof of scientific validity.

Artifacts:

- `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_gradients_2026-06-07.json`
- `experiments/dpf_implementation/reports/dpf-common-model-suite-v2-gradients-2026-06-07.md`
- P5 result ledger under `docs/plans/`.

Required artifact sections:

- `primary_criterion_fields`;
- `veto_diagnostics`;
- `explanatory_only_fields`;
- `review_round`;
- `open_material_blockers`;
- `repair_amendment_required`;
- `next_allowed_action`.

## Required Initial Knob Set

- `lgssm_2d_h25_rich`: transition matrix scale; observation noise scale if the
  adapter route is stable.
- `sv_1d_h18_rich`: `phi`, `sigma`; `mu` if included before results.
- `range_bearing_4d_h20_rich`: `sigma_range`; `sigma_bearing` if included
  before results.
- `structural_ar1_quadratic_h16`: `rho`, `sigma`, and one deterministic
  completion coefficient such as `c`.
- `spatial_sir_j3_rk4`: no required gradient until a reviewed physical-knob
  contract exists for both BF and FF.
- `predator_prey_rk4`: at least one ODE parameter inside `(r,K,a,s,u,v)`.

## Planned Command

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_gradients_tf
```

## Pre-Execution Skeptical Audit

Audit status before launch: PASS after reviewed repair amendment.

The planned P5 evidence answers only the fixed-branch physical-knob gradient
tie-out question for the frozen P1 `READY_FOR_P5` rows. It does not treat
BayesFilter or FilterFlow as an oracle, and it does not execute the P1-blocked
SIR gradient row. The scalar remains the fixed-branch sum of predictive log
normalizers with fixed additive transition innovations and fixed ancestor
indices. Central finite differences are explanatory-only diagnostics for each
implementation, not a promotion gate.

Pre-execution audit found that some physical transition-scale knobs can be
inactive under the frozen additive-innovation scalar. The earlier reviewed
disconnected-zero-gradient repair amendment is superseded by the FD
diagnostic-only amendment wherever it used an FD-zero or FD-nonzero check as a
promotion or veto condition. If an included required knob has a disconnected AD
gradient under the frozen scalar, that row/knob must be resolved by predeclared
contract classification, derivation, or reviewed exclusion/blocking, not by an
FD pass/fail check. This does not change fixtures, scalar, branch, tolerances,
or P1 classifications.

## Tasks

1. Implement fixed-branch gradient replay from declarative v2 contracts.
2. Preflight fail if the runner imports the old three-row v1 API as its v2
   source or writes old 2026-06-06 artifact names.
3. Compare BF and FF scalar values and gradients.
4. Run central finite-difference diagnostics.
5. Classify excluded knobs before result inspection.
6. Run Claude result/governance review.

## Exit Criteria

- All required non-blocked BF/FF scalars and AD gradients match, or rows are
  explicitly classified.

## Stop Conditions

- Correct gradient semantics require changing the v2 scalar, branch, or model
  contract.
