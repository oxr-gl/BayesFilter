# Phase 1 Subplan: Scalar Filtering-Likelihood Geometry Target

Date: 2026-07-08
Status: `DRAFT_READY_FOR_REVIEW`
Master program: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md`
Phase 0 result: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase0-governance-result-2026-07-08.md`

## Phase Objective

Build and run the smallest scalar SSL-LSTM filtering-likelihood geometry diagnostic after the complete-data oracle geometry pass. The diagnostic must use the inherited four free parameters and the existing TensorFlow/TFP filtering score helper, starting with the deterministic `svd_ukf` branch.

This phase answers whether the filtering target can provide finite value/score telemetry and an accepted local SPD geometry candidate in whitened coordinates. It does not run HMC.

## Entry Conditions Inherited From Phase 0

- Phase 0 governance result is `PASSED_WITH_CODEX_SUBSTITUTE_REVIEW`.
- Claude external review is policy-blocked for private-context transfer; material review uses local Codex substitute review unless the user explicitly approves the external transfer after being informed of the risk.
- Existing dirty worktree must be preserved.
- Complete-data oracle result is an anchor only, not proof of filtering-likelihood geometry.
- The coordinate convention for geometry is `theta = center + scale * z`.

## Required Artifacts

- Phase 1 subplan: this file.
- Phase 1 review bundle: `docs/reviews/scalar-filtering-geometry-hmc-phase1-subplan-review-bundle-2026-07-08.md`
- Benchmark script: `docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_geometry_2026_07_08.py`
- Focused tests: `tests/test_scalar_ssl_lstm_filtering_geometry.py`
- JSON artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json`
- Markdown artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.md`
- Log artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.log`
- Phase 1 result: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-filtering-geometry-result-2026-07-08.md`
- Phase 2 subplan draft if geometry is accepted: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase2-mass-handoff-subplan-2026-07-08.md`

## Required Checks, Tests, Reviews

- Review this Phase 1 subplan before code execution. Because Claude review is policy-blocked, use a Codex substitute review over the same bounded artifact set and label it weaker than Claude review.
- `python -m py_compile docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_geometry_2026_07_08.py`
- `pytest tests/test_scalar_ssl_lstm_filtering_geometry.py tests/test_quadratic_geometry.py -q`
- CPU-hidden diagnostic command with quiet logging:

```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_geometry_2026_07_08.py \
  --json-path docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json \
  --markdown-path docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.md \
  > docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.log 2>&1
