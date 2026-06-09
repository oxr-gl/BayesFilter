# Visible Execution Ledger: DPF Filter Oracle Comparison

metadata_date: 2026-06-08
status: `PASS_P0_TARGET_ROUTE_REGISTRY_READY_FOR_P1`

## Role Contract

Codex is supervisor and executor in this dialogue.

Claude is a read-only critical reviewer only.

No detached supervisor, copied workspace, background phase runner, or nested
agent execution is authorized by this visible ledger.

## 2026-06-08 - P0 - PRECHECK

Evidence contract:

- Question: which target-route pairs can support later DPF value and gradient
  comparisons, and with what claim class?
- Baseline/comparator: P42 validation rules, P45 registry schema pattern, and
  local code/document inventory.
- Primary criterion: create and validate a registry with target identity,
  route identity, claim class, tolerance/certification fields, gradient
  statistic, blockers, and P1-P5 eligibility.
- Veto diagnostics: missing target identity, missing route status, missing
  tolerance/certification band, missing gradient statistic for
  gradient-eligible rows, approximate route labeled exact, blocked route
  silently omitted, or DPF row declared comparable without seed/evaluator
  variance policy.
- Non-claims: P0 does not run numerical filters and does not establish value,
  gradient, HMC, production, GPU, or paper-scale evidence.

Skeptical audit:

- Wrong-baseline risk is controlled by making P0 a registry/classification
  phase only.
- Proxy-promotion risk is controlled by requiring `promotion_tolerance`,
  `certification_band`, and `primary_gradient_statistic` before later
  execution.
- Missing-stop-condition risk is controlled by explicit `BLOCKED` rows and
  the max-five Claude review loop.
- Environment risk is low for P0 because the registry validator is expected to
  be pure Python/JSON unless the phase records a reviewed TensorFlow need.

Actions:

- Created visible runbook and visible execution ledger.

Artifacts:

- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-gated-execution-runbook-2026-06-08.md`
- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md`

Gate status:

- `P0_PRECHECK_PASSED_VALIDATION_PENDING_CLAUDE_REVIEW`

Next action:

- Run Claude read-only P0 gate review.

## 2026-06-08 - P0 - EXECUTE_MINIMAL

Actions:

- Added pure-Python P0 validator:
  `experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p0_registry_tf.py`
- Generated registry:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-target-route-registry-2026-06-08.json`
- Generated summary:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p0_target_route_registry_2026-06-08.json`

Commands:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p0_registry_tf.py
python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p0_registry_tf --write-seed-registry --validate-only
python -m json.tool docs/plans/bayesfilter-dpf-filter-oracle-comparison-target-route-registry-2026-06-08.json
python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p0_registry_tf
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p0_target_route_registry_2026-06-08.json
```

Observed validator output:

```text
P0_REGISTRY_VALID targets=13 route_rows=104 blocked_rows=58
```

Validation summary:

| Metric | Value |
| --- | ---: |
| Targets | 13 |
| Route rows | 104 |
| Blocked rows | 58 |
| DPF rows with seed/evaluator policy | 8 |

Claim-class counts:

| Claim class | Count |
| --- | ---: |
| `EXACT_ORACLE` | 6 |
| `CERTIFIED_APPROXIMATION` | 7 |
| `SURROGATE_USEFULNESS` | 2 |
| `DIAGNOSTIC_ONLY` | 31 |
| `BLOCKED` | 58 |

Gate status:

- `P0_VALIDATED_PENDING_CLAUDE_REVIEW`

Next action:

- Run Claude read-only P0 gate review, max five iterations.

## 2026-06-08 - P0 - CLAUDE_REVIEW_ITERATION_1

Claude status: `VERDICT: REVISE`.

Accepted findings:

- Registry JSON needed a top-level `run_manifest`.
- Summary JSON and markdown result needed the same manifest fields.
- `lgssm_2d_h25_rich/kalman_exact` incorrectly carried DPF seed/evaluator
  policy because policy assignment keyed on `"dpf"` in `route_path`.

Repairs:

- Added top-level registry manifest generation and validation.
- Expanded the JSON manifest to include environment, seeds, particle counts,
  data version, registry path, summary/output path, plan path, and result path.
- Replaced path-string DPF detection with route-id-based policy assignment.
- Added validator checks that reject DPF execution policy on non-DPF rows.

Repair validation:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p0_registry_tf.py
python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p0_registry_tf --write-seed-registry --validate-only
python -m json.tool docs/plans/bayesfilter-dpf-filter-oracle-comparison-target-route-registry-2026-06-08.json
python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p0_registry_tf
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p0_target_route_registry_2026-06-08.json
```

Observed validator output:

```text
P0_REGISTRY_VALID targets=13 route_rows=104 blocked_rows=58
```

Gate status:

- `P0_REVALIDATED_AFTER_CLAUDE_REVISE_PENDING_REVIEW_ITERATION_2`

Next action:

- Run Claude read-only P0 gate review iteration 2.

## 2026-06-08 - P0 - CLAUDE_REVIEW_ITERATION_2

Claude status: `REVIEW_EXECUTION_HUNG_STOPPED_NO_VERDICT`.

Observation:

- The read-only Claude process remained alive for more than eight minutes with
  no output.

Control:

- Stopped only the stuck iteration-2 review process.
- No P0 pass/fail evidence is inferred from the hung call.
- Retry with a smaller read-only prompt as iteration 2b.

Gate status:

- `P0_REVALIDATED_AFTER_CLAUDE_REVISE_PENDING_REVIEW_ITERATION_2B`

Next action:

- Run Claude read-only P0 gate review iteration 2b.

## 2026-06-08 - P0 - CLAUDE_REVIEW_ITERATION_2B

Claude status: `VERDICT: AGREE`.

Findings:

- No material P0 blockers found.
- Iteration-1 manifest and seed-policy blockers were resolved.

Codex decision:

- Accept Claude iteration-2b agreement.
- P0 exits `PASS_P0_TARGET_ROUTE_REGISTRY_READY_FOR_P1`.

Gate status:

- `PASS_P0_TARGET_ROUTE_REGISTRY_READY_FOR_P1`

Next action:

- Start P1 LGSSM exact-oracle precheck in this visible dialogue. Do not run P1
  numerical commands until the P1 evidence contract and skeptical audit are
  recorded.

## 2026-06-08 - P1 - PRECHECK

Evidence contract:

- Question: for the P0 LGSSM row, are DPF bootstrap-OT and LEDH-PFPF-OT value
  and fixed-branch gradient estimates close to exact Kalman value and analytic
  Kalman gradient in the same parameterization?
- Baseline/comparator: exact Kalman log likelihood and `reference_score`
  gradient for `lgssm_2d_h25_rich` with parameters
  `(transition_matrix_scale, observation_noise_scale)`.
- Primary criterion: write P1 JSON, markdown report, and phase result with
  Kalman value/gradient reference validation, deterministic sanity-route
  classification, DPF paired seed/particle ladder metrics, evaluator variance,
  veto diagnostics, nonclaims, and a run manifest.
- Veto diagnostics: missing analytic Kalman gradient, parameterization
  mismatch, value sign/scalar mismatch, DPF fixed-branch gradient reported as
  stochastic score, evaluator variance omitted, value pass used to excuse
  gradient failure, or prior BF/FilterFlow agreement treated as oracle
  evidence.
- Explanatory diagnostics: ESS, resampling counts, Sinkhorn diagnostics,
  runtime, AD-vs-FD checks, and deterministic affine sanity route residuals.
- Nonclaims: P1 does not establish nonlinear-model correctness,
  stochastic-resampling distribution correctness, HMC readiness, production
  readiness, GPU readiness, or paper-scale claims.

Skeptical audit:

- Existing V2 DPF value/gradient runners are useful implementation plumbing but
  are not sufficient P1 evidence because they compare BayesFilter against a
  BayesFilter-owned FilterFlow-side adapter, not against Kalman.
- Existing V2 gradient runners use fixed branch contracts and do not establish
  stochastic-score correctness; P1 must preserve that distinction explicitly.
- The P1 runner must compute fresh same-target Kalman value and gradient in the
  declared `(transition_matrix_scale, observation_noise_scale)`
  parameterization and compare DPF outputs against that reference.
- TensorFlow numerical commands must be CPU-only with `CUDA_VISIBLE_DEVICES=-1`
  before TensorFlow import; GPU evidence is out of scope for P1.

Gate status:

- `P1_PRECHECK_IN_PROGRESS`

Next action:

