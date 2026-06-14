# P37-M5 Result: Stress-Ladder First Gate

metadata_date: 2026-06-06
phase: P37-M5

## Decision

Decision: `PASS_M5`.

M5 implements the first stress-ladder gate only.  It hardens the BayesFilter
stress-manifest layer with explicit P37-M5 phase identity, one-axis-at-a-time
ladder declarations, lower-phase guardrail status, exact-reference versus
diagnostic-only interpretation, resource/failure metadata, and first-gate
promotion boundaries.  It also reruns tiny CPU-only LGSSM stress-smoke rows.
It does not claim correctness, scalability, GPU readiness, HMC readiness, DSGE
readiness, or paper-model reproduction from stress success.

## Source-Governance Status

- P30 anchors identified: `eq:p27-bf1`--`eq:p27-bf4` for the generic
  BayesFilter stress family and `eq:p27-r1`--`eq:p27-r9` for robustness and
  failure-mode governance.
- Zhao--Cui paper anchors identified: none as direct reproduction targets;
  this is a BayesFilter extension beyond paper-model reproduction.
- MATLAB behavioral anchors identified: none required for this extension;
  the audited MATLAB model suite informs stress shapes only.
- BayesFilter code/test anchors identified:
  `bayesfilter/highdim/validation.py`,
  `bayesfilter/highdim/__init__.py`,
  `tests/highdim/test_p30_stress_ladders.py`,
  `tests/highdim/test_scaling_smoke.py`, and
  `tests/highdim/test_p30_model_suite_contracts.py`.
- Deviations listed: yes.  M5 stress rows are resource/failure governance and
  diagnostic smoke evidence, not Zhao--Cui paper reproduction.
- Clean-room boundary respected: yes.  No MATLAB code is copied or
  line-translated.
- Unsupported claims removed: yes.
- Reviewer verdict: `PASS_M5_CODE_GOVERNANCE`.

## Evidence Contract Status

| Field | Status |
|---|---|
| Primary criterion | `PASS_LOCAL`; complete stress-row manifests, one-axis ladder declarations, lower-phase blocking, diagnostic-only boundaries, and tiny CPU smoke rows pass |
| Veto diagnostics | `PASS_LOCAL`; no multiple-axis variation, missing fixed axis, lower-phase regression interpretation, first-gate promotion, nonfinite resource, public API overclaim, or lower-phase regression observed |
| Explanatory diagnostics | test counts, warning counts, wall time, dirty/untracked workspace status |
| Main uncertainty | first-gate governance and tiny-row evidence only; no long ladder or scalability evidence |
| Next justified action | M6 fixed-branch gradient plan gate |
| What is not concluded | no correctness from stress rows, no large-scale scalability, no GPU readiness, no HMC readiness, no DSGE readiness, no paper-model reproduction, no stable top-level public API |

## Implementation Summary

- Added `P30StressLadderRowManifest` in `bayesfilter/highdim/validation.py`.
- Preserved the existing `StressRunManifest` public symbol for compatibility
  while updating its documentation to P37-M5 stress-smoke language.
- Exported `P30StressLadderRowManifest` from the experimental
  `bayesfilter.highdim` subpackage only.
- Added `tests/highdim/test_p30_stress_ladders.py` for M5 first-gate schema and
  non-claim checks.
- Updated the generic stress registry row and model-suite contract test to
  the P37-M5 first-gate boundary.
- Updated the traceability ledger row for M5 stress-smoke governance.

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
m5-stress-seed for manifest schema tests; existing scaling-smoke rows use
deterministic seeds such as phase6-lgssm-d{state_dim}-h{horizon} and
phase6-scalar-tt-artifact for backward-compatible replay identifiers.
```

focused command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_stress_ladders.py \
  tests/highdim/test_scaling_smoke.py
```

result:

```text
13 passed, 2 warnings in 7.07s
```

focused registry/public API command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_stress_ladders.py \
  tests/highdim/test_scaling_smoke.py \
  tests/highdim/test_p30_model_suite_contracts.py \
  tests/test_v1_public_api.py \
  tests/highdim/test_public_api_highdim.py
```

result:

```text
initial: 34 passed, 2 warnings in 3.49s
after Claude-requested repair: 36 passed, 2 warnings in 3.22s
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
  tests/highdim/test_p30_stress_ladders.py \
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
initial: 170 passed, 2 warnings in 13.84s
after Claude-requested repair: 172 passed, 2 warnings in 13.05s
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
  bayesfilter/highdim/validation.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p30_stress_ladders.py \
  tests/highdim/test_p30_model_suite_contracts.py \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase5-stress-ladders-subplan-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase5-stress-ladders-claude-review-ledger-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

result:

```text
passed
```

file-content whitespace command:

```bash
grep -n '[[:blank:]]$' \
  bayesfilter/highdim/validation.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p30_stress_ladders.py \
  tests/highdim/test_p30_model_suite_contracts.py \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase5-stress-ladders-subplan-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase5-stress-ladders-claude-review-ledger-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

result:

```text
passed; no trailing whitespace matches were reported.  The command returned
exit status 1 because grep found no matches.
```

output artifacts:

```text
bayesfilter/highdim/validation.py
bayesfilter/highdim/__init__.py
tests/highdim/test_p30_stress_ladders.py
tests/highdim/test_p30_model_suite_contracts.py
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase5-stress-ladders-subplan-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase5-stress-ladders-claude-review-ledger-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase5-stress-ladders-result-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

## Failure And Repair Log

failed attempt:

```text
No focused implementation failure occurred.  The first focused M5 test command
passed.  Claude code/governance review iteration 2 returned
`BLOCKED_M5_CODE_GOVERNANCE` because two consistency checks were one-way only:
lower-phase regression blocking and exact-reference interpretation.
```

blocker classification:

```text
Fixable code-governance consistency issue.  A consistency repair was made
before broad evidence: the generic stress registry row still used older
`phase6_smoke` language.  It was updated to the P37-M5 first-gate boundary and
guarded by a registry contract test.  After Claude iteration 2, the validator
was also tightened so regression-blocked status must match a failing
lower-phase guardrail, and `PASS_EXACT_REFERENCE` status must use
`EXACT_REFERENCE` interpretation.
```

rerun evidence:

```text
Focused M5 plus registry/public API checks passed with 36 tests.  Broad highdim
guardrail passed with 172 tests.  Compile and whitespace checks passed.
```

## Decision Table

| Field | Status |
|---|---|
| Decision | `PASS_M5` |
| Primary criterion status | `PASS_LOCAL` |
| Veto diagnostic status | `PASS_LOCAL` |
| Strongest uncertainty | first-gate schema/tiny-row evidence only; no long ladder or scalability evidence |
| Next justified action | M6 fixed-branch gradient plan gate |
| Non-claims | no correctness from stress rows, no large-scale scalability, no GPU readiness, no HMC readiness, no DSGE readiness, no paper-model reproduction, no stable top-level public API |
