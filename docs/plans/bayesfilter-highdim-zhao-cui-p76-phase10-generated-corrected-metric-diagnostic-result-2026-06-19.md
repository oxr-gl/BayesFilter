# P76 Phase 10 Result: Generated Corrected-Metric Diagnostic

metadata_date: 2026-06-19
status: PHASE10_CLAUDE_AGREE_CLOSED_READY_FOR_PHASE11_SUBPLAN
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-subplan-2026-06-19.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-result-2026-06-19.md
phase: 10
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Summary

Phase 10 executed a tiny CPU-only generated-sample diagnostic for the Phase 8
corrected heldout density metric.  It reused the Phase 6 UKF-frame bridge,
constructed the UKF-initialized untrained TT candidate, converted generated
holdout/replay target clouds to `P76CorrectedHeldoutMetricBatch`, and evaluated
`corrected_heldout_density_metric()`.

This was not a training phase.  No optimizer was constructed, no `train_step`
was called, and no candidate selection or tuning was performed.

The generated diagnostic JSON records:

- UKF-frame bridge status: `pass`;
- gate status: `pass`;
- `train_step_count: 0`;
- `optimizer_used: false`;
- `generated_sample_metric_only: true`;
- `fit_quality_claimed: false`;
- pairwise-disjoint seed roles;
- finite corrected CE, finite \(\rho_\theta\), finite normalizer, target-only
  alpha mass, and exact CE reconstruction for both holdout and replay.

The numeric CE values are explanatory only.  They are not fit-quality evidence,
not UKF success or rejection evidence, not lower-gate repair evidence, and not
validation/HMC readiness evidence.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | Can the corrected heldout density metric be evaluated on tiny generated UKF-frame diagnostic samples with frame tieout, role/provenance preservation, and no training leakage? |
| Baseline/comparator | Phase 9 manual smoke and the Phase 6 UKF-frame bridge. |
| Primary criterion | Passed locally: bridge pass, finite generated holdout/replay corrected metrics, finite \(\rho_\theta\), finite normalizer, target-only alpha mass within numerical tolerance, CE reconstruction from JSON values, role/provenance/nonclaims, `train_step_count: 0`, `optimizer_used: false`, `generated_sample_metric_only: true`, and disjoint shift/bridge/holdout/replay seed roles. |
| Veto diagnostics | No optimizer, no training step, no generated metric batch used for fitting/stopping/tuning/selection, no role/provenance loss, no bridge blocker, no nonfinite metric quantity, no default behavior change, no GPU use, no network, no package install, no source-prefit revival, and no fit-quality/lower-gate/validation/HMC/scaling/source-faithfulness claim. |
| Explanatory only | Numeric CE values, alpha effective sample sizes, rho ranges, target ranges, raw square-root residuals, centered log-shape RMS, and TensorFlow CUDA log noise during CPU-only import. |
| What will not be concluded | No fit-quality result, no UKF success/rejection, no training readiness, no lower-gate repair, no validation/HMC readiness, no scaling, no final rank/sample policy, no hyperparameter choice. |

## Artifacts

- Subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-subplan-2026-06-19.md`
- Diagnostic runner:
  `scripts/p76_generated_corrected_metric_diagnostic.py`
- Focused tests:
  `tests/highdim/test_p76_generated_corrected_metric_diagnostic.py`
- Diagnostic JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-2026-06-19.json`

## Local Checks

Subplan review:

- `p76-phase10-subplan-review-r1`: `VERDICT: BLOCK`.
- Claude required exact Phase 6 bridge fields/tolerances, a tighter
  bridge-only training-role fence, a full seed manifest including shift,
  bridge, holdout, and replay roles, and mandatory JSON provenance/nonclaim
  keys.
- Repaired the subplan visibly.
- `p76-phase10-subplan-review-r2`: `VERDICT: AGREE`.