- Implement or select a P1 runner that answers the exact-oracle question rather
  than reusing BF/FilterFlow agreement as oracle evidence.

## 2026-06-08 - P1 - EXECUTE_MINIMAL_ITERATION_1

Actions:

- Added focused P1 runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p1_lgssm_exact_oracle_tf.py`
- Ran P1 CPU-only TensorFlow command visibly.

First run issue:

- Initial execution failed on `_mvn_sample` scalar sample-shape handling.
- Patched `_mvn_sample` to use `tf.linalg.matvec` for rank-1 draws.

Second run status:

- Local P1 runner completed with
  `PASS_P1_LGSSM_EXACT_ORACLE_PENDING_CLAUDE_REVIEW`.
- Local validator passed.

Post-run skeptical audit:

- Material issue found before Claude review: the master stochastic evidence
  minimums require a third particle count when the larger of the first two
  counts fails to reduce value RMSE or score RMSE by at least 25%, or when CI
  diagnostics remain suspicious.
- The first P1 implementation used only `[32, 64]`, so it was insufficient for
  review.

Control:

- Patched the runner to include a third particle count `[32, 64, 128]` and to
  record third-count trigger reasons in `method_summaries`.

Gate status:

- `P1_RERUN_REQUIRED_AFTER_THIRD_PARTICLE_TRIGGER_AUDIT`

Next action:

- Rerun P1 CPU-only TensorFlow comparison with the corrected particle ladder.

## 2026-06-08 - P1 - EXECUTE_MINIMAL_FINAL

Actions:

- Reran P1 with particle counts `[32, 64, 128]` and five paired seeds.
- Generated JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p1_lgssm_exact_oracle_2026-06-08.json`
- Generated report:
  `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p1-lgssm-exact-oracle-2026-06-08.md`
- Generated phase result:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p1-lgssm-exact-oracle-result-2026-06-08.md`

Commands:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p1_lgssm_exact_oracle_tf
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p1_lgssm_exact_oracle_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p1_lgssm_exact_oracle_2026-06-08.json
```

Observed outputs:

```text
PASS_P1_LGSSM_EXACT_ORACLE_PENDING_CLAUDE_REVIEW
P1_LGSSM_EXACT_ORACLE_VALIDATED
```

Key results:

- Kalman log likelihood: `-17.140691771439727`.
- Kalman score:
  `[-5.594936987211544, -3.9076975934307616]`.
- Bootstrap-OT final tier `N=128`: value RMSE `0.8339700259704327`,
  score RMSE `3.311843492600966`, final value CI excludes zero, so P1
  interpretation is `P1_DIAGNOSTIC_OR_BIASED_EVIDENCE_PENDING_P5`.
- LEDH-PFPF-OT final tier `N=128`: value RMSE `0.3114821802004455`,
  score RMSE `1.4723557709307777`, final value CI includes zero, so P1
  interpretation is `P1_LOCAL_LGSSM_CLOSENESS_EVIDENCE_NOT_PROMOTION`.
- No P1 correctness promotion is claimed for either DPF method.
- Veto diagnostics are all false, including
  `third_particle_trigger_missing`.

Gate status:

- `PASS_P1_LGSSM_EXACT_ORACLE_PENDING_CLAUDE_REVIEW`

Next action:

- Run Claude read-only P1 gate review.

## 2026-06-08 - P1 - CLAUDE_REVIEW_ITERATION_1

Claude status: `VERDICT: REVISE`.

Accepted findings:

- Gradient evaluator variance was incomplete: value SE/CI was reported, but
  gradient SE/CI was not.
- Common-random-number and branch-freeze policies were not explicit enough for
  the master stochastic evidence contract.
- Markdown result/report lacked a standalone veto-diagnostics section and a
  full manifest summary aligned with the JSON.

Repairs:

- Added gradient mean error, coordinate SE/CI/RMSE, gradient-norm SE/CI, and
  validator checks.
- Added explicit `common_random_number_policy`, `branch_freeze_policy`, and
  `transport_branch_policy`.
- Added generated markdown sections for stochastic policy, veto diagnostics,
  fuller run manifest, and final gradient uncertainty.

Gate status:

- `P1_REPAIR_AFTER_REVIEW_ITERATION_1_IN_PROGRESS`

Next action:

- Rerun P1 CPU-only TensorFlow artifact generation and validation.

## 2026-06-08 - P1 - REPAIR_RERUN_AFTER_REVIEW_ITERATION_1

Actions:

- Reran the repaired P1 CPU-only TensorFlow artifact generation after accepting
  Claude iteration-1 findings.
- Confirmed the JSON now records gradient evaluator uncertainty, common random
  numbers, branch-freeze policy, transport-branch policy, standalone veto
  diagnostics, and a full run manifest.
- Ran local artifact sanity checks before review iteration 2.

Commands:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p1_lgssm_exact_oracle_tf
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p1_lgssm_exact_oracle_tf --validate-only
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p1_lgssm_exact_oracle_tf.py
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p1_lgssm_exact_oracle_2026-06-08.json
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p1_lgssm_exact_oracle_tf.py docs/plans/bayesfilter-dpf-filter-oracle-comparison-p1-lgssm-exact-oracle-result-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-p1-claude-review-ledger-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p1-lgssm-exact-oracle-2026-06-08.md experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p1_lgssm_exact_oracle_2026-06-08.json
```

Observed outputs:

```text
PASS_P1_LGSSM_EXACT_ORACLE_PENDING_CLAUDE_REVIEW
P1_LGSSM_EXACT_ORACLE_VALIDATED
```

Validation summary:

- `python -m py_compile` passed.
- `python -m json.tool` passed.
- `git diff --check` passed for the touched P1 artifacts.
- All P1 veto diagnostics are false, including
  `missing_evaluator_variance`, `common_random_number_policy_missing`, and
  `branch_freeze_policy_missing`.

Gate status:

- `P1_REPAIRED_AND_REVALIDATED_PENDING_CLAUDE_REVIEW_ITERATION_2`

Next action:

- Run Claude read-only P1 gate review iteration 2 in this visible dialogue.

## 2026-06-08 - P1 - CLAUDE_REVIEW_ITERATION_2

Claude status: `VERDICT: AGREE`.

Findings:

- Gradient evaluator variance/CI is now reported in JSON and markdown and
  validated by the P1 runner.
- Common-random-number, branch-freeze, and transport-branch policy are explicit
  in the stochastic contract; fixed-branch gradients are not overclaimed as
  stochastic scores.
- Markdown result/report now include standalone veto diagnostics and run
  manifest sections.
- No new material P1 blocker was found for oracle misuse, fixed-branch
  overclaim, missing third particle count, missing evaluator variance,
  environment mismatch, missing artifacts, or validator blind spots.
- Non-blocking hardening note: two policy-related veto booleans are hard-coded
  false in `_veto_diagnostics`, but `_validate_payload` separately enforces
  policy-field presence.

Codex decision:

- Accept Claude iteration-2 agreement.
- P1 exits `PASS_P1_LGSSM_EXACT_ORACLE_READY_FOR_P2`.
- Keep DPF method conclusions scoped: bootstrap-OT remains
  `P1_DIAGNOSTIC_OR_BIASED_EVIDENCE_PENDING_P5`; LEDH-PFPF-OT has
  `P1_LOCAL_LGSSM_CLOSENESS_EVIDENCE_NOT_PROMOTION`; neither receives P1
  correctness promotion.

Gate status:

- `PASS_P1_LGSSM_EXACT_ORACLE_READY_FOR_P2`

Next action:

- Start P2 tiny nonlinear dense-oracle precheck in this visible dialogue.

## 2026-06-08 - P2 - PRECHECK

Evidence contract:

- Question: for tiny nonlinear targets where dense/refined quadrature is
  feasible, can P2 promote at least one dense same-target reference row while
  reporting UKF, SVD/cubature, CUT4, and Zhao-Cui/fixed-design TT only in their
  P0 claim classes?
- Baseline/comparator: dense order-241 fixed quadrature after order-161
  refinement passes value and directional score tolerances on the selected
  P44-M2 cubic additive-Gaussian target.
- Primary criterion: at least one promoted dense-oracle row; all selected dims
  record dense refinement, deterministic route value/gradient gaps, P42-style
  directional finite-difference diagnostics, veto diagnostics, nonclaims, and
  a run manifest.
- Veto diagnostics: dense reference lacks refinement, DPF executed in P2,
  non-P2 route executed, UKF/SVD/CUT4 called oracle, nonfinite route,
  parameterization mismatch, or single-step finite differences used as a
  promotion gate.
- Explanatory diagnostics: point counts, route finite status, route gap sizes,
  multi-step directional finite differences, and TensorFlow startup warnings.
- Nonclaims: P2 does not establish DPF correctness, stochastic-resampling
  correctness, HMC readiness, production readiness, GPU readiness, or
  paper-scale claims.

Skeptical audit:

- Wrong-baseline risk is controlled by selecting only P0 rows where
  `dense_refined_quadrature` is `EXACT_ORACLE` and P2-eligible.
- Proxy-promotion risk is controlled by making dense refinement the oracle
  promotion criterion; finite values, FD checks, and point counts are
  diagnostics only.
- Missing-stop-condition risk is controlled by explicit veto diagnostics and
  the max-five Claude review loop.
- Unfair-comparison risk is controlled by deferring DPF rows to P5 because P0
  marks `dpf_bootstrap_ot` and `dpf_ledh_pfpf_ot` as `p2=false`, `p5=true` for
  the P44 tiny nonlinear targets.
- Environment risk is controlled by running TensorFlow CPU-only with
  `CUDA_VISIBLE_DEVICES=-1` before import; GPU evidence is out of scope.

Gate status:

- `P2_PRECHECK_PASSED_READY_TO_EXECUTE_MINIMAL`

Next action:

- Implement and run the P2 dense-oracle runner visibly in this dialogue.

## 2026-06-08 - P2 - EXECUTE_MINIMAL

Actions:

- Added focused P2 runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p2_tiny_nonlinear_dense_oracle_tf.py`
- Selected P44-M2 cubic additive-Gaussian panel as the first tiny nonlinear
  dense-oracle target.
