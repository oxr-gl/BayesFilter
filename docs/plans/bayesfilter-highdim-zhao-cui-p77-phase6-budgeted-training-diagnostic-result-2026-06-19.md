# P77 Phase 6 Result: Budgeted Corrected-Metric Training Diagnostic

metadata_date: 2026-06-20
status: PHASE6_CLAUDE_AGREE_READY_FOR_PHASE7_DECISION
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-subplan-2026-06-19.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-result-2026-06-19.md
phase: 6
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Summary

Phase 6 launched the exact reviewed CPU-only evidence command after user
approval.  The run completed all requested `1024 x 40` fresh mini-batches and
passed the Phase 6 primary validation criterion against the untrained
UKF-initialized baseline.

The result is a positive budgeted diagnostic for the current P77 training path,
not a final scientific or product claim.  It does not establish source-faithful
Zhao--Cui behavior, final audit validity, lower-gate repair, HMC readiness,
scaling behavior, default policy, or final rank/sample/learning-rate policy.

## Command Actually Run

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p77_budgeted_corrected_metric_training.py --output docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-lr1e-3-2026-06-19.json --degree 2 --rank 4 --batch-size 1024 --batches 40 --learning-rate 0.001 --max-seconds 7200 --seed 7706 --evidence-run
```

Artifact:

- `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-lr1e-3-2026-06-19.json`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | Does the UKF-warm-started P77 runner improve corrected validation CE against the untrained UKF baseline under \(N_{\rm train}=40960\ge33120\)? |
| Exact baseline/comparator | UKF-initialized untrained TT baseline, same corrected validation role as the trained candidate. |
| Primary criterion | Passed.  The run completed 40/40 batches, recorded `evidence_run=true`, `hard_budget_gate_passed=true`, `fit_quality_claim_permitted=true`, empty blockers, and `validation_improved_for_selection=true`. |
| Veto diagnostics | Passed for this phase.  No incomplete-batch, under-budget, nonfinite, bridge/tieout, seed-overlap, audit-selection, failed-route-revival, default-change, GPU, network, destructive, detached, or command-mismatch blocker was recorded. |
| Explanatory only | Training loss, gradient norm, rho range, normalizer, replay CE values after validity checks, runtime, TensorFlow startup warnings, and Phase 4 smoke CE. |
| What is not concluded | No source-faithful Zhao--Cui claim, no final audit claim, no lower-gate repair, no validation/HMC readiness, no scaling, no default policy, no final rank/sample/learning-rate policy. |
| Artifact preserving result | This Phase 6 result, the Phase 6 JSON, and the Phase 7 decision-boundary subplan. |

## Key Numbers

| Quantity | Value |
| --- | --- |
| \(P_\theta\) | `1656` |
| Required samples | `33120 = 20 * P_theta` |
| Actual training samples | `40960` |
| Samples per parameter | `24.734299516908212` |
| Batch size | `1024` |
| Requested batches | `40` |
| Completed batches | `40` |
| Learning rate | `0.001` |
| Degree/rank | `2 / 4` |
| CPU-only flag | `CUDA_VISIBLE_DEVICES=-1` |
| Wall time recorded by runner | `14.989` seconds |

## Validation Result

The corrected validation CE improved against the untrained UKF baseline:

| Metric | Value |
| --- | --- |
| Untrained UKF baseline corrected validation CE | `-23.797689401261703` |
| Trained corrected validation CE | `-24.339592237328375` |
| Trained minus baseline | `-0.5419028360666722` |
| Relative CE change | `-0.02277123744786507` |
| `validation_improved_for_selection` | `true` |

The Phase 6 selection rule treats lower corrected validation CE as better.
Under that rule, this run passed the validation gate.

## Gate Summary

The JSON recorded:

- `status=P77_BUDGETED_CORRECTED_METRIC_TRAINING_COMPLETED`;
- `gate_summary.overall_status=pass`;
- `gate_summary.blockers=[]`;
- `evidence_run=true`;
- `hard_budget_gate_passed=true`;
- `fit_quality_claim_permitted=true`;
- `all_requested_batches_completed=true`;
- `completed_training_samples=40960`;
- `validation_improvement_observed_explanatory_only=false`;
- `audit_used_for_selection=false`;
- `source_route_prefit_used=false`;
- `default_behavior_changed=false`.

## Bridge, Seeds, And Numerical Diagnostics

UKF-frame bridge:

- `status=pass`;
- `blockers=[]`;
- `dimension_match=true`;
- `training_target_values_finite=true`;
- `audit_target_values_finite=true`;
- `reconstruction_max_abs_error=6.22052119162378e-15`;
- `target_tieout_max_abs_error=0.0`;
- `training_clip_fraction_max=0.00013563368055555556`;
- `audit_clip_fraction_max=5.425347222222222e-05`.

Seed and selection discipline:

- validation-only selection was recorded;
- audit was final-only and not used for selection;
- role seeds were pairwise disjoint;
- overlapping seed values were empty.

Final training terms were finite:

- `total_loss=-24.44213325354077`;
- `weighted_empirical_cross_entropy=-21.74910939593761`;
- `gradient_norm=1.664178721875933`;
- `alpha_sum=1.0`;
- `rho_min=0.3368046806061109`;
- `rho_max=10250938398.747362`;
- `normalizer=0.06767589681482894`.

TensorFlow emitted CUDA plugin-registration and `cuInit` startup messages even
though the reviewed command set `CUDA_VISIBLE_DEVICES=-1` and the JSON recorded
`cpu_only=true`.  Phase 6 treats those messages as explanatory startup logging,
not GPU evidence.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 6 as a passing first budgeted corrected-metric training diagnostic | Passed: validation CE improved after 40/40 batches and budget gate passed | Passed for Phase 6: blockers empty and bridge/seed/selection fences held | Single run, single learning rate, no final audit cloud, no HMC/lower-gate test | Draft and review Phase 7 decision boundary for whether to replicate, add audit, or design next-scale evidence | No source-faithfulness, no final correctness, no default policy, no HMC readiness, no scaling claim |

## Post-Run Red Team Note

The strongest alternative explanation is that this is a favorable single-seed
validation result for the current generated validation cloud, not robust
evidence that the learned branch generalizes across seeds, final audit clouds,
lower gates, or downstream HMC.  A result that would overturn the Phase 6
decision is a corrected audit or replicated validation run showing the
improvement disappears or reverses under the same frozen metric discipline.
The weakest part of the evidence is that Phase 6 tests only one learning rate
and one seed; it is enough to pass the first diagnostic, but not enough to
promote defaults.

## Local Checks

Prechecks:

```bash
rg -n "PHASE5|1024 x 40|40960|33120|learning-rate=0.001|validation_improved_for_selection|validation_not_improved_against_untrained_ukf_baseline|approval" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-subplan-2026-06-19.md
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p77_budgeted_corrected_metric_training.py tests/highdim/test_p77_budgeted_corrected_metric_training.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p77_budgeted_corrected_metric_training.py
```

Precheck result:

- plan grep passed;
- compileall passed;
- focused pytest passed: `9 passed, 2 warnings`.

Postchecks:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-lr1e-3-2026-06-19.json
rg -n '"evidence_run": true|"hard_budget_gate_passed": true|"fit_quality_claim_permitted": true|"P_theta": 1656|"minimum_training_samples": 33120|"N_train": 40960|"completed_batches": 40|"validation_improved_for_selection"|"audit_used_for_selection": false|"source_route_prefit_used": false|"default_behavior_changed": false' docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-lr1e-3-2026-06-19.json
```

Postcheck result:

- JSON parsed;
- required evidence, budget, validation, audit-exclusion, source-prefit, and
  default-change fields were present.
- Claude R2 found and the runner repaired a validation-boundary artifact bug:
  evidence runs must not label validation improvement as explanatory-only.
  The repaired JSON now records
  `validation_improvement_observed_explanatory_only=false` while preserving
  `validation_improved_for_selection=true`.

## Phase 7 Handoff

Claude R4 agreed this Phase 6 result and the Phase 7 subplan.  Phase 7 may
now classify the result and decide the next evidence boundary without
retroactively changing Phase 6 criteria.
