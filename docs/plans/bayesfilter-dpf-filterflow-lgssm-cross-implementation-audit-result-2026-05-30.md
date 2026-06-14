# Result: Filterflow LGSSM Cross-Implementation Audit

## Decision

`red_flag`

Decision reason: the original filterflow execution is blocked, the BayesFilter
primary scaled-ESS grid is incomplete because of Sinkhorn residual vetoes, and
the BayesFilter fixed-epsilon Sinkhorn policy does not match filterflow's
epsilon annealing policy.

## Evidence Contract Status

Question: does BayesFilter's TF/TFP finite-Sinkhorn OT-DPF reproduce the
qualitative LGSSM behavior reported in Corenflos et al. Section 5.1 and encoded
in JTT94/filterflow when model, epsilon, cost scaling, particle count, time
horizon, resampling rule, and seed protocol are matched as closely as this
environment allows?

Answer: not established. The BayesFilter PF baseline is qualitatively close to
the reported PF table, but the primary BayesFilter scaled-ESS OT lane is not a
valid reproduction:

- original filterflow execution is blocked by dependency drift
  (`ModuleNotFoundError: No module named 'pykalman'`);
- BayesFilter scaled-cost Sinkhorn does not implement filterflow's epsilon
  annealing schedule;
- primary `bayesfilter_scaled_ess` runs only for epsilon `0.75`; epsilon `0.25`
  and `0.5` hit Sinkhorn marginal residual vetoes;
- the paper text and filterflow comparison script disagree on transition
  covariance.

## Artifacts

- Plan:
  `docs/plans/bayesfilter-dpf-filterflow-lgssm-cross-implementation-audit-plan-2026-05-30.md`
- Report:
  `experiments/dpf_implementation/reports/dpf-filterflow-lgssm-cross-implementation-audit-2026-05-30.md`
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_lgssm_cross_audit_2026-05-30.json`
- Runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_cross_audit_tf.py`

## Filterflow Source Status

- Checkout path: `.localsource/filterflow`
- Commit: `5d8300ba247c4c17e1a301a22560c24fd0670bfe`
- Dirty status: `## master...origin/master`
- Source treatment: read-only external reference source.
- Execution blocker: `scripts.simple_linear_common` imports `pykalman`, which
  is unavailable in the current environment.

## Section 5.1 Settings Recovered

- Paper text: two-dimensional LGSSM, diagonal transition
  `diag(theta_1, theta_2)`, transition covariance `0.5 I_2`, observation
  covariance `0.1 I_2`, `T=150`, `N=25`, 100 realizations, theta grid
  `(0.25,0.25)`, `(0.5,0.5)`, `(0.75,0.75)`, DPF epsilons `0.25`, `0.5`,
  `0.75`.
- Filterflow `scripts/simple_linear_comparison.py`: same theta grid, horizon,
  particle count, and observation covariance, but transition covariance `I_2`.
  It uses `RegularisedTransform(epsilon=eps, scaling=0.9,
  convergence_threshold=1e-3)` with a relative Neff threshold `0.5`.
- Filterflow `scripts/simple_linear_mle.py`: uses transition covariance
  `0.5 I_2`, so the external repository has an unresolved
  comparison-versus-MLE covariance split.

## Source-Level Implementation Discrepancies

| Dimension | Filterflow | BayesFilter audit runner | Status |
| --- | --- | --- | --- |
| cost centering | centered particles | centered particles | matched |
| cost scale | diameter times `sqrt(dimension)` | diameter times `sqrt(dimension)` | matched |
| cost formula | squared distance divided by 2 | squared distance divided by 2 | matched |
| epsilon policy | initialize at squared max-min scale, geometrically anneal by `scaling^2` to target | fixed target epsilon for 100 log-domain iterations | not matched |
| convergence policy | potential-update threshold, `convergence_threshold=1e-3` | marginal residual veto at `1e-5` | not matched |
| resampling trigger | relative Neff threshold `0.5` | ESS threshold `0.5` | conceptually matched |
| external execution | original filterflow code | blocked by missing `pykalman` | blocked |

## Required Scaling And Epsilon Ledger

| Field | Value |
| --- | --- |
| `filterflow_centering_formula` | `x - stop_gradient(mean(x, axis=particles))` |
| `filterflow_scale_formula` | `diameter(x, x) * sqrt(dimension)`, with diameter the maximum particle coordinate standard deviation and zero fallback |
| `filterflow_scaled_particles_formula` | `centered_x / stop_gradient(scale)` |
| `filterflow_cost_formula` | squared distance divided by `2` on the scaled particle cloud |
| `filterflow_epsilon_schedule` | `epsilon_0=max_min(scaled_x, scaled_x)^2`, geometric decrease by `scaling^2` down to target epsilon |
| `bayesfilter_scaled_cost_formula` | matches centering/scale/cost formula |
| `bayesfilter_epsilon_schedule` | `similar_not_matched`: fixed target epsilon for 100 log-domain iterations |
| `match_status` | `similar_not_matched` |
| `consequence` | `consistent` decision is forbidden unless `match_status == matched` |

