# Claude Read-Only Review Bundle: LEDH Forward Scalar Phase 3 Result And Phase 4 Handoff

Date: 2026-07-07

## Role Contract

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Codex is supervisor and executor. Claude is a read-only reviewer only.

## Review Scope

Review only these fixed paths:

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase3-fixed-sir-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase4-predator-prey-subplan-2026-07-07.md`
- `docs/plans/ledh-phase3-fixed-sir-forward-scalar-artifact-2026-07-07.md`
- `docs/plans/ledh-phase3-fixed-sir-forward-scalar-artifact-2026-07-07.json`
- `tests/highdim/test_ledh_phase3_fixed_sir_forward_scalar_artifact.py`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-visible-execution-ledger-2026-07-07.md`

Do not review the whole repository.

## Objective

Check whether Phase 3 correctly closes fixed SIR same-target forward scalar
reconfirmation under `sir_log_scale_theta` and whether the Phase 4
predator-prey subplan safely starts the first previously blocked model:
`zhao_cui_predator_prey_T20`.

Target scalar: `observed_data_log_likelihood_estimator`, reported in artifacts
as `log_likelihood`.

## Phase 3 Summary

Phase 3 normalized the existing fixed SIR N=10000 value artifact into the Phase
1 canonical executable artifact schema.

The canonical artifact:

- uses row id `zhao_cui_spatial_sir_austria_j9_T20`;
- maps old top-level `log_likelihood` to canonical `log_likelihood_by_seed`;
- records `average_log_likelihood_by_seed`;
- binds `theta_coordinate_system = sir_log_scale_theta`;
- binds theta `[0.0, 0.0, 0.0]`;
- records `target_density_used_for_correction = true`;
- validates with `validate_ledh_forward_scalar_artifact(..., require_admitted=True)`;
- is explicitly not old `no_free_theta` admission and not score evidence.

## Local Check Evidence

Mandatory Phase 3 replay check:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_fixed_sir_forward_scalar_artifact.py -q
```

Result:

```text
2 passed, 2 warnings in 2.50s
```

Combined required check set:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py \
  tests/highdim/test_ledh_phase2_lgssm_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase3_fixed_sir_forward_scalar_artifact.py -q
```

Result:

```text
28 passed, 2 warnings in 2.57s
```

These were CPU-hidden validation/replay checks. Phase 3 did not run a new GPU
model job.

## Review Questions

1. Does Phase 3 avoid claiming predator-prey/SV/generalized-SV admission,
   score admission, score correctness, leaderboard rebuild, new GPU model
   evidence, exact nonlinear likelihood correctness, Zhao-Cui TT/SIRT
   source-faithfulness, or scientific conclusions?
2. Is the fixed SIR canonical artifact sufficient for the Phase 1 executable
   forward-scalar schema and `require_admitted=True` gate under
   `sir_log_scale_theta`?
3. Does the mandatory replay test read the actual Phase 3 artifact from disk
   and enforce the intended fixed SIR row/target/theta/nonclaim boundaries?
4. Does the Phase 4 predator-prey subplan correctly treat predator-prey as a
   previously blocked model requiring runner inventory, canonical artifact or
   blocker result, mandatory replay if artifact exists, and no LGSSM/SIR
   evidence borrowing?
5. Are Phase 4 stop and handoff conditions strong enough before actual-SV
   Phase 5?

Findings first. End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
