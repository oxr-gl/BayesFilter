# BayesFilter LGSSM-First NeuTra/HMC Master Program

Date: 2026-07-06

## Status

`PHASE10_COMPLETED_PHASE11_READY`

## Objective

Build BayesFilter's generic Bayesian SSM target adapter and NeuTra/HMC path
starting from LGSSM, then simple nonlinear non-DSGE SSMs, then multi-filter
targets. DSGE/c603 is deferred to a later stress-test phase only.

This program is engineering integration and evidence discipline. It does not
claim posterior convergence, HMC readiness, production readiness, sampler
superiority, scientific validity, or a BayesFilter default-policy change.

## Design Principle

```text
LGSSM for correctness,
simple nonlinear SSM for generality,
DSGE for stress.
```

The starting point is BayesFilter-owned LGSSM because it has exact Kalman
likelihood/reference structure and inspectable parameter transforms. DSGE/c603
proved ambition in `dsge_hmc`, but it is not a good architectural foundation
for BayesFilter because it requires rational-expectations solving, structural
filtering, second-order perturbation machinery, and no simple analytical
posterior reference.

## Existing BayesFilter Surfaces To Reuse

- `bayesfilter/ssm/contracts.py::SSMTargetContract`
- `bayesfilter/ssm/target_builder.py::GenericSSMPosteriorAdapter`
- `bayesfilter/linear/types_tf.py::TFLinearGaussianStateSpace`
- `bayesfilter/linear/kalman_qr_tf.py`
- `bayesfilter/linear/kalman_qr_derivatives_tf.py`
- `bayesfilter/inference/fixed_transport_hmc.py`
- `bayesfilter/inference/neutra_artifacts.py`
- `tests/test_general_ssm_target_builder.py`
- `tests/test_linear_qr_compact_loglik_tf.py`
- `tests/test_hmc_linear_qr_readiness_tf.py`
- `bayesfilter/testing/tf_hmc_readiness.py::QRStaticLGSSMTarget`

These are starting surfaces, not automatic claims of full HMC/NeuTra readiness.

## Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter build a generic Bayesian SSM target adapter and NeuTra/HMC mechanics path from an exact LGSSM base before moving to nonlinear SSMs and later DSGE stress targets? |
| Baseline/comparator | Existing `SSMTargetContract`, `GenericSSMPosteriorAdapter`, QR Kalman LGSSM code, fixed-transport mechanics, and opt-in QR static LGSSM HMC smoke harness. |
| Primary pass criterion | Each phase either produces a reviewed, tested artifact for its boundary or records an exact blocker without promoting weaker evidence. |
| Veto diagnostics | DSGE/c603 used as foundation, synthetic targets promoted to real LGSSM/nonlinear evidence, finite smoke promoted to convergence, GPU/training/long-HMC/package/git actions without approval, unsupported posterior/product/scientific claims. |
| Explanatory diagnostics | Target signatures, adapter manifests, finite value/score probes, gradient/reference residuals, mechanics manifests, review status. |
| Not concluded | Posterior convergence, sampler ranking, production readiness, broad nonlinear SSM validity, or DSGE/c603 real target readiness. |
| Artifacts | Master program, phase subplans/results, visible runbook/ledger, stop handoff, review bundles, tests/logs when phases reach implementation. |

## Phase Index

