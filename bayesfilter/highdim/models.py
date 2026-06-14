"""Small TensorFlow state-space model contracts for highdim value gates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol

import tensorflow as tf
import tensorflow_probability as tfp

from bayesfilter.highdim.diagnostics import HighDimStatus, assert_tf_float64


class TFHighDimStateSpaceModel(Protocol):
    """TensorFlow log-density protocol for high-dimensional value paths."""

    def parameter_dim(self) -> int:
        """Return static parameter dimension."""

    def state_dim(self) -> int:
        """Return static state dimension."""

    def observation_dim(self) -> int:
        """Return static observation dimension."""

    def initial_log_density(self, theta: tf.Tensor, x0: tf.Tensor) -> tf.Tensor:
        """Return initial log density for rows of ``x0``."""

    def transition_log_density(
        self,
        theta: tf.Tensor,
        x_prev: tf.Tensor,
        x_next: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        """Return transition log density for rows of ``x_prev,x_next``."""

    def observation_log_density(
        self,
        theta: tf.Tensor,
        x_t: tf.Tensor,
        y_t: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        """Return observation log density for rows of ``x_t``."""

    def manifest_payload(self) -> Mapping[str, object]:
        """Return deterministic model manifest fields."""


@dataclass(frozen=True)
class LinearGaussianSSM:
    """Time-invariant linear Gaussian state-space model for Phase-4 gates."""

    initial_mean: tf.Tensor
    initial_covariance: tf.Tensor
    transition_matrix: tf.Tensor
    transition_covariance: tf.Tensor
    observation_matrix: tf.Tensor
    observation_covariance: tf.Tensor
    transition_offset: tf.Tensor | None = None
    observation_offset: tf.Tensor | None = None

    def __post_init__(self) -> None:
        initial_mean = tf.convert_to_tensor(self.initial_mean, dtype=tf.float64)
        initial_covariance = tf.convert_to_tensor(self.initial_covariance, dtype=tf.float64)
        transition_matrix = tf.convert_to_tensor(self.transition_matrix, dtype=tf.float64)
        transition_covariance = tf.convert_to_tensor(self.transition_covariance, dtype=tf.float64)
        observation_matrix = tf.convert_to_tensor(self.observation_matrix, dtype=tf.float64)
        observation_covariance = tf.convert_to_tensor(self.observation_covariance, dtype=tf.float64)
        for name, value in (
            ("initial_mean", initial_mean),
            ("initial_covariance", initial_covariance),
            ("transition_matrix", transition_matrix),
            ("transition_covariance", transition_covariance),
            ("observation_matrix", observation_matrix),
            ("observation_covariance", observation_covariance),
        ):
            assert_tf_float64(name, value)
            if not bool(tf.reduce_all(tf.math.is_finite(value)).numpy()):
                raise ValueError(f"{name}: {HighDimStatus.NONFINITE_VALUE.value}")
        if initial_mean.shape.rank != 1:
            raise ValueError(f"initial_mean: {HighDimStatus.INVALID_SHAPE.value}")
        state_dim = int(initial_mean.shape[0])
        if initial_covariance.shape != (state_dim, state_dim):
            raise ValueError(f"initial_covariance: {HighDimStatus.INVALID_SHAPE.value}")
        if transition_matrix.shape != (state_dim, state_dim):
            raise ValueError(f"transition_matrix: {HighDimStatus.INVALID_SHAPE.value}")
        if transition_covariance.shape != (state_dim, state_dim):
            raise ValueError(f"transition_covariance: {HighDimStatus.INVALID_SHAPE.value}")
        if observation_matrix.shape.rank != 2 or observation_matrix.shape[1] != state_dim:
            raise ValueError(f"observation_matrix: {HighDimStatus.INVALID_SHAPE.value}")
        obs_dim = int(observation_matrix.shape[0])
        if observation_covariance.shape != (obs_dim, obs_dim):
            raise ValueError(f"observation_covariance: {HighDimStatus.INVALID_SHAPE.value}")
        transition_offset = (
            tf.zeros([state_dim], dtype=tf.float64)
            if self.transition_offset is None
            else tf.convert_to_tensor(self.transition_offset, dtype=tf.float64)
        )
        observation_offset = (
            tf.zeros([obs_dim], dtype=tf.float64)
            if self.observation_offset is None
            else tf.convert_to_tensor(self.observation_offset, dtype=tf.float64)
        )
        if transition_offset.shape != (state_dim,):
            raise ValueError(f"transition_offset: {HighDimStatus.INVALID_SHAPE.value}")
        if observation_offset.shape != (obs_dim,):
            raise ValueError(f"observation_offset: {HighDimStatus.INVALID_SHAPE.value}")
        object.__setattr__(self, "initial_mean", initial_mean)
        object.__setattr__(self, "initial_covariance", _symmetrize(initial_covariance))
        object.__setattr__(self, "transition_matrix", transition_matrix)
        object.__setattr__(self, "transition_covariance", _symmetrize(transition_covariance))
        object.__setattr__(self, "observation_matrix", observation_matrix)
        object.__setattr__(self, "observation_covariance", _symmetrize(observation_covariance))
        object.__setattr__(self, "transition_offset", transition_offset)
        object.__setattr__(self, "observation_offset", observation_offset)

    def parameter_dim(self) -> int:
        return 0

    def state_dim(self) -> int:
        return int(self.initial_mean.shape[0])

    def observation_dim(self) -> int:
        return int(self.observation_matrix.shape[0])

    def initial_log_density(self, theta: tf.Tensor, x0: tf.Tensor) -> tf.Tensor:
        del theta
        values = _as_row_matrix(x0, self.state_dim(), "x0")
        return _mvn_log_prob(values, self.initial_mean, self.initial_covariance)

    def transition_log_density(
        self,
        theta: tf.Tensor,
        x_prev: tf.Tensor,
        x_next: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del theta, t
        previous = _as_row_matrix(x_prev, self.state_dim(), "x_prev")
        next_values = _as_row_matrix(x_next, self.state_dim(), "x_next")
        loc = self.transition_offset[tf.newaxis, :] + tf.linalg.matmul(
            previous,
            self.transition_matrix,
            transpose_b=True,
        )
        return _mvn_log_prob(next_values, loc, self.transition_covariance)

    def observation_log_density(
        self,
        theta: tf.Tensor,
        x_t: tf.Tensor,
        y_t: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del theta, t
        values = _as_row_matrix(x_t, self.state_dim(), "x_t")
        observation = tf.reshape(tf.convert_to_tensor(y_t, dtype=tf.float64), [self.observation_dim()])
        loc = self.observation_offset[tf.newaxis, :] + tf.linalg.matmul(
            values,
            self.observation_matrix,
            transpose_b=True,
        )
        return _mvn_log_prob(
            tf.broadcast_to(observation, tf.shape(loc)),
            loc,
            self.observation_covariance,
        )

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "LinearGaussianSSM",
            "initial_mean": self.initial_mean,
            "initial_covariance": self.initial_covariance,
            "transition_matrix": self.transition_matrix,
            "transition_covariance": self.transition_covariance,
            "transition_offset": self.transition_offset,
            "observation_matrix": self.observation_matrix,
            "observation_covariance": self.observation_covariance,
            "observation_offset": self.observation_offset,
        }


@dataclass(frozen=True)
class StochasticVolatilitySSM:
    """P30 synthetic stochastic-volatility model with transformed parameters.

    The model expects synthetic transformed coordinates
    ``theta'=(Phi^{-1}(gamma), log(beta))`` and keeps ``X'_t=X_t``.  This is the
    fixed-``sigma`` convention in P30 equation ``eq:p27-sv5a``.
    """

    sigma: float | tf.Tensor = 1.0
    parameterization: str = "synthetic_unconstrained"

    def __post_init__(self) -> None:
        sigma = tf.convert_to_tensor(self.sigma, dtype=tf.float64)
        if sigma.shape.rank != 0:
            raise ValueError(f"sigma: {HighDimStatus.INVALID_SHAPE.value}")
        if not bool(tf.math.is_finite(sigma).numpy()) or bool((sigma <= 0.0).numpy()):
            raise ValueError(f"sigma: {HighDimStatus.NONFINITE_VALUE.value}")
        if self.parameterization != "synthetic_unconstrained":
            raise ValueError("StochasticVolatilitySSM currently supports synthetic_unconstrained")
        object.__setattr__(self, "sigma", sigma)

    def parameter_dim(self) -> int:
        return 2

    def state_dim(self) -> int:
        return 1

    def observation_dim(self) -> int:
        return 1

    def physical_parameters(self, theta: tf.Tensor) -> Mapping[str, tf.Tensor]:
        theta_vector = _as_parameter_vector(theta, self.parameter_dim(), "theta")
        standard_normal = _standard_normal()
        gamma = standard_normal.cdf(theta_vector[0])
        beta = tf.exp(theta_vector[1])
        return {"gamma": gamma, "beta": beta, "sigma": self.sigma}

    def unconstrained_from_physical(self, gamma: float | tf.Tensor, beta: float | tf.Tensor) -> tf.Tensor:
        gamma_tensor = tf.convert_to_tensor(gamma, dtype=tf.float64)
        beta_tensor = tf.convert_to_tensor(beta, dtype=tf.float64)
        if gamma_tensor.shape.rank != 0 or beta_tensor.shape.rank != 0:
            raise ValueError(f"physical parameter: {HighDimStatus.INVALID_SHAPE.value}")
        if not bool(
            tf.math.is_finite(gamma_tensor).numpy()
            and tf.math.is_finite(beta_tensor).numpy()
            and (gamma_tensor > 0.0).numpy()
            and (gamma_tensor < 1.0).numpy()
            and (beta_tensor > 0.0).numpy()
        ):
            raise ValueError(f"physical parameter: {HighDimStatus.NONFINITE_VALUE.value}")
        standard_normal = _standard_normal()
        return tf.stack([standard_normal.quantile(gamma_tensor), tf.math.log(beta_tensor)])

    def initial_log_density(self, theta: tf.Tensor, x0: tf.Tensor) -> tf.Tensor:
        values = _as_row_matrix(x0, self.state_dim(), "x0")
        parameters = self.physical_parameters(theta)
        gamma = parameters["gamma"]
        stationary_variance = tf.square(self.sigma) / (1.0 - tf.square(gamma))
        distribution = tfp.distributions.Normal(
            loc=tf.constant(0.0, dtype=tf.float64),
            scale=tf.sqrt(stationary_variance),
        )
        return distribution.log_prob(values[:, 0])

    def transition_log_density(
        self,
        theta: tf.Tensor,
        x_prev: tf.Tensor,
        x_next: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del t
        previous = _as_row_matrix(x_prev, self.state_dim(), "x_prev")
        next_values = _as_row_matrix(x_next, self.state_dim(), "x_next")
        parameters = self.physical_parameters(theta)
        distribution = tfp.distributions.Normal(
            loc=parameters["gamma"] * previous[:, 0],
            scale=self.sigma,
        )
        return distribution.log_prob(next_values[:, 0])

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
        scale = parameters["beta"] * tf.exp(0.5 * values[:, 0])
        distribution = tfp.distributions.Normal(
            loc=tf.zeros_like(scale, dtype=tf.float64),
            scale=scale,
        )
        return distribution.log_prob(tf.broadcast_to(observation[0], tf.shape(scale)))

    def simulate(
        self,
        theta: tf.Tensor,
        final_time: int,
        seed: int,
    ) -> tuple[tf.Tensor, tf.Tensor]:
        """Generate ``x_0:x_T`` and ``y_0:y_T`` for a fixed integer seed."""

        if int(final_time) < 0:
            raise ValueError("final_time must be nonnegative")
        parameters = self.physical_parameters(theta)
        gamma = parameters["gamma"]
        beta = parameters["beta"]
        generator = tf.random.Generator.from_seed(int(seed))
        initial_scale = self.sigma / tf.sqrt(1.0 - tf.square(gamma))
        x_values = [initial_scale * generator.normal([], dtype=tf.float64)]
        y_values = [beta * tf.exp(0.5 * x_values[0]) * generator.normal([], dtype=tf.float64)]
        for _time_index in range(1, int(final_time) + 1):
            next_x = gamma * x_values[-1] + self.sigma * generator.normal([], dtype=tf.float64)
            x_values.append(next_x)
            y_values.append(beta * tf.exp(0.5 * next_x) * generator.normal([], dtype=tf.float64))
        return tf.reshape(tf.stack(x_values), [-1, 1]), tf.reshape(tf.stack(y_values), [-1, 1])

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "StochasticVolatilitySSM",
            "sigma": self.sigma,
            "parameterization": self.parameterization,
            "parameter_transform": "theta_prime=(Phi^{-1}(gamma), log(beta)); X_prime_t=X_t",
            "source_equations": ("eq:p27-sv1", "eq:p27-sv2", "eq:p27-sv3", "eq:p27-sv5a"),
            "dimension_convention": "synthetic row includes x_0:x_T; joint dimension is 2+(T+1)",
        }


@dataclass(frozen=True)
class SpatialSIRSSM:
    """P30 spatial SIR model contract for the M3 first gate.

    The state stores only susceptible and infectious coordinates,
    ``(S_1,I_1,...,S_J,I_J)``.  Removed populations are bookkeeping variables in
    P30 and are not part of the BayesFilter first-gate state vector.
    """

    kappa: tf.Tensor
    nu: tf.Tensor
    initial_mean: tf.Tensor
    neighbor_sets: tuple[tuple[int, ...], ...]
    delta: float | tf.Tensor = 0.02
    rk4_internal_step: float | tf.Tensor = 0.005
    process_covariance: tf.Tensor | None = None
    observation_covariance: tf.Tensor | None = None
    initial_covariance: tf.Tensor | None = None
    domain_policy: str = "diagnose_negative_after_noise"
    rk4_variant: str = "classical"
    process_noise_policy: str = "diagnose_negative_after_noise"

    def __post_init__(self) -> None:
        kappa = tf.convert_to_tensor(self.kappa, dtype=tf.float64)
        nu = tf.convert_to_tensor(self.nu, dtype=tf.float64)
        initial_mean = tf.convert_to_tensor(self.initial_mean, dtype=tf.float64)
        delta = tf.convert_to_tensor(self.delta, dtype=tf.float64)
        rk4_internal_step = tf.convert_to_tensor(self.rk4_internal_step, dtype=tf.float64)
        if kappa.shape.rank != 1 or nu.shape != kappa.shape:
            raise ValueError(f"SIR parameters: {HighDimStatus.INVALID_SHAPE.value}")
        compartments = int(kappa.shape[0])
        state_dim = 2 * compartments
        if initial_mean.shape != (state_dim,):
            raise ValueError(f"initial_mean: {HighDimStatus.INVALID_SHAPE.value}")
        if delta.shape.rank != 0 or rk4_internal_step.shape.rank != 0:
            raise ValueError(f"time step: {HighDimStatus.INVALID_SHAPE.value}")
        if not bool(
            tf.reduce_all(tf.math.is_finite(kappa)).numpy()
            and tf.reduce_all(tf.math.is_finite(nu)).numpy()
            and tf.reduce_all(tf.math.is_finite(initial_mean)).numpy()
            and tf.math.is_finite(delta).numpy()
            and tf.math.is_finite(rk4_internal_step).numpy()
            and (tf.reduce_all(kappa > 0.0)).numpy()
            and (tf.reduce_all(nu > 0.0)).numpy()
            and (delta > 0.0).numpy()
            and (rk4_internal_step > 0.0).numpy()
        ):
            raise ValueError(f"SIR parameters: {HighDimStatus.NONFINITE_VALUE.value}")
        ratio = delta / rk4_internal_step
        substeps = int(tf.round(ratio).numpy())
        if substeps <= 0 or abs(float((ratio - tf.cast(substeps, tf.float64)).numpy())) > 1e-12:
            raise ValueError("delta must be an integer multiple of rk4_internal_step")
        neighbor_sets = _normalize_neighbor_sets(self.neighbor_sets, compartments)
        process_covariance = (
            tf.eye(state_dim, dtype=tf.float64)
            if self.process_covariance is None
            else tf.convert_to_tensor(self.process_covariance, dtype=tf.float64)
        )
        observation_covariance = (
            100.0 * tf.eye(compartments, dtype=tf.float64)
            if self.observation_covariance is None
            else tf.convert_to_tensor(self.observation_covariance, dtype=tf.float64)
        )
        initial_covariance = (
            tf.eye(state_dim, dtype=tf.float64)
            if self.initial_covariance is None
            else tf.convert_to_tensor(self.initial_covariance, dtype=tf.float64)
        )
        if process_covariance.shape != (state_dim, state_dim):
            raise ValueError(f"process_covariance: {HighDimStatus.INVALID_SHAPE.value}")
        if observation_covariance.shape != (compartments, compartments):
            raise ValueError(f"observation_covariance: {HighDimStatus.INVALID_SHAPE.value}")
        if initial_covariance.shape != (state_dim, state_dim):
            raise ValueError(f"initial_covariance: {HighDimStatus.INVALID_SHAPE.value}")
        for name, value in (
            ("process_covariance", process_covariance),
            ("observation_covariance", observation_covariance),
            ("initial_covariance", initial_covariance),
        ):
            if not bool(tf.reduce_all(tf.math.is_finite(value)).numpy()):
                raise ValueError(f"{name}: {HighDimStatus.NONFINITE_VALUE.value}")
        if self.domain_policy != "diagnose_negative_after_noise":
            raise ValueError("SpatialSIRSSM first gate requires diagnose_negative_after_noise")
        if self.rk4_variant not in ("classical", "zhao_cui_sir_step"):
            raise ValueError("rk4_variant must be classical or zhao_cui_sir_step")
        if self.process_noise_policy not in (
            "diagnose_negative_after_noise",
            "clip_susceptible_after_noise",
        ):
            raise ValueError(
                "process_noise_policy must be diagnose_negative_after_noise "
                "or clip_susceptible_after_noise"
            )
        object.__setattr__(self, "kappa", kappa)
        object.__setattr__(self, "nu", nu)
        object.__setattr__(self, "initial_mean", initial_mean)
        object.__setattr__(self, "neighbor_sets", neighbor_sets)
        object.__setattr__(self, "delta", delta)
        object.__setattr__(self, "rk4_internal_step", rk4_internal_step)
        object.__setattr__(self, "process_covariance", _symmetrize(process_covariance))
        object.__setattr__(self, "observation_covariance", _symmetrize(observation_covariance))
        object.__setattr__(self, "initial_covariance", _symmetrize(initial_covariance))
        object.__setattr__(self, "_adjacency_matrix", _neighbor_adjacency_matrix(neighbor_sets))
        object.__setattr__(self, "_neighbor_degree", tf.reduce_sum(self._adjacency_matrix, axis=1))
        object.__setattr__(self, "_rk4_substeps", substeps)

    def parameter_dim(self) -> int:
        return 0

    def state_dim(self) -> int:
        return 2 * int(self.kappa.shape[0])

    def observation_dim(self) -> int:
        return int(self.kappa.shape[0])

    def observed_state_indices(self) -> tuple[int, ...]:
        return tuple(2 * index + 1 for index in range(self.observation_dim()))

    def unobserved_state_indices(self) -> tuple[int, ...]:
        return tuple(2 * index for index in range(self.observation_dim()))

    def initial_log_density(self, theta: tf.Tensor, x0: tf.Tensor) -> tf.Tensor:
        del theta
        values = _as_row_matrix(x0, self.state_dim(), "x0")
        return _mvn_log_prob(values, self.initial_mean, self.initial_covariance)

    def transition_mean(self, x_prev: tf.Tensor) -> tf.Tensor:
        """Return the deterministic RK4 mean in P30 equation ``eq:p27-sir6``."""

        state = _as_row_matrix(x_prev, self.state_dim(), "x_prev")
        step = self.delta / tf.cast(self._rk4_substeps, tf.float64)
        for _ in range(int(self._rk4_substeps)):
            state = self._rk4_step(state, step)
        return state

    def transition_log_density(
        self,
        theta: tf.Tensor,
        x_prev: tf.Tensor,
        x_next: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del theta, t
        previous = _as_row_matrix(x_prev, self.state_dim(), "x_prev")
        next_values = _as_row_matrix(x_next, self.state_dim(), "x_next")
        return _mvn_log_prob(next_values, self.transition_mean(previous), self.process_covariance)

    def transition_push_from_standard_normal(
        self,
        theta: tf.Tensor,
        x_prev: tf.Tensor,
        standard_normal_noise: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        """Push states with declared process-noise policy for source parity tests."""

        del theta, t
        previous = _as_row_matrix(x_prev, self.state_dim(), "x_prev")
        noise = _as_row_matrix(standard_normal_noise, self.state_dim(), "standard_normal_noise")
        mean = self.transition_mean(previous)
        process_chol = tf.linalg.cholesky(self.process_covariance)
        pushed = mean + tf.linalg.matmul(noise, process_chol, transpose_b=True)
        return self._apply_process_noise_policy(pushed)

    def observation_log_density(
        self,
        theta: tf.Tensor,
        x_t: tf.Tensor,
        y_t: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del theta, t
        values = _as_row_matrix(x_t, self.state_dim(), "x_t")
        observation = tf.reshape(tf.convert_to_tensor(y_t, dtype=tf.float64), [self.observation_dim()])
        infectious = self.infectious_components(values)
        return _mvn_log_prob(
            tf.broadcast_to(observation, tf.shape(infectious)),
            infectious,
            self.observation_covariance,
        )

    def susceptible_components(self, x_t: tf.Tensor) -> tf.Tensor:
        return _as_row_matrix(x_t, self.state_dim(), "x_t")[:, 0::2]

    def infectious_components(self, x_t: tf.Tensor) -> tf.Tensor:
        return _as_row_matrix(x_t, self.state_dim(), "x_t")[:, 1::2]

    def simulate(
        self,
        final_time: int,
        seed: int,
    ) -> tuple[tf.Tensor, tf.Tensor]:
        """Generate ``x_0:x_T`` and ``y_0:y_T`` without positivity projection."""

        if int(final_time) < 0:
            raise ValueError("final_time must be nonnegative")
        generator = tf.random.Generator.from_seed(int(seed))
        initial_chol = tf.linalg.cholesky(self.initial_covariance)
        process_chol = tf.linalg.cholesky(self.process_covariance)
        observation_chol = tf.linalg.cholesky(self.observation_covariance)
        state = self.initial_mean + tf.linalg.matvec(
            initial_chol,
            generator.normal([self.state_dim()], dtype=tf.float64),
        )
        states = [state]
        observations = [
            self.infectious_components(state)[0]
            + tf.linalg.matvec(
                observation_chol,
                generator.normal([self.observation_dim()], dtype=tf.float64),
            )
        ]
        for _time_index in range(1, int(final_time) + 1):
            mean = self.transition_mean(state)[0]
            state = mean + tf.linalg.matvec(
                process_chol,
                generator.normal([self.state_dim()], dtype=tf.float64),
            )
            state = self._apply_process_noise_policy(state[tf.newaxis, :])[0]
            states.append(state)
            observations.append(
                self.infectious_components(state)[0]
                + tf.linalg.matvec(
                    observation_chol,
                    generator.normal([self.observation_dim()], dtype=tf.float64),
                )
            )
        return tf.stack(states), tf.stack(observations)

    def observed_unobserved_rmse(
        self,
        truth_path: tf.Tensor,
        estimate_path: tf.Tensor,
    ) -> Mapping[str, tf.Tensor]:
        truth = _as_path_matrix(truth_path, self.state_dim(), "truth_path")
        estimate = _as_path_matrix(estimate_path, self.state_dim(), "estimate_path")
        if truth.shape != estimate.shape:
            raise ValueError(f"estimate_path: {HighDimStatus.INVALID_SHAPE.value}")
        observed = tf.gather(truth - estimate, self.observed_state_indices(), axis=1)
        unobserved = tf.gather(truth - estimate, self.unobserved_state_indices(), axis=1)
        return {
            "rmse_observed": tf.sqrt(tf.reduce_mean(tf.square(observed))),
            "rmse_unobserved": tf.sqrt(tf.reduce_mean(tf.square(unobserved))),
        }

    def domain_diagnostics(self, path: tf.Tensor) -> Mapping[str, object]:
        values = _as_path_matrix(path, self.state_dim(), "path")
        return {
            "domain_policy": self.domain_policy,
            "min_state": tf.reduce_min(values),
            "has_negative_state": bool(tf.reduce_any(values < 0.0).numpy()),
        }

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SpatialSIRSSM",
            "source_equations": (
                "eq:p27-sir1",
                "eq:p27-sir2",
                "eq:p27-sir3",
                "eq:p27-sir4",
                "eq:p27-sir5",
                "eq:p27-sir6",
                "eq:p27-sir7",
                "eq:p27-sir8a",
                "eq:p27-sir8b",
                "eq:p27-sir8c",
                "eq:p27-sir9",
                "eq:p27-sir10",
                "eq:p27-sir11",
                "eq:p27-sir13",
            ),
            "compartments": self.observation_dim(),
            "state_dimension": self.state_dim(),
            "observation_dimension": self.observation_dim(),
            "dimension_convention": "state is (S_1,I_1,...,S_J,I_J) in R^{2J}; R is eliminated",
            "observation_convention": "infectious coordinates only",
            "neighbor_sets": self.neighbor_sets,
            "delta": self.delta,
            "rk4_internal_step": self.rk4_internal_step,
            "rk4_variant": self.rk4_variant,
            "rk4_substeps": int(self._rk4_substeps),
            "domain_policy": self.domain_policy,
            "process_noise_policy": self.process_noise_policy,
            "what_is_not_claimed": (
                "production_tt_sirt_sir_filtering",
                "paper_scale_j9_accuracy",
                "rank_ladder_evidence",
                "high_dimensional_scalability",
                "hmc_or_dsge_readiness",
            ),
        }

    def _rk4_step(self, state: tf.Tensor, step: tf.Tensor) -> tf.Tensor:
        k1 = self._rhs(state)
        k2 = self._rhs(state + 0.5 * step * k1)
        k3 = self._rhs(state + 0.5 * step * k2)
        if self.rk4_variant == "zhao_cui_sir_step":
            k4 = self._rhs(state + 0.5 * step * k3)
        else:
            k4 = self._rhs(state + step * k3)
        return state + (step / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    def _rhs(self, state: tf.Tensor) -> tf.Tensor:
        values = _as_row_matrix(state, self.state_dim(), "state")
        susceptible = values[:, 0::2]
        infectious = values[:, 1::2]
        susceptible_neighbor = (
            tf.linalg.matmul(susceptible, self._adjacency_matrix, transpose_b=True)
            - susceptible * self._neighbor_degree[tf.newaxis, :]
        )
        infectious_neighbor = (
            tf.linalg.matmul(infectious, self._adjacency_matrix, transpose_b=True)
            - infectious * self._neighbor_degree[tf.newaxis, :]
        )
        infection = self.kappa[tf.newaxis, :] * susceptible * infectious
        d_susceptible = -infection + 0.5 * susceptible_neighbor
        d_infectious = infection - self.nu[tf.newaxis, :] * infectious + 0.5 * infectious_neighbor
        return tf.reshape(
            tf.stack([d_susceptible, d_infectious], axis=2),
            [tf.shape(values)[0], self.state_dim()],
        )

    def _apply_process_noise_policy(self, values: tf.Tensor) -> tf.Tensor:
        state = _as_row_matrix(values, self.state_dim(), "values")
        if self.process_noise_policy != "clip_susceptible_after_noise":
            return state
        susceptible = tf.maximum(state[:, 0::2], tf.constant(0.0, dtype=tf.float64))
        infectious = state[:, 1::2]
        return tf.reshape(
            tf.stack([susceptible, infectious], axis=2),
            [tf.shape(state)[0], self.state_dim()],
        )


def p30_spatial_sir_fixture_model(
    compartments: int,
    neighbor_sets: tuple[tuple[int, ...], ...] | None = None,
) -> SpatialSIRSSM:
    """Return a small clean-room P30 SIR fixture with declared graph."""

    if int(compartments) <= 0:
        raise ValueError("compartments must be positive")
    j_values = tf.cast(tf.range(1, int(compartments) + 1), tf.float64)
    initial_pairs = tf.stack([485.0 + j_values, 15.0 - j_values], axis=1)
    if neighbor_sets is None:
        neighbor_sets = _chain_neighbor_sets(int(compartments))
    return SpatialSIRSSM(
        kappa=tf.fill([int(compartments)], tf.constant(0.1, dtype=tf.float64)),
        nu=tf.fill([int(compartments)], tf.constant(18.0, dtype=tf.float64)),
        initial_mean=tf.reshape(initial_pairs, [-1]),
        neighbor_sets=neighbor_sets,
    )


def zhao_cui_sir_austria_model() -> SpatialSIRSSM:
    """Return the author-source ``eg3_sir/sir_austria`` callback contract."""

    compartments = 9
    j_values = tf.cast(tf.range(1, compartments + 1), tf.float64)
    initial_pairs = tf.stack([486.0 + j_values, 14.0 - j_values], axis=1)
    return SpatialSIRSSM(
        kappa=tf.fill([compartments], tf.constant(0.1, dtype=tf.float64)),
        nu=tf.fill([compartments], tf.constant(18.0, dtype=tf.float64)),
        initial_mean=tf.reshape(initial_pairs, [-1]),
        neighbor_sets=_zhao_cui_sir_austria_neighbor_sets(),
        delta=0.02,
        rk4_internal_step=0.005,
        process_covariance=tf.eye(2 * compartments, dtype=tf.float64),
        observation_covariance=100.0 * tf.eye(compartments, dtype=tf.float64),
        initial_covariance=tf.eye(2 * compartments, dtype=tf.float64),
        rk4_variant="zhao_cui_sir_step",
        process_noise_policy="clip_susceptible_after_noise",
    )


@dataclass(frozen=True)
class PredatorPreySSM:
    """P30 predator-prey model contract for the M4 first gate."""

    initial_mean: tf.Tensor = tf.constant([50.0, 5.0], dtype=tf.float64)
    delta: float | tf.Tensor = 2.0
    rk4_internal_step: float | tf.Tensor = 0.1
    process_covariance: tf.Tensor | None = None
    observation_covariance: tf.Tensor | None = None
    initial_covariance: tf.Tensor | None = None
    domain_policy: str = "diagnose_negative_after_noise"

    def __post_init__(self) -> None:
        initial_mean = tf.convert_to_tensor(self.initial_mean, dtype=tf.float64)
        delta = tf.convert_to_tensor(self.delta, dtype=tf.float64)
        rk4_internal_step = tf.convert_to_tensor(self.rk4_internal_step, dtype=tf.float64)
        if initial_mean.shape != (2,):
            raise ValueError(f"initial_mean: {HighDimStatus.INVALID_SHAPE.value}")
        if delta.shape.rank != 0 or rk4_internal_step.shape.rank != 0:
            raise ValueError(f"time step: {HighDimStatus.INVALID_SHAPE.value}")
        if not bool(
            tf.reduce_all(tf.math.is_finite(initial_mean)).numpy()
            and tf.math.is_finite(delta).numpy()
            and tf.math.is_finite(rk4_internal_step).numpy()
            and (delta > 0.0).numpy()
            and (rk4_internal_step > 0.0).numpy()
        ):
            raise ValueError(f"PredatorPreySSM: {HighDimStatus.NONFINITE_VALUE.value}")
        ratio = delta / rk4_internal_step
        substeps = int(tf.round(ratio).numpy())
        if substeps <= 0 or abs(float((ratio - tf.cast(substeps, tf.float64)).numpy())) > 1e-12:
            raise ValueError("delta must be an integer multiple of rk4_internal_step")
        process_covariance = (
            4.0 * tf.eye(2, dtype=tf.float64)
            if self.process_covariance is None
            else tf.convert_to_tensor(self.process_covariance, dtype=tf.float64)
        )
        observation_covariance = (
            4.0 * tf.eye(2, dtype=tf.float64)
            if self.observation_covariance is None
            else tf.convert_to_tensor(self.observation_covariance, dtype=tf.float64)
        )
        initial_covariance = (
            tf.eye(2, dtype=tf.float64)
            if self.initial_covariance is None
            else tf.convert_to_tensor(self.initial_covariance, dtype=tf.float64)
        )
        for name, value in (
            ("process_covariance", process_covariance),
            ("observation_covariance", observation_covariance),
            ("initial_covariance", initial_covariance),
        ):
            if value.shape != (2, 2):
                raise ValueError(f"{name}: {HighDimStatus.INVALID_SHAPE.value}")
            if not bool(tf.reduce_all(tf.math.is_finite(value)).numpy()):
                raise ValueError(f"{name}: {HighDimStatus.NONFINITE_VALUE.value}")
        if self.domain_policy != "diagnose_negative_after_noise":
            raise ValueError("PredatorPreySSM first gate requires diagnose_negative_after_noise")
        object.__setattr__(self, "initial_mean", initial_mean)
        object.__setattr__(self, "delta", delta)
        object.__setattr__(self, "rk4_internal_step", rk4_internal_step)
        object.__setattr__(self, "process_covariance", _symmetrize(process_covariance))
        object.__setattr__(self, "observation_covariance", _symmetrize(observation_covariance))
        object.__setattr__(self, "initial_covariance", _symmetrize(initial_covariance))
        object.__setattr__(self, "_rk4_substeps", substeps)

    def parameter_dim(self) -> int:
        return 6

    def state_dim(self) -> int:
        return 2

    def observation_dim(self) -> int:
        return 2

    def parameter_box(self) -> Mapping[str, tuple[float, float]]:
        return {
            "r": (0.1, 1.1),
            "K": (110.0, 130.0),
            "a": (20.0, 30.0),
            "s": (0.1, 1.1),
            "u": (0.0, 1.0),
            "v": (0.0, 1.0),
        }

    def true_parameters(self) -> tf.Tensor:
        return tf.constant([0.6, 114.0, 25.0, 0.3, 0.5, 0.5], dtype=tf.float64)

    def validate_parameter_box(self, theta: tf.Tensor) -> bool:
        vector = _as_parameter_vector(theta, self.parameter_dim(), "theta")
        bounds = tf.constant(list(self.parameter_box().values()), dtype=tf.float64)
        return bool(tf.reduce_all(vector >= bounds[:, 0]).numpy() and tf.reduce_all(vector <= bounds[:, 1]).numpy())

    def initial_log_density(self, theta: tf.Tensor, x0: tf.Tensor) -> tf.Tensor:
        del theta
        values = _as_row_matrix(x0, self.state_dim(), "x0")
        return _mvn_log_prob(values, self.initial_mean, self.initial_covariance)

    def transition_mean(self, theta: tf.Tensor, x_prev: tf.Tensor) -> tf.Tensor:
        """Return the deterministic RK4 mean in P30 equation ``eq:p27-pp4``."""

        parameters = _as_parameter_vector(theta, self.parameter_dim(), "theta")
        if not self.validate_parameter_box(parameters):
            raise ValueError("theta outside P30 predator-prey parameter box")
        state = _as_row_matrix(x_prev, self.state_dim(), "x_prev")
        step = self.delta / tf.cast(self._rk4_substeps, tf.float64)
        for _ in range(int(self._rk4_substeps)):
            state = self._rk4_step(parameters, state, step)
        return state

    def transition_log_density(
        self,
        theta: tf.Tensor,
        x_prev: tf.Tensor,
        x_next: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del t
        previous = _as_row_matrix(x_prev, self.state_dim(), "x_prev")
        next_values = _as_row_matrix(x_next, self.state_dim(), "x_next")
        return _mvn_log_prob(next_values, self.transition_mean(theta, previous), self.process_covariance)

    def observation_log_density(
        self,
        theta: tf.Tensor,
        x_t: tf.Tensor,
        y_t: tf.Tensor,
        t: int,
    ) -> tf.Tensor:
        del theta, t
        values = _as_row_matrix(x_t, self.state_dim(), "x_t")
        observation = tf.reshape(tf.convert_to_tensor(y_t, dtype=tf.float64), [self.observation_dim()])
        return _mvn_log_prob(
            tf.broadcast_to(observation, tf.shape(values)),
            values,
            self.observation_covariance,
        )

    def simulate(
        self,
        theta: tf.Tensor,
        final_time: int,
        seed: int,
    ) -> tuple[tf.Tensor, tf.Tensor]:
        """Generate ``x_0:x_T`` and ``y_0:y_T`` without positivity projection."""

        if int(final_time) < 0:
            raise ValueError("final_time must be nonnegative")
        parameters = _as_parameter_vector(theta, self.parameter_dim(), "theta")
        if not self.validate_parameter_box(parameters):
            raise ValueError("theta outside P30 predator-prey parameter box")
        generator = tf.random.Generator.from_seed(int(seed))
        initial_chol = tf.linalg.cholesky(self.initial_covariance)
        process_chol = tf.linalg.cholesky(self.process_covariance)
        observation_chol = tf.linalg.cholesky(self.observation_covariance)
        state = self.initial_mean + tf.linalg.matvec(
            initial_chol,
            generator.normal([self.state_dim()], dtype=tf.float64),
        )
        states = [state]
        observations = [
            state
            + tf.linalg.matvec(
                observation_chol,
                generator.normal([self.observation_dim()], dtype=tf.float64),
            )
        ]
        for _time_index in range(1, int(final_time) + 1):
            mean = self.transition_mean(parameters, state)[0]
            state = mean + tf.linalg.matvec(
                process_chol,
                generator.normal([self.state_dim()], dtype=tf.float64),
            )
            states.append(state)
            observations.append(
                state
                + tf.linalg.matvec(
                    observation_chol,
                    generator.normal([self.observation_dim()], dtype=tf.float64),
                )
            )
        return tf.stack(states), tf.stack(observations)

    def trajectory_rmse(
        self,
        truth_path: tf.Tensor,
        estimate_path: tf.Tensor,
    ) -> tf.Tensor:
        truth = _as_path_matrix(truth_path, self.state_dim(), "truth_path")
        estimate = _as_path_matrix(estimate_path, self.state_dim(), "estimate_path")
        if truth.shape != estimate.shape:
            raise ValueError(f"estimate_path: {HighDimStatus.INVALID_SHAPE.value}")
        return tf.sqrt(tf.reduce_mean(tf.square(truth - estimate)))

    def domain_diagnostics(self, path: tf.Tensor) -> Mapping[str, object]:
        values = _as_path_matrix(path, self.state_dim(), "path")
        return {
            "domain_policy": self.domain_policy,
            "min_state": tf.reduce_min(values),
            "has_negative_state": bool(tf.reduce_any(values < 0.0).numpy()),
        }

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "PredatorPreySSM",
            "source_equations": (
                "eq:p27-pp1",
                "eq:p27-pp2",
                "eq:p27-pp3",
                "eq:p27-pp4",
                "eq:p27-pp5",
                "eq:p27-pp5a",
                "eq:p27-pp5b",
                "eq:p27-pp5c",
                "eq:p27-pp5d",
                "eq:p27-pp6",
                "eq:p27-pp7",
                "eq:p27-pp8",
            ),
            "state_dimension": self.state_dim(),
            "observation_dimension": self.observation_dim(),
            "parameter_dimension": self.parameter_dim(),
            "dimension_convention": "state is (P,Q); parameter is (r,K,a,s,u,v)",
            "parameter_box": self.parameter_box(),
            "initial_mean": self.initial_mean,
            "delta": self.delta,
            "rk4_internal_step": self.rk4_internal_step,
            "rk4_substeps": int(self._rk4_substeps),
            "domain_policy": self.domain_policy,
            "what_is_not_claimed": (
                "nonlinear_preconditioning_usefulness",
                "matched_linear_nonlinear_comparison_success",
                "paper_scale_predator_prey_result",
                "adaptive_matlab_behavior",
                "high_dimensional_scalability",
            ),
        }

    def _rk4_step(self, theta: tf.Tensor, state: tf.Tensor, step: tf.Tensor) -> tf.Tensor:
        k1 = self._rhs(theta, state)
        k2 = self._rhs(theta, state + 0.5 * step * k1)
        k3 = self._rhs(theta, state + 0.5 * step * k2)
        k4 = self._rhs(theta, state + step * k3)
        return state + (step / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    def _rhs(self, theta: tf.Tensor, state: tf.Tensor) -> tf.Tensor:
        parameters = _as_parameter_vector(theta, self.parameter_dim(), "theta")
        values = _as_row_matrix(state, self.state_dim(), "state")
        r, k_capacity, a_half, s_rate, u_rate, v_rate = tf.unstack(parameters)
        prey = values[:, 0]
        predator = values[:, 1]
        denominator = a_half + prey
        if bool(tf.reduce_any(tf.abs(denominator) <= 0.0).numpy()):
            raise ValueError(f"predator-prey denominator: {HighDimStatus.NONFINITE_VALUE.value}")
        interaction = prey * predator / denominator
        d_prey = r * prey * (1.0 - prey / k_capacity) - s_rate * interaction
        d_predator = u_rate * interaction - v_rate * predator
        return tf.stack([d_prey, d_predator], axis=1)


def p30_predator_prey_fixture_model() -> PredatorPreySSM:
    """Return the clean-room P30 predator-prey first-gate fixture."""

    return PredatorPreySSM()


def _as_row_matrix(values: tf.Tensor, width: int, name: str) -> tf.Tensor:
    tensor = tf.convert_to_tensor(values, dtype=tf.float64)
    if tensor.shape.rank == 1:
        tensor = tensor[tf.newaxis, :]
    if tensor.shape.rank != 2 or tensor.shape[1] != width:
        raise ValueError(f"{name}: {HighDimStatus.INVALID_SHAPE.value}")
    if not bool(tf.reduce_all(tf.math.is_finite(tensor)).numpy()):
        raise ValueError(f"{name}: {HighDimStatus.NONFINITE_VALUE.value}")
    return tensor


def _as_path_matrix(values: tf.Tensor, width: int, name: str) -> tf.Tensor:
    tensor = tf.convert_to_tensor(values, dtype=tf.float64)
    if tensor.shape.rank != 2 or tensor.shape[1] != width:
        raise ValueError(f"{name}: {HighDimStatus.INVALID_SHAPE.value}")
    if not bool(tf.reduce_all(tf.math.is_finite(tensor)).numpy()):
        raise ValueError(f"{name}: {HighDimStatus.NONFINITE_VALUE.value}")
    return tensor


def _as_parameter_vector(values: tf.Tensor, width: int, name: str) -> tf.Tensor:
    tensor = tf.convert_to_tensor(values, dtype=tf.float64)
    if tensor.shape.rank == 2 and tensor.shape[0] == 1:
        tensor = tensor[0]
    if tensor.shape.rank != 1 or tensor.shape[0] != width:
        raise ValueError(f"{name}: {HighDimStatus.INVALID_SHAPE.value}")
    if not bool(tf.reduce_all(tf.math.is_finite(tensor)).numpy()):
        raise ValueError(f"{name}: {HighDimStatus.NONFINITE_VALUE.value}")
    return tensor


def _mvn_log_prob(values: tf.Tensor, loc: tf.Tensor, covariance: tf.Tensor) -> tf.Tensor:
    covariance = _symmetrize(covariance)
    chol = tf.linalg.cholesky(covariance)
    distribution = tfp.distributions.MultivariateNormalTriL(loc=loc, scale_tril=chol)
    return distribution.log_prob(values)


def _symmetrize(matrix: tf.Tensor) -> tf.Tensor:
    return 0.5 * (matrix + tf.linalg.matrix_transpose(matrix))


def _standard_normal() -> tfp.distributions.Normal:
    return tfp.distributions.Normal(
        loc=tf.constant(0.0, dtype=tf.float64),
        scale=tf.constant(1.0, dtype=tf.float64),
    )


def _normalize_neighbor_sets(
    neighbor_sets: tuple[tuple[int, ...], ...],
    compartments: int,
) -> tuple[tuple[int, ...], ...]:
    if len(neighbor_sets) != int(compartments):
        raise ValueError(f"neighbor_sets: {HighDimStatus.INVALID_SHAPE.value}")
    normalized = []
    for index, neighbors in enumerate(neighbor_sets):
        clean = tuple(int(neighbor) for neighbor in neighbors)
        if any(neighbor < 0 or neighbor >= compartments or neighbor == index for neighbor in clean):
            raise ValueError(f"neighbor_sets: {HighDimStatus.INVALID_SHAPE.value}")
        if len(set(clean)) != len(clean):
            raise ValueError(f"neighbor_sets: {HighDimStatus.INVALID_SHAPE.value}")
        normalized.append(clean)
    return tuple(normalized)


def _neighbor_adjacency_matrix(neighbor_sets: tuple[tuple[int, ...], ...]) -> tf.Tensor:
    rows = []
    for neighbors in neighbor_sets:
        rows.append([1.0 if col in neighbors else 0.0 for col in range(len(neighbor_sets))])
    return tf.constant(rows, dtype=tf.float64)


def _chain_neighbor_sets(compartments: int) -> tuple[tuple[int, ...], ...]:
    rows = []
    for index in range(int(compartments)):
        neighbors = []
        if index > 0:
            neighbors.append(index - 1)
        if index + 1 < int(compartments):
            neighbors.append(index + 1)
        rows.append(tuple(neighbors))
    return tuple(rows)


def _zhao_cui_sir_austria_neighbor_sets() -> tuple[tuple[int, ...], ...]:
    raw_sets = (
        (0, 1),
        (0, 1, 2, 3),
        (1, 2, 3, 4, 5),
        (1, 2, 3, 4),
        (2, 3, 4, 5, 6, 8),
        (2, 4, 5, 6),
        (4, 5, 6, 7, 8),
        (6, 7),
        (4, 6, 8),
    )
    return tuple(
        tuple(neighbor for neighbor in neighbors if neighbor != index)
        for index, neighbors in enumerate(raw_sets)
    )