- Ran dense order-161/order-241 refinement and deterministic UKF, SVD/cubature,
  CUT4, and Zhao-Cui/fixed-design TT route comparisons for dims 1, 2, and 3.
- Deferred DPF bootstrap-OT and LEDH-PFPF-OT to P5 per P0 route eligibility.

Commands:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p2_tiny_nonlinear_dense_oracle_tf.py
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p2_tiny_nonlinear_dense_oracle_tf.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p2_tiny_nonlinear_dense_oracle_tf
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p2_tiny_nonlinear_dense_oracle_tf --validate-only
python -c "import json; json.load(open('experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p2_tiny_nonlinear_dense_oracle_2026-06-08.json')); print('P2_JSON_OK')"
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p2_tiny_nonlinear_dense_oracle_tf.py experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p2_tiny_nonlinear_dense_oracle_2026-06-08.json experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p2-tiny-nonlinear-dense-oracle-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-p2-tiny-nonlinear-dense-oracle-result-2026-06-08.md
```

Observed outputs:

```text
PASS_P2_TINY_NONLINEAR_DENSE_ORACLE_PENDING_CLAUDE_REVIEW
P2_TINY_NONLINEAR_DENSE_ORACLE_VALIDATED
P2_JSON_OK
```

Key results:

- Dense promoted dims: `[1, 2, 3]`.
- Max dense value refinement gap: `2.1538326677728037e-14`.
- Max dense directional score refinement gap: `7.86124949083722e-15`.
- Max UKF value/score gaps: value `0.037994488785619174`,
  directional score `0.10008449900276654`; diagnostic-only.
- Max SVD/cubature value/score gaps: value `0.03799447645266696`,
  directional score `0.10008443469741578`; diagnostic-only.
- Max CUT4 value/score gaps: value `0.01541070953116952`,
  directional score `0.04073840839807784`; certified approximation, not
  oracle.
- Max Zhao-Cui/fixed-design TT value/score gaps: value
  `0.0003496295403593308`, directional score `0.0018185324574571116`;
  certified approximation, not oracle.
- All P2 veto diagnostics are false.

Gate status:

- `PASS_P2_TINY_NONLINEAR_DENSE_ORACLE_PENDING_CLAUDE_REVIEW`

Next action:

- Run Claude read-only P2 gate review in this visible dialogue.

## 2026-06-08 - P2 - CLAUDE_REVIEW_ITERATION_1

Claude status: `VERDICT: REVISE`.

Accepted findings:

- The first P2 runner compared different initial-state parameterizations across
  routes while calling them same-target: the dense scalar route used the
  predictive initial law `initial_mean = rho * raw_initial_mean` and
  `initial_variance = rho^2 * raw_initial_variance + transition_variance`,
  while the structural sigma-point routes used `raw_initial_mean` and
  `raw_initial_variance` directly.
- The validator did not derive `gradient_parameterization_mismatch` from a
  recorded same-target initial-law check.

Repairs:

- Changed the structural sigma-point model to use `initial_mean` and
  `initial_variance`, matching the dense scalar route.
- Added per-dim `initial_law_alignment` records and made the validator reject
  dense/structural initial-law mismatch.
- Derived `gradient_parameterization_mismatch` from the recorded initial-law
  alignment.

Repair validation:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p2_tiny_nonlinear_dense_oracle_tf.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p2_tiny_nonlinear_dense_oracle_tf
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p2_tiny_nonlinear_dense_oracle_tf --validate-only
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p2_tiny_nonlinear_dense_oracle_tf.py experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p2_tiny_nonlinear_dense_oracle_2026-06-08.json experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p2-tiny-nonlinear-dense-oracle-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-p2-tiny-nonlinear-dense-oracle-result-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-p2-claude-review-ledger-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md
```

Observed outputs:

```text
PASS_P2_TINY_NONLINEAR_DENSE_ORACLE_PENDING_CLAUDE_REVIEW
P2_TINY_NONLINEAR_DENSE_ORACLE_VALIDATED
```

Repair summary:

- Initial-law alignment gaps are zero for dims 1, 2, and 3.
- `gradient_parameterization_mismatch` is `False` after the derived check.
- All P2 veto diagnostics are false.
- Updated route gap maxima after same-target repair:
  UKF value `0.01354373616081661`, directional score
  `0.19744859531069286`; SVD/cubature value `0.013543727112987014`,
  directional score `0.19744866605344374`; CUT4 value
  `0.010705509431428561`, directional score `0.19438180479176714`;
  Zhao-Cui/fixed-design TT value `0.0003496295403593308`, directional score
  `0.0018185324574571116`.

Gate status:

- `P2_REPAIRED_AND_REVALIDATED_PENDING_CLAUDE_REVIEW_ITERATION_2`

Next action:

- Run Claude read-only P2 gate review iteration 2.

## 2026-06-08 - P2 - CLAUDE_REVIEW_ITERATION_2

Claude status: `VERDICT: AGREE`.

Findings:

- Iteration-1 same-target blocker is resolved: scalar dense and structural
  sigma-point routes now share the same predictive initial law.
- P2 JSON records `initial_law_alignment` with zero mean/covariance gaps for
  dims 1, 2, and 3.
- `gradient_parameterization_mismatch` is derived from the recorded alignment,
  and validation rejects unaligned rows.
- Dense refined quadrature remains the only `EXACT_ORACLE`; UKF and SVD remain
  `DIAGNOSTIC_ONLY`; CUT4 and Zhao-Cui/fixed-design TT remain
  `CERTIFIED_APPROXIMATION`, with non-oracle labels preserved.
- DPF bootstrap-OT and LEDH-PFPF-OT remain deferred to P5 rather than promoted
  in P2.
- Dense refinement, value gaps, gradient/directional gaps, multi-step finite
  difference diagnostics, veto diagnostics, and CPU-only environment recording
  are present for the P2 gate.
- Non-blocking hardening note: `single_step_finite_difference_used_as_promotion`
  remains hard-coded `False`, but the promotion path is dense refinement plus
  multi-step finite-difference checks.

Codex decision:

- Accept Claude iteration-2 agreement.
- P2 exits `PASS_P2_TINY_NONLINEAR_DENSE_ORACLE_READY_FOR_P3`.

Gate status:

- `PASS_P2_TINY_NONLINEAR_DENSE_ORACLE_READY_FOR_P3`

Next action:

- Start P3 conditional Gaussian mixture precheck in this visible dialogue.

## 2026-06-08 - P3 - PRECHECK

Evidence contract:

- Question: for transformed-SV and finite-mixture SV targets with approved P0
  rows, can P3 record value and gradient evidence against exact same-target
  references without promoting native-SV or DPF claims?
- Baseline/comparator: `sv_exact_transformed_log_chi_square_panel` uses dense
  exact transformed log-chi-square quadrature as reference and
  Zhao-Cui/fixed-design TT as a local same-target certificate;
  `sv_ksc_transformed_mixture_panel` uses component-enumerated KSC Kalman
  mixture as reference and CUT4 as a same-target finite-mixture certificate.
