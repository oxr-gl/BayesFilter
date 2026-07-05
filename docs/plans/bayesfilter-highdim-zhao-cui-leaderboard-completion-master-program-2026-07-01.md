# BayesFilter Highdim Zhao-Cui Leaderboard Completion Master Program

Date: 2026-07-01

Status: `DRAFT_REVIEW_READY`

Program owner: Codex supervisor/executor in the current conversation.

Claude role: read-only reviewer only. Claude may find consistency problems or
agree that a plan/result is internally safe, but Claude is not an execution
authority and cannot authorize human, runtime, model-file, funding,
product-capability, default-policy, or scientific-claim boundary crossings.

## Objective

Complete the remaining Zhao-Cui cells in the non-LEDH high-dimensional
leaderboard, excluding SGQF work now owned by another agent. The program fixes
or precisely blocks Zhao-Cui value and analytical-score gaps for:

- `zhao_cui_sv_actual_nongaussian_T1000`;
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`;
- `zhao_cui_spatial_sir_austria_j9_T20`;
- `zhao_cui_predator_prey_T20`;
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`.

The LGSSM Zhao-Cui exact-oracle row is retained as an already-admitted
baseline and is not a source-faithful Zhao-Cui TT/SIRT claim.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the remaining Zhao-Cui leaderboard cells be repaired into honest value plus manual analytical-score rows, or else blocked with exact evaluator/derivative gaps, without using autodiff as the admitted score? |
| Baseline/comparator | Current artifact `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`; current Markdown table `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`; prior Zhao-Cui source/derivative ledgers including P82/P83/P87/P91; Zhao-Cui author paper/source anchors only where source-faithfulness is claimed. |
| Primary pass criterion | Every Zhao-Cui row is either `executed_value_score` with finite value, finite manual analytical score, declared theta coordinates, same-scalar provenance, and no autodiff/tape admission, or is blocked with a precise missing target/evaluator/derivative item. Batch/GPU/XLA and score-at-true results are recorded as separate readiness/diagnostic statuses and do not silently decide row admission. |
| Veto diagnostics | `GradientTape`, `ForwardAccumulator`, `.gradient`, finite differences, or autodiff provenance admitted as analytical score; "source-faithful" without paper/source anchors; value-only row treated as gradient evidence; score row without free theta; local complete-data SIR component reported as full observed-data/filtering likelihood; SGQF/UKF work mixed into Zhao-Cui admission; GPU/XLA claim from non-trusted context; score-at-true treated as exact likelihood proof. |
| Explanatory diagnostics | FD consistency, centered-difference residuals, runtime, score norm, CPU-only smokes, trusted GPU/XLA compiles, and expected-score calibration explain behavior. For rows with simulator/truth support, expected-score calibration is a required implementation-consistency diagnostic and may veto scientific-consistency/readiness wording, but it does not prove exact likelihood correctness, posterior correctness, or production readiness. |
| Not concluded | No exact nonlinear likelihood correctness, posterior correctness, HMC convergence, universal GPU superiority, default-policy change, release readiness, or broad source-faithful adaptive Zhao-Cui reproduction unless separately gated and reviewed. |
| Artifacts | This master program, phase subplans/results, review ledger, visible execution ledger, visible overnight runbook, stop handoff, regenerated leaderboard JSON/Markdown, and final reset/release note if the program reaches closeout. |

## Owner Decisions Incorporated

- Actual leaderboard gradient cells must use analytical/manual score routes.
  Autodiff is diagnostic only.
- FD consistency is necessary engineering evidence but not a gradient oracle.
- Score-at-true consistency is the main high-dimensional implementation
  consistency diagnostic under the stated data-generation assumption: for data
  generated at true `theta_0`, average score over multiple seeds should be near
  zero under the reviewed uncertainty rule. It is not an exact-likelihood,
  posterior-correctness, or source-faithfulness proof.
- Solving `score(theta) = 0` is not a gate for high-dimensional Zhao-Cui.
- Hessian/information checks are optional future diagnostics.
- GPU/XLA JIT capability is required for HMC-facing production use, but CPU/GPU
  performance is model-specific. Lack of a trusted GPU/XLA result blocks only
  GPU/HMC-facing readiness wording, not the row's value/score admission.
- Batched value/score routes are required for production-facing rows. Lack of
  batched parity blocks production-facing readiness wording, not the row's
  value/score admission.

## Current Zhao-Cui Gaps

