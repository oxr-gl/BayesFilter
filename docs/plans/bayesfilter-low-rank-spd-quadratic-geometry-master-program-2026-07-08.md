# BayesFilter Low-Rank SPD Quadratic Geometry Master Program

Date: 2026-07-08
Status: `DRAFT_MASTER_PROGRAM_READY_FOR_PHASE0_REVIEW`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer if available; Codex substitute review if Claude is unavailable or blocked

## Objective

Implement a reusable BayesFilter utility for low-rank SPD quadratic regression geometry in whitened coordinates, then integrate it as an optional initial-geometry path in the minimal scalar SSL-LSTM `zhaocui_fixed` HMC tuning diagnostic.

This is classified as `extension_or_invention`. It is not Zhao-Cui source-faithful behavior and must not close any Zhao-Cui source-anchor gate.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can a reusable low-rank SPD quadratic fit provide a finite, bounded-condition initial precision/covariance candidate for difficult HMC geometry diagnostics? |
| Candidate mechanism | Fit `log p(c + S z) ~= a + b'z - 0.5 z'Kz` in whitened coordinates with `K = lambda0 I + Q diag(mu) Q'`, SPD and condition bounded by construction. |
| Baseline/comparator | Current minimal SSL-LSTM geometry path: rejected L-BFGS MAP candidate, local initial-position negative Hessian fallback, or `0.01^2 I` covariance fallback. |
| Expected failure mode | Function values may be too nonquadratic, nonfinite, under-sampled, or poorly fit; refined center may fail trust-region or score checks; short HMC tuning may still find no viable `L, epsilon` pair. |
| Promotion criterion | Focused unit tests pass and the minimal diagnostic can record structured low-rank SPD geometry diagnostics or an honest fallback without unsupported claims. |
| Promotion veto | Undersampled regression accepted; non-SPD or over-condition precision accepted; nonfinite values silently accepted; bad holdout fit accepted; out-of-trust refined center accepted; missing provenance. |
| Continuation veto | Touched tests fail after local repair, plan/review gate returns unresolved material `REVISE`, utility cannot produce structured diagnostics, or integration would require default policy/scientific claim boundary crossing. |
| Repair trigger | Bad synthetic recovery, condition cap violation, unstable deterministic behavior, minimal diagnostic artifact missing low-rank geometry provenance, or benchmark still treating proxy diagnostics as promotion evidence. |
| Explanatory diagnostics | Fit residuals, holdout residuals, finite sample count, parameter count, eigenvalue summaries, condition number, pilot curvature count, center-refinement diagnostics, step/leapfrog/tau summaries. |
| Must not conclude | No posterior correctness, HMC convergence, zero divergences, sampler superiority, default readiness, production readiness, public API readiness, package readiness, GPU/XLA readiness, or Zhao-Cui source-faithful parity. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance, plan, and review gate | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase0-governance-subplan-2026-07-08.md` | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase0-governance-result-2026-07-08.md` |
| 1 | General utility and focused unit tests | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase1-utility-subplan-2026-07-08.md` | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase1-utility-result-2026-07-08.md` |
| 2 | Minimal SSL-LSTM diagnostic integration | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase2-minimal-ssl-lstm-integration-subplan-2026-07-08.md` | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase2-minimal-ssl-lstm-integration-result-2026-07-08.md` |
| 3 | Focused checks and bounded CPU-hidden diagnostic | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase3-checks-diagnostic-subplan-2026-07-08.md` | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase3-checks-diagnostic-result-2026-07-08.md` |
| 4 | Closeout and next handoff | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase4-closeout-subplan-2026-07-08.md` | `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase4-closeout-result-2026-07-08.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can the repository own a reusable TensorFlow/TFP-oriented low-rank SPD quadratic geometry utility with explicit safeguards and diagnostics? |
| Scientific question | Only whether this diagnostic geometry mechanism is mechanically valid on focused checks and useful enough to try in the minimal target; not whether HMC converges. |
| Exact baseline | Existing `map_candidate_hessian` / `initial_covariance` path in `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py`. |
| Primary pass criterion | Unit tests pass; utility enforces SPD, condition cap, sample-ratio, finite-value, holdout, and center-refinement gates; benchmark artifact records provenance. |
| Veto diagnostics | Failed focused tests, accepted under-sampled fit, accepted non-SPD precision, accepted over-condition matrix, nonfinite silent accept, missing artifact provenance, unsupported readiness claim. |
| Explanatory only | Residual sizes, score norm changes, optimizer iterations, condition number magnitude, HMC acceptance, runtime, candidate count, tau distance. |
| Not concluded | Posterior correctness, HMC convergence, zero divergences, statistical ranking, superiority, default readiness, GPU/XLA readiness, Zhao-Cui source-faithfulness. |
| Preserving artifacts | Plan/subplan/result docs, review bundle/status, source/test diffs, diagnostic JSON/Markdown/logs. |

