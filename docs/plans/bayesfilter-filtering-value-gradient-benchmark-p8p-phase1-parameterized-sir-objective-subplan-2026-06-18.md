# P8p Phase 1 Subplan: Parameterized SIR Objective Contract

Date: 2026-06-18

Status: `ACTIVE_AFTER_PHASE0_PASS`

## Phase Objective

Design the parameterized SIR d18 diagnostic objective before implementation.
The objective must be small enough to debug and meaningful enough for HMC
mechanics:

```text
theta = [
  log_kappa_scale,
  log_nu_scale,
  log_obs_noise_scale
]
```

Phase 1 must specify how theta enters the existing actual-SIR streaming
callbacks, how common random numbers are frozen, and which artifacts Phase 2
must implement.

The current value-only harness is not already parameterized.  Phase 1 must
bind theta to exact implementation points before Phase 2 edits code:

- `docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py::_make_actual_sir_callbacks`
  currently captures fixed `kappa`, `nu`, `process_chol`, and
  `observation_covariance`;
- `transition_mean` and its nested `sir_rhs` must receive theta-dependent
  `kappa` and `nu`;
- `pre_flow_step` must use theta-dependent transition means while preserving
  fixed stateless process-noise draws;
- `transition_log_density_fn` must use the same theta-dependent transition
  mean as `pre_flow_step`;
- `observation_log_density_fn`, LEDH flow covariance inputs, and the tiled
  `observation_covariance` tensor must receive theta-dependent observation
  covariance for `log_obs_noise_scale`;
- Phase 2 must add or wrap a value-and-gradient path with explicit per-theta
  connectivity diagnostics, because the existing streaming score helper
  zero-fills unconnected gradients.

## Entry Conditions Inherited From Previous Phase

Phase 1 may start only after Phase 0 passes:

- P8p lane boundary reviewed;
- P8o value-only result confirmed as entry evidence only;
- Phase 0 result written;
- Claude review converged on the master program/runbook/Phase 1 draft.

## Required Artifacts

- Phase 1 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase1-parameterized-sir-objective-result-2026-06-18.md`
- Phase 2 subplan draft:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase2-gradient-smoke-subplan-2026-06-18.md`
- If code edits are needed, a minimal implementation-surface note naming exact
  files and tests before edits.

## Required Checks, Tests, And Reviews

Required local checks before result:

```bash
python -m py_compile docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py
rg -n "transition_mean|pre_flow_step|observation_log_density_fn|process_chol|observation_covariance|kappa|nu" docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py bayesfilter/highdim/models.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-*
```

Required review:

- Claude read-only review if the target contract changes theta, changes the
  fixed-randomness policy, changes allowed claims, or identifies code edits.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the proposed theta target differentiable, fixed-randomness, SIR d18-shaped, and narrow enough for diagnostic gradient/HMC-mechanics testing? |
| Baseline/comparator | Current fixed-parameter actual-SIR harness with P8o settings at theta zero. |
| Primary pass criterion | Phase 1 passes if the result specifies theta transforms, fixed observations, fixed initial/process random streams, differentiable relaxed OT, no categorical resampling, exact implementation surface, Phase 2 smoke sizes, and forbidden claims. |
| Veto diagnostics | Random streams depending on theta; stochastic categorical resampling; theta changes that alter state/observation dimensions; hidden NumPy implementation for differentiable path; missing fixed-seed contract; relying only on the zero-filled score helper for connectivity; missing exact theta-dependent edit points; claiming scientific posterior parameterization. |
| Explanatory diagnostics | Code anchors, callback contract, shape contract, chosen smoke sizes, expected runtime and memory. |
| Not concluded | Gradient correctness, HMC readiness, exact likelihood correctness, posterior validity, or production/default readiness. |
| Artifact | Phase 1 result and Phase 2 subplan. |

## Forbidden Claims And Actions

- Do not run the full SIR d18 N=10000/N=50000 ladder in Phase 1.
- Do not claim the diagnostic theta is the scientific posterior target.
- Do not use PyTorch/JAX/NumPy for BayesFilter-owned differentiable
  implementation paths.
- Do not change fixed-parameter P8o leaderboard artifacts.
- Do not modify unrelated Zhao-Cui fixed-branch or monograph files.
- Do not pass Phase 1 unless the result names exact theta-dependent edit points
  and the explicit connectivity diagnostic required in Phase 2.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if:

- Phase 1 result defines the theta contract and implementation surface;
- Phase 2 subplan exists and includes a small gradient smoke, for example
  `T=3`, small `N`, one or two seeds, trusted GPU if GPU is claimed;
- fixed-randomness and relaxed-OT policies are explicit;
- the Phase 2 connectivity diagnostic is explicit and is not satisfied merely
  by the current zero-filled score helper;
- local checks pass and review converges for material target changes.

## Stop Conditions

Stop and write a blocker if:

- the target requires a human scientific decision beyond the diagnostic
  three-parameter scale target;
- the current harness cannot support theta without a broad rewrite;
- fixed randomness cannot be preserved through the streaming route;
- implementation would require package installation, network, credentials, or
  unrelated dirty-worktree edits.
