# Phase 1 Result: Scalar Posterior/Reference Oracle Design

Date: 2026-07-06

Status: `PASSED_PHASE2_REVIEW_CONVERGED_VALUE_TOLERANCE_REPAIRED`

## Phase Objective

Design the smallest independent reference artifact for the minimal
`zhaocui_fixed` HMC target so later HMC diagnostics can be compared against a
predeclared target/reference surface rather than launch, acceptance, or finite
sample checks alone.

## Key Finding

The fixture is scalar in model dimensions, but not scalar in parameter
dimension:

- horizon: 2
- latent dimension: 1
- hidden dimension: 1
- observation dimension: 1
- parameter dimension: 24

Therefore a full 24-dimensional quadrature posterior reference is not a
credible minimal Phase 2 artifact. Phase 2 should instead build a conditional
one-dimensional slice oracle over selected parameter coordinates, paired with
local value/score checks. This can detect target implementation drift and
conditional posterior geometry mismatches, but it cannot certify the full
posterior or HMC convergence.

## Skeptical Audit

Result: `PASS_WITH_NARROWED_CLAIM`.

| Risk checked | Phase 1 disposition |
| --- | --- |
| Wrong baseline | Uses `hmc-next` Phase 5 only as mechanics context; reference design targets the current internal adapter. |
| Proxy metric promotion | Acceptance, runtime, and short sample summaries remain explanatory only. |
| Missing stop condition | Phase 2 stops on missing independence, nonfinite values, mass/domain failure, value mismatch, gradient mismatch, or unsupported claim. |
| Unfair comparison | No ranking or HMC comparison is allowed in Phase 2. |
| Hidden assumption | Full 24D posterior reference is explicitly out of scope. |
| Environment mismatch | Phase 2 is CPU-hidden debug/reference only and must record that status. |
| Artifact mismatch | Phase 2 artifact schema is predeclared below. |

## Research Intent Ledger

| Field | Ledger |
| --- | --- |
| Main question | Can a minimal independent reference artifact distinguish target/log-density errors from sampler launch mechanics? |
| Candidate/mechanism under test | Independent NumPy scalar replay value oracle plus TensorFlow same-scalar finite-difference score checks on selected parameter coordinates. |
| Expected failure mode | Reference is accidentally coupled to TensorFlow target code, grid misses posterior mass, tolerances are unsupported, or the artifact is mistaken for full posterior correctness. |
| Promotion criterion | Phase 2 implements the predeclared reference harness and produces a valid JSON/Markdown artifact with no hard vetoes. |
| Promotion veto | Nonfinite target/reference values, reference/target value mismatch outside hypothesis tolerance, finite-difference score mismatch outside hypothesis tolerance, insufficient domain mass, schema invalidity, or circular reference construction. |
| Continuation veto | Need for package install, network fetch, GPU/HMC runtime, public API/default-policy change, source-faithful claim, or long runtime. |
| Repair trigger | Any Phase 2 hard veto should trigger local target/reference localization before longer HMC. |
| Explanatory diagnostics | Runtime, coordinate rows, grid bounds, log-sum-exp normalization, posterior mass-at-boundary indicators, conditional means/standard deviations, and selected finite-difference residuals. |
| Must not conclude | Full posterior correctness, HMC convergence, ranking, readiness, source-faithful parity, or LEDH evidence. |

## Phase 2 Oracle Design

Phase 2 will add a dedicated debug/reference harness under:

- `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_oracle_2026_07_06.py`

The harness is a reference artifact, not a BayesFilter-owned differentiable
algorithmic backend. NumPy is allowed only for this independent reference,
reporting, and finite-grid calculations under the repository governance
exception for independent reference solutions.

### Target Quantity

The target quantity is the scalar log density returned by:

- `MinimalZhaoCuiHMCTargetAdapter.log_prob_and_grad(theta)[0]`

at the frozen minimal fixture, including:

- fixed `zhaocui_fixed` replay log likelihood;
- Gaussian prior centered at `minimal_ssl_lstm_theta()`;
- `prior_scale = 5.0`;
- deterministic near-center point from
  `initial_minimal_ssl_lstm_hmc_state(1.0e-3)`.

### Independent Reference Approximation

The independent reference value oracle recomputes the frozen scalar replay in
plain NumPy expressions inside the harness, including:

- parameter unpacking and softplus covariance transforms;
- stateless normal draws materialized once from the TensorFlow fixture seeds and
  recorded in the artifact;
- scalar LSTM transition and scalar observation likelihood;
- fixed replay log-mean-exp likelihood;
- Gaussian prior contribution.

This reference may import TensorFlow only to obtain the deterministic fixture
values/noise arrays and to compare against the implementation target. The
actual reference replay arithmetic must not call
`tf_ssl_lstm_zhaocui_fixed_score`,
`MinimalZhaoCuiHMCTargetAdapter.log_prob_and_grad`, TensorFlow autodiff, or the
TensorFlow transition/observation helper functions.

