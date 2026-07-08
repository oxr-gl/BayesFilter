from __future__ import annotations

import argparse
import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import tensorflow as tf

from docs.benchmarks import benchmark_p8p_parameterized_sir_gradient as p8p
from docs.benchmarks import benchmark_p8p_regional_orthogonal_gradient_decomposition as regional


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
        transport_ad_mode="stabilized",
        row_chunk_size=2,
        col_chunk_size=2,
        particle_chunk_size=2,
        dtype=dtype,
        tf32_mode="disabled" if dtype == "float64" else "enabled",
        device="/CPU:0",
        device_scope="cpu",
        cuda_visible_devices=None,
        expect_device_kind="cpu",
        seed_microbatch_size=0,
    )


def test_regional_kappa_nu_components_sum_to_scalar_manual_scores() -> None:
    args = _args()
    p8p._configure_precision(args)
    contexts, _semantics = regional.p8p_reg._build_microbatch_contexts(args)

    diagnostic = regional._manual_regional_knu_diagnostic_for_contexts(
        contexts,
        args.theta_values,
    )

    kappa_per_seed = diagnostic["regional_kappa_score_per_seed"]
    nu_per_seed = diagnostic["regional_nu_score_per_seed"]
    scalar_per_seed = diagnostic["per_seed_gradient"]
    np.testing.assert_allclose(
        tf.reduce_sum(kappa_per_seed, axis=1).numpy(),
        scalar_per_seed[:, p8p.PARAMETER_NAMES.index("log_kappa_scale")].numpy(),
        atol=1.0e-8,
        rtol=1.0e-8,
    )
    np.testing.assert_allclose(
        tf.reduce_sum(nu_per_seed, axis=1).numpy(),
        scalar_per_seed[:, p8p.PARAMETER_NAMES.index("log_nu_scale")].numpy(),
        atol=1.0e-8,
        rtol=1.0e-8,
    )


def test_regional_rho_tau_linear_mapping_reconstructs_kappa_nu() -> None:
    args = _args()
    p8p._configure_precision(args)
    contexts, _semantics = regional.p8p_reg._build_microbatch_contexts(args)
    diagnostic = regional._manual_regional_knu_diagnostic_for_contexts(
        contexts,
        args.theta_values,
    )

    kappa = diagnostic["regional_kappa_score_per_seed"]
    nu = diagnostic["regional_nu_score_per_seed"]
    sqrt2 = tf.sqrt(tf.constant(2.0, dtype=p8p.DTYPE))
    rho = (kappa - nu) / sqrt2
    tau = (kappa + nu) / sqrt2

    np.testing.assert_allclose(((rho + tau) / sqrt2).numpy(), kappa.numpy())
    np.testing.assert_allclose(((tau - rho) / sqrt2).numpy(), nu.numpy())


def test_regional_knu_value_matches_scalar_diagonal() -> None:
    args = _args()
    p8p._configure_precision(args)
    tensors, _semantics = p8p._build_base_tensors(args)
    contexts, _context_semantics = regional.p8p_reg._build_microbatch_contexts(args)
    theta = args.theta_values
    region_count = 9
    kappa = tf.fill([region_count], tf.constant(theta[0], dtype=p8p.DTYPE))
    nu = tf.fill([region_count], tf.constant(theta[1], dtype=p8p.DTYPE))

    scalar_objective, _ = p8p._objective_from_components(
        tensors,
        args,
        p8p._theta_components(theta),
    )
    regional_objective = regional._value_for_regional_knu_contexts(
        contexts,
        theta,
        kappa,
        nu,
    )

    np.testing.assert_allclose(
        regional_objective.numpy(),
        scalar_objective.numpy(),
        atol=1.0e-10,
        rtol=1.0e-10,
    )
