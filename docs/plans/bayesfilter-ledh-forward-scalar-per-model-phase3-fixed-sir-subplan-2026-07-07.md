# Phase 3 Subplan: Fixed SIR Forward Scalar Reconfirmation

metadata_date: 2026-07-07
status: `DRAFT_AFTER_PHASE2`
master_program: `docs/plans/bayesfilter-ledh-forward-scalar-per-model-master-program-2026-07-07.md`
phase: 3

## Phase Objective

Reconfirm the fixed spatial SIR row as an executable same-target observed-data
forward scalar under the shared schema and the amended free-parameter
`sir_log_scale_theta` contract.

This phase is forward-scalar-only. It must not implement scores, admit scores,
or rebuild the leaderboard.

Target scalar: `observed_data_log_likelihood_estimator`, reported as
`log_likelihood`.

## Entry Conditions Inherited From Previous Phase

- Phase 1 schema guard passed after theta-equality repair.
- Phase 2 LGSSM canonical artifact validated locally with
  `require_admitted=True`.
- Phase 2 local checks passed:
  `26 passed, 2 warnings`.
- Phase 2 did not admit any nonlinear row and did not run score work.
- Phase 2 result and this subplan must pass read-only review before execution.

## Required Artifacts

- Phase 3 result:
  `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase3-fixed-sir-result-2026-07-07.md`
- Canonical fixed SIR executable schema artifact:
  `docs/plans/ledh-phase3-fixed-sir-forward-scalar-artifact-2026-07-07.json`
- Optional markdown summary:
  `docs/plans/ledh-phase3-fixed-sir-forward-scalar-artifact-2026-07-07.md`
- Phase 4 predator-prey subplan:
  `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase4-predator-prey-subplan-2026-07-07.md`
- Phase 3 review bundle:
  `docs/reviews/bayesfilter-ledh-forward-scalar-per-model-phase3-review-bundle-2026-07-07.md`
- Mandatory fixed SIR artifact replay test:
  `tests/highdim/test_ledh_phase3_fixed_sir_forward_scalar_artifact.py`

## Required Checks/Tests/Reviews

Required local checks:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py \
  tests/highdim/test_ledh_phase2_lgssm_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase3_fixed_sir_forward_scalar_artifact.py -q
