# P37-M3 Result: Spatial SIR First Gate

metadata_date: 2026-06-06
phase: P37-M3

## Decision

Decision: `PASS_M3`.

M3 implements the first source-governed Spatial SIR gate only.  It adds a
clean-room TensorFlow `SpatialSIRSSM` contract with deterministic RK4
transition mean, Gaussian transition density, infectious-coordinate observation
likelihood, seeded simulation, explicit `diagnose_negative_after_noise` domain
policy, and observed/unobserved RMSE diagnostics for small fixture rows.  It
does not implement production TT/SIRT SIR filtering or paper-scale SIR
accuracy.

## Source-Governance Status

- P30 anchors identified: `eq:p27-sir1`--`eq:p27-sir13`, with implementation
  evidence concentrated on state representation, S/I ODEs, RK4 transition,
  Gaussian process noise, infectious-only observation, and RMSE_O/RMSE_U
  diagnostics.
- Zhao--Cui paper anchors identified: spatial SIR benchmark, Section 6.3 and
  Eq. (37) context.
- MATLAB behavioral anchors identified: `eg3_sir/mainscript.m` and
  `deep-tensor.dev/tests/test_sparse_sirt/sir_ll_ftt.m` as audit/reference
  material only.
- BayesFilter code/test anchors identified:
  `bayesfilter/highdim/models.py`,
  `bayesfilter/highdim/validation.py`,
  `bayesfilter/highdim/__init__.py`,
  `tests/highdim/test_p30_spatial_sir.py`, and
  `tests/highdim/test_p30_model_suite_contracts.py`.
- Deviations listed: yes.  This is a BayesFilter first-gate model-contract
  extension, not adaptive MATLAB TT/SIRT behavior.
- Clean-room boundary respected: yes.  The implementation derives from P30
  equations and tests; MATLAB remains reference/audit material.
- Unsupported claims removed: yes.
- Reviewer verdict: `PASS_M3_CODE_GOVERNANCE`.

## Evidence Contract Status

| Field | Status |
|---|---|
| Primary criterion | `PASS_LOCAL`; small `J=1`/`J=3` rows pass transition/domain/observation/likelihood/simulation checks and report observed plus unobserved RMSE diagnostics under a declared one-step transition-mean baseline |
| Veto diagnostics | `PASS_LOCAL`; no silent negative-population clipping, ODE-step mismatch, observed-only diagnostic claim, nonfinite state/likelihood, public API overclaim, or unclassified resource failure observed |
| Explanatory diagnostics | test counts, warning counts, wall time, dirty/untracked workspace status |
| Main uncertainty | model-contract gate only; no nonlinear posterior filtering or rank-ladder evidence |
| Next justified action | M4 predator-prey preconditioning plan gate |
| What is not concluded | no production TT/SIRT SIR filtering, no paper-scale `J=9` accuracy, no rank-ladder evidence, no adaptive MATLAB behavior, no high-dimensional scalability, no HMC/DSGE/GPU readiness, no stable top-level public API |

## Implementation Summary

- Added `SpatialSIRSSM` in `bayesfilter/highdim/models.py`.
- Added `p30_spatial_sir_fixture_model(...)` for small clean-room fixture rows.
- Exported both only from the experimental `bayesfilter.highdim` subpackage.
- Updated the P30 registry row for spatial SIR from `REFERENCE_ONLY` to
  `BAYESFILTER_EXTENSION`, with first-gate-only non-claims.
- Added focused M3 tests and updated the registry guardrail test.
- Updated the traceability ledger row to the first-gate evidence boundary.

## Run Manifest

git commit: `7ccb9c39883471c2d5ec2891cbf33b9ed436bada`

dirty/untracked status:

```text
dirty/untracked workspace; active highdim code, tests, and P30 plan files are
untracked in this repository state.
```

environment: `/home/chakwong/anaconda3/envs/tf-gpu`

CPU/GPU status:

```text
deliberate CPU-only tests; CUDA_VISIBLE_DEVICES=-1 set in pytest commands.
No GPU claim is made.
```

dtype: `tf.float64`

random seeds:

```text
3703 for replayable SIR simulation smoke; 3704 for synthetic-truth RMSE
diagnostic row.
```

focused command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_spatial_sir.py
```

result:

```text
7 passed, 2 warnings in 2.85s
```

focused registry/public API command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_spatial_sir.py \
  tests/highdim/test_p30_model_suite_contracts.py \
  tests/test_v1_public_api.py
```

result:

```text
21 passed, 2 warnings in 3.64s
```

