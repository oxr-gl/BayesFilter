# BayesFilter-MacroFinance Phase 7 Result: Backend Parity Gates

Date: 2026-06-09

## Status

`PASSED`

## Role And Runtime Classification

Codex is supervisor and executor. Claude is read-only reviewer only.

Runtime classification:

- BayesFilter library primitive: deterministic fixture/test helper and
  target-agnostic validation gate.
- MacroFinance compatibility: no-HMC client parity gate on the current
  matched-DGP Phase 4 validation surface.
- No HMC chain execution, posterior convergence, sampler superiority, empirical
  validity, GPU/XLA readiness, default backend promotion, or production
  readiness is authorized by this phase.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter own a reusable backend parity gate that compares two or more backend evaluations of the same scalar target, including value, score, latent-wrapper, shape, branch/failure-policy, and optional Hessian diagnostics, without making backend-specific target changes invisible? |
| Baseline/comparator | Accepted Phase 7 of `docs/plans/bayesfilter_macrofinance_hmc_filtering_consolidation_plan_2026_06_09.md`, existing BayesFilter Cholesky/QR/SVD linear Gaussian tests, Stage 1 `LatentAffineHMCTransform`, Stage 4 evidence manifests, and current MacroFinance matched-DGP SVD capability validation rows. |
| Primary criterion | A BayesFilter-owned gate accepts labeled backend rows with a shared target scope, checks finite scalar values, optional scores, shapes, branch/failure labels, and optional latent-wrapper parity; reports max value/score/Hessian discrepancies; fails closed on target-scope mismatch, unlabeled target-changing regularization, shape mismatch, nonfinite required arrays, or branch-policy mismatch; and keeps Hessian parity explanatory-only by default. |
| Veto diagnostics | Value and score correspond to different scalar targets; backend-specific regularization changes the target without an explicit label; a parity row uses old mismatched Phase 4 data; shape or branch/failure-policy mismatch is ignored; Hessian parity is silently promoted to a hard criterion; or MacroFinance-specific fields become required in BayesFilter. |
| Repair triggers | Missing helper/export/test, incomplete row validation, tolerance role ambiguity, same-target metadata missing, latent-wrapper parity omitted, failure-policy mismatch not classified, MacroFinance compatibility still using only ad hoc parity logic, or Claude `NEEDS_REVISION` with fixable findings. |
| Explanatory diagnostics | Exact class/function names, tolerance values, value/score/Hessian max differences, backend labels, branch labels, and whether a TensorFlow fixture was run CPU-only. |
| Non-claims | Passing this gate does not prove global backend equivalence, posterior convergence, sampler superiority, empirical validity, GPU/XLA readiness, or default backend readiness. |

## Skeptical Audit

- Wrong baseline: The baseline is the accepted consolidation plan and current
  BayesFilter/MacroFinance matched-DGP artifacts, not the old mismatched Phase
  4 payload or a fresh HMC pilot.
- Proxy metric promotion: Pointwise parity checks are validity gates for a
  named target and fixture only. They do not establish global equivalence,
  convergence, or default readiness.
- Stop conditions: Target-scope mismatch, unlabeled target-changing
  regularization, required shape mismatch, nonfinite required arrays, or
  branch-policy mismatch stop the phase until repaired.
- Fair comparison: All rows must declare the same target scope and comparable
  parameter coordinates. Backend-specific regularization is allowed only when
  explicitly labeled and interpreted as a target/implementation-policy
  difference, not hidden parity.
- Hidden assumptions: Hessian parity is optional and explanatory-only; this
  phase will not turn Hessian differences into pass/fail evidence.
- Stale context: BayesFilter and MacroFinance both have dirty worktrees;
  unrelated changes must be preserved.
- Environment/import mismatch: BayesFilter tests run from
  `/home/ubuntu/python/BayesFilter`; MacroFinance compatibility should use
  `PYTHONPATH=/home/ubuntu/python/BayesFilter` and
  `CUDA_VISIBLE_DEVICES=-1` for CPU-only no-HMC checks.
- Artifact relevance: Required artifacts are this result note, focused
  BayesFilter parity tests, a MacroFinance compatibility test calling the
  BayesFilter gate, and Claude read-only pre/post reviews.
- Role-contract check: Claude pre-review must be read-only; Codex performs all
  edits and tests.
- BayesFilter/MacroFinance ownership: The reusable parity primitive belongs in
  BayesFilter; MacroFinance remains a client fixture and should not require
  MacroFinance-specific fields in BayesFilter.

