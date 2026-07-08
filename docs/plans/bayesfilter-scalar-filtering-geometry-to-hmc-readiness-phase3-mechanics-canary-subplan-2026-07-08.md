# Phase 3 Subplan: HMC Mechanics Canary

Date: 2026-07-08
Status: `DRAFT_READY_FOR_REVIEW`
Master program: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md`
Phase 2 result: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase2-mass-handoff-result-2026-07-08.md`

## Phase Objective

Run a tiny HMC mechanics canary with the Phase 2 mass handoff applied as an affine preconditioner over the Phase 1 whitened coordinates. The canary checks only whether a fixed small grid of `L`, step size, and trajectory length can evaluate finite energies and produce bounded launch telemetry.

This phase is not a posterior validation, convergence run, or sampler ranking.

## Entry Conditions Inherited From Phase 2

- Phase 2 mass handoff artifact exists and reports `mass_handoff_passed: true`.
- Handoff matrix is `M_z`, a whitened covariance/mass candidate.
- Inverse-mass/precision convention is explicit as `K_z`.
- Center role remains `truth_free_initial_center`, not MAP.
- Phase 1 and Phase 2 artifacts are CPU-hidden debug/reference evidence, not GPU/XLA production evidence.

## Required Artifacts

- Phase 3 subplan: this file.
- Phase 3 review bundle: `docs/reviews/scalar-filtering-geometry-hmc-phase3-mechanics-canary-review-bundle-2026-07-08.md`
- Mechanics canary script: `docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_hmc_mechanics_canary_2026_07_08.py`
- Focused tests: `tests/test_scalar_ssl_lstm_filtering_hmc_mechanics_canary.py`
- JSON artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_mechanics_canary_cpu_hidden_2026-07-08.json`
- Markdown artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_mechanics_canary_cpu_hidden_2026-07-08.md`
- Log artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_mechanics_canary_cpu_hidden_2026-07-08.log`
- Phase 3 result: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase3-mechanics-canary-result-2026-07-08.md`
- Phase 4 subplan draft if mechanics canary passes.

## Required Checks, Tests, Reviews

- Local Codex substitute review of this Phase 3 subplan because Claude review is policy-blocked for private repository context transfer.
- `python -m py_compile docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_hmc_mechanics_canary_2026_07_08.py`
- `pytest tests/test_scalar_ssl_lstm_filtering_hmc_mechanics_canary.py -q`
- CPU-hidden mechanics canary command:

```bash
timeout 180 env CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_hmc_mechanics_canary_2026_07_08.py \
  --geometry-json docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json \
  --mass-json docs/benchmarks/scalar_ssl_lstm_filtering_mass_handoff_cpu_hidden_2026-07-08.json \
  --json-path docs/benchmarks/scalar_ssl_lstm_filtering_hmc_mechanics_canary_cpu_hidden_2026-07-08.json \
  --markdown-path docs/benchmarks/scalar_ssl_lstm_filtering_hmc_mechanics_canary_cpu_hidden_2026-07-08.md \
  > docs/benchmarks/scalar_ssl_lstm_filtering_hmc_mechanics_canary_cpu_hidden_2026-07-08.log 2>&1
```

- `git diff --check`
- Review Phase 3 result and Phase 4 subplan before any short HMC smoke.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a tiny fixed-grid mass-preconditioned HMC mechanics canary evaluate finite target/energy telemetry using the Phase 2 mass handoff? |
| Baseline/comparator | Phase 2 mass handoff artifact. No sampler ranking is attempted. |
| Primary criterion | At least one predeclared tiny candidate has finite initial and proposal target values, finite Hamiltonian change, no runtime exception, and records trajectory length `L * epsilon`; all metrics remain mechanics-only. |
| Veto diagnostics | Target nonfinite, energy nonfinite, runtime exception, coordinate/mass convention mismatch, missing artifacts, timeout, hidden posterior/convergence/default claim. |
| Explanatory diagnostics | Acceptance probability, log accept ratio, `L * epsilon`, energy change, candidate runtime, and whether the user heuristic near `1.57` is approached. |
| Not concluded | No posterior correctness, HMC convergence, zero divergences, sampler superiority, statistical ranking, default readiness, GPU/XLA readiness, or Zhao-Cui source-faithfulness. |
| Preserving artifact | Phase 3 JSON/Markdown/log/result note and ledger entry. |

