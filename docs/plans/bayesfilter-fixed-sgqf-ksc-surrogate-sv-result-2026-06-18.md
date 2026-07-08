# KSC-Surrogate Fixed-SGQF Result Note

metadata_date: 2026-06-18
program_id: fixed-sgqf-ksc-surrogate-sv
status: PARTIAL_PASS_SAME_TARGET_SGQF_ROUTE_VALUE_AND_ANALYTICAL_SCORE
plan_file: docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-sv-route-gap-plan-2026-06-18.md

## Question

Can BayesFilter now support a **same-target Fixed-SGQF** route on
the declared KSC Gaussian-mixture surrogate stochastic-volatility row without
silently changing the target?

## Skeptical audit outcome

Pass, with explicit scope limits.

The implementation avoided the previously blocked mistake of pretending the
existing additive-Gaussian Fixed-SGQF core already matched the KSC surrogate
likelihood. Instead, the admitted route is a new **highdim wrapper** that:
- enumerates KSC mixture component tuples,
- runs Fixed-SGQF on each Gaussian component closure,
- collapses the posterior components with the same Gaussian-mixture collapse
  logic already used by the Kalman and CUT4 surrogate routes.

This preserves the declared surrogate target more faithfully than a
single-Gaussian moment-matched shortcut would have.

### 2026-06-18 analytic-gradient correction

This note is intentionally corrected from the earlier autodiff-backed wrapper
claim, but it is **no longer value-only**.

Reason:
- the outer KSC surrogate wrapper now uses the repo’s explicit analytical
  Fixed-SGQF score contract in `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`
  through `highdim.independent_panel_sv_mixture_fixed_sgqf_score(...)`.
- same-target UKF analytical wrapper-score support also exists via
  `highdim.independent_panel_sv_mixture_ukf_score(...)`.
- wrapper score evidence is validated against centered finite differences on the
  declared tiny KSC-surrogate fixture.
- autodiff remains acceptable only as a **diagnostic oracle to validate an
  already-implemented analytical gradient**; it is not admissible as SGQF score
  evidence by itself.

Therefore the KSC surrogate Fixed-SGQF wrapper is admitted as a same-target
surrogate **value + analytical-score** route on the declared tiny fixture,
subject to the existing nonclaims and same-target scope limits.

## Evidence contract

Baseline / truth anchor:
- `ksc_sv_gaussian_mixture_kalman_enumeration`

Primary promotion criterion:
- same-target Fixed-SGQF route exists,
- returns finite surrogate-row value,
- agrees with Kalman mixture enumeration on the tiny dim 1/2/3 fixture within
  declared surrogate-row tolerances.

Veto diagnostics:
- target mismatch with actual transformed non-Gaussian SV,
- component-lane SGQF failure,
- governance artifacts inconsistent with the admitted surrogate-only scope,
- any attempt to treat wrapper autodiff as analytic SGQF score evidence.

Explanatory-only diagnostics:
- direct SGQF vs CUT4 value agreement,
- sparse-level details of the admitted route,
- smoke-payload representation values.

What is not concluded:
- no actual transformed non-Gaussian SV claim,
- no HMC readiness claim,
- no production-readiness claim.

## Implementation summary

### New route admitted
- `highdim.independent_panel_sv_mixture_fixed_sgqf_filter(...)`
- `highdim.independent_panel_sv_mixture_fixed_sgqf_score(...)`
  in `bayesfilter/highdim/sv_mixture_cut4.py`

### Main implementation shape
- per-mixture-component Gaussian closure
- Fixed-SGQF kernel evaluation via `tf_fixed_sgqf_filter(...)`
- analytical Fixed-SGQF wrapper score via `tf_fixed_sgqf_score(...)` plus
  outer mixture log-sum-exp aggregation
- posterior Gaussian-component collapse via `_collapse_gaussian_components(...)`

### Export update
- public highdim export added in `bayesfilter/highdim/__init__.py`

## Verification run manifest

- git branch: `fix/fixed-sgqf-merge-audit`
- environment: `tf-gpu` conda env
- CPU/GPU status: CPU-only by explicit `CUDA_VISIBLE_DEVICES=-1`
- plan file: `docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-sv-route-gap-plan-2026-06-18.md`
- result file: `docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-sv-result-2026-06-18.md`
- random seeds: deterministic fixture / no stochastic benchmark run
- data version: fixed tiny in-repo fixture observations

## Results

### Admitted evidence
- same-target SGQF-vs-Kalman **value** checks now exist for dims 1, 2, 3
- same-target SGQF-vs-CUT4 **value** bounded-gap checks now exist
- same-target SGQF analytical wrapper-score checks now exist and are validated
  against centered finite differences on the declared tiny fixture
- same-target UKF analytical wrapper-score checks now exist and are validated
  against centered finite differences on the same fixture
- p43 keeps the distinction between surrogate-row evidence and actual exact
  transformed SV evidence
- deterministic coverage and smoke artifacts now include a `fixed_sgqf`
  surrogate-row algorithm entry; later benchmark-governance artifacts must treat
  it as analytical-score-admissible only where this same-target surrogate scope
  is preserved

### Demoted evidence
- the previously written wrapper-gradient claims are withdrawn only insofar as
  they relied on autodiff rather than the explicit analytical wrapper route
- no benchmark artifact should treat this row as actual transformed non-Gaussian
  SV evidence

## Decision table

| decision | primary criterion | veto diagnostics | main uncertainty | next justified action | not concluded |
|---|---|---|---|---|---|
| Admit same-target KSC-surrogate Fixed-SGQF route for value + analytical score on the declared tiny surrogate fixture | Passed focused dim 1/2/3 value checks vs Kalman surrogate oracle and wrapper-score FD checks on the declared tiny fixture | No component-lane failure seen; autodiff-based gradient admission remains vetoed as a promotion route | Whether broader surrogate fixtures or later benchmark-governance artifacts preserve the same score contract cleanly | Keep the route analytical-score-admitted only within the declared same-target surrogate scope and update later benchmark-governance artifacts accordingly | No actual-SV, HMC, or production claim |

## Interpretation

The repo now has a real same-target Fixed-SGQF **value + analytical-score**
route for the KSC surrogate SV row on the declared tiny fixture.

That means:
- the route is a surrogate-target wrapper around per-component Gaussian closures,
- it is benchmark-admitted only for declared surrogate-row evidence under the
  same-target tiny-fixture scope,
- and autodiff may remain only as a validation tool, not as the promoted SGQF
  score route.

## Red-team note

Weakest part of the current implementation boundary:
- the wrapper now has an analytical outer score contract, but its promotion is
  still only justified on the declared tiny same-target surrogate fixture until
  broader governance artifacts are refreshed.
- autodiff could still be used later as a **validation tool** for this analytical
  outer score, but it does not define the promoted route.

What would overturn even the current value-only conclusion:
- branch instability or value disagreement vs Kalman enumeration on broader
  surrogate fixtures.

## Next steps

1. Keep the route analytical-score-admitted only within the declared tiny
   same-target surrogate fixture scope until later matrix/benchmark artifacts are
   refreshed.
2. Update downstream benchmark/governance artifacts so they no longer describe
   this row as SGQF value-only where the analytical wrapper-score evidence now
   applies.
3. Keep actual transformed non-Gaussian SV as a separate evidence problem.
