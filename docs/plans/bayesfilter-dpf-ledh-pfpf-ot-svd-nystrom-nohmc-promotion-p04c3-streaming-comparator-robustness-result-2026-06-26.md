# P04C3 Result: Streaming Comparator Robustness Diagnostic

Date: 2026-06-26

Status: `P04C3_BLOCKED_COMPARATOR_INVALID_FOR_P04C`

## Phase Objective

Determine the smallest reviewed repair or diagnostic that can make the
range-bearing streaming comparator valid for seed `84101` on GPU, or establish
that P04C calibration cannot use the current streaming comparator on this
fixture.

## Decision Table

| Field | Result |
| --- | --- |
| Decision | `P04C3_BLOCKED_COMPARATOR_INVALID_FOR_P04C` |
| Primary criterion status | NOT MET: focused tests passed, but the exact GPU/no-TF32/no-JIT streaming canary remained a structured hard-veto artifact. |
| Veto diagnostic status | GPU canary wrote valid JSON/Markdown/log artifacts and failed with `streaming:route_exception`. |
| Main uncertainty | The explicit `MatrixInverse` failure mode was removed, but the same comparator canary now fails in the GPU eigensolver/Cholesky stabilization path. Further repair would require a new reviewed comparator-stabilization or comparator-replacement boundary. |
| Next justified action | Stop P04C calibration and draft a separate owner-reviewed comparator strategy plan before any further runtime ladder. |
| What is not concluded | No SVD-Nystrom rejection, no threshold freeze, no P04C resume, no P05 launch, no default promotion, no posterior correctness, no HMC readiness, and no statistical superiority. |

## Evidence Contract Outcome

| Field | Contract Outcome |
| --- | --- |
| Question | Answered negatively for the narrow P04C3 repair: replacing explicit posterior precision inverse with Cholesky solve did not make the seed `84101` GPU/no-TF32/no-JIT streaming comparator valid. |
| Baseline/comparator | P04C1 CPU/no-TF32/no-JIT streaming pass and repaired P04C2 GPU/no-TF32/no-JIT streaming exception on seed `84101`. |
| Primary criterion | Failed: exact GPU canary artifact was structured but not valid. |
| Veto diagnostics | Structured `streaming:route_exception` in the P04C3 GPU canary. |
| Explanatory diagnostics | Previous `MatrixInverse` exception was replaced by TensorFlow `InvalidArgumentError` at `SelfAdjointEigV2`; log also reports GPU Cholesky failure for one batch. |
| Not concluded | No method-quality ranking, no SVD-Nystrom rejection, no calibration threshold, no P04C resume, and no promotion/default/scientific/HMC claim. |
| Artifact | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c3-gpu-notf32-nojit-streaming-canary-seed84101-2026-06-26.json` |

## Plan Review

Claude read-only review:

| Round | Verdict | Outcome |
| --- | --- | --- |
| `P04C3-R1` | `VERDICT: REVISE` | Repaired over-strong inverse-to-Cholesky wording, made no-jitter/no-stabilization-policy boundary explicit, and pinned exact canary artifacts. |
| `P04C3-R2` | `VERDICT: AGREE` | Confirmed scoped wording, exact canary artifacts, and no P04C/P05/threshold/promotion leakage. |

Claude did not read source code, tests, logs, benchmark JSONs, credentials, or
unrelated paths.

## Implementation Summary

Modified:

- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
- `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`

Changes:

- Replaced explicit `tf.linalg.inv` of the stabilized posterior precision with
  `tf.linalg.cholesky_solve` against identity on the same already-stabilized
  precision path.
- Kept LEDH jitter amount, stabilization policy, fixture, thresholds, dtype,
  seed, particle count, transport policy, and SVD-Nystrom policy unchanged.
- Fixed a TensorArray chunk writer index dtype issue exposed by focused XLA
  tests: the streaming chunk block index is now kept as `int32`.
- Added a focused ill-conditioned posterior precision test for the shared LEDH
  flow core.

This implementation is not a completed comparator repair because the GPU canary
still failed.

## Required Local Checks

Command:

```bash
/home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest tests/test_experimental_batched_ledh_pfpf_ot_tf.py tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py tests/test_svd_nystrom_range_bearing_gate.py -q
```

First run:

```text
4 failed, 41 passed
```

The failures exposed a streaming TensorArray index dtype mismatch. That was
patched within the P04C3 comparator robustness scope.

Second run:

```text
45 passed, 18193 warnings in 55.74s
```

The warnings are TensorFlow/TFP/gast deprecation warnings and did not fail the
focused gate.

## Trusted GPU Canary

Trusted GPU preflight:

| GPU | Memory used | Total memory | Utilization |
| ---: | ---: | ---: | ---: |
| 0 | 1254 MiB | 32760 MiB | 16% |
| 1 | 18 MiB | 32760 MiB | 0% |

Selected GPU1 under the owner rule "GPU1 if available, otherwise GPU0".

Canary row:

| Row | Device / mode | Status | Hard vetoes | Exception |
| --- | --- | --- | --- | --- |
| `gpu-notf32-nojit-streaming-canary-seed84101` | GPU1, TF32 disabled, JIT off | `FAIL` | `streaming:route_exception` | TensorFlow `InvalidArgumentError`, `SelfAdjointEigV2`, compile-and-first stage |

The canary command used the exact predeclared P04C3 JSON/Markdown/log trio.

Artifacts:

- JSON:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c3-gpu-notf32-nojit-streaming-canary-seed84101-2026-06-26.json`
- Markdown:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c3-gpu-notf32-nojit-streaming-canary-seed84101-2026-06-26.md`
- Log:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c3-gpu-notf32-nojit-streaming-canary-seed84101.log`

