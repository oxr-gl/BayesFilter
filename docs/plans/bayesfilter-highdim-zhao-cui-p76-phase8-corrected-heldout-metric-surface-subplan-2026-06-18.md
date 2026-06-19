# P76 Phase 8 Subplan: Corrected Heldout Metric Surface

metadata_date: 2026-06-18
status: REPAIRED_AFTER_CLAUDE_BLOCK_ITER1_PENDING_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-result-v2-2026-06-18.md
phase: 8
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Design and, only after approval, implement an opt-in corrected heldout metric
surface for P76.  The surface must compute the target-only density-aligned
heldout cross-entropy required by Phase 6b/7 v2 without changing defaults and
without reusing the current helper-alpha rule as the primary heldout metric.

Phase 8 is not a training or fitting phase.  It must not launch a pilot or
generate substantive train/validation/audit samples.  Its implementation, if
approved, is limited to metric helpers, focused tests, and documentation.

## Entry Conditions Inherited From Phase 7 v2

Phase 8 may begin only if:

- Phase 7 v2 result exists;
- Claude agrees Phase 7 v2 execution;
- Phase 7 v2 result identifies this corrected heldout metric surface as the
  next justified action;
- the legacy Phase 7 draft remains superseded;
- Phase 6 remains mechanics-only evidence;
- target-only heldout density cross-entropy remains primary for future
  fit-quality interpretation;
- raw and sign/scale-adjusted square-root residuals remain secondary and
  explanatory only.

## Required Artifacts

If Phase 8 is approved for implementation, it must produce:

- opt-in metric code in a reviewed location, preferably a small helper in
  `bayesfilter/highdim/stochastic_density_training.py` or a dedicated P76
  helper module if that is cleaner;
- a dedicated corrected heldout metric batch/terms surface that is not
  `P75ObjectiveBatch` and is not duck-compatible with the training objective
  path.  The metric input should use non-training field names such as
  `target_sqrt_values` and `integration_weights`, plus a required declared
  metric role, rather than reusing the training names `target_values` and
  `weights`;
- focused tests under `tests/highdim/`;
- Phase 8 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase8-corrected-heldout-metric-surface-result-2026-06-18.md`;
- refreshed runbook, execution ledger, Claude review ledger, and stop handoff;
- either a Phase 9 subplan for a tiny metric-only smoke or a stop handoff.

No artifact may change default training behavior or treat the new metric as a
validated fit-quality result.

## Required Checks/Tests/Reviews

Prechecks:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-2026-06-18.json
rg -n "weighted_empirical_cross_entropy_weights|raw = batch.weights|tau \\* q0|rho_theta|normalizer|log_density" bayesfilter/highdim/stochastic_density_training.py
rg -n "local_fit_points|target_values|fit_weights|_target_batch_from_data|audit_seed_policy" scripts/p76_bounded_ukf_minibatch_pilot.py bayesfilter/highdim/source_route.py
```

