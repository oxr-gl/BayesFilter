# Plan: Row 173 Post-Update Route Hypothesis Probe

## Decision

`planned_pending_claude_review`

## Scope

This is a BayesFilter-owned experimental DPF difference audit for the local
float64 FilterFlow comparator. It continues the row `173`, time `93`
smoothness-gradient debugging after the adjacent-boundary probe showed that the
observed residual is reconstructed exactly by the `post_update_log_likelihoods`
parameter-path row.

Allowed write set:

- `experiments/dpf_implementation/tf_tfp/`
- `experiments/dpf_implementation/reports/`
- `docs/plans/`

Forbidden write set:

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `.localsource/filterflow/`
- vendored student code
- high-dimensional nonlinear filtering lane artifacts
- DSGE/NAWM-specific implementations or tests

## Evidence Contract

Question: Which of the four remaining post-update graph-route hypotheses best
explains the row-173/time-93 BayesFilter-vs-local-float64-FilterFlow gradient
residual?

Comparator: the local executable float64 FilterFlow checkout, treated only as
the canonical comparator for this audit lane.

Primary criterion: identify whether the residual is explained by the
`post_update_log_likelihoods` route itself, by the
`pre_current_log_likelihoods + increment` split, by carried cumulative
likelihood state routing, or by the adjacent transport/post-state tape topology.

Artifact: preserve the result in
`docs/plans/bayesfilter-dpf-filterflow-float64-row-173-post-update-route-hypotheses-result-2026-06-04.md`
and
`experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_post_update_route_hypotheses_2026-06-04.json`.

Promotion criterion: the result may promote one hypothesis only if value
addition holds, scalar and resampling gates pass, all compared gradients are
finite, and the promoted residual reconstruction is within `2e-4` in max
absolute residual.

Decision rule, applied in order:

| Outcome | Required condition | Tie handling |
| --- | --- | --- |
| `h1_value_additivity_veto` | Value additivity fails on either side for `post_update_log_likelihoods = pre_current_log_likelihoods + increment`, before gradient interpretation. | This veto wins over all gradient diagnostics. |
| `h2_component_sum_reconstructs` | Values match, scalar/resampling/finite gates pass, and `abs((pre_current_delta + increment_delta) - observed_residual) <= 2e-4` componentwise. | H2 wins over H3 because it is the more specific split-component explanation. |
| `h3_post_update_route_residual` | Values match, component-sum reconstruction fails tolerance, and `abs(post_update_delta - observed_residual) <= 2e-4` componentwise. | H3 is admissible only if H2 fails. |
| `inconclusive_h4_next_boundary_nominated` | H1-H3 are not satisfied, and explanatory-only boundary or same-tape state-adjoint diagnostics name a narrower upstream boundary. | H4 is not promoted as a peer hypothesis in this probe; it only nominates the next debugging target. |
| `inconclusive_no_unique_hypothesis` | The run technically succeeds but multiple non-ordered interpretations remain, no admissible outcome is found, or explanatory diagnostics do not nominate a narrower boundary. | No hypothesis is promoted; the result must name the next smallest discriminating probe. |

If the ordered decision table yields anything other than exactly one admissible
promoted outcome among H1-H3, execution is non-promoting. Boundary and same-tape
state-adjoint diagnostics cannot override H1-H3 or break ties except by naming a
future probe under the H4 nomination outcome.

Veto diagnostics:

- FilterFlow subprocess cannot run.
- BayesFilter TF/TFP path cannot run CPU-only.
- FilterFlow reference status or fingerprint validation fails.
- Values violate `post_update_log_likelihoods =
  pre_current_log_likelihoods + increment` before gradient interpretation.
- Scalar values or resampling flags disagree.
- Any tested gradient row is non-finite.
- JSON validation fails.
- The probe writes outside the allowed lane.

Explanatory-only diagnostics:

- Within-side post-update additivity gaps.
- Boundary-mode gradients for BayesFilter-only stop-gradient controls.
- Same-tape state-adjoint identity residuals.
- Per-field maximum and sum deltas.

