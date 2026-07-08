# Phase 4 Subplan: Short HMC Smoke

Date: 2026-07-08
Status: `DRAFT_READY_FOR_REVIEW`
Master program: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md`
Phase 3 result: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase3-mechanics-canary-result-2026-07-08.md`

## Phase Objective

Run a short fixed-kernel HMC smoke on the scalar filtering-likelihood target using the repaired Phase 3 mass-preconditioned coordinate composition. The smoke extends the mechanics canary from two retained samples to a small fixed sample count, only to check finite samples, finite target trace, acceptance telemetry, and artifact integrity.

This phase is not a convergence run, posterior validation, tuning result, ranking, or default-readiness claim.

## Entry Conditions Inherited From Phase 3

- Phase 3 final artifact reports `mechanics_canary_passed: true`.
- Phase 3 uses the explicit coordinate composition `z = u @ chol(M_z).T` and `free = center + scale * z`.
- Phase 3 result records that native divergence telemetry is not exposed by the TFP kernel and must not be treated as zero divergences.
- Phase 1/2/3 artifacts are CPU-hidden debug/reference evidence, not GPU/XLA production evidence.
- Center role remains `truth_free_initial_center`, not MAP.

## Required Artifacts

- Phase 4 subplan: this file.
- Phase 4 review bundle: `docs/reviews/scalar-filtering-geometry-hmc-phase4-short-hmc-smoke-review-bundle-2026-07-08.md`
- Short-smoke script: `docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_hmc_short_smoke_2026_07_08.py`
- Focused tests: `tests/test_scalar_ssl_lstm_filtering_hmc_short_smoke.py`
- JSON artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_short_smoke_cpu_hidden_2026-07-08.json`
- Markdown artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_short_smoke_cpu_hidden_2026-07-08.md`
- Log artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_short_smoke_cpu_hidden_2026-07-08.log`
- Phase 4 result: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase4-short-hmc-smoke-result-2026-07-08.md`
- Phase 5 subplan draft only if the short smoke passes.

## Required Checks, Tests, Reviews

- Local Codex substitute review of this Phase 4 subplan because Claude review is policy-blocked for private repository context transfer.
- `python -m py_compile docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_hmc_short_smoke_2026_07_08.py`
- `pytest tests/test_scalar_ssl_lstm_filtering_hmc_short_smoke.py -q`
- CPU-hidden short-smoke command:

```bash
timeout 240 env CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_hmc_short_smoke_2026_07_08.py \
  --geometry-json docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json \
  --mass-json docs/benchmarks/scalar_ssl_lstm_filtering_mass_handoff_cpu_hidden_2026-07-08.json \
  --phase3-json docs/benchmarks/scalar_ssl_lstm_filtering_hmc_mechanics_canary_cpu_hidden_2026-07-08.json \
  --json-path docs/benchmarks/scalar_ssl_lstm_filtering_hmc_short_smoke_cpu_hidden_2026-07-08.json \
  --markdown-path docs/benchmarks/scalar_ssl_lstm_filtering_hmc_short_smoke_cpu_hidden_2026-07-08.md \
  > docs/benchmarks/scalar_ssl_lstm_filtering_hmc_short_smoke_cpu_hidden_2026-07-08.log 2>&1
```

- `git diff --check`
- Review Phase 4 result and Phase 5 subplan before any replicated scalar HMC diagnostic.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a short fixed-kernel HMC smoke produce finite retained samples and finite target/acceptance telemetry using the Phase 3 coordinate composition? |
| Baseline/comparator | Phase 3 mechanics canary artifact. No sampler ranking is attempted. |
| Primary criterion | A fixed short smoke with `L = 4`, `epsilon = 0.3925`, `num_results = 8`, and `num_burnin_steps = 2` writes a structured artifact with finite samples, finite target-log-prob trace, finite log-accept ratios, and no runtime exception. |
| Veto diagnostics | Runtime exception, timeout, missing artifact, nonfinite retained sample, nonfinite target trace, nonfinite log-accept ratio, native divergence if available and positive, coordinate/mass convention mismatch, hidden posterior/convergence/default claim. |
| Explanatory diagnostics | Acceptance rate, log-accept ratio range, target-log-prob range, sample range in `u`, runtime, and native-divergence availability status. |
| Not concluded | No posterior correctness, HMC convergence, zero divergences, tuned kernel, sampler superiority, statistical ranking, default readiness, GPU/XLA readiness, or Zhao-Cui source-faithfulness. |
| Preserving artifact | Phase 4 JSON/Markdown/log/result note and ledger entry. |

## Fixed Smoke Settings

| Setting | Value | Role |
| --- | --- | --- |
| TFP HMC coordinate | `u` with `z = u @ chol(M_z).T` | Binding coordinate convention |
| Base target coordinate | free parameter values, `free = center + scale * z` | Binding target convention |
| Kernel | fixed TFP `HamiltonianMonteCarlo`, no adaptation | Smoke-only |
| Leapfrog steps | `4` | Inherited from Phase 3 finite mechanics candidate near `L * epsilon = 1.57` |
| Step size | `0.3925` | Inherited from Phase 3 finite mechanics candidate |
| Retained samples | `8` | Short smoke only |
| Burn-in steps | `2` | Short smoke only |
| Timeout | `240` seconds | Continuation veto |

## Forbidden Claims And Actions

- Do not claim posterior correctness, HMC convergence, tuned kernel readiness, zero divergences, sampler superiority, or default readiness.
- Do not treat native divergence unavailability as zero divergences.
- Do not change Phase 1/2/3 artifacts.
- Do not change pass/fail criteria after seeing the smoke result.
- Do not install packages, fetch network resources, edit model files, or perform destructive git/filesystem actions.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 only if:

- Phase 4 subplan review has no unresolved material blocker.
- Required checks pass.
- Phase 4 artifact reports no hard vetoes.
- Retained samples and target/log-accept telemetry are finite.
- Phase 4 result preserves non-claims and labels all sampler metrics as short-smoke evidence only.
- Phase 5 replicated-scalar-HMC subplan is drafted and reviewed.

If the smoke fails, write a Phase 4 blocker/repair result and stop before replicated diagnostics.

## Stop Conditions

- Phase 4 subplan review returns unresolved `REVISE`.
- Script cannot validate coordinate/mass conventions inherited from Phase 3.
- Timeout, runtime exception, missing structured artifact, nonfinite retained samples, nonfinite target trace, or nonfinite log-accept ratio.
- Required tests fail and cannot be repaired within Phase 4 scope.
- Continuing would require package installation, network fetch, credentials, default-policy change, model-file edit, destructive git/filesystem action, or unsupported scientific/runtime claim.

## Skeptical Audit

- Wrong baseline: Phase 4 extends only the Phase 3 mechanics canary, not posterior quality.
- Proxy metric risk: acceptance and finite short-chain samples are smoke diagnostics only.
- Missing stop conditions: runtime, nonfinite, timeout, and unsupported-claim failures stop before Phase 5.
- Unfair comparison: no ranking or stochastic method comparison occurs.
- Hidden assumptions: eight retained samples cannot establish convergence or posterior correctness.
- Stale context: Phase 3 coordinate-composition repair is binding for this phase.
- Environment mismatch: CPU-hidden smoke is not GPU/XLA production evidence.
- Artifact adequacy: JSON/Markdown/log answer only short-smoke finiteness and trace integrity.

Audit result: `PASS_WITH_BOUNDARIES_PENDING_REVIEW`. Execute only after Phase 4 subplan review.