Implementation checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p76_generated_corrected_metric_diagnostic.py tests/highdim/test_p76_generated_corrected_metric_diagnostic.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p76_generated_corrected_metric_diagnostic.py tests/highdim/test_p76_corrected_heldout_metric.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p76_generated_corrected_metric_diagnostic.py --output docs/plans/bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-2026-06-19.json --sample-count 32 --degree 2 --rank 4 --seed 7610
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-2026-06-19.json
```

Results:

- compileall passed;
- pytest passed: `28 passed, 2 warnings`;
- diagnostic command completed and wrote the JSON artifact;
- JSON parses.

TensorFlow emitted CUDA plugin/cuInit log noise during the CPU-only diagnostic,
but the command intentionally set `CUDA_VISIBLE_DEVICES=-1` before import and
the JSON records `cpu_only: true` and `cuda_visible_devices: "-1"`.

## Repair During Execution

The first diagnostic JSON correctly evaluated the metric but the runner's gate
used exact equality for `alpha_sum == 1.0`.  TensorFlow produced the expected
floating-point values `1.0000000000000002` and `0.9999999999999999`, so the
gate reported `target_only_alpha_mass_not_one`.

This was a checker bug, not a metric failure.  The gate was repaired to use a
`1e-10` numerical tolerance, the focused compile/test checks were rerun, and
the diagnostic was rerun with the same reviewed command.  The final JSON gate
passes.

## Diagnostic JSON Key Values

Bridge:

- `ukf_frame_bridge.status`: `pass`;
- reconstruction max absolute error: `6.22052119162378e-15`;
- target tieout max absolute error: `0.0`;
- training clip fraction max: `0.0`;
- audit clip fraction max: `0.0008680555555555555`;
- bridge blockers: `[]`.

Seed and role fences:

- `pairwise_disjoint_roles: true`;
- shift calibration seeds: `974001`, `974101`;
- bridge-training bookkeeping-only seeds: `975000`, `976000`;
- holdout metric seeds: `7301`, `7401`;
- replay metric seeds: `7311`, `7501`;
- bridge-training cloud present but bookkeeping-only and never passed to the
  corrected metric.

Generated metric batches:

- holdout role/provenance: `heldout_metric` / `reviewed_target_bridge`;
- replay role/provenance: `audit_metric` / `reviewed_target_bridge`;
- holdout CE: `-24.545784256998118`;
- replay CE: `-22.63588476639768`;
- normalizer: `0.10490675084866147`;
- holdout CE reconstruction error: `0.0`;
- replay CE reconstruction error: `0.0`;
- holdout corrected alpha sum: `1.0000000000000002`;
- replay corrected alpha sum: `0.9999999999999999`;
- all primary finite flags: true.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 10 as generated metric-plumbing evidence | Local checks pass and Claude agrees execution | No veto triggered after tolerance repair | This still says nothing about whether training can improve the corrected metric | Draft a Phase 11 training-design subplan or stop | No fit-quality result, no UKF success/rejection, no lower-gate repair, no validation/HMC readiness, no scaling, no final rank/sample policy |

## Claude Execution Review

- `p76-phase10-execution-review-r1` returned `VERDICT: AGREE`.
- Claude found no required fixes.
- Claude agreed Phase 10 stayed within the reviewed generated-sample
  corrected-metric-only boundary, preserved the no-training/no-optimizer
  contract, reused the Phase 6 bridge criteria, recorded the required disjoint
  seed manifest, fenced the bridge-training cloud as bookkeeping only,
  preserved CE reconstruction from JSON values, and made no fit-quality,
  lower-gate, validation/HMC, scaling, source-faithfulness, or default-change
  claim.
- Claude agreed the `alpha_sum` tolerance repair was acceptable because the
  observed values were ordinary double-precision roundoff around a normalized
  construction.

## Phase 11 Handoff

Phase 11 should not begin without a dedicated reviewed subplan.  The next
subplan, if drafted, should decide how to run a genuinely training-relevant
diagnostic using the corrected metric as the primary evaluation surface, with
predeclared training/validation/audit separation and no large-pilot escalation
without separate approval.
