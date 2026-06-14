# DPF2 Resampling Test Contract

## Status

DPF2 execution artifact.  This contract defines bounded tests required before
optional differentiable resampling components can be implemented or compared.

## Test Matrix

| Test ID | Component | Baseline/reference | Primary criterion | Veto diagnostics | Explanatory only |
| --- | --- | --- | --- | --- | --- |
| DPF2-T1 | Soft resampling affine summary | Closed-form two-particle or small-cloud expectation | Affine/mean residual within tolerance | Missing alpha/observable class or non-finite output | Runtime |
| DPF2-T2 | Soft resampling nonlinear bias | Categorical-summary reference | Nonzero/recorded nonlinear delta with caveat | Claiming nonlinear unbiasedness | Bias magnitude trend |
| DPF2-T3 | Finite Sinkhorn residual | Manual balanced marginal reference | Row/column/mass/nonnegative/finite residuals pass at declared budget | Missing epsilon, budget, stabilization, or tolerance | Residual trend before final budget |
| DPF2-T4 | Sinkhorn gradient smoke | Named scalar using finite solver | Finite gradient and same object label | Treating gradient as categorical likelihood score | Gradient norm |
| DPF2-T5 | Memory/runtime smoke | Declared `N`, `K`, dtype, device | Bounded artifact row; no unplanned GPU use | Runtime-only promotion | Runtime and memory notes |
| DPF2-T6 | Learned/neural gate | Approved teacher/student artifact | Artifact provenance exists before residual execution | Inventing substitute teacher or using student checkpoint as authority | Architecture notes |

## Artifact Requirements

Each test artifact must record:

- component id and mathematical object;
- reference/comparator id;
- `alpha` or `epsilon/K/stabilization/tolerance` as applicable;
- dtype, device, seed/key, CPU/GPU status;
- exact scalar for gradient tests;
- pass/fail/veto fields;
- non-implication text.

## GPU/CPU Policy

DPF2 tests should start CPU-only unless a reviewed result explicitly justifies a
GPU run.  If CPU-only, set `CUDA_VISIBLE_DEVICES=-1` before scientific imports.
If GPU/CUDA is used, commands must run with trusted/escalated permissions per
the repository policy.

## Stop Rules

Stop before implementation movement if:

- the component cannot state whether it is hard, soft, EOT, finite Sinkhorn,
  solver-gradient, learned, or neural;
- finite gradients are used as correctness or HMC evidence;
- a learned/neural path lacks approved teacher/student provenance;
- student code or checkpoints are required as authority;
- high-dimensional lane material is needed.

## Non-Implications

DPF2 tests do not validate a full DPF, original posterior preservation, HMC
target correctness, production API readiness, or banking/model-risk use.
