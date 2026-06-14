# P57-M6 Sequential Fixed-HMC Source Loop Result

metadata_date: 2026-06-11
status: PASS
phase: P57-M6

## Decision

`PASS_P57_M6_SEQUENTIAL_FIXED_HMC_SOURCE_LOOP`

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can BayesFilter run a replayable sequential source-route loop that carries retained objects and evaluates the previous retained marginal instead of promoting the old one-step route? |
| Baseline/comparator | Zhao-Cui author `full_sol.m:21-43` solve loop and `full_sol.m:46-130` reapprox loop, especially `full_sol.m:76-80` previous SIRT marginal prior and `full_sol.m:124` normalizer increment. |
| Primary criterion | Implemented a two-or-more-step fixed-HMC sequential runner with frozen per-step specs, retained-object carry, previous marginal-density evidence for every `t > 1`, source-route branch audit coverage, retained sample proposal correction, and log marginal likelihood as the sum of source-style normalizer increments. |
| Veto diagnostics | One-step route cannot be promoted: `source_route_run_sequential_fixed_hmc` rejects fewer than two steps, and `source_route_one_step_reapproximation` remains `t=1` only. Missing previous marginal axes or incomplete branch audit is rejected. |
| Not concluded | No TT/SIRT fitting quality, rank selection, UKF calibration, preconditioned Algorithm 5 route, HMC production readiness, or spatial SIR `d=18/d=50/d=100` success. Those remain M7-M9/M11 gates. |

## Implementation

Touched source files:

- `bayesfilter/highdim/source_route.py`
- `bayesfilter/highdim/__init__.py`

Added tests:

- `tests/highdim/test_p57_m6_sequential_fixed_hmc_source_loop.py`

Key implementation points:

- `SourceRouteSequentialStepSpec` freezes the target, transport, reference samples, measure convention, and previous-marginal axes.
- `SourceRouteSequentialDensityComponents` records the source physical target
  components: prior or previous retained marginal, transition density, and
  likelihood density.
- `SourceRouteSequentialStepResult` records the retained object, previous retained object, and previous marginal-density diagnostic.
- `SourceRouteSequentialResult` requires at least two consecutive steps and a passing `SourceRouteImplementationAudit`.
- `source_route_previous_marginal_log_density(...)` mirrors the author prior term: marginalize the previous retained SIRT to the `[theta, x_{t-1}]` prefix, invert the previous affine frame prefix, evaluate `eval_pdf`, and subtract the prefix log determinant.
- `source_route_sequential_negative_log_physical_density(...)` provides an author-style physical negative-log target with prior/previous, transition, and likelihood terms.
- `source_route_run_sequential_fixed_hmc(...)` carries the retained object
  forward, builds each per-step target from the source density components and
  the actual carried previous retained object, and rejects missing previous
  marginalization evidence.

## Source Anchors

| Source claim | Anchor |
| --- | --- |
| Sequential loop pushes samples, reapproximates, samples from current SIRT, and records ESS/weights. | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-43` |
| Previous retained-object prior uses previous SIRT marginal and previous affine `L/mu`. | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:76-80` |
| New SIRT target is prior/previous plus transition plus likelihood after affine shift. | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:92-130` |
| Log marginal likelihood increment is `log(sirt.z) - const`. | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:124` |

## Checks

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p57_m6_sequential_fixed_hmc_source_loop.py \
  tests/highdim/test_p57_m5_proposal_density_retained_sampling.py \
  tests/highdim/test_p55_source_route_one_step.py \
  tests/highdim/test_p49_source_route_retained_object.py
```

Result: `22 passed, 2 warnings`.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p57_m6_sequential_fixed_hmc_source_loop.py
```

Result: passed.

```text
git diff --check -- \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p57_m6_sequential_fixed_hmc_source_loop.py
```

Result: passed.

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass M6 and move to M7 after Claude review. | Met. The sequential runner carries previous retained objects and records previous marginal-density evidence for `t > 1`. | No veto triggered in focused checks. One-step promotion and missing previous marginalization are rejected. | This is a fixed-HMC source-loop skeleton over supplied/frozen transports, not a production TT fitting or rank policy. | M7 should address source-faithful rank/UKF calibration. | Spatial SIR high-dimensional success and HMC production readiness. |

## Nonclaims

- This does not certify adaptive TT-cross parity.
- This does not certify S&P 500 reproduction.
- This does not implement smoothing.
- This does not choose ranks or memory budgets.
- This does not validate paper-scale spatial SIR.