## Current Code Audit

BayesFilter currently has reusable transform, mass-artifact, diagnostic, and
manifest primitives from the earlier accepted stages. It also has separate
Cholesky, QR, and SVD linear Gaussian value tests. It does not yet expose a
generic target-agnostic parity row/gate that client projects can use to bind
same-target metadata, branch/failure labels, latent-wrapper rows, and
explanatory Hessian diagnostics in one auditable artifact.

MacroFinance currently contains Phase 4 matched-DGP SVD capability validation
logic with direct Cholesky/SVD value-score rows and dense-whitening wrapper
rows. Stage 5 should make that compatibility check call a BayesFilter-owned
gate while preserving the existing matched-DGP target, payload, and tolerances.

## Planned Minimal Implementation

1. Add a small BayesFilter parity module, likely
   `bayesfilter/inference/backend_parity.py`.
2. Define target-agnostic dataclasses such as `BackendParityRow`,
   `BackendParityGate`, and `BackendParityResult`.
3. Require each row to declare `backend_name`, `target_scope`, `value`, optional
   `score`, optional `hessian`, optional `position`, optional
   `latent_position`, `shape`, `branch_label`, `failure_policy_label`, and
   `regularization_label`.
4. Compare all rows against a baseline row selected by name or the first row.
5. Treat value and score parity as hard checks when supplied and required.
6. Treat shape and branch/failure-policy parity as hard checks when required.
7. Treat Hessian parity as explanatory-only by default and expose an explicit
   rejected/unsupported configuration if a caller asks to make it hard without
   a reviewed contract label.
8. Support latent-wrapper parity by letting rows carry `position` and
   `latent_position` metadata or by accepting separate wrapper rows with the
   same target scope and explicit role labels.
9. Export the helper through `bayesfilter.inference` and top-level
   `bayesfilter` if the public API tests require it.
10. Add focused BayesFilter tests for Gaussian exact parity, same-target
    mismatch rejection, shape mismatch, branch-policy mismatch, dense latent
    transform parity, explanatory Hessian differences, and LGSSM Cholesky/QR or
    Cholesky/SVD value parity.
11. Add a MacroFinance compatibility test that converts existing matched-DGP
    direct and wrapper rows into BayesFilter parity rows and asserts the
    BayesFilter gate passes without changing the current target/data/priors.

## Planned Checks

- `python -m pytest tests/test_common_inference_runtime_contracts.py -q`
- `python -m pytest tests/test_v1_public_api.py -q` if export surface changes.
- A focused BayesFilter linear parity test if the generic test module does not
  already cover the LGSSM Cholesky/QR or Cholesky/SVD value case.
- MacroFinance focused compatibility test with
  `PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1
  PYTHONDONTWRITEBYTECODE=1`, targeting the matched-DGP SVD pilot test module.

If the MacroFinance compatibility gate cannot be run because of import-path,
environment, stale-artifact, or fixture issues, Stage 5 enters the repair loop.
It must not weaken same-target metadata or turn MacroFinance-specific fields
into BayesFilter requirements to make the fixture pass.

## Pre-Review Request

Claude should verify that this Stage 5 precheck is consistent with accepted
Phase 7, preserves same-target value/score semantics, keeps Hessian parity
explanatory-only by default, avoids old mismatched Phase 4 data, and keeps
MacroFinance as a client of a BayesFilter-owned parity gate.

## Pre-Review Trail

- `docs/plans/bayesfilter_macrofinance_stage_5_backend_parity_gates_pre_review_round_01.md`
  returned `VERDICT: PROCEED`.
- Implementation must make baseline-row choice explicit in outputs.
- Implementation/result notes must pin the exact MacroFinance compatibility
  test and artifact paths used.

## Implementation Summary

Implemented a BayesFilter-owned backend parity gate in
`bayesfilter/inference/backend_parity.py`.

The implementation adds:

- `BackendParityRow`;
- `BackendParityGate`;
- `BackendParityResult`.

Each row records backend name, target scope, coordinate scope, scalar value,
optional score, optional Hessian, derivative target scope, optional position or
latent position, shape, branch/failure policy labels, regularization labels,
role, and metadata. Supplied scores and Hessians are required to be derivatives
of the row's declared scalar `target_scope`; mismatched derivative target scopes
are rejected at row construction.

The gate:

- requires at least two rows;
- records the baseline backend and whether it was selected by explicit name or
  by first row;
