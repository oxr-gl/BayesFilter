# P84 Phase 1 Result: Author Basis And Domain Parity

Date: 2026-06-23

Status: `BLOCK_P84_PHASE1_AUTHOR_BASIS_DOMAIN_PARITY_NOT_CLOSED`

## Phase Objective

Close or precisely block the gap between the author SIR basis/domain route
(`Lagrangep(4,8)` on `AlgebraicMapping(1)`) and the current local Legendre
diagnostic fitter.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is there a source-backed author-basis/domain parity path, or must local Legendre remain diagnostic-only? |
| Baseline/comparator | Zhao-Cui author SIR source, local Zhao-Cui paper/source ledgers, and P83/P84 local route documentation. |
| Primary criterion | A reviewed parity/adaptation decision with source anchors and tests, or a blocker. |
| Veto diagnostics | Claiming Legendre diagnostics equal author parity without review; missing author anchors. |
| Explanatory diagnostics | Basis cardinality, mapping semantics, local fitter compatibility. |
| Not concluded | No fit quality, correctness, rank convergence, production readiness. |
| Artifact | This Phase 1 result. |

## Source Support Summary

The local paper/source ledgers support using Zhao-Cui JMLR 2024 for the
sequential state-space TT/SIRT architecture, but not as evidence that the
current BayesFilter fixed Legendre/ridge route is paper-explicit:

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-source-support-ledger-2026-05-31.md:20`
  records the local JMLR PDF and allowed claims: state-space setup, sequential
  TT architecture, squared-TT approximation, evidence normalizer, and
  marginalization/KR map context.
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-source-support-ledger-2026-05-31.md:22`
  records inspected technical anchors for the sequential joint density,
  squared-TT density, normalizer/marginal architecture, and explicitly forbids
  treating the P15 fixed Legendre/Halton/ridge-ALS route as paper-explicit.
- A local `pdftotext` check of
  `.local_sources/highdim_nonlinear_filtering/zhao_cui_tt_sequential_learning_jmlr_23-0743.pdf`
  found Algorithm 1, Algorithm 2, and Section 6.3 SIR anchors.  Section 6.3
  defines the high-dimensional SIR benchmark and equation (37); it does not
  by itself certify the local BayesFilter basis/domain implementation.

## Author Source Anchors

The author SIR script fixes the concrete basis/domain route:

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:14-17`
  sets the SIR dimensions `d=0`, `m=18`, `n=9`, `T=20`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:39-45`
  sets `N=5e3`, `tau=10`, `sqr=1`, `dom = BoundedDomain([-1, 1])`, and
  constructs both `ApproxBases(Lagrangep(4, 8), dom, d + 2*m)` and
  `ApproxBases(Lagrangep(4, 8), AlgebraicMapping(1), d + 2*m)`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/ApproxBases.m:1-12`
  describes `ApproxBases` as tensor-product polynomial basis functions plus
  mappings from the approximation domain to the reference domain.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/ApproxBases.m:70-119`
  shows that `ApproxBases` stores and replicates the chosen one-dimensional
  basis and domain mapping across the requested dimension.

## Local BayesFilter Anchors

The current local route does not implement that author basis/domain parity:

- `bayesfilter/highdim/bases.py:55-73` defines `LegendreBasis1D` with
  `basis_dim = max_degree + 1`.
- `bayesfilter/highdim/bases.py:124-143` makes `ProductBasis` currently accept
  only `LegendreBasis1D`.
- `bayesfilter/highdim/source_route.py:2262-2269` constructs the P59 author SIR
  36d bounded-prep product basis with
  `LegendreBasis1D(BoundedInterval(-1.0, 1.0), fit_degree)`.
- `bayesfilter/highdim/source_route.py:3421-3427` constructs later fixed-TTSIRT
  product bases the same way.
- `tests/highdim/test_p59_author_sir_36d_target_fit.py:44-47` asserts the
  manifest records `no AlgebraicMapping(1) parity claim`.
- `docs/plans/bayesfilter-highdim-zhao-cui-p61-codex-source-faithfulness-reaudit-2026-06-12.md:45-46`
  independently classified this as `MISMATCH`: author SIR uses
  `Lagrangep(4,8)` with `AlgebraicMapping(1)`, while BayesFilter uses
  `LegendreBasis1D(BoundedInterval(-1,1), fit_degree)`.

## Classification Decision

| Route element | Classification | Reason |
|---|---|---|
| SIR model callback target | `source_faithful` for model formulas already anchored in prior P57/P83 artifacts | The author SIR model and callback semantics were previously anchored, but that does not close basis/domain parity. |
| Current local fixed Legendre basis/domain | `fixed_hmc_adaptation_diagnostic` | It is deterministic and useful for diagnostics, but it is not the author `Lagrangep(4,8)` plus `AlgebraicMapping(1)` route. |
| Author basis/domain parity | `blocked` | No local implementation or reviewed adaptation currently reproduces the author basis/domain route. |

## Decision

Phase 1 blocks production promotion:

```text
BLOCK_P84_PHASE1_AUTHOR_BASIS_DOMAIN_PARITY_NOT_CLOSED
```

The current local fixed Legendre route must remain diagnostic-only for
author-basis/domain parity.  It may support bounded implementation diagnostics,
but it cannot close the Zhao-Cui source-faithfulness gap or feed production
fitting gates as if it were author parity.

## Required Repair Before Phase 2 Fitting

Before Phase 2 can run production-relevant fitting, a reviewed Phase 1 repair
must do one of the following:

- implement a BayesFilter-owned author-basis/domain path matching
  `Lagrangep(4,8)` and `AlgebraicMapping(1)` with tests and manifests; or
- write a reviewed fixed-HMC adaptation contract explaining exactly which
  author operations are frozen or changed, why the change preserves the target
  phase scope, and why the resulting fitting evidence is allowed to feed Phase
  2; or
- keep the route blocked and skip production fitting.

Any repair must preserve TensorFlow/TFP as the BayesFilter algorithmic backend
and must not copy third-party code into production modules without a separate
license/reuse review.

## Local Checks

Phase 1 local checks passed:

- Required source/local basis scan found author `Lagrangep(4,8)`,
  `AlgebraicMapping(1)`, local `LegendreBasis1D`, source-faithfulness labels,
  and fixed-HMC adaptation labels across the expected source/code/doc surfaces.
- Focused anchor scan found the Phase 1 blocker status, author basis/domain
  anchors, local Legendre anchors, explicit `no AlgebraicMapping(1) parity
  claim`, and Phase 2 blocked handoff.
- `git diff --check` passed for P84 artifacts.
- Trailing-whitespace scan over P84 artifacts found no matches.

## Next-Phase Handoff

Phase 2 remains blocked for production-relevant fitting.  Its subplan must be
refreshed to require a Phase 1 repair or an explicit decision to keep Phase 2
blocked.  No fitting command, GPU command, validation command, or production
claim is authorized by this Phase 1 result.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Block Phase 1 parity closure. | PASS for precise blocker: author/source/local anchors identify the mismatch and route classification. | PASS: no Legendre-as-author-parity claim; no fitting or runtime launch. | Whether a clean TF/TFP author-basis/domain repair is worth implementing before fitting. | Draft/review a Phase 1 repair subplan or stop before Phase 2 fitting. | No fit quality, correctness, rank convergence, HMC readiness, LEDH agreement, scaling, or production readiness. |

## Final Status

`BLOCK_P84_PHASE1_AUTHOR_BASIS_DOMAIN_PARITY_NOT_CLOSED`
