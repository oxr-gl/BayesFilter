# Phase 1 Subplan: Shared Forward Scalar Runner Schema

metadata_date: 2026-07-07
status: `DRAFT_AFTER_PHASE0`
master_program: `docs/plans/bayesfilter-ledh-forward-scalar-per-model-master-program-2026-07-07.md`
phase: 1

## Phase Objective

Standardize the executable forward-scalar artifact schema and validator used by
all model-specific phases.

This phase is forward-scalar-only. It must not implement model-specific
adapters, admit a model row, implement scores, admit scores, or rebuild the
leaderboard.

Target scalar: `observed_data_log_likelihood_estimator`, reported as
`log_likelihood`.

## Entry Conditions Inherited From Previous Phase

- Phase 0 recorded exactly two value-admitted rows:
  - `benchmark_lgssm_exact_oracle_m3_T50`;
  - `zhao_cui_spatial_sir_austria_j9_T20`.
- Phase 0 recorded exactly four value-blocked rows:
  - `zhao_cui_predator_prey_T20`;
  - `zhao_cui_sv_actual_nongaussian_T1000`;
  - `zhao_cui_generalized_sv_synthetic_from_estimated_values`;
  - `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`.
- Phase 0 local checks passed.
- Launch review repair agreed after explicit stop conditions were added for
  callback-only evidence and actual-SV/KSC cross-use.

## Required Artifacts

- Phase 1 result:
  `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase1-runner-schema-result-2026-07-07.md`
- Schema/validator implementation, if needed.
- Focused tests, likely:
  `tests/highdim/test_ledh_forward_scalar_admission_guard.py`
- Phase 2 LGSSM subplan:
  `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase2-lgssm-subplan-2026-07-07.md`
- Phase 1 review bundle:
  `docs/reviews/bayesfilter-ledh-forward-scalar-per-model-phase1-review-bundle-2026-07-07.md`

## Required Checks/Tests/Reviews

Required local checks after any implementation:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py -q
```

If no new guard test file is added, the Phase 1 result must explain why
existing tests fully cover the schema guard. That explanation requires review.

Required review:

- bounded read-only review of Phase 1 result and Phase 2 subplan before Phase 2
  starts.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is there a shared executable artifact schema/validator that prevents metadata-only, callback-only, wrong-target, and actual-SV/KSC cross-use admission? |
| Baseline/comparator | Phase 0 baseline and existing forward contract metadata. |
| Primary criterion | A validator or tests reject artifacts without executable `log_likelihood` evidence and reject target/flow ambiguity before any model phase can admit a row. |
| Veto diagnostics | Schema validation alone admits a row; callback-only evidence can pass; actual-SV/KSC artifacts can be cross-used; proposal objective can be target scalar; score fields are required for value admission. |
| Explanatory diagnostics | Existing tiny artifacts, old N=10000 artifacts, and legacy callback inventories. |
| Not concluded | No model row admission, score admission, score correctness, HMC readiness, posterior correctness, scientific superiority, or runtime ranking. |
| Artifact | Phase 1 result, schema/validator/tests, Phase 2 subplan. |

## Forbidden Claims/Actions

- Do not admit a model row.
- Do not implement row-specific LEDH adapters.
- Do not run long GPU/XLA model jobs.
- Do not implement or admit scores.
- Do not rebuild the leaderboard.
- Do not change row targets or pass/fail criteria.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if:

- schema/validator checks pass locally;
- the Phase 1 result records the schema fields and rejection rules;
- callback-only and actual-SV/KSC cross-use are either tested or explicitly
  blocked with a reviewed reason;
- Phase 2 LGSSM subplan is drafted;
- read-only review agrees or a documented fallback Codex review accepts the
  boundary.

## Stop Conditions

Stop and update the visible stop handoff if:

- a shared schema cannot represent all row phases;
- schema validation could admit metadata-only evidence;
- schema validation could admit callback-only evidence;
- actual-SV and KSC-SV artifacts, callbacks, or target densities can be
  cross-used as admission evidence;
- Phase 1 would require model-specific adapter implementation;
- score work becomes necessary;
- a human approval boundary is reached.

## Skeptical Plan Audit

| Risk | Control |
| --- | --- |
| Wrong baseline | Phase 1 inherits the exact Phase 0 baseline. |
| Proxy metrics | Schema requires executable scalar identity, not runtime/memory/finite-output proxy. |
| Missing stop conditions | Stop conditions include metadata-only, callback-only, and actual-SV/KSC cross-use. |
| Hidden assumptions | Phase 1 does not implement model-specific row adapters. |
| Artifact mismatch | Phase 1 result must answer schema/validator readiness only. |

Audit status: passed for Phase 1 subplan draft.
