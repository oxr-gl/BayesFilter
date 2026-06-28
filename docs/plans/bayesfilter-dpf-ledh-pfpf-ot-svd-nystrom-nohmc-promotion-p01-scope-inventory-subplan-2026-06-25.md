# P01 Subplan: Scope, Inventory, And Harness Readiness

Date: 2026-06-25

Status: `DRAFT_AFTER_P00`

## Phase Objective

Verify the current code/artifact/test surface can support the SVD-Nystrom
no-HMC promotion program before launching material model-suite GPU phases.

## Entry Conditions Inherited From Previous Phase

- P00 governance/runbook review converged.
- Master program locks candidate policy
  `rank=32,epsilon=0.5,kernel_mode=raw,scaling_normalization=none,core_solver=svd_truncated,core_rcond=1e-6`.
- HMC readiness is excluded from the promotion scope.

## Required Artifacts

- Inventory JSON:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p01-scope-inventory-2026-06-25.json`
- P01 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p01-scope-inventory-result-2026-06-25.md`
- P02 refreshed subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p02-lgssm-reference-subplan-2026-06-25.md`

## Required Checks, Tests, And Reviews

- Parse P06 summary and P07 closeout.
- Inventory relevant SVD-Nystrom benchmark/test files.
- Verify current tests cover compiled-redo SVD metadata and CPU-hidden command
  shape.
- Run focused local tests that do not require GPU:
  `tests/test_actual_sir_nystrom_compiled_redo.py`,
  `tests/test_nystrom_transport_tf.py`, and
  `tests/test_actual_sir_nystrom_default_promotion.py`.
- Review P02 subplan for consistency, feasibility, artifact coverage, and
  boundary safety.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the local harness surface ready for no-HMC SVD-Nystrom promotion testing? |
| Baseline/comparator | P06/P07 evidence plus existing test/harness inventory. |
| Primary criterion | Inventory is complete enough to identify executable P02-P07 paths; focused local tests pass. |
| Veto diagnostics | Missing P06/P07 artifacts, missing SVD metadata tests, local test failure, active-path NumPy evidence, or inability to define executable next phase. |
| Explanatory diagnostics | File lists, test names, existing artifact provenance. |
| Not concluded | No model-suite validity, no GPU readiness, no promotion, no statistical ranking. |
| Artifact | Inventory JSON and P01 result. |

## Forbidden Claims And Actions

- Do not treat inventory as promotion evidence.
- Do not run long GPU benchmarks.
- Do not change candidate policy.
- Do not claim HMC readiness.

## Exact Next-Phase Handoff Conditions

- `P01_PASS_TO_P02_LGSSM_REFERENCE`: inventory and focused CPU/local tests pass;
  P02 subplan reviewed.
- `P01_REPAIR_LOOP`: fixable harness/test metadata issue.
- `P01_BLOCKED`: missing critical harness, local tests fail for material
  reasons, or next phase cannot be made executable.

## Stop Conditions

- P06/P07 entry artifacts missing or inconsistent.
- Focused local tests fail and cannot be classified as unrelated.
- Inventory shows no executable path for exact/reference quality testing.

## Local Self-Review Of Next Subplan

P02 names an exact-reference quality gate and blocks GPU execution until trusted
preflight and reviewed commands are available.
