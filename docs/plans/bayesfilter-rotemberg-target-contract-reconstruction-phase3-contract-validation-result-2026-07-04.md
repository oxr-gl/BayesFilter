# Phase 3 Result: Local `SSMTargetContract` Validation

Date: 2026-07-04

Status: `PHASE3_GATE_PASSED_LOCAL_VALIDATION`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the Phase 2 manifest be instantiated into a valid local `SSMTargetContract` with stable signatures and fail-closed checks? |
| Baseline/comparator | Phase 2 manifest JSON and the existing `bayesfilter.ssm.contracts` test suite. |
| Primary pass criterion | Contract instantiation succeeds with `frozen_transport=None`, stable signature generation succeeds, and targeted contract tests pass without loosening fail-closed checks. |
| Veto diagnostics | Unsupported or invented field, process-local identity, contract mismatch, unstable signature, accidental transport binding, or any HMC/payload/export claim. |
| Explanatory diagnostics | Signature string, manifest payload hash, contract field values, and test output. |
| Not concluded | Real-artifact load, payload export, HMC convergence, posterior correctness, sampler superiority, GPU readiness, or default policy change. |
| Result artifact | This file plus focused test output. |

## Decision

The Phase 2 Rotemberg manifest draft instantiates cleanly into a local
`SSMTargetContract` with `frozen_transport=None`. The resulting contract has a
stable 64-character SHA-256 target signature, preserves the reviewed
`state_dim=6` decision, and keeps `structural_state_dim=4` as model metadata.

The local contract checks and adjacent generic contract regressions passed
under deliberate CPU-only execution.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `99263ff22d11128a61c35668c7b530d870f91397` |
| Worktree state | Dirty; unrelated user changes preserved. |
| Command | `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_rotemberg_target_contract_reconstruction_phase3.py tests/test_general_ssm_contracts.py tests/test_general_ssm_filter_registry.py tests/test_neutra_artifact_loader.py -q -p no:cacheprovider` |
| Environment | Current BayesFilter shell. |
| CPU/GPU status | Deliberate CPU-only run with `CUDA_VISIBLE_DEVICES=-1` set before TensorFlow import. No GPU readiness claim. |
| Network status | No network fetch. |
| External mutation | None; `/home/chakwong/python` was not modified. |
| Output | `30 passed in 5.78s` |

## Checks

Commands:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_rotemberg_target_contract_reconstruction_phase3.py tests/test_general_ssm_contracts.py tests/test_general_ssm_filter_registry.py tests/test_neutra_artifact_loader.py -q -p no:cacheprovider
git diff --check -- tests/test_rotemberg_target_contract_reconstruction_phase3.py docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase3-contract-validation-subplan-2026-07-04.md docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase3-contract-validation-result-2026-07-04.md docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase4-bridge-rerun-subplan-2026-07-04.md
python -m json.tool docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase2-contract-manifest-2026-07-04.json
```

Result:

- Passed.

## Plain-Language Classification

| Statement | Classification | Support |
| --- | --- | --- |
| The manifest instantiates into a valid local `SSMTargetContract`. | `correct` | Focused tests passed. |
| The manifest preserves the reviewed state-dimension split. | `correct` | Contract checks and manifest inspection. |
| The contract proves payload reuse or bridge success. | `wrong relative to the stated target` | No bridge/load phase has run. |
| The contract proves HMC readiness or posterior correctness. | `unsupported` | No HMC/posterior run was performed. |

## Decision Table

| Decision field | Status |
| --- | --- |
| Primary criterion | Passed. |
| Veto diagnostic status | No Phase 3 stop condition fired. |
| Main uncertainty | Whether any historical embedded dense-IAF candidate can now be bridged using this validated manifest. |
| Next justified action | Phase 4 bridge rerun and payload boundary decision. |
| What is not concluded | No real-artifact load, no payload export, no HMC/posterior claim. |

`PHASE3_GATE_PASSED_LOCAL_VALIDATION`
