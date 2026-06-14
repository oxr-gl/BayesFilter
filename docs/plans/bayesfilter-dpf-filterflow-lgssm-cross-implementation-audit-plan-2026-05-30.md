# Plan: Filterflow LGSSM Cross-Implementation Audit

## Decision

`PLAN_READY_FOR_CLAUDE_REVIEW`

## Evidence Contract

Question: does the BayesFilter TF/TFP finite-Sinkhorn OT-DPF reproduce the
qualitative LGSSM behavior reported by Corenflos et al. Section 5.1 and encoded
in JTT94/filterflow when the model, theta grid, time horizon, particle count,
epsilon, cost scaling, resampling rule, and seed protocol are matched as closely
as the current environments allow?

Primary comparator: Corenflos et al. Section 5.1 plus the original
JTT94/filterflow implementation at commit
`5d8300ba247c4c17e1a301a22560c24fd0670bfe`.

Primary criterion: when the same mathematical object and calibration are used,
BayesFilter and filterflow should agree at the level of Section 5.1 qualitative
behavior. The explicit audit categories are:

- `consistent`: for all three theta grid points, the primary BayesFilter DET
  row `bayesfilter_scaled_ess` differs from the executable filterflow DET row
  `filterflow_regularized` by no more than one filterflow Monte Carlo sample
  standard deviation, and it has no unexplained sign, ordering, or scale
  inversion relative to the filterflow/PF table;
- `source_consistent_execution_blocked`: filterflow cannot execute because of
  dependency drift, but BayesFilter's closest calibrated row matches the paper
  Table 1 qualitative pattern within one reported paper standard deviation at
  all theta grid points and all implementation mismatches are explicitly
  ledgered;
- `red_flag`: any theta point exceeds the one-standard-deviation envelope, or
  the result has an unexplained sign/order/scale inversion;
- `blocked`: model settings, likelihood normalization, seed protocol, or
  filterflow execution cannot be recovered well enough to classify the result.

The one-standard-deviation envelope is not a universal promotion threshold. It
is only a reproduction-audit band for the reported Section 5.1 Monte Carlo
table.

Veto diagnostics:

- unable to recover the Section 5.1 LGSSM settings from the paper or filterflow;
- mismatched transition covariance, observation covariance, theta grid, horizon,
  particle count, or scaling convention without a recorded blocker;
- unmatched epsilon semantics treated as comparable evidence;
- unmatched resampling trigger treated as comparable evidence;
- non-finite log-likelihoods, weights, gradients, or Sinkhorn couplings;
- failed Sinkhorn marginal residuals in BayesFilter rows;
- filterflow dependency drift that prevents execution and is not recorded as a
  structured blocker;
- unauthorized edits to production `bayesfilter/`, `tests/`, vendored student
  code, monograph chapters, or the high-dimensional nonlinear filtering lane.

Explanatory diagnostics: filtered means, Kalman log likelihood, per-time
log-likelihood error, ESS, resampling count, runtime, Sinkhorn iterations, row
and column residuals, cost scale, scaling policy, epsilon, seed variability, and
environment/package versions.

What will not be concluded: no production readiness, public API readiness, HMC
readiness, posterior correctness, general nonlinear-SSM validity, learned/neural
OT promotion, banking/model-risk claim, or monograph claim.

## Section 5.1 Settings To Recover

Primary paper anchors from `.localsource/dpf_ot_audit/`:

- model:
  `X_{t+1} | X_t=x ~ Normal(diag(theta_1, theta_2) x, 0.5 I_2)`;
- observation:
  `Y_t | X_t=x ~ Normal(x, 0.1 I_2)`;
- data generation: `T=150` observations at `theta=(0.5, 0.5)`;
- evaluation theta grid:
  `(0.25, 0.25)`, `(0.5, 0.5)`, `(0.75, 0.75)`;
- particle count: `N=25`;
- Monte Carlo realizations: `100`;
- DPF epsilons: `0.25`, `0.5`, `0.75`;
- reported quantity:
  `(1/T) * (estimated log likelihood(theta; U) - exact log likelihood(theta))`;
- reported Table 1 values:
  PF means approximately `-1.13`, `-0.93`, `-1.05`;
  DPF epsilon `0.25` means approximately `-1.14`, `-0.94`, `-1.07`;
  DPF epsilon `0.5` means approximately `-1.14`, `-0.94`, `-1.08`;
  DPF epsilon `0.75` means approximately `-1.14`, `-0.94`, `-1.08`,
  with standard deviations around `0.17--0.20`.

