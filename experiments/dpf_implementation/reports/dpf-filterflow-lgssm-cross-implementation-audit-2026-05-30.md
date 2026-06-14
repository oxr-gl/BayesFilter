# DPF Filterflow LGSSM Cross-Implementation Audit

## Decision

`red_flag`

Decision reason: primary BayesFilter scaled-ESS rows have Sinkhorn residual
vetoes, filterflow execution is blocked by dependency drift, and the
BayesFilter fixed-epsilon Sinkhorn policy is not a full match to filterflow's
epsilon annealing.

## Decision Table

| Check | Status | Evidence |
| --- | --- | --- |
| filterflow checkout | recorded | `5d8300ba247c4c17e1a301a22560c24fd0670bfe` |
| filterflow execution | `blocked_dependency_drift` | `external_execution_blocked_by_missing_pykalman_or_dependency` |
| primary BayesFilter lane | recorded | `bayesfilter_scaled_ess` |
| primary external lane | recorded | `filterflow_regularized` |
| scaling/epsilon match | `similar_not_matched` | fixed-epsilon BayesFilter runner does not implement filterflow annealing |
| primary rows executed | veto diagnostic | `3/9` |
| primary Sinkhorn residual vetoes | veto diagnostic | `6/9` |
| primary rows within paper SD | diagnostic | `3/9` |

## Interpretation

The BayesFilter runner executed bounded TF/TFP LGSSM rows for the filterflow-code
covariance variant and the paper-text covariance sensitivity variant. Original
filterflow execution is blocked in this environment by dependency drift, so the
decision cannot be stronger than execution-blocked or red-flagged source-level
evidence. In this run, the primary BayesFilter scaled-ESS lane also hit
Sinkhorn marginal residual vetoes for epsilon `0.25` and `0.5`, so the audit is
classified as a red flag rather than a source-consistent reproduction.

## Section 5.1 Settings Recovered

- Paper text model: two-dimensional LGSSM with diagonal transition
  `diag(theta_1, theta_2)`, observation matrix `I_2`, `T=150`, `N=25`, 100
  Monte Carlo realizations, theta grid `(0.25,0.25)`, `(0.5,0.5)`,
  `(0.75,0.75)`, and DPF epsilon values `0.25`, `0.5`, `0.75`.
- Paper text covariance: transition covariance `0.5 I_2`, observation
  covariance `0.1 I_2`.
- Filterflow `simple_linear_comparison.py` setting: transition covariance
  `I_2`, observation covariance `0.1 I_2`, Neff threshold `0.5`,
  `RegularisedTransform(epsilon=eps, scaling=0.9, convergence_threshold=1e-3)`.
- Filterflow `simple_linear_mle.py` uses transition covariance `0.5 I_2`, so
  the repository contains an unresolved comparison-versus-MLE covariance split.

## Scaling And Epsilon Match Ledger

| Field | Value |
| --- | --- |
| `filterflow_centering_formula` | x - stop_gradient(mean(x, axis=particles)) |
| `filterflow_scale_formula` | diameter(x, x) * sqrt(dimension), diameter=max coordinate std with zero fallback |
| `filterflow_scaled_particles_formula` | centered_x / stop_gradient(scale) |
| `filterflow_cost_formula` | squared distance / 2 on scaled particle cloud |
| `filterflow_epsilon_schedule` | epsilon_0=max_min(scaled_x, scaled_x)^2, geometric decrease by scaling^2 to target epsilon |
| `bayesfilter_scaled_cost_formula` | matches centering/scale/cost formula |
| `bayesfilter_epsilon_schedule` | similar_not_matched: fixed target epsilon for 100 log-domain iterations |
| `match_status` | similar_not_matched |
| `consequence` | consistent decision forbidden unless match_status is matched |

## Source-Level Filterflow Anchors

- `scripts/simple_linear_comparison.py`: Section-5.1-style likelihood table
  driver, but currently import-blocked by `pykalman`.
- `filterflow/resampling/differentiable/biased.py`: `RegularisedTransform`
  applies the transport matrix and resets weights on flagged particles.
- `filterflow/resampling/differentiable/regularized_transport/plan.py`: centers
  particles, scales by diameter times `sqrt(dimension)`, computes transport,
  and defines a custom gradient.
- `filterflow/resampling/differentiable/regularized_transport/sinkhorn.py`:
  starts epsilon at a squared max-min scale and geometrically anneals by
  `scaling^2` toward the target epsilon.

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

