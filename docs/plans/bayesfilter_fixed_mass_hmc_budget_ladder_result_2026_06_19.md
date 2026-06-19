# BayesFilter Result: Fixed-Mass HMC Tuning-Budget Ladder

Date: 2026-06-19

Status: `IMPLEMENTED_REVIEW_REPAIRED_FOCUSED_TESTS_PASS`

## Decision Table

| Field | Entry |
| --- | --- |
| Decision | Added and review-repaired a generic BayesFilter fixed-mass HMC tuning-budget ladder as an additive API. |
| Primary criterion status | Passed focused deterministic and tiny real TFP Gaussian tests after implementation-review repairs. |
| Veto diagnostic status | No unbounded loops, no MacroFinance imports, no NumPy algorithmic HMC path, additive exports only; frozen mass is now operational geometry through a BayesFilter-built latent adapter. |
| Main uncertainty | Downstream MacroFinance wiring still needs focused integration tests and fresh artifacts. |
| Next justified action | Run Claude implementation review, then wire MacroFinance Phase 4/5 to call the BayesFilter ladder. |
| What is not concluded | No posterior convergence, no sampler superiority, no default budget recommendation, no GPU/XLA readiness, no empirical validity. |

## Implementation Summary

- Added `bayesfilter/inference/hmc_budget_ladder.py`.
- Added public exports in `bayesfilter.inference` and top-level `bayesfilter`.
- Added `tests/test_hmc_budget_ladder.py`.
- The ladder validates a position-coordinate `PrecomputedMassArtifact`, builds
  the latent fixed-mass HMC adapter internally, records full position-adapter,
  latent-HMC-adapter, and mass signatures, and keeps client diagnostics
  role-separated through `FixedMassHMCTuningBudgetCallbackResult`.
- Implementation-review repairs preserved continuation vetoes as a distinct
  terminal status, made pure repair triggers block promotion and advance to the
  next budget, and made optional step-stability diagnostics active.

## Verification

Command:

```bash
timeout 600 env CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_hmc_budget_ladder.py tests/test_generic_hmc_tuning.py
```

Result after repair: `14 passed, 2 warnings in 2.86s`.

## Nonclaims

- Fixed-mass HMC tuning-budget ladder only.
- Acceptance is a tuning-screen diagnostic only.
- No posterior convergence claim.
- No sampler superiority claim.
- No default sampler readiness claim.
- No empirical validity claim.
- No GPU or XLA readiness claim.
