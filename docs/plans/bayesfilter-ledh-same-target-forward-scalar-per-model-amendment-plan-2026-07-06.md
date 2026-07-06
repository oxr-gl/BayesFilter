# LEDH Same-Target Forward Scalar Per-Model Amendment Plan

Date: 2026-07-06

Status: `DRAFT_PER_MODEL_FORWARD_SCALAR_REPAIR_PLAN`

Supersedes for planning purposes only:

- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase3-model-forward-admission-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase3-model-forward-admission-result-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase3-remaining-row-forward-blockers-result-2026-07-06.md`

This amendment does not invalidate the two rows already admitted for value
under the prior Phase 3 result. It fixes the planning error that bundled
several different model-row repairs into one phase and allowed metadata,
callback presence, or old blocked evidence to stand too close to admission
evidence.

## Objective

Build and admit the same-target LEDH forward scalar for every intended
high-dimensional LEDH model row, one model row at a time, before any score work
resumes.

The target forward scalar is the row observed-data log likelihood estimator:

```text
observed_data_log_likelihood_estimator
```

reported as:

```text
log_likelihood
```

with LEDH correction:

```text
transition_log_density
+ observation_log_density
- pre_flow_log_density
+ forward_log_det
```

This is the log likelihood function for the row target, or the finite-`N`,
fixed-randomness LEDH estimator of that log likelihood. It is not the LEDH flow
objective, proposal density, transport objective, surrogate observation
surface, memory result, runtime result, or callback-existence result.

## Current State

The current code already has the right metadata vocabulary in
`bayesfilter/highdim/ledh_forward_contract.py`:

- target scalar: `observed_data_log_likelihood_estimator`;
- output field: `log_likelihood`;
- target density fields: `transition_log_density`, `observation_log_density`;
- proposal/flow correction fields: `pre_flow_log_density`, `forward_log_det`.

But that module explicitly says these contracts are metadata-only and do not
admit a row. The failed planning pattern was treating valid metadata or legacy
callbacks as if they were executable same-target scalar admission evidence.

Current model state:

| Row | Current state |
| --- | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | Value admitted; use as golden schema/template. |
| `zhao_cui_spatial_sir_austria_j9_T20` | Value admitted with amended `sir_log_scale_theta`; use as high-dimensional nonlinear template with explicit nonclaims. |
| `zhao_cui_predator_prey_T20` | Callback exists; no current streaming same-target LEDH admission artifact. |
| `zhao_cui_sv_actual_nongaussian_T1000` | Callback exists with raw target/log-square flow split; no current streaming same-target admission artifact. |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | Callback exists with raw target/log-square flow split; no current streaming same-target admission artifact. |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | KSC non-LEDH value routes exist; no KSC-specific LEDH route. |

## Skeptical Plan Audit

| Risk | Control |
| --- | --- |
| Wrong baseline | Start from the Phase 1 target/theta contracts, Phase 2 forward contract, and Phase 3 admitted/blocked result. |
| Metadata promoted as evidence | Every row phase must emit an executable artifact with finite `log_likelihood`; metadata-only contracts are blockers, not admission. |
| Callback promoted as evidence | Existing callbacks are source material only; each row needs a current runner artifact. |
| Proposal scalar promoted | Admission validator must reject proposal/flow objectives and require target density correction fields. |
| Actual-SV/KSC mixing | Actual SV and KSC get separate phases, separate target policies, and rejection tests against artifact borrowing. |
| Score before scalar | No score implementation, score test, memory score gate, or leaderboard score status can change in this amendment. |
| Runtime/memory proxy | Runtime, compile time, finite output, and memory are explanatory unless the same-target scalar identity passes. |
| Hidden row-target change | Each row freezes target, observations, theta, flow observation policy, and target observation density before execution. |

Audit status: passed for writing this amendment plan. Execution must still
begin with Phase 0 checks.

## Program Dependency Order

The correct order is:

1. shared admission guard;
2. shared runner schema;
3. LGSSM golden template;
4. fixed SIR amended high-dimensional template;
5. predator-prey additive-Gaussian nonlinear row;
6. actual SV raw-target/log-square-flow row;
7. generalized SV raw-target/log-square-flow row;
8. KSC surrogate row;
9. integration/leaderboard value rebuild.

KSC is last because it lacks a KSC-specific LEDH route. Actual SV and
generalized SV precede it because they share the existing non-Gaussian
flow-adapter pattern and can harden the target-vs-flow guard before the KSC
route is added.

## Phase 0: Baseline And Admission Guard

### Objective

Freeze the current state and add a strict rule: no model row is admitted for
the same-target forward scalar unless an executable artifact reports
`log_likelihood` from the row target correction.

### Entry Conditions

- Existing Phase 3 result admits value for LGSSM and fixed SIR only.
- Four remaining rows are blocked for value and score.
- No score work is in scope.

### Required Artifacts

- `docs/plans/bayesfilter-ledh-forward-scalar-amendment-phase0-baseline-result-2026-07-06.md`
- Optional validator tests if missing:
  `tests/highdim/test_ledh_forward_scalar_admission_guard.py`

### Steps

1. Read the Phase 3 result and remaining-row blocker result.
2. Record the admitted rows and blocked rows exactly.
3. Define admission status values:
   - `metadata_only_blocked`;
   - `tiny_executed_not_full_row`;
   - `n10000_same_target_value_admitted`;
   - `blocked_missing_current_runner`;
   - `blocked_wrong_target`;
   - `blocked_nonfinite`.
4. Add or tighten tests so metadata-only manifests cannot set
   `n10000_same_target_value_admitted`.
5. Add or tighten tests so a proposal scalar name cannot appear as
   `target_scalar`.
6. Add or tighten tests so a row without `log_likelihood_by_seed` cannot be
   admitted.
7. Write the Phase 0 result.

### Required Checks

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py -q
```

