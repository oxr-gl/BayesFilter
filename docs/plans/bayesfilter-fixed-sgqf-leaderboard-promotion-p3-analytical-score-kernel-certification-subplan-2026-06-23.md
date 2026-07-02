# Phase P3 Subplan: Analytical-Score Kernel Certification

metadata_date: 2026-06-23
status: DRAFT_PENDING_P2_HANDOFF_AND_LOCAL_CHECKS
master_program: docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-master-program-2026-06-23.md
phase: P3
executor: Claude Code
reviewer: read-only bounded reviewer only

## Phase Objective

Certify, for the current fixed-SGQF kernel scope, that score-bearing SGQF rows
use explicit analytical derivatives only, preserve accepted-branch / same-scalar
finite-difference discipline, and do not rely on autodiff as the promoted score
route.

P3 is a certification-and-boundary phase.  It may run focused SGQF score/branch
checks and, if required, tighten score-facing diagnostics or documentation in the
SGQF kernel layer.  It does not yet implement family-level wrapper analytical
scores; that remains P4 work.

## Entry Conditions Inherited From Previous Phase

- P2 result status is
  `PASS_P2_FIXED_SGQF_KERNEL_GAPS_CLASSIFIED` or a reviewed equivalent pass
  token.
- P2 classified G5 as closed at kernel level for the current scope.
- P1 still freezes family-level score admission at zero.
- KSC-surrogate score remains blocked pending analytical outer wrapper work.
- The visible execution ledger and visible stop handoff were updated through P2.
- Any P2 bounded-review findings were patched and the P2 packet rechecked.

## Required Artifacts

- Phase P3 result / close record:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-result-2026-06-23.md`
- Refreshed Phase P4 subplan:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p4-ksc-surrogate-analytical-wrapper-score-subplan-2026-06-23.md`
- Visible execution ledger entry in:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-execution-ledger-2026-06-23.md`
- Bounded review ledger entry in:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-claude-review-ledger-2026-06-23.md`
- Visible stop handoff update in:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-stop-handoff-2026-06-23.md`

## Required Checks, Tests, And Reviews

Local checks before writing the P3 result:

```bash
git diff --check -- docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-subplan-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-result-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p4-ksc-surrogate-analytical-wrapper-score-subplan-2026-06-23.md
rg -n "analytical|autodiff|same-branch|finite difference|blocked_missing_analytical_wrapper_score|diagnostic-only" docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-subplan-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-result-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-master-program-2026-06-23.md
```

Focused SGQF score/branch checks (CPU-only by design unless a later trusted GPU
plan says otherwise):

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_scores_tf.py tests/test_fixed_sgqf_branch_contract_tf.py tests/test_fixed_sgqf_testing_integration_tf.py tests/test_fixed_sgqf_verification_tf.py -k "score or branch or finite_difference"
```

If phase-local tightening is required, keep it inside the SGQF kernel/contract
surface only.  Do not begin KSC wrapper implementation in P3.

Bounded review:

- A read-only bounded review is required after the P3 result and P4 subplan are
  written.
- The review packet must be exact-path and limited to:
  - the master program,
  - the P3 subplan,
  - the P3 result,
  - the P4 subplan,
  - the visible execution ledger,
  - the review ledger,
  - the visible stop handoff,
  - and the exact SGQF score/branch files touched in P3, if any.
- The reviewer may assess only:
  - analytical-score certification correctness,
  - same-branch/same-scalar boundary discipline,
  - artifact coverage,
  - feasibility of P4,
  - boundary safety.
- The reviewer may not authorize family-level score promotion, wrapper-score
  completion, or benchmark-matrix integration.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the current fixed-SGQF kernel score route be certified as an analytical-derivative route with accepted-branch finite-difference support, while keeping autodiff diagnostic-only? |
| Baseline/comparator | Existing SGQF score/branch tests, the P2 gap ledger, and the master-program analytical-gradient rule. |
| Primary pass criterion | The P3 result shows that the SGQF kernel score route used for current promotion scope is explicit/analytical, branch-disciplined, supported by focused FD/branch tests, and not promoted via autodiff; and it refreshes a P4 subplan that keeps wrapper-score work separate. |
| Veto diagnostics | Any surviving dependence on autodiff as the promoted score route, missing same-branch/FD evidence on the current kernel score path, contradiction with the P2 gap ledger, or any spill into family-level wrapper-score promotion. |
| Explanatory diagnostics | focused score-suite status, branch-signature coverage, failure-signature coverage, diagnostic-only autodiff references if any, review verdict. |
| Not concluded | No KSC wrapper-score completion yet, no family-level score admission yet, no matrix integration yet, and no HMC readiness claim. |
| Artifact preserving result | P3 result note, visible execution ledger, review ledger entry, visible stop handoff, and refreshed P4 subplan. |

## Forbidden Claims And Actions

- Do not promote autodiff into the SGQF analytical-score route.
- Do not implement the KSC outer wrapper score in P3.
- Do not infer family-level score admission from kernel certification alone.
- Do not modify machine-readable benchmark registry/matrix artifacts in P3.
- Do not relax same-branch / same-scalar discipline for score rows.

## Exact Next-Phase Handoff Conditions

Advance to P4 only if all are true:

- the P3 result status is
  `PASS_P3_FIXED_SGQF_ANALYTICAL_SCORE_KERNEL_CERTIFIED` or an equivalent
  reviewed pass token;
- the P3 result explicitly states that autodiff remains diagnostic-only;
- the focused SGQF score/branch checks pass;
- the visible execution ledger and stop handoff are updated for P3;
- the P4 subplan exists and is locally reviewed for consistency, correctness,
  feasibility, artifact coverage, and boundary safety;
- the bounded review of the P3 packet returns `VERDICT: AGREE`, or any
  `VERDICT: REVISE` findings are visibly patched and the focused P3 checks are
  rerun successfully.

If any condition fails, write a blocked P3 result and stop.  P4 must not begin.

## Stop Conditions

Stop with a blocked P3 result if:

- the focused SGQF score/branch suite fails and the failure cannot be reconciled
  within the P3 repair loop;
- any kernel score path used for promotion still depends on autodiff as an
  implementation rather than as a diagnostic oracle;
- the certification would require family-level wrapper-score claims that belong
  to P4;
- the bounded review returns `VERDICT: REVISE` and the issue cannot be patched
  within five rounds.

## End-Of-Phase Protocol

At phase end:

1. Run the required focused local checks and SGQF score/branch tests.
2. Write the P3 phase result / close record.
3. Draft or refresh the P4 subplan.
4. Update the visible execution ledger and stop handoff.
5. Run the bounded read-only review on the exact P3 packet.
6. If review finds a fixable issue, patch the same P3 packet visibly and rerun
   the focused checks.
7. Advance only if the exact P4 handoff conditions are satisfied.

## Skeptical Plan Audit

P3 could mislead if it treats passing SGQF score tests as automatic permission to
promote family-level score cells, or if autodiff slips back in as an implicit
score implementation through convenience language.  It could also overread
accepted-branch FD parity as a broader HMC claim.  This subplan avoids those
failures by keeping P3 kernel-scoped, preserving autodiff as diagnostic-only,
requiring explicit same-branch score checks, and deferring all wrapper-family
score work to P4.
