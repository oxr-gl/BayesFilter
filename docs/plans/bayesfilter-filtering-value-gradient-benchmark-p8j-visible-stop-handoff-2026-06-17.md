# P8j Visible Stop Handoff

Date: 2026-06-17

Status: `PHASE5D_REVIEW_PASS_PHASE5E_READY_TO_EXECUTE`

## Current State

P8j has been drafted as the DPF SIR d18 leaderboard-completion lane.

This lane is distinct from:

- P71 Zhao-Cui fixed-branch/SIR d18 validation;
- P8h/P8i scalar-SV DPF/LEDH route repair and follow-on diagnostics;
- the monograph rewrite lane.

## Active Target

- row ID: `zhao_cui_spatial_sir_austria_j9_T20`;
- horizon: `T=20`;
- state dimension: `18`;
- observation dimension: `9`;
- fixed-parameter row with no free theta.

## Artifact Pointers

- Master program:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md`
- Visible runbook:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-gated-execution-runbook-2026-06-17.md`
- Phase 0 subplan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase0-governance-current-evidence-subplan-2026-06-17.md`
- Execution ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md`
- Claude review ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-claude-review-ledger-2026-06-17.md`

## Current Gate

Phase 0 passed.  Claude review iteration 1 returned `VERDICT: REVISE` for
fixable provenance, Phase 6 particle-count gating, and artifact-accounting
issues.  Those issues were patched and Claude review iteration 2 returned
`VERDICT: AGREE`.

Phase 1 callback-contract subplan completed local checks.  Claude review
iteration 1 returned `VERDICT: REVISE` for fixable contract issues:

- transition-density wording had to make clear that the Gaussian density is
  pre-projection adapter metadata for clipped propagation, not exact clipped
  pushforward density;
- Phase 2 tests had to include semantic tie-outs against
  `zhao_cui_sir_austria_model()`, not shape checks only.

Those issues were patched.  Claude review iteration 2 returned
`VERDICT: AGREE`.

Phase 1 passed.  Phase 2 bootstrap SIR smoke implementation subplan completed
local checks.  Claude review iteration 1 returned `VERDICT: REVISE` because
the smoke command used `_numeric_dpf_cell()`, whose artifact schema is
five-seed DPF value language.  Phase 2 has been patched to call
`_dpf_single_run()` directly and write an explicit one-seed smoke schema.

Claude review iteration 2 returned `VERDICT: AGREE`.  Phase 2 implementation
has run locally and passed focused tests and one-seed bootstrap smoke.  Phase 2
is pending Claude implementation/result review.  Phase 3 no-OT LEDH SIR smoke
subplan is drafted but not reviewed or executable yet.

Phase 0 must prove from local artifacts that SIR d18 DPF cells remain missing
and must preserve the no-free-theta and five-seed DPF value boundaries.

## Next Action

Claude review of the Phase 2 implementation/result packet returned
`VERDICT: REVISE`.  It found the SIR callback/smoke substance on contract, but
required two packet fixes: Phase 3 blocker handoff could not permit Phase 4,
and the Phase 2 code review packet needed explicit scope quarantine because the
touched code files contain older non-P8j churn.

Those issues were patched.  Claude read-only review iteration 2 returned
`VERDICT: AGREE`.  Phase 3 no-OT LEDH SIR smoke is now the active executable
gate.

Phase 3 local execution passed: focused SIR DPF tests passed and one-seed/N=4
no-OT LEDH smoke was finite.  Phase 3 result and Phase 4 OT-smoke subplan were
reviewed by Claude worker `p8j-phase3-result-phase4-subplan-review-iter1b`,
which returned `VERDICT: AGREE`.  Phase 4 OT-resampled LEDH SIR smoke is the
active executable gate.

Phase 4 local execution passed after a command-configuration repair.  The first
default-Sinkhorn attempt failed with `Sinkhorn row residual exceeded tolerance
envelope`; the repaired command used the inherited P8h settings
`epsilon=1.0`, `iterations=200`, `tolerance=1e-6` and produced a finite
one-seed/N=4 OT smoke.  Phase 4 result and Phase 5 particle-tuning subplan are
reviewed by Claude worker `p8j-phase4-result-phase5-subplan-review-iter1`,
which returned `VERDICT: AGREE`.  Phase 5 SIR particle-count tuning is the
active executable gate.

Phase 5 local tuning executed and blocked.  The P8j SIR tuning harness selected
no particle count.  Bootstrap DPF was finite at `N=16,32,64` but failed the MC
SE gate.  LEDH OT failed at seed `81120` for `N=16,32,64` with
`Sinkhorn row residual exceeded tolerance envelope`.  Phase 6 leaderboard
refresh is not authorized.  Phase 5 result and Phase 5b blocker-repair subplan
were reviewed by Claude worker
`p8j-phase5-result-phase5b-subplan-review-iter1`, which returned
`VERDICT: AGREE`.

Phase 5b local diagnostics executed.  Bootstrap higher-count diagnostics at
`N=128,256` remained finite and trusted-GPU but still failed MC SE.  LEDH OT
first-failure diagnostics showed a Sinkhorn cost-scale mismatch at the first
resampling event: cost mean `116.56402657134574`, cost max
`237.97475859459587`, nominal epsilon `1.0`.  A diagnostic-only
scale-adaptive probe with epsilon equal to cost mean and `500` iterations
produced finite first-event residuals.  Claude worker
`p8j-phase5b-result-phase5c-review-iter1b` reviewed the Phase 5b result and
Phase 5c scale-adaptive Sinkhorn repair subplan and returned
`VERDICT: AGREE`.  Phase 5c is the active executable gate.  Phase 6 leaderboard
refresh remains unauthorized.

Phase 5c local execution implemented an explicit opt-in scale-adaptive
Sinkhorn epsilon policy and ran trusted GPU LEDH OT diagnostics at `N=16,32`
with the five fixed seeds.  The repair fixed the nonfinite Sinkhorn blocker for
those rungs: both were finite, trusted-GPU, and transport-valid.  No count was
selected because MC SE remained high (`38.680160007903105` and
`41.269063039967556`).  Phase 5d larger-count subplan is drafted and pending
Claude read-only review.  Claude worker
`p8j-phase5c-result-phase5d-review-iter1` returned `VERDICT: AGREE`.  Phase 5d
is the active executable gate.  Phase 6 leaderboard refresh remains
unauthorized.

Phase 5d local execution ran the reviewed one-rung trusted-GPU adaptive LEDH OT
`N=64` probe with five fixed seeds.  The rung was finite and transport-valid,
but MC SE stayed high at `39.529955624675594` and runtime was `789.755664`
seconds.  Phase 5d therefore blocks `N=128` under the current budget and
drafts Phase 5e as a decision gate rather than another blind particle ladder.
Claude worker `p8j-phase5d-result-phase5e-review-iter1` returned
`VERDICT: AGREE`.  Phase 5e is the active executable decision gate.  Phase 6
leaderboard refresh remains unauthorized.

## Not Concluded

- SIR d18 DPF callback implementation exists locally and has passed P8j
  focused tests and Claude-bounded review.
- One-seed N=4 SIR d18 bootstrap, no-OT LEDH, and OT LEDH smokes exist from
  P8j.  Five-seed particle-count evidence exists for bootstrap and adaptive
  LEDH OT, but it remains blocked and selects no SIR d18 DPF count.
- A SIR d18 particle-count tuning result exists from P8j, but it is blocked:
  bootstrap failed MC SE and LEDH OT failed Sinkhorn residuals.  Phase 5b
  diagnosed the LEDH OT failure as a cost-scale/solver-configuration issue and
  identified a repair candidate requiring review.  Phase 5c repaired the LEDH
  OT execution failure for `N=16,32`, but LEDH OT remains MC-SE-blocked.
  Phase 5d shows `N=64` is still MC-SE-blocked and runtime-costly.
- No SIR d18 particle-count tuning has passed; no SIR d18 leaderboard refresh
  is authorized.
- No leaderboard refresh has occurred.
- No score, Hessian, theta-gradient, HMC, NUTS, source-faithful TT/SIRT, MATLAB
  parity, or production-readiness claim is made.