| Phase | Name | Objective | Subplan | Result |
| --- | --- | --- | --- | --- |
| 0 | Scope Reset And Launch | Freeze LGSSM-first scope, defer DSGE/c603, and validate review/runbook protocol. | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase0-scope-reset-subplan-2026-07-06.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase0-scope-reset-result-2026-07-06.md` |
| 1 | Interface Inventory And Gap Map | Inventory current generic target, LGSSM Kalman, transport, and HMC surfaces; decide minimal interface changes. | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase1-interface-inventory-subplan-2026-07-06.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase1-interface-inventory-result-2026-07-06.md` |
| 2 | LGSSM Exact Target Adapter | Materialize a reviewed LGSSM target via `SSMTargetContract` and batch-native value/score adapter. | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase2-lgssm-target-adapter-subplan-2026-07-06.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase2-lgssm-target-adapter-result-2026-07-06.md` |
| 3 | Plain HMC Mechanics Smoke | Run a tiny CPU-only plain HMC mechanics smoke on the reviewed LGSSM target. | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase3-plain-hmc-smoke-subplan-2026-07-06.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase3-plain-hmc-smoke-result-2026-07-06.md` |
| 4 | LGSSM Posterior Reference Validation | Compare sampler/path outputs against LGSSM reference under a reviewed evidence contract. | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase4-lgssm-reference-validation-subplan-2026-07-06.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase4-lgssm-reference-validation-result-2026-07-06.md` |
| 5 | Frozen Transport Binding | Add identity/affine/frozen transport mechanics gates while preserving target signatures. | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase5-frozen-transport-binding-subplan-2026-07-06.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase5-frozen-transport-binding-result-2026-07-06.md` |
| 6 | LGSSM NeuTra Training And Freeze | Train/freeze NeuTra on LGSSM only if prior mechanics/reference gates pass and approval is available. | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-subplan-2026-07-06.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-result-2026-07-06.md` |
| 7 | First Simple Nonlinear SSM | Move to a BayesFilter-owned non-DSGE nonlinear SSM target. | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase7-simple-nonlinear-ssm-subplan-2026-07-06.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase7-simple-nonlinear-ssm-result-2026-07-06.md` |
| 8 | Same Target Multiple Filters | Show the same target interface can use different filters without changing HMC/transport plumbing. | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase8-multifilter-subplan-2026-07-06.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase8-multifilter-result-2026-07-06.md` |
| 9 | GPU NeuTra Training Preflight | Check admitted non-DSGE routes can bind a GPU NeuTra-style objective and emit finite initial value/gradient diagnostics without training or HMC. | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase9-gpu-neutra-training-preflight-subplan-2026-07-07.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase9-gpu-neutra-training-preflight-result-2026-07-07.md` |
| 10 | Bounded GPU NeuTra Training | Run the first bounded GPU optimizer-training gate for one admitted LGSSM route, with `jit_compile=false` while the XLA blocker remains open. | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase10-bounded-gpu-training-subplan-2026-07-07.md` | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase10-bounded-gpu-training-result-2026-07-07.md` |
| 11 | Frozen GPU-Trained Affine Payload | Package the Phase 10 GPU-trained affine parameters into the frozen affine payload schema and run loader/mechanics checks. | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase11-frozen-gpu-affine-payload-subplan-2026-07-07.md` | `pending` |

## Human Approval Boundaries

Allowed inside visible Phase 0 and Phase 1:

- local read-only inventory;
- local text checks;
- CPU-only import/pytest-sized checks when the subplan names them and sets
  `CUDA_VISIBLE_DEVICES=-1` before framework import;
- bounded Claude read-only review gates, subject to sandbox approval;
- fresh Codex read-only substitute review if Claude is unavailable.

Requires explicit human approval before execution:

- GPU/CUDA jobs;
- NeuTra training;
- long or decision-making HMC;
- package installation or environment mutation;
- detached/overnight/copied-workspace execution;
- network fetch beyond already available local material;
- git commit/push;
- live DSGE/c603 runtime target authority;
- default-policy changes;
- scientific, production, or public benchmark claims.

## Skeptical Plan Audit

Pre-execution audit status: `PASS_WITH_BOUNDARIES`.

- Wrong baseline: LGSSM exact Kalman is the architectural baseline; c603 is
  stress evidence only.
- Proxy promotion: finite smoke, finite gradients, transport import, and
  training loss cannot become posterior convergence or production readiness.
- Missing stop conditions: every subplan must state stop conditions before
  execution.
- Unfair comparison: no sampler or method ranking is permitted without a
  separate statistical evidence plan.
- Hidden assumptions: current BayesFilter target/HMC surfaces may already cover
  more than expected; Phase 1 inventory must decide whether to reuse, patch, or
  block.
- Stale context: earlier c603 blocker remains valid for DSGE stress only and
  must not steer the LGSSM foundation.
- Environment mismatch: CPU-only checks must set `CUDA_VISIBLE_DEVICES=-1`;
  GPU evidence requires trusted-context approval.
- Artifact mismatch: each phase has a result artifact and review gate.

## Stop Conditions

Stop and write a blocker result if:

- DSGE/c603 work becomes required before the LGSSM/nonlinear foundation;
- a phase would need GPU, training, long HMC, package install, live external
  runtime target authority, or git commit/push without approval;
- target signatures or adapter manifests contain process-local identity;
- finite value/score or reference checks fail and the next repair is unclear;
- review does not converge after five rounds for the same material blocker;
- a result would require unsupported posterior, production, or scientific
  claims.
