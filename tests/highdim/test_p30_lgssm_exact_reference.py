from __future__ import annotations

import math

import tensorflow as tf

import bayesfilter.highdim as highdim


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _filter_config(state_dim: int, seed: str = "p37-m1-lgssm") -> highdim.FixedBranchFilterConfig:
    return highdim.FixedBranchFilterConfig(
        fit_config=None,
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(highdim.IdentityCoordinateMap(state_dim),),
        measure_convention=_convention(),
        deterministic_seed=seed,
    )


def _p30_observation_matrix(state_dim: int = 3, obs_dim: int = 3) -> tf.Tensor:
    """Deterministic clean-room observation matrix for the P30 LGSSM shape."""

    base = tf.constant(
        [
            [0.45, -0.10, 0.25],
            [0.15, 0.55, -0.20],
            [-0.30, 0.20, 0.50],
        ],
        dtype=tf.float64,
    )
    return base[:obs_dim, :state_dim]


def _p30_lgssm_model(
    *,
    process_noise_scale: float,
    observation_noise_scale: float,
    state_dim: int = 3,
    obs_dim: int = 3,
    mu: float = 0.0,
) -> highdim.LinearGaussianSSM:
    """Build the P30-shaped LGSSM for a fixed physical theta=(a,d)."""

    if not 0.0 < process_noise_scale < 1.0:
        raise ValueError("process_noise_scale must be in (0,1)")
    if observation_noise_scale <= 0.0:
        raise ValueError("observation_noise_scale must be positive")
    transition_scale = math.sqrt(1.0 - process_noise_scale**2)
    initial_mean = tf.fill([state_dim], tf.constant(mu, dtype=tf.float64))
    initial_covariance = tf.eye(state_dim, dtype=tf.float64)
    transition_matrix = transition_scale * tf.eye(state_dim, dtype=tf.float64)
    transition_offset = (1.0 - transition_scale) * initial_mean
    transition_covariance = (process_noise_scale**2) * tf.eye(state_dim, dtype=tf.float64)
    observation_matrix = _p30_observation_matrix(state_dim=state_dim, obs_dim=obs_dim)
    observation_covariance = (observation_noise_scale**2) * tf.eye(obs_dim, dtype=tf.float64)
    return highdim.LinearGaussianSSM(
        initial_mean=initial_mean,
        initial_covariance=initial_covariance,
        transition_matrix=transition_matrix,
        transition_covariance=transition_covariance,
        observation_matrix=observation_matrix,
        observation_covariance=observation_covariance,
        transition_offset=transition_offset,
    )


def _p30_observations(horizon: int, obs_dim: int = 3) -> tf.Tensor:
    """Small deterministic observation path for exact-reference tests."""

    rows = []
    for time_index in range(horizon):
        t = tf.constant(float(time_index + 1), dtype=tf.float64)
        rows.append(
            tf.stack(
                [
                    0.10 * tf.math.sin(t),
                    -0.05 + 0.03 * t,
                    0.07 * tf.math.cos(0.5 * t),
                ],
            )[:obs_dim]
        )
    return tf.stack(rows)


def _theta0() -> tf.Tensor:
    return tf.zeros([0], dtype=tf.float64)


