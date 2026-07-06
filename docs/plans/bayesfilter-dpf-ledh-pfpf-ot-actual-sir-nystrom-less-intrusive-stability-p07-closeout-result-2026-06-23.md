# P07 Closeout Result

Date: 2026-06-23

Status: `CLOSED_REPAIR_FAILED_OR_RESTRICT_POLICY`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Close the less-intrusive balanced-scaling repair lane as a valid candidate failure | `PASS`: completed artifacts and stop handoff preserve phase outcomes and nonclaims | `PASS`: no missing completed-phase artifact, unsupported default claim, threshold drift, or ledger/stop-handoff mismatch after local check | A different future repair family may exist, but this lane did not identify a bounded automatic continuation | Human/reviewed choice between fixed-policy validation around `rank=32,epsilon=0.5` or a new numerical-method repair lane | No default readiness, no superiority, no posterior correctness, no HMC readiness, no broad Nystrom unusability claim |

## What This Lane Established

- P00/P02/P03 review loops converged with Claude read-only review where
  required.
- P01 added/verified missing compiled-row denominator diagnostics without
  changing raw default behavior.
- P02 selected exactly one less-intrusive repair family: opt-in balanced
  Sinkhorn scaling gauge normalization.
- P03 implemented that repair mechanically, with default `none` preserved and
  focused tests passing:
  `13 passed, 15109 warnings in 30.10s`.
- Claude P03 implementation review returned `VERDICT: AGREE`.
- P04 ran the serious trusted GPU brittle row on physical GPU1 with raw kernel
  plus balanced scaling:
  `rank=32,epsilon=0.25`, `N=1024`, `T=20`, seeds `81920..81924`.
- P04 failed hard-veto screen:
  `nystrom:nonfinite_log_likelihood`,
  `nystrom:nonfinite_nystrom_factors`,
  `nystrom:nonfinite_nystrom_particles`.
- P05 was skipped by predeclared stop-on-hard-veto logic.
- P06 classified the result as a valid repair-candidate failure, not a harness
  invalidation.

## Artifact Index

Program/runbook:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-master-program-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-visible-gated-execution-runbook-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-visible-execution-ledger-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-claude-review-ledger-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-visible-stop-handoff-2026-06-23.md`

Phase results:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p00-program-review-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p01-diagnostic-adequacy-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p02-repair-selection-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p03-focused-implementation-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p04-brittle-row-repair-gate-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p06-promotion-readiness-decision-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p07-closeout-result-2026-06-23.md`

P04 benchmark artifacts:

- `docs/benchmarks/actual-sir-nystrom-less-intrusive-stability-p04-r32-eps0p25-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-less-intrusive-stability-p04-r32-eps0p25-2026-06-23.md`
- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p04-r32-eps0p25-2026-06-23.log`

Claude review logs:

- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p00-claude-review-r1-2026-06-23.log`
- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p00-claude-review-r2-2026-06-23.log`
- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p02-claude-review-r1-2026-06-23.log`
- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p02-claude-review-r2-2026-06-23.log`
- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p03-claude-review-r1-2026-06-23.log`

Focused test logs:

- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p01-focused-tests-2026-06-23.log`
- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p03-focused-tests-2026-06-23.log`

## Nonclaims

- This lane does not establish default readiness.
- This lane does not establish statistical superiority or ranking.
- This lane does not establish posterior correctness.
- This lane does not establish dense Sinkhorn equivalence.
- This lane does not establish scalable/high-N readiness.
- This lane does not establish HMC readiness.
- This lane does not prove that all Nystrom variants are unusable.

## Safest Next Human Decision

Choose a separate next program:

1. Fixed-policy validation around the known viable `rank=32,epsilon=0.5`
   setting, explicitly treating nearby brittle settings as excluded until
   repaired.
2. A new numerical-method repair lane for a more substantive low-rank-kernel
   stabilization/replacement, with a fresh reviewed master program.

This closed lane should not silently continue into either path.

## Local Closeout Check

Required local closeout check: `PASS`.

The check verified that completed-phase results and P04 benchmark artifacts
exist, final status is consistent across P07/ledger/stop handoff, P05 skip is
recorded, and forbidden default-readiness/superiority/HMC claims are absent.
