from __future__ import annotations

import ast
import importlib.util
import os
from pathlib import Path
from typing import Any

import numpy as np

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import tensorflow as tf

from experiments.dpf_implementation.tf_tfp.filters import (
    experimental_batched_ledh_pfpf_ot_tf as ledh,
)
from experiments.dpf_implementation.tf_tfp.resampling import annealed_transport_tf


ROOT = Path(__file__).resolve().parents[1]
RESET_HELPER_PATH = ROOT / "docs" / "benchmarks" / "contract_e_reset_tf.py"
GRADIENT_SCRIPT = (
    ROOT / "docs" / "benchmarks" / "diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py"
)
TRANSPORT_HELPER_PATH = (
    ROOT / "experiments" / "dpf_implementation" / "tf_tfp" / "resampling" / "annealed_transport_tf.py"
)
THIS_FILE = Path(__file__)
FULL_BLOCKER_CODE = "PHASE3_MATERIAL_FULL_GATE_PENDING_T10_MANUAL_ROUTE_VALIDATION"
DTYPE = tf.float64
annealed_transport_tf.DTYPE = DTYPE
ledh.DTYPE = DTYPE


def _load_reset_module() -> Any:
    spec = importlib.util.spec_from_file_location("contract_e_reset_tf_r5", RESET_HELPER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {RESET_HELPER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _function_source(path: Path, name: str) -> str:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            if node.end_lineno is None:
                raise AssertionError(f"missing end line for {name}")
            return "\n".join(lines[node.lineno - 1 : node.end_lineno])
    raise AssertionError(f"function not found: {name}")


def _fixture() -> dict[str, tf.Tensor]:
    post_flow = tf.constant(
        [
            [
                [-1.0, 0.2],
                [0.0, -0.4],
                [0.8, 0.6],
                [1.5, -0.1],
            ]
        ],
        dtype=DTYPE,
    )
    corrected_log_weights = tf.constant([[-0.35, 0.10, -0.20, 0.30]], dtype=DTYPE)
    residual_noise = tf.constant(
        [
            [
                [-0.3, 0.7],
                [0.5, -0.2],
                [1.0, 0.1],
                [-0.4, -0.8],
            ]
        ],
        dtype=DTYPE,
    )
    upstream_particles = tf.reshape(
        tf.linspace(tf.constant(-0.17, DTYPE), tf.constant(0.29, DTYPE), 8),
        [1, 4, 2],
    )
    increment_upstream = tf.constant([0.37], dtype=DTYPE)
    return {
        "post_flow": post_flow,
        "corrected_log_weights": corrected_log_weights,
        "residual_noise": residual_noise,
        "upstream_particles": upstream_particles,
        "increment_upstream": increment_upstream,
        "epsilon": tf.constant(0.55, dtype=DTYPE),
        "scaling": tf.constant(0.82, dtype=DTYPE),
        "steps": tf.constant(2, dtype=tf.int32),
        "floor": tf.constant(0.05, dtype=DTYPE),
        "ridge": tf.constant([0.75], dtype=DTYPE),
        "rho": tf.constant(1.0, dtype=DTYPE),
    }


def _transport_chart(post_flow: tf.Tensor) -> dict[str, tf.Tensor]:
    center = tf.reduce_mean(post_flow, axis=1, keepdims=True)
    scale = annealed_transport_tf._filterflow_scale(post_flow)  # noqa: SLF001
    x = (post_flow - center) / scale[:, None, None]
    epsilon0 = annealed_transport_tf._filterflow_epsilon_start(x)  # noqa: SLF001
    return {
        "center": center,
        "scale": scale,
        "key": x,
        "epsilon0": epsilon0,
    }


def _r5_transport_matrix_value_with_replayed_key(
    x: tf.Tensor,
    key: tf.Tensor,
    logw: tf.Tensor,
    eps: tf.Tensor,
    epsilon0: tf.Tensor,
    scaling: tf.Tensor,
    *,
    steps: int,
) -> tf.Tensor:
    float_n = tf.cast(tf.shape(x)[1], x.dtype)
    uniform_log_weight = -tf.math.log(float_n) * tf.ones_like(logw)
    cost = annealed_transport_tf._filterflow_exact_cost(x, key)  # noqa: SLF001
    alpha, beta, _a_x, _b_y = (
        annealed_transport_tf._filterflow_manual_dense_finite_sinkhorn_outputs(  # noqa: SLF001
            logw,
            uniform_log_weight,
            cost,
            cost,
            cost,
            cost,
            epsilon=eps,
            epsilon0=epsilon0,
            scaling=scaling,
            steps=steps,
        )
    )
    return annealed_transport_tf._filterflow_exact_transport_from_potentials(  # noqa: SLF001
        x,
        alpha,
        beta,
        eps,
        logw,
        float_n,
    )


def _r5_forward_parts(
    reset_module: Any,
    post_flow: tf.Tensor,
    corrected_log_weights: tf.Tensor,
    residual_noise: tf.Tensor,
    fixture: dict[str, tf.Tensor],
    chart: dict[str, tf.Tensor],
) -> dict[str, tf.Tensor]:
    weights, increment = ledh._normalize_log_weights(corrected_log_weights)  # noqa: SLF001
    transport_logw = tf.math.log(tf.maximum(weights, fixture["floor"]))
    x = (post_flow - chart["center"]) / chart["scale"][:, None, None]
    matrix = _r5_transport_matrix_value_with_replayed_key(
        x,
        chart["key"],
        transport_logw,
        fixture["epsilon"],
        chart["epsilon0"],
        fixture["scaling"],
        steps=int(fixture["steps"].numpy()),
    )
    reset = reset_module.contract_e_cholesky_ridge_reset_fixed_ridge(
        tf,
        post_flow=post_flow,
        weights=weights,
        matrix=matrix,
        residual_noise=residual_noise,
        rho=fixture["rho"],
        ridge=fixture["ridge"],
    )
    scalar = (
        tf.reduce_sum(reset["particles"] * fixture["upstream_particles"])
        + tf.reduce_sum(increment * fixture["increment_upstream"])
    )
    return {
        "scalar": scalar,
        "weights": weights,
        "increment": increment,
        "transport_logw": transport_logw,
        "matrix": matrix,
        "particles": reset["particles"],
        "floor_active": weights > fixture["floor"],
    }


def _r5_manual_vjp(
    reset_module: Any,
    post_flow: tf.Tensor,
    corrected_log_weights: tf.Tensor,
    residual_noise: tf.Tensor,
    fixture: dict[str, tf.Tensor],
    chart: dict[str, tf.Tensor],
) -> dict[str, tf.Tensor]:
    forward = _r5_forward_parts(
        reset_module,
        post_flow,
        corrected_log_weights,
        residual_noise,
        fixture,
        chart,
    )
    reset_vjp = reset_module.contract_e_cholesky_ridge_reset_fixed_ridge_vjp(
        tf,
        post_flow=post_flow,
        weights=forward["weights"],
        matrix=forward["matrix"],
        residual_noise=residual_noise,
        rho=fixture["rho"],
        ridge=fixture["ridge"],
        upstream_particles=fixture["upstream_particles"],
    )
    x = (post_flow - chart["center"]) / chart["scale"][:, None, None]
    transport_x_bar, transport_logw_bar = (
        annealed_transport_tf._filterflow_manual_dense_finite_transport_matrix_vjp_stopped_scale_keys(  # noqa: SLF001
            x,
            forward["transport_logw"],
            fixture["epsilon"],
            chart["epsilon0"],
            fixture["scaling"],
            reset_vjp["matrix"],
            steps=int(fixture["steps"].numpy()),
        )
    )
    post_flow_bar = reset_vjp["post_flow"] + transport_x_bar / chart["scale"][:, None, None]
    floor_bar = tf.where(forward["floor_active"], transport_logw_bar, tf.zeros_like(transport_logw_bar))
    normalized_log_bar = forward["weights"] * reset_vjp["weights"] + floor_bar
    corrected_bar, _weights, _increment = ledh._normalize_log_weights_vjp(  # noqa: SLF001
        corrected_log_weights,
        normalized_log_bar,
        fixture["increment_upstream"],
    )
    return {
        "post_flow": post_flow_bar,
        "corrected_log_weights": corrected_bar,
        "residual_noise": reset_vjp["residual_noise"],
        "reset_matrix_bar": reset_vjp["matrix"],
        "transport_x_bar": transport_x_bar,
        "transport_logw_bar": transport_logw_bar,
        "scalar": forward["scalar"],
    }


def _r5_branch_record(
    reset_module: Any,
    post_flow: tf.Tensor,
    corrected_log_weights: tf.Tensor,
    residual_noise: tf.Tensor,
    fixture: dict[str, tf.Tensor],
    chart: dict[str, tf.Tensor],
) -> dict[str, tf.Tensor]:
    forward = _r5_forward_parts(
        reset_module,
        post_flow,
        corrected_log_weights,
        residual_noise,
        fixture,
        chart,
    )
    branchy = reset_module.contract_e_cholesky_ridge_reset(
        tf,
        post_flow=post_flow,
        weights=forward["weights"],
        matrix=forward["matrix"],
        residual_noise=residual_noise,
        rho=fixture["rho"],
        ridge_rel=tf.constant(0.0, dtype=DTYPE),
        ridge_abs=fixture["ridge"][0],
        ridge_escalation=tf.constant(10.0, dtype=DTYPE),
        ridge_max_attempts=tf.constant(3, dtype=tf.int32),
    )
    return {
        "floor_active": forward["floor_active"],
        "max_realized_ridge": branchy["max_realized_ridge"],
        "ridge_attempts_used": branchy["ridge_attempts_used"],
        "ridge_failure": branchy["ridge_failure"],
    }


def _direction(shape: tuple[int, ...], start: float, stop: float) -> tf.Tensor:
    count = 1
    for dim in shape:
        count *= dim
    return tf.reshape(
        tf.linspace(tf.constant(start, DTYPE), tf.constant(stop, DTYPE), count),
        shape,
    )


def test_r5_one_step_composed_manual_vjp_matches_same_scalar_fd() -> None:
    reset_module = _load_reset_module()
    fixture = _fixture()
    post_flow = fixture["post_flow"]
    corrected = fixture["corrected_log_weights"]
    residual_noise = fixture["residual_noise"]
    chart = _transport_chart(post_flow)
    manual = _r5_manual_vjp(reset_module, post_flow, corrected, residual_noise, fixture, chart)
    center_record = _r5_branch_record(reset_module, post_flow, corrected, residual_noise, fixture, chart)
    assert not bool(center_record["ridge_failure"].numpy())

    directions = {
        "post_flow": _direction(tuple(post_flow.shape), -0.020, 0.017),
        "corrected_log_weights": tf.constant([[0.015, -0.025, 0.018, -0.010]], dtype=DTYPE),
        "residual_noise": _direction(tuple(residual_noise.shape), 0.012, -0.019),
    }
    zeros = {
        "post_flow": tf.zeros_like(post_flow),
        "corrected_log_weights": tf.zeros_like(corrected),
        "residual_noise": tf.zeros_like(residual_noise),
    }
    step = tf.constant(1.0e-5, dtype=DTYPE)

    def scalar(
        local_post_flow: tf.Tensor,
        local_corrected: tf.Tensor,
        local_residual_noise: tf.Tensor,
    ) -> tf.Tensor:
        return _r5_forward_parts(
            reset_module,
            local_post_flow,
            local_corrected,
            local_residual_noise,
            fixture,
            chart,
        )["scalar"]

    for name, direction in directions.items():
        perturb = dict(zeros)
        perturb[name] = direction
        plus_args = (
            post_flow + step * perturb["post_flow"],
            corrected + step * perturb["corrected_log_weights"],
            residual_noise + step * perturb["residual_noise"],
        )
        minus_args = (
            post_flow - step * perturb["post_flow"],
            corrected - step * perturb["corrected_log_weights"],
            residual_noise - step * perturb["residual_noise"],
        )
        plus_record = _r5_branch_record(reset_module, *plus_args, fixture, chart)
        minus_record = _r5_branch_record(reset_module, *minus_args, fixture, chart)
        np.testing.assert_array_equal(
            plus_record["floor_active"].numpy(),
            center_record["floor_active"].numpy(),
        )
        np.testing.assert_array_equal(
            minus_record["floor_active"].numpy(),
            center_record["floor_active"].numpy(),
        )
        np.testing.assert_allclose(
            plus_record["max_realized_ridge"].numpy(),
            center_record["max_realized_ridge"].numpy(),
        )
        np.testing.assert_allclose(
            minus_record["max_realized_ridge"].numpy(),
            center_record["max_realized_ridge"].numpy(),
        )
        assert int(plus_record["ridge_attempts_used"].numpy()) == int(
            center_record["ridge_attempts_used"].numpy()
        )
        assert int(minus_record["ridge_attempts_used"].numpy()) == int(
            center_record["ridge_attempts_used"].numpy()
        )
        assert not bool(plus_record["ridge_failure"].numpy())
        assert not bool(minus_record["ridge_failure"].numpy())

        manual_dot = tf.reduce_sum(manual[name] * direction)
        fd = (scalar(*plus_args) - scalar(*minus_args)) / (2.0 * step)
        np.testing.assert_allclose(
            float(manual_dot.numpy()),
            float(fd.numpy()),
            rtol=2.0e-4,
            atol=2.0e-6,
            err_msg=name,
        )


def test_r5_static_audit_blocks_hidden_autodiff_full_transport_and_eigh() -> None:
    local_sources = [
        _function_source(THIS_FILE, "_r5_transport_matrix_value_with_replayed_key"),
        _function_source(THIS_FILE, "_r5_forward_parts"),
        _function_source(THIS_FILE, "_r5_manual_vjp"),
        _function_source(THIS_FILE, "_r5_branch_record"),
    ]
    transport_sources = [
        _function_source(
            TRANSPORT_HELPER_PATH,
            "_filterflow_manual_dense_finite_transport_matrix_vjp_stopped_scale_keys",
        ),
        _function_source(
            TRANSPORT_HELPER_PATH,
            "_filterflow_manual_dense_finite_transport_matrix_value_stopped_scale_keys",
        ),
        _function_source(
            TRANSPORT_HELPER_PATH,
            "_filterflow_manual_dense_finite_transport_matrix_stopped_scale_keys",
        ),
        _function_source(
            TRANSPORT_HELPER_PATH,
            "_filterflow_manual_dense_finite_sinkhorn_outputs",
        ),
        _function_source(
            TRANSPORT_HELPER_PATH,
            "_filterflow_manual_dense_finite_sinkhorn_vjp",
        ),
        _function_source(
            TRANSPORT_HELPER_PATH,
            "_filterflow_manual_dense_finite_softmin_vjp",
        ),
        _function_source(
            TRANSPORT_HELPER_PATH,
            "_filterflow_manual_transport_from_potentials_vjp",
        ),
        _function_source(
            TRANSPORT_HELPER_PATH,
            "_filterflow_manual_same_particles_cost_vjp",
        ),
        _function_source(
            TRANSPORT_HELPER_PATH,
            "_filterflow_exact_transport_from_potentials",
        ),
        _function_source(TRANSPORT_HELPER_PATH, "_filterflow_exact_softmin"),
        _function_source(TRANSPORT_HELPER_PATH, "_filterflow_exact_cost"),
    ]
    forbidden = [
        "GradientTape",
        ".gradient(",
        ".jacobian(",
        "batch_jacobian",
        "ForwardAccumulator",
        "tf.gradients",
        "tf.compat.v1.gradients",
        "tf.linalg.eigh",
        'transport_ad_mode="full"',
        "transport_ad_mode='full'",
    ]
    for source in local_sources + transport_sources:
        for token in forbidden:
            assert token not in source

    gradient_source = GRADIENT_SCRIPT.read_text(encoding="utf-8")
    assert FULL_BLOCKER_CODE in gradient_source
