# P37-M4 Result: Predator-Prey First Gate

metadata_date: 2026-06-06
phase: P37-M4

## Decision

Decision: `PASS_M4`.

M4 implements the first source-governed predator-prey gate only.  It adds a
clean-room TensorFlow `PredatorPreySSM` contract with the P30 parameter box,
initial-state prior, deterministic RK4 transition mean, Gaussian transition
density, full-state Gaussian observation likelihood, seeded simulation,
trajectory RMSE diagnostics, and a matched-comparison manifest schema that
blocks unmatched budgets and proxy-only promotion.  It does not implement or
promote nonlinear preconditioning usefulness.

## Source-Governance Status

- P30 anchors identified: `eq:p27-pp1`--`eq:p27-pp8`, with implementation
  evidence concentrated on the predator-prey ODE, parameter box,
  initial-state prior, RK4 discretization, Gaussian transition/observation
  densities, simulation, and first-gate comparison-schema boundary.
- Zhao--Cui paper anchors identified: predator-prey validation example,
  state-space equations (1)--(3), Algorithm 1 context, Section 5,
  Eq. (30)--Eq. (35), and Algorithms 3--5 as later preconditioning comparison
  anchors.
- MATLAB behavioral anchors identified: `eg4_predatorprey/mainscript.m` and
  `models/pre_sol.m` as audit/reference material only.
- BayesFilter code/test anchors identified:
  `bayesfilter/highdim/models.py`,
  `bayesfilter/highdim/validation.py`,
  `bayesfilter/highdim/__init__.py`,
  `tests/highdim/test_p30_predator_prey.py`, and
  `tests/highdim/test_p30_model_suite_contracts.py`.
- Deviations listed: yes.  This is a BayesFilter first-gate model-contract and
  comparison-governance extension, not adaptive MATLAB preconditioning
  behavior.
- Clean-room boundary respected: yes.  The implementation derives from P30
  equations and independent tests; MATLAB remains reference/audit material.
- Unsupported claims removed: yes.
- Reviewer verdict: `PASS_M4_CODE_GOVERNANCE`.

## Evidence Contract Status

| Field | Status |
|---|---|
| Primary criterion | `PASS_LOCAL`; deterministic model, prior, likelihood, simulation, trajectory diagnostic, and manifest-schema tests pass |
| Veto diagnostics | `PASS_LOCAL`; no unmatched-budget acceptance, proxy-only usefulness promotion, nonfinite density, ODE mismatch, traceability overclaim, or public API overclaim observed |
| Explanatory diagnostics | test counts, warning counts, wall time, dirty/untracked workspace status |
| Main uncertainty | first-gate model-contract and schema evidence only; no linear/nonlinear preconditioning rows have run |
| Next justified action | M5 stress-ladder plan gate |
| What is not concluded | no nonlinear preconditioning usefulness, no matched linear/nonlinear comparison success, no paper-scale predator-prey result, no adaptive MATLAB behavior, no high-dimensional scalability, no HMC/DSGE/GPU readiness, no stable top-level public API |

## Implementation Summary

- Added `PredatorPreySSM` in `bayesfilter/highdim/models.py`.
- Added `p30_predator_prey_fixture_model()` for the clean-room P30 first-gate
  fixture.
- Added `P30PredatorPreyComparisonManifest` in
  `bayesfilter/highdim/validation.py`.
- Exported the new symbols only from the experimental `bayesfilter.highdim`
  subpackage.
- Updated the P30 registry row for predator-prey from `REFERENCE_ONLY` to
  `BAYESFILTER_EXTENSION`, with first-gate-only non-claims.
- Added focused M4 tests and updated the registry guardrail test.
- Updated the traceability ledger row to the first-gate evidence boundary.

## Run Manifest

git commit: `7ccb9c39883471c2d5ec2891cbf33b9ed436bada`

dirty/untracked status:

```text
dirty/untracked workspace; active highdim code, tests, and P30 plan files are
untracked in this repository state.
```

environment: `/home/chakwong/anaconda3/envs/tf-gpu`

python: `Python 3.11.14`

CPU/GPU status:

```text
deliberate CPU-only tests; CUDA_VISIBLE_DEVICES=-1 set in pytest commands.
No GPU claim is made.
```

dtype: `tf.float64`

random seeds:

```text
4401/4402 in the matched-comparison schema fixture, 4404 for replayable
predator-prey simulation.
```

focused command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_predator_prey.py
```

result:

```text
8 passed, 2 warnings in 3.54s
```

focused registry/public API command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_predator_prey.py \
  tests/highdim/test_p30_model_suite_contracts.py \
  tests/test_v1_public_api.py
```

result:

```text
23 passed, 2 warnings in 3.87s
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
  tests/highdim/test_p30_spatial_sir.py \
  tests/highdim/test_p30_predator_prey.py
```

result:

```text
161 passed, 2 warnings in 16.86s
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
  bayesfilter/highdim/validation.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p30_predator_prey.py \
  tests/highdim/test_p30_model_suite_contracts.py \
  docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase4-predator-prey-preconditioning-subplan-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase4-predator-prey-preconditioning-claude-review-ledger-2026-06-05.md
```

result:

```text
passed
```

file-content whitespace command:

```bash
grep -n '[[:blank:]]$' \
  bayesfilter/highdim/models.py \
  bayesfilter/highdim/validation.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p30_predator_prey.py \
  tests/highdim/test_p30_model_suite_contracts.py \
  docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase4-predator-prey-preconditioning-subplan-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase4-predator-prey-preconditioning-claude-review-ledger-2026-06-05.md
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
tests/highdim/test_p30_predator_prey.py
tests/highdim/test_p30_model_suite_contracts.py
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase4-predator-prey-preconditioning-subplan-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase4-predator-prey-preconditioning-claude-review-ledger-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase4-predator-prey-preconditioning-result-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

## Failure And Repair Log

failed attempt:

```text
No focused implementation failure occurred.  The initial focused
predator-prey test passed.  A pre-existing registry contract still listed
`predator_prey` as reference-only, which would have contradicted the reviewed
M4 first-gate transition.
```

blocker classification:

```text
fixable test-contract and traceability update.  The reviewed M4 plan
explicitly permits `REFERENCE_ONLY` to `BAYESFILTER_EXTENSION` only for
model-contract and comparison-governance evidence.
```

repair:

```text
Removed `predator_prey` from the reference-only loop, added a dedicated
`test_predator_prey_registry_records_first_gate_extension_boundary` assertion
set, and updated the traceability ledger row plus current-blocker list to the
first-gate boundary.
```

rerun evidence:

```text
Focused M4 plus registry/public API checks passed with 23 tests.  Broad highdim
guardrail passed with 161 tests.  Compile and whitespace checks passed.
```

## Decision Table

| Field | Status |
|---|---|
| Decision | `PASS_M4` |
| Primary criterion status | `PASS_LOCAL` |
| Veto diagnostic status | `PASS_LOCAL` |
| Strongest uncertainty | first-gate model-contract/schema evidence only; no usefulness comparison evidence |
| Next justified action | M5 stress-ladder plan gate |
| Non-claims | no nonlinear preconditioning usefulness, no matched linear/nonlinear comparison success, no paper-scale predator-prey result, no adaptive MATLAB behavior, no high-dimensional scalability, no HMC/DSGE/GPU readiness, no stable top-level public API |