Run any new admission-guard test added in this phase.

### Evidence Contract

The phase passes only if tests distinguish:

- contract exists;
- tiny scalar executed;
- full N=10000 same-target scalar admitted.

### Forbidden Claims/Actions

- Do not admit a new row.
- Do not run long GPU benchmarks.
- Do not implement model-specific adapters.
- Do not touch score code.

### Handoff Conditions

Phase 1 may begin only if the result records the exact admitted/blocked
baseline and the admission guard is tested.

### Stop Conditions

Stop if the current tests or artifacts cannot distinguish metadata-only from
executed scalar evidence.

## Phase 1: Shared Forward Scalar Runner Schema

### Objective

Standardize the executable artifact schema every model-specific phase must
emit.

### Entry Conditions

Phase 0 baseline and admission guard passed.

### Required Artifacts

- `docs/plans/bayesfilter-ledh-forward-scalar-amendment-phase1-runner-schema-result-2026-07-06.md`
- Shared schema helper or validator, if not already sufficient.
- Schema tests.

### Steps

1. Define the common runner input contract:
   - `row_id`;
   - frozen observations;
   - frozen theta;
   - flow observation transform;
   - target observation density callback;
   - transition density callback;
   - LEDH transport settings;
   - seed list;
   - particle count;
   - horizon.
2. Define the common output artifact:
   - `schema_version`;
   - `row_id`;
   - `forward_contract`;
   - `target_scalar`;
   - `target_output_tensor_field`;
   - `target_density_fields`;
   - `proposal_flow_fields`;
   - `correction_formula`;
   - `theta_values`;
   - `theta_coordinate_system`;
   - `flow_observation_policy`;
   - `target_observation_policy`;
   - `target_density_used_for_correction`;
   - `log_likelihood_by_seed`;
   - `average_log_likelihood_by_seed`;
   - finite checks;
   - ESS summaries;
   - runtime/device metadata;
   - `admission_status`;
   - nonclaims.
3. Add schema validation rejecting:
   - missing `log_likelihood_by_seed`;
   - empty seed list;
   - missing target density fields;
   - proposal objective in target field;
   - `target_density_used_for_correction != true`;
   - flow/target transform ambiguity.
4. Add a tiny dummy-Gaussian schema test that intentionally tries to swap flow
   and target fields and must fail.
5. Write the Phase 1 result.

### Required Checks

