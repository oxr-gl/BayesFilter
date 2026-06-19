"""Experimental transformed-SV Gaussian-mixture CUT4 comparator."""

from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import product
from types import MappingProxyType
from typing import Mapping

import tensorflow as tf
import tensorflow_probability as tfp

from bayesfilter import StatePartition
from bayesfilter.diagnostics import TFFilterDiagnostics, TFRegularizationDiagnostics
from bayesfilter.highdim.models import StochasticVolatilitySSM
from bayesfilter.nonlinear.fixed_sgqf_derivatives_tf import (
    TFFixedSGQFDerivatives,
    TFFixedSGQFScoreResult,
    tf_fixed_sgqf_score,
)
from bayesfilter.nonlinear.fixed_sgqf_tf import (
    TFFixedSGQFAffineModel,
    TFFixedSGQFBranchConfig,
    TFFixedSGQFCloud,
    tf_fixed_sgqf_cloud,
    tf_fixed_sgqf_filter,
)
from bayesfilter.nonlinear.svd_cut_tf import tf_svd_cut4_filter
from bayesfilter.nonlinear.svd_sigma_point_derivatives_tf import TFStructuralFirstDerivatives, tf_svd_ukf_score
from bayesfilter.nonlinear.sigma_points_tf import tf_svd_sigma_point_filter
from bayesfilter.results_tf import TFFilterDerivativeResult
from bayesfilter.structural import StructuralFilterConfig
from bayesfilter.structural_tf import make_affine_structural_tf


KSC_LOG_CHI_SQUARE_MEAN_SHIFT = tf.constant(1.2704, dtype=tf.float64)
_STD_NORMAL = tfp.distributions.Normal(
    loc=tf.constant(0.0, dtype=tf.float64),
    scale=tf.constant(1.0, dtype=tf.float64),
)


@dataclass(frozen=True)
class SVLogChiSquareGaussianMixture:
    """Finite normal mixture approximation for log chi-square observation noise."""

    weights: tf.Tensor
    means: tf.Tensor
    variances: tf.Tensor
    source: str = "p39_pinned_seven_component_log_chi_square_mixture_ksc_context"

    def __post_init__(self) -> None:
        weights = tf.convert_to_tensor(self.weights, dtype=tf.float64)
        means = tf.convert_to_tensor(self.means, dtype=tf.float64)
        variances = tf.convert_to_tensor(self.variances, dtype=tf.float64)
        if weights.shape.rank != 1 or means.shape != weights.shape or variances.shape != weights.shape:
            raise ValueError("mixture weights, means, and variances must be same-length vectors")
        if not bool(tf.reduce_all(tf.math.is_finite(weights)).numpy()):
            raise ValueError("mixture weights must be finite")
        if not bool(tf.reduce_all(tf.math.is_finite(means)).numpy()):
            raise ValueError("mixture means must be finite")
        if not bool(tf.reduce_all(tf.math.is_finite(variances)).numpy()):
            raise ValueError("mixture variances must be finite")
        if not bool(tf.reduce_all(weights > 0.0).numpy()):
            raise ValueError("mixture weights must be positive")
        if not bool(tf.reduce_all(variances > 0.0).numpy()):
            raise ValueError("mixture variances must be positive")
        if not bool(tf.abs(tf.reduce_sum(weights) - 1.0).numpy() <= 1e-12):
            raise ValueError("mixture weights must sum to one")
        object.__setattr__(self, "weights", weights)
        object.__setattr__(self, "means", means)
        object.__setattr__(self, "variances", variances)

    @property
    def component_count(self) -> int:
        return int(self.weights.shape[0])

    def manifest_payload(self) -> Mapping[str, object]:
        return MappingProxyType(
            {
                "source": self.source,
                "component_count": self.component_count,
                "weights": tuple(float(value) for value in self.weights.numpy()),
                "means": tuple(float(value) for value in self.means.numpy()),
                "variances": tuple(float(value) for value in self.variances.numpy()),
                "mean": float(tf.reduce_sum(self.weights * self.means).numpy()),
                "variance": float(
                    tf.reduce_sum(
                        self.weights
                        * (
                            self.variances
                            + tf.square(self.means - tf.reduce_sum(self.weights * self.means))
                        )
                    ).numpy()
                ),
            }
        )


@dataclass(frozen=True)
class SVMixtureCut4Result:
    """Value-path result for the P39 scalar transformed-SV mixture comparator."""

    log_likelihood: tf.Tensor
    log_normalizers: tf.Tensor
    mean_path: tf.Tensor
    variance_path: tf.Tensor
    component_weights: tf.Tensor
    diagnostics: Mapping[str, object]


@dataclass(frozen=True)
class SVPanelMixtureFilterResult:
    """Value-path result for independent-panel transformed-SV mixture filters."""

    log_likelihood: tf.Tensor
    log_normalizers: tf.Tensor
    mean_path: tf.Tensor
    covariance_path: tf.Tensor
    component_weights: tf.Tensor
    diagnostics: Mapping[str, object]


@dataclass(frozen=True)
class SVPanelMixtureScoreResult:
    """Analytic score result for independent-panel transformed-SV mixture filters."""

    log_likelihood: tf.Tensor | None
    score: tf.Tensor | None
    mean_path: tf.Tensor | None
    covariance_path: tf.Tensor | None
    d_mean_path: tf.Tensor | None
    d_covariance_path: tf.Tensor | None
    diagnostics: Mapping[str, object]


