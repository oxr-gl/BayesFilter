from __future__ import annotations

import math

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


def _model() -> highdim.PredatorPreySSM:
    return highdim.p30_predator_prey_fixture_model()


def _theta() -> tf.Tensor:
    return _model().true_parameters()


def _manual_rhs(theta: tf.Tensor, state: tf.Tensor) -> tf.Tensor:
    r, k_capacity, a_half, s_rate, u_rate, v_rate = tf.unstack(theta)
    prey = state[0]
    predator = state[1]
    interaction = prey * predator / (a_half + prey)
    return tf.stack(
        [
            r * prey * (1.0 - prey / k_capacity) - s_rate * interaction,
            u_rate * interaction - v_rate * predator,
        ]
    )


def _manual_rk4(theta: tf.Tensor, initial: tf.Tensor, *, step: float, substeps: int) -> tf.Tensor:
    state = tf.convert_to_tensor(initial, dtype=tf.float64)
    h = tf.constant(step, dtype=tf.float64)
    for _ in range(int(substeps)):
        k1 = _manual_rhs(theta, state)
        k2 = _manual_rhs(theta, state + 0.5 * h * k1)
        k3 = _manual_rhs(theta, state + 0.5 * h * k2)
        k4 = _manual_rhs(theta, state + h * k3)
        state = state + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return state


def _normal_log_prob(value: tf.Tensor, loc: tf.Tensor, covariance: tf.Tensor) -> tf.Tensor:
    chol = tf.linalg.cholesky(covariance)
    centered = value - loc
    solve = tf.linalg.cholesky_solve(chol, tf.reshape(centered, [-1, 1]))[:, 0]
    dim = tf.cast(tf.shape(value)[0], tf.float64)
    log_det = 2.0 * tf.reduce_sum(tf.math.log(tf.linalg.diag_part(chol)))
    return -0.5 * (
        dim * tf.math.log(tf.constant(2.0 * math.pi, dtype=tf.float64))
        + log_det
        + tf.reduce_sum(centered * solve)
    )


def _matched_settings(**overrides: object) -> dict[str, object]:
    settings = {
        "observations_seed": 4401,
        "truth_seed": 4402,
        "prior": "theta_uniform_box_x0_normal",
        "parameter_box": tuple(_model().parameter_box().values()),
        "initial_state_prior": "N((50,5), I_2)",
        "delta": 2.0,
        "rk4_internal_step": 0.1,
        "process_covariance": "4 I_2",
        "observation_covariance": "4 I_2",
        "dtype": "tf.float64",
        "basis_family": "legendre",
        "basis_size": 9,
        "nominal_rank_cap": 10,
        "sweep_count": 1,
        "stopping_tolerance": 1e-8,
        "sample_count": 128,
        "wall_time_accounting_policy": "include_target_evaluations_and_ode_solves",
    }
    settings.update(overrides)
    return settings


def _metrics(**overrides: object) -> dict[str, float]:
    metrics = {
        "q_ess_linear_0p50": 42.0,
        "q_ess_nonlinear_0p50": 43.0,
        "wall_time_linear_seconds": 2.0,
        "wall_time_nonlinear_seconds": 4.0,
        "delta_ess": 1.0,
        "delta_cost": -10.25,
        "trajectory_rmse_linear": 0.5,
        "trajectory_rmse_nonlinear": 0.4,
    }
    metrics.update(overrides)
    return metrics


def _comparison_manifest(
    *,
    linear_settings: dict[str, object] | None = None,
    nonlinear_settings: dict[str, object] | None = None,
    metrics: dict[str, float] | None = None,
    promotion_decision: str = "FIRST_GATE_SCHEMA_ONLY",
) -> highdim.P30PredatorPreyComparisonManifest:
    return highdim.P30PredatorPreyComparisonManifest(
        version="p37.m4.predator_prey.comparison_schema.v1",
        linear_settings=_matched_settings() if linear_settings is None else linear_settings,
        nonlinear_settings=_matched_settings() if nonlinear_settings is None else nonlinear_settings,
        metrics=_metrics() if metrics is None else metrics,
        promotion_decision=promotion_decision,
        non_claims=(
            "no nonlinear preconditioning usefulness claim",
            "no matched linear/nonlinear comparison success claim",
        ),
    )


def test_p30_predator_prey_manifest_and_parameter_box_match_source_contract():
    model = _model()
    payload = model.manifest_payload()

    assert model.state_dim() == 2
    assert model.observation_dim() == 2
    assert model.parameter_dim() == 6
    assert model.validate_parameter_box(_theta())
    assert not model.validate_parameter_box(tf.constant([2.0, 114.0, 25.0, 0.3, 0.5, 0.5], dtype=tf.float64))
    assert payload["dimension_convention"] == "state is (P,Q); parameter is (r,K,a,s,u,v)"
    assert "eq:p27-pp8" in payload["source_equations"]
    assert "nonlinear_preconditioning_usefulness" in payload["what_is_not_claimed"]