## Default And Assumption Audit

| Choice | Provenance | Classification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Rank `4` default | User/Codex design discussion for `d=24`, parameter count small enough for sample-ratio rule | Hypothesis default | Too low rank misses geometry | Synthetic and minimal diagnostic residuals | Reviewed in Phase 1 |
| Minimum finite samples `5 * n_params` | User instruction | Owner/user constraint | Too few samples overfits quadratic | Explicit sample-ratio rejection test | Binding |
| `K = lambda0 I + Q diag(mu) Q'` | User/Codex design discussion | Design constraint | Too restrictive for some targets | Holdout residual and fallback path | Reviewed |
| Condition cap `1e3` for new utility default | Prior discussion; lower than previous HMC cap | Hypothesis default | Too tight or too loose for target | Condition enforcement and diagnostic artifact | Reviewed in Phase 1 |
| CPU-hidden bounded diagnostic | Existing Phase 5 diagnostic lane | Debug/reference exception | CPU result mistaken for GPU evidence | Artifact records `CUDA_VISIBLE_DEVICES=-1` | Binding |

## Skeptical Plan Audit

- Wrong baseline: baseline is the existing initial-geometry path, not posterior quality or sampler performance.
- Proxy metric risk: regression residuals and HMC acceptance are not promotion criteria for posterior correctness; they only pass/fail the geometry diagnostic gates declared above.
- Missing stop conditions: phase subplans include stop conditions for review failure, test failure, invalid artifacts, unsupported claims, and boundary crossings.
- Unfair comparison risk: the minimal diagnostic is a first client and not a ranking against MAP Hessian, windowed mass, or other samplers.
- Hidden assumptions: the fitted center is a local quadratic suggestion, not a certified MAP. The plan requires explicit `extension_or_invention` classification.
- Stale context: this plan builds on the 2026-07-07 result where the L-BFGS MAP candidate failed stationarity and the tau window had no viable pair.
- Environment mismatch: production target remains GPU/XLA, but Phase 3 is explicitly CPU-hidden diagnostic only.
- Artifact adequacy: the utility tests answer mechanical geometry questions; the bounded diagnostic answers integration/provenance only.

Audit result: `PASS_WITH_BOUNDARIES`. Execution may start after Phase 0 review gate or documented reviewer unavailability/substitute review.

## Forbidden Claims

- Do not claim true MAP covariance unless a separate MAP plan proves stationarity and curvature quality.
- Do not claim posterior correctness, HMC convergence, zero divergences, sampler superiority, default readiness, production readiness, public API/package readiness, GPU/XLA readiness, or Zhao-Cui source-faithful parity.
- Do not treat residuals, short-chain acceptance, or tau-window behavior as scientific validation.

## Review Policy

Use Claude as a read-only reviewer only for material plan/result gates. Prefer `claude_review_gate.sh` for material review. If Claude is unavailable, transport-blocked, or rejected for private-context transfer, record a Codex substitute review and proceed only if the local evidence contract remains sufficient.

Claude is advisory only. Codex remains supervisor and executor.
