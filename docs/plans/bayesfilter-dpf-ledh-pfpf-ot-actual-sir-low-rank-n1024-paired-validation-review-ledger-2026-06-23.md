# Actual-SIR Low-Rank N1024 Paired Validation Review Ledger

Date: 2026-06-23

Status: `SUBPLAN_REVIEW_CONVERGED`

## Round 1

Reviewer: Claude Opus/max, read-only.

Scope:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n512-seed-replication-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n1024-paired-validation-subplan-2026-06-23.md`

Verdict: `VERDICT: REVISE`

Material findings:

- The subplan left an unconstrained branch to candidate consolidation without a
  predeclared engineering criterion.
- The formal stop-condition list did not explicitly mirror vetoes for
  nonfinite outputs, ESS, log-weight normalization, and factor residual
  threshold failures.

Patch:

- Required `N=1024` seed replication as the default viable-candidate handoff.
- Forbid consolidation at this handoff unless a separate reviewed consolidation
  subplan declares an engineering-only criterion based on hard-veto survival and
  resource envelope, not descriptive timing rank.
- Added nonfinite output, ESS hard veto, log-weight normalization failure, and
  factor residual threshold failure to explicit stop conditions.

Focused checks after patch:

- `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: pass, `17 passed`.
- Local patch consistency check.
  - Result: pass, `n1024-subplan-r1-patch-consistency-pass`.

## Round 2

Reviewer: Claude Opus/max, read-only focused review.

Scope:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n1024-paired-validation-subplan-2026-06-23.md`

Verdict: `VERDICT: AGREE`

Reviewer summary:

- The unconstrained consolidation issue is fixed.
- The stop-condition gap is fixed.
- Exact five-candidate survivor handling, artifact checks, nonclaim
  boundaries, and feasibility remain intact.

## Final Review State

The N1024 paired-validation subplan is reviewed and ready for execution subject
to trusted GPU availability and the pre-run checks in the subplan.
