# P02A Subplan: GPU TF32 SVD Numerical Repair

Date: 2026-06-25

Status: `P02A_REPAIR_PASS_TO_P02_RERUN`

## Phase Objective

Diagnose and repair the SVD-Nystrom GPU/TF32 numerical path that blocked P02,
without changing promotion criteria after seeing results or silently weakening
the default target.

## Entry Conditions Inherited From Previous Phase

- P02 emitted `P02_DETERMINISTIC_BLOCKER_GPU_TF32_SVD_NONFINITE`.
- CPU and GPU-no-TF32 diagnostics passed under the locked SVD-Nystrom policy.
- GPU/TF32 enabled failed with nonfinite route output and CUDA `gesvd` errors
  in the actual SVD core.
- P03 and later phases are blocked.

## Required Artifacts

- P02A repair result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p02a-gpu-tf32-svd-repair-result-2026-06-25.md`
- Repair diagnostics under:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p02a-*.json`,
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p02a-*.md`, and
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/`
- Any code patch must be bounded to:
  `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`,
  `docs/benchmarks/benchmark_svd_nystrom_lgssm_kalman_gate.py`, and focused
  tests.

## Required Checks, Tests, And Reviews

- Review the new P02 harness before relying on repaired evidence.
- Predeclare any repair candidate before running it.
- Compare at least:
  - current `svd_truncated` GPU/TF32 failure control;
  - GPU/TF32 disabled pass control;
  - one bounded repair candidate, such as local FP32/FP64 core solve,
    symmetric eigentruncated solve, explicit symmetrization/jitter, or a
    TensorFlow numerics-safe fallback.
- Run focused local tests for any code changes.
- Run trusted GPU1 diagnostics for each candidate; use GPU0 only if GPU1 is
  unavailable.
- Claude read-only review is required for material repair claims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the SVD-Nystrom core be made finite and exact-reference-valid under the default GPU/TF32 target without weakening the promotion gate post hoc? |
| Baseline/comparator | Failed P02 GPU/TF32 SVD run; passing CPU/GPU-no-TF32 diagnostics are explanatory controls. |
| Primary criterion | Repaired GPU/TF32 run passes P02 deterministic validity, exact-reference thresholds, route metadata, and no dense materialization. |
| Veto diagnostics | Nonfinite outputs, CUDA solver errors, policy mismatch, hidden precision-policy downgrade, dense materialization, missing metadata, or unsupported default/scientific claim. |
| Explanatory diagnostics | Core spectrum, residuals, runtime, memory, CPU/GPU-no-TF32 deltas. |
| Not concluded | No promotion, no statistical superiority, no HMC readiness, no broad model-suite validity. |
| Artifact | P02A result and repaired P02 rerun artifacts. |

## Forbidden Claims And Actions

- Do not proceed to P03 until P02 repair passes.
- Do not treat GPU-no-TF32 or CPU pass as satisfying the default GPU/TF32 gate.
- Do not retune rank/epsilon/kernel/scaling after seeing P02 failure unless the
  lane is explicitly downgraded to repair/tuning and promotion claims are
  withdrawn.
- Do not change code defaults in this repair phase.
- Do not claim the method is promoted.

## Exact Next-Phase Handoff Conditions

- `P02A_REPAIR_PASS_TO_P02_RERUN`: reviewed repair candidate passes local and
  trusted GPU/TF32 diagnostics; rerun P02 exact-reference gate.
- `P02A_REPAIR_REQUIRED`: repair candidate is promising but incomplete.
- `P02A_BLOCKED`: no bounded repair is available without changing the default
  precision target, candidate policy, or code-default boundary.

## Stop Conditions

- Any repair requires unapproved default precision-policy change.
- Any repair requires broad refactor outside the bounded write set.
- GPU/TF32 remains nonfinite after bounded repair candidates.
- Claude/Codex review does not converge after five rounds for the same
  blocker.

## Local Self-Review Of Next Subplan

This repair subplan preserves the P02 hard veto and does not authorize P03.
It treats CPU/GPU-no-TF32 passes as diagnostics only and keeps default-target
promotion blocked until a reviewed GPU/TF32 exact-reference rerun passes.