Run the new schema tests plus the Phase 0 checks.

### Evidence Contract

The phase passes if every later row phase has one schema to target and the
schema makes wrong-scalar admission impossible.

### Forbidden Claims/Actions

- Do not claim any model row admission from schema validation alone.
- Do not run N=10000 model jobs.
- Do not implement scores.

### Handoff Conditions

Phase 2 may begin only with a stable artifact schema and validator.

### Stop Conditions

Stop if row-specific runners still need incompatible artifact schemas.

## Phase 2: LGSSM Golden Forward Scalar

### Objective

Reconfirm LGSSM as the canonical executable same-target scalar template.

### Entry Conditions

Shared artifact schema and validator exist.

### Required Artifacts

- `docs/plans/bayesfilter-ledh-forward-scalar-amendment-phase2-lgssm-result-2026-07-06.md`
- LGSSM tiny artifact under `docs/plans/`
- LGSSM N=10000 artifact, reusing or refreshing the existing value artifact.

### Steps

1. Freeze row `benchmark_lgssm_exact_oracle_m3_T50`.
2. Freeze theta:
   `(phi1, phi2, phi3, q_scale, r_scale) = (0.72, 0.55, 0.35, 0.35, 0.45)`.
3. Freeze dataset seed `81100`, horizon `T=50`.
4. Bind identity flow observations.
5. Bind Gaussian transition density.
6. Bind Gaussian observation density.
7. Run tiny prefix with small `N` and one seed.
8. Compare tiny/full row value to `tf_kalman_log_likelihood` on the same
   observations/model as a reference diagnostic.
9. Run or validate existing N=10000 artifact through the new schema validator.
10. Write row result with `n10000_same_target_value_admitted` only if the
    executable artifact validates.

### Required Checks

- LGSSM schema validation.
- LGSSM exact Kalman comparator presence.
- Existing Phase 3 LGSSM admission test.

### Evidence Contract

LGSSM passes if `log_likelihood_by_seed` is finite and the target identity
matches the exact Kalman row target.

### Forbidden Claims/Actions

- Do not use LGSSM to validate nonlinear rows.
- Do not change score status.

### Handoff Conditions

Phase 3 may begin when LGSSM has a validated artifact that future phases can
copy structurally.

### Stop Conditions

Stop if the old LGSSM artifact cannot be normalized to the new schema.

## Phase 3: Fixed SIR Forward Scalar

### Objective

Reconfirm the amended fixed SIR row as a full observed-data row with free model
parameters.

### Entry Conditions

LGSSM template passed. The fixed SIR target/theta amendment is accepted.

### Required Artifacts

- `docs/plans/bayesfilter-ledh-forward-scalar-amendment-phase3-fixed-sir-result-2026-07-06.md`
- Fixed SIR tiny artifact.
- Fixed SIR N=10000 artifact, reusing or refreshing the existing value artifact.

### Steps

1. Freeze row `zhao_cui_spatial_sir_austria_j9_T20`.
2. Freeze theta coordinate `sir_log_scale_theta`.
3. Freeze theta:
   `(log_kappa_scale, log_nu_scale, log_obs_noise_scale) = (0, 0, 0)`.
4. Ensure dataset comes from the parameterized/scaled SIR model at the log-scale
   origin.
5. Reject the old `no_free_theta` route as admission evidence.
6. Bind identity flow observations: infectious components with Gaussian
   observation model.
7. Bind SIR transition density used by the reviewed clipped/process-noise
   policy.
8. Bind SIR observation density.
9. Run tiny prefix with small `N` and one seed.
10. Validate or refresh N=10000 artifact through the new schema.
11. Write explicit nonclaims:
    - not exact nonlinear likelihood proof;
    - not Zhao-Cui source-faithful free-theta claim;
    - not score admission.

### Required Checks

- Contract theta dimension is `3`.
- Parameter order is exactly
  `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)`.
- No artifact with `no_free_theta` can admit this row.

### Evidence Contract

Fixed SIR passes if the executed `log_likelihood` is from the amended
observed-data row and not from the legacy scoped parameterized diagnostic.

### Forbidden Claims/Actions

