from __future__ import annotations

from dataclasses import dataclass
import math

import tensorflow as tf
import tensorflow_probability as tfp

import bayesfilter.highdim as highdim
from bayesfilter.nonlinear.svd_cut_tf import tf_svd_cut4_filter
from bayesfilter.structural import StatePartition, StructuralFilterConfig
from bayesfilter.structural_tf import TFStructuralStateSpace


DTYPE = tf.float64


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _observations(dim: int) -> tf.Tensor:
    values = tf.constant(
        [
            [0.16, 0.11, 0.20],
            [0.09, 0.18, 0.13],
        ],
        dtype=DTYPE,
    )
    return values[:, : int(dim)]


def _theta0() -> tf.Tensor:
    return tf.constant([0.18, math.log(0.13), math.log(0.09), 0.02], dtype=DTYPE)


def _physical_parts(theta: tf.Tensor, dim: int) -> dict[str, tf.Tensor]:
    theta = tf.convert_to_tensor(theta, dtype=DTYPE)
    rho_scale = tf.constant([1.00, 0.88, 0.76], dtype=DTYPE)[:dim]
    q_scale = tf.constant([0.90, 1.12, 1.30], dtype=DTYPE)[:dim]
    r_scale = tf.constant([1.00, 1.18, 0.90], dtype=DTYPE)[:dim]
    mean_scale = tf.constant([1.00, -0.50, 0.25], dtype=DTYPE)[:dim]
    raw_initial_variance = tf.constant([0.50, 0.68, 0.82], dtype=DTYPE)[:dim]
    rho = 0.40 * tf.tanh(theta[0]) * rho_scale
    transition_variance = tf.exp(theta[1]) * q_scale
    observation_variance = tf.exp(theta[2]) * r_scale
    raw_initial_mean = theta[3] * mean_scale
    initial_mean = rho * raw_initial_mean
    initial_variance = tf.square(rho) * raw_initial_variance + transition_variance
    return {
        "rho": rho,
        "transition_variance": transition_variance,
        "observation_variance": observation_variance,
        "raw_initial_mean": raw_initial_mean,
        "raw_initial_variance": raw_initial_variance,
        "initial_mean": initial_mean,
        "initial_variance": initial_variance,
    }


def _axis_part(theta: tf.Tensor, axis: int) -> dict[str, tf.Tensor]:
    parts = _physical_parts(theta, axis + 1)
    return {key: value[axis] for key, value in parts.items()}


def _rows(values: tf.Tensor, width: int, name: str) -> tf.Tensor:
    tensor = tf.convert_to_tensor(values, dtype=DTYPE)
    if tensor.shape.rank == 1:
        tensor = tensor[tf.newaxis, :]
    if tensor.shape.rank != 2 or tensor.shape[1] != int(width):
        raise ValueError(f"{name} has wrong shape")
    return tensor


