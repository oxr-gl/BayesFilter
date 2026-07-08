from __future__ import annotations

import argparse
import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import tensorflow as tf

from docs.benchmarks import benchmark_p8p_parameterized_sir_gradient as p8p
from docs.benchmarks import benchmark_p8p_regression_fd_reparameterization as p8p_regression
from scripts import audit_ledh_no_autodiff as audit


def _args(*, dtype: str = "float64") -> argparse.Namespace:
    return argparse.Namespace(
        batch_seeds=[81120],
        time_steps=1,
        num_particles=2,
        theta_values=[0.02, -0.01, 0.01],
        transport_policy="active-all",
        sinkhorn_iterations=1,
        sinkhorn_epsilon=1.0,
        annealed_scaling=0.9,
        annealed_convergence_threshold=1.0e-3,
        transport_plan_mode="streaming",
        transport_gradient_mode=p8p.core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE,
        transport_ad_mode="full",
        row_chunk_size=2,
        col_chunk_size=2,
        particle_chunk_size=2,
        dtype=dtype,
        tf32_mode="disabled" if dtype == "float64" else "enabled",
        seed_microbatch_size=0,
    )


def test_p7_manual_score_matches_tiny_diagnostic_autodiff() -> None:
    args = _args()
    p8p._configure_precision(args)
    tensors, _semantics = p8p._build_base_tensors(args)

    manual = p8p._manual_gradient_diagnostic(tensors, args, args.theta_values)
    diagnostic = p8p._gradient_diagnostic(tensors, args, args.theta_values)

    np.testing.assert_allclose(
        manual["log_likelihood"].numpy(),
        diagnostic["log_likelihood"].numpy(),
        atol=1.0e-10,
        rtol=1.0e-10,
    )
    np.testing.assert_allclose(
        manual["gradient_tensor"].numpy(),
        diagnostic["gradient_tensor"].numpy(),
        atol=1.0e-9,
        rtol=1.0e-9,
    )
    assert manual["score_route"] == "manual_reverse_scan_no_autodiff"


def test_p7_manual_score_runs_under_runtime_autodiff_sentinel() -> None:
    args = _args(dtype="float32")
    args.transport_ad_mode = "stabilized"
    p8p._configure_precision(args)
    tensors, _semantics = p8p._build_base_tensors(args)

    with audit.AutodiffRuntimeSentinel(p8p.tf, route_id="p7_manual_score"):
        diagnostic = p8p._manual_gradient_diagnostic(tensors, args, args.theta_values)

    assert bool(tf.reduce_all(tf.math.is_finite(diagnostic["log_likelihood"])).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(diagnostic["gradient_tensor"])).numpy())
    assert diagnostic["gradients_connected"] is True


def test_p7_manual_full_transport_score_runs_under_runtime_autodiff_sentinel() -> None:
    args = _args(dtype="float32")
    args.transport_ad_mode = "full"
    p8p._configure_precision(args)
    tensors, _semantics = p8p._build_base_tensors(args)

    with audit.AutodiffRuntimeSentinel(p8p.tf, route_id="p7_manual_full_score"):
        diagnostic = p8p._manual_gradient_diagnostic(tensors, args, args.theta_values)

    assert bool(tf.reduce_all(tf.math.is_finite(diagnostic["log_likelihood"])).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(diagnostic["gradient_tensor"])).numpy())
    assert diagnostic["gradients_connected"] is True
    assert diagnostic["score_route"] == "manual_reverse_scan_no_autodiff"


def test_p7_manual_score_decomposition_reconstructs_gradient() -> None:
    args = _args(dtype="float32")
    args.transport_ad_mode = "stabilized"
    p8p._configure_precision(args)
    tensors, _semantics = p8p._build_base_tensors(args)

    diagnostic = p8p._manual_value_and_score_from_components(
        tensors,
        args,
        p8p._theta_components(args.theta_values),
        return_score_decomposition=True,
    )

    components = diagnostic["manual_score_components"]
    per_seed_gradient = diagnostic["per_seed_gradient"]
    np.testing.assert_allclose(
        tf.reduce_sum(components, axis=0).numpy(),
        per_seed_gradient.numpy(),
        atol=1.0e-4,
        rtol=1.0e-5,
    )
    assert components.shape[0] == len(p8p.MANUAL_SCORE_COMPONENT_NAMES)


def test_p7_manual_no_resampling_transport_shortcuts_are_identity() -> None:
    args = _args(dtype="float32")
    args.transport_ad_mode = "stabilized"
    args.transport_policy = "no-resampling"
    p8p._configure_precision(args)
    post_flow = tf.reshape(
        tf.range(36, dtype=p8p.DTYPE),
        [1, 2, 18],
    )
    normalized_log_weights = tf.constant([[-0.25, -1.5]], dtype=p8p.DTYPE)
    mask = tf.zeros([1], dtype=tf.bool)
    upstream = tf.ones_like(post_flow)

    next_particles, next_log_weights = p8p._manual_forward_transport_tf(
        post_flow=post_flow,
        normalized_log_weights=normalized_log_weights,
        mask=mask,
        args=args,
    )
    bar_post, bar_logw = p8p._manual_transport_vjp_tf(
        post_flow=post_flow,
        normalized_log_weights=normalized_log_weights,
        mask=mask,
        args=args,
        upstream_particles=upstream,
    )

    np.testing.assert_allclose(next_particles.numpy(), post_flow.numpy())
    np.testing.assert_allclose(next_log_weights.numpy(), normalized_log_weights.numpy())
    np.testing.assert_allclose(bar_post.numpy(), np.zeros_like(post_flow.numpy()))
    np.testing.assert_allclose(bar_logw.numpy(), np.zeros_like(normalized_log_weights.numpy()))


def test_p7_context_aggregation_uses_manual_route() -> None:
    args = _args(dtype="float32")
    args.transport_ad_mode = "stabilized"
    p8p._configure_precision(args)
    contexts, _semantics = p8p_regression._build_microbatch_contexts(args)

    with audit.AutodiffRuntimeSentinel(p8p.tf, route_id="p7_context_manual_score"):
        diagnostic = p8p_regression._manual_gradient_diagnostic_for_contexts(
            contexts,
            args.theta_values,
        )

    assert diagnostic["score_route"] == "manual_reverse_scan_no_autodiff"
    assert diagnostic["per_seed_gradient"].shape == (1, len(p8p.PARAMETER_NAMES))
    assert bool(tf.reduce_all(tf.math.is_finite(diagnostic["gradient_tensor"])).numpy())
