# P04C1 Result: Streaming Comparator Nonfinite Diagnostic

Date: 2026-06-26

Status: `P04C1_GPU_TF32_OR_JIT_SPECIFIC_DIAGNOSTIC`

## Phase Objective

Diagnose why P04C seed `84101` produced a deterministic-invalid streaming
comparator artifact while the SVD-Nystrom route passed deterministic checks.

## Decision Table

| Field | Result |
| --- | --- |
| Decision | `P04C1_GPU_TF32_OR_JIT_SPECIFIC_DIAGNOSTIC` |
| Primary criterion status | PASS for P04C1 diagnostic classification: exact row artifacts were produced and parsed. |
| Veto diagnostic status | No P04C1 artifact-validity veto fired. The original P04C calibration veto remains active. |
| Main uncertainty | P04C1 localizes the nonfinite behavior to GPU/TF32/JIT streaming execution for seed `84101`, but it does not distinguish TF32, JIT/XLA, GPU kernel/device behavior, or their interaction. |
| Next justified action | Draft, review, and execute a P04C2 GPU TF32/JIT isolation subplan before any calibration redesign or P04C continuation. |
| What is not concluded | No calibrated threshold, no repaired P04C panel, no seed exclusion, no SVD-Nystrom rejection, no default promotion, no posterior correctness, no HMC readiness, no statistical superiority, and no broad nonlinear validity. |

## Evidence Contract Outcome

| Field | Contract Outcome |
| --- | --- |
| Question | Answered diagnostically: seed `84101` streaming nonfinite behavior is reproducible under GPU/TF32/JIT, seed-neighbor controlled, and finite under CPU/no-JIT/no-TF32. |
| Baseline/comparator | P04C seed `84101` failed both-route artifact and P04C seed `84100` passed artifact. |
| Primary criterion | Met for diagnostic classification; P04C calibration remains blocked. |
| Veto diagnostics | No missing, malformed, route-mismatched, GPU/TF32-mismatched, or unsupported-claim artifact found. |
| Explanatory diagnostics | Route finite status, hard vetoes, log likelihood, ESS, runtime, GPU/CPU/JIT differences. |
| Not concluded | No threshold freeze, P04C resume, P05 launch, promotion, HMC, posterior-correctness, or scientific-validity claim. |
| Artifact | `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-streaming-nonfinite-diagnostic-summary-2026-06-26.json` |

## Diagnostic Rows

Trusted GPU preflight selected physical GPU1 under the owner rule "GPU1 if
available, otherwise GPU0":

| GPU | Memory used | Total memory | Utilization |
| ---: | ---: | ---: | ---: |
| 0 | 1242 MiB | 32760 MiB | 23% |
| 1 | 18 MiB | 32760 MiB | 0% |

| Row | Device / mode | Route | Seed | Status | Streaming hard vetoes | Nystrom status |
| --- | --- | --- | ---: | --- | --- | --- |
| `gpu-streaming-repro-84101` | GPU1, TF32 enabled, JIT on | `streaming` | 84101 | `FAIL` | `nonfinite_log_likelihood`, `nonfinite_filtered_means`, `nonfinite_filtered_variances`, `nonfinite_ess_by_time` | N/A |
| `gpu-both-repro-84101` | GPU1, TF32 enabled, JIT on | `both` | 84101 | `FAIL` | `nonfinite_log_likelihood`, `nonfinite_filtered_means`, `nonfinite_filtered_variances`, `nonfinite_ess_by_time` | `PASS` |
| `gpu-streaming-control-84100` | GPU1, TF32 enabled, JIT on | `streaming` | 84100 | `PASS` | `[]` | N/A |
| `cpu-streaming-control-84101` | CPU hidden, TF32 disabled, JIT off | `streaming` | 84101 | `PASS` | `[]` | N/A |

The nonzero exits for the two failing GPU rows are expected diagnostic exits:
both wrote valid JSON artifacts with streaming-route nonfinite hard vetoes.

