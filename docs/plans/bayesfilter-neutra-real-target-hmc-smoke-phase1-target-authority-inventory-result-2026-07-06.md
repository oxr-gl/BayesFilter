# BayesFilter NeuTra Real Target HMC Smoke Phase 1 Result

Date: 2026-07-06

## Status

`PASSED_INVENTORY_DESIGN_ONLY`

## Phase Objective

Inventory whether BayesFilter has enough real c603 target/value-score authority
to replace the synthetic quadratic base adapter used by the c603 mechanics
fixture.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Is there a reviewed real c603 target/value-score authority in BayesFilter that can support Phase 2 adapter work? |
| Baseline/comparator | Existing `GenericSSMPosteriorAdapter`, c603 import/mechanics fixture results, c603 handoff proposal/preflight, and local BayesFilter code inventory. |
| Primary criterion | Passed as an inventory: next boundary is `design_only`, not `bridgeable_real_target_adapter`. |
| Veto diagnostics | No historical `dsge_hmc` code was treated as live BayesFilter authority; no prior/filter/data fields were invented; synthetic mechanics were not promoted. |
| Explanatory diagnostics | BayesFilter has generic adapter and transport mechanics surfaces, but lacks the live c603 Rotemberg prior/model/filter value-score wrapper. |
| Not concluded | No adapter correctness, no HMC readiness, no posterior correctness, no production readiness. |
| Artifact | This Phase 1 inventory result and refreshed Phase 2 subplan. |

## Classification

The Phase 1 classification is:

```text
design_only
```

BayesFilter has enough metadata and external source anchors to design the next
adapter-authority bridge, but it does not yet have a BayesFilter-owned callable
real c603 target adapter.

This classification is deliberately weaker than `bridgeable_real_target_adapter`
and deliberately different from `blocked_missing_real_target_authority`:

- not `bridgeable_real_target_adapter`: the live BayesFilter repo does not
  contain the c603 Rotemberg prior/model/filter value-score callable needed for
  mechanics or HMC;
- not `blocked_missing_real_target_authority`: the c603 handoff contains exact
  source anchors, preflight evidence, target metadata, and callable names needed
  to plan a reviewed BayesFilter port/reconstruction attempt;
- therefore `design_only`: Phase 2 may plan and attempt the smallest reviewed
  adapter-authority bridge, but Phase 2 must stop fail-closed if the source
  anchors cannot be ported without inventing model, prior, filter, data, or
  runtime fields.

The practical effect is a hard non-authorization for real-target mechanics and
HMC until Phase 2 produces a BayesFilter-owned callable adapter with finite
batch value/score probes and the unchanged c603 target signature.

## Inventory

| Surface | Status | Evidence |
| --- | --- | --- |
| c603 target identity and stable signature | Present as metadata/import evidence | `docs/plans/bayesfilter-neutra-c603-handoff-import-validation-result-2026-07-06.md` computed `stable_ssm_target_signature = 8f5caae87797898bd8d4f0c795246f5103e3535e247a49e5ebf01217ece20d07`; follow-up import result validated the transport payload. |
| Frozen dense-IAF import | Present | `docs/plans/bayesfilter-neutra-c603-followup-import-validation-result-2026-07-06.md` records successful finalization/load and legacy forward/logdet parity. |
| Generic posterior adapter | Present but requires callables | `bayesfilter/ssm/target_builder.py` requires `prior_log_prob_and_grad` and `filter_log_likelihood_and_grad` callables and validates rank-2 batch value/score outputs. |
| Fixed-transport mechanics binding | Present but target-agnostic | `bayesfilter/inference/fixed_transport_hmc.py` can bind a loaded transport to a base adapter and run finite mechanics checks. |
| Existing c603 mechanics fixture | Synthetic base target only | `tests/test_fixed_transport_hmc_binding_c603_fixture.py` binds c603 transport to `BatchedQuadraticAdapter`; this is correct mechanics evidence but wrong relative to a real Rotemberg target-adapter claim. |
| BayesFilter nonlinear batched principal-sqrt kernel | Partially present | `bayesfilter/nonlinear/experimental_batched_svd_sigma_point_tf.py` exposes `tf_batched_svd_sigma_point_value_and_score(..., backend="tf_principal_sqrt_ukf")`; it is experimental and does not by itself build c603 Rotemberg model/prior callables. |
| c603 handoff target wrapper | External source anchor only | The dsge_hmc handoff script calls `model.rotemberg_second_order_svd_bayesfilter_model_and_derivatives`, `tf_batched_svd_sigma_point_value_and_score_custom_gradient`, and `model.log_prior_value_and_score_analytical_batch`. Those names are not live BayesFilter callables in this repo. |
| Rotemberg prior and transform authority | External source anchor only | Handoff proposal and preflight name `RotembergNKEstimable` methods, but BayesFilter does not currently contain a local `RotembergNKEstimable` target adapter. |

