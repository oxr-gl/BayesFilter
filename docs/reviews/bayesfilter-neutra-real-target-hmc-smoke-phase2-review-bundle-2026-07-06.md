# BayesFilter NeuTra Real Target HMC Smoke Phase 2 Review Bundle

Date: 2026-07-06

## Role Contract

READ-ONLY BOUNDED REVIEW.

Codex is supervisor and executor. Claude is read-only reviewer only.

Do not edit files, run commands, launch agents, inspect the whole repository,
or authorize runtime, model-file, funding, product-capability, default-policy,
or scientific-claim boundaries.

## Review Question

Is it consistent, correct, feasible, artifact-covered, and boundary-safe for
Phase 2 to close as `BLOCKED_MISSING_PORTABLE_REAL_TARGET_AUTHORITY` and for
Phase 3 to be refreshed from mechanics into blocker-handoff handling?

End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```

## Artifacts Under Review

- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase2-real-target-adapter-result-2026-07-06.md`
- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase3-real-target-mechanics-subplan-2026-07-06.md`

## Phase 2 Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter expose a real c603 target adapter with batch-native finite value/score under reviewed authority? |
| Primary criterion | Either a reviewed adapter bridge emits finite rank-2 values/scores with the c603 target signature, or a blocker records the exact missing port/source/runtime authority. |
| Veto diagnostics | Synthetic target mislabeled real, live `dsge_hmc` runtime promoted as BayesFilter authority, unreviewed GradientTape fallback promoted, nonfinite probes, target-signature mismatch, HMC/GPU/training launch. |
| Not concluded | HMC convergence, posterior correctness, production readiness. |

## Material Findings To Review

Codex found that Phase 2 cannot safely implement the real c603 adapter from
current BayesFilter authority.

Supporting observations:

- The c603 handoff wrapper calls
  `model.rotemberg_second_order_svd_bayesfilter_model_and_derivatives`,
  `tf_batched_svd_sigma_point_value_and_score_custom_gradient`, and
  `model.log_prior_value_and_score_analytical_batch`.
- The model/derivative builder in the handoff source depends on
  `RotembergNKEstimable._tf_solver.solve(...)` and solution-sensitivity
  routines in `dsge_hmc`.
- Local BayesFilter code has a batch SVD sigma-point kernel, but not the
  c603 Rotemberg model/derivative builder, not the handoff custom-gradient
  wrapper symbol, and not the Rotemberg analytical prior callable.
- The c603 preflight JSON names three portable `.npz` files:
  `rotemberg_second_order_svd_target_arrays.npz`,
  `rotemberg_second_order_svd_probe_cloud.npz`, and
  `rotemberg_second_order_svd_data.npz`; direct file checks show all three are
  absent from the fetched handoff checkout.
- The frozen c603 NeuTra transport import remains valid, but that is transport
  evidence only and does not supply a real target callable.

## Local Checks

The Phase 2 result records:

```text
PHASE2_LOCAL_CHECKS_BLOCKER_CONFIRMED
target_arrays_npz: absent
probe_cloud_npz: absent
data_npz: absent
bayesfilter_real_target_symbols: absent
c603_preflight_json: present and names the missing arrays
```

Claude health probe in trusted context returned:

```text
CLAUDE_PROBE_OK
```

## Boundary Decision

Codex proposes:

- accept Phase 2 as a fail-closed blocker;
- do not run mechanics, HMC, GPU, training, package installation, or git
  operations;
- refresh Phase 3 as blocker-handoff handling, not mechanics;
- require a separate reviewed repair program to port the Rotemberg c603
  model/solver/sensitivity/prior authority into BayesFilter, or to request a
  follow-up handoff with portable target adapter material.

## Review Checklist

Please check:

- wrong baseline;
- proxy metrics promoted to pass criteria;
- missing stop condition;
- hidden assumption;
- stale context;
- environment mismatch;
- unsupported claim;
- artifact mismatch;
- boundary unsafe action;
- whether a missing diagnostic replay `.npz` is being incorrectly equated with
  a real adapter. It should not be.
