from __future__ import annotations

import ast
import importlib.util
import math
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
LEDH_HELPER_PATH = (
    ROOT
    / "experiments"
    / "dpf_implementation"
    / "tf_tfp"
    / "filters"
    / "experimental_batched_ledh_pfpf_ot_tf.py"
)
THIS_FILE = Path(__file__)
ROUTE_LABEL = "contract_e_cholesky_fixed_ridge_manual_lgssm_tiny"
FULL_BLOCKER_CODE = "PHASE3_MATERIAL_FULL_GATE_PENDING_T10_MANUAL_ROUTE_VALIDATION"
DTYPE = tf.float64
annealed_transport_tf.DTYPE = DTYPE
ledh.DTYPE = DTYPE


def _load_reset_module() -> Any:
    spec = importlib.util.spec_from_file_location("contract_e_reset_tf_r7", RESET_HELPER_PATH)
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


def _fixture() -> dict[str, tf.Tensor | str]:
    return {
        "route_label": ROUTE_LABEL,
        "theta": tf.constant([[0.72, math.log(0.22), math.log(0.30)]], dtype=DTYPE),
        "initial_particles": tf.constant([[[-0.62], [-0.11], [0.27], [0.84]]], dtype=DTYPE),
        "transition_noise": tf.constant(
            [
                [
                    [[-0.35], [0.18], [0.62], [-0.21]],
                    [[0.41], [-0.47], [0.14], [0.53]],
                ]
            ],
            dtype=DTYPE,
        ),
        "residual_noise": tf.constant(
            [
                [
                    [[-0.28], [0.72], [0.48], [-0.18]],
                    [[0.36], [-0.58], [-0.44], [0.16]],
                ]
            ],
            dtype=DTYPE,
        ),
        "observations": tf.constant([[0.14], [-0.09]], dtype=DTYPE),
        "epsilon": tf.constant(0.55, dtype=DTYPE),
        "scaling": tf.constant(0.82, dtype=DTYPE),
        "steps": tf.constant(2, dtype=tf.int32),
        "floor": tf.constant(0.05, dtype=DTYPE),
        "ridge": tf.constant([0.75], dtype=DTYPE),
        "rho": tf.constant(1.0, dtype=DTYPE),
    }