### Conditional Slice Surface

Phase 2 will evaluate one-dimensional conditional grids with all other
coordinates fixed at the near-center point. The initial selected coordinates
are:

| Index | Name | Reason |
| --- | --- | --- |
| 0 | `lstm_input.input.0.0` | LSTM input gate weight |
| 4 | `lstm_recurrent.input.0.0` | recurrent gate weight |
| 8 | `lstm_bias.input.0` | gate bias |
| 12 | `latent_mean_weight.0.0` | transition mean scale |
| 13 | `latent_mean_bias.0` | transition mean bias |
| 14 | `observation_weight.0.0` | observation loading |
| 15 | `observation_bias.0` | observation intercept |
| 16 | `initial_mean.0` | latent initial mean |
| 19 | `initial_std_unconstrained.0` | latent initial scale transform |
| 22 | `process_std_unconstrained.0` | process scale transform |
| 23 | `observation_std_unconstrained.0` | observation scale transform |

These coordinates extend the previous smoke finite-difference subset with the
observation-scale coordinate.

### Grid And Domain Hypotheses

Phase 2 predeclares these hypothesis settings:

- grid half-widths: `0.5`, `1.0`, `2.0`, `5.0`, `10.0`, and `20.0`
  per coordinate;
- grid point count per coordinate/width: `401`;
- default retained slice for result summaries: narrowest width whose estimated
  normalized edge mass is at most `1.0e-4` on both edges;
- hard veto if no tested width reaches the edge-mass hypothesis for any
  required coordinate;
- log-sum-exp normalization over each conditional grid with uniform spacing;
- conditional mean, standard deviation, MAP grid point, edge mass, and
  normalization constant recorded per coordinate.

The edge-mass threshold is a reviewed hypothesis for minimal conditional-slice
evidence. It is not a proof of full posterior mass coverage.

Repair note: the original Phase 1 draft listed maximum half-width `2.0`. A
pre-implementation skeptical audit found that this was too narrow for a
Gaussian prior with `prior_scale = 5.0`: prior-dominated directions could fail
the edge-mass check because the domain was still inside the prior bulk. The
expanded width ladder keeps the same edge-mass veto but gives the domain check
a chance to distinguish broad conditional slices from implementation failure.

### Value And Score Tolerances

Phase 2 predeclares these hypothesis tolerances:

- target/reference scalar value mismatch at grid points: absolute error
  `<= 1.0e-9` or relative error `<= 1.0e-12`;
- central finite-difference score step: `1.0e-5`;
- finite-difference score max absolute mismatch on selected coordinates:
  `1.0e-3`;
- deterministic repeat max absolute delta: `1.0e-12`.

The value tolerance is strict near ordinary log-density magnitudes while
allowing machine-epsilon relative agreement at extreme negative log densities
on wide scale-transform grids. The finite-difference tolerance is looser
because it is a numerical derivative diagnostic, not an exact score proof.

### Artifact Schema

Phase 2 JSON must include:

- `schema_version`;
- `status`;
- `artifact_role`;
- `target_quantity`;
- `reference_independence_contract`;
- `fixture`;
- `selected_coordinates`;
- `grid_settings`;
- `tolerances`;
- `target_reference_value_check`;
- `finite_difference_score_check`;
- `conditional_slice_rows`;
- `hard_vetoes`;
- `diagnostic_roles`;
- `decision_table`;
- `run_manifest`;
- `nonclaims`.

Phase 2 Markdown must summarize the same gate fields without implying full
posterior validity.

## Phase 2 Evidence Roles

| Diagnostic | Role |
| --- | --- |
| Reference implementation independence | promotion veto |
| Target/reference value mismatch | promotion veto |
| Nonfinite target/reference values | promotion veto |
| Determinism repeat delta | promotion veto |
| Finite-difference score mismatch | promotion veto for local score consistency |
| Conditional grid edge mass | promotion veto for selected slice adequacy |
| Conditional means/std/MAP | explanatory |
| Runtime | explanatory |
| Previous HMC acceptance/sample summaries | explanatory context only |

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Refresh Phase 2 subplan and review it before implementation. |
| Primary criterion status | Passed: concrete Phase 2 reference method, target quantity, grid/domain checks, tolerances, artifacts, and nonclaims are specified. |
| Veto diagnostic status | No Phase 1 veto fired. |
| Main uncertainty | Conditional slices may reveal local target issues but cannot represent the full 24D posterior. |
| Next justified action | Review and execute Phase 2 oracle implementation if the refreshed subplan converges. |
| What is not concluded | Posterior correctness, HMC convergence, R-hat/ESS, ranking, default readiness, production readiness, public API readiness, source-faithful parity, or LEDH evidence. |

## Phase 2 Handoff

Proceed to Phase 2 only after material review of:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase2-oracle-implementation-subplan-2026-07-06.md`

If review requires repairs, patch the same subplan visibly and rerun focused
checks/review. If review does not converge after five rounds for the same
blocker, stop with a blocker result.
