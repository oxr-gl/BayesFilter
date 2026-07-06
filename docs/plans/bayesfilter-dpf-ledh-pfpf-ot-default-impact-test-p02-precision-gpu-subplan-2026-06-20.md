# P02 Subplan: Trusted GPU Precision Drift Screen

Date: 2026-06-20

## Phase Objective

Run a small trusted-GPU three-arm precision comparison for the promoted
GPU-oriented LEDH-PFPF-OT TF32 default: FP64 reference, FP32 with TF32 disabled,
and FP32 with TF32 enabled.  The phase checks finite GPU execution, matching
fixtures/configuration, expected precision metadata, and a loose predeclared
drift sanity bound before any larger target-shape run.

## Entry Conditions Inherited From Previous Phase

- P00 governance gate passed with Claude P00-R4 `VERDICT: AGREE`.
- P01 CPU-hidden deterministic correctness gate passed and wrote result
  artifacts.
- GPU TF32 LEDH-PFPF-OT remains the default target by owner directive.
- P02 is the first trusted GPU evidence in this master program.
- Peer low-rank artifacts and unrelated HMC dirty files remain out of scope.

## Required Artifacts

- JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-2026-06-20.json`
- Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-2026-06-20.md`
- Child artifact directory:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-children-2026-06-20/`
- P02 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p02-precision-gpu-result-2026-06-20.md`
- P03 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p03-target-gpu-subplan-2026-06-20.md`

## Required Checks, Tests, And Reviews

- Syntax checks:
  `python -m py_compile docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_precision.py docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py`
- Trusted GPU availability check:
  `nvidia-smi`
- Precision comparison:
  `python docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_precision.py --cuda-visible-devices 0 --device-scope visible --device /GPU:0 --expect-device-kind gpu --batch-size 1 --time-steps 5 --num-particles 32 --state-dim 4 --obs-dim 4 --transport-policy active-odd --proposal-mode callback --sinkhorn-iterations 2 --sinkhorn-epsilon 0.5 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 16 --col-chunk-size 16 --particle-chunk-size 16 --warmups 0 --repeats 1 --seed 20260620 --child-timeout-seconds 300 --artifact-dir docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-children-2026-06-20 --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-2026-06-20.json --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-2026-06-20.md`
- JSON hard-screen audit:
  `python -c "import json, math, pathlib; p=pathlib.Path('docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-2026-06-20.json'); d=json.load(open(p)); expected_arms={'fp64_reference','fp32_tf32_disabled','fp32_tf32_enabled'}; expected_cmp={'fp32_tf32_disabled','fp32_tf32_enabled'}; expected_outputs={'log_likelihood','filtered_means','filtered_variances','ess_by_time'}; assert d['overall_passed'] is True; assert d['device']=='/GPU:0'; assert d['device_scope']=='visible'; assert d['expect_device_kind']=='gpu'; assert d['cuda_visible_devices_arg']=='0'; assert pathlib.Path(d['artifact_dir']).is_dir(); assert set(d['hard_screen']['config_matches'].keys())==expected_arms and set(d['hard_screen']['config_matches'].values())=={True}; assert set(d['hard_screen']['arrays_present'].keys())==expected_arms and set(d['hard_screen']['arrays_present'].values())=={True}; assert set(d['hard_screen']['finite_outputs'].keys())==expected_arms and set(d['hard_screen']['finite_outputs'].values())=={True}; assert {c['arm_id'] for c in d['children']}==expected_arms; assert all(c['passed'] for c in d['children']); assert all(pathlib.Path(c['json_path']).is_file() and pathlib.Path(c['markdown_path']).is_file() for c in d['children']); assert all(c['benchmark']['finite_output'] for c in d['children']); assert all(c['benchmark']['cuda_visible_devices']=='0' for c in d['children']); assert all(c['benchmark']['physical_gpus'] and c['benchmark']['logical_gpus'] for c in d['children']); assert all(c['benchmark']['output_devices'] and all('GPU' in x.upper() for x in c['benchmark']['output_devices']) for c in d['children']); assert any(c['arm_id']=='fp64_reference' and c['benchmark']['precision']['dtype']=='float64' and c['benchmark']['precision']['tf32_execution_enabled'] is False for c in d['children']); assert any(c['arm_id']=='fp32_tf32_enabled' and c['benchmark']['precision']['dtype']=='float32' and c['benchmark']['precision']['tf32_execution_enabled'] is True for c in d['children']); assert any(c['arm_id']=='fp32_tf32_disabled' and c['benchmark']['precision']['dtype']=='float32' and c['benchmark']['precision']['tf32_execution_enabled'] is False for c in d['children']); assert {cmp['arm_id'] for cmp in d['comparisons']}==expected_cmp; assert all(set(cmp['drift_vs_fp64'].keys())==expected_outputs for cmp in d['comparisons']); assert all(math.isfinite(v['max_relative_to_max1_abs_reference']) and v['max_relative_to_max1_abs_reference'] <= 1.0e-2 for cmp in d['comparisons'] for v in cmp['drift_vs_fp64'].values())"`
- Write P02 result.
- Draft P03 subplan and review it locally for consistency, correctness,
  feasibility, artifact coverage, and boundary safety.  P03 is a material
  trusted-GPU target-shape subplan and cannot execute until its own Claude
  read-only review converges.
- Claude Opus max-effort read-only review is required for P02 before execution
  because this phase crosses into trusted GPU precision evidence.  Claude is not
  an execution authority.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | On a small deterministic trusted-GPU fixture, do FP64, FP32-no-TF32, and FP32+TF32 LEDH-PFPF-OT arms all run finitely on GPU with matching configuration and no gross TF32 drift? |
| Baseline/comparator | FP64 reference arm from `compare_experimental_batched_ledh_pfpf_ot_streaming_precision.py`; FP32-no-TF32 is a descriptive precision comparator. |
| Primary pass criterion | Syntax checks pass; trusted `nvidia-smi` succeeds; precision command exits 0 and writes JSON/MD; JSON reports `overall_passed: true`; parent artifact directory exists; every child JSON/MD exists; every child runs on GPU with nonempty physical/logical GPU metadata, `cuda_visible_devices == "0"`, and finite output; hard screen reports all three expected arm configs match, all three output-array sets are present, and all three outputs are finite; precision metadata matches the three arms; comparisons contain exactly `fp32_tf32_disabled` and `fp32_tf32_enabled`; each comparison contains drift entries for `log_likelihood`, `filtered_means`, `filtered_variances`, and `ess_by_time`; every reported max relative drift is finite and `<= 1.0e-2`. |
| Veto diagnostics | GPU unavailable in trusted context, missing physical/logical GPU enumeration, any child failure, CPU fallback, nonfinite output, missing output arrays, config mismatch, missing comparison arm, missing drift output entry, unexpected TF32 metadata, missing parent/child artifact, or max relative drift above `1.0e-2`. |
| Explanatory diagnostics | Compile/first-call time, warm-call timing, absolute drift, RMS drift, exact GPU memory info, and drift differences between FP32-no-TF32 and FP32+TF32. |
| Not concluded | No posterior correctness, no HMC readiness, no target-shape viability, no statistical superiority, no broad speedup claim, no dense Sinkhorn equivalence, and no public API readiness. |
| Artifact | P02 JSON/MD, child JSON/MD artifacts, P02 result note, and execution/review ledger updates. |

## Forbidden Claims/Actions

- Do not claim TF32 is statistically superior or scientifically correct from a
  single deterministic fixture.
- Do not use timing to rank methods.
- Do not treat this small fixture as target-shape viability.
- Do not edit algorithm code in P02 unless a separate repair subplan is written
  and reviewed first.
- Do not touch peer low-rank files or unrelated HMC dirty files.
- Do not let Claude edit, execute, launch workers, or authorize phase crossing.

## Exact Next-Phase Handoff Conditions

Proceed to P03 only if:

- P02 subplan converges under local and Claude read-only review;
- syntax checks pass;
- trusted GPU availability check succeeds;
- precision JSON/MD and all child artifacts are written;
- hard screen reports all cross-arm configs match, all output arrays are
  present, and all outputs are finite;
- each child benchmark records nonempty physical/logical GPU metadata and GPU
  output placement;
- JSON hard-screen audit passes exactly as stated;
- P02 result preserves command, artifact paths, interpretation, and nonclaims;
- P03 subplan exists and has been reviewed for consistency, correctness,
  feasibility, artifact coverage, and boundary safety;
- P03 subplan records that it cannot execute until Claude read-only review
  converges for P03.

## Stop Conditions

- Trusted GPU is unavailable or `nvidia-smi` fails.
- The precision command exits nonzero or times out.
- Any child arm fails, falls back to CPU, emits nonfinite output, or lacks output
  arrays.
- Drift hard screen exceeds the predeclared `1.0e-2` max-relative bound.
- Required artifacts are missing or malformed.
- Passing would require changing thresholds after seeing output.
- Fix would require algorithm changes beyond a reviewed repair subplan.
- Any action would cross human, runtime, model-file, funding,
  product-capability, default-policy, or scientific-claim boundaries.