## Fixed Canary Settings

| Setting | Value | Provenance | Role |
| --- | --- | --- | --- |
| Target coordinate | Phase 1 whitened `z`, `theta = center + scale * z` | Phase 1/2 contract | Binding |
| TFP HMC coordinate | Internal unit coordinate `u`, with `z = u @ chol(M_z).T` | TFP HMC identity kinetic energy plus Phase 2 mass handoff | Binding |
| Mass matrix use | `M_z` is the covariance/mass handoff; `chol(M_z)` is used only as the affine factor from `u` into `z`; `K_z = inv(M_z)` remains the precision convention | Phase 2 artifact | Binding |
| Initial position | `u = 0` | Centered mechanics preflight | Mechanics diagnostic |
| Candidate grid | Exactly `(L, epsilon)` in `{(1, 0.10), (2, 0.25), (4, 0.3925)}`, so `L * epsilon` is `{0.10, 0.50, 1.57}` | User trajectory-length heuristic plus safety | Mechanics diagnostic only |
| Timeout | `180` seconds | Visible execution cap | Continuation veto |

## Forbidden Claims And Actions

- Do not claim posterior correctness, HMC convergence, tuned step size, zero divergences, sampler superiority, or default readiness.
- Do not change Phase 1/2 artifacts.
- Do not use original-coordinate mass by accident.
- Do not pass `M_z` to a TFP API as though stock TFP HMC directly accepted a dense mass matrix; represent it explicitly through the affine `u -> z` transform.
- Do not treat `L * epsilon ~= 1.57` as proof of correctness.
- Do not install packages, fetch network resources, edit model files, or perform destructive git/filesystem actions.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 only if:

- Phase 3 subplan review has no unresolved material blocker.
- Required checks pass.
- Phase 3 artifact reports no hard vetoes.
- At least one candidate has finite mechanics telemetry.
- Phase 3 result preserves non-claims and labels all HMC metrics as mechanics-only.
- Phase 4 short-smoke subplan is drafted and reviewed.

If all candidates fail, write a Phase 3 blocker/repair result and stop before short HMC smoke.

## Stop Conditions

- Phase 3 subplan review returns unresolved `REVISE`.
- Mechanics script cannot validate coordinate/mass conventions.
- All candidates produce nonfinite target/energy or runtime exceptions.
- Required tests fail and cannot be repaired within Phase 3 scope.
- Continuing would require package installation, network fetch, credentials, default-policy change, model-file edit, destructive git/filesystem action, or unsupported scientific/runtime claim.

## Skeptical Audit

- Wrong baseline: Phase 3 tests mechanics against Phase 2 mass handoff, not posterior quality.
- Proxy metric risk: acceptance, energy change, and trajectory length are mechanics diagnostics only.
- Missing stop conditions: all nonfinite/runtime failures stop before Phase 4.
- Unfair comparison: no ranking or stochastic method comparison occurs.
- Hidden assumptions: a finite mechanics canary may still fail short chains or longer validation.
- Stale context: previous trajectory tuning concerns motivate recording `L * epsilon`, but not promoting it.
- Environment mismatch: CPU-hidden canary is not GPU/XLA production evidence.
- Artifact adequacy: JSON/Markdown/log answer only finite mechanics telemetry.

Audit result: `PASS_WITH_BOUNDARIES_PENDING_REVIEW`. Execute only after Phase 3 subplan review.
