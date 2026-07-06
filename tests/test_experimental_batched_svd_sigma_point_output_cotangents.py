from __future__ import annotations

import inspect
import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import tensorflow as tf

from bayesfilter.nonlinear.experimental_batched_svd_sigma_point_tf import (
    TFBatchedStructuralLinearizations,
    tf_batched_svd_sigma_point_value_and_output_cotangents,
    tf_batched_svd_sigma_point_value_and_score,
)
from docs.benchmarks.benchmark_experimental_batched_svd_sigma_point_cpu_gpu import (
    _batched_model_and_derivatives,
    _stable_fixture,
    _to_tensors,
)


def _fixture(*, batch_size: int = 2, time_steps: int = 3) -> dict[str, tf.Tensor]:
    return _to_tensors(
        _stable_fixture(
            batch_size=batch_size,
            time_steps=time_steps,
            state_dim=2,
            obs_dim=2,
            parameter_dim=2,
        )
    )


def _linearizations(derivatives):
    return TFBatchedStructuralLinearizations(
        transition_state_jacobian_fn=derivatives.transition_state_jacobian_fn,
        transition_innovation_jacobian_fn=(
            derivatives.transition_innovation_jacobian_fn
        ),
        observation_state_jacobian_fn=derivatives.observation_state_jacobian_fn,
        name="fixture_linearizations",
    )


def _score_from_cotangents(tf, derivatives, cotangents):
    score = tf.einsum(
        "bi,bpi->bp",
        cotangents.initial_mean_cotangent,
        derivatives.d_initial_mean,
    )
    score = score + tf.einsum(
        "bij,bpij->bp",
        cotangents.initial_covariance_cotangent,
        derivatives.d_initial_covariance,
    )
    score = score + tf.einsum(
        "bij,bpij->bp",
        cotangents.innovation_covariance_cotangent,
        derivatives.d_innovation_covariance,
    )
    score = score + tf.einsum(
        "bij,bpij->bp",
        cotangents.observation_covariance_cotangent,
        derivatives.d_observation_covariance,
    )
    transition_points = cotangents.transition_previous_points
    innovation_points = cotangents.transition_innovation_points
    observation_points = cotangents.observation_state_points
    transition_terms = tf.map_fn(
        lambda args: tf.einsum(
            "bro,bpro->bp",
            args[2],
            derivatives.d_transition_fn(args[0], args[1]),
        ),
        (
            transition_points,
            innovation_points,
            cotangents.transition_output_cotangent,
        ),
        fn_output_signature=tf.TensorSpec(score.shape, dtype=tf.float64),
    )
    observation_terms = tf.map_fn(
        lambda args: tf.einsum(
            "brm,bprm->bp",
            args[1],
            derivatives.d_observation_fn(args[0]),
        ),
        (
            observation_points,
            cotangents.observation_output_cotangent,
        ),
        fn_output_signature=tf.TensorSpec(score.shape, dtype=tf.float64),
    )
    return score + tf.reduce_sum(transition_terms, axis=0) + tf.reduce_sum(
        observation_terms,
        axis=0,
    )


def test_batched_svd_output_cotangents_match_forward_score_route():
    tensors = _fixture()
    model, derivatives = _batched_model_and_derivatives(tensors)
    cotangents = tf_batched_svd_sigma_point_value_and_output_cotangents(
        tensors["observations"],
        model,
        _linearizations(derivatives),
        backend="tf_principal_sqrt_ukf",
    )
    expected_value, expected_score, expected_diagnostics = (
        tf_batched_svd_sigma_point_value_and_score(
            tensors["observations"],
            model,
            derivatives,
            backend="tf_principal_sqrt_ukf",
            spectral_gap_tolerance=tf.constant(1.0e-10, dtype=tf.float64),
        )
    )
    actual_score = _score_from_cotangents(tf, derivatives, cotangents)

    np.testing.assert_allclose(cotangents.value.numpy(), expected_value.numpy(), atol=1e-8)
    np.testing.assert_allclose(
        actual_score.numpy(),
        expected_score.numpy(),
        rtol=1.0e-7,
        atol=1.0e-7,
    )
    assert cotangents.diagnostics["backend"].numpy() == expected_diagnostics[
        "backend"
    ].numpy()
    assert bool(cotangents.diagnostics["filter_autodiff_allowed_for_hmc"].numpy()) is False


def test_batched_svd_output_cotangents_tensorflow_eigh_backend_matches_default():
    tensors = _fixture()
    model, derivatives = _batched_model_and_derivatives(tensors)
    linearizations = _linearizations(derivatives)
    default = tf_batched_svd_sigma_point_value_and_output_cotangents(
        tensors["observations"],
        model,
        linearizations,
        backend="tf_principal_sqrt_ukf",
    )
    native = tf_batched_svd_sigma_point_value_and_output_cotangents(
        tensors["observations"],
        model,
        linearizations,
        backend="tf_principal_sqrt_ukf",
        principal_sqrt_backend="tensorflow_eigh",
    )

    np.testing.assert_allclose(native.value.numpy(), default.value.numpy(), atol=1e-8)
    np.testing.assert_allclose(
        native.initial_mean_cotangent.numpy(),
        default.initial_mean_cotangent.numpy(),
        rtol=1.0e-7,
        atol=1.0e-7,
    )
    np.testing.assert_allclose(
        native.transition_output_cotangent.numpy(),
        default.transition_output_cotangent.numpy(),
        rtol=1.0e-7,
        atol=1.0e-7,
    )


def test_batched_svd_output_cotangent_source_contract():
    import bayesfilter.nonlinear.experimental_batched_svd_sigma_point_tf as module

    source = inspect.getsource(
        module.tf_batched_svd_sigma_point_value_and_output_cotangents
    )
    forbidden = (
        "GradientTape",
        "tape.gradient",
        ".numpy(",
        "tf.py_function",
        "d_transition_fn",
        "d_observation_fn",
    )
    for token in forbidden:
        assert token not in source
    assert "tf.while_loop" in source
    assert "symmetric_sylvester_solve" in inspect.getsource(
        module._symmetric_sylvester_factor_solve
    )
