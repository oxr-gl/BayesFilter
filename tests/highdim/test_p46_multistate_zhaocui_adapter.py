from __future__ import annotations

from dataclasses import dataclass

import pytest
import tensorflow as tf
import tensorflow_probability as tfp

import bayesfilter.highdim as highdim


DTYPE = tf.float64


@dataclass(frozen=True)
class _IndependentGaussianMultistateModel:
    dim: int

    def parameter_dim(self) -> int:
        return 0

    def state_dim(self) -> int:
        return int(self.dim)

    def observation_dim(self) -> int:
        return int(self.dim)

    def initial_log_density(self, theta: tf.Tensor, x0: tf.Tensor) -> tf.Tensor:
        del theta
        values = _as_matrix(x0, self.dim)
        return tf.reduce_sum(_normal_log_prob(values, 0.0, 1.0), axis=1)

    def transition_log_density(
        self,
        theta: tf.Tensor,
        x_prev: tf.Tensor,
        x_next: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del theta, t
        previous = _as_matrix(x_prev, self.dim)
        current = _as_matrix(x_next, self.dim)
        loc = 0.55 * previous
        return tf.reduce_sum(_normal_log_prob(current, loc, 0.75), axis=1)

    def observation_log_density(
        self,
        theta: tf.Tensor,
        x_t: tf.Tensor,
        y_t: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del theta, t
        values = _as_matrix(x_t, self.dim)
        observation = tf.reshape(tf.convert_to_tensor(y_t, dtype=DTYPE), [self.dim])
        loc = 0.35 * values + 0.04 * tf.square(values)
        return tf.reduce_sum(_normal_log_prob(observation[tf.newaxis, :], loc, 0.55), axis=1)

    def manifest_payload(self) -> dict[str, object]:
        return {"family": "p46_independent_gaussian_multistate_fixture", "dim": int(self.dim)}


def _as_matrix(values: tf.Tensor, dim: int) -> tf.Tensor:
    tensor = tf.convert_to_tensor(values, dtype=DTYPE)
    if tensor.shape.rank == 1:
        tensor = tensor[tf.newaxis, :]
    if tensor.shape.rank != 2 or tensor.shape[1] != int(dim):
        raise ValueError("invalid fixture shape")
    return tensor


def _normal_log_prob(value: tf.Tensor, loc: float | tf.Tensor, scale: float | tf.Tensor) -> tf.Tensor:
    distribution = tfp.distributions.Normal(
        loc=tf.convert_to_tensor(loc, dtype=DTYPE),
        scale=tf.convert_to_tensor(scale, dtype=DTYPE),
    )
    return distribution.log_prob(tf.convert_to_tensor(value, dtype=DTYPE))


def _observations(dim: int) -> tf.Tensor:
    base = tf.constant(
        [
            [0.12, -0.08, 0.05],
            [-0.07, 0.11, -0.04],
        ],
        dtype=DTYPE,
    )
    return base[:, : int(dim)]


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _basis(dim: int, degree: int) -> highdim.ProductBasis:
    return highdim.ProductBasis(
        [
            highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), degree)
            for _ in range(int(dim))
        ],
        _convention(),
    )


def _initial_cores(product_basis: highdim.ProductBasis, ranks: tuple[int, ...]) -> tuple[highdim.TTCore, ...]:
    cores = []
    for axis, basis in enumerate(product_basis.bases):
        cores.append(tf.ones([ranks[axis], basis.basis_dim, ranks[axis + 1]], dtype=DTYPE))
    return tuple(highdim.TTCore(core) for core in cores)


def _tt_config(dim: int, seed: str, *, quadrature_order: int = 5) -> highdim.FixedBranchFilterConfig:
    product_basis = _basis(dim, degree=max(5, int(quadrature_order) - 1))
    ranks = tuple([1] + [2] * (int(dim) - 1) + [1])
    return highdim.FixedBranchFilterConfig(
        fit_config=highdim.FixedTTFitConfig(
            ranks=ranks,
            ridge=1e-10,
            max_sweeps=3,
            sweep_order=tuple(range(int(dim))),
            row_budget=400,
            column_budget=80,
            dense_matrix_byte_budget=300_000,
            normal_matrix_byte_budget=80_000,
            condition_number_warning=1e11,
            condition_number_veto=1e16,
            holdout_tolerance=1e-2,
        ),
        density_tau=1e-12,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(
            highdim.AffineCoordinateMap(
                offset=tf.zeros([int(dim)], dtype=DTYPE),
                matrix=5.0 * tf.eye(int(dim), dtype=DTYPE),
            ),
        ),
        measure_convention=_convention(),
        deterministic_seed=seed,
        product_basis=product_basis,
        initial_cores=_initial_cores(product_basis, ranks),
        fit_quadrature_order=int(quadrature_order),
    )


