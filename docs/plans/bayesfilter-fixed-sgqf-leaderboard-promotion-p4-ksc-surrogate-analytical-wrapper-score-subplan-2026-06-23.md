# Phase P4 Subplan: KSC-Surrogate Analytical Wrapper Score Certification And Reconciliation

metadata_date: 2026-06-23
status: DRAFT_PENDING_P3_HANDOFF_AND_LOCAL_CHECKS
master_program: docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-master-program-2026-06-23.md
phase: P4
executor: Claude Code
reviewer: read-only bounded reviewer only

## Phase Objective

Certify and reconcile the KSC-surrogate SGQF analytical outer wrapper score so
that the code, tests, and governance artifacts all agree on whether the
same-target KSC-surrogate SGQF route remains value-only or is now eligible for
analytical-score admission.

P4 is both an implementation-reconciliation and governance-reconciliation phase.
Unlike the earlier assumption that the analytical wrapper score was still missing,
P3 established that `bayesfilter/highdim/sv_mixture_cut4.py` already contains:
- `independent_panel_sv_mixture_fixed_sgqf_score(...)`,
- component analytical score helpers,
- and same-target UKF analytical wrapper score support.

Therefore P4 must answer the stricter question:
- is the existing wrapper-score implementation analytically correct and governed
  well enough to replace the current value-only artifact status?

## Entry Conditions Inherited From Previous Phase

- P3 result status is
  `PASS_P3_FIXED_SGQF_ANALYTICAL_SCORE_KERNEL_CERTIFIED` or a reviewed equivalent
  pass token.
- P3 certified the SGQF kernel score route as analytical-only and
  branch-disciplined.
- P1 still keeps KSC-surrogate score blocked pending wrapper-score
  certification/reconciliation.
- The visible execution ledger and visible stop handoff were updated through P3.
- Any P3 bounded-review findings were patched and the P3 packet rechecked.

## Required Artifacts

- Phase P4 result / close record:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p4-ksc-surrogate-analytical-wrapper-score-result-2026-06-23.md`
- Refreshed Phase P5 subplan:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p5-family-by-family-admission-subplan-2026-06-23.md`
- Visible execution ledger entry in:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-execution-ledger-2026-06-23.md`
- Bounded review ledger entry in:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-claude-review-ledger-2026-06-23.md`
- Visible stop handoff update in:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-stop-handoff-2026-06-23.md`

## Required Checks, Tests, And Reviews

Local checks before writing the P4 result:

```bash
git diff --check -- docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p4-ksc-surrogate-analytical-wrapper-score-subplan-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p4-ksc-surrogate-analytical-wrapper-score-result-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p5-family-by-family-admission-subplan-2026-06-23.md
rg -n "independent_panel_sv_mixture_fixed_sgqf_score|independent_panel_sv_mixture_ukf_score|wrapper_score_contract|value-only|autodiff|finite_difference|diagnostic" bayesfilter/highdim/sv_mixture_cut4.py tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py tests/highdim/test_p47_generalized_sv_equality.py docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-sv-result-2026-06-18.md docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-analytic-score-plan-2026-06-18.md
```

Focused wrapper-score checks (CPU-only by design unless a later trusted GPU plan
says otherwise):

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py tests/highdim/test_p47_generalized_sv_equality.py -k "ksc and (score or fixed_sgqf or ukf)"
```

Required reconciliation work:
- if the focused wrapper-score tests are sufficient and passing, update the
  governance/result language that still says the KSC SGQF route is value-only;
- if the focused wrapper-score tests are insufficient, add the smallest focused
  tests needed to certify the existing wrapper analytical score;
- if the implementation itself is unsound, repair it visibly and rerun the
  focused wrapper-score checks.

Bounded review:

- A read-only bounded review is required after the P4 result and P5 subplan are
  written.
