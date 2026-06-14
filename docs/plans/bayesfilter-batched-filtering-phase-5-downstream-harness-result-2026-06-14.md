# Phase 5 Result: Downstream HMC/NeuTra Harness

Date: 2026-06-14

## Status

`PASSED_AS_NAMED_DOWNSTREAM_VALUE_SCORE_BOUNDARY`

## Objective

Validate that the experimental batched value+score interface can be consumed at
a named existing downstream value/score boundary without production default or
public export changes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can the experimental batched value+score interface be consumed at a named existing downstream target/harness boundary while preserving HMC-style value/score shapes and explicit experimental metadata? |
| Baseline/comparator | Phase 3 interface contract, existing value+score adapter conventions, scalar fallback callback semantics, and Phase 1-3 correctness artifacts. Phase 4 timing is context only. |
| Primary criterion | Required tests pass against a named existing downstream boundary; the boundary receives `[B]` values and `[B, p]` scores; finite outputs and row order are preserved; no export/default edit occurs; HMC/NeuTra gate status is audited before any downstream claim. |
| Veto diagnostics | Shape mismatch, nonfinite output, row-order failure, implicit scalar fallback, missing experimental metadata, public export/default edit, stale/missing HMC/NeuTra gate status used as readiness evidence. |
| Not concluded | No sampler convergence, no posterior quality, no HMC/NeuTra production readiness, no default policy, no broad speedup claim. |

## Named Boundary Exercised

Existing downstream boundary:

- `bayesfilter.inference.hmc.static_unroll_chain_value_and_score`

This helper is already used by existing HMC/value-score runtime tests and is a
value/score consumer boundary without launching a sampler chain.  Phase 5
exercised it with an experimental adapter whose `log_prob_and_grad` calls
`experimental_batched_kalman_value_score` row by row through the downstream
static-unroll boundary, then compared the resulting stacked values/scores to a
direct batched reference.

## HMC/NeuTra Gate-Status Audit

Current-code-relevant local artifact checked:

- `docs/plans/nonlinear-ssm-jit-hmc-phase-6-engineering-canary-result-2026-06-08.md`

Relevant finding:

- It records a toy BayesFilter engineering canary exercising graph-native
  value/score authority, static chain-batched value/score, and a tiny
  `tfp.mcmc.sample_chain` wrapper.
- It explicitly does **not** conclude sampler convergence, posterior validity,
  real-model readiness, GPU readiness, or production robustness.

Interpretation for this phase:

- Sufficient to justify using `static_unroll_chain_value_and_score` as a named
  downstream engineering boundary.
- Insufficient to claim HMC/NeuTra production readiness or posterior validity.

## Implementation

Added:

- `tests/test_experimental_batched_downstream_value_score_harness.py`

The test covers:

- named downstream boundary consumption by
  `static_unroll_chain_value_and_score`;
- `value.shape == [B]` and `score.shape == [B, p]`;
- finite value/score tensors;
- row order preservation;
- scalar callback fallback remains explicit;
- target-scope mismatch fails closed;
- no public export/default change.

## Checks Run

### Downstream Harness Gate

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_downstream_value_score_harness.py tests/test_experimental_batched_value_score_interface.py tests/test_experimental_batched_benchmark_harness.py
```

Result:

- `16 passed`

### Experimental Correctness Guard

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_linear_kalman_tf.py tests/test_experimental_batched_svd_sigma_point_tf.py tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py
```

Result:

- `28 passed`

### Public API Guard

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_v1_public_api.py -k public_api
```

Result:

- `5 passed`

### Export Scan

```bash
rg -n "experimental_batched_value_score|experimental_batched_kalman|experimental_batched_svd" bayesfilter/__init__.py bayesfilter/linear/__init__.py bayesfilter/nonlinear/__init__.py
```

Result:

- empty output; no experimental batched public export/default entry found.

## Claude Review Trail

Phase 5 subplan review:

- `docs/plans/bayesfilter-batched-filtering-phase-5-claude-review-round-01-2026-06-14.md`
- `docs/plans/bayesfilter-batched-filtering-phase-5-claude-review-round-02-2026-06-14.md`

Round 1 required revision because a generic harness could have counted as
downstream evidence.  The subplan was patched so a pass requires a named
existing boundary.  Round 2 ended with:

- `VERDICT: AGREE`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Phase 5 passes as a named downstream value/score boundary test | `static_unroll_chain_value_and_score` consumed the experimental batched adapter; required tests passed | No shape, nonfinite, row-order, fallback, export/default, or gate-status misuse veto observed | Boundary is value/score-only and does not run HMC chains or NeuTra training | Draft Phase 6 default-readiness decision subplan | Sampler convergence, posterior quality, production default readiness |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for the named value/score boundary |
| Statistically supported ranking | Not applicable |
| Descriptive-only differences | Phase 4 timing remains contextual only |
| Default-readiness | Not established |
| Next evidence needed | Phase 6 decision table separating optional experimental path from production default |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `207419e49d2dbbc5c6aa3bca2f2ce450b6e2ffde` |
| Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python` |
| CPU/GPU status | CPU-only tests with `CUDA_VISIBLE_DEVICES=-1` |
| Data version | Synthetic deterministic fixtures |
| Random seeds | N/A |
| Plan file | `docs/plans/bayesfilter-batched-filtering-phase-5-downstream-harness-subplan-2026-06-14.md` |
| Result file | `docs/plans/bayesfilter-batched-filtering-phase-5-downstream-harness-result-2026-06-14.md` |

## Handoff To Phase 6

Phase 6 may evaluate default-readiness.  The current evidence supports an
optional experimental batched value+score path and a named value/score boundary
test.  It does not by itself justify a production default change.