Implementation checks, only if approved:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/stochastic_density_training.py tests/highdim/test_p76_corrected_heldout_metric.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p76_corrected_heldout_metric.py tests/highdim/test_p76_bounded_ukf_minibatch_pilot.py tests/highdim/test_p75_stochastic_density_training.py
```

Focused test obligations:

- the metric input rejects missing roles and training/fit roles, and accepts
  only declared non-training metric roles such as `heldout_metric` and
  `audit_metric`;
- the metric input rejects missing provenance, forbidden provenance, and
  unreviewed target-bridge provenance.  Allowed provenance must be declared in
  code by a finite whitelist such as `reviewed_target_bridge`,
  `unit_test_reviewed_target_bridge`, or `manual_metric_fixture`; provenance
  containing `train`, `fit`, `prefit`, `source_prefit`,
  `source-guided-prefit`, `selection`, `stopping`, `tuning`, or
  `unreviewed_target_bridge` must be rejected;
- point records with missing provenance or forbidden training/prefit/source
  provenance are rejected by the metric batch;
- point records with training/fit roles are rejected by the metric batch;
- the metric batch is a separate API surface from `P75ObjectiveBatch` and does
  not expose `target_values`/`weights` attributes that could silently feed
  `objective()` or `train_step()`;
- a differential fixture proves the old helper rule
  \(\alpha_i\propto w_i(s_i^2+\tau q_0(z_i))\) and the corrected heldout rule
  \(\alpha_i\propto w_i s_i^2\) differ, and the new metric matches only the
  corrected heldout rule;
- a hand-computed fixture proves the metric equals
  \(-\sum_i\alpha_i\log\rho_\theta(z_i)+\log Z_\theta\) using
  `rho_theta()` and `normalizer()`;
- veto tests cover all-zero target mass, mixed zero/positive targets, nonfinite
  points/targets/weights, negative weights, dimension mismatch, and nonfinite
  rho/normalizer/loss where practical in the focused unit surface;
- payload tests prove role, provenance, classification, status, finite flags,
  nonclaims, alpha diagnostics, rho diagnostics, and explanatory-only status
  survive JSON-friendly reporting.

Documentation checks:

```bash
rg -n "target-only|density-aligned heldout|s_i\\^2|tau q0|reviewed target bridge|audit/test|finite candidate set|source-prefit revival|no training pilot" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase8-corrected-heldout-metric-surface-result-2026-06-18.md
git diff --check -- bayesfilter/highdim/stochastic_density_training.py tests/highdim/test_p76_corrected_heldout_metric.py docs/plans/bayesfilter-highdim-zhao-cui-p76-phase8-corrected-heldout-metric-surface-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase8-corrected-heldout-metric-surface-result-2026-06-18.md
```

Review:

- Claude read-only review of this subplan before implementation.
- Claude read-only review of implementation/result artifacts after local
  checks.
- Loop repair to convergence or max five rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can we add a small opt-in metric surface that computes the corrected target-only heldout density cross-entropy and helper-boundary diagnostics needed before any future P76 fitting run? |
| Exact baseline/comparator | Existing `TrainableFunctionalTT` density methods and the current helper-alpha rule, which is retained as historical training behavior but not approved as the primary heldout metric. |
| Primary criterion | Focused tests show the new metric computes \(\alpha_i\propto w_i s_i^2\), reports finite heldout cross-entropy from \(\rho_\theta\) and \(Z_\theta\), vetoes invalid target mass/nonfinite values, records role/provenance, uses a dedicated non-training metric batch, and does not call or promote `weighted_empirical_cross_entropy_weights` as the primary heldout metric. |
| Veto diagnostics | Default behavior change; reuse of `P75ObjectiveBatch` as the heldout metric API; heldout metric batch exposing training-compatible `target_values`/`weights` attributes; use of \(s_i^2+\tau q_0\) as primary heldout target without reviewed target bridge; audit leakage; implementation edits outside the reviewed surface; generated substantive samples; training pilot; GPU/CUDA; network; package installation; source-prefit revival; fit-quality/lower-gate/validation/HMC/scaling claims. |
| Explanatory only | Metric values on synthetic/unit-test fixtures, alpha concentration, effective sample size, secondary residuals, and helper-boundary diagnostics. |
| What will not be concluded | No fit-quality result, no UKF success/rejection, no lower-gate repair, no validation/HMC readiness, no scaling, no final rank/sample policy. |
| Artifact preserving result | Phase 8 result, focused tests, and optional Phase 9 subplan. |

## Required Metric Semantics

### Required API Boundary

The corrected heldout metric must be opt-in and separated from the training
objective surface.

Required implementation shape:

- define a dedicated immutable metric input, for example
  `P76CorrectedHeldoutMetricBatch`;
- define dedicated metric terms, for example
  `P76CorrectedHeldoutMetricTerms`;
- expose a dedicated helper, for example
  `TrainableFunctionalTT.corrected_heldout_density_metric(batch)`;
- require `batch.role` to be declared and in a finite non-training set such as
  `{"heldout_metric", "audit_metric"}`;
- require `batch.provenance_label` to be declared and in a finite allowed
  provenance set for metric-only reviewed target bridges or manual unit
  fixtures;
- reject record roles such as `fit`, `train`, `training`, `prefit`, and the
  existing audit-line roles if they conflict with the declared metric role;
- reject batch or point-record provenance containing training, prefit,
  source-prefit, selection, stopping, tuning, or unreviewed target-bridge
  markers;
- avoid fields named `target_values` and `weights` on the metric batch so it
  cannot silently satisfy the training objective's duck-typed surface;
- preserve `P75ObjectiveBatch`, `objective()`, `train_step()`, and
  `weighted_empirical_cross_entropy_weights()` semantics unchanged.

The payload must label the surface as `extension_or_invention`,
`corrected_heldout_metric`, `explanatory_only`, and `not_training_or_selection`.

For a metric batch \(B=\{(z_i,w_i,s_i)\}_{i=1}^n\), Phase 8 must compute:

\[
  u_i=s_i^2,\qquad
  M_B=\sum_i w_i u_i,\qquad
  \alpha_i^B=\frac{w_i u_i}{M_B},
\]

and

\[
  \mathcal L_B(\theta)
  =
  -\sum_i\alpha_i^B\log\rho_\theta(z_i)+\log Z_\theta .
\]

The metric must veto if:

- \(M_B\le0\) or nonfinite;
- any point, target value, weight, rho value, normalizer, log density, or loss
  is nonfinite;
- any weight is negative;
- dimensions are inconsistent;
- the batch role is not declared;
- the batch role is a training/fit/prefit role rather than an approved metric
  role;
- the batch provenance is missing, forbidden, or not in the approved metric
  provenance set;
- point records use training/fit/prefit roles;
- point records have missing, forbidden, or unreviewed target-bridge
  provenance;
- audit/test records are used for training, stopping, hyperparameter
  selection, or metric selection.

The metric may report secondary diagnostics:

- raw square-root residual;
- optimal-scale square-root residual;
- centered log-shape residual;
- alpha effective sample size;
- target and rho dynamic ranges.

These are explanatory only.

## Hyperparameter And Sample-Budget Boundary

Phase 8 must not tune hyperparameters.  It may document that a future fitting
phase must use finite candidate sets, predeclared learning rate,
regularization, clipping, batch size, batch count, degree, rank, validation
cadence, and stopping rule.

For the current degree-2/rank-4/dimension-36 configuration, future substantive
fit-quality pilots must use at least `16560` training samples.  This is a
minimum necessary condition, not sufficient evidence.

## Forbidden Claims/Actions

- Do not run a training pilot.
- Do not generate substantive train/validation/audit samples.
- Do not use GPU/CUDA.
- Do not install or fetch packages.
- Do not use network.
- Do not launch detached agents.
- Do not change defaults.
- Do not revive source-prefit as a live repair method.
- Do not use audit/test samples for training, stopping, hyperparameter
  selection, or metric selection.
- Do not claim fit-quality success, UKF success/rejection, lower-gate repair,
  validation readiness, HMC readiness, scaling, source-faithfulness, or final
  rank/sample policy.

## Exact Next-Phase Handoff Conditions

Phase 9 may begin only if:

- Phase 8 result exists;
- focused tests pass;
- Claude agrees the implementation/result;
- Phase 9 has a dedicated reviewed subplan;
- any generated-sample diagnostic, training pilot, tuning run, large run,
  GPU/CUDA use, default change, source-prefit comparison, or target change has
  separate approval.

## Stop Conditions

Stop if:

- the corrected metric cannot be implemented without changing default training
  behavior;
- target-only alpha cannot be computed separately from the existing helper
  alpha;
- focused tests require substantive generated samples;
- implementation would require GPU/CUDA, network, package installation, or
  unrelated code edits;
- Claude identifies a material blocker that cannot be repaired within five
  rounds.

## Skeptical Plan Audit

The main risk is accidentally making the old training helper look like the new
heldout metric, or making a metric-only helper look like fit evidence.  Phase 8
therefore keeps the surface opt-in, unit-testable, and non-promotional.
