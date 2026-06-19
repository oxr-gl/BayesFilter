# Fixed-SGQF KSC Surrogate SV Route-Gap Follow-up Plan

metadata_date: 2026-06-18
program_id: fixed-sgqf-ksc-surrogate-sv-route-gap
status: PLANNING_READY

## Purpose

This follow-up plan exists because
[bayesfilter-fixed-sgqf-ksc-surrogate-sv-plan-2026-06-17.md](docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-sv-plan-2026-06-17.md)
was found to be blocked at execution time.

The blocked step assumed an already-existing same-target Fixed-SGQF route for
 the KSC Gaussian-mixture surrogate stochastic-volatility target. That route is
 not currently present in the repo.

This artifact narrows the next work to **designing and, if approved,
implementing a same-target KSC-surrogate Fixed-SGQF adapter/value/score path**
with an explicit claim boundary.

## Current grounded facts

Confirmed by restart audit:
- same-target surrogate routes currently exist for:
  - Kalman mixture enumeration,
  - CUT4,
  - Zhao-Cui fixed-design TT.
- evidence anchors include:
  - `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
  - `tests/highdim/test_p47_generalized_sv_equality.py`
  - `bayesfilter/highdim/sv_mixture_cut4.py`
- the surrogate truth anchor remains:
  - `ksc_sv_gaussian_mixture_kalman_enumeration`
- current Fixed-SGQF machinery is additive-Gaussian and moment-based, with
  interfaces centered on:
  - `TFFixedSGQFNonlinearModel`
  - `TFFixedSGQFAffineModel`
  - `tf_fixed_sgqf_filter`
  - `tf_fixed_sgqf_score`
- no current deterministic-filter coverage row or benchmark artifact advertises
  a Fixed-SGQF algorithm on
  `sv_ksc_gaussian_mixture_surrogate_dim_1_2_3`.

## Design question

What is the smallest reviewed same-target route that would let Fixed-SGQF
produce a value and gradient on the declared KSC surrogate target without
silently changing the target?

## Candidate implementation directions

### Option A — mixture-collapsed observation route
Build a dedicated Fixed-SGQF KSC surrogate model whose observation evaluation is
 the finite Gaussian-mixture likelihood itself:
- keep SGQF as the state quadrature rule,
- evaluate the KSC finite-mixture observation density at each SGQF point,
- normalize by weighted log-sum-exp over the fixed cloud,
- derive/implement the analytic score or a reviewed autodiff-compatible score
  route on the same declared target.

Pros:
- target-faithful to the declared KSC surrogate likelihood.
- avoids pretending the route is additive-Gaussian.

Main risks:
- current `tf_fixed_sgqf_filter` is Kalman-update shaped and assumes Gaussian
  observation closure through `observation_covariance`.
- likely requires a new value/score path rather than a light adapter.

### Option B — per-mixture-component SGQF collapse route
For each KSC mixture component tuple:
- run a Gaussian observation SGQF update conditional on that tuple,
- then collapse component posteriors exactly, analogous to the Kalman/CUT4
  component-collapse structure already present in `sv_mixture_cut4.py`.

Pros:
- closely mirrors the currently admitted same-target Kalman and CUT4 surrogate
  construction.
- may fit the existing Gaussian-observation SGQF recursion better.

Main risks:
- requires explicit component enumeration logic around SGQF.
- gradient path must differentiate through the component collapse and branch
  identity contract.
- may still require new interfaces or wrappers for score support.

### Option C — do not implement SGQF for this row
Leave SGQF blocked on KSC surrogate SV and move to another family where a real
 same-target SGQF route already exists.

Pros:
- no target mismatch risk.
- cheapest governance-safe path.

Main risks:
- leaves an intended SGQF comparison gap unresolved.

## Skeptical plan audit

Main failure modes to prevent:
1. building an additive-Gaussian approximation and then labeling it as the KSC
   surrogate target.
2. using CUT4/Zhao-Cui same-target evidence as if it implied SGQF availability.
3. introducing a new SGQF route without updating deterministic coverage,
   reference-oracle evidence, and explicit nonclaims.
4. using a score route that breaks the same-branch contract or changes the
   branch under finite-difference checks.

Blocking rule:
- if the proposed route cannot state exactly where the finite-mixture likelihood
  enters the SGQF value computation, do not implement.

## Evidence contract

Question:
- Can we construct a same-target Fixed-SGQF value/gradient route for the KSC
  Gaussian-mixture surrogate SV target without target mismatch?

Baseline / comparator:
- Kalman mixture enumeration is the truth anchor.
- existing same-target CUT4 and Zhao-Cui routes are implementation comparators,
  not truth.

Primary promotion criterion:
- a new SGQF route must evaluate the declared KSC surrogate target explicitly
  and admit a value/gradient test against Kalman mixture enumeration.

Veto diagnostics:
- additive-Gaussian observation closure standing in for finite-mixture
  likelihood,
- branch-instability that invalidates score comparisons,
- missing deterministic coverage or missing nonclaim updates.

Explanatory-only diagnostics:
- runtime, cloud size, and agreement with CUT4/Zhao-Cui are explanatory unless
  Kalman-enumeration comparison exists.

What will not be concluded even if the route works:
- no claim about actual transformed non-Gaussian SV,
- no HMC readiness claim,
- no production-readiness claim,
- no source-faithful Zhao-Cui equivalence claim.

## Expected files if implementation is approved

Likely design/implementation surfaces:
- `bayesfilter/highdim/sv_mixture_cut4.py`
- possibly a new highdim SGQF surrogate module or helper
- `bayesfilter/nonlinear/fixed_sgqf_tf.py`
- `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- potentially a new sibling SGQF surrogate SV test file
- deterministic coverage / smoke payload artifacts if a new algorithm row is
  admitted

## Immediate next step

Before coding, produce a concrete implementation design choosing between:
- mixture-collapsed SGQF observation evaluation,
- per-component SGQF collapse,
- or explicit non-implementation / continued block.
