# P60-1 Subplan: Source Rank Knobs And Comparator Contract

metadata_date: 2026-06-12
status: PLAN_CREATED_NOT_EXECUTED

## Question

Which Zhao-Cui source-code knobs define the author-SIR rank route, and what
exact comparator contract is needed before BayesFilter may claim same-route
rank convergence?

## Tasks

1. Re-read and cite the author SIR source anchors:
   - `eg3_sir/mainscript.m`;
   - `models/full_sol.m`;
   - any TTIRT/TTSIRT option files used by the author row.
2. Extract source facts:
   - state dimension, target dimension, horizon, sample count, rank settings,
     polynomial basis settings, ESS/recentering behavior, and correction
     formula;
   - which quantities are author facts versus fixed-HMC variant choices.
3. Define the same-route comparator contract:
   - same observations and target;
   - same generic Zhao-Cui `full_sol` ordering `[theta, x_t, x_{t-1}]`;
   - for this author SIR row, `d=0`, so theta is an empty block and the
     realized 36D route is `[x_t, x_{t-1}]`;
   - same route ordering and previous-marginal semantics;
   - lower-rank candidate versus strictly stronger feasible comparator;
   - frozen diagnostics/probes where needed for deterministic testing.
4. Define pass/fail tolerances for rank convergence before running the
   comparator.  Tolerances must include log marginal likelihood, normalizer
   increments, proposal-correction diagnostics, retained/probe density deltas,
   and replay validity.
5. Record memory and runtime bounds before execution.

## Pass Criteria

`PASS_P60_1_SOURCE_RANK_COMPARATOR_CONTRACT` requires a result artifact that
lists:

- source anchors with line references;
- author-code facts versus fixed-variant choices;
- comparator configurations;
- declared tolerances;
- veto diagnostics;
- planned artifact paths.

## Vetoes

- comparator contract relies on UKF, memory, or finite values as correctness;
- 18D target is used for source-route reapproximation instead of the realized
  36D `[x_t, x_{t-1}]` target;
- old all-grid/local route is allowed;
- tolerances are chosen after looking at the comparator result;
- fixed-variant choices are described as author-code facts.

## Token

`PLAN_P60_1_SOURCE_RANK_COMPARATOR_CONTRACT`
