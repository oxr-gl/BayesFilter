# Phase 4 Subplan: Frozen NeuTra Transport Artifact Loader

Date: 2026-07-03

Status: `REVIEWED_READY_FOR_PHASE4_EXECUTION`

## Phase Objective

Add a BayesFilter-owned frozen transport protocol and artifact loader that can
load reviewed NeuTra training-state JSON payloads as frozen transports only
after schema, dimension, target signature, and transport manifest checks pass.

Phase 4 uses live Phase 1/3 public export boundaries:

- `FrozenTransportBinding` and `stable_ssm_target_signature` from
  `bayesfilter/ssm/__init__.py`;
- `FilterProgramDescriptor`, `FilterProgramRegistry`, and
  `build_filter_program_registry` from `bayesfilter/ssm/__init__.py`;
- existing `FixedTransportValueScoreAdapter` behavior in
  `bayesfilter/inference/batched_value_score.py`.

Phase 3 result anchor:
`docs/plans/bayesfilter-general-neutra-ssm-interface-phase3-filter-registry-result-2026-07-03.md`.

## Entry Conditions Inherited From Previous Phase

- Phase 3 result states `PHASE3_GATE_PASSED`.
- Generic target builder and filter registry exist.
- Phase 4 subplan has been refreshed and reviewed.

Concrete inherited Phase 3 decisions Phase 4 must preserve:

- Registry decisions are admissibility/manifest decisions only, not filter
  correctness or sampler-readiness evidence.
- Frozen transport target-signature binding must use Phase 1 target signatures.
- Loader correctness, artifact availability, and sampler validity remain
  separate ledgers.
- CPU-only loader checks must not be reported as GPU training evidence.

## Required Artifacts

- Source module:
  `bayesfilter/inference/neutra_artifacts.py`
- Export refresh if public:
  `bayesfilter/inference/__init__.py`
- Optional transport protocol refinements in:
  `bayesfilter/inference/batched_value_score.py`
- Focused tests:
  `tests/test_neutra_artifact_loader.py`
- Phase 4 result:
  `docs/plans/bayesfilter-general-neutra-ssm-interface-phase4-neutra-artifacts-result-2026-07-03.md`
- Refreshed Phase 5 subplan.

## Required Checks, Tests, And Reviews

Local checks:

- `python -m pytest tests/test_neutra_artifact_loader.py tests/test_batched_value_score.py -q -p no:cacheprovider`
- Loader rejects missing schema, wrong dimension, unsupported transport blocks,
  and target-signature mismatch.
- Loader accepts a small synthetic frozen transport fixture.
- Loader creates or validates a `FrozenTransportBinding`-compatible manifest
  without requiring model-specific training code.
- Existing `FixedTransportValueScoreAdapter` tests remain green if touched.

Review:

- Claude read-only review of Phase 5 subplan.
- Claude source review if the loader accepts real external artifact formats.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter represent frozen NeuTra transports as reusable target transforms without retraining or weakening target authority? |
| Baseline/comparator | Existing `FixedTransportValueScoreAdapter` chain-rule behavior and existing DSGE training-state summaries. |
| Primary pass criterion | Synthetic artifact loads to a stable frozen transport manifest; mismatches fail closed; fixed transport wrapper preserves base value/score authority. |
| Veto diagnostics | Loader silently ignores target mismatch, reconstructs process-local signatures, accepts missing log-Jacobian, imports large model-specific training code into BayesFilter, promotes fallback base authority, or claims training success from loader checks. |
| Explanatory diagnostics | Transport manifest hash, loader schema fields, and synthetic roundtrip error. |
| Not concluded | No real artifact availability, no HMC tuning, no posterior convergence, no NeuTra training readiness. |
| Artifacts | Loader module, tests, Phase 4 result. |

## Forbidden Claims And Actions

- Do not train NeuTra.
- Do not commit large generated training JSON payloads.
- Do not load real artifacts as proof of sampler validity.
- Do not use CPU-only loader checks as GPU/training evidence.
- Do not import external model packages or `~/python` training modules into
  BayesFilter loader code.
- Do not add real external artifacts unless they are tiny, reviewed, and
  signature-bound.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin only if:

- loader and fixed-transport tests pass;
- Phase 4 result states `PHASE4_GATE_PASSED`;
- transport manifests bind to target signatures or explicitly record missing
  signature as non-reusable;
- Phase 5 subplan is refreshed and reviewed.

## Stop Conditions

Stop if:

- existing DSGE artifact format cannot be parsed without importing large
  model-specific training code into BayesFilter;
- target signature binding is absent and no safe non-reuse policy exists;
- efficient score pullback API needs a design decision beyond this phase.
- parsing real existing artifacts would require network access, package
  installation, model-specific imports, or large-file commits.

## Skeptical Plan Audit

Status: `PASSED_FOR_PHASE4_EXECUTION_AFTER_REVIEW`

Checked risks:

- Wrong baseline: Phase 4 uses synthetic artifact loader checks and existing
  fixed-transport wrapper behavior, not NeuTra sampler performance.
- Proxy metrics: roundtrip error and manifest hash are loader diagnostics only,
  not training success or posterior validity evidence.
- Missing stop conditions: target-signature absence, large/model-specific
  imports, score-pullback design needs, and real-artifact parsing boundaries are
  explicit stops.
- Hidden assumptions: loader correctness is separate from artifact availability
  and sampler validity.
- Artifact mismatch: Phase 4 must write source, tests, result, and refreshed
  Phase 5 subplan before handoff.

## Phase Execution Steps

1. Define frozen transport protocol/loader.
2. Add synthetic artifact fixtures.
3. Add fail-closed tests.
4. Run local checks.
5. Write Phase 4 result.
6. Refresh and review Phase 5 subplan.

## End-Of-Subplan Closeout Requirements

The result must separate loader correctness, artifact availability, and sampler
validity as distinct ledgers.
