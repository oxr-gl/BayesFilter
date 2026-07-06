# BayesFilter NeuTra c603 Integration Phase 3 Subplan

Date: 2026-07-06

## Phase Objective

Run mechanics-only fixed-transport checks using the loaded c603 frozen dense-IAF
artifact and a reviewed value/score fixture or adapter boundary.

## Entry Conditions Inherited From Previous Phase

- Phase 2 c603 fixture import test passes CPU-only.
- The loaded artifact carries the expected c603 target signature and stable
  transport hashes.
- The mechanics target is explicitly classified as fixture/mechanics-only or
  reviewed target-adapter work.
- The exact Phase 2 local artifact source is the reviewed handoff checkout at
  `BAYESFILTER_DSGE_HMC_HANDOFF_ROOT` or the default
  `/tmp/dsge_hmc-neutra-handoff-20260705`, loaded through
  `tests/test_neutra_c603_import_fixture.py` semantics.

## Required Artifacts

- Mechanics smoke test or diagnostic, expected location:
  `tests/test_fixed_transport_hmc_binding_c603_fixture.py`.
- Phase 3 result note:
  `docs/plans/bayesfilter-neutra-c603-integration-phase3-fixed-transport-mechanics-result-2026-07-06.md`.
- Phase 4 refreshed subplan.

## Required Checks, Tests, Reviews

- CPU-only focused pytest or diagnostic using
  `bind_fixed_transport_hmc_mechanics`, expected command:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_fixed_transport_hmc_binding_c603_fixture.py tests/test_fixed_transport_hmc_binding.py tests/test_neutra_c603_import_fixture.py -q -p no:cacheprovider`
- Confirm finite transformed value/score and manifest nonclaims.
- Confirm no chain sampling, no long HMC, no GPU, and no HMC readiness claim.
- Confirm the mechanics test uses a fixture base adapter only unless a reviewed
  real Rotemberg value/score adapter is introduced.
- Review if a real Rotemberg value/score adapter is introduced.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the loaded c603 frozen transport participate in BayesFilter fixed-transport mechanics surfaces without running HMC sampling? |
| Baseline/comparator | Existing toy fixed-transport mechanics tests and Phase 2 loaded c603 artifact. |
| Primary criterion | Mechanics binding emits finite value/score and a manifest preserving the c603 target signature, c603 transport hash, and mechanics-only nonclaims when paired with a reviewed fixture base adapter. |
| Veto diagnostics | HMC chain sampling, GPU dependence, fallback authority promoted to XLA/HMC readiness, nonfinite values/scores, signature mismatch, or silent drift away from the reviewed Phase 2 c603 loaded artifact source. |
| Explanatory diagnostics | Runtime, manifest signature, policy hash, finite tensors, chain-rule spot checks. |
| Not concluded | No HMC convergence, no sampler tuning success, no Rotemberg posterior correctness, no production readiness. |
| Artifact | Phase 3 result note plus test/diagnostic log. |

## Forbidden Claims/Actions

- Do not run long HMC or training.
- Do not treat mechanics-only success as sampler validity.
- Do not promote fallback value/score authority.
- Do not change default HMC policy.
- Do not describe a synthetic/quadratic/base fixture adapter as a real Rotemberg
  target adapter.

## Exact Next-Phase Handoff Conditions

Phase 4 may begin only if:

- mechanics smoke passes;
- result note states mechanics-only target and computed quantities;
- result note names the exact c603 loaded artifact source and any synthetic base
  adapter boundary;
- any target-adapter limitations are recorded;
- generic interface subplan is refreshed with the actual learned boundaries.

## Stop Conditions

Stop if:

- mechanics requires unreviewed target authority;
- finite value/score cannot be produced;
- the work would become real HMC sampling without approval;
- review does not converge after five rounds for the same material blocker.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 3 result;
3. draft or refresh Phase 4 subplan;
4. review Phase 4 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
