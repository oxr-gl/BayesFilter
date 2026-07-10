# Claude Read-Only Review Bundle: Phase 5 Actual-SV Full-Row Refresh

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Codex remains supervisor and executor. Claude is read-only reviewer only.

## Objective

Review whether the refreshed Phase 5 actual-SV full-row score/memory subplan is
boundary-safe after the streaming-flow parity repair passed tiny diagnostics.

## Fixed Paths To Review

- `docs/plans/bayesfilter-ledh-score-per-model-phase5-actual-sv-streaming-flow-parity-repair-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-score-per-model-phase5-actual-sv-full-row-score-subplan-refresh-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-score-per-model-visible-execution-ledger-2026-07-07.md`
- `docs/benchmarks/benchmark_ledh_same_target_actual_sv_score.py`
- `tests/highdim/test_ledh_actual_sv_score_phase5_contract.py`

## Evidence Summary

The previous full-row gate was blocked because the score route did not use the
same forward scalar as the admitted actual-SV value route. The repair result
records two fixes:

- score flow primal now mirrors streaming value flow chunking/padding/core
  arithmetic;
- score transport primal now uses raw streaming transport for forward particles
  and log weights, while retaining manual no-tape VJP for reverse cotangents.

Required local checks passed:

```text
30 passed, 2 warnings
```

Repaired tiny diagnostic:

```text
score = [-0.13676240070260542, 0.38478843496586546]
fd_score = [-0.1367604994584326, 0.38480405004648327]
max_abs_error = 1.561508061781458e-05
max_rel_error = 4.057930423530709e-05
score_admission_status = tiny_score_diagnostic_not_admitted
```

## Evidence Contract

Actual-SV full score admission still requires the no-tape total derivative of
the exact same finite-`N` streaming-flow value algorithm admitted for:

```text
zhao_cui_sv_actual_nongaussian_T1000
```

The target scalar is:

```text
observed_data_log_likelihood_estimator
```

reported as:

```text
log_likelihood
```

The target observation policy is:

```text
transformed_actual_sv_log_y_square
```

The parameter vector is:

```text
[gamma_unconstrained, log_beta]
```

Full `N=10000,T=1000` execution is still forbidden until the refreshed subplan
is reviewed and the memory-risk audit passes.

## Review Questions

1. Does the refreshed full-row subplan correctly start from the repaired
   streaming-flow parity result rather than the stale matrix-flow tiny result?
2. Does it preserve the boundary that tiny diagnostics and ladder runs are not
   full score admission?
3. Does it require memory-risk audit and reviewed trusted GPU ladder before any
   full `N=10000,T=1000` run?
4. Does it preserve no-tape, same-target, and same-algorithm constraints?
5. Is it boundary-safe to continue to the refreshed full-row score/memory gate?

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
