"""Experimental shape contract for batched LEDH-PFPF-OT.

This module is intentionally not exported from the public ``bayesfilter`` API.
It defines the fixed-contract tensor shapes needed before implementing a
batch-native LEDH-PFPF-OT value or score recursion.
"""

from __future__ import annotations

import inspect
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

import tensorflow as tf

from experiments.dpf_implementation.tf_tfp.resampling import annealed_transport_tf
from experiments.dpf_implementation.tf_tfp.resampling.annealed_transport_tf import (
    AnnealedTransportWarmstartStateTF,
    DEFAULT_STREAMING_CHUNK_SIZE,
    _maybe_stop,
    _clip_transport_upstream_gradient,
    _filterflow_custom_gradient_transport_matrix,
    _filterflow_exact_transport_matrix,
    _filterflow_scale,
    _filterflow_streaming_transport,
    _transport_ad_stop_scale,
    _validate_transport_ad_mode,
)


DEFAULT_DTYPE = tf.float32
DTYPE = DEFAULT_DTYPE
DEFAULT_TF32_MODE = "enabled"
DEFAULT_PRECISION_POLICY = "experimental_ledh_pfpf_ot_gpu_tf32"

SCALAR_PARITY_ATOL = 1.0e-10
SCALAR_PARITY_RTOL = 1.0e-10
TRANSPORT_PARITY_ATOL = 1.0e-8
TRANSPORT_PARITY_RTOL = 1.0e-8

FORBIDDEN_RNG_SOURCE_TOKENS = (
    "tf.random",
    "tensorflow.random",
    "np.random",
    "numpy.random",
    "random.",
)


def _sync_transport_dtype() -> None:
    """Keep imported transport helper globals aligned with this experimental lane."""

    annealed_transport_tf.DTYPE = DTYPE


def precision_policy_metadata() -> dict[str, Any]:
    """Return the scoped precision policy for the experimental batched DPF lane."""

    return {
        "precision_default_policy": DEFAULT_PRECISION_POLICY,
        "default_dtype": DEFAULT_DTYPE.name,
        "active_dtype": DTYPE.name,
        "default_tf32_mode": DEFAULT_TF32_MODE,
        "fp64_reference_requires_explicit_dtype": True,
        "scope": "experimental_batched_ledh_pfpf_ot_gpu_performance_lane",
    }

NONCLAIMS = (
    "experimental opt-in DPF contract only",
    "no production default readiness claim",
    "no public API claim",
    "no categorical particle-filter gradient claim",
    "no GPU performance claim",
)


@dataclass(frozen=True)
class BatchedLEDHPFPFOTShapeContract:
    """Static tensor dimensions for a fixed-branch batched LEDH-PFPF-OT run."""

    batch_size: int
    time_steps: int
    num_particles: int
    state_dim: int
    observation_dim: int
    parameter_dim: int
    scalar_parity_atol: float = SCALAR_PARITY_ATOL
    scalar_parity_rtol: float = SCALAR_PARITY_RTOL
    transport_parity_atol: float = TRANSPORT_PARITY_ATOL
    transport_parity_rtol: float = TRANSPORT_PARITY_RTOL
    nonclaims: tuple[str, ...] = NONCLAIMS

    @property
    def value_shape(self) -> tuple[int]:
        return (self.batch_size,)

    @property
    def score_shape(self) -> tuple[int, int]:
        return (self.batch_size, self.parameter_dim)

    @property
    def particle_shape(self) -> tuple[int, int, int]:
        return (self.batch_size, self.num_particles, self.state_dim)

    @property
    def fixed_pre_flow_shape(self) -> tuple[int, int, int, int]:
        return (
            self.batch_size,
            self.time_steps,
            self.num_particles,
            self.state_dim,
        )

    @property
    def fixed_mask_shape(self) -> tuple[int, int]:
        return (self.batch_size, self.time_steps)

    def as_dict(self) -> dict[str, Any]:
        return {
            "batch_size": self.batch_size,
            "time_steps": self.time_steps,
            "num_particles": self.num_particles,
            "state_dim": self.state_dim,
            "observation_dim": self.observation_dim,
            "parameter_dim": self.parameter_dim,
            "scalar_parity_atol": self.scalar_parity_atol,
            "scalar_parity_rtol": self.scalar_parity_rtol,
            "transport_parity_atol": self.transport_parity_atol,
            "transport_parity_rtol": self.transport_parity_rtol,
            "nonclaims": self.nonclaims,
        }


