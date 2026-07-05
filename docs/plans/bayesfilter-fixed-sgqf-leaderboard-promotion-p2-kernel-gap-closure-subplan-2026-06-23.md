# Phase P2 Subplan: Kernel Gap Closure

metadata_date: 2026-06-23
status: DRAFT_PENDING_P1_HANDOFF_AND_LOCAL_CHECKS
master_program: docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-master-program-2026-06-23.md
phase: P2
executor: Claude Code
reviewer: read-only bounded reviewer only

## Phase Objective

Revisit the earlier fixed-SGQF gap set G1-G8 and classify each item as already
closed by existing evidence, requiring a new focused test, requiring a new
analytical-derivative route, or irreducibly outside the current leaderboard
scope.  Where a gap can be closed by focused SGQF kernel/contract testing without
changing benchmark semantics, do so and record the result.

P2 is the first phase allowed to run focused SGQF kernel/contract checks under
this new master program.  It is still not allowed to update machine-readable
leaderboard registry/matrix artifacts; those remain later-phase work.

## Entry Conditions Inherited From Previous Phase

- P1 result status is
  `PASS_P1_FIXED_SGQF_ADMISSION_LEDGER_WRITTEN` or a reviewed equivalent pass
  token.
- P1 froze the family-level value and analytical-score admission boundaries.
- The KSC-surrogate family remains value-admitted but score-blocked pending P4.
- The visible execution ledger and visible stop handoff were updated through P1.
- Any P1 bounded-review findings were patched and the P1 packet rechecked.

## Required Artifacts

- Phase P2 result / close record:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p2-kernel-gap-closure-result-2026-06-23.md`
- Refreshed Phase P3 subplan:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-subplan-2026-06-23.md`
- Visible execution ledger entry in:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-execution-ledger-2026-06-23.md`
- Bounded review ledger entry in:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-claude-review-ledger-2026-06-23.md`
- Visible stop handoff update in:
  `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-visible-stop-handoff-2026-06-23.md`

## Required Checks, Tests, And Reviews

Local checks before writing the P2 result:

```bash
git diff --check -- docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p2-kernel-gap-closure-subplan-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p2-kernel-gap-closure-result-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-subplan-2026-06-23.md
rg -n "G1|G2|G3|G4|G5|G6|G7|G8|analytical|autodiff|fixed_sgqf_level_2|blocked_missing_analytical_wrapper_score" docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p2-kernel-gap-closure-subplan-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p2-kernel-gap-closure-result-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-master-program-2026-06-23.md
```