- Do not claim source-faithful Zhao-Cui free-theta semantics.
- Do not use scoped SIR diagnostic as full row evidence.
- Do not score.

### Handoff Conditions

Phase 4 may begin with two validated templates: exact linear-Gaussian and
high-dimensional nonlinear Gaussian-observation.

### Stop Conditions

Stop if the artifact cannot prove the model-parameter theta path is the one
used by the scalar.

## Phase 4: Predator-Prey Forward Scalar

### Objective

Build and admit the additive-Gaussian predator-prey LEDH forward scalar.

### Entry Conditions

Shared runner schema passed. LGSSM and fixed SIR templates are available.

### Required Artifacts

- `docs/plans/bayesfilter-ledh-forward-scalar-amendment-phase4-predator-prey-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-amendment-phase4-predator-prey-result-2026-07-06.md`
- Tiny predator-prey value artifact.
- N=10000 predator-prey value artifact if tiny passes.

### Steps

1. Freeze row `zhao_cui_predator_prey_T20`.
2. Freeze dataset seed `81104`, horizon `T=20`.
3. Freeze theta:
   `(r, K, a, s, u, v) = (0.6, 114.0, 25.0, 0.3, 0.5, 0.5)`.
4. Bind model source: `p30_predator_prey_fixture_model`.
5. Bind identity flow observations.
6. Bind transition mean and transition Gaussian density from the predator-prey
   process model.
7. Bind observation mean as state identity and additive Gaussian observation
   density.
8. Add a one-step replay test:
   independently compute one time-step correction from transition density,
   observation density, `pre_flow_log_density`, and `forward_log_det`.
9. Run tiny fixed-randomness value.
10. If tiny passes, run trusted GPU/XLA N=10000 value.
11. Validate artifact and record admission or blocker.

### Required Checks

- Contract validation for predator-prey.
- One-step replay or density callback shape/value check.
- Tiny finite scalar.
- N=10000 finite scalar for admission.

### Evidence Contract

Predator-prey passes only if the artifact proves the additive-Gaussian
predator-prey observation density, not a UKF/SVD/SRQF surrogate row, is used
in the LEDH correction.

### Forbidden Claims/Actions

- Do not use non-LEDH predator-prey SGQF/UKF value as LEDH admission.
- Do not admit from callback existence.
- Do not score.

### Handoff Conditions

Phase 5 may begin after predator-prey is either admitted or blocked with an
exact row-level reason.

### Stop Conditions

Stop this row if transition/observation callback semantics cannot be tied to
the frozen row target.

## Phase 5: Actual SV Forward Scalar

### Objective

Build and admit actual SV using raw target density with a log-square flow-only
adapter.

### Entry Conditions

The shared schema can distinguish flow observations from target observations.

### Required Artifacts

- `docs/plans/bayesfilter-ledh-forward-scalar-amendment-phase5-actual-sv-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-amendment-phase5-actual-sv-result-2026-07-06.md`
- Tiny actual-SV value artifact.
- N=10000 actual-SV value artifact if tiny passes.

### Steps

1. Freeze row `zhao_cui_sv_actual_nongaussian_T1000`.
2. Freeze dataset seed `81101`, horizon `T=1000`.
3. Freeze raw observations from `_sv_dataset`.
4. Freeze theta:
   `(gamma_unconstrained, log_beta)`.
5. Amend the contract wording if necessary:
   target policy is raw actual-SV observation density;
   log-square observations are flow-only.
6. Bind flow observations:
   `log(y_t^2 + offset) - 2 log(beta)`.
7. Bind target observation density:
   raw zero-mean normal SV density for raw `y_t`.
8. Bind transition density:
   latent AR(1) Gaussian SV transition.
9. Add guard test:
   the row is rejected if transformed observations are used as target
   observations.
10. Add guard test:
    the row is rejected if KSC mixture density is used as target density.
11. Run tiny fixed-randomness value.
12. If tiny passes, run trusted GPU/XLA N=10000 value.
13. Validate artifact and record admission or blocker.

### Required Checks

- Actual-SV contract validation.
- Raw-target/log-square-flow adapter audit.
- Tiny finite scalar.
- N=10000 finite scalar for admission.

