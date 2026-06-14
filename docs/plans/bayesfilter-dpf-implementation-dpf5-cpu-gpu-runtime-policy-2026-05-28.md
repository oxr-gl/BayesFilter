# DPF5 CPU/GPU Runtime Policy

## Status

DPF5 execution artifact.  This policy governs device and runtime evidence for
future DPF validation commands.

## CPU/GPU Rules

- Start with CPU-only diagnostics for algebra, reference, shape, and small
  component tests unless a reviewed plan justifies GPU use.
- For deliberate CPU-only runs, set `CUDA_VISIBLE_DEVICES=-1` before framework
  imports and record that choice in the artifact.
- Any command that detects, initializes, benchmarks, or uses GPU/CUDA/NVIDIA
  devices must run with trusted/escalated permissions per repository policy.
- Treat non-escalated GPU failures as sandbox evidence only.
- Runtime evidence must record device, dtype, particle count, horizon, batch
  size, warmup/compilation status, and artifact paths.

## Runtime Interpretation

| Runtime evidence | Allowed use | Forbidden use |
| --- | --- | --- |
| Smoke timing | Detect runaway paths or gross feasibility. | Rank methods. |
| Bounded CPU timing after veto pass | Compare engineering cost on small fixture. | Claim production performance. |
| GPU timing after trusted run | Scaling diagnostic under stated device. | Claim default readiness without DPF6. |
| Student runtime | Qualitative comparison context. | BayesFilter performance evidence. |

## Stop Rules

Stop or label blocked if:

- GPU access is needed but not run under trusted/escalated permissions;
- CPU-only artifact fails to record GPU hiding;
- runtime is used to override failed correctness/gradient/numerical vetoes;
- benchmark artifact size or duration exceeds the reviewed phase contract.
