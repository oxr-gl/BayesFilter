# P81 Phase 2 Result: Fixed-Branch/JVP-Backed SIR d=18 Wiring

status: PHASE2_WIRING_RESTORED_READY_FOR_PHASE3
date: 2026-06-21

## Decision

Phase 2 restored the missing fixed-branch/JVP-backed SIR d=18 wiring needed
for Phase 3.  The code now exposes the parameterized Zhao-Cui SIR surface and
the bounded multistate fixed-branch score API used by the horizon-0 smoke.

## Artifacts

| Artifact | Role |
|---|---|
| `bayesfilter/highdim/models.py` | Adds `ParameterizedZhaoCuiSIRSSM` and `parameterized_zhao_cui_sir_austria_model()`. |
| `bayesfilter/highdim/filtering.py` | Adds multistate adjacent target derivative result, horizon-0 multistate fixed-design score path, and same-branch compatibility hash. |
| `bayesfilter/highdim/__init__.py` | Exports the new model and multistate score APIs. |
| `tests/highdim/test_fixed_branch_derivatives.py` | Adds a tiny multistate horizon-0 finite-difference regression. |
| `tests/highdim/test_p81_analytical_sir_score.py` | Adds P81 SIR theta convention, model sensitivity, and d=18 horizon-0 score smoke tests. |

## Theta Convention

The wrapper follows the P8p/P79 convention:

- `kappa = base_kappa * exp(theta[0])`;
- `nu = base_nu * exp(theta[1])`;
- `observation_covariance = base_observation_covariance * exp(2 * theta[2])`.

## Boundary

The multistate score path is intentionally horizon-0 only.  It rejects
observation histories longer than one row and therefore does not claim full
transition/filter likelihood correctness.

## Checks

Phase 2 wiring is covered by the Phase 3 check set:

- `CUDA_VISIBLE_DEVICES=-1 python -m py_compile ...` passed.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_fixed_branch_derivatives.py -k "multistate_fixed_design_tt_score_path or scalar_fixed_design_tt_score_path"` passed: 2 passed, 17 deselected, 2 TFP deprecation warnings.
- Combined focused rerun after diagnostic-label cleanup passed: 5 passed, 17 deselected, 2 TFP deprecation warnings.

## What Is Not Claimed

No source-faithful adaptive Zhao-Cui route is claimed.  No closed-form hand
derivative is claimed.  No mini-batch training, LEDH-PFPF-OT comparison, GPU
performance, full likelihood correctness, HMC readiness, or production default
readiness is claimed from Phase 2.