Classification mapping: the external filterflow lanes are fully blocked, not
partial executions. The BayesFilter primary lane is therefore classified as
`red_flag`, with a separate source-level external dependency blocker. The
plan's `partial_execution_red_flag` and `partial_pf_only_blocker` subclasses do
not apply because no executable filterflow grid cell completed.

## Kalman Reference Summary

| Spec | Theta | Mean log likelihood | Std log likelihood | Mean per-time | Std per-time |
| --- | --- | ---: | ---: | ---: | ---: |
| `primary_filterflow_code_covariance` | 0.25 | -456.759 | 15.3093 | -3.04506 | 0.102062 |
| `primary_filterflow_code_covariance` | 0.5 | -445.312 | 13.1405 | -2.96875 | 0.0876034 |
| `primary_filterflow_code_covariance` | 0.75 | -456.018 | 13.9682 | -3.04012 | 0.0931212 |
| `sensitivity_paper_text_covariance` | 0.25 | -366.898 | 15.0821 | -2.44599 | 0.100547 |
| `sensitivity_paper_text_covariance` | 0.5 | -356.762 | 13.0069 | -2.37841 | 0.0867125 |
| `sensitivity_paper_text_covariance` | 0.75 | -366.603 | 13.5195 | -2.44402 | 0.0901297 |

## Primary BayesFilter Scaled-ESS Rows

| epsilon | theta | status | mean error | std | paper mean | paper std | residual |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 0.25 | 0.25 | `sinkhorn_residual_veto` | N/A | N/A | -1.14 | 0.2 | 7.93697e-05 |
| 0.25 | 0.5 | `sinkhorn_residual_veto` | N/A | N/A | -0.94 | 0.18 | 7.93697e-05 |
| 0.25 | 0.75 | `sinkhorn_residual_veto` | N/A | N/A | -1.07 | 0.19 | 7.93697e-05 |
| 0.5 | 0.25 | `sinkhorn_residual_veto` | N/A | N/A | -1.14 | 0.2 | 4.86051e-05 |
| 0.5 | 0.5 | `sinkhorn_residual_veto` | N/A | N/A | -0.94 | 0.18 | 4.86051e-05 |
| 0.5 | 0.75 | `sinkhorn_residual_veto` | N/A | N/A | -1.08 | 0.18 | 4.86051e-05 |
| 0.75 | 0.25 | `executed` | -1.01786 | 0.256345 | -1.14 | 0.2 | 9.80533e-08 |
| 0.75 | 0.5 | `executed` | -0.885273 | 0.219452 | -0.94 | 0.18 | 9.91954e-08 |
| 0.75 | 0.75 | `executed` | -0.965631 | 0.243505 | -1.08 | 0.18 | 8.42253e-08 |

## BayesFilter PF Comparator Rows

| theta | status | mean error | std | paper mean | paper std | within paper SD |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 0.25 | `executed` | -0.995667 | 0.248037 | -1.13 | 0.2 | True |
| 0.5 | `executed` | -0.874662 | 0.208538 | -0.93 | 0.18 | True |
| 0.75 | `executed` | -0.97403 | 0.22653 | -1.05 | 0.17 | True |

## Red Flags

- The paper text says transition covariance `0.5 I_2`, while filterflow
  `simple_linear_comparison.py` uses `I_2`.
- Filterflow source-level import of `scripts.simple_linear_common` fails with
  `ModuleNotFoundError: No module named 'pykalman'`, so the original
  `filterflow_regularized` grid was not executed.
- BayesFilter scaled cost matches the filterflow centering/scale/cost formula,
  but this runner does not implement filterflow's epsilon annealing schedule.
- BayesFilter primary scaled-ESS rows execute only for epsilon `0.75`; epsilon
  `0.25` and `0.5` are vetoed by Sinkhorn residuals around `1e-4` to `5e-5`.
- Raw-cost Sinkhorn rows are vetoed across all three epsilon values in both the
  filterflow-code covariance and paper-text covariance variants.

## Artifacts

- JSON: `experiments/dpf_implementation/reports/outputs/dpf_filterflow_lgssm_cross_audit_2026-05-30.json`
- Report: `experiments/dpf_implementation/reports/dpf-filterflow-lgssm-cross-implementation-audit-2026-05-30.md`
- Runner: `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_cross_audit_tf.py`
- Reproducibility digest: `195012fb9e067253391ce09ee4fe2df17cc0558b1d6cc7ed966c8edf5edc8fb7`

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No HMC readiness is concluded.
- No posterior correctness is concluded.
- No general nonlinear-SSM validity is concluded.
- No learned or neural OT promotion is concluded.
- No banking or model-risk claim is concluded.
- No monograph claim is concluded.
