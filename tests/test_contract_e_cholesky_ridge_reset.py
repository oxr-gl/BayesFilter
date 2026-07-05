from __future__ import annotations

import ast
import importlib.util
import os
from pathlib import Path


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf


ROOT = Path(__file__).resolve().parents[1]
RESET_HELPER_PATH = ROOT / "docs" / "benchmarks" / "contract_e_reset_tf.py"
GRADIENT_SCRIPT = (
    ROOT / "docs" / "benchmarks" / "diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py"
)
VALUE_SCRIPT = ROOT / "docs" / "benchmarks" / "diagnose_ledh_pfpf_ot_contract_e_lgssm_value.py"
FULL_BLOCKER_CODE = "PHASE3_MATERIAL_FULL_GATE_PENDING_T10_MANUAL_ROUTE_VALIDATION"
DTYPE = tf.float64


def _fixture() -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
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
    logits = tf.constant([[-0.25, 0.15, -0.75, 0.30]], dtype=DTYPE)
    weights = tf.nn.softmax(logits, axis=1)
    matrix = tf.constant(
        [
            [
                [0.50, 0.25, 0.10, 0.15],
                [0.15, 0.40, 0.25, 0.20],
                [0.20, 0.15, 0.45, 0.20],
                [0.15, 0.20, 0.20, 0.45],
            ]
        ],
        dtype=DTYPE,
    )
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
    upstream = tf.reshape(tf.linspace(tf.constant(-0.2, DTYPE), tf.constant(0.3, DTYPE), 8), [1, 4, 2])
    ridge = tf.constant([1.0e-3], dtype=DTYPE)
    return post_flow, logits, weights, matrix, residual_noise, upstream, ridge


def _load_reset_module():
    spec = importlib.util.spec_from_file_location("contract_e_reset_tf_test", RESET_HELPER_PATH)
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


def test_cholesky_ridge_reset_local_fixture_preserves_mean_and_reports_residual() -> None:
    reset_module = _load_reset_module()
    post_flow = tf.constant(
        [
            [
                [-1.0, 0.2],
                [0.0, -0.4],
                [0.8, 0.6],
                [1.5, -0.1],
            ]
        ],
        dtype=tf.float32,
    )
    weights = tf.constant([[0.2, 0.3, 0.1, 0.4]], dtype=tf.float32)
    matrix = tf.constant(
        [
            [
                [0.50, 0.25, 0.10, 0.15],
                [0.15, 0.40, 0.25, 0.20],
                [0.20, 0.15, 0.45, 0.20],
                [0.15, 0.20, 0.20, 0.45],
            ]
        ],
        dtype=tf.float32,
    )
    residual_noise = tf.constant(
        [
            [
                [-0.3, 0.7],
                [0.5, -0.2],
                [1.0, 0.1],
                [-0.4, -0.8],
            ]
        ],
        dtype=tf.float32,
    )

    reset = reset_module.contract_e_cholesky_ridge_reset(
        tf,
        post_flow=post_flow,
        weights=weights,
        matrix=matrix,
        residual_noise=residual_noise,
        rho=tf.constant(1.0, dtype=tf.float32),
        ridge_rel=tf.constant(1.0e-4, dtype=tf.float32),
        ridge_abs=tf.constant(1.0e-5, dtype=tf.float32),
        ridge_escalation=tf.constant(10.0, dtype=tf.float32),
        ridge_max_attempts=tf.constant(3, dtype=tf.int32),
    )

    particles = reset["particles"].numpy()
    target_mean = tf.reduce_sum(weights[:, :, None] * post_flow, axis=1).numpy()
    star_mean = np.mean(particles, axis=1)

    np.testing.assert_allclose(star_mean, target_mean, atol=2.0e-6)
    assert np.isfinite(particles).all()
    assert float(reset["max_covariance_relative_residual"].numpy()) < 5.0e-3
    assert float(reset["max_mean_linf_residual"].numpy()) < 2.0e-6
    assert float(reset["max_realized_ridge"].numpy()) > 0.0
    assert int(reset["ridge_attempts_used"].numpy()) >= 1
    assert bool(reset["ridge_failure"].numpy()) is False


def test_cholesky_ridge_helper_has_no_eigh_or_hidden_autodiff() -> None:
    sources = [
        _function_source(RESET_HELPER_PATH, "contract_e_cholesky_ridge_reset"),
        _function_source(RESET_HELPER_PATH, "contract_e_cholesky_ridge_reset_fixed_ridge"),
        _function_source(RESET_HELPER_PATH, "contract_e_cholesky_ridge_reset_fixed_ridge_vjp"),
        _function_source(RESET_HELPER_PATH, "_contract_e_cholesky_ridge_fixed_ridge_forward"),
    ]

    forbidden = [
        "tf.linalg.eigh",
        "GradientTape",
        "tf.gradients",
        "tf.compat.v1.gradients",
        ".gradient(",
        ".jacobian(",
        "batch_jacobian",
        "ForwardAccumulator",
    ]
    for source in sources:
        for token in forbidden:
            assert token not in source

        assert "tf.linalg.cholesky" in RESET_HELPER_PATH.read_text(encoding="utf-8")
        assert "tf.linalg.triangular_solve" in RESET_HELPER_PATH.read_text(encoding="utf-8")


