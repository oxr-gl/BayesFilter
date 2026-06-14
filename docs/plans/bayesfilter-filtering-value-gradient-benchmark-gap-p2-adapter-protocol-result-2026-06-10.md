# P2 Result: Unified Filter Adapter Protocol

metadata_date: 2026-06-10
phase: FILTER_BENCH_P2
status: PASS_FILTER_BENCH_P2_ADAPTER_PROTOCOL
supervisor: Codex
reviewer: Claude Code read-only

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can every filter expose value, gradient, diagnostics, runtime, and status through one benchmark interface? |
| Baseline/comparator | Current BayesFilter highdim/nonlinear interfaces, experimental DPF runners, and the P1 target registry rows. |
| Primary criterion | Met after Claude review: a durable adapter schema exists and exercised fixture payloads cover Kalman/mixture, deterministic sigma-point, Zhao-Cui TT, current particle filters, blocked-only rows, historical-only rows, valid gradients, unavailable gradients, stochastic/invalid/disconnected gradients, and no-theta blocked status. |
| Veto diagnostics | Not fired locally: one top-level payload shape is used for all families; every payload has row id, value status, gradient status, reason codes, diagnostics, and nonclaims; historical `LEDH-PFPF-OT` is represented only as historical-only; current DPF identity is restricted to bootstrap DPF or source-faithful Algorithm 1 UKF LEDH-PFPF. |
| Nonclaims | No filter accuracy result, no benchmark ranking, no DPF gradient certification, no public API promotion for experimental DPF code, no HMC/GPU/Bayesian-estimation readiness. |

## Artifacts

- Adapter schema: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-adapter-schema-2026-06-10.json`
- Exercised fixture payloads: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-adapter-fixtures-2026-06-10.json`
- Focused schema test: `tests/highdim/test_filtering_value_gradient_benchmark_adapter_schema.py`
- Visible ledger: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-execution-ledger-2026-06-10.md`

## Adapter Contract

The adapter payload top level is stable across families.  It carries:

- algorithm and target identity;
- registry row id, model id, dimension, horizon, theta id, theta dimension, and observation id;
- scalar value and value status;
- gradient vector and gradient status;
- reference type and evidence role;
- reason codes, diagnostics, runtime, seed, artifact path, and nonclaims.

The diagnostics object is the only algorithm-specific extension point.  This
keeps deterministic filters, Zhao-Cui TT routes, current DPF routes,
blocked-only rows, and historical-only rows on one reporting surface.

## Exercised Payload Coverage

The fixture artifact exercises:

| Family | Representative payload | Status coverage |
| --- | --- | --- |
| `kalman_or_mixture` | `kalman_exact` on LGSSM dim 1 | valid value and valid gradient |
| `deterministic_sigma_point` | `cut4` on P44 quadratic dim 2 | valid value and `GRADIENT_NOT_EXPOSED` |
| `zhao_cui_tt` | `zhao_cui_tt` on transformed SV dim 3 | valid value and valid gradient representation |
| `particle_filter_current` | `bootstrap_dpf_current` on P44 cubic dim 3 | valid value and `STOCHASTIC_GRADIENT_DIAGNOSTIC` |
| `particle_filter_current` | `ledh_pfpf_alg1_ukf_current` on P44 nonlinear/native SV rows | valid value with `INVALID_GRADIENT_NONFINITE` and `DISCONNECTED_GRADIENT` statuses |
| `blocked_only` | d=18 spatial SIR route | `BLOCKED_VALUE_ROUTE` with `BLOCK_P53_M5_RANK_SELECTION_INTEGRATION` |
| `historical_only` | `ledh_pfpf_ot_historical` | `HISTORICAL_ONLY_NOT_EVIDENCE` with supersession reason code |

## Validation

Commands run:

```bash
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-adapter-schema-2026-06-10.json >/dev/null
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-adapter-fixtures-2026-06-10.json >/dev/null
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_adapter_schema.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_filtering_value_gradient_benchmark_adapter_schema.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-adapter-schema-2026-06-10.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-adapter-fixtures-2026-06-10.json tests/highdim/test_filtering_value_gradient_benchmark_adapter_schema.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p2-adapter-protocol-result-2026-06-10.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-execution-ledger-2026-06-10.md
```

Results:

```text
schema json.tool exited 0
fixture json.tool exited 0
5 passed in 0.07s
compileall exited 0
git diff --check exited 0
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | dirty worktree; P2 artifacts uncommitted |
| Environment | local Python environment |
| CPU/GPU status | CPU-only schema validation with `CUDA_VISIBLE_DEVICES=-1`; no GPU conclusion |
| Random seeds | Fixture metadata only: 20260610, 20260611, 20260612 where particle payloads require a seed |
| Wall time | focused pytest 0.07s |
| Plan | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p2-adapter-protocol-subplan-2026-06-10.md` |
| Result | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p2-adapter-protocol-result-2026-06-10.md` |
| Schema | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-adapter-schema-2026-06-10.json` |
| Fixtures | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-adapter-fixtures-2026-06-10.json` |

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass P2 | Uniform schema and fixture payloads cover all required families/statuses; local validation passed; Claude returned `VERDICT: AGREE` | No old LEDH-PFPF-OT current evidence; no per-family top-level JSON special case; no hidden invalid-gradient hole | Some declared vocabulary paths are not implementation-validated until later phases | Advance to P3 reference-oracle wiring | Filter accuracy, benchmark ranking, DPF gradient correctness, HMC/GPU/Bayesian-estimation readiness |

## Claude Read-Only Review

Claude iteration 1 returned:

```text
VERDICT: AGREE
```

Minor caution recorded for downstream phases:

- `NO_THETA_GRADIENT_DIM0`, `NOT_RUN`, `UNSUPPORTED_BY_TARGET`, and value-side
  failure statuses are schema vocabulary, not yet validated implementation
  paths.
- The blocked-only row's `diagnostics.current_evidence` means current evidence
  of the blocker, not current benchmark-performance evidence; consumers must
  use `evidence_role` and status fields as authoritative.

Required token:

`PASS_FILTER_BENCH_P2_ADAPTER_PROTOCOL`
