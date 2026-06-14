# Plan: R1 Observation-Path Mismatch Hypothesis Test

## Scope

This plan tests hypotheses for the first accepted BayesFilter/filterflow
mismatch found in the 1D-to-smoothness agreement ladder:
`R1_1d_T100_filterflow_observation_path / T100_filterflow_observation_path`.
The question is cross-implementation agreement only. It does not assert that
BayesFilter or filterflow is mathematically correct.

Lane boundary: BayesFilter-owned DPF implementation/evidence lane only. Do not
edit production `bayesfilter/`, `tests/`, monograph chapters under
`docs/chapters/`, high-dimensional nonlinear filtering lane artifacts,
student/vendored code, DSGE/NAWM artifacts, or `.localsource/filterflow`
source. Keep BayesFilter-owned implementation under
`experiments/dpf_implementation/tf_tfp/`; keep reports under
`experiments/dpf_implementation/reports/` and `docs/plans/`.

## Evidence Contract

Primary question: which concrete mechanism explains the R1 mismatch between
BayesFilter TF/TFP annealed transport and the local executable filterflow
reference when only the observation path is swapped to the filterflow
T=100 path?

Primary comparator: current local patched executable filterflow checkout under
`.localsource/filterflow`, identified by HEAD commit plus local diff/status
fingerprint. The branch string is descriptive only.

Primary criterion: a hypothesis status is assigned by hypothesis class.
All support classes require:

- the same-harness `generated_T100` matched-control arm passes
  BayesFilter/filterflow agreement;
- the unscaled R1 observation-path arm reproduces the accepted R1 mismatch;
- the diagnostic does not mutate filterflow source.

Additional class-specific support rules:

- intervention hypotheses H1/H2/H7 require a targeted diagnostic to change the
  BayesFilter/filterflow delta in the predeclared predicted direction;
- localization hypotheses H3/H4/H5 require the predeclared first-failure
  structure to isolate the mismatch mechanism under the unscaled R1 path;
- scalar-scale hypothesis H6 requires the predeclared absolute-vs-relative
  scalar pattern under the unscaled R1 path;
- audit hypothesis H8 is not eligible for `supported` without a future
  executable A/B diagnostic; this plan records only `audit_risk_identified`,
  `audit_risk_not_found`, or `inconclusive`.

If the evidence identifies only a first failing time/field set but not a
delta-changing mechanism, the result may record `localized_unexplained`.

Veto diagnostics:

- filterflow subprocess blocker;
- nonfinite scalar, gradient, weights, particles, or transport matrix;
- CPU-only manifest failure for TensorFlow runs;
- comparator fingerprint drift during execution;
- forbidden path/import use;
- hidden mutation of `.localsource/filterflow`;
- result artifacts that change the comparison question from
  BayesFilter-vs-filterflow agreement to correctness of either implementation.

Explanatory-only diagnostics:

- absolute transport residual magnitude when shared;
- relative scalar delta unless predeclared as an explanatory scale diagnostic;
- gradient AD-vs-FD agreement;
- runtime;
- filtered-state RMSE or Kalman agreement.

Not concluded even if a hypothesis is supported:

- production readiness;
- public API readiness;
- posterior correctness;
- HMC readiness;
- general nonlinear-SSM validity;
- DSGE/NAWM validation;
- banking/model-risk claims;
- monograph claims;
- correctness of either implementation;
- gradient correctness.

Artifact preserving the result:

- `docs/plans/bayesfilter-dpf-r1-observation-path-mismatch-hypothesis-result-2026-06-02.md`
- `experiments/dpf_implementation/reports/dpf-filterflow-r1-observation-path-mismatch-localization-2026-06-02.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_r1_observation_path_mismatch_localization_2026-06-02.json`

## Hypotheses

