# Streaming Manual VJP Phase 7R Result: Metadata Remediation

date: 2026-06-23
phase: S7R-METADATA-REMEDIATION
status: BLOCKED_N2500_GPU_OOM_AFTER_VALID_N100_N1000

## Objective

Repair the S7 actual-gradient harness metadata contract without changing the
scientific question, S7 route, defaults, pass/fail criteria, or GPU ladder
sequence.

## Decision

The CPU-hidden S7R metadata remediation passed local checks, and the
remediated trusted GPU rerun advanced through valid N100 and N1000 artifacts.
The rerun then blocked at N2500 with a GPU `RESOURCE_EXHAUSTED` error before a
valid N2500 JSON artifact was written.

This result does not claim GPU ladder success, N10000 feasibility, or FD
agreement.  It does not reuse or hand-edit the old N100 JSON artifact.  The
reviewed ladder contract requires stopping at the first failed rung, so S8/P82
FD remains prohibited.

The next governed action is bounded exact-path Claude review of this updated
result.  Any attempt to change chunk sizes, allocator policy, route semantics,
or ladder criteria requires a new reviewed remediation plan.

## Scope Applied

Patched files:

- `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`
- `tests/highdim/test_p82_regression_fd_harness_protocol.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-visible-execution-ledger-2026-06-23.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-visible-stop-handoff-2026-06-23.md`

No old JSON artifact was edited.

## Harness Metadata Remediation

The regression harness now builds governed result-contract metadata in
`_result_contract_metadata`.

New or refreshed emitted keys:

- top-level `status`;
- top-level `primary_pass`;
- top-level `batch_seeds`;
- top-level `gradient_values`;
- top-level `objective_finite`;
- top-level `gradient_finite`;
- top-level `monte_carlo_gradient_noise_mcse_finite`;
- top-level `gradients_connected`;
- top-level `primary_pass_criterion`;
- `transport.dense_transport_matrix_materialized`.

`primary_pass` is intentionally narrow: finite objective, finite gradient
components, finite seed-gradient MCSE values, and connected AD path.  It is not
FD agreement, posterior correctness, production readiness, HMC readiness, or a
scientific-validity claim.  Device placement, route, particle count, seed
count, and transport metadata remain separately validated by the original S7
exact JSON contract before rung advancement.

The transport metadata is now emitted through `_transport_metadata`, including
`dense_transport_matrix_materialized: false`.

## Focused Protocol Tests Added

Added CPU-hidden protocol tests proving metadata emission without GPU work:

- `test_s7r_result_contract_metadata_emits_required_top_level_keys`;
- `test_s7r_result_contract_metadata_blocks_nonfinite_gradient`;
- `test_s7r_transport_metadata_declares_no_dense_transport_matrix`.

These tests construct tiny tensors and parser metadata only.  They do not
launch the SIR model, GPU work, FD comparison, or a ladder rung.

## Checks

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p82_regression_fd_harness_protocol.py -q
```

Output:

```text
16 passed, 2 warnings in 9.26s
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
```

Passed:

```text
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py tests/highdim/test_p82_regression_fd_harness_protocol.py docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7r-metadata-remediation-subplan-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-visible-execution-ledger-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-visible-stop-handoff-2026-06-23.md
```

## Evidence Contract Outcome

| Field | Outcome |
|---|---|
| Question | Can we repair the S7 harness metadata so newly emitted actual-gradient JSON artifacts satisfy the predeclared exact validation keys without changing route or scientific criteria? |
| Primary criterion | Metadata remediation passed locally, but the S7 ladder primary criterion failed before N10000 because N2500 exited nonzero with GPU OOM. |
| Veto diagnostics | Triggered at N2500: trusted GPU rung exited nonzero with `RESOURCE_EXHAUSTED`; no valid N2500 JSON exists. |
| Explanatory only | Valid N100 and N1000 artifacts show the remediated metadata contract works for smaller rungs. |
| Not concluded | No N10000 feasibility, no FD agreement, no HMC/default readiness, no production readiness, no posterior correctness, no scientific superiority. |

## Trusted GPU Rerun Outcome

Trusted GPU preflight passed after S7R result review:

- `nvidia-smi` saw NVIDIA GeForce RTX 4080 SUPER, Driver `591.86`, CUDA `13.1`.
- TensorFlow `2.19.1` saw `PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')`.