## Exact Missing Authority For Phase 2

Phase 2 must either port/reconstruct these pieces into BayesFilter or write a
blocker result:

| Required piece | Current status | Source anchor |
| --- | --- | --- |
| c603 model/derivative builder | Missing in BayesFilter | `/tmp/dsge_hmc-neutra-handoff-20260705/scripts/prepare_neutra_rotemberg_second_order_svd_target.py:305-319` calls `model.rotemberg_second_order_svd_bayesfilter_model_and_derivatives(u_batch)`. |
| c603 filter likelihood value/score wrapper | Missing in BayesFilter under the handoff name | Same handoff lines call `tf_batched_svd_sigma_point_value_and_score_custom_gradient(...)`; BayesFilter currently exposes `bayesfilter/nonlinear/experimental_batched_svd_sigma_point_tf.py:1271` as `tf_batched_svd_sigma_point_value_and_score(...)`, not the handoff wrapper. |
| c603 analytical prior value/score | Missing in BayesFilter | `/tmp/dsge_hmc-neutra-handoff-20260705/scripts/prepare_neutra_rotemberg_second_order_svd_target.py:321-323` calls `model.log_prior_value_and_score_analytical_batch(u_batch)`. |
| c603 posterior composition | Missing in BayesFilter | `/tmp/dsge_hmc-neutra-handoff-20260705/scripts/prepare_neutra_rotemberg_second_order_svd_target.py:447-459` identifies `RotembergSecondOrderSVDBayesFilterPosterior` and the required call path. |

These source anchors are not execution authority. They are inputs to a Phase 2
port/reconstruction plan. Phase 2 must not import live `dsge_hmc` modules as
BayesFilter authority unless a separately reviewed boundary approves that
runtime dependency.

## Direct Verdicts

| Statement | Classification | Support |
| --- | --- | --- |
| BayesFilter can load the c603 frozen transport against the c603 target signature. | `correct` | Prior c603 follow-up import validation passed. |
| BayesFilter can run c603 fixed-transport mechanics with a synthetic base adapter. | `correct` | Prior c603 mechanics fixture passed. |
| BayesFilter currently has a real c603 Rotemberg posterior adapter callable ready for mechanics/HMC. | `unsupported` | Local search found no BayesFilter-owned `RotembergSecondOrderSVDBayesFilterPosterior`, no `rotemberg_second_order_svd_bayesfilter_model_and_derivatives`, no `tf_batched_svd_sigma_point_value_and_score_custom_gradient`, and no local Rotemberg analytical prior callable in BayesFilter code. |
| Synthetic quadratic mechanics can be called real c603 target mechanics. | `wrong relative to the stated target` | The synthetic fixture computes a quadratic base target, not the Rotemberg posterior. |
| The dsge_hmc handoff source can be copied or executed as live BayesFilter authority without a port/review gate. | `unsupported` | Phase 1 was read-only inventory; Phase 2 must define the port/reconstruction boundary. |

