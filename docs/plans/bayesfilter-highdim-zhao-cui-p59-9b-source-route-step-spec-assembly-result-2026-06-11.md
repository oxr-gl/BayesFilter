# P59-9b Result: Source-Route Step-Spec Assembly

metadata_date: 2026-06-11
status: PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can BayesFilter assemble bounded two-step author-SIR `SourceRouteSequentialStepSpec` objects after consuming P59-9a and P59-9c, while preserving the source full-route ordering and previous-marginal evidence? |
| Baseline/comparator | Zhao-Cui `eg3_sir/mainscript.m`, `models/full_sol.m`; P59-9a bounded 36D fixed-TTSIRT prep; P59-9c `full_route_selected`; P57-M5/P57-M6 source-route retained-sample and sequential-loop contracts. |
| Primary criterion | At least two consecutive 36D author-SIR source-route step specs, fixed-TTSIRT transports, frozen reference samples, previous-retained marginal evidence at time 2, and a P58-consumable manifest whose only remaining assembly blocker is the runner path. |
| Veto diagnostics | Missing P59-9c route decision, non-`full_route_selected` route, missing P59-9a pass, 18D target, contract-test transport, old all-grid/local route, missing time-2 previous marginal, or validation/performance overclaim. |
| Explanatory diagnostics | CPU-only focused pytest, bounded rank-1/degree-0 fixed-TTSIRT fits, time-2 previous-marginal axis checks, P58 partial-readiness manifest. |
| Not concluded | No Phase-9 validation launch, no d=18 filtering accuracy, no same-route rank convergence, no d=50/d=100 scaling, no HMC production readiness, no adaptive Zhao-Cui parity. |

## Source Anchors Checked

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:14-56`
  fixes the author SIR row at `d=0`, `m=18`, basis dimension `d + 2*m`, and
  launches `full_sol`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-38`
  pushes samples, augments `[theta, x_t, x_{t-1}]`, reapproximates, generates
  retained samples through `eval_irt`, and applies proposal correction.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:72-93`
  uses the prior at `t=1` and the previous marginal SIRT density for `t > 1`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:101-130`
  builds TTIRT/TTSIRT and updates the normalizer.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:132-135`
  defines the target density terms: prior/previous, transition, likelihood.

## Implementation

Changed code:

- `bayesfilter/highdim/source_route.py`
  - Added P59-9b status constants.
  - Added `P59AuthorSIRStepSpecAssemblyResult`.
  - Added `p59_author_sir_step_spec_assembly(...)`.
  - Added bounded fixed-TTSIRT construction helpers and author-SIR unit
    reference probes.
  - Extended previous-marginal evaluation so a real `FixedTTSIRTTransport`
    marginal (`SquaredTTMarginal`) can be evaluated, rather than relying only
    on the P57-M6 analytic test double.
  - Materializes a time-1 retained object before fitting the bounded time-2
    target, so the time-2 fit uses the previous retained marginal route.
- `bayesfilter/highdim/__init__.py`
  - Exported the P59-9b constants, result class, and helper.
- `tests/highdim/test_p59_author_sir_step_spec_assembly.py`
  - Added tests for two-step 36D assembly, full-route axis ordering, time-2
    previous-marginal evidence, P58 partial-readiness status, and fail-closed
    behavior when P59-9c has not passed.

## Artifact Manifest

Key emitted values from `p59_author_sir_step_spec_assembly(sample_count=1, fit_sample_count=2)`:

| Field | Value |
| --- | --- |
| Status | `PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY` |
| Step count | `2` |
| Target dimension | `36` |
| Source target order | `[theta, x_t, x_{t-1}]` |
| Route decision | `full_route_selected` |
| P59-9a status | `PASS_P59_9A_AUTHOR_SIR_36D_TARGET_FIT_PREP` |
| Previous marginal keep axes | `0..17` |
| Previous marginal input axes | `18..35` |
| Transport contract levels | `fixed_ttsirt`, `fixed_ttsirt` |
| P58 readiness after 9b | `BLOCK_P58_M9_SOURCE_ROUTE_PIPELINE_STILL_MISSING_ASSEMBLY` |
| Expected remaining P58 blocker | `missing_has_m9_runner_manifest_path` |

The P58 blocker is expected: P59-9d has not yet created the runner/manifest
path.

## Commands Run

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_step_spec_assembly.py
```

Result: `5 passed, 2 warnings` in about 3 minutes 53 seconds.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_step_spec_assembly.py tests/highdim/test_p59_author_sir_route_decision.py tests/highdim/test_p59_author_sir_36d_target_fit.py tests/highdim/test_p58_m9_source_route_pipeline_readiness.py tests/highdim/test_p57_m6_sequential_fixed_hmc_source_loop.py tests/highdim/test_p57_m5_proposal_density_retained_sampling.py
```

Result: `27 passed, 2 warnings` in about 3 minutes 59 seconds.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p59_author_sir_route_decision.py tests/highdim/test_p59_author_sir_step_spec_assembly.py
```

Result: passed.

```text
git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p59_author_sir_route_decision.py tests/highdim/test_p59_author_sir_step_spec_assembly.py docs/plans/bayesfilter-highdim-zhao-cui-p59-9c-preconditioned-route-integration-result-2026-06-11.md
```

Result: passed.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -c '... p59_author_sir_step_spec_assembly(sample_count=1, fit_sample_count=2) ...'
```

Result: emitted the manifest values above. TensorFlow printed CUDA plugin import
warnings even with `CUDA_VISIBLE_DEVICES=-1`; this was not a GPU run and is not
used as GPU evidence.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| Working tree | Dirty before and after; P59 changes are local/uncommitted and unrelated prior artifacts remain present. |
| Python | `Python 3.11.14` |
| CPU/GPU status | CPU-only intended via `CUDA_VISIBLE_DEVICES=-1`; no GPU benchmark or GPU initialization claim. |
| Seeds | Author-SIR observation simulation seed `5901`; deterministic bounded reference probes; fixed branch seeds `p59-9b-author-sir-step1-fixed-ttsirt` and `p59-9b-author-sir-step2-fixed-ttsirt`. |
| Wall time | Focused suite completed in about 4 minutes. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9b-source-route-step-spec-assembly-subplan-2026-06-11.md` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p59-9b-source-route-step-spec-assembly-result-2026-06-11.md` |

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass P59-9b bounded source-route step-spec assembly. | Met: two consecutive 36D author-SIR specs, fixed-TTSIRT transports, time-2 previous marginal present, and P58 now blocks only on missing runner path. | No route-gate miss, 18D target, contract double, old grid route, missing previous marginal, or validation overclaim in tests/artifact. | The bounded rank-1/degree-0 transports are assembly evidence only; they are not validation or rank-convergence evidence. | Execute P59-9d: create the runner and manifest path consuming P59-9a/9b/9c. | No d=18 filtering accuracy, no rank convergence, no paper-scale validation. |

## Token

`PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY`
