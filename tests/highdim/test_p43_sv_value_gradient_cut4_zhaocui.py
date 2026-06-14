from __future__ import annotations

import math

import pytest
import tensorflow as tf
import tensorflow_probability as tfp

import bayesfilter.highdim as highdim
from bayesfilter.nonlinear.svd_cut_tf import tf_svd_cut4_filter
from bayesfilter.structural import StatePartition, StructuralFilterConfig
from bayesfilter.structural_tf import TFStructuralStateSpace


_STD_NORMAL = tfp.distributions.Normal(
    loc=tf.constant(0.0, dtype=tf.float64),
    scale=tf.constant(1.0, dtype=tf.float64),
)


def _observations(dim: int) -> tf.Tensor:
    values = tf.constant(
        [
            [0.12, -0.08, 0.05],
            [-0.07, 0.11, -0.04],
        ],
        dtype=tf.float64,
    )
    return values[:, : int(dim)]


def _physical_parameters(dim: int) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    gamma = tf.constant([0.60, 0.52, 0.47], dtype=tf.float64)[: int(dim)]
    beta = tf.constant([0.40, 0.35, 0.45], dtype=tf.float64)[: int(dim)]
    sigma = tf.constant([1.00, 0.85, 0.75], dtype=tf.float64)[: int(dim)]
    return gamma, beta, sigma


def _theta_from_physical(gamma: tf.Tensor, beta: tf.Tensor) -> tf.Tensor:
    return tf.reshape(tf.stack([_STD_NORMAL.quantile(gamma), tf.math.log(beta)], axis=1), [-1])


def _physical_from_theta(theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
    theta_matrix = tf.reshape(tf.convert_to_tensor(theta, dtype=tf.float64), [-1, 2])
    return _STD_NORMAL.cdf(theta_matrix[:, 0]), tf.exp(theta_matrix[:, 1])


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _tt_config(seed: str = "p43-sv-gradient") -> highdim.FixedBranchFilterConfig:
    convention = _convention()
    product_basis = highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 48)],
        convention,
    )
    return highdim.FixedBranchFilterConfig(
        fit_config=highdim.FixedTTFitConfig(
            ranks=(1, 1),
            ridge=1e-12,
            max_sweeps=2,
            sweep_order=(0,),
            row_budget=512,
            column_budget=128,
            dense_matrix_byte_budget=200_000,
            normal_matrix_byte_budget=100_000,
            condition_number_warning=1e10,
            condition_number_veto=1e14,
            holdout_tolerance=5e-4,
        ),
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(
            highdim.AffineCoordinateMap(
                offset=tf.constant([0.0], dtype=tf.float64),
                matrix=tf.constant([[8.0]], dtype=tf.float64),
            ),
        ),
        measure_convention=convention,
        deterministic_seed=seed,
        product_basis=product_basis,
        initial_cores=(
            highdim.TTCore(tf.ones([1, product_basis.bases[0].basis_dim, 1], dtype=tf.float64)),
        ),
        fit_quadrature_order=141,
    )


def _ksc_kalman_value(theta: tf.Tensor, observations: tf.Tensor, sigma: tf.Tensor) -> tf.Tensor:
    gamma, beta = _physical_from_theta(theta)
    return highdim.independent_panel_sv_mixture_kalman_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
    ).log_likelihood


def _ksc_cut4_value(theta: tf.Tensor, observations: tf.Tensor, sigma: tf.Tensor) -> tf.Tensor:
    gamma, beta = _physical_from_theta(theta)
    return highdim.independent_panel_sv_mixture_cut4_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
    ).log_likelihood


def _exact_dense_value(theta: tf.Tensor, observations: tf.Tensor, sigma: tf.Tensor) -> tf.Tensor:
    gamma, beta = _physical_from_theta(theta)
    return highdim.exact_transformed_sv_independent_panel_dense_reference(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        order=401,
        radius=8.0,
    ).log_likelihood


def _exact_tt_value(
    theta: tf.Tensor,
    observations: tf.Tensor,
    sigma: tf.Tensor,
    *,
    seed: str,
) -> tf.Tensor:
    gamma, beta = _physical_from_theta(theta)
    return highdim.exact_transformed_sv_independent_panel_zhaocui_tt_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        config=_tt_config(seed),
        fixture_id=f"p43.exact-transformed-gradient.{seed}",
        branch_seed_prefix=f"p43-exact-transformed-gradient-{seed}",
    ).log_likelihood


