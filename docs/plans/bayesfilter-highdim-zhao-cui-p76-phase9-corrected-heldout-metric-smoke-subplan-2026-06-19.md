# P76 Phase 9 Subplan: Corrected Heldout Metric Smoke

metadata_date: 2026-06-19
status: DRAFT_PENDING_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase8-corrected-heldout-metric-surface-result-2026-06-18.md
phase: 9
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Run a tiny CPU-only metric-only smoke that exercises the Phase 8 corrected
heldout metric surface end to end on a deterministic manual fixture.  The smoke
must prove metric wiring and artifact reporting only:

\[
  \alpha_i=\frac{w_i s_i^2}{\sum_j w_j s_j^2},
  \qquad
  \mathcal L_B(\theta)
  =
  -\sum_i \alpha_i \log \rho_\theta(z_i)+\log Z_\theta .
\]

Phase 9 is not a fitting, training, tuning, or validation phase.  It must not
generate substantive train/validation/audit samples and must not use the
metric value as fit-quality evidence.

## Entry Conditions Inherited From Phase 8

Phase 9 may begin only if:

- Phase 8 result exists;
- Phase 8 status is `PHASE8_CLAUDE_AGREE_CLOSED_READY_FOR_PHASE9_SUBPLAN`;
- Claude agreed Phase 8 execution;
- corrected heldout metric code and tests exist;
- target-only heldout density cross-entropy remains primary for future
  fit-quality interpretation;
- the historical \(\tau q_0\) helper remains a training-only comparator and is
  not promoted as a heldout metric;
- any generated-sample diagnostic, training pilot, tuning run, large run,
  GPU/CUDA use, default change, source-prefit comparison, or target change has
  separate reviewed approval.

## Required Artifacts

If approved, Phase 9 must produce:

- a tiny metric-only smoke runner, preferably
  `scripts/p76_corrected_heldout_metric_smoke.py`;
- focused tests for the runner under `tests/highdim/`, preferably
  `tests/highdim/test_p76_corrected_heldout_metric_smoke.py`;
- smoke JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-2026-06-19.json`;
- Phase 9 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-result-2026-06-19.md`;
- refreshed runbook, execution ledger, Claude review ledger, and stop handoff;
- either a Phase 10 subplan for a genuinely bounded generated-sample metric
  diagnostic, or a stop handoff.

No artifact may change default training behavior or claim fit quality.

## Required Checks/Tests/Reviews

Prechecks:

```bash
rg -n "PHASE8_CLAUDE_AGREE_CLOSED_READY_FOR_PHASE9_SUBPLAN|corrected_heldout_density_metric|target-only|VERDICT: AGREE" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase8-corrected-heldout-metric-surface-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
rg -n "P76CorrectedHeldoutMetricBatch|corrected_heldout_metric_weights|corrected_heldout_density_metric|weighted_empirical_cross_entropy_weights" bayesfilter/highdim/stochastic_density_training.py tests/highdim/test_p76_corrected_heldout_metric.py
```