- The review packet must be exact-path and limited to:
  - the master program,
  - the P4 subplan,
  - the P4 result,
  - the P5 subplan,
  - the visible execution ledger,
  - the review ledger,
  - the visible stop handoff,
  - the exact wrapper-score code/tests/artifacts touched in P4:
    - `bayesfilter/highdim/sv_mixture_cut4.py`
    - `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
    - `tests/highdim/test_p47_generalized_sv_equality.py`
    - `docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-sv-result-2026-06-18.md`
- The reviewer may assess only:
  - analytical wrapper-score correctness and evidence adequacy,
  - whether autodiff stayed diagnostic-only,
  - whether value-only status was lifted or preserved honestly,
  - feasibility of P5,
  - boundary safety.
- The reviewer may not authorize benchmark-matrix integration or broader family
  score admission beyond the KSC wrapper row.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the existing KSC-surrogate SGQF wrapper score implementation analytically correct and sufficiently evidenced to replace the current value-only governance status, while keeping autodiff diagnostic-only? |
| Baseline/comparator | `bayesfilter/highdim/sv_mixture_cut4.py`, the 2026-06-18 KSC value-only result note, the 2026-06-18 KSC analytical-score plan, focused highdim tests, and the P3 kernel-score certification result. |
| Primary pass criterion | The P4 result shows either: (A) the existing SGQF KSC wrapper score is analytically correct, FD-supported, and governance-reconciled, or (B) the row remains value-only with an explicit blocker reason preserved. In either case the code/tests/artifacts agree after P4. |
| Veto diagnostics | Any dependence on autodiff as the promoted SGQF wrapper score route, failed wrapper finite-difference checks, component/wrapper branch inconsistency, contradiction between code/tests and governance artifacts, or silent promotion without artifact reconciliation. |
| Explanatory diagnostics | wrapper-score test status, UKF wrapper-score status, SGQF-vs-UKF same-target score comparison availability, any remaining nonclaims, review verdict. |
| Not concluded | No broader family score admission beyond the KSC wrapper row, no benchmark-matrix integration yet, no actual transformed non-Gaussian SV claim, no HMC readiness claim. |
| Artifact preserving result | P4 result note, visible execution ledger, review ledger entry, visible stop handoff, and refreshed P5 subplan. |

## Forbidden Claims And Actions

- Do not promote autodiff into the SGQF wrapper score route.
- Do not treat existing code presence alone as sufficient admission evidence.
- Do not broaden KSC wrapper-score success into universal SGQF family score
  readiness.
- Do not modify machine-readable benchmark registry/matrix artifacts in P4.
- Do not silently leave value-only governance text in place if the row is now
  genuinely analytical-score-admissible.

## Exact Next-Phase Handoff Conditions

Advance to P5 only if all are true:

- the P4 result status is either
  `PASS_P4_FIXED_SGQF_KSC_ANALYTICAL_WRAPPER_SCORE_CERTIFIED` or a reviewed
  blocker status that honestly preserves value-only state;
- the focused KSC wrapper-score checks pass if score admission is claimed;
- any remaining autodiff references are diagnostic-only;
- code/tests/governance artifacts agree on the KSC SGQF wrapper score status;
- the visible execution ledger and stop handoff are updated for P4;
- the P5 subplan exists and is locally reviewed for consistency, correctness,
  feasibility, artifact coverage, and boundary safety;
- the bounded review of the P4 packet returns `VERDICT: AGREE`, or any
  `VERDICT: REVISE` findings are visibly patched and the focused P4 checks are
  rerun successfully.

If any condition fails, write a blocked P4 result and stop.  P5 must not begin.

## Stop Conditions

Stop with a blocked P4 result if:

- the existing KSC wrapper-score implementation fails focused FD/correctness
  checks and cannot be repaired within the P4 loop;
- SGQF wrapper score would still depend on autodiff as implementation rather
  than as a diagnostic oracle;
- governance/result artifacts cannot be reconciled honestly with the actual code
  and tests;
- the bounded review returns `VERDICT: REVISE` and the issue cannot be patched
  within five rounds.

## End-Of-Phase Protocol

At phase end:

1. Run the required focused local checks and KSC wrapper-score tests.
2. Write the P4 phase result / close record.
3. Draft or refresh the P5 subplan.
4. Update the visible execution ledger and stop handoff.
5. Run the bounded read-only review on the exact P4 packet.
6. If review finds a fixable issue, patch the same P4 packet visibly and rerun
   the focused checks.
7. Advance only if the exact P5 handoff conditions are satisfied.

## Skeptical Plan Audit

P4 could mislead in two opposite ways: it could leave the row value-only even
though the code/tests already justify analytical-score admission, or it could
promote the row merely because score code exists without fully reconciling tests
and governance artifacts.  It could also let autodiff creep back in as implied
score evidence.  This subplan avoids those failures by forcing code/test/artifact
reconciliation on the KSC wrapper row specifically, keeping autodiff
validation-only, and allowing an honest blocked/value-only outcome if the wrapper
score still fails certification.
