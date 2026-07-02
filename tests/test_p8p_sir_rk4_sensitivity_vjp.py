from __future__ import annotations

import argparse
import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np

from docs.benchmarks import diagnose_p8p_sir_rk4_sensitivity_vjp as diagnostic


def _args() -> argparse.Namespace:
    return argparse.Namespace(
        batch_size=2,
        num_particles=3,
        theta_values=[0.02, -0.01, 0.01],
        max_abs_tolerance=diagnostic.DEFAULT_MAX_ABS,
        rel_l2_tolerance=diagnostic.DEFAULT_REL_L2,
    )


def test_phase3_rk4_sensitivity_diagnostic_passes_contract() -> None:
    payload = diagnostic.run_diagnostic(_args())

    assert payload["passed"] is True
    assert payload["failure_localization"] == "pass"
    assert payload["environment"]["visible_cuda_devices"] == "-1"
    for item in payload["comparisons"]:
        assert item["passed"], item
        assert item["max_abs_residual"] <= diagnostic.DEFAULT_MAX_ABS
        assert item["relative_l2_residual"] <= diagnostic.DEFAULT_REL_L2


def test_rhs_manual_vjp_matches_autodiff_components() -> None:
    diagnostic._configure_float64_cpu()
    points = diagnostic._fixed_points(batch_size=2, num_particles=3)
    upstream = diagnostic._fixed_upstream(batch_size=2, num_particles=3)
    params = diagnostic._parameters([0.02, -0.01, 0.01])

    manual = diagnostic._manual_rhs(points, upstream, params)
    reference = diagnostic._rhs_autodiff(points, upstream, params)

    for actual, expected in zip(manual, reference, strict=True):
        np.testing.assert_allclose(actual.numpy(), expected.numpy(), atol=1.0e-8, rtol=1.0e-7)


def test_full_rk4_regional_log_chain_rule_matches_regional_autodiff() -> None:
    diagnostic._configure_float64_cpu()
    theta = [0.02, -0.01, 0.01]
    points = diagnostic._fixed_points(batch_size=2, num_particles=3)
    upstream = diagnostic._fixed_upstream(batch_size=2, num_particles=3)
    params = diagnostic._parameters(theta)
    full_substeps = int(diagnostic.p8p._SIR_RK4_SUBSTEPS)  # noqa: SLF001

    manual = diagnostic._manual_transition(
        points,
        upstream,
        params,
        substeps=full_substeps,
    )
    regional_kappa = diagnostic.p8p._regional_kappa_score_from_cotangent(
        kappa=params["kappa"],
        bar_kappa=manual[1],
    )
    regional_nu = diagnostic.p8p._regional_nu_score_from_cotangent(
        nu=params["nu"],
        bar_nu=manual[2],
    )

    kappa_reference = diagnostic._regional_log_autodiff(
        points,
        upstream,
        theta,
        parameter="kappa",
        substeps=full_substeps,
    )
    nu_reference = diagnostic._regional_log_autodiff(
        points,
        upstream,
        theta,
        parameter="nu",
        substeps=full_substeps,
    )

    np.testing.assert_allclose(regional_kappa.numpy(), kappa_reference.numpy(), atol=1.0e-8, rtol=1.0e-7)
    np.testing.assert_allclose(regional_nu.numpy(), nu_reference.numpy(), atol=1.0e-8, rtol=1.0e-7)