Filterflow source anchors:

- `.localsource/filterflow/scripts/simple_linear_comparison.py`;
- `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/plan.py`;
- `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/sinkhorn.py`;
- `.localsource/filterflow/filterflow/resampling/differentiable/biased.py`;
- `.localsource/filterflow/filterflow/smc.py`;
- `.localsource/filterflow/filterflow/models/simple_linear_gaussian.py`;
- `.localsource/filterflow/filterflow/resampling/criterion.py`.

Important mismatch to record: filterflow's `simple_linear_comparison.py` uses
`transition_covariance = I_2`, while the paper text says `0.5 I_2`. The primary
BayesFilter-vs-filterflow execution comparator is the filterflow code setting
because that is the implementation being audited. The paper-text covariance
variant is a required sensitivity row. If the audit cannot determine whether
the mismatch is intentional, a covariance-versus-Cholesky interpretation issue,
or code/paper drift, the final decision must be no stronger than `red_flag` or
`blocked`.

## Inputs

- `AGENTS.md`
- `CLAUDE.md`
- `docs/plans/bayesfilter-dpf-ot-resampling-math-source-audit-result-2026-05-30.md`
- `.localsource/dpf_ot_audit/corenflos2021_differentiable_particle_filtering_eot.pdf`
- `.localsource/dpf_ot_audit/corenflos2021_differentiable_particle_filtering_eot_supp.pdf`
- `.localsource/filterflow/`
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/dpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/bootstrap_pf_tf.py`
- `experiments/dpf_implementation/tf_tfp/references/kalman_lgssm_tf.py`

## Outputs

- `docs/plans/bayesfilter-dpf-filterflow-lgssm-cross-implementation-audit-result-2026-05-30.md`
- `experiments/dpf_implementation/reports/dpf-filterflow-lgssm-cross-implementation-audit-2026-05-30.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_lgssm_cross_audit_2026-05-30.json`
- experimental runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_cross_audit_tf.py`

## Allowed Write Set

- this plan file;
- the result files listed above;
- JSON outputs under `experiments/dpf_implementation/reports/outputs/`;
- optional experimental BayesFilter runner under
  `experiments/dpf_implementation/tf_tfp/runners/`;
- optional experimental helper:
  `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_scaled_tf.py`.
- external-source acquisition target:
  `.localsource/filterflow/`, only if absent. If present, record commit and
  dirty state without modifying it.

During result-review iterations, code changes are allowed only in the optional
runner/helper paths above. Documentation/result fixes are allowed only in this
plan and the listed result/report artifacts.

## Forbidden Write Set

- production `bayesfilter/`;
- `tests/`;
- vendored student code under `experiments/student_dpf_baselines/vendor/`;
- original filterflow source under `.localsource/filterflow/`;
- monograph chapters under `docs/chapters/`;
- high-dimensional nonlinear filtering plans, code, or artifacts;
- unrelated dirty files.

## Method

1. Confirm `.localsource/filterflow` exists and record its commit and dirty
   status. If it is absent, clone `https://github.com/JTT94/filterflow` there.
   If network or sandbox blocks cloning, rerun with escalation. If the clone
   still fails, record a structured blocker.
2. Inspect paper Section 5.1 and filterflow `simple_linear_comparison.py` to
   produce a paper/code settings ledger.
3. Attempt a filterflow execution using original code and a bounded command.
   Prefer importing and calling `scripts.simple_linear_comparison.main` from a
   wrapper rather than editing filterflow. If dependency drift blocks execution,
   record the exact missing dependency or incompatibility and continue with
   source-level comparison.
