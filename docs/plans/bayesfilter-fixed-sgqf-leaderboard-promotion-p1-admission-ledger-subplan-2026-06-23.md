# Phase P1 Subplan: Admission Ledger

metadata_date: 2026-06-23
status: DRAFT_PENDING_P0_HANDOFF_AND_LOCAL_CHECKS
master_program: docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-master-program-2026-06-23.md
phase: P1
executor: Claude Code
reviewer: read-only bounded reviewer only

## Phase Objective

Assign every intended fixed-SGQF × target-family cell an explicit admission
class, scalar meaning, reference policy, comparator-eligibility status, and
blocker reason when not admitted, so that later matrix integration phases cannot
create silent holes or informal scope drift.

P1 is a governance/classification phase.  It may prepare ledger artifacts and,
if needed, phase-local planning notes, but it does not yet integrate SGQF cells
into the machine-readable benchmark registry/matrix artifacts.  That work belongs
to later phases after the ledger is frozen.

## Entry Conditions Inherited From Previous Phase

- P0 result status is
  `PASS_P0_FIXED_SGQF_LEADERBOARD_SCOPE_FROZEN` or a reviewed equivalent pass
  token.
- P0 froze `fixed_sgqf_level_2` as the first intended leaderboard variant.
- P0 recorded a supersession ledger for prior fixed-SGQF planning/results.
- The visible execution ledger and visible stop handoff were updated through P0.
- Any P0 bounded-review findings were patched and the P0 packet rechecked.

## Required Artifacts

