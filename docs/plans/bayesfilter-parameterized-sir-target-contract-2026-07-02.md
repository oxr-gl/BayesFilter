# Target Contract: Parameterized Zhao-Cui SIR Leaderboard Row

Date: 2026-07-02

Status: `DRAFT_PENDING_CLAUDE_REVIEW`

## Purpose

Define the free-theta SIR target that can repair the leaderboard behavior
without silently reinterpreting the existing fixed/no-free-theta source-parity
row.

## Row Identity

| Field | Value |
| --- | --- |
| Fixed source-parity row | `zhao_cui_spatial_sir_austria_j9_T20` |
| New parameterized row | `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` |
| Theta coordinate | `sir_log_scale_theta` |
| Truth theta | `[0.0, 0.0, 0.0]` |
| Truth theta semantics | Log-scale origin that reproduces fixed source base SIR parameters; not an author-source free-inference-theta claim |
| Parameter order | `log_kappa_scale`, `log_nu_scale`, `log_obs_noise_scale` |
| State dimension | 18 |
| Observation dimension | 9 |
| Horizon | 20 |
| Candidate evaluator route id | `multistate_nonlinear_fixed_design_tt_score_path` |
| Candidate published value implementation | `bayesfilter/highdim/filtering.py::multistate_nonlinear_fixed_design_tt_value_path`, returned as `FixedBranchScoreResult.log_likelihood` by `multistate_nonlinear_fixed_design_tt_score_path` |
| Candidate published score implementation | `bayesfilter/highdim/filtering.py::multistate_nonlinear_fixed_design_tt_score_path`, returned as `FixedBranchScoreResult.score` |
| Candidate local score hooks | `bayesfilter/highdim/models.py::ParameterizedZhaoCuiSIRSSM.initial_log_density_parameter_score`, `transition_log_density_parameter_score`, `observation_log_density_parameter_score` |
| Candidate route admission status | `PENDING_PHASE3_FULL_T20_EVALUATOR_CHECK` |

The fixed source-parity row remains fixed-target evidence and must not be
retired, replaced, or rank-compared as the same target without explicit human
authorization.

## Source And Local Code Anchors

The fixed SIR base formulas are source-anchored by
`docs/plans/bayesfilter-highdim-zhao-cui-p57-m1-author-model-callback-parity-result-2026-06-11.md`:

- author SIR setup uses fixed `theta=[.1,18]`, `sigma1=1`, `sigma2=10`;
- transition density uses `sir_step(x_{t-1}, theta)` and Gaussian process
  noise;
- observation likelihood uses infectious-coordinate observations and Gaussian
  observation noise;
- prior is Gaussian with the author prior mean/covariance;
- `zhao_cui_sir_austria_model()` is source-faithful for the fixed callback
  formulas plus fixed-HMC deterministic push adaptation.

The parameterized surface is locally anchored in
`bayesfilter/highdim/models.py`:

- `ParameterizedZhaoCuiSIRSSM.parameter_dim() == 3`;
- `kappa(theta) = base_kappa * exp(log_kappa_scale)`;
- `nu(theta) = base_nu * exp(log_nu_scale)`;
- `observation_covariance(theta) =
  base_observation_covariance * exp(2 * log_obs_noise_scale)`;
- initial density is independent of theta;
- transition and observation analytical score hooks are implemented.

Focused local tests:

- `tests/highdim/test_p81_analytical_sir_score.py::test_parameterized_zhao_cui_sir_matches_p8p_p79_theta_convention`;
- `tests/highdim/test_p81_analytical_sir_score.py::test_parameterized_sir_log_density_parameter_scores_match_diagnostic_tape`.

## Local Score-Route Math Contract Citations

The current Phase 1 contract cites the local score route as a candidate
mathematical implementation contract, not as full `T=20` row admission:

- `bayesfilter/highdim/filtering.py:1392` defines
  `multistate_nonlinear_fixed_design_tt_score_path`;
- `bayesfilter/highdim/filtering.py:1424`-`1470` routes multi-parameter
  scores through the same scalar-parameter score path and concatenates the
  returned analytical/manual scores while preserving the first returned
  `log_likelihood`;
- `bayesfilter/highdim/filtering.py:1501`-`1512` calls
  `multistate_nonlinear_fixed_design_tt_value_path` first, so the score route
  is bound to the same reviewed value path before derivative propagation;
- `bayesfilter/highdim/filtering.py:1521`-`1606` builds the per-time target
  derivative, solves the fixed-design least-squares derivative system, and
  accumulates derivative contributions to the log normalizer plus scale shift;
- `bayesfilter/highdim/filtering.py:1628` and
  `bayesfilter/highdim/filtering.py:1704`-`1709` sum the score terms and return
  `FixedBranchScoreResult(log_likelihood=value_result.log_likelihood,
  score=...)`;
