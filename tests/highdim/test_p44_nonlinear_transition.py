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


def _observations(dim: int, horizon: int) -> tf.Tensor:
    values = tf.constant(
        [
            [0.08, -0.03, 0.06],
            [-0.02, 0.05, -0.04],
            [0.04, -0.01, 0.03],
            [0.01, 0.02, -0.02],
        ],
        dtype=DTYPE,
    )
    return values[: int(horizon), : int(dim)]


def _theta0() -> tf.Tensor:
    return tf.constant([0.22, math.log(0.12), math.log(0.09), 0.03, 0.40], dtype=DTYPE)


def _linear_theta0() -> tf.Tensor:
    return tf.tensor_scatter_nd_update(_theta0(), indices=[[4]], updates=tf.constant([0.0], dtype=DTYPE))


def _physical_parts(theta: tf.Tensor, dim: int) -> dict[str, tf.Tensor]:
    theta = tf.convert_to_tensor(theta, dtype=DTYPE)
    rho_scale = tf.constant([1.00, 0.88, 0.76], dtype=DTYPE)[:dim]
    q_scale = tf.constant([0.90, 1.12, 1.30], dtype=DTYPE)[:dim]
    r_scale = tf.constant([1.00, 1.18, 0.90], dtype=DTYPE)[:dim]
    mean_scale = tf.constant([1.00, -0.50, 0.25], dtype=DTYPE)[:dim]
    nonlin_scale = tf.constant([1.00, 0.75, 1.15], dtype=DTYPE)[:dim]
    raw_initial_variance = tf.constant([0.50, 0.68, 0.82], dtype=DTYPE)[:dim]
    rho = 0.42 * tf.tanh(theta[0]) * rho_scale
    transition_variance = tf.exp(theta[1]) * q_scale
    observation_variance = tf.exp(theta[2]) * r_scale
    raw_initial_mean = theta[3] * mean_scale
    nonlin = 0.05 * tf.tanh(theta[4]) * nonlin_scale
    initial_mean_linear = rho * raw_initial_mean
    initial_variance_linear = tf.square(rho) * raw_initial_variance + transition_variance
    return {
        "rho": rho,
        "transition_variance": transition_variance,
        "observation_variance": observation_variance,
        "raw_initial_mean": raw_initial_mean,
        "raw_initial_variance": raw_initial_variance,
        "nonlin": nonlin,
        "initial_mean_linear": initial_mean_linear,
        "initial_variance_linear": initial_variance_linear,
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


def _transition_mean_scalar(raw_or_previous: tf.Tensor, parts: dict[str, tf.Tensor]) -> tf.Tensor:
    values = tf.convert_to_tensor(raw_or_previous, dtype=DTYPE)
    return parts["rho"] * values + parts["nonlin"] * tf.math.tanh(values)


@dataclass(frozen=True)
class _ScalarNonlinearTransitionSSM:
    axis: int
    initial_quadrature_order: int

    def parameter_dim(self) -> int:
        return 5

    def state_dim(self) -> int:
        return 1

    def observation_dim(self) -> int:
        return 1

    def initial_log_density(self, theta: tf.Tensor, x0: tf.Tensor) -> tf.Tensor:
        points = _rows(x0, 1, "x0")[:, 0]
        parts = _axis_part(theta, self.axis)
        nodes, weights = highdim.legendre_gauss_nodes_weights(int(self.initial_quadrature_order))
        raw = 6.0 * nodes
        scaled_weights = 6.0 * weights
        raw_prior = tfp.distributions.Normal(
            loc=parts["raw_initial_mean"],
            scale=tf.sqrt(parts["raw_initial_variance"]),
        )
        transition = tfp.distributions.Normal(
            loc=_transition_mean_scalar(raw, parts),
            scale=tf.sqrt(parts["transition_variance"]),
        )
        log_terms = (
            tf.math.log(scaled_weights)[tf.newaxis, :]
            + raw_prior.log_prob(raw)[tf.newaxis, :]
            + transition.log_prob(points[:, tf.newaxis])
        )
        return tf.reduce_logsumexp(log_terms, axis=1)

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
            loc=_transition_mean_scalar(previous, parts),
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
            loc=points,
            scale=tf.sqrt(parts["observation_variance"]),
        ).log_prob(observation)

    def manifest_payload(self) -> dict[str, object]:
        return {
            "family": "p44_m4_scalar_nonlinear_transition",
            "axis": int(self.axis),
            "parameterization": "(rho_raw, log_q, log_r, raw_initial_mean, nonlin_raw)",
            "transition": "rho*x + c*tanh(x)",
            "initial_density": "quadrature over raw pre-transition Gaussian state",
        }


