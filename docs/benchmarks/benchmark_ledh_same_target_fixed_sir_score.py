"""Same-target fixed-SIR LEDH score adapter for Phase 4.

This module gives the amended fixed SIR row its own public score identity while
reusing the repaired no-tape total VJP implementation from the parameterized
SIR diagnostic harness.  The target is the finite-N fixed-randomness
observed-data LEDH likelihood scalar for
``zhao_cui_spatial_sir_austria_j9_T20`` with
``sir_log_scale_theta = (log_kappa_scale, log_nu_scale,
log_obs_noise_scale)``.

The older parameterized diagnostic row remains historical/diagnostic.  Calls
through this adapter must use the full manual transport derivative, not the
stopped-scale diagnostic route.
"""

from __future__ import annotations

import argparse
from typing import Any, Sequence

import tensorflow as tf

from bayesfilter.highdim.ledh_forward_contract import (
    FIXED_SIR_AUSTRIA_ROW_ID,
    MAIN_OBSERVED_DATA_ROW_SCOPE,
    make_fixed_sir_logscale_forward_contract,
    validate_ledh_forward_contract_manifest,
)
from docs.benchmarks import benchmark_p8p_parameterized_sir_gradient as p8p


FIXED_SIR_MANUAL_SCORE_ROUTE_ID = (
    "manual_total_vjp_no_autodiff_same_scalar_fixed_sir_logscale_ledh_pfpf_ot"
)
FIXED_SIR_SAME_SCALAR_ROUTE_ID = (
    "same_target_fixed_sir_logscale_ledh_pfpf_ot_streaming_manual_total"
)
PARAMETER_NAMES = p8p.PARAMETER_NAMES
MANUAL_SCORE_COMPONENT_NAMES = p8p.MANUAL_SCORE_COMPONENT_NAMES
NONCLAIMS = (
    "not N=10000 memory evidence",
    "not full leaderboard admission",
    "not exact nonlinear likelihood correctness",
    "not HMC/NUTS readiness",
    "not posterior correctness",
    "not Zhao-Cui TT/SIRT source-faithfulness",
)


def _configure_precision(args: argparse.Namespace) -> dict[str, Any]:
    return p8p._configure_precision(args)  # noqa: SLF001


def _full_leaderboard_identity(args: argparse.Namespace) -> bool:
    return bool(
        int(args.time_steps) == 20
        and int(args.num_particles) == 10000
        and tuple(int(seed) for seed in args.batch_seeds)
        == (81120, 81121, 81122, 81123, 81124)
        and args.transport_policy == "active-all"
        and int(args.sinkhorn_iterations) == 10
        and float(args.sinkhorn_epsilon) == 1.0
    )


def _fixed_sir_forward_contract(args: argparse.Namespace) -> dict[str, Any]:
    contract = make_fixed_sir_logscale_forward_contract(
        time_steps=int(args.time_steps),
        num_particles=int(args.num_particles),
        batch_seeds=[int(seed) for seed in args.batch_seeds],
        full_leaderboard_row=_full_leaderboard_identity(args),
    ).to_manifest()
    return validate_ledh_forward_contract_manifest(contract)


def _require_fixed_sir_score_args(args: argparse.Namespace) -> None:
    if args.transport_plan_mode != "streaming":
        raise ValueError("fixed-SIR admitted score requires streaming transport")
    if args.transport_ad_mode != "full":
        raise ValueError(
            "fixed-SIR admitted score requires transport_ad_mode='full'; "
            "stopped-scale/stabilized routes remain diagnostic only"
        )
    if args.transport_gradient_mode not in {
        p8p.core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE,
        p8p.core_tf.MANUAL_STREAMING_BLOCKWISE_VJP_FINITE_TRANSPORT_GRADIENT_MODE,
    }:
        raise ValueError("fixed-SIR admitted score requires a manual streaming transport VJP")
    if args.transport_policy == "no-resampling":
        raise ValueError("fixed-SIR admitted score requires active relaxed Sinkhorn transport")


def _theta_values(theta_values: Sequence[float] | None) -> list[float]:
    if theta_values is None:
        return [0.0, 0.0, 0.0]
    values = [float(value) for value in theta_values]
    if len(values) != len(PARAMETER_NAMES):
        raise ValueError("fixed-SIR theta must have three log-scale entries")
    return values


def _build_fixed_sir_tensors(
    args: argparse.Namespace,
) -> tuple[dict[str, tf.Tensor], dict[str, Any]]:
    tensors, semantics = p8p._build_base_tensors(args)  # noqa: SLF001
    semantics = dict(semantics)
    semantics.update(
        {
            "row_id": FIXED_SIR_AUSTRIA_ROW_ID,
            "row_scope": MAIN_OBSERVED_DATA_ROW_SCOPE,
            "theta_coordinate_system": "sir_log_scale_theta",
            "score_adapter": "fixed_sir_same_target_phase4",
            "diagnostic_module_reused_for_vjp": (
                "docs.benchmarks.benchmark_p8p_parameterized_sir_gradient"
            ),
        }
    )
    return tensors, semantics


