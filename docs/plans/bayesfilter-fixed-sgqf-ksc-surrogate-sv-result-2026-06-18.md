# KSC-Surrogate Fixed-SGQF Result Note

metadata_date: 2026-06-18
program_id: fixed-sgqf-ksc-surrogate-sv
status: PARTIAL_PASS_SAME_TARGET_SGQF_ROUTE_VALUE_ONLY
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

This note is intentionally corrected to **value-only** status.

Reason:
- the outer KSC surrogate wrapper does **not** currently use the repo’s analytic
  Fixed-SGQF score contract in `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`.
- prior wrapper-gradient evidence relied on TensorFlow autodiff through the
  wrapper value path.
- per user policy, autodiff is acceptable only as a **test oracle to validate an
  already-implemented analytical gradient**; it is not admissible as SGQF score
  evidence by itself.

Therefore the KSC surrogate Fixed-SGQF wrapper is admitted only as a same-target
surrogate **value** route until a true analytic outer mixture score contract is
implemented.

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
- no outer analytic score admission,
- no wrapper gradient-valid claim,
- no actual transformed non-Gaussian SV claim,
- no HMC readiness claim,
- no production-readiness claim.

## Implementation summary

### New route admitted
- `highdim.independent_panel_sv_mixture_fixed_sgqf_filter(...)`
  in `bayesfilter/highdim/sv_mixture_cut4.py`

### Main implementation shape
- per-mixture-component Gaussian closure
- Fixed-SGQF kernel evaluation via `tf_fixed_sgqf_filter(...)`
- posterior Gaussian-component collapse via `_collapse_gaussian_components(...)`
- **no admitted outer analytic score path yet**

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
- p43 keeps the distinction between surrogate-row evidence and actual exact
  transformed SV evidence
- deterministic coverage and smoke artifacts now include a `fixed_sgqf`
  surrogate-row algorithm entry as **value-only**

### Demoted evidence
- the previously written wrapper-gradient claims are withdrawn
- the outer KSC surrogate wrapper is **not** an analytic-score-admitted
  Fixed-SGQF route
- no benchmark artifact should treat this row as gradient-valid for `fixed_sgqf`

## Decision table

| decision | primary criterion | veto diagnostics | main uncertainty | next justified action | not concluded |
|---|---|---|---|---|---|
| Admit same-target KSC-surrogate Fixed-SGQF route for value only | Passed focused dim 1/2/3 value checks vs Kalman surrogate oracle | No component-lane failure seen; autodiff-based gradient admission vetoed and removed | Outer analytic mixture score is still missing | Keep value route; create a separate plan if analytic outer score is needed | No wrapper gradient, actual-SV, HMC, or production claim |

## Interpretation

The repo now has a real same-target Fixed-SGQF **value** route for the KSC
surrogate SV row, but not a score-admitted one.

That means:
- the route is a surrogate-target wrapper around per-component Gaussian closures,
- it is benchmark-admitted only for declared surrogate-row value evidence,
- and it must not be cited as analytic Fixed-SGQF gradient evidence until a true
  analytic outer mixture score path is implemented.

## Red-team note

Weakest part of the current implementation boundary:
- the wrapper reuses an analytic inner SGQF kernel but has no aggregate analytic
  outer score contract or same-branch wrapper identity.
- autodiff could be used later as a **validation tool** for such an analytical
  outer score once implemented, but it does not supply the missing contract.

What would overturn even the current value-only conclusion:
- branch instability or value disagreement vs Kalman enumeration on broader
  surrogate fixtures.

## Next steps

1. Keep the route as value-only in all benchmark/governance artifacts.
2. If analytic score evidence is required, write a separate plan for:
   - outer mixture score derivation,
   - aggregate branch identity / replay semantics,
   - analytic admission criteria.
3. Keep actual transformed non-Gaussian SV as a separate evidence problem.