- Phase P1 result / close record:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p1-admission-ledger-result-2026-06-23.md`
- Refreshed Phase P2 subplan:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p2-kernel-gap-closure-subplan-2026-06-23.md`
- Visible execution ledger entry in:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-execution-ledger-2026-06-23.md`
- Bounded review ledger entry in:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-claude-review-ledger-2026-06-23.md`
- Visible stop handoff update in:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-stop-handoff-2026-06-23.md`

## Required Checks, Tests, And Reviews

Local checks before writing the P1 result:

```bash
git diff --check -- docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p1-admission-ledger-subplan-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p1-admission-ledger-result-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p2-kernel-gap-closure-subplan-2026-06-23.md
rg -n "benchmark_lgssm_exact_oracle_m3_T50|zhao_cui_sv_actual_nongaussian_T1000|zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000|zhao_cui_spatial_sir_austria_j9_T20|zhao_cui_predator_prey_T20|zhao_cui_generalized_sv_synthetic_from_estimated_values|fixed_sgqf_level_2|admit_exact|admit_dense_reference_only|admit_value_baseline_only|admit_analytical_score|blocked_not_same_target|blocked_missing_analytical_wrapper_score|blocked_branch_inconsistent|blocked_unstable_fd_window|diagnostic_only|historical_only" docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p1-admission-ledger-subplan-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p1-admission-ledger-result-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-master-program-2026-06-23.md
```

Context-loading and classification checks:

- load and record the following artifacts before writing the P1 result:
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json`
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json`
  - `docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-closeout-result-2026-06-16.md`
  - `docs/plans/bayesfilter-fixed-sgqf-broader-nonlinear-comparison-closeout-result-2026-06-16.md`
  - `docs/plans/bayesfilter-fixed-sgqf-structural-adapter-result-2026-06-16.md`
  - `docs/plans/bayesfilter-fixed-sgqf-ksc-surrogate-analytic-score-plan-2026-06-18.md`
- verify that the P1 result contains, for every intended SGQF family cell:
  - admission class,
  - scalar meaning,
  - reference policy,
  - comparator eligibility,
  - blocker reason when not admitted,
  - explicit nonclaims.
- verify that blocked families remain visible and are not silently omitted.

Bounded review:

- A read-only bounded review is required after the P1 result and P2 subplan are
  written.
- The review packet must be exact-path and limited to:
  - the master program,
  - the P1 subplan,
  - the P1 result,
  - the P2 subplan,
  - the visible execution ledger,
  - the review ledger,
  - the visible stop handoff.
- The reviewer may assess only:
  - admission-logic consistency,
  - classification correctness relative to loaded artifacts,
  - feasibility of later phases,
  - artifact coverage,
  - boundary safety.
- The reviewer may not authorize SGQF numerical promotion, alter benchmark scope,
  or override blocked-family reasons.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can every intended fixed-SGQF family cell be classified explicitly now, without changing target semantics or overclaiming score readiness? |
| Baseline/comparator | The source-paper scope contract, the target registry, the fixed-SGQF broader-comparison closeout, the nonlinear-model-suite closeout, the structural-adapter result, and the KSC analytical-score plan. |
| Primary pass criterion | The P1 result classifies every intended SGQF family cell with an explicit admission class; preserves `fixed_sgqf_level_2` as the first declared variant; states scalar meaning and reference policy; gives blocker reasons where needed; and drafts a P2 subplan that respects those boundaries. |
| Veto diagnostics | Any intended family cell omitted; any blocked family admitted without same-target justification; any score-bearing family treated as analytical-score-ready without explicit analytical derivative support; any contradiction with the source-paper scope contract or prior fixed-SGQF closeouts. |
| Explanatory diagnostics | Family roster, admission-class counts, blocker-reason counts, narrow-harness vs literature-backed distinctions, review verdict. |
| Not concluded | No numeric leaderboard integration yet, no machine-readable matrix updates yet, no new SGQF kernel evidence yet, no KSC wrapper-score completion yet, and no universal family readiness claim. |
| Artifact preserving result | P1 result note, visible execution ledger, review ledger entry, visible stop handoff, and refreshed P2 subplan. |

## Forbidden Claims And Actions

- Do not admit a family by silently changing target semantics or scalar meaning.
- Do not claim SGQF analytical-score admission for any family lacking explicit
  analytical derivative support.
- Do not treat autodiff-backed wrapper evidence as analytical-score admission.
- Do not modify the machine-readable benchmark registry or coverage/preflight
  JSON artifacts yet.
- Do not erase blocked families; preserve them explicitly in the admission
  ledger.
- Do not convert engineering/debugging-only P44 rows into final literature-backed
  leaderboard scope.

## Exact Next-Phase Handoff Conditions

Advance to P2 only if all are true:

- the P1 result status is
  `PASS_P1_FIXED_SGQF_ADMISSION_LEDGER_WRITTEN` or an equivalent reviewed pass
  token;
- every intended SGQF family cell has an explicit admission class and blocker
  reason if not admitted;
- the P1 result preserves `fixed_sgqf_level_2` as the first declared variant and
  carries explicit nonclaims about score readiness and blocked families;
- the visible execution ledger and stop handoff are updated for P1;
- the P2 subplan exists and is locally reviewed for consistency, correctness,
  feasibility, artifact coverage, and boundary safety;
- the bounded review of the P1 packet returns `VERDICT: AGREE`, or any
  `VERDICT: REVISE` findings are visibly patched and the focused P1 checks are
  rerun successfully.

If any condition fails, write a blocked P1 result and stop.  P2 must not begin.

## Stop Conditions

Stop with a blocked P1 result if:

- any intended family cell cannot be classified without inventing new SGQF route
  semantics;
- the loaded artifacts disagree materially about the current status of a family
  and the disagreement cannot be reconciled honestly in the ledger;
- the KSC-surrogate family would need to be marked score-admitted before the
  analytical-wrapper-score phase exists;
- focused classification consistency checks fail and cannot be repaired cleanly;
- the bounded review returns `VERDICT: REVISE` and the issue cannot be patched
  within five rounds.

## End-Of-Phase Protocol

At phase end:

1. Run the required focused local checks.
2. Write the P1 phase result / close record.
3. Draft or refresh the P2 subplan.
4. Update the visible execution ledger and stop handoff.
5. Run the bounded read-only review on the exact P1 packet.
6. If review finds a fixable issue, patch the same P1 packet visibly and rerun
   the focused checks.
7. Advance only if the exact P2 handoff conditions are satisfied.

## Skeptical Plan Audit

P1 could appear to pass while still setting up a misleading leaderboard if it
compresses literature-backed families and narrow harness rows into one undifferentiated
admission claim, or if it quietly treats the KSC wrapper as score-ready before an
analytical outer score exists.  It could also fail by omitting blocked cells and
thereby creating silent holes for later matrix phases.  This subplan prevents
those failures by forcing per-family admission classes, preserving blocked-family
reasons, freezing `fixed_sgqf_level_2`, and keeping score admission gated on
explicit analytical-derivative support.
