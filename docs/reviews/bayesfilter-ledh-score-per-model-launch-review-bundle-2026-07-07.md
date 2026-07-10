# LEDH Score Per-Model Launch Review Bundle

metadata_date: 2026-07-07
review_scope: `score_runbook_launch_package`

## Role Contract

Claude is read-only reviewer only.

Do not edit files, run experiments, launch agents, approve policy boundaries,
or change state.

Codex remains supervisor and executor.

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```

## Objective

Review whether the LEDH score per-model launch package is safe to launch Phase
0.

Scores are not admitted at launch.

The target scalar to differentiate is:

```text
observed_data_log_likelihood_estimator
```

reported as:

```text
log_likelihood
```

Admitted LEDH scores must be analytical/manual no-tape total derivatives.

## Fixed Paths To Review

- `docs/plans/bayesfilter-ledh-score-per-model-master-program-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-score-per-model-visible-gated-execution-runbook-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-score-per-model-phase0-baseline-governance-subplan-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase8-integration-result-2026-07-07.md`

Do not review the whole repo.

## Launch Package Summary

The score program starts after value-only integration closed. The eligible
value row set is:

- `benchmark_lgssm_exact_oracle_m3_T50`;
- `zhao_cui_spatial_sir_austria_j9_T20`;
- `zhao_cui_predator_prey_T20`;
- `zhao_cui_sv_actual_nongaussian_T1000`;
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`;
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`.

The parameterized SIR diagnostic row is excluded.

Launch boundaries:

- no score admission at launch;
- no score before admitted value;
- no `GradientTape`, `ForwardAccumulator`, hidden autodiff, or stopped partial
  derivative for admitted score evidence;
- each model gets a separate phase;
- tiny checks precede `N=10000` score-memory checks;
- runtime/memory/FD-smoke alone do not promote a score;
- no HMC/posterior/scientific-superiority/runtime-ranking claim.

## Review Questions

1. Does the master program use the Phase 8 value integration artifact as the
   score row-set anchor?
2. Does it ban tape/autodiff and stopped partial derivatives for admitted LEDH
   score evidence?
3. Does it prevent diagnostic SIR promotion?
4. Does Phase 0 avoid admitting scores and instead freeze baseline/governance?
5. Are stop conditions and handoff conditions sufficient before Phase 1 score
   schema work?

## Pass Criteria

Return `VERDICT: AGREE` only if:

- the launch package is internally consistent;
- Phase 0 is safe to launch;
- no score/scientific/runtime boundary is crossed; and
- no fixable blocker remains.

Return `VERDICT: REVISE` if any material issue remains.
