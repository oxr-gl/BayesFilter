# BayesFilter leaderboard repair master program

Date: 2026-06-30

Status: `DRAFT_REVIEW_READY`

Program owner: Codex supervisor/executor in the current conversation.

Claude role: read-only reviewer only. Claude may agree or request revision, but cannot authorize crossing human, runtime, model-file, funding, product-capability, or scientific-claim boundaries.

## Objective

Repair the non-LEDH high-dimensional leaderboard so SGQF, Zhao-Cui, UKF, CUT4, and exact/reference rows are reported under one honest value/score contract. The program fixes stale blockers, missing adapters, and invalid gradient claims one by one, then regenerates the leaderboard with explicit target, theta, score, batch, CPU, and GPU/XLA statuses.

LEDH/PFPF-OT/DPF rows remain omitted from this leaderboard program unless a later reviewed plan explicitly reopens them.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the current leaderboard blockers be repaired into honest value and analytical-score cells without reviving stale target mistakes or unsupported production claims? |
| Baseline/comparator | Current artifacts `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`, `docs/plans/bayesfilter-two-lane-lowdim-leaderboard-results-2026-06-30.json`, corrected actual-SV note `docs/plans/bayesfilter-highdim-actual-sv-single-target-corrected-derivation-note-2026-06-29.md`, P91 SIR d18 artifacts `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-result-2026-06-29.md`, `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-manifest-2026-06-29.json`, `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-manifest-2026-06-29.json`, and exact/Kalman references only where the model row is actually affine/Gaussian. |
| Primary pass criterion | Every final leaderboard cell is either executed with finite value and correctly classified analytical score provenance, or explicitly blocked with a specific next implementation gap. |
| Veto diagnostics | `GradientTape`/autodiff provenance in a cell claiming analytical score; stale `blocked_not_same_target` for corrected direct actual-SV SGQF route; a score row without declared free `theta`; source-faithfulness claim without Zhao-Cui paper/source anchors; GPU/XLA claim from non-trusted GPU context; value-only row treated as gradient evidence. |
| Explanatory diagnostics | FD checks, short smokes, timing, validation loss, CPU-only checks, and multi-replicate expected-score calibration probes explain implementation status but do not alone prove production readiness. |
| Not concluded | No exact nonlinear likelihood claim unless separately proved; no posterior/HMC convergence claim from leaderboard values; no GPU production performance claim from CPU-only artifacts; no broad SGQF/Zhao-Cui source-faithfulness claim beyond cited source scope. |
| Artifacts | This master program; phase subplans/results listed below; Claude review ledger `docs/plans/bayesfilter-leaderboard-repair-claude-review-ledger-2026-06-30.md`; visible execution ledger `docs/plans/bayesfilter-leaderboard-repair-visible-execution-ledger-2026-06-30.md`; visible runbook `docs/plans/bayesfilter-leaderboard-repair-visible-gated-execution-runbook-2026-06-30.md`; regenerated JSON/Markdown leaderboard; final reset memo; and final stop handoff `docs/plans/bayesfilter-leaderboard-repair-visible-stop-handoff-2026-06-30.md`. |

## Current Known Issues

| Issue | Current evidence | Repair class |
| --- | --- | --- |
| SGQF actual SV T1000 still says `blocked_not_same_target` | Corrected derivation note says direct transformed-SV SGQF is same-target; leaderboard emitter still hardcodes stale block. | Stale label plus missing leaderboard value wiring. |
| SGQF actual SV score uses `GradientTape` route | `bayesfilter/highdim/sv_mixture_cut4.py` documents `GradientTape score` for direct actual-SV SGQF score. | Real analytical-derivative implementation gap. |
| Zhao-Cui LGSSM m3 T50 blocked | P8D artifact reports `P8D_MODEL_SPECIFIC_NUMERIC_EVALUATOR_ADAPTER_REQUIRED`. | Missing evaluator adapter. |
| SGQF predator-prey score blocked | Value route exists; current derivative adapter uses TensorFlow tape internally. | Real analytical-derivative implementation gap. |
| Zhao-Cui predator-prey blocked | No source-scope evaluator adapter in the current highdim leaderboard emitter. | Missing evaluator adapter. |
| SIR d18 row is not a full observed-data leaderboard likelihood | P91 closed scoped local complete-data component only. | Parameterized observed-data row and evaluator required. |
| Generalized SV rows blocked | No reviewed same-target leaderboard evaluator for SGQF or Zhao-Cui in this table. | Target contract plus evaluator work. |
| Batch/GPU/XLA status missing from final leaderboard shape | Current two-lane artifact is CPU/status focused. | Benchmark and schema extension. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Contract audit and fail-closed schema | `docs/plans/bayesfilter-leaderboard-repair-phase0-contract-audit-subplan-2026-06-30.md` | `docs/plans/bayesfilter-leaderboard-repair-phase0-contract-audit-result-2026-06-30.md` |
| 1 | Actual-SV SGQF same-target value row | `docs/plans/bayesfilter-leaderboard-repair-phase1-actual-sv-sgqf-value-subplan-2026-06-30.md` | `docs/plans/bayesfilter-leaderboard-repair-phase1-actual-sv-sgqf-value-result-2026-06-30.md` |
| 2 | Actual-SV SGQF strict analytical score | `docs/plans/bayesfilter-leaderboard-repair-phase2-actual-sv-sgqf-score-subplan-2026-06-30.md` | `docs/plans/bayesfilter-leaderboard-repair-phase2-actual-sv-sgqf-score-result-2026-06-30.md` |
| 3 | Zhao-Cui LGSSM m3 evaluator adapter | `docs/plans/bayesfilter-leaderboard-repair-phase3-zhaocui-lgssm-adapter-subplan-2026-06-30.md` | `docs/plans/bayesfilter-leaderboard-repair-phase3-zhaocui-lgssm-adapter-result-2026-06-30.md` |
| 4 | Predator-prey SGQF/Zhao-Cui cells | `docs/plans/bayesfilter-leaderboard-repair-phase4-predator-prey-cells-subplan-2026-06-30.md` | `docs/plans/bayesfilter-leaderboard-repair-phase4-predator-prey-cells-result-2026-06-30.md` |
| 5 | Spatial SIR d18 parameterized observed-data row | `docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-subplan-2026-06-30.md` | `docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-result-2026-06-30.md` |
| 6 | Generalized SV target/evaluator repair | `docs/plans/bayesfilter-leaderboard-repair-phase6-generalized-sv-subplan-2026-06-30.md` | `docs/plans/bayesfilter-leaderboard-repair-phase6-generalized-sv-result-2026-06-30.md` |
| 7 | Batched CPU/GPU/XLA benchmarking | `docs/plans/bayesfilter-leaderboard-repair-phase7-batch-gpu-xla-subplan-2026-06-30.md` | `docs/plans/bayesfilter-leaderboard-repair-phase7-batch-gpu-xla-result-2026-06-30.md` |
| 8 | Final regeneration and release note | `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-subplan-2026-06-30.md` | `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-result-2026-06-30.md` |