def _fixed_sir_manual_score_diagnostic(
    args: argparse.Namespace,
    theta_values: Sequence[float] | None = None,
    *,
    return_score_decomposition: bool = True,
) -> dict[str, Any]:
    """Compute the fixed-SIR no-tape score for the same forward scalar."""

    _require_fixed_sir_score_args(args)
    theta = _theta_values(theta_values)
    tensors, semantics = _build_fixed_sir_tensors(args)
    result = p8p._manual_value_and_score_from_components(  # noqa: SLF001
        tensors,
        args,
        p8p._theta_components(theta),  # noqa: SLF001
        return_score_decomposition=return_score_decomposition,
    )
    contract = _fixed_sir_forward_contract(args)
    component_names = list(MANUAL_SCORE_COMPONENT_NAMES)
    diagnostic: dict[str, Any] = {
        **result,
        "row_id": FIXED_SIR_AUSTRIA_ROW_ID,
        "target_scope": MAIN_OBSERVED_DATA_ROW_SCOPE,
        "forward_contract": contract,
        "target_scalar": contract["target_scalar"],
        "target_output_tensor_field": contract["output_tensor_field"],
        "target_density_fields": contract["target_density_fields"],
        "proposal_flow_fields": contract["proposal_flow_fields"],
        "correction_formula": contract["correction_formula"],
        "sir_semantics": semantics,
        "theta_values": theta,
        "theta_coordinate_system": "sir_log_scale_theta",
        "parameter_order": list(PARAMETER_NAMES),
        "score_route": FIXED_SIR_MANUAL_SCORE_ROUTE_ID,
        "score_route_id": FIXED_SIR_SAME_SCALAR_ROUTE_ID,
        "value_score_route_status": "same_route_value_score",
        "value_score_same_transport_algorithm": True,
        "no_autodiff_score_route": True,
        "old_parameterized_route_status": "historical_diagnostic_only",
        "manual_score_component_names": component_names,
        "transport": {
            "value_core_mode": "manual_forward_replay_same_scalar",
            "transport_plan_mode": args.transport_plan_mode,
            "transport_ad_mode": args.transport_ad_mode,
            "gradient_mode": args.transport_gradient_mode,
            "row_chunk_size": int(args.row_chunk_size),
            "col_chunk_size": int(args.col_chunk_size),
            "particle_chunk_size": int(args.particle_chunk_size),
            "sinkhorn_iterations": int(args.sinkhorn_iterations),
            "sinkhorn_epsilon": float(args.sinkhorn_epsilon),
            "dense_transport_matrix_materialized": False,
        },
        "nonclaims": list(NONCLAIMS),
    }
    if return_score_decomposition:
        component_tensor = tf.convert_to_tensor(
            diagnostic["manual_score_components"],
            dtype=p8p.DTYPE,
        )
        diagnostic["manual_score_component_sum"] = tf.reduce_sum(component_tensor, axis=0)
        diagnostic["manual_score_component_reconstruction_max_abs_delta"] = tf.reduce_max(
            tf.abs(
                diagnostic["manual_score_component_sum"]
                - tf.convert_to_tensor(diagnostic["per_seed_gradient"], dtype=p8p.DTYPE)
            )
        )
    return diagnostic


def _fixed_sir_same_scalar_fd_diagnostic(
    args: argparse.Namespace,
    theta_values: Sequence[float] | None = None,
    *,
    direction: Sequence[float] = (0.2, -0.1, 0.3),
) -> dict[str, Any]:
    """Centered directional FD against the same fixed-SIR scalar."""

    _require_fixed_sir_score_args(args)
    theta = tf.constant(_theta_values(theta_values), dtype=p8p.DTYPE)
    direction_tensor = tf.constant([float(value) for value in direction], dtype=p8p.DTYPE)
    if int(direction_tensor.shape[0]) != len(PARAMETER_NAMES):
        raise ValueError("fixed-SIR FD direction must have three entries")
    step = tf.constant(float(args.fd_step), dtype=p8p.DTYPE)
    base = _fixed_sir_manual_score_diagnostic(
        args,
        theta.numpy().tolist(),
        return_score_decomposition=True,
    )
    tensors, _semantics = _build_fixed_sir_tensors(args)
    plus_theta = (theta + step * direction_tensor).numpy().tolist()
    minus_theta = (theta - step * direction_tensor).numpy().tolist()
    plus = p8p._manual_value_and_score_from_components(  # noqa: SLF001
        tensors,
        args,
        p8p._theta_components(plus_theta),  # noqa: SLF001
    )
    minus = p8p._manual_value_and_score_from_components(  # noqa: SLF001
        tensors,
        args,
        p8p._theta_components(minus_theta),  # noqa: SLF001
    )
    score_directional = tf.reduce_sum(
        tf.convert_to_tensor(base["gradient_tensor"], dtype=p8p.DTYPE)
        * direction_tensor
    )
    fd_directional = (plus["objective"] - minus["objective"]) / (2.0 * step)
    abs_error = tf.abs(score_directional - fd_directional)
    rel_error = abs_error / tf.maximum(
        tf.maximum(tf.abs(score_directional), tf.abs(fd_directional)),
        tf.constant(1.0e-12, dtype=p8p.DTYPE),
    )
    atol = tf.constant(float(getattr(args, "score_fd_atol", 1.0e-2)), dtype=p8p.DTYPE)
    rtol = tf.constant(float(getattr(args, "score_fd_rtol", 5.0e-2)), dtype=p8p.DTYPE)
    passed = bool((abs_error <= atol or rel_error <= rtol).numpy())
    return {
        "status": "pass" if passed else "fail",
        "row_id": FIXED_SIR_AUSTRIA_ROW_ID,
        "target_scope": MAIN_OBSERVED_DATA_ROW_SCOPE,
        "score_route": FIXED_SIR_MANUAL_SCORE_ROUTE_ID,
        "theta_values": [float(value) for value in theta.numpy().tolist()],
        "direction": [float(value) for value in direction_tensor.numpy().tolist()],
        "fd_step": float(step.numpy()),
        "score_directional": float(score_directional.numpy()),
        "fd_directional": float(fd_directional.numpy()),
        "abs_error": float(abs_error.numpy()),
        "rel_error": float(rel_error.numpy()),
        "atol": float(atol.numpy()),
        "rtol": float(rtol.numpy()),
        "base": base,
    }
