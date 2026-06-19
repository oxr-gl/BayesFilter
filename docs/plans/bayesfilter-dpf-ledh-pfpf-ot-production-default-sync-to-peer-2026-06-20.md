# BayesFilter DPF LEDH-PFPF-OT Production Default Sync To Peer - 2026-06-20

## Message To Peer Lane

The repository DPF transport default has been promoted by owner directive:
GPU-oriented LEDH-PFPF-OT TF32 is now the production/default target.

Canonical policy/result artifacts:

- `AGENTS.md`
- `CLAUDE.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-gpu-tf32-production-default-result-2026-06-20.md`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-production-default-gpu-tf32-smoke-2026-06-20.{json,md}`

Fresh trusted GPU smoke status:

- route: streaming LEDH-PFPF-OT LGSSM default;
- device: `/GPU:0`;
- output placement: GPU;
- precision policy: `production_ledh_pfpf_ot_gpu_tf32`;
- default execution target: `gpu`;
- dtype: `float32`;
- TF32 execution: enabled;
- output: finite.

## Boundary For Peer Work

The low-rank coupling solver-route remains an independent candidate lane.  It
should continue to report its own evidence, invariants, and artifacts without
waiting for or merging into the positive-feature/LEDH default lane unless a
future integration phase explicitly asks for that.

The peer lane should not reinterpret this default-policy promotion as:

- low-rank candidate rejection;
- proof of posterior correctness;
- HMC readiness;
- statistical superiority;
- dense Sinkhorn equivalence;
- public API readiness.

The useful shared boundary is now simple: independent candidate artifacts may
be compared or audited later, but the repo default for DPF transport starts from
GPU-oriented LEDH-PFPF-OT TF32 unless a reviewed artifact or human directive
supersedes it.