@dataclass(frozen=True)
class _ScalarQuadraticObservationSSM:
    axis: int

    def parameter_dim(self) -> int:
        return 4

    def state_dim(self) -> int:
        return 1

    def observation_dim(self) -> int:
        return 1

    def initial_log_density(self, theta: tf.Tensor, x0: tf.Tensor) -> tf.Tensor:
        points = _rows(x0, 1, "x0")[:, 0]
        parts = _axis_part(theta, self.axis)
        return tfp.distributions.Normal(
            loc=parts["initial_mean"],
            scale=tf.sqrt(parts["initial_variance"]),
        ).log_prob(points)

    def transition_log_density(
        self,
        theta: tf.Tensor,
        x_prev: tf.Tensor,
        x_next: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del t
        previous = _rows(x_prev, 1, "x_prev")[:, 0]
        current = _rows(x_next, 1, "x_next")[:, 0]
        parts = _axis_part(theta, self.axis)
        return tfp.distributions.Normal(
            loc=parts["rho"] * previous,
            scale=tf.sqrt(parts["transition_variance"]),
        ).log_prob(current)

    def observation_log_density(
        self,
        theta: tf.Tensor,
        x_t: tf.Tensor,
        y_t: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del t
        points = _rows(x_t, 1, "x_t")[:, 0]
        observation = tf.reshape(tf.convert_to_tensor(y_t, dtype=DTYPE), [1])[0]
        parts = _axis_part(theta, self.axis)
        return tfp.distributions.Normal(
            loc=tf.square(points),
            scale=tf.sqrt(parts["observation_variance"]),
        ).log_prob(observation)

    def manifest_payload(self) -> dict[str, object]:
        return {
            "family": "p44_m3_scalar_quadratic_observation",
            "axis": int(self.axis),
            "parameterization": "(rho_raw, log_q, log_r, raw_initial_mean)",
        }


def _structural_model(theta: tf.Tensor, dim: int) -> TFStructuralStateSpace:
    parts = _physical_parts(theta, dim)
    padding_dim = max(0, 3 - (2 * dim))
    innovation_dim = dim + padding_dim

    def transition_fn(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        previous = _rows(previous_state, dim, "previous_state")
        innovation_points = _rows(innovation, innovation_dim, "innovation")[:, :dim]
        next_points = (
            parts["rho"][tf.newaxis, :] * previous
            + tf.sqrt(parts["transition_variance"])[tf.newaxis, :] * innovation_points
        )
        return next_points[0] if tf.convert_to_tensor(previous_state).shape.rank == 1 else next_points

    def observation_fn(state_points: tf.Tensor) -> tf.Tensor:
        points = _rows(state_points, dim, "state_points")
        observations = tf.square(points)
        return observations[0] if tf.convert_to_tensor(state_points).shape.rank == 1 else observations

    return TFStructuralStateSpace(
        partition=StatePartition(
            state_names=tuple(f"x{axis}" for axis in range(dim)),
            stochastic_indices=tuple(range(dim)),
            deterministic_indices=(),
            innovation_dim=innovation_dim,
        ),
        config=StructuralFilterConfig(
            integration_space="innovation",
            deterministic_completion="none",
            approximation_label="p44_m3_quadratic_observation_cut4_same_target_approximation",
        ),
        initial_mean=parts["raw_initial_mean"],
        initial_covariance=tf.linalg.diag(parts["raw_initial_variance"]),
        innovation_covariance=tf.eye(innovation_dim, dtype=DTYPE),
        observation_covariance=tf.linalg.diag(parts["observation_variance"]),
        transition_fn=transition_fn,
        observation_fn=observation_fn,
        name=f"p44_m3_quadratic_observation_dim_{dim}",
    )


def _dense_config(axis: int, order: int) -> highdim.FixedBranchFilterConfig:
    return highdim.FixedBranchFilterConfig(
        fit_config=None,
        density_tau=0.0,
        normalizer_floor=1e-14,
        denominator_floor=1e-14,
        retained_storage_byte_budget=20_000_000,
        coordinate_maps=(
            highdim.AffineCoordinateMap(
                offset=tf.constant([0.0], dtype=DTYPE),
                matrix=tf.constant([[6.0]], dtype=DTYPE),
            ),
        ),
        measure_convention=_convention(),
        deterministic_seed=f"p44-m3-dense-axis-{axis}-order-{order}",
        fit_quadrature_order=int(order),
    )


def _tt_config(axis: int) -> highdim.FixedBranchFilterConfig:
    convention = _convention()
    product_basis = highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 56)],
        convention,
    )
    return highdim.FixedBranchFilterConfig(
        fit_config=highdim.FixedTTFitConfig(
            ranks=(1, 1),
            ridge=1e-12,
            max_sweeps=2,
            sweep_order=(0,),
            row_budget=512,
            column_budget=160,
            dense_matrix_byte_budget=500_000,
            normal_matrix_byte_budget=250_000,
            condition_number_warning=1e10,
            condition_number_veto=1e14,
            holdout_tolerance=1e-3,
        ),
        density_tau=0.0,
        normalizer_floor=1e-14,
        denominator_floor=1e-14,
        retained_storage_byte_budget=20_000_000,
        coordinate_maps=(
            highdim.AffineCoordinateMap(
                offset=tf.constant([0.0], dtype=DTYPE),
                matrix=tf.constant([[6.0]], dtype=DTYPE),
            ),
        ),
        measure_convention=convention,
        deterministic_seed=f"p44-m3-tt-axis-{axis}",
        product_basis=product_basis,
        initial_cores=(
            highdim.TTCore(tf.ones([1, product_basis.bases[0].basis_dim, 1], dtype=DTYPE)),
        ),
        fit_quadrature_order=181,
    )


def _dense_scalar_value(theta: tf.Tensor, axis: int, order: int) -> tf.Tensor:
    return highdim.FixedBranchSquaredTTFilter(_dense_config(axis, order)).log_likelihood(
        _ScalarQuadraticObservationSSM(axis),
        theta,
        _observations(axis + 1)[:, axis : axis + 1],
    ).log_likelihood


def _dense_panel_value(theta: tf.Tensor, dim: int, order: int = 281) -> tf.Tensor:
    return tf.reduce_sum(tf.stack([_dense_scalar_value(theta, axis, order) for axis in range(dim)]))


def _cut4_panel_value(theta: tf.Tensor, dim: int) -> tf.Tensor:
    return tf_svd_cut4_filter(
        _observations(dim),
        _structural_model(theta, dim),
        innovation_floor=tf.constant(1e-12, dtype=DTYPE),
        return_filtered=True,
    ).log_likelihood