@dataclass(frozen=True)
class BatchedLEDHPFPFOTFixedInputs:
    """Deterministic inputs for a fixed-branch batched LEDH-PFPF-OT fixture."""

    theta_batch: tf.Tensor
    observations: tf.Tensor
    initial_particles: tf.Tensor
    pre_flow_particles: tf.Tensor
    fixed_resampling_mask: tf.Tensor
    initial_log_weights: tf.Tensor | None = None
    shape_contract: BatchedLEDHPFPFOTShapeContract = field(init=False)

    def __post_init__(self) -> None:
        theta_batch = _to_float_tensor(self.theta_batch, "theta_batch")
        observations = _to_float_tensor(self.observations, "observations")
        initial_particles = _to_float_tensor(self.initial_particles, "initial_particles")
        pre_flow_particles = _to_float_tensor(self.pre_flow_particles, "pre_flow_particles")
        fixed_resampling_mask = tf.convert_to_tensor(
            self.fixed_resampling_mask,
            dtype=tf.bool,
        )

        _require_static_rank(theta_batch, 2, "theta_batch")
        _require_static_rank(observations, 2, "observations")
        _require_static_rank(initial_particles, 3, "initial_particles")
        _require_static_rank(pre_flow_particles, 4, "pre_flow_particles")
        _require_static_rank(fixed_resampling_mask, 2, "fixed_resampling_mask")

        batch_size, num_particles, state_dim = _static_shape(
            initial_particles,
            "initial_particles",
        )
        theta_batch_size, parameter_dim = _static_shape(theta_batch, "theta_batch")
        time_steps, observation_dim = _static_shape(observations, "observations")
        pre_batch, pre_time, pre_particles, pre_state = _static_shape(
            pre_flow_particles,
            "pre_flow_particles",
        )
        mask_batch, mask_time = _static_shape(
            fixed_resampling_mask,
            "fixed_resampling_mask",
        )

        _require_equal(theta_batch_size, batch_size, "theta_batch batch size")
        _require_equal(pre_batch, batch_size, "pre_flow_particles batch size")
        _require_equal(pre_time, time_steps, "pre_flow_particles time steps")
        _require_equal(pre_particles, num_particles, "pre_flow_particles particle count")
        _require_equal(pre_state, state_dim, "pre_flow_particles state dim")
        _require_equal(mask_batch, batch_size, "fixed_resampling_mask batch size")
        _require_equal(mask_time, time_steps, "fixed_resampling_mask time steps")

        if self.initial_log_weights is None:
            initial_log_weights = uniform_log_weights(batch_size, num_particles)
        else:
            initial_log_weights = _to_float_tensor(
                self.initial_log_weights,
                "initial_log_weights",
            )
            _require_static_rank(initial_log_weights, 2, "initial_log_weights")
            weights_batch, weights_particles = _static_shape(
                initial_log_weights,
                "initial_log_weights",
            )
            _require_equal(weights_batch, batch_size, "initial_log_weights batch size")
            _require_equal(
                weights_particles,
                num_particles,
                "initial_log_weights particle count",
            )

        shape_contract = BatchedLEDHPFPFOTShapeContract(
            batch_size=batch_size,
            time_steps=time_steps,
            num_particles=num_particles,
            state_dim=state_dim,
            observation_dim=observation_dim,
            parameter_dim=parameter_dim,
        )

        object.__setattr__(self, "theta_batch", theta_batch)
        object.__setattr__(self, "observations", observations)
        object.__setattr__(self, "initial_particles", initial_particles)
        object.__setattr__(self, "pre_flow_particles", pre_flow_particles)
        object.__setattr__(self, "fixed_resampling_mask", fixed_resampling_mask)
        object.__setattr__(self, "initial_log_weights", initial_log_weights)
        object.__setattr__(self, "shape_contract", shape_contract)


@dataclass(frozen=True)
class BatchedLEDHFlowTensors:
    """Tensor output contract for one batched LEDH flow step."""

    post_flow_particles: tf.Tensor
    pre_flow_log_density: tf.Tensor
    forward_log_det: tf.Tensor
    local_posterior_means: tf.Tensor
    local_posterior_covariances: tf.Tensor

    def __post_init__(self) -> None:
        post_flow_particles = _to_float_tensor(
            self.post_flow_particles,
            "post_flow_particles",
        )
        pre_flow_log_density = _to_float_tensor(
            self.pre_flow_log_density,
            "pre_flow_log_density",
        )
        forward_log_det = _to_float_tensor(self.forward_log_det, "forward_log_det")
        local_posterior_means = _to_float_tensor(
            self.local_posterior_means,
            "local_posterior_means",
        )
        local_posterior_covariances = _to_float_tensor(
            self.local_posterior_covariances,
            "local_posterior_covariances",
        )

        _require_static_rank(post_flow_particles, 3, "post_flow_particles")
        _require_static_rank(pre_flow_log_density, 2, "pre_flow_log_density")
        _require_static_rank(forward_log_det, 2, "forward_log_det")
        _require_static_rank(local_posterior_means, 3, "local_posterior_means")
        _require_static_rank(
            local_posterior_covariances,
            4,
            "local_posterior_covariances",
        )
        _require_flow_shapes(
            post_flow_particles=post_flow_particles,
            pre_flow_log_density=pre_flow_log_density,
            forward_log_det=forward_log_det,
            local_posterior_means=local_posterior_means,
            local_posterior_covariances=local_posterior_covariances,
        )

        object.__setattr__(self, "post_flow_particles", post_flow_particles)
        object.__setattr__(self, "pre_flow_log_density", pre_flow_log_density)
        object.__setattr__(self, "forward_log_det", forward_log_det)
        object.__setattr__(self, "local_posterior_means", local_posterior_means)
        object.__setattr__(
            self,
            "local_posterior_covariances",
            local_posterior_covariances,
        )


@dataclass(frozen=True)
class BatchedAnnealedTransportTensors:
    """Tensor output contract for one fixed-mask annealed transport step."""

    particles: tf.Tensor
    log_weights: tf.Tensor
    transport_matrix: tf.Tensor
    max_row_residual: tf.Tensor
    max_column_residual: tf.Tensor

    def __post_init__(self) -> None:
        particles = _to_float_tensor(self.particles, "transported_particles")
        log_weights = _to_float_tensor(self.log_weights, "transported_log_weights")
        transport_matrix = _to_float_tensor(self.transport_matrix, "transport_matrix")
        max_row_residual = _to_float_tensor(self.max_row_residual, "max_row_residual")
        max_column_residual = _to_float_tensor(
            self.max_column_residual,
            "max_column_residual",
        )

        _require_static_rank(particles, 3, "transported_particles")
        _require_static_rank(log_weights, 2, "transported_log_weights")
        _require_static_rank(transport_matrix, 3, "transport_matrix")
        _require_static_rank(max_row_residual, 0, "max_row_residual")
        _require_static_rank(max_column_residual, 0, "max_column_residual")
        batch_size, num_particles, _state_dim = _static_shape(
            particles,
            "transported_particles",
        )
        _require_equal(
            _static_shape(log_weights, "transported_log_weights")[0],
            batch_size,
            "transported_log_weights batch size",
        )
        _require_equal(
            _static_shape(log_weights, "transported_log_weights")[1],
            num_particles,
            "transported_log_weights particle count",
        )
        matrix_shape = _static_shape(transport_matrix, "transport_matrix")
        expected_matrix_shape = (batch_size, num_particles, num_particles)
        sentinel_shape = (batch_size, 0, 0)
        if matrix_shape not in {expected_matrix_shape, sentinel_shape}:
            raise ValueError(
                "transport_matrix shape mismatch: "
                f"got {matrix_shape}, expected {expected_matrix_shape} or {sentinel_shape}"
            )

        object.__setattr__(self, "particles", particles)
        object.__setattr__(self, "log_weights", log_weights)
        object.__setattr__(self, "transport_matrix", transport_matrix)
        object.__setattr__(self, "max_row_residual", max_row_residual)
        object.__setattr__(self, "max_column_residual", max_column_residual)


