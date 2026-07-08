# Phase 1 Subplan: Low-Rank SPD Quadratic Geometry Utility

Date: 2026-07-08
Status: `DRAFT_PENDING_PHASE0_GATE`
Master program: `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-master-program-2026-07-08.md`

## Phase Objective

Implement a reusable BayesFilter utility for fitting low-rank SPD quadratic geometry in whitened coordinates, with focused unit tests for the mechanical gates.

## Entry Conditions Inherited From Phase 0

- Phase 0 result records plan/review gate pass or documented substitute review.
- `git diff --check` passed for planning artifacts.
- No unresolved material review blocker remains.
- Work remains classified as `extension_or_invention`.

## Required Artifacts

- Source: `bayesfilter/inference/quadratic_geometry.py`
- Export update if needed: `bayesfilter/inference/__init__.py`
- Tests: `tests/test_quadratic_geometry.py`
- Phase 1 result: `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase1-utility-result-2026-07-08.md`
- Refreshed Phase 2 subplan: `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase2-minimal-ssl-lstm-integration-subplan-2026-07-08.md`

## Utility Design

Fit in whitened coordinates:

```text
ell(c + S z) ~= a + b'z - 0.5 z'Kz
K = lambda0 I + Q diag(mu) Q'
```

Constraints:

```text
lambda0 >= eigenvalue_floor
mu_j >= 0
(lambda0 + max(mu)) / lambda0 <= max_condition_number
finite_sample_count >= min_samples_per_parameter * regression_parameter_count
```

Regression parameter count after fixing `Q`:

```text
1 + d + 1 + rank
```

`Q` is fixed by a pilot symmetric directional-curvature sketch. The fit returns structured diagnostics including precision, covariance, eigen summaries, finite sample count, parameter count, train/holdout residuals, pilot curvature diagnostics, and center-refinement accept/reject metadata.

## Required Checks, Tests, Reviews

- `PYTHONPYCACHEPREFIX=/tmp/bayesfilter-pycache CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m py_compile bayesfilter/inference/quadratic_geometry.py tests/test_quadratic_geometry.py`
- `PYTHONPYCACHEPREFIX=/tmp/bayesfilter-pycache CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest tests/test_quadratic_geometry.py -q`
- `git diff --check`
- Codex self-review of source/test diff before Phase 2.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the utility enforce the declared SPD, condition, sample-ratio, finite-value, holdout, and center-refinement gates on controlled targets? |
| Baseline/comparator | Synthetic quadratic targets with known low-rank SPD precision and adversarial under-sampled/nonfinite/bad-fit cases. |
| Primary criterion | Focused tests pass and result payloads expose the required diagnostics. |
| Veto diagnostics | Accepted under-sampled fit, non-SPD precision, over-condition matrix, nonfinite silent accept, bad holdout accepted, out-of-trust refined center accepted, nondeterministic seed behavior. |
| Explanatory only | Numeric residual magnitudes and estimated condition numbers beyond pass/fail thresholds. |
| Not concluded | No HMC performance, posterior correctness, MAP certification, or target-specific readiness. |
| Preserving artifact | Phase 1 result note with commands/checks and code path references. |

## Forbidden Claims And Actions

- Do not claim the utility computes a true MAP.
- Do not claim a good fit implies a good HMC mass matrix on real targets.
- Do not use NumPy as the gradient-bearing algorithmic backend; NumPy is allowed only for deterministic array assembly, reporting, and independent test checks.
- Do not change default HMC policy or public API readiness.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if:

- Source and focused tests are implemented.
- Required Phase 1 checks pass.
- Phase 1 result records evidence and nonclaims.
- Phase 2 subplan is drafted/refreshed and reviewed locally for consistency.

## Stop Conditions

- TFP/TensorFlow dependencies are unavailable in the existing environment.
- The constrained fit cannot satisfy SPD/condition/sample-ratio gates on controlled tests without changing the evidence contract.
- Required focused tests fail after local repair.
- Any implementation path would require package installation or a non-default backend exception.