```

- `git diff --check`
- Review the Phase 1 result and Phase 2 subplan before advancing.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the scalar SSL-LSTM filtering likelihood provide finite value/score telemetry and an accepted local SPD geometry candidate for the inherited four free parameters? |
| Baseline/comparator | Passed complete-data oracle geometry result and current `tf_ssl_lstm_svd_ukf_score` filtering helper. The oracle result is a baseline anchor, not a promotion comparator. |
| Primary criterion | Artifact records finite filtering value/score at the chosen center, declared four-parameter mapping, sufficient finite low-rank geometry samples, accepted SPD/condition-bounded whitened precision, and no hard vetoes. |
| Veto diagnostics | Nonfinite value/score accepted, unknown free parameter, target/score shape mismatch, insufficient finite samples accepted, low-rank geometry rejected but treated as pass, non-SPD or over-conditioned accepted precision, missing CPU-hidden provenance, unsupported HMC/posterior/default claim. |
| Explanatory diagnostics | MAP optimizer status, score norm, dense finite-difference score-Jacobian summary if computed, low-rank residuals, condition numbers, runtime, and comparison to oracle settings. |
| Not concluded | No HMC readiness, HMC convergence, posterior correctness, sampler superiority, statistical ranking, default readiness, GPU/XLA readiness, or Zhao-Cui source-faithfulness. |
| Preserving artifact | Phase 1 result note, benchmark JSON/Markdown/log, focused tests, and ledger entries. |

## Planned Target Design

- Configuration: scalar SSL-LSTM with `latent_dim=1`, `hidden_dim=1`, `observation_dim=1`, and horizon fixed in the benchmark settings before execution.
- Free parameters inherited from the oracle diagnostic:
  - `latent_mean_weight.0.0`
  - `latent_mean_bias.0`
  - `observation_weight.0.0`
  - `observation_bias.0`
- Fixed parameters: all other entries from `minimal_ssl_lstm_theta()`.
- Observations: simulate a scalar observation path from the same fixture-generation route used by the oracle diagnostic, but evaluate only the filtering likelihood.
- Filtering branch: `tf_ssl_lstm_svd_ukf_score` first because it is deterministic and already admitted for analytic score checks.
- Prior: weak Gaussian prior centered on the inherited truth-free values, used only to stabilize the local four-parameter target.
- Geometry: `fit_low_rank_spd_quadratic_geometry` in whitened coordinates with sample-count and condition gates recorded in the artifact.

## Fixed Benchmark Settings Before Execution

| Setting | Value | Provenance | Role |
| --- | --- | --- | --- |
| Horizon | `30` | Repair setting after the first visible horizon-100/260-sample command exceeded the practical Phase 1 visible budget before writing an artifact | Bounded diagnostic setting, not statistical sufficiency |
| Filter branch | `svd_ukf` | Existing deterministic analytic filtering score helper | Initial branch, not default claim |
| Free-parameter scale | `(0.35, 0.35, 0.35, 0.35)` | Inherited from passed oracle diagnostic | Whitened-coordinate scale |
| Prior scale | `4.0` | Inherited from passed oracle diagnostic | Weak local stabilizer |
| Low-rank rank | `4`, effective `3` for four dimensions | Existing utility caps rank at `dim - 1` | Geometry diagnostic setting |
| Low-rank sample count | `72` | Repair setting; still exceeds `5 * (1 + dim + 1 + rank) = 45` | Sample-ratio hard gate |
| Trust radius | `0.30` | Inherited from passed oracle diagnostic | Local geometry region |
| Pilot radius | `0.08` | Inherited from passed oracle diagnostic | Pilot curvature basis |
| Pilot direction count | `64` | Repair setting after first visible command exceeded budget before writing an artifact | Explanatory basis-search effort |
| Eigenvalue floor | `1.0e-4` | Inherited from passed oracle diagnostic | SPD floor |
| Max condition number | `1.0e5` | Inherited from passed oracle diagnostic | Condition hard gate |
| Holdout RMSE absolute tolerance | `5.0e-2` | Inherited from passed oracle diagnostic | Fit-quality hard gate |
| Holdout RMSE relative tolerance | `5.0e-3` | Inherited from passed oracle diagnostic | Fit-quality hard gate |
| MAP iterations | `0` in Phase 1 initial target | Conservative choice after user questioned weak MAP candidates | No MAP claim; center role is `truth_free_initial_center` |
| Command wall timeout | `300` seconds | Repair setting after the first visible command lacked a shell timeout | Execution-flow stop condition |

These repaired settings are fixed before the repaired execution and must be serialized in the Phase 1 JSON artifact. They are not defaults, production settings, statistical sufficiency claims, or scientific claims. The abandoned horizon-100/260-sample command produced no JSON/Markdown artifact and is treated only as an execution-flow repair trigger.

## Forbidden Claims And Actions

- Do not run HMC in Phase 1.
- Do not claim the filtering target is correct just because the geometry candidate passes.
- Do not claim posterior correctness, convergence, sampler superiority, default readiness, GPU/XLA production readiness, or source-faithful Zhao-Cui behavior.
- Do not change BayesFilter default policy.
- Do not install packages, fetch network resources, edit model files, or perform destructive git/filesystem actions.
- Do not revert unrelated dirty worktree changes.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if:

- Phase 1 subplan review has no unresolved material blocker.
- Required checks pass.
- The JSON artifact records `geometry_sanity_passed: true`.
- The artifact records the coordinate system as whitened `theta = center + scale * z`.
- The accepted precision is SPD and condition-bounded by recorded thresholds.
- Phase 1 result states non-claims and distinguishes complete-data oracle evidence from filtering-likelihood evidence.
- Phase 2 mass-handoff subplan is drafted and reviewed.

If geometry is rejected, do not advance to Phase 2. Write the Phase 1 result as a repair-trigger artifact and draft a focused repair subplan instead.

## Stop Conditions

- Phase 1 subplan review returns unresolved `REVISE`.
- Filtering value/score is nonfinite at the initial target center and cannot be localized by a bounded diagnostic.
- The four free-parameter mapping does not match the scalar SSL-LSTM config.
- The benchmark cannot write structured JSON/Markdown/log artifacts.
- Required tests fail and cannot be repaired within the phase scope.
- Continuing would require HMC execution, package installation, network fetch, credentials, default-policy change, model-file edit, destructive git/filesystem action, or unsupported scientific/runtime claim.

## Skeptical Audit

- Wrong baseline: the complete-data oracle is an anchor only; Phase 1 must evaluate filtering-likelihood geometry directly.
- Proxy metric risk: residuals, optimizer status, and condition numbers can explain viability but cannot prove HMC or posterior correctness.
- Missing stop conditions: rejected geometry blocks Phase 2 and triggers repair instead.
- Unfair comparison: there is no stochastic method ranking in Phase 1.
- Hidden assumptions: four-parameter scalar success may not transfer to full SSL-LSTM or Zhao-Cui routes.
- Stale context: prior HMC failures remain relevant; this phase intentionally returns to the filtering geometry prerequisite.
- Environment mismatch: the run is CPU-hidden debug/reference evidence and must not be described as GPU/XLA readiness.
- Artifact adequacy: JSON/Markdown/log artifacts answer target/geometry viability only.

Audit result: `PASS_WITH_BOUNDARIES_PENDING_REVIEW`. Execute only after subplan review.
