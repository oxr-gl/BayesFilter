# Phase Result: Two-Lane Comparison P7 Closeout And Leaderboard Result

metadata_date: 2026-06-24
plan_reference: `docs/plans/bayesfilter-two-lane-filter-comparison-p7-closeout-and-leaderboard-result-subplan-2026-06-24.md`
master_program: `docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md`
status: PASS_P7_TWO_LANE_REFERENCE_LEADERBOARD_CLOSEOUT_WITH_REPAIRED_SGQF_HIGHDIM_CLASSIFICATION

## Phase Objective

Close the two-lane leaderboard program with repaired SGQF classification and
explicit scope limits.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| close the current program as a reference two-lane leaderboard with repaired SGQF row classification | satisfied for governance and emitted reference artifacts | no CUT4 leakage into highdim, no actual-vs-surrogate SV merge, no blanket false SGQF block remains | several highdim rows still are not full three-way comparison rows because SGQF and/or Zhao-Cui source-scope evaluators are genuinely missing | if desired, begin a new reviewed program to broaden source-scope SGQF and Zhao-Cui evaluator coverage and/or open a GPU timing lane | no merged overall winner, no fully populated three-way highdim leaderboard, no production-GPU timing claim |

## Final Emitted Artifacts

### Low-dimensional lane
- JSON: `docs/plans/bayesfilter-two-lane-lowdim-leaderboard-results-2026-06-24.json`
- Markdown: `docs/plans/bayesfilter-two-lane-lowdim-leaderboard-results-2026-06-24.md`
- Harness: `docs/benchmarks/benchmark_two_lane_lowdim_leaderboard.py`

### High-dimensional / source-scope lane
- JSON: `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-24.json`
- Markdown: `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-24.md`
- Harness: `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`

## Final Program Summary

### Lowdim lane
The lowdim lane has a CPU-only reference leaderboard packet with rankable LGSSM
and KSC surrogate rows, plus explicit SGQF status-only/blocked rows where the
current lane does not support broader same-target execution.

### Highdim lane
The repaired highdim lane now reflects actual current SGQF support more
faithfully:
- source-scope LGSSM: SGQF executed, UKF executed, Zhao-Cui still missing evaluator
- actual transformed SV: SGQF remains blocked, UKF and Zhao-Cui executed
- KSC surrogate T1000: SGQF still blocked at source-scope T1000 level, UKF and Zhao-Cui executed
- spatial SIR: SGQF blocked, UKF value-only executed, Zhao-Cui missing evaluator
- predator-prey: SGQF executed, UKF executed, Zhao-Cui missing evaluator
- generalized SV source row: SGQF blocked, UKF executed, Zhao-Cui missing evaluator

## Strongest Current Conclusions

1. The two-lane leaderboard contract is implemented durably in emitted artifacts.
2. SGQF should not be blanket-blocked on the highdim lane; the repaired packet now executes SGQF where direct reviewed routes exist.
3. Actual transformed SV and KSC surrogate SV remain separated correctly.
4. CUT4 stays out of the highdim lane.
5. Remaining SGQF blocks are now row-specific rather than blanket.

## Final Nonclaims

- No merged overall repo-wide leaderboard is claimed.
- No full three-way highdim winner table is claimed.
- No production-GPU timing result is claimed.
- No broadened SGQF high-dimensional admission beyond the repaired row-specific route set is claimed.
- No actual-transformed-SV and KSC-surrogate-SV merged ranking is claimed.
