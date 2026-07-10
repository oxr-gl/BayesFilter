# Claude Read-Only Review Bundle: LEDH Score Phase 4 Predator-Prey Repair

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Codex remains supervisor and executor. Claude is a read-only reviewer only.

## Objective

Review whether the Phase 4 predator-prey repair subplan correctly addresses
the missing same-target no-tape total-score adapter.

## Fixed Paths To Review

- `docs/plans/bayesfilter-ledh-score-per-model-phase4-predator-prey-route-inventory-blocker-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-score-per-model-phase4-predator-prey-repair-subplan-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-score-per-model-phase4-predator-prey-subplan-2026-07-07.md`
- `docs/benchmarks/benchmark_ledh_same_target_predator_prey_value.py`
- `bayesfilter/highdim/models.py`
- `tests/highdim/test_ledh_predator_prey_score_phase4_contract.py`

## Evidence Contract

The admitted LEDH score is the no-tape total derivative of the same realized
finite-`N` LEDH estimator:

```text
observed_data_log_likelihood_estimator
```

reported as:

```text
log_likelihood
```

Predator-prey parameter order is:

```text
r, K, a, s, u, v
```

`GradientTape`, `ForwardAccumulator`, hidden autodiff, stopped partial
derivatives, wrong scalar, wrong row, wrong theta coordinate/order, local
density-only scores, value-only artifacts, and directional-only correctness as
full admission are forbidden.

## Local Checks

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_predator_prey_score_phase4_contract.py \
  tests/highdim/test_ledh_phase4_predator_prey_forward_scalar_artifact.py \
  tests/highdim/test_ledh_score_contract_phase1.py -q
```

Result:

```text
23 passed, 2 warnings
```

## Review Questions

1. Does the blocker result correctly identify the missing total LEDH score
   adapter as fixable, while refusing score admission?
2. Does the repair subplan require the necessary reverse-scan pieces: transport
   VJP, normalization VJP, LEDH flow VJP, pre-flow process-noise VJP, and RK4
   state/parameter VJP?
3. Does the plan prevent local-density-only, value-only, or directional-only
   evidence from being promoted as a full score?
4. Is it boundary-safe to execute the repair subplan?

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