- `bayesfilter/highdim/models.py:1034`-`1053` implements the analytical
  transition log-density parameter score for `ParameterizedZhaoCuiSIRSSM`;
- `bayesfilter/highdim/models.py:1055`-`1092` implements the analytical
  observation log-density parameter score;
- `bayesfilter/highdim/models.py:1104`-`1110` implements a theta-independent
  initial density and zero initial parameter score.

The local test contract currently covers:

- `tests/highdim/test_p81_analytical_sir_score.py:132`-`166`, which runs the
  score path on SIR `d=18` horizon-0 observation terms and verifies finite
  value, finite score, and same-branch finite-difference rows;
- `tests/highdim/test_p81_analytical_sir_score.py:169`-`199`, which records
  that the current all-grid two-row route is still blocked by the complexity
  gate and therefore is not full-row admission evidence;
- `tests/highdim/test_p81_analytical_sir_score.py:202`-`268`, which verifies
  the transition mean Jacobian and local transition/observation log-density
  parameter score hooks against diagnostic TensorFlow tapes.

These citations are sufficient for Phase 1 target binding only. Phase 3 must
still prove that the candidate route runs for the declared
`zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` row and returns
finite published value and finite analytical/manual score before leaderboard
admission.

## Classification

| Component | Classification | Reason |
| --- | --- | --- |
| Fixed SIR base formulas | `source_faithful` | Source-parity ledger anchors author setup, transition, observation, prior, graph, and RK convention. |
| Deterministic push replay for fixed branch | `fixed_hmc_adaptation` | Replaces random draws with supplied standard normals while preserving the source push route and clipping policy. |
| Three-parameter log-scale inference surface | `extension_or_invention` | The author SIR source is fixed-parameter for this example. The log-scale inference theta is a BayesFilter benchmark parameterization over the source-anchored formulas, not currently an author-source inference-theta claim. |

This classification is binding for leaderboard language. The parameterized row
may be described as source-anchored in its base formulas, but not
`source_faithful` as an inference parameterization unless a later source-anchor
phase proves that stronger claim.

## Mathematical And Operational Targets

Let

```text
theta = (theta_kappa, theta_nu, theta_obs)
```

with

```text
kappa_j(theta) = 0.1 * exp(theta_kappa)
nu_j(theta) = 18.0 * exp(theta_nu)
R(theta) = 100 I_9 * exp(2 theta_obs)
```

for all nine compartments. At `theta = [0, 0, 0]`, the parameterized model
equals the fixed source SIR base values: `kappa_j = 0.1`, `nu_j = 18.0`, and
observation standard deviation `10`.

## Theta Domain

The leaderboard row domain is a reviewed bounded diagnostic/inference
neighborhood around truth:

```text
theta_kappa in [-0.5, 0.5]
theta_nu in [-0.5, 0.5]
theta_obs in [-0.5, 0.5]
```

All dataset-generation, value, score, FD diagnostic, and score-at-true
diagnostic theta points used for admission must lie inside this domain and
must return finite model parameters, finite value, and finite score. This
domain is an admission/testing contract, not a claim that inference cannot be
run outside the interval after additional review.

Boundary/corner admission diagnostic:

- before leaderboard admission, evaluate the truth point `[0.0, 0.0, 0.0]`
  and all eight corners of `[-0.5, 0.5]^3` under the declared parameterized row
  and candidate evaluator route;
- at each of these nine points, require finite scaled SIR model parameters,
  finite candidate published value, and finite candidate analytical/manual
  score;
- if a cheaper preflight is run before the full evaluator, it may explain a
  failure but cannot replace the full boundary/corner admission diagnostic;
- any nonfinite parameter, nonfinite value, nonfinite score, route mismatch, or
  out-of-domain evaluation is a blocker that must be recorded before Phase 5.

The ideal observed-data likelihood for observations `y_{0:T-1}` is

```text
ell(theta; y) =
  log int p_theta(x_0)
          prod_{t=0}^{T-1} g_theta(y_t | x_t)
          prod_{t=1}^{T-1} f_theta(x_t | x_{t-1})
      dx_{0:T-1}.
```

This ideal likelihood is the mathematical reference target. The leaderboard
row is not allowed to claim that it computes this integral exactly.

The candidate published leaderboard value for this row is the reviewed
operational approximate observed-data filtering value emitted by
`bayesfilter/highdim/filtering.py::multistate_nonlinear_fixed_design_tt_value_path`
and returned by
`bayesfilter/highdim/filtering.py::multistate_nonlinear_fixed_design_tt_score_path`
as `FixedBranchScoreResult.log_likelihood`.

