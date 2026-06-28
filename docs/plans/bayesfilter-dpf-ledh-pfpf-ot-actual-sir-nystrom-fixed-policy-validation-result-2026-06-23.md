# Actual-SIR Nystrom Fixed-Policy Validation Result

Date: 2026-06-23

Status: `FIXED_POLICY_P01_PASS_RECOMMEND_SEPARATE_STRESS_RUNBOOK`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Keep `rank=32,epsilon=0.5`, raw kernel, scaling normalization `none` as a viable restricted fixed-policy candidate | `PASS`: aggregate artifact status `PASS`, finite GPU outputs, residuals within threshold, paired deltas within thresholds, fixed-policy metadata present | `PASS`: no hard vetoes, no missing GPU/TF32 evidence, no selected-policy metadata drift | This is one serious confirmation row; nearby policy settings remain brittle from prior evidence | Create a separate fixed-policy stress/replication runbook before any default or promotion claim | No default readiness, no broad rank/epsilon robustness, no statistical ranking, no superiority, no posterior correctness, no HMC readiness |

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | Is the restricted fixed policy still viable on the serious actual-SIR comparator row with current code? |
| Baseline/comparator | Compiled streaming TF32 actual-SIR route in the same artifact. |
| Primary pass/fail criterion | `PASS`: aggregate artifact `status == PASS`. |
| Veto diagnostics | `PASS`: no aggregate hard vetoes, GPU/TF32 evidence present, fixed-policy metadata present, finite outputs, residuals and paired thresholds pass. |
| Explanatory only | Runtime, warm timing ratio, factor/scaling ranges, denominator floor hits, spectrum diagnostics. |
| Not concluded | No default readiness, no superiority/ranking, no broad rank/epsilon robustness, no posterior correctness, no HMC readiness. |
| Artifact preserving result | P01 JSON/Markdown/log and this result note. |

## Command And Artifacts

Trusted GPU preflight selected physical GPU1:

```text
0, NVIDIA GeForce RTX 4080 SUPER, 1525 MiB used / 32760 MiB, 26% utilization
1, NVIDIA GeForce RTX 4080 SUPER, 18 MiB used / 32760 MiB, 0% utilization
```

Artifacts:

- Plan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-validation-plan-2026-06-23.md`
- JSON: `docs/benchmarks/actual-sir-nystrom-fixed-policy-p01-r32-eps0p5-2026-06-23.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-fixed-policy-p01-r32-eps0p5-2026-06-23.md`
- Log: `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-p01-r32-eps0p5-2026-06-23.log`

## Result Summary

Aggregate status: `PASS`.

Aggregate hard vetoes: `[]`.

Selected policy metadata:

- `nystrom_rank`: `32`;
- `nystrom_epsilon`: `0.5`;
- `nystrom_kernel_mode`: `raw`;
- `nystrom_scaling_normalization`: `none`;
- `nystrom_diagnostics_enabled`: `true`.

Streaming comparator:

- status: `PASS`;
- log likelihoods:
  `[-902.23779296875, -901.313720703125, -901.726806640625, -902.2744140625, -900.0975952148438]`.

Nystrom fixed-policy candidate:

- status: `PASS`;
- log likelihoods:
  `[-903.1004028320312, -902.972412109375, -903.3366088867188, -898.5984497070312, -896.8526000976562]`;
- `finite_factors`: `True`;
- `finite_particles`: `True`;
- `max_row_residual`: `9.500980377197266e-05`;
- `max_column_residual`: `1.9073486328125e-06`;
- `min_kernel_denominator`: `0.1508975327014923`;
- `denominator_floor_hits`: `0.0`;
- `max_abs_log_scaling_gauge_shift`: `0.0`;
- `scaling_normalization_applications`: `0.0`;
- `scaling_u_min..max`: `0.0026294889394193888 .. 0.03608550876379013`;
- `scaling_v_min..max`: `0.08321866393089294 .. 12.063054084777832`;
- `landmark_core_effective_rank_min`: `32.0`.

Paired comparability:

- deltas:
  `[-0.86260986328125, -1.65869140625, -1.60980224609375, 3.67596435546875, 3.2449951171875]`;
- max absolute delta: `3.67596435546875` <= `10.0`;
- mean absolute delta: `2.21041259765625` <= `5.0`.

## Local Checks

Artifact consistency check:

```bash
python -c '...'
```

Result: `fixed-policy P01 artifact check PASS`.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu`; TensorFlow GPU run |
| GPU status | Trusted GPU; physical GPU1 selected; process visible device `/GPU:0` |
| CUDA_VISIBLE_DEVICES | `1` |
| TF32 | Enabled and recorded true for float32 |
| Dtype | `float32` |
| Shape | batch seeds `81920..81924`, `T=20`, `N=1024` |
| Wall time | `36.53139637503773` seconds |
| Started | `2026-06-23T10:49:10.715983+00:00` |
| Ended | `2026-06-23T10:49:47.247427+00:00` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-validation-plan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-validation-result-2026-06-23.md` |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS` for this fixed-policy confirmation row. |
| Statistically supported ranking | `NO`. |
| Descriptive-only differences | Runtime and warm timing ratio are descriptive only. |
| Default-readiness | `NO`. |
| Next evidence needed | Separate fixed-policy stress/replication runbook with predeclared gates. |

## Post-Run Red Team

Strongest alternative explanation: `rank=32,epsilon=0.5` may be an isolated safe
configuration rather than a robust policy family.  Prior artifacts showed
nearby settings can fail or become nonfinite.

What would overturn this decision: replicated or stress artifacts showing
nonfinite outputs, residual vetoes, paired threshold failures, or instability at
the fixed policy itself.

Weakest part of evidence: this is still one serious shape/seed batch; it does
not include high-N stress, seed replication beyond the current batch, history
mode, gradient/HMC, or robustness under allowed perturbations.

## Next Action

Create a separate fixed-policy stress runbook before any further promotion or
default-readiness discussion.  Suggested first stress gates:

- same fixed policy, additional seed batches at `N=1024,T=20`;
- one-seed high-N ladder using only `rank=32,epsilon=0.5`;
- history-mode memory/shape check if history artifacts matter;
- explicit HMC/gradient gate only after fixed-policy forward stability passes.
