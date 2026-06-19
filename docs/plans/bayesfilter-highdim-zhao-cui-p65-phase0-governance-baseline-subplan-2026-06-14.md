# P65 Phase 0 Subplan: Governance, Baseline, And Launch Readiness

metadata_date: 2026-06-14
status: DRAFT_FOR_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p65-fixed-branch-rank-capacity-master-program-2026-06-14.md
phase: 0
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Lock the P65 baseline, source/document anchors, forbidden changes, review loop,
and local verification commands before any implementation repair.  Confirm that
the current local code still reproduces the P64 defensive-only high-rank
baseline.

## Entry Conditions Inherited From Previous Phase

- P64 result exists:
  `docs/plans/bayesfilter-highdim-zhao-cui-p64-normalizer-diagnosis-result-2026-06-14.md`.
- P50 fixed-branch derivation builds and has accepted readability review.
- Current P60 blocker is localized to high-rank defensive-only collapse.
- The worktree is dirty and contains untracked critical files; unrelated changes
  must be preserved.

## Required Artifacts

- This subplan.
- Master program:
  `docs/plans/bayesfilter-highdim-zhao-cui-p65-fixed-branch-rank-capacity-master-program-2026-06-14.md`.
- Visible runbook:
  `docs/plans/bayesfilter-highdim-zhao-cui-p65-visible-gated-execution-runbook-2026-06-14.md`.
- Execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p65-visible-execution-ledger-2026-06-14.md`.
- Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p65-claude-review-ledger-2026-06-14.md`.
- Phase result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase0-governance-baseline-result-2026-06-14.md`.
- Refreshed Phase 1 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the P65 program ready to launch against the current P64 baseline without wrong-baseline, threshold, source-anchor, or artifact-boundary drift? |
| Baseline/comparator | P64 result plus a fresh CPU-only JSON probe of the full pinned comparator tuple: `sample_count=1`, `fit_sample_count=2`, `low_fit_degree=0`, `high_fit_degree=1`, `low_fit_rank=1`, `high_fit_rank=2`. |
| Primary pass criterion | Local compile/import checks pass, the JSON probe still reports `candidate_high_defensive_only_transport`, high defensive-only steps `(1, 2)`, and high fitted square-root masses equal to zero at both steps, and bounded Claude review of planning artifacts ends in `VERDICT: AGREE`. |
| Veto diagnostics | Missing P64 result; changed baseline status; missing defensive-only blocker; missing source anchors; subplan lacks stop conditions; Claude review unavailable after successful probe; any pressure to weaken thresholds or skip review. |
| Explanatory diagnostics | Worktree status, current PDF/build note, normalizer decomposition, line anchors for source/document claims. |
| Not concluded | No bug fix, no rank/capacity diagnosis beyond P64, no implementation repair, no d=18 correctness. |
| Result artifact | Phase 0 result file with command outputs summarized and Phase 1 handoff. |

## Required Checks/Tests/Reviews

1. Local static context checks:
   - verify required files exist;
   - inspect exact template path;
   - scan phase artifacts for missing required headings.
2. Compile/import check:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

3. Fresh P64 baseline JSON probe:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python - <<'PY'
import json
import bayesfilter.highdim as h
r = h.p60_author_sir_same_route_rank_comparator(
    sample_count=1,
    fit_sample_count=2,
    low_fit_degree=0,
    high_fit_degree=1,
    low_fit_rank=1,
    high_fit_rank=2,
)
decomp = r.manifest.get("normalizer_decomposition", {})
high_terms = decomp.get("candidate_high", ())
print(json.dumps({
    "comparator_tuple": {
        "sample_count": 1,
        "fit_sample_count": 2,
        "low_fit_degree": 0,
        "high_fit_degree": 1,
        "low_fit_rank": 1,
        "high_fit_rank": 2,
    },
    "status": r.status,
    "blockers": r.blockers,
    "candidate_high_defensive_only_steps": decomp.get("candidate_high_defensive_only_steps"),
    "candidate_high_sqrt_square_normalizers": [
        row.get("sqrt_square_normalizer") for row in high_terms
    ],
    "normalizer_decomposition": decomp,
    "log_marginal_abs_delta": r.manifest.get("log_marginal_abs_delta"),
    "normalizer_increment_abs_deltas": r.manifest.get("normalizer_increment_abs_deltas"),
}, indent=2, default=str))
PY
```

4. Bounded Claude read-only review of:
   - master-program evidence contract and phase index;
   - Phase 0 evidence contract and stop conditions;
   - visible runbook role contract and state machine.

## Forbidden Claims/Actions

- Do not patch implementation in Phase 0.
- Do not run broad test suites.
- Do not run GPU/CUDA commands.
- Do not launch detached jobs.
- Do not change P60 thresholds or defensive `tau`.
- Do not claim the bug is fixed.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- compile/import passes;
- fresh P64 probe reproduces the defensive-only high-rank baseline;
- Claude review of planning artifacts returns a final post-repair
  `VERDICT: AGREE`;
- Phase 1 subplan is refreshed with any Phase 0 findings.

## Stop Conditions

Stop and write the Phase 0 result as blocked if:

- the P64 baseline no longer reproduces and the reason is not immediately
  explained by intended local changes;
- Claude review does not converge after five rounds for the same blocker;
- a required approval is denied;
- a needed command would require network, package installation, destructive git,
  or writes outside approved roots;
- a fix would require changing scope before Phase 1.

## End-Of-Subplan Protocol

1. Run the required local checks.
2. Write the Phase 0 result or blocker record.
3. Draft or refresh the Phase 1 subplan.
4. Review the Phase 1 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
