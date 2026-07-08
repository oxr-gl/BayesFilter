# BayesFilter NeuTra c603 Integration Phase 2 Subplan

Date: 2026-07-06

## Phase Objective

Add a repeatable c603 fixture test path that uses the Phase 1 adapter to
reproduce the validated import, loader acceptance, payload/hash identity, and
legacy forward/logdet tie-out from a documented local dsge_hmc handoff checkout.

## Entry Conditions Inherited From Previous Phase

- Phase 1 adapter exists and passes focused unit tests.
- The adapter preserves c603 component order and mixing/affine orientation.
- The expected c603 target signature remains unchanged:
  `8f5caae87797898bd8d4f0c795246f5103e3535e247a49e5ebf01217ece20d07`.
- The validated local handoff root is expected at
  `/tmp/dsge_hmc-neutra-handoff-20260705` unless
  `BAYESFILTER_DSGE_HMC_HANDOFF_ROOT` points elsewhere.

## Required Artifacts

- c603 fixture helper or test-local fixture under `tests/`.
- Focused c603 import test, expected location:
  `tests/test_neutra_c603_import_fixture.py`.
- Phase 2 result note:
  `docs/plans/bayesfilter-neutra-c603-integration-phase2-c603-fixture-tests-result-2026-07-06.md`.
- Phase 3 refreshed subplan.

## Required Checks, Tests, Reviews

- CPU-only pytest:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_neutra_c603_import_fixture.py tests/test_legacy_neutra_import.py tests/test_dense_iaf_neutra_artifact_loader.py -q -p no:cacheprovider`
- Verify the fixture uses a documented local handoff checkout rooted at
  `BAYESFILTER_DSGE_HMC_HANDOFF_ROOT` or the reviewed default
  `/tmp/dsge_hmc-neutra-handoff-20260705`.
- Verify the test does not fetch from network and does not import live
  `dsge_hmc` Python modules.
- Verify the test checks the three c603 file SHA-256 digests declared in the
  handoff follow-up.
- Verify the loaded payload carries the reviewed Phase 1 target-signature
  constant and reproduces the validated transport/artifact hashes.
- Review if fixture design adds large files, hidden external dependencies, or
  broad public API.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the c603 import validation be reproduced by ordinary BayesFilter tests without one-off manual scripts? |
| Baseline/comparator | Manual c603 validation result and Phase 1 adapter tests. |
| Primary criterion | Test verifies the local c603 handoff file hashes, builds the payload with the Phase 1 adapter, finalizes and loads it against the reviewed target-signature constant, reproduces the validated topology/tensor/transport/artifact hashes, and matches a direct legacy forward/logdet replay to declared tolerance. |
| Veto diagnostics | Network-required test, missing c603 handoff files, SHA-256 mismatch, hidden process-local identity, tolerance failure, loader bypass, or GPU/training/HMC requirement. |
| Explanatory diagnostics | Runtime, TensorFlow CPU warnings, component order, topology/tensor/transport hashes, artifact signature. |
| Not concluded | No generic `SSMTargetContract` reconstruction claim from this fixture alone, no HMC quality, no posterior correctness, no production readiness. |
| Artifact | Phase 2 result note plus test logs. |

## Forbidden Claims/Actions

- Do not add large generated payloads to the repo without a reviewed storage
  decision.
- Do not make c603 fixture tests depend on live dsge_hmc network fetch by
  default.
- Do not silently treat the local handoff checkout as a tracked BayesFilter repo
  artifact.
- Do not claim that this fixture reconstructs the generic c603 target contract
  from first principles unless that reconstruction is explicitly tested.
- Do not promote fixture pass to scientific validity.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if:

- c603 fixture test passes CPU-only;
- fixture dependency path is documented and explicit;
- the result note distinguishes the reviewed target-signature constant from any
  future generic target-contract reconstruction work;
- Phase 2 result records nonclaims and any storage/runtime tradeoff;
- Phase 3 mechanics subplan names the exact loaded artifact source.

## Stop Conditions

Stop if:

- the fixture cannot be made deterministic and local enough for tests;
- importing c603 requires committing oversized artifacts without approval;
- the local handoff checkout is absent or its payload hashes do not match the
  reviewed follow-up evidence;
- the legacy tie-out fails;
- review does not converge after five rounds for the same material blocker.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 2 result;
3. draft or refresh Phase 3 subplan;
4. review Phase 3 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