def _theta_to_lgssm(values: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    eye = tf.ones([1, 1, 1], dtype=DTYPE)
    transition_matrix = values[:, 0, None, None] * eye
    transition_covariance = tf.exp(values[:, 1])[:, None, None] * eye
    observation_covariance = tf.exp(values[:, 2])[:, None, None] * eye
    return transition_matrix, transition_covariance, observation_covariance


def _diag_gaussian_logpdf(residual: tf.Tensor, covariance: tf.Tensor) -> tf.Tensor:
    variance = tf.linalg.diag_part(covariance)
    quad = tf.reduce_sum(tf.square(residual) / variance[:, None, :], axis=-1)
    log_det = tf.reduce_sum(tf.math.log(variance), axis=-1)
    return -0.5 * (tf.math.log(tf.constant(2.0 * math.pi, DTYPE)) + log_det[:, None] + quad)


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


def _transport_matrix_value_with_replayed_key(
    x: tf.Tensor,
    key: tf.Tensor,
    logw: tf.Tensor,
    fixture: dict[str, tf.Tensor | str],
    *,
    steps: int,
) -> tf.Tensor:
    eps = tf.convert_to_tensor(fixture["epsilon"], dtype=DTYPE)
    scaling = tf.convert_to_tensor(fixture["scaling"], dtype=DTYPE)
    epsilon0 = tf.convert_to_tensor(fixture["epsilon0"], dtype=DTYPE) if "epsilon0" in fixture else None
    if epsilon0 is None:
        raise AssertionError("epsilon0 must be replayed")
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


def _step_forward(
    reset_module: Any,
    post_flow: tf.Tensor,
    corrected_log_weights: tf.Tensor,
    residual_noise: tf.Tensor,
    fixture: dict[str, tf.Tensor | str],
    chart: dict[str, tf.Tensor],
) -> dict[str, tf.Tensor]:
    assert fixture["route_label"] == ROUTE_LABEL
    weights, increment = ledh._normalize_log_weights(corrected_log_weights)  # noqa: SLF001
    transport_logw = tf.math.log(tf.maximum(weights, tf.convert_to_tensor(fixture["floor"], dtype=DTYPE)))
    x = (post_flow - chart["center"]) / chart["scale"][:, None, None]
    transport_fixture = dict(fixture)
    transport_fixture["epsilon0"] = chart["epsilon0"]
    matrix = _transport_matrix_value_with_replayed_key(
        x,
        chart["key"],
        transport_logw,
        transport_fixture,
        steps=int(tf.get_static_value(fixture["steps"])),
    )
    reset = reset_module.contract_e_cholesky_ridge_reset_fixed_ridge(
        tf,
        post_flow=post_flow,
        weights=weights,
        matrix=matrix,
        residual_noise=residual_noise,
        rho=tf.convert_to_tensor(fixture["rho"], dtype=DTYPE),
        ridge=tf.convert_to_tensor(fixture["ridge"], dtype=DTYPE),
    )
    return {
        "particles": reset["particles"],
        "weights": weights,
        "increment": increment,
        "transport_logw": transport_logw,
        "matrix": matrix,
        "floor_active": weights > tf.convert_to_tensor(fixture["floor"], dtype=DTYPE),
        "cov_residual": reset["max_covariance_relative_residual"],
        "mean_residual": reset["max_mean_linf_residual"],
        "ridge": reset["max_realized_ridge"],
        "ridge_attempts": reset["ridge_attempts_used"],
        "ridge_failure": reset["ridge_failure"],
    }


def _base_charts(reset_module: Any, fixture: dict[str, tf.Tensor | str]) -> list[dict[str, tf.Tensor]]:
    values = tf.convert_to_tensor(fixture["theta"], dtype=DTYPE)
    transition_matrix, transition_covariance, observation_covariance = _theta_to_lgssm(values)
    transition_std = tf.sqrt(tf.linalg.diag_part(transition_covariance))
    h_jac = tf.ones([1, 4, 1, 1], dtype=DTYPE)
    particles = tf.convert_to_tensor(fixture["initial_particles"], dtype=DTYPE)
    log_weights = ledh.uniform_log_weights(1, 4)
    charts: list[dict[str, tf.Tensor]] = []
    for time_index in range(2):
        prior_mean = tf.einsum("bnj,bdj->bnd", particles, transition_matrix)
        noise = tf.convert_to_tensor(fixture["transition_noise"], dtype=DTYPE)[:, time_index, :, :]
        pre_flow = prior_mean + noise * transition_std[:, None, :]
        observation = tf.convert_to_tensor(fixture["observations"], dtype=DTYPE)[time_index]
        residual = observation[None, None, :] - pre_flow
        flow, _flow_aux = ledh._batched_ledh_linearized_flow_with_aux_tf(  # noqa: SLF001
            pre_flow_particles=pre_flow,
            prior_means=prior_mean,
            observation_jacobian=h_jac,
            observation_residual=residual,
            transition_covariance=transition_covariance,
            observation_covariance=observation_covariance,
        )
        post_flow = flow.post_flow_particles
        charts.append(_transport_chart(post_flow))
        transition_log_density = _diag_gaussian_logpdf(post_flow - prior_mean, transition_covariance)
        observation_log_density = _diag_gaussian_logpdf(
            post_flow - observation[None, None, :],
            observation_covariance,
        )
        corrected = (
            log_weights
            + transition_log_density
            + observation_log_density
            - flow.pre_flow_log_density
            + flow.forward_log_det
        )
        step = _step_forward(
            reset_module,
            post_flow,
            corrected,
            tf.convert_to_tensor(fixture["residual_noise"], dtype=DTYPE)[:, time_index, :, :],
            fixture,
            charts[-1],
        )
        particles = step["particles"]
        log_weights = ledh.uniform_log_weights(1, 4)
    return charts


def _forward_records(
    reset_module: Any,
    values: tf.Tensor,
    fixture: dict[str, tf.Tensor | str],
    charts: list[dict[str, tf.Tensor]],
) -> dict[str, Any]:
    assert fixture["route_label"] == ROUTE_LABEL
    transition_matrix, transition_covariance, observation_covariance = _theta_to_lgssm(values)
    transition_std = tf.sqrt(tf.linalg.diag_part(transition_covariance))
    h_jac = tf.ones([1, 4, 1, 1], dtype=DTYPE)
    particles = tf.convert_to_tensor(fixture["initial_particles"], dtype=DTYPE)
    log_weights = ledh.uniform_log_weights(1, 4)
    log_likelihood = tf.zeros([1], dtype=DTYPE)
    records: list[dict[str, tf.Tensor]] = []
    for time_index in range(2):
        observation = tf.convert_to_tensor(fixture["observations"], dtype=DTYPE)[time_index]
        ancestors = particles
        prior_mean = tf.einsum("bnj,bdj->bnd", ancestors, transition_matrix)
        noise = tf.convert_to_tensor(fixture["transition_noise"], dtype=DTYPE)[:, time_index, :, :]
        pre_flow = prior_mean + noise * transition_std[:, None, :]
        residual = observation[None, None, :] - pre_flow
        flow, flow_aux = ledh._batched_ledh_linearized_flow_with_aux_tf(  # noqa: SLF001
            pre_flow_particles=pre_flow,
            prior_means=prior_mean,
            observation_jacobian=h_jac,
            observation_residual=residual,
            transition_covariance=transition_covariance,
            observation_covariance=observation_covariance,
        )
        post_flow = flow.post_flow_particles
        transition_log_density = _diag_gaussian_logpdf(post_flow - prior_mean, transition_covariance)
        observation_log_density = _diag_gaussian_logpdf(
            post_flow - observation[None, None, :],
            observation_covariance,
        )
        corrected = (
            log_weights
            + transition_log_density
            + observation_log_density
            - flow.pre_flow_log_density
            + flow.forward_log_det
        )
        step = _step_forward(
            reset_module,
            post_flow,
            corrected,
            tf.convert_to_tensor(fixture["residual_noise"], dtype=DTYPE)[:, time_index, :, :],
            fixture,
            charts[time_index],
        )
        log_likelihood = log_likelihood + step["increment"]
        records.append(
            {
                "ancestors": ancestors,
                "current_log_weights": log_weights,
                "prior_mean": prior_mean,
                "noise": noise,
                "pre_flow": pre_flow,
                "flow_aux": flow_aux,
                "post_flow": post_flow,
                "observation": observation,
                "transition_covariance": transition_covariance,
                "observation_covariance": observation_covariance,
                "transition_matrix": transition_matrix,
                "transition_std": transition_std,
                "corrected": corrected,
                "step_particles": step["particles"],
                "weights": step["weights"],
                "transport_logw": step["transport_logw"],
                "matrix": step["matrix"],
                "floor_active": step["floor_active"],
                "ridge": step["ridge"],
                "ridge_attempts": tf.cast(step["ridge_attempts"], tf.int32),
                "ridge_failure": step["ridge_failure"],
                "residual_noise": tf.convert_to_tensor(fixture["residual_noise"], dtype=DTYPE)[
                    :, time_index, :, :
                ],
            }
        )
        particles = step["particles"]
        log_weights = ledh.uniform_log_weights(1, 4)
    return {
        "value": log_likelihood,
        "records": records,
        "final_particles": particles,
    }


def _step_vjp(
    reset_module: Any,
    record: dict[str, tf.Tensor],
    fixture: dict[str, tf.Tensor | str],
    chart: dict[str, tf.Tensor],
    upstream_particles: tf.Tensor,
    increment_upstream: tf.Tensor,
) -> dict[str, tf.Tensor]:
    reset_vjp = reset_module.contract_e_cholesky_ridge_reset_fixed_ridge_vjp(
        tf,
        post_flow=record["post_flow"],
        weights=record["weights"],
        matrix=record["matrix"],
        residual_noise=record["residual_noise"],
        rho=tf.convert_to_tensor(fixture["rho"], dtype=DTYPE),
        ridge=tf.convert_to_tensor(fixture["ridge"], dtype=DTYPE),
        upstream_particles=upstream_particles,
    )
    x = (record["post_flow"] - chart["center"]) / chart["scale"][:, None, None]
    transport_x_bar, transport_logw_bar = (
        annealed_transport_tf._filterflow_manual_dense_finite_transport_matrix_vjp_stopped_scale_keys(  # noqa: SLF001
            x,
            record["transport_logw"],
            tf.convert_to_tensor(fixture["epsilon"], dtype=DTYPE),
            chart["epsilon0"],
            tf.convert_to_tensor(fixture["scaling"], dtype=DTYPE),
            reset_vjp["matrix"],
            steps=int(tf.get_static_value(fixture["steps"])),
        )
    )
    post_flow_bar = reset_vjp["post_flow"] + transport_x_bar / chart["scale"][:, None, None]
    floor_bar = tf.where(record["floor_active"], transport_logw_bar, tf.zeros_like(transport_logw_bar))
    normalized_log_bar = record["weights"] * reset_vjp["weights"] + floor_bar
    corrected_bar, _weights, _increment = ledh._normalize_log_weights_vjp(  # noqa: SLF001
        record["corrected"],
        normalized_log_bar,
        increment_upstream,
    )
    return {
        "post_flow": post_flow_bar,
        "corrected": corrected_bar,
        "residual_noise": reset_vjp["residual_noise"],
        "transport_x_bar": transport_x_bar,
        "transport_logw_bar": transport_logw_bar,
    }


def _manual_value_and_score(
    reset_module: Any,
    values: tf.Tensor,
    fixture: dict[str, tf.Tensor | str],
    charts: list[dict[str, tf.Tensor]],
) -> dict[str, tf.Tensor]:
    forward = _forward_records(reset_module, values, fixture, charts)
    transition_matrix, transition_covariance, observation_covariance = _theta_to_lgssm(values)
    bar_particles = tf.zeros_like(forward["final_particles"])
    score = tf.zeros([1, 3], dtype=DTYPE)
    for time_index in reversed(range(2)):
        record = forward["records"][time_index]
        step_vjp = _step_vjp(
            reset_module,
            record,
            fixture,
            charts[time_index],
            bar_particles,
            tf.ones([1], dtype=DTYPE),
        )
        correction_bars = ledh._log_weight_correction_vjp(step_vjp["corrected"])  # noqa: SLF001
        transition_vjp = ledh._transition_gaussian_log_density_vjp(  # noqa: SLF001
            record["post_flow"],
            record["prior_mean"],
            transition_covariance,
            correction_bars["transition_log_density"],
        )
        observation_vjp = ledh._observation_gaussian_log_density_vjp(  # noqa: SLF001
            record["post_flow"],
            record["observation"],
            observation_covariance,
            correction_bars["observation_log_density"],
            residual_convention="model_minus_observation",
        )
        bar_post = (
            step_vjp["post_flow"]
            + transition_vjp["x_next"]
            + observation_vjp["predicted_observation"]
        )
        flow_vjp = ledh._batched_ledh_linearized_flow_vjp(  # noqa: SLF001
            record["flow_aux"],
            bar_post,
            correction_bars["pre_flow_log_density"],
            correction_bars["forward_log_det"],
        )
        bar_pre_flow = flow_vjp.pre_flow_particles - flow_vjp.observation_residual
        bar_prior_mean = transition_vjp["transition_mean"] + flow_vjp.prior_means + bar_pre_flow
        transition_matrix_score = tf.reduce_sum(bar_prior_mean * record["ancestors"], axis=[1, 2])
        transition_covariance_score = tf.reduce_sum(
            (transition_vjp["transition_covariance"] + flow_vjp.transition_covariance)
            * transition_covariance,
            axis=[1, 2],
        )
        pre_flow_noise_score = tf.reduce_sum(
            bar_pre_flow * record["noise"] * (0.5 * record["transition_std"][:, None, :]),
            axis=[1, 2],
        )
        observation_covariance_score = tf.reduce_sum(
            (observation_vjp["observation_covariance"] + flow_vjp.observation_covariance)
            * observation_covariance,
            axis=[1, 2],
        )
        score = score + tf.stack(
            [
                transition_matrix_score,
                transition_covariance_score + pre_flow_noise_score,
                observation_covariance_score,
            ],
            axis=1,
        )
        bar_particles = tf.einsum("bnd,bdj->bnj", bar_prior_mean, transition_matrix)
    return {
        "value": forward["value"],
        "score": score,
        "records": forward["records"],
        "final_bar_particles": bar_particles,
    }


def _branch_record(
    reset_module: Any,
    values: tf.Tensor,
    fixture: dict[str, tf.Tensor | str],
    charts: list[dict[str, tf.Tensor]],
) -> dict[str, list[np.ndarray] | list[float] | list[int] | list[bool]]:
    forward = _forward_records(reset_module, values, fixture, charts)
    return {
        "floor_active": [record["floor_active"].numpy() for record in forward["records"]],
        "ridge": [float(record["ridge"].numpy()) for record in forward["records"]],
        "ridge_attempts": [int(record["ridge_attempts"].numpy()) for record in forward["records"]],
        "ridge_failure": [bool(record["ridge_failure"].numpy()) for record in forward["records"]],
    }


def _assert_branch_record_matches(candidate: dict[str, Any], center: dict[str, Any]) -> None:
    for left, right in zip(candidate["floor_active"], center["floor_active"], strict=True):
        np.testing.assert_array_equal(left, right)
    np.testing.assert_allclose(candidate["ridge"], center["ridge"])
    assert candidate["ridge_attempts"] == center["ridge_attempts"]
    assert not any(candidate["ridge_failure"])


def test_r7_tiny_lgssm_manual_score_matches_same_scalar_fd() -> None:
    reset_module = _load_reset_module()
    fixture = _fixture()
    assert fixture["route_label"] == ROUTE_LABEL
    charts = _base_charts(reset_module, fixture)
    theta = tf.convert_to_tensor(fixture["theta"], dtype=DTYPE)
    manual = _manual_value_and_score(reset_module, theta, fixture, charts)
    center_record = _branch_record(reset_module, theta, fixture, charts)
    assert not any(center_record["ridge_failure"])
    assert np.linalg.norm(manual["score"].numpy()) > 1.0e-8
    step = tf.constant(1.0e-5, dtype=DTYPE)
    eye = tf.eye(3, dtype=DTYPE)
    for parameter_index in range(3):
        direction = eye[parameter_index][None, :]
        plus_theta = theta + step * direction
        minus_theta = theta - step * direction
        plus_record = _branch_record(reset_module, plus_theta, fixture, charts)
        minus_record = _branch_record(reset_module, minus_theta, fixture, charts)
        _assert_branch_record_matches(plus_record, center_record)
        _assert_branch_record_matches(minus_record, center_record)
        plus = _forward_records(reset_module, plus_theta, fixture, charts)["value"]
        minus = _forward_records(reset_module, minus_theta, fixture, charts)["value"]
        fd = (plus - minus) / (2.0 * step)
        np.testing.assert_allclose(
            float(manual["score"][0, parameter_index].numpy()),
            float(fd[0].numpy()),
            rtol=5.0e-4,
            atol=1.0e-5,
            err_msg=f"parameter {parameter_index}",
        )


def test_r7_static_audit_blocks_hidden_autodiff_full_transport_eigh_and_preserves_blocker() -> None:
    local_sources = [
        _function_source(THIS_FILE, "_theta_to_lgssm"),
        _function_source(THIS_FILE, "_diag_gaussian_logpdf"),
        _function_source(THIS_FILE, "_transport_chart"),
        _function_source(THIS_FILE, "_transport_matrix_value_with_replayed_key"),
        _function_source(THIS_FILE, "_step_forward"),
        _function_source(THIS_FILE, "_base_charts"),
        _function_source(THIS_FILE, "_forward_records"),
        _function_source(THIS_FILE, "_step_vjp"),
        _function_source(THIS_FILE, "_manual_value_and_score"),
        _function_source(THIS_FILE, "_branch_record"),
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
    ledh_sources = [
        _function_source(LEDH_HELPER_PATH, "_transition_gaussian_log_density_vjp"),
        _function_source(LEDH_HELPER_PATH, "_observation_gaussian_log_density_vjp"),
        _function_source(LEDH_HELPER_PATH, "_normalize_log_weights_vjp"),
        _function_source(LEDH_HELPER_PATH, "_log_weight_correction_vjp"),
        _function_source(LEDH_HELPER_PATH, "_batched_ledh_linearized_flow_vjp"),
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
        "contract_e_cholesky_ridge_reset(",
    ]
    for source in local_sources + reset_sources + transport_sources + ledh_sources:
        for token in forbidden:
            assert token not in source

    gradient_source = GRADIENT_SCRIPT.read_text(encoding="utf-8")
    assert FULL_BLOCKER_CODE in gradient_source
    assert ROUTE_LABEL in gradient_source
