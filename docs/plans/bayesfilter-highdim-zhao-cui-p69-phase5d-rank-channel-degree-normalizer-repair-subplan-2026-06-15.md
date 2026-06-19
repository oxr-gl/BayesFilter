# P69 Phase 5d Subplan: Rank-Channel Activation And Degree-Normalizer Repair Design

metadata_date: 2026-06-15
status: READY_AFTER_PHASE5C_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p69-remaining-gaps-master-program-2026-06-15.md
phase: 5d
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

review_status: CLAUDE_VERDICT_AGREE_ON_PHASE5C_HANDOFF

## Phase Objective

Design the smallest fixed-variant repair path that can address the Phase 5c
findings before any d18 validation is launched:

- rank-channel inactivity in the realized fixed-TTSIRT fit;
- degree-2 normalizer/design/target-scale instability.

Phase 5d is not d18 validation.  It may produce a repair design, a bounded
implementation subplan, or a blocker.

## Entry Conditions Inherited From Phase 5c

- Phase 5c result exists:
  `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase5c-rank-activity-degree-normalizer-result-2026-06-15.md`.
- Phase 5c diagnostic JSON exists:
  `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase5c-rank-activity-degree-normalizer-diagnostics-2026-06-15.json`.
- Claude read-only review of Phase 5c returns `VERDICT: AGREE`.
- Rank-channel activity is classified as inactive in the realized fixed fit.
- Degree-normalizer/design sensitivity is supported but not repaired.
- Phase 6 d18 validation is blocked pending repair evidence.

## Required Artifacts

- Phase 5d repair-design result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase5d-rank-channel-degree-normalizer-repair-result-2026-06-15.md`.
- Refreshed implementation subplan or blocker handoff.
- Updated P69 visible execution ledger.
- Updated P69 Claude review ledger.

## Required Checks/Tests/Reviews

Start with read-only code and artifact inspection.  If Phase 5d proposes a code
change, it must first classify the change as one of:

- `fixed_hmc_adaptation`: freezes or stabilizes the fixed variant while
  preserving the author's broad route;
- `extension_or_invention`: changes the route beyond the author/fixed-variant
  adaptation and needs explicit approval before being treated as a Zhao--Cui
  gap closure.

Required local checks if any code or test files change:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q <changed files>
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q <focused tests>
```

Claude review must inspect the repair design, classification, and next handoff.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What minimal fixed-variant repair is justified by Phase 5c before validation: rank-channel activation, degree-normalizer stabilization, conservative branch only, or blocker? |
| Baseline/comparator | Phase 5c JSON and Phase 3 comparator rows. |
| Primary criterion | Produce a repair design or blocker that directly targets realized rank-channel inactivity and degree-normalizer/design sensitivity without launching d18 validation. |
| Veto diagnostics | Adaptive parity claim; treating rank-one collapse as scientific sufficiency; treating degree-1/rank-2 as validated; threshold tuning; broad ladder; GPU/HMC use; source-route semantic change without classification and approval. |
| Explanatory diagnostics | Initialization support, ALS sweep/environment dependence, channel activity diagnostics, target scaling summaries, normalizer terms, design condition summaries. |
| Not concluded | No correctness, scaling, HMC readiness, adaptive parity, or paper-failure claim. |
| Artifact preserving result | Phase 5d repair-design result. |

## Forbidden Claims/Actions

- Do not launch Phase 6 d18 validation.
- Do not claim that rank 1 is scientifically sufficient.
- Do not claim degree 1/rank 2 is validated.
- Do not tune Phase 3 thresholds after seeing results.
- Do not use GPU/CUDA/HMC commands.
- Do not call the fixed repair adaptive Zhao--Cui parity.
- Do not close a source-faithfulness gap without paper and author-source line
  anchors.

## Exact Next-Phase Handoff Conditions

Phase 5d may hand off only if:

- it chooses exactly one next route:
  - bounded rank-channel activation implementation;
  - bounded degree-normalizer/design repair implementation;
  - conservative-branch diagnostic-only route with explicit blockers;
  - adaptive-reproduction fork requiring a separate master program;
  - blocker/human direction;
- the chosen route names required artifacts and focused checks;
- Phase 6 remains blocked unless the handoff explicitly states the repaired
  lower gates that must pass before validation;
- Claude returns `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker if:

- the repair requires changing the scientific target rather than the fixed
  adaptation machinery;
- the repair requires adaptive source reproduction under the current phase;
- the repair requires GPU/HMC/long runs without a reviewed subplan and approval;
- Claude and Codex do not converge after five review rounds.