@dataclass(frozen=True)
class BatchedLEDHPFPFOTValueTensors:
    """Batched fixed-branch LEDH-PFPF-OT value-recursion outputs."""

    log_likelihood: tf.Tensor
    filtered_means: tf.Tensor
    filtered_variances: tf.Tensor
    ess_by_time: tf.Tensor

    def __post_init__(self) -> None:
        log_likelihood = _to_float_tensor(self.log_likelihood, "log_likelihood")
        filtered_means = _to_float_tensor(self.filtered_means, "filtered_means")
        filtered_variances = _to_float_tensor(
            self.filtered_variances,
            "filtered_variances",
        )
        ess_by_time = _to_float_tensor(self.ess_by_time, "ess_by_time")
        _require_static_rank(log_likelihood, 1, "log_likelihood")
        _require_static_rank(filtered_means, 3, "filtered_means")
        _require_static_rank(filtered_variances, 3, "filtered_variances")
        _require_static_rank(ess_by_time, 2, "ess_by_time")
        time_steps, batch_size, state_dim = _static_shape(
            filtered_means,
            "filtered_means",
        )
        variance_shape = _static_shape(filtered_variances, "filtered_variances")
        expected_variance_shape = (time_steps, batch_size, state_dim)
        if variance_shape != expected_variance_shape:
            raise ValueError(
                "filtered_variances shape mismatch: "
                f"got {variance_shape}, expected {expected_variance_shape}"
            )
        _require_equal(
            _static_shape(log_likelihood, "log_likelihood")[0],
            batch_size,
            "log_likelihood batch size",
        )
        ess_shape = _static_shape(ess_by_time, "ess_by_time")
        expected_ess_shape = (time_steps, batch_size)
        if ess_shape != expected_ess_shape:
            raise ValueError(
                f"ess_by_time shape mismatch: got {ess_shape}, expected {expected_ess_shape}"
            )

        object.__setattr__(self, "log_likelihood", log_likelihood)
        object.__setattr__(self, "filtered_means", filtered_means)
        object.__setattr__(self, "filtered_variances", filtered_variances)
        object.__setattr__(self, "ess_by_time", ess_by_time)


@dataclass(frozen=True)
class BatchedLEDHPFPFOTValueScoreTensors:
    """Batched relaxed-objective value and TensorFlow autodiff score."""

    log_likelihood: tf.Tensor
    score: tf.Tensor

    def __post_init__(self) -> None:
        log_likelihood = _to_float_tensor(self.log_likelihood, "log_likelihood")
        score = _to_float_tensor(self.score, "score")
        _require_static_rank(log_likelihood, 1, "log_likelihood")
        _require_static_rank(score, 2, "score")
        batch_size = _static_shape(log_likelihood, "log_likelihood")[0]
        _require_equal(_static_shape(score, "score")[0], batch_size, "score batch size")

        object.__setattr__(self, "log_likelihood", log_likelihood)
        object.__setattr__(self, "score", score)


@dataclass(frozen=True)
class BatchedLEDHPFPFOTCallbacks:
    """Readiness wrapper for deterministic batched model callbacks."""

    ledh_flow: Callable[..., BatchedLEDHFlowTensors]
    transition_log_density: Callable[..., tf.Tensor]
    observation_log_density: Callable[..., tf.Tensor]
    allow_uninspectable_callbacks: bool = False

    def __post_init__(self) -> None:
        for name, callback in (
            ("ledh_flow", self.ledh_flow),
            ("transition_log_density", self.transition_log_density),
            ("observation_log_density", self.observation_log_density),
        ):
            assert_callback_has_no_forbidden_rng(
                callback,
                name=name,
                allow_uninspectable=self.allow_uninspectable_callbacks,
            )


def uniform_log_weights(batch_size: int, num_particles: int) -> tf.Tensor:
    """Return normalized uniform log weights with shape ``[B,N]``."""

    if batch_size <= 0:
        raise ValueError("batch_size must be positive")
    if num_particles <= 0:
        raise ValueError("num_particles must be positive")
    return tf.fill(
        [batch_size, num_particles],
        -tf.math.log(tf.cast(num_particles, DTYPE)),
    )


def validate_batched_value_tensor(
    value: tf.Tensor,
    contract: BatchedLEDHPFPFOTShapeContract,
) -> tf.Tensor:
    """Validate and return a batched value tensor with shape ``[B]``."""

    value = _to_float_tensor(value, "value")
    _require_static_rank(value, 1, "value")
    _require_equal(_static_shape(value, "value")[0], contract.batch_size, "value batch size")
    return value


def validate_batched_score_tensor(
    score: tf.Tensor,
    contract: BatchedLEDHPFPFOTShapeContract,
) -> tf.Tensor:
    """Validate and return a batched score tensor with shape ``[B,p]``."""

    score = _to_float_tensor(score, "score")
    _require_static_rank(score, 2, "score")
    batch_size, parameter_dim = _static_shape(score, "score")
    _require_equal(batch_size, contract.batch_size, "score batch size")
    _require_equal(parameter_dim, contract.parameter_dim, "score parameter dim")
    return score


