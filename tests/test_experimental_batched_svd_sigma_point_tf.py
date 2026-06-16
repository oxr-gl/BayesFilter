from __future__ import annotations

import os
from types import SimpleNamespace

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

from bayesfilter.nonlinear.experimental_batched_svd_sigma_point_tf import (
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
