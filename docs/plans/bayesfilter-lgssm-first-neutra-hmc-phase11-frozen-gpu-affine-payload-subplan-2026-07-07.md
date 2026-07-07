# Phase 11 Subplan: Frozen GPU-Trained Affine Payload

Date: 2026-07-07

## Phase Objective

Package the Phase 10 GPU-trained LGSSM affine parameters into the existing
frozen affine NeuTra artifact schema, load the payload through
`load_frozen_neutra_artifact`, and run mechanics/reference checks that prove the
payload is structurally usable by the existing fixed-transport boundary.

This phase must not run new NeuTra training, HMC sampling, HMC tuning, external
sample generation, dense IAF training, XLA repair, route ranking, production
promotion, default-policy changes, or scientific promotion.

## Entry Conditions Inherited From Previous Phase

- Phase 10 passed bounded GPU affine NeuTra optimizer training for
  `lgssm-static-qr-exact-kalman`.
- Phase 10 wrote the GPU training-state artifact:
  `docs/plans/artifacts/lgssm-first-neutra-gpu-training-2026-07-07/lgssm_static_qr_exact_kalman_affine_neutra_gpu_training_state_seed20260707.json`.
- Phase 10 target signature:
  `290a91d2a8f90d5b29243965b258b1ec6fd965aa46ffca69dcb78f7fa1ecabcb`.
- Phase 10 adapter signature:
  `0a48b43d2750cad5b452708f7619a1119a259231d8955769809460f256575a97`.
- Phase 10 used trusted GPU execution with `jit_compile=false`, TF32 enabled,
  and no CPU fallback.
- Phase 9 XLA/JIT blocker remains open. Phase 11 must not claim XLA readiness
  or require `jit_compile=true`.
- No frozen transport payload was written in Phase 10.
- No HMC sampling/tuning or external sample generation has been authorized for
  Phase 11.
- External sample generation remains a separate multicore CPU phase.

## Required Artifacts

- Frozen affine payload JSON under:
  `docs/plans/artifacts/lgssm-first-neutra-gpu-training-2026-07-07/`
- Phase 11 validation JSON under:
  `docs/plans/artifacts/lgssm-first-neutra-gpu-training-2026-07-07/`
- Phase 11 result or blocker:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase11-frozen-gpu-affine-payload-result-2026-07-07.md`
- Updated or new focused tests covering:
  - training-state schema/input checks;
  - target-signature preservation;
  - frozen affine payload schema and loader compatibility;
  - finite transformed target value/score or mechanics-only diagnostics;
  - no-HMC/no-sample/no-training flags.
- Draft Phase 12 subplan for either:
  - XLA/JIT repair; or
  - CPU multicore external sample-generation separation; or
  - a reviewed fixed-transport HMC mechanics/smoke gate.

## Required Checks/Tests/Reviews

- CPU-safe artifact/loader tests must set `CUDA_VISIBLE_DEVICES=-1` before
  TensorFlow import.
- Run `python -m json.tool` on Phase 10 training-state JSON and any Phase 11
  generated JSON artifacts.
- Run focused pytest for the Phase 11 payload/loader tests.
- Run `python -m py_compile` on any new Phase 11 helper/test modules.
- Run `git diff --check` on Phase 11 code and artifacts.
- Bounded read-only review must inspect the Phase 11 result/blocker and Phase
  12 subplan before crossing into HMC sampling, sample generation, XLA repair,
  or additional training.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the Phase 10 GPU-trained affine parameters be packaged into BayesFilter's frozen affine transport schema and loaded/mechanics-checked without new training, HMC, or sample generation? |
| Baseline/comparator | Phase 5 fixed identity/affine transport mechanics and Phase 6 CPU affine payload schema, with Phase 10 GPU training state as the source of learned parameters. |
| Primary criterion | Frozen affine payload loads with the Phase 10 target signature, preserves finite forward/logdet behavior, and passes finite mechanics/reference checks against the LGSSM generic adapter. |
| Veto diagnostics | Missing Phase 10 training state, malformed schema, target-signature or adapter-signature mismatch, nonfinite payload tensors, loader failure, mechanics/reference failure, hidden training, hidden HMC sampling/tuning, hidden sample generation, XLA/JIT requirement, or unsupported readiness/scientific claim. |
| Explanatory diagnostics | Payload hash, loaded artifact signature, transport hash, value/score residuals, transformed target finite checks, and mechanics-only manifest fields. |
| Not concluded | Transport quality, posterior correctness, HMC readiness, XLA readiness, route superiority, production readiness, default execution readiness, or scientific validity. |
| Artifact | Phase 11 payload JSON, validation JSON, result/blocker, tests, and Phase 12 subplan. |

## Forbidden Claims/Actions

- Do not run new NeuTra training.
- Do not run CPU NeuTra training.
- Do not run HMC sampling or HMC tuning.
- Do not generate external samples.
- Do not train or package a dense IAF payload.
- Do not use DSGE/c603.
- Do not require or claim XLA/JIT readiness.
- Do not promote loss decrease, finite mechanics, or successful payload loading
  into posterior correctness, HMC readiness, production readiness, default
  execution readiness, route superiority, or scientific validity.
- Do not overwrite Phase 10 training-state evidence except through an explicit
  reviewed rerun plan.

## Exact Next-Phase Handoff Conditions

Phase 12 may begin only if:

- Phase 11 records pass/blocker with a result artifact;
- the frozen affine payload JSON and validation JSON are schema-checked and
  below repository size policy;
- the payload loads through `load_frozen_neutra_artifact` with the exact Phase
  10 target signature;
- the validation records the exact Phase 10 adapter signature or writes a
  blocker explaining any mismatch;
- finite forward/logdet and mechanics/reference diagnostics are recorded or the
  blocker explains the failure;
- no new training, HMC sampling/tuning, XLA/JIT repair, or external sample
  generation occurred;
- a Phase 12 subplan states whether the next step is XLA repair, CPU multicore
  external sample-generation separation, or a reviewed fixed-transport HMC
  mechanics/smoke gate;
- bounded read-only review agrees with the Phase 12 boundary.

## Stop Conditions

Stop if:

- the Phase 10 training-state artifact is missing or malformed;
- target signature or adapter signature does not match Phase 10;
- payload tensors are nonfinite;
- `load_frozen_neutra_artifact` rejects the payload;
- transformed target value/score or mechanics-only diagnostics are nonfinite;
- HMC sampling/tuning, sample generation, XLA/JIT repair, or new training
  becomes necessary to proceed;
- artifact sizes violate repository policy;
- review does not converge after five rounds.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 11 result or blocker;
3. draft or refresh the Phase 12 subplan;
4. review the Phase 12 subplan for consistency, correctness, feasibility,
   artifact coverage, GPU/CPU boundary safety, and claim discipline.
