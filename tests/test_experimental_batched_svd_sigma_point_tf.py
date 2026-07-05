from __future__ import annotations

import os
from types import SimpleNamespace

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

from bayesfilter.nonlinear.experimental_batched_svd_sigma_point_tf import (
    TFBatchedStructuralFirstDerivatives,
    TFBatchedStructuralStateSpace,
    _checked_batched_principal_sqrt_factor_first_derivatives,
    tf_batched_svd_sigma_point_value_and_score,
)
from docs.benchmarks.benchmark_experimental_batched_svd_sigma_point_cpu_gpu import (
    _batched_model_and_derivatives,
    _scalar_model_and_derivatives,
    _scalar_score,
    _stable_fixture,
    _to_tensors,
)


BACKENDS = ("tf_svd_ukf", "tf_svd_cubature")
OLD_BACKENDS = ("tf_svd_ukf", "tf_svd_cubature", "tf_svd_cut4")


def _args() -> SimpleNamespace:
    return SimpleNamespace(
        placement_floor=0.0,
        innovation_floor=1.0e-12,
        rank_tolerance=1.0e-12,
        spectral_gap_tolerance=1.0e-10,
        fixed_null_tolerance=1.0e-10,
        jitter=0.0,
    )


def _fixture(*, batch_size: int = 3, time_steps: int = 5) -> dict[str, tf.Tensor]:
    return _to_tensors(
        _stable_fixture(
            batch_size=batch_size,
            time_steps=time_steps,
            state_dim=2,
            obs_dim=2,
            parameter_dim=2,
        )
    )


def _value_and_score(
    tensors: dict[str, tf.Tensor],
    *,
    backend: str,
) -> tuple[tf.Tensor, tf.Tensor]:
    model, derivatives = _batched_model_and_derivatives(tensors)
    value, score, _diagnostics = tf_batched_svd_sigma_point_value_and_score(
        tensors["observations"],
        model,
        derivatives,
        backend=backend,
        placement_floor=tf.constant(0.0, dtype=tf.float64),
        innovation_floor=tf.constant(1.0e-12, dtype=tf.float64),
        rank_tolerance=tf.constant(1.0e-12, dtype=tf.float64),
        spectral_gap_tolerance=tf.constant(1.0e-10, dtype=tf.float64),
        fixed_null_tolerance=tf.constant(1.0e-10, dtype=tf.float64),
        jitter=tf.constant(0.0, dtype=tf.float64),
    )
    return value, score


def _value_score_diagnostics(
    tensors: dict[str, tf.Tensor],
    *,
    backend: str,
) -> tuple[tf.Tensor, tf.Tensor, dict[str, tf.Tensor]]:
    model, derivatives = _batched_model_and_derivatives(tensors)
    value, score, diagnostics = tf_batched_svd_sigma_point_value_and_score(
        tensors["observations"],
        model,
        derivatives,
        backend=backend,
        placement_floor=tf.constant(0.0, dtype=tf.float64),
        innovation_floor=tf.constant(1.0e-12, dtype=tf.float64),
        rank_tolerance=tf.constant(1.0e-12, dtype=tf.float64),
        spectral_gap_tolerance=tf.constant(1.0e-10, dtype=tf.float64),
        fixed_null_tolerance=tf.constant(1.0e-10, dtype=tf.float64),
        jitter=tf.constant(0.0, dtype=tf.float64),
    )
    return value, score, dict(diagnostics)