## Required Review Loop

1. Review the master program with Claude in read-only mode, bounded to this exact file first.
2. Review each material subplan before executing the phase. For implementation phases, review the subplan first and the result/diff after execution.
3. If Claude requests a fixable revision, patch the same artifact visibly and rerun focused local checks.
4. Stop after five Claude review rounds for the same blocker and write a blocker result.
5. Claude agreement is a consistency review, not execution authority.

## Approval And Trusted-Context Needs

Execution-context rules:

- Any command that imports TensorFlow/JAX/PyTorch/CuPy or otherwise might detect, initialize, benchmark, or use GPU/CUDA/NVIDIA devices must either:
  - force CPU-only execution before framework import, e.g. `CUDA_VISIBLE_DEVICES=-1`, and record that CPU-only choice in the artifact; or
  - run in trusted/escalated context before any GPU/XLA claim is made.
- Non-escalated GPU/CUDA failures are sandbox evidence only and cannot be used to conclude the GPU stack is broken.
- GPU/XLA benchmark phases must start with trusted GPU device and framework probes.

Anticipated trusted commands:

- Claude read-only reviews using this bounded visible form:
  `claude -p --model opus --effort max --tools Read --permission-mode dontAsk '<bounded one-path read-only review prompt>'`.
- GPU/XLA phases using escalated GPU/CUDA commands per repo policy.
- Possible `git add`, `git commit`, `git push` only if the user explicitly asks after results.

No package installation, network data fetch, detached supervisor, copied workspace, destructive git operation, or default policy change is authorized by this master program.

## Phase Gate Summary

| Gate | Must be true to advance |
| --- | --- |
| Phase 0 to 1 | Validator and schema contract distinguish value-only, analytical-score, autodiff-diagnostic, and blocked cells. |
| Phase 1 to 2 | Actual-SV direct SGQF value row is same-target and value-only, with stale `not_same_target` removed. |
| Phase 2 to 3 | Actual-SV SGQF score is either strict analytical and tested, or explicitly remains value-only with no gradient claim. |
| Phase 3 to 4 | Zhao-Cui LGSSM m3 row has finite same-target value plus correctly classified analytical-score status, value-only status, or a precise adapter blocker. |
| Phase 4 to 5 | Predator-prey SGQF/Zhao-Cui cells are either value+analytical-score or honestly value-only/blocked. |
| Phase 5 to 6 | SIR d18 row exposes a real parameterized observed-data likelihood contract and does not confuse complete-data component evidence with full filtering. |
| Phase 6 to 7 | Generalized SV cells have a reviewed target/evaluator status and no unsupported same-target claim. |
| Phase 7 to 8 | Batch and GPU/XLA results are recorded only from trusted GPU context and benchmarked per model. |
| Phase 8 close | Final JSON leaderboard, final Markdown leaderboard, reset/release note, nonclaims recorded in both `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md` and `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-result-2026-06-30.md`, final review trail in `docs/plans/bayesfilter-leaderboard-repair-claude-review-ledger-2026-06-30.md`, and stop handoff are internally consistent and reviewed. |

## Skeptical Audit

Initial audit status: `PASSED_FOR_PLANNING_ONLY`.

Material risks found and incorporated:

- The old SGQF actual-SV `not_same_target` blocker is stale after the corrected derivation note.
- Direct actual-SV SGQF score is not strict analytical while it uses `GradientTape`.
- SIR d18 cannot be a score row unless a free parameter vector and observed-data likelihood are declared.
- FD consistency is necessary but not sufficient; multi-replicate expected-score calibration checks whether the mean score at the true parameter is near zero within uncertainty, and is a high-dimensional consistency diagnostic rather than a per-dataset zero-score requirement.
- GPU/XLA performance must be model-specific and trusted-context, not inferred from CPU-only runs.

If a phase cannot establish same-target value validity or analytical-score validity, the cell must close as blocked or value-only with a precise reason. The program may continue only if downstream artifacts can represent that status without ambiguity.

## Final Required Output Artifacts

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-claude-review-ledger-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-visible-execution-ledger-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-visible-gated-execution-runbook-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-result-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-reset-memo-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-visible-stop-handoff-2026-06-30.md`

Execution begins only through `docs/plans/bayesfilter-leaderboard-repair-visible-gated-execution-runbook-2026-06-30.md` and the phase subplans listed in this master program.
