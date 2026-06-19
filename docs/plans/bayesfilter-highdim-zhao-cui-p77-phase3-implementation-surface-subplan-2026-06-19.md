# P77 Phase 3 Subplan: Implementation Surface For Budgeted Training

metadata_date: 2026-06-19
status: DRAFT_READY_FOR_CLAUDE_GOVERNANCE_REREVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-result-2026-06-19.md
phase: 3
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Design and implement the scoped P77 runner and tests needed for budgeted
corrected-metric training diagnostics.

Phase 3 should not run a training-evidence command.  Its implementation surface
must make Phase 4 mechanics smokes and Phase 6 proper evidence runs possible
without changing defaults or reviving failed historical routes.

## Entry Conditions Inherited From Phase 2

Phase 3 may begin only if:

- Phase 2 result exists;
- Claude agrees Phase 2 execution/result and this Phase 3 subplan is adequate
  for execution;
- \(P_\theta=1656\), \(20P_\theta=33120\), and preferred first proper budget
  `1024 x 40 = 40960` are recorded for the current candidate;
- validation-only tuning/stopping/selection, replay role, and audit exclusion
  are frozen;
- random, calibrated-constant, and source-prefit remain failed historical
  routes only;
- this subplan has been reviewed by Claude after the P77 scoped-code-edit
  governance patch.

## Required Artifacts

Phase 3 must produce:

- Phase 3 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-result-2026-06-19.md`;
- scoped implementation diff, expected paths:
  `scripts/p77_budgeted_corrected_metric_training.py` and
  `tests/highdim/test_p77_budgeted_corrected_metric_training.py`;
- drafted Phase 4 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-subplan-2026-06-19.md`;
- updated P77 master program, runbook, execution ledger, Claude review ledger,
  and stop handoff.

## Required Checks/Tests/Reviews

Prechecks:

```bash
rg -n "PHASE2|P_theta|1656|33120|40960|learning-rate|validation-only|audit exclusion|failed historical routes" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-subplan-2026-06-19.md
rg -n "bounded_ukf_minibatch_pilot_payload|generated_corrected_metric_diagnostic_payload|P76CorrectedHeldoutMetricBatch|corrected_heldout_density_metric|train_step|make_adam_optimizer" scripts/p76_bounded_ukf_minibatch_pilot.py scripts/p76_generated_corrected_metric_diagnostic.py bayesfilter/highdim/stochastic_density_training.py
```

Focused checks must include at least:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p77_budgeted_corrected_metric_training.py tests/highdim/test_p77_budgeted_corrected_metric_training.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p77_budgeted_corrected_metric_training.py
```

Documentation checks:

```bash
rg -n "P_theta|parameter count|rank|degree|basis|trainable mask|recompute|1656|33120|40960|20P|budget arithmetic|evidence gate|non-evidence|mechanics smoke" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-subplan-2026-06-19.md
rg -n "learning rate|batch count|validation stopping|selection protocol|audit exclusion|replay veto|untrained UKF baseline|comparator|corrected validation CE|random|calibrated-constant|source-prefit" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-subplan-2026-06-19.md
git diff --check -- scripts/p77_budgeted_corrected_metric_training.py tests/highdim/test_p77_budgeted_corrected_metric_training.py docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-execution-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-claude-review-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-stop-handoff-2026-06-19.md
```

Review:

- Claude read-only review of Phase 3 result, implementation diff if any, and
  Phase 4 subplan.
- Repair loop to convergence within at most five rounds.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can P77 expose a scoped runner/test surface that enforces the Phase 2 budget/tuning contract before any evidence run? |
| Exact baseline/comparator | UKF-initialized untrained TT candidate evaluated with corrected validation/replay/audit CE under the same roles as trained candidates. |
| Primary criterion | The implementation surface records \(P_\theta\), budget gates, fresh-sample counts, learning-rate protocol, corrected validation/replay/audit metrics, untrained UKF baseline, failed-route fences, and nonclaims. |
| Veto diagnostics | Code edits outside the scoped P77 runner/test surface, training-evidence command, default change, under-budget evidence path, audit tuning, failed-route revival, missing budget/comparator fields, GPU/network/package use, or tests absent. |
| Explanatory only | Mechanics-smoke command shape, runtime estimates, P76 runner reuse details. |
| What will not be concluded | No training improvement, no proper evidence run, no final hyperparameter selection, no lower-gate repair, no validation/HMC readiness, no scaling. |
| Artifact preserving result | Phase 3 result, scoped diff/tests, and Phase 4 mechanics-smoke subplan. |

## Required Implementation Surface

The runner must:

- remain opt-in and CPU-only by default via `CUDA_VISIBLE_DEVICES=-1`;
- reuse the P76 UKF-frame bridge and UKF initializer route;
- start every candidate from the untrained UKF-initialized TT;
- expose batch size, batches, learning rate, degree, rank, output path, and
  max-seconds as explicit arguments;
- record \(P_\theta\), parameter count, rank, degree, basis, trainable mask,
  recompute status, budget arithmetic, evidence gate status, and
  `N_train_over_P_theta`;
- fail closed if a result is marked evidence while \(N_{\rm train}<20P_\theta\);
- allow under-budget mechanics smoke only with explicit non-evidence status;
- report untrained UKF baseline corrected validation CE, trained corrected
  validation CE, replay corrected CE, and final-only audit fields when allowed;
- preserve validation stopping and selection protocol fields, even if Phase 4
  mechanics smoke does not perform selection;
- record audit exclusion and replay veto/explanatory role;
- forbid random, calibrated-constant, and source-prefit live routes in code,
  tests, JSON, and result notes;
- emit nonclaims for source-faithfulness, lower-gate repair, HMC readiness,
  scaling, and default policy.

## Forbidden Claims/Actions

- Do not run a training-evidence command in Phase 3.
- Do not edit implementation code outside the scoped P77 runner/test surface.
- Do not use GPU/CUDA, network, package installs, detached agents, or default
  changes.
- Do not revive random, calibrated-constant, or source-prefit routes.
- Do not use audit for tuning, stopping, selection, or rescue.
- Do not claim training improvement, validation/HMC readiness, lower-gate
  repair, scaling, or source-faithful Zhao--Cui parity.

## Exact Next-Phase Handoff Conditions

Phase 4 may begin only if:

- Phase 3 result exists;
- Claude agrees Phase 3 execution/result;
- implementation and tests are passing, or Phase 3 closes with a blocker
  explaining why the scoped surface cannot be implemented safely;
- Phase 4 subplan exists and bounds a CPU-only non-evidence mechanics smoke;
- no training-evidence command or large run is required for Phase 4.

## Stop Conditions

Stop if:

- implementation edits would exceed the scoped P77 runner/test surface;
- code surface cannot enforce the \(20P_\theta\) evidence gate;
- untrained UKF baseline corrected CE cannot be reported;
- failed historical routes cannot remain fenced;
- audit exclusion cannot be represented;
- focused tests cannot be written or run within CPU-only bounds;
- Claude identifies a material blocker that cannot be repaired within five
  rounds.

## Skeptical Plan Audit

The main risk is accidentally turning an implementation phase into an evidence
run, or adding a runner that can silently mark under-budget smokes as evidence.
Phase 3 must make the runner fail closed and manifest-rich before any training
result is interpreted.
