# P77 Phase 4 Result: Tiny Training Mechanics Smoke

metadata_date: 2026-06-19
status: PHASE4_CLAUDE_AGREE_READY_FOR_PHASE5_DESIGN
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-subplan-2026-06-19.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-result-2026-06-19.md
phase: 4
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Summary

Phase 4 ran the P77 runner on a tiny CPU-only non-evidence mechanics smoke.
The command constructed the UKF-frame target context, applied the UKF
initializer, completed one optimizer step, computed corrected validation and
replay CE for the untrained UKF baseline and trained candidate, and wrote the
manifest-rich JSON artifact.

This is not a training-evidence result.  The smoke used \(N_{\rm train}=4\)
fresh training samples, far below the hard evidence minimum
\(20P_\theta=33120\).  The output explicitly records
`evidence_run=false`, `hard_budget_gate_passed=false`,
`non_evidence_mechanics_smoke=true`, `fit_quality_claim_permitted=false`, and
`validation_improved_for_selection=null`.

## Smoke Command

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p77_budgeted_corrected_metric_training.py --output docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-2026-06-19.json --degree 2 --rank 4 --batch-size 4 --batches 1 --learning-rate 0.001 --max-seconds 300 --seed 7704
```

The command intentionally omitted `--evidence-run`.

Output artifact:

- `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-2026-06-19.json`

Runtime manifest highlights:

- CPU-only intent: `CUDA_VISIBLE_DEVICES=-1`;
- TensorFlow version: `2.19.1`;
- git head: `9bcad31f0d9b21731b3915083d86834b43730f51`;
- dirty worktree: true;
- elapsed seconds recorded in JSON: `1.354`.

TensorFlow printed CUDA plugin/cuInit warnings despite
`CUDA_VISIBLE_DEVICES=-1`.  The JSON records `cpu_only=true` and
`cuda_visible_devices="-1"`.  Under the local GPU/CUDA sandbox policy this is
CPU-hidden environment noise for this deliberate CPU-only run, not evidence of
GPU execution.

## Phase 4 Manifest Result

The smoke JSON records:

- status: `P77_BUDGETED_CORRECTED_METRIC_TRAINING_COMPLETED`;
- \(P_\theta=1656\);
- `minimum_training_samples=33120`;
- preferred first proper budget: `1024 x 40 = 40960`;
- `batch_size=4`, `batches=1`, `N_train=4`;
- `N_train_over_P_theta=0.0024154589371980675`;
- `hard_budget_gate_passed=false`;
- `evidence_run=false`;
- `non_evidence_mechanics_smoke=true`;
- `completed_batches=1`;
- `training_started=true`;
- `optimizer_constructed=true`;
- `source_route_prefit_used=false`;
- `default_behavior_changed=false`;
- `audit_used_for_selection=false`;
- `audit_evaluated=false`;
- failed historical route fence present for random, calibrated-constant, and
  source-route prefit routes.

The UKF-frame bridge passed:

- bridge status: `pass`;
- target dimension: `36`;
- frame dimension: `36`;
- product-basis dimension: `36`;
- reconstruction max absolute error: `6.22052119162378e-15`;
- target tieout max absolute error: `0.0`;
- training and audit clip fractions: `0.0`.

The runtime trainable parameter count matched the formula:

- `trainable_variable_count_runtime=1656`;
- `runtime_count_matches_formula=true`.

## Metric Result

The corrected validation CE values in the smoke JSON are:

- untrained UKF baseline corrected validation CE:
  `-24.560392210531344`;
- trained corrected validation CE after one tiny smoke step:
  `-24.574272643112636`;
- absolute CE change trained minus baseline:
  `-0.013880432581292013`;
- relative CE change:
  `-0.0005651551678128401`.

These values are explanatory only.  They do not imply training success,
promotion, tuning, lower-gate repair, validation/HMC readiness, scaling, or a
rank/sample policy because \(N_{\rm train}=4\ll33120\).

To prevent overclaim, Phase 4 repaired the P77 runner manifest after the first
smoke attempt.  The initial smoke output contained a bare
`validation_improved=true` field.  That was a governance bug because an
under-budget mechanics smoke could be misread as a fit-quality claim.  The
runner and focused tests were patched so non-evidence runs now record:

- `validation_improvement_observed_explanatory_only=true`;
- `fit_quality_claim_permitted=false`;
- `validation_improved_for_selection=null`;
- `non_evidence_smoke_no_fit_quality_claim=true`.

The smoke JSON was regenerated after this repair.

Replay CE values were finite and explanatory:

- replay baseline CE: `-21.065180391491175`;
- replay trained CE: `-21.08006762002332`.

Replay is not a selection metric in Phase 4.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | Does the P77 runner execute a tiny CPU-only mechanics smoke and preserve the non-evidence/budget/audit fences? |
| Exact baseline/comparator | UKF-initialized untrained TT baseline is reported by the runner, but the smoke is not a fit-quality comparison. |
| Primary criterion | Passed locally pending Claude review: JSON written and parsed; it records `evidence_run=false`, `non_evidence_mechanics_smoke=true`, \(P_\theta=1656\), \(N_{\rm train}=4\), minimum 33120, corrected validation/replay fields, audit exclusion, failed-route fences, and no default change. |
| Veto diagnostics | No `--evidence-run`; no `1024 x 40`; no GPU/CUDA command; no network/package/default/destructive/detached action; metrics finite; bridge passed; audit excluded; failed routes fenced; smoke CE cannot promote. |
| Explanatory only | Smoke CE values, one-step training loss, gradient norm, replay values, runtime, and TensorFlow CUDA plugin/cuInit warnings under CPU-hidden execution. |
| What will not be concluded | No training improvement, no hyperparameter choice, no proper evidence run, no lower-gate repair, no validation/HMC readiness, no scaling. |
| Artifact preserving result | This Phase 4 result, the smoke JSON, and the Phase 5 budgeted-training design subplan. |

## Local Checks

Prechecks:

```bash
rg -n "PHASE3|P77 runner|20P|33120|40960|non-evidence|mechanics smoke|no training-evidence" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-subplan-2026-06-19.md
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p77_budgeted_corrected_metric_training.py tests/highdim/test_p77_budgeted_corrected_metric_training.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p77_budgeted_corrected_metric_training.py
```

Results:

- precheck grep passed;
- compileall passed;
- focused pytest passed after the manifest-labeling and future evidence-veto
  repairs: `8 passed, 2 warnings`;
- warnings were TensorFlow Probability `distutils` deprecation warnings.

Smoke/postchecks:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-2026-06-19.json
rg -n '"non_evidence_mechanics_smoke": true|"evidence_run": false|"hard_budget_gate_passed": false|"P_theta": 1656|"minimum_training_samples": 33120|"N_train": 4|"audit_used_for_selection": false|"source_route_prefit_used": false|"default_behavior_changed": false|"fit_quality_claim_permitted": false|"validation_improved_for_selection": null|"non_evidence_smoke_no_fit_quality_claim": true|"validation_improvement_observed_explanatory_only"' docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-2026-06-19.json
git diff --check -- scripts/p77_budgeted_corrected_metric_training.py tests/highdim/test_p77_budgeted_corrected_metric_training.py docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-2026-06-19.json docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-execution-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-claude-review-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-stop-handoff-2026-06-19.md
```