Non-conclusions:

- No claim that BayesFilter or FilterFlow is mathematically correct.
- No claim of analytic smoothness-gradient correctness.
- No production readiness, public API readiness, posterior correctness, HMC
  readiness, DSGE/NAWM validation, banking/model-risk claim, or monograph claim.
- No mutation of FilterFlow source and no claim about pristine upstream
  FilterFlow.
- No extrapolation from row `173`, time `93` to other rows, times, horizons,
  datasets, parameter settings, models, or the global BayesFilter-vs-FilterFlow
  smoothness-gradient discrepancy.

## Exact Input Manifest

The runner must emit all input identifiers below into the JSON output and use
them to prove same-input replay.

| Input | Source and required recorded evidence |
| --- | --- |
| Row index | `173`, the smoothness mesh row recorded in `run_filterflow_float64_row_173_vjp_decomposition_tf.py::MESH_INDEX` and prior row-173 artifacts. |
| Target time | `93`, passed through `RunConfig.target_time_index` and reflected in the artifact tag `row-173-post-update-route`. |
| Theta | `[0.9710526315789474, 0.9842105263157894]`, from `run_filterflow_float64_row_173_vjp_decomposition_tf.py::THETA`; record both numeric values and a stable digest. |
| Observations | Generated by local executable FilterFlow `scripts.simple_linear_smoothness.get_data` with `DATA_SEED=123`; record checksum and stable digest of the observation tensor. |
| Initial particles/state | Generated by the same FilterFlow subprocess with `rng.normal(0.0, 0.01, [1, 50, 2])` after data generation; record checksum and stable digest. |
| Seeds | `DATA_SEED=123`, `FILTER_SEED=1234`, and TensorFlow split-seed protocol from the VJP helper; record all seed values. |
| Resampling/ancestry | RegularisedTransform transport matrix and resampling flags at time `93`; record flag values, transport matrix shape, and stable digest. |
| Dtype | `float64` for both the local FilterFlow comparator and BayesFilter TF/TFP replay. |
| Covariance convention | Executable FilterFlow constant-velocity LGSSM covariance convention from the VJP helper: transition covariance `[[1/3, 0.5], [0.5, 1.0]]`, observation covariance `[[0.01]]`. |
| Comparator | Local checkout at `.localsource/filterflow`; record path, branch marker, commit SHA when available, dirty status, and hashes or mtimes for the executed comparator entrypoints/config files. |
| Prior localization artifact | `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_adjacent_boundary_2026-06-04.json`; record its decision and observed residual as the baseline residual being decomposed. |

Execution must stop on comparator drift relative to the baseline artifact and
current fingerprint. The drift check must include the local FilterFlow checkout
path, commit SHA when available, dirty status, branch marker, and hashes or
mtimes for the comparator entrypoints/configs used by the probe.

## Four Hypotheses

H1. Value/addition mismatch: the residual is caused by a value-path mismatch in
`post_update_log_likelihoods = pre_current_log_likelihoods + increment`. If this
is true, stop gradient interpretation and repair value replay first.

H2. Split-component mismatch: the residual is caused by the
`pre_current_log_likelihoods` or `increment` parameter-path components
themselves. If this is true, the sum of the component deltas should reconstruct
the observed residual.

H3. Post-update route/tape-topology mismatch: values and split components match,
but the full `post_update_log_likelihoods` parameter route carries a side-
specific graph residual. If this is true, the post-update row reconstructs the
observed residual while the component-row deltas remain near tolerance.

H4. Upstream carried-state/transport boundary nomination: the post-update route
residual may be an adjacent symptom of the resampling/post-state tape topology
or carried cumulative-likelihood state routing. In this probe H4 cannot be
promoted as a peer explanation; same-tape state-adjoint residuals and
BayesFilter boundary modes may only nominate a more specific upstream boundary
for the next reviewed diagnostic.

## Planned Probe