```

The fixed SIR artifact replay test is mandatory. Phase 3 may not hand off to
Phase 4 without an automated read-from-disk revalidation of the actual Phase 3
canonical artifact.

Required review:

- bounded read-only review of Phase 3 result and Phase 4 subplan before Phase 4
  starts.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the fixed SIR row produce or preserve an executable same-target observed-data log likelihood artifact under the shared schema and amended free-parameter target? |
| Baseline/comparator | Existing fixed SIR N=10000 value artifact, fixed SIR tiny artifact, Phase 1 schema validator, and the accepted `sir_log_scale_theta` row contract. |
| Primary criterion | A canonical fixed SIR artifact validates with `require_admitted=True`, finite `log_likelihood_by_seed`, row id `zhao_cui_spatial_sir_austria_j9_T20`, theta coordinate `sir_log_scale_theta`, theta values `(0,0,0)`, full-row scale, and target-density correction. |
| Veto diagnostics | Old `no_free_theta` route used as admission; missing `log_likelihood_by_seed`; theta coordinate not `sir_log_scale_theta`; theta values differ from `(0,0,0)`; target density not used for correction; row target mismatch; score fields used as value evidence; runtime or finite output used without schema validation. |
| Explanatory diagnostics | Runtime, compile time, ESS, old SIR artifact shape, and tiny prefix artifact. |
| Not concluded | No score admission, score correctness, exact nonlinear likelihood correctness, Zhao-Cui TT/SIRT source-faithfulness, HMC readiness, posterior correctness, scientific superiority, or runtime ranking. |
| Artifact | Phase 3 result, canonical fixed SIR schema artifact, Phase 4 subplan. |

## Step-By-Step Plan

1. Read existing fixed SIR N=10000 value artifact:
   `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-fixed-sir-value-ladder-N10000-2026-07-03.json`.
2. Verify it has:
   - finite `log_likelihood`;
   - `primary_pass_5x_runtime_gate == true`;
   - `shape.num_particles == 10000`;
   - `shape.time_steps == 20`;
   - batch seeds `[81120, 81121, 81122, 81123, 81124]`;
   - `sir_semantics.row_id == zhao_cui_spatial_sir_austria_j9_T20`;
   - `sir_semantics.target_density_used_for_correction == true`.
3. Reject old `no_free_theta` semantics as admission evidence unless the
   canonical artifact explicitly binds:
   - theta coordinate `sir_log_scale_theta`;
   - theta values `[0.0, 0.0, 0.0]`;
   - forward contract from `make_fixed_sir_logscale_forward_contract(...)`.
4. Build a canonical Phase 1 artifact using:
   - `log_likelihood_by_seed = log_likelihood`;
   - `average_log_likelihood_by_seed = log_likelihood / 20`;
   - `flow_observation_policy = sir_infectious_components_gaussian_flow_observation`;
   - `target_observation_policy = fixed_sir_infectious_components_gaussian_observation_density`;
   - `target_density_used_for_correction = true`;
   - the fixed SIR forward contract with `full_leaderboard_row=True`.
5. Validate the canonical artifact with:
   - `validate_ledh_forward_scalar_artifact(..., expected_row_id=..., require_admitted=True)`.
6. If validation passes, write the canonical artifact and Phase 3 result.
7. Add a fixed SIR artifact replay test that reads the actual Phase 3
   canonical JSON artifact from disk and validates it with
   `require_admitted=True`.
8. Draft Phase 4 predator-prey subplan.
9. Run required local checks.
10. Send Phase 3 result and Phase 4 subplan for bounded read-only review.

## Forbidden Claims/Actions

- Do not use SIR evidence for predator-prey or SV rows.
- Do not revert to old `no_free_theta` row semantics.
- Do not change fixed SIR target, theta, seed list, horizon, or particle count
  after seeing results.
- Do not implement or admit scores.
- Do not rebuild the leaderboard.
- Do not claim exact nonlinear likelihood correctness or runtime ranking.

## Exact Next-Phase Handoff Conditions

Phase 4 may begin only if:

- the canonical fixed SIR artifact validates with `require_admitted=True`;
- the mandatory fixed SIR artifact replay test passes on the actual Phase 3
  canonical JSON artifact;
- Phase 3 result records the source artifact and canonical artifact paths;
- Phase 3 local checks pass;
- Phase 4 predator-prey subplan is drafted;
- read-only review agrees, or a documented fallback Codex review accepts the
  boundary.

## Stop Conditions

Stop and update the visible stop handoff if:

- the old SIR artifact cannot be normalized without changing target identity;
- `log_likelihood` is missing or nonfinite;
- `sir_log_scale_theta` cannot be bound as the free-parameter contract;
- theta values differ from `[0.0, 0.0, 0.0]`;
- target density correction is absent or ambiguous;
- the canonical artifact fails Phase 1 validation;
- the phase would need score work;
- a human approval boundary is reached.

## Skeptical Plan Audit

| Risk | Control |
| --- | --- |
| Wrong baseline | Uses only the fixed SIR N=10000 row artifact and amended SIR theta contract. |
| Proxy metrics | Runtime and finite output cannot pass without canonical schema validation. |
| Missing stop conditions | Stop conditions cover missing likelihood vector, no free theta, wrong theta, missing target correction, failed validation, and score creep. |
| Hidden assumptions | Normalization maps old top-level `log_likelihood` to canonical `log_likelihood_by_seed` explicitly. |
| Artifact mismatch | Required output is a canonical schema artifact plus result, not a leaderboard rebuild. |

Audit status: passed for Phase 3 subplan draft.