Focused SGQF kernel/contract checks (CPU-only by design unless a later trusted
GPU plan says otherwise):

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_tf.py tests/test_fixed_sgqf_values_tf.py tests/test_fixed_sgqf_scores_tf.py tests/test_fixed_sgqf_branch_contract_tf.py tests/test_fixed_sgqf_verification_tf.py tests/test_fixed_sgqf_audit_tf.py tests/test_fixed_sgqf_testing_integration_tf.py tests/test_fixed_sgqf_integration_tf.py
```

If needed for gap-specific classification, add only focused subsets justified in
the P2 result note.  Do not run benchmark harnesses or wrapper-family-specific
score phases in P2.

Bounded review:

- A read-only bounded review is required after the P2 result and P3 subplan are
  written.
- The review packet must be exact-path and limited to:
  - the master program,
  - the P2 subplan,
  - the P2 result,
  - the P3 subplan,
  - the visible execution ledger,
  - the review ledger,
  - the visible stop handoff,
  - and the exact SGQF kernel/contract files touched in P2, if any.
- The reviewer may assess only:
  - G1-G8 classification correctness,
  - consistency with the frozen P1 admission ledger,
  - feasibility of P3,
  - artifact coverage,
  - boundary safety.
- The reviewer may not authorize family-level score promotion, benchmark matrix
  edits, or scope widening.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which earlier SGQF kernel/testing gaps G1-G8 are already closed by current evidence, which need new focused SGQF tests, which need new analytical derivative work, and which remain outside current leaderboard scope? |
| Baseline/comparator | The original fixed-SGQF gap program and inventory result, the repaired-lane reset memo, the current SGQF regression suites, and the P1 admission ledger boundaries. |
| Primary pass criterion | The P2 result classifies every G1-G8 gap explicitly; runs the focused SGQF kernel/contract checks needed to support those classifications; preserves the analytical-gradient-only rule; and drafts a P3 subplan that stays within the P1 ledger boundaries. |
| Veto diagnostics | Any G1-G8 item omitted; any gap declared closed without citing current evidence or focused checks; any score-related gap closed by appealing to autodiff; or any P2 action that quietly spills into family-level wrapper-score or benchmark-matrix work. |
| Explanatory diagnostics | SGQF regression-suite status, per-gap classification counts, unchanged-vs-new evidence split, review verdict. |
| Not concluded | No machine-readable leaderboard integration yet, no KSC wrapper-score completion yet, no family-level score admission yet, and no universal SGQF superiority claim. |
| Artifact preserving result | P2 result note, visible execution ledger, review ledger entry, visible stop handoff, and refreshed P3 subplan. |

## Forbidden Claims And Actions

- Do not close a score-related gap by citing autodiff-backed evidence as if it
  were analytical derivative support.
- Do not run benchmark harnesses, preflight matrices, or numeric leaderboard
  runners in P2.
- Do not modify machine-readable benchmark registry/matrix JSON artifacts in P2.
- Do not reopen blocked literature-backed families by reinterpretation.
- Do not treat a passing SGQF kernel regression suite as automatic family-level
  benchmark admission.

## Exact Next-Phase Handoff Conditions

Advance to P3 only if all are true:

- the P2 result status is
  `PASS_P2_FIXED_SGQF_KERNEL_GAPS_CLASSIFIED` or an equivalent reviewed pass
  token;
- every G1-G8 item has an explicit classification;
- no score-related gap is marked closed by autodiff-backed reasoning;
- the visible execution ledger and stop handoff are updated for P2;
- the P3 subplan exists and is locally reviewed for consistency, correctness,
  feasibility, artifact coverage, and boundary safety;
- the bounded review of the P2 packet returns `VERDICT: AGREE`, or any
  `VERDICT: REVISE` findings are visibly patched and the focused P2 checks are
  rerun successfully.

If any condition fails, write a blocked P2 result and stop.  P3 must not begin.

## Stop Conditions

Stop with a blocked P2 result if:

- any G1-G8 item cannot be classified honestly from current evidence plus focused
  SGQF kernel checks;
- the focused SGQF regression suite fails and the failure cannot be reconciled
  within the P2 repair loop;
- a gap appears to require wrapper-family work, benchmark-matrix work, or
  numerical leaderboard work that belongs to later phases;
- the bounded review returns `VERDICT: REVISE` and the issue cannot be patched
  within five rounds.

## End-Of-Phase Protocol

At phase end:

1. Run the required focused local checks and SGQF kernel/contract tests.
2. Write the P2 phase result / close record.
3. Draft or refresh the P3 subplan.
4. Update the visible execution ledger and stop handoff.
5. Run the bounded read-only review on the exact P2 packet.
6. If review finds a fixable issue, patch the same P2 packet visibly and rerun
   the focused checks.
7. Advance only if the exact P3 handoff conditions are satisfied.

## Skeptical Plan Audit

P2 could mislead if it treats the repaired SGQF regression suite as proof that
all leaderboard-family problems are solved, or if it quietly substitutes
autodiff-backed evidence for analytical-score closure.  It could also blur the
line between kernel evidence and wrapper-family admission.  This subplan prevents
those failures by forcing explicit G1-G8 classification, restricting execution
to focused SGQF kernel/contract checks, keeping family-level wrapper-score work
for later phases, and preserving the analytical-gradient-only rule.