def _value_and_score(value_fn, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
    theta = tf.convert_to_tensor(theta, dtype=tf.float64)
    with tf.GradientTape() as tape:
        tape.watch(theta)
        value = value_fn(theta)
    score = tape.gradient(value, theta)
    if score is None:
        raise AssertionError("GradientTape returned None")
    return value, score


def _relative_error(candidate: tf.Tensor, reference: tf.Tensor) -> tf.Tensor:
    return tf.linalg.norm(candidate - reference) / tf.maximum(
        tf.constant(1.0, dtype=tf.float64),
        tf.linalg.norm(reference),
    )


def _directions(size: int) -> tf.Tensor:
    eye = tf.eye(size, dtype=tf.float64)
    mixed_a = tf.cast(tf.range(1, size + 1), tf.float64)
    mixed_a = mixed_a / tf.linalg.norm(mixed_a)
    mixed_b = tf.where(
        tf.math.floormod(tf.range(size), 2) == 0,
        tf.ones([size], dtype=tf.float64),
        -tf.ones([size], dtype=tf.float64),
    )
    mixed_b = mixed_b / tf.linalg.norm(mixed_b)
    mixed_c = tf.reverse(mixed_a, axis=[0])
    directions = tf.concat(
        [eye, mixed_a[tf.newaxis, :], mixed_b[tf.newaxis, :], mixed_c[tf.newaxis, :]],
        axis=0,
    )
    if int(directions.shape[0]) < 5:
        extra = tf.ones([1, size], dtype=tf.float64) / tf.sqrt(tf.cast(size, tf.float64))
        directions = tf.concat([directions, extra], axis=0)
    return directions


def _assert_directional_residuals(
    candidate_score: tf.Tensor,
    reference_score: tf.Tensor,
    *,
    atol: float,
) -> None:
    diff = candidate_score - reference_score
    directional = tf.linalg.matvec(_directions(int(diff.shape[0])), diff)
    tf.debugging.assert_near(directional, tf.zeros_like(directional), atol=atol, rtol=atol)
    assert int(directional.shape[0]) >= 5


@pytest.mark.parametrize("dim", [1, 2, 3])
def test_p43_ksc_cut4_matches_kalman_value_and_diagnostic_score(dim: int) -> None:
    observations = _observations(dim)
    gamma, beta, sigma = _physical_parameters(dim)
    theta = _theta_from_physical(gamma, beta)

    kalman_value, kalman_score = _value_and_score(
        lambda current_theta: _ksc_kalman_value(current_theta, observations, sigma),
        theta,
    )
    cut4_value, cut4_score = _value_and_score(
        lambda current_theta: _ksc_cut4_value(current_theta, observations, sigma),
        theta,
    )

    tf.debugging.assert_near(cut4_value, kalman_value, atol=2e-6, rtol=2e-6)
    tf.debugging.assert_near(cut4_score, kalman_score, atol=2e-8, rtol=2e-8)
    tf.debugging.assert_less(_relative_error(cut4_score, kalman_score), tf.constant(1e-8, dtype=tf.float64))
    _assert_directional_residuals(cut4_score, kalman_score, atol=2e-8)


@pytest.mark.parametrize("dim", [1, 2, 3])
def test_p43_exact_transformed_zhaocui_matches_dense_value_and_diagnostic_score(dim: int) -> None:
    observations = _observations(dim)
    gamma, beta, sigma = _physical_parameters(dim)
    theta = _theta_from_physical(gamma, beta)

    dense_value, dense_score = _value_and_score(
        lambda current_theta: _exact_dense_value(current_theta, observations, sigma),
        theta,
    )
    tt_value, tt_score = _value_and_score(
        lambda current_theta: _exact_tt_value(
            current_theta,
            observations,
            sigma,
            seed=f"dim-{dim}",
        ),
        theta,
    )

    tf.debugging.assert_near(tt_value, dense_value, atol=2e-6, rtol=2e-6)
    tf.debugging.assert_near(tt_score, dense_score, atol=2e-5, rtol=2e-5)
    tf.debugging.assert_less(_relative_error(tt_score, dense_score), tf.constant(1e-5, dtype=tf.float64))
    _assert_directional_residuals(tt_score, dense_score, atol=2e-5)


@pytest.mark.parametrize("dim", [1, 2, 3])
def test_p43_ksc_mixture_gradient_gap_to_exact_transformed_is_approximation_only(dim: int) -> None:
    observations = _observations(dim)
    gamma, beta, sigma = _physical_parameters(dim)
    theta = _theta_from_physical(gamma, beta)

    ksc_value, ksc_score = _value_and_score(
        lambda current_theta: _ksc_kalman_value(current_theta, observations, sigma),
        theta,
    )
    exact_value, exact_score = _value_and_score(
        lambda current_theta: _exact_dense_value(current_theta, observations, sigma),
        theta,
    )
    value_gap = ksc_value - exact_value
    score_gap = ksc_score - exact_score

    assert bool(tf.math.is_finite(value_gap).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(score_gap)).numpy())
    assert abs(float(value_gap.numpy())) > 0.0
    assert float(tf.linalg.norm(score_gap).numpy()) > 0.0


