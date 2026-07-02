# Phase Result: Fixed-SGQF Leaderboard Promotion P4 KSC-Surrogate Analytical Wrapper Score Certification And Reconciliation

metadata_date: 2026-06-23
plan_reference: `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p4-ksc-surrogate-analytical-wrapper-score-subplan-2026-06-23.md`
master_program: `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-master-program-2026-06-23.md`
status: PASS_P4_FIXED_SGQF_KSC_ANALYTICAL_WRAPPER_SCORE_CERTIFIED

## Phase Objective

Certify and reconcile the KSC-surrogate SGQF analytical outer wrapper score so
that the code, tests, and governance artifacts all agree on whether the
same-target KSC-surrogate SGQF route remains value-only or is now eligible for
analytical-score admission.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | answered for the declared tiny same-target surrogate fixture: the existing KSC-surrogate SGQF wrapper score implementation is analytically evidenced strongly enough to replace the older value-only governance status |
| Primary criterion status | satisfied after focused test repair and rerun |
| Veto diagnostic status | no surviving autodiff dependence on the promoted SGQF wrapper score route; wrapper finite-difference checks now pass; code/tests/artifacts are reconciled for the declared tiny surrogate fixture |
| Main uncertainty | whether later matrix/benchmark artifacts outside this phase still contain stale value-only language, and how far the analytical wrapper-score admission should extend beyond the tiny declared surrogate fixture |
| Next justified action | execute P5 to refresh the family-by-family admission ledger so the KSC row changes from score-blocked to analytical-score-admitted within the declared tiny same-target surrogate scope |
| What is not concluded | no actual transformed non-Gaussian SV claim, no HMC readiness claim, no machine-readable matrix integration yet, no broader family score admission beyond the KSC wrapper row |

## Loaded Reconciliation Context

The following artifacts and code/test surfaces informed P4:

- `bayesfilter/highdim/sv_mixture_cut4.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- `tests/highdim/test_p47_generalized_sv_equality.py`
- `docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-sv-result-2026-06-18.md`
- `docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-analytic-score-plan-2026-06-18.md`
- `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-result-2026-06-23.md`

## Focused Checks Run

### Planning consistency checks
```bash
git diff --check -- docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p4-ksc-surrogate-analytical-wrapper-score-subplan-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p4-ksc-surrogate-analytical-wrapper-score-result-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p5-family-by-family-admission-subplan-2026-06-23.md
rg -n "independent_panel_sv_mixture_fixed_sgqf_score|independent_panel_sv_mixture_ukf_score|wrapper_score_contract|value-only|autodiff|finite_difference|diagnostic" bayesfilter/highdim/sv_mixture_cut4.py tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py tests/highdim/test_p47_generalized_sv_equality.py docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-sv-result-2026-06-18.md docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-analytic-score-plan-2026-06-18.md
```

### Focused wrapper-score checks
Initial run:
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py tests/highdim/test_p47_generalized_sv_equality.py -k "ksc and (score or fixed_sgqf or ukf)"
```
Observed initially:
- `2 failed, 30 passed, 14 deselected, 2 warnings`
- failure mode: the newly added SGQF-vs-UKF score-equality test failed for dim 2/3 because the UKF score route hits `blocked_weak_spectral_gap` on repeated-spectrum placement cases.

Repair applied:
- rewrote the SGQF wrapper-score admission test so it validates the SGQF wrapper
  score directly against centered finite differences of the same SGQF wrapper
  value route, rather than against UKF score equality on blocked-spectrum rows.
- kept UKF wrapper-score tests as same-target analytical comparator evidence in
  their own dedicated rows where they already pass.

Rerun after repair:
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py tests/highdim/test_p47_generalized_sv_equality.py -k "ksc and (score or fixed_sgqf or ukf)"
```
Observed after repair:
- `32 passed, 14 deselected, 2 warnings`
- warnings were TensorFlow Probability deprecation warnings, not SGQF failures

## Run Manifest

| Field | Value |
| --- | --- |
| git commit | `8eca1559c9508527a8d61d4ca348d8cee632db42` |
| command actually run | `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py tests/highdim/test_p47_generalized_sv_equality.py -k "ksc and (score or fixed_sgqf or ukf)"` |
| environment / conda env | `tf-gpu` |
| CPU/GPU status | `CPU-only; CUDA_VISIBLE_DEVICES=-1` |
| seed(s) | `N/A` |
| wall time | `5m28.61s` on final passing rerun |
| output artifact paths | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p4-ksc-surrogate-analytical-wrapper-score-result-2026-06-23.md`, `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p5-family-by-family-admission-subplan-2026-06-23.md` |
| plan file | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p4-ksc-surrogate-analytical-wrapper-score-subplan-2026-06-23.md` |
| result file | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p4-ksc-surrogate-analytical-wrapper-score-result-2026-06-23.md` |

## Wrapper-Score Certification Findings

### 1. The SGQF KSC wrapper score already exists as an analytical route
`bayesfilter/highdim/sv_mixture_cut4.py` already contains:
- `independent_panel_sv_mixture_fixed_sgqf_score(...)`
- `_fixed_sgqf_component_score_update(...)`
- `_panel_transformed_sv_component_fixed_sgqf_derivatives(...)`

