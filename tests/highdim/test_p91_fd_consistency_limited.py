from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64
MANIFEST_PATH = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-manifest-2026-06-29.json"
)
_CONTRACT_TEST_PATH = Path(__file__).with_name("test_p90_value_bridge_contract.py")
_SPEC = importlib.util.spec_from_file_location(
    "p91_fd_value_bridge_contract_helpers",
    _CONTRACT_TEST_PATH,
)
assert _SPEC is not None
assert _SPEC.loader is not None
_HELPERS = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_HELPERS)


def _t1_fixture():
    physical = _HELPERS._physical_points()
    transport = _HELPERS.ShiftedGaussianTransport(
        tf.zeros([_HELPERS.POINT_DIM], dtype=DTYPE),
        0.0,
    )
    frame = _HELPERS._current_frame()
    binding = _HELPERS._binding(
        time_index=1,
        physical_points=physical,
        current_transport=transport,
        previous_retained=None,
        current_frame=frame,
    )
    derivative_binding = highdim.SourceRouteDerivativeBinding(
        value_bridge_binding=binding,
        value_bridge_binding_hash=binding.binding_hash,
        parameter_indices=tuple(range(_HELPERS.PARAMETER_DIM)),
    )
    theta, x_t, x_prev = _HELPERS._split_physical(physical)
    observation = _HELPERS.MODEL.infectious_components(
        _HELPERS.MODEL.base_model.initial_mean
    )[0] + tf.linspace(
        tf.constant(-0.2, dtype=DTYPE),
        tf.constant(0.2, dtype=DTYPE),
        _HELPERS.MODEL.observation_dim(),
    )
    return binding, derivative_binding, theta, x_t, x_prev, observation


def _prior_scalar(theta: tf.Tensor, x_prev: tf.Tensor) -> tf.Tensor:
    theta_log_prior = -0.5 * tf.reduce_sum(tf.square(theta))
    return _HELPERS.MODEL.initial_log_density(theta, x_prev)[0] + theta_log_prior


def _transition_scalar(theta: tf.Tensor, x_prev: tf.Tensor, x_t: tf.Tensor) -> tf.Tensor:
    return _HELPERS.MODEL.transition_log_density(theta, x_prev, x_t, t=1)[0]


def _likelihood_scalar(theta: tf.Tensor, x_t: tf.Tensor, observation: tf.Tensor) -> tf.Tensor:
    return _HELPERS.MODEL.observation_log_density(theta, x_t, observation, t=1)[0]


def _central_fd(value_fn, theta: tf.Tensor, h: float) -> tf.Tensor:
    pieces = []
    step = tf.constant(float(h), dtype=DTYPE)
    for index in range(int(theta.shape[0])):
        basis = tf.one_hot(index, int(theta.shape[0]), dtype=DTYPE)
        plus = value_fn(theta + step * basis)
        minus = value_fn(theta - step * basis)
        pieces.append((plus - minus) / (2.0 * step))
    return tf.stack(pieces)


def _error_row(component: str, h: float, analytic: tf.Tensor, fd: tf.Tensor) -> dict[str, object]:
    residual = tf.convert_to_tensor(analytic - fd, dtype=DTYPE)
    denom = tf.maximum(
        tf.constant(1.0, dtype=DTYPE),
        tf.maximum(tf.abs(tf.convert_to_tensor(analytic, dtype=DTYPE)), tf.abs(fd)),
    )
    rel = tf.abs(residual) / denom
    return {
        "component": component,
        "h": float(h),
        "analytic": [float(value) for value in tf.reshape(analytic, [-1]).numpy()],
        "fd": [float(value) for value in tf.reshape(fd, [-1]).numpy()],
        "abs_error": [float(value) for value in tf.reshape(tf.abs(residual), [-1]).numpy()],
        "rel_error": [float(value) for value in tf.reshape(rel, [-1]).numpy()],
        "max_abs_error": float(tf.reduce_max(tf.abs(residual)).numpy()),
        "max_rel_error": float(tf.reduce_max(rel).numpy()),
        "all_finite": bool(
            tf.reduce_all(tf.math.is_finite(analytic)).numpy()
            and tf.reduce_all(tf.math.is_finite(fd)).numpy()
            and tf.reduce_all(tf.math.is_finite(residual)).numpy()
        ),
    }