4. Implement the BayesFilter experimental runner
   `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_cross_audit_tf.py`.
   The runner must:
   - sets `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import;
   - builds the Section 5.1 LGSSM with the filterflow-code covariance variant as
     the primary implementation comparator and the paper-text covariance variant
     as sensitivity;
   - computes exact Kalman log likelihood for each theta in the grid;
   - uses one shared observation path across all theta values within each
     realization;
   - uses common realization ids and recorded seed offsets for PF, raw DET, and
     scaled DET where feasible, while acknowledging that filterflow's random
     stream may not be bitwise matched;
   - reports `(estimated_log_likelihood(theta; U) - kalman_log_likelihood(theta)) / T`;
   - runs the minimal comparator matrix below;
   - labels the primary BayesFilter decision lane exactly as
     `bayesfilter_scaled_ess` and treats all other BayesFilter DET rows as
     sensitivity-only. Sensitivity rows may explain a failure but may not rescue
     the primary decision.
   - records finite diagnostics, Sinkhorn residuals, cost scales, seed protocol,
     and per-time log-likelihood errors.
5. Compare output against Table 1 only qualitatively unless the exact random
   stream and environment match filterflow. Treat one-machine reproduction
   differences as calibration evidence, not paper refutation.
6. Write result and report artifacts with a decision table and red-flag ledger.

## Minimal Comparator Matrix

Primary lanes:

| Lane | Role | Covariance | Resampling | Cost scaling | Epsilon |
| --- | --- | --- | --- | --- | --- |
| `filterflow_regularized` | primary external implementation comparator | filterflow code | ESS threshold 0.5 | filterflow centered/diameter scaling and epsilon annealing | 0.25, 0.5, 0.75 |
| `bayesfilter_scaled_ess` | primary BayesFilter implementation comparator | filterflow code | ESS threshold 0.5 | paper/filterflow-style scaled cost | 0.25, 0.5, 0.75 |
| `filterflow_pf` | primary PF comparator | filterflow code | ESS threshold 0.5 | N/A | N/A |
| `bayesfilter_pf` | BayesFilter PF comparator | filterflow code | ESS threshold 0.5 | N/A | N/A |

Sensitivity lanes:

| Lane | Role | Covariance | Resampling | Cost scaling | Epsilon |
| --- | --- | --- | --- | --- | --- |
| `bayesfilter_raw_ess` | current-helper sensitivity | filterflow code | ESS threshold 0.5 | raw squared Euclidean | 0.25, 0.5, 0.75 |
| `bayesfilter_scaled_every_step` | resampling-trigger sensitivity | filterflow code | every step | paper/filterflow-style scaled cost | 0.25, 0.5, 0.75 |
| `bayesfilter_scaled_paper_covariance` | paper-text covariance sensitivity | `0.5 I_2` | ESS threshold 0.5 | paper/filterflow-style scaled cost | 0.25, 0.5, 0.75 |

If filterflow cannot execute, `filterflow_regularized` and `filterflow_pf` are
replaced by a source-level settings row and the final decision cannot exceed
`source_consistent_execution_blocked`.

If filterflow executes only partially, the result must be classified as:

- `partial_execution_red_flag` when `filterflow_regularized` is missing any
  theta/effective-epsilon cell in the `3 x 3` theta-by-epsilon grid;
- `partial_pf_only_blocker` when `filterflow_pf` runs but
  `filterflow_regularized` does not;
- never `consistent` unless the full primary `filterflow_regularized` grid and
  `filterflow_pf` comparator complete with finite values.

## Scaling And Epsilon Match Ledger

The result must include a ledger with these exact fields:

- `filterflow_centering_formula`: expected
  `x - stop_gradient(mean(x, axis=particles))`;
- `filterflow_scale_formula`: expected
  `diameter(x, x) * sqrt(dimension)`, where `diameter` is the maximum particle
  coordinate standard deviation with zero fallback;
- `filterflow_scaled_particles_formula`: expected
  `centered_x / stop_gradient(scale)`;
- `filterflow_cost_formula`: expected squared distance divided by `2` on the
  scaled particle cloud;
- `filterflow_epsilon_schedule`: expected initialization at
  `max_min(scaled_x, scaled_x)^2` and geometric decrease by `scaling^2` down to
  target epsilon;
- `bayesfilter_scaled_cost_formula`: must be either exactly the filterflow
  scaled cost above or explicitly marked `similar_not_matched`;
- `bayesfilter_epsilon_schedule`: must be either exactly the filterflow
  schedule above or explicitly marked `similar_not_matched`;
- `match_status`: one of `matched`, `similar_not_matched`, or `blocked`.

The primary decision may be `consistent` only when `match_status == matched`.
If BayesFilter implements scaled cost but not the filterflow epsilon annealing
schedule, the primary decision must be no stronger than `red_flag`, with the
discrepancy attributed to `implementation/calibration`.

## Skeptical Pre-Execution Audit

| Risk | Status | Mitigation |
| --- | --- | --- |
| stale context | pass | Read repo governance, prior OT math audit, paper text, filterflow commit, and BayesFilter TF files. |
| wrong paper settings | watch | The paper says `0.5 I_2`; filterflow script sets `I_2`. The audit must split these variants. |
| wrong LGSSM | pass | The runner must use 2D state, identity observation, theta diagonal transition, `T=150`, theta grid `{0.25,0.5,0.75}`. |
| wrong epsilon semantics | watch | Raw-cost and scaled-cost BayesFilter variants must be labelled separately. |
| cost scaling mismatch | watch | This is a primary discrepancy, not an implementation detail to hide. |
| resampling trigger mismatch | watch | ESS-triggered and every-step policies must be labelled separately. |
| value-only evidence overclaimed as gradient evidence | pass | Gradient is explanatory only; Section 5.1 table is likelihood-value evidence. |
| hidden production drift | pass | Forbidden write set excludes production code and tests. |
| monograph drift | pass | No chapter edits. |
| vendored-code contamination | pass | Student code is not used; filterflow is external source/reference only. |
| high-dimensional-lane contamination | pass | No high-dimensional lane files are in the write set. |
| artifact answers question | pass | The artifacts compare paper settings, filterflow source/execution, and BayesFilter variants with discrepancy ledgers. |

## Stop Conditions

- exact Claude command/model/effort unavailable during required review;
- TF/TFP unavailable for BayesFilter runner;
- filterflow clone unavailable and no existing clone exists;
- filterflow execution requires modifying filterflow source;
- paper-vs-filterflow covariance ambiguity cannot be represented as primary
  implementation comparator plus paper-text sensitivity row;
- likelihood normalization cannot be confirmed as per-time
  `(estimate - exact) / T`;
- seed protocol cannot be recorded for data, initial particles, transition
  noise, and resampling randomness in the BayesFilter runner;
- dependency installation would require adding heavy dependencies without a
  reviewed plan;
- BayesFilter runner cannot set CPU-only before TensorFlow import;
- the audit would require production, tests, vendored, monograph, or highdim
  edits;
- non-finite core results in all comparable BayesFilter methods;
- JSON output cannot be parsed or reproduced for BayesFilter runner.

## Claude Review Protocol

Review this plan and the final result with:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Claude must return `ACCEPT` or `REJECT` with findings. Codex audits Claude's
findings. If rejected and Codex agrees, patch and resubmit. Loop until `ACCEPT`
or max five iterations. On iteration five, accept only for user inspection
unless there is a major blocker.

## Verification Commands

- `git status --short --branch`
- `git -C .localsource/filterflow rev-parse HEAD`
- `git -C .localsource/filterflow status --short --branch`
- result artifact contains paper-vs-filterflow settings ledger
- result artifact contains primary/sensitivity comparator table
- result artifact labels the primary decision lane exactly as
  `bayesfilter_scaled_ess` versus `filterflow_regularized`
- result artifact reports sensitivity outcomes separately and does not use a
  sensitivity lane to rescue a failed primary comparison
- result artifact contains the scaling and epsilon match ledger with
  `match_status`
- result artifact contains exact Kalman log likelihood per theta
- result artifact contains per-theta mean and standard deviation over 100
  realizations for each executed lane
- result artifact contains discrepancy ledger classifying mismatches as
  paper/code/environment/implementation
- `rg -n "student_dpf_baselines|vendor|highdim|NAWM|DSGE" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_cross_audit_tf.py`
- `rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp`
- `python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_cross_audit_tf.py`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_lgssm_cross_audit_tf`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_lgssm_cross_audit_tf --validate-only`
- JSON parse check for the new output file
- lane-scoped trailing whitespace check for touched plan/report/python files
- `git diff --check`
- `git status --short -- bayesfilter tests`
- `git status --short --branch`

## What Must Not Be Concluded

- Do not claim BayesFilter exactly reproduces filterflow unless the same model,
  random stream, covariance convention, scaling, epsilon, and resampling rule
  are matched.
- Do not claim finite Sinkhorn DET is categorical resampling.
- Do not claim finite Sinkhorn DET gives an unbiased likelihood estimator.
- Do not claim small Sinkhorn residuals validate likelihood, posterior, MLE, or
  gradient correctness.
- Do not claim a filterflow execution blocker is evidence against Corenflos.
- Do not claim general nonlinear-SSM or structural-model validity from this
  LGSSM audit.
- Do not claim production, public API, HMC, banking/model-risk, or monograph
  readiness.
