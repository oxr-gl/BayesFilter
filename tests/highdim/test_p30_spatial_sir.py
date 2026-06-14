from __future__ import annotations

import math

import tensorflow as tf

import bayesfilter.highdim as highdim


def _sir_j1() -> highdim.SpatialSIRSSM:
    return highdim.SpatialSIRSSM(
        kappa=tf.constant([0.1], dtype=tf.float64),
        nu=tf.constant([18.0], dtype=tf.float64),
        initial_mean=tf.constant([486.0, 14.0], dtype=tf.float64),
        neighbor_sets=((),),
        delta=0.02,
        rk4_internal_step=0.005,
        process_covariance=tf.eye(2, dtype=tf.float64),
        observation_covariance=100.0 * tf.eye(1, dtype=tf.float64),
        initial_covariance=tf.eye(2, dtype=tf.float64),
    )


def _sir_j3() -> highdim.SpatialSIRSSM:
    return highdim.p30_spatial_sir_fixture_model(3)


def _manual_j1_rhs(state: tf.Tensor) -> tf.Tensor:
    susceptible = state[0]
    infectious = state[1]
    infection = tf.constant(0.1, dtype=tf.float64) * susceptible * infectious
    return tf.stack(
        [
            -infection,
            infection - tf.constant(18.0, dtype=tf.float64) * infectious,
        ]
    )


def _manual_j1_rk4(initial: tf.Tensor, *, step: float, substeps: int) -> tf.Tensor:
    state = tf.convert_to_tensor(initial, dtype=tf.float64)
    h = tf.constant(step, dtype=tf.float64)
    for _ in range(int(substeps)):
        k1 = _manual_j1_rhs(state)
        k2 = _manual_j1_rhs(state + 0.5 * h * k1)
        k3 = _manual_j1_rhs(state + 0.5 * h * k2)
        k4 = _manual_j1_rhs(state + h * k3)
        state = state + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return state


def _normal_log_prob(value: tf.Tensor, loc: tf.Tensor, covariance: tf.Tensor) -> tf.Tensor:
    chol = tf.linalg.cholesky(covariance)
    solve = tf.linalg.cholesky_solve(chol, tf.reshape(value - loc, [-1, 1]))[:, 0]
    dim = tf.cast(tf.shape(value)[0], tf.float64)
    log_det = 2.0 * tf.reduce_sum(tf.math.log(tf.linalg.diag_part(chol)))
    return -0.5 * (
        dim * tf.math.log(tf.constant(2.0 * math.pi, dtype=tf.float64))
        + log_det
        + tf.reduce_sum((value - loc) * solve)
    )


def test_p30_sir_fixture_manifest_matches_source_contract():
    model = _sir_j3()
    payload = model.manifest_payload()

    assert model.parameter_dim() == 0
    assert model.state_dim() == 6
    assert model.observation_dim() == 3
    assert model.observed_state_indices() == (1, 3, 5)
    assert model.unobserved_state_indices() == (0, 2, 4)
    assert payload["dimension_convention"] == "state is (S_1,I_1,...,S_J,I_J) in R^{2J}; R is eliminated"
    assert payload["observation_convention"] == "infectious coordinates only"
    assert payload["domain_policy"] == "diagnose_negative_after_noise"
    assert "eq:p27-sir6" in payload["source_equations"]
    assert "eq:p27-sir11" in payload["source_equations"]
    assert "production_tt_sirt_sir_filtering" in payload["what_is_not_claimed"]


def test_p30_sir_rk4_transition_matches_independent_j1_reference():
    model = _sir_j1()
    initial = tf.constant([486.0, 14.0], dtype=tf.float64)

    expected = _manual_j1_rk4(initial, step=0.005, substeps=4)
    actual = model.transition_mean(initial)[0]

    tf.debugging.assert_near(actual, expected, atol=2e-12)
    assert bool(tf.reduce_all(tf.math.is_finite(actual)).numpy())


