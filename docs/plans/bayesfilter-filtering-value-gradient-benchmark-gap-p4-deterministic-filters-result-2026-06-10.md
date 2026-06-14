# P4 Result: Deterministic Filter Wiring

metadata_date: 2026-06-10
phase: FILTER_BENCH_P4
status: PASS_FILTER_BENCH_P4_DETERMINISTIC_FILTERS
supervisor: Codex
reviewer: Claude Code read-only

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can deterministic filters run through the same benchmark adapter across the declared model rows? |
| Baseline/comparator | Existing Kalman, UKF/SVD/CUT4 TensorFlow APIs, highdim Zhao-Cui scalar/factorized/multistate routes, SV mixture routes, P1 registry, P2 adapter schema, and P3 reference manifest. |
| Primary criterion | Met after Claude iteration-2 agreement: every deterministic algorithm/target pair has a structured coverage cell with value/gradient status and reason codes, and every deterministic algorithm has a P2-shaped smoke payload. |
| Veto diagnostics | Not fired locally in the manifest: stale scalar-only Zhao-Cui blocker is not current admission logic; no approximate filter is marked exact; UKF scout is not truth; unsupported/adapter-required rows are explicit; blocked d=18 spatial SIR is retained. |
| Nonclaims | P4 coverage is not the final benchmark matrix, does not rank filters, does not certify DPF or deterministic gradients, and does not claim HMC/GPU/Bayesian-estimation readiness. |

## Artifacts

- Deterministic coverage manifest: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-coverage-2026-06-10.json`
- Deterministic smoke payloads: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-smoke-payloads-2026-06-10.json`
- Focused coverage test: `tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py`
- Visible ledger: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-execution-ledger-2026-06-10.md`

## Coverage Summary

The manifest covers five deterministic algorithm ids over every P1 row:

- `kalman_exact_or_mixture_enumeration`;
- `ukf`;
- `svd_sigma_point`;
- `cut4`;
- `zhao_cui_scalar_or_multistate`.

Every algorithm/row pair is one of:

- ready value/gradient;
- ready value-only;
- ready diagnostic-only;
- ready surrogate value/gradient;
- scout-only not truth;
- adapter-required with reason;
- unsupported with reason;
- blocked value route.

## Validation

Commands planned/run:

```bash
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-coverage-2026-06-10.json >/dev/null
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-smoke-payloads-2026-06-10.json >/dev/null
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-coverage-2026-06-10.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-smoke-payloads-2026-06-10.json tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p4-deterministic-filters-result-2026-06-10.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-execution-ledger-2026-06-10.md
```

Results:

```text
coverage json.tool exited 0
smoke payload json.tool exited 0
5 passed in 0.21s
compileall exited 0
git diff --check exited 0
Claude iteration 1 returned REVISE on h4 diagnostic proxy promotion, spatial SIR dim0 gradient status, and Zhao-Cui LGSSM reason code
repair validation: coverage json.tool exited 0
repair validation: smoke json.tool exited 0
repair validation: 5 passed in 0.19s
repair validation: compileall exited 0
repair validation: git diff --check exited 0
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | dirty worktree; P4 artifacts uncommitted |
| Environment | local Python environment |
| CPU/GPU status | CPU-only manifest validation with `CUDA_VISIBLE_DEVICES=-1`; no GPU conclusion |
| Random seeds | N/A, manifest/schema validation only |
| Wall time | focused pytest 0.19s after Claude iteration-1 repair |
| Plan | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p4-deterministic-filters-subplan-2026-06-10.md` |
| Result | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p4-deterministic-filters-result-2026-06-10.md` |
| Coverage manifest | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-coverage-2026-06-10.json` |
| Smoke payloads | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-smoke-payloads-2026-06-10.json` |

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass P4 | Full deterministic algorithm x target coverage matrix plus P2-shaped smoke payloads; local validation passed after iteration-1 repair and Claude iteration 2 agreed | No stale Zhao-Cui scalar-only blocker; h4 diagnostic cells are no longer benchmark-ready; SIR dim0 gradient statuses are explicit; no hidden unsupported/blocked cells | P8 still needs actual benchmark execution, and P6 must classify gradients before gradient-error interpretation | Advance to P5 DPF filter wiring and supersession guard | Filter ranking, gradient correctness, DPF correctness, HMC/GPU/Bayesian-estimation readiness |

## Claude Iteration 1 Repair

Claude returned `VERDICT: REVISE`.

Repairs applied:

- h4 nonlinear-transition diagnostic row was split out of UKF/SVD/CUT4
  ready-value-only groups and marked `READY_DIAGNOSTIC_ONLY`;
- fixed-theta spatial SIR lower-rung row was split out of UKF/SVD/CUT4 groups
  and now reports `NO_THETA_GRADIENT_DIM0`;
- Zhao-Cui LGSSM diagnostic cell now uses
  `ZHAOCUI_LGSSM_DIAGNOSTIC_NOT_ORACLE` instead of implying the Kalman
  reference gradient is unavailable;
- focused tests now lock these cases.

Required token after Claude agreement:

`PASS_FILTER_BENCH_P4_DETERMINISTIC_FILTERS`

## Claude Iteration 2

Claude returned:

```text
VERDICT: AGREE
MAJOR:
- None.
MINOR:
- None.
```

Gate status:

`PASS_FILTER_BENCH_P4_DETERMINISTIC_FILTERS`
