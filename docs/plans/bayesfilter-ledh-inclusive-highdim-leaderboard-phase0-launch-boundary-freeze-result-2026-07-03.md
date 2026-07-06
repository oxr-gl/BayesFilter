# Phase 0 Result: Launch Boundary Freeze

Date: 2026-07-03

Status: `PASSED_PHASE0_BOUNDARY_FREEZE`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Launch the LEDH-inclusive highdim leaderboard program into Phase 1. |
| Primary criterion | Passed: baseline, row set, algorithm set, nonclaims, Claude review role, and repair loop are frozen in plan artifacts. |
| Veto diagnostics | Passed: no claim that LEDH already ran in the July 3 full leaderboard; no detached execution; no runtime cross-ranking in frozen-baseline mode; no score admission without total-derivative artifact. |
| Main uncertainty | Row-by-row LEDH same-target adapter availability is not yet known; this is the Phase 1 question. |
| Next justified action | Execute Phase 1 row admission and adapter inventory. |
| Not concluded | No LEDH value correctness, score correctness, all-model readiness, runtime superiority, HMC readiness, posterior correctness, or scientific superiority. |

## Frozen Baseline

The baseline artifact is:

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json`

This artifact explicitly excludes:

- `ledh_pfpf_alg1_ukf_current`;
- `ledh_pfpf_ot`.

It also states that LEDH/PFPF-OT and DPF transport rows are omitted from the
non-LEDH rebuild. Therefore it is a frozen non-LEDH baseline, not a LEDH run.

## Frozen Algorithms

The intended comparison algorithms are:

- `fixed_sgqf`;
- `ukf`;
- `zhao_cui_scalar_or_multistate`;
- `ledh_pfpf_ot`.

## Frozen Rows

Every requested row must appear in the final LEDH-inclusive artifact as full,
scoped, or blocked:

- `benchmark_lgssm_exact_oracle_m3_T50`;
- `zhao_cui_sv_actual_nongaussian_T1000`;
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`;
- `zhao_cui_spatial_sir_austria_j9_T20`;
- `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`;
- `zhao_cui_predator_prey_T20`;
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`.

## Comparator Mode

Default comparator mode is:

`frozen_non_ledh_baseline_plus_fresh_ledh`

In this mode:

- non-LEDH rows are copied from the July 3 baseline with provenance labels;
- LEDH rows are fresh artifacts from this program;
- value and score status may be compared by target and row scope;
- runtime cross-ranking between frozen non-LEDH rows and fresh LEDH rows is
  forbidden.

## LEDH Ladder Policy

Default LEDH ladder:

- seeds: `81120,81121,81122,81123,81124`;
- default rungs: `N=1000` and `N=10000`;
- optional high rung: `N=50000` only if pre-run budget and memory checks pass
  before row execution;
- any deviation requires a blocker or reviewed row-specific ladder before
  seeing results.

## Score Admission Policy

A LEDH row can be `executed_value_score` only if it has a row-specific artifact
showing the total derivative of the stated log likelihood target by:

- exact derivation;
- trusted same-target finite difference with fixed randomness;
- exact oracle.

Partial derivatives are not MLE/HMC score evidence.

## Checks Run

- Plan path existence check: passed.
- Baseline LEDH exclusion grep: passed.
- Required subplan-section grep: passed.
- `git diff --check` on plan artifacts: passed.
- Claude health probe: passed with `CLAUDE_PROBE_OK`.
- Claude bounded review round 1: `VERDICT: REVISE`.
- Plan patched for comparator provenance, ladder policy, score admission, and
  every-row inclusion.
- Claude focused review round 2: `VERDICT: AGREE`.

## Next-Phase Handoff

Phase 1 may begin. It must create a row admission ledger that records, for every
requested row:

- LEDH adapter availability;
- target computed by LEDH;
- full/scoped/blocked status;
- value status;
- score status;
- planned total-derivative score admission artifact or `blocked_score`.