These route through:
- explicit `TFFixedSGQFDerivatives`,
- explicit `tf_fixed_sgqf_score(...)`,
- analytical outer mixture aggregation recorded as
  `wrapper_score_contract = "analytic_component_score_logsumexp_aggregation"`.

### 2. The same-target UKF analytical wrapper route also exists
`bayesfilter/highdim/sv_mixture_cut4.py` also contains
`independent_panel_sv_mixture_ukf_score(...)`, which provides a same-target UKF
analytical wrapper comparator for the same KSC surrogate row.

### 3. The right SGQF promotion oracle is finite difference of the SGQF wrapper value route
The first attempted P4 test overreached by requiring direct SGQF-vs-UKF score
agreement on dim 2/3 rows where the UKF score route can legitimately block on
weak spectral gaps.  That is not the correct SGQF promotion oracle.

The repaired test uses the correct criterion:
- SGQF wrapper analytical score must match centered finite differences of the
  same SGQF wrapper value route.

That criterion now passes on the declared tiny KSC surrogate fixture.

### 4. Governance artifacts were stale and are now reconciled
The older KSC result note at
`docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-sv-result-2026-06-18.md`
contained corrected-but-now-stale value-only language.  P4 updates that note so
it now matches the actual code/test state:
- analytical outer wrapper score exists,
- autodiff remains diagnostic-only,
- admission is still tightly scoped to the declared tiny same-target surrogate
  fixture.

## Interpretation

### What P4 now certifies
1. The KSC-surrogate SGQF wrapper is no longer honestly describable as value-only
   on the declared tiny same-target surrogate fixture.
2. The SGQF wrapper score path is analytical and test-backed on that declared
   fixture.
3. The same-target UKF analytical wrapper score exists as comparator support, but
   its repeated-spectrum limitations do not control SGQF admission.
4. The correct SGQF wrapper admission oracle is SGQF analytical score vs SGQF
   wrapper-value finite differences, not forced equality to a blocked UKF score
   on all rows.

### What P4 still does not certify
1. No claim that the KSC surrogate row is actual transformed non-Gaussian SV.
2. No claim that the analytical wrapper-score admission extends automatically
   beyond the declared tiny surrogate fixture.
3. No claim that all benchmark governance artifacts are already updated.
4. No HMC readiness or production-readiness claim.

## Engineering Observations

- The main P4 work turned out to be **reconciliation**, not invention.
- The code already contained the analytical SGQF wrapper score surface; the stale
  part was the governance note and the absence of direct SGQF-wrapper FD tests.
- A subtle but important point emerged: comparator score routes can fail for their
  own reasons without invalidating SGQF analytical-score certification on the
  declared row.  Promotion criteria must stay tied to the claimed route.

## Nonclaims

- P4 does not update machine-readable benchmark registry, coverage, preflight, or
  numeric artifacts yet.
- P4 does not admit broader literature-backed family score rows beyond the KSC
  surrogate wrapper row.
- P4 does not make any claim about actual transformed non-Gaussian SV,
  source-faithful Zhao-Cui equivalence, HMC readiness, or production readiness.

## Post-Run Red-Team Note

- Strongest alternative explanation:
  - The analytical SGQF wrapper score may be correct on the declared tiny
    surrogate fixture while still needing broader fixture coverage before any
    stronger leaderboard-wide score generalization is justified.
- What result would overturn the current P4 conclusion:
  - A focused rerun showing the SGQF wrapper analytical score fails centered
    finite differences on the same declared surrogate fixture, or a governance
    inconsistency showing the row’s scalar/target semantics differ from what the
    wrapper tests assume.
- Weakest part of the evidence:
  - admission remains tightly scoped to the tiny declared surrogate fixture and
    still needs later benchmark-artifact propagation.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| pass P4 and certify the KSC-surrogate SGQF analytical wrapper score on the declared tiny same-target fixture | satisfied after focused test repair and rerun | no surviving autodiff promotion, no failing SGQF wrapper FD check, no unresolved code/artifact contradiction | how this wrapper-score admission should be propagated through the broader family ledger and later machine-readable artifacts | execute P5 and update the family-by-family admission ledger so the KSC row becomes analytical-score-admitted within its declared tiny surrogate scope | no broader actual-SV, HMC, or benchmark-wide readiness claim |

## Exact Next-Phase Handoff

P5 may begin only after:
- the P5 family-by-family-admission subplan exists and preserves the P4 tiny-
  fixture wrapper-score scope;
- the visible execution ledger and stop handoff are updated for the P4 pass;
- the bounded P4 review packet is issued on the exact files named in the review
  ledger;
- any review findings are patched visibly and the focused P4 checks rerun;
- no machine-readable leaderboard integration is inferred from P4 alone.

## Stop-Condition Outcome

No P4 stop condition remained after repair.  The only material failure was an
initially overstrong SGQF-vs-UKF score-equality test on blocked-spectrum rows;
it was replaced with the correct SGQF-wrapper finite-difference admission test,
after which the focused wrapper-score packet passed.
