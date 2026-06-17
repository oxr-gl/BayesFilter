# Phase 2 Subplan - Single-GPU Batched Value Runner - 2026-06-16

## Phase Objective

Implement or verify a single-GPU runner for independent-row batched streaming
LEDH-PFPF-OT value evaluation using the current TF32 performance default.

This phase is value-only. It does not repair or promote the score path.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result records `PHASE_0_PASSED`.
- Phase 1 result records `PHASE_1_PASSED`.
- Phase 1 identified the streaming value path, precision lanes, and score/JIT
  boundary.
- Worktree may be dirty; existing untracked DPF artifacts are preserved.
- Claude is read-only reviewer only when materially needed.

## Required Artifacts

- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p2-single-gpu-batched-value-result-2026-06-16.md`
- Updated execution ledger entry for Phase 2.
- Any new or updated opt-in runner/check artifacts needed for independent-row
  single-GPU value evaluation.
- Benchmark/check JSON and Markdown artifacts under `docs/benchmarks/` for
  bounded Phase 2 runs.
- Draft or refreshed Phase 3 subplan:
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p3-two-gpu-row-splitting-subplan-2026-06-16.md`

## Required Checks, Tests, And Reviews

Local checks before material edits or runs:

1. Reconfirm the streaming correctness gate can run on a tiny CPU fixture or
   explain why it cannot.
2. Reconfirm the streaming value path JIT smoke on a small bounded shape before
   any larger GPU run.
3. Verify benchmark artifacts record dtype, TF32 mode, JIT status, device
   placement, finite output, proposal mode, return-history mode, and nonclaims.

Phase 2 target checks:

1. Single-GPU TF32 value run for a bounded independent-row batch with
   `return_history=False`, `proposal-mode=callback`, and JIT enabled.
2. At least one tiny or small reference/comparison run that keeps FP64 or
   FP32-no-TF32 available as a comparator.
3. Row-locality or permutation/identical-row check if any new batch runner is
   introduced.

Review:

- Use Claude read-only review if Phase 2 introduces a new runner, materially
  changes existing runner semantics, or changes the Phase 3 scope.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the current streaming value path evaluate independent batch rows on one GPU under the scoped TF32 performance policy with bounded correctness guardrails? |
| Baseline/comparator | Existing streaming correctness gate, fixed-branch baseline on tiny fixtures, and FP64/FP32-no-TF32 lanes for reference/comparison. |
| Primary pass criterion | Bounded single-GPU TF32 value artifact is finite, JIT-compiled, device-placed on GPU in trusted context, records precision metadata, and does not regress tiny correctness checks. |
| Veto diagnostics | Non-finite value; missing JIT metadata; wrong device in trusted GPU run; missing precision metadata; missing reference lane; row cross-talk in any new batch runner; score/HMC claim; production/public API claim. |
| Explanatory diagnostics | Compile time, warm-call time, GPU memory, batch size, particle count, state dimension, and transport chunk settings. |
| Not concluded | No speed superiority, no HMC readiness, no score correctness, no production default, no public API readiness, no single-filter multi-GPU particle sharding. |
| Artifact preserving result | Phase 2 result file plus benchmark/check JSON and Markdown artifacts. |

## Skeptical Audit Before Execution

Before running Phase 2 commands, check:

- wrong baseline: value path must compare against existing streaming/fixed
  correctness gates, not HMC diagnostics;
- proxy metric risk: timing and memory are explanatory unless a specific pass
  criterion says otherwise;
- missing stop condition: non-finite, wrong device, missing JIT metadata, or
  missing precision metadata must stop promotion;
- unfair comparison: compare like precision lanes only when making precision
  statements;
- hidden assumption: batch rows are independent filters, not one sharded filter;
- stale context: re-run tiny checks before interpreting larger artifacts;
- environment mismatch: GPU results require trusted context;
- artifact adequacy: each run must write JSON/Markdown artifacts with metadata.

## Forbidden Claims And Actions

- Do not claim HMC readiness or score JIT readiness.
- Do not change production defaults or public API exports.
- Do not claim single-filter multi-GPU particle-cloud sharding.
- Do not rank TF32 versus FP64 by speed or accuracy without a later
  predeclared uncertainty/comparison contract.
- Do not modify unrelated dirty worktree files.
- Do not run long capacity tests before a smaller Phase 2 gate passes.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only after:

- Phase 2 result exists and records `PHASE_2_PASSED`;
- bounded single-GPU TF32 value artifact exists and is finite, JIT-compiled,
  GPU-placed in trusted context, and precision-metadata complete;
- tiny correctness/JIT guardrail artifacts are recorded or a blocker explains
  why they could not run;
- any new runner has row-locality or equivalent independent-row guardrails;
- Phase 3 subplan exists and explicitly limits multi-GPU work to independent
  row splitting;
- no human-required stop condition is active.

## Stop Conditions

Stop and write a blocker result if:

- TensorFlow/GPU access fails in trusted context;
- tiny correctness/JIT guardrails fail;
- benchmark artifacts are missing required metadata;
- a new runner shows row cross-talk;
- the work would require package installation, network fetch, credentials,
  destructive filesystem/git action, detached execution, or changing a
  production default;
- continuing would require resolving the score/HMC path before value batching.
