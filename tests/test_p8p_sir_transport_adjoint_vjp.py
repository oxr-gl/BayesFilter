from __future__ import annotations

import argparse
import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np

from docs.benchmarks import diagnose_p8p_sir_transport_adjoint_vjp as diagnostic


def _args() -> argparse.Namespace:
    return argparse.Namespace(
        batch_size=2,
        num_particles=4,
        state_dim=3,
        sinkhorn_iterations=3,
        sinkhorn_epsilon=0.7,
        annealed_scaling=0.8,
        row_chunk_size=2,
        col_chunk_size=2,
        max_abs_tolerance=diagnostic.DEFAULT_MAX_ABS,
        rel_l2_tolerance=diagnostic.DEFAULT_REL_L2,
    )


def test_phase4_transport_adjoint_diagnostic_passes_contract() -> None:
    payload = diagnostic.run_diagnostic(_args())

    assert payload["passed"] is True
    assert payload["failure_localization"] == "pass"
    assert payload["environment"]["visible_cuda_devices"] == "-1"
    assert payload["comparator_guard"]["passed"] is True
    assert all(
        count == 0
        for count in payload["comparator_guard"]["forbidden_route_call_counts"].values()
    )
    assert {item["mask_case"] for item in payload["comparisons"]} == {
        "active_all",
        "inactive_all",
        "mixed",
    }
    for item in payload["comparisons"]:
        assert item["passed"], item
        assert item["max_abs_residual"] <= diagnostic.DEFAULT_MAX_ABS
        assert item["relative_l2_residual"] <= diagnostic.DEFAULT_REL_L2


def test_transport_contribution_vjp_matches_independent_autodiff_for_mixed_mask() -> None:
    diagnostic._configure_float64_cpu()
    args = _args()
    transport_args = diagnostic._transport_args(args)
    post_flow = diagnostic._fixed_post_flow(args.batch_size, args.num_particles, args.state_dim)
    log_weights = diagnostic._fixed_log_weights(args.batch_size, args.num_particles)
    upstream = diagnostic._fixed_particle_upstream(args.batch_size, args.num_particles, args.state_dim)
    mask = diagnostic._mask_cases(args.batch_size)["mixed"]

    manual = diagnostic._manual_transport_contribution_vjp(
        post_flow=post_flow,
        normalized_log_weights=log_weights,
        mask=mask,
        args=transport_args,
        upstream_particles=upstream,
    )
    reference = diagnostic._autodiff_transport_contribution_vjp(
        post_flow=post_flow,
        normalized_log_weights=log_weights,
        mask=mask,
        args=transport_args,
        upstream_particles=upstream,
    )

    for actual, expected in zip(manual, reference[:2], strict=True):
        np.testing.assert_allclose(actual.numpy(), expected.numpy(), atol=1.0e-8, rtol=1.0e-7)
    assert all(count == 0 for count in reference[2].values())


def test_full_masked_step_adds_inactive_identity_terms() -> None:
    diagnostic._configure_float64_cpu()
    args = _args()
    transport_args = diagnostic._transport_args(args)
    post_flow = diagnostic._fixed_post_flow(args.batch_size, args.num_particles, args.state_dim)
    log_weights = diagnostic._fixed_log_weights(args.batch_size, args.num_particles)
    upstream_particles = diagnostic._fixed_particle_upstream(
        args.batch_size,
        args.num_particles,
        args.state_dim,
    )
    upstream_log_weights = diagnostic._fixed_log_weight_upstream(args.batch_size, args.num_particles)
    mask = diagnostic._mask_cases(args.batch_size)["inactive_all"]

    manual = diagnostic._manual_full_masked_step_vjp(
        post_flow=post_flow,
        normalized_log_weights=log_weights,
        mask=mask,
        args=transport_args,
        upstream_particles=upstream_particles,
        upstream_log_weights=upstream_log_weights,
    )

    np.testing.assert_allclose(manual[0].numpy(), upstream_particles.numpy(), atol=1.0e-12)
    np.testing.assert_allclose(manual[1].numpy(), upstream_log_weights.numpy(), atol=1.0e-12)
