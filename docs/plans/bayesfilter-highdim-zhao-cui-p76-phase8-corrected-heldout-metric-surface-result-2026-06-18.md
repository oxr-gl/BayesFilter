# P76 Phase 8 Result: Corrected Heldout Metric Surface

metadata_date: 2026-06-18
status: PHASE8_CLAUDE_AGREE_CLOSED_READY_FOR_PHASE9_SUBPLAN
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase8-corrected-heldout-metric-surface-subplan-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-result-v2-2026-06-18.md
phase: 8
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Summary

Phase 8 added an opt-in corrected heldout metric surface for P76.  The new
surface computes the target-only density-aligned heldout cross-entropy

\[
  \alpha_i=\frac{w_i s_i^2}{\sum_j w_j s_j^2},
  \qquad
  \mathcal L_B(\theta)
  =
  -\sum_i \alpha_i \log \rho_\theta(z_i)+\log Z_\theta .
\]

The historical training helper
`weighted_empirical_cross_entropy_weights()` remains unchanged and continues
to use its training-only \(\tau q_0\) smoothing.  The corrected heldout metric
does not reuse `P75ObjectiveBatch` and does not change default behavior.

Boundary terms for the Phase 8 documentation check: target-only,
density-aligned heldout, \(s_i^2\), tau q0, reviewed target bridge,
audit/test separation, finite candidate set for future tuning, source-prefit
revival forbidden, and no training pilot.

## Skeptical Plan Audit

Passed after repair.  The initial Phase 8 subplan was too loose because the
metric could have been implemented as a thin variant of the training batch
surface.  Claude blocked that plan.  The repaired subplan requires a dedicated
non-training metric batch, mandatory role and provenance guards, a differential
test against the old \(\tau q_0\) helper rule, hand-computed heldout CE checks,
veto tests, and payload boundary tests.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can we add a small opt-in metric surface that computes target-only heldout density cross-entropy and helper-boundary diagnostics before future P76 fitting runs? |
| Baseline/comparator | Existing `TrainableFunctionalTT` density methods and the historical helper-alpha rule. |
| Primary criterion | Passed locally: focused tests verify target-only alpha, exact CE decomposition, old-vs-corrected alpha separation, role/provenance rejection, target-mass vetoes, finite diagnostics, and payload nonclaims. |
| Veto diagnostics | No default behavior change, no `P75ObjectiveBatch` reuse for the metric API, no training pilot, no substantive generated samples, no GPU/CUDA, no network, no package install, no source-prefit revival, and no fit-quality/lower-gate/validation/HMC/scaling claim. |
| Explanatory only | Unit-test metric values, alpha concentration, effective sample size, square-root residuals, centered log-shape residuals, and payload finite flags. |
| Not concluded | No fit-quality result, no UKF success/rejection, no lower-gate repair, no validation/HMC readiness, no scaling, no final rank/sample policy. |

## Implementation Artifacts

- `bayesfilter/highdim/stochastic_density_training.py`
  - added `P76CorrectedHeldoutMetricBatch`;
  - added `P76CorrectedHeldoutMetricTerms`;
  - added `TrainableFunctionalTT.corrected_heldout_metric_weights()`;
  - added `TrainableFunctionalTT.corrected_heldout_density_metric()`;
  - added `corrected_heldout_metric_terms_payload()`;
  - preserved `P75ObjectiveBatch`, `objective()`, `train_step()`, and
    `weighted_empirical_cross_entropy_weights()`.
- `tests/highdim/test_p76_corrected_heldout_metric.py`
  - added focused tests for the corrected metric surface.

## Boundary Details

The metric input surface uses non-training names:

- `target_sqrt_values`;
- `integration_weights`;
- `role`;
- `provenance_label`.

The metric batch rejects training/fit/prefit roles and missing or forbidden
provenance.  Allowed provenance is finite and reviewed:

- `reviewed_target_bridge`;
- `unit_test_reviewed_target_bridge`;
- `manual_metric_fixture`.

Forbidden provenance includes training, prefit, source-prefit, selection,
stopping, tuning, and unreviewed target-bridge markers.

## Local Checks

Prechecks:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-2026-06-18.json
rg -n "weighted_empirical_cross_entropy_weights|raw = batch.weights|tau \\* q0|rho_theta|normalizer|log_density" bayesfilter/highdim/stochastic_density_training.py
rg -n "local_fit_points|target_values|fit_weights|_target_batch_from_data|audit_seed_policy" scripts/p76_bounded_ukf_minibatch_pilot.py bayesfilter/highdim/source_route.py
```

Implementation checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/stochastic_density_training.py tests/highdim/test_p76_corrected_heldout_metric.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p76_corrected_heldout_metric.py tests/highdim/test_p76_bounded_ukf_minibatch_pilot.py tests/highdim/test_p75_stochastic_density_training.py
```

Result:

- compileall passed;
- pytest passed: `45 passed, 2 warnings`;
- the first pytest attempt failed because one test fixture used two point rows
  with four target rows, so shape validation fired before the intended
  nonfinite-points check.  The fixture was corrected and the same test command
  passed.

Diff check:

```bash
git diff --check -- bayesfilter/highdim/stochastic_density_training.py tests/highdim/test_p76_corrected_heldout_metric.py docs/plans/bayesfilter-highdim-zhao-cui-p76-phase8-corrected-heldout-metric-surface-subplan-2026-06-18.md
```

Result: passed.

## Claude Reviews

Subplan review iter1:

- `p76-phase8-subplan-review-iter1`;
- `VERDICT: BLOCK`;
- required a dedicated heldout metric batch or equivalent hard separation,
  explicit role guard, old-vs-corrected alpha differential test, hand-computed
  CE test, stronger invalid-mass/nonfinite tests, and payload provenance tests.

Subplan review iter2:

- `p76-phase8-subplan-review-iter2`;
- `VERDICT: BLOCK`;
- required provenance to be a declared validated input with rejection
  semantics, not only a payload field.

Subplan review iter3:

- `p76-phase8-subplan-review-iter3`;
- `VERDICT: AGREE`;
- Claude agreed the repaired subplan was safe and sufficient for the bounded
  implementation.

Execution review:

- `p76-phase8-execution-review-r2` returned `VERDICT: AGREE`.
- Claude agreed the dedicated non-training batch, role/provenance guards,
  target-only alpha, exact CE decomposition, historical helper boundary,
  focused tests, payload nonclaims, and no-overclaim boundary.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 8 as a metric-only implementation | Local checks pass and Claude agrees execution | No veto triggered | Future generated-sample metric use still needs a reviewed Phase 9 subplan | Draft Phase 9 metric-only smoke subplan or stop handoff | No fit-quality result, no UKF success/rejection, no lower-gate repair, no validation/HMC readiness, no scaling, no final rank/sample policy |

## Phase 9 Handoff

Phase 9 may begin only after Claude agrees the Phase 8 execution/result.  The
next phase should be a tiny metric-only smoke or a stop handoff.  Any
generated-sample diagnostic, training pilot, tuning run, large run, GPU/CUDA
use, default change, source-prefit comparison, or target change still requires
separate reviewed approval.
