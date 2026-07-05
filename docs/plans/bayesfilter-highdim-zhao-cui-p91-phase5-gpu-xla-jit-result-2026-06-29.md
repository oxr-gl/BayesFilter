# P91 Phase 5 Result: GPU/XLA JIT Capability

Date: 2026-06-29

Status: `PASS_P91_PHASE5_GPU_XLA_JIT_LOCAL_COMPLETE_DATA`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 5 added narrow TensorFlow local complete-data Zhao-Cui SIR d18 value helpers, verified the associated autodiff score path against the existing eager local scalar/score, and passed trusted GPU/XLA single and batched compile/run checks. |
| Primary criterion status | Passed: single and batched local complete-data value/score functions compiled with `jit_compile=True`, executed on `/GPU:0`, returned finite outputs/scores on GPU devices, and had stable post-warmup tracing counts. |
| Veto diagnostic status | Passed: trusted GPU evidence was used; TensorFlow saw `/physical_device:GPU:0`; no CPU output-device fallback was detected for compiled outputs; no NaN/Inf, OOM, compile failure, or post-warmup retracing was recorded. |
| Main uncertainty | This is a local complete-data GPU/XLA capability gate. It does not establish full observed-data/filtering score identity, previous-marginal/fixed-TTSIRT derivative readiness, GPU speed superiority, HMC posterior validity, or production readiness. |
| Next justified action | Review this Phase 5 result and the refreshed Phase 6 CPU/GPU/batched benchmark subplan. |
| What is not being concluded | No full observed-data/filtering score identity, no previous-marginal derivative readiness, no fixed TTSIRT proposal/transport derivative readiness, no GPU speed superiority, no benchmark pass, no HMC posterior validity, no packaging/default readiness, and no production readiness. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the HMC-relevant local complete-data Zhao-Cui SIR d18 target component compile and run with its autodiff score path on GPU/XLA in trusted context, without claiming HMC readiness for a full target? |
| Baseline/comparator | Phase 2 single/batched API semantics, Phase 4 local complete-data score identity setup, and CPU parity between the new helper and existing eager local complete-data value plus tape-derived parameter score. |
| Primary criterion | Passed for the deterministic local complete-data fixture. |
| Veto diagnostics | Passed for trusted device visibility, output device placement, finite outputs/scores, post-warmup retracing count, compile success, and no recorded runtime errors. |
| Explanatory diagnostics | First-call/second-call/steady timings, output devices, tracing counts, TensorFlow/CUDA build info, and `nvidia-smi` output. Timings are explanatory only. |
| Not concluded | No full filtering score identity, speed superiority, benchmark pass, HMC readiness, package/release/CI readiness, default-policy authorization/change, or production readiness. |
| Artifact | Phase 5 manifest, this result, and refreshed Phase 6 subplan. |

## Local Checks

Commands:

```bash
git diff --check -- bayesfilter/highdim/models.py bayesfilter/highdim/__init__.py scripts/p91_gpu_xla_jit_check.py tests/highdim/test_p91_gpu_xla_local_target.py docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
CUDA_VISIBLE_DEVICES=-1 python -m py_compile scripts/p91_gpu_xla_jit_check.py
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p81_analytical_sir_score.py::test_parameterized_sir_log_density_parameter_scores_match_diagnostic_tape tests/highdim/test_p91_score_identity.py tests/highdim/test_p91_gpu_xla_local_target.py -q
```

Outcome:

- `git diff --check`: passed.
- Harness compile check: passed.
- Focused CPU-only pytest: `4 passed, 2 warnings in 16.83s`.
- Warnings were TensorFlow Probability `distutils` deprecation warnings from
  environment imports; they were not Phase 5 harness failures.
- CPU-only pytest intentionally set `CUDA_VISIBLE_DEVICES=-1`.

## Trusted GPU/XLA Checks

Commands:

```bash
nvidia-smi
python scripts/p91_gpu_xla_jit_check.py --manifest docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-manifest-2026-06-29.json
```

`nvidia-smi` outcome:

- Trusted command passed.
- Driver `591.86`, CUDA `13.1` reported by `nvidia-smi`.
- GPU reported as NVIDIA GeForce RTX 4080-class device with 16376 MiB memory.

TensorFlow/XLA harness outcome:

- Trusted command passed with status
  `PASS_P91_PHASE5_GPU_XLA_JIT_LOCAL_COMPLETE_DATA`.
- TensorFlow version `2.19.1`.
- TensorFlow build CUDA version `12.4`.
- TensorFlow saw physical GPU `/physical_device:GPU:0` and logical GPU
  `/device:GPU:0`.