def validate_flow_tensors_against_contract(
    flow: BatchedLEDHFlowTensors,
    contract: BatchedLEDHPFPFOTShapeContract,
) -> BatchedLEDHFlowTensors:
    """Fail closed if one-step LEDH flow tensors violate ``[B,N,D]`` shapes."""

    batch_size, num_particles, state_dim = _static_shape(
        flow.post_flow_particles,
        "post_flow_particles",
    )
    _require_equal(batch_size, contract.batch_size, "flow batch size")
    _require_equal(num_particles, contract.num_particles, "flow particle count")
    _require_equal(state_dim, contract.state_dim, "flow state dim")
    return flow


def batched_ledh_flow_core_tf(
    *,
    pre_flow_particles: tf.Tensor,
    ancestors: tf.Tensor,
    observation: tf.Tensor,
    transition_matrix: tf.Tensor,
    transition_covariance: tf.Tensor,
    observation_covariance: tf.Tensor,
    observation_fn: Callable[[tf.Tensor], tf.Tensor],
    observation_jacobian_fn: Callable[[tf.Tensor], tf.Tensor],
    observation_residual_fn: Callable[[tf.Tensor, tf.Tensor], tf.Tensor],
    prior_mean_fn: Callable[[tf.Tensor], tf.Tensor] | None = None,
    jitter: float | tf.Tensor = 1.0e-9,
) -> BatchedLEDHFlowTensors:
    """Vectorized one-step LEDH affine flow over parameter rows and particles."""

    x0 = _to_float_tensor(pre_flow_particles, "pre_flow_particles")
    ancestors = _to_float_tensor(ancestors, "ancestors")
    observation = _to_float_tensor(observation, "observation")
    transition_matrix = _to_float_tensor(transition_matrix, "transition_matrix")
    transition_covariance = _stabilize_batch_covariance(
        transition_covariance,
        jitter,
        "transition_covariance",
    )
    observation_covariance = _stabilize_batch_covariance(
        observation_covariance,
        jitter,
        "observation_covariance",
    )

    _require_static_rank(x0, 3, "pre_flow_particles")
    _require_static_rank(ancestors, 3, "ancestors")
    _require_static_rank(transition_matrix, 3, "transition_matrix")
    _require_static_rank(transition_covariance, 3, "transition_covariance")
    _require_static_rank(observation_covariance, 3, "observation_covariance")

    batch_size, num_particles, state_dim = _static_shape(x0, "pre_flow_particles")
    _require_equal(
        _static_shape(ancestors, "ancestors")[0],
        batch_size,
        "ancestors batch size",
    )
    _require_equal(
        _static_shape(ancestors, "ancestors")[1],
        num_particles,
        "ancestors particle count",
    )
    _require_equal(
        _static_shape(ancestors, "ancestors")[2],
        state_dim,
        "ancestors state dim",
    )
    _require_square_batch(transition_matrix, batch_size, state_dim, "transition_matrix")
    _require_square_batch(
        transition_covariance,
        batch_size,
        state_dim,
        "transition_covariance",
    )
    observation_dim = _static_shape(observation_covariance, "observation_covariance")[1]
    _require_square_batch(
        observation_covariance,
        batch_size,
        observation_dim,
        "observation_covariance",
    )

    if prior_mean_fn is None:
        prior_means = tf.einsum("bnj,bdj->bnd", ancestors, transition_matrix)
    else:
        prior_means = _to_float_tensor(
            prior_mean_fn(ancestors),
            "prior_mean_fn output",
        )
        _require_static_rank(prior_means, 3, "prior_mean_fn output")
        if _static_shape(prior_means, "prior_mean_fn output") != (
            batch_size,
            num_particles,
            state_dim,
        ):
            raise ValueError("prior_mean_fn output shape mismatch")
    pre_flow_log_density = _batched_gaussian_logpdf(
        x0 - prior_means,
        transition_covariance,
    )

    prior_chol = tf.linalg.cholesky(transition_covariance)
    prior_precision = tf.linalg.cholesky_solve(
        prior_chol,
        _tile_eye(batch_size, state_dim),
    )
    obs_chol = tf.linalg.cholesky(observation_covariance)
    obs_precision = tf.linalg.cholesky_solve(
        obs_chol,
        _tile_eye(batch_size, observation_dim),
    )

    h_ref = _to_float_tensor(observation_fn(x0), "observation_fn output")
    h_jac = _to_float_tensor(observation_jacobian_fn(x0), "observation_jacobian_fn output")
    residual = _to_float_tensor(
        observation_residual_fn(h_ref, observation),
        "observation_residual_fn output",
    )
    _require_static_rank(h_ref, 3, "observation_fn output")
    _require_static_rank(h_jac, 4, "observation_jacobian_fn output")
    _require_static_rank(residual, 3, "observation_residual_fn output")
    _require_observation_callback_shapes(
        h_ref=h_ref,
        h_jac=h_jac,
        residual=residual,
        batch_size=batch_size,
        num_particles=num_particles,
        state_dim=state_dim,
        observation_dim=observation_dim,
    )

    pseudo_observation = tf.einsum("bnod,bnd->bno", h_jac, x0) + residual
    post_precision = prior_precision[:, None, :, :] + tf.einsum(
        "bnod,boq,bnqe->bnde",
        h_jac,
        obs_precision,
        h_jac,
    )
    post_covariance = tf.linalg.inv(
        _stabilize_batch_covariance(
            post_precision,
            jitter,
            "post_precision",
        )
    )
    post_covariance = _stabilize_batch_covariance(
        post_covariance,
        jitter,
        "post_covariance",
    )
    info = tf.einsum("bde,bne->bnd", prior_precision, prior_means) + tf.einsum(
        "bnod,boq,bnq->bnd",
        h_jac,
        obs_precision,
        pseudo_observation,
    )
    post_mean = tf.einsum("bnde,bne->bnd", post_covariance, info)
    post_chol = tf.linalg.cholesky(post_covariance)
    prior_inv = tf.linalg.triangular_solve(
        prior_chol,
        _tile_eye(batch_size, state_dim),
    )
    affine_transform = tf.einsum("bnij,bjk->bnik", post_chol, prior_inv)
    post_flow_particles = post_mean + tf.einsum(
        "bnij,bnj->bni",
        affine_transform,
        x0 - prior_means,
    )
    forward_log_det = tf.reduce_sum(
        tf.math.log(tf.linalg.diag_part(post_chol)),
        axis=-1,
    ) - tf.reduce_sum(
        tf.math.log(tf.linalg.diag_part(prior_chol)),
        axis=-1,
    )[:, None]

    return BatchedLEDHFlowTensors(
        post_flow_particles=post_flow_particles,
        pre_flow_log_density=pre_flow_log_density,
        forward_log_det=forward_log_det,
        local_posterior_means=post_mean,
        local_posterior_covariances=post_covariance,
    )


