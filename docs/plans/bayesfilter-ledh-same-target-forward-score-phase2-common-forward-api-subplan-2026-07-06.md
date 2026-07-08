# Phase 2 Subplan: Common Forward Likelihood API

metadata_date: 2026-07-06
status: DRAFT
master_program: docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md
phase: 2

## Phase Objective

Build or standardize a TensorFlow/TFP adapter API that separates proposal/flow
surfaces from target likelihood densities and returns the finite-`N`
same-target LEDH log-likelihood estimator.

## Entry Conditions Inherited From Previous Phase

- Phase 1 froze each row target and theta vector.
- No score implementation is allowed for rows without a frozen target.
- By explicit human amendment on 2026-07-06, the fixed spatial SIR row uses
  `sir_log_scale_theta` with theta
  `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)` and truth theta
  `[0,0,0]`.
- The current parameterized SIR row remains scoped/legacy diagnostic and must
  not be promoted as a shortcut around fixed-row full observed-data gates.

## Required Artifacts

- Phase 2 result:
  `docs/plans/bayesfilter-ledh-same-target-forward-score-phase2-common-forward-api-result-2026-07-06.md`
- Code changes for shared adapter interfaces and route metadata.
- Focused unit tests for API contracts and no proposal-target conflation.
- Refreshed Phase 3 subplan.

## Required Checks/Tests/Reviews

- Unit tests that target densities, proposal observations, and correction
  weights are distinct fields.
- Static/text checks that admitted forward paths expose
  `target_scalar = observed_data_log_likelihood_estimator`.
- Focused checks that fixed SIR API metadata exposes `sir_log_scale_theta`,
  `theta_dimension = 3`, and the exact parameter order.
- CPU smoke tests may run with GPU hidden; GPU/XLA tests require trusted
  execution.
- Claude read-only code/plan review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the shared API make it impossible to confuse proposal flow quantities with the target likelihood scalar? |
| Baseline/comparator | Phase 1 target contract and existing LEDH runner interfaces. |
| Primary criterion | The API computes and labels the corrected finite-`N` likelihood estimator separately from proposal diagnostics. |
| Veto diagnostics | A proposal scalar exposed as leaderboard value; target likelihood density missing; route metadata missing; NumPy backend in new algorithmic code. |
| Explanatory diagnostics | API ergonomics, compile notes, and old callback compatibility. |
| Not concluded | No model row is admitted until Phase 3 row-specific value checks pass. |

## Forbidden Claims/Actions

- Do not claim model-level row admission from API shape alone.
- Do not implement score logic except harmless metadata placeholders.
- Do not reintroduce `no_free_theta` for the fixed SIR row.
- Do not introduce PyTorch/JAX/NumPy algorithmic implementation paths.

## Allowed Operations

- Edit TensorFlow/TFP implementation and tests.
- Run focused CPU smoke tests.
- Run trusted GPU/XLA smoke tests if the sub-result requires them.
- Use Claude read-only review of diffs and API contracts.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if:

- API tests pass;
- target likelihood estimator metadata is present;
- fixed SIR metadata carries the amended 3D `sir_log_scale_theta` contract;
- Phase 2 result records changed files, checks, and unresolved risks;
- Phase 3 subplan names the model order and row-specific value gates.

## Stop Conditions

Stop if the repo architecture cannot express target likelihood correction
without conflating proposal quantities, or if required code edits would cross a
human-required backend/policy boundary.