## Phase 2 Handoff

Phase 2 must be an adapter-authority bridge, not a direct real-target mechanics
or HMC phase.

Required Phase 2 work:

- choose an explicit bridge route: port the minimal c603 target wrapper into
  BayesFilter, or write a fail-closed blocker if that requires unapproved
  dsge_hmc/runtime/model-file boundaries;
- materialize an untransported `SSMTargetContract` whose stable signature
  remains `8f5caae87797898bd8d4f0c795246f5103e3535e247a49e5ebf01217ece20d07`;
- expose separate batch-native `prior_log_prob_and_grad` and
  `filter_log_likelihood_and_grad` callables, or document exactly why they
  cannot be ported safely;
- prove finite rank-2 batch values/scores on tiny c603 preflight probes before
  any c603 real-target mechanics;
- preserve nonclaims: no HMC convergence, no posterior correctness, no
  production readiness, no default-policy change.

## Local Checks

Required local checks for this close:

```text
test -f docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase1-target-authority-inventory-subplan-2026-07-06.md
test -f docs/plans/bayesfilter-neutra-c603-followup-import-validation-result-2026-07-06.md
test -f /tmp/dsge_hmc-neutra-handoff-20260705/docs/plans/bayesfilter-neutra-export-proposal-c603-rotemberg-second-order-svd-2026-07-05.json
rg -n "def tf_batched_svd_sigma_point_value_and_score" bayesfilter/nonlinear/experimental_batched_svd_sigma_point_tf.py
absence check for c603 real-target wrapper symbols in BayesFilter Python code
git diff --check -- new Phase 1/Phase 2/review artifacts
```

Result:

```text
PHASE1_LOCAL_CHECKS_OK
```

## Claude Review

Round 1 review gate:

```text
REVIEW_STATUS=revise
VERDICT=REVISE
SUMMARY_JSON=/home/chakwong/BayesFilter/.claude_reviews/20260706-154335-bayesfilter-neutra-real-target-hmc-smoke-phase1/status.json
```

The primary review timed out after the health probe returned `OK`; the bounded
fallback responded that the packet did not contain enough detail to distinguish
`design_only` from a terminal missing-authority blocker and that the missing
real-target bridge must remain explicitly non-authorizing.

Repair:

- added the explicit classification rule above;
- listed the exact missing authority pieces and handoff source anchors;
- preserved the hard non-authorization for mechanics, HMC, GPU, training, and
  posterior/product/scientific claims.

Round 2 review is pending.

Round 2 Claude gate:

```text
REVIEW_STATUS=probe_timeout
VERDICT=NONE
SUMMARY_JSON=/home/chakwong/BayesFilter/.claude_reviews/20260706-161225-bayesfilter-neutra-real-target-hmc-smoke-phase1-r2/status.json
```

Direct tiny probe after the gate timeout:

```text
timeout 90s claude -p "Return exactly CLAUDE_PROBE_OK."
exit_status: 124
```

Because the tiny direct probe also timed out, Claude is classified as
unavailable for this Phase 1 gate. Per the runbook, Phase 1 review is being
substituted with a fresh Codex read-only review.

Substitute Codex review:

```text
status: agreed
agent_id: 019f3682-8aa1-77c0-a7e9-8cae370612f5
verdict: VERDICT: AGREE
```

Reviewer summary:

- no blocking findings;
- `design_only` is coherent and fail-closed;
- Phase 2 authorizes only a source-anchored bridge attempt or blocker;
- residual risk is bounded because insufficient portable authority remains a
  Phase 2 blocker.

## Nonclaims

- no real c603 adapter implementation has been accepted;
- no c603 real-target mechanics pass has been produced;
- no HMC, GPU, or training has been run;
- no posterior correctness, production readiness, scientific promotion, or
  default-policy claim is made.
