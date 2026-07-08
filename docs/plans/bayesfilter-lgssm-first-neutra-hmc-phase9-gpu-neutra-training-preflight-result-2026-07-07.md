# Phase 9 Result: GPU NeuTra Training Preflight

Date: 2026-07-07

## Scope

This result closes the Phase 9 GPU-only NeuTra training preflight for the
LGSSM-first BayesFilter NeuTra/HMC program.  It checks that the admitted LGSSM
and simple nonlinear non-DSGE routes can bind a tiny affine NeuTra-style
training objective on GPU, emit finite initial objective and gradient
diagnostics, and refuse CPU training fallback.

This is not full NeuTra training, not a learned-transport claim, not HMC
sampling or tuning, not posterior convergence evidence, not route ranking, not
production readiness, and not scientific validity.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | `PASS_PHASE9_GPU_NEUTRA_TRAINING_PREFLIGHT` |
| Primary criterion status | Passed: all admitted routes emitted finite initial loss and trainable affine-gradient diagnostics with outputs placed on `/GPU:0` under trusted execution. |
| Veto diagnostic status | No Phase 9 veto fired: trusted TensorFlow GPU was visible, CPU fallback was forbidden, deferred routes were rejected, no nonfinite loss/gradient occurred, no HMC or external sample generation ran, and no optimizer step ran. |
| Main uncertainty | The preflight is initial plumbing only. It does not show that any transport trains well, improves HMC, or is posterior-correct. |
| Next justified action | Phase 10 may either repair XLA/JIT first or run an explicitly non-XLA bounded GPU optimizer-training preflight for a selected admitted route, with separate review and no HMC/sample-generation work. |
| What is not concluded | Full NeuTra quality, dense IAF quality, HMC readiness, posterior correctness, sampler convergence, route superiority, production readiness, default-policy change, or scientific validity. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can admitted non-DSGE SSM targets bind a GPU NeuTra training objective and emit finite initial loss/gradient diagnostics without full training or HMC? |
| Baseline/comparator | Phase 6 LGSSM affine training mechanics, Phase 7 simple nonlinear SVD-UKF target route, and Phase 8 simple nonlinear SVD cubature target route. |
| Primary criterion | All admitted route losses and trainable affine-gradient diagnostics are finite and placed on GPU output devices. |
| Veto diagnostics | Missing trusted TensorFlow GPU, CPU training fallback, deferred route use, nonfinite loss or gradient, non-GPU output device, hidden HMC, hidden optimizer step, or hidden external sample generation. |
| Explanatory diagnostics | Initial loss, gradient norms, route signatures, GPU device manifest, and runtime. |
| Not concluded | Training quality, HMC readiness, posterior correctness, sampler convergence, route ranking, production readiness, or scientific validity. |
| Artifact | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase9-gpu-neutra-training-preflight-2026-07-07.json` |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Working tree; Phase 9 result pending commit. |
| GPU probe | Trusted `nvidia-smi`: NVIDIA GeForce RTX 4080 SUPER visible, driver `591.86`, CUDA `13.1`. |
| TensorFlow GPU probe | Trusted Python probe: TensorFlow `2.19.1`, physical GPU `/physical_device:GPU:0`, logical GPU `/device:GPU:0`. |
| Preflight command | `TF_FORCE_GPU_ALLOW_GROWTH=true python -m bayesfilter.testing.neutra_gpu_training_preflight_tf` |
| Execution target | GPU required, strict placement, soft placement disabled inside route checks. |
| CPU training fallback | Forbidden. |
| External sample generation | Not run; reserved for a separate multicore CPU phase. |
| HMC | Not run. |
| Optimizer steps | `0`; this is objective/gradient preflight only. |
| Seed | `20260707` |
| Batch size | `16` |
| Wall time | `33.63581864815205` seconds recorded in artifact. |
| Plan file | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase9-gpu-neutra-training-preflight-subplan-2026-07-07.md` |
| Result file | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase9-gpu-neutra-training-preflight-result-2026-07-07.md` |
| Validation artifact | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase9-gpu-neutra-training-preflight-2026-07-07.json` |
| XLA blocker artifact | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase9-gpu-neutra-training-preflight-xla-blocker-2026-07-07.json` |

## Route Outcomes

| Route | Target signature | Adapter signature | Initial loss | Gradient norms | Status |
| --- | --- | --- | --- | --- | --- |
| `lgssm-static-qr-exact-kalman` | `290a91d2a8f90d5b29243965b258b1ec6fd965aa46ffca69dcb78f7fa1ecabcb` | `0a48b43d2750cad5b452708f7619a1119a259231d8955769809460f256575a97` | `4.270573668036143` | `[1.1184880186335193, 1.2371718623608414]` | Passed Phase 9 preflight. |
| `model-b-svd-ukf-deterministic-loglikelihood` | `c6a942c251e08f111b5647f814c1815535f931fcd13a09d337a74b8fb5eacaa0` | `9fdc2ef475992711dd1ed5aadc0b47aeed235d7ccea9e9567740b57aaf2a04dd` | `10.043907730802296` | `[5.3424620219797285, 5.2082360981313665]` | Passed Phase 9 preflight. |
| `model-b-svd-cubature-deterministic-loglikelihood` | `19e87b2090c353ddc855791c36a1a325246b0a275886c92f3fa8dc625467d1ee` | `39927792f114f9d80f540b4f6759e9b5cd22c4c55d1d5cb7df13fc0e4756a9b9` | `10.951616558345272` | `[3.2381605366816353, 6.020535942703095]` | Passed Phase 9 preflight. |

Deferred routes remained deferred:

- `model-b-svd-cut4-deterministic-loglikelihood`
- `model-b-principal-sqrt-ukf-deterministic-loglikelihood`

## Artifact Hashes

| Artifact | Hash |
| --- | --- |
| Phase 9 pass JSON file SHA-256 | `c60ae71858a43e38a5b153f97b6c75b846ba71f6529039740d0438cb1b135e2c` |
| Phase 9 pass JSON stable payload SHA-256 excluding artifact hash fields | `4bda5ebbc3e2ddbeb27a984ff0fb1574d8c6b23ab45ef253c27bd126d9fce306` |
| Phase 9 XLA blocker JSON file SHA-256 | `d6b94488139ef5a981596df8e18a3bfbedfc2103be2b921fef76db1ab3611530` |

## XLA/JIT Blocker

A JIT/XLA probe was attempted before the final Phase 9 pass. It blocked with
TensorFlow:

```text
XLA compilation requires a fixed tensor list size.
```

The failure is recorded in:

```text
docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase9-gpu-neutra-training-preflight-xla-blocker-2026-07-07.json
```

This is not treated as a Phase 9 GPU-training preflight veto because Phase 9's
reviewed primary criterion is GPU objective/gradient plumbing, not XLA
readiness.  The XLA blocker must be handled by a later explicit XLA-readiness
gate before any XLA/HMC-readiness claim.

Phase 10 inherits this blocker. If Phase 10 proceeds before XLA repair, it must
set and record `jit_compile=false`, label the run as non-XLA bounded GPU
training-preflight evidence only, and state that passing Phase 10 cannot support
XLA readiness, HMC readiness, or default execution readiness.

## Skeptical Plan Audit

| Risk | Control |
| --- | --- |
| Wrong baseline | Phase 9 used only admitted LGSSM/simple nonlinear routes from prior gates; DSGE/c603 and LEDH evidence were not used. |
| Proxy metric promoted | Initial loss and gradient norms are explanatory plumbing diagnostics only. |
| Missing stop conditions | CPU fallback, missing GPU, deferred route use, nonfinite diagnostics, HMC, optimizer steps, and sample generation are explicit vetoes. |
| Unfair route comparison | Route losses are not compared or ranked. |
| Environment mismatch | GPU/CUDA probes and the preflight were run under trusted/escalated execution per local policy. |
| Artifact mismatch | The pass artifact records zero optimizer steps and no HMC/sample generation, matching the phase question. |

Audit status: passed for Phase 9 execution.

## Local Checks

- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_neutra_gpu_training_preflight_tf.py -q`: passed, `9 passed, 2 warnings`.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_neutra_gpu_training_preflight_tf.py tests/test_simple_nonlinear_generic_target_adapter_tf.py -q`: passed, `32 passed, 2 warnings`.
- `python -m json.tool docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase9-gpu-neutra-training-preflight-2026-07-07.json`: passed.
- `python -m json.tool docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase9-gpu-neutra-training-preflight-xla-blocker-2026-07-07.json`: passed.
- `python -m py_compile bayesfilter/testing/neutra_gpu_training_preflight_tf.py tests/test_neutra_gpu_training_preflight_tf.py`: passed.
- Trusted `nvidia-smi`: passed.
- Trusted TensorFlow GPU visibility probe: passed.
- Trusted Phase 9 GPU preflight command: passed.

The CPU-hidden pytest commands are test-only policy checks. They are not
training runs and are not GPU evidence.

## Implementation Artifacts

- `bayesfilter/testing/neutra_gpu_training_preflight_tf.py`
- `tests/test_neutra_gpu_training_preflight_tf.py`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase9-gpu-neutra-training-preflight-2026-07-07.json`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase9-gpu-neutra-training-preflight-xla-blocker-2026-07-07.json`

## Phase Close Duties

1. Required local checks were run and recorded above.
2. This Phase 9 result records the close decision and nonclaims.
3. The Phase 10 subplan was drafted:
   `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase10-bounded-gpu-training-subplan-2026-07-07.md`.
4. The next subplan must receive bounded read-only review before execution.

## Nonclaims

- No full NeuTra training was run.
- No learned transport was frozen or promoted.
- No HMC sampling or tuning was run.
- No external sample generation was run.
- No XLA readiness claim is made.
- No route ranking is claimed.
- No posterior correctness, convergence, sampler superiority, production
  readiness, default-policy change, or scientific validity is claimed.
