# P77 Phase 5 Result: Proper Budgeted Training Diagnostic Design

metadata_date: 2026-06-19
status: PHASE5_CLAUDE_AGREE_STOP_FOR_PHASE6_EVIDENCE_APPROVAL
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-subplan-2026-06-19.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-result-2026-06-19.md
phase: 5
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Summary

Phase 5 freezes the first proper P77 budgeted corrected-metric training
diagnostic design.  It is design-only: no `--evidence-run` command was
launched, no `1024 x 40` training run was launched, no GPU/CUDA command was
used, and no network/package/default/destructive/detached action occurred.

The first proper Phase 6 diagnostic will use one learning-rate candidate:

\[
  \eta = 10^{-3}.
\]

This is the current configured default and was already in the predeclared
Phase 2 set \(\{10^{-4},3\cdot10^{-4},10^{-3}\}\).  The choice is not based
on the Phase 4 smoke CE movement.  The reason is conservative cost control:
the first evidence question is whether the existing UKF-warm-started
mini-batch training path works at the required \(20P_\theta\) budget.  A
three-rate ladder would be a later tuning diagnostic and would triple the
first evidence cost before we know whether the basic path is viable.

## Frozen Phase 6 Command

Phase 6 must not launch until the user explicitly approves it after Claude
reviews this result and the Phase 6 subplan.

Exact command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p77_budgeted_corrected_metric_training.py --output docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-lr1e-3-2026-06-19.json --degree 2 --rank 4 --batch-size 1024 --batches 40 --learning-rate 0.001 --max-seconds 7200 --seed 7706 --evidence-run
```

Frozen settings:

- `degree=2`;
- `rank=4`;
- `batch_size=1024`;
- `batches=40`;
- \(N_{\rm train}=40960\);
- \(P_\theta=1656\);
- minimum evidence samples: \(20P_\theta=33120\);
- learning rate: `0.001`;
- seed: `7706`;
- CPU-only: `CUDA_VISIBLE_DEVICES=-1`;
- wall-clock cap: `7200` seconds;
- output:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-lr1e-3-2026-06-19.json`.

If the wall-clock cap stops the runner before 40 completed batches, Phase 6
must report a blocked or incomplete result and must not claim training
evidence.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | Can the existing UKF-warm-started P77 training path improve corrected validation CE against the untrained UKF baseline under \(N_{\rm train}=40960\ge33120\) fresh training samples? |
| Exact baseline/comparator | UKF-initialized untrained TT baseline evaluated by the same corrected validation and replay CE roles as the trained candidate. |
| Primary criterion | Phase 6 passes only if the exact command records `evidence_run=true`, `hard_budget_gate_passed=true`, `N_train=40960`, `fit_quality_claim_permitted=true`, no veto blockers, and `validation_improved_for_selection=true` against the untrained UKF baseline. |
| Veto diagnostics | Incomplete batch count, under-budget evidence, nonfinite training or metric values, bridge/tieout failure, CE reconstruction mismatch, corrected alpha mass failure, seed overlap, audit selection/tuning, failed-route revival, default/GPU/network/package/destructive/detached action, or validation not improved against the untrained UKF baseline. |
| Explanatory only | Training loss, gradient norm, rho range, normalizer, replay CE values after finite/reconstruction/alpha/role checks, runtime, TensorFlow warnings, and Phase 4 smoke CE movement. |
| What will not be concluded | No source-faithful Zhao--Cui claim, no final audit claim, no lower-gate repair, no validation/HMC readiness, no scaling, no default policy, no final rank/sample/learning-rate policy. |
| Artifact preserving result | This Phase 5 result and the Phase 6 budgeted-training diagnostic subplan. |

## Pass And Veto Rules For Phase 6

Phase 6 can pass only if all of the following are true in the JSON and result
note:

- `status` is `P77_BUDGETED_CORRECTED_METRIC_TRAINING_COMPLETED`;
- `evidence_run=true`;
- `hard_budget_gate_passed=true`;
- `P_theta=1656`;
- `minimum_training_samples=33120`;
- `N_train=40960`;
- `completed_batches=40`;
- `completed_training_samples=40960`;
- `fit_quality_claim_permitted=true`;
- `validation_improved_for_selection=true`;
- `gate_summary.blockers` is empty;
- UKF-frame bridge status is `pass`;
- corrected validation CE for the trained candidate is lower than corrected
  validation CE for the untrained UKF baseline;
