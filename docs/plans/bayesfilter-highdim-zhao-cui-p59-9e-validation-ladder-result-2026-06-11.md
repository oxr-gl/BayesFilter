# P59-9e Result: Validation Ladder

metadata_date: 2026-06-11
status: PASS_P59_9E_D18_EXECUTION_ONLY

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | After P59-9a through P59-9d pass, can the author-SIR d=18 source-route pipeline execute and preserve honest validation-tier boundaries? |
| Baseline/comparator | Zhao-Cui author SIR route selected from `eg3_sir/mainscript.m` and `models/full_sol.m`; P59-9a bounded 36D target fit; P59-9b two-step source-route step-spec assembly; P59-9c `full_route_selected`; P59-9d runner manifest. |
| Primary criterion | `d18_execution_only` returns finite execution diagnostics with P59-9a/9b/9c/9d/P58 prerequisite tokens present and blocks stronger tiers. |
| Veto diagnostics | Missing prerequisite pass; nonfinite log marginal likelihood; missing sequential carry; validation launched on old local/all-grid route; synthetic/contract-double transport used as evidence; d=50/d=100 attempted before d=18 tier gate; rank convergence, correctness, HMC, UKF, or adaptive parity overclaim. |
| Explanatory diagnostics | CPU-only focused pytest, combined P58/P59 pytest, compile check, `git diff --check`, ladder manifest payload. |
| Not concluded | No d=18 filtering accuracy, no same-route rank convergence, no d=18 correctness candidate, no d=50/d=100 scaling, no HMC production readiness, no adaptive Zhao-Cui parity, no UKF correctness comparator. |

## Source Anchors Checked

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m`
  sets `d=0`, `m=18`, `T=20`, `N=5e3`, `tau=10`, `sqr=1`, builds
  `ApproxBases(..., d + 2*m)`, and calls `full_sol(...)`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-39`
  initializes prior samples, pushes/augments `[theta, x_t, x_{t-1}]`,
  reapproximates, inverse-maps retained samples, and applies proposal
  correction.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:72-80`
  supplies the previous retained marginal at `t > 1`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:101-130`
  supplies TTIRT/TTSIRT construction and log-marginal update.

## Implementation

Changed code:

- `bayesfilter/highdim/source_route.py`
  - Added P59-9e execution-only and block status constants.
  - Added `P59AuthorSIRValidationLadderResult`.
  - Added `p59_author_sir_validation_ladder(...)`.
  - Added fail-closed blocker payloads for unsupported or stronger tiers.
- `bayesfilter/highdim/__init__.py`
  - Exported the P59-9e constants, result class, and helper.
- `tests/highdim/test_p59_author_sir_validation_ladder.py`
  - Added tests for execution-only pass, nonclaim boundaries, stronger-tier
    blockers, and incoherent pass rejection.

## Ladder Result

The only passed tier is `d18_execution_only`.

| Field | Value |
| --- | --- |
| Status | `PASS_P59_9E_D18_EXECUTION_ONLY` |
| Tier | `d18_execution_only` |
| Step count | `2` |
| Target dimension | `36` |
| State dimension | `18` |
| Parameter dimension | `0` |
| Log marginal likelihood | `-132.67807596118908` |
| Normalizer increments | `[-73.71286230209996, -58.96521365908912]` |
| Effective sample size by step | `[1.0, 1.0]` |
| Correction log-weight ranges | `[(22.03002089794578, 22.03002089794578), (23.389939795736023, 23.389939795736023)]` |
| Runner manifest | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9d-runner-readiness-manifest-2026-06-11.json` |

Blocked higher tiers:

| Tier | Status |
| --- | --- |
| `d18_same_route_rank_convergence` | `missing_higher_rank_same_route_comparator` |
| `d18_correctness_candidate` | `missing_same_target_reference_or_bridge` |
| `d50` | requires `d18_same_route_rank_convergence` first |
| `d100` | requires d50 non-veto scaling evidence first |

## Commands Run

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_validation_ladder.py
```

Result: `5 passed, 2 warnings` in about 2 minutes 46 seconds.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_validation_ladder.py tests/highdim/test_p59_author_sir_runner_manifest.py tests/highdim/test_p59_author_sir_step_spec_assembly.py tests/highdim/test_p59_author_sir_route_decision.py tests/highdim/test_p59_author_sir_36d_target_fit.py tests/highdim/test_p58_m9_source_route_pipeline_readiness.py
```

Result: `30 passed, 2 warnings` in about 10 minutes 10 seconds.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py scripts/p59_author_sir_m9_runner_manifest.py tests/highdim/test_p59_author_sir_validation_ladder.py
```

Result: passed.

```text
git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py scripts/p59_author_sir_m9_runner_manifest.py tests/highdim/test_p59_author_sir_validation_ladder.py
```

Result: passed.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -c "import json, bayesfilter.highdim as highdim; r = highdim.p59_author_sir_validation_ladder(tier='d18_execution_only', sample_count=1, fit_sample_count=2); keys = ['status','tier','step_count','target_dimension','state_dimension','parameter_dimension','log_marginal_likelihood','normalizer_increments','effective_sample_size_by_step','correction_log_weight_ranges','blocked_higher_tiers','nonclaims','runner_manifest_path']; print(json.dumps({k: r.manifest[k] for k in keys}, indent=2, sort_keys=True))"
```

Result: emitted the ladder payload summarized above.  TensorFlow printed CUDA
plugin import warnings even with `CUDA_VISIBLE_DEVICES=-1`; this was an
intentional CPU-only run and is not GPU evidence.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| Working tree | Dirty before and after; P59 changes are local/uncommitted and unrelated prior artifacts remain present. |
| Python | `Python 3.11.14` |
| CPU/GPU status | CPU-only intended via `CUDA_VISIBLE_DEVICES=-1`; no GPU benchmark or GPU initialization claim. |
| Seeds | Author-SIR observation simulation seed `5901`; deterministic bounded reference probes; fixed branch seeds from P59-9b/P59-9d. |
| Wall time | Focused P59/P58 suite completed in about 10 minutes 10 seconds. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9e-validation-ladder-subplan-2026-06-11.md` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9e-validation-ladder-result-2026-06-11.md` |
| JSON manifest | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9d-runner-readiness-manifest-2026-06-11.json` |

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass P59-9e at execution-only tier. | Met: finite d=18 source-route diagnostics with P59-9a/9b/9c/9d/P58 prerequisite tokens and explicit stronger-tier blockers. | No missing prerequisite, nonfinite value, old route, contract-double route, premature d=50/d=100, or overclaim in tests/artifact. | Tiny-sample execution is not accuracy evidence and cannot select rank. | Build the same-route higher-rank comparator before claiming rank convergence; build a same-target reference or bridge before claiming correctness. | No filtering accuracy, rank convergence, paper-scale validation, scaling, HMC readiness, adaptive parity, or UKF correctness. |

## Token

`PASS_P59_9E_D18_EXECUTION_ONLY`
