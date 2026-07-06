# P01A LGSSM Exact-Kalman Harness Implementation Result

Date: 2026-06-24

Status: `PASS_P01A_IMPLEMENTATION_READY_FOR_P01B_APPROVAL`

## Phase Summary

P01A implemented the missing LGSSM exact-Kalman gate harness and focused test
pair required by the refreshed P01 subplan. The implementation creates
deterministic TensorFlow/TFP LGSSM fixtures, computes exact Kalman references,
runs the existing streaming LEDH flow and low-rank coupling solver route, and
emits JSON/Markdown diagnostics for filtered mean RMSE, filtered variance RMSE,
log-likelihood absolute delta, route-fired evidence, nonmaterialization
evidence, and low-rank factor diagnostics.

The focused local checks passed. This result certifies that the P01A harness is
implemented and locally checkable. It does not certify LGSSM quality, GPU/TF32
runtime, model-suite recommendation, statistical superiority, posterior
correctness, HMC readiness, package/API readiness, or package/public default
readiness.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | P01A implementation passes local checks and is ready for explicit P01B trusted-GPU approval decision. |
| Primary criterion status | `PASS`: named harness and test exist; compile passed; focused pytest passed; active route implementation uses TensorFlow/TFP route components; reporting conversions are outside the TensorFlow route core. |
| Veto diagnostic status | No P01A implementation veto remains active. P01B runtime remains unapproved and unrun. |
| Main uncertainty | The tiny CPU-hidden smoke proves command shape and artifact contract only; it does not answer the P01 LGSSM quality gate. |
| Next justified action | Ask for explicit approval to run P01B trusted-GPU LGSSM exact-Kalman benchmark using the pinned P01 cases, seeds, and tolerances. |
| What is not being concluded | No LGSSM pass, model-suite recommendation, statistical ranking, posterior correctness, dense equivalence, HMC readiness, public API readiness, package default readiness, or scientific validity. |

## Implemented Artifacts

| Artifact | Status |
| --- | --- |
| Harness | Present: `docs/benchmarks/benchmark_low_rank_ledh_lgssm_kalman_gate.py` |
| Focused test | Present: `tests/test_low_rank_ledh_lgssm_kalman_gate.py` |
| P01A result | This file |
| P01 subplan | Refreshed and review-converged: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p01-lgssm-kalman-subplan-2026-06-24.md` |

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | Is the P01 LGSSM exact-Kalman harness implemented and locally checkable before trusted GPU runtime? |
| Baseline/comparator | P00 harness-missing audit and refreshed P01 implementation-before-runtime subplan. |
| Primary pass criterion | New harness/test exists and passes focused local checks without active-path NumPy or boundary drift. |
| Result | `PASS`. |
| Veto diagnostics | No compile failure, no focused pytest failure, no missing pinned case contract, no active-path NumPy implementation, no unapproved GPU/HMC/default/API/science boundary crossed. |
| Artifact | Harness, focused test, this result, execution ledger. |

## Local Checks

Commands run:

```bash
python -m py_compile docs/benchmarks/benchmark_low_rank_ledh_lgssm_kalman_gate.py tests/test_low_rank_ledh_lgssm_kalman_gate.py
```

Result: pass.

```bash
python -m pytest tests/test_low_rank_ledh_lgssm_kalman_gate.py -q
```

Initial result: fail, `1 failed, 2 passed`. The failure was a reporting-only
JSON serialization issue after tensors were materialized for artifact writing.
Repair: extend `_json_ready` to handle objects with `tolist()` before JSON
encoding.

Rerun result: pass, `3 passed`.

```bash
rg -n "import numpy|np\\.|\\.numpy\\(|numpy" docs/benchmarks/benchmark_low_rank_ledh_lgssm_kalman_gate.py tests/test_low_rank_ledh_lgssm_kalman_gate.py experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py
```

Result: no NumPy imports or `np.` references in the new harness/test. `.numpy()`
hits in the new harness are reporting/materialization helpers after TensorFlow
route execution:

- route timing materialization;
- scalar and boolean extraction for JSON/Markdown artifacts;
- preview/report serialization.

These are outside the compiled route core and are not used as differentiable or
gradient-bearing algorithmic implementation.

## Harness Contract

The harness records:

- pinned P01 case IDs, dimensions, seeds, particle counts, and tolerances;
- deterministic TensorFlow/TFP LGSSM fixture generation;
- exact Kalman filtered means, variances, and log likelihood;
- low-rank route-fired count and active resampling count;
- transport matrix sentinel shape `[1, 0, 0]` for nonmaterialization;
- low-rank factor residual, induced row/column residuals, factor finiteness,
  particle finiteness, nonnegative factors, positive `g`, and projection
  iterations;
- run manifest with command, git commit, dirty worktree text, TensorFlow/TFP
  versions, device scope, CUDA visibility, dtype, TF32 setting, and plan paths;
- nonclaims.

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for P01A implementation/local checks. |
| Statistically supported ranking | None. |
| Descriptive-only differences | Tiny CPU-hidden smoke outputs are command-shape/debug diagnostics only. |
| Default-readiness | Not evaluated. |
| Next evidence needed | Explicitly approved P01B trusted-GPU runtime over pinned LGSSM cases/seeds/tolerances. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4`; working tree is dirty with unrelated existing changes. |
| Commands | `py_compile`; focused `pytest`; active-path NumPy/reporting audit. |
| Environment | Local repository environment, `/home/ubuntu/python/BayesFilter`. |
| CPU/GPU status | Focused test used CPU-hidden debug path (`CUDA_VISIBLE_DEVICES=-1`); no GPU runtime claim. |
| Data version | Deterministic synthetic LGSSM fixtures generated by the new harness. |
| Random seeds | Focused test seed `91001`; P01B pinned seeds remain as declared in the P01 subplan. |
| Wall time | N/A. |
| Output artifact paths | This result; harness; focused test. |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p01-lgssm-kalman-subplan-2026-06-24.md` |
| Result file | This file. |

## Post-Run Red-Team Note

The strongest alternative explanation is that P01A only shows the harness can
execute a tiny CPU-hidden debug case and write artifacts. It does not show that
the locked low-rank route satisfies the pinned LGSSM tolerances under trusted
GPU/TF32/XLA execution. That remains the P01B gate.

## Handoff

P01B may be requested only after explicit human approval for trusted GPU
runtime. If approval is not granted or trusted GPU runtime is unavailable, P01
must write a blocker result and stop at P01; any P02 refresh in that path must
be labeled `P02_DRAFT_NO_EXECUTION_AUTHORIZED`.