- validation and replay metric finite flags, CE reconstruction checks, and
  corrected alpha mass checks pass;
- `audit_used_for_selection=false`;
- `source_route_prefit_used=false`;
- `default_behavior_changed=false`;
- failed historical route fence remains present.

Phase 6 must block, not pass, if validation does not improve against the
untrained UKF baseline.  The runner now includes the explicit blocker
`validation_not_improved_against_untrained_ukf_baseline` for budget-passing
evidence runs that fail this validation rule.

## Replay And Audit Boundary

Replay is not a selector in Phase 6.  It may veto only for:

- nonfinite CE or other metric quantities;
- CE reconstruction mismatch;
- corrected alpha mass failure;
- wrong role or provenance.

No numeric severe-degradation replay threshold is frozen in Phase 5; replay CE
differences are otherwise explanatory.

The current P77 runner does not evaluate a separate final audit cloud.  Phase
6 therefore makes no final audit claim.  Audit remains excluded from training,
stopping, tuning, and selection; `audit_used_for_selection=false` is required.
A later phase may design final-audit evaluation, but it must not reinterpret
Phase 6 as audit evidence retroactively.

## Learning-Rate Boundary

The Phase 6 run uses only `learning-rate=0.001`.  The other predeclared Phase 2
candidates, `0.0001` and `0.0003`, remain available for a later reviewed
tuning phase only if Phase 6 fails, blocks, or returns a result that justifies
learning-rate diagnosis.  They are not silently part of Phase 6.

## Local Checks

Phase 5 prechecks:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-2026-06-19.json
rg -n '"non_evidence_mechanics_smoke": true|"evidence_run": false|"hard_budget_gate_passed": false|"fit_quality_claim_permitted": false|"validation_improved_for_selection": null|"P_theta": 1656|"minimum_training_samples": 33120|"N_train": 4' docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-2026-06-19.json
rg -n "P_theta|1656|33120|40960|learning rate|validation-only|audit exclusion|replay|untrained UKF baseline|failed historical routes" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-result-2026-06-19.md
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p77_budgeted_corrected_metric_training.py tests/highdim/test_p77_budgeted_corrected_metric_training.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p77_budgeted_corrected_metric_training.py
```

Results:

- Phase 4 JSON parsed.
- Phase 4 non-evidence/budget/claim-fence fields were present.
- Phase 2 and Phase 4 source-result terms were present.
- Compileall passed.
- Focused pytest passed after the incomplete-evidence-run veto repair:
  `9 passed, 2 warnings`.

Documentation checks:

```bash
rg -n "1024 x 40|40960|33120|20P|evidence-run|--evidence-run|learning-rate|0.0001|0.0003|0.001|validation-only|audit final|replay|approval" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-subplan-2026-06-19.md
rg -n "primary criterion|veto diagnostics|explanatory only|not concluded|non-evidence|fit_quality_claim_permitted|validation_improved_for_selection|untrained UKF baseline" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-subplan-2026-06-19.md
git diff --check -- scripts/p77_budgeted_corrected_metric_training.py tests/highdim/test_p77_budgeted_corrected_metric_training.py docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-execution-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-claude-review-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-stop-handoff-2026-06-19.md
```

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Freeze single-candidate Phase 6 evidence design at `learning-rate=0.001` | Pending local docs checks and Claude review | No evidence command launched in Phase 5 | CPU runtime and actual validation behavior remain unknown until approved Phase 6 | Claude review this result and Phase 6 subplan, then request explicit human approval for Phase 6 evidence | No training improvement, no final learning-rate policy, no audit claim, no lower-gate repair |

## Phase 6 Handoff

Phase 6 may launch only after Claude agrees this Phase 5 result and the Phase
6 subplan, and after the user explicitly approves the exact Phase 6 evidence
command.  Without that approval, stop at Phase 5 closure.

## R1 Review Repair Note

Claude Phase 5 review R1 found that the runner did not yet enforce the
documented requirement that an evidence run complete all requested batches.
The runner and focused tests were patched so evidence runs now block on
`incomplete_batch_count` unless `completed_batches == requested_batches`; the
blocked-payload path also records `all_requested_batches_completed=false`.

Claude execution review:

- `p77-phase5-execution-review-r1`: `VERDICT: BLOCK`.
- `p77-phase5-execution-review-r2`: `VERDICT: AGREE`.
- Claude agreed the incomplete-batch evidence veto blocker is repaired and
  Phase 5 may close.
