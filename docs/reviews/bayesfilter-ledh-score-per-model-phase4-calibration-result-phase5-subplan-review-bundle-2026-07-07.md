# Claude Read-Only Review Bundle: Phase 4 Calibration Result And Phase 5 Actual-SV Score Subplan

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Codex remains supervisor and executor. Claude is read-only reviewer only.

## Objective

Review whether Phase 4 predator-prey is correctly closed as blocked/not
admitted and whether Phase 5 actual-SV score may start from the drafted
subplan.

## Fixed Paths To Review

- `docs/plans/bayesfilter-ledh-score-per-model-phase4-predator-prey-full-row-correctness-calibration-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-score-per-model-phase5-actual-sv-subplan-2026-07-07.md`
- `docs/plans/ledh-phase5-actual-sv-forward-scalar-artifact-2026-07-07.json`
- `bayesfilter/highdim/ledh_score_contract.py`

## Evidence Contract

For every admitted LEDH score, the differentiated scalar must be:

```text
observed_data_log_likelihood_estimator
```

reported as:

```text
log_likelihood
```

The score must be a no-tape total derivative of the same realized finite-`N`
value artifact. `GradientTape`, `ForwardAccumulator`, hidden autodiff, stopped
partials, wrong scalar, wrong target policy, wrong theta coordinate/order, and
tiny diagnostic promotion are blockers.

## Phase 4 Decision Summary

Predator-prey has:

- bounded FP64 same-scalar all-coordinate FD pass at `T=2,N=64`;
- bounded FP64 same-scalar all-coordinate FD pass at `T=5,N=256`;
- float32/TF32 same-scalar FD fail at `T=2,N=64`;
- float32/TF32 same-scalar FD fail at `T=5,N=256`;
- no full `N=10000,T=20` validating score artifact.

The Phase 4 result therefore closes predator-prey as blocked/not admitted and
allows Phase 5 to start with this blocker recorded.

## Phase 5 Subplan Summary

Actual-SV value artifact is admitted for:

- row id: `zhao_cui_sv_actual_nongaussian_T1000`;
- target scalar: `observed_data_log_likelihood_estimator`;
- output field: `log_likelihood`;
- target observation policy: `transformed_actual_sv_log_y_square`;
- theta coordinate: `synthetic_unconstrained`;
- parameter order: `[gamma_unconstrained, log_beta]`;
- `N=10000,T=1000`, seeds `[81120,81121,81122,81123,81124]`.

The Phase 5 subplan starts with inventory, manual/no-tape derivative
implementation, tiny all-coordinate FP64 same-scalar FD, and a separate
reviewed full-row score/memory subplan before any full `N=10000,T=1000` score
attempt.

It explicitly forbids:

- KSC mixture target substitution;
- raw Gaussian observation likelihood target substitution;
- augmented-noise Gaussian closure;
- wrong theta coordinate/order;
- `GradientTape`, `ForwardAccumulator`, hidden autodiff, or stopped partials;
- tiny diagnostic promotion as full score admission.

## Review Questions

1. Does the Phase 4 calibration result correctly refuse predator-prey score
   admission from bounded FP64 diagnostics and failed FP32/TF32 diagnostics?
2. Does the Phase 5 subplan preserve the exact actual-SV transformed target,
   row id, target scalar, output field, theta coordinate, and parameter order?
3. Does the Phase 5 subplan avoid launching a full score run before a tiny
   no-tape all-coordinate correctness gate and reviewed full-row subplan?
4. Is it boundary-safe to start Phase 5 under this subplan?

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