Implementation checks, only after Claude agrees this subplan:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p76_corrected_heldout_metric_smoke.py tests/highdim/test_p76_corrected_heldout_metric_smoke.py bayesfilter/highdim/stochastic_density_training.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p76_corrected_heldout_metric_smoke.py tests/highdim/test_p76_corrected_heldout_metric.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p76_corrected_heldout_metric_smoke.py --output docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-2026-06-19.json
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-2026-06-19.json
```

Documentation checks:

```bash
rg -n "metric-only|target-only|manual_metric_fixture|not fit-quality|no training|tau q0|Phase 10|VERDICT" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-result-2026-06-19.md
git diff --check -- scripts/p76_corrected_heldout_metric_smoke.py tests/highdim/test_p76_corrected_heldout_metric_smoke.py docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-stop-handoff-2026-06-18.md
```

Review:

- Claude read-only review of this subplan before implementation.
- Claude read-only review of implementation/result artifacts after local
  checks.
- Loop repair to convergence or max five rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can the Phase 8 corrected heldout metric surface be exercised end to end on a deterministic manual fixture and produce a finite, self-consistent, JSON-preserved metric artifact? |
| Exact baseline/comparator | Phase 8 unit tests and the historical \(\tau q_0\) helper as a boundary comparator only. |
| Primary criterion | Smoke JSON shows corrected target-only alpha exactly matches the hand-computable manual fixture, heldout CE matches the decomposition from JSON \(\rho_\theta\), \(Z_\theta\), and alpha, finite \(\rho_\theta\), finite normalizer, payload role/provenance/nonclaims, no training step, no optimizer, no generated target cloud, and a positive separation between corrected alpha and the historical helper alpha on the manual fixture. |
| Veto diagnostics | Any optimizer/training step; generated substantive samples; use of `P75ObjectiveBatch` as the metric input; missing metric role/provenance; audit/test leakage; default behavior change; GPU/CUDA; network; package installation; source-prefit revival; fit-quality/lower-gate/validation/HMC/scaling/source-faithfulness claims. |
| Explanatory only | Numeric heldout CE on the manual fixture, alpha effective sample size, rho range, residual diagnostics, and old-vs-corrected alpha distance. |
| What will not be concluded | No fit-quality result, no UKF success/rejection, no lower-gate repair, no validation/HMC readiness, no scaling, no final rank/sample policy, no hyperparameter choice. |
| Artifact preserving result | Phase 9 smoke JSON, Phase 9 result, tests, and updated ledgers. |

## Smoke Fixture Contract

The smoke fixture must be deterministic and small:

- dimension at most 2;
- degree at most 1;
- rank tuple `(1, 2, 1)`;
- at most 4 points;
- manually specified points, target square-root values, integration weights,
  role, and provenance;
- hand-set TT cores, not random initialization;
- deterministic `tau = 2.5`;
- deterministic defensive reference density \(q_0(z_i)=1\) on all smoke
  points under the repository's tensor-product reference density;
- provenance must be `manual_metric_fixture`;
- role must be `heldout_metric`;
- no source-route generated cloud;
- no optimizer;
- no `train_step`;
- no call to `objective()` as a metric;
- no GPU/CUDA.

The smoke may compute the historical helper alpha only as a boundary
diagnostic:

\[
  \alpha_i^{\mathrm{old}}\propto w_i(s_i^2+\tau q_0(z_i)),
\]

and must label that quantity `historical_helper_boundary_only`.

The smoke runner and tests must use the same fixed manual fixture:

\[
z =
\begin{bmatrix}
-0.75 & -0.25\\
-0.25 &  0.50\\
 0.25 & -0.50\\
 0.75 &  0.25
\end{bmatrix},
\quad
s=(0,0.5,1,2),
\quad
w=(1,2,1.5,0.5),
\quad
\tau=2.5,
\quad
q_0(z_i)=1.
\]

Therefore:

\[
w_i s_i^2=(0,0.5,1.5,2),\quad
\alpha=(0,0.125,0.375,0.5),
\]

and the historical boundary-only helper alpha is

\[
\alpha^{\mathrm{old}}
=
\frac{w_i(s_i^2+2.5)}{\sum_j w_j(s_j^2+2.5)}
=
\frac{(2.5,5.5,5.25,3.25)}{16.5}.
\]

The implementation must use fixed TT cores equivalent to the Phase 8 unit
fixture:

```python
(
    tf.constant([[[0.4, -0.1], [0.2, 0.3]]], dtype=tf.float64),
    tf.constant([[[0.5], [0.1]], [[-0.2], [0.4]]], dtype=tf.float64),
)
```

The tests must verify the JSON artifact values against these exact alpha
vectors and must recompute the heldout CE decomposition from JSON-preserved
`rho_theta_values`, `normalizer`, and `corrected_alpha`.

## Forbidden Claims/Actions

- Do not run training.
- Do not use an optimizer.
- Do not generate substantive train/validation/audit samples.
- Do not use GPU/CUDA.
- Do not install or fetch packages.
- Do not use network.
- Do not launch detached agents.
- Do not change defaults.
- Do not revive source-prefit as a live repair method.
- Do not use the metric value for stopping, tuning, selection, or scientific
  interpretation.
- Do not claim fit-quality success, UKF success/rejection, lower-gate repair,
  validation readiness, HMC readiness, scaling, source-faithfulness, or final
  rank/sample policy.

## Exact Next-Phase Handoff Conditions

Phase 10 may begin only if:

- Phase 9 result exists;
- smoke JSON exists and parses;
- focused tests pass;
- Claude agrees the implementation/result;
- Phase 10 has a dedicated reviewed subplan;
- any generated-sample diagnostic, training pilot, tuning run, large run,
  GPU/CUDA use, default change, source-prefit comparison, target change, or
  fit-quality interpretation has separate approval.

## Stop Conditions

Stop if:

- the smoke cannot run without optimizer/training behavior;
- the metric smoke requires generated substantive samples;
- role/provenance cannot be preserved in the JSON artifact;
- corrected alpha and historical helper alpha are accidentally identical on
  the manual fixture, making the helper-boundary check non-discriminating;
- JSON alpha or CE values fail the hand-check against the fixed manual
  fixture;
- implementation would require GPU/CUDA, network, package installation, or
  unrelated code edits;
- Claude identifies a material blocker that cannot be repaired within five
  rounds.

## Skeptical Plan Audit

The main risk is treating a metric smoke as fit evidence.  The phase therefore
uses a manual fixture, bounded JSON payload, no optimizer, and explicit
nonclaims.  The old helper is allowed only as a boundary comparator so a future
reader can see that Phase 9 is exercising the corrected target-only path rather
than the historical training helper.
