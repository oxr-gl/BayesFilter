"""Generic batch-native value/score target helpers.

This module factors the reviewed value/score custom-gradient pattern out of
HMC-specific code.  It is intentionally small: adapters must already expose a
true batched ``log_prob_and_grad`` implementation for rank-2 positions.  The
helpers fail closed instead of hiding scalar row loops in the runtime layer.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any, Literal

import tensorflow as tf

from bayesfilter.inference.posterior_adapter import (
    ValueScoreCapability,
    value_score_capability,
)


BatchValueScoreRank = Literal["scalar", "batch"]

NONCLAIMS = (
    "target value/score helper only",
    "no HMC tuning or sampling claim",
    "no full-chain XLA readiness claim",
    "no posterior convergence claim",
    "no scientific validity claim",
)

_GRAPH_NATIVE_AUTHORITIES = frozenset(
    {
        "graph_native",
        "reviewed_gradient_tape_xla_exception",
    }
)


@dataclass(frozen=True)
class BatchValueScoreMetadata:
    """Shape and authority metadata for a batch-native value/score call."""

    rank: BatchValueScoreRank
    batch_size: int | None
    parameter_dim: int
    value_score_authority: str
    runtime_backend: str
    target_scope: str | None
    nonclaims: tuple[str, ...] = NONCLAIMS


@dataclass(frozen=True)
class BatchValueScoreResult:
    """Value/score tensors plus explicit non-HMC metadata."""

    value: tf.Tensor
    score: tf.Tensor
    metadata: BatchValueScoreMetadata
    diagnostics: Mapping[str, Any]


def _static_rank_and_dim(theta: tf.Tensor) -> tuple[BatchValueScoreRank, int | None, int]:
    if theta.shape.rank == 1:
        parameter_dim = theta.shape[-1]
        if parameter_dim is None:
            raise ValueError("scalar theta must have static parameter dimension")
        return "scalar", None, int(parameter_dim)
    if theta.shape.rank == 2:
        batch_size = theta.shape[0]
        parameter_dim = theta.shape[1]
        if batch_size is None or parameter_dim is None:
            raise ValueError("batched theta must have static batch and parameter dimensions")
        return "batch", int(batch_size), int(parameter_dim)
    raise ValueError("theta must have rank 1 [parameter] or rank 2 [batch, parameter]")


def _validate_value_score_shapes(
    *,
    theta: tf.Tensor,
    value: tf.Tensor,
    score: tf.Tensor,
) -> tuple[BatchValueScoreRank, int | None, int]:
    rank, batch_size, parameter_dim = _static_rank_and_dim(theta)
    if rank == "scalar":
        if value.shape.rank not in (0, None):
            raise ValueError("scalar target value must be rank 0")
        if score.shape.rank != 1:
            raise ValueError("scalar target score must have rank 1")
        if score.shape[-1] is not None and int(score.shape[-1]) != parameter_dim:
            raise ValueError("scalar target score parameter dimension mismatch")
    else:
        if value.shape.rank != 1:
            raise ValueError("batched target value must have rank 1")
        if score.shape.rank != 2:
            raise ValueError("batched target score must have rank 2")
        if value.shape[0] is not None and int(value.shape[0]) != batch_size:
            raise ValueError("batched target value leading dimension mismatch")
        if score.shape[0] is not None and int(score.shape[0]) != batch_size:
            raise ValueError("batched target score leading dimension mismatch")
        if score.shape[1] is not None and int(score.shape[1]) != parameter_dim:
            raise ValueError("batched target score parameter dimension mismatch")
    return rank, batch_size, parameter_dim


def _broadcast_upstream_gradient_to_score(dy: Any, score: tf.Tensor) -> tf.Tensor:
    """Broadcast target upstream gradients over trailing parameter axes only."""

    score_tensor = tf.convert_to_tensor(score)
    upstream = tf.cast(dy, score_tensor.dtype)
    upstream_shape = upstream.shape
    score_shape = score_tensor.shape
    if upstream_shape.rank is not None and score_shape.rank is not None:
        if upstream_shape.rank > score_shape.rank:
            raise ValueError("target upstream gradient rank exceeds score rank")
        for idx, dim in enumerate(upstream_shape.as_list()):
            score_dim = score_shape[idx]
            if dim is not None and score_dim is not None and int(dim) != int(score_dim):
                raise ValueError(
                    "target upstream gradient leading dimensions must match score"
                )
        if upstream_shape.rank == score_shape.rank:
            return upstream
        return tf.reshape(
            upstream,
            tf.concat(
                [
                    tf.shape(upstream),
                    tf.ones([score_shape.rank - upstream_shape.rank], dtype=tf.int32),
                ],
                axis=0,
            ),
        )
    rank_delta = tf.rank(score_tensor) - tf.rank(upstream)
    with tf.control_dependencies(
        [
            tf.debugging.assert_greater_equal(
                rank_delta,
                0,
                message="target upstream gradient rank exceeds score rank",
            ),
            tf.debugging.assert_equal(
                tf.shape(upstream),
                tf.shape(score_tensor)[: tf.rank(upstream)],
                message="target upstream gradient leading dimensions must match score",
            ),
        ]
    ):
        return tf.reshape(
            upstream,
            tf.concat([tf.shape(upstream), tf.ones([rank_delta], dtype=tf.int32)], axis=0),
        )


def reviewed_value_score_target_fn(
    adapter: Any,
    *,
    dtype: Any = tf.float64,
    require_batched: bool = False,
) -> Callable[[Any], tf.Tensor]:
    """Return a custom-gradient target value function backed by adapter scores.

    The adapter must expose ``log_prob_and_grad(theta)``.  If
    ``require_batched=True``, the returned function fails closed for rank-1
    inputs so callers cannot accidentally use a scalar-only path where a
    batch-native target is required.
    """

    if not hasattr(adapter, "log_prob_and_grad"):
        raise TypeError("adapter must expose log_prob_and_grad")

    def target_value(theta: Any) -> tf.Tensor:
        values = tf.convert_to_tensor(theta, dtype=dtype)
        if require_batched and values.shape.rank != 2:
            raise ValueError("batch-native target requires rank 2 theta [batch, parameter]")

        @tf.custom_gradient
        def value_with_reviewed_score(x: tf.Tensor) -> tuple[tf.Tensor, Callable[[Any], tf.Tensor]]:
            value, score = adapter.log_prob_and_grad(x)
            value_tensor = tf.cast(tf.convert_to_tensor(value), dtype)
            score_tensor = tf.cast(tf.convert_to_tensor(score), dtype)
            _validate_value_score_shapes(theta=x, value=value_tensor, score=score_tensor)

            def grad(dy: Any) -> tf.Tensor:
                upstream = _broadcast_upstream_gradient_to_score(dy, score_tensor)
                return upstream * score_tensor

            return value_tensor, grad

        return value_with_reviewed_score(values)

    return target_value


def evaluate_batch_native_value_score(
    adapter: Any,
    theta: Any,
    *,
    dtype: Any = tf.float64,
    require_batched: bool = True,
) -> BatchValueScoreResult:
    """Evaluate an adapter value/score path with strict shape metadata.

    This helper calls the adapter once with the supplied tensor.  It does not
    loop over rows and does not provide a scalar fallback.  Use it when a phase
    needs evidence that the adapter itself accepts batch-shaped positions.
    """

    if not hasattr(adapter, "log_prob_and_grad"):
        raise TypeError("adapter must expose log_prob_and_grad")
    theta_tensor = tf.cast(tf.convert_to_tensor(theta), dtype)
    if require_batched and theta_tensor.shape.rank != 2:
        raise ValueError("batch-native value/score requires rank 2 theta")
    value, score = adapter.log_prob_and_grad(theta_tensor)
    value_tensor = tf.cast(tf.convert_to_tensor(value), dtype)
    score_tensor = tf.cast(tf.convert_to_tensor(score), dtype)
    rank, batch_size, parameter_dim = _validate_value_score_shapes(
        theta=theta_tensor,
        value=value_tensor,
        score=score_tensor,
    )
    capability: ValueScoreCapability = value_score_capability(adapter)
    return BatchValueScoreResult(
        value=value_tensor,
        score=score_tensor,
        metadata=BatchValueScoreMetadata(
            rank=rank,
            batch_size=batch_size,
            parameter_dim=parameter_dim,
            value_score_authority=capability.value_score_authority,
            runtime_backend=capability.runtime_backend,
            target_scope=capability.target_scope,
        ),
        diagnostics={
            "path": "batch_native_adapter_log_prob_and_grad",
            "require_batched": bool(require_batched),
            "xla_hmc_ready": bool(capability.xla_hmc_ready),
            "accepted_target_xla_authority": bool(
                capability.is_accepted_xla_hmc_authority
            ),
            "full_chain_xla_diagnostic_ready": bool(
                capability.full_chain_xla_diagnostic_ready
            ),
        },
    )


class LatentAffineBatchValueScoreAdapter:
    """Batch-native latent affine value/score wrapper for HMC targets.

    The wrapped target lives in position coordinates ``theta`` while HMC may run
    in latent row-vector coordinates ``z``.  For BayesFilter mass artifacts the
    transform is

    ``theta = center + z @ factor.T``

    and the score maps by the row-vector chain rule

    ``grad_z = grad_theta @ factor``.

    Rank-2 inputs are delegated to the base adapter once.  This class does not
    provide a Python row loop, ``tf.map_fn``, or scalar fallback for batched
    inputs; scalar-only base adapters fail through the shared value/score shape
    validators.
    """

    def __init__(
        self,
        *,
        base_adapter: Any,
        transform: Any,
        target_scope: str,
        runtime_backend: str = "bayesfilter.inference.LatentAffineBatchValueScoreAdapter",
        evidence_path: str | None = None,
        xla_hmc_ready: bool = False,
        full_chain_xla_diagnostic_ready: bool = False,
        nonclaims: tuple[str, ...] = NONCLAIMS,
    ) -> None:
        if not hasattr(base_adapter, "log_prob_and_grad"):
            raise TypeError("base_adapter must expose log_prob_and_grad")
        self.base_adapter = base_adapter
        self.transform = transform
        self.parameter_dim = int(transform.dimension)
        self.target_scope = str(target_scope)
        if not self.target_scope:
            raise ValueError("target_scope must be non-empty")
        self.runtime_backend = str(runtime_backend)
        self.evidence_path = evidence_path
        self.xla_hmc_ready = bool(xla_hmc_ready)
        self.full_chain_xla_diagnostic_ready = bool(full_chain_xla_diagnostic_ready)
        self.nonclaims = tuple(str(item) for item in nonclaims) or NONCLAIMS

    def value_score_capability(self) -> ValueScoreCapability:
        base_capability = value_score_capability(self.base_adapter)
        graph_native_base = base_capability.value_score_authority in _GRAPH_NATIVE_AUTHORITIES
        authority = base_capability.value_score_authority
        xla_ready = bool(
            self.xla_hmc_ready
            and graph_native_base
            and base_capability.is_accepted_xla_hmc_authority
        )
        full_chain_ready = bool(
            self.full_chain_xla_diagnostic_ready
            and xla_ready
            and base_capability.is_accepted_full_chain_xla_diagnostic_authority
        )
        nonclaims = self.nonclaims + (
            f"base value/score authority: {base_capability.value_score_authority}",
            "latent wrapper cannot promote fallback base authority",
        )
        return ValueScoreCapability(
            value_score_authority=authority,
            xla_hmc_ready=xla_ready,
            full_chain_xla_diagnostic_ready=full_chain_ready,
            runtime_backend=self.runtime_backend,
            evidence_path=self.evidence_path,
            target_scope=self.target_scope,
            nonclaims=nonclaims,
        )

    def initial_position(self) -> tf.Tensor:
        return tf.zeros((self.parameter_dim,), dtype=tf.float64)

    def latent_to_position(self, z: Any) -> tf.Tensor:
        z_tensor = self._validate_latent_tensor(z, allow_sample_axes=True)
        center = tf.convert_to_tensor(self.transform.center, dtype=z_tensor.dtype)
        factor = tf.convert_to_tensor(self.transform.factor, dtype=z_tensor.dtype)
        return center + tf.tensordot(z_tensor, factor, axes=[[-1], [1]])

    def theta_score_to_latent_score(self, theta_score: Any) -> tf.Tensor:
        score_tensor = self._validate_position_tensor(
            theta_score,
            allow_sample_axes=True,
        )
        factor = tf.convert_to_tensor(self.transform.factor, dtype=score_tensor.dtype)
        return tf.tensordot(score_tensor, factor, axes=[[-1], [0]])

    def log_prob_and_grad(self, z: Any) -> tuple[tf.Tensor, tf.Tensor]:
        z_tensor = self._validate_latent_tensor(z)
        theta = self.latent_to_position(z_tensor)
        value, theta_score = self.base_adapter.log_prob_and_grad(theta)
        value_tensor = tf.convert_to_tensor(value, dtype=z_tensor.dtype)
        theta_score_tensor = tf.convert_to_tensor(theta_score, dtype=z_tensor.dtype)
        _validate_value_score_shapes(theta=theta, value=value_tensor, score=theta_score_tensor)
        return value_tensor, self.theta_score_to_latent_score(theta_score_tensor)

    def target_status_telemetry(self, z: Any) -> Mapping[str, Any]:
        """Return base-target telemetry after applying the latent transform.

        HMC trace collection is owned by BayesFilter, while model-specific
        target status is owned by the wrapped adapter.  This method is an
        explicit bridge for retained-chain-step telemetry; it does not change
        value/score semantics and fails closed when the base adapter lacks the
        reviewed telemetry method.
        """

        telemetry = getattr(self.base_adapter, "target_status_telemetry", None)
        if not callable(telemetry):
            raise TypeError("base_adapter must expose target_status_telemetry")
        z_tensor = self._validate_latent_tensor(z)
        theta = self.latent_to_position(z_tensor)
        payload = telemetry(theta)
        if not isinstance(payload, Mapping):
            raise TypeError("target_status_telemetry must return a mapping")
        return payload

    def _validate_latent_tensor(
        self,
        value: Any,
        *,
        allow_sample_axes: bool = False,
    ) -> tf.Tensor:
        tensor = tf.convert_to_tensor(value, dtype=tf.float64)
        return self._validate_trailing_dimension(
            tensor,
            "latent coordinate",
            allow_sample_axes=allow_sample_axes,
        )

    def _validate_position_tensor(
        self,
        value: Any,
        *,
        allow_sample_axes: bool = False,
    ) -> tf.Tensor:
        tensor = tf.convert_to_tensor(value, dtype=tf.float64)
        return self._validate_trailing_dimension(
            tensor,
            "position/score",
            allow_sample_axes=allow_sample_axes,
        )

    def _validate_trailing_dimension(
        self,
        tensor: tf.Tensor,
        label: str,
        *,
        allow_sample_axes: bool = False,
    ) -> tf.Tensor:
        min_rank = 1
        max_rank = None if allow_sample_axes else 2
        if tensor.shape.rank is None:
            raise ValueError(f"{label} tensor must have static rank")
        if tensor.shape.rank < min_rank or (
            max_rank is not None and tensor.shape.rank > max_rank
        ):
            if allow_sample_axes:
                raise ValueError(
                    f"{label} tensor must have rank at least 1 with trailing parameter dimension"
                )
            raise ValueError(f"{label} tensor must have rank 1 or rank 2")
        trailing = tensor.shape[-1]
        if trailing is None:
            raise ValueError(f"{label} tensor must have static trailing dimension")
        if int(trailing) != self.parameter_dim:
            raise ValueError(f"{label} trailing dimension must match transform dimension")
        return tensor