def _grid(config: highdim.FixedBranchFilterConfig) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    reference_points, reference_weights = _reference_grid(config.product_basis, config.fit_quadrature_order)
    physical_points, log_abs_det = config.coordinate_maps[0].forward(reference_points)
    return reference_points, reference_weights, physical_points, log_abs_det


def _log_uniform_reference_weight_density(product_basis: highdim.ProductBasis) -> tf.Tensor:
    log_density = tf.constant(0.0, dtype=DTYPE)
    for basis in product_basis.bases:
        log_density = log_density - tf.math.log(basis.domain.length)
    return log_density


def _reference_grid(product_basis: highdim.ProductBasis, order: int) -> tuple[tf.Tensor, tf.Tensor]:
    nodes_1d, weights_1d = highdim.legendre_gauss_nodes_weights(order)
    axis_nodes = []
    axis_weights = []
    for basis in product_basis.bases:
        half_length = 0.5 * basis.domain.length
        midpoint = 0.5 * (basis.domain.left + basis.domain.right)
        axis_nodes.append(midpoint + half_length * nodes_1d)
        axis_weights.append(0.5 * weights_1d)
    mesh_nodes = tf.meshgrid(*axis_nodes, indexing="ij")
    mesh_weights = tf.meshgrid(*axis_weights, indexing="ij")
    points = tf.stack([tf.reshape(axis, [-1]) for axis in mesh_nodes], axis=1)
    weights = tf.ones([tf.shape(points)[0]], dtype=DTYPE)
    for axis_weight in mesh_weights:
        weights = weights * tf.reshape(axis_weight, [-1])
    return points, weights


def _dense_reference(dim: int, order: int = 7) -> dict[str, tf.Tensor]:
    model = _IndependentGaussianMultistateModel(dim)
    config = _tt_config(dim, f"p46-dense-grid-dim-{dim}", quadrature_order=order)
    observations = _observations(dim)
    _, weights, physical_points, log_abs_det = _grid(config)
    log_reference_weight = _log_uniform_reference_weight_density(config.product_basis)
    log_terms = []
    means = []
    covariances = []
    log_posterior_physical = None
    for time_index in range(int(observations.shape[0])):
        if time_index == 0:
            log_unnormalized = model.initial_log_density(
                tf.zeros([0], dtype=DTYPE),
                physical_points,
            ) + model.observation_log_density(
                tf.zeros([0], dtype=DTYPE),
                physical_points,
                observations[time_index],
                t=time_index,
            )
        else:
            previous_count = int(physical_points.shape[0])
            current_count = int(physical_points.shape[0])
            next_points = tf.repeat(physical_points, repeats=previous_count, axis=0)
            previous_points = tf.tile(physical_points, [current_count, 1])
            transition_log = tf.reshape(
                model.transition_log_density(
                    tf.zeros([0], dtype=DTYPE),
                    previous_points,
                    next_points,
                    t=time_index,
                ),
                [current_count, previous_count],
            )
            log_predictive = tf.reduce_logsumexp(
                tf.math.log(weights)[tf.newaxis, :]
                + log_abs_det[tf.newaxis, :]
                - log_reference_weight
                + log_posterior_physical[tf.newaxis, :]
                + transition_log,
                axis=1,
            )
            log_unnormalized = log_predictive + model.observation_log_density(
                tf.zeros([0], dtype=DTYPE),
                physical_points,
                observations[time_index],
                t=time_index,
            )
        log_increment = _logsumexp_weighted(
            log_unnormalized + log_abs_det - log_reference_weight,
            weights,
        )
        log_posterior_physical = log_unnormalized - log_increment
        mass = weights * tf.exp(log_posterior_physical + log_abs_det - log_reference_weight)
        mean = tf.reduce_sum(physical_points * mass[:, tf.newaxis], axis=0)
        centered = physical_points - mean[tf.newaxis, :]
        covariance = tf.einsum("n,ni,nj->ij", mass, centered, centered)
        log_terms.append(log_increment)
        means.append(mean)
        covariances.append(covariance)
    return {
        "log_likelihood": tf.reduce_sum(tf.stack(log_terms)),
        "log_normalizers": tf.stack(log_terms),
        "mean_path": tf.stack(means),
        "covariance_path": tf.stack(covariances),
    }


