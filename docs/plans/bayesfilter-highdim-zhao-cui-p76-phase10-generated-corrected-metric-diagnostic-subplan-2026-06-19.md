# P76 Phase 10 Subplan: Generated Corrected-Metric Diagnostic

metadata_date: 2026-06-19
status: PHASE10_SUBPLAN_CLAUDE_AGREE_READY_FOR_EXECUTION
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-result-2026-06-19.md
phase: 10
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Run a tiny CPU-only generated-sample diagnostic that evaluates the Phase 8
corrected heldout density cross-entropy on UKF-frame generated diagnostic
samples, without training.  The diagnostic checks that the corrected metric
pipeline works beyond the manual Phase 9 fixture:

\[
  \alpha_i^{\rm hold}
  =
  \frac{w_i s_i^2}{\sum_j w_j s_j^2},
  \qquad
  \widehat{\mathcal L}_{\rm hold}(\theta)
  =
  -\sum_i\alpha_i^{\rm hold}\log q_\theta(z_i)+\log Z_\theta .
\]

Phase 10 is not a fitting phase.  It must not use an optimizer, call
`train_step`, tune hyperparameters, compare candidate fits, or interpret the
metric value as fit quality.

## Entry Conditions Inherited From Phase 9

Phase 10 may begin only if:

- Phase 9 result exists;
- Phase 9 status is `PHASE9_CLAUDE_AGREE_CLOSED_READY_FOR_PHASE10_SUBPLAN`;
- Claude agreed Phase 9 execution;
- Phase 8 corrected metric surface remains implemented and tested;
- Phase 9 demonstrated deterministic JSON hand-checks for the metric surface;
- no generated-sample diagnostic, training pilot, tuning run, large run,
  GPU/CUDA use, default change, source-prefit comparison, target change, or
  fit-quality interpretation proceeds without this reviewed Phase 10 subplan.

## Required Artifacts

If approved, Phase 10 must produce:

- a tiny generated-sample metric diagnostic runner, preferably
  `scripts/p76_generated_corrected_metric_diagnostic.py`;
- focused tests, preferably
  `tests/highdim/test_p76_generated_corrected_metric_diagnostic.py`;
- diagnostic JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-2026-06-19.json`;
- Phase 10 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-result-2026-06-19.md`;
- refreshed runbook, execution ledger, Claude review ledger, and stop handoff;
- either a Phase 11 subplan for a carefully bounded training-design decision,
  or a stop handoff.

No artifact may change defaults or claim fit quality.

The diagnostic JSON must include, at minimum:

- `schema_version`, `status`, `run_manifest`, `cpu_only`,
  `cuda_visible_devices`, `default_behavior_changed`, and `nonclaims`;
- `train_step_count: 0`, `optimizer_used: false`,
  `generated_sample_metric_only: true`, `source_route_prefit_used: false`,
  and `fit_quality_claimed: false`;
- `requested_bounds` with `sample_count`, `degree`, `rank`, and `seed`;
- `seed_manifest` covering shift calibration, bridge-only training if present,
  holdout, and replay seeds, plus pairwise-disjointness checks and
  `stop_on_overlap: true`;
- `shift_manifest` describing that the shift constant is calibrated only from
  the shift-calibration cloud and is not selected from holdout/replay metric
  values;
- `ukf_frame_bridge` with the exact Phase 6 bridge status, fields, thresholds,
  and blockers listed below;
- `initializer_manifest` and `ukf_frame_manifest`;
- `metric_batches` for holdout and replay, each with role/provenance labels,
  point count, target/integration-weight mass, corrected alpha summary,
  `corrected_alpha`, `rho_theta_values`, `normalizer`,
  `heldout_cross_entropy`, `reconstructed_heldout_cross_entropy`, and
  `heldout_cross_entropy_reconstruction_abs_error`;
- `gate_summary` with pass/block status and blockers.

## Required Checks/Tests/Reviews

Prechecks:

```bash
rg -n "PHASE9_CLAUDE_AGREE_CLOSED_READY_FOR_PHASE10_SUBPLAN|corrected alpha|CE reconstruction|VERDICT: AGREE" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
rg -n "P76CorrectedHeldoutMetricBatch|corrected_heldout_density_metric|_target_context|_diagnostic_data|_ukf_frame_bridge|p76_build_ukf_initializer" bayesfilter/highdim/stochastic_density_training.py scripts/p76_bounded_ukf_minibatch_pilot.py bayesfilter/highdim/source_route.py
```