- GPU name: NVIDIA GeForce RTX 4080 SUPER.
- TensorFlow logs recorded XLA CUDA service initialization and one compiled
  XLA cluster.

## Manifest Summary

Manifest:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-manifest-2026-06-29.json`

Manifest status:

```text
PASS_P91_PHASE5_GPU_XLA_JIT_LOCAL_COMPLETE_DATA
```

| Check | Pass | Output devices | Trace counts | First call seconds | Second call seconds | Repeated call seconds |
| --- | --- | --- | --- | --- | --- | --- |
| single_local_complete_data | true | GPU:0 value and score | `0 -> 1 -> 1` | `1.7764` | `0.0016` | `0.0008` |
| batched_local_complete_data | true | GPU:0 values and scores | `0 -> 1 -> 1` | `5.7253` | `0.0009` | `0.0041` |

Representative outputs:

- Single value: `-227.76731057912758`.
- Single score: `[15.804320716438662, 0.6904322032950851, -44.9925]`.
- Batched values: `[-227.7673105791276, -227.77357993782164, -227.7833583105829, -227.79664568445125]`.
- Batched scores were finite for all four rows and are recorded in the
  manifest.

## Implementation Artifacts

Changed/added artifacts:

- `bayesfilter/highdim/models.py`: added XLA-oriented local complete-data SIR
  d18 value helpers.
- `bayesfilter/highdim/__init__.py`: exported the helper through the
  highdim subpackage only.
- `tests/highdim/test_p91_gpu_xla_local_target.py`: CPU parity checks against
  the existing eager local complete-data scalar/score and batched-vs-looped
  helper values.
- `scripts/p91_gpu_xla_jit_check.py`: trusted GPU/XLA manifest-writing
  harness.

The helper intentionally does not make the Python score API packaging,
dataclass manifests, or branch metadata layer part of the XLA-compiled target.

## Blockers Preserved

The manifest preserves:

- `full_observed_data_filtering_score_identity = NOT_CLAIMED`;
- `BLOCK_FIXED_TTSIRT_PREVIOUS_MARGINAL_DERIVATIVE_NOT_IMPLEMENTED`;
- `BLOCK_FIXED_TTSIRT_PROPOSAL_TRANSPORT_DERIVATIVE_NOT_IMPLEMENTED`;
- `BLOCK_FULL_SOURCE_ROUTE_FD_NOT_CLAIMED`.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `c815edc52162779e969b2982723b2f52770fd849` |
| Worktree status | Dirty research worktree; unrelated dirty changes preserved. |
| Python executable | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python` |
| Conda environment | `tf-gpu` |
| Execution target | Trusted GPU/XLA local complete-data value/score capability; CPU-only parity checks before runtime. |
| CPU/GPU status | CPU parity tests intentionally hid GPU; GPU/XLA harness used trusted/escalated execution. |
| Commands | `git diff --check -- bayesfilter/highdim/models.py bayesfilter/highdim/__init__.py scripts/p91_gpu_xla_jit_check.py tests/highdim/test_p91_gpu_xla_local_target.py docs/plans/bayesfilter-highdim-zhao-cui-p91*.md`; `CUDA_VISIBLE_DEVICES=-1 python -m py_compile scripts/p91_gpu_xla_jit_check.py`; `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p81_analytical_sir_score.py::test_parameterized_sir_log_density_parameter_scores_match_diagnostic_tape tests/highdim/test_p91_score_identity.py tests/highdim/test_p91_gpu_xla_local_target.py -q`; `nvidia-smi`; `python scripts/p91_gpu_xla_jit_check.py --manifest docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-manifest-2026-06-29.json` |
| Data version | `N/A`; deterministic local complete-data fixture. |
| Random seeds | `N/A`; deterministic fixture. |
| Wall time | CPU pytest reported `16.83s`; the shell-reported XLA harness elapsed time was approximately `16.00s` from the tool wrapper; `nvidia-smi` completed with exit code 0. |
| Phase 5 subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-subplan-2026-06-29.md` |
| Manifest | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-manifest-2026-06-29.json` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-result-2026-06-29.md` |
| Refreshed Phase 6 subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-subplan-2026-06-29.md` |

## Phase 6 Handoff

Phase 6 may proceed only after Claude review agrees on this Phase 5 result and
the refreshed Phase 6 benchmark subplan. Phase 6 must preserve that Phase 5 is
only a local complete-data GPU/XLA capability pass and not a speed, HMC,
posterior, full filtering-score, release, default-policy, or production pass.