def batched_annealed_transport_core_tf(
    particles: tf.Tensor,
    log_weights: tf.Tensor,
    fixed_resampling_mask: tf.Tensor,
    *,
    epsilon: float | tf.Tensor = 0.5,
    scaling: float | tf.Tensor = 0.9,
    convergence_threshold: float | tf.Tensor = 1.0e-3,
    max_iterations: int | tf.Tensor = 100,
    transport_gradient_mode: str = "filterflow_clipped",
    transport_plan_mode: str = "dense",
    transport_ad_mode: str = "stabilized",
    row_chunk_size: int = DEFAULT_STREAMING_CHUNK_SIZE,
    col_chunk_size: int = DEFAULT_STREAMING_CHUNK_SIZE,
    warmstart_state: AnnealedTransportWarmstartStateTF | None = None,
) -> BatchedAnnealedTransportTensors:
    """Apply annealed transport to fixed-mask rows without eager branch logic."""

    _sync_transport_dtype()
    if transport_gradient_mode not in {"filterflow_clipped", "filterflow_custom_op", "raw"}:
        raise ValueError(
            "transport_gradient_mode must be 'filterflow_clipped', "
            "'filterflow_custom_op', or 'raw'"
        )
    if transport_plan_mode not in {"dense", "streaming"}:
        raise ValueError("transport_plan_mode must be 'dense' or 'streaming'")
    _validate_transport_ad_mode(transport_ad_mode)
    if transport_plan_mode == "streaming" and transport_gradient_mode != "raw":
        raise ValueError("streaming transport currently supports transport_gradient_mode='raw' only")
    if row_chunk_size <= 0 or col_chunk_size <= 0:
        raise ValueError("row_chunk_size and col_chunk_size must be positive")
    x = _to_float_tensor(particles, "particles")
    logw = _to_float_tensor(log_weights, "log_weights")
    mask = tf.reshape(tf.convert_to_tensor(fixed_resampling_mask, dtype=tf.bool), [-1])
    _require_static_rank(x, 3, "particles")
    _require_static_rank(logw, 2, "log_weights")
    _require_static_rank(mask, 1, "fixed_resampling_mask")

    batch_size, num_particles, _state_dim = _static_shape(x, "particles")
    _require_equal(
        _static_shape(logw, "log_weights")[0],
        batch_size,
        "log_weights batch size",
    )
    _require_equal(
        _static_shape(logw, "log_weights")[1],
        num_particles,
        "log_weights particle count",
    )
    _require_equal(
        _static_shape(mask, "fixed_resampling_mask")[0],
        batch_size,
        "fixed_resampling_mask batch size",
    )

    center = tf.reduce_mean(x, axis=1, keepdims=True)
    center = _maybe_stop(center, stop=_transport_ad_stop_scale(transport_ad_mode))
    centered = x - center
    scale = _filterflow_scale(x)
    scale_for_division = _maybe_stop(
        scale,
        stop=_transport_ad_stop_scale(transport_ad_mode),
    )
    scaled_x = centered / scale_for_division[:, None, None]
    epsilon_tensor = tf.convert_to_tensor(epsilon, dtype=DTYPE)
    scaling_tensor = tf.convert_to_tensor(scaling, dtype=DTYPE)
    threshold_tensor = tf.convert_to_tensor(convergence_threshold, dtype=DTYPE)
    max_iterations_tensor = tf.convert_to_tensor(max_iterations, dtype=tf.int32)
    num_particles_tensor = tf.shape(x)[1]
    if transport_plan_mode == "streaming":
        transport_matrix = tf.zeros([batch_size, 0, 0], dtype=DTYPE)
        (
            transported,
            _iterations,
            row_residual,
            column_residual,
        ) = _filterflow_streaming_transport(
            scaled_x,
            x,
            logw,
            epsilon_tensor,
            scaling_tensor,
            threshold_tensor,
            max_iterations_tensor,
            num_particles_tensor,
            row_chunk_size=row_chunk_size,
            col_chunk_size=col_chunk_size,
            transport_ad_mode=transport_ad_mode,
            warmstart_state=warmstart_state,
        )
    elif transport_gradient_mode == "filterflow_custom_op":
        transport_matrix, _iterations = _filterflow_custom_gradient_transport_matrix(
            scaled_x,
            logw,
            epsilon_tensor,
            scaling_tensor,
            threshold_tensor,
            max_iterations_tensor,
            num_particles_tensor,
        )
        transported = tf.linalg.matmul(transport_matrix, x)
        row_residual = tf.reduce_max(tf.abs(tf.reduce_sum(transport_matrix, axis=2) - 1.0))
        source_weights = tf.exp(logw)
        column_mass = tf.reduce_sum(transport_matrix, axis=1)
        column_target = source_weights * tf.cast(num_particles, DTYPE)
        column_residual = tf.reduce_max(tf.abs(column_mass - column_target))
    else:
        transport_matrix, _iterations = _filterflow_exact_transport_matrix(
            scaled_x,
            logw,
            epsilon_tensor,
            scaling_tensor,
            threshold_tensor,
            max_iterations_tensor,
            num_particles_tensor,
            transport_ad_mode=transport_ad_mode,
            warmstart_state=warmstart_state,
        )
        if transport_gradient_mode == "filterflow_clipped":
            transport_matrix = _clip_transport_upstream_gradient(transport_matrix)
        transported = tf.linalg.matmul(transport_matrix, x)
        row_residual = tf.reduce_max(tf.abs(tf.reduce_sum(transport_matrix, axis=2) - 1.0))
        source_weights = tf.exp(logw)
        column_mass = tf.reduce_sum(transport_matrix, axis=1)
        column_target = source_weights * tf.cast(num_particles, DTYPE)
        column_residual = tf.reduce_max(tf.abs(column_mass - column_target))
    uniform_log = uniform_log_weights(batch_size, num_particles)
    out_particles = tf.where(mask[:, None, None], transported, x)
    out_log_weights = tf.where(mask[:, None], uniform_log, logw)
    if transport_plan_mode == "dense":
        identity_transport = tf.tile(
            tf.eye(num_particles, dtype=DTYPE)[None, :, :],
            [batch_size, 1, 1],
        )
        out_transport = tf.where(mask[:, None, None], transport_matrix, identity_transport)
    else:
        out_transport = transport_matrix
    return BatchedAnnealedTransportTensors(
        particles=out_particles,
        log_weights=out_log_weights,
        transport_matrix=out_transport,
        max_row_residual=tf.cast(row_residual, DTYPE),
        max_column_residual=tf.cast(column_residual, DTYPE),
    )


