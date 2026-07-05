# Highdim Leaderboard Remaining Blockers Master Program

Date: 2026-07-02

Status: `DRAFT_REVIEW_READY`

Program owner: Codex supervisor/executor in the current conversation.

Claude role: read-only reviewer only. Claude may identify plan, evidence, or
claim-safety defects, but Claude cannot authorize crossing human, runtime,
model-file, funding, product-capability, default-policy, or scientific-claim
boundaries.

## Objective

Repair, or precisely block, the remaining non-complete high-dimensional
leaderboard cells after the July 1 Zhao-Cui actual-SV/KSC manual-score repair.
The program works one row family at a time:

1. `zhao_cui_predator_prey_T20`;
2. `zhao_cui_generalized_sv_synthetic_from_estimated_values`;
3. `zhao_cui_spatial_sir_austria_j9_T20`;
4. UKF analytical-score cleanup for predator-prey and generalized SV where
   needed after the row-family repairs.

SGQF work remains out of scope except for blocker classification in the
leaderboard artifact. LEDH/PFPF-OT remains omitted from this non-LEDH
leaderboard.

## Baseline

Authoritative baseline:

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`

Current blocked cells from that baseline:

| Row | Algorithm | Current status | Current blocker |
| --- | --- | --- | --- |
| `zhao_cui_predator_prey_T20` | `zhao_cui_scalar_or_multistate` | `blocked_or_status_only` | `P8D_MODEL_SPECIFIC_NUMERIC_EVALUATOR_ADAPTER_REQUIRED` |
| `zhao_cui_predator_prey_T20` | `ukf` | `executed_value_only` | score provenance is autodiff, not admitted |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `zhao_cui_scalar_or_multistate` | `blocked_or_status_only` | exact source-row evaluator missing |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `ukf` | `executed_value_only` | score provenance is autodiff, not admitted |
| `zhao_cui_spatial_sir_austria_j9_T20` | `zhao_cui_scalar_or_multistate` | `blocked_or_status_only` | P91 local component ready; full observed-data/filtering evaluator missing |
| `zhao_cui_spatial_sir_austria_j9_T20` | `ukf` | `executed_value_only` | no-free-theta value-only status in current artifact |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the remaining highdim leaderboard blockers be repaired into honest value plus analytical/manual score rows, or else preserved as precise blockers, without admitting autodiff/FD scores or lower-rung diagnostics as leaderboard evidence? |
| Baseline/comparator | July 1 regenerated highdim leaderboard JSON/Markdown; phase-local target contracts; prior P47/P91 and generalized-SV artifacts only as explicitly classified context, not automatic admission evidence. |
| Primary pass criterion | Each targeted cell either emits finite value and finite analytical/manual score with declared theta coordinates and provenance free of autodiff/FD, or has a precise blocker that separates target, value evaluator, score derivative, and readiness gaps. |
| Veto diagnostics | Autodiff/FD/tape admitted as analytical score; P47 lower-rung diagnostic reported as predator-prey T20; P91 local complete-data SIR sidecar reported as full observed-data/filtering likelihood; actual-SV/KSC/precursor evidence reported as generalized-SV exact source-row evidence; score row without free theta; source-faithful claim without paper/source anchors; GPU/XLA claim from non-trusted context. |
| Explanatory diagnostics | FD consistency, score norm, runtime, score-at-true calibration, CPU-only smoke, trusted GPU/XLA compile or timing, and batch parity. These explain or veto readiness wording but do not prove exact likelihood correctness or posterior correctness. |
| Not concluded | No broad source-faithful adaptive Zhao-Cui reproduction, exact nonlinear likelihood proof, posterior correctness, HMC convergence, GPU superiority, production release readiness, or default-policy change unless separately gated. |
| Artifacts | Master program, visible runbook, phase subplans/results, review ledger, execution ledger, stop handoff, regenerated leaderboard artifacts, and final closeout/reset note if reached. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Baseline freeze and launch gate | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase0-baseline-freeze-subplan-2026-07-02.md` | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase0-baseline-freeze-result-2026-07-02.md` |
| 1 | Predator-prey T20 Zhao-Cui evaluator and analytical score | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase1-predator-prey-subplan-2026-07-02.md` | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase1-predator-prey-result-2026-07-02.md` |
| 2 | Generalized-SV exact source-row evaluator and analytical score | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase2-generalized-sv-subplan-2026-07-02.md` | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase2-generalized-sv-result-2026-07-02.md` |
| 3 | Spatial SIR full observed-data/filtering route | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase3-spatial-sir-subplan-2026-07-02.md` | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase3-spatial-sir-result-2026-07-02.md` |
| 4 | UKF analytical-score cleanup for remaining value-only rows | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-ukf-score-cleanup-subplan-2026-07-02.md` | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-ukf-score-cleanup-result-2026-07-02.md` |
| 5 | Batch/GPU/XLA readiness and score-at-true calibration | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-readiness-calibration-subplan-2026-07-02.md` | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-readiness-calibration-result-2026-07-02.md` |
| 6 | Final regeneration and closeout | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase6-final-regeneration-subplan-2026-07-02.md` | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase6-final-regeneration-result-2026-07-02.md` |

## Per-Phase Required Subplan Fields

Every phase subplan must state:

- phase objective;
- entry conditions inherited from the previous phase;
- required artifacts;
- required checks/tests/reviews;
- evidence contract;
- forbidden claims/actions;
- exact next-phase handoff conditions;
- stop conditions.

At each phase end Codex must:

1. run required local checks;
2. write a phase result / close record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Repair Loop

- Claude may be used as a read-only reviewer for material subplans and phase
  results.
- Use bounded one-path Claude prompts first. Do not paste whole files when a
  path-based review can answer the gate.
- If Claude does not respond, first run a small probe. If the probe responds,
  treat the original review prompt as the problem and redesign it into a
  smaller bounded prompt.
- If review finds a fixable problem, patch the same subplan visibly and rerun
  focused local checks.
- Loop Claude review at high/max effort only for material issues, stopping
  after five rounds for the same blocker.
- If a subplan converges, continue to the next phase.
- If a subplan does not converge, write a blocker result and stop for human
  direction.

## Approval And Execution Needs

Already anticipated from the user request:

- Claude Code read-only review approval for bounded `claude -p` calls.
- CPU-only local checks with `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import.
- Source, test, and planning document edits within `/home/chakwong/BayesFilter`.

Ask for explicit approval before:

- GPU/CUDA/XLA commands or benchmarks;
- network/package/remote-service access;
- destructive git/filesystem actions;
- changing leaderboard admission criteria after seeing results;
- release tagging, default-policy changes, or product-capability claims.

## Skeptical Audit

Initial audit status: `PASSED_FOR_PLANNING_ONLY`.

Risks encoded in the phases:

- A row can have a finite value while score admission remains blocked.
- Autodiff score provenance must stay diagnostic only.
- Lower-rung P47 predator-prey fixtures are not T20 source-row evidence.
- P91 SIR local complete-data evidence is not full filtering evidence.
- Generalized-SV exact source-row target cannot borrow actual-SV/KSC evidence.
- Score-at-true consistency can veto readiness wording but cannot prove exact
  likelihood correctness.
- Batch/GPU/XLA readiness is separate from value/score row admission.

Execution begins only through:

- `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-visible-gated-execution-runbook-2026-07-02.md`