- Primary criterion: write P3 JSON, markdown report, and result artifact with
  target identity, transformation/Jacobian convention, reference scores,
  route value/gradient gaps, approximation-only KSC-vs-exact gaps, blocked DPF
  rows, veto diagnostics, nonclaims, and a run manifest.
- Veto diagnostics: native and transformed likelihoods mixed in one metric,
  KSC mixture called native exact truth, Jacobian terms missing, DPF executed
  despite P0 blockers, route target mismatch, gradient parameterization
  mismatch, nonfinite rows, missing reference score/gaps, or unsupported
  generalized-SV/native claim.
- Explanatory diagnostics: component tuple counts, mixture metadata, TT/CUT4
  diagnostics, directional score residuals, KSC-vs-exact transformed
  approximation gap, and TensorFlow startup warnings.
- Nonclaims: P3 does not establish DPF correctness, native SV correctness from
  mixture agreement, generalized-SV native equality, HMC readiness, production
  readiness, GPU readiness, or paper-scale claims.

Skeptical audit:

- Wrong-baseline risk is controlled by selecting only the two P0 P3-eligible SV
  targets and keeping exact transformed and finite-mixture target rows
  separate.
- Proxy-promotion risk is controlled by making same-target reference
  value/score agreement the route criterion; finite status, component counts,
  and KSC-vs-exact gaps are diagnostics or approximation evidence only.
- Missing-stop-condition risk is controlled by explicit veto diagnostics and
  the max-five Claude review loop.
- Unfair-comparison risk is controlled by preserving P0 DPF blockers. P3 must
  not run bootstrap-OT or LEDH-PFPF-OT for either selected SV target.
- Hidden-assumption risk is controlled by recording the transform convention:
  exact transformed rows use `z = log(y^2)` with offset zero; raw-native
  likelihoods require subtracting the observation-only Jacobian; KSC rows use
  `z = log(y^2 + 1e-8)` and are exact only for the declared finite-mixture
  approximation target.
- Environment risk is controlled by running TensorFlow CPU-only with
  `CUDA_VISIBLE_DEVICES=-1` before import; GPU evidence is out of scope.

Gate status:

- `P3_PRECHECK_PASSED_READY_TO_EXECUTE_MINIMAL`

Next action:

- Implement and run the P3 conditional Gaussian mixture runner visibly in this
  dialogue.

## 2026-06-08 - P3 - EXECUTE_MINIMAL

Actions:

- Added focused P3 runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p3_conditional_gaussian_mixture_tf.py`
- Selected the two P0 P3-eligible SV targets:
  `sv_exact_transformed_log_chi_square_panel` and
  `sv_ksc_transformed_mixture_panel`.
- Ran exact transformed dense vs Zhao-Cui/fixed-design TT value and gradient
  comparisons for dims 1, 2, and 3.
- Ran component-enumerated KSC Kalman mixture vs CUT4 value and gradient
  comparisons for dims 1, 2, and 3.
- Recorded KSC-vs-exact transformed gaps as approximation-only diagnostics,
  not native-SV promotion evidence.
- Preserved DPF bootstrap-OT and LEDH-PFPF-OT blockers from P0; no DPF route
  was executed in P3.

Commands:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p3_conditional_gaussian_mixture_tf.py
git diff --check -- docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p3_conditional_gaussian_mixture_tf.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p3_conditional_gaussian_mixture_tf
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p3_conditional_gaussian_mixture_tf --validate-only
python -c "import json; json.load(open('experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p3_conditional_gaussian_mixture_2026-06-08.json')); print('P3_JSON_OK')"
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p3_conditional_gaussian_mixture_tf.py experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p3_conditional_gaussian_mixture_2026-06-08.json experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p3-conditional-gaussian-mixture-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-p3-conditional-gaussian-mixture-result-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md
```

Observed outputs:

```text
PASS_P3_CONDITIONAL_GAUSSIAN_MIXTURE_PENDING_CLAUDE_REVIEW
P3_CONDITIONAL_GAUSSIAN_MIXTURE_VALIDATED
P3_JSON_OK
```

TensorFlow note:

- The CPU-only TensorFlow run emitted CUDA factory/cuInit startup warnings even
  with `CUDA_VISIBLE_DEVICES=-1`; this is recorded as environment noise, not a
  GPU-readiness or GPU-failure claim. P3 is CPU-only by contract.

Key results:

- Exact transformed dense reference finite dims: `[1, 2, 3]`.
- Exact transformed Zhao-Cui/fixed-design TT certificate dims: `[1, 2, 3]`.
- Max exact transformed TT absolute value error:
  `1.2017054018542694e-11`.
- Max exact transformed TT directional score gap:
  `3.689717277906871e-15`.
- Max exact transformed TT relative score error:
  `2.523371726816434e-15`.
- KSC Kalman mixture component tuple counts: `[7, 49, 343]`.
- KSC mixture CUT4 certificate dims: `[1, 2, 3]`.
- Max KSC CUT4 absolute value error: `5.329070518200751e-15`.
- Max KSC CUT4 directional score gap: `3.3306690738754696e-15`.
- Max KSC CUT4 relative score error: `1.2901875993693761e-15`.
- Max KSC-vs-exact transformed approximation-only value gap:
  `0.058681351263409454`.
- Max KSC-vs-exact transformed approximation-only directional score gap:
  `0.03555605677160689`.
- All P3 veto diagnostics are false.

