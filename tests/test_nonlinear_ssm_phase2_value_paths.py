from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

from bayesfilter.nonlinear import (
    InvalidCompiledValuePathContract,
    find_forbidden_compiled_value_tokens,
    stable_nonlinear_filter_value_path_signature,
    tensorflow_nonlinear_value_path_contract,
    tf_svd_cut4_filter,
    tf_svd_sigma_point_filter,
)
from bayesfilter.testing import (
    make_nonlinear_accumulation_model_tf,
    make_univariate_nonlinear_growth_model_tf,
    model_b_observations_tf,
    model_c_observations_tf,
)

_BACKENDS = ("tf_svd_cubature", "tf_svd_ukf", "tf_svd_cut4")
_PRODUCTION_VALUE_SOURCE_PATHS = (
    "bayesfilter/nonlinear/sigma_points_tf.py",
    "bayesfilter/nonlinear/svd_cut_tf.py",
    "bayesfilter/nonlinear/cut_tf.py",
    "bayesfilter/linear/svd_factor_tf.py",
    "bayesfilter/structural_tf.py",
)


def _fixture(name: str):
    if name == "model_b":
        return (
            model_b_observations_tf(),
            make_nonlinear_accumulation_model_tf(),
            "phase2_model_b_value_fixture",
        )
    if name == "model_c":
        return (
            model_c_observations_tf(),
            make_univariate_nonlinear_growth_model_tf(),
            "phase2_model_c_value_fixture",
        )
    raise ValueError(name)


def _value_result(backend: str, observations: tf.Tensor, model, return_filtered: bool):
    kwargs = {
        "innovation_floor": tf.constant(1e-12, dtype=tf.float64),
        "return_filtered": return_filtered,
    }
    if backend == "tf_svd_cut4":
        return tf_svd_cut4_filter(observations, model, **kwargs)
    return tf_svd_sigma_point_filter(observations, model, backend=backend, **kwargs)


def _value_and_regularization(
    backend: str,
    observations: tf.Tensor,
    model,
    return_filtered: bool,
):
    result = _value_result(backend, observations, model, return_filtered)
    regularization = result.diagnostics.regularization
    outputs = [
        result.log_likelihood,
        tf.cast(regularization.floor_count, tf.float64),
        regularization.psd_projection_residual,
        regularization.implemented_covariance,
    ]
    if return_filtered:
        outputs.extend([result.filtered_means, result.filtered_covariances])
    return tuple(outputs)


def _compiled_value_and_regularization(backend: str, model, return_filtered: bool):
    @tf.function(jit_compile=True, reduce_retracing=True)
    def compiled(obs: tf.Tensor):
        return _value_and_regularization(backend, obs, model, return_filtered)

    return compiled


def _assert_allclose_sequence(graph, eager) -> None:
    for graph_value, eager_value in zip(graph, eager, strict=True):
        np.testing.assert_allclose(
            graph_value.numpy(),
            eager_value.numpy(),
            atol=1e-12,
        )


def test_phase2_cpu_only_hides_gpu_before_tensorflow_runtime_probe() -> None:
    assert os.environ.get("CUDA_VISIBLE_DEVICES") == "-1"
    assert tf.config.list_physical_devices("GPU") == []


@pytest.mark.parametrize("fixture_name", ("model_b", "model_c"))
@pytest.mark.parametrize("backend", _BACKENDS)
@pytest.mark.parametrize("return_filtered", (False, True))
def test_phase2_value_paths_preserve_value_and_regularization_under_xla(
    fixture_name: str,
    backend: str,
    return_filtered: bool,
) -> None:
    observations, model, contract_fixture_name = _fixture(fixture_name)
    contract = tensorflow_nonlinear_value_path_contract(
        fixture_name=contract_fixture_name,
        observations=observations,
        model=model,
        backend=backend,
        return_filtered=return_filtered,
    )
    eager = _value_and_regularization(backend, observations, model, return_filtered)
    compiled = _compiled_value_and_regularization(backend, model, return_filtered)
    graph = compiled(observations)

    assert contract.is_promoted_fixed_shape_value_path is True
    assert contract.value_authority == "graph_native_value_only"
    assert contract.score_status == "not_claimed"
    assert contract.hmc_status == "not_claimed"
    assert contract.dynamic_horizon_status == "not_claimed"
    assert contract.static_shape.horizon == int(observations.shape[0])
    assert contract.static_shape.observation_shape == tuple(observations.shape.as_list())
    assert contract.regularization.repair_role == "target"
    assert contract.regularization.implemented_covariance == (
        "post_floor_innovation_covariance"
    )
    _assert_allclose_sequence(graph, eager)
    compiled(tf.identity(observations))
    assert len(compiled._list_all_concrete_functions_for_serialization()) == 1


def test_phase2_value_path_signature_tracks_shape_backend_and_return_policy() -> None:
    observations, model, fixture_name = _fixture("model_b")
    base = tensorflow_nonlinear_value_path_contract(
        fixture_name=fixture_name,
        observations=observations,
        model=model,
        backend="tf_svd_cubature",
        return_filtered=False,
    )
    same = tensorflow_nonlinear_value_path_contract(
        fixture_name=fixture_name,
        observations=tf.identity(observations),
        model=model,
        backend="tf_svd_cubature",
        return_filtered=False,
    )
    different_backend = tensorflow_nonlinear_value_path_contract(
        fixture_name=fixture_name,
        observations=observations,
        model=model,
        backend="tf_svd_ukf",
        return_filtered=False,
    )
    different_return = tensorflow_nonlinear_value_path_contract(
        fixture_name=fixture_name,
        observations=observations,
        model=model,
        backend="tf_svd_cubature",
        return_filtered=True,
    )
    different_shape = tensorflow_nonlinear_value_path_contract(
        fixture_name=fixture_name,
        observations=observations[:2],
        model=model,
        backend="tf_svd_cubature",
        return_filtered=False,
    )

    assert stable_nonlinear_filter_value_path_signature(base) == (
        stable_nonlinear_filter_value_path_signature(same)
    )
    signatures = {
        stable_nonlinear_filter_value_path_signature(base),
        stable_nonlinear_filter_value_path_signature(different_backend),
        stable_nonlinear_filter_value_path_signature(different_return),
        stable_nonlinear_filter_value_path_signature(different_shape),
    }
    assert len(signatures) == 4


def test_phase2_value_path_contract_fails_closed_for_unknown_backend() -> None:
    observations, model, fixture_name = _fixture("model_b")

    with pytest.raises(InvalidCompiledValuePathContract, match="unknown value backend"):
        tensorflow_nonlinear_value_path_contract(
            fixture_name=fixture_name,
            observations=observations,
            model=model,
            backend="tf_numpy_reference",
            return_filtered=False,
        )


def test_phase2_promoted_value_sources_do_not_contain_host_callbacks() -> None:
    root = Path(__file__).resolve().parents[1]
    findings = {}
    for relative_path in _PRODUCTION_VALUE_SOURCE_PATHS:
        source = (root / relative_path).read_text(encoding="utf-8")
        tokens = find_forbidden_compiled_value_tokens(source)
        if tokens:
            findings[relative_path] = tokens

    assert findings == {}


def test_phase2_host_callback_scan_rejects_intentionally_blocked_fixture() -> None:
    source = """
def blocked(x):
    return tf.numpy_function(lambda y: y, [x], Tout=tf.float64).numpy()
"""

    assert find_forbidden_compiled_value_tokens(source) == (
        "tf.numpy_function",
        ".numpy(",
    )
