# P69 Phase 5c Subplan: Rank Activity And Degree-Normalizer Design Diagnostic

metadata_date: 2026-06-15
status: READY_AFTER_PHASE5B_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p69-remaining-gaps-master-program-2026-06-15.md
phase: 5c
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Diagnose the selected fixed-variant repair/design target:

`RANK_ACTIVITY_AND_DEGREE_NORMALIZER_DESIGN_DIAGNOSTIC`

The phase must determine whether the next repair is:

- rank-channel activity exposure or initialization/fitting repair;
- degree-normalizer/design-coverage repair;
- conservative branch selection for later d18 validation;
- or blocker/human direction.

## Entry Conditions Inherited From Phase 5b

- Phase 5b result exists:
  `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase5b-fixed-variant-repair-design-diagnostic-result-2026-06-15.md`.
- Claude read-only review of Phase 5b returns `VERDICT: AGREE`.
- Deterministic degeneracy, overfitting, and target scaling remain live
  unresolved explanations.
- No d18 validation, scaling, HMC readiness, or adaptive reproduction is
  authorized.

## Required Artifacts

- Phase 5c diagnostic result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase5c-rank-activity-degree-normalizer-result-2026-06-15.md`.
- Optional small JSON artifact under `docs/plans/` if a diagnostic script is
  needed.
- Updated P69 execution and Claude review ledgers.
- Refreshed next subplan or blocker handoff.

## Required Checks/Tests/Reviews

Start with read-only artifact inspection.  If existing artifacts cannot expose
rank-channel or degree-normalizer details, add only a small CPU-only diagnostic
script or helper under a reviewed evidence contract.

Required pre-run evidence contract must state:

- exact diagnostic question;
- comparator/baseline;
- primary criterion;
- veto diagnostics;
- explanatory-only diagnostics;
- what is not concluded;
- artifact path.

Required local checks if code changes:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q <changed files>
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q <focused tests>
```

Claude review must inspect the diagnostic result and next handoff.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are rank-3 channels inactive by construction/fit, and is degree-2 instability driven by normalizer/design scaling rather than a route wiring bug? |
| Baseline/comparator | Phase 3 rank 2 vs rank 3 row pair and degree 1 vs degree 2 row pair. |
| Primary criterion | Produce direct diagnostics or a blocker for rank-channel activity and degree-normalizer/design sensitivity without changing thresholds or running a broad ladder. |
| Veto diagnostics | Source-route drift; branch-identity drift; threshold tuning; treating fixed diagnostics as adaptive parity; claiming d18/scaling/HMC readiness. |
| Explanatory diagnostics | Per-rank-channel norms, core activity summaries, normalizer decomposition, target scale summaries, design coverage summaries, fit/holdout/replay residuals. |
| Not concluded | No correctness, scaling, HMC readiness, adaptive parity, or paper-failure claim. |
| Artifact preserving result | Phase 5c diagnostic result. |

## Forbidden Claims/Actions

- Do not run a broad ladder or long sweep.
- Do not use GPU/CUDA/HMC commands.
- Do not tune thresholds.
- Do not change source-route semantics.
- Do not claim adaptive Zhao--Cui parity.
- Do not authorize d18 validation unless the result explicitly supports a
  conservative branch and states remaining blockers.

## Exact Next-Phase Handoff Conditions

Phase 5c may hand off only if:

- rank-channel activity is classified as active, inactive, gauge-hidden, or
  unresolved;
- degree-normalizer/design sensitivity is classified as repairable,
  conservative-branch-only, or unresolved;
- deterministic degeneracy, overfitting, and target scaling are explicitly
  updated as resolved, weakened, or still unresolved;
- any code changes are locally checked;
- Claude returns `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker if:

- diagnostics cannot be obtained without broad reruns or source-route changes;
- the next step requires adaptive reproduction or human target change;
- the next step requires GPU/HMC/long runs without approval;
- Claude and Codex do not converge after five review rounds.
