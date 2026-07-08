# Phase 5 Subplan: Replicated Scalar HMC Diagnostic

Date: 2026-07-08
Status: `DRAFT_READY_FOR_REVIEW`
Master program: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md`
Phase 4 result: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase4-short-hmc-smoke-result-2026-07-08.md`

## Phase Objective

Run a small replicated scalar HMC diagnostic to check whether the fixed Phase 4 kernel can produce finite short-chain telemetry across a few seeds. The phase records descriptive sampler diagnostics and hard vetoes, but it does not claim convergence, posterior correctness, statistical superiority, tuned-kernel readiness, or default readiness.

## Entry Conditions Inherited From Phase 4

- Phase 4 final artifact reports `short_smoke_passed: true`.
- Phase 4 fixed kernel is `L = 4`, `epsilon = 0.3925`, no adaptation.
- The repaired coordinate composition remains binding: `z = u @ chol(M_z).T`, `free = center + scale * z`.
- Native divergence telemetry is not exposed by this TFP kernel path and must not be treated as zero divergences.
- All artifacts remain CPU-hidden debug/reference evidence unless a separately reviewed plan changes the execution target.

## Required Artifacts

- Phase 5 subplan: this file.
- Phase 5 review bundle: `docs/reviews/scalar-filtering-geometry-hmc-phase5-replicated-scalar-hmc-review-bundle-2026-07-08.md`
- Diagnostic script: `docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_2026_07_08.py`
- Focused tests: `tests/test_scalar_ssl_lstm_filtering_hmc_replicated_diagnostic.py`
- JSON artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_cpu_hidden_2026-07-08.json`
- Markdown artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_cpu_hidden_2026-07-08.md`
- Log artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_cpu_hidden_2026-07-08.log`
- Phase 5 result: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase5-replicated-scalar-hmc-result-2026-07-08.md`
- Phase 6 closeout subplan draft if Phase 5 completes.

## Required Checks, Tests, Reviews

- Local Codex substitute review of this Phase 5 subplan because Claude review is policy-blocked for private repository context transfer.
- `python -m py_compile docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_2026_07_08.py`
- `pytest tests/test_scalar_ssl_lstm_filtering_hmc_replicated_diagnostic.py -q`
- CPU-hidden replicated diagnostic command:

```bash
timeout 480 env CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_2026_07_08.py \
  --geometry-json docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json \
  --mass-json docs/benchmarks/scalar_ssl_lstm_filtering_mass_handoff_cpu_hidden_2026-07-08.json \
  --phase4-json docs/benchmarks/scalar_ssl_lstm_filtering_hmc_short_smoke_cpu_hidden_2026-07-08.json \
  --json-path docs/benchmarks/scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_cpu_hidden_2026-07-08.json \
  --markdown-path docs/benchmarks/scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_cpu_hidden_2026-07-08.md \
  > docs/benchmarks/scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_cpu_hidden_2026-07-08.log 2>&1
```

- `git diff --check`
- Review Phase 5 result and Phase 6 closeout subplan before closing the master program.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Across a small fixed set of seeds, does the Phase 4 fixed kernel continue to produce finite short-chain telemetry without hard vetoes? |
| Baseline/comparator | Phase 4 short-smoke artifact. No method or kernel ranking is attempted. |
| Primary criterion | Three fixed seeds each run `num_results = 16`, `num_burnin_steps = 4`, `L = 4`, `epsilon = 0.3925`, and all rows write finite retained samples, finite target-log-prob trace, finite log-accept ratios, and no runtime exception. |
| Veto diagnostics | Runtime exception, timeout, missing artifact, nonfinite retained sample, nonfinite target trace, nonfinite log-accept ratio, native divergence if available and positive, coordinate/mass convention mismatch, unsupported posterior/convergence/default claim. |
| Explanatory diagnostics | Per-seed acceptance, log-accept range, target-log-prob range, sample range in `u`, between-seed descriptive variation, runtime, and native-divergence availability. |
| Not concluded | No posterior correctness, HMC convergence, zero divergences, tuned kernel, sampler superiority, statistical ranking, default readiness, GPU/XLA readiness, or Zhao-Cui source-faithfulness. |
| Preserving artifact | Phase 5 JSON/Markdown/log/result note and ledger entry. |