def _independent_kalman(
    model: highdim.LinearGaussianSSM,
    observations: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    """Independent covariance-form Kalman reference for M1 tests."""

    y = tf.convert_to_tensor(observations, dtype=tf.float64)
    mean = model.initial_mean
    covariance = model.initial_covariance
    log_terms = []
    for time_index in range(int(y.shape[0])):
        if time_index > 0:
            mean = model.transition_offset + tf.linalg.matvec(model.transition_matrix, mean)
            covariance = _symmetrize(
                model.transition_matrix @ covariance @ tf.transpose(model.transition_matrix)
                + model.transition_covariance
            )
        predictive_mean = model.observation_offset + tf.linalg.matvec(
            model.observation_matrix,
            mean,
        )
        innovation = y[time_index] - predictive_mean
        innovation_covariance = _symmetrize(
            model.observation_matrix @ covariance @ tf.transpose(model.observation_matrix)
            + model.observation_covariance
        )
        log_terms.append(_mvn_log_prob_zero_mean(innovation, innovation_covariance))
        gain_rhs = covariance @ tf.transpose(model.observation_matrix)
        chol = tf.linalg.cholesky(innovation_covariance)
        kalman_gain = tf.transpose(tf.linalg.cholesky_solve(chol, tf.transpose(gain_rhs)))
        mean = mean + tf.linalg.matvec(kalman_gain, innovation)
        left = tf.eye(model.state_dim(), dtype=tf.float64) - kalman_gain @ model.observation_matrix
        covariance = _symmetrize(
            left @ covariance @ tf.transpose(left)
            + kalman_gain @ model.observation_covariance @ tf.transpose(kalman_gain)
        )
    return tf.reduce_sum(tf.stack(log_terms)), mean, covariance


def _mvn_log_prob_zero_mean(value: tf.Tensor, covariance: tf.Tensor) -> tf.Tensor:
    chol = tf.linalg.cholesky(covariance)
    solve = tf.linalg.cholesky_solve(chol, tf.reshape(value, [-1, 1]))[:, 0]
    dim = tf.cast(tf.shape(value)[0], tf.float64)
    log_det = 2.0 * tf.reduce_sum(tf.math.log(tf.linalg.diag_part(chol)))
    return -0.5 * (
        dim * tf.math.log(tf.constant(2.0 * math.pi, dtype=tf.float64))
        + log_det
        + tf.reduce_sum(value * solve)
    )


def _symmetrize(matrix: tf.Tensor) -> tf.Tensor:
    return 0.5 * (matrix + tf.linalg.matrix_transpose(matrix))


def _grid_posterior(log_values: tf.Tensor) -> tf.Tensor:
    shifted = log_values - tf.reduce_max(log_values)
    weights = tf.exp(shifted)
    return weights / tf.reduce_sum(weights)


def _hellinger(discrete_p: tf.Tensor, discrete_q: tf.Tensor) -> tf.Tensor:
    return tf.sqrt(0.5 * tf.reduce_sum(tf.square(tf.sqrt(discrete_p) - tf.sqrt(discrete_q))))


def _relative_l1(discrete_p: tf.Tensor, discrete_q: tf.Tensor) -> tf.Tensor:
    return tf.reduce_sum(tf.abs(discrete_p - discrete_q)) / tf.reduce_sum(tf.abs(discrete_q))


def test_p30_lgssm_clean_room_fixture_matches_independent_kalman_reference():
    model = _p30_lgssm_model(process_noise_scale=0.8, observation_noise_scale=0.5)
    observations = _p30_observations(horizon=4)

    result = highdim.FixedBranchSquaredTTFilter(_filter_config(state_dim=3)).log_likelihood(
        model,
        _theta0(),
        observations,
    )
    reference_log_likelihood, reference_mean, reference_covariance = _independent_kalman(
        model,
        observations,
    )

    tf.debugging.assert_near(result.log_likelihood, reference_log_likelihood, atol=2e-12)
    tf.debugging.assert_near(
        result.retained_filter.diagnostics["mean"],
        reference_mean,
        atol=2e-12,
    )
    tf.debugging.assert_near(
        result.retained_filter.diagnostics["covariance"],
        reference_covariance,
        atol=2e-12,
    )
    assert result.status is highdim.HighDimStatus.OK


def test_p30_lgssm_parameter_grid_posterior_matches_kalman_oracle():
    observations = _p30_observations(horizon=3)
    a_grid = (0.50, 0.65, 0.80)
    d_grid = (0.45, 0.60, 0.75)
    bf_log_values = []
    reference_log_values = []

    for process_noise_scale in a_grid:
        for observation_noise_scale in d_grid:
            model = _p30_lgssm_model(
                process_noise_scale=process_noise_scale,
                observation_noise_scale=observation_noise_scale,
            )
            result = highdim.FixedBranchSquaredTTFilter(
                _filter_config(state_dim=3, seed=f"p37-m1-{process_noise_scale}-{observation_noise_scale}")
            ).log_likelihood(model, _theta0(), observations)
            reference_log_likelihood, _, _ = _independent_kalman(model, observations)
            bf_log_values.append(result.log_likelihood)
            reference_log_values.append(reference_log_likelihood)

    bf_log = tf.stack(bf_log_values)
    reference_log = tf.stack(reference_log_values)
    bf_posterior = _grid_posterior(bf_log)
    reference_posterior = _grid_posterior(reference_log)

    tf.debugging.assert_near(bf_log, reference_log, atol=2e-12)
    tf.debugging.assert_near(_hellinger(bf_posterior, reference_posterior), 0.0, atol=2e-12)
    tf.debugging.assert_near(_relative_l1(bf_posterior, reference_posterior), 0.0, atol=2e-12)


def test_p30_lgssm_fixture_manifest_records_partial_grid_nonclaim():
    manifest = highdim.P30ModelSuiteFixtureManifest(
        version="p37.m1.lgssm.fixture.v1",
        model_id=highdim.P30ModelSuiteModelID.LGSSM_EXACT,
        source_equations=("eq:p27-lg1", "eq:p27-lg2", "eq:p27-lg3", "eq:p27-lg9"),
        paper_anchor="Zhao--Cui linear Gaussian benchmark, Section 6.1",
        matlab_anchor="eg1_kalman/main_script.m; models/kalman/setup.m",
        parameter_values={"a_grid": (0.50, 0.65, 0.80), "d_grid": (0.45, 0.60, 0.75)},
        prior={"a": "uniform grid diagnostic", "d": "uniform grid diagnostic"},
        state_dimension=3,
        parameter_dimension=2,
        horizon=3,
        basis={"family": "not_used_exact_kalman_value_path"},
        rank=(1, 1),
        sweeps=0,
        seed="p37-m1-clean-room-deterministic",
        dtype="tf.float64",
        reference_method="independent covariance-form Kalman oracle",
        expected_metrics=("log_evidence_error", "hellinger", "relative_l1"),
        vetoes=("exact_reference_mismatch", "nonfinite_posterior_grid"),
        non_claims=(
            "not the full Zhao--Cui T=50 reproduction grid",
            "no fixed-branch derivative claim",
            "no TT approximation accuracy claim",
        ),
        clean_room_status="P30 equations with audited MATLAB settings as behavioral anchors only",
        dimension_convention="state dimension m=3, observation dimension n=3, parameter grid over (a,d)",
    )

    assert manifest.model_id is highdim.P30ModelSuiteModelID.LGSSM_EXACT
    assert "not the full Zhao--Cui T=50 reproduction grid" in manifest.non_claims
