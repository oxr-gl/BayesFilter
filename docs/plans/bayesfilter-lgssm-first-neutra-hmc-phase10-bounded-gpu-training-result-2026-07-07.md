# Phase 10 Result: Bounded GPU NeuTra Training

Date: 2026-07-07

## Scope

This result closes the Phase 10 bounded GPU NeuTra optimizer-training gate for
the LGSSM-first BayesFilter NeuTra/HMC program.  It trains a small
affine-diagonal NeuTra-style transport parameterization for the admitted
`lgssm-static-qr-exact-kalman` route for a fixed, bounded number of optimizer
steps on GPU and writes a training-state artifact.

This is not full NeuTra training, not a dense IAF claim, not a frozen transport
promotion, not HMC sampling or tuning, not posterior convergence evidence, not
XLA readiness, not route ranking, not production readiness, not default
execution readiness, and not scientific validity.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | `PASS_PHASE10_BOUNDED_GPU_NEUTRA_TRAINING` |
| Primary criterion status | Passed: 12 predeclared optimizer steps completed on `/GPU:0`, the loss and gradient diagnostics were finite, optimizer state was materialized on GPU, and the training-state JSON was written. |
| Veto diagnostic status | No final Phase 10 veto fired: trusted TensorFlow GPU was visible, CPU training fallback was forbidden, `jit_compile=false`, the route was admitted, all recorded objective tensors were on GPU, and no HMC or external sample generation ran. |
| Main uncertainty | This is a bounded affine training gate.  The observed loss history is explanatory only and does not establish transport quality, posterior correctness, HMC readiness, XLA readiness, or production/default readiness. |
| Next justified action | Phase 11 should package the GPU-trained affine parameters into the existing frozen affine transport schema and run loader/mechanics checks before any sampler or sample-generation work. |
| What is not concluded | Full NeuTra quality, dense IAF quality, HMC readiness, posterior correctness, sampler convergence, route superiority, XLA readiness, production readiness, default-policy change, or scientific validity. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter run bounded GPU NeuTra optimizer training for one admitted non-DSGE route without CPU fallback, HMC, or sample generation? |
| Baseline/comparator | Phase 9 GPU objective/gradient preflight; Phase 6 CPU affine fixture only as a historical schema/mechanics reference, not as execution policy. |
| Primary criterion | Selected route completes the predeclared bounded optimizer steps on GPU with `jit_compile=false`, emits finite loss and gradient diagnostics, and writes a training-state artifact with no CPU fallback. |
| Veto diagnostics | Missing trusted GPU, CPU fallback, nonfinite loss/gradient, optimizer state missing, artifact schema failure, route not admitted, hidden HMC, hidden external sample generation, unrecorded TF32/JIT/device provenance, or unreviewed XLA/JIT requirement. |
| Explanatory diagnostics | Initial/final loss, loss curve, gradient norms, runtime, GPU device placement, route signatures, TF32 status, and optimizer-state placement. |
| Not concluded | Transport quality, HMC readiness, posterior correctness, route superiority, dense IAF readiness, production readiness, default execution readiness, XLA readiness, or scientific validity. |
| Artifact | `docs/plans/artifacts/lgssm-first-neutra-gpu-training-2026-07-07/lgssm_static_qr_exact_kalman_affine_neutra_gpu_training_state_seed20260707.json` |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `9cab7483956a3835a8a484fb04e485b5e9e2ddff` before Phase 10 edits. |
| Python | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python`, Python `3.11.14`. |
| TensorFlow | `2.19.1`. |
| GPU probe | Trusted `nvidia-smi`: NVIDIA GeForce RTX 4080 SUPER visible, driver `591.86`, CUDA `13.1`. |
| TensorFlow GPU probe | Trusted Python probe: physical GPU `/physical_device:GPU:0`, logical GPU `/device:GPU:0`, TF32 enabled. |
| Training command | `TF_FORCE_GPU_ALLOW_GROWTH=true python -m bayesfilter.testing.neutra_gpu_bounded_training_tf` |
| Execution target | GPU required, strict placement, soft placement disabled inside route checks. |
| CPU training fallback | Forbidden. |
| JIT/XLA | `jit_compile=false`; Phase 9 XLA blocker inherited. |
| TF32 | `true`, recorded in artifact. |
| External sample generation | Not run; reserved for a separate multicore CPU phase. |
| HMC | Not run. |
| Route | `lgssm-static-qr-exact-kalman`. |
| Seed | `20260707`. |
| Optimizer | `tf.keras.optimizers.Adam`. |
| Steps | `12`. |
| Batch size | `16`. |
| Learning rate | `0.03`. |
| Wall time | `29.95598600502126` seconds recorded in artifact. |
| Plan file | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase10-bounded-gpu-training-subplan-2026-07-07.md` |
| Result file | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase10-bounded-gpu-training-result-2026-07-07.md` |

## Training Outcome

| Field | Value |
| --- | --- |
| Target signature | `290a91d2a8f90d5b29243965b258b1ec6fd965aa46ffca69dcb78f7fa1ecabcb` |
| Adapter signature | `0a48b43d2750cad5b452708f7619a1119a259231d8955769809460f256575a97` |
| Initial loss | `4.270573668036143` |
| Final loss | `3.678928622118027` |
| Final shift | `[-0.02355730854089814, -1.3783530510587625]` |
| Final raw scale | `[-1.030798470103552, -1.0321253740715555]` |
| Artifact stable hash | `sha256:5b6bb48c74fc3ddc4d97404d7220a08323d90337e2a72e24f1fcdaa82a7de351` |
| Artifact file SHA-256 | `263c492c9789c9b50e245b14efd0bacb114d281b52285267c9ce4c5280496811` |
| Artifact size | `18798` bytes |

The loss change is a training diagnostic only.  It is not evidence of posterior
correctness, sampler readiness, route superiority, or production readiness.

## Repair Loop

The first trusted Phase 10 GPU attempt failed while writing provenance:

```text
AttributeError: 'Variable' object has no attribute 'device'
```

This was a mechanical artifact-writing issue: Keras optimizer variables in this
environment do not expose `.device` directly.  The runner was patched to record
placement through a compatibility helper that handles tensors, TensorFlow
variables, and Keras variables.  Focused CPU-hidden checks were rerun after the
patch, and the trusted GPU command was rerun successfully.

This repair did not change the research target, route, optimizer, step count,
batch size, XLA policy, HMC boundary, or sample-generation boundary.

## Skeptical Plan Audit

| Risk | Control |
| --- | --- |
| Wrong baseline | Phase 10 selected the LGSSM QR route admitted by Phase 9; DSGE/c603 and LEDH evidence were not used. |
| Proxy promotion | Loss history and gradient norms are explanatory training diagnostics only. |
| Missing stop conditions | CPU fallback, missing GPU, unreviewed XLA/JIT, nonfinite diagnostics, hidden HMC, hidden sample generation, and malformed artifact are explicit vetoes. |
| Hidden assumption | The Phase 9 XLA blocker is inherited; Phase 10 proceeds only as a non-XLA bounded GPU training gate. |
| Environment mismatch | GPU probes and training were run under trusted/escalated execution per local policy. |
| Artifact mismatch | The artifact records no frozen payload, no HMC, no sample generation, no XLA readiness, and no full NeuTra claim. |

Audit status: passed for the final Phase 10 execution.

## Local Checks

- `python -m py_compile bayesfilter/testing/neutra_gpu_bounded_training_tf.py tests/test_neutra_gpu_bounded_training_tf.py`: passed.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_neutra_gpu_bounded_training_tf.py -q`: passed, `7 passed, 2 warnings` after the trusted GPU artifact was generated.
- `python -m json.tool docs/plans/artifacts/lgssm-first-neutra-gpu-training-2026-07-07/lgssm_static_qr_exact_kalman_affine_neutra_gpu_training_state_seed20260707.json`: passed.
- Trusted `nvidia-smi`: passed.
- Trusted TensorFlow GPU visibility probe: passed.
- Trusted Phase 10 GPU bounded training command: passed.

The CPU-hidden pytest command is a test-only policy/schema check.  It is not a
training run and is not GPU evidence.

## Implementation Artifacts

- `bayesfilter/testing/neutra_gpu_bounded_training_tf.py`
- `tests/test_neutra_gpu_bounded_training_tf.py`
- `docs/plans/artifacts/lgssm-first-neutra-gpu-training-2026-07-07/lgssm_static_qr_exact_kalman_affine_neutra_gpu_training_state_seed20260707.json`

## Phase Close Duties

1. Required local checks were run and recorded above.
2. This Phase 10 result records the close decision and nonclaims.
3. The Phase 11 subplan was drafted:
   `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase11-frozen-gpu-affine-payload-subplan-2026-07-07.md`.
4. The Phase 10 result and Phase 11 subplan require bounded read-only review
   before Phase 11 execution.

## Nonclaims

- No full NeuTra training claim is made.
- No dense IAF training claim is made.
- No frozen transport payload was written or promoted in Phase 10.
- No HMC sampling or tuning was run.
- No external sample generation was run.
- No XLA readiness claim is made.
- No route ranking is claimed.
- No posterior correctness, convergence, sampler superiority, production
  readiness, default execution readiness, default-policy change, or scientific
  validity is claimed.
