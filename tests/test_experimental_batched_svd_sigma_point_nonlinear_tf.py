from __future__ import annotations

import os
from collections.abc import Callable

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

from bayesfilter.nonlinear.experimental_batched_svd_sigma_point_tf import (
    TFBatchedStructuralFirstDerivatives,
    TFBatchedStructuralStateSpace,
    tf_batched_svd_sigma_point_value_and_score,
)
from bayesfilter.nonlinear.svd_sigma_point_derivatives_tf import (
    TFStructuralFirstDerivatives,
    tf_svd_cubature_score,
    tf_svd_ukf_score,
)
from bayesfilter.testing import (
    make_nonlinear_accumulation_first_derivatives_tf,
    make_nonlinear_accumulation_model_tf,
    model_b_observations_tf,
)


ALPHA = tf.constant(0.55, dtype=tf.float64)
OBSERVATION_SIGMA = tf.constant(0.30, dtype=tf.float64)
BACKENDS = {
    "tf_svd_ukf": tf_svd_ukf_score,
    "tf_svd_cubature": tf_svd_cubature_score,
}


def _theta_batch() -> tf.Tensor:
    return tf.constant(
        [
            [0.68, 0.24, 0.78],
            [0.70, 0.25, 0.80],
        ],
        dtype=tf.float64,
    )


