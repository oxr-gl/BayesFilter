# Phase Result: Fixed-SGQF Leaderboard Promotion P1 Admission Ledger

metadata_date: 2026-06-23
plan_reference: `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p1-admission-ledger-subplan-2026-06-23.md`
master_program: `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-master-program-2026-06-23.md`
status: PASS_P1_FIXED_SGQF_ADMISSION_LEDGER_WRITTEN

## Phase Objective

Assign every intended fixed-SGQF × target-family cell an explicit admission
class, scalar meaning, reference policy, comparator-eligibility status, and
blocker reason when not admitted, so that later matrix integration phases cannot
create silent holes or informal scope drift.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | answered for the current promotion scope: every intended SGQF family cell is now classified explicitly without changing target semantics or overclaiming score readiness |
| Primary criterion status | satisfied |
| Veto diagnostic status | no intended family cell was omitted; no blocked family was silently admitted; no family was given analytical-score admission without explicit analytical derivative support |
| Main uncertainty | the KSC-surrogate family still needs wrapper analytical-score completion and several literature-backed families remain blocked under current additive-state SGQF semantics |
| Next justified action | execute P2 kernel-gap classification/closure while preserving the P1 value/score admission boundaries |
| What is not concluded | no machine-readable matrix integration yet, no new SGQF kernel evidence yet, no KSC analytical-wrapper-score completion yet, no universal family readiness claim |

## Loaded Classification Context

The following artifacts were loaded and used to build the P1 admission ledger:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json`
- `docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-closeout-result-2026-06-16.md`
- `docs/plans/bayesfilter-fixed-sgqf-broader-nonlinear-comparison-closeout-result-2026-06-16.md`
- `docs/plans/bayesfilter-fixed-sgqf-structural-adapter-result-2026-06-16.md`
- `docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-analytic-score-plan-2026-06-18.md`

## Frozen Variant And Scope Reminder

This ledger preserves the P0 freeze that the first intended fixed-SGQF
leaderboard variant is:

- `fixed_sgqf_level_2`

The final literature-facing scope remains the six source-paper rows named in the
source-paper scope contract.  Narrow-harness Model A/B/C rows remain important
engineering/bridge evidence, but they do not replace the literature-backed final
scope.

## Run Manifest

| Field | Value |
| --- | --- |
| git commit | `N/A` |
| command actually run | `Focused planning/classification checks only; no SGQF numerical execution in P1.` |
| environment / conda env | `N/A` |
| CPU/GPU status | `N/A; no numerical execution performed` |
| seed(s) | `N/A` |
| wall time | `N/A` |
| output artifact paths | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p1-admission-ledger-result-2026-06-23.md`, `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p2-kernel-gap-closure-subplan-2026-06-23.md` |
| plan file | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p1-admission-ledger-subplan-2026-06-23.md` |
| result file | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p1-admission-ledger-result-2026-06-23.md` |

## Admission Ledger

### A. Literature-backed final-scope families

| Family / row id | Scope role | Value admission class | Analytical-score status | Scalar meaning / reference policy | Comparator eligibility | Blocker or note |
| --- | --- | --- | --- | --- | --- | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | final literature-backed scope | `admit_exact` | `diagnostic_only` | log marginal likelihood under the fixed observations/theta with exact Kalman oracle reference | same-target exact-row comparison is eligible under the benchmark backbone | value support is already strong; score remains outside admitted leaderboard cells until P3 certifies the analytical score route in benchmark terms |
| `zhao_cui_sv_actual_nongaussian_T1000` | final literature-backed scope | `blocked_not_same_target` | `blocked_not_same_target` | transformed actual non-Gaussian SV target under source-paper scope | not comparator-eligible for current additive-state SGQF lane | current fixed-SGQF lane is not yet an admitted same-target route for this family |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | final literature-backed scope | `admit_value_baseline_only` | `blocked_missing_analytical_wrapper_score` | KSC Gaussian-mixture surrogate value target; same-target value route exists in `sv_mixture_cut4.py` and uses the declared surrogate semantics | same-target value comparison is intended to be eligible once matrix/benchmark phases integrate it | current broader closeout still treated this row as diagnostic/adapter-required; the current program refines that status by recognizing the existing value route while keeping score blocked until P4 completes the analytical outer wrapper score |
| `zhao_cui_spatial_sir_austria_j9_T20` | final literature-backed scope | `blocked_not_same_target` | `blocked_not_same_target` | source-route/scaling-ladder SIR target under source-paper scope | not comparator-eligible for current additive-state SGQF lane | current SGQF route is not an admitted same-target source-route/scaling lane |
| `zhao_cui_predator_prey_T20` | final literature-backed scope | `blocked_not_same_target` | `blocked_not_same_target` | predator-prey production target under source-paper scope | not comparator-eligible for current additive-state SGQF lane | no current same-target SGQF production route is defined for this family |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | final literature-backed scope | `blocked_not_same_target` | `blocked_not_same_target` | generalized SV synthetic target under source-paper scope | not comparator-eligible for current additive-state SGQF lane | current fixed-SGQF lane does not yet provide the admitted same-target route for this family |

### B. Narrow-harness bridge rows retained as engineering evidence