Create:

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_post_update_route_probe_tf.py`
- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-post-update-route-hypotheses-result-2026-06-04.md`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-post-update-route-hypotheses-2026-06-04.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_post_update_route_hypotheses_2026-06-04.json`
- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-post-update-route-hypotheses-review-loop-2026-06-04.md`

The runner will:

1. Reuse the existing row-173/time-93 VJP helper to execute the local float64
   FilterFlow subprocess and the BayesFilter TF/TFP replay path.
2. Check value addition for `post_update_log_likelihoods`,
   `pre_current_log_likelihoods`, and `increment` on both sides.
3. Compare parameter-path rows for those three fields and compute:
   `post_update_delta`, `pre_current_delta + increment_delta`, and the residual
   after each reconstruction.
4. Compare within-side post-update route gaps:
   `post_update - (pre_current + increment)` for each implementation and the
   delta between those gaps.
5. Reuse BayesFilter boundary modes from the VJP helper to test whether carried
   log-likelihood, carried log-weight, transport-gradient, or proposal-sample
   boundaries reduce the residual against FilterFlow.
6. Record same-tape state-adjoint identity summaries as explanatory evidence
   for the next boundary.
7. Record a full manifest: git branch/commit/dirty summary, exact command,
   Python/package versions, CPU-only status before TensorFlow import, visible
   GPU list, seeds, wall time, output paths, plan path, and result path.

## Required JSON Schema

The output JSON must contain at least:

- `decision`, `hypothesis_classification`, `hypothesis_reason`, and
  `veto_status_table`;
- `manifest` or `run_manifest` with exact command, git branch/commit/dirty
  summary, Python/package versions, CPU-only pre-import status, informational
  visible GPU list, seeds, wall time, plan/result/report/JSON paths;
- `input_manifest` with row/time/theta hashes, observation checksum/digest,
  initial-particle checksum/digest, dtype, covariance convention, resampling
  flag, transport matrix digest, comparator path, comparator commit/dirty
  status, and prior adjacent-boundary artifact decision/residual;
- `comparator_fingerprint` with local FilterFlow checkout path, branch marker,
  commit SHA when available, dirty status, and hashes or mtimes for the
  executed comparator entrypoints/configs;
- scalar equality and resampling gate results;
- per-field values for `post_update_log_likelihoods`,
  `pre_current_log_likelihoods`, and `increment` for both implementations;
- per-field parameter-path gradient rows for both implementations;
- `observed_residual`, `post_update_delta`, `pre_current_delta`,
  `increment_delta`, `component_sum_delta`;
- reconstruction residuals for the post-update and component-sum routes;
- within-side additivity gaps;
- boundary-mode summary table;
- same-tape state-adjoint summary table;
- final decision table and non-implications.

## Skeptical Pre-Execution Audit

- Stale context: the direct-theta probe ruled out frozen current-step direct
  arithmetic, and the adjacent-boundary probe localized the full residual to
  `post_update_log_likelihoods`. This plan starts there.
- Wrong baseline: compare only to the local executable float64 FilterFlow
  checkout.
- Proxy metric risk: finite gradients and boundary-mode improvements are
  diagnostics, not correctness proof.
- Fairness: use the same row/time, theta, observations, particles, seeds,
  dtype, covariance convention, and executable FilterFlow comparator.
- Stop conditions: stop on subprocess failure, reference drift, scalar/value
  mismatch, non-finite rows, JSON failure, lane contamination, or unresolved
  material Claude/Codex disagreement.
- Ambiguity stop: if the ordered decision rule does not yield exactly one
  admissible promoted outcome among H1-H3, the result is non-promoting and must
  record `inconclusive_*` plus the next smallest discriminating probe.
- Hidden drift: do not edit production, tests, chapters, highdim, vendored code,
  DSGE/NAWM, or FilterFlow source.
- Artifact fit: the proposed artifacts answer which of the four route
  hypotheses is supported for this row/time; they do not answer global gradient
  correctness.