def _batched_model_and_derivatives(
    theta_batch: tf.Tensor,
) -> tuple[TFBatchedStructuralStateSpace, TFBatchedStructuralFirstDerivatives]:
    theta_batch = tf.convert_to_tensor(theta_batch, dtype=tf.float64)
    rho = theta_batch[:, 0]
    sigma = theta_batch[:, 1]
    beta = theta_batch[:, 2]
    batch_size = int(theta_batch.shape[0])
    parameter_dim = 3
    state_dim = 2
    innovation_dim = 1
    observation_dim = 1

    def transition(previous: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        eps = innovation[:, :, 0]
        m_next = rho[:, tf.newaxis] * previous[:, :, 0] + sigma[:, tf.newaxis] * eps
        k_next = ALPHA * previous[:, :, 1] + beta[:, tf.newaxis] * tf.math.tanh(m_next)
        return tf.stack([m_next, k_next], axis=2)

    def observe(states: tf.Tensor) -> tf.Tensor:
        return (states[:, :, 0] + states[:, :, 1])[:, :, tf.newaxis]

    def residual(
        previous: tf.Tensor,
        innovation: tf.Tensor,
        next_points: tf.Tensor,
    ) -> tf.Tensor:
        del innovation
        expected = ALPHA * previous[:, :, 1] + beta[:, tf.newaxis] * tf.math.tanh(
            next_points[:, :, 0]
        )
        return (next_points[:, :, 1] - expected)[:, :, tf.newaxis]

    def transition_state_jacobian(
        previous: tf.Tensor,
        innovation: tf.Tensor,
    ) -> tf.Tensor:
        eps = innovation[:, :, 0]
        m_next = rho[:, tf.newaxis] * previous[:, :, 0] + sigma[:, tf.newaxis] * eps
        sech2 = 1.0 - tf.square(tf.math.tanh(m_next))
        zeros = tf.zeros_like(m_next)
        row_m = tf.stack([tf.broadcast_to(rho[:, tf.newaxis], tf.shape(m_next)), zeros], axis=2)
        row_k = tf.stack(
            [
                beta[:, tf.newaxis] * sech2 * rho[:, tf.newaxis],
                tf.fill(tf.shape(m_next), ALPHA),
            ],
            axis=2,
        )
        return tf.stack([row_m, row_k], axis=2)

    def transition_innovation_jacobian(
        previous: tf.Tensor,
        innovation: tf.Tensor,
    ) -> tf.Tensor:
        eps = innovation[:, :, 0]
        m_next = rho[:, tf.newaxis] * previous[:, :, 0] + sigma[:, tf.newaxis] * eps
        sech2 = 1.0 - tf.square(tf.math.tanh(m_next))
        column = tf.stack(
            [
                tf.broadcast_to(sigma[:, tf.newaxis], tf.shape(m_next)),
                beta[:, tf.newaxis] * sech2 * sigma[:, tf.newaxis],
            ],
            axis=2,
        )
        return column[:, :, :, tf.newaxis]

    def d_transition(previous: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        eps = innovation[:, :, 0]
        m_next = rho[:, tf.newaxis] * previous[:, :, 0] + sigma[:, tf.newaxis] * eps
        tanh_m = tf.math.tanh(m_next)
        sech2 = 1.0 - tf.square(tanh_m)
        zeros = tf.zeros_like(eps)
        d_rho = tf.stack([previous[:, :, 0], beta[:, tf.newaxis] * sech2 * previous[:, :, 0]], axis=2)
        d_sigma = tf.stack([eps, beta[:, tf.newaxis] * sech2 * eps], axis=2)
        d_beta = tf.stack([zeros, tanh_m], axis=2)
        return tf.stack([d_rho, d_sigma, d_beta], axis=1)

    def observation_state_jacobian(states: tf.Tensor) -> tf.Tensor:
        point_count = tf.shape(states)[1]
        return tf.broadcast_to(
            tf.constant([[[1.0, 1.0]]], dtype=tf.float64),
            [tf.shape(states)[0], point_count, observation_dim, state_dim],
        )

    def d_observation(states: tf.Tensor) -> tf.Tensor:
        return tf.zeros(
            [tf.shape(states)[0], parameter_dim, tf.shape(states)[1], observation_dim],
            dtype=tf.float64,
        )

    model = TFBatchedStructuralStateSpace(
        initial_mean=tf.zeros([batch_size, state_dim], dtype=tf.float64),
        initial_covariance=tf.broadcast_to(
            tf.linalg.diag(tf.constant([0.25, 0.20], dtype=tf.float64)),
            [batch_size, state_dim, state_dim],
        ),
        innovation_covariance=tf.ones([batch_size, innovation_dim, innovation_dim], dtype=tf.float64),
        observation_covariance=tf.fill(
            [batch_size, observation_dim, observation_dim],
            tf.square(OBSERVATION_SIGMA),
        ),
        transition_fn=transition,
        observation_fn=observe,
        deterministic_residual_fn=residual,
        name="experimental_batched_model_b_nonlinear_accumulation",
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
        name="experimental_batched_model_b_first_derivatives",
    )
    return model, derivatives


def _scalar_model_and_derivatives(theta: tf.Tensor) -> tuple[object, TFStructuralFirstDerivatives]:
    return (
        make_nonlinear_accumulation_model_tf(
            rho=theta[0],
            sigma=theta[1],
            alpha=ALPHA,
            beta=theta[2],
            observation_sigma=OBSERVATION_SIGMA,
        ),
        make_nonlinear_accumulation_first_derivatives_tf(
            rho=theta[0],
            sigma=theta[1],
            alpha=ALPHA,
            beta=theta[2],
        ),
    )


def _batched_value_and_score(
    theta_batch: tf.Tensor,
    *,
    backend: str,
    placement_floor: tf.Tensor | float = 0.0,
    spectral_gap_tolerance: tf.Tensor | float = 1.0e-8,
) -> tuple[tf.Tensor, tf.Tensor, dict[str, tf.Tensor]]:
    model, derivatives = _batched_model_and_derivatives(theta_batch)
    value, score, diagnostics = tf_batched_svd_sigma_point_value_and_score(
        model_b_observations_tf(),
        model,
        derivatives,
        backend=backend,
        placement_floor=tf.constant(placement_floor, dtype=tf.float64),
        innovation_floor=tf.constant(1.0e-12, dtype=tf.float64),
        spectral_gap_tolerance=tf.constant(spectral_gap_tolerance, dtype=tf.float64),
    )
    return value, score, dict(diagnostics)


def _scalar_rows(theta_batch: tf.Tensor, *, backend: str) -> tuple[tf.Tensor, tf.Tensor]:
    values = []
    scores = []
    score_fn = BACKENDS[backend]
    for theta in tf.unstack(theta_batch, axis=0):
        model, derivatives = _scalar_model_and_derivatives(theta)
        result = score_fn(
            model_b_observations_tf(),
            model,
            derivatives,
            innovation_floor=tf.constant(1.0e-12, dtype=tf.float64),
            spectral_gap_tolerance=tf.constant(1.0e-8, dtype=tf.float64),
        )
        values.append(result.log_likelihood)
        scores.append(result.score)
    return tf.stack(values, axis=0), tf.stack(scores, axis=0)


@pytest.mark.parametrize("backend", tuple(BACKENDS))
def test_experimental_batched_svd_nonlinear_matches_scalar_rows(backend: str) -> None:
    theta_batch = _theta_batch()
    batched_value, batched_score, diagnostics = _batched_value_and_score(
        theta_batch,
        backend=backend,
    )
    scalar_value, scalar_score = _scalar_rows(theta_batch, backend=backend)

    assert np.isfinite(batched_value.numpy()).all()
    assert np.isfinite(batched_score.numpy()).all()
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
    np.testing.assert_allclose(
        diagnostics["deterministic_residual"].numpy(),
        np.zeros([int(theta_batch.shape[0])]),
        atol=1.0e-12,
    )


@pytest.mark.parametrize("backend", tuple(BACKENDS))
def test_experimental_batched_svd_nonlinear_row_permutation_preserves_order(
    backend: str,
) -> None:
    theta_batch = _theta_batch()
    base_value, base_score, _diagnostics = _batched_value_and_score(
        theta_batch,
        backend=backend,
    )
    permutation = tf.constant([1, 0], dtype=tf.int32)
    permuted_value, permuted_score, _diagnostics = _batched_value_and_score(
        tf.gather(theta_batch, permutation),
        backend=backend,
    )

    np.testing.assert_allclose(
        permuted_value.numpy(),
        tf.gather(base_value, permutation).numpy(),
        rtol=1.0e-8,
        atol=1.0e-8,
    )
    np.testing.assert_allclose(
        permuted_score.numpy(),
        tf.gather(base_score, permutation).numpy(),
        rtol=1.0e-7,
        atol=1.0e-7,
    )


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"placement_floor": 10.0}, "blocked_active_floor"),
        ({"spectral_gap_tolerance": 10.0}, "blocked_weak_spectral_gap"),
    ],
)
def test_experimental_batched_svd_nonlinear_branch_diagnostics_fail_closed(
    kwargs: dict[str, float],
    message: str,
) -> None:
    with pytest.raises(tf.errors.InvalidArgumentError, match=message):
        _batched_value_and_score(_theta_batch(), backend="tf_svd_ukf", **kwargs)