def test_p30_sir_observation_uses_only_infectious_coordinates():
    model = _sir_j3()
    state = tf.constant([[486.0, 14.0, 487.0, 13.0, 488.0, 12.0]], dtype=tf.float64)
    observation = tf.constant([13.5, 12.5, 12.25], dtype=tf.float64)

    actual = model.observation_log_density(tf.zeros([0], dtype=tf.float64), state, observation, t=0)[0]
    expected = _normal_log_prob(
        observation,
        tf.constant([14.0, 13.0, 12.0], dtype=tf.float64),
        100.0 * tf.eye(3, dtype=tf.float64),
    )

    tf.debugging.assert_near(actual, expected, atol=2e-14)

    susceptible_changed = tf.constant([[999.0, 14.0, 111.0, 13.0, 222.0, 12.0]], dtype=tf.float64)
    unchanged = model.observation_log_density(
        tf.zeros([0], dtype=tf.float64),
        susceptible_changed,
        observation,
        t=0,
    )[0]
    tf.debugging.assert_near(actual, unchanged, atol=0.0)


def test_p30_sir_transition_density_is_gaussian_around_rk4_mean():
    model = _sir_j1()
    previous = tf.constant([486.0, 14.0], dtype=tf.float64)
    mean = model.transition_mean(previous)[0]
    next_state = mean + tf.constant([0.25, -0.5], dtype=tf.float64)

    actual = model.transition_log_density(
        tf.zeros([0], dtype=tf.float64),
        previous,
        next_state,
        t=1,
    )[0]
    expected = _normal_log_prob(next_state, mean, tf.eye(2, dtype=tf.float64))

    tf.debugging.assert_near(actual, expected, atol=2e-14)
    assert bool(tf.math.is_finite(actual).numpy())


def test_p30_sir_simulation_is_replayable_and_records_domain_policy():
    model = _sir_j3()

    x_left, y_left = model.simulate(final_time=3, seed=3703)
    x_right, y_right = model.simulate(final_time=3, seed=3703)
    diagnostics = model.domain_diagnostics(x_left)

    tf.debugging.assert_near(x_left, x_right, atol=0.0)
    tf.debugging.assert_near(y_left, y_right, atol=0.0)
    assert x_left.shape == (4, 6)
    assert y_left.shape == (4, 3)
    assert diagnostics["domain_policy"] == "diagnose_negative_after_noise"
    assert bool(tf.math.is_finite(diagnostics["min_state"]).numpy())


def test_p30_sir_observed_and_unobserved_rmse_are_reported_separately():
    model = _sir_j3()
    truth, _observations = model.simulate(final_time=2, seed=3704)
    estimates = []
    state = truth[0]
    estimates.append(state)
    for _ in range(1, int(truth.shape[0])):
        state = model.transition_mean(state)[0]
        estimates.append(state)
    estimate_path = tf.stack(estimates)

    metrics = model.observed_unobserved_rmse(truth, estimate_path)

    assert set(metrics) == {"rmse_observed", "rmse_unobserved"}
    assert bool(tf.math.is_finite(metrics["rmse_observed"]).numpy())
    assert bool(tf.math.is_finite(metrics["rmse_unobserved"]).numpy())
    assert float(metrics["rmse_observed"].numpy()) >= 0.0
    assert float(metrics["rmse_unobserved"].numpy()) >= 0.0


def test_p30_sir_registry_promotes_only_first_gate_boundary():
    row = highdim.p30_model_suite_registry()["spatial_sir"]

    assert row.status is highdim.ModelSuiteTraceabilityStatus.BAYESFILTER_EXTENSION
    assert row.bayesfilter_code_anchor == "bayesfilter/highdim/models.py"
    assert row.bayesfilter_test_anchor == "tests/highdim/test_p30_spatial_sir.py"
    assert row.implementation_status == "first_gate_model_contract_only"
    assert "eq:p27-sir10" in row.source_equations
    assert any("not production TT/SIRT SIR filtering" in claim for claim in row.non_claims)
    assert any("not paper-scale J=9 accuracy" in claim for claim in row.non_claims)
    assert any("no partial-observation scalability claim" in claim for claim in row.non_claims)
