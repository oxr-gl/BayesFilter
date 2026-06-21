# Generic Fixed-Branch Zhao--Cui Analytical-Derivative Implementation Plan

**Date:** 2026-06-20
**Scope:** Generic fixed-branch TT / KR analytical derivative lane in `bayesfilter.highdim`, with KSC-mixture and exact-transformed SV wrappers treated as downstream instantiations rather than the implementation target itself.

## Context

The canonical monograph chapters included by `docs/main.tex` now carry the missing implementation-critical derivative links for the generic fixed-branch Zhao--Cui lane:

- explicit retained-numerator contractions `a_t` and `\dot a_t`
- explicit retained-filter storage / query semantics for next-step closure

This resolves the documentation-side ambiguity that previously forced readers back into support notes for implementation-grade detail.

The code situation is now:
- the generic fixed-design TT **value** path exists in `bayesfilter/highdim/filtering.py`
- low-level derivative primitives exist in `bayesfilter/highdim/derivatives.py`
- but there is still no end-to-end generic fixed-branch TT **score** path
- current Zhao--Cui score-style evidence still relies on autodiff wrappers in tests / score API, which is not sufficient analytical certification for this lane

So the next task is to implement a generic analytical derivative for the fixed-branch Zhao--Cui route itself, then let specific wrappers such as KSC mixture and exact transformed SV call into that generic lane.

## Question

How should BayesFilter implement a generic analytical derivative for the fixed-branch Zhao--Cui TT / KR lane so that:
1. the derivative is of the same frozen-branch scalar as the value path,
2. retained-object closure is propagated correctly across time,
3. wrapper routes can reuse the lane without becoming KSC-specific,
4. and certification can rely on same-branch finite differences rather than autodiff through `tf.linalg.lstsq(fast=False)`?

## Evidence contract

### Engineering question
Can we wire the existing fixed-branch TT derivative primitives into a generic score path that is structurally parallel to the current value path and returns a certified fixed-branch score artifact?

### Baseline / comparator
- Baseline value path: `bayesfilter/highdim/filtering.py:775-986`
- Baseline derivative primitives: `bayesfilter/highdim/derivatives.py:490-669`
- Structural comparison pattern: `bayesfilter/highdim/sv_mixture_cut4.py:1035-1156`
- Same-branch certification standard: canonical `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`

### Primary pass criterion
A new generic TT score path returns finite value-and-score results for small fixed-branch fixtures and passes same-branch finite-difference checks with explicit branch-identity validity.

### Veto diagnostics
- branch identity mismatch between base and perturbed runs
- copied-core or reused-perturbed-core behavior
- nonfinite retained derivative objects
- derivative solve failure / condition-number veto
- mismatch between value-path branch record and derivative-path branch record

### Explanatory-only diagnostics
- absolute / relative score error within valid FD windows
- condition-number summaries when below veto thresholds
- retained moment / retained coefficient summaries

### What this will not conclude, even if it passes
- no claim of source-faithful adaptive Zhao--Cui TT-cross/SIRT reproduction
- no claim of high-dimensional scalability
- no claim of HMC readiness by default
- no claim that KSC-specific or native generalized-SV wrapper APIs are production-ready

### Artifact
This plan note plus a follow-on implementation result note under `docs/plans/`.

## Mechanism being implemented

The mechanism is a **generic fixed-branch TT score path** parallel to the existing value path:

1. build the same adjacent target on the same frozen branch,
2. differentiate the square-root target values on that branch,
3. replay the same deterministic TT fitting sweep while propagating dotted core states,
4. differentiate squared-TT normalizers and retained numerators,
5. build the normalized retained derivative object for the next step,
6. aggregate score increments over time,
7. return a fixed-branch score artifact with replay / FD evidence.

## Proposed implementation shape

### 1. Add a generic score-path entrypoint in `bayesfilter/highdim/filtering.py`

Add a sibling to:
- `scalar_nonlinear_fixed_design_tt_value_path(...)`

Proposed target shape:
- `scalar_nonlinear_fixed_design_tt_score_path(...)`

This function should accept the same frozen-branch inputs as the value path plus derivative configuration and return a generic score artifact, likely reusing `FixedBranchScoreResult` from `bayesfilter/highdim/derivatives.py`.

It should remain generic over the nonlinear model and target family; wrappers like KSC mixture and exact transformed SV should sit above it.

### 2. Introduce derivative-aware adjacent-target builders

Current target builders are value-only:
- `scalar_nonlinear_initial_adjacent_target_batch(...)`
- `scalar_nonlinear_transition_adjacent_target_batch(...)`

Add derivative-aware variants or shared helpers that produce:
- forward target values
- dotted target values for the declared parameter coordinate(s)
- any branch metadata needed to certify same-scalar reuse

These helpers must implement the canonical derivative ledger:
- `\widetilde q_{t,j}`
- `\dot{\widetilde q}_{t,j}`
- `y_j=e^{c_t/2}\sqrt{\widetilde q_{t,j}}`
- `\dot y_j=e^{c_t/2}\dot{\widetilde q}_{t,j}/(2\sqrt{\widetilde q}_{t,j})`