Log excerpt summary:

- GPU device created successfully.
- GPU solver handles were created.
- GPU Cholesky reported an unsuccessful decomposition for batch `335`.
- TensorFlow raised `InvalidArgumentError` from `SelfAdjointEigV2` with
  `heevd` solver info `1`.

## Interpretation

P04C3 removed the original explicit `MatrixInverse` failure path but did not
make the streaming comparator deterministic-valid on the P04C failure seed.
The remaining failure is in the same broad comparator stabilization path and
would require a new reviewed plan that either changes the comparator
regularization/stabilization policy or replaces the nonlinear comparator
strategy.

P04C calibration must not resume under the current comparator. The current
evidence does not reject SVD-Nystrom: seed `84101` previously showed
SVD-Nystrom passed while the streaming comparator failed. This is a comparator
validity blocker.

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | FAIL for streaming comparator validity on seed `84101` GPU/no-TF32/no-JIT. |
| Statistically supported ranking | NO |
| Descriptive-only differences | Runtime, exception type, and solve-route changes are diagnostic only. |
| Default-readiness | NO |
| Next evidence needed | Owner-reviewed comparator strategy plan before any further P04C calibration or P05 execution. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Conda/Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13` |
| TensorFlow | `2.20.0` |
| GPU preflight | GPU1 selected: 18 MiB used, 0% utilization |
| Seeds | `84101` |
| Shape | Range-bearing fixture, `T=20`, `N=4096`, `float32` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c3-streaming-comparator-robustness-subplan-2026-06-26.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c3-streaming-comparator-robustness-result-2026-06-26.md` |

## Post-Run Red-Team Note

Strongest alternative explanation: P04C3 may have uncovered a deeper
ill-conditioning issue in the per-particle local posterior covariance rather
than merely a bad solve primitive. A future repair that changes jitter,
stabilization policy, or comparator target would need explicit review and
labeling.

Weakest part of the evidence: one GPU canary establishes that the narrow repair
does not rescue the known failure seed, but it does not map the full
distribution of comparator failures. That broader mapping should not proceed
until the comparator strategy boundary is reviewed.

## Handoff

`P04C3_BLOCKED_COMPARATOR_INVALID_FOR_P04C`

Do not resume P04C calibration, do not drop seed `84101`, do not count it as a
non-exceedance, do not launch P05, and do not freeze a threshold. The next
phase requires an owner-reviewed comparator strategy plan because further repair
would cross the P04C3 no-jitter/no-stabilization-policy-change boundary or
replace the comparator.
