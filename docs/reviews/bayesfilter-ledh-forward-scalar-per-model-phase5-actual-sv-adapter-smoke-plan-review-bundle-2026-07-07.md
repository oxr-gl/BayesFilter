# Read-Only Review Bundle: Phase 5 Actual-SV Adapter Smoke Plan

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state. Codex is
supervisor and executor. Claude is read-only reviewer only.

## Objective

Review the plan to implement and smoke-test a tiny exact transformed actual-SV
LEDH adapter before any full `N=10000,T=1000` actual-SV run.

Plan path:

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-adapter-smoke-subplan-2026-07-07.md`

Parent Phase 5 path:

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-subplan-2026-07-07.md`

## Target Contract To Check

The target scalar is:

```text
observed_data_log_likelihood_estimator
```

The reported field is:

```text
log_likelihood
```

The actual-SV target is exact transformed actual SV:

```text
z_t = log(y_t^2)
z_t - 2 log(beta) - h_t ~ log(chi_square_1)
```

The proposed tiny runner must use LEDH flow only as a proposal surface, then
correct with the exact target density:

```text
target_transition_or_initial_density
+ exact_log_chi_square_log_density(z_t - 2log(beta) - x_t)
- pre_flow_log_density
+ forward_log_det
```

The tiny artifact must have:

```text
admission_status = tiny_executed_not_full_row
```

It must not admit the full actual-SV row.

## Review Questions

Please inspect only the cited plan paths and this packet. Return `VERDICT:
REVISE` if any of these are true:

- the plan could allow a full `N=10000,T=1000` run before tiny adapter smoke
  evidence;
- the plan could admit actual-SV from a tiny artifact;
- the plan allows raw Gaussian observation likelihood, KSC finite mixture, or
  augmented-noise Gaussian closure as the actual-SV target correction;
- the plan omits the exact `log(y^2)` transform with zero offset;
- the plan omits target-density correction;
- the plan omits a replay test that confirms `require_admitted=True` rejects
  the tiny artifact;
- the plan makes score, HMC, posterior, scientific-superiority, or runtime
  ranking claims.

Return `VERDICT: AGREE` only if the plan is consistent, feasible, and bounded
for tiny exact transformed actual-SV adapter smoke execution.

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