Results:

- JSON parsed;
- required evidence/budget/audit/failure-route/nonclaim fields were present;
- `git diff --check` passed for the touched Phase 4 files before this result
  note was written.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 4 pending Claude review | Local mechanics and manifest checks pass after one manifest-labeling repair | No Phase 4 veto remains active | Proper budgeted training has not been run and the one-step CE change is explanatory only | Claude review Phase 4 result and Phase 5 design subplan | No training improvement, no hyperparameter choice, no evidence run, no lower-gate repair, no validation/HMC readiness |

## Phase 5 Handoff

Phase 5 should be design-only.  It should freeze the exact proper budgeted
training diagnostic command(s), learning-rate handling, pass/fail rule,
replay/audit use, runtime bounds, and approval boundary for Phase 6.  Phase 5
must not launch the `1024 x 40` evidence run.

Claude execution review:

- `p77-phase4-execution-review-r1`: `VERDICT: BLOCK`.
- R1 blocker was stale current-gate bookkeeping: Phase 4 still recorded
  `7 passed, 2 warnings` after the future evidence-veto repair added an eighth
  focused test.
- Patched the Phase 4 result, execution ledger, and stop handoff to record
  `8 passed, 2 warnings`; reran focused pytest and `git diff --check`.
- `p77-phase4-execution-review-r2`: `VERDICT: AGREE`.
- Claude agreed Phase 4 may close and Phase 5 may proceed as design-only.
