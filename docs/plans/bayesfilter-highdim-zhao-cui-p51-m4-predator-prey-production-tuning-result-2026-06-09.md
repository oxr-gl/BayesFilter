# P51-M4 Result: Predator-Prey Production Accuracy Tuning

metadata_date: 2026-06-09
phase: P51-M4
status: PASS_P51_M4_PREDATOR_PREY_PRODUCTION_TUNING
supervisor: Codex
reviewer: Claude Code read-only

## Decision

P51-M4 closes the P47/P50 fixed-design predator-prey production tuning blocker
for the declared horizon-25 additive-Gaussian RK4 closure.  The predeclared
candidate `P51-M4-2`, with fit order 9 and rank 10, passes every preserved
P47/P50 production tolerance against the same dense horizon-25 reference.

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | A bounded tuning repair can make the same P47/P50 horizon-25 predator-prey production candidate meet preserved reference/tolerance criteria. |
| Baseline/comparator | P47-M5b blocker, P50-M6 predator-prey production row, unchanged horizon-25 dense reference, and unchanged production tolerances. |
| Primary criterion | Passed: `P51-M4-2` passes all preserved tolerances and deterministic replay. |
| Veto diagnostics | Passed: no threshold loosened after results; lower-rung evidence is not used; reference metrics, not internal diagnostics, decide the gate. |
| Not concluded | No HMC readiness. No nonlinear preconditioning usefulness. No native non-Gaussian predator-prey correctness. |

## Candidate Ladder

| Candidate | Fit Order | Rank | Log Gap | Step Gap | Mean Gap | Cov Gap | Replay | Decision |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| P51-M4-0 | 7 | 8 | 145.7760213472871 | 11.414750146529755 | 19.45492436940154 | 44.61958715970044 | pass | fail |
| P51-M4-1 | 7 | 10 | 145.77571268796095 | 11.414774164303584 | 19.4549243695202 | 44.61958619855251 | pass | fail |
| P51-M4-2 | 9 | 10 | 0.0026244076792636406 | 0.0002265739885594087 | 0.00014690055770927302 | 0.0007808143975545079 | pass | pass |

Preserved tolerances:

- absolute log-likelihood gap `< 5.0`;
- max step log-normalizer gap `< 1.0`;
- max state mean component error `< 5.0`;
- max covariance entry error `< 8.0`;
- truth-path prey RMSE `< 8.0`;
- truth-path predator RMSE `< 2.0`;
- deterministic replay required.

## Validation

Focused validation was run CPU-only with `CUDA_VISIBLE_DEVICES=-1`:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p51_predator_prey_production_tuning.py tests/highdim/test_p50_spatial_sir_predator_prey_ladder.py tests/highdim/test_p47_m4b_m5b_production_repair.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_p51_predator_prey_production_tuning.py
git diff --check -- tests/highdim/test_p51_predator_prey_production_tuning.py docs/plans/bayesfilter-highdim-zhao-cui-p51-m4-predator-prey-production-tuning-manifest-2026-06-09.json docs/plans/bayesfilter-highdim-zhao-cui-p51-m4-predator-prey-production-tuning-result-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p51-visible-execution-ledger-2026-06-09.md
```

Outcomes:

- pytest passed: 14 tests passed, with 2 TensorFlow Probability deprecation
  warnings;
- compileall passed;
- git diff whitespace check passed.

## Nonclaims

- No HMC readiness.
- No production HMC readiness.
- No nonlinear preconditioning usefulness claim.
- No native non-Gaussian predator-prey correctness.
- No source-faithful adaptive TT/SIRT filtering.
- No S&P 500 reproduction.
