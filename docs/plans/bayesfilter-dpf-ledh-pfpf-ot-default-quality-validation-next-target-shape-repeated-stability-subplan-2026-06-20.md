# Draft Next-Rung Subplan: Target-Shape Repeated Stability

Status: `DRAFT_NOT_LAUNCHED`

## Phase Objective

If approved later, extend the medium paired quality result to a target-shape or
near-target-shape repeated stability screen for the promoted GPU TF32 streaming
LEDH-PFPF-OT default.

## Entry Conditions Inherited From Previous Phase

- P02 medium trusted-GPU paired quality screen passed.
- P02 artifacts are internally consistent and preserve per-seed/per-output
  drift records, metadata assertions, GPU placement, and output-array screens.
- This draft has not been reviewed for launch and must not be executed without
  a new reviewed plan/execution request.
- GPU selection policy for future launch: run trusted `nvidia-smi` first;
  prefer GPU1 if it is not busy, and use GPU0 only if GPU1 is busy or otherwise
  unsuitable. Record the selected GPU, reason, and `CUDA_VISIBLE_DEVICES` value
  in the run manifest.

## Required Artifacts

- Reviewed target-shape repeated stability subplan.
- Parent JSON/Markdown artifacts under `docs/benchmarks`.
- Child artifacts with paired seeds and precision arms.
- Result note with decision table, inference-status table, run manifest, and
  post-run red-team note.

## Required Checks, Tests, And Reviews

- Re-run trusted `nvidia-smi`.
- Apply the GPU selection policy: prefer GPU1 unless busy; otherwise use GPU0.
- Reconfirm no stale artifacts from the medium P02 run are reused.
- Review shape, runtime budget, and timeout before launch.
- Claude may review the launch subplan read-only if this becomes material.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the GPU TF32 default preserve downstream filter outputs at target or near-target shape across repeated trusted-GPU runs? |
| Baseline/comparator | Paired FP64 TF32-disabled arm if feasible at the selected shape; otherwise a separately justified comparator must be reviewed before execution. |
| Primary pass criterion | To be set before launch; must include finite outputs, GPU placement, metadata assertions, paired seed count, per-output drift preservation, and predeclared tolerance. |
| Veto diagnostics | Nonfinite output, CPU fallback, missing arrays, stale metadata, missing paired-seed/per-output records, timeout not attributable to shape selection, or drift above tolerance. |
| Explanatory diagnostics | Runtime, memory, compile time, warm timing, and FP32-no-TF32 drift. |
| Not concluded | No posterior correctness, HMC readiness, sampler convergence, speedup, statistical superiority, or scientific validity without separate evidence. |

## Forbidden Claims And Actions

- Do not launch this draft as-is.
- Do not change the tolerance after seeing target-shape results.
- Do not omit FP64 comparator feasibility review.
- Do not treat timing as speedup evidence without a separate statistical plan.

## Exact Next-Phase Handoff Conditions

Before launch, write a new reviewed subplan that fixes:

- exact shape and runtime budget;
- whether FP64 target-shape comparison is feasible;
- number of paired seeds;
- tolerance and drift formula;
- timeout and continuation rules;
- artifact paths.

## Stop Conditions

Stop before launch if FP64 target-shape comparator is infeasible and no reviewed
alternative comparator has been approved, if GPU resources are unavailable, or
if the run would cross a runtime/funding/scientific-claim boundary not already
approved.
