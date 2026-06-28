# Actual-SIR Nystrom Stability Repair Visible Stop Handoff

Date: 2026-06-23

Status: `REPAIR_FAILED_OR_BLOCKED`

## Current Phase

`P07_CLOSEOUT`

## Last Completed Phase

`P06_REPAIR_GATE_FAILED`

## Active Blocker

The opt-in `positive_projected` Nystrom kernel diagnostic made the first known
failing row finite and residual-valid, but it failed the predeclared paired
max log-likelihood threshold.

Hard veto:

- `paired:paired_log_likelihood_max_abs_delta`
- observed max delta: `12.91107177734375`
- threshold: `10.0`

Required artifact:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p06-p09-regate-decision-result-2026-06-23.md`
- `docs/benchmarks/actual-sir-nystrom-stability-repair-p06-positive-projected-r32-eps0p25-2026-06-23.json`

## Program Outcome

`REPAIR_FAILED_OR_BLOCKED`

P09/P10 must not be reopened from this repair attempt.

The result separates two facts:

- finite numerical rescue evidence: `positive_projected` produced finite
  factors/particles and residuals below threshold on `rank=32,epsilon=0.25`;
- repair acceptance failure: paired max log-likelihood delta exceeded the
  predeclared threshold.

## Required Next Action

Do not launch another experimental phase without a new reviewed subplan.

Reasonable next reviewed paths:

- fixed-policy closeout around `rank=32,epsilon=0.5`, explicitly recording the
  unsupported brittle neighborhood; or
- a new repair plan for a less intrusive stabilization that preserves paired
  comparability on the same `rank=32,epsilon=0.25` row before attempting broader
  P09/P10 gates.

## Nonclaims

- No default readiness is established.
- No repair success is established.
- No broad Nystrom robustness or unusability claim is established.
- No statistical ranking, posterior correctness, dense Sinkhorn equivalence,
  scalable/high-N readiness, or HMC readiness is established.
