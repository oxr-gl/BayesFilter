from __future__ import annotations

import inspect
import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

import bayesfilter.ops.symmetric_principal_sqrt_tf as symmetric_principal_sqrt_tf
from bayesfilter.ops import SymmetricPrincipalSqrtStatus, symmetric_principal_sqrt
from bayesfilter.ops.symmetric_principal_sqrt_tf import _validate_shapes


def _reference_principal_sqrt(covariance: np.ndarray) -> np.ndarray:
    values = []
    for b in range(covariance.shape[0]):
        eigvals, eigvecs = np.linalg.eigh(covariance[b])
        values.append(eigvecs @ np.diag(np.sqrt(eigvals)) @ eigvecs.T)
    return np.asarray(values, dtype=np.float64)


def _fixture() -> tf.Tensor:
    covariance = np.asarray(
        [
            [
                [4.0, 0.0, 0.0],
                [0.0, 4.0, 0.0],
                [0.0, 0.0, 9.0],
            ],
            [
                [3.0, 0.25, 0.0],
                [0.25, 4.0, 0.1],
                [0.0, 0.1, 6.0],
            ],
        ],
        dtype=np.float64,
    )
    return tf.constant(covariance, dtype=tf.float64)


def test_symmetric_principal_sqrt_contract_reports_static_shape_metadata() -> None:
    status = _validate_shapes(tf.eye(3, batch_shape=[2], dtype=tf.float64))

    assert isinstance(status, SymmetricPrincipalSqrtStatus)
    assert status.batch_size == 2
    assert status.dimension == 3
    assert status.implemented is True
    assert status.backend == "compiled_symmetric_principal_sqrt"


def test_symmetric_principal_sqrt_matches_reference_and_reconstructs() -> None:
    covariance = _fixture()
    actual = symmetric_principal_sqrt(covariance)
    expected = _reference_principal_sqrt(covariance.numpy())

    np.testing.assert_allclose(actual.numpy(), expected, rtol=1.0e-11, atol=1.0e-11)
    np.testing.assert_allclose(
        (actual @ tf.linalg.matrix_transpose(actual)).numpy(),
        covariance.numpy(),
        rtol=1.0e-11,
        atol=1.0e-11,
    )


def test_symmetric_principal_sqrt_repeated_positive_eigenvalue_fixture_passes() -> None:
    covariance = 6.25 * tf.eye(4, batch_shape=[1], dtype=tf.float64)
    actual = symmetric_principal_sqrt(covariance)

    np.testing.assert_allclose(actual.numpy(), (2.5 * tf.eye(4, batch_shape=[1], dtype=tf.float64)).numpy(), atol=1.0e-12)


def test_symmetric_principal_sqrt_graph_and_cpu_xla_match_eager() -> None:
    covariance = _fixture()
    eager = symmetric_principal_sqrt(covariance)

    @tf.function(reduce_retracing=True)
    def graph_call() -> tf.Tensor:
        return symmetric_principal_sqrt(covariance)

    @tf.function(jit_compile=True, reduce_retracing=True)
    def xla_call() -> tf.Tensor:
        return symmetric_principal_sqrt(covariance)

    np.testing.assert_allclose(graph_call().numpy(), eager.numpy(), atol=1.0e-11)
    np.testing.assert_allclose(xla_call().numpy(), eager.numpy(), atol=1.0e-11)


def test_symmetric_principal_sqrt_casts_to_float64() -> None:
    actual = symmetric_principal_sqrt(tf.eye(2, batch_shape=[1], dtype=tf.float32))

    assert actual.dtype == tf.float64


def test_symmetric_principal_sqrt_rejects_non_symmetric_precondition() -> None:
    with pytest.raises(tf.errors.InvalidArgumentError, match="must be symmetric"):
        symmetric_principal_sqrt(
            tf.constant([[[2.0, 1.0], [0.0, 2.0]]], dtype=tf.float64),
        )


def test_symmetric_principal_sqrt_rejects_unknown_backend() -> None:
    with pytest.raises(ValueError, match="unknown symmetric principal-sqrt backend"):
        symmetric_principal_sqrt(
            tf.eye(2, batch_shape=[1], dtype=tf.float64),
            backend="tensorflow_fallback",
        )


def test_symmetric_principal_sqrt_contract_rejects_shape_mismatch() -> None:
    with pytest.raises(ValueError, match="square"):
        _validate_shapes(tf.ones([1, 2, 3], dtype=tf.float64))


def test_symmetric_principal_sqrt_source_has_no_tensorflow_factorization_fallbacks() -> None:
    source = inspect.getsource(symmetric_principal_sqrt_tf)
    forbidden = (
        "tf.linalg.eigh",
        "tf.linalg.svd",
        "tf.linalg.cholesky",
        "tf.vectorized_map",
        "GradientTape",
        "custom_gradient",
    )
    for pattern in forbidden:
        assert pattern not in source


def test_symmetric_principal_sqrt_cpu_only_hides_gpu() -> None:
    assert os.environ.get("CUDA_VISIBLE_DEVICES") == "-1"
    assert tf.config.list_physical_devices("GPU") == []
