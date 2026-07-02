# SIR Gradient HMC-Direction Visible Stop Handoff

Date: 2026-07-01

Status: `CLOSED_WITH_BUDGET100_MEMORY_BLOCKER`

## Final State

The visible gated SIR gradient program is closed for this run.  It no longer
has the earlier Phase 3 approval blocker.  Phase 3 passed, Phase 5 budget 10
completed, and the active unresolved blocker is budget-100 diagnostic memory.

## Final Phase Reached

- Final phase reached: `Phase 6`
- Final status: `CLOSED_WITH_BUDGET100_MEMORY_BLOCKER`
- Active blocker: `BLOCKED_SINGLE_BUDGET100_EXIT137`

## What Was Established

- The SIR diagnostic route can execute on trusted GPU/XLA/TF32.
- The route prerequisite gate passed for Phase 3 smoke and Phase 5 budget 10.
- Phase 5 budget 10 produced a full material JSON/Markdown artifact.
- At budget 10, row residual passes but all raw SIR gradient directions do not
  pass the frozen HMC-direction gate.

## What Remains Blocked

- Budget 100 cannot complete with the current material diagnostic shape at
  `N=64`, `T=3`, five seeds, 13 FD offsets, XLA manual reverse, and reviewed
  chunking knobs.
- Budget 100 exits with code 137 even in a separate Python process.

## Main Result Artifacts

- Phase 6 closeout:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase6-closeout-result-2026-06-30.md`
- Phase 5 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-repair-ladders-result-2026-06-30.md`
- Phase 5 budget 10 JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget10-2026-06-30.json`
- Phase 5 budget 100 progress:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget100-progress-2026-06-30.json`
- Execution ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-visible-execution-ledger-2026-06-30.md`
- Claude review ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-claude-review-ledger-2026-06-30.md`

## Recommended Next Action

Create a new reviewed subplan for finer-grained scalar artifact construction:

- one process per budget and seed group for manual score;
- one process per budget, FD direction, theta-offset chunk, and seed group for
  objective values;
- deterministic aggregation into the same regression and frozen Phase 1 gate;
- aggregation must exactly reproduce the current estimator/comparator before
  any material rerun.

Do not rerun budget 100 monolithically.  Do not use CPU fallback as material
evidence.  Do not change the gate thresholds to rescue budget-10 results.

## Nonclaims

- No SIR gradient correctness claim.
- No HMC readiness claim.
- No posterior correctness claim.
- No global Sinkhorn budget claim.
- No nonlinear-model generalization claim.
