# P51-M5 Result: HMC Tier 2 Leapfrog Diagnostics

metadata_date: 2026-06-09
phase: P51-M5
status: PASS_P51_M5_HMC_TIER2_LEAPFROG
supervisor: Codex
reviewer: Claude Code read-only

## Decision

P51-M5 passes a scoped Tier 2 Hamiltonian/leapfrog diagnostic.  The diagnostic
uses a fixed identity mass matrix, deterministic value/score paths, two step
sizes per target, and explicit energy and reversibility tolerances.

The model-bearing row is the exact transformed SV dim-1 dense reference target
from the P50 strict SV family.  The quadratic row is retained only as a harness
sanity check.

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | Fixed-mass leapfrog energy/reversibility diagnostics for deterministic score targets. |
| Baseline/comparator | P50 Tier 2 definition, P51-M1 stable highdim score API boundary, and P50 strict SV rows. |
| Primary criterion | Passed: the strict exact transformed SV dim-1 dense reference target and the harness fixture pass all predeclared Tier 2 tolerances. |
| Veto diagnostics | Passed: finite gradients are not promoted; the quadratic fixture is not treated as model evidence; CPU-only checks do not imply GPU readiness. |
| Not concluded | No short-chain sampler health, no production HMC readiness, no GPU readiness, no model production readiness, and no broad HMC convergence. |

## Target Summary

| Target | Role | Step Sizes | Decision |
| --- | --- | --- | --- |
| `p51_m5_quadratic_harness_fixture` | harness fixture only | `0.05`, `0.025` | pass |
| `p51_m5_exact_transformed_sv_dim1_dense_reference` | exact transformed SV dim-1 dense reference | `0.005`, `0.0025` | pass |

Detailed metrics are recorded in:

`docs/plans/bayesfilter-highdim-zhao-cui-p51-m5-hmc-tier2-leapfrog-manifest-2026-06-09.json`

## Validation

Focused validation was run CPU-only with `CUDA_VISIBLE_DEVICES=-1`:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p51_hmc_tier2_leapfrog.py tests/highdim/test_p50_hmc_readiness_tiers.py tests/highdim/test_p51_stable_score_api.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_p51_hmc_tier2_leapfrog.py
git diff --check -- tests/highdim/test_p51_hmc_tier2_leapfrog.py docs/plans/bayesfilter-highdim-zhao-cui-p51-m5-hmc-tier2-leapfrog-manifest-2026-06-09.json docs/plans/bayesfilter-highdim-zhao-cui-p51-m5-hmc-tier2-leapfrog-result-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p51-visible-execution-ledger-2026-06-09.md
```

Outcomes:

- pytest passed: 13 tests passed, with 2 TensorFlow Probability deprecation
  warnings;
- compileall passed;
- git diff whitespace check passed.

## Nonclaims

- No short-chain sampler health.
- No production HMC readiness.
- No GPU readiness.
- No model production readiness.
- No broad HMC convergence.
- No source-faithful adaptive TT/SIRT filtering.
- No S&P 500 reproduction.
