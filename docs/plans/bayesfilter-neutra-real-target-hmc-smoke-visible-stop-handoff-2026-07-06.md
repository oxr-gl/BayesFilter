# BayesFilter NeuTra Real Target HMC Smoke Visible Stop Handoff

Date: 2026-07-06

## Status

`CLOSED_BLOCKED_MISSING_PORTABLE_REAL_TARGET_AUTHORITY`

## Current Phase

Phase 5 terminal closeout passed final review.

## Current Evidence

- Prior c603 import/mechanics fixture program is closed.
- New real-target program planning artifacts have been drafted.
- Phase 0 local text checks passed.
- Phase 0 Claude read-only launch review returned `VERDICT=AGREE`.
- Phase 1 inventory classified the next boundary as `design_only`.
- Phase 1 local checks passed.
- Claude review became unavailable after a Phase 2-style probe timeout and
  direct tiny-probe timeout; a fresh Codex read-only substitute reviewer
  returned `VERDICT: AGREE`.
- Phase 2 source-anchor inspection found no safe portable real-target adapter
  implementation boundary in the current BayesFilter repo.
- The c603 preflight JSON names `rotemberg_second_order_svd_target_arrays.npz`,
  `rotemberg_second_order_svd_probe_cloud.npz`, and
  `rotemberg_second_order_svd_data.npz`, but those files are absent from the
  fetched handoff checkout.
- BayesFilter still lacks the c603 Rotemberg model/derivative builder,
  handoff custom-gradient wrapper symbol, and analytical prior callable.
- A Phase 2 blocker result and refreshed Phase 3 blocker-handoff subplan were
  reviewed by Claude with `VERDICT=AGREE`.
- Phase 3 blocker-handoff result passed substitute Codex read-only review after
  Claude review timed out.
- Phase 4 subplan has been refreshed as a no-entry HMC-smoke blocker.
- Phase 4 no-entry result local checks passed.
- Phase 5 closeout subplan has been refreshed for terminal close.
- Phase 5 closeout result passed final read-only review.
- The visible program is closed blocked on missing portable c603 real-target
  authority.
- No HMC, GPU, training, or package/environment mutation has been run.

## Stop Conditions To Preserve

Stop before GPU/CUDA jobs, training, long HMC sampling, package installation,
destructive git/filesystem action, git commit/push, default-policy change,
unreviewed target authority, or unsupported scientific/product claims.

## Resume Instructions

If interrupted, resume by reading:

1. `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-master-program-2026-07-06.md`
2. `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-visible-gated-execution-runbook-2026-07-06.md`
3. `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-visible-execution-ledger-2026-07-06.md`
4. the current phase subplan.

Then start a separate reviewed repair program before advancing to real-target
mechanics or HMC smoke.