| ID | Hypothesis | Predicted evidence | Primary test |
| --- | --- | --- | --- |
| H1 | Float32/float64 mismatch drives the R1 scalar and ledger deltas. filterflow runs `tf.float32`; the BayesFilter mirror currently runs `tf.float64`. | A BayesFilter float32 mirror reduces scalar, ledger, and residual deltas materially versus BayesFilter float64. | Run BayesFilter mirror in both float64 and float32 against the same filterflow subprocess payload. |
| H2 | The filterflow observation path creates a scale/outlier stress that turns tiny per-step numeric differences into absolute scalar failures. | The relative scalar delta remains small while absolute scalar delta grows with observation scale; scaled observations reduce absolute deltas. | Compare observation scales `1.0`, `0.1`, and `0.01` using the same initial particles and transition-noise ledger. |
| H3 | The mismatch begins at a specific prefix/time rather than being a uniform whole-horizon drift. | Prefix ladder identifies the first `T` and per-time ledger field where tolerance first fails. | Run prefixes `T=1,2,4,8,16,32,64,100`; record first failing time and field. |
| H4 | Transport residual convergence semantics differ between the reusable TF component and executable filterflow under the R1 path. | First mismatch occurs at a resampling step; row/column residual deltas and transport-matrix deltas spike at the same time. | Record ESS, flags, transport matrix delta, residual deltas, and iteration count where available for each prefix/time. |
| H5 | Cost scaling or near-degenerate particle clouds create different normalized cost matrices. | The first failing field is `transport_cost_matrix`, or cost-scale diagnostics differ before transport/output deltas. | Record per-time max deltas for cost matrix, particles before transport, and post-transport particles. |
| H6 | The fixed absolute scalar tolerance is inappropriate for the R1 scalar scale, but the implementations may still agree relatively. | Scalar relative delta is near float32 precision while ledger field deltas may remain small or dtype-localized. | Report both absolute and relative scalar deltas, without changing the promotion criterion. |
| H7 | The scalar 1D stress fixture is intentionally mismatched to the 2D filterflow-generated observation process, producing extreme observations that expose numeric sensitivity. | Observation magnitude summaries are much larger than the controlled generated 1D paths; scaling reduces deltas but does not prove correctness. | Record min/max/RMS observation summaries and scale ladder deltas. |
| H8 | The filterflow subprocess wrapper might not mirror the same executable transport/cost path after observation substitution. | A source-inspection/wrapper audit finds or rules out wrapper risk; this is audit-localization only unless paired with an executable A/B diagnostic. | Compare wrapper script constants and imported filterflow utilities; record digest and source paths inspected. |

## Hypothesis Status Rubric

All thresholds below are cross-implementation diagnostics, not correctness
criteria. `generated_T100` matched-control failure blocks all mechanism
promotion and yields `harness_control_failed`.

| Hypothesis | Supported | Partially supported | Weakened | Inconclusive |
| --- | --- | --- | --- | --- |
| H1 dtype | BayesFilter float32 reduces scalar delta and max ledger delta by at least 10x versus float64, and float32 scalar plus ledger deltas are within existing tolerances. | Float32 reduces scalar delta or max ledger delta by at least 10x, but one promoted tolerance still fails. | Float32 does not reduce both scalar and max ledger deltas by at least 2x. | filterflow or BF32 diagnostic blocked. |
| H2 observation scale | BF64 scale `0.1` and `0.01` reduce absolute scalar delta by at least the square of the scale factor within a factor of 5, and each scaled BF64 first-failing field set intersects the unscaled BF64 first-failing field set. | BF64 scaling reduces scalar delta monotonically but not by the threshold above, or only one scaled arm's first-failing field set intersects the unscaled field set. | BF64 scaling does not monotonically reduce scalar delta. | matched-control or scale arm blocked. |
| H3 prefix/time | A first failing prefix, first failing time, and nonempty first failing field set are identified under unscaled R1. | A first failing prefix is identified, but time/field-set extraction is incomplete. | No failing prefix is reproduced despite full R1 mismatch previously accepted. | filterflow or prefix diagnostic blocked. |
| H4 transport convergence | The unscaled first failing field set includes `transport_matrix`, `post_transport_particles`, `row_residual`, or `column_residual` at a triggered resampling step, and transport/residual delta exceeds `5e-5` before scalar-only failure. | Transport/residual fields fail at the first failing time but only alongside a non-transport upstream field. | First failure occurs before any triggered transport field or no residual delta exceeds `5e-5`. | no triggered step in prefix where mismatch occurs. |
| H5 cost scaling | The unscaled first failing field set includes `transport_cost_matrix`, or its max delta exceeds `5e-5` before transport/post-transport deltas. | Cost matrix delta exceeds tolerance at the same first failing time as transport matrix. | Cost matrix remains within tolerance before transport/output failure. | cost diagnostic unavailable. |
| H6 scalar tolerance | Absolute scalar delta fails while relative scalar delta is below `5e-7`, matched-control passes, and promoted ledger fields except scalar/residual deltas are within tolerance. | Relative scalar delta is below `5e-7`, but one or more ledger fields also fail. | Relative scalar delta is at least `5e-7`. | scalar values unavailable or nonfinite. |
| H7 fixture stress | R1 observation RMS is at least 10x the matched-control observation RMS, and scale diagnostics reduce scalar delta monotonically. | Observation RMS is at least 3x matched-control RMS or scaling is monotone, but not both threshold criteria. | Observation RMS is less than 3x matched-control RMS and scaling is not monotone. | fixture summaries unavailable. |
| H8 wrapper audit | Not eligible for `supported` without executable A/B evidence. | `audit_risk_identified` if constants/imported utilities differ from the canonical wrapper contract. | `audit_risk_not_found` if constants/imported utilities match the canonical wrapper contract. | source inspection blocked. |