def _generalized_sv_diagnostic_model(
    *,
    observation: tf.Tensor,
    beta: tf.Tensor,
) -> TFStructuralStateSpace:
    gamma_s = tf.constant(0.55, dtype=tf.float64)
    gamma_h = tf.constant(0.65, dtype=tf.float64)
    sigma_s = tf.constant(0.30, dtype=tf.float64)
    sigma_h = tf.constant(0.45, dtype=tf.float64)
    initial_covariance = tf.linalg.diag(
        tf.stack(
            [
                tf.square(sigma_s) / (1.0 - tf.square(gamma_s)),
                tf.square(sigma_h) / (1.0 - tf.square(gamma_h)),
            ]
        )
    )
    observed_scalar = tf.reshape(tf.convert_to_tensor(observation, dtype=tf.float64), [])

    def transition_fn(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        del innovation
        return tf.convert_to_tensor(previous_state, dtype=tf.float64)

    def observation_fn(state_points: tf.Tensor) -> tf.Tensor:
        points = tf.convert_to_tensor(state_points, dtype=tf.float64)
        if points.shape.rank == 1:
            points = points[tf.newaxis, :]
        residual = observed_scalar - beta * points[:, 0]
        transformed_residual = tf.math.log(tf.square(residual) + tf.constant(1e-8, dtype=tf.float64)) - points[:, 1]
        return transformed_residual[:, tf.newaxis]

    return TFStructuralStateSpace(
        partition=StatePartition(
            state_names=("s", "h"),
            stochastic_indices=(0, 1),
            deterministic_indices=(),
            innovation_dim=2,
        ),
        config=StructuralFilterConfig(
            integration_space="innovation",
            deterministic_completion="none",
            approximation_label="p43_generalized_sv_cut4_gradient_diagnostic_not_exact",
        ),
        initial_mean=tf.zeros([2], dtype=tf.float64),
        initial_covariance=initial_covariance,
        innovation_covariance=tf.eye(2, dtype=tf.float64),
        observation_covariance=tf.reshape(tf.constant(1.0, dtype=tf.float64), [1, 1]),
        transition_fn=transition_fn,
        observation_fn=observation_fn,
        name="p43_generalized_sv_cut4_gradient_diagnostic_not_exact",
    )


def test_p43_generalized_sv_cut4_diagnostic_value_and_gradient_are_finite_with_nonclaim() -> None:
    theta = tf.constant(math.log(0.35), dtype=tf.float64)

    with tf.GradientTape() as tape:
        tape.watch(theta)
        beta = tf.exp(theta)
        model = _generalized_sv_diagnostic_model(
            observation=tf.constant(0.18, dtype=tf.float64),
            beta=beta,
        )
        result = tf_svd_cut4_filter(
            tf.constant([[0.0]], dtype=tf.float64),
            model,
            return_filtered=True,
        )
        value = result.log_likelihood
    score = tape.gradient(value, theta)

    assert bool(tf.math.is_finite(value).numpy())
    assert score is not None
    assert bool(tf.math.is_finite(score).numpy())
    assert result.metadata.approximation_label == "p43_generalized_sv_cut4_gradient_diagnostic_not_exact"
    assert int(result.diagnostics.extra["augmented_dim"].numpy()) == 4
