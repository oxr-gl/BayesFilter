# Fixed-SGQF KSC Surrogate SV Plan

metadata_date: 2026-06-17
program_id: fixed-sgqf-ksc-surrogate-sv
status: BLOCKED_ON_SAME_TARGET_SGQF_ROUTE_GAP

## Purpose

This plan governs the next family-level fixed-SGQF benchmark program after
predator-prey: the KSC Gaussian-mixture surrogate stochastic-volatility row.

The goal is to add value and gradient comparison rows for:
- fixed SGQF,
- UKF,
- Zhao-Cui where same-target surrogate semantics are truly available,
- and the best same-target reference: Kalman mixture enumeration.

This pass should also include an SGQF tuning report for the surrogate target.

## Governing references

- `tests/highdim/test_p40_sv_kalman_cut4_zhaocui.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_reference_oracles.py`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json`

## Target identity

This family is the **KSC Gaussian-mixture surrogate** SV target only.
It is not the same as the actual transformed non-Gaussian SV target.

## Primary comparator policy

### Same-target reference
- Kalman mixture enumeration
- current oracle id in repo policy:
  - `ksc_sv_gaussian_mixture_kalman_enumeration`

### Comparator rows to implement
- SGQF vs Kalman mixture enumeration
- UKF vs Kalman mixture enumeration
- CUT4 vs Kalman mixture enumeration
- Zhao-Cui only if the route is explicitly implemented on the same surrogate
  target; otherwise keep it blocked or diagnostic.

### Nonclaims
- no claim that surrogate-target success implies actual transformed SV success
- no HMC readiness claim
- no production-ready claim
- no source-faithful adaptive TT/SIRT claim
- no universal ranking claim

## SGQF tuning ladder

Primary SGQF budget axis:
- `sparse_level`

Hold fixed:
- branch tolerances
- merge tolerances
- observations
- theta
- surrogate target definition

Suggested ladder:
- level 1
- level 2
- level 3
- level 4 where tractable

For each rung report:
- point count
- value gap vs Kalman mixture enumeration
- gradient gap vs Kalman mixture enumeration
- directional residuals
- branch/failure status

## Skeptical plan audit

Status target: `PASS_TO_KSC_SURROGATE_SV_IMPLEMENTATION`

Main risks:
1. accidentally blurring actual transformed SV with the KSC surrogate target
2. treating Zhao-Cui as same-target if the surrogate route is not truly wired
3. promoting SGQF tuning observations into a general theorem
4. treating SGQF-vs-UKF agreement as truth without the Kalman mixture anchor

### 2026-06-18 restart audit update

Audit result: **FAIL / BLOCK before execution**.

Material flaw found:
- the plan assumes an already-existing same-target fixed-SGQF route for the KSC
  Gaussian-mixture surrogate target, but the current repo surfaces inspected in
  `bayesfilter/highdim/sv_mixture_cut4.py`, `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`,
  `tests/highdim/test_p47_generalized_sv_equality.py`, and the deterministic
  filter coverage artifacts expose same-target surrogate routes only for:
  - Kalman mixture enumeration,
  - CUT4,
  - and Zhao-Cui fixed-design TT.
- no existing fixed-SGQF algorithm row or same-target KSC surrogate adapter was
  found in the benchmark coverage artifacts or highdim entry points.
- the current fixed-SGQF implementation is additive-Gaussian, requiring
  `observation_covariance` and `observation_fn` moment closure, not a declared
  finite-mixture likelihood or per-mixture-component collapse route.

Why this blocks the current execution order:
- execution step 2 says to "Add SGQF same-target surrogate value/gradient tests"
  but there is presently no same-target SGQF route to test.
- executing that step as written would force an unreviewed invention or a silent
  target mismatch, violating the skeptical-audit and evidence-contract policy.

Disposition:
- keep the existing CUT4/Kalman and Zhao-Cui same-target surrogate evidence as
  the current admitted evidence for this row.
- block SGQF on a follow-up implementation plan that explicitly designs a KSC
  surrogate fixed-SGQF adapter/value/score route before any benchmark claim.

## Evidence contract

Question:

On the declared KSC Gaussian-mixture surrogate SV target, how do SGQF, UKF,
CUT4, and (if same-target available) Zhao-Cui compare against Kalman mixture
enumeration for both value and gradient, and how does the SGQF budget ladder
behave?

### Primary promotion conditions
- same target is explicit
- same observations and parameterization are explicit
- Kalman mixture enumeration remains the truth anchor
- SGQF tuning ladder is predeclared
- no tolerance changes after seeing results

### Veto / block conditions
- target mismatch is hidden
- Zhao-Cui surrogate-target availability is assumed rather than verified
- SGQF tuning ladder is used to overclaim beyond the row

### 2026-06-18 restart evidence-contract update

Scientific / engineering question now permitted under this artifact:
- confirm what same-target surrogate evidence already exists for the KSC row,
  and record whether fixed-SGQF is currently benchmarkable on that exact target.

Exact baseline / comparator:
- Kalman mixture enumeration remains the only truth anchor for the declared KSC
  surrogate target.

Primary pass/fail criterion:
- PASS only if a real same-target fixed-SGQF KSC surrogate route exists and can
  be named with explicit implementation entry points.
- Otherwise BLOCK the SGQF row and do not fabricate comparison tests.

Veto diagnostics:
- any route whose likelihood remains additive-Gaussian rather than finite
  mixture-conditioned or mixture-collapsed on the KSC surrogate target vetoes
  "same-target SGQF available".
- absence of a deterministic-coverage algorithm row for SGQF on
  `sv_ksc_gaussian_mixture_surrogate_dim_1_2_3` vetoes benchmark execution under
  this plan.

Explanatory-only diagnostics:
- CUT4/Kalman and Zhao-Cui/dense same-target tests are explanatory evidence
  about the surrogate row and do not establish SGQF availability.

What will not be concluded:
- no SGQF-vs-Kalman value/gradient result for this row,
- no SGQF sparse-level tuning conclusion for this row,
- no claim that SGQF is same-target-ready on KSC surrogate SV without a new
  reviewed implementation path.

Artifact preserving the result:
- this plan file should record the block, and the next step should be a narrow
  follow-up plan for a KSC-surrogate fixed-SGQF adapter/value/score route.

## Files to modify

Primary likely files:
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- potentially a new sibling test file dedicated to SGQF surrogate SV rows
- `tests/highdim/test_filtering_value_gradient_benchmark_reference_oracles.py`
- if needed, `docs/plans/...reference-oracles...json` or related scope artifacts

## Execution order

1. Write this plan artifact.
2. Add SGQF same-target surrogate value/gradient tests against Kalman mixture enumeration.
3. Add UKF same-target surrogate value/gradient tests if not already explicit enough.
4. Verify whether Zhao-Cui on the same surrogate target exists; block if not.
5. Add SGQF tuning ladder tests on this surrogate target.
6. Run focused SV family tests.
7. Write the result artifact.