## Interpretation

P04C1 confirms that the seed `84101` blocker is reproducible in the streaming
comparator route under the same GPU/TF32/JIT execution target used by P04C.
The both-route repro also confirms that the locked SVD-Nystrom route remains
deterministic-valid on seed `84101`.

The passing `84100` streaming GPU control argues against a blanket streaming
route failure. The passing seed `84101` CPU/no-JIT/no-TF32 control argues
against broad fixture or seed invalidity. The remaining uncertainty is whether
the culprit is TF32, JIT/XLA, GPU kernel/device behavior, or a TF32+JIT
interaction.

## Artifacts

- Aggregate summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-streaming-nonfinite-diagnostic-summary-2026-06-26.json`
- `gpu-streaming-repro-84101` JSON:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-streaming-repro-seed84101-2026-06-26.json`
- `gpu-streaming-repro-84101` Markdown:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-streaming-repro-seed84101-2026-06-26.md`
- `gpu-streaming-repro-84101` log:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c1-streaming-repro-seed84101.log`
- `gpu-both-repro-84101` JSON:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-both-repro-seed84101-2026-06-26.json`
- `gpu-both-repro-84101` Markdown:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-both-repro-seed84101-2026-06-26.md`
- `gpu-both-repro-84101` log:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c1-both-repro-seed84101.log`
- `gpu-streaming-control-84100` JSON:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-streaming-control-seed84100-2026-06-26.json`
- `gpu-streaming-control-84100` Markdown:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-streaming-control-seed84100-2026-06-26.md`
- `gpu-streaming-control-84100` log:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c1-streaming-control-seed84100.log`
- `cpu-streaming-control-84101` JSON:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-cpu-streaming-control-seed84101-2026-06-26.json`
- `cpu-streaming-control-84101` Markdown:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c1-cpu-streaming-control-seed84101-2026-06-26.md`
- `cpu-streaming-control-84101` log:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c1-cpu-streaming-control-seed84101.log`

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | P04C calibration remains blocked by invalid streaming comparator artifact on seed `84101`; P04C1 artifacts themselves are valid. |
| Statistically supported ranking | NO |
| Descriptive-only differences | Runtime, log likelihood, and ESS differences are diagnostic only. |
| Default-readiness | NO |
| Next evidence needed | Reviewed P04C2 GPU TF32/JIT isolation panel. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Conda/Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13` |
| TensorFlow | `2.20.0` |
| GPU preflight | GPU1 selected: 18 MiB used, 0% utilization |
| Seeds | `84101`, `84100` |
| Shape | Range-bearing fixture, `T=20`, `N=4096`, `float32` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c1-streaming-nonfinite-diagnostic-subplan-2026-06-26.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c1-streaming-nonfinite-diagnostic-result-2026-06-26.md` |

## Post-Run Red-Team Note

Strongest alternative explanation: the observed CPU pass may reflect the
combined change of device, TF32, and JIT status rather than one isolated cause.
P04C1 therefore must not label the issue as purely TF32, purely JIT, or purely
GPU. The result that would overturn the current classification would be a
reviewed rerun showing seed `84101` streaming finite under GPU/TF32/JIT with
the same command and artifact contract, or showing malformed P04C1 artifacts.

Weakest part of the evidence: the CPU control changes three execution factors
at once. P04C2 should isolate TF32, JIT, and GPU/no-TF32/no-JIT behavior before
any repair or calibration redesign.

## Handoff

`P04C1_GPU_TF32_OR_JIT_SPECIFIC_DIAGNOSTIC`

P04C remains blocked. Do not run remaining P04C calibration seeds, do not drop
seed `84101`, do not count it as a non-exceedance, do not launch P05, and do
not freeze a nonlinear threshold. The next justified action is the reviewed
P04C2 GPU TF32/JIT isolation subplan.