## Comparator Outcome Matrix

| Lane | Role | Status | Executed cells | Expected cells | Mapping |
| --- | --- | --- | ---: | ---: | --- |
| `filterflow_regularized` | primary external implementation comparator | `blocked_dependency_drift` | 0 | 9 | `blocked_external_execution_not_partial_execution` |
| `filterflow_pf` | primary external PF comparator | `blocked_dependency_drift` | 0 | 3 | `blocked_external_execution_not_partial_pf_only_blocker` |
| `bayesfilter_scaled_ess` | primary BayesFilter implementation comparator | `partial_sinkhorn_residual_veto` | 3 | 9 | `red_flag` |
| `primary_filterflow_code_covariance:bayesfilter_pf` | BayesFilter PF comparator | `executed` | 3 | 3 | `pf_calibration` |
| `primary_filterflow_code_covariance:bayesfilter_raw_ess` | raw-cost Sinkhorn sensitivity | `partial_sinkhorn_residual_veto` | 0 | 9 | `sensitivity_only` |
| `primary_filterflow_code_covariance:bayesfilter_scaled_every_step` | every-step scaled Sinkhorn sensitivity | `partial_sinkhorn_residual_veto` | 3 | 9 | `sensitivity_only` |
| `sensitivity_paper_text_covariance:bayesfilter_pf` | paper-covariance PF sensitivity | `executed` | 3 | 3 | `sensitivity_only` |
| `sensitivity_paper_text_covariance:bayesfilter_raw_ess` | raw-cost Sinkhorn sensitivity | `partial_sinkhorn_residual_veto` | 0 | 9 | `sensitivity_only` |
| `sensitivity_paper_text_covariance:bayesfilter_scaled_every_step` | every-step scaled Sinkhorn sensitivity | `partial_sinkhorn_residual_veto` | 3 | 9 | `sensitivity_only` |

Classification reconciliation: the external filterflow lanes are fully blocked
by dependency drift, not partial executions. Therefore the plan's
`partial_execution_red_flag` and `partial_pf_only_blocker` subclasses do not
apply to filterflow. The overall plan vocabulary category is `red_flag` because
the BayesFilter primary lane is itself incomplete and the calibration is not a
full filterflow match.

## Exact Kalman Reference Summary

The JSON output stores the exact Kalman log likelihood for each of the 100
realizations. The human-readable summary is:

| Spec | Theta | Mean log likelihood | Std log likelihood | Mean per-time | Std per-time |
| --- | --- | ---: | ---: | ---: | ---: |
| `primary_filterflow_code_covariance` | 0.25 | -456.759293 | 15.309348 | -3.045062 | 0.102062 |
| `primary_filterflow_code_covariance` | 0.50 | -445.312150 | 13.140507 | -2.968748 | 0.087603 |
| `primary_filterflow_code_covariance` | 0.75 | -456.018100 | 13.968186 | -3.040121 | 0.093121 |
| `sensitivity_paper_text_covariance` | 0.25 | -366.897957 | 15.082115 | -2.445986 | 0.100547 |
| `sensitivity_paper_text_covariance` | 0.50 | -356.761937 | 13.006880 | -2.378413 | 0.086713 |
| `sensitivity_paper_text_covariance` | 0.75 | -366.602764 | 13.519459 | -2.444018 | 0.090130 |

## Primary BayesFilter Scaled-ESS Result

Primary lane: `bayesfilter_scaled_ess` with filterflow-code covariance
`I_2`.

| epsilon | theta | status | mean per-time error | std | paper mean | paper std | residual |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 0.25 | 0.25 | `sinkhorn_residual_veto` | N/A | N/A | -1.14 | 0.20 | 7.93697e-05 |
| 0.25 | 0.50 | `sinkhorn_residual_veto` | N/A | N/A | -0.94 | 0.18 | 7.93697e-05 |
| 0.25 | 0.75 | `sinkhorn_residual_veto` | N/A | N/A | -1.07 | 0.19 | 7.93697e-05 |
| 0.50 | 0.25 | `sinkhorn_residual_veto` | N/A | N/A | -1.14 | 0.20 | 4.86051e-05 |
| 0.50 | 0.50 | `sinkhorn_residual_veto` | N/A | N/A | -0.94 | 0.18 | 4.86051e-05 |
| 0.50 | 0.75 | `sinkhorn_residual_veto` | N/A | N/A | -1.08 | 0.18 | 4.86051e-05 |
| 0.75 | 0.25 | `executed` | -1.01786 | 0.256345 | -1.14 | 0.20 | 9.80533e-08 |
| 0.75 | 0.50 | `executed` | -0.885273 | 0.219452 | -0.94 | 0.18 | 9.91954e-08 |
| 0.75 | 0.75 | `executed` | -0.965631 | 0.243505 | -1.08 | 0.18 | 8.42253e-08 |