## Fixed Diagnostic Settings

| Setting | Value | Role |
| --- | --- | --- |
| TFP HMC coordinate | `u` with `z = u @ chol(M_z).T` | Binding coordinate convention |
| Base target coordinate | free parameter values, `free = center + scale * z` | Binding target convention |
| Kernel | fixed TFP `HamiltonianMonteCarlo`, no adaptation | Diagnostic-only |
| Leapfrog steps | `4` | Inherited from Phase 4 |
| Step size | `0.3925` | Inherited from Phase 4 |
| Retained samples per seed | `16` | Short replicated diagnostic |
| Burn-in steps per seed | `4` | Short replicated diagnostic |
| Seeds | `(20260708, 5501)`, `(20260708, 5502)`, `(20260708, 5503)` | Fixed replication set |
| Timeout | `480` seconds | Continuation veto |

## Statistical Evidence Discipline

- Passing Phase 5 would mean only that the fixed kernel remains viable under a small replicated finite-telemetry screen.
- Acceptance, target ranges, log-accept ranges, and sample ranges are descriptive only.
- Three short chains with 16 retained samples each are not enough to support convergence, posterior correctness, ranking, or default readiness.
- No ESS/R-hat promotion is allowed unless the implementation explicitly computes them and the result labels them as descriptive under the short-chain limit.
- Native divergence unavailability must remain distinct from zero divergences.

## Forbidden Claims And Actions

- Do not claim posterior correctness, HMC convergence, tuned kernel readiness, zero divergences, sampler superiority, statistically supported ranking, or default readiness.
- Do not treat finite short chains as convergence evidence.
- Do not treat native divergence unavailability as zero divergences.
- Do not change Phase 1/2/3/4 artifacts.
- Do not change pass/fail criteria after seeing results.
- Do not install packages, fetch network resources, edit model files, or perform destructive git/filesystem actions.

## Exact Next-Phase Handoff Conditions

Advance to Phase 6 closeout only if:

- Phase 5 subplan review has no unresolved material blocker.
- Required checks pass.
- Phase 5 artifact reports no hard vetoes.
- All retained samples and target/log-accept telemetry are finite for all fixed seeds.
- Phase 5 result preserves non-claims and includes the required inference-status table.
- Phase 6 closeout subplan is drafted and reviewed.

If Phase 5 fails, write a Phase 5 blocker/repair result and stop before closeout or dimensional lift claims.

## Stop Conditions

- Phase 5 subplan review returns unresolved `REVISE`.
- Script cannot validate coordinate/mass conventions inherited from Phase 4.
- Timeout, runtime exception, missing structured artifact, nonfinite retained samples, nonfinite target trace, or nonfinite log-accept ratio.
- Required tests fail and cannot be repaired within Phase 5 scope.
- Continuing would require package installation, network fetch, credentials, default-policy change, model-file edit, destructive git/filesystem action, or unsupported scientific/runtime claim.

## Skeptical Audit

- Wrong baseline: Phase 5 only extends Phase 4 fixed-kernel smoke across a few seeds.
- Proxy metric risk: acceptance, finite samples, and descriptive ranges are not convergence or posterior evidence.
- Missing stop conditions: runtime, nonfinite, timeout, and unsupported-claim failures stop before closeout.
- Unfair comparison: no ranking or method comparison occurs.
- Hidden assumptions: small scalar diagnostics may not transfer to longer chains, higher dimensions, Zhao-Cui routes, GPU/XLA, or real posterior validation.
- Stale context: Phase 3 coordinate-composition repair and Phase 4 smoke settings are binding.
- Environment mismatch: CPU-hidden diagnostics are not GPU/XLA production evidence.
- Artifact adequacy: JSON/Markdown/log answer only replicated finite-telemetry viability under a fixed kernel.

Audit result: `PASS_WITH_BOUNDARIES_PENDING_REVIEW`. Execute only after Phase 5 subplan review.
