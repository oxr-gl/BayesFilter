# BayesFilter Identifiable SSL-LSTM Oracle Geometry Test Plan - 2026-07-08

## Objective

Build and run the smallest proper identifiable SSL-LSTM geometry diagnostic after the 2-observation / 24-parameter toy proved unsuitable.  The diagnostic must test whether the reusable low-rank SPD quadratic geometry utility can recover sensible local curvature on a scalar SSL-LSTM state-space target with enough data and only a few free parameters.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | On an identifiable scalar SSL-LSTM oracle target with a simulated length-200 path, does the low-rank SPD quadratic geometry fit produce a finite SPD local precision that agrees with a dense local Hessian baseline in the same coordinates? |
| Mechanism under test | `fit_low_rank_spd_quadratic_geometry` applied to a scalar SSL-LSTM complete-data oracle likelihood with four free mean parameters and all other parameters fixed at truth. |
| Baseline/comparator | Dense TensorFlow autodiff negative Hessian of the same oracle log posterior at the MAP-candidate center in the same free-parameter coordinates. |
| Expected failure mode | Bad setup would show non-finite values, undersampling relative to regression parameter count, rejected holdout fit, dense Hessian not SPD, or large fitted-vs-dense precision mismatch. |
| Promotion criterion | The run may pass only if the MAP candidate has a small scaled score norm, the dense Hessian is finite SPD, finite samples satisfy at least 5x the regression parameter count, the low-rank fit is accepted, its precision is finite SPD and within the predeclared relative Frobenius tolerance of the dense precision, and the artifact records nonclaims. |
| Promotion veto | Any non-finite target/score/Hessian, MAP-candidate failure, dense Hessian not SPD, sample-ratio failure, low-rank rejection, missing artifact, missing nonclaims, or precision relative Frobenius error above tolerance. |
| Continuation veto | Broken imports, target construction inconsistent with declared free-parameter set, artifact write failure, or a result that invalidates the harness rather than rejecting the candidate. |
| Repair trigger | Low-rank rejection or mismatch on the identifiable oracle triggers narrower trust radius, more samples, or a simpler/free-parameter split before any filtering-likelihood or HMC test. |
| Explanatory diagnostics | Runtime, dense and fitted eigen summaries, center score norm, holdout RMSE, train RMSE, max absolute dense-precision residual, condition numbers, and CPU-hidden device provenance. |
| What must not be concluded | No filtering-likelihood validity, no HMC convergence, no posterior correctness, no sampler superiority, no Zhao-Cui source-faithfulness, no GPU/XLA production readiness, and no default-readiness claim. |

## Evidence Contract

- Scientific question: whether the geometry utility behaves sensibly on a properly identified scalar SSL-LSTM oracle target.
- Exact baseline: dense autodiff negative Hessian in the four-dimensional free-parameter coordinate system.
- Primary pass/fail criterion: `geometry_sanity_passed == true` in the JSON artifact, defined by all promotion criteria above.
- Veto diagnostics: non-finite values, MAP-candidate failure, Hessian non-SPD, low-rank rejection, undersampling, relative Frobenius tolerance failure, artifact/schema failure.
- Explanatory-only diagnostics: runtime, exact fitted eigenvalues, center score norm, train/holdout residuals, max absolute dense-precision residual, and descriptive condition numbers.
- Nonclaims: this is not a filter-likelihood, HMC, convergence, Zhao-Cui source-faithfulness, production, or default-readiness result.
- Artifact preserving result: `docs/benchmarks/identifiable_ssl_lstm_oracle_geometry_cpu_hidden_2026-07-08.json` plus Markdown companion and this result note.

## Design

- Target: scalar SSL-LSTM with `latent_dim=hidden_dim=observation_dim=1`, horizon 200.
- Data: deterministic stateless TensorFlow simulation from `minimal_ssl_lstm_theta()` extended to horizon 200.
- Free parameters: `latent_mean_weight.0.0`, `latent_mean_bias.0`, `observation_weight.0.0`, and `observation_bias.0`.
- Fixed parameters: all LSTM gate, initial-state, process-scale, and observation-scale parameters fixed at truth.
- Likelihood: complete-data oracle Gaussian likelihood for the latent path and observations, plus a weak Gaussian prior around truth.
- Geometry fit: low-rank SPD quadratic parameterization `lambda0 I + Q diag(mu) Q'` in the four-dimensional free coordinate, with effective rank capped at `dim - 1` so the isotropic term and directional terms are identifiable.
- Sample rule: finite samples must be at least five times the regression parameter count `1 + dim + 1 + effective_rank`.

## Required Artifacts

- Plan: this file.
- Benchmark script: `docs/benchmarks/benchmark_identifiable_ssl_lstm_oracle_geometry_2026_07_08.py`.
- Tests: `tests/test_identifiable_ssl_lstm_oracle_geometry.py`.
- JSON output: `docs/benchmarks/identifiable_ssl_lstm_oracle_geometry_cpu_hidden_2026-07-08.json`.
- Markdown output: `docs/benchmarks/identifiable_ssl_lstm_oracle_geometry_cpu_hidden_2026-07-08.md`.
- Result note: `docs/plans/bayesfilter-identifiable-ssl-lstm-oracle-geometry-test-result-2026-07-08.md`.

## Required Checks

- `python -m py_compile docs/benchmarks/benchmark_identifiable_ssl_lstm_oracle_geometry_2026_07_08.py`
- `pytest tests/test_identifiable_ssl_lstm_oracle_geometry.py tests/test_quadratic_geometry.py -q`
- `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_identifiable_ssl_lstm_oracle_geometry_2026_07_08.py`
- `git diff --check`

## Skeptical Plan Audit

| Risk | Audit |
| --- | --- |
| Wrong baseline | Uses dense autodiff Hessian of the same oracle target, not the failed 2-observation target and not HMC tuning success. |
| Proxy metric promoted | Holdout RMSE, max absolute residual, and runtime are not promoted by themselves; relative precision agreement with dense Hessian is required. |
| Missing stop conditions | Harness-invalidity, non-finite values, artifact failure, and sample-ratio failures are continuation vetoes or promotion vetoes. |
| Unfair comparison | Both fitted and dense precision use the same target, center, free coordinates, and CPU-hidden run context. |
| Hidden assumption | Complete-data oracle likelihood is explicitly not a filtering likelihood. |
| Environment mismatch | CPU-hidden debug run is required and recorded; no GPU/XLA readiness claim is allowed. |
| Artifacts would not answer question | JSON records dense baseline, fitted geometry, pass/fail decomposition, free parameters, sample ratio, and nonclaims. |

Audit verdict: pass for a first identifiable geometry diagnostic.  The plan intentionally does not cross into filtering-likelihood or HMC-readiness claims.

## Review Record

Claude review is not used for this pass because prior attempts to send private repository context to the external review gate were blocked.  Local Codex substitute review checked the evidence contract, promotion/veto separation, artifact coverage, and boundary safety before execution.

## Stop Conditions

Stop and write a blocker/result note if the benchmark cannot import, the oracle target is not finite at truth, dense Hessian construction fails, artifacts cannot be written, or checks fail in a way that cannot be repaired locally without changing the scientific question.