and must preserve the fixed-branch assumptions on domains, points, basis, Jacobian convention, and floors.

### 3. Add a derivative replay driver around `FixedTTFitter.fit`

The low-level derivative primitives already exist, but there is no driver that follows the actual realized forward sweep sequence and emits dotted cores on the same branch.

Needed layer:
- replay the forward sweep order from the value path
- rebuild current environments after each core update
- compute `\dot A_k`, `\dot N_k`, `\dot d_k`
- solve `N_k\dot g_k=\dot d_k-\dot N_kg_k`
- update dotted cores and mark stale caches for recomputation

This driver should be aligned with the same sweep rule / cached-environment discipline already documented in canonical `ch36b`.

### 4. Add retained-object derivative propagation

This is the main missing mathematical-to-code bridge.

Implement helpers for:
- dotted right-mass contractions / normalizer derivative
- dotted left-mass contractions for retained numerators
- retained numerator derivative `\dot a_t`
- normalized retained derivative object `\dot{\widehat p}_t`
- storage of the retained coefficient matrix / evaluator and its dotted companion

The code should match the canonical chapter contract:
- coefficient object `Q_t`
- derivative object `\dot Q_t`
- normalized evaluator `P_t`
- derivative evaluator `\dot P_t`
- query rule over the previous-state block of the next step’s fitting points

### 5. Package the result as a true fixed-branch score artifact

Use or extend:
- `FixedBranchReplayTape`
- `FiniteDifferenceTable`
- `FixedBranchScoreResult`

The score path should return:
- scalar log likelihood
- score vector
- branch identity
- replay tape hash
- finite-difference evidence table
- diagnostics explaining branch validity, derivative solve status, retained evaluator status, and nonclaims

### 6. Add thin wrapper score functions above the generic lane

After the generic score path exists, wrappers can expose route-specific APIs such as:
- exact transformed SV fixed-branch TT score
- KSC-mixture fixed-branch TT score

But those wrappers should do only:
- observation-model / parameterization setup
- coordinatewise or panel aggregation
- diagnostics appropriate to that wrapper

They should not own the generic TT derivative mechanics.

## Critical files to modify

### Primary implementation files
- `bayesfilter/highdim/filtering.py`
- `bayesfilter/highdim/derivatives.py`
- `bayesfilter/highdim/sv_mixture_cut4.py`

### Possible support files
- `bayesfilter/highdim/score_api.py` (only if a score API entrypoint should call the new lane rather than autodiff)
- `bayesfilter/highdim/__init__.py` (exports)

### Primary tests to add/update
- `tests/highdim/test_p47_generalized_sv_equality.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- new focused generic fixed-branch TT derivative tests under `tests/highdim/`

## Verification plan

### Smallest focused diagnostics first
1. unit-test the derivative-aware fixed LS replay on tiny scalar fixtures
2. unit-test retained-numerator / retained-filter derivative helpers separately
3. add a one-step scalar TT fixed-branch score fixture with exact or dense reference comparison
4. add short multi-step same-branch finite-difference tests
5. only then wire wrapper-level evidence for exact transformed SV and KSC-mixture panel routes

### Commands
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_fixed_branch_derivatives.py \
  tests/highdim/test_p30_fixed_branch_gradient_tables.py

CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py \
  tests/highdim/test_p47_generalized_sv_equality.py
```

Add a new focused test module for the generic score path and run it first before broad wrapper suites.

## Expected failure modes
- derivative replay diverges from the actual forward sweep state
- retained numerator derivative uses the wrong retained-coordinate query rule
- value path and derivative path disagree on the fixed branch identity
- derivative path silently assumes scalar retained objects and fails to generalize
- wrapper APIs reintroduce autodiff-based score evidence instead of consuming the analytical lane

## What would change the next step
- If same-branch scalar fixtures fail before wrapper integration, stop and repair the generic lane first.
- If the generic lane passes scalar exact-transformed SV but KSC wrappers still fail, treat that as a wrapper/model-layer issue rather than a generic TT derivative failure.
- If multistate retained-query storage becomes too heavy in coefficient-matrix form, document a TT/low-rank retained-storage variant, but preserve the same evaluator contract.

## Implementation sequencing
1. Introduce the generic scalar fixed-branch TT score-path skeleton.
2. Add derivative-aware target-value helpers.
3. Add TT sweep replay / dotted-core driver.
4. Add retained-numerator and retained-filter derivative propagation.
5. Package `FixedBranchScoreResult` outputs.
6. Add focused scalar tests.
7. Wire exact-transformed SV wrapper.
8. Wire KSC-mixture wrapper.
9. Revisit score API / equality tests to replace autodiff score evidence with the analytical lane.

## Nonclaims
- No source-faithful adaptive Zhao--Cui claim.
- No paper-scale TT-cross/SIRT reproduction claim.
- No HMC-readiness promotion from this implementation step alone.
- No high-dimensional scaling claim from tiny fixed-branch validation fixtures.
