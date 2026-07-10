# Claude Read-Only Review Bundle: LEDH Score Phase 3 Result and Phase 4 Subplan

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Codex remains supervisor and executor. Claude is a read-only reviewer only and
cannot authorize human, runtime, model-file, funding, product-capability,
scientific-claim, or boundary crossings.

## Objective

Review whether Phase 3 fixed-SIR can close as blocked/not admitted and whether
Phase 4 predator-prey may start under the runbook.

## Fixed Paths To Review

- `docs/plans/bayesfilter-ledh-score-per-model-master-program-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-score-per-model-phase3-fixed-sir-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-score-per-model-phase4-predator-prey-subplan-2026-07-07.md`
- `docs/benchmarks/benchmark_ledh_same_target_fixed_sir_score.py`
- `tests/highdim/test_ledh_fixed_sir_score_phase3_contract.py`
- `bayesfilter/highdim/ledh_score_contract.py`

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

`GradientTape`, `ForwardAccumulator`, hidden autodiff, stopped partial
derivatives, wrong scalar, wrong row, wrong theta coordinate/order, and
directional-only correctness as full admission are forbidden.

## Summary Of Local Checks

Command:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_ledh_fixed_sir_score_phase3_contract.py tests/test_ledh_fixed_sir_manual_score_phase4.py tests/highdim/test_ledh_score_contract_phase1.py -q
```

Result:

```text
29 passed, 2 warnings
```

## Material Change

The fixed-SIR adapter now rejects flag-only all-parameter promotion. Full
admission requires an explicit `all_parameter_score_correctness` record with
same-scalar finite-difference status `pass` and parameter names matching
`[log_kappa_scale, log_nu_scale, log_obs_noise_scale]`.

## Phase 4 Subplan Boundary Summary

The Phase 4 predator-prey subplan states these admission boundaries:

- row id: `zhao_cui_predator_prey_T20`;
- target scalar: `observed_data_log_likelihood_estimator`;
- output field: `log_likelihood`;
- source value artifact:
  `docs/plans/ledh-phase4-predator-prey-forward-scalar-artifact-2026-07-07.json`;
- target observation policy: `additive_gaussian_predator_prey`;
- theta coordinate system: `physical`;
- parameter order: `[r, K, a, s, u, v]`;
- admitted route, if implemented:
  `manual_total_vjp_no_autodiff_same_scalar_predator_prey_ledh_pfpf_ot`;
- full-row identity: `T=20,N=10000` matching the admitted value artifact;
- required correctness: all-parameter same-scalar correctness for all six
  physical parameters;
- forbidden for admission: value-only artifacts, directional-only finite
  differences, local-density-only scores, `GradientTape`,
  `ForwardAccumulator`, hidden autodiff, stopped partials, wrong target scalar,
  wrong observation policy, wrong theta coordinate, wrong parameter order,
  nonfinite score, or memory/device failure.

The subplan requires a blocker result instead of score admission if no
same-target no-tape total-score route exists or all-parameter correctness
cannot be established.

## Review Questions

1. Does Phase 3 correctly close fixed-SIR as blocked/not admitted because only
   directional FD correctness exists?
2. Does the fixed-SIR guard repair prevent accidental promotion of
   directional-only evidence?
3. Does Phase 4 predator-prey subplan preserve the same target scalar,
   physical parameter order `[r,K,a,s,u,v]`, no-tape requirement, and
   all-parameter correctness boundary?
4. Is it boundary-safe to start Phase 4 after this Phase 3 result?

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