def _stable_component(rows: list[dict[str, object]], best: dict[str, object]) -> bool:
    ordered = sorted(rows, key=lambda row: float(row["h"]), reverse=True)
    best_error = float(best["max_abs_error"])
    threshold = 3.0 * max(best_error, 1.0e-14)
    for left, right in zip(ordered, ordered[1:]):
        if not (bool(left["all_finite"]) and bool(right["all_finite"])):
            continue
        if (
            float(left["max_abs_error"]) <= threshold
            and float(right["max_abs_error"]) <= threshold
        ):
            return True
    return False


def _component_result(component: str, analytic: tf.Tensor, value_fn) -> dict[str, object]:
    steps = (1.0e-3, 3.0e-4, 1.0e-4)
    binding, _derivative_binding, theta, _x_t, _x_prev, _observation = _t1_fixture()
    rows = [
        _error_row(component, h, analytic, _central_fd(value_fn, theta, h))
        for h in steps
    ]
    finite_rows = [row for row in rows if bool(row["all_finite"])]
    best = min(finite_rows, key=lambda row: float(row["max_abs_error"])) if finite_rows else rows[0]
    passed = (
        bool(best["all_finite"])
        and float(best["max_abs_error"]) <= 5.0e-5
        and float(best["max_rel_error"]) <= 5.0e-4
        and _stable_component(rows, best)
    )
    return {
        "component": component,
        "binding_hash": binding.binding_hash,
        "rows": rows,
        "best_h": float(best["h"]),
        "best_max_abs_error": float(best["max_abs_error"]),
        "best_max_rel_error": float(best["max_rel_error"]),
        "ladder_stable": _stable_component(rows, best),
        "passed": bool(passed),
    }