Artifacts:

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p3_conditional_gaussian_mixture_2026-06-08.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p3-conditional-gaussian-mixture-2026-06-08.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p3-conditional-gaussian-mixture-result-2026-06-08.md`

Gate status:

- `PASS_P3_CONDITIONAL_GAUSSIAN_MIXTURE_PENDING_CLAUDE_REVIEW`

Next action:

- Run Claude read-only P3 gate review in this visible dialogue.

## 2026-06-08 - P3 - CLAUDE_REVIEW_ITERATION_1

Claude status: `VERDICT: AGREE`.

Findings:

- P3 answers the scoped conditional-Gaussian/mixture target question with
  target separation and claim scoping preserved.
- Exact transformed SV and finite KSC-mixture SV rows are kept separate in the
  subplan, visible ledger, registry, runner, JSON, and result note.
- P0 route classes are preserved: exact transformed dense and KSC Kalman are
  exact only for their declared targets; Zhao-Cui/fixed-design TT and CUT4
  remain `CERTIFIED_APPROXIMATION`; DPF bootstrap-OT and LEDH-PFPF-OT remain
  blocked and are not executed.
- Transform/Jacobian conventions are recorded: exact transformed rows use
  `z = log(y^2)` with zero offset and a raw-native Jacobian relation; KSC rows
  use `z = log(y^2 + 1e-8)` and do not promote native exactness.
- Value and gradient gaps are present for same-target rows, and
  KSC-vs-exact transformed gaps are approximation-only diagnostics.
- CPU-only TensorFlow execution and artifacts are recorded.
- Claude found no material wrong-baseline, proxy-promotion, stop-condition,
  unfair-comparison, stale-context, environment, or unsupported-claim blocker.

Codex decision:

- Accept Claude iteration-1 agreement.
- P3 exits `PASS_P3_CONDITIONAL_GAUSSIAN_READY_FOR_P4`.
- Keep P3 conclusions scoped: no DPF correctness, native SV correctness,
  generalized-SV equality, HMC, production, GPU, or paper-scale claim.

Gate status:

- `PASS_P3_CONDITIONAL_GAUSSIAN_READY_FOR_P4`

Next action:

- Start P4 Zhao-Cui route classification precheck in this visible dialogue.

## 2026-06-08 - P4 - PRECHECK

Evidence contract:

- Question: for every P0 target row, what master-schema claim class should the
  Zhao-Cui/fixed-design TT route carry, and is P5 eligibility known without
  treating sanity checks, fit residuals, or blocked multistate rows as oracle
  evidence?
- Baseline/comparator: P0 target-route registry; P1 LGSSM exact-oracle result;
  P2 tiny nonlinear dense-oracle result; P3 transformed/mixture result; P30
  highdim Zhao-Cui closeout; P45 target registry and cross-model calibration
  blockers.
- Primary criterion: write P4 JSON, markdown report, and result artifact that
  classify every `zhao_cui_fixed_design_tt` row using exactly one master claim
  class, record source evidence or blocker, preserve phase eligibility and P5
  eligibility, include branch/fixed-design/basis/rank metadata for runnable
  rows, and expose veto diagnostics.
- Veto diagnostics: missing target row, invalid claim class, scalar-only route
  applied to multistate target without reviewed adapter, adaptive TT fit or
  branch mutation hidden inside a fixed-branch gradient claim, fit residual
  promoted to likelihood correctness, Zhao-Cui treated as exact oracle where
  dense/Kalman is the exact baseline, runnable row lacking value evidence, or
  blocked row lacking blockers.
- Explanatory diagnostics: TT basis size, ranks, fit quadrature order, branch
  seed policy, source artifacts, whether gradients are fixed-branch only,
  and why P5 DPF statistical closeness is or is not eligible.
- Nonclaims: P4 does not establish DPF correctness, paper-scale Zhao-Cui
  reproduction, adaptive MATLAB TT-cross/SIRT behavior, coupled multivariate
  TT correctness, HMC readiness, production readiness, GPU readiness, or
  native model correctness for blocked rows.

Skeptical audit:

- Wrong-baseline risk is controlled by making P4 classification-only: P4 uses
  P1-P3/P45 reviewed artifacts and P0 rows instead of inventing a new numerical
  comparator.
- Proxy-promotion risk is controlled by requiring same-target value evidence
  before gradient-bearing rows and by treating fit/holdout residuals, finite
  status, and Kalman sanity checks as auxiliary diagnostics only.
- Missing-stop-condition risk is controlled by explicit veto diagnostics and
  the max-five Claude review loop.
- Unfair-comparison risk is controlled by preserving blocked multistate/native
  rows rather than forcing scalar fixed-design TT routes onto unsupported
  targets.
- Environment risk is low because P4 is a pure-Python registry/artifact
  classifier. TensorFlow reruns would not better answer the classification
  question; this is a reviewed amendment to the subplan's optional pure-Python
  path.

Gate status:

- `P4_PRECHECK_PASSED_READY_TO_EXECUTE_CLASSIFICATION_VALIDATOR`

Next action:

- Implement and run the P4 pure-Python Zhao-Cui route classification validator
  visibly in this dialogue.

## 2026-06-08 - P4 - EXECUTE_CLASSIFICATION_VALIDATOR

Actions:

- Added focused P4 pure-Python classifier:
  `experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p4_zhaocui_tt_route_classification_tf.py`
- Classified every P0 `zhao_cui_fixed_design_tt` row under the master claim
  classes.
- Preserved blocked multistate/native/KSC-mixture rows and recorded P5
  eligibility from P0.
- Recorded branch/fixed-design/basis/rank metadata for runnable local
  certificate rows where available.

Initial implementation repair:

- The first P4 runner import path reused `common_tf`, which imported
  TensorFlow at module import time despite the intended classification-only
  gate.
- Codex repaired the runner to use local pure-Python JSON/path helpers and
  added validation that fails if `tensorflow` or `tensorflow_probability`
  appears in `sys.modules`.
- The repaired P4 run is pure Python; its manifest records
  `tensorflow_imported: False`.

Commands:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p4_zhaocui_tt_route_classification_tf.py
git diff --check -- docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p4_zhaocui_tt_route_classification_tf.py
python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p4_zhaocui_tt_route_classification_tf
python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p4_zhaocui_tt_route_classification_tf --validate-only
python -c "import json; json.load(open('experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p4_zhaocui_tt_route_classification_2026-06-08.json')); print('P4_JSON_OK')"
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p4_zhaocui_tt_route_classification_tf.py experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p4_zhaocui_tt_route_classification_2026-06-08.json experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p4-zhaocui-tt-route-classification-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-p4-zhaocui-tt-route-classification-result-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md
```

Observed outputs:

```text
PASS_P4_ZHAOCUI_ROUTE_CLASSIFICATION_PENDING_CLAUDE_REVIEW
P4_ZHAOCUI_ROUTE_CLASSIFICATION_VALIDATED
P4_JSON_OK
```

Key results:

- Row count: `13`.
- Zhao-Cui/fixed-design TT claim-class counts:
  `{'BLOCKED': 8, 'CERTIFIED_APPROXIMATION': 4, 'DIAGNOSTIC_ONLY': 1, 'EXACT_ORACLE': 0, 'SURROGATE_USEFULNESS': 0}`.
- Runnable or diagnostic rows:
  `['lgssm_2d_h25_rich', 'p44_m2_cubic_additive_gaussian_panel', 'p44_m3_quadratic_observation_panel', 'p44_m4_nonlinear_transition_h2_panel', 'sv_exact_transformed_log_chi_square_panel']`.
- Blocked rows:
  `['sv_ksc_transformed_mixture_panel', 'generalized_sv_native_raw_observation', 'generalized_sv_transformed_residual_diagnostic', 'generalized_sv_gaussian_mixture_or_moment_matched_approximation', 'spatial_sir_additive_gaussian_closure', 'spatial_sir_native_or_nongaussian_route', 'predator_prey_additive_gaussian_rk4_closure', 'predator_prey_native_or_nongaussian_route']`.
- P5 DPF-eligible targets:
  `['lgssm_2d_h25_rich', 'p44_m2_cubic_additive_gaussian_panel', 'p44_m3_quadratic_observation_panel', 'p44_m4_nonlinear_transition_h2_panel']`.
- No Zhao-Cui/fixed-design TT row is classified as `EXACT_ORACLE`.
- All P4 veto diagnostics are false.

Artifacts:

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p4_zhaocui_tt_route_classification_2026-06-08.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p4-zhaocui-tt-route-classification-2026-06-08.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p4-zhaocui-tt-route-classification-result-2026-06-08.md`

Gate status:

- `PASS_P4_ZHAOCUI_ROUTE_CLASSIFICATION_PENDING_CLAUDE_REVIEW`

Next action:

- Run Claude read-only P4 gate review in this visible dialogue.

## 2026-06-08 - P4 - CLAUDE_REVIEW_ITERATION_1

Claude status: `VERDICT: AGREE`.

Findings:

- P4 answers the route-classification question as a classification-only gate
  with explicit non-promotion language.
- All 13 P0 targets receive a Zhao-Cui/fixed-design TT classification.
- Claim classes are restricted to the master schema and no Zhao-Cui row is
  promoted to `EXACT_ORACLE`.
- Same-target value evidence exists before gradient-bearing runnable rows are
  interpreted.
- Blocked KSC-mixture, generalized-SV, spatial-SIR, and predator-prey rows
  stay blocked; scalar-only TT is not applied to unsupported multistate rows.
- P5 eligibility matches P0: LGSSM and P44-M2/M3/M4 only.
- Zhao-Cui is not used as the P5 comparator; P5 should use exact Kalman or
  dense/refined references.
- The repaired P4 runner is pure Python and records TensorFlow/TFP not
  imported.

Codex decision:

- Accept Claude iteration-1 agreement.
- P4 exits `PASS_P4_ZHAOCUI_ROUTE_CLASSIFICATION_READY_FOR_P5`.
- Keep P4 conclusions scoped: no DPF correctness, no Zhao-Cui exact-oracle
  claim, no paper-scale/adaptive/coupled TT claim, no HMC, production, or GPU
  claim.

Gate status:

- `PASS_P4_ZHAOCUI_ROUTE_CLASSIFICATION_READY_FOR_P5`

Next action:

- Start P5 DPF statistical closeness precheck in this visible dialogue.

## 2026-06-08 - P5 - PRECHECK

Evidence contract:

- Question: for P0/P4 DPF-eligible rows, can bootstrap-OT and LEDH-PFPF-OT be
  promoted as statistically close in value and fixed-branch gradient to the
  approved exact/dense references, or must the rows be downgraded or blocked?
- Baseline/comparator: P0 registry and P4 P5-readiness routes; exact Kalman for
  `lgssm_2d_h25_rich`; `dense_refined_quadrature` for
  `p44_m2_cubic_additive_gaussian_panel`,
  `p44_m3_quadratic_observation_panel`, and
  `p44_m4_nonlinear_transition_h2_panel`.
- Primary criterion: every eligible target-route row is classified as promoted,
  downgraded/diagnostic, or blocked; promotion requires predeclared numeric P5
  tolerance and certification bands, paired seeds, evaluator variance,
  fixed-branch score tied to the value scalar, directional residuals, branch
  decisions, and passing value/gradient CI and max-error criteria.
- Veto diagnostics: placeholder or missing P0 DPF tolerance/band used for
  promotion, missing seed variability, stochastic and fixed-branch gradients
  mixed, branch decisions not recorded, same-target and approximation-target
  rows merged, Zhao-Cui/CUT4/SVD/UKF used as P5 DPF comparators, value closeness
  used to promote gradient closeness, or any eligible row omitted.
- Explanatory diagnostics: P1 LGSSM ESS/resampling/Sinkhorn/value/gradient
  summaries, reference availability for P44 rows, and missing adapter evidence.
- Nonclaims: P5 does not establish DPF correctness, stochastic-score
  correctness, nonlinear P44 DPF closeness, HMC readiness, production
  readiness, GPU readiness, or paper-scale claims.

Skeptical audit:

- Wrong-baseline risk is controlled by using P0/P4 reference-route decisions
  and P1 Kalman evidence only; prior BF/FilterFlow agreement is not oracle
  evidence.
- Proxy-promotion risk is material: P0 DPF rows carry
  `dpf_p5_pending_mc_band` and `p5_pending_mc_band`, which are placeholders
  rather than numeric promotion criteria. Because P1 DPF results are already
  visible, Codex must not invent post hoc numeric bands and call them
  predeclared.
- Missing-stop-condition risk is controlled by requiring all four eligible
  targets and both DPF methods to receive explicit row decisions.
- Unfair-comparison risk is controlled by separating LGSSM exact-target
  evidence from P44 dense-reference rows, and by not using Zhao-Cui/CUT4/SVD/UKF
  as P5 DPF comparators.
- Environment risk is controlled by making P5 a pure-Python evidence
  classifier unless a reviewed adapter-and-band amendment exists. No new
  TensorFlow DPF run is justified before the placeholder-band and nonlinear
  adapter gaps are resolved.

Gate status:

- `P5_PRECHECK_PASSED_CLASSIFICATION_ONLY_EXECUTION_READY`

Next action:

- Run the P5 pure-Python evidence-classification runner visibly in this
  dialogue, then request Claude read-only review of the result.

## 2026-06-08 - P5 - EXECUTE_CLASSIFICATION_VALIDATOR

Actions:

- Added focused P5 pure-Python evidence classifier:
  `experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p5_dpf_statistical_closeness_tf.py`
- Consumed P0 registry, P1 LGSSM DPF-vs-Kalman evidence, P2/P44 dense
  reference evidence, and P4 P5-readiness classification.
- Classified all P5-eligible target-route rows without running a detached
  process or hidden TensorFlow experiment.
- Preserved the placeholder-band blocker:
  `dpf_p5_pending_mc_band` / `p5_pending_mc_band` cannot support promotion.

Commands:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p5_dpf_statistical_closeness_tf.py
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p5_dpf_statistical_closeness_tf.py docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md
python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p5_dpf_statistical_closeness_tf
python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p5_dpf_statistical_closeness_tf --validate-only
python -c "import json; p='experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p5_dpf_statistical_closeness_2026-06-08.json'; d=json.load(open(p)); print(d['decision']); print(d['route_summaries']); print(d['veto_diagnostics'])"
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p5_dpf_statistical_closeness_tf.py experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p5_dpf_statistical_closeness_2026-06-08.json experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p5-dpf-statistical-closeness-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-p5-dpf-statistical-closeness-result-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md
```