### Evidence Contract

Actual SV passes only if raw observations feed the target observation density
and transformed observations feed only the LEDH flow/proposal mechanism.

### Forbidden Claims/Actions

- Do not claim KSC surrogate evidence.
- Do not use transformed observations as actual-SV target density.
- Do not use raw Gaussian-closure/SRUKF evidence as LEDH admission.
- Do not score.

### Handoff Conditions

Phase 6 may begin when the first raw-target/log-square-flow adapter is
admitted or blocked with a precise implementation/math reason.

### Stop Conditions

Stop this row if target policy remains ambiguous between raw SV and transformed
SV.

## Phase 6: Generalized SV Forward Scalar

### Objective

Build and admit generalized SV using the same raw-target/log-square-flow
discipline as actual SV, with its own row target and theta semantics.

### Entry Conditions

Actual SV adapter audit exists, even if actual SV was blocked.

### Required Artifacts

- `docs/plans/bayesfilter-ledh-forward-scalar-amendment-phase6-generalized-sv-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-amendment-phase6-generalized-sv-result-2026-07-06.md`
- Tiny generalized-SV value artifact.
- N=10000 generalized-SV value artifact if tiny passes.

### Steps

1. Freeze row `zhao_cui_generalized_sv_synthetic_from_estimated_values`.
2. Freeze dataset seed `81105`, horizon `T=1008`.
3. Freeze theta coordinate `source_route_active_transformed_prior_mean`.
4. Freeze theta:
   `(gamma_unconstrained, log_tau, mu)`.
5. Freeze row target:
   raw generalized-SV observed-data likelihood for the generated synthetic row.
6. Bind flow observations:
   `log(y_t^2 + offset)`.
7. Bind target observation density:
   raw zero-mean generalized-SV normal density for raw `y_t`.
8. Bind transition density:
   prior-mean generalized-SV latent transition.
9. Add guard test:
   actual-SV artifacts cannot admit generalized SV.
10. Add guard test:
    KSC artifacts cannot admit generalized SV.
11. Add one-step theta semantics replay:
    `gamma = Normal(0,1).cdf(gamma_unconstrained)`,
    `tau = exp(log_tau)`,
    `mu = theta[2]`.
12. Run tiny fixed-randomness value.
13. If tiny passes, run trusted GPU/XLA N=10000 value.
14. Validate artifact and record admission or blocker.

### Required Checks

- Generalized-SV contract validation.
- Raw-target/log-square-flow adapter audit.
- Theta semantics replay.
- Tiny finite scalar.
- N=10000 finite scalar for admission.

### Evidence Contract

Generalized SV passes only if the artifact proves the source-row target, not
native-oracle, actual-SV, KSC, or auxiliary evidence.

### Forbidden Claims/Actions

- Do not borrow actual-SV or KSC evidence.
- Do not claim SP500 posterior or paper-data evidence.
- Do not score.

### Handoff Conditions

Phase 7 may begin after generalized SV is admitted or blocked with a precise
row-level reason.

### Stop Conditions

Stop this row if the source-row theta or target policy is not frozen.

## Phase 7: KSC SV Forward Scalar

### Objective

Build the missing KSC-specific LEDH route and admit the KSC finite-mixture
surrogate forward scalar.

### Entry Conditions

Actual SV and generalized SV phases have hardened the target-vs-flow adapter
guards. KSC remains separate from actual SV.

### Required Artifacts

- `docs/plans/bayesfilter-ledh-forward-scalar-amendment-phase7-ksc-sv-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-amendment-phase7-ksc-sv-result-2026-07-06.md`
- Tiny KSC value artifact.
- N=10000 KSC value artifact if tiny passes.

### Steps

1. Freeze row `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`.
2. Freeze source actual-SV dataset seed used to derive transformed KSC
   observations.
3. Freeze transformed KSC observations:
   `log(y_t^2 + offset)`.
4. Freeze theta:
   `(gamma_unconstrained, log_beta)`.
5. Build a KSC-specific LEDH callback/route.
6. Bind flow observations in KSC transformed space.
7. Bind target observation density:
   KSC finite Gaussian-mixture surrogate likelihood.
