# P69 Phase 5b Subplan: Fixed-Variant Repair/Design Diagnostic

metadata_date: 2026-06-15
status: READY_AFTER_PHASE5_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p69-remaining-gaps-master-program-2026-06-15.md
phase: 5b
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Run a bounded diagnostic of the current fixed-HMC adaptation before any d18
validation, scaling, or HMC-readiness phase.

The diagnostic must answer whether the next repair target is:

- inactive rank channels;
- deterministic degeneracy as a live unresolved rank zero-delta explanation;
- degree/basis and design coverage sensitivity;
- target scaling/normalization sensitivity;
- overfitting-like degree behavior;
- or an explicit blocker requiring human scientific direction.

## Entry Conditions Inherited From Phase 5

- Phase 5 route decision selects
  `CONTINUE_FIXED_VARIANT_WITH_BOUNDED_REPAIR_DESIGN_DIAGNOSTIC`.
- Claude read-only review of Phase 5 returns `VERDICT: AGREE`.
- Adaptive Zhao--Cui reproduction remains deferred to a separate lane.
- No d18 correctness, scaling, or HMC readiness claim is authorized.

## Required Artifacts

- Phase 5b diagnostic result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase5b-fixed-variant-repair-design-diagnostic-result-2026-06-15.md`.
- Optional JSON/CSV diagnostic artifact under `docs/plans/` if a small script is
  needed.
- Updated P69 execution and Claude review ledgers.
- Refreshed next subplan: either a fixed-variant repair implementation
  subplan, a d18 validation subplan amendment, or a blocker/human-direction
  handoff.

## Required Checks/Tests/Reviews

Before any command beyond read-only analysis, write an evidence contract that
states:

- exact diagnostic question;
- comparator/baseline;
- primary criterion;
- veto diagnostics;
- explanatory-only diagnostics;
- what is not concluded;
- artifact path.

Allowed small diagnostics:

- read-only parsing of Phase 3 JSON;
- inspecting fitted branch manifests, fit residuals, holdout/replay residuals,
  branch hashes, and TT core activity summaries already present;
- adding a small CPU-only diagnostic script only if the required branch-channel
  or design-coverage summary is absent from current artifacts.

Forbidden without a reviewed amendment:

- long ladder rerun;
- GPU/CUDA/HMC command;
- threshold tuning;
- model-file changes;
- adaptive reproduction.

Claude review must inspect the diagnostic result and any next subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which bounded repair/design diagnostic should be applied to the fixed-HMC adaptation before validation/scaling/HMC phases? |
| Baseline/comparator | Phase 3/4 rank zero-delta and degree-instability artifacts. |
| Primary criterion | Identify a concrete repair/design target or blocker without changing thresholds or making correctness claims. |
| Veto diagnostics | Treating fixed-variant diagnostics as adaptive parity; launching long or GPU/HMC work; changing thresholds; claiming d18/scaling/HMC readiness. |
| Explanatory diagnostics | Rank-channel activity, TT core norms, fit/holdout/replay residuals, condition numbers, target scaling, design coverage counts. |
| Not concluded | No correctness, scaling, HMC readiness, adaptive parity, or paper-failure claim. |
| Artifact preserving result | Phase 5b diagnostic result. |

## Forbidden Claims/Actions

- Do not call this an adaptive Zhao--Cui reproduction.
- Do not tune thresholds after seeing results.
- Do not claim d18 validation readiness from Phase 5b alone.
- Do not run GPU/CUDA/HMC commands.
- Do not run a long sweep without a separate reviewed subplan.

## Exact Next-Phase Handoff Conditions

Phase 5b may hand off only if:

- the diagnostic identifies a concrete next repair/design action or blocker;
- deterministic degeneracy is explicitly reported as resolved, weakened, or
  still unresolved;
- unresolved explanations remain explicitly listed;
- claim boundaries are preserved;
- local checks pass for any code changes;
- Claude returns `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker if:

- a bounded diagnostic cannot distinguish the remaining explanations;
- the next action requires changing the scientific target;
- the next action requires long/GPU/HMC/adaptive work without user approval;
- Claude and Codex do not converge after five rounds.