Observed outputs:

```text
PASS_P5_DPF_STATISTICAL_CLOSENESS_PENDING_CLAUDE_REVIEW
P5_DPF_STATISTICAL_CLOSENESS_VALIDATED
```

Key results:

- Eligible targets:
  `['lgssm_2d_h25_rich', 'p44_m2_cubic_additive_gaussian_panel', 'p44_m3_quadratic_observation_panel', 'p44_m4_nonlinear_transition_h2_panel']`.
- Classified rows: `8`.
- Promoted rows: `[]`.
- Downgraded/diagnostic rows:
  `['lgssm_2d_h25_rich/dpf_bootstrap_ot', 'lgssm_2d_h25_rich/dpf_ledh_pfpf_ot']`.
- Blocked rows:
  `['p44_m2_cubic_additive_gaussian_panel/dpf_bootstrap_ot', 'p44_m2_cubic_additive_gaussian_panel/dpf_ledh_pfpf_ot', 'p44_m3_quadratic_observation_panel/dpf_bootstrap_ot', 'p44_m3_quadratic_observation_panel/dpf_ledh_pfpf_ot', 'p44_m4_nonlinear_transition_h2_panel/dpf_bootstrap_ot', 'p44_m4_nonlinear_transition_h2_panel/dpf_ledh_pfpf_ot']`.
- LGSSM final-particle diagnostic summaries:
  - `dpf_bootstrap_ot`, N=128: mean value error `0.782254`,
    value CI95 `[0.4989267853919508, 1.0655816202598167]`,
    score RMSE `3.31184`, mean relative score error `0.456505`.
  - `dpf_ledh_pfpf_ot`, N=128: mean value error `0.0821037`,
    value CI95 `[-0.21235352408532082, 0.3765608732534155]`,
    score RMSE `1.47236`, mean relative score error `0.172433`.
- All phase-level veto diagnostics are false because no row is promoted with
  missing bands/adapters; row-level blockers and downgrade reasons are recorded.
- The P5 runner manifest records `tensorflow_imported: False` and
  `tensorflow_probability_imported: False`.

Artifacts:

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p5_dpf_statistical_closeness_2026-06-08.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p5-dpf-statistical-closeness-2026-06-08.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p5-dpf-statistical-closeness-result-2026-06-08.md`

Gate status:

- `PASS_P5_DPF_STATISTICAL_CLOSENESS_PENDING_CLAUDE_REVIEW`

Next action:

- Run Claude read-only P5 gate review in this visible dialogue.

## 2026-06-08 - P5 - CLAUDE_REVIEW_ITERATION_1

Claude status: `VERDICT: AGREE`.

Findings:

- No wrong-baseline or comparator drift found: P5 keeps exact Kalman for
  `lgssm_2d_h25_rich` and `dense_refined_quadrature` for P44-M2/M3/M4.
- Zhao-Cui, CUT4, SVD, UKF, and BF/FilterFlow agreement are explicitly excluded
  as P5 DPF comparators.
- No placeholder DPF band is promoted and no eligible row is omitted: all 8
  P4-eligible rows are classified, with 0 promoted, 2 LGSSM rows downgraded,
  and 6 P44 rows blocked.
- No fixed/stochastic gradient mixing or branch/residual overclaim appears:
  all rows stay `fixed_branch_score`, LGSSM rows are downgraded because
  directional residuals are missing and branch decisions are aggregate-only,
  and P44 rows are blocked pending reviewed same-target adapters, evaluator
  variance, scalar/gradient tie, and branch diagnostics.
- The P6 mention is conditional only and does not claim DPF promotion
  readiness.

Codex decision:

- Accept Claude iteration-1 agreement.
- P5 exits `PASS_P5_DPF_STATISTICAL_CLOSENESS_READY_FOR_P6`.
- Keep P5 conclusions scoped: classification pass only; no DPF bootstrap-OT or
  LEDH-PFPF-OT correctness promotion.

Gate status:

- `PASS_P5_DPF_STATISTICAL_CLOSENESS_READY_FOR_P6`

Next action:

- Start P6 cross-filter calibration precheck in this visible dialogue if the
  user wants the run to continue.

## 2026-06-08 - P6 - PRECHECK

Evidence contract:

- Question: how large are DPF, UKF, SVD/sigma-point, CUT4, and Zhao-Cui value
  and gradient errors relative to reference error scales and evaluator
  variability, without turning approximation rows into exactness claims?
- Baseline/comparator: P1-P5 row-level artifacts. Exact/dense references must
  remain target-specific: Kalman for LGSSM, dense refined quadrature for P44
  and exact transformed SV, and KSC Kalman mixture only for the declared KSC
  approximation target.
- Primary criterion: produce exact-target, approximation-target, diagnostic,
  and blocked ledgers that preserve claim classes, normalize available value
  and score errors, include reference refinement uncertainty and DPF evaluator
  variance where available, and avoid a single cross-target ranking.
- Veto diagnostics: data-law variability used to excuse same-target numerical
  mismatch, approximation route ranked as exact, reference uncertainty omitted
  from rows that use dense refinement, DPF evaluator variance omitted when DPF
  diagnostics are shown, failed-gradient or blocked rows included as valid
  rankings, or fabricated metrics where no structured row-level data exists.
- Explanatory diagnostics: particle count, seed count, quadrature order,
  component count, point count, route availability, runtime, and blocker reason.
- Nonclaims: no global filter ranking, no default-policy change, no HMC
  readiness, no production readiness, no GPU readiness, and no paper-scale
  conclusion.

Skeptical audit:

- Wrong-baseline risk is controlled by carrying the target/reference route in
  every row and by separating exact-target and approximation-target tables.
- Proxy-promotion risk is controlled by reporting DPF P5 rows as
  diagnostic/blocked only, even though LGSSM DPF has finite value/gradient
  summaries.
- Missing-stop-condition risk is controlled by an explicit empty/blocked
  category for rows whose calibration would require unstructured or missing
  metrics.
- Unfair-comparison risk is controlled by classifying filters by evidence class
  rather than ranking them across LGSSM, P44, exact transformed SV, and KSC
  mixture targets.
- Environment risk is low for a pure-Python artifact assembler; TensorFlow
  reruns are not needed to normalize already-written errors and would not
  repair missing DPF promotion bands or nonlinear adapters.

Gate status:

- `P6_PRECHECK_PASSED_READY_TO_EXECUTE_CLASSIFICATION_CALIBRATION`

Next action:

- Implement and run a pure-Python P6 calibration artifact builder visibly in
  this dialogue.

## 2026-06-08 - P6 - EXECUTE_CALIBRATION_BUILDER

Actions:

- Added focused P6 pure-Python artifact builder:
  `experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p6_cross_filter_error_calibration_tf.py`
- Consumed P1-P5 artifacts plus the P45 empty multistate calibration blocker.
- Built claim-class-separated ledgers for exact-target deterministic rows,
  approximation-target rows, DPF diagnostic/blocker rows, blocked rows, and
  unstructured metric rows.
- Did not emit a global filter ranking.
- Did not run TensorFlow or any new numerical experiment.

Commands:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p6_cross_filter_error_calibration_tf.py
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p6_cross_filter_error_calibration_tf.py docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md
python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p6_cross_filter_error_calibration_tf
python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p6_cross_filter_error_calibration_tf --validate-only
python - <<'PY'
import json
p='experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p6_cross_filter_error_calibration_2026-06-08.json'
d=json.load(open(p))
print(d['decision'])
print(d['route_summaries'])
print(d['veto_diagnostics'])
PY
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p6_cross_filter_error_calibration_tf.py experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p6_cross_filter_error_calibration_2026-06-08.json experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-result-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md
```

