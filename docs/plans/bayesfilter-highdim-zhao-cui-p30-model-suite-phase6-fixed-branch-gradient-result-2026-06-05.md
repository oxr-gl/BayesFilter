# P37-M6 Result: Fixed-Branch Gradient First Gate

metadata_date: 2026-06-06
phase: P37-M6

## Decision

Decision: `PASS_M6`.

M6 implements the first fixed-branch gradient-table gate only.  It adds a
P30-shaped `P30FixedBranchGradientTableManifest` for scalar exact-score LGSSM
fixtures, validates branch-compatible finite-difference rows, records
value-path prerequisite status, perturbation coordinate, tolerance policy,
stable-window status, derivative row decision, and explicit non-claims.  It
does not validate adaptive Zhao--Cui derivatives, a stable score API, HMC
readiness, DSGE readiness, GPU readiness, or general nonlinear derivative
validity.

## Source-Governance Status

- P30 anchors identified: `eq:p27-lg11a`--`eq:p27-lg15`,
  robustness derivative veto `eq:p27-r7`, and derivative table `eq:p27-t2`.
- Zhao--Cui paper anchors identified: no stable BayesFilter score API is
  supplied by the paper; this is a BayesFilter fixed-branch extension.
- MATLAB behavioral anchors identified: no audited MATLAB end-to-end score API
  for the BayesFilter fixed branch.
- BayesFilter code/test anchors identified:
  `bayesfilter/highdim/derivatives.py`,
  `bayesfilter/highdim/__init__.py`,
  `tests/highdim/test_fixed_branch_derivatives.py`,
  `tests/highdim/test_p30_fixed_branch_gradient_tables.py`, and
  `tests/highdim/test_public_api_highdim.py`.
- Deviations listed: yes.  This validates only scalar exact-score fixture rows
  and derivative-table governance.
- Clean-room boundary respected: yes.
- Unsupported claims removed: yes; the traceability ledger keeps the
  end-to-end score API `BLOCKED_UNVALIDATED`.
- Reviewer verdict: `PASS_M6_CODE_GOVERNANCE`.

## Evidence Contract Status

| Field | Status |
|---|---|
| Primary criterion | `PASS_LOCAL`; scalar LGSSM exact-score derivative table validates branch-compatible finite differences and stable-window status |
| Veto diagnostics | `PASS_LOCAL`; no branch-mismatch pass, missing value prerequisite, unstable-window pass, missing non-claim, public API overclaim, or lower-phase regression observed |
| Explanatory diagnostics | test counts, warning counts, wall time, dirty/untracked workspace status |
| Main uncertainty | first-gate scalar fixture evidence only; no nonlinear end-to-end score API |
| Next justified action | M7 integration closeout plan gate |
| What is not concluded | no adaptive derivative support, no stable score API, no HMC readiness, no DSGE readiness, no GPU readiness, no general nonlinear derivative validity, no stable top-level public API |

## Implementation Summary

- Added `P30FixedBranchGradientTableManifest` in
  `bayesfilter/highdim/derivatives.py`.
- Exported the new manifest only from the experimental `bayesfilter.highdim`
  subpackage.
- Added `tests/highdim/test_p30_fixed_branch_gradient_tables.py`.
- Updated the highdim public API containment test for the new subpackage-only
  symbol.
- Updated the traceability ledger row for fixed-branch derivative components
  while keeping the end-to-end score API blocked.

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
N/A; exact scalar LGSSM derivative-table fixtures are deterministic.
```

focused command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_fixed_branch_gradient_tables.py \
  tests/highdim/test_fixed_branch_derivatives.py
```

result:

```text
initial fixture attempt failed because the test called an existing exact-score
helper with an unsupported `prior_mean` keyword; after replacing the plus/minus
fixture with a local one-step Gaussian log-evidence formula:
24 passed, 2 warnings in 4.03s
```

focused public API command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p30_fixed_branch_gradient_tables.py \
  tests/highdim/test_fixed_branch_derivatives.py \
  tests/highdim/test_public_api_highdim.py \
  tests/test_v1_public_api.py
