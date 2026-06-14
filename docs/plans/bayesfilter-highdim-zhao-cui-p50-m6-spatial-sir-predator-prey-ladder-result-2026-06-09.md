# P50-M6 Spatial SIR And Predator-Prey Ladder Result

metadata_date: 2026-06-09
phase: P50-M6
status: PASS_P50_M6_SPATIAL_SIR_PREDATOR_PREY_LADDER

## Decision Table

| Field | Decision |
| --- | --- |
| Gate decision | Pass M6 with scoped nonlinear-model evidence and preserved production blockers. |
| Primary criterion status | Passed in the subplan sense: spatial SIR and predator-prey lower-rung value diagnostics pass; finite score probes remain local diagnostics with uncertified-derivative boundaries; production rows retain reviewed blockers. |
| Veto diagnostic status | Passed: diagnostic smoke is not treated as production readiness; production route blockers are preserved; finite CUT4 scores are not promoted to certified gradients or HMC readiness. |
| Main uncertainty | Current nonlinear-model evidence is lower-rung and diagnostic.  Production spatial SIR remains blocked by route architecture; production predator-prey remains blocked by accuracy/tuning. |
| Next justified action | Advance to M7 HMC readiness tiers, using M5/M6 evidence boundaries rather than promoting diagnostics. |
| Not concluded | No production spatial SIR readiness, no production predator-prey readiness, no certified nonlinear-model gradient correctness, no HMC readiness, no smoothing support, no source-faithful adaptive TT/SIRT filtering, and no S&P 500 reproduction. |

## Artifacts

- `docs/plans/bayesfilter-highdim-zhao-cui-p50-m6-spatial-sir-predator-prey-ladder-manifest-2026-06-09.json`
- `tests/highdim/test_p50_spatial_sir_predator_prey_ladder.py`
- `tests/highdim/test_p47_spatial_sir_filtering.py`
- `tests/highdim/test_p47_predator_prey_filtering.py`
- `tests/highdim/test_p44_spatial_sir_diagnostic.py`
- `tests/highdim/test_p44_predator_prey_diagnostic.py`
- `tests/highdim/test_p47_m4b_m5b_production_repair.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p50-m6-spatial-sir-predator-prey-ladder-result-2026-06-09.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p50-visible-execution-ledger-2026-06-09.md`

## Supported Diagnostic Rows

| Row | M4 class | Boundary |
| --- | --- | --- |
| Spatial SIR J=1 Zhao-Cui vs dense | `PASS_VALUE_ONLY_DIAGNOSTIC` | lower-rung value/moment evidence only |
| Spatial SIR CUT4 finite score | `PASS_GRADIENT_LOCAL_DIAGNOSTIC` | metadata remains `value_only`; derivatives not certified |
| Predator-prey Zhao-Cui vs dense | `PASS_VALUE_ONLY_DIAGNOSTIC` | lower-rung value/moment evidence only |
| Predator-prey CUT4 finite score | `PASS_GRADIENT_LOCAL_DIAGNOSTIC` | metadata remains `value_only`; derivatives not certified |

## Preserved Production Blockers

| Row | Blocker |
| --- | --- |
| Spatial SIR production route | `BLOCKED_M4B_ROUTE_ARCHITECTURE` |
| Predator-prey production route | `BLOCKED_M5B_PRODUCTION_ACCURACY_TUNING` |

## Local Validation

Commands run CPU-only:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p50_spatial_sir_predator_prey_ladder.py tests/highdim/test_p47_spatial_sir_filtering.py tests/highdim/test_p47_predator_prey_filtering.py tests/highdim/test_p44_spatial_sir_diagnostic.py tests/highdim/test_p44_predator_prey_diagnostic.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_m4b_m5b_production_repair.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_p50_spatial_sir_predator_prey_ladder.py
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p50-m6-spatial-sir-predator-prey-ladder-manifest-2026-06-09.json tests/highdim/test_p50_spatial_sir_predator_prey_ladder.py docs/plans/bayesfilter-highdim-zhao-cui-p50-m6-spatial-sir-predator-prey-ladder-result-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p50-visible-execution-ledger-2026-06-09.md
```

Observed results:

- lower-rung and diagnostic suite: `25 passed, 2 TensorFlow Probability
  deprecation warnings`;
- production-blocker suite: `4 passed, 2 TensorFlow Probability deprecation
  warnings`;
- compileall passed with no output;
- `git diff --check` passed.

## Non-Claims

M6 does not claim:

- production spatial SIR readiness;
- production predator-prey readiness;
- certified nonlinear-model gradient correctness;
- nonlinear preconditioning usefulness;
- HMC readiness;
- smoothing support;
- source-faithful adaptive TT/SIRT filtering;
- S&P 500 reproduction.