def _linear_gaussian_model(theta: tf.Tensor, dim: int) -> highdim.LinearGaussianSSM:
    parts = _physical_parts(theta, dim)
    return highdim.LinearGaussianSSM(
        initial_mean=parts["initial_mean_linear"],
        initial_covariance=tf.linalg.diag(parts["initial_variance_linear"]),
        transition_matrix=tf.linalg.diag(parts["rho"]),
        transition_covariance=tf.linalg.diag(parts["transition_variance"]),
        observation_matrix=tf.eye(dim, dtype=DTYPE),
        observation_covariance=tf.linalg.diag(parts["observation_variance"]),
    )


def _structural_model(theta: tf.Tensor, dim: int) -> TFStructuralStateSpace:
    parts = _physical_parts(theta, dim)
    padding_dim = max(0, 3 - (2 * dim))
    innovation_dim = dim + padding_dim

    def transition_fn(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        previous = _rows(previous_state, dim, "previous_state")
        innovation_points = _rows(innovation, innovation_dim, "innovation")[:, :dim]
        next_points = (
            parts["rho"][tf.newaxis, :] * previous
            + parts["nonlin"][tf.newaxis, :] * tf.math.tanh(previous)
            + tf.sqrt(parts["transition_variance"])[tf.newaxis, :] * innovation_points
        )
        return next_points[0] if tf.convert_to_tensor(previous_state).shape.rank == 1 else next_points

    def observation_fn(state_points: tf.Tensor) -> tf.Tensor:
        points = _rows(state_points, dim, "state_points")
        return points[0] if tf.convert_to_tensor(state_points).shape.rank == 1 else points

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
            approximation_label="p44_m4_nonlinear_transition_cut4_same_target_approximation",
        ),
        initial_mean=parts["raw_initial_mean"],
        initial_covariance=tf.linalg.diag(parts["raw_initial_variance"]),
        innovation_covariance=tf.eye(innovation_dim, dtype=DTYPE),
        observation_covariance=tf.linalg.diag(parts["observation_variance"]),
        transition_fn=transition_fn,
        observation_fn=observation_fn,
        name=f"p44_m4_nonlinear_transition_dim_{dim}",
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
        deterministic_seed=f"p44-m4-dense-axis-{axis}-order-{order}",
        fit_quadrature_order=int(order),
    )


def _tt_config(axis: int) -> highdim.FixedBranchFilterConfig:
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
        deterministic_seed=f"p44-m4-tt-axis-{axis}",
        product_basis=product_basis,
        initial_cores=(
            highdim.TTCore(tf.ones([1, product_basis.bases[0].basis_dim, 1], dtype=DTYPE)),
        ),
        fit_quadrature_order=181,
    )


def _dense_scalar_value(theta: tf.Tensor, axis: int, horizon: int, order: int) -> tf.Tensor:
    return highdim.FixedBranchSquaredTTFilter(_dense_config(axis, order)).log_likelihood(
        _ScalarNonlinearTransitionSSM(axis, initial_quadrature_order=order),
        theta,
        _observations(axis + 1, horizon)[:, axis : axis + 1],
    ).log_likelihood


def _dense_panel_value(theta: tf.Tensor, dim: int, horizon: int, order: int = 241) -> tf.Tensor:
    return tf.reduce_sum(tf.stack([_dense_scalar_value(theta, axis, horizon, order) for axis in range(dim)]))