The audit passes for execution planning because the probe is a narrow
difference-audit cut-set and its vetoes prevent correctness overclaiming.

## Verification Commands

Plan and result review:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Codex must run Claude review with trusted/elevated permissions. Non-escalated
Claude hangs, auth failures, missing output, or network failures are sandbox
evidence only and cannot be treated as review evidence.

Every BayesFilter Python invocation in this audit must set
`CUDA_VISIBLE_DEVICES=-1` before interpreter start, and every runner must also
set it before TensorFlow import. The artifact must record that CPU-only
execution was intentionally forced before TensorFlow import. Any visible GPU
list recorded under CPU-only execution is informational only and is not evidence
about the machine CUDA/GPU setup. No GPU/CUDA probing is required for this
CPU-only audit lane.

Execution:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_post_update_route_probe_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_post_update_route_probe_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_post_update_route_probe_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_post_update_route_hypotheses_2026-06-04.json
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_post_update_route_probe_tf.py
rg -n "student|highdim|DSGE|NAWM|\\.localsource" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_post_update_route_probe_tf.py
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_post_update_route_probe_tf.py docs/plans/bayesfilter-dpf-filterflow-float64-row-173-post-update-route-hypotheses-plan-2026-06-04.md docs/plans/bayesfilter-dpf-filterflow-float64-row-173-post-update-route-hypotheses-result-2026-06-04.md docs/plans/bayesfilter-dpf-filterflow-float64-row-173-post-update-route-hypotheses-review-loop-2026-06-04.md
git status --short -- bayesfilter tests docs/chapters .localsource/filterflow
git status --short -- bayesfilter tests docs/chapters .localsource/filterflow third_party experiments/controlled_dpf_baseline docs/plans/bayesfilter-highdim-nonlinear-filtering-* docs/plans/*DSGE* docs/plans/*NAWM*
git status --short --branch
```

Before execution is approved, the review-loop artifact must explicitly confirm
lane-boundary cleanliness for all forbidden roots named in this plan:
`bayesfilter/`, `tests/`, `docs/chapters/`, `.localsource/filterflow/`,
vendored/student roots, high-dimensional lane artifact roots, and DSGE/NAWM
roots. Pre-existing unrelated dirty files may be recorded but not reverted.

## Claude Review Protocol

Use exactly:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Plan-review prompt template:

```text
Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-post-update-route-hypotheses-plan-2026-06-04.md plus AGENTS.md and CLAUDE.md read-only. Review whether the plan is adequate to test the four post-update route hypotheses under the BayesFilter-vs-local-float64-FilterFlow difference-audit governance. Check evidence contract, exact inputs/outputs, lane boundaries, CPU-only controls, stop conditions, non-conclusions, exact decision rule, and Claude/Codex finding-classification rules. Output ACCEPT or REJECT first. If REJECT, list findings with exact required controls. Do not edit files.
```

Result-review prompt template:

```text
Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-post-update-route-hypotheses-result-2026-06-04.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-post-update-route-hypotheses-plan-2026-06-04.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-post-update-route-hypotheses-review-loop-2026-06-04.md, and experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_post_update_route_probe_tf.py read-only. Review whether the result follows the accepted plan, uses the ordered decision rule correctly, preserves difference-audit governance, records exact inputs/outputs, lane-boundary and CPU-only controls, and avoids non-concluded claims. Output ACCEPT or REJECT first. If REJECT, list exact required controls. Do not edit files.
```

Claude reviews read-only and returns `ACCEPT` or `REJECT` with findings. Claude
must be launched in trusted/elevated execution per the cross-agent policy. Codex
must independently classify every Claude finding as `ACCEPT`, `PARTIAL`,
`DISPUTE`, or `CLARIFY` in the review-loop artifact. Accepted or partially
accepted findings must be patched with the exact control recorded. Disputed
findings must receive a concise rebuttal in the next Claude prompt. Loop until
`ACCEPT` or max five rounds. If a major blocker remains after round five, block
execution pending human direction.

After execution, repeat the same review loop for the result artifact.