Implementation checks, only after Claude agrees this subplan:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p76_generated_corrected_metric_diagnostic.py tests/highdim/test_p76_generated_corrected_metric_diagnostic.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p76_generated_corrected_metric_diagnostic.py tests/highdim/test_p76_corrected_heldout_metric.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p76_generated_corrected_metric_diagnostic.py --output docs/plans/bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-2026-06-19.json --sample-count 32 --degree 2 --rank 4 --seed 7610
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-2026-06-19.json
```

Documentation checks:

```bash
rg -n "generated-sample|corrected heldout|target-only|no training|optimizer_used: false|train_step_count: 0|not fit-quality|Phase 11|VERDICT" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-result-2026-06-19.md
git diff --check -- scripts/p76_generated_corrected_metric_diagnostic.py tests/highdim/test_p76_generated_corrected_metric_diagnostic.py docs/plans/bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-stop-handoff-2026-06-18.md
```

Review:

- Claude read-only review of this subplan before implementation.
- Claude read-only review of implementation/result artifacts after local
  checks.
- Loop repair to convergence or max five rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can the corrected heldout density metric be evaluated on tiny generated UKF-frame diagnostic samples with frame tieout, role/provenance preservation, and no training leakage? |
| Exact baseline/comparator | Phase 9 manual smoke and the existing UKF-frame bridge from Phase 6. Historical \(\tau q_0\) helper may appear only as a labeled boundary comparator if used. |
| Primary criterion | JSON shows bridge pass or explicit fail-closed bridge blocker using the exact Phase 6 UKF-frame bridge criteria below; if bridge passes, generated holdout/replay corrected metrics have finite CE, finite \(\rho_\theta\), finite normalizer, target-only alpha mass, role/provenance/nonclaims, CE reconstruction from JSON values, `train_step_count: 0`, `optimizer_used: false`, `generated_sample_metric_only: true`, and pairwise-disjoint shift/bridge-training/holdout/replay seed roles. |
| Veto diagnostics | Optimizer/training step; use of generated diagnostic samples for fitting, stopping, tuning, or selection; missing role/provenance; bridge/tieout failure not recorded fail-closed; nonfinite targets/rho/normalizer/CE; audit leakage; default behavior change; GPU/CUDA; network; package installation; source-prefit revival; fit-quality/lower-gate/validation/HMC/scaling/source-faithfulness claims. |
| Explanatory only | Numeric CE values for UKF-initialized untrained candidate, alpha effective sample sizes, rho ranges, target ranges, clipping fractions, old-helper boundary distance if reported. |
| What will not be concluded | No fit-quality result, no UKF success/rejection, no training readiness, no lower-gate repair, no validation/HMC readiness, no scaling, no final rank/sample policy, no hyperparameter choice. |
| Artifact preserving result | Phase 10 JSON, Phase 10 result, tests, and updated ledgers. |

## Diagnostic Design

The diagnostic should mirror the existing Phase 6 UKF-frame context but stop
before training:

- construct the author SIR Austria model and observations as in Phase 6;
- run the UKF scout and build the UKF initializer;
- construct the local product basis with degree `2` and rank `4`;
- build the UKF frame;
- generate a shift calibration batch only to define the common shift constant;
- generate tiny metric-only holdout and replay batches using the existing
  audit seeds;
- generate at most one tiny bridge-training-role batch only if needed to reuse
  the Phase 6 bridge/tieout surface.  This bridge-only batch must never be
  passed to `corrected_heldout_density_metric`, never be passed to any
  objective/training helper, never be used for shift choice, stopping,
  selection, tuning, or interpretation, and must be omitted unless strictly
  necessary for the fail-closed bridge check;
- build a `TrainableFunctionalTT` from the UKF initializer cores;
- convert holdout/replay generated data to `P76CorrectedHeldoutMetricBatch`
  with role `heldout_metric` or `audit_metric` and provenance
  `reviewed_target_bridge`;
- evaluate `corrected_heldout_density_metric()` on those batches;
- preserve JSON values sufficient to recompute CE:
  `corrected_alpha`, `rho_theta_values`, `normalizer`, and
  `heldout_cross_entropy`.

Hard bounds for the reviewed command:

- `sample_count <= 32`;
- `degree == 2`;
- `rank == 4`;
- CPU-only with `CUDA_VISIBLE_DEVICES=-1`;
- no optimizer construction;
- no call to `train_step`;
- no generated diagnostic sample used for training, stopping, tuning, or
  selection.

## Required UKF-Frame Bridge Criteria

Phase 10 must reuse the Phase 6 bridge schema and thresholds exactly, either
by calling the existing Phase 6 bridge helper or by emitting an equivalent JSON
block with these fields:

- `status`;
- `target_dimension`;
- `frame_dimension`;
- `product_basis_dimension`;
- `initializer_dimension`;
- `dimension_match`;
- `frame_hash`;
- `training_frame_hashes`;
- `audit_frame_hashes`;
- `reconstruction_max_abs_error`;
- `target_tieout_max_abs_error`;
- `target_tieout_source`;
- `training_clip_fraction_max`;
- `audit_clip_fraction_max`;
- `bridge_target_values_finite`;
- `training_target_values_finite`;
- `audit_target_values_finite`;
- `nonfinite_target_value_count`;
- `thresholds`;
- `blockers`.

The thresholds are inherited from Phase 6:

- `reconstruction_max_abs_error <= 1e-10`;
- `target_tieout_max_abs_error <= 1e-10`;
- `training_clip_fraction_max <= 0.25`;
- `audit_clip_fraction_max <= 0.25`.

If any criterion fails, Phase 10 must write a fail-closed JSON/result with no
metric promotion and no fit-quality interpretation.

## Seed And Role Fences

The JSON must record a `seed_manifest` with all generated-sample roles:

- shift calibration prior/process seeds;
- bridge-training prior/process seeds if a bridge-only training cloud is
  generated;
- holdout prior/process seeds;
- replay prior/process seeds.

All seed pairs must be pairwise disjoint by role.  Any overlap is a stop
condition and must produce a blocked JSON/result before metric interpretation.
The bridge-training role is a bridge/tieout bookkeeping role only; it is not a
training dataset for Phase 10.

## Forbidden Claims/Actions

- Do not train.
- Do not construct or use an optimizer.
- Do not call `train_step`.
- Do not tune hyperparameters.
- Do not compare candidate fits.
- Do not use GPU/CUDA.
- Do not install or fetch packages.
- Do not use network.
- Do not launch detached agents.
- Do not change defaults.
- Do not revive source-prefit as a live repair method.
- Do not interpret generated metric values as fit quality.
- Do not claim UKF success/rejection, lower-gate repair, validation readiness,
  HMC readiness, scaling, source-faithfulness, or final rank/sample policy.

## Exact Next-Phase Handoff Conditions

Phase 11 may begin only if:

- Phase 10 result exists;
- diagnostic JSON exists and parses;
- focused tests pass;
- Claude agrees the implementation/result;
- Phase 11 has a dedicated reviewed subplan;
- any training pilot, tuning run, large run, GPU/CUDA use, default change,
  source-prefit comparison, target change, or fit-quality interpretation has
  separate approval.

## Stop Conditions

Stop if:

- the generated diagnostic cannot run without optimizer/training behavior;
- bridge/tieout fails and cannot be recorded fail-closed;
- target-only alpha mass is zero or nonfinite for holdout/replay;
- role/provenance cannot be preserved in metric batches or JSON;
- CE cannot be reconstructed from JSON values;
- generated holdout/replay seeds overlap with training/shift seeds;
- implementation would require GPU/CUDA, network, package installation, or
  unrelated code edits;
- Claude identifies a material blocker that cannot be repaired within five
  rounds.

## Skeptical Plan Audit

The main risk is that generated-sample metric values look like model-quality
evidence.  Phase 10 blocks that interpretation: the candidate is the
UKF-initialized untrained density, and numeric CE values are explanatory only.
The phase is a plumbing and leakage diagnostic for the corrected target-only
metric on generated UKF-frame samples.  A later phase must separately design
any training experiment.
