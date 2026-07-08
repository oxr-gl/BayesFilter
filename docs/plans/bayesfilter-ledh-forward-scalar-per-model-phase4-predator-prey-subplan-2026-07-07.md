# Phase 4 Subplan: Predator-Prey Forward Scalar Build

metadata_date: 2026-07-07
status: `DRAFT_AFTER_PHASE3`
master_program: `docs/plans/bayesfilter-ledh-forward-scalar-per-model-master-program-2026-07-07.md`
phase: 4

## Phase Objective

Build or locate an executable same-target observed-data LEDH forward scalar
artifact for the previously blocked additive-Gaussian predator-prey row.

This phase is forward-scalar-only. It must not implement scores, admit scores,
or rebuild the leaderboard.

Target scalar: `observed_data_log_likelihood_estimator`, reported as
`log_likelihood`.

## Entry Conditions Inherited From Previous Phase

- Phase 1 schema guard passed after theta-equality repair.
- Phase 2 LGSSM canonical artifact validates locally.
- Phase 3 fixed SIR canonical artifact validates locally under
  `sir_log_scale_theta`.
- Phase 3 local checks passed:
  `28 passed, 2 warnings`.
- Phase 3 did not admit predator-prey, SV, generalized-SV, or any score.
- Phase 3 result and this subplan must pass read-only review before execution.

## Required Artifacts

- Phase 4 result:
  `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase4-predator-prey-result-2026-07-07.md`
- Canonical predator-prey executable schema artifact:
  `docs/plans/ledh-phase4-predator-prey-forward-scalar-artifact-2026-07-07.json`
- Optional markdown summary:
  `docs/plans/ledh-phase4-predator-prey-forward-scalar-artifact-2026-07-07.md`
- Mandatory predator-prey artifact replay test:
  `tests/highdim/test_ledh_phase4_predator_prey_forward_scalar_artifact.py`
- Phase 5 actual-SV subplan:
  `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase5-actual-sv-subplan-2026-07-07.md`
- Phase 4 review bundle:
  `docs/reviews/bayesfilter-ledh-forward-scalar-per-model-phase4-review-bundle-2026-07-07.md`

## Required Checks/Tests/Reviews

Required local checks after implementation:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py \
  tests/highdim/test_ledh_phase2_lgssm_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase3_fixed_sir_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase4_predator_prey_forward_scalar_artifact.py -q
```

Required review:

- bounded read-only review of Phase 4 result and Phase 5 subplan before Phase 5
  starts.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the predator-prey row produce an executable same-target observed-data log likelihood artifact under the shared schema? |
| Baseline/comparator | Current predator-prey row metadata contract, any existing predator-prey runner/callback code, Phase 1 schema validator, and row-specific target definitions discovered in code. |
| Primary criterion | A canonical predator-prey artifact validates with `require_admitted=True`, finite `log_likelihood_by_seed`, row id `zhao_cui_predator_prey_T20`, theta coordinate `physical`, theta values `(0.6,114,25,0.3,0.5,0.5)`, full-row scale, and additive-Gaussian predator-prey target-density correction. |
| Veto diagnostics | No executable runner path; missing `log_likelihood_by_seed`; wrong row target; wrong theta; target density not used for correction; callback-only evidence; metadata-only evidence; score fields used as value evidence; runtime or finite output used without schema validation. |
| Explanatory diagnostics | Runtime, compile time, ESS, tiny smoke artifacts, and any row-specific reference diagnostics. |
| Not concluded | No score admission, score correctness, exact nonlinear likelihood correctness, HMC readiness, posterior correctness, scientific superiority, or runtime ranking. |
| Artifact | Phase 4 result, canonical predator-prey schema artifact, mandatory replay test, Phase 5 subplan. |

## Step-By-Step Plan

1. Inventory predator-prey code paths and artifacts:
   - search for `zhao_cui_predator_prey_T20`;
   - search for predator-prey runner/callback/model code;
   - identify whether an executable LEDH value runner already exists.
2. Freeze row contract from `make_predator_prey_forward_contract(...)`:
   - row id `zhao_cui_predator_prey_T20`;
   - theta coordinate `physical`;
   - theta values `[0.6, 114.0, 25.0, 0.3, 0.5, 0.5]`;
   - target observation policy `additive_gaussian_predator_prey`.
3. If an existing executable artifact is found, normalize it only if it
   preserves row id, theta, target observation policy, target-density
   correction, seed list, horizon, particle count, and finite likelihood
   vector.
4. If no executable artifact exists, implement the smallest runner or adapter
   needed to emit the canonical artifact. Start with a tiny smoke artifact
   before any full-row run.
5. Validate any canonical artifact with:
   - `validate_ledh_forward_scalar_artifact(..., expected_row_id=..., require_admitted=True)`.
6. Add a mandatory replay test that reads the actual Phase 4 canonical JSON
   artifact from disk and validates it with `require_admitted=True`.
7. If the full-row canonical artifact cannot be produced in this phase, write a
   blocker result instead of admitting predator-prey.
8. Draft Phase 5 actual-SV subplan.
9. Run required local checks.
10. Send Phase 4 result and Phase 5 subplan for bounded read-only review.

## Forbidden Claims/Actions

- Do not use LGSSM or SIR evidence for predator-prey admission.
- Do not admit metadata-only or callback-only evidence.
- Do not change predator-prey row target, theta, seed list, horizon, or
  particle count after seeing results.
- Do not implement or admit scores.
- Do not rebuild the leaderboard.
- Do not claim exact nonlinear likelihood correctness or runtime ranking.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin only if:

- either the canonical predator-prey artifact validates with
  `require_admitted=True`, or a blocker result explains why it cannot yet be
  produced;
- the mandatory predator-prey replay test passes if a canonical artifact is
  produced;
- Phase 4 result records source/runner/artifact paths and nonclaims;
- Phase 4 local checks pass or the blocker result explains why they cannot;
- Phase 5 actual-SV subplan is drafted;
- read-only review agrees, or a documented fallback Codex review accepts the
  boundary.

## Stop Conditions

Stop and update the visible stop handoff if:

- no executable predator-prey LEDH value runner path exists and implementing one
  would exceed this phase's scope;
- `log_likelihood_by_seed` is missing or nonfinite;
- target-density correction is absent or ambiguous;
- theta values differ from `[0.6, 114.0, 25.0, 0.3, 0.5, 0.5]`;
- the canonical artifact fails Phase 1 validation;
- the phase would need score work;
- a human approval boundary is reached.

## Skeptical Plan Audit

| Risk | Control |
| --- | --- |
| Wrong baseline | Phase starts with inventory; no LGSSM/SIR artifact can admit predator-prey. |
| Proxy metrics | Runtime and finite output cannot pass without canonical schema validation. |
| Missing stop conditions | Stop conditions cover missing runner, missing likelihood vector, wrong theta, missing target correction, failed validation, and score creep. |
| Hidden assumptions | Runner discovery is explicit before implementation. |
| Artifact mismatch | Required output is a canonical schema artifact or blocker result, not a leaderboard rebuild. |

Audit status: passed for Phase 4 subplan draft.
