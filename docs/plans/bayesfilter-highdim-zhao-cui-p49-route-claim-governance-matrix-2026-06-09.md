# P49 Route-Claim Governance Matrix

metadata_date: 2026-06-09
program: P49-source-faithful-repair
phase: P49-M0
status: EXECUTED_STATIC_AUDIT

## Purpose

This matrix prevents BayesFilter artifacts from conflating five distinct
Zhao--Cui-related routes:

- `source_understanding`;
- `source_faithful_filtering`;
- `gradient_bearing_adaptation`;
- `diagnostic_smoke`;
- `blocked`.

The central rule is that analytical gradients are a valid reason to maintain a
separate deterministic lane, but they are not a reason to call an altered route
source-faithful Zhao--Cui.  Likewise, tiny fixed-branch or fixed-grid tests may
be useful diagnostics, but they do not certify adaptive TT/SIRT reproduction.

## Route Labels

| Route label | Allowed claims | Required evidence before promotion | Forbidden claims |
| --- | --- | --- | --- |
| `source_understanding` | Source paper/code was read, crosswalked, summarized, or audited. | Source anchors, line/table references, no production code copied. | BayesFilter implements the same route; production readiness; adaptive TT/SIRT reproduction. |
| `source_faithful_filtering` | Clean-room BayesFilter route implements the material filtering mechanics: retained density/transport object, sample propagation, ESS/proposal correction, recentering, normalizer accounting, and relevant preconditioners. | P49 M1--M5 gates, source-route tests, route-specific result tokens, and Claude review. | Current fixed branch is source-faithful; all-grid pairwise propagation is paper-scale source route; source code copied into production. |
| `gradient_bearing_adaptation` | Deterministic fixed branch has replayable values and analytical gradients under its own contract. | Branch replay, value/gradient tests, scale-aware error rules, exact/dense/CUT4/source-route comparator where an accuracy claim is made. | HMC readiness by default; source-faithful adaptive Zhao--Cui; differentiating stochastic/adaptive source branches without a separate contract. |
| `diagnostic_smoke` | Tiny, bounded, proxy, or first-gate tests executed and their blockers are understood. | Explicit baseline, non-claims, result artifact, and no proxy promotion. | Production, paper-scale, high-dimensional scalability, or source-route equivalence. |
| `blocked` | A target is not promoted and has a named blocker or human decision. | Block token, blocker cause, repair path or human-required stop condition. | Silent pass; tolerance changes after seeing results; treating fixed-route failure as source-route failure. |

## P49 Phase Token Interpretation

| Phase token | Route interpretation | Promotion boundary |
| --- | --- | --- |
| `PASS_P49_M0_ROUTE_CLAIM_GOVERNANCE` | Claim governance passed. | No code repair or source-faithful filtering result. |
| `PASS_P49_M1_SOURCE_ROUTE_CONTRACT` | Source-route design contract passed. | No numerical accuracy claim. |
| `PASS_P49_M2_RETAINED_TRANSPORT_OBJECT` | Source-route retained-object skeleton or design passed. | No adaptive TT-cross production quality. |
| `PASS_P49_M3_SAMPLE_ESS_PROPOSAL` | Source-route sample/ESS/proposal mechanics passed for scoped tests. | No paper-scale accuracy or HMC readiness. |
| `PASS_P49_M4_RECENTERING_NORMALIZER` | Source-route recentering/Jacobian/normalizer accounting passed for scoped tests. | No target tuning or production claim. |
| `PASS_P49_M5_PRECONDITIONED_PREDATOR_PREY` | Predator-prey ladder separates route mismatch, tuning failure, and source-route evidence. | No production predator-prey token unless ladder passes its own criteria. |
| `PASS_P49_M6_SMOOTHING_BOUNDARY` | Smoothing claims are excluded or separately tested. | Filtering success is not smoothing success. |
| `PASS_P49_M7_GRADIENT_LANE_BOUNDARY` | Fixed-branch gradient lane has an honest adaptation contract. | Gradient success does not prove source-faithful filtering. |
| `PASS_P49_M8_INTEGRATION_CLOSEOUT` | P49 closeout table reconciles all routes and blockers. | No claim outside passed phase gates. |

The corresponding `BLOCK_P49_*` token means the phase did not pass and must not
be used as positive evidence for any route.

## Searchable Forbidden-Claim Patterns

Future reviews should search P30+ artifacts, highdim tests, and highdim code
for these patterns and classify any hit as allowed negative context, forbidden
promotion, or out-of-scope historical/source-paper language:

- `current fixed branch.*source[- ]faithful`
- `fixed[- ]branch evidence.*source[- ]route equivalence`
- `source[- ]faithful adaptive Zhao`
- `faithful adaptive Zhao`
- `adaptive MATLAB TT-cross/SIRT reproduction` outside non-claim,
  forbidden-token, or blocker text
- `PASS_ADAPTIVE_MATLAB_TT_CROSS_SIRT_REPRODUCTION` outside
  `forbidden_tokens`, tests asserting it is not promoted, or negative context
- `HMC readiness is validated` outside explicit forbidden-claim tests
- `paper-scale.*Zhao` outside a passed paper-scale gate or non-claim text

## Static Audit Summary

| Surface | Finding | Decision |
| --- | --- | --- |
| P48 discrepancy ledger and result | Correctly states P10/P34 are source-understanding only and fixed branch is a deterministic adaptation. | Use as M0 baseline. |
| Active P49 master/runbook/subplans | Route split is explicit; P49 pass/block tokens and required result paths are consistent. | No patch required. |
| P47 route registry and tests | The adaptive reproduction token appears only as a forbidden token or a test asserting it is not promoted. | Allowed negative context. |
| `bayesfilter/highdim/filtering.py` | Multistate fixed-design path docstring says it is not adaptive TT-cross, SIRT, or paper-scale Zhao--Cui reproduction. | Correct current boundary. |
| P30--P47 highdim tests | Hits are mostly non-claims, forbidden-token checks, or bounded fixed-branch tests. | No M0 patch required. |
| P32--P41 fixed-SGQF companion drafts | Phrase "source-faithful comparison" refers to a Jia--Xin--Cheng SGQF source-paper benchmark, not Zhao--Cui route fidelity. | Out of M0 Zhao--Cui scope; no patch. |

## Patch List

No scoped claim-language patch was applied in M0.  The static audit did not find
an active/current artifact that says or implies the current fixed branch is a
source-faithful adaptive Zhao--Cui implementation.  Historical and companion
note wording is preserved when it is either negative context, a non-claim, a
forbidden-token test, or non-Zhao--Cui source-paper language.

## Follow-Up Guardrail

P49 implementation phases must cite this matrix when assigning a route label to
new code, tests, manifests, or result artifacts.  If a result uses fixed-branch
or diagnostic evidence, it must explicitly say why that evidence is not being
promoted to source-faithful filtering.