| Row | Current status | Completion work |
| --- | --- | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | Admitted exact-oracle affine adapter row. | Preserve as baseline; ensure no source-faithful TT overclaim. |
| `zhao_cui_sv_actual_nongaussian_T1000` | Value executes; score blocked because current provenance is autodiff. | Replace or precisely block with manual same-scalar analytical score. |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | Value executes; score blocked because current provenance is autodiff. | Replace or precisely block with manual same-scalar analytical score. |
| `zhao_cui_spatial_sir_austria_j9_T20` | P91 local complete-data component passed; full observed-data/filtering row remains blocked. | Build or block full filtering evaluator with previous-marginal and fixed-TTSIRT derivative ownership. |
| `zhao_cui_predator_prey_T20` | Model-specific evaluator adapter required. | Freeze T20 target and implement or block Zhao-Cui value/score adapter. |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | Exact source-row evaluator missing. | Freeze exact source-row target and implement or block Zhao-Cui value/score adapter. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Launch inventory and fail-closed Zhao-Cui contract | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase0-launch-inventory-subplan-2026-07-01.md` | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase0-launch-inventory-result-2026-07-01.md` |
| 1 | Actual-SV and KSC Zhao-Cui analytical score repair | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase1-sv-ksc-score-subplan-2026-07-01.md` | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase1-sv-ksc-score-result-2026-07-01.md` |
| 2 | Predator-prey T20 Zhao-Cui evaluator adapter | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase2-predator-prey-subplan-2026-07-01.md` | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase2-predator-prey-result-2026-07-01.md` |
| 3 | Generalized-SV exact source-row Zhao-Cui evaluator | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase3-generalized-sv-subplan-2026-07-01.md` | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase3-generalized-sv-result-2026-07-01.md` |
| 4 | Spatial SIR d18 full observed-data/filtering route | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase4-sir-full-filtering-subplan-2026-07-01.md` | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase4-sir-full-filtering-result-2026-07-01.md` |
| 5 | Batched, GPU/XLA, and score-at-true calibration ladder | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase5-batch-gpu-calibration-subplan-2026-07-01.md` | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase5-batch-gpu-calibration-result-2026-07-01.md` |
| 6 | Final leaderboard regeneration and closeout | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase6-final-regeneration-subplan-2026-07-01.md` | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase6-final-regeneration-result-2026-07-01.md` |

## Required Review Loop

1. Review this master program with Claude in read-only mode, bounded to this
   exact path first.
2. Review the visible overnight runbook and Phase 0 subplan before Phase 0
   execution.
3. Review every material phase subplan before execution.
4. At phase end, run local checks, write the phase result, draft or refresh the
   next subplan, and review the next subplan for consistency, correctness,
   feasibility, artifact coverage, and boundary safety.
5. If Claude finds a fixable issue, patch the same artifact visibly and rerun
   focused local checks.
6. Stop after five Claude review rounds for the same blocker and write a
   blocker result.

## Repair Attempt Bounds

Each implementation phase must fail closed instead of looping indefinitely.

- Before code edits, the phase must identify the exact target, theta
  coordinates, value scalar, derivative ownership, and artifact expected to
  answer the phase question.
- If that inventory cannot be stated, write the phase result as a precise
  blocker and advance or stop according to the phase handoff.
- After implementation starts, at most two focused code repair iterations are
  allowed for the same row/blocker before the phase must either:
  - record the row as admitted with passing focused checks; or
  - record a precise blocker in that phase result.
- Additional repair iterations are allowed only when a local check or Claude
  review identifies a narrow patch that does not change criteria after seeing
  results. Claude review still stops after five rounds for the same blocker.

## Approval And Trusted-Context Needs

The user has requested Claude read-only review for this program. Each Claude
call still runs through trusted/escalated sandbox execution because repo policy
requires trusted context for cross-agent work.

No extra human approval is anticipated for:

- document edits under `docs/plans`;
- CPU-only local checks with GPU hidden before framework import;
- bounded Claude read-only review;
- non-destructive source/test edits that are explicitly authorized by a
  reviewed phase subplan.

Human or explicit approval is still required for:

- package installation, network fetches, credentials, remote services, release
  tagging, CI-service mutation, or default-policy changes;
- destructive git/filesystem actions;
- treating a GPU/XLA result as evidence without trusted GPU execution;
- changing pass/fail criteria after seeing results.

## Skeptical Audit

Initial audit status: `PASSED_FOR_PLANNING_ONLY`.

Material risks incorporated into the plan:

- The leaderboard can look complete when value-only Zhao-Cui rows exist; score
  admission must be checked independently.
- Existing actual-SV/KSC Zhao-Cui scores are blocked because autodiff
  provenance is diagnostic only.
- P91 SIR d18 evidence is local complete-data component evidence, not a full
  observed-data/filtering leaderboard row.
- Predator-prey and generalized-SV gaps are target/evaluator gaps, not table
  formatting gaps.
- FD and score-at-true consistency are useful but must not become exact
  likelihood or posterior correctness claims.
- SGQF work is excluded here to avoid crossing into another agent's active
  lane.

## Artifact Map

| Artifact class | Exact path or rule |
| --- | --- |
| Master program | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-master-program-2026-07-01.md` |
| Visible runbook | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-visible-gated-overnight-execution-runbook-2026-07-01.md` |
| Claude review ledger | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-claude-review-ledger-2026-07-01.md` |
| Execution ledger | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-visible-execution-ledger-2026-07-01.md` |
| Stop handoff | `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-visible-stop-handoff-2026-07-01.md` |
| Phase blocker result | The phase result artifact listed in the Phase Index; if the whole program stops early, also update the stop handoff. |
| Final leaderboard JSON | `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`, or a later dated file only if Phase 6 explicitly records the supersession. |
| Final leaderboard Markdown | `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`, or a later dated file only if Phase 6 explicitly records the supersession. |
| Trusted GPU/XLA evidence | Phase 5 result plus row-specific manifests that state trusted/escalated context, device probe, framework probe, command, environment, and whether the result is a claim or a blocker. |
| Source-faithfulness evidence | Exact paper/source anchors in the phase result. If anchors are partial, missing, or conflicting, the row must be classified as a manual adapter/extension or precise blocker, not source-faithful. |

Execution begins only through
`docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-visible-gated-overnight-execution-runbook-2026-07-01.md`.