broad highdim guardrail command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/test_v1_public_api.py \
  tests/highdim/test_phase0_contracts.py \
  tests/highdim/test_bases.py \
  tests/highdim/test_tt_algebra.py \
  tests/highdim/test_squared_tt_density.py \
  tests/highdim/test_transport.py \
  tests/highdim/test_fixed_branch_fit.py \
  tests/highdim/test_failure_exits.py \
  tests/highdim/test_filtering_kalman_exact.py \
  tests/highdim/test_fixed_branch_derivatives.py \
  tests/highdim/test_scaling_smoke.py \
  tests/highdim/test_public_api_highdim.py \
  tests/highdim/test_p30_model_suite_contracts.py \
  tests/highdim/test_p30_lgssm_exact_reference.py \
  tests/highdim/test_p30_stochastic_volatility.py \
  tests/highdim/test_p30_sv_fixed_design_tt_target.py \
  tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py \
  tests/highdim/test_p30_sv_short_sequential_tt_value_path.py \
  tests/highdim/test_p30_spatial_sir.py
```

result:

```text
152 passed, 2 warnings in 14.66s
```

compile command:

```bash
python -m compileall -q bayesfilter/highdim tests/highdim
```

result:

```text
passed
```

whitespace command:

```bash
git diff --check -- \
  bayesfilter/highdim/models.py \
  bayesfilter/highdim/__init__.py \
  bayesfilter/highdim/validation.py \
  tests/highdim/test_p30_spatial_sir.py \
  tests/highdim/test_p30_model_suite_contracts.py \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase3-spatial-sir-subplan-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase3-spatial-sir-claude-review-ledger-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

result:

```text
passed
```

file-content whitespace command:

```bash
grep -n '[[:blank:]]$' \
  bayesfilter/highdim/models.py \
  bayesfilter/highdim/__init__.py \
  bayesfilter/highdim/validation.py \
  tests/highdim/test_p30_spatial_sir.py \
  tests/highdim/test_p30_model_suite_contracts.py \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase3-spatial-sir-subplan-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase3-spatial-sir-claude-review-ledger-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

result:

```text
passed; no trailing whitespace matches were reported.  The command returned
exit status 1 because grep found no matches.
```

output artifacts:

```text
bayesfilter/highdim/models.py
bayesfilter/highdim/__init__.py
bayesfilter/highdim/validation.py
tests/highdim/test_p30_spatial_sir.py
tests/highdim/test_p30_model_suite_contracts.py
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase3-spatial-sir-subplan-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase3-spatial-sir-claude-review-ledger-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase3-spatial-sir-result-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

## Failure And Repair Log

failed attempt:

```text
After the SIR registry row was promoted from REFERENCE_ONLY to
BAYESFILTER_EXTENSION, the existing registry guardrail failed:
tests/highdim/test_p30_model_suite_contracts.py::test_reference_only_models_are_not_bayesfilter_evidence.
```

blocker classification:

```text
fixable test-contract update.  The reviewed M3 plan explicitly required
registry promotion after BayesFilter-native first-gate evidence.  The old test
still assumed SIR was unimplemented.
```

repair:

```text
Removed `spatial_sir` from the reference-only loop and added a dedicated
`test_spatial_sir_registry_records_first_gate_extension_boundary` assertion set
that checks the new first-gate boundary and non-claims.
```

rerun evidence:

```text
Focused M3 plus registry/public API checks passed with 21 tests.  Broad highdim
guardrail passed with 152 tests.  Compile and whitespace checks passed.
```

## Decision Table

| Field | Status |
|---|---|
| Decision | `PASS_M3` |
| Primary criterion status | `PASS_LOCAL` |
| Veto diagnostic status | `PASS_LOCAL` |
| Strongest uncertainty | first-gate model-contract evidence only; no filtering/rank/scalability evidence |
| Next justified action | M4 predator-prey preconditioning plan gate |
| Non-claims | no production TT/SIRT SIR filtering, no paper-scale `J=9`, no rank ladder, no adaptive MATLAB behavior, no high-dimensional scalability, no HMC/DSGE/GPU readiness, no stable top-level public API |

## Post-Run Red Team

Strongest alternative explanation:

- The new SIR tests may be persuasive because they use P30 settings, but they
  only establish model-contract behavior.  They do not prove posterior
  filtering quality.

What would overturn promotion:

- Claude identifies a mismatch between the RK4/observation implementation and
  P30 equations;
- a reviewer judges the registry status too strong for a first gate;
- broad highdim guardrails regress;
- traceability wording overclaims filtering, paper-scale, or scalability
  evidence.

Weakest evidence:

- The synthetic-truth RMSE row uses deterministic one-step transition means as
  a declared diagnostic baseline.  It is not posterior filtering accuracy.
