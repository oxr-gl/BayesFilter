# P39 Master Plan: Gaussian-Mixture CUT4 Comparator For Transformed SV

metadata_date: 2026-06-06
phase: P39

## Decision Target

Create a source-governed Gaussian-mixture CUT4 comparator for transformed
stochastic-volatility models, document the method self-containedly in the
LaTeX chapter, and compare the resulting mixture-CUT4 value path against
dense mixture references and the existing scalar SV TT lane where the target
semantics match.

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_REVIEW_WITH_BOUNDARIES`.

- Wrong baseline risk: native SV likelihood, transformed mixture likelihood,
  mixture CUT4, and scalar TT value paths are not the same object by default.
  The plan therefore compares mixture CUT4 first against a dense
  transformed-mixture reference, and compares against TT only through the
  already validated native scalar SV lane as an explanatory approximation
  gap unless a same-target TT mixture lane is added.
- Proxy metric risk: finite values and single-run closeness are not production
  evidence.  The primary local criterion is equivalence against a dense
  mixture reference on pinned tiny fixtures; native SV and TT comparisons are
  explanatory unless explicitly same-target.
- Semantic mismatch risk: the current P38 boundary remains true for direct
  native SV.  P39 introduces a new transformed Gaussian-mixture approximation,
  not a direct native CUT4 likelihood.
- Hidden Gaussianization risk: a one-component Gaussian approximation is not
  allowed as the promoted comparator.  The seven-component mixture table is
  pinned in the LaTeX chapter, code diagnostics, and tests as the BayesFilter
  P39 approximation contract.  The KSC table convention was checked from an
  accessible working-paper PDF during this gate: KSC tabulates locations for
  \(U_t+1.2704\), so the implementation uses effective means
  \(a_j-1.2704\) for \(U_t=\log\epsilon_t^2\).
- Missing stop conditions: stop if mixture weights are invalid, transformed
  observations are nonfinite, dense mixture reference fails, CUT4 diagnostics
  are nonfinite, or the implementation silently promotes native SV equivalence.
- CUT4 overread risk: on the scalar simple-SV transformed mixture fixture, the
  conditional component observation is linear Gaussian, so parity validates
  mixture bookkeeping, log-sum-exp normalization, moment collapse, and CUT4
  reduction to the exact Gaussian component update.  It does not validate
  nonlinear CUT4 accuracy unless a same-target nonlinear fixture is added.
- Artifact adequacy: plan, source ledger, claim ledger, LaTeX section, tests,
  result note, and Claude review ledger are required before promotion.

## Evidence Contract

Question: can BayesFilter build a transformed stochastic-volatility
Gaussian-mixture CUT4 comparator whose local value path agrees with an
independent dense transformed-mixture reference on small pinned fixtures?

Comparator ladder:

1. native scalar SV dense quadrature from P37-M2/M2.5;
2. transformed Gaussian-mixture dense quadrature;
3. transformed Gaussian-mixture CUT4;
4. existing scalar SV TT lane, recorded only as an explanatory approximation
   comparison unless a same-target mixture TT lane is implemented.

Primary pass/fail criterion:

- for pinned one-step and two-step scalar SV transformed-mixture fixtures,
  mixture-CUT4 log evidence and retained mean/variance agree with dense
  transformed-mixture reference inside declared local tolerances.  This is a
  local bookkeeping/component-update contract, not nonlinear CUT4 accuracy
  evidence.

Veto diagnostics:

- mixture weights do not sum to one;
- any mixture variance is nonpositive;
- transformed observations are nonfinite;
- dense mixture reference is nonfinite;
- CUT4 component diagnostics are nonfinite;
- component normalizer weights do not sum to one after normalization;
- native SV equivalence or production default is claimed;
- TT comparison is treated as same-target evidence without a same-target TT
  mixture lane with the same transformed-mixture likelihood, offset, mixture
  table, horizon, parameter values, and fixture observations;
- scalar transformed-mixture parity is described as validating nonlinear CUT4
  accuracy rather than the finite-mixture bookkeeping and Gaussian component
  update.

Explanatory diagnostics:

- native dense SV versus transformed mixture dense gap;
- scalar TT native lane versus mixture-CUT4 gap;
- component posterior weights and CUT4 point count.

What will not be concluded:

- no exact native SV likelihood claim;
- no KSC importance reweighting implementation;
- no full publication-grade SV literature review;
- no CNS generalized-SV implementation or source-governed CNS equation
  support until exact primary-source technical anchors are inspected;
- no nonlinear CUT4-specific accuracy claim from the current scalar linear
  conditional mixture fixtures;
- no full Chib--Nardari--Shephard generalized SV estimator;
- no paper-scale `T=1000` or S&P 500 result;
- no adaptive MATLAB TT-cross/SIRT reproduction;
- no HMC, DSGE, GPU, derivative, or stable public API readiness;
- no production default change.

Artifacts:

- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- `docs/references.bib`
- `bayesfilter/highdim/sv_mixture_cut4.py`
- `tests/highdim/test_p39_sv_mixture_cut4.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p39-sv-mixture-cut4-*.md`

## Literature And Source Governance

Primary sources:

- Zhao--Cui P30 SV equations and BayesFilter source-governance ledgers.
- Zhao--Cui MATLAB audit tree: `eg2_sv/mainscript.m` and SV model helpers.
- Kim, Shephard, and Chib (1998), for transformed SV and normal-mixture
  approximation context.  Current P39 source status includes checked
  working-paper anchors for the log-square transform, offset representation,
  seven-component Table 4, and \(-1.2704\) component-location shift.
- Chib, Nardari, and Shephard (2002), for generalized SV likelihood context.
  Current P39 source status is contextual only until the exact technical
  equations are inspected.

Literature ledgers:

- source-support ledger: inspect technical anchors and permitted claims;
- claim-support ledger: map every document/code claim to source or project
  derivation;
- omitted-paper-risk ledger: record likely reviewer objections.

Network metadata is useful but not required for this execution.  Citation counts
and venue rankings are not used as correctness evidence.

## Implementation Plan

1. Add a scoped highdim experimental module implementing:
   - pinned seven-component Gaussian-mixture parameters for `log(epsilon^2)`;
   - `transformed_sv_observations(y, offset)`;
   - dense transformed-mixture scalar SV reference;
   - mixture-CUT4 scalar SV recursion with component-wise additive-Gaussian
     structural models.
2. Export the symbols only from `bayesfilter.highdim`.
3. Add tests for:
   - mixture invariants;
   - transform domain and finite likelihood;
   - one-step dense mixture versus mixture-CUT4 equivalence;
   - two-step dense mixture versus mixture-CUT4 equivalence;
   - native dense/TT comparisons marked explanatory;
   - public API subpackage-only guard.
4. Update traceability ledger with a P39 row.
5. Add a self-contained LaTeX section after the high-degree cubature discussion
   and before tensor-product GHQF.
6. Run CPU-only focused and highdim guardrail tests.

## Claude Review Gates

Review loops run until convergence or max 5 iterations:

1. P39 math/literature/implementation plan review.
2. P39 code/governance review after implementation.
