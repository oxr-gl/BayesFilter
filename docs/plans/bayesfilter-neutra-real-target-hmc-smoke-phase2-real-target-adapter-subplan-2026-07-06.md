# BayesFilter NeuTra Real Target HMC Smoke Phase 2 Subplan

Date: 2026-07-06

## Phase Objective

Build or fail-closed document the c603 adapter-authority bridge needed before
real-target mechanics. Phase 1 classified the current state as `design_only`:
BayesFilter has c603 transport/signature evidence and generic adapter surfaces,
but no live BayesFilter-owned c603 Rotemberg prior/model/filter value-score
callables.

`design_only` authorizes only a source-anchored bridge attempt. It does not
authorize real-target mechanics, HMC, GPU, training, or treating `dsge_hmc`
runtime modules as BayesFilter authority.

## Entry Conditions Inherited From Previous Phase

- Phase 1 result exists and classifies the next boundary as `design_only`.
- The c603 frozen transport import remains validated against target signature
  `8f5caae87797898bd8d4f0c795246f5103e3535e247a49e5ebf01217ece20d07`.
- The Phase 1 inventory did not authorize real-target mechanics, HMC, GPU, or
  training.

## Required Artifacts

- Minimal adapter-authority bridge code or blocker note.
- Focused tests if code is added.
- If code is added, a small source-authority note or manifest that maps each
  BayesFilter callable to the exact handoff source anchor it implements.
- Phase 2 result:
  `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase2-real-target-adapter-result-2026-07-06.md`.
- Refreshed Phase 3 subplan.

## Required Checks/Tests/Reviews

- Read-only source-anchor check against the c603 handoff proposal/preflight and
  local BayesFilter APIs before editing code.
- If code is added, CPU-only focused pytest for:
  - contract signature reconstruction;
  - batch-native finite value/score shape checks;
  - fail-closed missing-source or shape mismatch cases;
  - no HMC/GPU/training side effects.
- Bounded Claude read-only review of implementation or blocker result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter expose a real c603 target adapter with batch-native finite value/score under reviewed authority? |
| Baseline/comparator | Phase 1 `design_only` classification, c603 proposal/preflight, `GenericSSMPosteriorAdapter`, and existing BayesFilter batch SVD sigma-point APIs. |
| Primary criterion | Either a reviewed adapter-authority bridge emits finite rank-2 values/scores with the c603 target signature, or a blocker records the exact missing port/source/runtime authority. |
| Veto diagnostics | Synthetic target mislabeled real, dsge_hmc runtime import treated as BayesFilter authority, unreviewed GradientTape fallback promoted, nonfinite values/scores, target-signature mismatch, HMC/GPU/training launch. |
| Explanatory diagnostics | Value/score shape, adapter signature, c603 target signature, source anchors, finite probes. |
| Not concluded | No HMC convergence, no posterior correctness, no production readiness. |
| Artifact | Phase 2 result and tests/blocker. |

## Required Source-Authority Bridge Pieces

Phase 2 may proceed only against these source anchors:

- c603 model/derivative builder:
  `/tmp/dsge_hmc-neutra-handoff-20260705/scripts/prepare_neutra_rotemberg_second_order_svd_target.py:305-319`;
- c603 analytical prior value/score:
  `/tmp/dsge_hmc-neutra-handoff-20260705/scripts/prepare_neutra_rotemberg_second_order_svd_target.py:321-323`;
- c603 posterior call-path identity:
  `/tmp/dsge_hmc-neutra-handoff-20260705/scripts/prepare_neutra_rotemberg_second_order_svd_target.py:447-459`;
- BayesFilter batch principal-sqrt value/score candidate:
  `bayesfilter/nonlinear/experimental_batched_svd_sigma_point_tf.py:1271`.

If those anchors are insufficient to reconstruct a local BayesFilter callable
without live external runtime imports, Phase 2 must write
`blocked_missing_portable_real_target_authority` and stop.

## Forbidden Claims/Actions

- Do not run HMC.
- Do not call synthetic fixtures real target adapters.
- Do not import or execute live `dsge_hmc` modules as BayesFilter target
  authority unless a separately reviewed source-port boundary approves it.
- Do not use unreviewed GradientTape fallback as XLA/HMC authority.
- Do not run GPU/CUDA jobs, training, package installation, or git commit/push.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if a real adapter boundary passes focused tests and
records target signature, adapter signature, source authority, finite
value/score probes, and explicit nonclaims. If Phase 2 records a blocker, Phase
3 must be refreshed as closeout/blocker handling rather than mechanics.

## Stop Conditions

Stop if the only available target is synthetic, if prior/model/filter
value-score authority cannot be ported without inventing fields, if the target
signature changes without explanation, if finite probes fail, or if review does
not converge after five rounds for the same material blocker.

Also stop if Phase 2 would require a package install, model-file fetch,
unreviewed `dsge_hmc` runtime dependency, GPU/CUDA execution, training, or HMC
to establish the adapter boundary.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 2 result;
3. draft or refresh Phase 3 subplan;
4. review Phase 3 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
