# BayesFilter DPF LEDH-PFPF-OT FP32/TF32 vs FP64 Precision Plan - 2026-06-15

## Research Intent Ledger

- Main question: Can the experimental streaming GPU LEDH-PFPF-OT value path run in `float32`, with and without NVIDIA TF32 math, while staying numerically close enough to the `float64` reference on a deterministic LGSSM-shaped particle-filter fixture?
- Candidate or mechanism under test: dtype-selectable experimental streaming value path using the same fixed particles, observations, resampling mask, chunks, and Sinkhorn settings across `float64`, `float32` with TF32 disabled, and `float32` with TF32 enabled.
- Expected failure mode: FP32 may emit non-finite values, underflow log-weight floors, drift in log likelihood or filtered moments, or compile to a different device/mode than requested.
- Promotion criterion: all arms compile with XLA on the requested device, emit finite outputs, and the FP32 arms have small descriptive drift from the FP64 reference on log likelihood, filtered means, filtered variances, and ESS.
- Promotion veto: any non-finite output, failed JIT/device check, missing artifact, or comparison run whose fixture/settings differ between arms.
- Continuation veto: do not proceed to larger benchmarks if the small/tiny comparison cannot run deterministically or if the dtype patch changes the FP64 default behavior.
- Repair trigger: FP32 non-finites or large drift trigger scale/log-domain diagnostics before any speed interpretation.
- Explanatory diagnostics: compile time, warm-call time, TensorFlow TF32 execution flag, allocator memory, absolute/relative drift summaries.
- What must not be concluded: no posterior validity claim, no HMC-readiness claim, no production default change, no statistical superiority claim, and no claim that TF32 is used by every op.

## Evidence Contract

- Engineering question: Does a dtype-selectable experimental streaming benchmark provide a fair FP64/FP32/TF32 accuracy and speed screen?
- Exact baseline/comparator: `float64` streaming LEDH-PFPF-OT on the same deterministic fixture is the reference; FP32 arms are compared against that output.
- Primary pass/fail criterion: finite compiled outputs and identical fixture/config manifest across arms.
- Diagnostics that can veto: non-finite output, failed device placement, failed child process, missing JSON artifact, or mismatched shape/transport settings.
- Explanatory-only diagnostics: drift magnitudes and single-run warm-call timings. They describe this run only; they do not rank precision policies statistically.
- Artifact preserving result: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-precision-*.json` and `.md`, with this plan linked in the result note.

## Skeptical Plan Audit

- Wrong baseline: avoided by making FP64 the reference arm in the same script and fixture.
- Proxy metrics: runtime is explanatory only; finite output and fixture equality are hard screens.
- Missing stop conditions: stop if tiny CPU correctness or focused GPU comparison fails.
- Unfair comparison: all arms must share seed, shape, transport policy, chunk sizes, Sinkhorn settings, proposal mode, and return-history setting.
- Hidden assumption: TF32 is a `float32` matmul mode, not a dtype; the artifact will record it as requested/enabled, not as proof every op used TF32.
- Environment mismatch: GPU runs must use trusted/elevated execution and record visible GPUs, TensorFlow version, device outputs, and `CUDA_VISIBLE_DEVICES`.
- Artifact mismatch: comparison script must write both child arm artifacts and an aggregate artifact with drift summaries.

Audit status: passed for an initial viability screen. The plan does not claim production readiness or posterior/HMC validity.

## Implementation Steps

1. Preserve the experimental default as FP64.
2. Add dtype-aware log-weight floors so FP32 cannot convert `1e-300` to zero.
3. Add precision controls to the streaming LGSSM benchmark.
4. Add an aggregate FP64/FP32/TF32 comparison script that launches isolated child arms and records drift.
5. Add a tiny CPU harness test for the new comparison script.
6. Run targeted tests.
7. Run a focused GPU comparison at `T=100`, `D=10`, `N=1000`, active transport, callback proposal, return history enabled.
8. Record the result with decision table, inference-status table, manifest, and nonclaims.
