# P57-M9 Subplan: Spatial SIR Validation Ladder

metadata_date: 2026-06-11
status: PLAN_REVIEW_CONVERGED

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the repaired source route run and validate spatial SIR at d=18, then stress d=50/d=100 without overclaiming? |
| Baseline/comparator | Author SIR settings, lower-rung dense/exact rows, same-route rank ladder, UKF scout as diagnostic-only, memory budget from M7. |
| Primary pass criterion | d=18 uses the source-route pipeline and passes a declared comparator strategy before any correctness-style claim; d=50/d=100 are attempted only after d=18 passes and are labeled stress/scaling unless a reference strategy exists. |
| Veto diagnostics | d=18 uses local/operator/all-grid route; d=50/d=100 promoted to correctness from UKF or finite values; memory cap exceeded; no result manifest. |
| Not concluded | No universal high-dimensional correctness or HMC production readiness. |

## Tasks

1. Build lower-rung smoke rows first: scalar/two-step, reduced SIR sites, then
   paper d=18.
2. For d=18, use author state ordering, T=20, observation model, rank ladder,
   and preconditioning choices unless a fixed-HMC adaptation is documented.
3. Record value, gradient, replay, ESS, normalizer, rank, memory, and wall-time
   diagnostics.
4. Declare the exact d=18 claim tier before running:
   - `d18_correctness_candidate` requires same-target dense/reference evidence
     on a lower-rung or feasible same-target d=18 reference plus the M7
     tolerances;
   - `d18_same_route_rank_convergence` requires a strictly higher feasible
     fixed TT/SIRT rank comparator and cannot claim exact correctness;
   - `d18_execution_only` may report replay, ESS, finite values/gradients, and
     wall time, but cannot claim source-route accuracy.
5. Attempt d=50 only as scaling/self-convergence after d=18 passes at least
   `d18_same_route_rank_convergence`.
6. Attempt d=100 only as scout/preflight or bounded stress after d=50 passes.

## Required Checks

- targeted pytest for source-route and spatial SIR rows;
- run manifests with git status, CPU/GPU status, seeds/frozen draws, commands,
  wall time, and artifact paths.
- Claude review must verify d=50/d=100 claim boundaries.