def test_cholesky_ridge_fixed_ridge_vjp_matches_central_fd_and_records_fixed_chart() -> None:
    reset_module = _load_reset_module()
    post_flow, logits, weights, matrix, residual_noise, upstream, ridge = _fixture()
    rho = tf.constant(1.0, dtype=DTYPE)

    def objective(
        local_post_flow: tf.Tensor,
        local_logits: tf.Tensor,
        local_matrix: tf.Tensor,
        local_residual_noise: tf.Tensor,
    ) -> tf.Tensor:
        local_weights = tf.nn.softmax(local_logits, axis=1)
        reset = reset_module.contract_e_cholesky_ridge_reset_fixed_ridge(
            tf,
            post_flow=local_post_flow,
            weights=local_weights,
            matrix=local_matrix,
            residual_noise=local_residual_noise,
            rho=rho,
            ridge=ridge,
        )
        return tf.reduce_sum(reset["particles"] * upstream)

    def branchy_reset(
        local_post_flow: tf.Tensor,
        local_logits: tf.Tensor,
        local_matrix: tf.Tensor,
        local_residual_noise: tf.Tensor,
    ) -> dict[str, tf.Tensor]:
        return reset_module.contract_e_cholesky_ridge_reset(
            tf,
            post_flow=local_post_flow,
            weights=tf.nn.softmax(local_logits, axis=1),
            matrix=local_matrix,
            residual_noise=local_residual_noise,
            rho=rho,
            ridge_rel=tf.constant(0.0, dtype=DTYPE),
            ridge_abs=ridge[0],
            ridge_escalation=tf.constant(10.0, dtype=DTYPE),
            ridge_max_attempts=tf.constant(3, dtype=tf.int32),
        )

    vjp = reset_module.contract_e_cholesky_ridge_reset_fixed_ridge_vjp(
        tf,
        post_flow=post_flow,
        weights=weights,
        matrix=matrix,
        residual_noise=residual_noise,
        rho=rho,
        ridge=ridge,
        upstream_particles=upstream,
    )
    weights_bar = vjp["weights"]
    logits_bar = weights * (
        weights_bar - tf.reduce_sum(weights * weights_bar, axis=1, keepdims=True)
    )
    directions = {
        "post_flow": tf.reshape(tf.linspace(tf.constant(-0.03, DTYPE), tf.constant(0.04, DTYPE), 8), [1, 4, 2]),
        "logits": tf.constant([[0.02, -0.03, 0.01, -0.015]], dtype=DTYPE),
        "matrix": tf.reshape(tf.linspace(tf.constant(-0.02, DTYPE), tf.constant(0.025, DTYPE), 16), [1, 4, 4]),
        "residual_noise": tf.reshape(tf.linspace(tf.constant(0.01, DTYPE), tf.constant(-0.035, DTYPE), 8), [1, 4, 2]),
    }
    manual = {
        "post_flow": tf.reduce_sum(vjp["post_flow"] * directions["post_flow"]),
        "logits": tf.reduce_sum(logits_bar * directions["logits"]),
        "matrix": tf.reduce_sum(vjp["matrix"] * directions["matrix"]),
        "residual_noise": tf.reduce_sum(vjp["residual_noise"] * directions["residual_noise"]),
    }
    step = tf.constant(1.0e-5, dtype=DTYPE)
    zeros = {
        "post_flow": tf.zeros_like(post_flow),
        "logits": tf.zeros_like(logits),
        "matrix": tf.zeros_like(matrix),
        "residual_noise": tf.zeros_like(residual_noise),
    }

    for name, direction in directions.items():
        perturb = dict(zeros)
        perturb[name] = direction
        plus_args = (
            post_flow + step * perturb["post_flow"],
            logits + step * perturb["logits"],
            matrix + step * perturb["matrix"],
            residual_noise + step * perturb["residual_noise"],
        )
        minus_args = (
            post_flow - step * perturb["post_flow"],
            logits - step * perturb["logits"],
            matrix - step * perturb["matrix"],
            residual_noise - step * perturb["residual_noise"],
        )
        center = branchy_reset(post_flow, logits, matrix, residual_noise)
        plus = branchy_reset(*plus_args)
        minus = branchy_reset(*minus_args)
        np.testing.assert_allclose(plus["max_realized_ridge"].numpy(), center["max_realized_ridge"].numpy())
        np.testing.assert_allclose(minus["max_realized_ridge"].numpy(), center["max_realized_ridge"].numpy())
        assert int(plus["ridge_attempts_used"].numpy()) == int(center["ridge_attempts_used"].numpy())
        assert int(minus["ridge_attempts_used"].numpy()) == int(center["ridge_attempts_used"].numpy())

        fd = (objective(*plus_args) - objective(*minus_args)) / (2.0 * step)
        np.testing.assert_allclose(
            float(manual[name].numpy()),
            float(fd.numpy()),
            rtol=5.0e-4,
            atol=5.0e-6,
            err_msg=name,
        )