- compares local pointwise value and optional score parity under one target
  scope;
- enforces required shape parity and branch/failure-policy parity by default;
- fails closed when target scopes differ;
- fails closed when target-changing regularization is unlabeled;
- keeps Hessian parity explanatory-only by default;
- rejects hard Hessian parity unless a `reviewed_hessian_contract` is supplied;
- records nonclaims that parity is local fixture evidence only and is not
  posterior convergence, global backend equivalence, or default backend
  readiness.

Exports were updated through `bayesfilter.inference` and the top-level lazy
`bayesfilter` API.

## MacroFinance Compatibility Pin

Exact MacroFinance compatibility test:

- `/home/ubuntu/python/MacroFinance/tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py::test_bayesfilter_backend_parity_gate_represents_matched_dgp_direct_and_wrapper_rows`

Exact current matched-DGP artifact used by that test:

- `/home/ubuntu/python/MacroFinance/results/hmc/mixed_frequency_tfp_phase4_matched_dgp_hessian_scaled_initialization_gate.json`

The compatibility test converts the current
`evaluate_matched_svd_capability_validation(...)` direct Cholesky/SVD-derived
rows and dense-whitening wrapper rows into BayesFilter `BackendParityGate`
evaluations. Each direct point gets its own target scope
`mixed_frequency_tfp_phase4_matched_dgp:<point_name>`, and each wrapper point
gets its own latent-coordinate target scope
`mixed_frequency_tfp_phase4_matched_dgp_wrapper:<point_name>`. The baseline
backend is explicit: `tf_cholesky` for direct rows and
`tf_svd_derived_direct_chain_rule` for wrapper rows.

No MacroFinance likelihood, priors, data payload, parameterization, HMC config,
or artifact semantics were changed.

## Files Touched For Stage 5

BayesFilter:

- `bayesfilter/inference/backend_parity.py`
- `bayesfilter/inference/__init__.py`
- `bayesfilter/__init__.py`
- `tests/test_common_inference_runtime_contracts.py`
- `tests/test_linear_kalman_svd_tf.py`
- `tests/test_v1_public_api.py`
- `docs/plans/bayesfilter_macrofinance_phase_7_backend_parity_gates_result_2026_06_09.md`
- `docs/plans/bayesfilter_macrofinance_stage_5_backend_parity_gates_pre_review_round_01.md`

MacroFinance:

- `tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py`
- `docs/plans/bayesfilter_macrofinance_visible_execution_ledger_2026_06_09.md`

## Checks Run

| Command | Result | Role |
| --- | --- | --- |
| `python -m pytest tests/test_common_inference_runtime_contracts.py -q` from `/home/ubuntu/python/BayesFilter` | `39 passed in 0.20s` | BayesFilter parity contract gate |
| `python -m pytest tests/test_v1_public_api.py -q` from `/home/ubuntu/python/BayesFilter` | `4 passed, 2 warnings in 2.46s` | Public export/lazy import gate |
| `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_linear_kalman_svd_tf.py::test_backend_parity_gate_covers_linear_cholesky_qr_svd_value_fixture -q` from `/home/ubuntu/python/BayesFilter` | `1 passed, 3475 warnings in 4.55s` | LGSSM Cholesky/QR/SVD value parity gate |
| `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_linear_kalman_svd_tf.py -q` from `/home/ubuntu/python/BayesFilter` | `9 passed, 5077 warnings in 6.37s` | BayesFilter SVD module compatibility |
| `env PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py::test_bayesfilter_backend_parity_gate_represents_matched_dgp_direct_and_wrapper_rows -q` from `/home/ubuntu/python/MacroFinance` | `1 passed, 20867 warnings in 42.69s` | MacroFinance BayesFilter parity compatibility gate |
| `env PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py -q` from `/home/ubuntu/python/MacroFinance` | `13 passed, 20867 warnings in 147.80s` | Full matched-DGP compatibility module |

Warnings were TensorFlow Probability `distutils` deprecations, `gast`
deprecations, and BayesFilter `.pytest_cache` write warnings from a read-only
cache path. They are explanatory only for this no-HMC parity gate.

## Repair And Explanatory Notes

- `python -m py_compile bayesfilter/inference/backend_parity.py` failed because
  Python attempted to write a `.pyc` file under
  `/home/ubuntu/python/BayesFilter/bayesfilter/inference/__pycache__`, which is
  read-only in this execution context. This was not treated as a code failure
  because the pytest gates imported and executed the new module successfully.
