# Actual-SIR Nystrom Less-Intrusive Stability Visible Stop Handoff

Date: 2026-06-23

Status: `CLOSED_REPAIR_FAILED_OR_RESTRICT_POLICY`

## Current Phase

`P07_CLOSEOUT_COMPLETE`

## Last Completed Phase

`P07_CLOSEOUT`

## Active Blocker

None.

## Final Result

The opt-in balanced Sinkhorn scaling gauge-normalization repair was implemented
and mechanically validated, but it failed the first serious trusted GPU brittle
row.  The P04 Nystrom candidate produced nonfinite log likelihood, factors, and
particles at `rank=32,epsilon=0.25`, `N=1024`, `T=20`, seeds `81920..81924`,
with `--nystrom-kernel-mode raw` and
`--nystrom-scaling-normalization balanced`.

This is a valid repair-candidate failure, not a harness or trusted-GPU artifact
failure.  The streaming comparator passed, GPU1/TF32 evidence was present, and
the selected repair metadata was recorded.

P05 was skipped by the predeclared stop-on-hard-veto logic after P04 failed.

## Result Artifacts

- P07 closeout:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p07-closeout-result-2026-06-23.md`
- P06 classification:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p06-promotion-readiness-decision-result-2026-06-23.md`
- P04 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p04-brittle-row-repair-gate-result-2026-06-23.md`
- P04 JSON:
  `docs/benchmarks/actual-sir-nystrom-less-intrusive-stability-p04-r32-eps0p25-2026-06-23.json`
- P04 Markdown:
  `docs/benchmarks/actual-sir-nystrom-less-intrusive-stability-p04-r32-eps0p25-2026-06-23.md`
- P04 log:
  `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p04-r32-eps0p25-2026-06-23.log`

## Claude Review Trail

- P00 R1: `VERDICT: REVISE`
- P00 R2: `VERDICT: AGREE`
- P02 R1: `VERDICT: REVISE`
- P02 R2: `VERDICT: AGREE`
- P03 implementation R1: `VERDICT: AGREE`

Claude was read-only reviewer only.

## Tests And Benchmarks Run

- P01 focused CPU-hidden tests:
  `10 passed, 14695 warnings in 22.87s`.
- P03 focused CPU-hidden tests:
  `13 passed, 15109 warnings in 30.10s`.
- P04 trusted GPU benchmark:
  status `FAIL`, hard vetoes
  `nystrom:nonfinite_log_likelihood`,
  `nystrom:nonfinite_nystrom_factors`,
  `nystrom:nonfinite_nystrom_particles`.

## Unresolved Blockers

None for this lane.  The repair candidate failed; the lane is closed.

## What Was Not Concluded

- No default readiness is established.
- No statistical ranking or superiority is established.
- No posterior correctness is established.
- No dense Sinkhorn equivalence is established.
- No scalable/high-N readiness is established.
- No HMC readiness is established.
- No broad claim that all Nystrom variants are unusable is established.

## Safest Next Human Decision

Choose a separate next program:

1. fixed-policy validation around the known viable `rank=32,epsilon=0.5`
   setting, explicitly restricting brittle nearby settings; or
2. a new numerical-method repair lane for a more substantive low-rank-kernel
   stabilization/replacement.

Do not silently continue this closed lane into either path.
