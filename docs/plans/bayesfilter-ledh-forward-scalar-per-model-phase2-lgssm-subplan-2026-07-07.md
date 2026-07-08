# Phase 2 Subplan: LGSSM Forward Scalar Reconfirmation

metadata_date: 2026-07-07
status: `DRAFT_AFTER_PHASE1`
master_program: `docs/plans/bayesfilter-ledh-forward-scalar-per-model-master-program-2026-07-07.md`
phase: 2

## Phase Objective

Reconfirm the exact linear-Gaussian LEDH row under the shared executable
forward-scalar artifact schema.

This phase is forward-scalar-only. It must not implement scores, admit scores,
or rebuild the leaderboard.

Target scalar: `observed_data_log_likelihood_estimator`, reported as
`log_likelihood`.

## Entry Conditions Inherited From Previous Phase

- Phase 0 froze the admitted/blocked baseline.
- Phase 1 added the canonical executable artifact schema:
  `bayesfilter.highdim.ledh_forward_scalar_artifact.v1`.
- Phase 1 local checks passed:
  `23 passed, 2 warnings`.
- Phase 1 did not admit any new row.
- Phase 1 result and this subplan must pass read-only review before execution.

## Required Artifacts

- Phase 2 result:
  `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase2-lgssm-result-2026-07-07.md`
- Canonical LGSSM executable schema artifact:
  `docs/plans/ledh-phase2-lgssm-forward-scalar-artifact-2026-07-07.json`
- Optional refreshed markdown summary:
  `docs/plans/ledh-phase2-lgssm-forward-scalar-artifact-2026-07-07.md`
- Phase 3 fixed SIR subplan:
  `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase3-fixed-sir-subplan-2026-07-07.md`
- Phase 2 review bundle:
  `docs/reviews/bayesfilter-ledh-forward-scalar-per-model-phase2-review-bundle-2026-07-07.md`

## Required Checks/Tests/Reviews

Required local checks:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py -q
```

If Phase 2 adds a specific LGSSM normalization test, include it in this check
set.

Required review:

- bounded read-only review of Phase 2 result and Phase 3 subplan before Phase 3
  starts.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the LGSSM row produce or preserve an executable same-target observed-data log likelihood artifact under the shared schema? |
| Baseline/comparator | Existing LGSSM N=10000 value artifact, LGSSM tiny artifact, exact Kalman log likelihood on the same observations/model, and Phase 1 schema validator. |
| Primary criterion | A canonical LGSSM artifact validates with `require_admitted=True`, finite `log_likelihood_by_seed`, row id `benchmark_lgssm_exact_oracle_m3_T50`, full-row scale, and target identity matching the exact Kalman comparator. |
| Veto diagnostics | Missing canonical artifact; missing `log_likelihood_by_seed`; target scalar not `observed_data_log_likelihood_estimator`; missing exact Kalman comparator identity; row target or theta mismatch; score fields used as value evidence; runtime or finite output used without schema validation. |
| Explanatory diagnostics | Runtime, compile time, ESS, exact Kalman delta, tiny prefix artifact, and old artifact shape. |
| Not concluded | No score admission, score correctness, HMC readiness, posterior correctness, scientific superiority, or runtime ranking. |
| Artifact | Phase 2 result, canonical LGSSM schema artifact, Phase 3 subplan. |

## Step-By-Step Plan

1. Read the existing LGSSM N=10000 artifact:
   `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-lgssm-m3-t50-same-target-value-ladder-N10000-2026-07-03.json`.
2. Verify it has:
   - row id `benchmark_lgssm_exact_oracle_m3_T50`;
   - `primary_pass_same_target_value_execution == true`;
   - finite `total_log_likelihood_by_seed`;
   - `shape.num_particles == 10000`;
   - `shape.time_steps == 50`;
   - batch seeds `[81120, 81121, 81122, 81123, 81124]`;
   - exact comparator `tf_kalman_log_likelihood on same observations/model`;
   - truth theta `(0.72, 0.55, 0.35, 0.35, 0.45)`.
3. Build a canonical Phase 1 artifact using:
   - `log_likelihood_by_seed = total_log_likelihood_by_seed`;
   - `average_log_likelihood_by_seed = total_log_likelihood_by_seed / 50`;
   - `flow_observation_policy = identity_lgssm_observation_flow`;
   - `target_observation_policy = lgssm_gaussian_observation_density`;
   - `target_density_used_for_correction = true`;
   - the LGSSM forward contract with `full_leaderboard_row=True`.
4. Validate the canonical artifact with:
   - `validate_ledh_forward_scalar_artifact(..., expected_row_id=..., require_admitted=True)`.
5. If validation passes, write the canonical artifact and Phase 2 result.
6. Draft Phase 3 fixed SIR subplan.
7. Run required local checks.
8. Send Phase 2 result and Phase 3 subplan for bounded read-only review.

## Forbidden Claims/Actions

- Do not use LGSSM evidence for nonlinear rows.
- Do not change the LGSSM row target, theta, seed list, horizon, or particle
  count after seeing results.
- Do not implement or admit scores.
- Do not rebuild the leaderboard.
- Do not claim runtime ranking.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if:

- the canonical LGSSM artifact validates with `require_admitted=True`;
- Phase 2 result records the source artifact and canonical artifact paths;
- Phase 2 local checks pass;
- Phase 3 fixed SIR subplan is drafted;
- read-only review agrees, or a documented fallback Codex review accepts the
  boundary.

## Stop Conditions

Stop and update the visible stop handoff if:

- the old LGSSM artifact cannot be normalized without changing target identity;
- `total_log_likelihood_by_seed` is missing or nonfinite;
- exact Kalman comparator identity is missing or wrong;
- theta values differ from forward-contract `truth_theta`;
- the canonical artifact fails Phase 1 validation;
- the phase would need score work;
- a human approval boundary is reached.

## Skeptical Plan Audit

| Risk | Control |
| --- | --- |
| Wrong baseline | Uses only the existing LGSSM row artifact and exact Kalman comparator identity. |
| Proxy metrics | Runtime and finite output cannot pass without canonical schema validation. |
| Missing stop conditions | Stop conditions cover missing likelihood vector, wrong target, failed validation, and score creep. |
| Hidden assumptions | Normalization maps old `total_log_likelihood_by_seed` to canonical `log_likelihood_by_seed` explicitly. |
| Artifact mismatch | Required output is a canonical schema artifact plus result, not a leaderboard rebuild. |

Audit status: passed for Phase 2 subplan draft.
