# Phase 3 Subplan: Filter-Program Registry And Capability Gates

Date: 2026-07-03

Status: `REVIEWED_READY_FOR_PHASE3_EXECUTION`

## Phase Objective

Add a small filter-program registry and capability gate so generic SSM targets
can bind to any BayesFilter filter only when the model and filter capabilities
match and the filter is deterministic/admissible for HMC.

Phase 3 uses the live Phase 2 public export boundary in
`bayesfilter/ssm/__init__.py` and the implementation in
`bayesfilter/ssm/target_builder.py`. The Phase 2 result records the same export
inventory:
`docs/plans/bayesfilter-general-neutra-ssm-interface-phase2-target-builder-result-2026-07-03.md`.

Relevant Phase 2 names:

- `GenericSSMPosteriorAdapter`
- `SSMTargetBuilderMetadata`
- `build_ssm_posterior_adapter`
- `stable_ssm_posterior_adapter_signature`

## Entry Conditions Inherited From Previous Phase

- Phase 2 result states `PHASE2_GATE_PASSED`.
- Generic target builder exists and passes focused tests.
- Phase 3 subplan has been refreshed and reviewed.

Concrete inherited Phase 2 decisions Phase 3 must preserve:

- `GenericSSMPosteriorAdapter` already validates batch-native `[B, D]` value and
  score shape; Phase 3 should not duplicate target evaluation logic.
- `FilterProgram` remains the stable filter manifest surface from Phase 1.
- Registry output must feed `FilterProgram` and preserve
  `deterministic_target_policy`, `approximation_semantics`, and
  `required_model_capabilities`.
- Top-level `bayesfilter.__all__` remains unchanged unless a focused public API
  review is added.
- Phase 3 must not alter existing filter algorithms, numerical policy, HMC
  runtime semantics, or target-builder value/score authority semantics.

## Required Artifacts

- Source module:
  `bayesfilter/ssm/filter_registry.py`
- Package export refresh:
  `bayesfilter/ssm/__init__.py`
- Focused tests:
  `tests/test_general_ssm_filter_registry.py`
- Phase 3 result:
  `docs/plans/bayesfilter-general-neutra-ssm-interface-phase3-filter-registry-result-2026-07-03.md`
- Refreshed Phase 4 subplan.

## Required Checks, Tests, And Reviews

Local checks:

- `python -m pytest tests/test_general_ssm_contracts.py tests/test_general_ssm_target_builder.py tests/test_general_ssm_filter_registry.py -q -p no:cacheprovider`
- Registry rejects filters whose required capabilities are absent.
- Registry rejects stochastic particle filters unless deterministic artifact
  state is declared.
- Registry preserves stable `FilterProgram` signatures across equivalent
  descriptors.
- Export allowlist refresh for `bayesfilter.ssm.__all__` if new symbols are
  public.
- Import smoke for `bayesfilter.ssm`.
- Test that registry output can be assembled into `SSMTargetContract` and
  validated by `validate_ssm_target_contract` without the registry bypassing or
  replacing that validator.

Review:

- Claude read-only review of Phase 4 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter decide whether a model/filter pair is admissible for a deterministic HMC target before building the target? |
| Baseline/comparator | Phase 2 direct fixture binding with no registry. |
| Primary pass criterion | Registry produces stable `FilterProgram` manifests, verifies model/filter capability compatibility, and fails closed on missing model capabilities or stochastic nondeterministic HMC targets. |
| Veto diagnostics | Silent acceptance of stochastic fresh-randomness particle likelihood, missing filter approximation semantics, missing deterministic target policy, top-level public API expansion without review, or capability mismatch. |
| Explanatory diagnostics | Supported toy filters and rejected fixture filters. |
| Not concluded | No production particle-filter HMC readiness, no all-filter guarantee, no filter accuracy claim. |
| Artifacts | Registry module, tests, Phase 3 result. |

## Forbidden Claims And Actions

- Do not mark arbitrary particle filters HMC-ready.
- Do not change existing filter numerical policy.
- Do not claim registry support is filter correctness evidence.
- Do not change target-builder value/score behavior.
- Do not mark a stochastic filter HMC-ready unless deterministic artifact state
  is explicitly declared in the descriptor manifest.

## Exact Next-Phase Handoff Conditions

Phase 4 may begin only if:

- registry tests pass;
- Phase 3 result states `PHASE3_GATE_PASSED`;
- deterministic target policy is explicit in manifests;
- registry output includes `FilterProgram` fields required by Phase 1; the
  registry returns `FilterProgram`-compatible metadata and tests verify the
  downstream `SSMTargetContract` still calls `validate_ssm_target_contract`
  rather than replacing that validator inside the registry;
- `bayesfilter.ssm.__all__` is refreshed and tested if new symbols are public;
- Phase 4 subplan is refreshed and reviewed.

## Stop Conditions

Stop if:

- filter capability labels are too ambiguous to gate safely;
- existing filter APIs cannot be represented without a human naming decision;
- a required filter is stochastic and no deterministic artifact contract exists.
- representing filter capability would require changing existing filter
  algorithm behavior or target-builder semantics.

## Skeptical Plan Audit

Status: `PASSED_FOR_PHASE3_EXECUTION_AFTER_REVIEW`

Checked risks:

- Wrong baseline: Phase 3 compares registry decisions to explicit descriptor
  manifests and Phase 1 `FilterProgram`, not to sampler performance.
- Proxy metrics: registry acceptance is an admissibility gate only, not filter
  correctness or HMC readiness evidence.
- Missing stop conditions: ambiguous capability labels, stochastic filters
  without deterministic artifact state, and required behavior changes are stop
  conditions.
- Hidden assumptions: deterministic target policy and approximation semantics
  must be manifest fields.
- Descriptor scope: Phase 3 does not define or require a regularization-policy
  surface; adding one requires a later reviewed subplan or an explicit Phase 3
  repair.
- Artifact mismatch: Phase 3 must write source, tests, result, and refreshed
  Phase 4 subplan before handoff.

## Phase Execution Steps

1. Implement registry dataclasses/helpers.
2. Add accepted and rejected fixture filters.
3. Run local checks.
4. Write Phase 3 result.
5. Refresh and review Phase 4 subplan.

## End-Of-Subplan Closeout Requirements

The result must classify every tested registry decision as accepted,
wrong relative to requested target, unsupported, or not checked.
