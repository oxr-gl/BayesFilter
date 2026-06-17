# Phase 5 Subplan - HMC-Facing Diagnostics - 2026-06-17

## Phase Objective

Run bounded HMC-facing diagnostics for the experimental TF32 batched
LEDH-PFPF-OT DPF lane after the score path has become JIT-safe on tiny
active-transport fixtures.

The phase asks whether TF32/FP32 value and gradient behavior is viable enough
to justify longer HMC experiments. It does not establish posterior correctness
or production readiness.

## Entry Conditions Inherited From Previous Phase

- Phase 0 through Phase 3 passed.
- Phase 4 no-resampling score/JIT repair passed.
- Phase 4 active-transport streaming-gradient NaN repair result exists and
  records `PHASE_4_STREAMING_GRADIENT_NAN_REPAIR_PASSED`.
- Active-odd FP64 score/JIT artifact records `overall_passed=true`.
- No-resampling FP64 score/JIT regression records `overall_passed=true`.
- The score route is raw streaming gradient stabilization, not dense-gradient
  hybrid and not custom gradient.

## Required Artifacts

- This subplan.
- A small HMC-facing value/gradient precision plan or harness artifact under
  `docs/benchmarks/`.
- FP64 reference value/gradient artifact.
- FP32-no-TF32 comparison artifact.
- FP32-with-TF32 comparison artifact on GPU in trusted context if available.
- A bounded HMC diagnostic artifact with short-chain or mechanics-only
  diagnostics.
- Logs under `docs/benchmarks/logs/`.
- Phase 5 result:
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p5-hmc-facing-diagnostics-result-2026-06-17.md`.
- Refreshed Phase 6 subplan or closeout handoff.

## Required Checks, Tests, And Reviews

Local checks:

1. Preserve the research question separately from implementation tasks.
2. Classify diagnostics before interpreting them:
   - hard veto: non-finite value or gradient, JIT failure, wrong trusted device,
     HMC divergence/invalid transition, missing MH correction artifact;
   - promotion criterion: bounded value/gradient drift relative to FP64 must be
     small compared with predeclared PF Monte Carlo error proxy or replicated
     PF variability;
   - explanatory only: runtime, compile time, GPU memory, warm-call timing,
     acceptance rate from too-short chains.
3. Reuse existing gradient-structure and precision scripts where possible
   before adding new scripts.
4. Run a tiny CPU FP64 active-odd score/JIT guardrail before GPU diagnostics.
5. Run trusted GPU diagnostics only with quiet stdout/stderr redirection.
6. Run `py_compile` on new or patched scripts.
7. Run `git diff --check`.

Review:

- Claude read-only review is required before interpreting any HMC-facing
  diagnostic as evidence beyond a smoke/mechanics check.
- Claude cannot authorize HMC readiness, posterior correctness, production
  readiness, default-policy changes, or particle-cloud sharding claims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Are TF32/FP32 value and gradient errors small relative to particle-filter Monte Carlo variability on bounded fixtures, and do tiny HMC mechanics checks avoid hard vetoes? |
| Baseline/comparator | FP64 score/JIT reference lane; FP32-no-TF32 lane; existing PF MC error vs precision result from 2026-06-15. |
| Primary promotion/pass criterion | No hard veto; FP32-with-TF32 value/gradient drift is a predeclared fraction of PF MC variability on the tested fixture; tiny mechanics/HMC artifact is finite and records MH correction diagnostics. |
| Veto diagnostics | Non-finite value/gradient, JIT failure, wrong trusted GPU placement, missing FP64 reference, missing PF MC comparator, missing MH correction evidence, divergence/invalid sampler transition, or unsupported posterior/HMC-readiness claim. |
| Explanatory diagnostics | Runtime, compile time, memory, ESS, acceptance, gradient norm/cosine, and descriptive drift tables without uncertainty support. |
| What will not be concluded | No posterior correctness, no chain convergence, no production/default readiness, no superiority ranking, no 100k-particle score scalability proof. |
| Artifact preserving result | Phase 5 JSON/Markdown diagnostics plus the Phase 5 result note. |

## Forbidden Claims And Actions

- Do not claim HMC readiness from a smoke test or short chain.
- Do not claim posterior correctness.
- Do not claim production/default/public API readiness.
- Do not rank TF32 as superior using descriptive diagnostics alone.
- Do not treat runtime as correctness evidence.
- Do not shard one filter's particles across GPUs.
- Do not use NumPy in BayesFilter-owned algorithmic implementation paths.

## Exact Next-Phase Handoff Conditions

Phase 6 may begin only if:

- Phase 5 result records either a scoped pass or a clear blocker;
- all required artifacts exist;
- hard veto diagnostics are listed before descriptive metrics;
- unsupported HMC/posterior/default claims are absent;
- Phase 6 subplan or final closeout handoff is refreshed and self-reviewed.

## Stop Conditions

Stop and write a blocker if:

- any hard veto fires;
- the FP64 reference lane fails;
- TF32/FP32 diagnostics cannot be compared against PF MC variability;
- HMC mechanics require broader sampler redesign;
- trusted GPU context is unavailable after rerun;
- a result would need a posterior/HMC-readiness claim not supported by the
  evidence contract.

## Subplan Self-Review

- Consistency: entry conditions match the Phase 4 close record.
- Correctness: FP64 reference and PF MC variability remain explicit baselines.
- Feasibility: the first action is a small CPU guardrail, not a long chain.
- Artifact coverage: JSON/Markdown/log/result paths are required before
  interpretation.
- Boundary safety: HMC readiness, posterior correctness, default policy, and
  particle-cloud sharding claims remain forbidden.
