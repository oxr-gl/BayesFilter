# Phase 4 Claude Micro Review: Threshold And Source Route Repair

Date: 2026-06-17
Review timestamp: 2026-06-18T00:49:52+08:00

## Scope

Read-only no-file micro review of the repaired Phase 4 claims after Claude
round 01 requested:

- concrete Phase 4 dense-reference/residual thresholds;
- sharper separation between paper/source-faithful Nystrom operations and
  BayesFilter-specific adapter operations.

Claude did not inspect files, edit files, run commands, or authorize phase
advancement.  Codex remains supervisor and executor.

## Repaired Claims Reviewed

Threshold gate:

- `PHASE_4_NYSTROM_PROTOTYPE_PASSED` requires hard transport-validity vetoes
  and dense-reference viability thresholds to pass.
- If hard validity vetoes pass but dense-reference viability thresholds fail,
  the result status must be
  `PHASE_4_NYSTROM_PROTOTYPE_COMPLETED_CANDIDATE_NOT_PROMOTED`, not `PASSED`.
- Hard veto thresholds include finite outputs/factors/residuals/errors,
  particle shape matching the dense baseline, and row/column residuals
  `<= 5e-2` for every fixture/rank record.
- Promotion thresholds require at least one tested rank for each of
  `tiny_manual`, `small_parity`, and `high_dim_low_rank` to have
  dense-reference max error `<= 5e-2` and RMS error `<= 2e-2`.
- `high_dim_locality` dense-reference error is explanatory/repair-trigger only
  in Phase 4.
- Runtime and memory are explanatory only.

Source-route separation:

- `source_faithful` applies only to paper/source-anchored Nystrom Gaussian
  factors `V`, `A`, `V A^{-1} V^T`, Cholesky/triangular-solve matvec
  preserving `A^{-1}`, and low-rank Sinkhorn scaling through factors.
- Local FilterFlow scaling, annealing schedule, cost-normalization adapter,
  epsilon/reg/sigma/eta adapter, deterministic landmarks, jitter, and schedule
  freezing must be classified separately as `fixed_hmc_adaptation` or
  `extension_or_invention`.
- The result must not call the entire prototype `source_faithful` unless it
  also states which adapter pieces are not paper-source-faithful.

Non-claims:

- No speedup, ranking, production/default-readiness, posterior correctness, or
  general scalability claim is made from Phase 4.

## Claude Findings

Claude found that:

- the threshold-gate repair separates hard validity vetoes from
  promotion/viability thresholds;
- the repaired status logic prevents a valid-but-not-promoted Nystrom candidate
  from being marked `PASSED`;
- `high_dim_locality`, runtime, and memory remain explanatory-only;
- source-route separation now restricts `source_faithful` to anchored Nystrom
  factorization/matvec/scaling operations and labels adapters separately;
- no new material boundary problem was introduced.

Claude noted one mild editorial caution: when reporting Phase 4, apply status
logic at the aggregate phase level and hard vetoes at the fixture/rank record
level.

## Verdict

`VERDICT: AGREE`

## Codex Decision

This micro review resolves the Round 01 material issues for purposes of the
Phase 4 precheck.  It is review-convergence evidence only, not authorization;
Codex must still enforce the subplan, local checks, and human-required
boundaries during implementation.
