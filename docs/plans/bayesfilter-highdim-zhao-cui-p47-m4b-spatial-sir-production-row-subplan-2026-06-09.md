# P47-M4b Subplan: Spatial SIR Production Row Repair

metadata_date: 2026-06-09
phase: P47-M4b
status: `EXECUTED_PRELIGHT_BLOCKED_REVIEW_PENDING`

## Purpose

Try to repair `PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING` without
promoting the lower-rung M4a row.  The current all-axes retained-grid
Zhao--Cui route must pass a route-complexity preflight before any near-paper
J=9 run is attempted.

## Prerequisites

- `PASS_P47_M2_PAPER_SCALE_READINESS`
- `PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY`
- M1 route label: `documented-deviation fixed-design substitute`
- S&P 500 reproduction remains out of scope.

## Evidence Contract

Question: can the current P46/P47 fixed-design multistate route support a
production or near-paper-scale spatial SIR row while preserving the M4a target
family and target identity?

Primary pass criterion: a production or near-paper-scale spatial SIR row runs
under declared resource caps, preserves the M4a target family and route label,
reports observed infectious and unobserved susceptible filtering errors, and
satisfies the reviewed tolerance.

Preflight criterion: before running a ladder candidate, compute
`grid_points = order^(2J)` and
`pairwise_transition_evaluations = grid_points^2` for the all-axes retained-grid
route.  If the candidate exceeds the declared CPU pairwise-transition cap, the
candidate is blocked as `BLOCKED_M4B_ROUTE_ARCHITECTURE`; do not run it.

## Ladder

| Candidate | Sites J | State Dim | Horizon | Order | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| M4b-0 | 3 | 6 | 2 | 3 | replay prior feasibility row; already below near-paper |
| M4b-1 | 5 | 10 | 2 | 3 | route preflight; expected to expose all-grid scaling |
| M4b-2 | 9 | 18 | 25 | 3 | near-paper candidate; run only if preflight passes |

Resource caps:

- maximum CPU pairwise-transition evaluations per candidate:
  `50_000_000`;
- maximum wall time per candidate: `3600` seconds;
- maximum retained storage: `16` GB;
- one ladder axis changes at a time unless a reviewed amendment says otherwise.

## Veto Diagnostics

- target changes from the M4a additive-Gaussian closure without amendment;
- observed-only filtering error is presented as full-state accuracy;
- negative-state domain policy changes from `diagnose_negative_after_noise`;
- finite production output is promoted as correctness;
- a J=9 run is attempted after preflight veto;
- S&P 500 data or claims appear.

## Expected Outcomes

Expected current-route outcome:

```text
BLOCKED_M4B_ROUTE_ARCHITECTURE
```

That blocker is acceptable if it is reviewed, because it is a truthful route
architecture limitation rather than a production filtering pass.

## Initial Execution Result

The preflight gate blocked the current retained-grid route before a near-paper
run:

- J=3, order 3 has `3^(2J) = 729` grid points and about `531441` pairwise
  transition evaluations, so it remains a below-near-paper feasibility row.
- J=5, order 3 has `59049` grid points and about `3.49e9` pairwise transition
  evaluations, exceeding the CPU cap of `50_000_000`.
- J=9, order 3 has `387420489` grid points and about `1.50e17` pairwise
  transition evaluations, exceeding the CPU cap by many orders of magnitude.

Decision: record `BLOCKED_M4B_ROUTE_ARCHITECTURE`; do not emit
`PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING`.

Production pass token, only if all criteria pass:

```text
PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING
```
