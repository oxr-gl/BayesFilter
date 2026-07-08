# Phase 3 Review Bundle: Minimal SSL-LSTM Zhao-Cui HMC Validity

Date: 2026-07-06

Review status: `PENDING`

## Scope

Read-only review of the exact Phase 3 longer-HMC diagnostic plan and harness.
Do not edit files. Do not authorize runtime, product, source-faithful,
scientific-claim, default-policy, package, network, or destructive boundaries.

## Artifacts To Inspect

- Subplan:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase3-longer-hmc-diagnostics-subplan-2026-07-06.md`
- Harness:
  `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_validity_phase3_2026_07_06.py`
- Tests:
  `tests/test_minimal_ssl_lstm_zhaocui_hmc_validity_phase3.py`
- Phase 2 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase2-oracle-implementation-result-2026-07-06.md`

## Evidence Contract To Review

Question: Does a modest longer trusted GPU/XLA fixed-kernel HMC run on the
minimal target produce valid artifacts, finite samples, sampled-state
target/reference agreement, and minimal R-hat/ESS convergence-screen evidence?

Baseline/comparator: Phase 2 conditional-slice/sampled-value oracle machinery
plus the completed `hmc-next` Phase 5 GPU/XLA hard-veto mechanics artifact.

Primary artifact criterion: the exact command runs or cleanly records a
preflight blocker, writes valid JSON/Markdown/log artifacts, and preserves all
diagnostic roles and nonclaims.

Promotion criterion: no hard runtime vetoes, sampled-state target/reference
checks pass, split R-hat is finite for all 24 coordinates with max `<= 1.2`,
cross-chain ESS is finite for all 24 coordinates with min `>= 16.0`, and
required provenance is present.

Continuation vetoes: runtime exception preventing diagnostics, nonfinite
samples or target values, invalid JSON/artifact schema, missing required
diagnostics, corrupted Phase 2 comparator, GPU/XLA provenance failure for the
trusted run, or unsupported claim.

Not concluded: full posterior correctness, broad HMC convergence, dimensional
generality, source-faithful Zhao-Cui parity, ranking/superiority, default
readiness, production readiness, public API/package readiness, or LEDH evidence.

## Exact Runtime Command Under Review

```bash
CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_validity_phase3_2026_07_06.py --trusted-gpu-xla-approval --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase3_longer_gpu_xla_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase3_longer_gpu_xla_2026-07-06.md
```

Stdout/stderr will be captured to:

`docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_validity_gaps_2026-07-06/phase3_longer_gpu_xla_2026-07-06.log`

## Local Checks Already Run

- `python -m py_compile docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_validity_phase3_2026_07_06.py tests/test_minimal_ssl_lstm_zhaocui_hmc_validity_phase3.py`: passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest -q tests/test_minimal_ssl_lstm_zhaocui_hmc_validity_phase3.py`: passed, `9 passed`.

## Review Questions

1. Does the subplan state exact runtime settings, artifacts, evidence roles,
   forbidden claims/actions, handoff conditions, and stop conditions?
2. Does the harness separate artifact validity, promotion vetoes, and
   continuation vetoes without silently promoting proxy metrics?
3. Are R-hat/ESS/reference checks scoped as minimal-target diagnostics rather
   than full posterior or broad HMC-convergence proof?
4. Does the plan avoid source-faithful Zhao-Cui claims and preserve the Phase 2
   conditional-slice limitation?
5. Is there any blocker that must be fixed before launching the exact command?

Return one of:

- `VERDICT: AGREE` with residual risks; or
- `VERDICT: REVISE` with blocking findings and file/line references.