```

result:

```text
initial: 31 passed, 2 warnings in 3.83s
after Claude-requested repair: 33 passed, 2 warnings in 2.88s
after second Claude-requested repair: 35 passed, 2 warnings in 4.19s
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
  tests/highdim/test_p30_fixed_branch_gradient_tables.py \
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
initial: 179 passed, 2 warnings in 17.02s
after Claude-requested repair: 181 passed, 2 warnings in 14.18s
after second Claude-requested repair: 183 passed, 2 warnings in 20.24s
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
  bayesfilter/highdim/derivatives.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p30_fixed_branch_gradient_tables.py \
  tests/highdim/test_fixed_branch_derivatives.py \
  tests/highdim/test_public_api_highdim.py \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase6-fixed-branch-gradient-subplan-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase6-fixed-branch-gradient-claude-review-ledger-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

result:

```text
passed
```

file-content whitespace command:

```bash
grep -n '[[:blank:]]$' \
  bayesfilter/highdim/derivatives.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p30_fixed_branch_gradient_tables.py \
  tests/highdim/test_fixed_branch_derivatives.py \
  tests/highdim/test_public_api_highdim.py \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase6-fixed-branch-gradient-subplan-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase6-fixed-branch-gradient-claude-review-ledger-2026-06-05.md \
  docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

result:

```text
passed; no trailing whitespace matches were reported.  The command returned
exit status 1 because grep found no matches.
```

output artifacts:

```text
bayesfilter/highdim/derivatives.py
bayesfilter/highdim/__init__.py
tests/highdim/test_p30_fixed_branch_gradient_tables.py
tests/highdim/test_public_api_highdim.py
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase6-fixed-branch-gradient-subplan-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase6-fixed-branch-gradient-claude-review-ledger-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase6-fixed-branch-gradient-result-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
```

## Failure And Repair Log

failed attempt:

```text
The initial focused M6 test run failed in the new test fixture because
`scalar_one_step_lgssm_prior_mean_score()` does not accept a `prior_mean`
keyword.  The failure occurred before testing the manifest implementation.
Claude code/governance review iteration 1 later returned
`BLOCKED_M6_CODE_GOVERNANCE` because the manifest did not yet enforce all-row
validity for passed rows, stable-window status consistency, or exact matching
between the declared `h` ladder and table-row `h` values.  Claude review
iteration 2 then found one remaining consistency gap: valid rows with no
stable window could still be mislabeled as branch/value blocked.
```

blocker classification:

```text
Fixable test-fixture issue.  The implementation contract did not need to
change.
```

repair:

```text
Replaced the finite-difference plus/minus fixture with a local one-step
Gaussian log-evidence formula matching the existing exact-score helper at the
base point, while continuing to use the helper for the analytic score.  After
Claude iteration 1, tightened `P30FixedBranchGradientTableManifest` so
`DERIVATIVE_PASSED` requires every finite-difference row to be valid, the
declared stable-window status must be allowed and consistent with the row
decision, and the declared `finite_difference_h` ladder must match the table
rows.  After Claude iteration 2, the stable-window status is computed from
value prerequisite, row validity, row presence, and stable-window evidence, and
the declared status must match exactly.
```

rerun evidence:

```text
Focused M6 plus public API checks passed with 35 tests.  Broad highdim
guardrail passed with 183 tests.  Compile and whitespace checks passed.
```

## Decision Table

| Field | Status |
|---|---|
| Decision | `PASS_M6` |
| Primary criterion status | `PASS_LOCAL` |
| Veto diagnostic status | `PASS_LOCAL` |
| Strongest uncertainty | scalar exact-score fixture evidence only; no nonlinear end-to-end score API |
| Next justified action | M7 integration closeout plan gate |
| Non-claims | no adaptive derivative support, no stable score API, no HMC readiness, no DSGE readiness, no GPU readiness, no general nonlinear derivative validity, no stable top-level public API |