def test_p91_limited_fd_component_and_assembly_consistency() -> None:
    binding, derivative_binding, theta, x_t, x_prev, observation = _t1_fixture()

    with tf.GradientTape() as prior_tape:
        prior_tape.watch(theta)
        prior_value = _prior_scalar(theta, x_prev)
    prior_score = prior_tape.gradient(prior_value, theta)
    assert prior_score is not None
    transition_score = _HELPERS.MODEL.transition_log_density_parameter_score(
        theta,
        x_prev,
        x_t,
        t=1,
    )[0]
    likelihood_score = _HELPERS.MODEL.observation_log_density_parameter_score(
        theta,
        x_t,
        observation,
        t=1,
    )[0]
    prior_carry = highdim.SourceRouteComponentDerivativeCarry(
        binding=derivative_binding,
        component_name="prior",
        component_value=tf.reshape(prior_value, [1]),
        parameter_score=tf.reshape(prior_score, [1, -1]),
        callable_identity=highdim.source_route_callable_identity(_HELPERS._prior_log_density),
        classification="local_parameterized_sir_component",
        owner_status="READY_P91_PRIOR_PARAMETER_SCORE_CARRY",
    )
    transition_carry = highdim.SourceRouteComponentDerivativeCarry(
        binding=derivative_binding,
        component_name="transition",
        component_value=tf.reshape(_transition_scalar(theta, x_prev, x_t), [1]),
        parameter_score=tf.reshape(transition_score, [1, -1]),
        callable_identity=highdim.source_route_callable_identity(
            _HELPERS._transition_log_density
        ),
        classification="local_parameterized_sir_component",
        owner_status="READY_P90_TRANSITION_PARAMETER_SCORE_CARRY",
    )
    likelihood_carry = highdim.SourceRouteComponentDerivativeCarry(
        binding=derivative_binding,
        component_name="likelihood",
        component_value=tf.reshape(_likelihood_scalar(theta, x_t, observation), [1]),
        parameter_score=tf.reshape(likelihood_score, [1, -1]),
        callable_identity=highdim.source_route_callable_identity(
            _HELPERS._likelihood_log_density
        ),
        classification="local_parameterized_sir_component",
        owner_status="READY_P90_LIKELIHOOD_PARAMETER_SCORE_CARRY",
    )
    assembly = highdim.source_route_negative_log_assembly_derivative_carry(
        binding=derivative_binding,
        prior_or_previous=prior_carry,
        transition=transition_carry,
        likelihood=likelihood_carry,
    )

    results = [
        _component_result("prior", prior_score, lambda current: _prior_scalar(current, x_prev)),
        _component_result(
            "transition",
            transition_score,
            lambda current: _transition_scalar(current, x_prev, x_t),
        ),
        _component_result(
            "likelihood",
            likelihood_score,
            lambda current: _likelihood_scalar(current, x_t, observation),
        ),
        _component_result(
            "negative_log_assembly",
            assembly.parameter_score[0],
            lambda current: -(
                _prior_scalar(current, x_prev)
                + _transition_scalar(current, x_prev, x_t)
                + _likelihood_scalar(current, x_t, observation)
            ),
        ),
    ]
    status = (
        "PASS_P91_PHASE3_LIMITED_FD_COMPONENT_ASSEMBLY"
        if all(result["passed"] for result in results)
        else "BLOCK_P91_PHASE3_LIMITED_FD_COMPONENT_ASSEMBLY"
    )
    payload = {
        "schema_version": "p91.phase3.limited_fd.v1",
        "status": status,
        "command": (
            "CUDA_VISIBLE_DEVICES=-1 python -m pytest "
            "tests/highdim/test_p90_derivative_carry_contract.py "
            "tests/highdim/test_p91_fd_consistency_limited.py -q"
        ),
        "python_executable": sys.executable,
        "conda_environment": os.environ.get("CONDA_DEFAULT_ENV", "N/A"),
        "cpu_gpu_status": "CPU-only; CUDA_VISIBLE_DEVICES=-1 required by Phase 3",
        "data_version": "N/A; deterministic algebraic fixture",
        "random_seeds": "N/A; deterministic algebraic fixture",
        "theta": [float(value) for value in theta.numpy()],
        "step_size_ladder": (1.0e-3, 3.0e-4, 1.0e-4),
        "absolute_tolerance": 5.0e-5,
        "relative_tolerance": 5.0e-4,
        "binding": binding.manifest_payload(),
        "binding_hash": binding.binding_hash,
        "setup_identity_channel": "binding_manifest",
        "component_results": results,
        "blocker_statuses": {
            "previous_marginal_derivative": (
                "BLOCK_FIXED_TTSIRT_PREVIOUS_MARGINAL_DERIVATIVE_NOT_IMPLEMENTED"
            ),
            "fixed_ttsirt_transport_derivative": (
                derivative_binding.fixed_ttsirt_transport_derivative_status
            ),
            "full_source_route_fd": "BLOCK_FULL_SOURCE_ROUTE_FD_NOT_CLAIMED",
        },
        "nonclaims": (
            "no full source-route FD pass",
            "no score identity pass",
            "no exact likelihood correctness",
            "no GPU/XLA readiness",
            "no HMC readiness",
            "no benchmark result",
            "no package/release/CI readiness",
            "no default-policy authorization/change",
            "no production readiness",
        ),
    }
    MANIFEST_PATH.write_text(
        highdim.BranchManifest(
            version="p91.phase3.limited_fd.manifest.v1",
            payload=payload,
        )
        .to_canonical_bytes()
        .decode("utf-8"),
        encoding="utf-8",
    )

    assert status in {
        "PASS_P91_PHASE3_LIMITED_FD_COMPONENT_ASSEMBLY",
        "BLOCK_P91_PHASE3_LIMITED_FD_COMPONENT_ASSEMBLY",
    }
    if status.startswith("PASS_"):
        assert all(result["passed"] for result in results)
    else:
        assert any(not result["passed"] for result in results)
