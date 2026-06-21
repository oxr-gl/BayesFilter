# P04 Same-Route TF32-Vs-FP32 Runtime Result

Date: 2026-06-21

Status: PASSED

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Advance to P05 dense breakpoint context or a justified P05 skip record. |
| Primary criterion status | Passed: both matched `N=10000` arms passed finite/device/storage/precision hard gates on physical GPU1 with `CUDA_VISIBLE_DEVICES=1`. |
| Veto diagnostic status | No P04 veto fired. The two arms matched shape/config except TF32 mode, used GPU output placement, produced finite outputs, used streaming plan mode, did not materialize dense transport storage, did not store full pre-flow particles, and used `return_history=False`. |
| Main uncertainty | The timing ratio is one-repeat descriptive evidence only; it is not a statistically supported speedup claim. |
| Next justified action | Run or skip P05 under its explicit context-only contract, then close out P06. |
| Not concluded | No statistical speedup, no dense-vs-streaming speed verdict, no posterior correctness, no HMC readiness, no public API readiness, and no dense Sinkhorn equivalence. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | At matched large-`N` shape, is TF32-enabled streaming descriptively faster than TF32-disabled streaming on the same route and selected GPU? |
| Baseline/comparator | Same-route FP32 with TF32 disabled. |
| Candidate | Same-route FP32 with TF32 enabled. |
| Primary criterion | Both arms pass hard finite/device/storage/default-metadata gates and produce a matched-shape timing summary. |
| Veto diagnostics | Failed arm, mismatched shape/config, CPU fallback, non-finite output, dense storage, missing artifact, or TF32 mode mismatch. |
| Explanatory diagnostics | Warm median, compile plus first-call time, memory metadata, and timing ratio. |
| Artifact | P04 JSON/Markdown and this result. |

## Run Manifest

| Field | Value |
| --- | --- |
| Command | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_large_particle_efficiency.py --run-kind tf32-vs-fp32 --num-particles 10000 --batch-size 1 --time-steps 80 --state-dim 20 --obs-dim 20 --transport-policy active-all --proposal-mode callback --sinkhorn-iterations 4 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 256 --warmups 0 --repeats 1 --seed 20260621 --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --child-timeout-seconds 3600 --phase-wall-time-budget-seconds 10800 --selected-physical-gpu 1 --gpu-selection-reason jit_clean_gpu1_p04_preflight --artifact-dir docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-gpu-children-2026-06-21 --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-gpu-2026-06-21.json --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-gpu-2026-06-21.md` |
| Conda/env | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13`, TensorFlow `2.20.0` in child artifacts |
| Selected GPU | Physical GPU1, child logical `/GPU:0` |
| Preflight GPU status | Trusted `nvidia-smi`: GPU1 `18 MiB / 32760 MiB`, `0%` utilization, no listed compute apps |
| Seed | `20260621` |
| Shape | `B=1`, `T=80`, `N=10000`, `state_dim=20`, `obs_dim=20` |
| Transport | active-all, streaming plan mode, `sinkhorn_iterations=4`, row/column chunks `1024`, particle chunk `256` |
| Parent wall time | `79.41282888804562` seconds |
| Parent JSON | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-gpu-2026-06-21.json` |
| Parent Markdown | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-gpu-2026-06-21.md` |
| Child artifacts | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-gpu-children-2026-06-21/` |

## Results

| Arm | Hard gate | Compile plus first call s | Warm median s | Child elapsed s | Peak GPU allocator bytes |
| --- | --- | ---: | ---: | ---: | ---: |
| `fp32_tf32_enabled` | passed | `25.014469312038273` | `11.870695133926347` | `40.349858831148595` | `77677056` |
| `fp32_tf32_disabled` | passed | `23.42192833404988` | `12.24538614996709` | `39.061799485003576` | `18875392` |

Matched comparison:

- warm-median ratio `enabled / disabled`: `0.9694014536208195`;
- descriptive warm-median difference: TF32-enabled was `0.3746910160407424`
  seconds lower in this one run, about `3.06%` lower than TF32-disabled;
- matched config except TF32: `true`;
- timing interpretation: descriptive only.

## Required Local Checks

Commands run after P04:

```bash
/home/ubuntu/anaconda3/envs/tfgpu/bin/python -m py_compile docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_large_particle_efficiency.py docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py
```

```bash
/home/ubuntu/anaconda3/envs/tfgpu/bin/python -c "import json, math, pathlib; p=pathlib.Path('docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-gpu-2026-06-21.json'); data=json.loads(p.read_text()); assert data['overall_passed'] is True; assert data['run_kind']=='tf32-vs-fp32'; assert data['shape']=={'batch_size':1,'time_steps':80,'num_particles':10000,'state_dim':20,'obs_dim':20}; children={c['arm_id']:c for c in data['children']}; assert set(children)=={'fp32_tf32_enabled','fp32_tf32_disabled'}; enabled=children['fp32_tf32_enabled']['benchmark']; disabled=children['fp32_tf32_disabled']['benchmark']; assert children['fp32_tf32_enabled']['hard_gate']['passed'] is True; assert children['fp32_tf32_disabled']['hard_gate']['passed'] is True; assert enabled['finite_output'] and disabled['finite_output']; assert enabled['transport']['dense_transport_matrix_materialized'] is False; assert disabled['transport']['dense_transport_matrix_materialized'] is False; assert enabled['stores_full_pre_flow_particles'] is False; assert disabled['stores_full_pre_flow_particles'] is False; assert enabled['return_history'] is False; assert disabled['return_history'] is False; assert enabled['precision']['tf32_execution_enabled'] is True; assert disabled['precision']['tf32_execution_enabled'] is False; assert enabled['shape']==disabled['shape']; assert data['comparison']['matched_config_except_tf32'] is True; ratio=float(data['comparison']['enabled_to_disabled_warm_median_ratio']); assert math.isfinite(ratio) and ratio > 0"
```

Both checks passed.

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for both arms. |
| Statistically supported ranking | None; this is one repeat. |
| Descriptive-only differences | TF32-enabled warm median was lower by about `3.06%`; compile plus first-call and allocator peak differed, but remain descriptive. |
| Default-readiness | P04 is consistent with the owner-directed GPU TF32 default, but does not by itself establish scientific/default validity. |
| Next evidence needed | Replicated matched timing if a defensible speed ranking is needed; otherwise P05/P06 can close the large-particle efficiency program around memory/capacity. |

## Post-Run Red-Team Note

Strongest alternative explanation: the approximately `3%` warm-median advantage
could be ordinary run-to-run noise, compile/cache behavior, or scheduler noise
rather than a stable TF32 runtime advantage.

What would overturn this result: a repeated matched timing ladder showing no
consistent TF32 advantage, or evidence that the arms were not actually matched
except for TF32 mode.

Weakest part of the evidence: one repeat with no uncertainty analysis. Treat the
P04 timing ratio as operational context, not a speed claim.

## Handoff

P05 may start because P04 produced a valid matched-shape same-route timing
artifact and no hard veto fired. P05 must preserve its context-only dense
boundary and must not reinterpret P04 as a statistical speedup result.
