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
    spec = importlib.util.spec_from_file_location("contract_e_reset_tf_r6", RESET_HELPER_PATH)
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


def _r6_fixture() -> dict[str, tf.Tensor]:
    post_flow0 = tf.constant(
        [
            [
                [-1.1, 0.25],
                [-0.1, -0.45],
                [0.75, 0.65],
                [1.45, -0.05],
            ]
        ],
        dtype=DTYPE,
    )
    corrected0 = tf.constant([[-0.31, 0.12, -0.24, 0.28]], dtype=DTYPE)
    corrected1 = tf.constant([[0.18, -0.22, 0.09, -0.16]], dtype=DTYPE)
    residual0 = tf.constant(
        [
            [
                [-0.28, 0.72],
                [0.48, -0.18],
                [1.04, 0.08],
                [-0.42, -0.82],
            ]
        ],
        dtype=DTYPE,
    )
    residual1 = tf.constant(
        [
            [
                [0.36, -0.58],
                [-0.44, 0.16],
                [0.82, 0.34],
                [-0.21, -0.73],
            ]
        ],
        dtype=DTYPE,
    )
    upstream0 = tf.reshape(
        tf.linspace(tf.constant(0.11, DTYPE), tf.constant(-0.23, DTYPE), 8),
        [1, 4, 2],
    )
    upstream1 = tf.reshape(
        tf.linspace(tf.constant(-0.19, DTYPE), tf.constant(0.31, DTYPE), 8),
        [1, 4, 2],
    )
    return {
        "post_flow0": post_flow0,
        "corrected_log_weights0": corrected0,
        "corrected_log_weights1": corrected1,
        "residual_noise0": residual0,
        "residual_noise1": residual1,
        "upstream_particles0": upstream0,
        "upstream_particles1": upstream1,
        "increment_upstream0": tf.constant([0.29], dtype=DTYPE),
        "increment_upstream1": tf.constant([-0.34], dtype=DTYPE),
        "transition_operator": tf.constant([[0.82, -0.16], [0.21, 0.74]], dtype=DTYPE),
        "transition_bias": tf.constant([0.045, -0.035], dtype=DTYPE),
        "epsilon": tf.constant(0.55, dtype=DTYPE),
        "scaling": tf.constant(0.82, dtype=DTYPE),
        "steps": tf.constant(2, dtype=tf.int32),
        "floor": tf.constant(0.05, dtype=DTYPE),
        "ridge": tf.constant([0.75], dtype=DTYPE),
        "rho": tf.constant(1.0, dtype=DTYPE),
    }


def _r6_transition_forward(particles: tf.Tensor, fixture: dict[str, tf.Tensor]) -> tf.Tensor:
    return (
        tf.einsum("bnd,de->bne", particles, fixture["transition_operator"])
        + fixture["transition_bias"][None, None, :]
    )


def _r6_transition_vjp(
    upstream_post_flow1: tf.Tensor,
    fixture: dict[str, tf.Tensor],
) -> tf.Tensor:
    return tf.einsum("bne,de->bnd", upstream_post_flow1, fixture["transition_operator"])


def _r6_transport_chart(post_flow: tf.Tensor) -> dict[str, tf.Tensor]:
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


