# P57-M11 Subplan: Integration Closeout

metadata_date: 2026-06-11
status: PLAN_REVIEW_CONVERGED

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can P57 declare the repaired fixed Zhao-Cui source route complete for its scoped claims? |
| Baseline/comparator | P57 M0-M10 results, tests, manifests, source-anchor ledgers, Claude reviews. |
| Primary pass criterion | All phases required for the declared claim have pass tokens; scoped blockers may only narrow the final claim, not silently satisfy prerequisites; remaining gaps are classified without adaptive parity/S&P/smoothing noise. |
| Veto diagnostics | Missing phase result; failed Claude source review; source-route blockers hidden as future work; d=18 claim made without M9 pass; old UKF/rank route promoted. |
| Not concluded | Anything outside the final declared scope. |

## Tasks

1. Build a decision table separating engineering correctness, numerical
   validity, and scientific/source-faithfulness claims.
2. Summarize passed phases, blocked phases, tests, manifests, and remaining
   non-goals.
3. Record whether BayesFilter can claim: fixed source-route substrate, d=18
   spatial SIR, d=50/d=100 stress, HMC readiness.
4. Apply this claim-to-phase gate matrix:
   - `fixed_source_route_substrate` requires P57-M0 through P57-M6 pass.
   - `source_faithful_rank_policy` requires P57-M7 pass in addition to M0-M6.
   - `preconditioned_spatial_sir_route` requires P57-M8 pass in addition to
     M0-M7.
   - `d18_spatial_sir_same_route_rank_convergence` requires P57-M9 pass at the
     corresponding claim tier plus M0-M8 pass.
   - `d18_spatial_sir_correctness_candidate` requires P57-M9 pass with its
     comparator strategy, not execution-only diagnostics.
   - `d50_or_d100_scaling_stress` requires the relevant M9 stress rows and may
     not be phrased as correctness unless a reviewed reference strategy exists.
   - `HMC_readiness` is not claimable from P57 unless a separate reviewed HMC
     tier gate is added.
5. Run final Claude read-only review.
6. Write closeout result.

## Required Checks

- `pytest` only over changed/highdim targeted tests unless a broader suite is
  explicitly planned.
- `git diff --check` over changed files.
- Claude final review must compare the closeout against source anchors and
  phase results.
