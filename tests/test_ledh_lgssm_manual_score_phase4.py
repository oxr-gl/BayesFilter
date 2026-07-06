from __future__ import annotations

import argparse
import ast
import inspect
import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import tensorflow as tf

from docs.benchmarks import benchmark_ledh_same_target_lgssm_m3_t50_value as lgssm
from scripts import audit_ledh_no_autodiff as audit


def _args(*, transport_policy: str = "active-all") -> argparse.Namespace:
    return argparse.Namespace(
        batch_seeds=[81120],
        num_particles=4,
        time_steps=2,
        transport_policy=transport_policy,
        sinkhorn_iterations=2,
        sinkhorn_epsilon=0.5,
        annealed_scaling=0.9,
        annealed_convergence_threshold=1.0e-3,
        transport_gradient_mode=lgssm.core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE,
        transport_ad_mode="full",
        row_chunk_size=4,
        col_chunk_size=4,
        particle_chunk_size=4,
        score_fd_step=1.0e-5,
        score_fd_atol=5.0e-3,
        score_fd_rtol=5.0e-3,
        dtype="float64",
        tf32_mode="disabled",
    )


def test_phase4_lgssm_manual_score_matches_same_scalar_fd_for_active_transport() -> None:
    args = _args()
    args.score_mode = "compact-sensitivity"
    lgssm._configure_precision(args)

    diagnostic = lgssm._manual_score_diagnostic(
        args,
        tf.constant(lgssm.TRUTH_THETA, dtype=lgssm.DTYPE),
    )

    assert diagnostic["score_route"] == lgssm.COMPACT_SCORE_ROUTE_ID
    assert diagnostic["old_full_history_route_status"] == "historical_diagnostic_only"
    assert diagnostic["value_score_route_status"] == "same_route_value_score"
    assert diagnostic["value_score_same_transport_algorithm"] is True
    assert diagnostic["same_scalar_fd"]["status"] == "pass"
    assert diagnostic["same_scalar_fd"]["max_abs_error"] <= 1.0e-6


def test_phase4_lgssm_manual_score_runs_under_runtime_autodiff_sentinel() -> None:
    args = _args(transport_policy="active-all")
    args.score_mode = "compact-sensitivity"
    lgssm._configure_precision(args)

    with audit.AutodiffRuntimeSentinel(lgssm.tf, route_id="phase4_lgssm_manual_score"):
        diagnostic = lgssm._manual_score_diagnostic(
            args,
            tf.constant(lgssm.TRUTH_THETA, dtype=lgssm.DTYPE),
        )

    assert diagnostic["no_autodiff_score_route"] is True
    assert diagnostic["same_scalar_fd"]["status"] == "pass"


def test_phase4_lgssm_compact_score_matches_historical_manual_reverse_diagnostic() -> None:
    args = _args(transport_policy="active-all")
    lgssm._configure_precision(args)
    tensors = lgssm._build_lgssm_manual_tensors(
        args,
        tf.constant(lgssm.TRUTH_THETA, dtype=lgssm.DTYPE),
    )
    theta = tf.constant(lgssm.TRUTH_THETA, dtype=lgssm.DTYPE)

    compact = lgssm._compact_value_and_score_from_components(tensors, args, theta)
    historical = lgssm._manual_value_and_score_from_components(tensors, args, theta)

    tf.debugging.assert_near(compact["objective"], historical["objective"], atol=1.0e-8)
    tf.debugging.assert_near(
        compact["gradient_tensor"],
        historical["gradient_tensor"],
        atol=5.0e-6,
    )


def test_phase4_lgssm_score_admission_promotes_only_compact_default_route() -> None:
    compact = lgssm._score_admission_decision(
        score_mode="compact-sensitivity",
        fd_status="pass",
        same_target_full_row=True,
        runtime_gate_applicable=True,
    )
    historical = lgssm._score_admission_decision(
        score_mode="manual-reverse",
        fd_status="pass",
        same_target_full_row=True,
        runtime_gate_applicable=True,
    )

    assert compact["score_admission_status"] == "admitted_same_target_compact_score"
    assert compact["score_status"] == "executed_same_target_compact_score_fd_pass_gpu_material"
    assert historical["score_admission_status"] == "blocked_historical_manual_reverse_not_default"
    assert historical["score_status"] == "executed_historical_manual_reverse_score_fd_pass_not_admitted"


def test_phase4_lgssm_full_row_identity_requires_full_particle_seed_and_transport_settings() -> None:
    diagnostic_args = _args()
    _tensors, diagnostic_identity = lgssm._build_lgssm_tensors(diagnostic_args)

    full_args = _args()
    full_args.batch_seeds = list(lgssm.FULL_ROW_BATCH_SEEDS)
    full_args.num_particles = lgssm.FULL_ROW_NUM_PARTICLES
    full_args.time_steps = lgssm.FULL_ROW_TIME_STEPS
    full_args.sinkhorn_iterations = lgssm.FULL_ROW_SINKHORN_ITERATIONS
    full_args.sinkhorn_epsilon = lgssm.FULL_ROW_SINKHORN_EPSILON
    full_args.transport_policy = lgssm.FULL_ROW_TRANSPORT_POLICY
    _tensors, full_identity = lgssm._build_lgssm_tensors(full_args)

    assert diagnostic_identity["full_leaderboard_row"] is False
    assert full_identity["full_leaderboard_row"] is True


def test_phase4_lgssm_manual_score_source_has_no_tape_or_forward_accumulator() -> None:
    helper_names = {
        "_compact_value_and_score_from_components",
        "_compact_forward_transport_jvp_tf",
        "_normalize_log_weights_jvp",
        "_batched_gaussian_logpdf_jvp",
        "_manual_value_and_score_from_components",
        "_manual_score_diagnostic",
        "_manual_transport_vjp_tf",
        "_manual_forward_transport_tf",
    }
    forbidden_attrs = {"GradientTape", "ForwardAccumulator"}
    forbidden_calls = {"gradient", "jacobian", "batch_jacobian", "watch"}
    for name in helper_names:
        source = inspect.getsource(getattr(lgssm, name))
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute):
                assert node.attr not in forbidden_attrs | forbidden_calls
            if isinstance(node, ast.Name):
                assert node.id not in forbidden_attrs
