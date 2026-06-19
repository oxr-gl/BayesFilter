# P76 Phase 9 Result: Corrected Heldout Metric Smoke

metadata_date: 2026-06-19
status: PHASE9_CLAUDE_AGREE_CLOSED_READY_FOR_PHASE10_SUBPLAN
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-subplan-2026-06-19.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase8-corrected-heldout-metric-surface-result-2026-06-18.md
phase: 9
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Summary

Phase 9 executed a tiny CPU-only metric-only smoke for the Phase 8 corrected
heldout metric.  The smoke used a deterministic manual metric fixture, fixed
TT cores, fixed `tau = 2.5`, and no optimizer or training step.

The smoke JSON confirms the target-only corrected alpha:

\[
\alpha=(0,0.125,0.375,0.5),
\]

and the historical helper boundary-only alpha:

\[
\alpha^{\rm old}=(2.5,5.5,5.25,3.25)/16.5.
\]

The JSON hand checks passed:

- corrected alpha matches expected;
- historical helper alpha matches expected;
- old/new alpha are separated;
- heldout CE reconstructs exactly from JSON `rho_theta_values`, `normalizer`,
  and `corrected_alpha`.

Phase 9 is metric-only.  It is not fit-quality evidence, not lower-gate repair
evidence, not validation evidence, and not HMC readiness evidence.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | Can the Phase 8 corrected heldout metric surface be exercised end to end on a deterministic manual fixture and produce a finite, self-consistent, JSON-preserved metric artifact? |
| Baseline/comparator | Phase 8 unit tests plus the historical \(\tau q_0\) helper as a boundary comparator only. |
| Primary criterion | Passed locally: smoke JSON has target-only corrected alpha, exact CE reconstruction, finite \(\rho_\theta\), finite normalizer, role/provenance/nonclaims, no optimizer, no training step, no generated target cloud, and separated old/new alpha. |
| Veto diagnostics | No optimizer, no training step, no generated substantive samples, no `P75ObjectiveBatch` metric input, no role/provenance loss, no default behavior change, no GPU/CUDA, no network, no package install, no source-prefit revival, and no fit-quality/lower-gate/validation/HMC/scaling/source-faithfulness claim. |
| Explanatory only | Numeric heldout CE, alpha effective sample size, rho range, residual diagnostics, and old-vs-corrected alpha distance on the manual fixture. |
| What will not be concluded | No fit-quality result, no UKF success/rejection, no lower-gate repair, no validation/HMC readiness, no scaling, no final rank/sample policy, no hyperparameter choice. |

## Artifacts

- Subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-subplan-2026-06-19.md`
- Smoke runner:
  `scripts/p76_corrected_heldout_metric_smoke.py`
- Focused tests:
  `tests/highdim/test_p76_corrected_heldout_metric_smoke.py`
- Smoke JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-2026-06-19.json`

## Local Checks

Subplan review:

- `p76-phase9-subplan-review-r1`: `VERDICT: BLOCK`.
- Claude required explicit deterministic `tau/q0` for the old-helper boundary,
  hand-set deterministic TT cores, and exact JSON hand-checks.
- Repaired subplan.
- `p76-phase9-subplan-review-r2`: `VERDICT: AGREE`.

Implementation checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p76_corrected_heldout_metric_smoke.py tests/highdim/test_p76_corrected_heldout_metric_smoke.py bayesfilter/highdim/stochastic_density_training.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p76_corrected_heldout_metric_smoke.py tests/highdim/test_p76_corrected_heldout_metric.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p76_corrected_heldout_metric_smoke.py --output docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-2026-06-19.json
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-2026-06-19.json
```

Results:

- compileall passed;
- pytest passed: `25 passed, 2 warnings`;
- smoke command completed and wrote the JSON artifact;
- JSON parses.

TensorFlow emitted CUDA plugin/cuInit log noise during the CPU-only smoke, but
the command intentionally set `CUDA_VISIBLE_DEVICES=-1` before import and the
artifact records:

- `cpu_only: true`;
- `cuda_visible_devices: "-1"`;
- `train_step_count: 0`;
- `optimizer_used: false`.

Documentation checks:

```bash
rg -n "metric-only|target-only|manual_metric_fixture|not fit-quality|no training|tau q0|Phase 10|VERDICT" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-result-2026-06-19.md
git diff --check -- scripts/p76_corrected_heldout_metric_smoke.py tests/highdim/test_p76_corrected_heldout_metric_smoke.py docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-stop-handoff-2026-06-18.md
```

Status: passed and reviewed by Claude.

## Smoke JSON Key Values

- corrected alpha: `[0.0, 0.125, 0.375, 0.5]`;
- historical helper boundary alpha:
  `[0.15151515151515152, 0.3333333333333333, 0.3181818181818182, 0.19696969696969696]`;
- old/new alpha L1 distance: `0.7196969696969697`;
- heldout CE: `-0.002765941550252893`;
- CE reconstruction absolute error: `0.0`;
- normalizer: `2.5696`;
- rho range: `[2.522553879794644, 2.622998573225672]`;
- finite flags: all true.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 9 as a metric-only smoke | Local checks pass and Claude agrees execution | No veto triggered | Any generated-sample or fitting diagnostic still needs a reviewed Phase 10 subplan | Draft Phase 10 subplan or stop handoff | No fit-quality result, no UKF success/rejection, no lower-gate repair, no validation/HMC readiness, no scaling, no final rank/sample policy |

## Claude Execution Review

- `p76-phase9-execution-review-r1` returned `VERDICT: AGREE`.
- Claude found no required fixes.
- Claude agreed the smoke is metric-only and deterministic, records no
  optimizer/training/generated target cloud/default change, preserves exact
  corrected alpha and historical helper boundary alpha, reconstructs CE from
  JSON values, preserves role/provenance/nonclaims, records CPU-only
  provenance despite TensorFlow CUDA log noise, and does not overclaim.

## Phase 10 Handoff

Phase 10 may begin only after Claude agrees the Phase 9 execution/result and a
dedicated Phase 10 subplan is reviewed.  Any generated-sample diagnostic,
training pilot, tuning run, large run, GPU/CUDA use, default change,
source-prefit comparison, target change, or fit-quality interpretation still
requires separate reviewed approval.
