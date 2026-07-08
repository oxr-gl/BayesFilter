# Codex Substitute Review: Minimal SSL-LSTM Zhao-Cui MAP-Candidate Covariance Geometry

Date: 2026-07-07

Reviewer: Codex visible substitute review

Claude status: unavailable for this private repository lane because the
external Claude review gate was rejected for private-context transfer risk. No
workaround was attempted.

Reviewed artifacts:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-map-covariance-geometry-plan-2026-07-07.md`
- `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-map-covariance-geometry-review-bundle-2026-07-07.md`
- `bayesfilter/inference/hmc_kernel_tuning.py`
- `bayesfilter/inference/mass_matrix.py`
- `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py`
- `tests/test_hmc_kernel_tuning_fixed_mass_step.py`
- `tests/test_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5.py`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_map_covariance_prior_floor_cpu_hidden_2026-07-07.json`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_map_covariance_prior_floor_public_artifacts_2026-07-07/`

## Review Scope

Check the plan and execution for consistency, correctness, feasibility,
artifact coverage, boundary safety, and repair-loop fit. This review is scoped
to the MAP-candidate/initial-position curvature geometry diagnostic and the
joint `L, epsilon` trajectory-window viability gate. It does not certify
unrelated dirty worktree changes from the larger HMC runbook.

## Findings

No blocking findings for the bounded diagnostic repair.

The execution preserves the planned distinction between a local
`map_candidate` attempt and a valid MAP covariance. The diagnostic artifact
correctly rejects the MAP candidate because the score norm is far above the
diagnostic tolerance, then falls back to a finite regularized negative Hessian
at the initial position with explicit `position_role="initial_position"` and
`covariance_source="regularized_negative_hessian_at_initial_position"`
metadata.

The joint `L, epsilon` viability repair addresses the observed defect: ladder
candidates outside the declared trajectory window are marked non-viable and
receive direction-specific repair triggers. The fresh diagnostic shows the two
ladder-passed candidates had `L * epsilon` below the window and were not
selected.

## Review Checklist

| Check | Status | Note |
| --- | --- | --- |
| Research question preserved | `PASS` | The phase asks whether geometry provenance and tau-window viability are repaired, not whether HMC converged. |
| Baseline identified | `PASS` | The plan names the prior `0.01^2 I` covariance and acceptance-only joint viability behavior. |
| MAP wording boundary | `PASS` | Artifact labels the final source as initial-position curvature, not MAP. |
| SPD mass provenance | `PASS` | Private mass summary is finite, positive definite, and records eigenvalue floor/provenance. |
| Tau-window gate | `PASS` | Out-of-window candidates are non-viable and carry `trajectory_length_outside_window` plus direction triggers. |
| Tests/checks | `PASS` | Focused py_compile, pytest, and `git diff --check` passed after recovery. |
| Artifact coverage | `PASS` | Plan, review bundle, substitute review, JSON/Markdown diagnostics, and private tuning events are present. |
| Boundary safety | `PASS` | CPU-hidden diagnostic only; no GPU/XLA, default-policy, public API, model-file, or source-faithful claim is introduced. |
| Statistical discipline | `PASS` | Runtime, acceptance, candidate counts, and tau distances remain descriptive diagnostics. |
| Zhao-Cui source gate | `PASS` | No source-faithful Zhao-Cui parity claim is made. |

## Residual Risks

- The fixed-mass joint grid still found no viable handoff pair. This is a
  tuning-design blocker, not a geometry-validity success.
- The accepted diagnostic covariance is not a MAP covariance; it is a
  regularized initial-position curvature fallback after a rejected MAP
  candidate.
- The evidence is CPU-hidden and smoke-scale, with no posterior correctness,
  convergence, zero-divergence, GPU/XLA-readiness, or statistical ranking
  support.
- The current worktree contains broader prior runbook changes. This review
  covers the named plan and artifacts only.

## Verdict

`VERDICT: AGREE`

The plan and executed artifacts are acceptable as a non-promoting diagnostic
repair. The next work should target the remaining no-viable-pair fixed-mass
tuning design blocker under a separate reviewed subplan.