@dataclass(frozen=True)
class ExactTransformedSVSSM:
    """Scalar SV model for the exact ``z=log(y**2)`` transformed target."""

    sigma: float | tf.Tensor = 1.0
    parameterization: str = "synthetic_unconstrained"

    def __post_init__(self) -> None:
        sigma = tf.convert_to_tensor(self.sigma, dtype=tf.float64)
        if sigma.shape.rank != 0:
            raise ValueError("sigma must be scalar")
        if not bool(tf.math.is_finite(sigma).numpy()) or bool((sigma <= 0.0).numpy()):
            raise ValueError("sigma must be finite and positive")
        if self.parameterization != "synthetic_unconstrained":
            raise ValueError("ExactTransformedSVSSM currently supports synthetic_unconstrained")
        object.__setattr__(self, "sigma", sigma)

    def parameter_dim(self) -> int:
        return 2

    def state_dim(self) -> int:
        return 1

    def observation_dim(self) -> int:
        return 1

    def physical_parameters(self, theta: tf.Tensor) -> Mapping[str, tf.Tensor]:
        return StochasticVolatilitySSM(
            sigma=self.sigma,
            parameterization=self.parameterization,
        ).physical_parameters(theta)

    def unconstrained_from_physical(self, gamma: float | tf.Tensor, beta: float | tf.Tensor) -> tf.Tensor:
        return StochasticVolatilitySSM(
            sigma=self.sigma,
            parameterization=self.parameterization,
        ).unconstrained_from_physical(gamma=gamma, beta=beta)

    def initial_log_density(self, theta: tf.Tensor, x0: tf.Tensor) -> tf.Tensor:
        return StochasticVolatilitySSM(
            sigma=self.sigma,
            parameterization=self.parameterization,
        ).initial_log_density(theta, x0)

    def transition_log_density(
        self,
        theta: tf.Tensor,
        x_prev: tf.Tensor,
        x_next: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        return StochasticVolatilitySSM(
            sigma=self.sigma,
            parameterization=self.parameterization,
        ).transition_log_density(theta, x_prev, x_next, t=t)

    def observation_log_density(
        self,
        theta: tf.Tensor,
        x_t: tf.Tensor,
        y_t: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del t
        values = _as_row_matrix(x_t, self.state_dim(), "x_t")
        observation = tf.reshape(tf.convert_to_tensor(y_t, dtype=tf.float64), [self.observation_dim()])
        parameters = self.physical_parameters(theta)
        residual = observation[0] - tf.math.log(tf.square(parameters["beta"])) - values[:, 0]
        return exact_log_chi_square_log_density(residual)

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "ExactTransformedSVSSM",
            "sigma": self.sigma,
            "parameterization": self.parameterization,
            "target": "z_t=log(y_t^2), z_t-log(beta^2)-h_t ~ log(chi_square_1)",
            "source": "P41 exact transformed stochastic-volatility ladder",
            "what_is_not_claimed": (
                "KSC Gaussian mixture approximation",
                "coupled multivariate Zhao-Cui TT",
                "generalized SV/CNS estimator",
            ),
        }


@dataclass(frozen=True)
class KSCMixtureTransformedSVSSM:
    """Scalar transformed SV model with finite Gaussian-mixture observation noise."""

    sigma: float | tf.Tensor = 1.0
    mixture: SVLogChiSquareGaussianMixture | None = None
    transform_offset: float | tf.Tensor = 1e-8
    parameterization: str = "synthetic_unconstrained"

    def __post_init__(self) -> None:
        sigma = tf.convert_to_tensor(self.sigma, dtype=tf.float64)
        transform_offset = tf.convert_to_tensor(self.transform_offset, dtype=tf.float64)
        mixture = self.mixture or ksc_1998_log_chi_square_mixture()
        if sigma.shape.rank != 0:
            raise ValueError("sigma must be scalar")
        if transform_offset.shape.rank != 0:
            raise ValueError("transform_offset must be scalar")
        if not bool(tf.math.is_finite(sigma).numpy()) or bool((sigma <= 0.0).numpy()):
            raise ValueError("sigma must be finite and positive")
        if not bool(tf.math.is_finite(transform_offset).numpy()) or bool((transform_offset < 0.0).numpy()):
            raise ValueError("transform_offset must be finite and nonnegative")
        if self.parameterization != "synthetic_unconstrained":
            raise ValueError("KSCMixtureTransformedSVSSM currently supports synthetic_unconstrained")
        object.__setattr__(self, "sigma", sigma)
        object.__setattr__(self, "mixture", mixture)
        object.__setattr__(self, "transform_offset", transform_offset)

    def parameter_dim(self) -> int:
        return 2

    def state_dim(self) -> int:
        return 1

    def observation_dim(self) -> int:
        return 1

    def physical_parameters(self, theta: tf.Tensor) -> Mapping[str, tf.Tensor]:
        return StochasticVolatilitySSM(
            sigma=self.sigma,
            parameterization=self.parameterization,
        ).physical_parameters(theta)

    def unconstrained_from_physical(self, gamma: float | tf.Tensor, beta: float | tf.Tensor) -> tf.Tensor:
        return StochasticVolatilitySSM(
            sigma=self.sigma,
            parameterization=self.parameterization,
        ).unconstrained_from_physical(gamma=gamma, beta=beta)

    def initial_log_density(self, theta: tf.Tensor, x0: tf.Tensor) -> tf.Tensor:
        return StochasticVolatilitySSM(
            sigma=self.sigma,
            parameterization=self.parameterization,
        ).initial_log_density(theta, x0)

    def transition_log_density(
        self,
        theta: tf.Tensor,
        x_prev: tf.Tensor,
        x_next: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        return StochasticVolatilitySSM(
            sigma=self.sigma,
            parameterization=self.parameterization,
        ).transition_log_density(theta, x_prev, x_next, t=t)

    def observation_log_density(
        self,
        theta: tf.Tensor,
        x_t: tf.Tensor,
        y_t: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del t
        values = _as_row_matrix(x_t, self.state_dim(), "x_t")
        transformed_observation = tf.reshape(tf.convert_to_tensor(y_t, dtype=tf.float64), [1])
        parameters = self.physical_parameters(theta)
        loc_base = tf.math.log(tf.square(parameters["beta"])) + values[:, 0]
        component_log_terms = []
        for component in range(self.mixture.component_count):
            component_log_terms.append(
                tf.math.log(self.mixture.weights[component])
                + _normal_log_prob(
                    transformed_observation[0],
                    loc_base + self.mixture.means[component],
                    tf.sqrt(self.mixture.variances[component]),
                )
            )
        return tf.reduce_logsumexp(tf.stack(component_log_terms, axis=0), axis=0)

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "KSCMixtureTransformedSVSSM",
            "sigma": self.sigma,
            "parameterization": self.parameterization,
            "target": "z_t=log(y_t^2+offset), z_t-log(beta^2)-h_t approximated by finite Gaussian mixture",
            "transform_offset": self.transform_offset,
            "mixture": self.mixture.manifest_payload(),
            "source": "Kim-Shephard-Chib finite mixture context used as a declared approximation target",
            "what_is_not_claimed": (
                "exact native SV likelihood",
                "native generalized SV/CNS estimator",
                "KSC importance reweighting",
                "coupled multivariate Zhao-Cui TT",
            ),
        }


@dataclass(frozen=True)
class ExactTransformedSVPanelResult:
    """Independent-panel exact transformed SV value-path result."""

    log_likelihood: tf.Tensor
    log_normalizers: tf.Tensor
    coordinate_results: tuple[object, ...]
    diagnostics: Mapping[str, object]


def ksc_1998_log_chi_square_mixture() -> SVLogChiSquareGaussianMixture:
    """Return the KSC seven-component mixture for ``log(epsilon**2)``.

    Kim--Shephard--Chib tabulate component locations for
    ``log(epsilon**2) + 1.2704``.  The BayesFilter observation equation uses
    ``log(epsilon**2)`` directly, so the effective component means subtract
    the same shift.
    """

    raw_locations = tf.constant(
        [-10.12999, -3.97281, -8.56686, 2.77786, 0.61942, 1.79518, -1.08819],
        dtype=tf.float64,
    )
    return SVLogChiSquareGaussianMixture(
        weights=tf.constant(
            [0.00730, 0.10556, 0.00002, 0.04395, 0.34001, 0.24566, 0.25750],
            dtype=tf.float64,
        ),
        means=raw_locations - KSC_LOG_CHI_SQUARE_MEAN_SHIFT,
        variances=tf.constant(
            [5.79596, 2.61369, 5.17950, 0.16735, 0.64009, 0.34023, 1.26261],
            dtype=tf.float64,
        ),
        source="kim_shephard_chib_1998_table_4_locations_shifted_by_minus_1p2704",
    )


def exact_log_chi_square_log_density(value: tf.Tensor) -> tf.Tensor:
    """Return log density of ``log(epsilon**2)`` for ``epsilon ~ N(0, 1)``."""

    u = tf.convert_to_tensor(value, dtype=tf.float64)
    return 0.5 * u - 0.5 * tf.exp(u) - 0.5 * tf.math.log(tf.constant(2.0 * math.pi, dtype=tf.float64))


def exact_transformed_sv_observations(observations: tf.Tensor) -> tf.Tensor:
    """Return coordinatewise exact ``log(y_t**2)`` for nonzero SV observations."""

    y = tf.convert_to_tensor(observations, dtype=tf.float64)
    if y.shape.rank == 1:
        y = y[:, tf.newaxis]
    if y.shape.rank != 2:
        raise ValueError("exact transformed SV observations require [time, dim] observations")
    if not bool(tf.reduce_all(tf.math.is_finite(y)).numpy()):
        raise ValueError("observations must be finite")
    if not bool(tf.reduce_all(tf.not_equal(y, 0.0)).numpy()):
        raise ValueError("exact log-square transform requires nonzero observations")
    return tf.math.log(tf.square(y))


def exact_transformed_sv_jacobian_log_abs_det(observations: tf.Tensor) -> tf.Tensor:
    """Return ``sum_t,i log(abs(y_ti))`` for the raw-to-log-square relation."""

    y = tf.convert_to_tensor(observations, dtype=tf.float64)
    if y.shape.rank == 1:
        y = y[:, tf.newaxis]
    if y.shape.rank != 2:
        raise ValueError("SV observations require [time, dim] observations")
    if not bool(tf.reduce_all(tf.math.is_finite(y)).numpy()):
        raise ValueError("observations must be finite")
    if not bool(tf.reduce_all(tf.not_equal(y, 0.0)).numpy()):
        raise ValueError("Jacobian relation requires nonzero observations")
    return tf.reduce_sum(tf.math.log(tf.abs(y)))


def exact_transformed_sv_scalar_dense_reference(
    model: ExactTransformedSVSSM,
    theta: tf.Tensor,
    observations: tf.Tensor,
    *,
    order: int = 321,
    radius: float = 8.0,
) -> SVMixtureCut4Result:
    """Sequential dense-grid reference for exact transformed scalar SV."""

    z = exact_transformed_sv_observations(observations)
    if int(z.shape[1]) != 1:
        raise ValueError("scalar exact transformed SV dense reference requires scalar observations")
    x_grid, weights = _legendre_interval_nodes_weights(order=order, left=-radius, right=radius)
    theta_vector = tf.convert_to_tensor(theta, dtype=tf.float64)
    parameters = model.physical_parameters(theta_vector)
    gamma = parameters["gamma"]
    sigma = parameters["sigma"]
    prior_scale = sigma / tf.sqrt(1.0 - tf.square(gamma))
    log_density = _normal_log_prob(x_grid, tf.constant(0.0, dtype=tf.float64), prior_scale)
    log_terms = []
    means = []
    variances = []

    for time_index in range(int(z.shape[0])):
        if time_index > 0:
            previous_density = tf.exp(log_density - log_terms[-1])
            transition_log = _normal_log_prob(
                x_grid[:, tf.newaxis],
                gamma * x_grid[tf.newaxis, :],
                sigma,
            )
            predictive = tf.reduce_sum(
                weights[tf.newaxis, :] * previous_density[tf.newaxis, :] * tf.exp(transition_log),
                axis=1,
            )
            log_density = tf.math.log(predictive)
        observation_log = model.observation_log_density(
            theta_vector,
            x_grid[:, tf.newaxis],
            z[time_index],
            t=time_index,
        )
        log_density = log_density + observation_log
        log_normalizer = _logsumexp_weighted(log_density, weights)
        normalized_density = tf.exp(log_density - log_normalizer)
        mean = tf.reduce_sum(weights * x_grid * normalized_density)
        second = tf.reduce_sum(weights * tf.square(x_grid) * normalized_density)
        log_terms.append(log_normalizer)
        means.append(mean)
        variances.append(second - tf.square(mean))

    return SVMixtureCut4Result(
        log_likelihood=tf.reduce_sum(tf.stack(log_terms)),
        log_normalizers=tf.stack(log_terms),
        mean_path=tf.stack(means),
        variance_path=tf.stack(variances),
        component_weights=tf.zeros([int(z.shape[0]), 0], dtype=tf.float64),
        diagnostics=MappingProxyType(
            {
                "backend": "dense_exact_transformed_sv_log_chi_square",
                "grid_order": int(order),
                "radius": float(radius),
                "target": "z=log(y^2), exact log-chi-square observation noise",
                "transform_offset": 0.0,
                "non_claims": (
                    "not KSC Gaussian mixture approximation",
                    "not coupled multivariate Zhao-Cui TT",
                    "no generalized SV/CNS estimator",
                ),
            }
        ),
    )


def exact_transformed_sv_independent_panel_dense_reference(
    observations: tf.Tensor,
    *,
    gamma: float | tf.Tensor,
    beta: float | tf.Tensor,
    sigma: float | tf.Tensor,
    order: int = 321,
    radius: float = 8.0,
) -> ExactTransformedSVPanelResult:
    """Independent-panel exact transformed dense reference by coordinate sum."""

    y = tf.convert_to_tensor(observations, dtype=tf.float64)
    if y.shape.rank == 1:
        y = y[:, tf.newaxis]
    z = exact_transformed_sv_observations(y)
    dim = int(z.shape[1])
    gamma_vector = _as_panel_parameter(gamma, dim, "gamma")
    beta_vector = _as_panel_parameter(beta, dim, "beta")
    sigma_vector = _as_panel_parameter(sigma, dim, "sigma")
    _validate_panel_parameters(gamma_vector, beta_vector, sigma_vector)
    results = []
    log_terms = []
    for axis in range(dim):
        model = ExactTransformedSVSSM(sigma=sigma_vector[axis])
        theta = model.unconstrained_from_physical(gamma=gamma_vector[axis], beta=beta_vector[axis])
        result = exact_transformed_sv_scalar_dense_reference(
            model,
            theta,
            y[:, axis : axis + 1],
            order=order,
            radius=radius,
        )
        results.append(result)
        log_terms.append(result.log_normalizers)
    stacked_log_terms = tf.stack(log_terms, axis=0)
    return ExactTransformedSVPanelResult(
        log_likelihood=tf.reduce_sum(stacked_log_terms),
        log_normalizers=tf.reduce_sum(stacked_log_terms, axis=0),
        coordinate_results=tuple(results),
        diagnostics=MappingProxyType(
            {
                "backend": "independent_panel_dense_exact_transformed_sv",
                "panel_dim": dim,
                "target": "factorized coordinatewise exact transformed SV",
                "transform_offset": 0.0,
                "non_claims": (
                    "not coupled multivariate Zhao-Cui TT",
                    "not KSC Gaussian mixture approximation",
                    "no generalized SV/CNS estimator",
                ),
            }
        ),
    )


def exact_transformed_sv_independent_panel_zhaocui_tt_filter(
    observations: tf.Tensor,
    *,
    gamma: float | tf.Tensor,
    beta: float | tf.Tensor,
    sigma: float | tf.Tensor,
    config,
    fixture_id: str = "p41.exact-transformed-sv.factorized-zhaocui-tt.v1",
    branch_seed_prefix: str = "p41-exact-transformed-sv-factorized-tt",
) -> ExactTransformedSVPanelResult:
    """Run scalar fixed-design TT lanes per coordinate for exact transformed SV.

    This is an independent-product panel construction.  It is not a coupled
    multivariate Zhao--Cui TT implementation.
    """

    from bayesfilter.highdim.filtering import scalar_nonlinear_fixed_design_tt_value_path

    z = exact_transformed_sv_observations(observations)
    dim = int(z.shape[1])
    gamma_vector = _as_panel_parameter(gamma, dim, "gamma")
    beta_vector = _as_panel_parameter(beta, dim, "beta")
    sigma_vector = _as_panel_parameter(sigma, dim, "sigma")
    _validate_panel_parameters(gamma_vector, beta_vector, sigma_vector)
    results = []
    log_terms = []
    for axis in range(dim):
        model = ExactTransformedSVSSM(sigma=sigma_vector[axis])
        theta = model.unconstrained_from_physical(gamma=gamma_vector[axis], beta=beta_vector[axis])
        result = scalar_nonlinear_fixed_design_tt_value_path(
            model,
            theta,
            z[:, axis : axis + 1],
            config,
            fixture_id=f"{fixture_id}.coord{axis}",
            branch_seed_prefix=f"{branch_seed_prefix}:coord{axis}",
        )
        results.append(result)
        log_terms.append(tf.stack([step.log_normalizer for step in result.steps]))
    stacked_log_terms = tf.stack(log_terms, axis=0)
    return ExactTransformedSVPanelResult(
        log_likelihood=tf.reduce_sum(stacked_log_terms),
        log_normalizers=tf.reduce_sum(stacked_log_terms, axis=0),
        coordinate_results=tuple(results),
        diagnostics=MappingProxyType(
            {
                "backend": "factorized_scalar_zhaocui_tt_exact_transformed_sv",
                "panel_dim": dim,
                "target": "factorized coordinatewise exact transformed SV",
                "transform_offset": 0.0,
                "value_path": "scalar_nonlinear_fixed_design_tt_value_path_per_coordinate",
                "non_claims": (
                    "not coupled multivariate Zhao-Cui TT",
                    "not KSC Gaussian mixture approximation",
                    "no generalized SV/CNS estimator",
                    "no high-dimensional scalability claim",
                ),
            }
        ),
    )


def independent_panel_sv_mixture_zhaocui_tt_filter(
    observations: tf.Tensor,
    *,
    gamma: float | tf.Tensor,
    beta: float | tf.Tensor,
    sigma: float | tf.Tensor,
    config,
    mixture: SVLogChiSquareGaussianMixture | None = None,
    transform_offset: float | tf.Tensor = 1e-8,
    fixture_id: str = "p47.ksc-mixture-sv.factorized-zhaocui-tt.v1",
    branch_seed_prefix: str = "p47-ksc-mixture-sv-factorized-tt",
) -> SVPanelMixtureFilterResult:
    """Run scalar fixed-design TT lanes per coordinate for the KSC mixture target.

    The route evaluates the declared finite-mixture transformed-SV target with
    independent scalar fixed-design TT lanes.  It is not adaptive TT-cross/SIRT,
    not a coupled multivariate TT implementation, and not native generalized SV.
    """

    from bayesfilter.highdim.filtering import scalar_nonlinear_fixed_design_tt_value_path

    mixture = mixture or ksc_1998_log_chi_square_mixture()
    z = transformed_sv_panel_observations(observations, offset=transform_offset)
    dim = int(z.shape[1])
    gamma_vector = _as_panel_parameter(gamma, dim, "gamma")
    beta_vector = _as_panel_parameter(beta, dim, "beta")
    sigma_vector = _as_panel_parameter(sigma, dim, "sigma")
    _validate_panel_parameters(gamma_vector, beta_vector, sigma_vector)
    results = []
    log_terms = []
    mean_terms = []
    variance_terms = []
    for axis in range(dim):
        model = KSCMixtureTransformedSVSSM(
            sigma=sigma_vector[axis],
            mixture=mixture,
            transform_offset=(
                transform_offset
                if tf.convert_to_tensor(transform_offset, dtype=tf.float64).shape.rank == 0
                else tf.convert_to_tensor(transform_offset, dtype=tf.float64)[axis]
            ),
        )
        theta = model.unconstrained_from_physical(gamma=gamma_vector[axis], beta=beta_vector[axis])
        result = scalar_nonlinear_fixed_design_tt_value_path(
            model,
            theta,
            z[:, axis : axis + 1],
            config,
            fixture_id=f"{fixture_id}.coord{axis}",
            branch_seed_prefix=f"{branch_seed_prefix}:coord{axis}",
        )
        results.append(result)
        log_terms.append(tf.stack([step.log_normalizer for step in result.steps]))
        mean_terms.append(tf.concat([step.diagnostics["retained_mean"] for step in result.steps], axis=0))
        variance_terms.append(tf.stack([step.diagnostics["retained_variance"] for step in result.steps]))
    stacked_log_terms = tf.stack(log_terms, axis=0)
    stacked_means = tf.transpose(tf.stack(mean_terms, axis=0))
    stacked_variances = tf.transpose(tf.stack(variance_terms, axis=0))
    covariance_path = tf.stack(
        [tf.linalg.diag(stacked_variances[time_index]) for time_index in range(int(z.shape[0]))],
        axis=0,
    )
    return SVPanelMixtureFilterResult(
        log_likelihood=tf.reduce_sum(stacked_log_terms),
        log_normalizers=tf.reduce_sum(stacked_log_terms, axis=0),
        mean_path=stacked_means,
        covariance_path=covariance_path,
        component_weights=tf.zeros([int(z.shape[0]), 0], dtype=tf.float64),
        diagnostics=MappingProxyType(
            {
                "backend": "factorized_scalar_zhaocui_tt_transformed_sv_gaussian_mixture",
                "panel_dim": dim,
                "target": "factorized coordinatewise transformed SV finite Gaussian mixture",
                "transform_offset": _manifest_value(transform_offset),
                "value_path": "scalar_nonlinear_fixed_design_tt_value_path_per_coordinate",
                "coordinate_result_count": len(results),
                "mixture": mixture.manifest_payload(),
                "target_scope": "independent_product_transformed_sv_panel_tiny_fixture",
                "m1_route_label": "documented-deviation fixed-design substitute",
                "non_claims": (
                    "not exact native SV likelihood",
                    "not native generalized SV/CNS estimator",
                    "not coupled multivariate Zhao-Cui TT",
                    "not adaptive MATLAB TT-cross/SIRT reproduction",
                    "no high-dimensional scalability claim",
                ),
            }
        ),
    )


def transformed_sv_observations(
    observations: tf.Tensor,
    *,
    offset: float | tf.Tensor = 1e-8,
) -> tf.Tensor:
    """Return `log(y_t^2 + offset)` for scalar SV observations."""

    y = tf.convert_to_tensor(observations, dtype=tf.float64)
    if y.shape.rank == 1:
        y = y[:, tf.newaxis]
    if y.shape.rank != 2 or y.shape[1] != 1:
        raise ValueError("SV mixture transform requires scalar observations")
    offset_tensor = tf.convert_to_tensor(offset, dtype=tf.float64)
    if offset_tensor.shape.rank != 0 or not bool(tf.math.is_finite(offset_tensor).numpy()):
        raise ValueError("offset must be a finite scalar")
    if bool((offset_tensor < 0.0).numpy()):
        raise ValueError("offset must be nonnegative")
    transformed = tf.math.log(tf.square(y) + offset_tensor)
    if not bool(tf.reduce_all(tf.math.is_finite(transformed)).numpy()):
        raise ValueError("transformed observations must be finite")
    return transformed


def transformed_sv_panel_observations(
    observations: tf.Tensor,
    *,
    offset: float | tf.Tensor = 1e-8,
) -> tf.Tensor:
    """Return coordinatewise ``log(y_t**2 + offset)`` for panel SV observations."""

    y = tf.convert_to_tensor(observations, dtype=tf.float64)
    if y.shape.rank == 1:
        y = y[:, tf.newaxis]
    if y.shape.rank != 2:
        raise ValueError("SV panel mixture transform requires [time, dim] observations")
    offset_tensor = tf.convert_to_tensor(offset, dtype=tf.float64)
    if offset_tensor.shape.rank == 0:
        offset_tensor = tf.fill([int(y.shape[1])], offset_tensor)
    if offset_tensor.shape.rank != 1 or int(offset_tensor.shape[0]) != int(y.shape[1]):
        raise ValueError("offset must be scalar or length observation_dim")
    if not bool(tf.reduce_all(tf.math.is_finite(offset_tensor)).numpy()):
        raise ValueError("offset must be finite")
    if not bool(tf.reduce_all(offset_tensor >= 0.0).numpy()):
        raise ValueError("offset must be nonnegative")
    transformed = tf.math.log(tf.square(y) + offset_tensor[tf.newaxis, :])
    if not bool(tf.reduce_all(tf.math.is_finite(transformed)).numpy()):
        raise ValueError("transformed observations must be finite")
    return transformed


def independent_panel_sv_mixture_kalman_filter(
    observations: tf.Tensor,
    *,
    gamma: float | tf.Tensor,
    beta: float | tf.Tensor,
    sigma: float | tf.Tensor,
    mixture: SVLogChiSquareGaussianMixture | None = None,
    transform_offset: float | tf.Tensor = 1e-8,
) -> SVPanelMixtureFilterResult:
    """Exact Kalman-mixture oracle for independent transformed-SV panels.

    This oracle is intended for tiny test fixtures.  It enumerates all
    ``K**dim`` observation-mixture component tuples at each time step.
    """

    mixture = mixture or ksc_1998_log_chi_square_mixture()
    z = transformed_sv_panel_observations(observations, offset=transform_offset)
    dim = int(z.shape[1])
    gamma_vector = _as_panel_parameter(gamma, dim, "gamma")
    beta_vector = _as_panel_parameter(beta, dim, "beta")
    sigma_vector = _as_panel_parameter(sigma, dim, "sigma")
    _validate_panel_parameters(gamma_vector, beta_vector, sigma_vector)
    component_tuples = _component_tuples(mixture.component_count, dim)
    mean = tf.zeros([dim], dtype=tf.float64)
    covariance = tf.linalg.diag(tf.square(sigma_vector) / (1.0 - tf.square(gamma_vector)))
    log_terms = []
    means = []
    covariances = []
    component_weights_by_time = []

    for time_index in range(int(z.shape[0])):
        if time_index > 0:
            transition_matrix = tf.linalg.diag(gamma_vector)
            mean = tf.linalg.matvec(transition_matrix, mean)
            covariance = _symmetrize(
                transition_matrix @ covariance @ tf.transpose(transition_matrix)
                + tf.linalg.diag(tf.square(sigma_vector))
            )
        component_log_weights = []
        component_means = []
        component_covariances = []
        for component_tuple in component_tuples:
            component_index = tf.constant(component_tuple, dtype=tf.int32)
            mixture_weight = tf.reduce_sum(tf.math.log(tf.gather(mixture.weights, component_index)))
            observation_offset = tf.math.log(tf.square(beta_vector)) + tf.gather(
                mixture.means,
                component_index,
            )
            observation_covariance = tf.linalg.diag(tf.gather(mixture.variances, component_index))
            log_increment, component_mean, component_covariance = _kalman_update_identity_observation(
                mean,
                covariance,
                z[time_index],
                observation_offset,
                observation_covariance,
            )
            component_log_weights.append(mixture_weight + log_increment)
            component_means.append(component_mean)
            component_covariances.append(component_covariance)
        log_normalizer, mean, covariance, normalized_weights = _collapse_gaussian_components(
            component_log_weights,
            component_means,
            component_covariances,
        )
        log_terms.append(log_normalizer)
        means.append(mean)
        covariances.append(covariance)
        component_weights_by_time.append(normalized_weights)

    return SVPanelMixtureFilterResult(
        log_likelihood=tf.reduce_sum(tf.stack(log_terms)),
        log_normalizers=tf.stack(log_terms),
        mean_path=tf.stack(means),
        covariance_path=tf.stack(covariances),
        component_weights=tf.stack(component_weights_by_time),
        diagnostics=MappingProxyType(
            {
                "backend": "kalman_independent_panel_transformed_sv_gaussian_mixture",
                "panel_dim": dim,
                "component_tuple_count": len(component_tuples),
                "component_tuples": tuple(component_tuples),
                "transform_offset": _manifest_value(transform_offset),
                "mixture": mixture.manifest_payload(),
                "target_scope": "independent_product_transformed_sv_panel_tiny_fixture",
                "non_claims": (
                    "not exact native SV likelihood",
                    "no KSC importance reweighting",
                    "no coupled multivariate SV claim",
                    "not scalable component enumeration",
                ),
            }
        ),
    )


def independent_panel_sv_mixture_cut4_filter(
    observations: tf.Tensor,
    *,
    gamma: float | tf.Tensor,
    beta: float | tf.Tensor,
    sigma: float | tf.Tensor,
    mixture: SVLogChiSquareGaussianMixture | None = None,
    transform_offset: float | tf.Tensor = 1e-8,
    innovation_floor: float = 1e-12,
) -> SVPanelMixtureFilterResult:
    """Component-enumerated CUT4 filter for independent transformed-SV panels."""

    mixture = mixture or ksc_1998_log_chi_square_mixture()
    z = transformed_sv_panel_observations(observations, offset=transform_offset)
    dim = int(z.shape[1])
    gamma_vector = _as_panel_parameter(gamma, dim, "gamma")
    beta_vector = _as_panel_parameter(beta, dim, "beta")
    sigma_vector = _as_panel_parameter(sigma, dim, "sigma")
    _validate_panel_parameters(gamma_vector, beta_vector, sigma_vector)
    component_tuples = _component_tuples(mixture.component_count, dim)
    mean = tf.zeros([dim], dtype=tf.float64)
    covariance = tf.linalg.diag(tf.square(sigma_vector) / (1.0 - tf.square(gamma_vector)))
    log_terms = []
    means = []
    covariances = []
    component_weights_by_time = []
    cut4_point_counts = []
    cut4_augmented_dims = []
    cut4_polynomial_degrees = []

    for time_index in range(int(z.shape[0])):
        component_log_weights = []
        component_means = []
        component_covariances = []
        component_point_counts = []
        for component_tuple in component_tuples:
            component_index = tf.constant(component_tuple, dtype=tf.int32)
            mixture_weight = tf.reduce_sum(tf.math.log(tf.gather(mixture.weights, component_index)))
            structural = _panel_transformed_sv_component_structural_model(
                current_mean=mean,
                current_covariance=covariance,
                gamma=gamma_vector,
                beta=beta_vector,
                sigma=sigma_vector,
                mixture_means=tf.gather(mixture.means, component_index),
                mixture_variances=tf.gather(mixture.variances, component_index),
                time_index=time_index,
            )
            cut4 = tf_svd_cut4_filter(
                z[time_index : time_index + 1],
                structural,
                innovation_floor=tf.constant(innovation_floor, dtype=tf.float64),
                return_filtered=True,
            )
            component_log_weights.append(mixture_weight + cut4.log_likelihood)
            component_means.append(cut4.filtered_means[0])
            component_covariances.append(cut4.filtered_covariances[0])
            point_count = int(cut4.diagnostics.extra["point_count"].numpy())
            component_point_counts.append(point_count)
            cut4_augmented_dims.append(int(cut4.diagnostics.extra["augmented_dim"].numpy()))
            cut4_polynomial_degrees.append(int(cut4.diagnostics.extra["polynomial_degree"].numpy()))
        log_normalizer, mean, covariance, normalized_weights = _collapse_gaussian_components(
            component_log_weights,
            component_means,
            component_covariances,
        )
        log_terms.append(log_normalizer)
        means.append(mean)
        covariances.append(covariance)
        component_weights_by_time.append(normalized_weights)
        cut4_point_counts.append(tuple(component_point_counts))

    return SVPanelMixtureFilterResult(
        log_likelihood=tf.reduce_sum(tf.stack(log_terms)),
        log_normalizers=tf.stack(log_terms),
        mean_path=tf.stack(means),
        covariance_path=tf.stack(covariances),
        component_weights=tf.stack(component_weights_by_time),
        diagnostics=MappingProxyType(
            {
                "backend": "cut4_independent_panel_transformed_sv_gaussian_mixture",
                "panel_dim": dim,
                "component_tuple_count": len(component_tuples),
                "component_tuples": tuple(component_tuples),
                "cut4_point_counts": tuple(cut4_point_counts),
                "max_cut4_point_count": max(max(row) for row in cut4_point_counts),
                "cut4_augmented_dims": tuple(cut4_augmented_dims),
                "cut4_polynomial_degrees": tuple(cut4_polynomial_degrees),
                "transform_offset": _manifest_value(transform_offset),
                "mixture": mixture.manifest_payload(),
                "target_scope": "independent_product_transformed_sv_panel_tiny_fixture",
                "non_claims": (
                    "not exact native SV likelihood",
                    "no KSC importance reweighting",
                    "no coupled multivariate SV claim",
                    "not scalable component enumeration",
                    "linear-Gaussian component fixtures do not validate nonlinear CUT4 accuracy",
                ),
            }
        ),
    )


def independent_panel_sv_mixture_fixed_sgqf_filter(
    observations: tf.Tensor,
    *,
    gamma: float | tf.Tensor,
    beta: float | tf.Tensor,
    sigma: float | tf.Tensor,
    mixture: SVLogChiSquareGaussianMixture | None = None,
    transform_offset: float | tf.Tensor = 1e-8,
    sparse_level: int = 2,
    cloud: TFFixedSGQFCloud | None = None,
    branch_config: TFFixedSGQFBranchConfig | None = None,
) -> SVPanelMixtureFilterResult:
    """Component-enumerated Fixed-SGQF filter for independent transformed-SV panels."""

    mixture = mixture or ksc_1998_log_chi_square_mixture()
    z = transformed_sv_panel_observations(observations, offset=transform_offset)
    dim = int(z.shape[1])
    gamma_vector = _as_panel_parameter(gamma, dim, "gamma")
    beta_vector = _as_panel_parameter(beta, dim, "beta")
    sigma_vector = _as_panel_parameter(sigma, dim, "sigma")
    _validate_panel_parameters(gamma_vector, beta_vector, sigma_vector)
    component_tuples = _component_tuples(mixture.component_count, dim)
    branch_config = branch_config or TFFixedSGQFBranchConfig(
        predictive_epsilon=1e-10,
        innovation_epsilon=1e-10,
    )
    cloud = cloud or tf_fixed_sgqf_cloud(dim=dim, sparse_level=sparse_level)
    branch_identity = branch_config.branch_identity(cloud)
    mean = tf.zeros([dim], dtype=tf.float64)
    covariance = tf.linalg.diag(tf.square(sigma_vector) / (1.0 - tf.square(gamma_vector)))
    log_terms = []
    means = []
    covariances = []
    component_weights_by_time = []

    for time_index in range(int(z.shape[0])):
        component_log_weights = []
        component_means = []
        component_covariances = []
        for component_tuple in component_tuples:
            component_index = tf.constant(component_tuple, dtype=tf.int32)
            mixture_weight = tf.reduce_sum(tf.math.log(tf.gather(mixture.weights, component_index)))
            component_result = _fixed_sgqf_component_update(
                observation=z[time_index],
                current_mean=mean,
                current_covariance=covariance,
                gamma=gamma_vector,
                beta=beta_vector,
                sigma=sigma_vector,
                mixture_means=tf.gather(mixture.means, component_index),
                mixture_variances=tf.gather(mixture.variances, component_index),
                time_index=time_index,
                cloud=cloud,
                branch_config=branch_config,
                branch_identity=branch_identity,
            )
            component_log_weights.append(mixture_weight + component_result.log_likelihood)
            component_means.append(component_result.filtered_means[0])
            component_covariances.append(component_result.filtered_covariances[0])
        log_normalizer, mean, covariance, normalized_weights = _collapse_gaussian_components(
            component_log_weights,
            component_means,
            component_covariances,
        )
        log_terms.append(log_normalizer)
        means.append(mean)
        covariances.append(covariance)
        component_weights_by_time.append(normalized_weights)

    return SVPanelMixtureFilterResult(
        log_likelihood=tf.reduce_sum(tf.stack(log_terms)),
        log_normalizers=tf.stack(log_terms),
        mean_path=tf.stack(means),
        covariance_path=tf.stack(covariances),
        component_weights=tf.stack(component_weights_by_time),
        diagnostics=MappingProxyType(
            {
                "backend": "fixed_sgqf_independent_panel_transformed_sv_gaussian_mixture",
                "panel_dim": dim,
                "component_tuple_count": len(component_tuples),
                "component_tuples": tuple(component_tuples),
                "fixed_sgqf_sparse_level": int(cloud.sparse_level),
                "fixed_sgqf_cloud_point_count": int(cloud.point_count),
                "fixed_sgqf_branch_hash": branch_identity.hash.value,
                "transform_offset": _manifest_value(transform_offset),
                "mixture": mixture.manifest_payload(),
                "target_scope": "independent_product_transformed_sv_panel_tiny_fixture",
                "non_claims": (
                    "not exact native SV likelihood",
                    "no KSC importance reweighting",
                    "no coupled multivariate SV claim",
                    "not scalable component enumeration",
                    "same-target SGQF evidence uses per-component Gaussian closure plus posterior collapse",
                ),
            }
        ),
    )


def independent_panel_sv_mixture_fixed_sgqf_score(
    observations: tf.Tensor,
    *,
    gamma: float | tf.Tensor,
    beta: float | tf.Tensor,
    sigma: float | tf.Tensor,
    mixture: SVLogChiSquareGaussianMixture | None = None,
    transform_offset: float | tf.Tensor = 1e-8,
    sparse_level: int = 2,
    cloud: TFFixedSGQFCloud | None = None,
    branch_config: TFFixedSGQFBranchConfig | None = None,
) -> SVPanelMixtureScoreResult:
    """Component-enumerated analytical Fixed-SGQF score for transformed-SV panels."""

    mixture = mixture or ksc_1998_log_chi_square_mixture()
    z = transformed_sv_panel_observations(observations, offset=transform_offset)
    dim = int(z.shape[1])
    gamma_vector = _as_panel_parameter(gamma, dim, "gamma")
    beta_vector = _as_panel_parameter(beta, dim, "beta")
    sigma_vector = _as_panel_parameter(sigma, dim, "sigma")
    _validate_panel_parameters(gamma_vector, beta_vector, sigma_vector)
    branch_config = branch_config or TFFixedSGQFBranchConfig(
        predictive_epsilon=1e-10,
        innovation_epsilon=1e-10,
    )
    cloud = cloud or tf_fixed_sgqf_cloud(dim=dim, sparse_level=sparse_level)
    branch_identity = branch_config.branch_identity(cloud)
    component_tuples = _component_tuples(mixture.component_count, dim)
    parameter_dim = 2 * dim

    mean = tf.zeros([dim], dtype=tf.float64)
    covariance = tf.linalg.diag(tf.square(sigma_vector) / (1.0 - tf.square(gamma_vector)))
    d_mean = tf.zeros([parameter_dim, dim], dtype=tf.float64)
    d_covariance = _gamma_seed_covariance_derivatives(gamma_vector, sigma_vector)

    log_terms = []
    score_terms = []
    means = []
    covariances = []
    d_means = []
    d_covariances = []

    for time_index in range(int(z.shape[0])):
        component_log_weights = []
        component_scores = []
        component_means = []
        component_covariances = []
        component_d_means = []
        component_d_covariances = []
        for component_tuple in component_tuples:
            component_index = tf.constant(component_tuple, dtype=tf.int32)
            mixture_weight = tf.reduce_sum(tf.math.log(tf.gather(mixture.weights, component_index)))
            component_result = _fixed_sgqf_component_score_update(
                observation=z[time_index],
                current_mean=mean,
                current_covariance=covariance,
                d_current_mean=d_mean,
                d_current_covariance=d_covariance,
                gamma=gamma_vector,
                beta=beta_vector,
                sigma=sigma_vector,
                mixture_means=tf.gather(mixture.means, component_index),
                mixture_variances=tf.gather(mixture.variances, component_index),
                time_index=time_index,
                cloud=cloud,
                branch_config=branch_config,
                branch_identity=branch_identity,
            )
            component_log_weights.append(mixture_weight + component_result.log_likelihood)
            component_scores.append(component_result.score)
            component_means.append(component_result.filtered_mean)
            component_covariances.append(component_result.filtered_covariance)
            component_d_means.append(component_result.d_filtered_mean)
            component_d_covariances.append(component_result.d_filtered_covariance)

        normalized_weights = tf.exp(tf.stack(component_log_weights) - tf.reduce_logsumexp(tf.stack(component_log_weights)))
        log_normalizer = tf.reduce_logsumexp(tf.stack(component_log_weights))
        score_increment = tf.reduce_sum(tf.stack(component_scores, axis=0) * normalized_weights[:, tf.newaxis], axis=0)
        mean, covariance, d_mean, d_covariance = _collapse_gaussian_components_with_derivatives(
            normalized_weights=normalized_weights,
            component_means=component_means,
            component_covariances=component_covariances,
            component_d_means=component_d_means,
            component_d_covariances=component_d_covariances,
            component_scores=component_scores,
        )
        log_terms.append(log_normalizer)
        score_terms.append(score_increment)
        means.append(mean)
        covariances.append(covariance)
        d_means.append(d_mean)
        d_covariances.append(d_covariance)

    return SVPanelMixtureScoreResult(
        log_likelihood=tf.reduce_sum(tf.stack(log_terms)),
        score=tf.reduce_sum(tf.stack(score_terms), axis=0),
        mean_path=tf.stack(means),
        covariance_path=tf.stack(covariances),
        d_mean_path=tf.stack(d_means),
        d_covariance_path=tf.stack(d_covariances),
        diagnostics=MappingProxyType(
            {
                "backend": "fixed_sgqf_independent_panel_transformed_sv_gaussian_mixture_score",
                "panel_dim": dim,
                "component_tuple_count": len(component_tuples),
                "component_tuples": tuple(component_tuples),
                "fixed_sgqf_sparse_level": int(cloud.sparse_level),
                "fixed_sgqf_cloud_point_count": int(cloud.point_count),
                "fixed_sgqf_branch_hash": branch_identity.hash.value,
                "wrapper_score_contract": "analytic_component_score_logsumexp_aggregation",
                "transform_offset": _manifest_value(transform_offset),
                "mixture": mixture.manifest_payload(),
                "target_scope": "independent_product_transformed_sv_panel_tiny_fixture",
                "non_claims": (
                    "not exact native SV likelihood",
                    "no KSC importance reweighting",
                    "no coupled multivariate SV claim",
                    "not scalable component enumeration",
                ),
            }
        ),
    )


def independent_panel_sv_mixture_ukf_filter(
    observations: tf.Tensor,
    *,
    gamma: float | tf.Tensor,
    beta: float | tf.Tensor,
    sigma: float | tf.Tensor,
    mixture: SVLogChiSquareGaussianMixture | None = None,
    transform_offset: float | tf.Tensor = 1e-8,
) -> SVPanelMixtureFilterResult:
    """Component-enumerated SVD-UKF filter for independent transformed-SV panels."""

    mixture = mixture or ksc_1998_log_chi_square_mixture()
    z = transformed_sv_panel_observations(observations, offset=transform_offset)
    dim = int(z.shape[1])
    gamma_vector = _as_panel_parameter(gamma, dim, "gamma")
    beta_vector = _as_panel_parameter(beta, dim, "beta")
    sigma_vector = _as_panel_parameter(sigma, dim, "sigma")
    _validate_panel_parameters(gamma_vector, beta_vector, sigma_vector)
    component_tuples = _component_tuples(mixture.component_count, dim)
    mean = tf.zeros([dim], dtype=tf.float64)
    covariance = tf.linalg.diag(tf.square(sigma_vector) / (1.0 - tf.square(gamma_vector)))
    log_terms = []
    means = []
    covariances = []
    component_weights_by_time = []

    for time_index in range(int(z.shape[0])):
        component_log_weights = []
        component_means = []
        component_covariances = []
        for component_tuple in component_tuples:
            component_index = tf.constant(component_tuple, dtype=tf.int32)
            mixture_weight = tf.reduce_sum(tf.math.log(tf.gather(mixture.weights, component_index)))
            structural = _panel_transformed_sv_component_structural_model(
                current_mean=mean,
                current_covariance=covariance,
                gamma=gamma_vector,
                beta=beta_vector,
                sigma=sigma_vector,
                mixture_means=tf.gather(mixture.means, component_index),
                mixture_variances=tf.gather(mixture.variances, component_index),
                time_index=time_index,
            )
            ukf = tf_svd_sigma_point_filter(
                z[time_index : time_index + 1],
                structural,
                backend="tf_svd_ukf",
                innovation_floor=tf.constant(1e-12, dtype=tf.float64),
                return_filtered=True,
            )
            component_log_weights.append(mixture_weight + ukf.log_likelihood)
            component_means.append(ukf.filtered_means[0])
            component_covariances.append(ukf.filtered_covariances[0])
        log_normalizer, mean, covariance, normalized_weights = _collapse_gaussian_components(
            component_log_weights,
            component_means,
            component_covariances,
        )
        log_terms.append(log_normalizer)
        means.append(mean)
        covariances.append(covariance)
        component_weights_by_time.append(normalized_weights)

    return SVPanelMixtureFilterResult(
        log_likelihood=tf.reduce_sum(tf.stack(log_terms)),
        log_normalizers=tf.stack(log_terms),
        mean_path=tf.stack(means),
        covariance_path=tf.stack(covariances),
        component_weights=tf.stack(component_weights_by_time),
        diagnostics=MappingProxyType(
            {
                "backend": "ukf_independent_panel_transformed_sv_gaussian_mixture",
                "panel_dim": dim,
                "component_tuple_count": len(component_tuples),
                "component_tuples": tuple(component_tuples),
                "transform_offset": _manifest_value(transform_offset),
                "mixture": mixture.manifest_payload(),
                "target_scope": "independent_product_transformed_sv_panel_tiny_fixture",
                "non_claims": (
                    "not exact native SV likelihood",
                    "no KSC importance reweighting",
                    "no coupled multivariate SV claim",
                    "not scalable component enumeration",
                ),
            }
        ),
    )


def independent_panel_sv_mixture_ukf_score(
    observations: tf.Tensor,
    *,
    gamma: float | tf.Tensor,
    beta: float | tf.Tensor,
    sigma: float | tf.Tensor,
    mixture: SVLogChiSquareGaussianMixture | None = None,
    transform_offset: float | tf.Tensor = 1e-8,
) -> SVPanelMixtureScoreResult:
    """Component-enumerated analytical SVD-UKF score for transformed-SV panels."""

    mixture = mixture or ksc_1998_log_chi_square_mixture()
    z = transformed_sv_panel_observations(observations, offset=transform_offset)
    dim = int(z.shape[1])
    gamma_vector = _as_panel_parameter(gamma, dim, "gamma")
    beta_vector = _as_panel_parameter(beta, dim, "beta")
    sigma_vector = _as_panel_parameter(sigma, dim, "sigma")
    _validate_panel_parameters(gamma_vector, beta_vector, sigma_vector)
    component_tuples = _component_tuples(mixture.component_count, dim)
    parameter_dim = 2 * dim

    mean = tf.zeros([dim], dtype=tf.float64)
    covariance = tf.linalg.diag(tf.square(sigma_vector) / (1.0 - tf.square(gamma_vector)))
    d_mean = tf.zeros([parameter_dim, dim], dtype=tf.float64)
    d_covariance = _gamma_seed_covariance_derivatives(gamma_vector, sigma_vector)

    log_terms = []
    score_terms = []
    means = []
    covariances = []
    d_means = []
    d_covariances = []

    for time_index in range(int(z.shape[0])):
        component_log_weights = []
        component_scores = []
        component_means = []
        component_covariances = []
        component_d_means = []
        component_d_covariances = []
        for component_tuple in component_tuples:
            component_index = tf.constant(component_tuple, dtype=tf.int32)
            mixture_weight = tf.reduce_sum(tf.math.log(tf.gather(mixture.weights, component_index)))
            component_result = _ukf_component_score_update(
                observation=z[time_index],
                current_mean=mean,
                current_covariance=covariance,
                d_current_mean=d_mean,
                d_current_covariance=d_covariance,
                gamma=gamma_vector,
                beta=beta_vector,
                sigma=sigma_vector,
                mixture_means=tf.gather(mixture.means, component_index),
                mixture_variances=tf.gather(mixture.variances, component_index),
                time_index=time_index,
            )
            component_log_weights.append(mixture_weight + component_result.log_likelihood)
            component_scores.append(component_result.score)
            component_means.append(component_result.trace[0]["filtered_mean"])
            component_covariances.append(component_result.trace[0]["filtered_covariance"])
            component_d_means.append(component_result.trace[0]["d_filtered_mean"])
            component_d_covariances.append(component_result.trace[0]["d_filtered_covariance"])

        normalized_weights = tf.exp(tf.stack(component_log_weights) - tf.reduce_logsumexp(tf.stack(component_log_weights)))
        log_normalizer = tf.reduce_logsumexp(tf.stack(component_log_weights))
        score_increment = tf.reduce_sum(tf.stack(component_scores, axis=0) * normalized_weights[:, tf.newaxis], axis=0)
        mean, covariance, d_mean, d_covariance = _collapse_gaussian_components_with_derivatives(
            normalized_weights=normalized_weights,
            component_means=component_means,
            component_covariances=component_covariances,
            component_d_means=component_d_means,
            component_d_covariances=component_d_covariances,
            component_scores=component_scores,
        )
        log_terms.append(log_normalizer)
        score_terms.append(score_increment)
        means.append(mean)
        covariances.append(covariance)
        d_means.append(d_mean)
        d_covariances.append(d_covariance)

    diagnostics = TFFilterDiagnostics(
        backend="ukf_independent_panel_transformed_sv_gaussian_mixture_score",
        mask_convention="none",
        regularization=TFRegularizationDiagnostics(
            branch_label="svd_sigma_point_analytic_score",
            derivative_target="implemented_regularized_law",
        ),
        extra={
            "panel_dim": dim,
            "component_tuple_count": len(component_tuples),
            "component_tuples": tuple(component_tuples),
            "wrapper_score_contract": "analytic_component_score_logsumexp_aggregation",
            "transform_offset": _manifest_value(transform_offset),
            "mixture": mixture.manifest_payload(),
            "target_scope": "independent_product_transformed_sv_panel_tiny_fixture",
        },
    )
    return SVPanelMixtureScoreResult(
        log_likelihood=tf.reduce_sum(tf.stack(log_terms)),
        score=tf.reduce_sum(tf.stack(score_terms), axis=0),
        mean_path=tf.stack(means),
        covariance_path=tf.stack(covariances),
        d_mean_path=tf.stack(d_means),
        d_covariance_path=tf.stack(d_covariances),
        diagnostics=diagnostics.as_dict(),
    )


def _as_panel_parameter(value: float | tf.Tensor, dim: int, name: str) -> tf.Tensor:
    tensor = tf.convert_to_tensor(value, dtype=tf.float64)
    if tensor.shape.rank == 0:
        tensor = tf.fill([int(dim)], tensor)
    if tensor.shape.rank != 1 or int(tensor.shape[0]) != int(dim):
        raise ValueError(f"{name} must be scalar or length panel_dim")
    if not bool(tf.reduce_all(tf.math.is_finite(tensor)).numpy()):
        raise ValueError(f"{name} must be finite")
    return tensor


def _as_row_matrix(values: tf.Tensor, width: int, name: str) -> tf.Tensor:
    tensor = tf.convert_to_tensor(values, dtype=tf.float64)
    if tensor.shape.rank == 1:
        tensor = tensor[:, tf.newaxis]
    if tensor.shape.rank != 2 or int(tensor.shape[1]) != int(width):
        raise ValueError(f"{name} must have shape [n, {int(width)}]")
    if not bool(tf.reduce_all(tf.math.is_finite(tensor)).numpy()):
        raise ValueError(f"{name} must be finite")
    return tensor


def _validate_panel_parameters(gamma: tf.Tensor, beta: tf.Tensor, sigma: tf.Tensor) -> None:
    if not bool(tf.reduce_all(tf.abs(gamma) < 1.0).numpy()):
        raise ValueError("gamma entries must have absolute value less than one")
    if not bool(tf.reduce_all(beta > 0.0).numpy()):
        raise ValueError("beta entries must be positive")
    if not bool(tf.reduce_all(sigma > 0.0).numpy()):
        raise ValueError("sigma entries must be positive")


def _component_tuples(component_count: int, dim: int) -> tuple[tuple[int, ...], ...]:
    return tuple(product(range(int(component_count)), repeat=int(dim)))


def _manifest_value(value: float | tf.Tensor) -> float | tuple[float, ...]:
    tensor = tf.convert_to_tensor(value, dtype=tf.float64)
    if tensor.shape.rank == 0:
        return float(tensor.numpy())
    if tensor.shape.rank == 1:
        return tuple(float(entry) for entry in tensor.numpy())
    raise ValueError("manifest values must be scalar or one-dimensional")


def _symmetrize(matrix: tf.Tensor) -> tf.Tensor:
    matrix = tf.convert_to_tensor(matrix, dtype=tf.float64)
    return 0.5 * (matrix + tf.linalg.matrix_transpose(matrix))


def _mvn_zero_log_prob(value: tf.Tensor, covariance: tf.Tensor) -> tf.Tensor:
    value = tf.convert_to_tensor(value, dtype=tf.float64)
    covariance = _symmetrize(covariance)
    chol = tf.linalg.cholesky(covariance)
    solve = tf.linalg.cholesky_solve(chol, value[:, tf.newaxis])[:, 0]
    mahalanobis = tf.reduce_sum(value * solve)
    log_det = 2.0 * tf.reduce_sum(tf.math.log(tf.linalg.diag_part(chol)))
    dim = tf.cast(tf.shape(value)[0], tf.float64)
    return -0.5 * (
        dim * tf.math.log(tf.constant(2.0 * math.pi, dtype=tf.float64))
        + log_det
        + mahalanobis
    )


def _kalman_update_identity_observation(
    mean: tf.Tensor,
    covariance: tf.Tensor,
    observation: tf.Tensor,
    observation_offset: tf.Tensor,
    observation_covariance: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    mean = tf.convert_to_tensor(mean, dtype=tf.float64)
    covariance = _symmetrize(covariance)
    observation = tf.convert_to_tensor(observation, dtype=tf.float64)
    observation_offset = tf.convert_to_tensor(observation_offset, dtype=tf.float64)
    observation_covariance = _symmetrize(observation_covariance)
    innovation = observation - observation_offset - mean
    innovation_covariance = _symmetrize(covariance + observation_covariance)
    log_increment = _mvn_zero_log_prob(innovation, innovation_covariance)
    chol = tf.linalg.cholesky(innovation_covariance)
    innovation_precision = tf.linalg.cholesky_solve(
        chol,
        tf.eye(int(mean.shape[0]), dtype=tf.float64),
    )
    kalman_gain = covariance @ innovation_precision
    updated_mean = mean + tf.linalg.matvec(kalman_gain, innovation)
    identity = tf.eye(int(mean.shape[0]), dtype=tf.float64)
    left = identity - kalman_gain
    updated_covariance = _symmetrize(
        left @ covariance @ tf.transpose(left)
        + kalman_gain @ observation_covariance @ tf.transpose(kalman_gain)
    )
    return log_increment, updated_mean, updated_covariance


def _collapse_gaussian_components(
    component_log_weights: list[tf.Tensor],
    component_means: list[tf.Tensor],
    component_covariances: list[tf.Tensor],
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    log_weights = tf.stack(component_log_weights)
    log_normalizer = tf.reduce_logsumexp(log_weights)
    normalized_weights = tf.exp(log_weights - log_normalizer)
    stacked_means = tf.stack(component_means, axis=0)
    stacked_covariances = tf.stack(component_covariances, axis=0)
    mean = tf.reduce_sum(stacked_means * normalized_weights[:, tf.newaxis], axis=0)
    centered = stacked_means - mean[tf.newaxis, :]
    covariance = tf.reduce_sum(
        normalized_weights[:, tf.newaxis, tf.newaxis]
        * (
            stacked_covariances
            + centered[:, :, tf.newaxis] * centered[:, tf.newaxis, :]
        ),
        axis=0,
    )
    return log_normalizer, mean, _symmetrize(covariance), normalized_weights


def _panel_transformed_sv_component_structural_model(
    *,
    current_mean: tf.Tensor,
    current_covariance: tf.Tensor,
    gamma: tf.Tensor,
    beta: tf.Tensor,
    sigma: tf.Tensor,
    mixture_means: tf.Tensor,
    mixture_variances: tf.Tensor,
    time_index: int,
):
    dim = int(current_mean.shape[0])
    process_dim = dim
    padding_dim = max(0, 3 - (dim + process_dim))
    innovation_dim = process_dim + padding_dim
    partition = StatePartition(
        state_names=tuple(f"x{index}" for index in range(dim)),
        stochastic_indices=tuple(range(dim)),
        deterministic_indices=(),
        innovation_dim=innovation_dim,
    )
    if int(time_index) == 0:
        transition_matrix = tf.eye(dim, dtype=tf.float64)
        innovation_matrix = tf.zeros([dim, innovation_dim], dtype=tf.float64)
        innovation_covariance = tf.eye(innovation_dim, dtype=tf.float64)
    else:
        transition_matrix = tf.linalg.diag(gamma)
        innovation_matrix = tf.concat(
            [
                tf.eye(dim, dtype=tf.float64),
                tf.zeros([dim, padding_dim], dtype=tf.float64),
            ],
            axis=1,
        )
        innovation_variances = tf.concat(
            [
                tf.square(sigma),
                tf.ones([padding_dim], dtype=tf.float64),
            ],
            axis=0,
        )
        innovation_covariance = tf.linalg.diag(innovation_variances)
    return make_affine_structural_tf(
        partition=partition,
        initial_mean=tf.reshape(current_mean, [dim]),
        initial_covariance=tf.reshape(current_covariance, [dim, dim]),
        transition_offset=tf.zeros([dim], dtype=tf.float64),
        transition_matrix=transition_matrix,
        innovation_matrix=innovation_matrix,
        innovation_covariance=innovation_covariance,
        observation_offset=tf.math.log(tf.square(beta)) + mixture_means,
        observation_matrix=tf.eye(dim, dtype=tf.float64),
        observation_covariance=tf.linalg.diag(mixture_variances),
        config=StructuralFilterConfig(
            integration_space="innovation",
            deterministic_completion="none",
            approximation_label="p40_independent_panel_transformed_sv_mixture_cut4_component",
        ),
        name="p40_independent_panel_transformed_sv_mixture_cut4_component",
    )


def _panel_transformed_sv_component_fixed_sgqf_model(
    *,
    current_mean: tf.Tensor,
    current_covariance: tf.Tensor,
    gamma: tf.Tensor,
    sigma: tf.Tensor,
    mixture_variances: tf.Tensor,
    time_index: int,
) -> TFFixedSGQFAffineModel:
    dim = int(current_mean.shape[0])
    if int(time_index) == 0:
        transition_matrix = tf.eye(dim, dtype=tf.float64)
        process_covariance = tf.zeros([dim, dim], dtype=tf.float64)
    else:
        transition_matrix = tf.linalg.diag(gamma)
        process_covariance = tf.linalg.diag(tf.square(sigma))
    return TFFixedSGQFAffineModel(
        initial_mean=tf.reshape(current_mean, [dim]),
        initial_covariance=tf.reshape(current_covariance, [dim, dim]),
        transition_matrix=transition_matrix,
        process_covariance=process_covariance,
        observation_matrix=tf.eye(dim, dtype=tf.float64),
        observation_covariance=tf.linalg.diag(mixture_variances),
        name="p47_independent_panel_transformed_sv_mixture_fixed_sgqf_component",
    )


def _fixed_sgqf_component_update(
    *,
    observation: tf.Tensor,
    current_mean: tf.Tensor,
    current_covariance: tf.Tensor,
    gamma: tf.Tensor,
    beta: tf.Tensor,
    sigma: tf.Tensor,
    mixture_means: tf.Tensor,
    mixture_variances: tf.Tensor,
    time_index: int,
    cloud: TFFixedSGQFCloud,
    branch_config: TFFixedSGQFBranchConfig,
    branch_identity,
):
    model = _panel_transformed_sv_component_fixed_sgqf_model(
        current_mean=current_mean,
        current_covariance=current_covariance,
        gamma=gamma,
        sigma=sigma,
        mixture_variances=mixture_variances,
        time_index=time_index,
    )
    centered_observation = tf.reshape(
        tf.convert_to_tensor(observation, dtype=tf.float64)
        - (tf.math.log(tf.square(beta)) + tf.convert_to_tensor(mixture_means, dtype=tf.float64)),
        [1, -1],
    )
    result = tf_fixed_sgqf_filter(
        centered_observation,
        model,
        cloud=cloud,
        branch_config=branch_config,
        branch_identity=branch_identity,
        return_filtered=True,
    )
    if result.failure is not None:
        tuple_failure = result.failure
        raise ValueError(
            "fixed_sgqf_component_failure"
            f": stage={tuple_failure.stage}, time_index={tuple_failure.time_index}, reason={tuple_failure.reason}"
        )
    return result


def _panel_transformed_sv_component_fixed_sgqf_derivatives(
    *,
    current_mean: tf.Tensor,
    current_covariance: tf.Tensor,
    d_current_mean: tf.Tensor,
    d_current_covariance: tf.Tensor,
    gamma: tf.Tensor,
    sigma: tf.Tensor,
    time_index: int,
) -> TFFixedSGQFDerivatives:
    del current_mean, current_covariance
    dim = int(gamma.shape[0])
    parameter_dim = 2 * dim
    d_process_covariance = tf.zeros([parameter_dim, dim, dim], dtype=tf.float64)
    d_observation_covariance = tf.zeros([parameter_dim, dim, dim], dtype=tf.float64)
    if int(time_index) == 0:
        transition_matrix = tf.eye(dim, dtype=tf.float64)
        d_transition_matrix = tf.zeros([parameter_dim, dim, dim], dtype=tf.float64)
    else:
        transition_matrix = tf.linalg.diag(gamma)
        d_transition_matrix = tf.zeros([parameter_dim, dim, dim], dtype=tf.float64)
        for axis in range(dim):
            row = 2 * axis
            d_transition_matrix = tf.tensor_scatter_nd_update(
                d_transition_matrix,
                indices=[[row, axis, axis]],
                updates=[1.0 - tf.square(gamma[axis])],
            )
    transition_state_jacobian_fn = lambda points: tf.broadcast_to(
        transition_matrix[tf.newaxis, :, :],
        [tf.shape(tf.convert_to_tensor(points, dtype=tf.float64))[0], dim, dim],
    )
    d_transition_fn = lambda points: tf.einsum(
        "pij,rj->pri",
        d_transition_matrix,
        tf.convert_to_tensor(points, dtype=tf.float64),
    )
    observation_state_jacobian_fn = lambda points: tf.broadcast_to(
        tf.eye(dim, dtype=tf.float64)[tf.newaxis, :, :],
        [tf.shape(tf.convert_to_tensor(points, dtype=tf.float64))[0], dim, dim],
    )
    d_observation_fn = lambda points: tf.zeros(
        [parameter_dim, tf.shape(tf.convert_to_tensor(points, dtype=tf.float64))[0], dim],
        dtype=tf.float64,
    )
    return TFFixedSGQFDerivatives(
        d_initial_mean=d_current_mean,
        d_initial_covariance=d_current_covariance,
        d_process_covariance=d_process_covariance,
        d_observation_covariance=d_observation_covariance,
        transition_state_jacobian_fn=transition_state_jacobian_fn,
        d_transition_fn=d_transition_fn,
        observation_state_jacobian_fn=observation_state_jacobian_fn,
        d_observation_fn=d_observation_fn,
        name="ksc_mixture_fixed_sgqf_component_derivatives",
    )


def _fixed_sgqf_component_score_update(
    *,
    observation: tf.Tensor,
    current_mean: tf.Tensor,
    current_covariance: tf.Tensor,
    d_current_mean: tf.Tensor,
    d_current_covariance: tf.Tensor,
    gamma: tf.Tensor,
    beta: tf.Tensor,
    sigma: tf.Tensor,
    mixture_means: tf.Tensor,
    mixture_variances: tf.Tensor,
    time_index: int,
    cloud: TFFixedSGQFCloud,
    branch_config: TFFixedSGQFBranchConfig,
    branch_identity,
):
    model = _panel_transformed_sv_component_fixed_sgqf_model(
        current_mean=current_mean,
        current_covariance=current_covariance,
        gamma=gamma,
        sigma=sigma,
        mixture_variances=mixture_variances,
        time_index=time_index,
    )
    derivatives = _panel_transformed_sv_component_fixed_sgqf_derivatives(
        current_mean=current_mean,
        current_covariance=current_covariance,
        d_current_mean=d_current_mean,
        d_current_covariance=d_current_covariance,
        gamma=gamma,
        sigma=sigma,
        time_index=time_index,
    )
    centered_observation = tf.reshape(
        tf.convert_to_tensor(observation, dtype=tf.float64)
        - (tf.math.log(tf.square(beta)) + tf.convert_to_tensor(mixture_means, dtype=tf.float64)),
        [1, -1],
    )
    result = tf_fixed_sgqf_score(
        centered_observation,
        model,
        derivatives,
        cloud=cloud,
        branch_config=branch_config,
        branch_identity=branch_identity,
        expected_branch_identity=branch_identity,
    )
    if result.failure is not None:
        tuple_failure = result.failure
        raise ValueError(
            "fixed_sgqf_component_score_failure"
            f": stage={tuple_failure.stage}, time_index={tuple_failure.time_index}, reason={tuple_failure.reason}"
        )
    beta_offset_score = tf.concat(
        [
            tf.zeros([int(gamma.shape[0])], dtype=tf.float64),
            tf.fill([int(gamma.shape[0])], tf.constant(2.0, dtype=tf.float64)),
        ],
        axis=0,
    )
    return TFFixedSGQFScoreResult(
        log_likelihood=result.log_likelihood,
        score=result.score + beta_offset_score,
        branch_identity=result.branch_identity,
        diagnostics=result.diagnostics,
        filtered_mean=result.filtered_mean,
        filtered_covariance=result.filtered_covariance,
        d_filtered_mean=result.d_filtered_mean,
        d_filtered_covariance=result.d_filtered_covariance,
        failure=result.failure,
    )


def _gamma_seed_covariance_derivatives(gamma: tf.Tensor, sigma: tf.Tensor) -> tf.Tensor:
    dim = int(gamma.shape[0])
    parameter_dim = 2 * dim
    d_covariance = tf.zeros([parameter_dim, dim, dim], dtype=tf.float64)
    for axis in range(dim):
        cov_derivative = 2.0 * tf.square(sigma[axis]) * gamma[axis] / tf.square(1.0 - tf.square(gamma[axis]))
        d_covariance = tf.tensor_scatter_nd_update(
            d_covariance,
            indices=[[2 * axis, axis, axis]],
            updates=[cov_derivative],
        )
    return d_covariance


def _physical_theta_jacobian(gamma: tf.Tensor, beta: tf.Tensor) -> tf.Tensor:
    del beta
    dim = int(gamma.shape[0])
    jacobian = tf.zeros([2 * dim, 2 * dim], dtype=tf.float64)
    for axis in range(dim):
        gamma_derivative = _STD_NORMAL.prob(_STD_NORMAL.quantile(gamma[axis]))
        jacobian = tf.tensor_scatter_nd_update(
            jacobian,
            indices=[[2 * axis, 2 * axis], [2 * axis + 1, 2 * axis + 1]],
            updates=[gamma_derivative, tf.constant(1.0, dtype=tf.float64)],
        )
    return jacobian


def _affine_observation_offset_theta_derivatives(beta: tf.Tensor) -> tf.Tensor:
    dim = int(beta.shape[0])
    parameter_dim = 2 * dim
    derivatives = tf.zeros([parameter_dim, dim], dtype=tf.float64)
    for axis in range(dim):
        derivatives = tf.tensor_scatter_nd_update(
            derivatives,
            indices=[[2 * axis + 1, axis]],
            updates=[tf.constant(2.0, dtype=tf.float64)],
        )
    return derivatives


def _collapse_gaussian_components_with_derivatives(
    *,
    normalized_weights: tf.Tensor,
    component_means: list[tf.Tensor],
    component_covariances: list[tf.Tensor],
    component_d_means: list[tf.Tensor],
    component_d_covariances: list[tf.Tensor],
    component_scores: list[tf.Tensor],
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    stacked_means = tf.stack(component_means, axis=0)
    stacked_covariances = tf.stack(component_covariances, axis=0)
    stacked_d_means = tf.stack(component_d_means, axis=0)
    stacked_d_covariances = tf.stack(component_d_covariances, axis=0)
    stacked_scores = tf.stack(component_scores, axis=0)
    mean = tf.reduce_sum(stacked_means * normalized_weights[:, tf.newaxis], axis=0)
    covariance = tf.reduce_sum(
        normalized_weights[:, tf.newaxis, tf.newaxis]
        * (
            stacked_covariances
            + (stacked_means - mean[tf.newaxis, :])[:, :, tf.newaxis]
            * (stacked_means - mean[tf.newaxis, :])[:, tf.newaxis, :]
        ),
        axis=0,
    )
    weighted_score = tf.reduce_sum(stacked_scores * normalized_weights[:, tf.newaxis], axis=0)
    d_mean = tf.reduce_sum(
        normalized_weights[:, tf.newaxis, tf.newaxis]
        * (
            stacked_d_means
            + stacked_scores[:, :, tf.newaxis] * stacked_means[:, tf.newaxis, :]
        ),
        axis=0,
    ) - weighted_score[:, tf.newaxis] * mean[tf.newaxis, :]
    centered = stacked_means - mean[tf.newaxis, :]
    d_covariance = tf.reduce_sum(
        normalized_weights[:, tf.newaxis, tf.newaxis, tf.newaxis]
        * (
            stacked_d_covariances
            + centered[:, tf.newaxis, :, tf.newaxis]
            * (stacked_d_means - d_mean[tf.newaxis, :, :])[:, :, tf.newaxis, :]
            + (stacked_d_means - d_mean[tf.newaxis, :, :])[:, :, :, tf.newaxis]
            * centered[:, tf.newaxis, tf.newaxis, :]
            + stacked_scores[:, :, tf.newaxis, tf.newaxis]
            * (
                stacked_covariances[:, tf.newaxis, :, :]
                + centered[:, tf.newaxis, :, tf.newaxis] * centered[:, tf.newaxis, tf.newaxis, :]
            )
        ),
        axis=0,
    ) - weighted_score[:, tf.newaxis, tf.newaxis] * covariance[tf.newaxis, :, :]
    return mean, _symmetrize(covariance), d_mean, _symmetrize(d_covariance)


def _panel_transformed_sv_component_structural_derivatives(
    *,
    current_mean: tf.Tensor,
    current_covariance: tf.Tensor,
    d_current_mean: tf.Tensor,
    d_current_covariance: tf.Tensor,
    gamma: tf.Tensor,
    beta: tf.Tensor,
    sigma: tf.Tensor,
    mixture_means: tf.Tensor,
    mixture_variances: tf.Tensor,
    time_index: int,
) -> TFStructuralFirstDerivatives:
    del current_mean, current_covariance, mixture_means, mixture_variances
    dim = int(gamma.shape[0])
    parameter_dim = 2 * dim
    process_dim = dim
    padding_dim = max(0, 3 - (dim + process_dim))
    innovation_dim = process_dim + padding_dim
    d_initial_mean = d_current_mean
    d_initial_covariance = d_current_covariance
    if int(time_index) == 0:
        transition_matrix = tf.eye(dim, dtype=tf.float64)
        d_transition_matrix = tf.zeros([parameter_dim, dim, dim], dtype=tf.float64)
        innovation_matrix = tf.zeros([dim, innovation_dim], dtype=tf.float64)
        d_innovation_covariance = tf.zeros([parameter_dim, innovation_dim, innovation_dim], dtype=tf.float64)
    else:
        transition_matrix = tf.linalg.diag(gamma)
        d_transition_matrix = tf.zeros([parameter_dim, dim, dim], dtype=tf.float64)
        for axis in range(dim):
            d_transition_matrix = tf.tensor_scatter_nd_update(
                d_transition_matrix,
                indices=[[2 * axis, axis, axis]],
                updates=[1.0 - tf.square(gamma[axis])],
            )
        innovation_matrix = tf.concat(
            [
                tf.eye(dim, dtype=tf.float64),
                tf.zeros([dim, padding_dim], dtype=tf.float64),
            ],
            axis=1,
        )
        d_innovation_covariance = tf.zeros([parameter_dim, innovation_dim, innovation_dim], dtype=tf.float64)
    d_observation_covariance = tf.zeros([parameter_dim, dim, dim], dtype=tf.float64)
    d_observation_offset = _affine_observation_offset_theta_derivatives(beta)
    observation_matrix = tf.eye(dim, dtype=tf.float64)

    def transition_state_jacobian_fn(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        del innovation
        point_count = tf.shape(tf.convert_to_tensor(previous_state, dtype=tf.float64))[0]
        return tf.broadcast_to(transition_matrix[tf.newaxis, :, :], [point_count, dim, dim])

    def transition_innovation_jacobian_fn(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        del innovation
        point_count = tf.shape(tf.convert_to_tensor(previous_state, dtype=tf.float64))[0]
        return tf.broadcast_to(innovation_matrix[tf.newaxis, :, :], [point_count, dim, innovation_dim])

    def d_transition_fn(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        del innovation
        return tf.einsum("pij,rj->pri", d_transition_matrix, tf.convert_to_tensor(previous_state, dtype=tf.float64))

    def observation_state_jacobian_fn(state_points: tf.Tensor) -> tf.Tensor:
        point_count = tf.shape(tf.convert_to_tensor(state_points, dtype=tf.float64))[0]
        return tf.broadcast_to(observation_matrix[tf.newaxis, :, :], [point_count, dim, dim])

    def d_observation_fn(state_points: tf.Tensor) -> tf.Tensor:
        point_count = tf.shape(tf.convert_to_tensor(state_points, dtype=tf.float64))[0]
        return tf.broadcast_to(d_observation_offset[:, tf.newaxis, :], [parameter_dim, point_count, dim])

    return TFStructuralFirstDerivatives(
        d_initial_mean=d_initial_mean,
        d_initial_covariance=d_initial_covariance,
        d_innovation_covariance=d_innovation_covariance,
        d_observation_covariance=d_observation_covariance,
        transition_state_jacobian_fn=transition_state_jacobian_fn,
        transition_innovation_jacobian_fn=transition_innovation_jacobian_fn,
        d_transition_fn=d_transition_fn,
        observation_state_jacobian_fn=observation_state_jacobian_fn,
        d_observation_fn=d_observation_fn,
        name="ksc_mixture_structural_component_derivatives",
    )


def _ukf_component_score_update(
    *,
    observation: tf.Tensor,
    current_mean: tf.Tensor,
    current_covariance: tf.Tensor,
    d_current_mean: tf.Tensor,
    d_current_covariance: tf.Tensor,
    gamma: tf.Tensor,
    beta: tf.Tensor,
    sigma: tf.Tensor,
    mixture_means: tf.Tensor,
    mixture_variances: tf.Tensor,
    time_index: int,
):
    structural = _panel_transformed_sv_component_structural_model(
        current_mean=current_mean,
        current_covariance=current_covariance,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        mixture_means=tf.gather(tf.convert_to_tensor(mixture_means, dtype=tf.float64), tf.range(int(current_mean.shape[0]))),
        mixture_variances=mixture_variances,
        time_index=time_index,
    )
    derivatives = _panel_transformed_sv_component_structural_derivatives(
        current_mean=current_mean,
        current_covariance=current_covariance,
        d_current_mean=d_current_mean,
        d_current_covariance=d_current_covariance,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        mixture_means=mixture_means,
        mixture_variances=mixture_variances,
        time_index=time_index,
    )
    return tf_svd_ukf_score(
        tf.reshape(tf.convert_to_tensor(observation, dtype=tf.float64), [1, -1]),
        structural,
        derivatives,
        innovation_floor=tf.constant(1e-12, dtype=tf.float64),
        spectral_gap_tolerance=tf.constant(1e-8, dtype=tf.float64),
        allow_fixed_null_support=True,
    )


def scalar_sv_mixture_dense_reference(
    model: StochasticVolatilitySSM,
    theta: tf.Tensor,
    observations: tf.Tensor,
    *,
    mixture: SVLogChiSquareGaussianMixture | None = None,
    order: int = 321,
    radius: float = 8.0,
    transform_offset: float = 1e-8,
) -> SVMixtureCut4Result:
    """Sequential dense-grid reference for the transformed mixture-SV model."""

    mixture = mixture or ksc_1998_log_chi_square_mixture()
    z = transformed_sv_observations(observations, offset=transform_offset)
    x_grid, weights = _legendre_interval_nodes_weights(order=order, left=-radius, right=radius)
    parameters = model.physical_parameters(theta)
    gamma = parameters["gamma"]
    beta = parameters["beta"]
    sigma = parameters["sigma"]
    prior_scale = sigma / tf.sqrt(1.0 - tf.square(gamma))
    log_density = _normal_log_prob(x_grid, tf.constant(0.0, dtype=tf.float64), prior_scale)
    log_terms = []
    means = []
    variances = []
    component_weights_by_time = []

    for time_index in range(int(z.shape[0])):
        if time_index > 0:
            previous_density = tf.exp(log_density - log_terms[-1])
            transition_log = _normal_log_prob(
                x_grid[:, tf.newaxis],
                gamma * x_grid[tf.newaxis, :],
                sigma,
            )
            predictive = tf.reduce_sum(
                weights[tf.newaxis, :] * previous_density[tf.newaxis, :] * tf.exp(transition_log),
                axis=1,
            )
            log_density = tf.math.log(predictive)
        component_log_densities = []
        component_integrals = []
        for component in range(mixture.component_count):
            loc = tf.math.log(tf.square(beta)) + x_grid + mixture.means[component]
            observation_log = _normal_log_prob(
                z[time_index, 0],
                loc,
                tf.sqrt(mixture.variances[component]),
            )
            component_log = log_density + observation_log
            component_log_densities.append(component_log)
            component_integrals.append(
                tf.math.log(mixture.weights[component])
                + _logsumexp_weighted(component_log, weights)
            )
        component_integrals_tensor = tf.stack(component_integrals)
        log_normalizer = tf.reduce_logsumexp(component_integrals_tensor)
        normalized_component_weights = tf.exp(component_integrals_tensor - log_normalizer)
        stacked_component_log = tf.stack(component_log_densities, axis=0)
        log_density = tf.reduce_logsumexp(
            tf.math.log(mixture.weights)[:, tf.newaxis] + stacked_component_log,
            axis=0,
        )
        normalized_density = tf.exp(log_density - log_normalizer)
        mean = tf.reduce_sum(weights * x_grid * normalized_density)
        second = tf.reduce_sum(weights * tf.square(x_grid) * normalized_density)
        log_terms.append(log_normalizer)
        means.append(mean)
        variances.append(second - tf.square(mean))
        component_weights_by_time.append(normalized_component_weights)

    return SVMixtureCut4Result(
        log_likelihood=tf.reduce_sum(tf.stack(log_terms)),
        log_normalizers=tf.stack(log_terms),
        mean_path=tf.stack(means),
        variance_path=tf.stack(variances),
        component_weights=tf.stack(component_weights_by_time),
        diagnostics=MappingProxyType(
            {
                "backend": "dense_transformed_sv_gaussian_mixture",
                "grid_order": int(order),
                "radius": float(radius),
                "transform_offset": float(transform_offset),
                "mixture": mixture.manifest_payload(),
                "non_claims": (
                    "not exact native SV likelihood",
                    "no KSC importance reweighting",
                    "no paper-scale validation",
                ),
            }
        ),
    )


def scalar_sv_mixture_cut4_filter(
    model: StochasticVolatilitySSM,
    theta: tf.Tensor,
    observations: tf.Tensor,
    *,
    mixture: SVLogChiSquareGaussianMixture | None = None,
    transform_offset: float = 1e-8,
    innovation_floor: float = 1e-12,
) -> SVMixtureCut4Result:
    """Component-wise CUT4 recursion for transformed scalar SV mixture observations."""

    mixture = mixture or ksc_1998_log_chi_square_mixture()
    z = transformed_sv_observations(observations, offset=transform_offset)
    parameters = model.physical_parameters(theta)
    gamma = parameters["gamma"]
    beta = parameters["beta"]
    sigma = parameters["sigma"]
    mean = tf.constant([0.0], dtype=tf.float64)
    covariance = tf.reshape(tf.square(sigma) / (1.0 - tf.square(gamma)), [1, 1])
    log_terms = []
    means = []
    variances = []
    component_weights_by_time = []
    cut4_point_counts = []
    cut4_augmented_dims = []
    cut4_polynomial_degrees = []

    for time_index in range(int(z.shape[0])):
        component_log_weights = []
        component_means = []
        component_covariances = []
        component_point_counts = []
        for component in range(mixture.component_count):
            structural = _transformed_sv_component_structural_model(
                predictive_mean=mean,
                predictive_covariance=covariance,
                gamma=gamma,
                sigma=sigma,
                beta=beta,
                mixture_mean=mixture.means[component],
                mixture_variance=mixture.variances[component],
                time_index=time_index,
            )
            cut4 = tf_svd_cut4_filter(
                z[time_index : time_index + 1],
                structural,
                innovation_floor=tf.constant(innovation_floor, dtype=tf.float64),
                return_filtered=True,
            )
            component_log_weights.append(tf.math.log(mixture.weights[component]) + cut4.log_likelihood)
            component_means.append(cut4.filtered_means[0])
            component_covariances.append(cut4.filtered_covariances[0])
            point_count = int(cut4.diagnostics.extra["point_count"].numpy())
            component_point_counts.append(point_count)
            cut4_augmented_dims.append(int(cut4.diagnostics.extra["augmented_dim"].numpy()))
            cut4_polynomial_degrees.append(int(cut4.diagnostics.extra["polynomial_degree"].numpy()))
        component_log_weights_tensor = tf.stack(component_log_weights)
        log_normalizer = tf.reduce_logsumexp(component_log_weights_tensor)
        normalized_component_weights = tf.exp(component_log_weights_tensor - log_normalizer)
        stacked_means = tf.stack(component_means, axis=0)
        stacked_covariances = tf.stack(component_covariances, axis=0)
        mean = tf.linalg.matvec(tf.transpose(stacked_means), normalized_component_weights)
        second = tf.reduce_sum(
            normalized_component_weights
            * (tf.reshape(stacked_covariances[:, 0, 0], [-1]) + tf.square(stacked_means[:, 0]))
        )
        variance = second - tf.square(mean[0])
        covariance = tf.reshape(variance, [1, 1])
        log_terms.append(log_normalizer)
        means.append(mean[0])
        variances.append(variance)
        component_weights_by_time.append(normalized_component_weights)
        cut4_point_counts.append(tuple(component_point_counts))

    return SVMixtureCut4Result(
        log_likelihood=tf.reduce_sum(tf.stack(log_terms)),
        log_normalizers=tf.stack(log_terms),
        mean_path=tf.stack(means),
        variance_path=tf.stack(variances),
        component_weights=tf.stack(component_weights_by_time),
        diagnostics=MappingProxyType(
            {
                "backend": "cut4_transformed_sv_gaussian_mixture",
                "cut4_point_counts": tuple(cut4_point_counts),
                "max_cut4_point_count": max(max(row) for row in cut4_point_counts),
                "cut4_augmented_dims": tuple(cut4_augmented_dims),
                "cut4_polynomial_degrees": tuple(cut4_polynomial_degrees),
                "cut4_padding": "one inert innovation coordinate because CUT4-G implementation requires augmented dim >= 3",
                "transform_offset": float(transform_offset),
                "mixture": mixture.manifest_payload(),
                "non_claims": (
                    "not exact native SV likelihood",
                    "no KSC importance reweighting",
                    "no paper-scale validation",
                    "no derivative claim",
                ),
            }
        ),
    )


def _transformed_sv_component_structural_model(
    *,
    predictive_mean: tf.Tensor,
    predictive_covariance: tf.Tensor,
    gamma: tf.Tensor,
    sigma: tf.Tensor,
    beta: tf.Tensor,
    mixture_mean: tf.Tensor,
    mixture_variance: tf.Tensor,
    time_index: int,
):
    partition = StatePartition(
        state_names=("x",),
        stochastic_indices=(0,),
        deterministic_indices=(),
        innovation_dim=2,
    )
    if int(time_index) == 0:
        transition_matrix = tf.eye(1, dtype=tf.float64)
        innovation_matrix = tf.zeros([1, 2], dtype=tf.float64)
        innovation_covariance = tf.eye(2, dtype=tf.float64)
    else:
        transition_matrix = tf.reshape(gamma, [1, 1])
        innovation_matrix = tf.constant([[1.0, 0.0]], dtype=tf.float64)
        innovation_covariance = tf.linalg.diag(tf.stack([tf.square(sigma), tf.constant(1.0, dtype=tf.float64)]))
    return make_affine_structural_tf(
        partition=partition,
        initial_mean=tf.reshape(predictive_mean, [1]),
        initial_covariance=tf.reshape(predictive_covariance, [1, 1]),
        transition_offset=tf.zeros([1], dtype=tf.float64),
        transition_matrix=transition_matrix,
        innovation_matrix=innovation_matrix,
        innovation_covariance=innovation_covariance,
        observation_offset=tf.reshape(tf.math.log(tf.square(beta)) + mixture_mean, [1]),
        observation_matrix=tf.ones([1, 1], dtype=tf.float64),
        observation_covariance=tf.reshape(mixture_variance, [1, 1]),
        config=StructuralFilterConfig(
            integration_space="innovation",
            deterministic_completion="none",
            approximation_label="p39_transformed_sv_gaussian_mixture_cut4_component",
        ),
        name="p39_transformed_sv_gaussian_mixture_cut4_component",
    )


def _normal_log_prob(value: tf.Tensor, loc: tf.Tensor, scale: tf.Tensor) -> tf.Tensor:
    return -0.5 * tf.square((value - loc) / scale) - tf.math.log(scale) - 0.5 * tf.math.log(
        tf.constant(2.0 * math.pi, dtype=tf.float64)
    )


def _legendre_interval_nodes_weights(
    *,
    order: int,
    left: float,
    right: float,
) -> tuple[tf.Tensor, tf.Tensor]:
    nodes, weights = _legendre_gauss_nodes_weights(int(order))
    half_length = tf.constant(0.5 * (right - left), dtype=tf.float64)
    midpoint = tf.constant(0.5 * (right + left), dtype=tf.float64)
    return midpoint + half_length * nodes, half_length * weights


def _legendre_gauss_nodes_weights(order: int) -> tuple[tf.Tensor, tf.Tensor]:
    import numpy as np

    nodes, weights = np.polynomial.legendre.leggauss(int(order))
    return tf.constant(nodes, dtype=tf.float64), tf.constant(weights, dtype=tf.float64)


def _logsumexp_weighted(log_values: tf.Tensor, weights: tf.Tensor) -> tf.Tensor:
    max_log = tf.reduce_max(log_values)
    return tf.math.log(tf.reduce_sum(weights * tf.exp(log_values - max_log))) + max_log