def batched_ledh_pfpf_ot_value_core_tf(
    *,
    observations: tf.Tensor,
    initial_particles: tf.Tensor,
    pre_flow_particles: tf.Tensor,
    fixed_resampling_mask: tf.Tensor,
    transition_matrix: tf.Tensor,
    transition_covariance: tf.Tensor,
    observation_covariance: tf.Tensor,
    observation_fn: Callable[[tf.Tensor], tf.Tensor],
    observation_jacobian_fn: Callable[[tf.Tensor], tf.Tensor],
    observation_residual_fn: Callable[[tf.Tensor, tf.Tensor], tf.Tensor],
    transition_log_density_fn: Callable[[tf.Tensor, tf.Tensor, tf.Tensor], tf.Tensor],
    observation_log_density_fn: Callable[[tf.Tensor, tf.Tensor, tf.Tensor], tf.Tensor],
    initial_log_weights: tf.Tensor | None = None,
    sinkhorn_epsilon: float | tf.Tensor = 0.5,
    annealed_scaling: float | tf.Tensor = 0.9,
    annealed_convergence_threshold: float | tf.Tensor = 1.0e-3,
    sinkhorn_iterations: int | tf.Tensor = 80,
    ledh_jitter: float | tf.Tensor = 1.0e-9,
    transport_gradient_mode: str = "filterflow_clipped",
    transport_plan_mode: str = "dense",
    transport_ad_mode: str = "stabilized",
    row_chunk_size: int = DEFAULT_STREAMING_CHUNK_SIZE,
    col_chunk_size: int = DEFAULT_STREAMING_CHUNK_SIZE,
) -> BatchedLEDHPFPFOTValueTensors:
    """Run fixed-branch batched LEDH-PFPF-OT value recursion."""

    observations = _to_float_tensor(observations, "observations")
    particles = _to_float_tensor(initial_particles, "initial_particles")
    pre_flow_particles = _to_float_tensor(pre_flow_particles, "pre_flow_particles")
    fixed_resampling_mask = tf.convert_to_tensor(fixed_resampling_mask, dtype=tf.bool)
    _require_static_rank(observations, 2, "observations")
    _require_static_rank(particles, 3, "initial_particles")
    _require_static_rank(pre_flow_particles, 4, "pre_flow_particles")
    _require_static_rank(fixed_resampling_mask, 2, "fixed_resampling_mask")

    batch_size, num_particles, state_dim = _static_shape(particles, "initial_particles")
    time_steps, _observation_dim = _static_shape(observations, "observations")
    expected_pre_flow_shape = (batch_size, time_steps, num_particles, state_dim)
    pre_flow_shape = _static_shape(pre_flow_particles, "pre_flow_particles")
    if pre_flow_shape != expected_pre_flow_shape:
        raise ValueError(
            f"pre_flow_particles shape mismatch: got {pre_flow_shape}, "
            f"expected {expected_pre_flow_shape}"
        )
    mask_shape = _static_shape(fixed_resampling_mask, "fixed_resampling_mask")
    expected_mask_shape = (batch_size, time_steps)
    if mask_shape != expected_mask_shape:
        raise ValueError(
            f"fixed_resampling_mask shape mismatch: got {mask_shape}, "
            f"expected {expected_mask_shape}"
        )
    if initial_log_weights is None:
        log_weights = uniform_log_weights(batch_size, num_particles)
    else:
        log_weights = _to_float_tensor(initial_log_weights, "initial_log_weights")
        _require_static_rank(log_weights, 2, "initial_log_weights")
        weights_shape = _static_shape(log_weights, "initial_log_weights")
        expected_weights_shape = (batch_size, num_particles)
        if weights_shape != expected_weights_shape:
            raise ValueError(
                f"initial_log_weights shape mismatch: got {weights_shape}, "
                f"expected {expected_weights_shape}"
            )

    log_likelihood = tf.zeros([batch_size], dtype=DTYPE)
    means = []
    variances = []
    esses = []
    for t in range(time_steps):
        observation = observations[t]
        ancestors = particles
        pre_flow = pre_flow_particles[:, t, :, :]
        flow = batched_ledh_flow_core_tf(
            pre_flow_particles=pre_flow,
            ancestors=ancestors,
            observation=observation,
            transition_matrix=transition_matrix,
            transition_covariance=transition_covariance,
            observation_covariance=observation_covariance,
            observation_fn=observation_fn,
            observation_jacobian_fn=observation_jacobian_fn,
            observation_residual_fn=observation_residual_fn,
            jitter=ledh_jitter,
        )
        post_flow = flow.post_flow_particles
        target_transition = _to_float_tensor(
            transition_log_density_fn(post_flow, ancestors, tf.constant(t, dtype=tf.int32)),
            "transition_log_density_fn output",
        )
        target_observation = _to_float_tensor(
            observation_log_density_fn(post_flow, observation, tf.constant(t, dtype=tf.int32)),
            "observation_log_density_fn output",
        )
        _require_static_rank(target_transition, 2, "transition_log_density_fn output")
        _require_static_rank(target_observation, 2, "observation_log_density_fn output")
        expected_log_density_shape = (batch_size, num_particles)
        if _static_shape(target_transition, "transition_log_density_fn output") != (
            expected_log_density_shape
        ):
            raise ValueError("transition_log_density_fn output shape mismatch")
        if _static_shape(target_observation, "observation_log_density_fn output") != (
            expected_log_density_shape
        ):
            raise ValueError("observation_log_density_fn output shape mismatch")

        corrected_log_weights = (
            log_weights
            + target_transition
            + target_observation
            - flow.pre_flow_log_density
            + flow.forward_log_det
        )
        weights, incremental = _normalize_log_weights(corrected_log_weights)
        log_likelihood = log_likelihood + incremental
        ess = 1.0 / tf.reduce_sum(weights * weights, axis=1)
        mean, variance = _weighted_mean_and_variance(post_flow, weights)
        means.append(mean)
        variances.append(variance)
        esses.append(ess)

        transported = batched_annealed_transport_core_tf(
            post_flow,
            tf.math.log(tf.maximum(weights, _log_weight_floor())),
            fixed_resampling_mask[:, t],
            epsilon=sinkhorn_epsilon,
            scaling=annealed_scaling,
            convergence_threshold=annealed_convergence_threshold,
            max_iterations=sinkhorn_iterations,
            transport_gradient_mode=transport_gradient_mode,
            transport_plan_mode=transport_plan_mode,
            transport_ad_mode=transport_ad_mode,
            row_chunk_size=row_chunk_size,
            col_chunk_size=col_chunk_size,
        )
        particles = transported.particles
        log_weights = transported.log_weights

    return BatchedLEDHPFPFOTValueTensors(
        log_likelihood=log_likelihood,
        filtered_means=tf.stack(means, axis=0),
        filtered_variances=tf.stack(variances, axis=0),
        ess_by_time=tf.stack(esses, axis=0),
    )


