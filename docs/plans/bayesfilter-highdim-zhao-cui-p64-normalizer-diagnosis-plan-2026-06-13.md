# P64 Plan: Zhao-Cui Normalizer And Log-Marginal Diagnosis

metadata_date: 2026-06-13
status: CREATED_FOR_EXECUTION
executor: Codex
reviewer: none unless explicitly requested
predecessor: docs/plans/bayesfilter-highdim-zhao-cui-p63-source-fit-data-repair-result-2026-06-13.md

## Objective

Localize and repair, if appropriate, the remaining P60 d=18 blocker after P63:
large same-route low/high-rank deltas in log marginal likelihood and normalizer
increments.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the remaining P60 blocker caused by a normalizer convention bug, by defensive-mixture accounting, or by genuine fixed-route rank/capacity instability? |
| Baseline/comparator | `full_sol.m:84-120`: `logfun_post = fun_into_sirt(..., L*x + mu, const) - log(abs(det(L)))`; update `logmarginal_likelihood += log(sirt.z) - const`. |
| Primary criterion | A targeted diagnostic separates `sqrt_square_normalizer`, defensive-mixture normalizer, shift constant, determinant contribution, pointwise density deltas, and P60 increments for low/high rows. |
| Veto diagnostics | Do not weaken P60 thresholds; do not return to artificial fit data; do not claim d=18 correctness from a smoke diagnostic; do not change fixed-HMC branch determinism. |
| Explanatory diagnostics | low/high `log_transport_normalizer`, `log_sqrt_square_normalizer`, `log_defensive_mixture_normalizer`, shift constants, log determinant, target/proposal/correction ranges. |
| Nonclaims | No paper-scale spatial SIR success, no d=50/d=100, no adaptive Zhao-Cui parity, no `AlgebraicMapping(1)` parity. |

## Skeptical Pre-Execution Audit

status: PASSED_FOR_DIAGNOSTIC_FIRST

The plan answers the current blocker directly and does not treat proxy density
agreement as correctness. It records source anchors and preserves P63 fit-data
mode. If the diagnostic finds a convention bug, patch it narrowly and rerun
focused tests. If it finds capacity instability only, record that as a blocker
instead of inventing a non-source fix.

## Steps

0. Mandatory micro-gate before any repair:
   - run one normalizer decomposition diagnostic;
   - record low/high `sqrt_square_normalizer`, defensive-mixture normalizer,
     transport `log_normalizer`, shift constants, determinant terms, and P60
     increments;
   - do not stop after plan text or hypothesis text alone.
1. Trace author normalizer convention against current `SourceRouteTarget`,
   `FixedTTSIRTTransport`, and `SquaredTTDensity`.
2. Add or run a bounded diagnostic that reports normalizer terms separately.
3. Patch only if the diagnostic identifies a convention mismatch.
4. Rerun focused tests and d=18 comparator.
5. Write P64 result artifact.

## Binding Stop Rule

This phase may stop only after one of the following artifacts exists:

- a diagnostic-backed code patch plus verification and d=18 rerun; or
- a diagnostic-backed no-patch result classifying the remaining blocker as
  rank/capacity or bounded-domain instability.

Plan creation, source reading, or an untested hypothesis is not a valid stop
condition.