Summary: `3/9` primary rows executed, `6/9` were vetoed by Sinkhorn residuals,
and the `3/9` executed rows were within one reported paper standard deviation.

## PF Comparator Result

BayesFilter PF with filterflow-code covariance qualitatively matches the
reported PF table within the one-standard-deviation reproduction-audit band:

| theta | mean per-time error | std | paper mean | paper std | within paper SD |
| --- | ---: | ---: | ---: | ---: | --- |
| 0.25 | -0.995667 | 0.248037 | -1.13 | 0.20 | true |
| 0.50 | -0.874662 | 0.208538 | -0.93 | 0.18 | true |
| 0.75 | -0.974030 | 0.226530 | -1.05 | 0.17 | true |

This PF result is useful as a calibration sanity check, but it does not rescue
the primary OT-DPF lane.

## Red-Flag Ledger

| Red flag | Classification | Consequence |
| --- | --- | --- |
| filterflow original LGSSM script cannot execute because `pykalman` is missing | environment/dependency | no executable filterflow comparator yet |
| paper text transition covariance `0.5 I_2` versus `simple_linear_comparison.py` covariance `I_2` | paper/code | paper Table 1 alignment remains ambiguous |
| BayesFilter fixed-epsilon Sinkhorn does not implement filterflow epsilon annealing | implementation/calibration | no exact method match |
| BayesFilter scaled-ESS rows veto at epsilon `0.25` and `0.5` | implementation/numerical | primary grid incomplete |
| raw-cost Sinkhorn vetoes across all epsilon values | implementation/numerical | raw-cost path is not a plausible reproduction of Section 5.1 |

## Verification Run Manifest

- Command:
  `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_lgssm_cross_audit_tf`
- Validation command:
  `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_lgssm_cross_audit_tf --validate-only`
- Py compile:
  `python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_cross_audit_tf.py` passed.
- Import-boundary check:
  `rg -n "student_dpf_baselines|vendor|highdim|NAWM|DSGE" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_cross_audit_tf.py` returned no matches.
- NumPy gate:
  `rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp` returned no matches.
- JSON parse:
  `python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_lgssm_cross_audit_2026-05-30.json` passed.
- Lane-scoped trailing whitespace:
  `rg -n "[[:blank:]]$" ...` over the touched plan, result, report, and runner returned no matches.
- `git diff --check` passed.
- Production/tests check:
  `git status --short -- bayesfilter tests` returned no matches.
- Final `git status --short --branch`:
  branch is `## main...origin/main [ahead 5]`; the worktree contains many
  pre-existing unrelated modified/untracked docs and experiment artifacts.
  Audit-owned additions are the plan, result, runner, report, and JSON output
  paths listed above.
- Write-set ledger:
  touched audit files stayed within `docs/plans`,
  `experiments/dpf_implementation/tf_tfp/runners`,
  `experiments/dpf_implementation/reports`, and
  `experiments/dpf_implementation/reports/outputs`.
- Forbidden write-set ledger:
  no production `bayesfilter/`, `tests/`, vendored student code, monograph
  chapters, or high-dimensional lane files were edited by this audit.
- CPU-only status: `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import.
- TensorFlow: `2.19.1`
- TensorFlow Probability: `0.25.0`
- Wall time: approximately 86 seconds for the final bounded run.
- Reproducibility digest:
  `195012fb9e067253391ce09ee4fe2df17cc0558b1d6cc7ed966c8edf5edc8fb7`

## What Is Not Concluded

- No production readiness.
- No public API readiness.
- No HMC readiness.
- No posterior correctness.
- No general nonlinear-SSM validity.
- No claim that filterflow or Corenflos is wrong.
- No claim that BayesFilter reproduces Section 5.1 until filterflow executes
  and the epsilon/covariance conventions are matched.

## Next Recommended Action

Create a narrow follow-up plan to run filterflow in an isolated legacy
environment with `pykalman`, then implement a BayesFilter experimental
filterflow-style Sinkhorn option that matches the epsilon annealing and
convergence policy before repeating the LGSSM comparison.
