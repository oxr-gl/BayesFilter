# Semantic Binding: Parameterized Zhao-Cui SIR Leaderboard Row

Date: 2026-07-02

Status: `DRAFT_PENDING_CLAUDE_REVIEW`

## Binding Purpose

This artifact is the canonical binding between the repaired leaderboard row,
the reviewed theta contract, the evaluator route, and the admitted
analytical/manual score provenance.

## Current Binding State

| Field | Current value |
| --- | --- |
| Binding status | `DATASET_ROW_CONTRACT_IMPLEMENTED_PENDING_EVALUATOR` |
| Target contract | `docs/plans/bayesfilter-parameterized-sir-target-contract-2026-07-02.md` |
| Fixed source row | `zhao_cui_spatial_sir_austria_j9_T20` |
| Parameterized row | `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` |
| Theta coordinate | `sir_log_scale_theta` |
| Truth theta | `[0.0, 0.0, 0.0]` |
| Truth theta semantics | Log-scale origin that reproduces fixed source base SIR parameters; not an author-source free-inference-theta claim |
| Theta domain | `[-0.5, 0.5]^3` for admission diagnostics |
| Parameter order | `log_kappa_scale`, `log_nu_scale`, `log_obs_noise_scale` |
| Classification | `extension_or_invention` for inference theta over source-anchored fixed SIR formulas |
| Evaluator route | `bayesfilter/highdim/filtering.py::multistate_nonlinear_fixed_design_tt_score_path` |
| Ideal reference quantity | Exact observed-data filtering log-likelihood; not claimed exact by leaderboard row |
| Published value quantity | Reviewed approximate fixed-design TT filtering value returned as `FixedBranchScoreResult.log_likelihood` |
| Published score quantity | Analytical/manual derivative of published value returned as `FixedBranchScoreResult.score` |
| Published value implementation | `bayesfilter/highdim/filtering.py::multistate_nonlinear_fixed_design_tt_value_path`, as called by `multistate_nonlinear_fixed_design_tt_score_path` |
| Published score implementation | `bayesfilter/highdim/filtering.py::multistate_nonlinear_fixed_design_tt_score_path` |
| Local score-route math contract | `bayesfilter/highdim/filtering.py:1392`-`1709`; local SIR score hooks at `bayesfilter/highdim/models.py:1034`-`1110`; local test contract at `tests/highdim/test_p81_analytical_sir_score.py:132`-`268` |
| Boundary/corner admission diagnostic | Required before admission: truth `[0.0, 0.0, 0.0]` plus all eight corners of `[-0.5, 0.5]^3`, each with finite scaled SIR parameters, finite candidate published value, and finite candidate analytical/manual score |
| Dataset manifest artifact | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.json` |
| Dataset manifest SHA256 | `77af3011569d4ed158ef736f3f5f9fdbb58fc84c08f99bc36e9b59f02fc6abfc` |
| Parameterized dataset row SHA256 | `46c5f88b1563f16723f6a92be8367b2ac9c5172664e248b54bd2731302b409ad` |
| Fixed dataset row SHA256 | `591c97ae11254441d6098bf148b1ad4d710dc013ad78403d2a154a535cc0ff2f` |
| Fixed row preservation | Preserved as `truth_theta_coordinate = no_free_theta`, `truth_theta = []`; not replaced or retired |
| Leaderboard admission | `NOT_ADMITTED` |

## Required Final Binding Fields

Before Phase 5 can pass, this artifact must contain:

- final dataset row artifact path and row hash;
- final evaluator route id and implementation path;
- final published value implementation path and method names;
- final ideal reference quantity;
- final published value quantity;
- final published score quantity;
- final analytical/manual score implementation path and method names;
- final local score-route math contract citation or proof artifact path;
- final boundary/corner diagnostic artifact path covering truth plus all eight
  corners of `[-0.5, 0.5]^3`;
- final truth theta semantics and theta-domain preservation statement;
- final validation artifact paths;
- final leaderboard JSON/MD paths and row hash;
- statement that the fixed row remains preserved as fixed-target evidence;
- statement that the parameterized row is not source-faithful as an inference
  parameterization unless later source anchors prove otherwise;
- statement that no autodiff or finite-difference gradient is admitted as the
  leaderboard score.

## Current Dataset Binding Evidence

- The parameterized row is present with row id
  `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`.
- The parameterized row declares `truth_theta_coordinate =
  sir_log_scale_theta`, `truth_theta = [0.0, 0.0, 0.0]`, the reviewed
  parameter order, the reviewed theta domain, and
  `fixed_base_model_row_id = zhao_cui_spatial_sir_austria_j9_T20`.
- The fixed source row remains present with `truth_theta_coordinate =
  no_free_theta` and `truth_theta = []`.
- The parameterized row uses the same generated observations/states as the
  fixed row at truth theta because the log-scale origin reproduces the fixed
  source SIR base values.

## Current Nonclaims

- No full observed-data/filtering evaluator route is admitted.
- No leaderboard score is admitted.
- No exact likelihood, HMC readiness, GPU production readiness, or
  source-faithful inference-theta claim is made.
- No claim is made that the score is the exact gradient of the exact
  observed-data filtering likelihood.
