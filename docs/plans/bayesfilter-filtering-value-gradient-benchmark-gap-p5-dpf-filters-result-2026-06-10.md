# P5 Result: DPF Filter Wiring And Supersession Guard

metadata_date: 2026-06-10
phase: FILTER_BENCH_P5
status: PASS_FILTER_BENCH_P5_DPF_FILTERS
supervisor: Codex
reviewer: Claude Code read-only

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can current DPF filters run through the benchmark adapter contract while old LEDH-PFPF-OT is prevented from re-entering as current evidence? |
| Baseline/comparator | P1 registry, P2 adapter schema, P3 references, current TensorFlow bootstrap PF, current Li-Coates Algorithm 1 UKF LEDH-PFPF implementation, and historical LEDH-PFPF-OT artifacts as quarantine records only. |
| Primary criterion | Met after Claude review iteration 2: current DPF coverage has a full two-algorithm by P1-target matrix, P2-shaped smoke payloads include seed/particle/MC/ESS/resampling diagnostics, and a minimal matrix preserves resampling-gradient invalidity, fixed-branch diagnostic gradients, adapter-required cells, blocked cells, and historical-only supersession. |
| Veto diagnostics | Not fired locally: old LEDH-PFPF-OT is historical-only, invalid/resampling/fixed-branch DPF gradient semantics are not hidden, one-seed smokes are not treated as exact, and missing same-target callbacks are explicit adapter-required cells. |
| Nonclaims | P5 does not rank filters, certify DPF gradients, certify statistical closeness, claim GPU/HMC/Bayesian-estimation readiness, or treat adapter-required cells as evidence against a method. |

## Artifacts

- DPF coverage manifest: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-filter-coverage-2026-06-10.json`
- DPF smoke payloads: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-filter-smoke-payloads-2026-06-10.json`
- DPF minimal matrix: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-minimal-matrix-2026-06-10.json`
- Focused validation test: `tests/highdim/test_filtering_value_gradient_benchmark_dpf_filters.py`
- Visible ledger: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-execution-ledger-2026-06-10.md`

## Coverage Summary

Current DPF algorithm ids:

- `bootstrap_dpf_current`;
- `ledh_pfpf_alg1_ukf_current`.

Historical-only algorithm id:

- `ledh_pfpf_ot_historical`.

P5 intentionally does not promote old `LEDH-PFPF-OT`, `dpf_ledh_pfpf_ot`, or
`ledh_pfpf_ot` artifacts into the current benchmark.  Those records may appear
only as historical quarantine entries.

## Validation

### Claude Review Iteration 1 Repair

Claude returned `VERDICT: REVISE` because the P5 smoke payloads flattened both
current DPF payloads to top-level `STOCHASTIC_GRADIENT_DIAGNOSTIC`, while the
coverage and matrix artifacts required route-specific preservation of
`RESAMPLING_GRADIENT_NOT_VALID` for bootstrap DPF and
`FIXED_BRANCH_GRADIENT_DIAGNOSTIC` for Algorithm 1 UKF LEDH-PFPF.  Claude also
noted that the focused tests did not assert `flow_anchor_route`.

Repair:

- extended the P2 adapter schema vocabulary to admit
  `RESAMPLING_GRADIENT_NOT_VALID` and `FIXED_BRANCH_GRADIENT_DIAGNOSTIC` as
  payload-level gradient statuses and reason codes;
- updated P5 smoke payloads so bootstrap DPF preserves
  `RESAMPLING_GRADIENT_NOT_VALID` and Algorithm 1 preserves
  `FIXED_BRANCH_GRADIENT_DIAGNOSTIC`;
- strengthened P5 focused tests to assert the route-specific smoke status
  fields and `flow_anchor_route == zero_noise_transition`;
- reran the upstream P2 adapter-schema test together with the P5 DPF tests.

Commands planned/run:

```bash
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-filter-coverage-2026-06-10.json >/dev/null
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-adapter-schema-2026-06-10.json >/dev/null
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-filter-smoke-payloads-2026-06-10.json >/dev/null
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-minimal-matrix-2026-06-10.json >/dev/null
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_adapter_schema.py tests/highdim/test_filtering_value_gradient_benchmark_dpf_filters.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_dpf_filters.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_filtering_value_gradient_benchmark_adapter_schema.py tests/highdim/test_filtering_value_gradient_benchmark_dpf_filters.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-adapter-schema-2026-06-10.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-filter-coverage-2026-06-10.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-filter-smoke-payloads-2026-06-10.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-minimal-matrix-2026-06-10.json tests/highdim/test_filtering_value_gradient_benchmark_adapter_schema.py tests/highdim/test_filtering_value_gradient_benchmark_dpf_filters.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p5-dpf-filters-result-2026-06-10.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-execution-ledger-2026-06-10.md
```

Results:

```text
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-filter-coverage-2026-06-10.json
exited 0

python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-adapter-schema-2026-06-10.json
exited 0

python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-filter-smoke-payloads-2026-06-10.json
exited 0

python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-minimal-matrix-2026-06-10.json
exited 0

CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_dpf_filters.py
6 passed in 0.11s

CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_adapter_schema.py tests/highdim/test_filtering_value_gradient_benchmark_dpf_filters.py
11 passed in 0.12s

CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_filtering_value_gradient_benchmark_adapter_schema.py tests/highdim/test_filtering_value_gradient_benchmark_dpf_filters.py
exited 0

git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-adapter-schema-2026-06-10.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-filter-coverage-2026-06-10.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-filter-smoke-payloads-2026-06-10.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-minimal-matrix-2026-06-10.json tests/highdim/test_filtering_value_gradient_benchmark_adapter_schema.py tests/highdim/test_filtering_value_gradient_benchmark_dpf_filters.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p5-dpf-filters-result-2026-06-10.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-execution-ledger-2026-06-10.md
exited 0
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | dirty worktree; P5 artifacts uncommitted |
| Environment | local Python environment |
| CPU/GPU status | CPU-only manifest validation planned with `CUDA_VISIBLE_DEVICES=-1`; no GPU conclusion |
| Random seeds | P5 smoke fixtures record seeds; no stochastic benchmark run in this gate |
| Wall time | repaired validation completed by 2026-06-11 01:39 HKT |
| Plan | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p5-dpf-filters-subplan-2026-06-10.md` |
| Result | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p5-dpf-filters-result-2026-06-10.md` |
| Coverage manifest | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-filter-coverage-2026-06-10.json` |
| Smoke payloads | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-filter-smoke-payloads-2026-06-10.json` |
| Minimal matrix | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-minimal-matrix-2026-06-10.json` |

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass after Claude review iteration 2 | Current DPF coverage, smoke payloads, and minimal matrix pass focused validation | Old OT current-evidence veto not fired; gradient status preservation is explicit | Full benchmark adapters are still required for several non-LGSSM rows before numeric P8 results can fill every cell | Advance to P6 gradient semantics | Filter ranking, DPF gradient certification, statistical closeness, HMC/GPU/Bayesian-estimation readiness |

Required token:

`PASS_FILTER_BENCH_P5_DPF_FILTERS`