Allowed hypothesis statuses:

- `supported`
- `partially_supported`
- `weakened`
- `inconclusive`
- `not_tested_blocked`
- `localized_unexplained`
- `harness_control_failed`
- `audit_risk_identified`
- `audit_risk_not_found`

## Test Plan

1. Reuse the accepted R1 fixture:
   - observations from local executable filterflow `simple_linear_smoothness.get_data`,
     scalar first coordinate, `T=100`, `data_seed=123`;
   - initial particles from the matched controlled 1D audit unless a diagnostic
     explicitly labels otherwise;
   - transition-noise ledger from existing controlled `generated_T100`, not
     from the filterflow fixture;
   - `theta=0.7`, `Q=0.04`, `R=0.04`, `N=4`, `epsilon=0.25`,
     `scaling=0.9`, `convergence_threshold=1e-6`, `max_iterations=200`.

2. Run a same-harness matched-control arm using the original controlled
   `generated_T100` observation path and transition-noise ledger. This control
   must pass scalar, ledger, trigger, and residual-delta agreement before any
   mechanism can be marked `supported` or `partially_supported`.

3. Run the unscaled R1 observation-path arm and confirm it reproduces the
   accepted R1 mismatch. If it does not reproduce, stop with
   `r1_mismatch_not_reproduced`.

4. Run a prefix ladder on the same observation path:
   `T in [1, 2, 4, 8, 16, 32, 64, 100]`.

5. For each prefix, compare filterflow against:
   - BayesFilter float64 mirror;
   - BayesFilter float32 mirror.

6. Run observation-scale diagnostics for scale factors `[1.0, 0.1, 0.01]`.
   The primary H2/H7 scale-promotion dtype is the BayesFilter float64 mirror,
   matching the current BayesFilter diagnostic implementation. BayesFilter
   float32 scale results are recorded as H1 sensitivity only and cannot promote
   H2/H7 unless a future reviewed plan changes the dtype contract. Scale
   diagnostics can support only H2/H7 scale-sensitivity. They cannot by
   themselves explain the unscaled R1 mismatch unless the unscaled first
   failing field is reproduced under BF64 and the same field remains the first
   failing field on the scaled BF64 arms.

7. Record first failing time and first failing field set among:
   `pre_particles`, `pre_log_weights`, `ess`, `transport_cost_matrix`,
   `transport_matrix`, `post_transport_particles`,
   `post_transport_log_weights`, `predicted_particles`,
   `observation_log_likelihoods`, `unnormalized_log_weights`,
   `per_step_log_normalizer`, `post_update_log_weights`, `row_residual`,
   `column_residual`.

   Simultaneous-failure policy: the first failing time is the earliest time
   index where one or more fields exceed tolerance. The first failing field set
   is the set of all fields exceeding tolerance at that same time. Hypothesis
   labels must use set membership rather than arbitrary field-list ordering.

8. Record hypothesis statuses using only the allowed status taxonomy above.

9. If H1 is supported and the float32 mirror matches filterflow, do not
   silently change the BayesFilter default dtype. Record the exact minimal next
   action as a reviewed dtype-contract decision.

10. If only H6 is supported, do not change pass/fail tolerances in this result.
   Record the exact minimal next action as a reviewed tolerance-contract
   decision.

## Allowed And Forbidden Write Sets

Allowed:

- `docs/plans/bayesfilter-dpf-r1-observation-path-mismatch-hypothesis-plan-2026-06-02.md`
- `docs/plans/bayesfilter-dpf-r1-observation-path-mismatch-hypothesis-result-2026-06-02.md`
- `docs/plans/bayesfilter-dpf-r1-observation-path-mismatch-hypothesis-review-loop-2026-06-02.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r1_observation_path_mismatch_localization_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-r1-observation-path-mismatch-localization-2026-06-02.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_r1_observation_path_mismatch_localization_2026-06-02.json`