def test_p30_predator_prey_rk4_transition_matches_independent_reference():
    model = _model()
    theta = _theta()
    initial = tf.constant([50.0, 5.0], dtype=tf.float64)

    expected = _manual_rk4(theta, initial, step=0.1, substeps=20)
    actual = model.transition_mean(theta, initial)[0]

    tf.debugging.assert_near(actual, expected, atol=2e-11)
    assert bool(tf.reduce_all(tf.math.is_finite(actual)).numpy())


def test_p30_predator_prey_transition_and_observation_densities_are_gaussian():
    model = _model()
    theta = _theta()
    previous = tf.constant([50.0, 5.0], dtype=tf.float64)
    mean = model.transition_mean(theta, previous)[0]
    next_state = mean + tf.constant([0.25, -0.5], dtype=tf.float64)
    observation = next_state + tf.constant([0.1, -0.2], dtype=tf.float64)

    transition = model.transition_log_density(theta, previous, next_state, t=1)[0]
    observation_log = model.observation_log_density(theta, next_state, observation, t=1)[0]

    tf.debugging.assert_near(
        transition,
        _normal_log_prob(next_state, mean, 4.0 * tf.eye(2, dtype=tf.float64)),
        atol=2e-14,
    )
    tf.debugging.assert_near(
        observation_log,
        _normal_log_prob(observation, next_state, 4.0 * tf.eye(2, dtype=tf.float64)),
        atol=2e-14,
    )


def test_p30_predator_prey_simulation_is_replayable_and_rmse_is_finite():
    model = _model()
    theta = _theta()

    x_left, y_left = model.simulate(theta, final_time=3, seed=4404)
    x_right, y_right = model.simulate(theta, final_time=3, seed=4404)
    estimates = []
    state = x_left[0]
    estimates.append(state)
    for _ in range(1, int(x_left.shape[0])):
        state = model.transition_mean(theta, state)[0]
        estimates.append(state)
    rmse = model.trajectory_rmse(x_left, tf.stack(estimates))
    diagnostics = model.domain_diagnostics(x_left)

    tf.debugging.assert_near(x_left, x_right, atol=0.0)
    tf.debugging.assert_near(y_left, y_right, atol=0.0)
    assert x_left.shape == (4, 2)
    assert y_left.shape == (4, 2)
    assert bool(tf.math.is_finite(rmse).numpy())
    assert float(rmse.numpy()) >= 0.0
    assert diagnostics["domain_policy"] == "diagnose_negative_after_noise"


def test_p30_predator_prey_comparison_manifest_accepts_schema_only_matched_row():
    manifest = _comparison_manifest()

    assert manifest.model_id is highdim.P30ModelSuiteModelID.PREDATOR_PREY
    assert manifest.promotion_decision == "FIRST_GATE_SCHEMA_ONLY"
    assert manifest.linear_settings["basis_size"] == manifest.nonlinear_settings["basis_size"]
    assert manifest.metrics["delta_ess"] == 1.0
    assert manifest.metrics["delta_cost"] < 0.0
    assert "no nonlinear preconditioning usefulness claim" in manifest.non_claims


def test_p30_predator_prey_comparison_manifest_rejects_unmatched_budget():
    with pytest.raises(ValueError, match="unmatched comparison settings"):
        _comparison_manifest(nonlinear_settings=_matched_settings(nominal_rank_cap=20))


def test_p30_predator_prey_comparison_manifest_rejects_proxy_only_promotion():
    with pytest.raises(ValueError, match="promotion requires positive delta_ess and delta_cost"):
        _comparison_manifest(promotion_decision="PROMOTE_NONLINEAR_USEFULNESS")

    with pytest.raises(ValueError, match="first gate cannot promote"):
        _comparison_manifest(
            metrics=_metrics(delta_cost=0.5),
            promotion_decision="PROMOTE_NONLINEAR_USEFULNESS",
        )


def test_p30_predator_prey_registry_records_first_gate_boundary():
    row = highdim.p30_model_suite_registry()["predator_prey"]

    assert row.status is highdim.ModelSuiteTraceabilityStatus.BAYESFILTER_EXTENSION
    assert row.implementation_status == "first_gate_model_contract_and_comparison_schema_only"
    assert row.test_status == "rk4_prior_likelihood_simulation_rmse_manifest_schema"
    assert "eq:p27-pp8" in row.source_equations
    assert "models.py" in row.bayesfilter_code_anchor
    assert "validation.py" in row.bayesfilter_code_anchor
    assert "test_p30_predator_prey.py" in row.bayesfilter_test_anchor
    assert any("no nonlinear preconditioning usefulness claim" in claim for claim in row.non_claims)
    assert any("no matched linear/nonlinear comparison success claim" in claim for claim in row.non_claims)
