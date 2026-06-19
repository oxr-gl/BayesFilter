# P77 Phase 4 Subplan: Tiny Training Mechanics Smoke

metadata_date: 2026-06-19
status: PHASE4_LOCAL_CHECKS_PASS_PENDING_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-result-2026-06-19.md
phase: 4
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Run a tiny CPU-only non-evidence mechanics smoke for the P77 runner.  The smoke
must prove that the runner can construct the UKF-frame context, apply the UKF
initializer, take a tiny number of optimizer steps, compute corrected
validation/replay CE, and write a manifest-rich JSON without crossing into
training evidence.

Phase 4 is not a proper training diagnostic.  It must not use the `1024 x 40`
budget, must not pass `--evidence-run`, and must not tune, select, promote, or
claim fit quality.

## Entry Conditions Inherited From Phase 3

Phase 4 may begin only if:

- Phase 3 result exists;
- Claude agrees Phase 3 execution/result and this Phase 4 subplan is adequate;
- `scripts/p77_budgeted_corrected_metric_training.py` exists;
- `tests/highdim/test_p77_budgeted_corrected_metric_training.py` exists and
  passes focused checks;
- Phase 4 is run CPU-only with `CUDA_VISIBLE_DEVICES=-1`;
- no training-evidence command, GPU/CUDA use, network/package operation,
  default change, detached agent, destructive action, or large diagnostic is
  required.

## Required Artifacts

Phase 4 must produce:

- mechanics-smoke JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-2026-06-19.json`;
- Phase 4 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-result-2026-06-19.md`;
- drafted Phase 5 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-subplan-2026-06-19.md`;
- updated P77 master program, runbook, execution ledger, Claude review ledger,
  and stop handoff.

## Required Checks/Tests/Reviews

Prechecks:

```bash
rg -n "PHASE3|P77 runner|20P|33120|40960|non-evidence|mechanics smoke|no training-evidence" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-subplan-2026-06-19.md
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p77_budgeted_corrected_metric_training.py tests/highdim/test_p77_budgeted_corrected_metric_training.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p77_budgeted_corrected_metric_training.py
```

Smoke command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p77_budgeted_corrected_metric_training.py --output docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-2026-06-19.json --degree 2 --rank 4 --batch-size 4 --batches 1 --learning-rate 0.001 --max-seconds 300 --seed 7704
```

The command intentionally omits `--evidence-run`.

Postchecks:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-2026-06-19.json
rg -n "\"non_evidence_mechanics_smoke\": true|\"evidence_run\": false|\"hard_budget_gate_passed\": false|\"P_theta\": 1656|\"minimum_training_samples\": 33120|\"N_train\": 4|\"audit_used_for_selection\": false|\"source_route_prefit_used\": false|\"default_behavior_changed\": false" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-2026-06-19.json
rg -n "P_theta|parameter count|rank|degree|basis|trainable mask|recompute|1656|33120|40960|20P|budget arithmetic|evidence gate|non-evidence|mechanics smoke" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-subplan-2026-06-19.md
rg -n "learning rate|batch count|validation stopping|selection protocol|audit exclusion|replay veto|untrained UKF baseline|comparator|corrected validation CE|random|calibrated-constant|source-prefit" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-subplan-2026-06-19.md
git diff --check -- scripts/p77_budgeted_corrected_metric_training.py tests/highdim/test_p77_budgeted_corrected_metric_training.py docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-execution-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-claude-review-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-stop-handoff-2026-06-19.md
```

Review:

- Claude read-only review of Phase 4 result and Phase 5 subplan.
- Repair loop to convergence within at most five rounds.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Does the P77 runner execute a tiny CPU-only mechanics smoke and preserve the non-evidence/budget/audit fences? |
| Exact baseline/comparator | UKF-initialized untrained TT baseline is reported by the runner, but the smoke is not a fit-quality comparison. |
| Primary criterion | The smoke JSON is written, parses, records `evidence_run=false`, `non_evidence_mechanics_smoke=true`, \(P_\theta=1656\), \(N_{\rm train}=4\), minimum samples 33120, corrected validation/replay metric fields, audit exclusion, failed-route fences, and no default change. |
| Veto diagnostics | `--evidence-run` used; \(N_{\rm train}\) treated as evidence; optimizer/metric nonfinite; bridge failure; seed overlap; audit used for selection; source-prefit/random/constant revival; GPU/CUDA/network/package/default/large-run action. |
| Explanatory only | Smoke CE values, training loss, gradient norm, runtime, TensorFlow warnings, and replay values. |
| What will not be concluded | No training improvement, no hyperparameter choice, no proper evidence run, no lower-gate repair, no validation/HMC readiness, no scaling. |
| Artifact preserving result | Phase 4 JSON, Phase 4 result, and Phase 5 budgeted-training design subplan. |

## Forbidden Claims/Actions

- Do not pass `--evidence-run`.
- Do not run `1024 x 40` or any proper evidence command.
- Do not use GPU/CUDA, network, package installs, detached agents, destructive
  actions, default changes, or large diagnostics.
- Do not tune, select, stop, or promote based on smoke CE values.
- Do not use audit for tuning, selection, stopping, or rescue.
- Do not revive random, calibrated-constant, or source-prefit routes.
- Do not claim training improvement, lower-gate repair, validation/HMC
  readiness, scaling, or source-faithful Zhao--Cui parity.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin only if:

- Phase 4 result exists;
- Claude agrees Phase 4 execution/result;
- Phase 5 subplan exists and designs the proper budgeted training diagnostic
  without executing it;
- no `1024 x 40` run, GPU/CUDA use, network/package operation, default change,
  destructive action, detached agent, or large diagnostic is required to begin
  Phase 5.

## Stop Conditions

Stop if:

- the smoke would require `--evidence-run`;
- the smoke would exceed tiny non-evidence bounds;
- the runner cannot construct the UKF-frame context within the reviewed CPU-only
  bounds;
- metric or training quantities are nonfinite;
- the smoke JSON omits budget/evidence/audit/failure-route fences;
- the result would be interpreted as fit-quality evidence;
- Claude identifies a material blocker that cannot be repaired within five
  rounds.

## Skeptical Plan Audit

The main risk is treating a tiny smoke as evidence.  Phase 4 blocks that by
omitting `--evidence-run`, requiring `N_train=4` to be recorded as under the
33120 hard minimum, and using the output only to validate wiring and manifests.
