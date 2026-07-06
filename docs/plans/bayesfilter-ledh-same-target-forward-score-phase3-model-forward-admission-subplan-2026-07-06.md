# Phase 3 Subplan: Model Forward Scalar Admission

metadata_date: 2026-07-06
status: DRAFT_AFTER_PHASE2_LOCAL_CHECKS
master_program: docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md
phase: 3

## Phase Objective

Admit same-target finite-`N` LEDH observed-data likelihood estimators model by
model, before any new score implementation. The target scalar is the row
observed-data log likelihood or a reviewed finite-`N`, fixed-randomness LEDH
estimator of that same scalar.

## Entry Conditions Inherited From Previous Phase

- Phase 1 froze row target and theta contracts.
- The fixed spatial SIR row now uses `sir_log_scale_theta` with theta
  `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)` and truth theta
  `[0,0,0]`.
- Phase 2 added the forward contract:
  `target_scalar = observed_data_log_likelihood_estimator`.
- Phase 2 validation separates target densities
  `transition_log_density`, `observation_log_density` from proposal/flow terms
  `pre_flow_log_density`, `forward_log_det`, and
  `proposal_observation_surface`.
- The correction formula is:
  `transition_log_density + observation_log_density - pre_flow_log_density + forward_log_det`.
- The scoped parameterized SIR diagnostic remains
  `legacy_scoped_parameterized_sir_diagnostic` and cannot admit the fixed full
  SIR row.

## Required Artifacts

- Phase 3 result:
  `docs/plans/bayesfilter-ledh-same-target-forward-score-phase3-model-forward-admission-result-2026-07-06.md`
- Row-specific value-admission notes where a row is newly checked or repaired.
- Tiny fixed-randomness value artifacts for each candidate row.
- Trusted GPU/XLA value artifacts when a row claims production-target value
  execution.
- Refreshed Phase 4 subplan listing only rows admitted in Phase 3.
- Claude or fallback read-only review bundle for material row-admission
  decisions.

## Candidate Row Order

1. `benchmark_lgssm_exact_oracle_m3_T50`
   - Purpose: preserve the known same-target reference lane.
   - Comparator: exact Kalman observed-data log likelihood.
   - Expected status: value admitted if Phase 2 contract is present and the
     existing same-target value checks still pass.
2. `zhao_cui_spatial_sir_austria_j9_T20`
   - Purpose: admit the amended fixed SIR full row as a 3D log-scale
     model-parameter target.
   - Comparator: reviewed same-target callback decomposition and tiny
     fixed-randomness value consistency; no scoped diagnostic may substitute.
   - Expected status: value candidate only; score remains blocked.
3. `zhao_cui_sv_actual_nongaussian_T1000`
   - Purpose: establish exact target identity for the actual SV row.
   - Comparator: declared actual-SV row target and row-specific bridge.
   - Expected status: blocked unless a same-target LEDH adapter exists or is
     repaired.
4. `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`
   - Purpose: establish exact KSC finite-mixture surrogate row likelihood.
   - Comparator: `logsumexp` mixture likelihood checks.
   - Expected status: blocked unless an LEDH KSC adapter exists or is repaired.
5. `zhao_cui_predator_prey_T20`
   - Purpose: establish additive-Gaussian predator-prey row likelihood.
   - Comparator: row model transition/observation density checks and tiny
     fixed-randomness value execution.
   - Expected status: blocked unless current-route bridge is reviewed.
6. `zhao_cui_generalized_sv_synthetic_from_estimated_values`
   - Purpose: establish frozen generalized-SV source-row likelihood.
   - Comparator: frozen row target and reviewed generalized-SV adapter.
   - Expected status: blocked unless current-route bridge is reviewed.

## Required Checks/Tests/Reviews

- For every candidate row:
  - contract validation via `validate_ledh_forward_contract_manifest`;
  - evidence that the executed scalar is `log_likelihood` for the Phase 2
    observed-data target, not a proposal or flow objective;
  - finite tiny fixed-randomness value run or explicit unsupported/blocker note;
  - row-specific check of target transition/observation density callbacks.
- For LGSSM:
  - exact Kalman comparator remains the value reference.
- For fixed SIR:
  - theta metadata remains `sir_log_scale_theta`, dimension `3`;
  - source base formulas and log-scale parameter extension are identified
    separately;
  - scoped parameterized-SIR diagnostic is not used as full-row admission.
- For KSC:
  - mixture target uses explicit `logsumexp` finite-mixture likelihood checks.
- Trusted GPU/XLA commands are required for production-target GPU claims.
- Claude read-only review is required for material admission or blocker
  decisions; fallback Codex review is allowed if Claude is unavailable or
  policy-blocked.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which rows now have an admitted same-target LEDH observed-data likelihood estimator? |
| Baseline/comparator | Phase 1 target/theta contract, Phase 2 forward API, row reference likelihoods, and prior blocked evidence. |
| Primary criterion | A row is admitted only if the executed LEDH scalar is the row finite-`N` observed-data likelihood estimator or a reviewed constant-offset equivalent. |
| Veto diagnostics | Proposal/flow objective used as value; wrong row target; scoped SIR substituted for fixed full SIR; unreviewed callback bridge; finite output only; memory/runtime-only pass; target metadata missing. |
| Explanatory diagnostics | Variance, runtime, memory, compile behavior, callback traces, and historical route comparisons. |
| Not concluded | No score correctness, score admission, HMC readiness, posterior correctness, scientific superiority, or fair runtime ranking. |
| Artifact | Phase 3 result plus row-specific value-admission or blocker records. |

## Forbidden Claims/Actions

- Do not implement or promote score for any row in Phase 3.
- Do not rebuild the leaderboard.
- Do not admit candidate callbacks without row-specific same-target evidence.
- Do not use scoped parameterized SIR evidence as fixed SIR full-row evidence.
- Do not treat memory, runtime, compile success, or finite output as target
  correctness.
- Do not change row target definitions or pass/fail criteria after seeing
  results.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 only if the Phase 3 result contains:

- an explicit admitted-row list;
- an explicit blocked-row list with blocker reasons;
- artifact paths for every row decision;
- a statement that rows not admitted in Phase 3 remain score-blocked;
- a refreshed Phase 4 subplan that lists only admitted rows as eligible for
  manual no-tape score implementation.

## Stop Conditions

Stop for a row if its target scalar is wrong, unsupported, or not checked.
Continue to other independent rows when safe, but do not silently promote the
blocked row.

Stop the phase if a required admission would require a human boundary change:
target redefinition, pass/fail criterion change, package/network fetch,
destructive filesystem/git action, or default backend/product-policy change.
