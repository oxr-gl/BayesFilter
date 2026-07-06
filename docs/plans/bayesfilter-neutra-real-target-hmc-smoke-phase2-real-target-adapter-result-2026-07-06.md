# BayesFilter NeuTra Real Target HMC Smoke Phase 2 Result

Date: 2026-07-06

## Status

`BLOCKED_MISSING_PORTABLE_REAL_TARGET_AUTHORITY`

## Phase Objective

Build or fail-closed document the c603 adapter-authority bridge needed before
real-target mechanics. Phase 1 classified the current state as `design_only`,
meaning BayesFilter had c603 transport/signature evidence and generic adapter
surfaces, but no live BayesFilter-owned c603 Rotemberg prior/model/filter
value-score callable.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can BayesFilter expose a real c603 target adapter with batch-native finite value/score under reviewed authority? |
| Baseline/comparator | Phase 1 `design_only` classification, c603 proposal/preflight, `GenericSSMPosteriorAdapter`, and existing BayesFilter batch SVD sigma-point APIs. |
| Primary criterion | Failed closed: no reviewed portable real-target adapter was implemented; the exact missing authority is recorded below. |
| Veto diagnostics | The available BayesFilter code lacks the c603 Rotemberg model/derivative builder and analytical prior callable; the handoff checkout lacks the referenced preflight `.npz` target/data/probe arrays; no synthetic target was promoted. |
| Explanatory diagnostics | c603 target signature and frozen transport import remain valid as transport evidence only. |
| Not concluded | No real c603 adapter correctness, no real-target mechanics, no HMC readiness, no posterior correctness, no production readiness. |
| Artifact | This Phase 2 blocker result and refreshed Phase 3 blocker-handoff subplan. |

## Decision

Phase 2 stops with:

```text
blocked_missing_portable_real_target_authority
```

This is not a failure of the frozen NeuTra transport import. It is a failure to
establish the separate BayesFilter-owned real target value/score authority
needed before mechanics or HMC can be called real c603 target evidence.

## What Was Checked

The c603 source wrapper in the handoff script defines the posterior as:

- `model.rotemberg_second_order_svd_bayesfilter_model_and_derivatives(u_batch)`;
- `tf_batched_svd_sigma_point_value_and_score_custom_gradient(...)` with
  `backend="tf_principal_sqrt_ukf"`;
- `model.log_prior_value_and_score_analytical_batch(u_batch)`;
- return of likelihood plus prior and score plus prior score.

Source anchors inspected:

- `/tmp/dsge_hmc-neutra-handoff-20260705/scripts/prepare_neutra_rotemberg_second_order_svd_target.py:186-199`
- `/tmp/dsge_hmc-neutra-handoff-20260705/scripts/prepare_neutra_rotemberg_second_order_svd_target.py:225-240`
- `/tmp/dsge_hmc-neutra-handoff-20260705/scripts/prepare_neutra_rotemberg_second_order_svd_target.py:305-324`
- `/tmp/dsge_hmc-neutra-handoff-20260705/scripts/prepare_neutra_rotemberg_second_order_svd_target.py:371-389`
- `/tmp/dsge_hmc-neutra-handoff-20260705/scripts/prepare_neutra_rotemberg_second_order_svd_target.py:447-459`
- `/tmp/dsge_hmc-neutra-handoff-20260705/src/dsge_hmc/models/rotemberg_nk.py:325-355`
- `/tmp/dsge_hmc-neutra-handoff-20260705/src/dsge_hmc/models/rotemberg_nk.py:1530-1692`
- `/tmp/dsge_hmc-neutra-handoff-20260705/src/dsge_hmc/models/rotemberg_nk.py:3849-4100`
- `bayesfilter/nonlinear/experimental_batched_svd_sigma_point_tf.py:1271`

## Exact Missing Authority

| Required authority | Current status | Consequence |
| --- | --- | --- |
| Portable c603 model/derivative builder | Missing in BayesFilter. The source implementation depends on `RotembergNKEstimable._tf_solver.solve(...)` and solution-sensitivity routines in `dsge_hmc`. | BayesFilter cannot build the real c603 state-space tensors and derivative hooks locally. |
| BayesFilter-owned c603 analytical prior value/score | Missing in BayesFilter. The source authority is `RotembergNKEstimable.log_prior_value_and_score_analytical_batch`. | BayesFilter cannot split prior and likelihood callables for `GenericSSMPosteriorAdapter`. |
| Handoff custom-gradient wrapper identity | Missing under the handoff symbol. BayesFilter has `tf_batched_svd_sigma_point_value_and_score`, but not the handoff `tf_batched_svd_sigma_point_value_and_score_custom_gradient` wrapper. | The local kernel alone is insufficient without the c603 model/derivative builder and wrapper mapping. |
| Portable preflight arrays | Missing from the fetched handoff checkout. The preflight JSON references `rotemberg_second_order_svd_target_arrays.npz`, `rotemberg_second_order_svd_probe_cloud.npz`, and `rotemberg_second_order_svd_data.npz`, but those files are absent. | BayesFilter cannot even build a frozen diagnostic replay table from the handoff preflight artifacts, and such a table would be diagnostic only, not a real adapter. |