Observed outputs:

```text
PASS_P6_CROSS_FILTER_CALIBRATION_PENDING_CLAUDE_REVIEW
P6_CROSS_FILTER_ERROR_CALIBRATION_VALIDATED
```

Key results:

- Exact-target calibration rows: `15`.
- Approximation-target calibration rows: `3`.
- DPF diagnostic/blocker rows: `8`; none are valid calibration-table rows.
- Blocked rows: `23`.
- Unstructured metric rows: `2` for P44-M3/M4 source notes that need
  machine-readable row metrics before P6-style calibration.
- Global ranking policy: `not_emitted`.
- Max exact-target absolute value error recorded:
  `0.01354373616081661`.
- Max exact-target relative score error recorded:
  `0.1127484708706417`.
- Max approximation-target absolute value error recorded:
  `5.329070518200751e-15`.
- Max approximation-target relative score error recorded:
  `1.2901875993693761e-15`.
- DPF diagnostic LGSSM RMSE/relative score summaries are preserved but not
  promoted or ranked:
  - `dpf_bootstrap_ot`: value RMSE `0.8339700259704327`, mean relative score
    error `0.4565046565890657`.
  - `dpf_ledh_pfpf_ot`: value RMSE `0.3114821802004455`, mean relative score
    error `0.1724329499486878`.
- All P6 veto diagnostics are false.
- The P6 runner manifest records `tensorflow_imported: False` and
  `tensorflow_probability_imported: False`.

Artifacts:

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p6_cross_filter_error_calibration_2026-06-08.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-2026-06-08.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-result-2026-06-08.md`

Gate status:

- `PASS_P6_CROSS_FILTER_CALIBRATION_PENDING_CLAUDE_REVIEW`

Next action:

- Run Claude read-only P6 gate review in this visible dialogue.

## 2026-06-08 - P6 - CLAUDE_REVIEW_ITERATION_1

Claude status: `VERDICT: REVISE`.

Accepted findings:

- P6 allowed P3 exact-transformed rows into the exact-target calibration table
  even though their reference uncertainty was recorded as
  `not_structured_in_p3_artifact`. The validator only rejected missing
  uncertainty for P2 dense rows, leaving a blind spot for exact-target rows from
  P3.
- The P6 markdown did not surface evaluator-variance fields for the downgraded
  LGSSM DPF rows, although the JSON preserved them.

Repairs:

- Moved P3 exact-transformed Zhao-Cui rows out of
  `exact_target_calibration_rows` into `unstructured_metric_rows` with observed
  gaps retained and `valid_for_calibration_table: False`.
- Added a validator veto and validation check rejecting exact-target
  calibration rows unless their reference uncertainty status is accepted.
- Updated the markdown DPF diagnostic table to include value standard error and
  gradient-error-norm standard error.

Repair validation:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p6_cross_filter_error_calibration_tf.py
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p6_cross_filter_error_calibration_tf.py
python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p6_cross_filter_error_calibration_tf
python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p6_cross_filter_error_calibration_tf --validate-only
python - <<'PY'
import json
p='experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p6_cross_filter_error_calibration_2026-06-08.json'
d=json.load(open(p))
print(d['route_summaries'])
print(d['veto_diagnostics'])
print('exact targets', sorted({r['target_id'] for r in d['exact_target_calibration_rows']}))
print('unstructured statuses', [(r['target_id'], r.get('status')) for r in d['unstructured_metric_rows']])
PY
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p6_cross_filter_error_calibration_tf.py experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p6_cross_filter_error_calibration_2026-06-08.json experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-result-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md
```

Observed repair outputs:

```text
PASS_P6_CROSS_FILTER_CALIBRATION_PENDING_CLAUDE_REVIEW
P6_CROSS_FILTER_ERROR_CALIBRATION_VALIDATED
```

Post-repair key results:

- Exact-target calibration rows decreased from `15` to `12`.
- Exact-target calibration now contains only
  `p44_m2_cubic_additive_gaussian_panel`, whose dense refinement uncertainty is
  structured in P2.
- Unstructured metric rows increased from `2` to `5`, adding the three P3
  exact-transformed rows with
  `reference_uncertainty_not_structured_in_p3_artifact`.
- P6 markdown now shows value SE and gradient-norm SE for the two downgraded
  LGSSM DPF rows.
- All P6 veto diagnostics are false after repair.

Gate status:

- `P6_REVALIDATED_AFTER_CLAUDE_REVISE_PENDING_REVIEW_ITERATION_2`

Next action:

- Run Claude read-only P6 gate review iteration 2.

## 2026-06-08 - P6 - CLAUDE_REVIEW_ITERATION_2

Claude status: `VERDICT: AGREE`.

Findings:

- Iteration-1 blockers are fixed: P3 exact-transformed rows are no longer in
  `exact_target_calibration_rows`; they are in `unstructured_metric_rows` with
  `reference_uncertainty_not_structured_in_p3_artifact` and
  `valid_for_calibration_table: false`.
- Exact-target calibration now contains only P2 dense-refinement rows.
- The runner enforces accepted exact-target uncertainty and keeps DPF out of
  valid calibration rows.
- DPF evaluator-variance fields are visible in both markdown and JSON.
- No remaining global-ranking or approximation-as-exact overclaim was found.

Codex decision:

- Accept Claude iteration-2 agreement.
- P6 exits `PASS_P6_CROSS_FILTER_CALIBRATION_READY_FOR_P7`.
- Keep P6 conclusions scoped: no global ranking, no DPF correctness, no
  approximation exactness, no default-policy change, and no HMC/production/GPU
  claim.

Gate status:

- `PASS_P6_CROSS_FILTER_CALIBRATION_READY_FOR_P7`

Next action:

- Start P7 integration closeout precheck in this visible dialogue.

## 2026-06-08 - P7 - PRECHECK

Evidence contract:

- Question: what can responsibly be concluded from the DPF-versus-filter
  comparison program, and what remains blocked or diagnostic-only?
- Baseline/comparator: P0-P6 reviewed artifacts and this visible execution
  ledger. P7 is closeout-only and must not introduce new numerical evidence.
- Primary criterion: every P0-P6 phase has a result and review artifact; exact,
  approximation, diagnostic-only, blocked, and unstructured rows are separated;
  final claims match the strongest valid evidence class; all nonclaims are
  preserved.