8. Bind transition density:
   latent AR(1) Gaussian transition matching the KSC surrogate row.
9. Add guard test:
   actual raw SV density is forbidden for this row.
10. Add guard test:
    actual-SV artifact cannot admit KSC.
11. Compare tiny prefix against existing KSC mixture Kalman/reference value
    where feasible.
12. Run tiny fixed-randomness value.
13. If tiny passes, run trusted GPU/XLA N=10000 value.
14. Validate artifact and record admission or blocker.

### Required Checks

- KSC contract validation.
- KSC-specific route presence.
- Mixture likelihood sanity check.
- Tiny finite scalar.
- N=10000 finite scalar for admission.

### Evidence Contract

KSC passes only if the row target is the KSC finite-mixture surrogate
likelihood. Raw actual-SV density is a veto.

### Forbidden Claims/Actions

- Do not reuse actual-SV callback as KSC evidence.
- Do not claim native actual-SV likelihood.
- Do not score.

### Handoff Conditions

Phase 8 may begin after every model has either an admitted N=10000 scalar
artifact or a precise blocker artifact.

### Stop Conditions

Stop this row if no KSC-specific LEDH route can be built without changing the
row target.

## Phase 8: Value Integration And Leaderboard Rebuild

### Objective

Rebuild the LEDH value layer using only rows with admitted same-target forward
scalar artifacts.

### Entry Conditions

All model phases are complete or blocked.

### Required Artifacts

- `docs/plans/bayesfilter-ledh-forward-scalar-amendment-phase8-integration-result-2026-07-06.md`
- Refreshed LEDH-inclusive leaderboard JSON/MD.
- Integration tests.

### Steps

1. Collect model results from Phases 2-7.
2. Build an admitted-row table:
   - row;
   - artifact path;
   - `log_likelihood` mean;
   - MC standard error;
   - target policy;
   - flow policy;
   - admission status.
3. Build a blocked-row table with precise blocker tokens.
4. Update LEDH leaderboard value rows from admitted artifacts only.
5. Preserve blocked rows visibly; do not omit them.
6. Ensure score fields remain blocked unless already independently admitted by
   prior score gates for rows whose scalar is admitted.
7. Add integration tests:
   - all admitted rows have `target_scalar`;
   - all admitted rows have `log_likelihood`;
   - no blocked row has a numeric LEDH value;
   - actual SV and KSC artifacts are not cross-used;
   - value and future score route IDs must match before score promotion.
8. Write the Phase 8 result.

### Required Checks

Run the integration tests and relevant leaderboard tests.

### Evidence Contract

The phase passes if the leaderboard value layer includes only admitted
same-target scalar rows and preserves all blockers.

### Forbidden Claims/Actions

- Do not claim score repair for rows whose score has not been separately
  admitted.
- Do not rank runtimes against non-LEDH rows.
- Do not claim HMC readiness, posterior correctness, or scientific
  superiority.

### Handoff Conditions

After Phase 8, a new score program may begin, but only for rows whose
same-target forward scalar is admitted.

### Stop Conditions

Stop if any leaderboard row would need to use metadata-only or callback-only
evidence as a numeric value.

## Review And Execution Policy

Each model phase must have its own subplan before execution. Each subplan must
state:

- phase objective;
- inherited entry conditions;
- required artifacts;
- required checks/tests/reviews;
- evidence contract;
- forbidden claims/actions;
- exact next-phase handoff conditions;
- stop conditions.

At the end of each model phase:

1. run required local checks;
2. write the phase result;
3. draft or refresh the next model subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

Claude may be used as read-only reviewer under the standing approval. Claude
has no edit, execution, approval, scientific-claim, or authority role. If
Claude does not respond, run a tiny probe; if the probe succeeds, narrow the
prompt; if Claude is unavailable or policy-blocked, replace with fresh Codex
read-only review.

## Nonclaims

- This plan does not admit any new scalar by itself.
- This plan does not admit any score.
- This plan does not establish exact nonlinear likelihood correctness for
  approximate LEDH estimators.
- This plan does not establish HMC readiness, posterior correctness, runtime
  ranking, or scientific superiority.