def _kalman_linear_value(theta: tf.Tensor, dim: int, horizon: int) -> tf.Tensor:
    return highdim.FixedBranchSquaredTTFilter(_kalman_config(dim)).log_likelihood(
        _linear_gaussian_model(theta, dim),
        tf.zeros([0], dtype=DTYPE),
        _observations(dim, horizon),
    ).log_likelihood


def _kalman_config(dim: int) -> highdim.FixedBranchFilterConfig:
    return highdim.FixedBranchFilterConfig(
        fit_config=None,
        density_tau=0.0,
        normalizer_floor=1e-14,
        denominator_floor=1e-14,
        retained_storage_byte_budget=20_000_000,
        coordinate_maps=(highdim.IdentityCoordinateMap(dim),),
        measure_convention=_convention(),
        deterministic_seed=f"p44-m4-linear-kalman-dim-{dim}",
    )


def _cut4_panel_value(theta: tf.Tensor, dim: int, horizon: int) -> tf.Tensor:
    return tf_svd_cut4_filter(
        _observations(dim, horizon),
        _structural_model(theta, dim),
        innovation_floor=tf.constant(1e-12, dtype=DTYPE),
        return_filtered=True,
    ).log_likelihood


def _tt_panel_value(theta: tf.Tensor, dim: int) -> tf.Tensor:
    terms = []
    for axis in range(dim):
        result = highdim.scalar_nonlinear_fixed_design_tt_value_path(
            _ScalarNonlinearTransitionSSM(axis, initial_quadrature_order=181),
            theta,
            _observations(axis + 1, 2)[:, axis : axis + 1],
            _tt_config(axis),
            fixture_id=f"p44.m4.nonlinear-transition.axis-{axis}.v1",
            branch_seed_prefix=f"p44-m4-nonlinear-transition-axis-{axis}",
            retained_moment_order=241,
            retained_propagation_order=241,
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


def test_p44_m4_nested_linear_dense_and_cut4_match_exact_kalman_dims_1_2_3_horizons_2_4() -> None:
    theta = _linear_theta0()
    for horizon in (2, 4):
        for dim in (1, 2, 3):
            kalman_value, kalman_score = _value_and_score(
                lambda current_theta: _kalman_linear_value(current_theta, dim, horizon),
                theta,
            )
            dense_value, dense_score = _value_and_score(
                lambda current_theta: _dense_panel_value(current_theta, dim, horizon, order=241),
                theta,
            )
            cut4_value, cut4_score = _value_and_score(
                lambda current_theta: _cut4_panel_value(current_theta, dim, horizon),
                theta,
            )
            tf.debugging.assert_near(dense_value, kalman_value, atol=2e-8, rtol=2e-8)
            tf.debugging.assert_near(cut4_value, kalman_value, atol=3e-11, rtol=3e-11)
            tf.debugging.assert_near(dense_score[:4], kalman_score[:4], atol=2e-7, rtol=2e-7)
            tf.debugging.assert_near(cut4_score[:4], kalman_score[:4], atol=3e-10, rtol=3e-10)
            assert bool(tf.math.is_finite(dense_score[4]).numpy())
            assert bool(tf.math.is_finite(cut4_score[4]).numpy())


def test_p44_m4_dense_reference_refines_value_and_score_dims_1_2_3_horizons_2_4() -> None:
    theta = _theta0()
    for horizon in (2, 4):
        for dim in (1, 2, 3):
            low_value, low_score = _value_and_score(
                lambda current_theta: _dense_panel_value(current_theta, dim, horizon, order=181),
                theta,
            )
            high_value, high_score = _value_and_score(
                lambda current_theta: _dense_panel_value(current_theta, dim, horizon, order=241),
                theta,
            )
            value_gap = tf.abs(low_value - high_value)
            score_gap = _directional_abs_max(low_score, high_score)
            print(
                "P44_M4_DENSE_REFINEMENT "
                f"horizon={horizon} dim={dim} value_gap={float(value_gap.numpy()):.6e} "
                f"directional_score_gap={float(score_gap.numpy()):.6e}"
            )
            tf.debugging.assert_less(value_gap, tf.constant(5e-8, dtype=DTYPE))
            tf.debugging.assert_less(score_gap, tf.constant(5e-7, dtype=DTYPE))


def test_p44_m4_cut4_and_zhaocui_match_dense_horizon_2_dims_1_2_3() -> None:
    theta = _theta0()
    for dim in (1, 2, 3):
        dense_value, dense_score = _value_and_score(
            lambda current_theta: _dense_panel_value(current_theta, dim, 2, order=241),
            theta,
        )
        cut4_value, cut4_score = _value_and_score(
            lambda current_theta: _cut4_panel_value(current_theta, dim, 2),
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
            "P44_M4_H2_APPROXIMATION_GAP "
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
        tf.debugging.assert_less(cut4_value_gap, tf.constant(1e-3 * dim, dtype=DTYPE))
        tf.debugging.assert_less(cut4_score_gap, tf.constant(5e-3 * dim, dtype=DTYPE))
        tf.debugging.assert_less(cut4_score_rel, tf.constant(5e-3, dtype=DTYPE))
        tf.debugging.assert_less(tt_value_gap, tf.constant(5e-3 * dim, dtype=DTYPE))
        tf.debugging.assert_less(tt_score_gap, tf.constant(2e-2 * dim, dtype=DTYPE))
        tf.debugging.assert_less(tt_score_rel, tf.constant(1e-2, dtype=DTYPE))


def test_p44_m4_cut4_horizon_4_error_accumulation_is_bounded_dims_1_2_3() -> None:
    theta = _theta0()
    for dim in (1, 2, 3):
        dense_value, dense_score = _value_and_score(
            lambda current_theta: _dense_panel_value(current_theta, dim, 4, order=241),
            theta,
        )
        cut4_value, cut4_score = _value_and_score(
            lambda current_theta: _cut4_panel_value(current_theta, dim, 4),
            theta,
        )
        value_gap = tf.abs(cut4_value - dense_value)
        score_gap = _directional_abs_max(cut4_score, dense_score)
        score_rel = _relative_score_error(cut4_score, dense_score)
        print(
            "P44_M4_H4_CUT4_ACCUMULATION_GAP "
            f"dim={dim} value_gap={float(value_gap.numpy()):.6e} "
            f"directional_score_gap={float(score_gap.numpy()):.6e} "
            f"score_rel={float(score_rel.numpy()):.6e}"
        )
        tf.debugging.assert_less(value_gap, tf.constant(4e-3 * dim, dtype=DTYPE))
        tf.debugging.assert_less(score_gap, tf.constant(2e-2 * dim, dtype=DTYPE))
        tf.debugging.assert_less(score_rel, tf.constant(1e-2, dtype=DTYPE))


def test_p44_m4_zhaocui_horizon_4_is_explicit_nonclaim_for_current_scalar_helper() -> None:
    try:
        highdim.scalar_nonlinear_fixed_design_tt_value_path(
            _ScalarNonlinearTransitionSSM(0, initial_quadrature_order=181),
            _theta0(),
            _observations(1, 4),
            _tt_config(0),
            fixture_id="p44.m4.nonlinear-transition.axis-0.horizon-4.nonclaim",
            branch_seed_prefix="p44-m4-nonlinear-transition-axis-0-horizon-4-nonclaim",
            retained_moment_order=241,
            retained_propagation_order=241,
        )
    except ValueError as exc:
        assert "pinned to exactly two observations" in str(exc)
    else:
        raise AssertionError("Zhao-Cui scalar helper unexpectedly accepted horizon 4")


def test_p44_m4_cut4_metadata_keeps_transition_stress_boundary() -> None:
    result = tf_svd_cut4_filter(
        _observations(3, 4),
        _structural_model(_theta0(), 3),
        innovation_floor=tf.constant(1e-12, dtype=DTYPE),
        return_filtered=True,
    )
    assert result.metadata.approximation_label == "p44_m4_nonlinear_transition_cut4_same_target_approximation"
    assert int(result.diagnostics.extra["augmented_dim"].numpy()) == 6
    assert int(result.diagnostics.extra["point_count"].numpy()) <= 76
    assert int(result.diagnostics.extra["polynomial_degree"].numpy()) == 5
    assert int(result.diagnostics.extra["innovation_floor_count"].numpy()) == 0