- No implementation repair loop was needed for Stage 5 test failures; focused
  tests passed on first run after the patch.

## Decision Table

| Item | Status |
| --- | --- |
| Decision | Stage 5 implementation ready for Claude read-only post-review |
| Primary criterion status | Passed focused BayesFilter and MacroFinance no-HMC parity gates |
| Veto diagnostic status | No target-scope mismatch, unlabeled target-changing regularization, shape/branch mismatch, old mismatched payload usage, or Hessian hard-gate promotion observed |
| Main uncertainty | Pointwise parity remains local fixture evidence only |
| Next justified action | Claude read-only post-review |
| What is not concluded | No global backend equivalence, posterior convergence, sampler superiority, empirical validity, GPU/XLA readiness, default backend readiness, or production readiness |

## Post-Run Red Team

Strongest alternative explanation: passing local parity rows may miss
state-dependent backend differences away from the tested LGSSM and matched-DGP
points.

What would overturn the Stage 5 gate: a reproduced case where
`BackendParityGate` passes rows with different scalar targets, silently accepts
unlabeled target-changing regularization, or promotes Hessian parity to hard
evidence without a reviewed contract.

Weakest evidence: MacroFinance compatibility still depends on the current
matched-DGP validation row generator and is not a global search over target
space.

## Post-Review Request

Claude should verify that the implementation satisfies accepted Phase 7,
preserves same-target value/score semantics, records explicit baseline
selection, keeps Hessian parity explanatory-only by default, pins the
MacroFinance compatibility artifact/test, avoids old mismatched Phase 4 data,
and preserves BayesFilter/MacroFinance ownership boundaries.

## Post-Review Trail

- `docs/plans/bayesfilter_macrofinance_stage_5_backend_parity_gates_post_review_round_01.md`
  returned `VERDICT: NEEDS_REVISION`.
- Finding: Hessian telemetry compared Hessians whenever both rows provided
  them, even when the row and baseline used different coordinate scopes. This
  was not a hard-gate issue under the default explanatory-only Hessian role, but
  it made Hessian derivative semantics ambiguous.
- Repair: Hessian comparisons now require matching `coordinate_scope`; if
  coordinate scopes differ, no numeric Hessian diff is reported,
  `hessian_coordinate_scope_matches` is false, explanatory Hessian parity is
  false, and reviewed-hard Hessian parity fails.
- Initial repair test run failed because the aggregate `max_hessian_abs_diff`
  still included the baseline row's trivial zero comparison. Codex tightened
  aggregate max-diff telemetry to exclude baseline self-comparisons for value,
  score, and Hessian summaries.
- Repair reruns:
  - `python -m pytest tests/test_common_inference_runtime_contracts.py -q`:
    `40 passed in 0.16s`.
  - `python -m pytest tests/test_v1_public_api.py -q`: `4 passed, 2 warnings
    in 2.66s`.
  - `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_linear_kalman_svd_tf.py::test_backend_parity_gate_covers_linear_cholesky_qr_svd_value_fixture -q`:
    `1 passed, 3475 warnings in 4.87s`.
  - `env PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_mixed_frequency_tfp_phase4_matched_dgp_svd_derived_hmc_pilot.py::test_bayesfilter_backend_parity_gate_represents_matched_dgp_direct_and_wrapper_rows -q`:
    `1 passed, 20867 warnings in 42.38s`.

## Post-Review Request Round 02

Claude should verify that the Hessian coordinate-scope repair resolves the
round-01 finding and that no new target-scope, derivative-target, baseline,
Hessian-role, ownership, or unsupported-claim issue was introduced.

## Post-Review Trail Round 02

- `docs/plans/bayesfilter_macrofinance_stage_5_backend_parity_gates_post_review_round_02.md`
  returned `VERDICT: PROCEED`.
- Claude confirmed the Hessian coordinate-scope finding was resolved, reviewed
  hard Hessian parity fails on coordinate mismatch, aggregate max-diff telemetry
  avoids baseline self-comparison artifacts, same-target value/score semantics
  did not regress, Hessian parity remains explanatory-only by default, baseline
  handling is explicit, and ownership boundaries remain clean.
- Residual risks: round-01 `NEEDS_REVISION` remains historical review record;
  post-repair reruns were focused rather than full breadth; stronger Hessian
  semantic alignment beyond coordinate label equality would need a future
  reviewed contract.
