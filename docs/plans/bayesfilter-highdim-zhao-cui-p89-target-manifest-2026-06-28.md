# P89 Target Manifest: Zhao-Cui SIR d18 Same-Scalar Branch Contract

Date: 2026-06-28

Status: `P89_TARGET_MANIFEST_REVIEWED_AGREE`

## Purpose

This manifest freezes the scalar and branch fields that later P89 value,
gradient, FD, HMC, GPU/XLA, packaging, and promotion phases must either use or
explicitly revise through a reviewed manifest update.

This manifest is not a correctness proof. It does not close the P88 missing
same-target source-backed reference bridge blocker, and it does not establish
source-route full-history analytical derivative readiness.

## Skeptical Audit

| Risk Checked | Result |
| --- | --- |
| Wrong baseline | Avoided. The inherited baseline is P88 `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE`, not correctness. |
| Proxy metric promoted | Avoided. Rank/degree stability, holdout residuals, ESS, replay, and finite normalizers are setup/evidence context only. |
| Missing stop conditions | Avoided. Later phases cannot use this manifest alone to run bridge, gradient, FD, HMC, GPU/XLA, production, or default-policy work. |
| Unfair comparison | Avoided by requiring same target, branch, retained objects, parameterization, basis/rank/order, sample clouds, schedules, and scalar before comparisons. |
| Hidden assumptions | Exposed. Basis/order/rank are setup-static choices; non-default basis choices are implementation/setup choices unless separately source-anchored. |
| Stale context | P88 Phase 3 and Phase 5 blockers remain binding. |
| Environment mismatch | This manifest was prepared from document/code/source inspection only. |
| Artifact usefulness | The field table below gives later phases exact fields to bind before value or gradient evidence is admissible. |

## Scalar Contract

The target scalar for P89 is the source-route sequential negative
log-physical-density contribution used to build and replay fixed TTSIRT
retained objects for the Zhao-Cui Austria SIR d18 route:

```text
target_id: zhao_cui_sir_austria_d18
pipeline_kind: author_sir_fixed_ttsirt_source_route
route_class: fixed_ttsirt_source_route
source ordering: [theta, x_t, x_{t-1}]
time index: t >= 1
```

At `t=1`, the prior term is the model prior over `[theta, x_0]`. At `t>1`,
the prior term is the previous retained object's marginal density over the
prefix `[theta, x_{t-1}]`. The scalar combines prior/previous-marginal,
transition, and likelihood terms in the same physical ordering.

All later value and gradient checks must bind the same scalar to the same
retained-object branch. FD may validate only the analytical gradient of this
same scalar; FD is not source correctness by itself.

## Field-Level Anchor Table

