# Read-Only Review Bundle: Phase 5 Actual-SV Full-Row Plan

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state. Codex is
supervisor and executor. Claude is read-only reviewer only.

## Objective

Review the plan for running the full actual-SV exact transformed LEDH
observed-data forward scalar row after the tiny adapter smoke passed.

Plan path:

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-full-row-subplan-2026-07-07.md`

Tiny result path:

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-adapter-smoke-result-2026-07-07.md`

## Target Contract

Target scalar:

```text
observed_data_log_likelihood_estimator
```

Reported tensor:

```text
log_likelihood
```

Exact transformed actual-SV target:

```text
z_t = log(y_t^2)
z_t - 2 log(beta) - x_t ~ log(chi_square_1)
```

Full-row admission requires:

```text
row_id = zhao_cui_sv_actual_nongaussian_T1000
T = 1000
N = 10000
seeds = [81120,81121,81122,81123,81124]
theta = [0.2533471031357997,-0.916290731874155]
admission_status = n10000_same_target_value_admitted
```

## Review Questions

Return `VERDICT: REVISE` if any are true:

- the plan allows full-row admission without an explicit full-row mode;
- the plan can accidentally admit the tiny artifact;
- the plan allows raw Gaussian observation likelihood, KSC finite mixture, or
  augmented-noise Gaussian closure as the actual-SV target correction;
- the plan allows a positive log-square transform offset;
- the plan omits validation with `require_admitted=True`;
- the plan omits a full-row replay test reading the actual JSON artifact;
- the plan omits preserving the tiny replay rejection of
  `require_admitted=True`;
- the plan makes score, HMC, posterior, scientific-superiority, runtime
  ranking, generalized-SV, KSC, or leaderboard claims.

Return `VERDICT: AGREE` if the plan is consistent, feasible, and bounded for
full-row actual-SV value admission only.

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