| Family / row class | Scope role | Value admission class | Analytical-score status | Scalar meaning / reference policy | Comparator eligibility | Blocker or note |
| --- | --- | --- | --- | --- | --- | --- |
| narrow-harness Model A affine oracle | local bridge evidence | `admit_exact` | `diagnostic_only` | exact-reference nonlinear harness row using Kalman oracle semantics | eligible within the existing nonlinear benchmark harness | already integrated and benchmarked in the narrow harness; score still remains outside admitted leaderboard score cells |
| narrow-harness Model B nonlinear accumulation | local bridge evidence | `blocked_not_same_target` | `blocked_not_same_target` | structural nonlinear benchmark row with deterministic block completion | not comparator-eligible for current additive-state SGQF lane | innovation enters the deterministic block through nonlinear completion, so the current lane is not exact same-target |
| narrow-harness Model C autonomous nonlinear growth | local bridge evidence | `admit_exact` | `diagnostic_only` | exact-gated structural-adapter row with semidefinite-capable state handling | eligible within the narrow benchmark harness only | admitted as an exact-gated extension, but this does not itself create broader literature-family admission |

### C. Explicitly excluded or engineering-only row classes

| Row class | Scope role | Value admission class | Analytical-score status | Note |
| --- | --- | --- | --- | --- |
| P44 debugging rows | excluded from final literature-facing scope | `diagnostic_only` | `diagnostic_only` | retained as engineering/debugging evidence only; not part of final literature-backed leaderboard scope |
| high-dimensional smoke rows incompatible with current additive-state lane | engineering smoke scope | `diagnostic_only` | `blocked_not_same_target` | preserve explicit skip/blocked visibility rather than silent omission |
| DPF / range-bearing external comparison streams | outside final deterministic SGQF scope | `historical_only` | `historical_only` | outside the intended fixed-SGQF leaderboard-family set for this program |

## Admission-Count Summary

### Literature-backed final-scope family counts
- value-admitted now or intentionally promotable under current same-target scope:
  - `2`
  - `benchmark_lgssm_exact_oracle_m3_T50`
  - `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`
- value-blocked under current additive-state lane semantics:
  - `4`
- analytical-score-admitted now:
  - `0`
- analytical-score blocked or diagnostic-only pending later phases:
  - `6`

### Narrow-harness bridge counts
- exact-admitted bridge rows:
  - `2`
  - Model A
  - Model C
- blocked bridge rows:
  - `1`
  - Model B

## Interpretation

### What is now fixed by the ledger
1. No intended SGQF family cell is left implicit.
2. Value and analytical-score statuses are now separated explicitly.
3. The KSC-surrogate family is recorded as the main literature-backed split case:
   same-target value route present, analytical wrapper score still missing.
4. The blocked literature-backed families remain visible rather than being pushed
   out of scope silently.

### What remains deliberately unresolved
1. P1 does not certify any SGQF analytical-score family cell yet.
2. P1 does not update any machine-readable registry or matrix artifact.
3. P1 does not reopen blocked families by reinterpretation.
4. P1 does not treat narrow-harness Model C admission as a blanket argument for
   broader nonlinear-family admission.

## Engineering Observations

- The current SGQF promotion bottleneck is not “missing any admission ledger at
  all”; it is the mixture of three different statuses across families:
  exact-admitted, value-route-present-but-score-missing, and structurally
  blocked.
- The KSC-surrogate row is the key bridge family because it already has a
  same-target value route and an explicit analytical-wrapper-score plan.
- The literature-backed blocked families should stay blocked until a richer SGQF
  lane exists rather than being forced into convenience comparisons.

## Nonclaims

- No machine-readable benchmark registry, deterministic coverage, preflight, or
  numeric artifact was updated in P1.
- No SGQF family received analytical-score admission in P1.
- No new SGQF kernel numerical evidence was generated in P1.
- No universal repo-wide SGQF family readiness claim is made here.
- No claim is made that autodiff-backed wrapper evidence is interchangeable with
  analytical gradient support.

## Post-Run Red-Team Note

- Strongest alternative explanation:
  - The ledger could still be too optimistic about the KSC-surrogate value row if
    the existing wrapper route turns out not to be admissible under the exact
    benchmark scalar semantics used later in matrix integration.
- What result would overturn the current P1 conclusion:
  - Evidence in a later phase that the KSC value route is not same-target after
    all, or that one of the currently blocked literature-backed families already
    has an admissible SGQF route under current semantics.
- Weakest part of the evidence:
  - P1 is a governance/classification phase built from existing artifacts rather
    than a new numerical execution phase, so its correctness depends on faithful
    interpretation of prior closeouts and route semantics.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| pass P1 and freeze the SGQF admission ledger | satisfied | no family omitted; no blocked family silently admitted; no score cell overclaimed | whether the current kernel evidence closes enough of G1-G8 and whether P4 can complete the KSC wrapper score cleanly | execute P2 kernel-gap classification/closure, then P3/P4 score-gating phases under this frozen ledger | no matrix integration or leaderboard performance claim from P1 alone |

## Exact Next-Phase Handoff

P2 may begin only after:
- the P2 kernel-gap subplan exists and respects the P1 value/score admission
  boundaries;
- the visible execution ledger and stop handoff are updated for the P1 pass;
- the bounded P1 review packet is issued on the exact files named in the review
  ledger;
- any review findings are patched visibly and the focused P1 checks rerun;
- no machine-readable registry, coverage, preflight, or numeric leaderboard work
  is started from the P1 handoff alone;
- no family-level analytical-score promotion is inferred from P1 classification
  alone.

## Stop-Condition Outcome

No P1 stop condition triggered during classification drafting.  The KSC row was
kept score-blocked rather than overpromoted, and the blocked literature-backed
families remained explicit.
