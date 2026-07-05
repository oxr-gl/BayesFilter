# Phase 5 Subplan: Fixed-Transport HMC Runtime Binding

Date: 2026-07-03

Status: `REVIEWED_READY_FOR_PHASE5_EXECUTION`

## Phase Objective

Bind generic SSM posterior adapters and frozen NeuTra transports to
BayesFilter-owned fixed-transport HMC target construction, existing HMC
policy/config binding, runtime diagnostics, and manifest emission. Phase 5 does
not tune a new HMC policy or change defaults.

Phase 5 uses the live Phase 4 loader/export boundary:

- `LoadedFrozenNeuTraArtifact`;
- `FrozenAffineDiagonalTransport`;
- `FrozenNeuTraArtifactManifest`;
- `load_frozen_neutra_artifact`;
- `stable_frozen_neutra_artifact_signature`;
- existing `FixedTransportValueScoreAdapter` and
  `reviewed_value_score_target_fn`.

Phase 4 result anchor:
`docs/plans/bayesfilter-general-neutra-ssm-interface-phase4-neutra-artifacts-result-2026-07-03.md`.

## Entry Conditions Inherited From Previous Phase

- Phase 4 result states `PHASE4_GATE_PASSED`.
- Frozen transport loader and target adapter tests pass.
- Phase 5 subplan has been refreshed and reviewed.

Concrete inherited Phase 4 decisions Phase 5 must preserve:

- Loader correctness, artifact availability, and sampler validity are separate
  ledgers.
- Only synthetic artifacts have been loaded; real artifact reuse remains
  unchecked.
- Fixed-transport wrapper authority must not promote fallback base authority.
- CPU-only HMC mechanics tests must be explicitly labeled and cannot support
  convergence or production-readiness claims.

## Required Artifacts

- Source module or extension:
  `bayesfilter/inference/fixed_transport_hmc.py`
- Focused tests:
  `tests/test_fixed_transport_hmc_binding.py`
- Phase 5 result:
  `docs/plans/bayesfilter-general-neutra-ssm-interface-phase5-hmc-binding-result-2026-07-03.md`
- Refreshed Phase 6 subplan.

## Required Checks, Tests, And Reviews

Local checks:

- `python -m pytest tests/test_fixed_transport_hmc_binding.py tests/test_batched_value_score.py -q -p no:cacheprovider`
- Tiny CPU-only HMC fixture is allowed only as a mechanics test and must state
  CPU-only status.
- Runtime manifest records target signature, transport hash, HMC policy label,
  HMC policy hash, XLA flag, mass policy, seed, and nonclaims.
- Tests must reject fallback value/score authority for any XLA-HMC-ready binding.
- Tests must distinguish target-construction mechanics from sampler convergence
  evidence.

Review:

- Claude read-only review of Phase 6 subplan.
- Claude review of HMC binding source if it changes HMC authority semantics.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a generic frozen-transport target be passed to BayesFilter HMC with complete target/transport/HMC manifests and fail-closed authority checks? |
| Baseline/comparator | Existing HMC target construction and fixed-transport value/score adapter. |
| Primary pass criterion | Tiny CPU-only fixture HMC mechanics test passes, manifest fields are complete, the runtime label states CPU-only mechanics smoke, and fallback value/score authority cannot enter XLA HMC. |
| Veto diagnostics | Missing target signature, missing transport hash, missing HMC policy label/hash, silent scalar target fallback, fallback authority promoted to XLA, or unlabeled CPU-only run. |
| Explanatory diagnostics | Acceptance, step size, leapfrog count, short-chain samples, and runtime. |
| Not concluded | No serious HMC convergence, no default sampler readiness, no real-artifact reuse success, no performance claim. |
| Artifacts | HMC binding source, tests, Phase 5 result. |

## Forbidden Claims And Actions

- Do not run serious HMC ladders.
- Do not interpret tiny chains as convergence.
- Do not run GPU HMC without trusted-context approval and a reviewed subplan.
- Do not change default HMC policy.
- Do not claim acceptance, short-chain samples, or finite mechanics output imply
  convergence.

## Exact Next-Phase Handoff Conditions

Phase 6 may begin only if:

- fixed-transport HMC binding tests pass;
- Phase 5 result states `PHASE5_GATE_PASSED`;
- runtime manifests distinguish mechanics smoke from serious HMC evidence;
- result inference-status table states that any ranking/convergence claim is not
  supported;
- Phase 6 subplan is refreshed and reviewed.

## Stop Conditions

Stop if:

- HMC runtime cannot consume the fixed-transport adapter without weakening
  value/score authority;
- manifest coverage is incomplete;
- a required check would become a serious stochastic comparison without a new
  evidence plan.
- CPU-only smoke output is tempting to use as promotion evidence rather than
  mechanics-only evidence.

## Skeptical Plan Audit

Status: `PASSED_FOR_PHASE5_EXECUTION_AFTER_REVIEW`

Checked risks:

- Wrong baseline: Phase 5 uses existing HMC target construction and
  fixed-transport adapter mechanics, not real NeuTra artifacts or new tuning
  policy selection.
- Proxy metrics: acceptance, short-chain samples, finite values, and runtime are
  explanatory only unless a later reviewed serious HMC plan promotes them.
- Missing stop conditions: authority weakening, manifest incompleteness,
  serious-comparison drift, and CPU-smoke overinterpretation are explicit stops.
- Hidden assumptions: CPU-only mechanics status and nonclaims must be recorded
  in the runtime manifest.
- Artifact mismatch: Phase 5 must write source/tests/result and refreshed Phase
  6 subplan before handoff.

## Phase Execution Steps

1. Implement fixed-transport HMC binding.
2. Add tiny deterministic fixture tests.
3. Run local checks.
4. Write Phase 5 result.
5. Refresh and review Phase 6 subplan.

## End-Of-Subplan Closeout Requirements

The result must include run manifest fields and state explicitly what the tiny
HMC smoke does and does not prove.
