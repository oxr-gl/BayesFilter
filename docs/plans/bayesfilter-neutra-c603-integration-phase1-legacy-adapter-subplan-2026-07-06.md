# BayesFilter NeuTra c603 Integration Phase 1 Subplan

Date: 2026-07-06

## Phase Objective

Implement a small BayesFilter-owned legacy dsge_hmc dense-IAF transport-state
adapter that converts reviewed legacy `transport_state` dictionaries into
`bayesfilter.neutra.dense_iaf_frozen_transport.v1` payloads.

## Entry Conditions Inherited From Previous Phase

- Phase 0 launch contract passed or has an explicitly accepted weak review
  substitute.
- c603 target signature remains
  `8f5caae87797898bd8d4f0c795246f5103e3535e247a49e5ebf01217ece20d07`.
- c603 payload hashes have been verified at the dsge_hmc follow-up commit.
- CPU-only import validation has already shown manual conversion can match
  legacy forward/logdet to roundoff.

## Required Artifacts

- Adapter source file, expected location:
  `bayesfilter/inference/legacy_neutra_import.py`.
- Public import wiring in `bayesfilter/inference/__init__.py` if the helper is
  meant to be public.
- Focused tests, expected location:
  `tests/test_legacy_neutra_import.py`.
- Phase 1 result note:
  `docs/plans/bayesfilter-neutra-c603-integration-phase1-legacy-adapter-result-2026-07-06.md`.
- Phase 2 refreshed subplan.

## Required Checks, Tests, Reviews

- CPU-only pytest:
  `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_legacy_neutra_import.py tests/test_dense_iaf_neutra_artifact_loader.py -q -p no:cacheprovider`
- Static/text checks:
  - adapter rejects unsupported component kinds;
  - adapter rejects nonfinite tensors;
  - adapter rejects legacy dense IAF `s_max != 1.0` unless a reviewed
    derivation/test is added;
  - tests cover mixing matrix transposition.
- Read-only review of material implementation or result when Phase 1 changes
  public API or claim boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter own the c603 legacy transport-state conversion with fail-closed semantics? |
| Baseline/comparator | Manual c603 conversion and existing BayesFilter dense-IAF loader behavior. |
| Primary criterion | Adapter-generated payload finalizes and loads with the expected target signature, and tests prove the orientation and rejection rules. |
| Veto diagnostics | Unknown component accepted, nonfinite tensor accepted, `s_max != 1.0` accepted without proof, mixing orientation mismatch, process-local identity, or loader bypass. |
| Explanatory diagnostics | Stable hashes, component order, artifact signature, finite smoke outputs. |
| Not concluded | No posterior correctness, no HMC readiness, no production readiness, no general legacy payload support beyond tested semantics. |
| Artifact | Phase 1 result note plus test logs. |

## Forbidden Claims/Actions

- Do not claim the adapter supports arbitrary dsge_hmc transports.
- Do not bypass `finalize_dense_iaf_neutra_artifact_payload` or
  `load_frozen_neutra_artifact`.
- Do not run training, long HMC, or GPU jobs.
- Do not silently change BayesFilter dense-IAF loader semantics.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if:

- adapter and tests exist;
- focused CPU-only tests pass;
- Phase 1 result records exact behavior and nonclaims;
- Phase 2 subplan is refreshed to use the adapter, not the one-off manual
  script.

## Stop Conditions

Stop and write a blocker result if:

- c603 conversion requires unsupported semantics not present in the loader;
- code would need a broad redesign of the dense-IAF loader;
- tests cannot run CPU-only;
- an unreviewed public API expansion is required;
- review does not converge after five rounds for the same material blocker.

## Phase Close Duties

At close:

1. run focused CPU-only tests;
2. write Phase 1 result;
3. draft or refresh Phase 2 subplan;
4. review Phase 2 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
