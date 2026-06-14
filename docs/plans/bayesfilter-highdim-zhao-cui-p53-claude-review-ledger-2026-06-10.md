# P53 Claude Review Ledger

metadata_date: 2026-06-10
program: P53-factorized-spatial-sir-transition-repair
status: PLAN_AMENDMENT_REVIEW_CONVERGED
supervisor: Codex
reviewer: Claude Code read-only

## Review Iterations

### Iteration 1 - 2026-06-10 - REVISE

Reviewer: Claude Code Opus read-only

Verdict:

- `VERDICT: REVISE`

Findings:

- P53 repaired the original P52 ordering error by requiring route design,
  implementation, and lower-rung tie-out before rank/scaling phases.
- P53 still had a material route-class loophole: a streaming dense-equivalent
  lower-rung route could pass M1-M3 and unlock M4-M6 even though the master
  text admitted that route is insufficient for high-dimensional scaling.
- M2's "factorized route" naming conflicted with allowing a non-factorized
  blocked streaming dense-equivalent route.
- The runbook needed stronger CPU-only/run-manifest discipline.

Repairs applied:

- Added a separate `P53-M4` scaling-route gate.
- Shifted rank selection and dimension phases to `P53-M5` through `P53-M8`.
- Added route classes: `lower_rung_dense_equivalent` and `scaling_route`.
- Required `PASS_P53_M4_SCALING_ROUTE_GATE` before rank selection or
  d=18/d=50/d=100 phases can run.
- Renamed M2 as lower-rung TensorFlow route implementation.
- Added CPU-only and run-manifest requirements to the visible runbook.

### Iteration 2 - 2026-06-10 - AGREE

Reviewer: Claude Code Opus read-only

Verdict:

- `VERDICT: AGREE`

Findings:

- The route-class loophole is materially closed.
- `PASS_P53_M4_SCALING_ROUTE_GATE` is required before rank selection or
  d=18/d=50/d=100 phases can run.
- Wrong-baseline and proxy-promotion discipline is sound enough for launch.
- Stop conditions and run-manifest discipline are adequate.
- Claude noted a nonblocking wording ambiguity that "used for d=18/d=50/d=100
  rows" should mean row-level pass/block outcomes, not full filtering at every
  dimension.

Repair applied after agreement:

- Reworded the master-program primary criterion to say the route is
  "addressed for d=18/d=50/d=100 rows with explicit pass/block tokens,
  dimension-specific claim classes, and Claude read-only review."

### Amendment Iteration 1 - 2026-06-10 - REVISE

Reviewer: Claude Code Opus read-only

Verdict:

- `VERDICT: REVISE`

Findings:

- The M4A-M4D split materially repaired the overloaded M4 planning error.
- Remaining blocker: the machine-readable DAG allowed P53-M8 closeout after
  M4D admission without requiring P53-M5, P53-M6, and P53-M7 outcomes.
- Static tests missed the M8 admission gap.
- M4D subplan promised M5/M6/M7 admission tests but not M8 admission tests.

Repairs applied:

- P53-M8 now depends on P53-M0/M1/M2/M3/M4D/M5/M6/M7.
- M4D subplan requires M8 admission tests.
- M8 subplan states closeout cannot substitute for substantive phases.
- Tests now prove M8 blocks after M4D alone and admits only after
  P53-M5/P53-M6/P53-M7 pass tokens.

### Amendment Iteration 2 - 2026-06-10 - AGREE

Reviewer: Claude Code Opus read-only

Verdict:

- `VERDICT: AGREE`

Findings:

- The M8 premature-closeout loophole is closed.
- M4D is an admission gate, not a completion surrogate.
- M8 cannot substitute for substantive M5/M6/M7 phases.
- The amended plan is convergent with the M4A-M4D split and M5-M8 gated by
  `PASS_P53_M4D_SCALING_ROUTE_ADMISSION` plus substantive outcomes.
