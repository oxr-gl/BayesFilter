# Minimal SSL-LSTM Zhao-Cui MAP-Candidate Covariance Geometry Plan

Date: 2026-07-07
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer if available

## Objective

Repair the minimal scalar SSL-LSTM `zhaocui_fixed` HMC geometry path so the first mass matrix is no longer the blunt `0.01^2 I` covariance when a finite local MAP-candidate and local curvature can be computed, and repair the fixed-mass joint `L, epsilon` selector so candidates outside the declared trajectory window are not viable.

This is a diagnostic geometry repair only. It does not claim posterior convergence, zero divergences, tuned-kernel readiness, source-faithful Zhao-Cui parity, sampler superiority, default readiness, or production readiness.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can the minimal scalar `zhaocui_fixed` HMC tuning harness use a better finite SPD initial covariance and prevent out-of-window `L * epsilon` handoffs? |
| Candidate mechanism | Bounded local MAP-candidate search from the current initial position, TensorFlow Hessian/Jacobian curvature at that candidate, SPD eigen-regularized covariance, plus trajectory-window viability enforcement in the joint grid. |
| Baseline/comparator | Current harness: `initial_position` plus `initial_covariance = 0.01^2 I`; current joint grid candidate viability based on ladder pass/acceptance/hard vetoes without requiring `L * epsilon` inside the target trajectory window. |
| Expected failure mode | MAP-candidate optimization or Hessian differentiation may fail, produce non-finite values, or produce indefinite/ill-conditioned curvature; fixed-mass ladders may still fail after the geometry repair. |
| Promotion criterion | Local checks pass and a CPU-hidden diagnostic rerun writes structured artifacts where geometry provenance records either `regularized_negative_hessian_at_map_candidate` or an explicit fallback, and joint-grid candidates outside the trajectory window are non-viable. |
| Promotion veto | Non-finite MAP-candidate/value/gradient/Hessian; invalid SPD covariance artifact; missing provenance; candidate outside trajectory window still marked viable; broken existing HMC tuning tests. |
| Continuation veto | Test failures in touched HMC selector/geometry harness tests that cannot be explained and repaired locally; runtime artifact missing or corrupt; plan evidence contract violated. |
| Repair trigger | Out-of-window joint candidate marked viable; MAP-candidate builder silently falling back without artifact metadata; diagnostic rerun still selecting tau far outside the window without recording trajectory-window repair triggers. |
| Explanatory diagnostics | MAP-candidate optimizer status, objective/gradient norm, Hessian eigenvalues, clipped eigenvalue count, condition number, selected `L`, step size, `L * step_size`, acceptance, runtime, budget status. |
| Must not conclude | No posterior correctness, convergence, zero-divergence, source-faithful Zhao-Cui parity, superiority, default-readiness, production-readiness, or public API readiness claim. |

## Skeptical Audit

- Wrong baseline: baseline is explicitly the current `0.01^2 I` initial covariance and current selector behavior, not Phase 3/4 sampler quality.
- Proxy metric risk: acceptance and runtime remain explanatory only. The selector validity repair uses the predeclared trajectory window as a hard viability condition, not as evidence of convergence.
- Missing stop conditions: the plan stops on unrepaired test failure, invalid artifact, non-finite geometry artifact, or missing review/evidence notes.
- Unfair comparison risk: the rerun is a before/after diagnostic against the latest comparable CPU-hidden artifact, not a ranking or performance claim.
- Hidden assumptions: the local optimizer finds a `map_candidate`, not a certified global MAP. The plan must preserve `position_role="map_candidate"` or equivalent non-promoting language.
- Environment mismatch: CPU-hidden diagnostic rerun must set `CUDA_VISIBLE_DEVICES=-1`; GPU/XLA readiness is not being tested.
- Artifact adequacy: required artifacts include plan, review bundle/gate status, code diffs, focused tests, and rerun JSON/Markdown/private tuning artifacts. These answer the stated geometry/selector question without smuggling sampler-readiness claims.

Audit result: pass to execute after read-only review or documented Claude unavailability/fallback. The plan uses a bounded diagnostic rerun and explicit nonclaims.

## Implementation Plan

1. Add a benchmark-local MAP-candidate covariance builder in `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py`.
   - Use `tfp.optimizer.lbfgs_minimize` on `-adapter.log_prob_and_grad(theta)` from the existing `initial_position`.
   - Compute local negative log-posterior Hessian as the negative Jacobian of the adapter score at the MAP candidate.
   - Symmetrize and pass the curvature through the existing BayesFilter geometry regularization by supplying `negative_hessian` to `tune_hmc_kernel`.
   - Fall back to the old covariance only with explicit artifact metadata and non-promoting language.

