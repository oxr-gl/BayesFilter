# P02A Result: GPU TF32 SVD Numerical Repair

Date: 2026-06-25

Status: `P02A_REPAIR_PASS_TO_P02_RERUN`

## Phase Objective

Diagnose and repair the SVD-Nystrom GPU/TF32 numerical path that blocked P02,
without changing promotion criteria, rank, epsilon, kernel mode, scaling mode,
or code defaults after seeing the blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the SVD-Nystrom core be made finite and exact-reference-valid under the default GPU/TF32 target without weakening the promotion gate post hoc? |
| Baseline/comparator | Failed P02 GPU/TF32 SVD run; passing CPU/GPU-no-TF32 diagnostics are explanatory controls. |
| Primary criterion | Repaired GPU/TF32 run passes P02 deterministic validity, exact-reference thresholds, route metadata, and no dense materialization. |
| Veto diagnostics | Nonfinite outputs, CUDA solver errors, policy mismatch, hidden precision-policy downgrade, dense materialization, missing metadata, or unsupported default/scientific claim. |
| Explanatory diagnostics | Core spectrum, residuals, runtime, memory, CPU/GPU-no-TF32 deltas. |
| Not concluded | No promotion, no statistical superiority, no HMC readiness, no broad model-suite validity. |
| Artifact | This result plus repaired P02 rerun artifacts. |

## Repair Candidate

The bounded repair keeps the locked SVD-Nystrom policy
`r32_eps0p5_raw_none_svd_rcond1e-6` and adds a local numerical precision island
inside the SVD-Nystrom factor/core route:

- `svd_truncated` core inversion uses a float64 solve tensor when route dtype is
  float32, then casts the symmetrized inverse back to the route dtype.
- Core spectral diagnostics use the same solve precision so the metadata path
  does not reintroduce the GPU/TF32 SVD failure.
- Low-rank factor matvec/matmul application casts factor/core/vector operands
  to the same local solve precision, then casts results back to the route dtype.

This is a bounded numerical repair. It is not a default-policy precision
change, not a retuning of rank/epsilon/kernel/scaling, and not a promotion
claim.

## Checks And Diagnostics

| Check | Artifact | Status | Interpretation |
| --- | --- | --- | --- |
| Focused local tests after factor/core precision repair | `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/p02a-local-tests-r3.log` | PASS: `6 passed` | Tensor core, SVD solver, diagnostics, and LGSSM harness tests remain executable. |
| First repair, GPU0 TF32 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p02a-lgssm-reference-small-gpu0-fp64core-2026-06-25.json` | FAIL | FP64 core inversion alone did not repair nonfinite route/factors/particles. |
| First repair, GPU0 no-TF32 control | `docs/benchmarks/svd-nystrom-nohmc-promotion-p02a-lgssm-reference-small-gpu0-fp64core-tf32disabled-2026-06-25.json` | PASS | The same policy remained finite with TF32 disabled; explanatory only. |
| Factor/core precision repair, GPU0 TF32 | `docs/benchmarks/svd-nystrom-nohmc-promotion-p02a-lgssm-reference-small-gpu0-factorprecision-2026-06-25.json` | PASS | Bounded repair produced finite GPU/TF32 output and passed the LGSSM exact-reference hard gate. |

GPU preflight found GPU1 saturated, so the repaired TF32 diagnostic used GPU0
under the owner rule: use GPU1 if available, otherwise GPU0.

## Repaired Diagnostic Fields

For
`docs/benchmarks/svd-nystrom-nohmc-promotion-p02a-lgssm-reference-small-gpu0-factorprecision-2026-06-25.json`:

| Field | Value |
| --- | --- |
| Top-level status | `PASS` |
| Hard vetoes | `[]` |
| TF32 execution recorded | `True` |
| Device | `/GPU:0`, `CUDA_VISIBLE_DEVICES=0` |
| Candidate core solver | `svd_truncated` |
| Transport matrix materialized | `False` |
| Finite output/factors/particles | `True / True / True` |
| Mean RMSE | `0.12198596717117477` |
| Variance RMSE | `0.2425361188055973` |
| Loglik abs delta | `1.7873344421386719` |
| Max row residual | `0.0034079551696777344` |
| Max column residual | `0.0034064650535583496` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass repair to P02 rerun | PASS for the bounded P02A repair diagnostic | No P02A hard vetoes in the repaired GPU/TF32 diagnostic | Need to rerun P02 itself and obtain read-only review of the material repair before advancing P03 | Rerun P02 exact-reference gate with repaired code and exact policy; then run bounded Claude review | No promotion, no statistical superiority, no nonlinear/model-suite validity, no HMC readiness |

## Inference Status

| Row | Status |
| --- | --- |
| Hard veto screen | PASS for the repaired P02A GPU/TF32 diagnostic |
| Statistically supported ranking | NO |
| Descriptive-only differences | Runtime and RMSE magnitudes are descriptive in this one-row repair check |
| Default-readiness | NO |
| Next evidence needed | Repaired P02 exact-reference rerun and read-only repair review before P03 |

## Handoff

`P02A_REPAIR_PASS_TO_P02_RERUN`

The repaired P02 LGSSM exact-reference rerun emitted
`P02_PASS_REPAIRED_PENDING_REVIEW_TO_P03_ACTUAL_SIR_STRESS` under the same
locked SVD-Nystrom policy. P03 remains blocked until material repair review
converges and the supervisor records the explicit post-review handoff token
`P02_REPAIR_REVIEW_AGREE_PASS_TO_P03_ACTUAL_SIR_STRESS`.