def batched_ledh_pfpf_ot_value_and_score_tf(
    theta_batch: tf.Tensor,
    value_fn: Callable[[tf.Tensor], BatchedLEDHPFPFOTValueTensors | tf.Tensor],
) -> BatchedLEDHPFPFOTValueScoreTensors:
    """Differentiate a fixed relaxed batched LEDH-PFPF-OT objective.

    The returned score is the TensorFlow autodiff gradient of
    ``sum(value_fn(theta_batch))``.  It is not a categorical classical
    particle-filter likelihood score.
    """

    theta = _to_float_tensor(theta_batch, "theta_batch")
    _require_static_rank(theta, 2, "theta_batch")
    batch_size = _static_shape(theta, "theta_batch")[0]

    with tf.GradientTape() as tape:
        tape.watch(theta)
        value_result = value_fn(theta)
        if isinstance(value_result, BatchedLEDHPFPFOTValueTensors):
            value = value_result.log_likelihood
        else:
            value = _to_float_tensor(value_result, "value_fn output")
        _require_static_rank(value, 1, "value_fn output")
        _require_equal(_static_shape(value, "value_fn output")[0], batch_size, "value batch size")
        objective = tf.reduce_sum(value)

    score = tape.gradient(
        objective,
        theta,
        unconnected_gradients=tf.UnconnectedGradients.ZERO,
    )
    if score is None:
        score = tf.zeros_like(theta)

    return BatchedLEDHPFPFOTValueScoreTensors(
        log_likelihood=value,
        score=score,
    )


def assert_callback_has_no_forbidden_rng(
    callback: Callable[..., Any],
    *,
    name: str,
    allow_uninspectable: bool = False,
) -> None:
    """Reject callbacks whose source contains known RNG calls.

    This is a conservative contract check for deterministic fixtures.  It is
    not a proof that a callback is mathematically deterministic.
    """

    try:
        source = inspect.getsource(callback)
    except (OSError, TypeError) as exc:
        if allow_uninspectable:
            return
        raise ValueError(
            f"{name} callback source is not inspectable; hidden RNG cannot be ruled out"
        ) from exc
    for token in FORBIDDEN_RNG_SOURCE_TOKENS:
        if token in source:
            raise ValueError(f"{name} callback source contains forbidden RNG token {token!r}")


def _to_float_tensor(value: object, name: str) -> tf.Tensor:
    try:
        return tf.convert_to_tensor(value, dtype=DTYPE)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be convertible to a floating Tensor") from exc


def _log_weight_floor() -> tf.Tensor:
    """Small positive floor that remains representable for the active dtype."""

    if DTYPE == tf.float32:
        return tf.constant(1.0e-30, dtype=DTYPE)
    return tf.constant(1.0e-300, dtype=DTYPE)


def _require_static_rank(tensor: tf.Tensor, rank: int, name: str) -> None:
    if tensor.shape.rank != rank:
        raise ValueError(f"{name} must have static rank {rank}")


def _static_shape(tensor: tf.Tensor, name: str) -> tuple[int, ...]:
    shape = tensor.shape.as_list()
    if any(dim is None for dim in shape):
        raise ValueError(f"{name} must have fully static shape")
    return tuple(int(dim) for dim in shape)


def _require_equal(actual: int, expected: int, name: str) -> None:
    if actual != expected:
        raise ValueError(f"{name} mismatch: got {actual}, expected {expected}")


def _require_square_batch(tensor: tf.Tensor, batch_size: int, dim: int, name: str) -> None:
    shape = _static_shape(tensor, name)
    expected = (batch_size, dim, dim)
    if shape != expected:
        raise ValueError(f"{name} shape mismatch: got {shape}, expected {expected}")