## Direct Verdicts

| Statement | Classification | Support |
| --- | --- | --- |
| The c603 frozen dense-IAF transport can be imported and loaded against the known target signature. | `correct` | Closed c603 follow-up import validation result. |
| The c603 transport can bind to a synthetic quadratic base adapter for mechanics-fixture checks. | `correct` | Closed c603 mechanics fixture result. |
| BayesFilter currently has a real c603 Rotemberg target adapter callable ready for mechanics/HMC. | `unsupported` | Local symbol search found no BayesFilter-owned Rotemberg target wrapper, model/derivative builder, custom-gradient wrapper symbol, or analytical prior callable. |
| A frozen probe table from c603 preflight arrays would be a real target adapter. | `wrong relative to the stated target` | Even if present, a finite probe table would be diagnostic replay evidence, not a batch-native callable over arbitrary HMC states. |
| Importing live `dsge_hmc` modules from `/tmp` is BayesFilter target authority. | `unsupported` | The Phase 2 subplan forbids treating live `dsge_hmc` runtime imports as BayesFilter authority without a separate reviewed port/runtime boundary. |
| The current Phase 2 evidence authorizes real-target mechanics or HMC. | `wrong relative to the stated target` | The required real c603 target value/score boundary was not established. |

## Local Checks

Required local checks executed:

```text
test -f /tmp/dsge_hmc-neutra-handoff-20260705/docs/plans/artifacts/rotemberg-second-order-svd-4d-minimal-principal-sqrt-baseline-2026-07-01/phase1/preflight/rotemberg_second_order_svd_target_arrays.npz
test -f /tmp/dsge_hmc-neutra-handoff-20260705/docs/plans/artifacts/rotemberg-second-order-svd-4d-minimal-principal-sqrt-baseline-2026-07-01/phase1/preflight/rotemberg_second_order_svd_probe_cloud.npz
test -f /tmp/dsge_hmc-neutra-handoff-20260705/docs/plans/artifacts/rotemberg-second-order-svd-4d-minimal-principal-sqrt-baseline-2026-07-01/phase1/preflight/rotemberg_second_order_svd_data.npz
python read of c603 preflight JSON keys
rg -n "RotembergSecondOrderSVDBayesFilterPosterior|rotemberg_second_order_svd_bayesfilter_model_and_derivatives|tf_batched_svd_sigma_point_value_and_score_custom_gradient|log_prior_value_and_score_analytical_batch|RotembergNKEstimable" bayesfilter tests -g "*.py"
```

Result:

```text
PHASE2_LOCAL_CHECKS_BLOCKER_CONFIRMED
target_arrays_npz: absent
probe_cloud_npz: absent
data_npz: absent
bayesfilter_real_target_symbols: absent
c603_preflight_json: present and names the missing arrays
```

## Phase 3 Handoff

Phase 3 must not run real-target mechanics. The refreshed Phase 3 subplan is a
blocker-handoff phase whose objective is to preserve the stop condition,
describe the next valid repair program, and prevent accidental promotion of
transport/mechanics fixture evidence into real c603 target evidence.

The next valid repair program must choose one reviewed route:

- port the minimal Rotemberg c603 model/solver/sensitivity/prior authority into
  BayesFilter with focused parity tests; or
- request a follow-up handoff containing portable BayesFilter-owned target
  adapter code or sufficient serialized real-target arrays for diagnostic
  replay, with the replay explicitly classified as diagnostic only.

## Review

Review is required for this blocker result and the refreshed Phase 3 subplan.
Claude was first probed with:

```text
timeout 90s claude -p "Return exactly CLAUDE_PROBE_OK."
```

The trusted probe returned:

```text
CLAUDE_PROBE_OK
```

Therefore a bounded Claude read-only review gate is required before accepting
this Phase 2 close.

Bounded Claude read-only review gate:

```text
REVIEW_STATUS=agreed
VERDICT=AGREE
RUN_DIR=/home/chakwong/BayesFilter/.claude_reviews/20260706-173915-bayesfilter-neutra-real-target-hmc-smoke-phase2
SUMMARY_JSON=/home/chakwong/BayesFilter/.claude_reviews/20260706-173915-bayesfilter-neutra-real-target-hmc-smoke-phase2/status.json
```

Phase 2 blocker close is accepted. Phase 3 is refreshed as blocker-handoff
handling, not mechanics.

## Nonclaims

- no real c603 adapter implementation has been accepted;
- no c603 real-target mechanics pass has been produced;
- no HMC, GPU, training, package installation, or git operation was run;
- no posterior correctness, HMC readiness, production readiness, scientific
  promotion, sampler ranking, or default-policy claim is made.