| Manifest field | Local code or artifact anchor | Paper / author-source anchor if any | Status | Field class |
| --- | --- | --- | --- | --- |
| Target id | `bayesfilter/highdim/source_route.py:102-103`; `:6701-6703`; `:6823-6827` | Author source anchor is indirect through local audited route; no standalone paper claim is asserted here. | fixed | implementation/setup choice tied to audited source route |
| Source-route pipeline kind | `bayesfilter/highdim/source_route.py:102`; `:6701-6705`; `:3217-3229` | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-38` for solve/push/reapprox/sample/weight loop. | fixed | fixed-HMC adaptation of author route |
| Physical target ordering `[theta, x_t, x_{t-1}]` | `bayesfilter/highdim/source_route.py:2385`; `:3248`; `:7981-7987` | `full_sol.m:14-17`, `:24-26`, `:132-135` uses `d+2m` current/previous state structure and target terms. | fixed | source claim adapted through local ordering contract |
| Parameter dimension | `bayesfilter/highdim/source_route.py:2223`; `:6836-6838` | SIR d18 local target has `d=0` parameter dimension in current route; no broader paper claim. | fixed for current P89 route | implementation/setup choice |
| State dimension | `bayesfilter/highdim/source_route.py:2225`; `:6836-6838` | Austria SIR d18 local model selection; no production-scale generality claim. | fixed for current P89 route | implementation/setup choice |
| Target dimension | `bayesfilter/highdim/source_route.py:113`; `:2388`; `:6836` | `full_sol.m:14-17` establishes `d+2m`; current route uses `0+2*18=36`. | fixed | fixed-HMC adaptation of author route |
| Time horizon used by current source-route skeleton | `bayesfilter/highdim/source_route.py:3030`; `:3204`; `:8086-8121` | `full_sol.m:21-43` supports sequential loop over `model.T`; P89 does not claim full-horizon production yet. | fixed for current bridge design entry; later phases may extend only by reviewed manifest update | implementation/setup choice |
| Prior term at `t=1` | `bayesfilter/highdim/source_route.py:8005-8014`; `:8063-8083` | `full_sol.m:72-75`; `:132-135` | fixed | source-route scalar component |
| Previous retained marginal at `t>1` | `bayesfilter/highdim/source_route.py:7894-7947`; `:8015-8025`; `:8123-8142` | `full_sol.m:75-80`; `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m:1-87`; `AbstractIRT.m:299-307` | fixed for value route; derivative propagation unresolved | source-route scalar component with derivative blocker |
| Transition term | `bayesfilter/highdim/source_route.py:7970-8039`; `:2434-2457` | `full_sol.m:132-135` calls `transition`. | fixed | source-route scalar component |
| Likelihood term | `bayesfilter/highdim/source_route.py:7970-8039`; `:2434-2457` | `full_sol.m:132-135` calls `like`. | fixed | source-route scalar component |
| Shift/normalizer terms | `bayesfilter/highdim/source_route.py:7879-7883`; `:8180-8192`; `:8492-8494` | `full_sol.m:90-94`; `:124`; `eval_irt_reference.m:41-42`, `:180-181` | fixed for value manifest; derivative unresolved | fixed-HMC adaptation of author route |
| Retained sample generation | `bayesfilter/highdim/source_route.py:7837-7891`; `:8159-8164` | `full_sol.m:33-38` generates samples through `eval_irt` and proposal correction weights. | fixed | fixed-HMC adaptation of author route |
| Retained object identity | `bayesfilter/highdim/source_route.py:8180-8206`; `:8430-8507` | No direct author hash mechanism; this is a local branch-stability guard. | fixed | implementation/setup choice |
| Retained carry between times | `bayesfilter/highdim/source_route.py:8112-8219`; `:6718-6725`; `:6851-6854` | `full_sol.m:75-80` consumes previous SIRT as a prior term. | fixed | fixed-HMC adaptation of author route |
| Source route operation coverage | `bayesfilter/highdim/source_route.py:52-63`; `:8042-8060`; `:8108-8110` | `full_sol.m:21-130` is the local operation audit source anchor. | fixed as audit precondition, not correctness | source-route coverage claim |
| Basis family | P88 Phase 1 result `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase1-degree-convergence-protocol-result-2026-06-27.md:59-64`; P88 Phase 2 result `:142-145` | No same-row author-source anchor is asserted here; the row records local reviewed basis classification only: `Lagrangep(4,8)` as the author-default reference classification in P88, and lower-degree comparators as `extension_or_invention`. | setup-static; current selected evidence includes lower-degree comparator but not a source-faithful default flip | implementation/setup choice requiring reviewed classification |
| TT rank | P88 Phase 2 result `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-convergence-execution-result-2026-06-27.md:142-145`; local rank tuple surfaces `bayesfilter/highdim/source_route.py:3278-3279` | Rank policy pass is local reviewed evidence, not a paper-scale correctness claim. | setup-static | implementation/setup choice |
| Sweep/order policy | `bayesfilter/highdim/source_route.py:2293`; `:3457`; `:3537` | No author-source general claim asserted here. | setup-static | implementation/setup choice |
| Seeds and sample clouds | `bayesfilter/highdim/source_route.py:3056-3069`; P88 Phase 2 result `:153` | `full_sol.m:22`, `:34`, `:55`, `:90` use random samples; P89 freezes seeds for differentiability/replay. | setup-static fixed-HMC adaptation | fixed_hmc_adaptation |
| Validation/holdout/audit split | P88 Phase 1 result `:70-77`, `:87-93`; P88 Phase 2 result `:90-94`, `:149-153` | No author-source claim; this is local training discipline. | fixed for future training evidence | implementation/setup choice |
| Training optimizer route | P88 Phase 1 result `:70-77`; P88 Phase 2 result `:149-152`; P86 Phase 6U result `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6u-l1-default-policy-result-2026-06-25.md:9-16` | No author-source claim; local owner policy. | fixed: training-base only | implementation/setup choice |
| L1 tuning policy | P86 Phase 6U result `:9-16`, `:22-36`; P88 Phase 2 result `:168-171` | No author-source claim; local owner policy. | fixed: L1 tuning default, zero-L1 comparator only | implementation/setup choice |
| XLA static fields | P89 master `docs/plans/bayesfilter-highdim-zhao-cui-p89-production-promotion-master-program-2026-06-28.md:118-131`; P89 runbook `docs/plans/bayesfilter-highdim-zhao-cui-p89-visible-gated-overnight-execution-plan-2026-06-28.md:75-78` | No author-source claim. | setup-static and must be remanifested if changed | implementation/setup choice |
| Correctness candidate | P88 Phase 3 result `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase3-same-target-bridge-design-result-2026-06-27.md:13-18`, `:98-100`; local fail-closed ladder `bayesfilter/highdim/source_route.py:6775-6779`, `:6864-6867` | No source-backed reference bridge found yet. | unresolved / blocked | scientific claim boundary |
| Source-route analytical derivative readiness | P88 Phase 5 result `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase5-source-route-derivative-design-result-2026-06-27.md:13-18`, `:48-77`; local source-route value surfaces `source_route.py:7894-8039`, `:7837-7891` | Derivative-capable author anchors: `eval_irt_reference.m:148-181`, `eval_rt_jac_reference.m:1-208`, `marginalise.m:1-87`, `AbstractIRT.m:275-307`; local full scalar derivative carry is missing. | unresolved / blocked | scientific claim boundary |

## Same-Scalar Invariants For Later Phases

Later value, gradient, FD, HMC, and GPU/XLA phases must preserve these
invariants unless a reviewed manifest revision states otherwise:

1. Same `target_id`, route class, source ordering, parameter/state/target
   dimensions, and time horizon.
2. Same physical scalar decomposition: prior or previous retained marginal,
   transition, likelihood, shift, affine determinant, and normalizer terms.
3. Same retained-object branch identity for any value/gradient/FD comparison.
4. Same basis/rank/order/sample/schedule setup for comparison arms, except
   where a reviewed subplan declares a single controlled comparator field.
5. Same parameterization for analytical gradient and FD perturbation.
6. Same validation/holdout/audit split for any future training evidence.
7. Same source-claim classification: source-faithfulness requires paper and
   author-source anchors; local setup choices cannot close source blockers.

## XLA Contract

Basis, basis order, number of elements, TT rank tuple, sweep/order policy,
target dimension, time horizon shape, sample-count shape, and branch identity
are setup-static for XLA purposes. Changing any of them may be valid, but it
creates a distinct manifest branch and can require retracing/recompilation and
fresh evidence. Runtime toggling of these fields inside one compiled claim is
forbidden.

## Nonclaims

- No `D18_CORRECTNESS_CANDIDATE`.
- No posterior correctness.
- No source-route analytical-gradient readiness.
- No FD validation.
- No HMC readiness.
- No GPU/XLA production readiness.
- No production-ready Zhao-Cui route.
- No LEDH agreement, d50/d100 scaling, or default-policy flip.

## Phase 2 Handoff

Phase 2 must design a same-target source-backed value bridge for exactly this
manifest. If Phase 2 cannot identify a source-backed bridge with tolerances,
Phase 2 must write a blocker result rather than execute a proxy comparison.

## Claude Review Status

Reviewed by bounded read-only Claude Opus max-effort review on 2026-06-28.

Iteration 1 returned `VERDICT: REVISE` for two fixable documentation issues:

- the basis-family row used source-faithfulness language without a same-row
  author-source anchor;
- the XLA-static row cited governance without line-level anchors.

Patch applied:

- rephrased the basis-family row as local reviewed classification only;
- added line anchors for the XLA-static governance sources.

Iteration 2 returned:

```text
VERDICT: AGREE
```