def _tile_eye(batch_size: int, dim: int) -> tf.Tensor:
    return tf.tile(tf.eye(dim, dtype=DTYPE)[None, :, :], [batch_size, 1, 1])


def _stabilize_batch_covariance(
    covariance: object,
    jitter: float | tf.Tensor,
    name: str,
) -> tf.Tensor:
    matrix = _to_float_tensor(covariance, name)
    _require_static_rank(matrix, matrix.shape.rank or 0, name)
    if matrix.shape.rank is None or matrix.shape.rank < 2:
        raise ValueError(f"{name} must have rank at least 2")
    shape = matrix.shape.as_list()
    if shape[-1] is None or shape[-2] is None or shape[-1] != shape[-2]:
        raise ValueError(f"{name} must have static square trailing dimensions")
    sym = 0.5 * (matrix + tf.linalg.matrix_transpose(matrix))
    eigvals = tf.linalg.eigvalsh(sym)
    min_eig = tf.reduce_min(eigvals, axis=-1)
    jitter_tensor = tf.convert_to_tensor(jitter, dtype=DTYPE)
    needed = tf.maximum(jitter_tensor - min_eig, tf.zeros_like(min_eig))
    eye = tf.eye(int(shape[-1]), dtype=DTYPE)
    return sym + needed[..., None, None] * eye


def _batched_gaussian_logpdf(residuals: tf.Tensor, covariance: tf.Tensor) -> tf.Tensor:
    residuals = _to_float_tensor(residuals, "residuals")
    covariance = _to_float_tensor(covariance, "covariance")
    _require_static_rank(residuals, 3, "residuals")
    _require_static_rank(covariance, 3, "covariance")
    batch_size, _num_particles, dim = _static_shape(residuals, "residuals")
    _require_square_batch(covariance, batch_size, dim, "covariance")
    chol = tf.linalg.cholesky(covariance)
    solved = tf.linalg.matrix_transpose(
        tf.linalg.cholesky_solve(chol, tf.linalg.matrix_transpose(residuals))
    )
    quad = tf.reduce_sum(solved * residuals, axis=-1)
    logdet = 2.0 * tf.reduce_sum(tf.math.log(tf.linalg.diag_part(chol)), axis=-1)
    dim_tensor = tf.cast(dim, DTYPE)
    return -0.5 * (
        dim_tensor * tf.math.log(tf.constant(2.0 * 3.141592653589793, DTYPE))
        + logdet[:, None]
        + quad
    )


def _normalize_log_weights(log_weights: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
    log_weights = _to_float_tensor(log_weights, "log_weights")
    log_normalizer = tf.reduce_logsumexp(log_weights, axis=1)
    normalized_log_weights = log_weights - log_normalizer[:, None]
    return tf.exp(normalized_log_weights), log_normalizer


def _weighted_mean_and_variance(
    particles: tf.Tensor,
    weights: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    mean = tf.reduce_sum(particles * weights[:, :, None], axis=1)
    centered = particles - mean[:, None, :]
    variance = tf.reduce_sum(centered * centered * weights[:, :, None], axis=1)
    return mean, variance


def _require_observation_callback_shapes(
    *,
    h_ref: tf.Tensor,
    h_jac: tf.Tensor,
    residual: tf.Tensor,
    batch_size: int,
    num_particles: int,
    state_dim: int,
    observation_dim: int,
) -> None:
    expected_observation_shape = (batch_size, num_particles, observation_dim)
    for name, tensor in (
        ("observation_fn output", h_ref),
        ("observation_residual_fn output", residual),
    ):
        shape = _static_shape(tensor, name)
        if shape != expected_observation_shape:
            raise ValueError(
                f"{name} shape mismatch: got {shape}, expected {expected_observation_shape}"
            )
    jac_shape = _static_shape(h_jac, "observation_jacobian_fn output")
    expected_jac_shape = (batch_size, num_particles, observation_dim, state_dim)
    if jac_shape != expected_jac_shape:
        raise ValueError(
            "observation_jacobian_fn output shape mismatch: "
            f"got {jac_shape}, expected {expected_jac_shape}"
        )


def _require_flow_shapes(
    *,
    post_flow_particles: tf.Tensor,
    pre_flow_log_density: tf.Tensor,
    forward_log_det: tf.Tensor,
    local_posterior_means: tf.Tensor,
    local_posterior_covariances: tf.Tensor,
) -> None:
    batch_size, num_particles, state_dim = _static_shape(
        post_flow_particles,
        "post_flow_particles",
    )
    _require_equal(
        _static_shape(pre_flow_log_density, "pre_flow_log_density")[0],
        batch_size,
        "pre_flow_log_density batch size",
    )
    _require_equal(
        _static_shape(pre_flow_log_density, "pre_flow_log_density")[1],
        num_particles,
        "pre_flow_log_density particle count",
    )
    _require_equal(
        _static_shape(forward_log_det, "forward_log_det")[0],
        batch_size,
        "forward_log_det batch size",
    )
    _require_equal(
        _static_shape(forward_log_det, "forward_log_det")[1],
        num_particles,
        "forward_log_det particle count",
    )
    _require_equal(
        _static_shape(local_posterior_means, "local_posterior_means")[0],
        batch_size,
        "local_posterior_means batch size",
    )
    _require_equal(
        _static_shape(local_posterior_means, "local_posterior_means")[1],
        num_particles,
        "local_posterior_means particle count",
    )
    _require_equal(
        _static_shape(local_posterior_means, "local_posterior_means")[2],
        state_dim,
        "local_posterior_means state dim",
    )
    cov_shape = _static_shape(local_posterior_covariances, "local_posterior_covariances")
    expected_cov_shape = (batch_size, num_particles, state_dim, state_dim)
    if cov_shape != expected_cov_shape:
        raise ValueError(
            "local_posterior_covariances shape mismatch: "
            f"got {cov_shape}, expected {expected_cov_shape}"
        )