def _r6_transport_matrix_value_with_replayed_key(
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


def _r6_step_forward(
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
    matrix = _r6_transport_matrix_value_with_replayed_key(
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
    return {
        "particles": reset["particles"],
        "weights": weights,
        "increment": increment,
        "transport_logw": transport_logw,
        "matrix": matrix,
        "floor_active": weights > fixture["floor"],
    }


def _r6_base_charts(
    reset_module: Any,
    fixture: dict[str, tf.Tensor],
) -> dict[str, dict[str, tf.Tensor]]:
    chart0 = _r6_transport_chart(fixture["post_flow0"])
    step0 = _r6_step_forward(
        reset_module,
        fixture["post_flow0"],
        fixture["corrected_log_weights0"],
        fixture["residual_noise0"],
        fixture,
        chart0,
    )
    post_flow1 = _r6_transition_forward(step0["particles"], fixture)
    return {
        "step0": chart0,
        "step1": _r6_transport_chart(post_flow1),
    }


def _r6_forward_parts(
    reset_module: Any,
    post_flow0: tf.Tensor,
    corrected_log_weights0: tf.Tensor,
    corrected_log_weights1: tf.Tensor,
    residual_noise0: tf.Tensor,
    residual_noise1: tf.Tensor,
    fixture: dict[str, tf.Tensor],
    charts: dict[str, dict[str, tf.Tensor]],
) -> dict[str, Any]:
    step0 = _r6_step_forward(
        reset_module,
        post_flow0,
        corrected_log_weights0,
        residual_noise0,
        fixture,
        charts["step0"],
    )
    post_flow1 = _r6_transition_forward(step0["particles"], fixture)
    step1 = _r6_step_forward(
        reset_module,
        post_flow1,
        corrected_log_weights1,
        residual_noise1,
        fixture,
        charts["step1"],
    )
    scalar = (
        tf.reduce_sum(step0["particles"] * fixture["upstream_particles0"])
        + tf.reduce_sum(step1["particles"] * fixture["upstream_particles1"])
        + tf.reduce_sum(step0["increment"] * fixture["increment_upstream0"])
        + tf.reduce_sum(step1["increment"] * fixture["increment_upstream1"])
    )
    return {
        "scalar": scalar,
        "post_flow1": post_flow1,
        "step0": step0,
        "step1": step1,
    }


def _r6_step_vjp(
    reset_module: Any,
    post_flow: tf.Tensor,
    corrected_log_weights: tf.Tensor,
    residual_noise: tf.Tensor,
    fixture: dict[str, tf.Tensor],
    chart: dict[str, tf.Tensor],
    upstream_particles: tf.Tensor,
    increment_upstream: tf.Tensor,
) -> dict[str, tf.Tensor]:
    forward = _r6_step_forward(
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
        upstream_particles=upstream_particles,
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
        increment_upstream,
    )
    return {
        "post_flow": post_flow_bar,
        "corrected_log_weights": corrected_bar,
        "residual_noise": reset_vjp["residual_noise"],
        "reset_matrix_bar": reset_vjp["matrix"],
        "transport_x_bar": transport_x_bar,
        "transport_logw_bar": transport_logw_bar,
    }


def _r6_manual_reverse_scan(
    reset_module: Any,
    post_flow0: tf.Tensor,
    corrected_log_weights0: tf.Tensor,
    corrected_log_weights1: tf.Tensor,
    residual_noise0: tf.Tensor,
    residual_noise1: tf.Tensor,
    fixture: dict[str, tf.Tensor],
    charts: dict[str, dict[str, tf.Tensor]],
) -> dict[str, tf.Tensor]:
    forward = _r6_forward_parts(
        reset_module,
        post_flow0,
        corrected_log_weights0,
        corrected_log_weights1,
        residual_noise0,
        residual_noise1,
        fixture,
        charts,
    )
    step1_vjp = _r6_step_vjp(
        reset_module,
        forward["post_flow1"],
        corrected_log_weights1,
        residual_noise1,
        fixture,
        charts["step1"],
        fixture["upstream_particles1"],
        fixture["increment_upstream1"],
    )
    particles0_bar_from_step1 = _r6_transition_vjp(step1_vjp["post_flow"], fixture)
    step0_upstream_particles = fixture["upstream_particles0"] + particles0_bar_from_step1
    step0_vjp = _r6_step_vjp(
        reset_module,
        post_flow0,
        corrected_log_weights0,
        residual_noise0,
        fixture,
        charts["step0"],
        step0_upstream_particles,
        fixture["increment_upstream0"],
    )
    return {
        "post_flow0": step0_vjp["post_flow"],
        "corrected_log_weights0": step0_vjp["corrected_log_weights"],
        "corrected_log_weights1": step1_vjp["corrected_log_weights"],
        "residual_noise0": step0_vjp["residual_noise"],
        "residual_noise1": step1_vjp["residual_noise"],
        "step1_post_flow_bar": step1_vjp["post_flow"],
        "particles0_bar_from_step1": particles0_bar_from_step1,
        "scalar": forward["scalar"],
    }


def _r6_branch_record(
    reset_module: Any,
    post_flow0: tf.Tensor,
    corrected_log_weights0: tf.Tensor,
    corrected_log_weights1: tf.Tensor,
    residual_noise0: tf.Tensor,
    residual_noise1: tf.Tensor,
    fixture: dict[str, tf.Tensor],
    charts: dict[str, dict[str, tf.Tensor]],
) -> dict[str, tf.Tensor]:
    forward = _r6_forward_parts(
        reset_module,
        post_flow0,
        corrected_log_weights0,
        corrected_log_weights1,
        residual_noise0,
        residual_noise1,
        fixture,
        charts,
    )

    def branchy(step: dict[str, tf.Tensor], post_flow: tf.Tensor, residual_noise: tf.Tensor) -> dict[str, tf.Tensor]:
        return reset_module.contract_e_cholesky_ridge_reset(
            tf,
            post_flow=post_flow,
            weights=step["weights"],
            matrix=step["matrix"],
            residual_noise=residual_noise,
            rho=fixture["rho"],
            ridge_rel=tf.constant(0.0, dtype=DTYPE),
            ridge_abs=fixture["ridge"][0],
            ridge_escalation=tf.constant(10.0, dtype=DTYPE),
            ridge_max_attempts=tf.constant(3, dtype=tf.int32),
        )

    branch0 = branchy(forward["step0"], post_flow0, residual_noise0)
    branch1 = branchy(forward["step1"], forward["post_flow1"], residual_noise1)
    return {
        "step0_floor_active": forward["step0"]["floor_active"],
        "step1_floor_active": forward["step1"]["floor_active"],
        "step0_max_realized_ridge": branch0["max_realized_ridge"],
        "step1_max_realized_ridge": branch1["max_realized_ridge"],
        "step0_ridge_attempts_used": branch0["ridge_attempts_used"],
        "step1_ridge_attempts_used": branch1["ridge_attempts_used"],
        "step0_ridge_failure": branch0["ridge_failure"],
        "step1_ridge_failure": branch1["ridge_failure"],
    }


def _direction(shape: tuple[int, ...], start: float, stop: float) -> tf.Tensor:
    count = 1
    for dim in shape:
        count *= dim
    return tf.reshape(
        tf.linspace(tf.constant(start, DTYPE), tf.constant(stop, DTYPE), count),
        shape,
    )


def _assert_branch_record_matches(
    candidate: dict[str, tf.Tensor],
    center: dict[str, tf.Tensor],
) -> None:
    for key in ("step0_floor_active", "step1_floor_active"):
        np.testing.assert_array_equal(candidate[key].numpy(), center[key].numpy())
    for key in ("step0_max_realized_ridge", "step1_max_realized_ridge"):
        np.testing.assert_allclose(candidate[key].numpy(), center[key].numpy())
    for key in ("step0_ridge_attempts_used", "step1_ridge_attempts_used"):
        assert int(candidate[key].numpy()) == int(center[key].numpy())
    assert not bool(candidate["step0_ridge_failure"].numpy())
    assert not bool(candidate["step1_ridge_failure"].numpy())


def test_r6_two_step_manual_reverse_scan_matches_same_scalar_fd() -> None:
    reset_module = _load_reset_module()
    fixture = _r6_fixture()
    charts = _r6_base_charts(reset_module, fixture)

    post_flow0 = fixture["post_flow0"]
    corrected0 = fixture["corrected_log_weights0"]
    corrected1 = fixture["corrected_log_weights1"]
    residual0 = fixture["residual_noise0"]
    residual1 = fixture["residual_noise1"]

    manual = _r6_manual_reverse_scan(
        reset_module,
        post_flow0,
        corrected0,
        corrected1,
        residual0,
        residual1,
        fixture,
        charts,
    )
    center_record = _r6_branch_record(
        reset_module,
        post_flow0,
        corrected0,
        corrected1,
        residual0,
        residual1,
        fixture,
        charts,
    )
    assert not bool(center_record["step0_ridge_failure"].numpy())
    assert not bool(center_record["step1_ridge_failure"].numpy())
    assert np.linalg.norm(manual["step1_post_flow_bar"].numpy()) > 1.0e-8
    assert np.linalg.norm(manual["particles0_bar_from_step1"].numpy()) > 1.0e-8

    directions = {
        "post_flow0": _direction(tuple(post_flow0.shape), -0.021, 0.018),
        "corrected_log_weights0": tf.constant([[0.014, -0.024, 0.019, -0.011]], dtype=DTYPE),
        "corrected_log_weights1": tf.constant([[-0.017, 0.013, -0.021, 0.025]], dtype=DTYPE),
        "residual_noise0": _direction(tuple(residual0.shape), 0.012, -0.019),
        "residual_noise1": _direction(tuple(residual1.shape), -0.016, 0.014),
    }
    zeros = {
        "post_flow0": tf.zeros_like(post_flow0),
        "corrected_log_weights0": tf.zeros_like(corrected0),
        "corrected_log_weights1": tf.zeros_like(corrected1),
        "residual_noise0": tf.zeros_like(residual0),
        "residual_noise1": tf.zeros_like(residual1),
    }
    step = tf.constant(1.0e-5, dtype=DTYPE)

    def scalar(
        local_post_flow0: tf.Tensor,
        local_corrected0: tf.Tensor,
        local_corrected1: tf.Tensor,
        local_residual0: tf.Tensor,
        local_residual1: tf.Tensor,
    ) -> tf.Tensor:
        return _r6_forward_parts(
            reset_module,
            local_post_flow0,
            local_corrected0,
            local_corrected1,
            local_residual0,
            local_residual1,
            fixture,
            charts,
        )["scalar"]

    for name, direction in directions.items():
        perturb = dict(zeros)
        perturb[name] = direction
        plus_args = (
            post_flow0 + step * perturb["post_flow0"],
            corrected0 + step * perturb["corrected_log_weights0"],
            corrected1 + step * perturb["corrected_log_weights1"],
            residual0 + step * perturb["residual_noise0"],
            residual1 + step * perturb["residual_noise1"],
        )
        minus_args = (
            post_flow0 - step * perturb["post_flow0"],
            corrected0 - step * perturb["corrected_log_weights0"],
            corrected1 - step * perturb["corrected_log_weights1"],
            residual0 - step * perturb["residual_noise0"],
            residual1 - step * perturb["residual_noise1"],
        )

        plus_record = _r6_branch_record(reset_module, *plus_args, fixture, charts)
        minus_record = _r6_branch_record(reset_module, *minus_args, fixture, charts)
        _assert_branch_record_matches(plus_record, center_record)
        _assert_branch_record_matches(minus_record, center_record)

        manual_dot = tf.reduce_sum(manual[name] * direction)
        fd = (scalar(*plus_args) - scalar(*minus_args)) / (2.0 * step)
        np.testing.assert_allclose(
            float(manual_dot.numpy()),
            float(fd.numpy()),
            rtol=3.0e-4,
            atol=5.0e-6,
            err_msg=name,
        )


def test_r6_static_audit_blocks_hidden_autodiff_full_transport_and_eigh() -> None:
    local_sources = [
        _function_source(THIS_FILE, "_r6_transition_forward"),
        _function_source(THIS_FILE, "_r6_transition_vjp"),
        _function_source(THIS_FILE, "_r6_transport_chart"),
        _function_source(THIS_FILE, "_r6_transport_matrix_value_with_replayed_key"),
        _function_source(THIS_FILE, "_r6_step_forward"),
        _function_source(THIS_FILE, "_r6_base_charts"),
        _function_source(THIS_FILE, "_r6_forward_parts"),
        _function_source(THIS_FILE, "_r6_step_vjp"),
        _function_source(THIS_FILE, "_r6_manual_reverse_scan"),
        _function_source(THIS_FILE, "_r6_branch_record"),
    ]
    reset_sources = [
        _function_source(RESET_HELPER_PATH, "contract_e_cholesky_ridge_reset_fixed_ridge"),
        _function_source(RESET_HELPER_PATH, "contract_e_cholesky_ridge_reset_fixed_ridge_vjp"),
        _function_source(RESET_HELPER_PATH, "_contract_e_cholesky_ridge_fixed_ridge_forward"),
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
    for source in local_sources + reset_sources + transport_sources:
        for token in forbidden:
            assert token not in source

    gradient_source = GRADIENT_SCRIPT.read_text(encoding="utf-8")
    assert FULL_BLOCKER_CODE in gradient_source