def _tt_panel_value(theta: tf.Tensor, dim: int) -> tf.Tensor:
    terms = []
    for axis in range(dim):
        result = highdim.scalar_nonlinear_fixed_design_tt_value_path(
            _ScalarQuadraticObservationSSM(axis),
            theta,
            _observations(axis + 1)[:, axis : axis + 1],
            _tt_config(axis),
            fixture_id=f"p44.m3.quadratic-observation.axis-{axis}.v1",
            branch_seed_prefix=f"p44-m3-quadratic-observation-axis-{axis}",
            retained_moment_order=281,
            retained_propagation_order=281,
        )
        terms.append(result.log_likelihood)
    return tf.reduce_sum(tf.stack(terms))


def _value_and_score(value_fn, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
    theta = tf.convert_to_tensor(theta, dtype=DTYPE)
    with tf.GradientTape() as tape:
        tape.watch(theta)
        value = value_fn(theta)
    score = tape.gradient(value, theta)
    if score is None:
        raise AssertionError("GradientTape returned None")
    return value, score


def _directions(size: int) -> tf.Tensor:
    eye = tf.eye(size, dtype=DTYPE)
    mixed_a = tf.cast(tf.range(1, size + 1), DTYPE)
    mixed_a = mixed_a / tf.linalg.norm(mixed_a)
    mixed_b = tf.where(
        tf.math.floormod(tf.range(size), 2) == 0,
        tf.ones([size], dtype=DTYPE),
        -tf.ones([size], dtype=DTYPE),
    )
    mixed_b = mixed_b / tf.linalg.norm(mixed_b)
    mixed_c = tf.reverse(mixed_a, axis=[0])
    directions = tf.concat(
        [eye, mixed_a[tf.newaxis, :], mixed_b[tf.newaxis, :], mixed_c[tf.newaxis, :]],
        axis=0,
    )
    assert int(directions.shape[0]) >= 5
    return directions


def _directional_abs_max(candidate_score: tf.Tensor, reference_score: tf.Tensor) -> tf.Tensor:
    residual = candidate_score - reference_score
    directional = tf.linalg.matvec(_directions(int(residual.shape[0])), residual)
    return tf.reduce_max(tf.abs(directional))


def _relative_score_error(candidate_score: tf.Tensor, reference_score: tf.Tensor) -> tf.Tensor:
    return tf.linalg.norm(candidate_score - reference_score) / tf.maximum(
        tf.constant(1.0, dtype=DTYPE),
        tf.linalg.norm(reference_score),
    )


def _first_observation_mode_masses(theta: tf.Tensor, axis: int, order: int = 401) -> tuple[tf.Tensor, tf.Tensor]:
    nodes, weights = highdim.legendre_gauss_nodes_weights(order)
    x = 6.0 * nodes
    scaled_weights = 6.0 * weights
    parts = _axis_part(theta, axis)
    y0 = _observations(axis + 1)[0, axis]
    prior = tfp.distributions.Normal(
        loc=parts["initial_mean"],
        scale=tf.sqrt(parts["initial_variance"]),
    )
    likelihood = tfp.distributions.Normal(
        loc=tf.square(x),
        scale=tf.sqrt(parts["observation_variance"]),
    )
    mass = scaled_weights * tf.exp(prior.log_prob(x) + likelihood.log_prob(y0))
    total = tf.reduce_sum(mass)
    negative = tf.reduce_sum(tf.boolean_mask(mass, x < -0.05)) / total
    positive = tf.reduce_sum(tf.boolean_mask(mass, x > 0.05)) / total
    return negative, positive


def test_p44_m3_structural_timing_matches_dense_initial_predictive_moments_dims_1_2_3() -> None:
    theta = _theta0()
    for dim in (1, 2, 3):
        parts = _physical_parts(theta, dim)
        structural = _structural_model(theta, dim)
        structural_mean = parts["rho"] * structural.initial_mean
        structural_variance = tf.square(parts["rho"]) * tf.linalg.diag_part(
            structural.initial_covariance
        ) + parts["transition_variance"]
        tf.debugging.assert_near(structural_mean, parts["initial_mean"], atol=0.0)
        tf.debugging.assert_near(structural_variance, parts["initial_variance"], atol=2e-15)


def test_p44_m3_dense_reference_covers_symmetric_modes_before_comparison() -> None:
    theta = _theta0()
    for axis in (0, 1, 2):
        negative, positive = _first_observation_mode_masses(theta, axis)
        print(
            "P44_M3_SYMMETRIC_MODE_COVERAGE "
            f"axis={axis} negative_mass={float(negative.numpy()):.6e} "
            f"positive_mass={float(positive.numpy()):.6e}"
        )
        tf.debugging.assert_greater(negative, tf.constant(0.25, dtype=DTYPE))
        tf.debugging.assert_greater(positive, tf.constant(0.25, dtype=DTYPE))


def test_p44_m3_dense_reference_refines_value_and_score_dims_1_2_3() -> None:
    theta = _theta0()
    for dim in (1, 2, 3):
        low_value, low_score = _value_and_score(
            lambda current_theta: _dense_panel_value(current_theta, dim, order=181),
            theta,
        )
        high_value, high_score = _value_and_score(
            lambda current_theta: _dense_panel_value(current_theta, dim, order=281),
            theta,
        )
        value_gap = tf.abs(low_value - high_value)
        score_gap = _directional_abs_max(low_score, high_score)
        print(
            "P44_M3_DENSE_REFINEMENT "
            f"dim={dim} value_gap={float(value_gap.numpy()):.6e} "
            f"directional_score_gap={float(score_gap.numpy()):.6e}"
        )
        tf.debugging.assert_less(value_gap, tf.constant(1e-10, dtype=DTYPE))
        tf.debugging.assert_less(score_gap, tf.constant(1e-9, dtype=DTYPE))


def test_p44_m3_cut4_records_stress_gap_and_zhaocui_matches_dense_dims_1_2_3() -> None:
    theta = _theta0()
    for dim in (1, 2, 3):
        dense_value, dense_score = _value_and_score(
            lambda current_theta: _dense_panel_value(current_theta, dim, order=281),
            theta,
        )
        cut4_value, cut4_score = _value_and_score(
            lambda current_theta: _cut4_panel_value(current_theta, dim),
            theta,
        )
        tt_value, tt_score = _value_and_score(
            lambda current_theta: _tt_panel_value(current_theta, dim),
            theta,
        )

        cut4_value_gap = tf.abs(cut4_value - dense_value)
        cut4_score_gap = _directional_abs_max(cut4_score, dense_score)
        cut4_score_rel = _relative_score_error(cut4_score, dense_score)
        tt_value_gap = tf.abs(tt_value - dense_value)
        tt_score_gap = _directional_abs_max(tt_score, dense_score)
        tt_score_rel = _relative_score_error(tt_score, dense_score)
        print(
            "P44_M3_APPROXIMATION_GAP "
            f"dim={dim} "
            f"cut4_value_gap={float(cut4_value_gap.numpy()):.6e} "
            f"cut4_directional_score_gap={float(cut4_score_gap.numpy()):.6e} "
            f"cut4_score_rel={float(cut4_score_rel.numpy()):.6e} "
            f"zhaocui_value_gap={float(tt_value_gap.numpy()):.6e} "
            f"zhaocui_directional_score_gap={float(tt_score_gap.numpy()):.6e} "
            f"zhaocui_score_rel={float(tt_score_rel.numpy()):.6e}"
        )
        assert bool(tf.math.is_finite(cut4_value).numpy())
        assert bool(tf.reduce_all(tf.math.is_finite(cut4_score)).numpy())
        assert bool(tf.math.is_finite(tt_value).numpy())
        assert bool(tf.reduce_all(tf.math.is_finite(tt_score)).numpy())
        tf.debugging.assert_greater(cut4_value_gap, tf.constant(5e-2 * dim, dtype=DTYPE))
        tf.debugging.assert_less(cut4_value_gap, tf.constant(1.3e-1 * dim, dtype=DTYPE))
        tf.debugging.assert_less(cut4_score_gap, tf.constant(4.0e-1 * dim, dtype=DTYPE))
        tf.debugging.assert_less(cut4_score_rel, tf.constant(5.0e-1, dtype=DTYPE))
        tf.debugging.assert_less(tt_value_gap, tf.constant(8e-3 * dim, dtype=DTYPE))
        tf.debugging.assert_less(tt_score_gap, tf.constant(4e-2 * dim, dtype=DTYPE))
        tf.debugging.assert_less(tt_score_rel, tf.constant(2e-2, dtype=DTYPE))


def test_p44_m3_cut4_metadata_keeps_quadratic_stress_boundary() -> None:
    result = tf_svd_cut4_filter(
        _observations(3),
        _structural_model(_theta0(), 3),
        innovation_floor=tf.constant(1e-12, dtype=DTYPE),
        return_filtered=True,
    )
    assert result.metadata.approximation_label == "p44_m3_quadratic_observation_cut4_same_target_approximation"
    assert int(result.diagnostics.extra["augmented_dim"].numpy()) == 6
    assert int(result.diagnostics.extra["point_count"].numpy()) <= 76
    assert int(result.diagnostics.extra["polynomial_degree"].numpy()) == 5
    assert int(result.diagnostics.extra["innovation_floor_count"].numpy()) == 0
