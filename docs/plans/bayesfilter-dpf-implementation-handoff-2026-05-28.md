# DPF7 Implementation Handoff

## Handoff Decision

`DPF_IMPLEMENTATION_HANDOFF_ACCEPTED`

The planning lane is accepted for user inspection.  The next recommended action
is a separate experimental implementation patch plan, not a production patch.

## Recommended Next Action

Create a reviewed implementation patch plan for:

`experiments/dpf_implementation/`

The first implementation plan should be narrow:

1. build an experimental classical PF harness aligned with DPF1;
2. add deterministic LGSSM/Kalman and affine PF-PF parity fixtures aligned with
   DPF3;
3. add soft-resampling and finite Sinkhorn component tests aligned with DPF2;
4. add same-scalar gradient fixtures aligned with DPF4;
5. wire the DPF5 validation harness as test/report artifacts;
6. keep production `bayesfilter/` exports unchanged until a later DPF6 review.

## Do Not Start With

- production `bayesfilter/` API edits;
- vendored student code;
- learned/amortized OT implementation;
- neural/transformer resampling;
- stochastic flow;
- kernel PFF;
- HMC/posterior sampler integration;
- high-dimensional nonlinear filtering lane artifacts.

## Implementation Acceptance Gates

The future patch plan should require:

- import-boundary check against student baselines;
- CPU-only first diagnostics unless GPU is explicitly justified;
- `CUDA_VISIBLE_DEVICES=-1` before scientific imports for CPU-only runs;
- trusted/escalated permissions for any GPU/CUDA command;
- deterministic/seeded result artifacts;
- DPF5 veto ordering before any proxy or runtime comparison;
- Claude review of plan and result.

## Candidate Artifact Names For Future Plan

- `docs/plans/bayesfilter-dpf-implementation-experimental-patch-plan-2026-05-28.md`
- `experiments/dpf_implementation/README.md`
- `experiments/dpf_implementation/reports/dpf-implementation-smoke-result.md`
- `experiments/dpf_implementation/reports/dpf-implementation-validation-result.md`

## Final Non-Implications

This handoff does not validate an implementation, production API, HMC target,
posterior inference, banking use, model-risk use, high-dimensional readiness, or
learned/neural component.
