# Phase 1 Subplan - Implementation And Precision Inventory - 2026-06-16

## Phase Objective

Inventory the current TF32 batched DPF implementation, precision controls, JIT
boundaries, benchmark scripts, and score-path blockers before any further
implementation.

This phase is read-mostly. It may update plan/result documentation, but it must
not change algorithm code unless a later reviewed repair subplan explicitly
authorizes that edit.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result records `PHASE_0_PASSED`.
- Phase 0 Claude review artifact exists and ends with `VERDICT: AGREE`.
- Visible runbook and execution ledger are active.
- Worktree may be dirty; unrelated changes remain protected.
- TF32 is scoped to the experimental LEDH-PFPF-OT GPU/performance lane only.

## Required Artifacts

- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p1-implementation-precision-inventory-result-2026-06-16.md`
- Updated execution ledger entry for Phase 1.
- Draft or refreshed Phase 2 subplan:
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p2-single-gpu-batched-value-subplan-2026-06-16.md`
- Optional Claude review artifact if Phase 1 changes the planned Phase 2 scope
  materially.

## Required Checks, Tests, And Reviews

Local checks:

1. Search and record implementation files for:
   - streaming LEDH-PFPF-OT value path;
   - fixed-branch experimental path;
   - TF32/default precision constants or CLI flags;
   - score/value-score path;
   - benchmark and correctness harnesses.
2. Record whether each path is value-only, value+score, JIT-safe, GPU-intended,
   reference/comparison-only, or reporting-only.
3. Record FP64, FP32-no-TF32, and FP32+TF32 lanes and their current artifact
   support.
4. Record dirty-worktree risks touching the DPF files without reverting
   unrelated changes.
5. Run only small import/source checks if needed; no long GPU benchmarks.

Review:

- Run Claude read-only review only if the inventory changes the master-program
  phase boundaries, uncovers a material blocker, or materially rewrites the
  Phase 2 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact code paths and precision knobs currently define the TF32 batched DPF lane, and what must Phase 2 use or avoid? |
| Baseline/comparator | Current repository files plus the 2026-06-15 TF32 default, MC-noise, capacity, and reset artifacts. |
| Primary pass criterion | Phase 1 result contains a file/function inventory, precision-lane table, score/JIT blocker statement, dirty-worktree boundary, and Phase 2 handoff. |
| Veto diagnostics | Missing streaming implementation path; missing precision controls; FP64/FP32-no-TF32 reference lanes omitted; HMC readiness claimed; implementation changes made without a repair subplan; unrelated dirty files modified. |
| Explanatory diagnostics | Counts of relevant files, source-level notes, and small import/source-check outputs. |
| Not concluded | No speed ranking, no correctness proof, no HMC readiness, no production default, no public API readiness. |
| Artifact preserving result | Phase 1 result file and optional Claude review artifact. |

## Forbidden Claims And Actions

- Do not modify algorithm code during inventory.
- Do not run long GPU benchmarks.
- Do not treat source existence as correctness.
- Do not claim HMC readiness from value-path inventory.
- Do not treat TF32 as a global BayesFilter dtype default.
- Do not claim two-GPU particle-cloud sharding.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only after:

- Phase 1 result exists and records `PHASE_1_PASSED`;
- the streaming value path and benchmark harnesses are identified;
- precision lanes and TF32 controls are identified;
- score/JIT blockers are explicitly separated from value batching;
- Phase 2 subplan exists with exact commands/artifacts/checks for the
  single-GPU batched value runner;
- no human-required stop condition is active.

## Stop Conditions

Stop and write a blocker result if:

- implementation files cited by prior artifacts are missing or unusable;
- the current repository state contradicts the reset memo in a way that changes
  the program scope;
- TensorFlow import/source inspection requires package installation or
  environment repair;
- the score path cannot be separated from value batching without a scientific
  or product decision;
- continuing would require modifying unrelated dirty worktree files.