def _repeated_positive_model_and_derivatives() -> tuple[
    tf.Tensor,
    TFBatchedStructuralStateSpace,
    TFBatchedStructuralFirstDerivatives,
]:
    batch_size = 2
    parameter_dim = 1
    state_dim = 1
    innovation_dim = 1
    observation_dim = 1
    observations = tf.constant([[0.0]], dtype=tf.float64)

    def transition(previous: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        return previous + innovation

    def observe(states: tf.Tensor) -> tf.Tensor:
        return states

    def transition_state_jacobian(
        previous: tf.Tensor,
        innovation: tf.Tensor,
    ) -> tf.Tensor:
        del innovation
        return tf.ones(
            [tf.shape(previous)[0], tf.shape(previous)[1], state_dim, state_dim],
            dtype=tf.float64,
        )

    def transition_innovation_jacobian(
        previous: tf.Tensor,
        innovation: tf.Tensor,
    ) -> tf.Tensor:
        del previous
        return tf.ones(
            [tf.shape(innovation)[0], tf.shape(innovation)[1], state_dim, innovation_dim],
            dtype=tf.float64,
        )

    def d_transition(previous: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        return tf.zeros(
            [tf.shape(previous)[0], parameter_dim, tf.shape(previous)[1], state_dim],
            dtype=tf.float64,
        )

    def observation_state_jacobian(states: tf.Tensor) -> tf.Tensor:
        return tf.ones(
            [tf.shape(states)[0], tf.shape(states)[1], observation_dim, state_dim],
            dtype=tf.float64,
        )

    def d_observation(states: tf.Tensor) -> tf.Tensor:
        return tf.zeros(
            [tf.shape(states)[0], parameter_dim, tf.shape(states)[1], observation_dim],
            dtype=tf.float64,
        )

    model = TFBatchedStructuralStateSpace(
        initial_mean=tf.zeros([batch_size, state_dim], dtype=tf.float64),
        initial_covariance=tf.ones([batch_size, state_dim, state_dim], dtype=tf.float64),
        innovation_covariance=tf.ones([batch_size, innovation_dim, innovation_dim], dtype=tf.float64),
        observation_covariance=tf.ones([batch_size, observation_dim, observation_dim], dtype=tf.float64),
        transition_fn=transition,
        observation_fn=observe,
    )
    derivatives = TFBatchedStructuralFirstDerivatives(
        d_initial_mean=tf.zeros([batch_size, parameter_dim, state_dim], dtype=tf.float64),
        d_initial_covariance=tf.zeros(
            [batch_size, parameter_dim, state_dim, state_dim],
            dtype=tf.float64,
        ),
        d_innovation_covariance=tf.zeros(
            [batch_size, parameter_dim, innovation_dim, innovation_dim],
            dtype=tf.float64,
        ),
        d_observation_covariance=tf.zeros(
            [batch_size, parameter_dim, observation_dim, observation_dim],
            dtype=tf.float64,
        ),
        transition_state_jacobian_fn=transition_state_jacobian,
        transition_innovation_jacobian_fn=transition_innovation_jacobian,
        d_transition_fn=d_transition,
        observation_state_jacobian_fn=observation_state_jacobian,
        d_observation_fn=d_observation,
    )
    return observations, model, derivatives


def _repeated_positive_innovation_model_and_derivatives() -> tuple[
    tf.Tensor,
    TFBatchedStructuralStateSpace,
    TFBatchedStructuralFirstDerivatives,
]:
    batch_size = 2
    parameter_dim = 1
    state_dim = 2
    innovation_dim = 2
    observation_dim = 2
    observations = tf.constant([[0.0, 0.0]], dtype=tf.float64)
    inverse_sqrt_two = tf.constant(1.0 / np.sqrt(2.0), dtype=tf.float64)

    def transition(previous: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        del innovation
        return tf.stack(
            [
                previous[:, :, 0],
                inverse_sqrt_two * previous[:, :, 1],
            ],
            axis=2,
        )

    def observe(states: tf.Tensor) -> tf.Tensor:
        return states

    def transition_state_jacobian(
        previous: tf.Tensor,
        innovation: tf.Tensor,
    ) -> tf.Tensor:
        del innovation
        jacobian = tf.constant(
            [
                [1.0, 0.0],
                [0.0, 1.0 / np.sqrt(2.0)],
            ],
            dtype=tf.float64,
        )
        return tf.broadcast_to(
            jacobian[tf.newaxis, tf.newaxis, :, :],
            [tf.shape(previous)[0], tf.shape(previous)[1], state_dim, state_dim],
        )

    def transition_innovation_jacobian(
        previous: tf.Tensor,
        innovation: tf.Tensor,
    ) -> tf.Tensor:
        del innovation
        return tf.zeros(
            [tf.shape(previous)[0], tf.shape(previous)[1], state_dim, innovation_dim],
            dtype=tf.float64,
        )

    def d_transition(previous: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        del innovation
        return tf.zeros(
            [tf.shape(previous)[0], parameter_dim, tf.shape(previous)[1], state_dim],
            dtype=tf.float64,
        )

    def observation_state_jacobian(states: tf.Tensor) -> tf.Tensor:
        return tf.broadcast_to(
            tf.eye(observation_dim, dtype=tf.float64)[tf.newaxis, tf.newaxis, :, :],
            [batch_size, tf.shape(states)[1], observation_dim, state_dim],
        )

    def d_observation(states: tf.Tensor) -> tf.Tensor:
        return tf.zeros(
            [batch_size, parameter_dim, tf.shape(states)[1], observation_dim],
            dtype=tf.float64,
        )

    model = TFBatchedStructuralStateSpace(
        initial_mean=tf.zeros([batch_size, state_dim], dtype=tf.float64),
        initial_covariance=tf.broadcast_to(
            tf.linalg.diag(tf.constant([1.0, 2.0], dtype=tf.float64)),
            [batch_size, state_dim, state_dim],
        ),
        innovation_covariance=tf.broadcast_to(
            tf.linalg.diag(tf.constant([3.0, 4.0], dtype=tf.float64)),
            [batch_size, innovation_dim, innovation_dim],
        ),
        observation_covariance=tf.zeros([batch_size, observation_dim, observation_dim], dtype=tf.float64),
        transition_fn=transition,
        observation_fn=observe,
    )
    derivatives = TFBatchedStructuralFirstDerivatives(
        d_initial_mean=tf.zeros([batch_size, parameter_dim, state_dim], dtype=tf.float64),
        d_initial_covariance=tf.zeros(
            [batch_size, parameter_dim, state_dim, state_dim],
            dtype=tf.float64,
        ),
        d_innovation_covariance=tf.zeros(
            [batch_size, parameter_dim, innovation_dim, innovation_dim],
            dtype=tf.float64,
        ),
        d_observation_covariance=tf.zeros(
            [batch_size, parameter_dim, observation_dim, observation_dim],
            dtype=tf.float64,
        ),
        transition_state_jacobian_fn=transition_state_jacobian,
        transition_innovation_jacobian_fn=transition_innovation_jacobian,
        d_transition_fn=d_transition,
        observation_state_jacobian_fn=observation_state_jacobian,
        d_observation_fn=d_observation,
    )
    return observations, model, derivatives


def _scalar_rows(
    tensors: dict[str, tf.Tensor],
    *,
    backend: str,
) -> tuple[tf.Tensor, tf.Tensor]:
    values = []
    scores = []
    batch_size = int(tensors["initial_mean"].shape[0])
    for row in range(batch_size):
        model, derivatives = _scalar_model_and_derivatives(tensors, row)
        value, score = _scalar_score(
            tensors["observations"],
            model,
            derivatives,
            backend=backend,
            args=_args(),
        )
        values.append(value)
        scores.append(score)
    return (
        tf.constant(values, dtype=tf.float64),
        tf.constant(np.stack(scores, axis=0), dtype=tf.float64),
    )


def _permute_tensors(
    tensors: dict[str, tf.Tensor],
    permutation: tf.Tensor,
) -> dict[str, tf.Tensor]:
    permuted = {}
    for name, tensor in tensors.items():
        if name == "observations":
            permuted[name] = tensor
        else:
            permuted[name] = tf.gather(tensor, permutation, axis=0)
    return permuted


@pytest.mark.parametrize("backend", BACKENDS)
def test_experimental_batched_svd_value_and_score_matches_scalar_rows(
    backend: str,
) -> None:
    tensors = _fixture()
    batched_value, batched_score = _value_and_score(tensors, backend=backend)
    scalar_value, scalar_score = _scalar_rows(tensors, backend=backend)

    np.testing.assert_allclose(
        batched_value.numpy(),
        scalar_value.numpy(),
        rtol=1.0e-8,
        atol=1.0e-8,
    )
    np.testing.assert_allclose(
        batched_score.numpy(),
        scalar_score.numpy(),
        rtol=1.0e-7,
        atol=1.0e-7,
    )


@pytest.mark.parametrize("backend", BACKENDS)
def test_experimental_batched_svd_singleton_matches_scalar_row(backend: str) -> None:
    tensors = _fixture(batch_size=1)
    batched_value, batched_score = _value_and_score(tensors, backend=backend)
    scalar_value, scalar_score = _scalar_rows(tensors, backend=backend)

    np.testing.assert_allclose(batched_value.numpy(), scalar_value.numpy(), atol=1.0e-8)
    np.testing.assert_allclose(
        batched_score.numpy(),
        scalar_score.numpy(),
        rtol=1.0e-7,
        atol=1.0e-7,
    )


@pytest.mark.parametrize("backend", BACKENDS)
def test_experimental_batched_svd_row_permutation_preserves_order(
    backend: str,
) -> None:
    tensors = _fixture()
    base_value, base_score = _value_and_score(tensors, backend=backend)
    permutation = tf.constant([2, 0, 1], dtype=tf.int32)
    permuted_value, permuted_score = _value_and_score(
        _permute_tensors(tensors, permutation),
        backend=backend,
    )

    np.testing.assert_allclose(
        permuted_value.numpy(),
        tf.gather(base_value, permutation).numpy(),
        atol=1.0e-8,
    )
    np.testing.assert_allclose(
        permuted_score.numpy(),
        tf.gather(base_score, permutation).numpy(),
        rtol=1.0e-7,
        atol=1.0e-7,
    )


@pytest.mark.parametrize("backend", BACKENDS)
def test_experimental_batched_svd_graph_and_cpu_xla_parity(backend: str) -> None:
    tensors = _fixture(batch_size=2, time_steps=3)
    eager_value, eager_score = _value_and_score(tensors, backend=backend)

    @tf.function(reduce_retracing=True)
    def graph_call() -> tuple[tf.Tensor, tf.Tensor]:
        return _value_and_score(tensors, backend=backend)

    @tf.function(jit_compile=True, reduce_retracing=True)
    def xla_call() -> tuple[tf.Tensor, tf.Tensor]:
        return _value_and_score(tensors, backend=backend)

    graph_value, graph_score = graph_call()
    xla_value, xla_score = xla_call()

    np.testing.assert_allclose(graph_value.numpy(), eager_value.numpy(), atol=1.0e-8)
    np.testing.assert_allclose(
        graph_score.numpy(),
        eager_score.numpy(),
        rtol=1.0e-7,
        atol=1.0e-7,
    )
    np.testing.assert_allclose(xla_value.numpy(), eager_value.numpy(), atol=1.0e-8)
    np.testing.assert_allclose(
        xla_score.numpy(),
        eager_score.numpy(),
        rtol=1.0e-7,
        atol=1.0e-7,
    )


def test_experimental_batched_svd_shape_mismatch_fails_closed() -> None:
    tensors = _fixture()
    bad_tensors = dict(tensors)
    bad_tensors["d_initial_mean"] = bad_tensors["d_initial_mean"][:2]

    with pytest.raises(ValueError, match="has shape|expected|derivative batch dimension"):
        _batched_model_and_derivatives(bad_tensors)


def test_experimental_batched_svd_cpu_only_hides_gpu() -> None:
    assert os.environ.get("CUDA_VISIBLE_DEVICES") == "-1"
    assert tf.config.list_physical_devices("GPU") == []


def test_principal_sqrt_helper_repeated_positive_reconstructs_derivative() -> None:
    covariance = tf.eye(3, batch_shape=[2], dtype=tf.float64)
    d_covariance = tf.constant(
        [
            [
                [[0.5, 0.1, -0.2], [0.1, -0.3, 0.4], [-0.2, 0.4, 0.7]],
                [[1.0, 0.0, 0.2], [0.0, 0.6, -0.1], [0.2, -0.1, 0.8]],
            ],
            [
                [[0.2, -0.2, 0.3], [-0.2, 0.9, 0.0], [0.3, 0.0, -0.4]],
                [[0.4, 0.5, 0.0], [0.5, 0.1, -0.3], [0.0, -0.3, 0.2]],
            ],
        ],
        dtype=tf.float64,
    )

    placement = _checked_batched_principal_sqrt_factor_first_derivatives(
        covariance,
        d_covariance,
        singular_floor=tf.constant(0.0, dtype=tf.float64),
        fixed_null_tolerance=tf.constant(1.0e-10, dtype=tf.float64),
        label="test repeated-positive placement",
    )
    lyapunov = (
        placement.factor[:, tf.newaxis, :, :] @ placement.d_factor
        + placement.d_factor @ placement.factor[:, tf.newaxis, :, :]
        - d_covariance
    )
    factor_reconstruction = (
        tf.matmul(placement.d_factor, placement.factor[:, tf.newaxis, :, :], transpose_b=True)
        + tf.matmul(placement.factor[:, tf.newaxis, :, :], placement.d_factor, transpose_b=True)
        - d_covariance
    )

    assert float(tf.reduce_max(tf.linalg.norm(lyapunov, axis=[-2, -1])).numpy()) <= 1.0e-10
    assert (
        float(tf.reduce_max(tf.linalg.norm(factor_reconstruction, axis=[-2, -1])).numpy())
        <= 1.0e-10
    )
    np.testing.assert_allclose(
        placement.derivative_reconstruction_residual.numpy(),
        np.zeros([2]),
        atol=1.0e-10,
    )


def test_principal_sqrt_dispatcher_passes_repeated_positive_while_svd_fails() -> None:
    observations, model, derivatives = _repeated_positive_model_and_derivatives()

    with pytest.raises(tf.errors.InvalidArgumentError, match="blocked_weak_spectral_gap"):
        tf_batched_svd_sigma_point_value_and_score(
            observations,
            model,
            derivatives,
            backend="tf_svd_ukf",
            spectral_gap_tolerance=tf.constant(1.0e-10, dtype=tf.float64),
        )

    value, score, diagnostics = tf_batched_svd_sigma_point_value_and_score(
        observations,
        model,
        derivatives,
        backend="tf_principal_sqrt_ukf",
        spectral_gap_tolerance=tf.constant(1.0e-10, dtype=tf.float64),
    )

    assert np.isfinite(value.numpy()).all()
    assert np.isfinite(score.numpy()).all()
    assert diagnostics["backend"].numpy() == b"tf_principal_sqrt_ukf"
    assert diagnostics["derivative_branch"].numpy() == b"strict_spd_principal_sqrt"
    np.testing.assert_allclose(
        diagnostics["factor_derivative_reconstruction_residual"].numpy(),
        np.zeros([2]),
        atol=1.0e-10,
    )


def test_principal_sqrt_innovation_dispatcher_passes_repeated_positive_while_svd_fails() -> None:
    observations, model, derivatives = _repeated_positive_innovation_model_and_derivatives()

    with pytest.raises(tf.errors.InvalidArgumentError, match="blocked_weak_spectral_gap"):
        tf_batched_svd_sigma_point_value_and_score(
            observations,
            model,
            derivatives,
            backend="tf_svd_ukf",
            spectral_gap_tolerance=tf.constant(1.0e-10, dtype=tf.float64),
        )

    value, score, diagnostics = tf_batched_svd_sigma_point_value_and_score(
        observations,
        model,
        derivatives,
        backend="tf_principal_sqrt_ukf",
        spectral_gap_tolerance=tf.constant(1.0e-10, dtype=tf.float64),
    )

    assert np.isfinite(value.numpy()).all()
    assert np.isfinite(score.numpy()).all()
    assert diagnostics["backend"].numpy() == b"tf_principal_sqrt_ukf"
    assert diagnostics["derivative_branch"].numpy() == b"strict_spd_principal_sqrt"
    np.testing.assert_allclose(
        diagnostics["factor_derivative_reconstruction_residual"].numpy(),
        np.zeros([2]),
        atol=1.0e-10,
    )
    np.testing.assert_allclose(
        diagnostics["innovation_sylvester_residual"].numpy(),
        np.zeros([2]),
        atol=1.0e-10,
    )


    tensors = _fixture(batch_size=2, time_steps=3)
    svd_value, svd_score, _diagnostics = _value_score_diagnostics(tensors, backend="tf_svd_ukf")
    sqrt_value, sqrt_score, diagnostics = _value_score_diagnostics(
        tensors,
        backend="tf_principal_sqrt_ukf",
    )

    np.testing.assert_allclose(sqrt_value.numpy(), svd_value.numpy(), atol=1.0e-7)
    np.testing.assert_allclose(
        sqrt_score.numpy(),
        svd_score.numpy(),
        rtol=1.0e-5,
        atol=1.0e-6,
    )
    assert diagnostics["backend"].numpy() == b"tf_principal_sqrt_ukf"


def test_principal_sqrt_ukf_graph_and_cpu_xla_smoke() -> None:
    tensors = _fixture(batch_size=2, time_steps=3)
    eager_value, eager_score, _diagnostics = _value_score_diagnostics(
        tensors,
        backend="tf_principal_sqrt_ukf",
    )

    @tf.function(reduce_retracing=True)
    def graph_call() -> tuple[tf.Tensor, tf.Tensor]:
        value, score, _diagnostics = _value_score_diagnostics(
            tensors,
            backend="tf_principal_sqrt_ukf",
        )
        return value, score

    @tf.function(jit_compile=True, reduce_retracing=True)
    def xla_call() -> tuple[tf.Tensor, tf.Tensor]:
        value, score, _diagnostics = _value_score_diagnostics(
            tensors,
            backend="tf_principal_sqrt_ukf",
        )
        return value, score

    graph_value, graph_score = graph_call()
    xla_value, xla_score = xla_call()

    np.testing.assert_allclose(graph_value.numpy(), eager_value.numpy(), atol=1.0e-7)
    np.testing.assert_allclose(graph_score.numpy(), eager_score.numpy(), rtol=1.0e-5, atol=1.0e-6)
    np.testing.assert_allclose(xla_value.numpy(), eager_value.numpy(), atol=1.0e-7)
    np.testing.assert_allclose(xla_score.numpy(), eager_score.numpy(), rtol=1.0e-5, atol=1.0e-6)


@pytest.mark.parametrize("backend", OLD_BACKENDS)
def test_old_backend_dispatcher_smoke_still_passes(backend: str) -> None:
    tensors = _fixture(batch_size=2, time_steps=3)
    value, score, diagnostics = _value_score_diagnostics(tensors, backend=backend)

    assert np.isfinite(value.numpy()).all()
    assert np.isfinite(score.numpy()).all()
    assert diagnostics["backend"].numpy() == backend.encode()
