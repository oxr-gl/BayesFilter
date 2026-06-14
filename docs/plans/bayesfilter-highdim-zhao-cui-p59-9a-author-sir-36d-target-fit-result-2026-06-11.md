# P59-9a Result: Author-SIR 36D Target And Bounded Fit Prep

metadata_date: 2026-06-11
status: PASS_P59_9A_AUTHOR_SIR_36D_TARGET_FIT_PREP

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can BayesFilter exercise the author Austria SIR source-route adjacent target in the correct 36D `[theta, x_t, x_{t-1}]` convention and build a bounded fixed-TT/SIRT preparation artifact? |
| Baseline/comparator | Zhao-Cui `eg3_sir/mainscript.m` and `models/full_sol.m`; P57 author SIR callback; P57/P58 source-route contracts. |
| Primary criterion | Executable evidence that the author-SIR reapproximation target has dimension `d + 2m = 36`, finite target values, and an OK bounded fixed-TT fit. |
| Veto diagnostics | 18D target, old local/operator/all-grid route, contract-double transport, nonfinite target values, or bounded fit promoted as validation evidence. |
| Explanatory diagnostics | CPU-only focused pytest, bounded rank-1/degree-0 fit, branch hashes, fixed-TTSIRT transport manifest, finite negative-log target values. |
| Not concluded | No Phase-9 validation launch, no d=18 filtering accuracy, no same-route rank convergence, no d=50/d=100 scaling, no HMC production readiness. |

## Source Anchors Checked

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:14-56`
  declares `d=0`, `m=18`, `T=20`, `N=5e3`, `sqr=1`, `tau=10`, and
  approximation basis dimension `d + 2*m`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:11-39`
  stores source-route samples in dimension `d + 2*m` and augments propagated
  current states with previous states.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:76-130`
  defines the prior/previous, transition, likelihood, shift, and TTSIRT
  reapproximation target.

## Implementation

Changed code:

- `bayesfilter/highdim/source_route.py`
  - Added P59-9a status constants.
  - Added `P59AuthorSIR36DTargetFitPrepResult`.
  - Added `p59_author_sir_36d_target_fit_prep(...)`.
  - The helper builds the author SIR model, verifies `d=0`, `m=18`,
    `d + 2m = 36`, evaluates the source sequential negative-log density at
    deterministic probes, performs a bounded rank-1/degree-0 fixed-TT fit, and
    wraps the resulting squared density in fixed-TTSIRT transport metadata.
- `bayesfilter/highdim/__init__.py`
  - Exported the P59-9a constants, result class, and helper.
- `tests/highdim/test_p59_author_sir_36d_target_fit.py`
  - Added tests for the 36D target, finite target values, fit status,
    fixed-TTSIRT transport metadata, explicit nonclaims, and fail-closed block
    behavior.

## Artifact Manifest

Key emitted values from `p59_author_sir_36d_target_fit_prep(sample_count=6)`:

| Field | Value |
| --- | --- |
| Status | `PASS_P59_9A_AUTHOR_SIR_36D_TARGET_FIT_PREP` |
| Target id | `zhao_cui_sir_austria_d18` |
| Parameter dimension | `0` |
| State dimension | `18` |
| Source target dimension | `36` |
| Source target order | `[theta, x_t, x_{t-1}]` |
| Sample count | `6` |
| Fit degree | `0` |
| Rank tuple | thirty-seven `1`s, i.e. rank-1 over 36 coordinates |
| Fit status | `OK` |
| Fit branch hash | `08b15f4ed431bc7e4e4f70032bdca1e8e6d8d52a9a60a0ba0de83e407e67f76f` |
| Density branch hash | `f1ee6307e54815bb9d30841de44d4c6c60e8f2df0e9f12a6ef06325bcd65aa28` |
| Transport family | `FixedTTSIRTTransport` |
| Transport dimension | `36` |

Finite negative-log target probe values:

```text
72.76375698476869
73.23345093419195
73.75014002690133
74.31383199489602
74.92453456902162
75.58225547896987
```

## Commands Run

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_36d_target_fit.py
```

Result: `4 passed, 2 warnings`.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_36d_target_fit.py tests/highdim/test_p58_m9_source_route_pipeline_readiness.py tests/highdim/test_p57_m1_author_sir_callback_parity.py tests/highdim/test_p57_m6_sequential_fixed_hmc_source_loop.py
```

Result: `19 passed, 2 warnings`.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -c '... p59_author_sir_36d_target_fit_prep(sample_count=6) ...'
```

Result: emitted the manifest values above.  TensorFlow printed CUDA import
warnings even with `CUDA_VISIBLE_DEVICES=-1`; this was not a GPU run and is not
used as GPU evidence.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| Working tree | Dirty before and after; P59 changes are local/uncommitted and unrelated prior artifacts remain present. |
| Python | `Python 3.11.14` |
| CPU/GPU status | CPU-only intended via `CUDA_VISIBLE_DEVICES=-1`; no GPU benchmark or GPU initialization claim. |
| Seeds | Author-SIR observation simulation seed `5901`; deterministic reference probes; fixed branch seed `p59-9a-author-sir-36d-bounded-fit`. |
| Wall time | Focused tests completed in under 10 seconds each. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9a-author-sir-36d-target-fit-subplan-2026-06-11.md` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9a-author-sir-36d-target-fit-result-2026-06-11.md` |

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass bounded P59-9a prep. | Met: 36D target, finite values, OK bounded fixed-TT fit, fixed-TTSIRT transport metadata. | No 18D target, old route, contract double, nonfinite values, or validation overclaim in tests/artifact. | This is rank-1/degree-0 preparation evidence only; it does not yet assemble a two-step source-route sequence. | Execute P59-9b: assemble bounded source-route step specs from 9a-style artifacts and previous marginal axes. | No d=18 filtering validation, no rank convergence, no paper-scale accuracy. |

## Token

`PASS_P59_9A_AUTHOR_SIR_36D_TARGET_FIT_PREP`
