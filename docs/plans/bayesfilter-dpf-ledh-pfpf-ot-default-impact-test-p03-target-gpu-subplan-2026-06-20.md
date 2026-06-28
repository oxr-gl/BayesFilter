# P03 Subplan: Target-Shape Trusted GPU Smoke

Date: 2026-06-20

## Phase Objective

Run a production-default trusted-GPU TF32 smoke at the previously demonstrated
capacity shape `B=1,T=120,N=5000,state_dim=50,obs_dim=50` to test whether the
promoted default route remains finite, GPU-placed, streaming, and metadata
consistent at a meaningful LEDH-PFPF-OT scale.

## Entry Conditions Inherited From Previous Phase

- P00 governance gate passed with Claude P00-R4 `VERDICT: AGREE`.
- P01 CPU-hidden deterministic correctness gate passed.
- P02 trusted-GPU precision drift screen passed with Claude-reviewed hard
  screens.
- GPU TF32 LEDH-PFPF-OT remains the production/default target by owner
  directive.
- Prior capacity evidence at this shape exists but used older experimental
  metadata; P03 must write fresh production-default artifacts.
- Peer low-rank artifacts and unrelated HMC dirty files remain out of scope.

## Required Artifacts

- JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p03-target-gpu-2026-06-20.json`
- Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p03-target-gpu-2026-06-20.md`
- P03 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p03-target-gpu-result-2026-06-20.md`
- P04 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p04-performance-memory-subplan-2026-06-20.md`

## Required Checks, Tests, And Reviews

- Syntax check:
  `python -m py_compile docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py`
- Trusted GPU availability check:
  `nvidia-smi`
- Target-shape smoke:
  `timeout 420 python docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py --cuda-visible-devices 0 --device-scope visible --device /GPU:0 --expect-device-kind gpu --batch-size 1 --time-steps 120 --num-particles 5000 --state-dim 50 --obs-dim 50 --transport-policy active-all --proposal-mode callback --sinkhorn-iterations 4 --sinkhorn-epsilon 0.5 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 64 --warmups 0 --repeats 1 --seed 20260620 --dtype float32 --tf32-mode enabled --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p03-target-gpu-2026-06-20.json --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p03-target-gpu-2026-06-20.md`
- JSON hard-screen audit:
  `python -c "import json, math, pathlib; p=pathlib.Path('docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p03-target-gpu-2026-06-20.json'); md=pathlib.Path('docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p03-target-gpu-2026-06-20.md'); d=json.load(open(p)); assert p.is_file() and md.is_file(); assert d['finite_output'] is True; assert d['device']=='/GPU:0'; assert d['device_scope']=='visible'; assert d['expect_device_kind']=='gpu'; assert d['cuda_visible_devices']=='0'; assert d['physical_gpus'] and d['logical_gpus']; assert d['output_devices'] and all('GPU' in x.upper() for x in d['output_devices']); assert d['shape']=={'batch_size':1,'time_steps':120,'num_particles':5000,'state_dim':50,'obs_dim':50}; assert d['transport_policy']=='active-all'; assert d['proposal_mode']=='callback'; assert d['stores_full_pre_flow_particles'] is False; assert d['return_history'] is False; assert d['transport']['plan_mode']=='streaming'; assert d['transport']['dense_transport_matrix_materialized'] is False; assert d['transport']['sinkhorn_iterations']==4; assert d['transport']['row_chunk_size']==512 and d['transport']['col_chunk_size']==512; assert d['particle_chunk_size']==64; prec=d['precision']; assert prec['dtype']=='float32'; assert prec['tf32_mode']=='enabled'; assert prec['tf32_execution_enabled'] is True; assert prec['precision_default_policy']=='production_ledh_pfpf_ot_gpu_tf32'; assert prec['default_algorithm_target']=='ledh_pfpf_ot_tf32'; assert prec['default_execution_target']=='gpu'; assert prec['default_target_status']=='production_default_by_owner_directive'; assert math.isfinite(d['compile_and_first_call_seconds']); assert d['warm_call_timing_summary_seconds']; assert all(math.isfinite(float(v)) for v in d['warm_call_timing_summary_seconds'].values())"`
- Write P03 result.
- Draft P04 subplan and review it locally for consistency, correctness,
  feasibility, artifact coverage, and boundary safety.  P04 is material and
  cannot execute until its own Claude read-only review converges.
- Claude Opus max-effort read-only review is required for P03 before execution
  because this phase runs a target-shape trusted GPU smoke.  Claude is not an
  execution authority.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the production-default GPU TF32 LEDH-PFPF-OT route run finitely on trusted GPU at the previously demonstrated `B=1,T=120,N=5000,D=50,M=50` capacity shape? |
| Baseline/comparator | Prior 2026-06-15 experimental-metadata capacity artifact is historical context only; P03 is a fresh production-default smoke, not a head-to-head speed comparison. |
| Primary pass criterion | Syntax check passes; trusted `nvidia-smi` succeeds; target-shape command exits 0 before timeout and writes JSON/MD; JSON reports finite output, GPU placement, nonempty GPU enumeration, production-default TF32 metadata, streaming/no-dense-transport metadata, callback proposal, no returned history, and exact target shape. |
| Veto diagnostics | Timeout, GPU unavailable in trusted context, CPU fallback, nonfinite output, missing artifact, shape mismatch, dense transport materialization, full pre-flow tensor storage, return-history storage, missing production-default metadata, or TF32 disabled unexpectedly. |
| Explanatory diagnostics | Compile/first-call time, warm-call timing, GPU memory info, log-likelihood preview, and comparison with historical capacity artifact metadata. |
| Not concluded | No posterior correctness, no HMC readiness, no statistical ranking, no broad speedup claim, no precision adequacy beyond P02, no dense Sinkhorn equivalence, and no public API readiness. |
| Artifact | P03 JSON/MD, P03 result note, P04 subplan, execution ledger, and Claude review ledger. |

## Forbidden Claims/Actions

- Do not compare timing against the historical artifact as a speedup claim.
- Do not claim target-shape posterior correctness or HMC readiness.
- Do not treat one synthetic LGSSM-shaped fixture as broad production
  validation.
- Do not edit algorithm code in P03 unless a separate repair subplan is written
  and reviewed first.
- Do not touch peer low-rank files or unrelated HMC dirty files.
- Do not let Claude edit, execute, launch workers, or authorize phase crossing.

## Exact Next-Phase Handoff Conditions

Proceed to P04 only if:

- P03 subplan converges under local and Claude read-only review;
- syntax check passes;
- trusted GPU availability check succeeds;
- target-shape command exits 0 before timeout;
- JSON/MD artifacts are written;
- JSON hard-screen audit passes exactly as stated;
- P03 result preserves command, artifact paths, interpretation, nonclaims, and
  runtime/memory diagnostics as explanatory only;
- P04 subplan exists and has been reviewed for consistency, correctness,
  feasibility, artifact coverage, and boundary safety;
- P04 subplan records that it cannot execute until Claude read-only review
  converges for P04.

## Stop Conditions

- Trusted GPU is unavailable or `nvidia-smi` fails.
- Target-shape command exits nonzero or times out.
- Required JSON/MD artifact is missing or malformed.
- Output is nonfinite or placed on CPU.
- Metadata contradicts production-default GPU TF32 status.
- Passing would require changing thresholds after seeing output.
- Fix would require algorithm changes beyond a reviewed repair subplan.
- Any action would cross human, runtime, model-file, funding,
  product-capability, default-policy, or scientific-claim boundaries.
