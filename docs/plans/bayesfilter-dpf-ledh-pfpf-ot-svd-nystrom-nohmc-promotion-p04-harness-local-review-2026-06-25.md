# P04 Harness Local Review: Range-Bearing Gate

Date: 2026-06-25

Status: `P04_HARNESS_LOCAL_TESTS_PASS_PENDING_CLAUDE_ARTIFACT_REVIEW`

## Scope

This is a local source-level review of the P04 range-bearing nonlinear Gaussian
gate harness. Claude is not asked to read the harness source because the
standing approval for this runbook explicitly forbids Claude Code from reading
source code. Claude may review this note, the P04 subplan, the P03 result, and
same-prefix local-test logs/artifacts for consistency only.

## Reviewed Local Files

- Harness: `docs/benchmarks/benchmark_svd_nystrom_range_bearing_gate.py`
- Tests: `tests/test_svd_nystrom_range_bearing_gate.py`
- Local test log:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04-range-bearing-local-tests.log`

## Decision Table

| Field | Result |
| --- | --- |
| Decision | `P04_HARNESS_LOCAL_TESTS_PASS_PENDING_CLAUDE_ARTIFACT_REVIEW` |
| Primary criterion status | PASS locally: syntax checks passed and focused tests passed |
| Veto diagnostic status | PASS locally: harness records fixture checksums, route metadata, TF32/GPU provenance fields, residual thresholds, ESS threshold, nonclaims, and no dense transport materialization flag |
| Main uncertainty | No P04 trusted GPU rows have been run; Claude artifact-level review is still pending |
| Next justified action | Run bounded Claude artifact consistency review, then trusted GPU preflight and seed `84000` if review agrees |
| What is not concluded | No P04 model gate pass, no default promotion, no posterior correctness, no statistical superiority, no HMC readiness |

## Local Checks

| Check | Result |
| --- | --- |
| `py_compile` for harness and focused test | PASS |
| Focused local pytest | PASS: `4 passed, 14508 warnings in 16.37s` |
| CPU-hidden tiny route smoke | PASS in focused tests; both streaming and Nystrom rows finite |
| Observation/residual agreement with fixture definitions | PASS in focused tests |
| Artifact metadata presence | PASS in focused tests |

## Source-Level Review Findings

- The harness uses the existing `range_bearing_gaussian_moderate` fixture and
  records the fixture model and observation checksums in artifacts.
- The harness implements the TensorFlow range-bearing observation,
  wrapped-angle residual, and Jacobian for the DPF route, while using NumPy
  only for fixture loading and test/reference comparisons.
- The P04 comparator is the same-artifact compiled streaming TF32 DPF route.
- The candidate route is the locked SVD-Nystrom policy:
  `rank=32`, `epsilon=0.5`, `raw`, `none`, `svd_truncated`, `rcond=1e-6`.
- The harness records hard-veto fields for nonfinite outputs, residual
  thresholds, final log-weight normalization, ESS fraction, GPU evidence, and
  TF32 evidence.
- The Nystrom row records `transport_matrix_materialized: false` and
  `transport_object_kind: nystrom_kernel_factors`.
- The result schema records nonclaims, including no default promotion, no
  posterior correctness, no statistical superiority, no HMC readiness, and no
  broad nonlinear validity claim.

## Skeptical Audit

| Risk | Audit |
| --- | --- |
| Wrong baseline | Guarded locally: comparator is same-artifact compiled streaming DPF, not a sigma-point or UKF proxy. |
| Proxy metric promoted | Guarded: normalized log-likelihood delta is only the predeclared P04 viability screen. Timing and ESS/tail details remain descriptive except for the stated hard vetoes. |
| Missing stop conditions | Guarded by P04 subplan: invalid harness, malformed artifacts, GPU/TF32 mismatch, residual/log-weight/ESS failures, and post-hoc changes stop execution. |
| Unfair comparison | Guarded: same fixture, seed, dtype, TF32 mode, route policy, and artifact schema are used for both routes in each row. |
| Hidden assumption | Guarded: this is one nonlinear Gaussian fixture only and does not replace P05-P08. |
| Stale context | Guarded: P04 follows P03 pass and repaired P02 GPU/TF32 SVD path; no HMC readiness is in scope. |
| Environment mismatch | Still pending: trusted GPU preflight must be run immediately before P04 GPU rows. |
| Artifact fit | Guarded locally: JSON, Markdown, log, summary, and result paths are predeclared in the subplan. |

Audit status: `PASS_FOR_CLAUDE_ARTIFACT_REVIEW_AND_P04_ROW84000_AFTER_REVIEW`.

## Boundary Notes

- Do not send the harness source or test source to Claude under the current
  approval.
- Do not interpret this local harness review as P04 passing.
- Do not launch P05 until P04 writes its result and emits
  `P04_PASS_TO_P05_SV_HEAVY_TAIL`.
