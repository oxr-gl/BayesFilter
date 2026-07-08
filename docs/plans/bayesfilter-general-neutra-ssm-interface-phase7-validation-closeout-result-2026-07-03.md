# Phase 7 Result: Validation Ladder And Closeout

Date: 2026-07-03

Status: `MASTER_PROGRAM_CLOSED_WITH_REAL_ARTIFACT_MIGRATION_BLOCKED`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | What level of evidence does the generic NeuTra SSM interface have after implementation and fail-closed real-artifact inventory? |
| Baseline/comparator | Phase-by-phase gates and focused tests, not method-performance comparisons. |
| Primary criterion | Passed: focused tests passed, validation ledger classifies every rung, and the closeout separates implemented surfaces from blocked real-artifact migration. |
| Veto diagnostics | No Phase 7 veto fired. Real artifacts are not described as reusable; no serious HMC/training/default-readiness claim was made. |
| Explanatory diagnostics | `44` focused tests passed under intentional CPU-only/GPU-hidden execution. Phase 6 classified `0` external artifacts as reusable. |
| Not concluded | No real-artifact reuse, no sampler superiority, no broad posterior correctness, no scientific claim, no all-filter HMC readiness, and no default product change. |
| Artifacts | `docs/plans/bayesfilter-general-neutra-ssm-interface-phase7-validation-ledger-2026-07-03.json` and this closeout. |

## What Is Implemented

The generic interface now has these BayesFilter-owned surfaces:

- `bayesfilter.ssm.contracts`: generic Bayesian SSM target identity,
  parameter chart, prior, filter program, frozen transport binding, stable
  signatures, and fail-closed validation.
- `bayesfilter.ssm.target_builder`: batch-native TensorFlow posterior
  value/score adapter for deterministic prior plus filter likelihood functions.
- `bayesfilter.ssm.filter_registry`: metadata registry for deciding whether a
  model/filter pair is admissible for a deterministic HMC target.
- `bayesfilter.inference.neutra_artifacts`: reviewed synthetic frozen
  affine-diagonal transport loader with target-signature binding.
- `bayesfilter.inference.fixed_transport_hmc`: mechanics-only fixed-transport
  HMC manifest binding over an existing value/score adapter.

## What Passed

Focused validation passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_general_ssm_contracts.py tests/test_general_ssm_target_builder.py tests/test_general_ssm_filter_registry.py tests/test_neutra_artifact_loader.py tests/test_fixed_transport_hmc_binding.py -q -p no:cacheprovider
44 passed in 6.66s
```

CPU hiding was intentional for these contract, loader, and mechanics checks.
No GPU/CUDA device was detected, initialized, benchmarked, or used in Phase 7.

The implemented checks cover:

- stable target and adapter signatures;
- process-local identity rejection;
- batch-native `[B, D]` target value/score behavior;
- rank-1 `[D]` target rejection;
- deterministic/fixed-randomness filter capability gates;
- synthetic frozen transport loader fail-closed behavior;
- fixed-transport mechanics manifest fields and fallback-authority rejection
  for XLA binding.

## Real-Artifact Status

Phase 6 found and classified the user-named historical NeuTra cells:

| Cell | Candidate | Step | L | Max R-hat | Phase 6 loader status |
| --- | ---: | ---: | ---: | ---: | --- |
| NK + linear solver + Kalman | 45 | 0.5 | 4 | 1.0007741578596723 | `signature_not_available_nonreusable` |
| NK + linear solver + principal-sqrt UKF | 44 | 0.5 | 3 | n/a | `signature_not_available_nonreusable` |
| Rotemberg + linear solver + KF | 46 | 0.5 | 8 | 1.0018239461076908 | `missing_payload` |
| Rotemberg + linear solver + pruned UKF | 92 | 1.03125 | 3 | 1.1364772795911446 | `missing_payload` |
| Rotemberg + second solver + pruned UKF | 603 | 0.729166666666 | 2 | 1.0032378500239167 | `missing_payload` |

These are real historical evidence cells and should be reused as design input.
They are not yet reusable by the new generic loader because checked artifacts
lack the reviewed loader schema and generic target signature, and some
referenced training-state payloads are absent.

## Decision Table

| Decision field | Status |
| --- | --- |
| Program decision | Close this master program as an implemented generic interface scaffold with real-artifact migration blocked. |
| Primary criterion | Passed for implementation and focused validation scope. |
| Veto diagnostic status | No active Phase 7 veto. Phase 6 real-artifact reuse veto is preserved. |
| Main uncertainty | Dense IAF artifact schema/export and target-signature migration remain unresolved. |
| Next justified action | Start a separate migration program for dense IAF frozen transport export, target-signature bridging, and restored payload hashing before any real-artifact mechanics canary. |
| What is not concluded | No real-artifact loader reuse, HMC convergence, posterior correctness, method superiority, all-filter readiness, or default-policy change. |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for focused interface tests; real-artifact reuse remains blocked, not promoted. |
| Statistically supported ranking | None. No stochastic comparison was run in this master program. |
| Descriptive-only differences | Historical R-hat/ESS/acceptance/candidate diagnostics remain descriptive unless governed by their source runbooks. |
| Default-readiness | Not established. |
| Next evidence needed | Dense-IAF loader/export schema, target-signature bridge, restored payload hashes, then a reviewed real-artifact mechanics canary and separate serious HMC plan. |

## Post-Run Red Team

Strongest alternative explanation:

- The generic interface tests pass because they use deterministic toy and
  synthetic affine-diagonal fixtures. That does not imply dense IAF artifacts or
  real nonlinear SSM filters are already integrated.

What would overturn this closeout:

- A focused test failure in the implemented surfaces, a discovered path that
  silently loads signature-absent external artifacts, or evidence that the
  public API exports differ from the result artifacts.

Weakest evidence:

- Real-artifact migration. Phase 6 found the intended historical evidence
  cells, but the old artifact format is not yet the new generic BayesFilter
  frozen-transport format.

## Required Follow-Up Program

The next program should be a migration bridge, not a rerun of this scaffold:

- define a dense IAF frozen-transport schema or exporter;
- bind old target identities to `SSMTargetContract` manifests and stable target
  signatures;
- restore or re-export missing training-state payloads with SHA-256 checks;
- add loader tests for dense IAF log-Jacobian and inverse/forward semantics;
- only then run a reviewed real-artifact load/value/mechanics canary.

`MASTER_PROGRAM_CLOSED_WITH_REAL_ARTIFACT_MIGRATION_BLOCKED`
