# Phase 2 Subplan: Posterior Target Builder And Toy Nonlinear Fixture

Date: 2026-07-03

Status: `REVIEWED_READY_FOR_PHASE2_EXECUTION`

## Phase Objective

Implement a generic posterior target builder that composes an
`SSMTargetContract` assembled from `BayesianSSMProblem`, `ParameterChart`,
`ParameterPrior`, and deterministic `FilterProgram` into a batch-native
value/score adapter. Validate it on a tiny nonlinear Gaussian SSM fixture.

Phase 2 uses the Phase 1 public exports from `bayesfilter.ssm`, anchored by the
Phase 1 result export inventory:
`docs/plans/bayesfilter-general-neutra-ssm-interface-phase1-contracts-result-2026-07-03.md`.

- `BayesianSSMProblem`
- `FilterProgram`
- `ParameterChart`
- `ParameterPrior`
- `SSMTargetContract`
- `stable_ssm_target_signature`
- `validate_ssm_target_contract`

## Entry Conditions Inherited From Previous Phase

- Phase 1 result states `PHASE1_GATE_PASSED`.
- Generic SSM contracts and focused tests exist.
- Phase 2 subplan has been refreshed with actual Phase 1 names and reviewed.

Concrete inherited Phase 1 decisions Phase 2 must preserve:

- Public imports come from `bayesfilter.ssm`; internal helper symbols from
  `bayesfilter/ssm/contracts.py` are not public API.
- The target-builder manifest must derive from
  `SSMTargetContract.manifest_payload()` and `stable_ssm_target_signature`.
- `validate_ssm_target_contract(..., require_filter_hmc_target_ready=True)` is
  the Phase 1 gate for deterministic/fixed-randomness filter target readiness.
- Phase 2 must not expand top-level `bayesfilter.__all__` unless a focused
  public API review is added.
- Phase 2 remains contract/toy-fixture work only: no NeuTra training, serious
  HMC, GPU run, package install, network fetch, detached execution, or default
  policy change is authorized.

## Required Artifacts

- Source module:
  `bayesfilter/ssm/target_builder.py`
- Package export refresh:
  `bayesfilter/ssm/__init__.py`
- Toy fixture helpers, either in tests or `bayesfilter/testing`.
- Focused tests:
  `tests/test_general_ssm_target_builder.py`
- Phase 2 result:
  `docs/plans/bayesfilter-general-neutra-ssm-interface-phase2-target-builder-result-2026-07-03.md`
- Refreshed Phase 3 subplan.

## Required Checks, Tests, And Reviews

Local checks:

- `python -m pytest tests/test_general_ssm_contracts.py tests/test_general_ssm_target_builder.py -q -p no:cacheprovider`
- Batch value/score shape check for `[B, D]`.
- Stable adapter signature check.
- Metadata/signature check that the builder manifest carries non-batch static
  SSM dimensions from `SSMStaticShape` and an explicit batch-rank policy.
- `tf.function` compile check for the tiny fixture under explicit CPU-only /
  GPU-hidden conditions, with `CUDA_VISIBLE_DEVICES=-1` set before TensorFlow
  import. XLA compile is optional in Phase 2 and may be omitted if it would
  trigger CUDA/GPU discovery or unstable environment behavior.
- Export allowlist refresh for `bayesfilter.ssm.__all__`.
- Import smoke for `bayesfilter.ssm`.

Review:

- Claude read-only review of Phase 3 subplan.
- Claude source review only if the target builder changes shared inference
  authority semantics.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the generic contracts produce a deterministic batch-native posterior value/score adapter for a toy nonlinear SSM and deterministic filter? |
| Baseline/comparator | Direct prior plus filter likelihood in unconstrained coordinates for the toy fixture. |
| Primary pass criterion | The target builder emits finite rank-1 values and rank-2 scores for rank-2 inputs `[B, D]`, rejects rank-1 scalar-position input `[D]` when batch-native mode is required, allows `[1, D]` as a batch of one, preserves the Phase 1 contract signature in adapter metadata, includes non-batch static SSM dimensions and batch-rank policy in the builder manifest/signature path, and produces stable adapter signatures. |
| Veto diagnostics | Hidden Python row loop in required batch path, stochastic fresh randomness in target value, missing problem/chart/prior/filter manifest in signature, fallback authority promoted to XLA, top-level public API expansion without review, or nonfinite toy target. |
| Explanatory diagnostics | Toy target values, finite-difference comparison, and compile trace count. |
| Not concluded | No correctness for real models, no HMC readiness, no NeuTra training readiness, no all-filter support. |
| Artifacts | Source module, tests, Phase 2 result. |

## Forbidden Claims And Actions

- Do not claim the toy fixture validates production nonlinear filters.
- Do not run serious stochastic comparisons.
- Do not use learned NeuTra transports.
- Do not introduce NumPy into differentiable target code except independent
  test references.
- Do not claim the target builder makes every BayesFilter filter HMC-ready.
- Do not export internal Phase 1 helper symbols.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if:

- target builder tests pass;
- Phase 2 result states `PHASE2_GATE_PASSED`;
- the target builder manifest includes problem, chart, prior, filter, dtype,
  non-batch static SSM dimensions from `SSMStaticShape`, batch-rank policy, and
  value/score authority fields;
- `bayesfilter.ssm.__all__` is refreshed and tested if new symbols are public;
- no top-level `bayesfilter.__all__` expansion occurs unless reviewed;
- Phase 3 subplan is refreshed and reviewed.

## Stop Conditions

Stop if:

- toy target cannot be made deterministic without changing the target claim;
- batch-native path requires scalar fallback;
- target signature cannot be stable;
- generic API naming needs human direction.
- implementing Phase 2 would require changes to existing filter algorithms or
  HMC runtime semantics.

## Skeptical Plan Audit

Status: `PASSED_FOR_PHASE2_EXECUTION_AFTER_REVIEW`

Checked risks:

- Wrong baseline: direct toy prior plus deterministic filter likelihood remains
  the comparator, not existing NeuTra artifacts.
- Proxy metrics: finite toy values and compile success are pass/fail checks for
  the builder only, not scientific validity.
- Missing stop conditions: deterministic target, batch-native shape,
  signature-stability, API naming, and shared-runtime-change stops are explicit.
- Hidden assumptions: Phase 1 exported names and CPU-only/GPU-hidden
  contract/toy checks are explicit; static-shape metadata means non-batch SSM
  dimensions plus explicit batch-rank policy, and is tested before handoff.
- Artifact mismatch: Phase 2 must write source, tests, result, and refreshed
  Phase 3 subplan before handoff.

## Phase Execution Steps

1. Implement target builder.
2. Implement tiny nonlinear SSM fixture and deterministic filter fixture.
3. Add tests for shape, signature, authority, and fail-closed behavior.
4. Run local checks.
5. Write Phase 2 result.
6. Refresh and review Phase 3 subplan.

## End-Of-Subplan Closeout Requirements

The Phase 2 result must state the claimed target, computed quantity, equality
checks performed, unsupported claims, and Phase 3 handoff status.