2. Preserve provenance in the phase artifact.
   - Record `initial_geometry_strategy`, `initial_geometry_diagnostics`, MAP-candidate optimizer status, finite checks, Hessian eigen summary, and fallback reason if any.
   - Keep the predeclared settings and result note clear that this is a diagnostic geometry initializer.

3. Repair joint `L, epsilon` viability in `bayesfilter/inference/hmc_kernel_tuning.py`.
   - Reuse the existing trajectory-window helpers.
   - Record `trajectory_window`, `trajectory_window_relation`, and `trajectory_target_ratio` on joint candidates.
   - Make `viable` require `trajectory_window_relation == "inside_trajectory_window"`.
   - Append `trajectory_length_outside_window`, plus direction-specific repair triggers, to candidate repair triggers when outside.

4. Add or update tests.
   - Harness test: MAP-candidate covariance diagnostics are finite and either use a negative Hessian or explicitly record fallback.
   - Selector test: a ladder-passed candidate with good acceptance but huge `L * epsilon` is not viable and gets trajectory-window repair triggers.
   - Preserve existing expectations for public nonclaims and CPU-hidden diagnostic scope.

5. Run local checks.
   - `PYTHONPYCACHEPREFIX=/tmp/bayesfilter-pycache CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m py_compile bayesfilter/inference/hmc_kernel_tuning.py docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py`
   - `PYTHONPYCACHEPREFIX=/tmp/bayesfilter-pycache CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest tests/test_hmc_kernel_tuning_fixed_mass_step.py tests/test_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5.py -q`
   - `git diff --check`

6. Run a bounded CPU-hidden diagnostic artifact.
   - Use fresh output names under `docs/benchmarks/` with date `2026-07-07`.
   - Preserve public timeout and terminal repair slot consistent with the recent comparable patch-validation run.

## Required Artifacts

- Plan: `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-map-covariance-geometry-plan-2026-07-07.md`
- Claude review bundle: `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-map-covariance-geometry-review-bundle-2026-07-07.md`
- Result note: `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-map-covariance-geometry-result-2026-07-07.md`
- Code edits:
  - `bayesfilter/inference/hmc_kernel_tuning.py`
  - `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py`
  - focused tests under `tests/`
- Diagnostic JSON/Markdown and tuning output directory under `docs/benchmarks/`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Does a MAP-candidate Hessian covariance initializer plus tau-window viability gate remove the known geometry/selector defect in the minimal diagnostic harness? |
| Exact baseline | Latest comparable CPU-hidden patch validation artifact using `initial_covariance = 0.01^2 I` and out-of-window joint candidate viability. |
| Primary pass/fail criterion | Focused tests pass; joint candidates outside trajectory window cannot be viable; rerun artifact records finite geometry provenance and structured tuning result or honest non-promoting blocker. |
| Veto diagnostics | Non-finite value/gradient/Hessian; invalid SPD mass artifact; candidate outside trajectory window marked viable; broken focused tests; missing artifact provenance; unsupported sampler-readiness claim. |
| Explanatory only | Acceptance, runtime, candidate count, selected step, selected `L`, descriptive tau distance, optimizer iterations, Hessian condition number. |
| Not concluded | Posterior correctness, convergence, zero divergences, superiority, source-faithful Zhao-Cui parity, default readiness, production readiness, GPU/XLA readiness. |
| Preserving artifact | Result note plus rerun JSON/Markdown and private tuning events. |

## Review Requirements

Claude is read-only. Claude may inspect this plan, the compact review bundle, and the named source/test files. Claude cannot authorize scientific claims or runtime/default-policy promotions.

Review questions:

1. Does the plan correctly separate a `map_candidate` geometry diagnostic from a true MAP or posterior correctness claim?
2. Does the tau-window viability repair address the observed `L * epsilon` bug without changing acceptance or hard-veto semantics incorrectly?
3. Are the proposed checks sufficient for a bounded diagnostic repair?
4. Are any unsupported numeric defaults or hidden authority transfers present?

## Stop Conditions

- Claude review returns `REVISE` for a material issue that cannot be patched locally.
- Focused tests or py_compile fail after reasonable repair.
- Diagnostic artifact cannot be written or lacks geometry/trajectory provenance.
- Any result would require claiming posterior correctness, zero divergences, convergence, source-faithful Zhao-Cui parity, sampler superiority, default readiness, or production readiness.
