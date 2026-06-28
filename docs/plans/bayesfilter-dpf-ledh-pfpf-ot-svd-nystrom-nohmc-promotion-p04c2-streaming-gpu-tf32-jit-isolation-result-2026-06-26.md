# P04C2 Result: Streaming GPU TF32/JIT Isolation

Date: 2026-06-26

Status: `P04C2_BLOCKED_INVALID_DIAGNOSTIC_ARTIFACT`

## Phase Objective

Disentangle the P04C1 seed `84101` streaming comparator nonfinite diagnostic by
isolating GPU device execution, TF32, and JIT/XLA factors for the streaming
route only.

## Decision Table

| Field | Result |
| --- | --- |
| Decision | `P04C2_BLOCKED_INVALID_DIAGNOSTIC_ARTIFACT` |
| Primary criterion status | NOT MET: the first P04C2 row exited before producing the required JSON and Markdown diagnostic artifacts. |
| Veto diagnostic status | Artifact-validity veto fired: missing structured JSON/Markdown for `gpu-tf32-nojit-84101`. |
| Main uncertainty | The row shows a TensorFlow streaming-route exception on GPU/TF32/no-JIT, but the current harness cannot serialize that exception as row evidence. TF32, JIT/XLA, GPU device behavior, and interaction classification remain unresolved. |
| Next justified action | Execute P04C2A harness exception-artifact repair before rerunning P04C2 rows. |
| What is not concluded | No threshold freeze, no P04C resume, no seed exclusion, no SVD-Nystrom rejection, no promotion, no posterior-correctness claim, no HMC readiness claim, no statistical ranking, and no broad nonlinear-validity claim. |

## Evidence Contract Outcome

| Field | Contract Outcome |
| --- | --- |
| Question | Not answered. P04C2 did not produce a valid row artifact, so no isolation classification is allowed. |
| Baseline/comparator | P04C1 GPU/TF32/JIT-on seed `84101` streaming failure and P04C1 CPU/no-JIT/TF32-disabled seed `84101` streaming pass remain the active diagnostic comparators. |
| Primary criterion | Failed: exact row artifacts were required before launching subsequent rows. |
| Veto diagnostics | Missing JSON and Markdown artifacts after a nonzero process exit. |
| Explanatory diagnostics | The log contains TensorFlow `InvalidArgumentError` from `MatrixInverse` with message `Input is not invertible.` This is explanatory only until serialized by a reviewed harness repair. |
| Not concluded | No calibrated threshold, no repaired P04C panel, no seed handling decision, no P05 launch, and no promotion/default/scientific/HMC claim. |
| Artifact | This P04C2 result/close record. |

## Executed Row

| Row | Device / mode | Route | Seed | Exit | JSON | Markdown | Log |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| `gpu-tf32-nojit-84101` | GPU1, TF32 enabled, JIT off | `streaming` | 84101 | 1 | MISSING | MISSING | PRESENT |

Log artifact:
`docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c2-gpu-tf32-nojit-seed84101.log`

The remaining P04C2 rows were not run because the subplan required each row's
JSON artifact to be parsed before launching the next row.

## Error Summary

The failed row command used:

```bash
--route streaming --seed 84101 --time-steps 20 --num-particles 4096 --transport-policy active-all --dtype float32 --tf32-mode enabled --no-jit-compile --device-scope visible --cuda-visible-devices 1 --device /GPU:0
```

The process exited before `build_result` could write the JSON artifact. The log
reports TensorFlow `InvalidArgumentError` at `MatrixInverse` inside the
streaming route:

```text
Input is not invertible.
```

This is not a valid P04C2 diagnostic artifact under the current contract because
the evidence is present only as an unstructured traceback.

## Interpretation

P04C2 must stop as an artifact-validity blocker. The observed exception may be
useful for the next diagnostic, but it cannot be used to classify TF32, JIT/XLA,
GPU device behavior, or interaction status until the harness can serialize
planned route exceptions as structured evidence.

This result does not show that SVD-Nystrom failed. The only row executed was the
streaming comparator. P04C1 still shows that SVD-Nystrom passed on seed `84101`
in the both-route reproduction while the streaming comparator failed.

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | P04C2 artifact-validity hard veto fired: missing structured JSON/Markdown after route exception. |
| Statistically supported ranking | NO |
| Descriptive-only differences | The traceback is explanatory only until captured in a structured artifact. |
| Default-readiness | NO |
| Next evidence needed | P04C2A harness exception-artifact repair, focused tests, then reviewed rerun of P04C2 rows one at a time. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Conda/Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13` |
| TensorFlow | `2.20.0` |
| GPU preflight | GPU1 selected under owner rule: use GPU1 if available, otherwise GPU0 |
| Seeds | `84101` |
| Shape | Range-bearing fixture, `T=20`, `N=4096`, `float32` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2-streaming-gpu-tf32-jit-isolation-subplan-2026-06-26.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c2-streaming-gpu-tf32-jit-isolation-result-2026-06-26.md` |

## Post-Run Red-Team Note

Strongest alternative explanation: the streaming route exception may be the
same mathematical/numerical instability that previously appeared as nonfinite
route output, or it may be a separate GPU/TF32/no-JIT execution path failure.
The present artifact cannot distinguish those explanations.

Weakest part of the evidence: the only preserved diagnostic is an unstructured
log traceback. The next phase must repair the harness artifact contract before
any further runtime classification.

## Handoff

`P04C2_BLOCKED_INVALID_DIAGNOSTIC_ARTIFACT`

Draft and review P04C2A before rerunning P04C2. Do not run remaining P04C2 rows,
resume P04C calibration seeds, drop seed `84101`, count it as a non-exceedance,
launch P05, freeze a threshold, or make promotion/default/scientific/HMC claims.