def _logsumexp_weighted(log_values: tf.Tensor, weights: tf.Tensor) -> tf.Tensor:
    max_value = tf.reduce_max(log_values)
    return tf.math.log(tf.reduce_sum(weights * tf.exp(log_values - max_value))) + max_value


def _tt_result(dim: int, seed: str) -> highdim.FixedBranchFilterResult:
    order = 7 if int(dim) == 2 else 5
    return highdim.multistate_nonlinear_fixed_design_tt_value_path(
        _IndependentGaussianMultistateModel(dim),
        tf.zeros([0], dtype=DTYPE),
        _observations(dim),
        _tt_config(dim, seed, quadrature_order=order),
        fixture_id=f"p46.multistate.dim{dim}.v1",
        branch_seed_prefix=seed,
        retained_moment_order=order,
        retained_propagation_order=order,
    )


@pytest.mark.parametrize("dim", [2, 3])
def test_p46_multistate_zhaocui_adapter_matches_dense_reference_value(dim: int) -> None:
    result = _tt_result(dim, f"p46-multistate-dim-{dim}")
    reference_order = 7 if int(dim) == 2 else 5
    reference = _dense_reference(dim, order=reference_order)

    assert result.status is highdim.HighDimStatus.OK
    assert result.diagnostics["value_path"] == "multistate_nonlinear_fixed_design_tt_value_path"
    assert result.diagnostics["state_dim"] == dim
    assert result.steps[0].diagnostics["retained_propagation_order"] == reference_order
    assert result.retained_filter.storage_kind == "multistate_tt_grid"
    assert result.retained_filter.retained_axes == tuple(range(dim))
    assert result.retained_filter.diagnostics["mean"].shape == (dim,)
    assert result.retained_filter.diagnostics["covariance"].shape == (dim, dim)

    log_normalizers = tf.stack([step.log_normalizer for step in result.steps])
    tf.debugging.assert_near(result.log_likelihood, reference["log_likelihood"], atol=8e-2, rtol=2e-2)
    tf.debugging.assert_near(log_normalizers, reference["log_normalizers"], atol=8e-2, rtol=2e-2)
    for step in result.steps:
        assert step.fit_result is not None
        assert step.density is not None
        assert step.diagnostics["density_hash"] == step.density.branch_identity.hash.value
        assert step.retained_filter.diagnostics["density_hash"] == step.density.branch_identity.hash.value
        tf.debugging.assert_near(
            step.diagnostics["retained_moment_mass"],
            tf.constant(1.0, dtype=DTYPE),
            atol=5e-3,
        )


def test_p46_multistate_zhaocui_adapter_replay_is_deterministic() -> None:
    left = _tt_result(2, "p46-multistate-replay")
    right = _tt_result(2, "p46-multistate-replay")

    tf.debugging.assert_near(left.log_likelihood, right.log_likelihood, atol=0.0)
    assert left.branch_identity.hash.value == right.branch_identity.hash.value
    assert left.retained_filter.branch_identity.hash.value == right.retained_filter.branch_identity.hash.value
    assert tuple(step.branch_identity.hash.value for step in left.steps) == tuple(
        step.branch_identity.hash.value for step in right.steps
    )


def test_p46_multistate_zhaocui_adapter_rejects_dimension_mismatch() -> None:
    config = _tt_config(2, "p46-dimension-mismatch")
    with pytest.raises(ValueError, match="product_basis"):
        highdim.multistate_nonlinear_fixed_design_tt_value_path(
            _IndependentGaussianMultistateModel(3),
            tf.zeros([0], dtype=DTYPE),
            _observations(3),
            config,
        )


def test_p46_multistate_zhaocui_adapter_rejects_scalar_model() -> None:
    with pytest.raises(TypeError, match="state_dim > 1"):
        highdim.multistate_nonlinear_fixed_design_tt_value_path(
            _IndependentGaussianMultistateModel(1),
            tf.zeros([0], dtype=DTYPE),
            _observations(1),
            _tt_config(1, "p46-scalar-rejection"),
        )