Forbidden:

- production `bayesfilter/`;
- `tests/`;
- `docs/chapters/`;
- high-dimensional nonlinear filtering lane artifacts;
- student/vendored code;
- DSGE/NAWM-specific artifacts;
- `.localsource/filterflow` source.

## Skeptical Pre-Execution Audit

- Stale context risk: use the accepted R1 result and runner from
  2026-06-02, not older filterflow comparison artifacts.
- Wrong goal risk: the diagnostics test BayesFilter/filterflow difference,
  not correctness of either implementation.
- Wrong baseline risk: the canonical comparator is the local patched
  executable filterflow checkout, not pristine upstream and not student code.
- Fixture drift risk: R1 transition noises must come from the accepted
  controlled `generated_T100` ledger; filterflow fixture transition noises
  must not enter this diagnostic.
- Proxy risk: relative scalar delta and shared residual magnitude are
  explanatory only.
- Dtype risk: BayesFilter float32 mirror is a diagnostic path, not a default
  implementation policy change.
- Hidden drift risk: record filterflow fingerprints before and after.
- Artifact relevance: result must name supported/weakened hypotheses and the
  first failing prefix/time/field, or a structured blocker.
- Harness-control risk: a new runner must first demonstrate that it preserves
  the known matched `generated_T100` control; otherwise downstream hypothesis
  labels are blocked.
- Post hoc threshold risk: use the predeclared rubric above; do not invent a
  new support threshold after observing results.

Audit status: proceed to Claude review before execution.

## Stop Conditions

- exact Claude command unavailable;
- TF/TFP unavailable;
- filterflow executable environment unavailable;
- implementing the diagnostic requires mutating `.localsource/filterflow`;
- implementing the diagnostic requires NumPy as BayesFilter algorithmic
  backend rather than only fixture/reporting use;
- comparator fingerprint changes during execution;
- CPU-only manifest fails for TensorFlow runs;
- forbidden write/import is needed;
- unresolved Claude/Codex disagreement after 5 rounds without human
  authorization.

## Claude Review Protocol

Use Claude Code exactly as:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Claude must return `ACCEPT` or `REJECT` with findings. Codex independently
classifies every finding as `ACCEPT`, `PARTIAL`, `DISPUTE`, or `CLARIFY`.
Patch accepted/partial findings and resubmit until `ACCEPT` or max 5 rounds.
If Codex disputes a finding, include the rebuttal in the next Claude prompt.
Use the same protocol for the result. On round 5, do not silently promote a
rejected plan/result; record inspection-only status unless the human explicitly
authorizes downstream use.

## Verification

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r1_observation_path_mismatch_localization_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_r1_observation_path_mismatch_localization_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_r1_observation_path_mismatch_localization_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_r1_observation_path_mismatch_localization_2026-06-02.json
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r1_observation_path_mismatch_localization_tf.py
rg -n "student|vendored|highdim|DSGE|NAWM|docs/chapters|bayesfilter/" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r1_observation_path_mismatch_localization_tf.py docs/plans/bayesfilter-dpf-r1-observation-path-mismatch-hypothesis-plan-2026-06-02.md docs/plans/bayesfilter-dpf-r1-observation-path-mismatch-hypothesis-result-2026-06-02.md
python -c "from pathlib import Path; paths=[Path('docs/plans/bayesfilter-dpf-r1-observation-path-mismatch-hypothesis-plan-2026-06-02.md'),Path('docs/plans/bayesfilter-dpf-r1-observation-path-mismatch-hypothesis-result-2026-06-02.md'),Path('docs/plans/bayesfilter-dpf-r1-observation-path-mismatch-hypothesis-review-loop-2026-06-02.md'),Path('experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r1_observation_path_mismatch_localization_tf.py'),Path('experiments/dpf_implementation/reports/dpf-filterflow-r1-observation-path-mismatch-localization-2026-06-02.md')]; bad=[str(p) for p in paths if p.exists() and any(line.rstrip('\\n').rstrip('\\r') != line.rstrip('\\n').rstrip('\\r').rstrip(' \\t') for line in p.read_text().splitlines(True))]; print(bad); raise SystemExit(bool(bad))"
git diff --check
git status --short -- bayesfilter tests docs/chapters
git status --short --branch
```

The NumPy import gate may report `import numpy` only inside embedded
filterflow/reference subprocess code or lightweight reporting fixtures. Any
BayesFilter algorithmic path in the runner must use TensorFlow.