N100 rerun:

- Artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n100-gpu-tf32-2026-06-23.json`
- Command exited 0.
- Exact S7 JSON validation passed.
- Elapsed seconds: `33.13039512500109`.
- Objective: `-125.5501708984375`.
- Gradient values:
  `[-181.25650024414062, 78.58741760253906, 47.45368194580078]`.
- MCSE values:
  `15.015740394592285`, `3.5778865814208984`,
  `0.5832633376121521`.

N1000 rerun:

- Artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n1000-gpu-tf32-2026-06-23.json`
- Command exited 0.
- Exact S7 JSON validation passed.
- Elapsed seconds: `94.3620965730006`.
- Objective: `-125.59538269042969`.
- Gradient values:
  `[-157.03570556640625, 70.12916564941406, 47.45121383666992]`.
- MCSE values:
  `6.860280513763428`, `1.8712393045425415`,
  `0.1242830753326416`.

N2500 rerun:

- Intended artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n2500-gpu-tf32-2026-06-23.json`
- Command exited nonzero before writing a valid JSON artifact.
- Failure:
  `tensorflow.python.framework.errors_impl.ResourceExhaustedError`.
- TensorFlow allocator warning:
  `Allocator (GPU_0_bfc) ran out of memory trying to allocate 1.00MiB`.
- Traceback location:
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`,
  `_filterflow_streaming_softmin`, in the blockwise `_pairwise_squared_cross`
  cost computation.
- Post-failure trusted `nvidia-smi` showed no running GPU processes.

N5000 and N10000 were not launched because N2500 triggered the first hard stop
condition.

## Decision Table

| Field | Status |
|---|---|
| Decision | S7R metadata remediation passed locally; remediated GPU ladder blocked at N2500 OOM after valid N100 and N1000 artifacts. |
| Primary criterion status | Failed for S7 ladder: no valid N10000 artifact exists. |
| Veto diagnostic status | Triggered at N2500 GPU OOM/nonzero exit. |
| Main uncertainty | Whether a separately reviewed chunk-size, allocator, or deeper streaming-memory remediation could move the OOM boundary. |
| Next justified action | Request bounded exact-path Claude review of this updated blocker result; draft a new remediation plan only after that review. |
| What is not concluded | No S7 ladder pass and no S8/P82 FD handoff. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `f4853625732f31870f7ff3fc9064b97c742c1bef` |
| Commands | CPU-hidden checks and trusted GPU rungs listed in this result. |
| Environment | Local repo shell; CPU-hidden checks used `CUDA_VISIBLE_DEVICES=-1`; GPU commands used trusted/elevated execution. |
| CPU/GPU status | CPU-hidden metadata checks passed; trusted GPU preflight passed; N100/N1000 wrote GPU artifacts; N2500 OOMed on GPU. |
| Dtype | GPU rungs used `float32`, TF32 enabled. |
| Seeds | `[81120, 81121, 81122, 81123, 81124]` with `seed_microbatch_size=1`. |
| Wall time | Pytest reported `9.26s`; N100 `33.13039512500109s`; N1000 `94.3620965730006s`; N2500 failed before JSON. |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7r-metadata-remediation-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7r-metadata-remediation-result-2026-06-23.md` |

## Handoff

S8/P82 FD remains prohibited because no valid S7 N10000 actual-gradient
artifact exists.

Request bounded exact-path Claude review of this updated result.  If Claude
agrees, the next useful work is a new reviewed remediation plan for the N2500
GPU OOM boundary.  Do not rerun GPU rungs, tune chunk sizes, change allocator
policy, use `transport_ad_mode=full`, or launch FD without a new reviewed
plan.

If Claude returns `VERDICT: REVISE`, patch the same remediation result or the
narrow metadata remediation visibly, rerun focused CPU-hidden checks, and loop
review at most five times for the same blocker.
