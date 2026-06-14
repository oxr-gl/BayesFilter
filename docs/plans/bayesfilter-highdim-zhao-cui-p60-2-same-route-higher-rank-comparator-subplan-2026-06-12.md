# P60-2 Subplan: Same-Route Higher-Rank Comparator

metadata_date: 2026-06-12
status: PLAN_CREATED_NOT_EXECUTED

## Question

Does the d=18 author-SIR source-route result remain stable when compared
against a strictly stronger feasible fixed-TT/SIRT approximation on the same
Zhao-Cui `full_sol` route, whose realized author-row target is the 36D
`[x_t, x_{t-1}]` object because `d=0`?

## Preconditions

- P59-9e has `PASS_P59_9E_D18_EXECUTION_ONLY`.
- P60-1 has `PASS_P60_1_SOURCE_RANK_COMPARATOR_CONTRACT`.
- Comparator tolerances are fixed before execution.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Baseline | Current d=18 execution-only source-route run from P59-9e, rerun through the same route. |
| Comparator | Strictly stronger same-route fixed-TT/SIRT run, with higher feasible rank or otherwise documented stronger approximation under the P60-1 contract. |
| Primary criterion | Declared rank-convergence tolerances pass for log marginal likelihood, normalizer increments, correction diagnostics, and retained/probe density summaries. |
| Veto diagnostics | Source-route drift, missing previous marginal, nonfinite values, ESS/correction collapse outside declared veto bounds, memory forecast breach, unfair frozen-draw/probe mismatch, old route, synthetic transport, or UKF correctness substitution. |
| Not concluded | Same-route rank convergence is not exact correctness and does not launch d=50/d=100. |

## Tasks

1. Add or reuse runner configuration for baseline and higher-rank comparator.
2. Keep the realized 36D `[x_t, x_{t-1}]` target, observations, source route,
   previous-marginal semantics, and correction formula identical across rows.
3. Record the rank/basis/sample settings and memory forecast for each row.
4. Run the baseline and comparator under the predeclared contract.
5. Emit a JSON/Markdown result with:
   - status token;
   - command manifest;
   - git commit and dirty-worktree note;
   - CPU/GPU status;
   - seeds/frozen draws/probes;
   - log marginal likelihood and normalizer increment deltas;
   - correction-log-weight ranges;
   - ESS summaries;
   - probe-density deltas;
   - veto status and nonclaims.

## Pass Criteria

`PASS_P60_D18_SAME_ROUTE_RANK_CONVERGENCE` requires all primary comparator
tolerances and veto diagnostics to pass.

## Block Criteria

`BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE` is required if:

- no strictly stronger same-route comparator can be run within the declared
  memory/runtime budget;
- comparator tolerances fail;
- the comparator route differs from Zhao-Cui `full_sol`;
- diagnostics pass only because tolerances were loosened after seeing results.

## Token

`PLAN_P60_2_SAME_ROUTE_HIGHER_RANK_COMPARATOR`