The candidate published leaderboard score is the analytical/manual derivative
computed by
`bayesfilter/highdim/filtering.py::multistate_nonlinear_fixed_design_tt_score_path`
and returned as `FixedBranchScoreResult.score`, using the
`ParameterizedZhaoCuiSIRSSM` local score hooks listed above. Phase 3 must prove
that this candidate route runs for the declared parameterized row at full
`T=20` before admission. Current horizon-0 evidence is not full-row admission.

Therefore Phase 3 and Phase 5 must bind three quantities explicitly:

- `ideal_reference_quantity`: the exact observed-data filtering
  log-likelihood above;
- `published_value_quantity`: the reviewed approximate filtering value
  computed by the named value implementation;
- `published_score_quantity`: the analytical/manual derivative of
  `published_value_quantity` as computed by the named score implementation,
  not merely a local complete-data score and not an unbound gradient of the
  ideal integral.

If the evaluator route changes the approximation, the score target changes
with that route and must be re-reviewed before leaderboard admission.

For this parameterization:

- `p_theta(x_0)` is independent of theta, so its parameter score is zero;
- `f_theta(x_t | x_{t-1})` depends on `theta_kappa` and `theta_nu` through the
  RK transition mean;
- `g_theta(y_t | x_t)` depends on `theta_obs` through observation covariance;
- the final full-row score must be bound to the analytical/manual derivative
  of the reviewed approximate observed-data filtering value route, not an
  autodiff or finite-difference leaderboard gradient.

## Truth-Theta Legitimacy

`truth_theta = [0, 0, 0]` is legitimate for this row because it exactly
reproduces the source base SIR parameters under the reviewed log-scale
parameterization. It is not a claim that the author source used free inference
theta for this example.

## Required Semantic-Binding Fields

Any final leaderboard row must bind:

- row id: `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`;
- theta coordinate: `sir_log_scale_theta`;
- truth theta: `[0.0, 0.0, 0.0]`;
- truth theta semantics;
- theta domain;
- parameter order;
- fixed base row id;
- source/adaptation classification;
- observed-data filtering target definition;
- published leaderboard value quantity and its relation to the ideal
  likelihood;
- published leaderboard score quantity and its relation to the published value
  quantity;
- evaluator route id: `multistate_nonlinear_fixed_design_tt_score_path`;
- published value implementation path and method names;
- analytical/manual score implementation path and method names;
- proof or local math-contract citation for the score route;
- boundary/corner diagnostic artifact covering truth plus all eight corners of
  `[-0.5, 0.5]^3`;
- validation artifacts;
- nonclaims.

## Required Validation Before Leaderboard Admission

- Dataset contract test proving the parameterized row does not regress to
  `no_free_theta`.
- Finite full observed-data/filtering value and finite analytical/manual score.
- Boundary/corner admission diagnostic over truth plus all eight corners of
  `[-0.5, 0.5]^3`, with finite scaled model parameters, finite candidate
  value, and finite analytical/manual score at every point.
- Analytical/manual score provenance in the leaderboard artifact.
- Local score identity tests.
- FD consistency as diagnostic only.
- Score-at-true multi-seed diagnostic using the owner-accepted rule.

The score-at-true rule for this program is:

- choose the reviewed truth theta, initially `[0.0, 0.0, 0.0]`;
- generate 10 datasets from the same parameterized model at that truth theta;
- compute 10 analytical/manual scores at that truth theta;
- for every parameter component, require the absolute sample mean score to be
  no larger than two sample standard deviations across the 10 scores;
- record the sample mean, sample standard deviation, component pass/fail, and
  seeds.

This rule is a consistency/admission diagnostic for the reviewed operational
approximate score. It is not proof that the score is the exact gradient of the
ideal observed-data likelihood.

## Admission Stop Conditions

The parameterized SIR row is not admissible if any of the following is true:

- target contract or semantic binding is missing;
- dataset contract test is missing or fails;
- local analytical score identity test is missing or fails;
- full observed-data/filtering value is missing or non-finite;
- analytical/manual score is missing or non-finite;
- any row-evaluated or diagnostic theta point lies outside the reviewed theta
  domain;
- any row-evaluated or diagnostic theta point gives non-finite model
  parameters, value, or score;
- leaderboard score provenance is autodiff or finite difference;
- score-at-true diagnostic is missing or fails;
- published value quantity and published score quantity are not bound to the
  same reviewed operational evaluator route and exact published value
  implementation path/method;
- the fixed source-parity row is replaced or retired without explicit human
  authorization.

## Forbidden Claims

- Do not claim exact likelihood correctness.
- Do not claim that the row score is the exact gradient of the exact
  observed-data filtering log-likelihood unless that equality is separately
  established by a reviewed derivation and checks.
- Do not claim source-faithful inference parameterization.
- Do not claim HMC readiness or GPU production readiness.
- Do not rank the fixed source-parity row and parameterized row as the same
  target.
- Do not admit autodiff or finite-difference gradients as leaderboard score
  provenance.