def test_minimal_stabilizing_ridge_uses_base_when_stable() -> None:
    reset_module = _load_reset_module()
    post_flow, _logits, weights, matrix, residual_noise, _upstream, _ridge = _fixture()
    selection = reset_module.contract_e_minimal_stabilizing_cholesky_ridge(
        tf,
        post_flow=post_flow,
        weights=weights,
        matrix=matrix,
        residual_noise=residual_noise,
        rho=tf.constant(1.0, dtype=DTYPE),
        ridge_rel=tf.constant(0.0, dtype=DTYPE),
        ridge_abs=tf.constant(1.0e-3, dtype=DTYPE),
        ridge_escalation=tf.constant(10.0, dtype=DTYPE),
        ridge_max_attempts=tf.constant(4, dtype=tf.int32),
    )

    np.testing.assert_allclose(selection["ridge"].numpy(), [1.0e-3])
    np.testing.assert_allclose(selection["base_ridge"].numpy(), [1.0e-3])
    np.testing.assert_array_equal(selection["attempts_used"].numpy(), [1])
    assert bool(selection["ridge_failure"].numpy()) is False


def test_minimal_stabilizing_ridge_escalates_only_unstable_batches() -> None:
    reset_module = _load_reset_module()
    post_flow, _logits, weights, _matrix, residual_noise, _upstream, _ridge = _fixture()
    batch_post_flow = tf.concat([post_flow, post_flow], axis=0)
    batch_weights = tf.concat([weights, weights], axis=0)
    identity_matrix = tf.eye(4, dtype=DTYPE)[None, :, :]
    averaging_matrix = tf.fill([1, 4, 4], tf.constant(0.25, dtype=DTYPE))
    matrix = tf.concat([averaging_matrix, identity_matrix], axis=0)
    batch_residual_noise = tf.concat([residual_noise, residual_noise], axis=0)

    selection = reset_module.contract_e_minimal_stabilizing_cholesky_ridge(
        tf,
        post_flow=batch_post_flow,
        weights=batch_weights,
        matrix=matrix,
        residual_noise=batch_residual_noise,
        rho=tf.constant(1.0, dtype=DTYPE),
        ridge_rel=tf.constant(0.0, dtype=DTYPE),
        ridge_abs=tf.constant(1.0e-9, dtype=DTYPE),
        ridge_escalation=tf.constant(10.0, dtype=DTYPE),
        ridge_max_attempts=tf.constant(12, dtype=tf.int32),
    )

    realized = selection["ridge"].numpy()
    attempts = selection["attempts_used"].numpy()
    assert realized[0] == pytest.approx(1.0e-9)
    assert attempts[0] == 1
    assert realized[1] > realized[0]
    assert attempts[1] > attempts[0]
    assert bool(selection["ridge_failure"].numpy()) is False


def test_cholesky_ridge_route_is_opt_in_and_full_material_blocker_remains() -> None:
    gradient_source = GRADIENT_SCRIPT.read_text(encoding="utf-8")
    value_source = VALUE_SCRIPT.read_text(encoding="utf-8")

    for source in (gradient_source, value_source):
        assert "--contract-e-reset-factorization" in source
        assert 'default="eigh-support"' in source
        assert "--chol-ridge-rel" in source
        assert "--chol-ridge-abs" in source
        assert "--chol-ridge-escalation" in source
        assert "--chol-ridge-max-attempts" in source
        assert "contract_e_reset_tf.contract_e_cholesky_ridge_reset" in source

    reset_source = RESET_HELPER_PATH.read_text(encoding="utf-8")
    assert "contract_e_minimal_stabilizing_cholesky_ridge" in reset_source
    assert "smallest per-batch ridge" in reset_source

    assert FULL_BLOCKER_CODE in gradient_source
    assert "manual_likelihood_reverse_scan_no_autodiff" in gradient_source


def test_cholesky_ridge_evidence_fields_are_serialized() -> None:
    gradient_source = GRADIENT_SCRIPT.read_text(encoding="utf-8")
    value_source = VALUE_SCRIPT.read_text(encoding="utf-8")

    required_fields = [
        '"contract_e_reset_factorization"',
        '"chol_ridge_rel"',
        '"chol_ridge_abs"',
        '"chol_ridge_escalation"',
        '"chol_ridge_max_attempts"',
        '"max_realized_ridge"',
        '"max_ridge_attempts_used"',
        '"any_ridge_failure"',
        '"contract_e_diagnostic_labels"',
        '"gap_diagnostic_label"',
        '"tilde_positive_diagnostic_label"',
        '"rank_margin_diagnostic_label"',
        "min residual Cholesky diagonal",
    ]
    for source in (gradient_source, value_source):
        for field in required_fields:
            assert field in source