- Veto diagnostics: missing phase artifact, blocked row hidden from final
  table, exact and approximation rows merged, value-only row described as
  gradient-valid, stochastic-gradient caveats omitted, or unsupported
  production/HMC/public API/global superiority claim.
- Explanatory diagnostics: phase pass tokens, total row counts by claim class,
  strongest comparator by target, unresolved implementation gaps, and next
  smallest discriminating run.
- Nonclaims: no universal DPF superiority, no default production method change,
  no DPF correctness promotion, no HMC readiness, no GPU/paper-scale/public API
  claim.

Skeptical audit:

- Wrong-baseline risk is controlled by treating P7 as an artifact closeout over
  P0-P6 only, not a new comparator phase.
- Proxy-promotion risk is controlled by preserving P5/P6 decisions: DPF rows
  remain diagnostic or blocked; deterministic approximation rows stay
  certified approximations, not exactness claims.
- Missing-stop-condition risk is controlled by validating every required phase
  JSON/result/review ledger and by recording unresolved blockers.
- Unfair-comparison risk is controlled by never emitting a global filter
  leaderboard.
- Environment risk is low because P7 is pure Python and must not import
  TensorFlow or run numerical filters.

Gate status:

- `P7_PRECHECK_PASSED_READY_TO_EXECUTE_CLOSEOUT_AUDIT`

Next action:

- Implement and run a pure-Python P7 closeout audit visibly in this dialogue.

## 2026-06-08 - P7 - EXECUTE_CLOSEOUT_AUDIT

Actions:

- Added focused P7 pure-Python closeout runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p7_integration_closeout.py`
- Generated final closeout JSON, report, phase result, and reset memo.
- Checked that P0-P6 JSON/result/review artifacts exist and that phase pass
  tokens are present in result/review/visible-ledger artifacts.
- Preserved DPF rows as diagnostic or blocked; no DPF correctness promotion was
  made.
- Preserved exact, approximation, diagnostic, blocked, and unstructured ledgers
  separately.

Commands:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p7_integration_closeout.py
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p7_integration_closeout.py docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md
python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p7_integration_closeout
python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p7_integration_closeout --validate-only
python - <<'PY'
import json
p='experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p7_integration_closeout_2026-06-08.json'
d=json.load(open(p))
print(d['decision'])
print(d['veto_diagnostics'])
print('phase count', len(d['phase_summaries']))
print('dpf summary', d['final_ledgers']['dpf_summary'])
print('unresolved', [g['gap_id'] for g in d['unresolved_gaps']])
PY
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p7_integration_closeout.py experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p7_integration_closeout_2026-06-08.json experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p7-integration-closeout-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-p7-integration-closeout-result-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-reset-memo-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md
```

Observed outputs:

```text
PASS_P7_FILTER_COMPARISON_CLOSEOUT_PENDING_CLAUDE_REVIEW
P7_INTEGRATION_CLOSEOUT_VALIDATED
```

Key results:

- Phase summaries: `7` for P0-P6.
- Final DPF summary: `0` promoted rows, `2` downgraded/diagnostic LGSSM rows,
  and `6` blocked P44 rows.
- Final ledgers:
  - exact-target certified approximation rows: `6`;
  - approximation-target rows: `3`;
  - diagnostic-only rows: `14`;
  - blocked rows: `23`;
  - unstructured metric rows: `5`.
- Unresolved gaps:
  `numeric_dpf_p5_bands`, `p44_same_target_dpf_adapters`,
  `fixed_branch_directional_residuals`,
  `p3_exact_transformed_reference_uncertainty_json`, and
  `p44_m3_m4_structured_metric_json`.
- All P7 veto diagnostics are false.
- The P7 runner manifest records `tensorflow_imported: False` and
  `tensorflow_probability_imported: False`.

Artifacts:

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p7_integration_closeout_2026-06-08.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p7-integration-closeout-2026-06-08.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p7-integration-closeout-result-2026-06-08.md`
- Reset memo:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-reset-memo-2026-06-08.md`

Gate status:

- `PASS_P7_FILTER_COMPARISON_CLOSEOUT_PENDING_CLAUDE_REVIEW`

Next action:

- Run Claude read-only P7 final closeout review.

## 2026-06-08 - P7 - CLAUDE_REVIEW_ITERATION_1

Claude status: `VERDICT: REVISE`.

Accepted findings:

- The required P7 Claude review ledger did not exist yet.
- The P7 result and JSON correctly remained
  `PASS_P7_FILTER_COMPARISON_CLOSEOUT_PENDING_CLAUDE_REVIEW`, with
  `claude_final_review_required: true` and
  `claude_final_review_recorded: false`.

Positive review findings:

- Blocked rows were visible.
- Exact and approximation ledgers were separated.
- DPF correctness and stochastic-score correctness were not promoted.
- Unsupported production/HMC/GPU/public API/global-superiority claims were
  withheld.
- The reset memo existed.
- The P7 artifact recorded TensorFlow not imported.

Repairs:

- Created
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p7-claude-review-ledger-2026-06-08.md`.
- Reran P7 with `--promote-after-review`, producing
  `PASS_P7_FILTER_COMPARISON_CLOSEOUT`.

Gate status:

- `P7_PROMOTED_AFTER_REVIEW_PENDING_CONFIRMATION`

Next action:

- Run Claude read-only P7 final confirmation.

## 2026-06-08 - P7 - CLAUDE_REVIEW_ITERATION_2

Claude status: `VERDICT: REVISE`.

Accepted findings:

- The P7 result and JSON had the final pass token, but the P7 review ledger
  still ended at iteration 1 with `PENDING_PROMOTION_RERUN`.
- The reset memo still said P7 awaited final Claude review.
- This visible execution ledger still recorded the pending-review P7 action as
  the latest P7 state.

Positive review findings:

- Final decision/pass token was present in the result and JSON.
- All veto diagnostics were false.
- Blocked rows remained visible.
- Exact, approximation, diagnostic, blocked, and unstructured ledgers remained
  separated.
- Prohibited DPF correctness, stochastic-score correctness, global-superiority,
  production, HMC, GPU, and public-API claims were withheld.

Repairs:

- Updated the P7 Claude review ledger to record iteration 2.
- Updated the reset memo generator so promoted closeout says P0-P7 are closed
  after final Claude review.
- Reran P7 with `--promote-after-review`.

Repair validation:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p7_integration_closeout.py
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p7_integration_closeout.py docs/plans/bayesfilter-dpf-filter-oracle-comparison-p7-claude-review-ledger-2026-06-08.md
python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p7_integration_closeout --promote-after-review
python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p7_integration_closeout --validate-only
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p7_integration_closeout.py experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p7_integration_closeout_2026-06-08.json experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p7-integration-closeout-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-p7-integration-closeout-result-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-reset-memo-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-p7-claude-review-ledger-2026-06-08.md docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md
```

Observed repair outputs:

```text
PASS_P7_FILTER_COMPARISON_CLOSEOUT
P7_INTEGRATION_CLOSEOUT_VALIDATED
```

Gate status:

- `PASS_P7_FILTER_COMPARISON_CLOSEOUT_PENDING_FINAL_CONFIRMATION`

Next action:

- Run Claude read-only P7 final confirmation iteration 3.

## 2026-06-08 - P7 - CLAUDE_REVIEW_ITERATION_3

Claude status: `VERDICT: AGREE`.

Findings:

- Prior repair state is present: the P7 review ledger records iterations 1 and
  2.
- Final promoted decision is present in both result and JSON:
  `PASS_P7_FILTER_COMPARISON_CLOSEOUT`.
- JSON review state records final review as recorded.
- The reset memo closes P0-P7 after final Claude review.
- This visible ledger records the iteration-2 repair and pending final
  confirmation.
- All veto diagnostics are false.
- Blocked rows remain visible and exact/approximation/diagnostic/blocked/
  unstructured ledgers remain separated.
- No prohibited DPF correctness, stochastic-score correctness,
  global-superiority, production, HMC, GPU, or public-API claims were found.

Codex decision:

- Accept Claude iteration-3 agreement.
- P7 exits `PASS_P7_FILTER_COMPARISON_CLOSEOUT`.
- The visible DPF filter-oracle comparison gated run is closed.

Gate status:

- `PASS_P7_FILTER_COMPARISON_CLOSEOUT`

Next action:

- No required phase work remains in this visible gated run. Future work should
  start from the reset memo and open a new reviewed plan for DPF bands or P44
  same-target adapters.