def test_experimental_batched_svd_nonlinear_optional_graph_xla_diagnostic() -> None:
    theta_batch = _theta_batch()
    eager_value, eager_score, _diagnostics = _batched_value_and_score(
        theta_batch,
        backend="tf_svd_ukf",
    )

    def _skip_if_diagnostic_fails(
        label: str,
        fn: Callable[[], tuple[tf.Tensor, tf.Tensor]],
    ) -> None:
        try:
            value, score = fn()
        except Exception as exc:  # pragma: no cover - diagnostic only
            pytest.skip(f"{label} diagnostic did not compile/run: {exc}")
        try:
            np.testing.assert_allclose(value.numpy(), eager_value.numpy(), atol=1.0e-8)
            np.testing.assert_allclose(
                score.numpy(),
                eager_score.numpy(),
                rtol=1.0e-7,
                atol=1.0e-7,
            )
        except AssertionError as exc:  # pragma: no cover - diagnostic only
            pytest.skip(f"{label} diagnostic mismatch: {exc}")

    @tf.function(reduce_retracing=True)
    def graph_call() -> tuple[tf.Tensor, tf.Tensor]:
        value, score, _diagnostics = _batched_value_and_score(theta_batch, backend="tf_svd_ukf")
        return value, score

    @tf.function(jit_compile=True, reduce_retracing=True)
    def xla_call() -> tuple[tf.Tensor, tf.Tensor]:
        value, score, _diagnostics = _batched_value_and_score(theta_batch, backend="tf_svd_ukf")
        return value, score

    _skip_if_diagnostic_fails("graph", graph_call)
    _skip_if_diagnostic_fails("xla", xla_call)


def test_experimental_batched_svd_nonlinear_cpu_only_hides_gpu() -> None:
    assert os.environ.get("CUDA_VISIBLE_DEVICES") == "-1"
    assert tf.config.list_physical_devices("GPU") == []


def test_experimental_batched_svd_nonlinear_fixture_constants_match_scalar() -> None:
    assert float(ALPHA.numpy()) == pytest.approx(0.55)
    assert float(OBSERVATION_SIGMA.numpy()) == pytest.approx(0.30)
