# Actual-SIR Nystrom Compiled-Redo P09D Spectral-Core Repair Plan

Date: 2026-06-23

Status: `READY_TO_IMPLEMENT_AND_LAUNCH`

## Purpose

P09B/P09C showed numerical brittleness in the Nystrom route:

- `rank=32,epsilon=0.25` fails with nonfinite Nystrom outputs.
- `rank=64,epsilon=0.3` fails with nonfinite Nystrom outputs.
- `rank=32,epsilon=0.5` remains viable.

This repair diagnostic tests whether replacing the Cholesky inverse of the
landmark kernel with a truncated spectral solve improves robustness.  Because
the user specifically asked whether SVD solve helps, the first implementation
target is `svd_truncated`; `eigh_truncated` is retained as the symmetric-PSD
variant if SVD is unavailable or not XLA-compatible.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Are the nonfinite failures caused mainly by inverse-conditioning of the landmark kernel core, and can truncated eigensolve rescue them without breaking the safe control? |
| Candidate mechanism | Nystrom core solver option `svd_truncated`, using relative singular-value cutoff before inversion; optional `eigh_truncated` fallback/variant. |
| Baseline/comparator | Existing `cholesky` core solver and compiled streaming TF32 paired comparator. |
| Failing rows | `rank=32,epsilon=0.25`; `rank=64,epsilon=0.3`. |
| Control row | `rank=32,epsilon=0.5`. |
| Shape | `B=5,T=20,N=1024,D=18,M=9`, seeds `81920..81924`. |
| Primary diagnostic criterion | SVD-truncated row reports `status=PASS`, `hard_vetoes=[]`, finite outputs, residuals pass, and paired thresholds pass. |
| Promotion criterion | None. This is a repair diagnostic only. |
| Promotion veto | Any claim that this single repair diagnostic establishes default-readiness or superiority. |
| Continuation veto | Implementation/test failure, GPU unavailable, artifact mismatch, or control row regression. |
| Repair trigger | Eigh-truncated rescues failures but control passes, motivating a reviewed implementation path and broader gate. |
| Explanatory diagnostics | Effective rank, min/max eigenvalues, eigenvalue cutoff, residuals, per-seed deltas, timing. |
| What must not be concluded | No default readiness, no statistical ranking, no posterior correctness, no HMC readiness. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does truncated SVD improve robustness of the Nystrom core on the known failing settings? |
| Exact baseline | Existing Cholesky core failures recorded in P09B/P09C and paired compiled streaming comparator for new rows. |
| Pass/fail criterion | Known failing rows pass under `svd_truncated` and the control row remains passing. |
| Veto diagnostics | Nonfinite factors/particles/log-likelihood, paired threshold failure, residual failure, missing GPU/TF32/JIT evidence, implementation test failure. |
| Explanatory-only diagnostics | Runtime, warm ratio, effective rank, eigenvalue spectrum summaries. |
| Not concluded | No default promotion or broad robust-policy proof. |
| Artifacts | `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09d-*.json/md` and this result prefix. |

## Skeptical Pre-Launch Audit

Status: `PASS_FOR_IMPLEMENTATION_DIAGNOSTIC`

This plan changes one algorithmic subcomponent while preserving the model,
seeds, comparator, dtype, transport policy, and thresholds.  It includes the
known failing rows and a safe control.  It does not relax thresholds after
observing failures.  Runtime is descriptive only.

## Implementation Scope

Allowed edits:

- `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`
- `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`
- focused tests in `tests/test_nystrom_transport_tf.py` and
  `tests/test_actual_sir_nystrom_compiled_redo.py`

Add options:

- `core_solver`: `cholesky`, `eigh_truncated`, or `svd_truncated`
- `core_rcond`: relative cutoff for spectral inversion

Default must remain `cholesky` for existing behavior.

## Diagnostic Rows

Use `svd_truncated` first with `core_rcond=1e-6`; if both failing rows remain
nonfinite, stop and classify.  If one is rescued but one remains failed, try
`1e-5`.  If SVD is not XLA-compatible, switch to the `eigh_truncated`
PSD-symmetric variant under the same row contract.  If both are rescued and
control passes, stop with a repair-success classification.

Rows:

| Row | Rank | Epsilon | Solver | Rcond |
| --- | ---: | ---: | --- | ---: |
| fail32_eps0p25_svd1e-6 | `32` | `0.25` | `svd_truncated` | `1e-6` |
| fail64_eps0p3_svd1e-6 | `64` | `0.3` | `svd_truncated` | `1e-6` |
| control32_eps0p5_svd1e-6 | `32` | `0.5` | `svd_truncated` | `1e-6` |

Optional escalation rows:

| Row | Rank | Epsilon | Solver | Rcond |
| --- | ---: | ---: | --- | ---: |
| fail32_eps0p25_svd1e-5 | `32` | `0.25` | `svd_truncated` | `1e-5` |
| fail64_eps0p3_svd1e-5 | `64` | `0.3` | `svd_truncated` | `1e-5` |
| control32_eps0p5_svd1e-5 | `32` | `0.5` | `svd_truncated` | `1e-5` |
