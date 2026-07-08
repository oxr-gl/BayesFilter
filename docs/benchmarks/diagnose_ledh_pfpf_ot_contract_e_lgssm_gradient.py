"""Phase 3 LGSSM gradient diagnostic for the Contract E reset.

This diagnostic evaluates the same transition-first LGSSM scalar used by the
Phase 2 Contract E value gate.  It compares:

* exact FP64 Kalman value/score for the LGSSM fixture;
* a reverse-mode diagnostic through the Contract E scalar, using a stopped-key
  finite dense transport VJP only.  The full likelihood score is still an outer
  TensorFlow tape diagnostic and is not material gradient evidence;
* an independent 13-point finite-difference regression on the same scalar.

The finite-difference regression is the promoted independent gradient
diagnostic.  Central differences are reported only as explanatory sanity
checks.  This script does not certify SIR/SV correctness, HMC readiness,
posterior correctness, production readiness, or broad Contract E validity.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import json
import math
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
import contract_e_reset_tf

PHASE2_SCRIPT_PATH = (
    ROOT / "docs" / "benchmarks" / "diagnose_ledh_pfpf_ot_contract_e_lgssm_value.py"
)
PHASE3_SUBPLAN = (
    "docs/plans/"
    "bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-subplan-2026-06-28.md"
)
SCHEMA_VERSION = "filter_bench.ledh_pfpf_ot_contract_e_lgssm_gradient.v1"
PARAMETER_NAMES = ("ar_coefficient", "log_transition_variance", "log_observation_variance")
FD_OFFSETS = tuple(range(-6, 7))
FD_STEPS = (5.0e-4, 1.0e-3, 1.0e-3)
MATERIAL_TINY_FD_STEPS = (1.0e-5, 1.0e-5, 1.0e-5)
MATERIAL_SCORE_ROUTE = "manual_likelihood_reverse_scan_no_autodiff"
MATERIAL_TINY_ROUTE_LABEL = "contract_e_cholesky_fixed_ridge_manual_lgssm_tiny"
MATERIAL_T10_ROUTE_LABEL = "contract_e_cholesky_fixed_ridge_manual_lgssm_t10"
MATERIAL_MINIMAL_RIDGE_TINY_ROUTE_LABEL = (
    "contract_e_cholesky_minimal_ridge_replayed_manual_lgssm_tiny"
)
MATERIAL_MINIMAL_RIDGE_T10_ROUTE_LABEL = (
    "contract_e_cholesky_minimal_ridge_replayed_manual_lgssm_t10"
)
MATERIAL_LEGACY_FIXED_RIDGE_POLICY = "legacy_fixed_ridge_lambda_0p75"
MATERIAL_MINIMAL_RIDGE_POLICY = "minimal_stabilizing_replayed_fixed_chart"
MATERIAL_FULL_BLOCKER_CODE = "PHASE3_MATERIAL_FULL_GATE_PENDING_T10_MANUAL_ROUTE_VALIDATION"


def _load_phase2_module() -> Any:
    spec = importlib.util.spec_from_file_location("contract_e_phase2_value", PHASE2_SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load Phase 2 helper from {PHASE2_SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


phase2 = _load_phase2_module()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--device-scope", choices=("cpu", "visible"), default="cpu")
    parser.add_argument("--cuda-visible-devices", default="0")
    parser.add_argument("--num-particles", type=int, default=64)
    parser.add_argument("--seed-count", type=int, default=10)
    parser.add_argument("--time-steps", type=int, default=10)
    parser.add_argument("--state-dims", type=int, nargs="+", default=[1, 2])
    parser.add_argument("--settings", type=phase2._parse_setting, nargs="+", default=[phase2._parse_setting("0.5:20")])
    parser.add_argument("--rho", type=float, default=1.0)
    parser.add_argument("--tau", type=float, default=1.0e-6)
    parser.add_argument("--spectral-floor", type=float, default=1.0e-6)
    parser.add_argument(
        "--contract-e-reset-factorization",
        choices=("eigh-support", "cholesky-ridge"),
        default="eigh-support",
    )
    parser.add_argument("--chol-ridge-rel", type=float, default=1.0e-5)
    parser.add_argument("--chol-ridge-abs", type=float, default=1.0e-8)
    parser.add_argument("--chol-ridge-escalation", type=float, default=10.0)
    parser.add_argument("--chol-ridge-max-attempts", type=int, default=1)
    parser.add_argument("--covariance-residual-limit", type=float, default=5.0e-4)
    parser.add_argument("--condition-limit", type=float, default=1.0e8)
    parser.add_argument("--tf32-mode", choices=("enabled", "disabled"), default="enabled")
    parser.add_argument("--xla", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--gate-mode", choices=("smoke", "material"), default="smoke")
    parser.add_argument(
        "--reverse-transport-gradient-route",
        choices=("manual-transport-vjp-only", "value-only-ad-probe"),
        default="manual-transport-vjp-only",
        help="value-only-ad-probe is a localization probe and is forbidden for material promotion",
    )
    parser.add_argument(
        "--reverse-contract-e-gradient-probe",
        choices=("full", "stop-affine", "stop-residual", "stop-reset", "skip-reset-computation"),
        default="full",
        help="localization probe for Contract E restoration gradients; non-full is forbidden for material promotion",
    )
    parser.add_argument(
        "--fd-steps",
        default=",".join(f"{value:g}" for value in FD_STEPS),
        help="comma-separated h0,h1,h2; defaults are frozen by the Phase 3 subplan",
    )
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", default="")
    args = parser.parse_args()
    args.fd_step_values = _parse_fd_steps(args.fd_steps, material=args.gate_mode == "material")
    material_scope = _material_scope(args)
    args.material_scope = material_scope
    args.material_ridge_policy = _material_ridge_policy(args)
    if args.num_particles <= 2:
        raise ValueError("--num-particles must exceed 2")
    if args.gate_mode != "material" and args.seed_count != 10:
        raise ValueError("Phase 3 contract freezes SEED_COUNT=10")
    if args.gate_mode != "material" and args.time_steps != 10:
        raise ValueError("Phase 3 contract freezes T=10")
    if any(dim not in (1, 2) for dim in args.state_dims):
        raise ValueError("--state-dims supports only 1 and 2")
    if args.rho <= 0.0 or args.rho > 1.0:
        raise ValueError("--rho must be in (0, 1]")
    if args.tau < 0.0:
        raise ValueError("--tau must be nonnegative")
    if args.spectral_floor <= 0.0:
        raise ValueError("--spectral-floor must be positive")
    if args.chol_ridge_rel < 0.0:
        raise ValueError("--chol-ridge-rel must be nonnegative")
    if args.chol_ridge_abs <= 0.0:
        raise ValueError("--chol-ridge-abs must be strictly positive")
    if args.chol_ridge_escalation <= 1.0:
        raise ValueError("--chol-ridge-escalation must exceed one")
    if args.chol_ridge_max_attempts <= 0:
        raise ValueError("--chol-ridge-max-attempts must be positive")
    if args.covariance_residual_limit <= 0.0:
        raise ValueError("--covariance-residual-limit must be positive")
    if args.condition_limit <= 1.0:
        raise ValueError("--condition-limit must exceed one")
    if args.gate_mode == "material":
        if material_scope == "unsupported":
            raise ValueError(
                f"{MATERIAL_FULL_BLOCKER_CODE}: material mode currently admits "
                "only the reviewed R8 tiny scope, R9 Stage A scope, or R9 Stage B scope."
            )
        if args.device_scope != "cpu":
            raise ValueError("R9 material manual route is CPU-hidden FP64 only")
        if args.contract_e_reset_factorization != "cholesky-ridge":
            raise ValueError("material manual route requires --contract-e-reset-factorization cholesky-ridge")
        if args.reverse_transport_gradient_route != "manual-transport-vjp-only":
            raise ValueError("material manual route requires manual-transport-vjp-only")
        if args.reverse_contract_e_gradient_probe != "full":
            raise ValueError("material manual route forbids gradient probes")
        if (
            args.material_ridge_policy == MATERIAL_LEGACY_FIXED_RIDGE_POLICY
            and (args.chol_ridge_rel != 0.0 or args.chol_ridge_abs != 0.75 or args.chol_ridge_max_attempts != 1)
        ):
            raise ValueError("legacy material route freezes fixed ridge lambda=0.75 via rel=0, abs=0.75")
        if (
            args.material_ridge_policy == MATERIAL_MINIMAL_RIDGE_POLICY
            and args.chol_ridge_max_attempts <= 1
        ):
            raise ValueError("minimal-ridge material route requires --chol-ridge-max-attempts > 1")
        if args.xla:
            raise ValueError("material CPU route requires --no-xla")
    return args


def _material_ridge_policy(args: argparse.Namespace) -> str:
    if args.gate_mode != "material":
        return "nonmaterial"
    if args.chol_ridge_rel == 0.0 and args.chol_ridge_abs == 0.75 and args.chol_ridge_max_attempts == 1:
        return MATERIAL_LEGACY_FIXED_RIDGE_POLICY
    return MATERIAL_MINIMAL_RIDGE_POLICY


def _is_r9_material_setting(args: argparse.Namespace) -> bool:
    return (
        len(args.settings) == 1
        and abs(float(args.settings[0]["epsilon"]) - 0.55) <= 0.0
        and int(args.settings[0]["steps"]) == 2
    )


def _is_material_tiny_scope(args: argparse.Namespace) -> bool:
    if args.gate_mode != "material":
        return False
    return (
        args.num_particles == 4
        and args.seed_count == 1
        and args.time_steps == 2
        and list(args.state_dims) == [1]
        and _is_r9_material_setting(args)
    )


def _material_scope(args: argparse.Namespace) -> str:
    if args.gate_mode != "material":
        return "nonmaterial"
    if _is_material_tiny_scope(args):
        return "tiny"
    if (
        args.num_particles == 16
        and args.seed_count == 3
        and args.time_steps == 10
        and list(args.state_dims) == [1]
        and _is_r9_material_setting(args)
    ):
        return "stage_a"
    if (
        args.num_particles == 64
        and args.seed_count == 10
        and args.time_steps == 10
        and list(args.state_dims) == [1, 2]
        and _is_r9_material_setting(args)
    ):
        return "stage_b"
    return "unsupported"


def _parse_fd_steps(text: str, *, material: bool = False) -> list[float]:
    values = [float(item.strip()) for item in str(text).split(",") if item.strip()]
    if len(values) != 3 or any((not math.isfinite(item) or item <= 0.0) for item in values):
        raise ValueError("--fd-steps must contain three positive finite values")
    frozen = list(MATERIAL_TINY_FD_STEPS if material else FD_STEPS)
    if any(abs(value - expected) > 0.0 for value, expected in zip(values, frozen, strict=True)):
        if material:
            raise ValueError("material FD steps are frozen to 1e-5,1e-5,1e-5")
        raise ValueError("Phase 3 FD steps are frozen to 5e-4,1e-3,1e-3")
    return values


def _configure_import_environment(args: argparse.Namespace) -> None:
    phase2._configure_import_environment(args)


def _configure_material_precision(harness: Any, args: argparse.Namespace) -> None:
    harness.DTYPE = harness.tf.float64
    harness.SEED_COUNT = int(args.seed_count)
    harness.THETA = harness.tf.cast(harness.THETA, harness.DTYPE)
    harness.core_ledh.DTYPE = harness.DTYPE
    harness.annealed_transport_tf.DTYPE = harness.DTYPE
    harness.tf.config.experimental.enable_tensor_float_32_execution(False)


def _stats_1d(samples: np.ndarray) -> dict[str, Any]:
    values = np.asarray(samples, dtype=np.float64)
    count = int(values.shape[0])
    mean = float(np.mean(values))
    sd = float(np.std(values, ddof=1)) if count > 1 else 0.0
    mcse = sd / math.sqrt(count) if count > 0 else float("nan")
    return {
        "mean": mean,
        "sd": sd,
        "mcse": mcse,
        "values": [float(item) for item in values.tolist()],
    }


def _stats_matrix(samples: np.ndarray) -> dict[str, Any]:
    values = np.asarray(samples, dtype=np.float64)
    count = int(values.shape[0])
    mean = np.mean(values, axis=0)
    sd = np.std(values, axis=0, ddof=1) if count > 1 else np.zeros_like(mean)
    mcse = sd / math.sqrt(count) if count > 0 else np.full_like(mean, np.nan)
    return {
        "mean": [float(item) for item in mean.tolist()],
        "sd": [float(item) for item in sd.tolist()],
        "mcse": [float(item) for item in mcse.tolist()],
        "values": [[float(x) for x in row] for row in values.tolist()],
    }


def _material_tiny_fixture(harness: Any, args: argparse.Namespace) -> dict[str, Any]:
    tf = harness.tf
    dtype = harness.DTYPE
    if args.num_particles != 4 or args.seed_count != 1 or args.time_steps != 2 or args.state_dims != [1]:
        raise ValueError("material tiny route requires D=1,T=2,N=4,seed_count=1")
    route_label = (
        MATERIAL_TINY_ROUTE_LABEL
        if args.material_ridge_policy == MATERIAL_LEGACY_FIXED_RIDGE_POLICY
        else MATERIAL_MINIMAL_RIDGE_TINY_ROUTE_LABEL
    )
    return {
        "route_label": route_label,
        "ridge_policy": args.material_ridge_policy,
        "material_scope": "tiny",
        "state_dim": 1,
        "num_particles": 4,
        "seed_count": 1,
        "time_steps": 2,
        "theta": tf.cast(harness.THETA[None, :], dtype),
        "initial_particles": tf.constant([[[-0.62], [-0.11], [0.27], [0.84]]], dtype=dtype),
        "transition_noise": tf.constant(
            [
                [
                    [[-0.35], [0.18], [0.62], [-0.21]],
                    [[0.41], [-0.47], [0.14], [0.53]],
                ]
            ],
            dtype=dtype,
        ),
        "residual_noise": tf.constant(
            [
                [
                    [[-0.28], [0.72], [0.48], [-0.18]],
                    [[0.36], [-0.58], [-0.44], [0.16]],
                ]
            ],
            dtype=dtype,
        ),
        "observations": tf.constant([[0.14], [-0.09]], dtype=dtype),
        "epsilon": tf.constant(float(args.settings[0]["epsilon"]), dtype=dtype),
        "scaling": tf.constant(harness.ANNEALED_SCALING, dtype=dtype),
        "steps": int(args.settings[0]["steps"]),
        "floor": harness.core_ledh._log_weight_floor(),
        "ridge": tf.constant([float(args.chol_ridge_abs)], dtype=dtype),
        "ridge_rel": tf.constant(float(args.chol_ridge_rel), dtype=dtype),
        "ridge_abs": tf.constant(float(args.chol_ridge_abs), dtype=dtype),
        "ridge_escalation": tf.constant(float(args.chol_ridge_escalation), dtype=dtype),
        "ridge_max_attempts": tf.constant(int(args.chol_ridge_max_attempts), dtype=tf.int32),
        "rho": tf.constant(float(args.rho), dtype=dtype),
    }


def _material_harness_fixture(harness: Any, args: argparse.Namespace, state_dim: int) -> dict[str, Any]:
    tf = harness.tf
    observations, initial_particles, transition_noise, residual_noise, theta_batch, _theta = _base_tensors(
        harness,
        state_dim,
    )
    route_label = (
        MATERIAL_T10_ROUTE_LABEL
        if args.material_ridge_policy == MATERIAL_LEGACY_FIXED_RIDGE_POLICY
        else MATERIAL_MINIMAL_RIDGE_T10_ROUTE_LABEL
    )
    return {
        "route_label": route_label,
        "ridge_policy": args.material_ridge_policy,
        "material_scope": str(args.material_scope),
        "state_dim": int(state_dim),
        "num_particles": int(args.num_particles),
        "seed_count": int(args.seed_count),
        "time_steps": int(args.time_steps),
        "theta": tf.cast(theta_batch, harness.DTYPE),
        "initial_particles": tf.cast(initial_particles, harness.DTYPE),
        "transition_noise": tf.cast(transition_noise, harness.DTYPE),
        "residual_noise": tf.cast(residual_noise, harness.DTYPE),
        "observations": tf.cast(observations, harness.DTYPE),
        "epsilon": tf.constant(float(args.settings[0]["epsilon"]), dtype=harness.DTYPE),
        "scaling": tf.constant(harness.ANNEALED_SCALING, dtype=harness.DTYPE),
        "steps": int(args.settings[0]["steps"]),
        "floor": harness.core_ledh._log_weight_floor(),
        "ridge": tf.fill([int(args.seed_count)], tf.constant(float(args.chol_ridge_abs), dtype=harness.DTYPE)),
        "ridge_rel": tf.constant(float(args.chol_ridge_rel), dtype=harness.DTYPE),
        "ridge_abs": tf.constant(float(args.chol_ridge_abs), dtype=harness.DTYPE),
        "ridge_escalation": tf.constant(float(args.chol_ridge_escalation), dtype=harness.DTYPE),
        "ridge_max_attempts": tf.constant(int(args.chol_ridge_max_attempts), dtype=tf.int32),
        "rho": tf.constant(float(args.rho), dtype=harness.DTYPE),
    }


def _material_fixture_for_state_dim(harness: Any, args: argparse.Namespace, state_dim: int) -> dict[str, Any]:
    if args.material_scope == "tiny":
        return _material_tiny_fixture(harness, args)
    return _material_harness_fixture(harness, args, state_dim)


def _material_transport_chart(harness: Any, post_flow: Any) -> dict[str, Any]:
    tf = harness.tf
    annealed = harness.annealed_transport_tf
    center = tf.reduce_mean(post_flow, axis=1, keepdims=True)
    scale = annealed._filterflow_scale(post_flow)
    scaled = (post_flow - center) / scale[:, None, None]
    return {
        "center": center,
        "scale": scale,
        "key": scaled,
        "epsilon0": annealed._filterflow_epsilon_start(scaled),
    }


def _material_transport_matrix_value(
    harness: Any,
    scaled: Any,
    key: Any,
    logw: Any,
    fixture: dict[str, Any],
    chart: dict[str, Any],
) -> Any:
    tf = harness.tf
    annealed = harness.annealed_transport_tf
    float_n = tf.cast(tf.shape(scaled)[1], harness.DTYPE)
    uniform_log_weight = -tf.math.log(float_n) * tf.ones_like(logw)
    cost = annealed._filterflow_exact_cost(scaled, key)
    alpha, beta, _a_x, _b_y = annealed._filterflow_manual_dense_finite_sinkhorn_outputs(
        logw,
        uniform_log_weight,
        cost,
        cost,
        cost,
        cost,
        epsilon=fixture["epsilon"],
        epsilon0=chart["epsilon0"],
        scaling=fixture["scaling"],
        steps=fixture["steps"],
    )
    return annealed._filterflow_exact_transport_from_potentials(
        scaled,
        alpha,
        beta,
        fixture["epsilon"],
        logw,
        float_n,
    )


def _material_select_ridge(
    harness: Any,
    reset_module: Any,
    *,
    post_flow: Any,
    weights: Any,
    matrix: Any,
    residual_noise: Any,
    fixture: dict[str, Any],
) -> dict[str, Any]:
    tf = harness.tf
    if fixture["ridge_policy"] == MATERIAL_LEGACY_FIXED_RIDGE_POLICY:
        ridge = fixture["ridge"]
        fixed = reset_module.contract_e_cholesky_ridge_reset_fixed_ridge(
            tf,
            post_flow=post_flow,
            weights=weights,
            matrix=matrix,
            residual_noise=residual_noise,
            rho=fixture["rho"],
            ridge=ridge,
            return_aux=True,
        )
        return {
            "ridge": ridge,
            "base_ridge": ridge,
            "attempts_used": tf.ones(tf.shape(ridge), dtype=tf.int32),
            "ok_per_batch": fixed["aux"]["ok_per_batch"],
            "ridge_failure": fixed["ridge_failure"],
        }
    return reset_module.contract_e_minimal_stabilizing_cholesky_ridge(
        tf,
        post_flow=post_flow,
        weights=weights,
        matrix=matrix,
        residual_noise=residual_noise,
        rho=fixture["rho"],
        ridge_rel=fixture["ridge_rel"],
        ridge_abs=fixture["ridge_abs"],
        ridge_escalation=fixture["ridge_escalation"],
        ridge_max_attempts=fixture["ridge_max_attempts"],
    )


def _material_step_ridge_selection(
    harness: Any,
    reset_module: Any,
    post_flow: Any,
    corrected_log_weights: Any,
    residual_noise: Any,
    fixture: dict[str, Any],
    chart: dict[str, Any],
) -> dict[str, Any]:
    tf = harness.tf
    core = harness.core_ledh
    weights, _increment = core._normalize_log_weights(corrected_log_weights)
    transport_logw = tf.math.log(tf.maximum(weights, fixture["floor"]))
    scaled = (post_flow - chart["center"]) / chart["scale"][:, None, None]
    matrix = _material_transport_matrix_value(
        harness,
        scaled,
        chart["key"],
        transport_logw,
        fixture,
        chart,
    )
    selection = _material_select_ridge(
        harness,
        reset_module,
        post_flow=post_flow,
        weights=weights,
        matrix=matrix,
        residual_noise=residual_noise,
        fixture=fixture,
    )
    return selection


def _material_fixed_ridge_step_forward(
    harness: Any,
    reset_module: Any,
    post_flow: Any,
    corrected_log_weights: Any,
    residual_noise: Any,
    fixture: dict[str, Any],
    chart: dict[str, Any],
) -> dict[str, Any]:
    tf = harness.tf
    core = harness.core_ledh
    if fixture["route_label"] not in (
        MATERIAL_TINY_ROUTE_LABEL,
        MATERIAL_T10_ROUTE_LABEL,
        MATERIAL_MINIMAL_RIDGE_TINY_ROUTE_LABEL,
        MATERIAL_MINIMAL_RIDGE_T10_ROUTE_LABEL,
    ):
        raise ValueError("unexpected material route label")
    if "ridge" not in chart:
        raise ValueError("material fixed-ridge step requires a replay ridge in the chart")
    weights, increment = core._normalize_log_weights(corrected_log_weights)
    transport_logw = tf.math.log(tf.maximum(weights, fixture["floor"]))
    scaled = (post_flow - chart["center"]) / chart["scale"][:, None, None]
    matrix = _material_transport_matrix_value(
        harness,
        scaled,
        chart["key"],
        transport_logw,
        fixture,
        chart,
    )
    reset = reset_module.contract_e_cholesky_ridge_reset_fixed_ridge(
        tf,
        post_flow=post_flow,
        weights=weights,
        matrix=matrix,
        residual_noise=residual_noise,
        rho=fixture["rho"],
        ridge=chart["ridge"],
    )
    return {
        "particles": reset["particles"],
        "weights": weights,
        "increment": increment,
        "transport_logw": transport_logw,
        "matrix": matrix,
        "floor_active": weights > fixture["floor"],
        "cov_residual": reset["max_covariance_relative_residual"],
        "mean_residual": reset["max_mean_linf_residual"],
        "ridge": reset["max_realized_ridge"],
        "replayed_ridge_by_batch": chart["ridge"],
        "base_ridge_by_batch": chart["base_ridge"],
        "ridge_attempts_by_batch": chart["ridge_attempts"],
        "ridge_ok_by_batch": chart["ridge_ok"],
        "ridge_attempts": reset["ridge_attempts_used"],
        "ridge_failure": reset["ridge_failure"],
    }


def _material_base_charts(
    harness: Any,
    reset_module: Any,
    values: Any,
    fixture: dict[str, Any],
) -> list[dict[str, Any]]:
    tf = harness.tf
    core = harness.core_ledh
    state_dim = int(fixture["state_dim"])
    num_particles = int(fixture["num_particles"])
    seed_count = int(fixture["seed_count"])
    time_steps = int(fixture["time_steps"])
    transition_matrix, transition_covariance, observation_covariance = harness._theta_to_lgssm(values, state_dim)
    transition_std = tf.sqrt(tf.linalg.diag_part(transition_covariance))
    h_jac = tf.tile(
        tf.eye(state_dim, dtype=harness.DTYPE)[None, None, :, :],
        [seed_count, num_particles, 1, 1],
    )
    particles = fixture["initial_particles"]
    log_weights = core.uniform_log_weights(seed_count, num_particles)
    charts = []
    for time_index in range(time_steps):
        prior_mean = tf.einsum("bnj,bdj->bnd", particles, transition_matrix)
        noise = fixture["transition_noise"][:, time_index, :, :]
        pre_flow = prior_mean + noise * transition_std[:, None, :]
        observation = fixture["observations"][time_index]
        residual = observation[None, None, :] - pre_flow
        flow, _flow_aux = core._batched_ledh_linearized_flow_with_aux_tf(
            pre_flow_particles=pre_flow,
            prior_means=prior_mean,
            observation_jacobian=h_jac,
            observation_residual=residual,
            transition_covariance=transition_covariance,
            observation_covariance=observation_covariance,
        )
        post_flow = flow.post_flow_particles
        chart = _material_transport_chart(harness, post_flow)
        transition_log_density = harness._diag_gaussian_logpdf(
            post_flow - prior_mean,
            transition_covariance,
        )
        observation_log_density = harness._diag_gaussian_logpdf(
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
        selection = _material_step_ridge_selection(
            harness,
            reset_module,
            post_flow,
            corrected,
            fixture["residual_noise"][:, time_index, :, :],
            fixture,
            chart,
        )
        chart = {
            **chart,
            "ridge": selection["ridge"],
            "base_ridge": selection["base_ridge"],
            "ridge_attempts": selection["attempts_used"],
            "ridge_ok": selection["ok_per_batch"],
            "ridge_failure": selection["ridge_failure"],
        }
        charts.append(chart)
        step = _material_fixed_ridge_step_forward(
            harness,
            reset_module,
            post_flow,
            corrected,
            fixture["residual_noise"][:, time_index, :, :],
            fixture,
            chart,
        )
        particles = step["particles"]
        log_weights = core.uniform_log_weights(seed_count, num_particles)
    return charts


def _material_forward_records(
    harness: Any,
    reset_module: Any,
    values: Any,
    fixture: dict[str, Any],
    charts: list[dict[str, Any]],
) -> dict[str, Any]:
    tf = harness.tf
    core = harness.core_ledh
    state_dim = int(fixture["state_dim"])
    num_particles = int(fixture["num_particles"])
    seed_count = int(fixture["seed_count"])
    time_steps = int(fixture["time_steps"])
    transition_matrix, transition_covariance, observation_covariance = harness._theta_to_lgssm(values, state_dim)
    transition_std = tf.sqrt(tf.linalg.diag_part(transition_covariance))
    h_jac = tf.tile(
        tf.eye(state_dim, dtype=harness.DTYPE)[None, None, :, :],
        [seed_count, num_particles, 1, 1],
    )
    particles = fixture["initial_particles"]
    log_weights = core.uniform_log_weights(seed_count, num_particles)
    log_likelihood = tf.zeros([seed_count], dtype=harness.DTYPE)
    records = []
    for time_index in range(time_steps):
        observation = fixture["observations"][time_index]
        ancestors = particles
        prior_mean = tf.einsum("bnj,bdj->bnd", ancestors, transition_matrix)
        noise = fixture["transition_noise"][:, time_index, :, :]
        pre_flow = prior_mean + noise * transition_std[:, None, :]
        residual = observation[None, None, :] - pre_flow
        flow, flow_aux = core._batched_ledh_linearized_flow_with_aux_tf(
            pre_flow_particles=pre_flow,
            prior_means=prior_mean,
            observation_jacobian=h_jac,
            observation_residual=residual,
            transition_covariance=transition_covariance,
            observation_covariance=observation_covariance,
        )
        post_flow = flow.post_flow_particles
        transition_log_density = harness._diag_gaussian_logpdf(
            post_flow - prior_mean,
            transition_covariance,
        )
        observation_log_density = harness._diag_gaussian_logpdf(
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
        step = _material_fixed_ridge_step_forward(
            harness,
            reset_module,
            post_flow,
            corrected,
            fixture["residual_noise"][:, time_index, :, :],
            fixture,
            charts[time_index],
        )
        log_likelihood = log_likelihood + step["increment"]
        records.append(
            {
                "ancestors": ancestors,
                "prior_mean": prior_mean,
                "noise": noise,
                "flow_aux": flow_aux,
                "post_flow": post_flow,
                "observation": observation,
                "corrected": corrected,
                "weights": step["weights"],
                "transport_logw": step["transport_logw"],
                "matrix": step["matrix"],
                "floor_active": step["floor_active"],
                "ridge": step["ridge"],
                "replayed_ridge_by_batch": step["replayed_ridge_by_batch"],
                "base_ridge_by_batch": step["base_ridge_by_batch"],
                "ridge_attempts_by_batch": step["ridge_attempts_by_batch"],
                "ridge_ok_by_batch": step["ridge_ok_by_batch"],
                "ridge_attempts": step["ridge_attempts"],
                "ridge_failure": step["ridge_failure"],
                "residual_noise": fixture["residual_noise"][:, time_index, :, :],
            }
        )
        particles = step["particles"]
        log_weights = core.uniform_log_weights(seed_count, num_particles)
    return {"value": log_likelihood, "records": records, "final_particles": particles}


def _material_fixed_ridge_step_vjp(
    harness: Any,
    reset_module: Any,
    record: dict[str, Any],
    fixture: dict[str, Any],
    chart: dict[str, Any],
    upstream_particles: Any,
    increment_upstream: Any,
) -> dict[str, Any]:
    tf = harness.tf
    core = harness.core_ledh
    annealed = harness.annealed_transport_tf
    reset_vjp = reset_module.contract_e_cholesky_ridge_reset_fixed_ridge_vjp(
        tf,
        post_flow=record["post_flow"],
        weights=record["weights"],
        matrix=record["matrix"],
        residual_noise=record["residual_noise"],
        rho=fixture["rho"],
        ridge=chart["ridge"],
        upstream_particles=upstream_particles,
    )
    scaled = (record["post_flow"] - chart["center"]) / chart["scale"][:, None, None]
    transport_x_bar, transport_logw_bar = (
        annealed._filterflow_manual_dense_finite_transport_matrix_vjp_stopped_scale_keys(
            scaled,
            record["transport_logw"],
            fixture["epsilon"],
            chart["epsilon0"],
            fixture["scaling"],
            reset_vjp["matrix"],
            steps=fixture["steps"],
        )
    )
    post_flow_bar = reset_vjp["post_flow"] + transport_x_bar / chart["scale"][:, None, None]
    floor_bar = tf.where(record["floor_active"], transport_logw_bar, tf.zeros_like(transport_logw_bar))
    normalized_log_bar = record["weights"] * reset_vjp["weights"] + floor_bar
    corrected_bar, _weights, _increment = core._normalize_log_weights_vjp(
        record["corrected"],
        normalized_log_bar,
        increment_upstream,
    )
    return {
        "post_flow": post_flow_bar,
        "corrected": corrected_bar,
        "residual_noise": reset_vjp["residual_noise"],
    }


def _material_manual_value_and_score(
    harness: Any,
    reset_module: Any,
    values: Any,
    fixture: dict[str, Any],
    charts: list[dict[str, Any]],
) -> dict[str, Any]:
    tf = harness.tf
    core = harness.core_ledh
    forward = _material_forward_records(harness, reset_module, values, fixture, charts)
    state_dim = int(fixture["state_dim"])
    seed_count = int(fixture["seed_count"])
    time_steps = int(fixture["time_steps"])
    transition_matrix, transition_covariance, observation_covariance = harness._theta_to_lgssm(values, state_dim)
    bar_particles = tf.zeros_like(forward["final_particles"])
    score = tf.zeros([seed_count, 3], dtype=harness.DTYPE)
    cotangent_norms = []
    for time_index in reversed(range(time_steps)):
        record = forward["records"][time_index]
        step_vjp = _material_fixed_ridge_step_vjp(
            harness,
            reset_module,
            record,
            fixture,
            charts[time_index],
            bar_particles,
            tf.ones([seed_count], dtype=harness.DTYPE),
        )
        correction_bars = core._log_weight_correction_vjp(step_vjp["corrected"])
        transition_vjp = core._transition_gaussian_log_density_vjp(
            record["post_flow"],
            record["prior_mean"],
            transition_covariance,
            correction_bars["transition_log_density"],
        )
        observation_vjp = core._observation_gaussian_log_density_vjp(
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
        flow_vjp = core._batched_ledh_linearized_flow_vjp(
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
            bar_pre_flow
            * record["noise"]
            * (0.5 * tf.sqrt(tf.linalg.diag_part(transition_covariance))[:, None, :]),
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
        cotangent_norms.append(float(tf.linalg.norm(bar_particles).numpy()))
    return {
        "value": forward["value"],
        "score": score,
        "records": forward["records"],
        "cotangent_norms_reversed": cotangent_norms,
    }


def _material_branch_record(
    harness: Any,
    reset_module: Any,
    values: Any,
    fixture: dict[str, Any],
    charts: list[dict[str, Any]],
) -> dict[str, Any]:
    forward = _material_forward_records(harness, reset_module, values, fixture, charts)
    reselected = []
    for record, chart in zip(forward["records"], charts, strict=True):
        selection = _material_step_ridge_selection(
            harness,
            reset_module,
            record["post_flow"],
            record["corrected"],
            record["residual_noise"],
            fixture,
            chart,
        )
        reselected.append(selection)
    return {
        "floor_active": [record["floor_active"].numpy().tolist() for record in forward["records"]],
        "ridge": [float(record["ridge"].numpy()) for record in forward["records"]],
        "replayed_ridge_by_batch": [
            [float(item) for item in record["replayed_ridge_by_batch"].numpy().tolist()]
            for record in forward["records"]
        ],
        "base_ridge_by_batch": [
            [float(item) for item in record["base_ridge_by_batch"].numpy().tolist()]
            for record in forward["records"]
        ],
        "reselected_ridge_by_batch": [
            [float(item) for item in selection["ridge"].numpy().tolist()]
            for selection in reselected
        ],
        "reselected_base_ridge_by_batch": [
            [float(item) for item in selection["base_ridge"].numpy().tolist()]
            for selection in reselected
        ],
        "reselected_ridge_attempts_by_batch": [
            [int(item) for item in selection["attempts_used"].numpy().tolist()]
            for selection in reselected
        ],
        "reselected_ridge_ok_by_batch": [
            [bool(item) for item in selection["ok_per_batch"].numpy().tolist()]
            for selection in reselected
        ],
        "ridge_attempts": [int(record["ridge_attempts"].numpy()) for record in forward["records"]],
        "ridge_failure": [bool(record["ridge_failure"].numpy()) for record in forward["records"]],
        "reselected_ridge_failure": [
            bool(selection["ridge_failure"].numpy())
            for selection in reselected
        ],
    }


def _material_branch_records_match(candidate: dict[str, Any], center: dict[str, Any]) -> bool:
    return (
        candidate["floor_active"] == center["floor_active"]
        and candidate["ridge_attempts"] == center["ridge_attempts"]
        and candidate["ridge_failure"] == center["ridge_failure"]
        and np.allclose(candidate["ridge"], center["ridge"])
        and candidate["reselected_ridge_attempts_by_batch"] == center["reselected_ridge_attempts_by_batch"]
        and candidate["reselected_ridge_ok_by_batch"] == center["reselected_ridge_ok_by_batch"]
        and candidate["reselected_ridge_failure"] == center["reselected_ridge_failure"]
        and np.allclose(candidate["reselected_ridge_by_batch"], center["reselected_ridge_by_batch"])
    )


def _material_fixture_gate(fixture: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    diagnostics = fixture["diagnostics"]
    same_scalar_ok = fixture["same_scalar_fd"]["status"] == "pass"
    value_mean = float(fixture["value"]["mean"])
    finite_value = math.isfinite(value_mean)
    finite_scores = _finite_list(fixture["score"]["mean"])
    no_ridge_failure = not bool(diagnostics["any_ridge_failure"])
    covariance_residual = diagnostics["max_covariance_relative_residual"]
    covariance_ok = (
        covariance_residual is not None
        and math.isfinite(float(covariance_residual))
        and float(covariance_residual) <= args.covariance_residual_limit
    )
    value_mcse = float(fixture["value"]["mcse"])
    value_delta = float(fixture["value"]["delta_to_kalman"])
    value_kalman_ok = (
        math.isfinite(value_delta)
        and (value_mcse <= 0.0 or abs(value_delta) <= 2.0 * value_mcse)
    )
    score_kalman_ok = all(
        bool(row["within_2_mcse_of_kalman"]) or float(row["mcse"]) <= 0.0
        for row in fixture["score"]["parameter_gates"]
    )
    route_ok = (
        fixture["score_route"] == MATERIAL_SCORE_ROUTE
        and bool(diagnostics["material_entrypoint_executed"])
        and not bool(diagnostics["outer_gradient_tape_used"])
    )
    base_ok = same_scalar_ok and route_ok and finite_value and finite_scores and no_ridge_failure
    stage_b_ok = base_ok and covariance_ok and value_kalman_ok and score_kalman_ok
    status = "pass" if (stage_b_ok if args.material_scope == "stage_b" else base_ok) else "fail"
    return {
        "status": status,
        "same_scalar_fd_ok": bool(same_scalar_ok),
        "route_ok": bool(route_ok),
        "finite_value_score": bool(finite_value and finite_scores),
        "no_ridge_failure": bool(no_ridge_failure),
        "covariance_restoration_ok": bool(covariance_ok),
        "value_within_2_mcse_of_kalman_if_required": bool(value_kalman_ok),
        "score_within_2_mcse_of_kalman_if_required": bool(score_kalman_ok),
    }


def _material_overall_gate(material: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    fixture_gates = [
        {
            "state_dim": int(fixture["state_dim"]),
            **_material_fixture_gate(fixture, args),
        }
        for fixture in material["fixtures"]
    ]
    status = "passed" if fixture_gates and all(item["status"] == "pass" for item in fixture_gates) else "failed"
    if args.material_scope in ("tiny", "stage_a"):
        criterion = (
            "material entrypoint executes replayed-fixed-chart no-autodiff manual route "
            "and same-scalar central FD passes for the reviewed route-scaling scope"
        )
    else:
        criterion = (
            "material entrypoint executes replayed-fixed-chart no-autodiff manual route, "
            "same-scalar central FD passes, reset residuals are bounded, and "
            "value/score means agree with exact Kalman within two MCSE where positive"
        )
    return {
        "status": status,
        "material_scope": args.material_scope,
        "fixture_gates": fixture_gates,
        "primary_criterion": criterion,
    }


def _run_material_manual_fixture(
    harness: Any,
    args: argparse.Namespace,
    state_dim: int,
) -> dict[str, Any]:
    tf = harness.tf
    fixture = _material_fixture_for_state_dim(harness, args, state_dim)
    theta = tf.cast(fixture["theta"], harness.DTYPE)
    charts = _material_base_charts(harness, contract_e_reset_tf, theta, fixture)
    manual = _material_manual_value_and_score(harness, contract_e_reset_tf, theta, fixture, charts)
    center_record = _material_branch_record(harness, contract_e_reset_tf, theta, fixture, charts)
    parameter_rows = []
    fd_pass = True
    fd_atol = 1.0e-5
    fd_rtol = 5.0e-4
    for parameter_index, step in enumerate(args.fd_step_values):
        direction = tf.eye(3, dtype=harness.DTYPE)[parameter_index][None, :]
        step_tensor = tf.constant(float(step), dtype=harness.DTYPE)
        plus_theta = theta + step_tensor * direction
        minus_theta = theta - step_tensor * direction
        plus_record = _material_branch_record(harness, contract_e_reset_tf, plus_theta, fixture, charts)
        minus_record = _material_branch_record(harness, contract_e_reset_tf, minus_theta, fixture, charts)
        branch_ok = _material_branch_records_match(plus_record, center_record) and _material_branch_records_match(
            minus_record,
            center_record,
        )
        plus = _material_forward_records(harness, contract_e_reset_tf, plus_theta, fixture, charts)["value"]
        minus = _material_forward_records(harness, contract_e_reset_tf, minus_theta, fixture, charts)["value"]
        fd = (plus - minus) / (2.0 * step_tensor)
        manual_values = manual["score"][:, parameter_index].numpy().astype(np.float64)
        fd_values = fd.numpy().astype(np.float64)
        abs_errors = np.abs(manual_values - fd_values)
        rel_errors = abs_errors / np.maximum(np.abs(fd_values), 1.0e-30)
        max_abs_error = float(np.max(abs_errors))
        max_rel_error = float(np.max(rel_errors))
        pass_item = bool(
            branch_ok
            and np.all(np.isfinite(abs_errors))
            and np.all((abs_errors <= fd_atol) | (rel_errors <= fd_rtol))
        )
        fd_pass = fd_pass and pass_item
        parameter_rows.append(
            {
                "parameter": PARAMETER_NAMES[parameter_index],
                "manual_score": [float(item) for item in manual_values.tolist()],
                "central_fd": [float(item) for item in fd_values.tolist()],
                "abs_error": max_abs_error,
                "rel_error": max_rel_error,
                "max_abs_error": max_abs_error,
                "max_rel_error": max_rel_error,
                "branch_replay_ok": bool(branch_ok),
                "pass": pass_item,
            }
        )
    values_np = manual["value"].numpy().astype(np.float64)
    scores_np = manual["score"].numpy().astype(np.float64)
    kalman_value, kalman_score = harness._kalman_value_and_score(int(fixture["state_dim"]))
    reset_cov_residuals = []
    reset_mean_residuals = []
    realized_ridges = []
    base_ridges = []
    ridge_attempts_by_batch = []
    ridge_ok_by_batch = []
    for record, chart in zip(manual["records"], charts, strict=True):
        reset = contract_e_reset_tf.contract_e_cholesky_ridge_reset_fixed_ridge(
            tf,
            post_flow=record["post_flow"],
            weights=record["weights"],
            matrix=record["matrix"],
            residual_noise=record["residual_noise"],
            rho=fixture["rho"],
            ridge=chart["ridge"],
        )
        reset_cov_residuals.append(float(reset["max_covariance_relative_residual"].numpy()))
        reset_mean_residuals.append(float(reset["max_mean_linf_residual"].numpy()))
        realized_ridges.extend(float(item) for item in chart["ridge"].numpy().tolist())
        base_ridges.extend(float(item) for item in chart["base_ridge"].numpy().tolist())
        ridge_attempts_by_batch.extend(int(item) for item in chart["ridge_attempts"].numpy().tolist())
        ridge_ok_by_batch.extend(bool(item) for item in chart["ridge_ok"].numpy().tolist())
    ridge_failures = [bool(item) for item in center_record["ridge_failure"]]
    value_stats = _stats_1d(values_np)
    score_stats = _stats_matrix(scores_np)
    kalman_value_float = float(kalman_value.numpy()[0])
    kalman_score_values = [float(item) for item in kalman_score.numpy()[0].tolist()]
    value_delta = value_stats["mean"] - kalman_value_float
    score_rows = []
    for index, parameter in enumerate(PARAMETER_NAMES):
        score_delta = score_stats["mean"][index] - kalman_score_values[index]
        score_mcse = score_stats["mcse"][index]
        score_rows.append(
            {
                "parameter": parameter,
                "mean": score_stats["mean"][index],
                "mcse": score_mcse,
                "kalman": kalman_score_values[index],
                "delta_to_kalman": score_delta,
                "within_2_mcse_of_kalman": bool(
                    math.isfinite(score_delta) and score_mcse > 0.0 and abs(score_delta) <= 2.0 * score_mcse
                ),
            }
        )
    value_within = bool(
        math.isfinite(value_delta)
        and value_stats["mcse"] > 0.0
        and abs(value_delta) <= 2.0 * value_stats["mcse"]
    )
    return {
        "state_dim": int(fixture["state_dim"]),
        "material_scope": fixture["material_scope"],
        "route_label": fixture["route_label"],
        "ridge_policy": fixture["ridge_policy"],
        "score_route": MATERIAL_SCORE_ROUTE,
        "value": {
            **value_stats,
            "kalman": kalman_value_float,
            "delta_to_kalman": value_delta,
            "within_2_mcse_of_kalman": value_within,
        },
        "score": {
            **score_stats,
            "kalman": kalman_score_values,
            "parameter_gates": score_rows,
        },
        "same_scalar_fd": {
            "status": "pass" if fd_pass else "fail",
            "step_values": [float(item) for item in args.fd_step_values],
            "rtol": fd_rtol,
            "atol": fd_atol,
            "parameters": parameter_rows,
        },
        "branch_record": center_record,
        "cotangent_norms_reversed": manual["cotangent_norms_reversed"],
        "diagnostics": {
            "material_entrypoint_executed": True,
            "outer_gradient_tape_used": False,
            "contract_e_reset_factorization": "cholesky-ridge-replayed-fixed-chart",
            "ridge_policy": fixture["ridge_policy"],
            "base_ridge_min": min(base_ridges) if base_ridges else None,
            "base_ridge_max": max(base_ridges) if base_ridges else None,
            "realized_ridge_min": min(realized_ridges) if realized_ridges else None,
            "realized_ridge_max": max(realized_ridges) if realized_ridges else None,
            "max_ridge_attempts_used": max(ridge_attempts_by_batch) if ridge_attempts_by_batch else None,
            "all_ridge_charts_ok": bool(all(ridge_ok_by_batch)) if ridge_ok_by_batch else False,
            "max_covariance_relative_residual": max(reset_cov_residuals) if reset_cov_residuals else None,
            "max_mean_linf_residual": max(reset_mean_residuals) if reset_mean_residuals else None,
            "any_ridge_failure": bool(any(ridge_failures)),
        },
    }


def _run_material_tiny_manual_route(
    harness: Any,
    args: argparse.Namespace,
) -> dict[str, Any]:
    return _run_material_manual_fixture(harness, args, 1)


def _run_material_manual_route(
    harness: Any,
    args: argparse.Namespace,
) -> dict[str, Any]:
    return {
        "fixtures": [
            _run_material_manual_fixture(harness, args, int(state_dim))
            for state_dim in args.state_dims
        ]
    }


def _linear_regression(xs: np.ndarray, ys: np.ndarray) -> dict[str, Any]:
    x = np.asarray(xs, dtype=np.float64)
    y = np.asarray(ys, dtype=np.float64)
    x_mean = float(np.mean(x))
    y_mean = float(np.mean(y))
    x_centered = x - x_mean
    y_centered = y - y_mean
    sxx = float(np.sum(x_centered * x_centered))
    if sxx <= 0.0:
        raise ValueError("regression requires nonzero x variation")
    slope = float(np.sum(x_centered * y_centered) / sxx)
    intercept = y_mean - slope * x_mean
    fitted = intercept + slope * x
    residuals = y - fitted
    sse = float(np.sum(residuals * residuals))
    sst = float(np.sum(y_centered * y_centered))
    dof = max(int(x.shape[0]) - 2, 1)
    residual_variance = sse / float(dof)
    slope_se = math.sqrt(max(residual_variance, 0.0) / sxx)
    r_squared = 1.0 - sse / max(sst, 1.0e-30)
    return {
        "slope": slope,
        "intercept": intercept,
        "slope_standard_error": slope_se,
        "residual_sse": sse,
        "r_squared": float(r_squared),
        "max_abs_residual": float(np.max(np.abs(residuals))),
    }


def _trim_high_low_objective(
    xs: np.ndarray,
    ys: np.ndarray,
    theta_rows: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, Any]]:
    order = np.argsort(ys)
    drop = {int(order[0]), int(order[-1])}
    keep = np.asarray([index not in drop for index in range(len(ys))], dtype=bool)
    return (
        xs[keep],
        ys[keep],
        theta_rows[keep],
        {
            "mode": "drop_highest_and_lowest_objective_values",
            "dropped_indices": sorted(drop),
            "dropped_x_values": [float(xs[index]) for index in sorted(drop)],
            "dropped_objective_values": [float(ys[index]) for index in sorted(drop)],
            "kept_count": int(np.sum(keep)),
        },
    )


def _make_compiled_contract_e(
    harness: Any,
    state_dim: int,
    setting: dict[str, Any],
    args: argparse.Namespace,
    batch_size: int,
) -> Any:
    tf = harness.tf
    core = harness.core_ledh
    annealed = harness.annealed_transport_tf
    dtype = harness.DTYPE
    num_particles = harness.NUM_PARTICLES
    time_steps = harness.TIME_STEPS
    rho = tf.constant(float(args.rho), dtype=dtype)
    tau = tf.constant(float(args.tau), dtype=dtype)
    spectral_floor = tf.constant(float(args.spectral_floor), dtype=dtype)
    chol_ridge_rel = tf.constant(float(args.chol_ridge_rel), dtype=dtype)
    chol_ridge_abs = tf.constant(float(args.chol_ridge_abs), dtype=dtype)
    chol_ridge_escalation = tf.constant(float(args.chol_ridge_escalation), dtype=dtype)
    chol_ridge_max_attempts = tf.constant(int(args.chol_ridge_max_attempts), dtype=tf.int32)

    def sym(matrix: Any) -> Any:
        return 0.5 * (matrix + tf.linalg.matrix_transpose(matrix))

    def small_batch_mm(left: Any, right: Any) -> Any:
        return tf.reduce_sum(left[:, :, :, None] * right[:, None, :, :], axis=2)

    def apply_batch_linear_rows(points: Any, matrix: Any) -> Any:
        return tf.reduce_sum(points[:, :, None, :] * matrix[:, None, :, :], axis=-1)

    def weighted_moments(points: Any, weights: Any) -> tuple[Any, Any]:
        mean = tf.reduce_sum(weights[:, :, None] * points, axis=1)
        centered = points - mean[:, None, :]
        covariance = tf.reduce_sum(
            weights[:, :, None, None] * centered[:, :, :, None] * centered[:, :, None, :],
            axis=1,
        )
        return mean, sym(covariance)

    def uniform_moments(points: Any) -> tuple[Any, Any]:
        count = tf.cast(tf.shape(points)[1], dtype)
        weights = tf.fill([tf.shape(points)[0], tf.shape(points)[1]], 1.0 / count)
        return weighted_moments(points, weights)

    def sqrt_psd(matrix: Any, floor: Any) -> Any:
        values, vectors = tf.linalg.eigh(sym(matrix))
        clipped = tf.maximum(values, floor)
        return small_batch_mm(
            vectors * tf.sqrt(clipped)[:, None, :],
            tf.linalg.matrix_transpose(vectors),
        )

    def pinv_sqrt_psd(matrix: Any, floor: Any) -> Any:
        values, vectors = tf.linalg.eigh(sym(matrix))
        inv = tf.where(values > floor, tf.math.rsqrt(tf.maximum(values, floor)), tf.zeros_like(values))
        return small_batch_mm(
            vectors * inv[:, None, :],
            tf.linalg.matrix_transpose(vectors),
        )

    def projector_psd(matrix: Any, floor: Any) -> tuple[Any, Any, Any]:
        values, vectors = tf.linalg.eigh(sym(matrix))
        mask = tf.cast(values > floor, dtype)
        projector = small_batch_mm(
            vectors * mask[:, None, :],
            tf.linalg.matrix_transpose(vectors),
        )
        rank = tf.reduce_sum(tf.cast(values > floor, tf.int32), axis=1)
        return projector, rank, values

    def condition_number(matrix: Any, floor: Any) -> tuple[Any, Any, Any, Any]:
        values, _vectors = tf.linalg.eigh(sym(matrix))
        retained = values > floor
        large = tf.where(retained, values, tf.fill(tf.shape(values), tf.constant(float("inf"), dtype=dtype)))
        small = tf.where(retained, values, tf.zeros_like(values))
        min_positive = tf.reduce_min(large, axis=1)
        max_positive = tf.reduce_max(small, axis=1)
        cond = max_positive / min_positive
        rank = tf.reduce_sum(tf.cast(retained, tf.int32), axis=1)
        return cond, rank, values, min_positive

    def dense_transport_matrix(post_flow: Any, normalized_log_weights: Any) -> Any:
        center = tf.stop_gradient(tf.reduce_mean(post_flow, axis=1, keepdims=True))
        scale = tf.stop_gradient(annealed._filterflow_scale(post_flow))
        scaled_x = (post_flow - center) / scale[:, None, None]
        epsilon = tf.constant(float(setting["epsilon"]), dtype=dtype)
        epsilon0 = tf.stop_gradient(annealed._filterflow_epsilon_start(scaled_x))
        if args.reverse_transport_gradient_route == "manual-transport-vjp-only":
            return annealed._filterflow_manual_dense_finite_transport_matrix_stopped_scale_keys(
                scaled_x,
                normalized_log_weights,
                epsilon,
                epsilon0,
                tf.constant(harness.ANNEALED_SCALING, dtype=dtype),
                steps=int(setting["steps"]),
            )
        return annealed._filterflow_manual_dense_finite_transport_matrix_value_stopped_scale_keys(
            scaled_x,
            normalized_log_weights,
            epsilon,
            epsilon0,
            tf.constant(harness.ANNEALED_SCALING, dtype=dtype),
            steps=int(setting["steps"]),
        )

    def matrix_residuals(matrix: Any, weights: Any) -> tuple[Any, Any]:
        float_n = tf.cast(tf.shape(matrix)[1], dtype)
        row_mass = tf.reduce_sum(matrix, axis=2)
        column_mass = tf.reduce_sum(matrix, axis=1)
        row_residual = tf.reduce_max(tf.abs(row_mass - 1.0))
        column_residual = tf.reduce_max(tf.abs(column_mass - float_n * weights))
        return row_residual, column_residual

    def contract_e_reset(
        post_flow: Any,
        weights: Any,
        matrix: Any,
        residual_noise: Any,
    ) -> tuple[Any, Any, Any, Any, Any, Any, Any, Any]:
        target_mean, target_cov = weighted_moments(post_flow, weights)
        y_plus = tf.linalg.matmul(matrix, post_flow)
        _plus_mean, plus_cov = uniform_moments(y_plus)
        gap = sym(target_cov - plus_cov)
        projector, target_rank, target_eigs = projector_psd(target_cov, spectral_floor)
        residual_cov = sym(gap + tau * projector)
        b_matrix = tf.sqrt(rho) * sqrt_psd(residual_cov, tf.constant(0.0, dtype=dtype))
        if args.reverse_contract_e_gradient_probe == "stop-residual":
            b_matrix = tf.stop_gradient(b_matrix)
        centered_noise = residual_noise - tf.reduce_mean(residual_noise, axis=1, keepdims=True)
        xi = tf.sqrt(tf.cast(num_particles, dtype) / tf.cast(num_particles - 1, dtype)) * centered_noise
        y_tilde = y_plus + apply_batch_linear_rows(xi, b_matrix)
        tilde_mean, tilde_cov = uniform_moments(y_tilde)
        target_sqrt = sqrt_psd(target_cov, tf.constant(0.0, dtype=dtype))
        tilde_pinv_sqrt = pinv_sqrt_psd(tilde_cov, spectral_floor)
        affine = small_batch_mm(target_sqrt, tilde_pinv_sqrt)
        if args.reverse_contract_e_gradient_probe == "stop-affine":
            affine = tf.stop_gradient(affine)
        y_star = target_mean[:, None, :] + apply_batch_linear_rows(
            y_tilde - tilde_mean[:, None, :],
            affine,
        )
        if args.reverse_contract_e_gradient_probe == "stop-reset":
            y_star = tf.stop_gradient(y_star)
        star_mean, star_cov = uniform_moments(y_star)
        cov_norm = tf.norm(target_cov, ord="fro", axis=[-2, -1])
        cov_residual = tf.norm(star_cov - target_cov, ord="fro", axis=[-2, -1]) / tf.maximum(
            cov_norm,
            tf.constant(1.0e-30, dtype=dtype),
        )
        mean_residual = tf.reduce_max(tf.abs(star_mean - target_mean), axis=1)
        tilde_cond, tilde_rank, _tilde_eigs, min_positive = condition_number(
            tilde_cov,
            spectral_floor,
        )
        gap_eigs, _vectors = tf.linalg.eigh(gap)
        return (
            y_star,
            tf.reduce_max(cov_residual),
            tf.reduce_max(mean_residual),
            tf.reduce_min(gap_eigs),
            tf.reduce_max(tilde_cond),
            tf.reduce_min(min_positive),
            tf.reduce_min(tf.cast(tilde_rank - target_rank, dtype)),
            tf.reduce_min(target_eigs),
        )

    def contract_e_cholesky_ridge_reset(
        post_flow: Any,
        weights: Any,
        matrix: Any,
        residual_noise: Any,
    ) -> tuple[Any, Any, Any, Any, Any, Any, Any, Any]:
        reset = contract_e_reset_tf.contract_e_cholesky_ridge_reset(
            tf,
            post_flow=post_flow,
            weights=weights,
            matrix=matrix,
            residual_noise=residual_noise,
            rho=rho,
            ridge_rel=chol_ridge_rel,
            ridge_abs=chol_ridge_abs,
            ridge_escalation=chol_ridge_escalation,
            ridge_max_attempts=chol_ridge_max_attempts,
        )
        return (
            reset["particles"],
            reset["max_covariance_relative_residual"],
            reset["max_mean_linf_residual"],
            reset["min_gap_diagnostic"],
            reset["max_condition_proxy"],
            reset["min_tilde_positive_diagnostic"],
            reset["min_rank_margin_diagnostic"],
            reset["min_target_positive_diagnostic"],
        )

    @tf.custom_gradient
    def contract_e_fixed_ridge_particles_custom_gradient(
        post_flow: Any,
        weights: Any,
        matrix: Any,
        residual_noise: Any,
        ridge: Any,
    ) -> tuple[Any, Any]:
        reset = contract_e_reset_tf.contract_e_cholesky_ridge_reset_fixed_ridge(
            tf,
            post_flow=post_flow,
            weights=weights,
            matrix=matrix,
            residual_noise=residual_noise,
            rho=rho,
            ridge=ridge,
        )

        def grad(upstream_particles: Any) -> tuple[Any, Any, Any, Any, Any]:
            vjp = contract_e_reset_tf.contract_e_cholesky_ridge_reset_fixed_ridge_vjp(
                tf,
                post_flow=post_flow,
                weights=weights,
                matrix=matrix,
                residual_noise=residual_noise,
                rho=rho,
                ridge=ridge,
                upstream_particles=upstream_particles,
            )
            return (
                vjp["post_flow"],
                vjp["weights"],
                vjp["matrix"],
                vjp["residual_noise"],
                tf.zeros_like(ridge),
            )

        return reset["particles"], grad

    @tf.function(
        input_signature=[
            tf.TensorSpec([batch_size, 3], dtype),
            tf.TensorSpec([batch_size, num_particles, state_dim], dtype),
            tf.TensorSpec([batch_size, time_steps, num_particles, state_dim], dtype),
            tf.TensorSpec([batch_size, time_steps, num_particles, state_dim], dtype),
            tf.TensorSpec([time_steps, state_dim], dtype),
        ],
        jit_compile=bool(args.xla),
        reduce_retracing=True,
    )
    def compiled(
        values: Any,
        initial_particles: Any,
        transition_noise: Any,
        residual_noise: Any,
        observations: Any,
    ) -> dict[str, Any]:
        transition_matrix, transition_covariance, observation_covariance = (
            harness._theta_to_lgssm(values, state_dim)
        )
        transition_std = tf.sqrt(tf.linalg.diag_part(transition_covariance))
        h_jac = tf.tile(
            tf.eye(state_dim, dtype=dtype)[None, None, :, :],
            [batch_size, num_particles, 1, 1],
        )
        particles = initial_particles
        log_weights = core.uniform_log_weights(batch_size, num_particles)
        increments = tf.TensorArray(
            dtype=dtype,
            size=time_steps,
            element_shape=tf.TensorShape([batch_size]),
        )
        row_residuals = tf.TensorArray(dtype=dtype, size=time_steps, element_shape=tf.TensorShape([]))
        column_residuals = tf.TensorArray(dtype=dtype, size=time_steps, element_shape=tf.TensorShape([]))
        contract_cov_residuals = tf.TensorArray(dtype=dtype, size=time_steps, element_shape=tf.TensorShape([]))
        contract_mean_residuals = tf.TensorArray(dtype=dtype, size=time_steps, element_shape=tf.TensorShape([]))
        contract_min_gap_eigs = tf.TensorArray(dtype=dtype, size=time_steps, element_shape=tf.TensorShape([]))
        contract_conditions = tf.TensorArray(dtype=dtype, size=time_steps, element_shape=tf.TensorShape([]))
        contract_min_tilde_eigs = tf.TensorArray(dtype=dtype, size=time_steps, element_shape=tf.TensorShape([]))
        contract_rank_margins = tf.TensorArray(dtype=dtype, size=time_steps, element_shape=tf.TensorShape([]))
        contract_ridges = tf.TensorArray(dtype=dtype, size=time_steps, element_shape=tf.TensorShape([]))
        contract_ridge_attempts = tf.TensorArray(
            dtype=tf.int32,
            size=time_steps,
            element_shape=tf.TensorShape([]),
        )
        contract_ridge_failures = tf.TensorArray(
            dtype=tf.bool,
            size=time_steps,
            element_shape=tf.TensorShape([]),
        )

        def cond(time_index: Any, *_loop_vars: Any) -> Any:
            return time_index < tf.constant(time_steps, dtype=tf.int32)

        def body(
            time_index: Any,
            current_particles: Any,
            current_log_weights: Any,
            increment_acc: Any,
            row_residual_acc: Any,
            column_residual_acc: Any,
            contract_cov_residual_acc: Any,
            contract_mean_residual_acc: Any,
            contract_min_gap_eig_acc: Any,
            contract_condition_acc: Any,
            contract_min_tilde_eig_acc: Any,
            contract_rank_margin_acc: Any,
            contract_ridge_acc: Any,
            contract_ridge_attempt_acc: Any,
            contract_ridge_failure_acc: Any,
        ) -> tuple[Any, ...]:
            observation = observations[time_index]
            prior_mean = tf.einsum("bnj,bdj->bnd", current_particles, transition_matrix)
            noise = transition_noise[:, time_index, :, :]
            pre_flow = prior_mean + noise * transition_std[:, None, :]
            residual = observation[None, None, :] - pre_flow
            flow, _flow_aux = core._batched_ledh_linearized_flow_with_aux_tf(
                pre_flow_particles=pre_flow,
                prior_means=prior_mean,
                observation_jacobian=h_jac,
                observation_residual=residual,
                transition_covariance=transition_covariance,
                observation_covariance=observation_covariance,
            )
            post_flow = flow.post_flow_particles
            transition_log_density = harness._diag_gaussian_logpdf(
                post_flow - prior_mean,
                transition_covariance,
            )
            observation_log_density = harness._diag_gaussian_logpdf(
                post_flow - observation[None, None, :],
                observation_covariance,
            )
            corrected_log_weights = (
                current_log_weights
                + transition_log_density
                + observation_log_density
                - flow.pre_flow_log_density
                + flow.forward_log_det
            )
            weights, increment = core._normalize_log_weights(corrected_log_weights)
            normalized_log_weights = tf.math.log(tf.maximum(weights, core._log_weight_floor()))
            matrix = dense_transport_matrix(post_flow, normalized_log_weights)
            row_residual, column_residual = matrix_residuals(matrix, weights)
            if args.reverse_contract_e_gradient_probe == "skip-reset-computation":
                next_particles = tf.stop_gradient(tf.linalg.matmul(matrix, post_flow))
                contract_cov_residual = tf.constant(float("nan"), dtype=dtype)
                contract_mean_residual = tf.constant(float("nan"), dtype=dtype)
                contract_min_gap_eig = tf.constant(float("nan"), dtype=dtype)
                contract_condition = tf.constant(float("nan"), dtype=dtype)
                contract_min_tilde_eig = tf.constant(float("nan"), dtype=dtype)
                contract_rank_margin = tf.constant(float("nan"), dtype=dtype)
                contract_ridge = tf.constant(float("nan"), dtype=dtype)
                contract_ridge_attempt = tf.constant(0, dtype=tf.int32)
                contract_ridge_failure = tf.constant(False, dtype=tf.bool)
            else:
                if args.contract_e_reset_factorization == "cholesky-ridge":
                    selection = contract_e_reset_tf.contract_e_minimal_stabilizing_cholesky_ridge(
                        tf,
                        post_flow=post_flow,
                        weights=weights,
                        matrix=matrix,
                        residual_noise=residual_noise[:, time_index, :, :],
                        rho=rho,
                        ridge_rel=chol_ridge_rel,
                        ridge_abs=chol_ridge_abs,
                        ridge_escalation=chol_ridge_escalation,
                        ridge_max_attempts=chol_ridge_max_attempts,
                    )
                    # The ridge-selection loop is a chart selector, not part of
                    # the smooth likelihood scalar. Replay the selected chart
                    # with a stopped ridge to avoid differentiating through the
                    # branchy Cholesky-stability search.
                    replay_ridge = tf.stop_gradient(selection["ridge"])
                    reset = contract_e_reset_tf.contract_e_cholesky_ridge_reset_fixed_ridge(
                        tf,
                        post_flow=post_flow,
                        weights=weights,
                        matrix=matrix,
                        residual_noise=residual_noise[:, time_index, :, :],
                        rho=rho,
                        ridge=replay_ridge,
                    )
                    next_particles = contract_e_fixed_ridge_particles_custom_gradient(
                        post_flow,
                        weights,
                        matrix,
                        residual_noise[:, time_index, :, :],
                        replay_ridge,
                    )
                    contract_cov_residual = reset["max_covariance_relative_residual"]
                    contract_mean_residual = reset["max_mean_linf_residual"]
                    contract_min_gap_eig = reset["min_gap_diagnostic"]
                    contract_condition = reset["max_condition_proxy"]
                    contract_min_tilde_eig = reset["min_tilde_positive_diagnostic"]
                    contract_rank_margin = reset["min_rank_margin_diagnostic"]
                    contract_ridge = reset["max_realized_ridge"]
                    contract_ridge_attempt = tf.reduce_max(selection["attempts_used"])
                    contract_ridge_failure = tf.logical_or(
                        reset["ridge_failure"],
                        selection["ridge_failure"],
                    )
                else:
                    (
                        next_particles,
                        contract_cov_residual,
                        contract_mean_residual,
                        contract_min_gap_eig,
                        contract_condition,
                        contract_min_tilde_eig,
                        contract_rank_margin,
                        _target_min_eig,
                    ) = contract_e_reset(
                        post_flow,
                        weights,
                        matrix,
                        residual_noise[:, time_index, :, :],
                    )
                    contract_ridge = tf.constant(float("nan"), dtype=dtype)
                    contract_ridge_attempt = tf.constant(0, dtype=tf.int32)
                    contract_ridge_failure = tf.constant(False, dtype=tf.bool)
            next_log_weights = core.uniform_log_weights(batch_size, num_particles)
            return (
                time_index + 1,
                next_particles,
                next_log_weights,
                increment_acc.write(time_index, increment),
                row_residual_acc.write(time_index, row_residual),
                column_residual_acc.write(time_index, column_residual),
                contract_cov_residual_acc.write(time_index, contract_cov_residual),
                contract_mean_residual_acc.write(time_index, contract_mean_residual),
                contract_min_gap_eig_acc.write(time_index, contract_min_gap_eig),
                contract_condition_acc.write(time_index, contract_condition),
                contract_min_tilde_eig_acc.write(time_index, contract_min_tilde_eig),
                contract_rank_margin_acc.write(time_index, contract_rank_margin),
                contract_ridge_acc.write(time_index, contract_ridge),
                contract_ridge_attempt_acc.write(time_index, contract_ridge_attempt),
                contract_ridge_failure_acc.write(time_index, contract_ridge_failure),
            )

        (
            _time_index,
            _final_particles,
            _final_log_weights,
            increments,
            row_residuals,
            column_residuals,
            contract_cov_residuals,
            contract_mean_residuals,
            contract_min_gap_eigs,
            contract_conditions,
            contract_min_tilde_eigs,
            contract_rank_margins,
            contract_ridges,
            contract_ridge_attempts,
            contract_ridge_failures,
        ) = tf.while_loop(
            cond,
            body,
            loop_vars=(
                tf.constant(0, dtype=tf.int32),
                particles,
                log_weights,
                increments,
                row_residuals,
                column_residuals,
                contract_cov_residuals,
                contract_mean_residuals,
                contract_min_gap_eigs,
                contract_conditions,
                contract_min_tilde_eigs,
                contract_rank_margins,
                contract_ridges,
                contract_ridge_attempts,
                contract_ridge_failures,
            ),
            parallel_iterations=1,
            maximum_iterations=time_steps,
        )
        increment_matrix = tf.transpose(increments.stack(), [1, 0])
        return {
            "increments": increment_matrix,
            "totals": tf.reduce_sum(increment_matrix, axis=1),
            "row_residuals": row_residuals.stack(),
            "column_residuals": column_residuals.stack(),
            "contract_cov_residuals": contract_cov_residuals.stack(),
            "contract_mean_residuals": contract_mean_residuals.stack(),
            "contract_min_gap_eigs": contract_min_gap_eigs.stack(),
            "contract_conditions": contract_conditions.stack(),
            "contract_min_tilde_eigs": contract_min_tilde_eigs.stack(),
            "contract_rank_margins": contract_rank_margins.stack(),
            "contract_ridges": contract_ridges.stack(),
            "contract_ridge_attempts": contract_ridge_attempts.stack(),
            "contract_ridge_failures": contract_ridge_failures.stack(),
        }

    return compiled


def _make_compiled_contract_e_manual_value_and_score(
    harness: Any,
    state_dim: int,
    setting: dict[str, Any],
    args: argparse.Namespace,
) -> Any:
    tf = harness.tf
    core = harness.core_ledh
    annealed = harness.annealed_transport_tf
    dtype = harness.DTYPE
    batch_size = harness.SEED_COUNT
    num_particles = harness.NUM_PARTICLES
    time_steps = harness.TIME_STEPS
    rho = tf.constant(float(args.rho), dtype=dtype)
    epsilon = tf.constant(float(setting["epsilon"]), dtype=dtype)
    scaling = tf.constant(harness.ANNEALED_SCALING, dtype=dtype)
    chol_ridge_rel = tf.constant(float(args.chol_ridge_rel), dtype=dtype)
    chol_ridge_abs = tf.constant(float(args.chol_ridge_abs), dtype=dtype)
    chol_ridge_escalation = tf.constant(float(args.chol_ridge_escalation), dtype=dtype)
    chol_ridge_max_attempts = tf.constant(int(args.chol_ridge_max_attempts), dtype=tf.int32)
    sinkhorn_steps = int(setting["steps"])

    def dense_transport_matrix_value(post_flow: Any, transport_logw: Any) -> tuple[Any, Any, Any, Any]:
        center = tf.stop_gradient(tf.reduce_mean(post_flow, axis=1, keepdims=True))
        scale = tf.stop_gradient(annealed._filterflow_scale(post_flow))
        scaled_x = (post_flow - center) / scale[:, None, None]
        epsilon0 = tf.stop_gradient(annealed._filterflow_epsilon_start(scaled_x))
        matrix = annealed._filterflow_manual_dense_finite_transport_matrix_value_stopped_scale_keys(
            scaled_x,
            transport_logw,
            epsilon,
            epsilon0,
            scaling,
            steps=sinkhorn_steps,
        )
        return matrix, center, scale, epsilon0

    def dense_transport_matrix_replay(post_flow: Any, transport_logw: Any, center: Any, scale: Any, epsilon0: Any) -> Any:
        scaled_x = (post_flow - center) / scale[:, None, None]
        return annealed._filterflow_manual_dense_finite_transport_matrix_value_stopped_scale_keys(
            scaled_x,
            transport_logw,
            epsilon,
            epsilon0,
            scaling,
            steps=sinkhorn_steps,
        )

    def dense_transport_matrix_vjp(
        post_flow: Any,
        transport_logw: Any,
        center: Any,
        scale: Any,
        epsilon0: Any,
        matrix_upstream: Any,
    ) -> tuple[Any, Any]:
        scaled_x = (post_flow - center) / scale[:, None, None]
        transport_x_bar, transport_logw_bar = (
            annealed._filterflow_manual_dense_finite_transport_matrix_vjp_stopped_scale_keys(
                scaled_x,
                transport_logw,
                epsilon,
                epsilon0,
                scaling,
                matrix_upstream,
                steps=sinkhorn_steps,
            )
        )
        return transport_x_bar / scale[:, None, None], transport_logw_bar

    def matrix_residuals(matrix: Any, weights: Any) -> tuple[Any, Any]:
        float_n = tf.cast(tf.shape(matrix)[1], dtype)
        row_mass = tf.reduce_sum(matrix, axis=2)
        column_mass = tf.reduce_sum(matrix, axis=1)
        row_residual = tf.reduce_max(tf.abs(row_mass - 1.0))
        column_residual = tf.reduce_max(tf.abs(column_mass - float_n * weights))
        return row_residual, column_residual

    @tf.function(
        input_signature=[
            tf.TensorSpec([batch_size, 3], dtype),
            tf.TensorSpec([batch_size, num_particles, state_dim], dtype),
            tf.TensorSpec([batch_size, time_steps, num_particles, state_dim], dtype),
            tf.TensorSpec([batch_size, time_steps, num_particles, state_dim], dtype),
            tf.TensorSpec([time_steps, state_dim], dtype),
        ],
        jit_compile=bool(args.xla),
        reduce_retracing=True,
    )
    def compiled(
        values: Any,
        initial_particles: Any,
        transition_noise: Any,
        residual_noise: Any,
        observations: Any,
    ) -> dict[str, Any]:
        transition_matrix, transition_covariance, observation_covariance = (
            harness._theta_to_lgssm(values, state_dim)
        )
        transition_std = tf.sqrt(tf.linalg.diag_part(transition_covariance))
        h_jac = tf.tile(
            tf.eye(state_dim, dtype=dtype)[None, None, :, :],
            [batch_size, num_particles, 1, 1],
        )
        log_weight_floor = core._log_weight_floor()

        def new_ta(element_shape: list[int]) -> Any:
            return tf.TensorArray(
                dtype=dtype,
                size=time_steps,
                element_shape=tf.TensorShape(element_shape),
                clear_after_read=False,
            )

        def new_bool_ta(element_shape: list[int]) -> Any:
            return tf.TensorArray(
                dtype=tf.bool,
                size=time_steps,
                element_shape=tf.TensorShape(element_shape),
                clear_after_read=False,
            )

        def new_int_ta(element_shape: list[int] | None = None) -> Any:
            return tf.TensorArray(
                dtype=tf.int32,
                size=time_steps,
                element_shape=tf.TensorShape([] if element_shape is None else element_shape),
                clear_after_read=False,
            )

        batch_particles_shape = [batch_size, num_particles, state_dim]
        batch_weights_shape = [batch_size, num_particles]
        batch_matrix_shape = [batch_size, state_dim, state_dim]
        batch_particle_matrix_shape = [batch_size, num_particles, state_dim, state_dim]

        ancestors_ta = new_ta(batch_particles_shape)
        noise_ta = new_ta(batch_particles_shape)
        post_flow_ta = new_ta(batch_particles_shape)
        corrected_log_weights_ta = new_ta(batch_weights_shape)
        weights_ta = new_ta(batch_weights_shape)
        transport_logw_ta = new_ta(batch_weights_shape)
        floor_active_ta = new_bool_ta(batch_weights_shape)
        residual_noise_ta = new_ta(batch_particles_shape)
        transport_center_ta = new_ta([batch_size, 1, state_dim])
        transport_scale_ta = new_ta([batch_size])
        transport_epsilon0_ta = new_ta([batch_size])
        ridge_ta = new_ta([batch_size])

        aux_x0_ta = new_ta(batch_particles_shape)
        aux_prior_means_ta = new_ta(batch_particles_shape)
        aux_observation_jacobian_ta = new_ta(batch_particle_matrix_shape)
        aux_observation_residual_ta = new_ta(batch_particles_shape)
        aux_transition_covariance_ta = new_ta(batch_matrix_shape)
        aux_observation_covariance_ta = new_ta(batch_matrix_shape)
        aux_transition_covariance_stable_ta = new_ta(batch_matrix_shape)
        aux_observation_covariance_stable_ta = new_ta(batch_matrix_shape)
        aux_prior_chol_ta = new_ta(batch_matrix_shape)
        aux_prior_precision_ta = new_ta(batch_matrix_shape)
        aux_obs_precision_ta = new_ta(batch_matrix_shape)
        aux_pseudo_observation_ta = new_ta(batch_particles_shape)
        aux_post_precision_ta = new_ta(batch_particle_matrix_shape)
        aux_post_precision_stable_ta = new_ta(batch_particle_matrix_shape)
        aux_post_covariance_unstabilized_ta = new_ta(batch_particle_matrix_shape)
        aux_post_covariance_ta = new_ta(batch_particle_matrix_shape)
        aux_post_chol_ta = new_ta(batch_particle_matrix_shape)
        aux_prior_inv_ta = new_ta(batch_matrix_shape)
        aux_affine_transform_ta = new_ta(batch_particle_matrix_shape)
        aux_delta_ta = new_ta(batch_particles_shape)
        aux_info_ta = new_ta(batch_particles_shape)

        increments_ta = new_ta([batch_size])
        row_residuals_ta = new_ta([])
        column_residuals_ta = new_ta([])
        contract_cov_residuals_ta = new_ta([])
        contract_mean_residuals_ta = new_ta([])
        contract_min_gap_eigs_ta = new_ta([])
        contract_conditions_ta = new_ta([])
        contract_min_tilde_eigs_ta = new_ta([])
        contract_rank_margins_ta = new_ta([])
        contract_ridges_ta = new_ta([])
        contract_ridge_attempts_ta = new_int_ta()
        contract_ridge_failures_ta = new_bool_ta([])

        def forward_cond(time_index: Any, *_loop_vars: Any) -> Any:
            return time_index < tf.constant(time_steps, dtype=tf.int32)

        def forward_body(
            time_index: Any,
            current_particles: Any,
            current_log_weights: Any,
            current_log_likelihood: Any,
            ancestors_acc: Any,
            noise_acc: Any,
            post_flow_acc: Any,
            corrected_log_weights_acc: Any,
            weights_acc: Any,
            transport_logw_acc: Any,
            floor_active_acc: Any,
            residual_noise_acc: Any,
            transport_center_acc: Any,
            transport_scale_acc: Any,
            transport_epsilon0_acc: Any,
            ridge_acc: Any,
            aux_x0_acc: Any,
            aux_prior_means_acc: Any,
            aux_observation_jacobian_acc: Any,
            aux_observation_residual_acc: Any,
            aux_transition_covariance_acc: Any,
            aux_observation_covariance_acc: Any,
            aux_transition_covariance_stable_acc: Any,
            aux_observation_covariance_stable_acc: Any,
            aux_prior_chol_acc: Any,
            aux_prior_precision_acc: Any,
            aux_obs_precision_acc: Any,
            aux_pseudo_observation_acc: Any,
            aux_post_precision_acc: Any,
            aux_post_precision_stable_acc: Any,
            aux_post_covariance_unstabilized_acc: Any,
            aux_post_covariance_acc: Any,
            aux_post_chol_acc: Any,
            aux_prior_inv_acc: Any,
            aux_affine_transform_acc: Any,
            aux_delta_acc: Any,
            aux_info_acc: Any,
            increments_acc: Any,
            row_residuals_acc: Any,
            column_residuals_acc: Any,
            contract_cov_residuals_acc: Any,
            contract_mean_residuals_acc: Any,
            contract_min_gap_eigs_acc: Any,
            contract_conditions_acc: Any,
            contract_min_tilde_eigs_acc: Any,
            contract_rank_margins_acc: Any,
            contract_ridges_acc: Any,
            contract_ridge_attempts_acc: Any,
            contract_ridge_failures_acc: Any,
        ) -> tuple[Any, ...]:
            observation = observations[time_index]
            ancestors = current_particles
            prior_mean = tf.einsum("bnj,bdj->bnd", ancestors, transition_matrix)
            noise = transition_noise[:, time_index, :, :]
            pre_flow = prior_mean + noise * transition_std[:, None, :]
            residual = observation[None, None, :] - pre_flow
            flow, flow_aux = core._batched_ledh_linearized_flow_with_aux_tf(
                pre_flow_particles=pre_flow,
                prior_means=prior_mean,
                observation_jacobian=h_jac,
                observation_residual=residual,
                transition_covariance=transition_covariance,
                observation_covariance=observation_covariance,
            )
            post_flow = flow.post_flow_particles
            transition_log_density = harness._diag_gaussian_logpdf(
                post_flow - prior_mean,
                transition_covariance,
            )
            observation_log_density = harness._diag_gaussian_logpdf(
                post_flow - observation[None, None, :],
                observation_covariance,
            )
            corrected_log_weights = (
                current_log_weights
                + transition_log_density
                + observation_log_density
                - flow.pre_flow_log_density
                + flow.forward_log_det
            )
            weights, increment = core._normalize_log_weights(corrected_log_weights)
            transport_logw = tf.math.log(tf.maximum(weights, log_weight_floor))
            matrix, center, scale, epsilon0 = dense_transport_matrix_value(post_flow, transport_logw)
            row_residual, column_residual = matrix_residuals(matrix, weights)
            selection = contract_e_reset_tf.contract_e_minimal_stabilizing_cholesky_ridge(
                tf,
                post_flow=post_flow,
                weights=weights,
                matrix=matrix,
                residual_noise=residual_noise[:, time_index, :, :],
                rho=rho,
                ridge_rel=chol_ridge_rel,
                ridge_abs=chol_ridge_abs,
                ridge_escalation=chol_ridge_escalation,
                ridge_max_attempts=chol_ridge_max_attempts,
            )
            replay_ridge = tf.stop_gradient(selection["ridge"])
            reset = contract_e_reset_tf.contract_e_cholesky_ridge_reset_fixed_ridge(
                tf,
                post_flow=post_flow,
                weights=weights,
                matrix=matrix,
                residual_noise=residual_noise[:, time_index, :, :],
                rho=rho,
                ridge=replay_ridge,
            )
            next_particles = reset["particles"]
            next_log_weights = core.uniform_log_weights(batch_size, num_particles)
            next_log_likelihood = current_log_likelihood + increment
            return (
                time_index + 1,
                next_particles,
                next_log_weights,
                next_log_likelihood,
                ancestors_acc.write(time_index, ancestors),
                noise_acc.write(time_index, noise),
                post_flow_acc.write(time_index, post_flow),
                corrected_log_weights_acc.write(time_index, corrected_log_weights),
                weights_acc.write(time_index, weights),
                transport_logw_acc.write(time_index, transport_logw),
                floor_active_acc.write(time_index, weights > log_weight_floor),
                residual_noise_acc.write(time_index, residual_noise[:, time_index, :, :]),
                transport_center_acc.write(time_index, center),
                transport_scale_acc.write(time_index, scale),
                transport_epsilon0_acc.write(time_index, epsilon0),
                ridge_acc.write(time_index, replay_ridge),
                aux_x0_acc.write(time_index, flow_aux.x0),
                aux_prior_means_acc.write(time_index, flow_aux.prior_means),
                aux_observation_jacobian_acc.write(time_index, flow_aux.observation_jacobian),
                aux_observation_residual_acc.write(time_index, flow_aux.observation_residual),
                aux_transition_covariance_acc.write(time_index, flow_aux.transition_covariance),
                aux_observation_covariance_acc.write(time_index, flow_aux.observation_covariance),
                aux_transition_covariance_stable_acc.write(
                    time_index,
                    flow_aux.transition_covariance_stable,
                ),
                aux_observation_covariance_stable_acc.write(
                    time_index,
                    flow_aux.observation_covariance_stable,
                ),
                aux_prior_chol_acc.write(time_index, flow_aux.prior_chol),
                aux_prior_precision_acc.write(time_index, flow_aux.prior_precision),
                aux_obs_precision_acc.write(time_index, flow_aux.obs_precision),
                aux_pseudo_observation_acc.write(time_index, flow_aux.pseudo_observation),
                aux_post_precision_acc.write(time_index, flow_aux.post_precision),
                aux_post_precision_stable_acc.write(time_index, flow_aux.post_precision_stable),
                aux_post_covariance_unstabilized_acc.write(
                    time_index,
                    flow_aux.post_covariance_unstabilized,
                ),
                aux_post_covariance_acc.write(time_index, flow_aux.post_covariance),
                aux_post_chol_acc.write(time_index, flow_aux.post_chol),
                aux_prior_inv_acc.write(time_index, flow_aux.prior_inv),
                aux_affine_transform_acc.write(time_index, flow_aux.affine_transform),
                aux_delta_acc.write(time_index, flow_aux.delta),
                aux_info_acc.write(time_index, flow_aux.info),
                increments_acc.write(time_index, increment),
                row_residuals_acc.write(time_index, row_residual),
                column_residuals_acc.write(time_index, column_residual),
                contract_cov_residuals_acc.write(time_index, reset["max_covariance_relative_residual"]),
                contract_mean_residuals_acc.write(time_index, reset["max_mean_linf_residual"]),
                contract_min_gap_eigs_acc.write(time_index, reset["min_gap_diagnostic"]),
                contract_conditions_acc.write(time_index, reset["max_condition_proxy"]),
                contract_min_tilde_eigs_acc.write(time_index, reset["min_tilde_positive_diagnostic"]),
                contract_rank_margins_acc.write(time_index, reset["min_rank_margin_diagnostic"]),
                contract_ridges_acc.write(time_index, reset["max_realized_ridge"]),
                contract_ridge_attempts_acc.write(time_index, tf.reduce_max(selection["attempts_used"])),
                contract_ridge_failures_acc.write(
                    time_index,
                    tf.logical_or(reset["ridge_failure"], selection["ridge_failure"]),
                ),
            )

        (
            _time_index,
            final_particles,
            _final_log_weights,
            log_likelihood,
            ancestors_ta,
            noise_ta,
            post_flow_ta,
            corrected_log_weights_ta,
            weights_ta,
            transport_logw_ta,
            floor_active_ta,
            residual_noise_ta,
            transport_center_ta,
            transport_scale_ta,
            transport_epsilon0_ta,
            ridge_ta,
            aux_x0_ta,
            aux_prior_means_ta,
            aux_observation_jacobian_ta,
            aux_observation_residual_ta,
            aux_transition_covariance_ta,
            aux_observation_covariance_ta,
            aux_transition_covariance_stable_ta,
            aux_observation_covariance_stable_ta,
            aux_prior_chol_ta,
            aux_prior_precision_ta,
            aux_obs_precision_ta,
            aux_pseudo_observation_ta,
            aux_post_precision_ta,
            aux_post_precision_stable_ta,
            aux_post_covariance_unstabilized_ta,
            aux_post_covariance_ta,
            aux_post_chol_ta,
            aux_prior_inv_ta,
            aux_affine_transform_ta,
            aux_delta_ta,
            aux_info_ta,
            increments_ta,
            row_residuals_ta,
            column_residuals_ta,
            contract_cov_residuals_ta,
            contract_mean_residuals_ta,
            contract_min_gap_eigs_ta,
            contract_conditions_ta,
            contract_min_tilde_eigs_ta,
            contract_rank_margins_ta,
            contract_ridges_ta,
            contract_ridge_attempts_ta,
            contract_ridge_failures_ta,
        ) = tf.while_loop(
            forward_cond,
            forward_body,
            loop_vars=(
                tf.constant(0, dtype=tf.int32),
                initial_particles,
                core.uniform_log_weights(batch_size, num_particles),
                tf.zeros([batch_size], dtype=dtype),
                ancestors_ta,
                noise_ta,
                post_flow_ta,
                corrected_log_weights_ta,
                weights_ta,
                transport_logw_ta,
                floor_active_ta,
                residual_noise_ta,
                transport_center_ta,
                transport_scale_ta,
                transport_epsilon0_ta,
                ridge_ta,
                aux_x0_ta,
                aux_prior_means_ta,
                aux_observation_jacobian_ta,
                aux_observation_residual_ta,
                aux_transition_covariance_ta,
                aux_observation_covariance_ta,
                aux_transition_covariance_stable_ta,
                aux_observation_covariance_stable_ta,
                aux_prior_chol_ta,
                aux_prior_precision_ta,
                aux_obs_precision_ta,
                aux_pseudo_observation_ta,
                aux_post_precision_ta,
                aux_post_precision_stable_ta,
                aux_post_covariance_unstabilized_ta,
                aux_post_covariance_ta,
                aux_post_chol_ta,
                aux_prior_inv_ta,
                aux_affine_transform_ta,
                aux_delta_ta,
                aux_info_ta,
                increments_ta,
                row_residuals_ta,
                column_residuals_ta,
                contract_cov_residuals_ta,
                contract_mean_residuals_ta,
                contract_min_gap_eigs_ta,
                contract_conditions_ta,
                contract_min_tilde_eigs_ta,
                contract_rank_margins_ta,
                contract_ridges_ta,
                contract_ridge_attempts_ta,
                contract_ridge_failures_ta,
            ),
            parallel_iterations=1,
            maximum_iterations=time_steps,
        )

        def reverse_cond(reverse_index: Any, _bar_particles: Any, _score: Any) -> Any:
            return reverse_index < tf.constant(time_steps, dtype=tf.int32)

        def reverse_body(reverse_index: Any, upstream_particles: Any, current_score: Any) -> tuple[Any, Any, Any]:
            time_index = tf.constant(time_steps - 1, dtype=tf.int32) - reverse_index
            post_flow = post_flow_ta.read(time_index)
            weights = weights_ta.read(time_index)
            transport_logw = transport_logw_ta.read(time_index)
            center = transport_center_ta.read(time_index)
            scale = transport_scale_ta.read(time_index)
            epsilon0 = transport_epsilon0_ta.read(time_index)
            matrix = dense_transport_matrix_replay(post_flow, transport_logw, center, scale, epsilon0)
            reset_vjp = contract_e_reset_tf.contract_e_cholesky_ridge_reset_fixed_ridge_vjp(
                tf,
                post_flow=post_flow,
                weights=weights,
                matrix=matrix,
                residual_noise=residual_noise_ta.read(time_index),
                rho=rho,
                ridge=ridge_ta.read(time_index),
                upstream_particles=upstream_particles,
            )
            transport_post_bar, transport_logw_bar = dense_transport_matrix_vjp(
                post_flow,
                transport_logw,
                center,
                scale,
                epsilon0,
                reset_vjp["matrix"],
            )
            post_flow_bar = reset_vjp["post_flow"] + transport_post_bar
            floor_bar = tf.where(
                floor_active_ta.read(time_index),
                transport_logw_bar,
                tf.zeros_like(transport_logw_bar),
            )
            normalized_weight_bar = weights * reset_vjp["weights"] + floor_bar
            corrected_bar, _weights, _increment = core._normalize_log_weights_vjp(
                corrected_log_weights_ta.read(time_index),
                normalized_weight_bar,
                tf.ones([batch_size], dtype=dtype),
            )
            correction_bars = core._log_weight_correction_vjp(corrected_bar)
            flow_aux = core._BatchedLEDHLinearizedFlowAux(
                x0=aux_x0_ta.read(time_index),
                prior_means=aux_prior_means_ta.read(time_index),
                observation_jacobian=aux_observation_jacobian_ta.read(time_index),
                observation_residual=aux_observation_residual_ta.read(time_index),
                transition_covariance=aux_transition_covariance_ta.read(time_index),
                observation_covariance=aux_observation_covariance_ta.read(time_index),
                transition_covariance_stable=aux_transition_covariance_stable_ta.read(time_index),
                observation_covariance_stable=aux_observation_covariance_stable_ta.read(time_index),
                prior_chol=aux_prior_chol_ta.read(time_index),
                prior_precision=aux_prior_precision_ta.read(time_index),
                obs_precision=aux_obs_precision_ta.read(time_index),
                pseudo_observation=aux_pseudo_observation_ta.read(time_index),
                post_precision=aux_post_precision_ta.read(time_index),
                post_precision_stable=aux_post_precision_stable_ta.read(time_index),
                post_covariance_unstabilized=aux_post_covariance_unstabilized_ta.read(time_index),
                post_covariance=aux_post_covariance_ta.read(time_index),
                post_chol=aux_post_chol_ta.read(time_index),
                prior_inv=aux_prior_inv_ta.read(time_index),
                affine_transform=aux_affine_transform_ta.read(time_index),
                delta=aux_delta_ta.read(time_index),
                info=aux_info_ta.read(time_index),
            )
            transition_vjp = core._transition_gaussian_log_density_vjp(
                post_flow,
                flow_aux.prior_means,
                transition_covariance,
                correction_bars["transition_log_density"],
            )
            observation_vjp = core._observation_gaussian_log_density_vjp(
                post_flow,
                observations[time_index],
                observation_covariance,
                correction_bars["observation_log_density"],
                residual_convention="model_minus_observation",
            )
            bar_post = (
                post_flow_bar
                + transition_vjp["x_next"]
                + observation_vjp["predicted_observation"]
            )
            flow_vjp = core._batched_ledh_linearized_flow_vjp(
                flow_aux,
                bar_post,
                correction_bars["pre_flow_log_density"],
                correction_bars["forward_log_det"],
            )
            bar_pre_flow = flow_vjp.pre_flow_particles - flow_vjp.observation_residual
            bar_prior_mean = transition_vjp["transition_mean"] + flow_vjp.prior_means + bar_pre_flow
            transition_matrix_score = tf.reduce_sum(
                bar_prior_mean * ancestors_ta.read(time_index),
                axis=[1, 2],
            )
            transition_covariance_score = tf.reduce_sum(
                (transition_vjp["transition_covariance"] + flow_vjp.transition_covariance)
                * transition_covariance,
                axis=[1, 2],
            )
            pre_flow_noise_score = tf.reduce_sum(
                bar_pre_flow * noise_ta.read(time_index) * (0.5 * transition_std[:, None, :]),
                axis=[1, 2],
            )
            observation_covariance_score = tf.reduce_sum(
                (observation_vjp["observation_covariance"] + flow_vjp.observation_covariance)
                * observation_covariance,
                axis=[1, 2],
            )
            next_score = current_score + tf.stack(
                [
                    transition_matrix_score,
                    transition_covariance_score + pre_flow_noise_score,
                    observation_covariance_score,
                ],
                axis=1,
            )
            next_bar_particles = tf.einsum("bnd,bdj->bnj", bar_prior_mean, transition_matrix)
            return reverse_index + 1, next_bar_particles, next_score

        _reverse_index, _bar_particles, score = tf.while_loop(
            reverse_cond,
            reverse_body,
            loop_vars=(
                tf.constant(0, dtype=tf.int32),
                tf.zeros_like(final_particles),
                tf.zeros([batch_size, 3], dtype=dtype),
            ),
            parallel_iterations=1,
            maximum_iterations=time_steps,
        )

        return {
            "increments": increments_ta.stack(),
            "totals": log_likelihood,
            "per_seed_gradient": score,
            "row_residuals": row_residuals_ta.stack(),
            "column_residuals": column_residuals_ta.stack(),
            "contract_cov_residuals": contract_cov_residuals_ta.stack(),
            "contract_mean_residuals": contract_mean_residuals_ta.stack(),
            "contract_min_gap_eigs": contract_min_gap_eigs_ta.stack(),
            "contract_conditions": contract_conditions_ta.stack(),
            "contract_min_tilde_eigs": contract_min_tilde_eigs_ta.stack(),
            "contract_rank_margins": contract_rank_margins_ta.stack(),
            "contract_ridges": contract_ridges_ta.stack(),
            "contract_ridge_attempts": contract_ridge_attempts_ta.stack(),
            "contract_ridge_failures": contract_ridge_failures_ta.stack(),
        }

    return compiled


def _make_compiled_value_and_gradient(
    harness: Any,
    state_dim: int,
    setting: dict[str, Any],
    args: argparse.Namespace,
) -> Any:
    tf = harness.tf
    dtype = harness.DTYPE
    base_compiled = _make_compiled_contract_e(harness, state_dim, setting, args, harness.SEED_COUNT)

    @tf.function(
        input_signature=[
            tf.TensorSpec([harness.SEED_COUNT, 3], dtype),
            tf.TensorSpec([harness.SEED_COUNT, harness.NUM_PARTICLES, state_dim], dtype),
            tf.TensorSpec([harness.SEED_COUNT, harness.TIME_STEPS, harness.NUM_PARTICLES, state_dim], dtype),
            tf.TensorSpec([harness.SEED_COUNT, harness.TIME_STEPS, harness.NUM_PARTICLES, state_dim], dtype),
            tf.TensorSpec([harness.TIME_STEPS, state_dim], dtype),
        ],
        jit_compile=bool(args.xla),
        reduce_retracing=True,
    )
    def compiled(
        values: Any,
        initial_particles: Any,
        transition_noise: Any,
        residual_noise: Any,
        observations: Any,
    ) -> dict[str, Any]:
        with tf.GradientTape() as tape:
            tape.watch(values)
            raw = base_compiled(
                values,
                initial_particles,
                transition_noise,
                residual_noise,
                observations,
            )
            totals = raw["totals"]
        gradient = tape.gradient(tf.reduce_sum(totals), values)
        if gradient is None:
            gradient = tf.fill(tf.shape(values), tf.constant(float("nan"), dtype=dtype))
        result = dict(raw)
        result["per_seed_gradient"] = gradient
        return result

    return compiled


def _base_tensors(harness: Any, state_dim: int) -> tuple[Any, Any, Any, Any, Any, Any]:
    tf = harness.tf
    observations = harness._observations(state_dim)
    initial_noise, transition_noise = harness._stateless_seeded_normals_batch(state_dim)
    residual_noise = phase2._stateless_residual_normals_batch(harness, state_dim)
    initial_particles = tf.sqrt(tf.constant(0.7, harness.DTYPE)) * initial_noise
    theta_batch = tf.tile(harness.THETA[None, :], [harness.SEED_COUNT, 1])
    return observations, initial_particles, transition_noise, residual_noise, theta_batch, harness.THETA


def _tile_for_theta_rows(
    harness: Any,
    theta_rows: Any,
    initial_particles: Any,
    transition_noise: Any,
    residual_noise: Any,
) -> tuple[Any, Any, Any, Any]:
    tf = harness.tf
    num_offsets = int(theta_rows.shape[0])
    if num_offsets <= 0:
        raise ValueError("theta_rows must be statically nonempty")
    batch_values = tf.reshape(
        tf.tile(theta_rows[:, None, :], [1, harness.SEED_COUNT, 1]),
        [num_offsets * harness.SEED_COUNT, 3],
    )
    batch_initial = tf.reshape(
        tf.tile(initial_particles[None, :, :, :], [num_offsets, 1, 1, 1]),
        [num_offsets * harness.SEED_COUNT, harness.NUM_PARTICLES, initial_particles.shape[-1]],
    )
    batch_transition = tf.reshape(
        tf.tile(transition_noise[None, :, :, :, :], [num_offsets, 1, 1, 1, 1]),
        [
            num_offsets * harness.SEED_COUNT,
            harness.TIME_STEPS,
            harness.NUM_PARTICLES,
            transition_noise.shape[-1],
        ],
    )
    batch_residual = tf.reshape(
        tf.tile(residual_noise[None, :, :, :, :], [num_offsets, 1, 1, 1, 1]),
        [
            num_offsets * harness.SEED_COUNT,
            harness.TIME_STEPS,
            harness.NUM_PARTICLES,
            residual_noise.shape[-1],
        ],
    )
    return batch_values, batch_initial, batch_transition, batch_residual


def _run_base_gradient(
    harness: Any,
    state_dim: int,
    setting: dict[str, Any],
    args: argparse.Namespace,
) -> dict[str, Any]:
    np_module = harness.np
    observations, initial_particles, transition_noise, residual_noise, theta_batch, _theta = (
        _base_tensors(harness, state_dim)
    )
    if getattr(args, "score_route", "") == "manual-reverse-scan":
        compiled = _make_compiled_contract_e_manual_value_and_score(harness, state_dim, setting, args)
    else:
        compiled = _make_compiled_value_and_gradient(harness, state_dim, setting, args)
    raw = compiled(theta_batch, initial_particles, transition_noise, residual_noise, observations)
    totals = raw["totals"].numpy().astype(np.float64)
    gradients = raw["per_seed_gradient"].numpy().astype(np.float64)
    kalman_value, kalman_score = harness._kalman_value_and_score(state_dim)
    return {
        "state_dim": int(state_dim),
        "setting": dict(setting),
        "value": {
            **_stats_1d(totals),
            "kalman": float(kalman_value.numpy()[0]),
            "delta_to_kalman": float(np.mean(totals) - float(kalman_value.numpy()[0])),
        },
        "gradient": {
            **_stats_matrix(gradients),
            "kalman": [float(item) for item in kalman_score.numpy()[0].tolist()],
        },
        "diagnostics": {
            "max_row_residual": phase2._nan_reduce_or_none(
                np_module,
                raw["row_residuals"].numpy(),
                reduction="max",
            ),
            "max_column_residual": phase2._nan_reduce_or_none(
                np_module,
                raw["column_residuals"].numpy(),
                reduction="max",
            ),
            "max_covariance_relative_residual": phase2._nan_reduce_or_none(
                np_module,
                raw["contract_cov_residuals"].numpy(),
                reduction="max",
            ),
            "max_mean_linf_residual": phase2._nan_reduce_or_none(
                np_module,
                raw["contract_mean_residuals"].numpy(),
                reduction="max",
            ),
            "min_gap_eig": phase2._nan_reduce_or_none(
                np_module,
                raw["contract_min_gap_eigs"].numpy(),
                reduction="min",
            ),
            "max_tilde_condition": phase2._nan_reduce_or_none(
                np_module,
                raw["contract_conditions"].numpy(),
                reduction="max",
            ),
            "min_tilde_positive_eig": phase2._nan_reduce_or_none(
                np_module,
                raw["contract_min_tilde_eigs"].numpy(),
                reduction="min",
            ),
            "min_rank_margin": phase2._nan_reduce_or_none(
                np_module,
                raw["contract_rank_margins"].numpy(),
                reduction="min",
            ),
            "max_realized_ridge": phase2._nan_reduce_or_none(
                np_module,
                raw["contract_ridges"].numpy(),
                reduction="max",
            ),
            "max_ridge_attempts_used": int(np_module.max(raw["contract_ridge_attempts"].numpy())),
            "any_ridge_failure": bool(np_module.any(raw["contract_ridge_failures"].numpy())),
            "gap_diagnostic_label": (
                "min residual Cholesky diagonal of sym(target_cov - plus_cov)+lambda I"
                if args.contract_e_reset_factorization == "cholesky-ridge"
                else "minimum eigenvalue of sym(target_cov - plus_cov)"
            ),
            "tilde_positive_diagnostic_label": (
                "min Cholesky diagonal of tilde_cov+lambda I"
                if args.contract_e_reset_factorization == "cholesky-ridge"
                else "minimum retained positive eigenvalue of tilde_cov"
            ),
            "rank_margin_diagnostic_label": (
                "legacy field: repeats min residual Cholesky diagonal under cholesky-ridge"
                if args.contract_e_reset_factorization == "cholesky-ridge"
                else "tilde rank minus target rank on the retained eigensupport"
            ),
        },
    }


def _run_fd_for_parameter(
    harness: Any,
    state_dim: int,
    setting: dict[str, Any],
    args: argparse.Namespace,
    parameter_index: int,
) -> dict[str, Any]:
    tf = harness.tf
    observations, initial_particles, transition_noise, residual_noise, _theta_batch, theta = (
        _base_tensors(harness, state_dim)
    )
    offsets = np.asarray(FD_OFFSETS, dtype=np.float64)
    step = float(args.fd_step_values[parameter_index])
    xs = offsets * step
    theta_rows_np = np.tile(theta.numpy()[None, :].astype(np.float64), [len(offsets), 1])
    theta_rows_np[:, parameter_index] += xs
    theta_rows = tf.constant(theta_rows_np, dtype=harness.DTYPE)
    values, initial_batch, transition_batch, residual_batch = _tile_for_theta_rows(
        harness,
        theta_rows,
        initial_particles,
        transition_noise,
        residual_noise,
    )
    batch_size = len(offsets) * harness.SEED_COUNT
    compiled = _make_compiled_contract_e(harness, state_dim, setting, args, batch_size)
    raw = compiled(values, initial_batch, transition_batch, residual_batch, observations)
    totals = raw["totals"].numpy().astype(np.float64).reshape([len(offsets), harness.SEED_COUNT])
    objective_values = np.mean(totals, axis=1)
    fit_xs, fit_y, fit_theta_rows, trim_record = _trim_high_low_objective(
        xs,
        objective_values,
        theta_rows_np,
    )
    fit = _linear_regression(fit_xs, fit_y)
    offset_to_index = {int(offset): index for index, offset in enumerate(FD_OFFSETS)}
    central = (
        objective_values[offset_to_index[1]] - objective_values[offset_to_index[-1]]
    ) / (2.0 * step)
    return {
        "parameter": PARAMETER_NAMES[parameter_index],
        "parameter_index": int(parameter_index),
        "step": step,
        "offsets": [int(item) for item in FD_OFFSETS],
        "x_values": [float(item) for item in xs.tolist()],
        "theta_values": [[float(x) for x in row] for row in theta_rows_np.tolist()],
        "per_seed_values": [[float(x) for x in row] for row in totals.tolist()],
        "objective_values": [float(item) for item in objective_values.tolist()],
        "central_fd_sanity": float(central),
        "fit_x_values": [float(item) for item in fit_xs.tolist()],
        "fit_theta_values": [[float(x) for x in row] for row in fit_theta_rows.tolist()],
        "fit_objective_values": [float(item) for item in fit_y.tolist()],
        "trim_extreme_points": trim_record,
        "regression": fit,
    }


def _run_fixture(
    harness: Any,
    state_dim: int,
    setting: dict[str, Any],
    args: argparse.Namespace,
) -> dict[str, Any]:
    base = _run_base_gradient(harness, state_dim, setting, args)
    fd_records = [
        _run_fd_for_parameter(harness, state_dim, setting, args, parameter_index)
        for parameter_index in range(len(PARAMETER_NAMES))
    ]
    return {
        "state_dim": int(state_dim),
        "setting": dict(setting),
        "base": base,
        "finite_difference": fd_records,
        "gate": _gate_fixture(base, fd_records, args),
    }


def _finite_list(values: list[float]) -> bool:
    return all(math.isfinite(float(item)) for item in values)


def _gate_fixture(
    base: dict[str, Any],
    fd_records: list[dict[str, Any]],
    args: argparse.Namespace,
) -> dict[str, Any]:
    value = base["value"]
    gradient = base["gradient"]
    diagnostics = base["diagnostics"]
    value_mcse = float(value["mcse"])
    value_delta = float(value["delta_to_kalman"])
    value_within = math.isfinite(value_delta) and value_mcse > 0.0 and abs(value_delta) <= 2.0 * value_mcse
    cov_residual = diagnostics["max_covariance_relative_residual"]
    condition = diagnostics["max_tilde_condition"]
    covariance_ok = cov_residual is not None and cov_residual <= args.covariance_residual_limit
    condition_ok = condition is not None and condition <= args.condition_limit
    finite_base = (
        math.isfinite(float(value["mean"]))
        and _finite_list(gradient["mean"])
        and _finite_list(gradient["mcse"])
        and _finite_list(gradient["kalman"])
    )
    parameter_gates = []
    for index, fd in enumerate(fd_records):
        grad_mean = float(gradient["mean"][index])
        grad_mcse = float(gradient["mcse"][index])
        kalman = float(gradient["kalman"][index])
        slope = float(fd["regression"]["slope"])
        slope_se = float(fd["regression"]["slope_standard_error"])
        exact_delta = grad_mean - kalman
        reverse_fd_delta = grad_mean - slope
        exact_se = grad_mcse
        combined_se = math.sqrt(max(grad_mcse, 0.0) ** 2 + max(slope_se, 0.0) ** 2)
        exact_z = None if exact_se <= 0.0 else exact_delta / exact_se
        reverse_fd_z = None if combined_se <= 0.0 else reverse_fd_delta / combined_se
        fd_protocol_ok = (
            len(fd["offsets"]) == 13
            and fd["trim_extreme_points"]["kept_count"] == 11
            and math.isfinite(slope)
            and math.isfinite(slope_se)
            and slope_se >= 0.0
        )
        parameter_gates.append(
            {
                "parameter": PARAMETER_NAMES[index],
                "gradient_mean": grad_mean,
                "gradient_mcse": grad_mcse,
                "kalman_gradient": kalman,
                "exact_delta": exact_delta,
                "exact_z_over_gradient_mcse": exact_z,
                "within_2_gradient_mcse_of_kalman": (
                    False if exact_z is None else abs(exact_z) <= 2.0
                ),
                "fd_regression_slope": slope,
                "fd_regression_slope_se": slope_se,
                "reverse_minus_fd": reverse_fd_delta,
                "reverse_fd_combined_se": combined_se,
                "reverse_minus_fd_z": reverse_fd_z,
                "within_2_combined_se_of_fd": (
                    False if reverse_fd_z is None else abs(reverse_fd_z) <= 2.0
                ),
                "fd_protocol_ok": fd_protocol_ok,
            }
        )
    parameter_status = all(
        item["within_2_gradient_mcse_of_kalman"]
        and item["within_2_combined_se_of_fd"]
        and item["fd_protocol_ok"]
        for item in parameter_gates
    )
    status = (
        "pass"
        if (
            value_within
            and finite_base
            and covariance_ok
            and condition_ok
            and parameter_status
        )
        else "fail"
    )
    if args.gate_mode == "smoke":
        status = "smoke_pass" if finite_base and all(item["fd_protocol_ok"] for item in parameter_gates) else "smoke_fail"
    return {
        "status": status,
        "value_within_2_mcse_of_kalman": value_within,
        "finite_base": finite_base,
        "covariance_restoration_ok": covariance_ok,
        "conditioning_ok": condition_ok,
        "parameter_gates": parameter_gates,
    }


def _overall_gate(records: list[dict[str, Any]], args: argparse.Namespace, device: dict[str, Any]) -> dict[str, Any]:
    if args.gate_mode == "smoke":
        status = "smoke_passed" if records and all(item["gate"]["status"] == "smoke_pass" for item in records) else "smoke_failed"
    else:
        gpu_claim_ok = bool(device["logical_gpus"]) if args.device_scope == "visible" else True
        status = "passed" if records and gpu_claim_ok and all(item["gate"]["status"] == "pass" for item in records) else "failed"
    return {
        "status": status,
        "fixture_gates": [
            {
                "state_dim": item["state_dim"],
                "setting": item["setting"]["label"],
                **item["gate"],
            }
            for item in records
        ],
        "primary_criterion": (
            "Contract E value/gradient means within two uncertainty units of exact Kalman "
            "and reverse diagnostic within two combined SE of 13-point FD regression"
        ),
    }


def _render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Contract E LGSSM Gradient Diagnostic",
        "",
        f"Date: {payload['timestamp_utc']}",
        "",
        f"Status: `{payload['gate']['status']}`",
        "",
        "## Manifest",
        "",
        f"- gate_mode: `{payload['manifest']['gate_mode']}`",
        f"- num_particles: `{payload['manifest']['num_particles']}`",
        f"- seed_count: `{payload['manifest']['seed_count']}`",
        f"- time_steps: `{payload['manifest']['time_steps']}`",
        f"- state_dims: `{payload['manifest']['state_dims']}`",
        f"- settings: `{payload['manifest']['settings']}`",
        f"- fd_steps: `{payload['manifest']['fd_steps']}`",
        f"- device_scope: `{payload['device']['device_scope']}`",
        f"- logical_gpus: `{payload['device']['logical_gpus']}`",
        f"- xla: `{payload['device']['xla']}`",
        f"- tf32_execution_enabled: `{payload['device']['tf32_execution_enabled']}`",
        "",
        "## Gradient Gate Table",
        "",
        "| dim | parameter | grad mean | Kalman | grad MCSE | exact z | FD slope | FD SE | reverse-FD z | status |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for record in payload["records"]:
        for gate in record["gate"]["parameter_gates"]:
            exact_z = gate["exact_z_over_gradient_mcse"]
            fd_z = gate["reverse_minus_fd_z"]
            status = (
                gate["within_2_gradient_mcse_of_kalman"]
                and gate["within_2_combined_se_of_fd"]
                and gate["fd_protocol_ok"]
            )
            lines.append(
                "| "
                f"{record['state_dim']} | "
                f"`{gate['parameter']}` | "
                f"{gate['gradient_mean']:.6f} | "
                f"{gate['kalman_gradient']:.6f} | "
                f"{gate['gradient_mcse']:.6f} | "
                f"{'NA' if exact_z is None else f'{exact_z:.3f}'} | "
                f"{gate['fd_regression_slope']:.6f} | "
                f"{gate['fd_regression_slope_se']:.6f} | "
                f"{'NA' if fd_z is None else f'{fd_z:.3f}'} | "
                f"`{status}` |"
            )
    lines.extend(
        [
            "",
            "## Gate",
            "",
            "```json",
            json.dumps(payload["gate"], indent=2, sort_keys=True),
            "```",
            "",
            "## Nonclaims",
            "",
            "- This diagnostic does not certify SIR/SV/nonlinear correctness.",
            "- This diagnostic does not certify production readiness, HMC readiness, or posterior correctness.",
            "- Reverse-mode gradients are diagnostics, not an oracle.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    args = _parse_args()
    _configure_import_environment(args)
    start = time.perf_counter()
    harness = phase2._load_harness(args)
    if args.gate_mode == "material":
        _configure_material_precision(harness, args)
    device = phase2._device_manifest(harness, args)
    if args.gate_mode == "material":
        material = _run_material_manual_route(harness, args)
        gate = _material_overall_gate(material, args)
        gate_status = gate["status"]
        primary_fixture = material["fixtures"][0]
        payload = {
            "schema_version": SCHEMA_VERSION,
            "timestamp_utc": _dt.datetime.now(tz=_dt.timezone.utc).isoformat(),
            "host": platform.node(),
            "python_version": platform.python_version(),
            "tensorflow_version": harness.tf.__version__,
            "phase3_subplan": PHASE3_SUBPLAN,
            "manifest": {
                "gate_mode": args.gate_mode,
                "num_particles": int(args.num_particles),
                "seed_count": int(args.seed_count),
                "time_steps": int(args.time_steps),
                "state_dims": [int(x) for x in args.state_dims],
                "settings": args.settings,
                "theta": [float(x) for x in harness.THETA.numpy().tolist()],
                "fd_steps": [float(x) for x in args.fd_step_values],
                "score_route": MATERIAL_SCORE_ROUTE,
                "route_label": primary_fixture["route_label"],
                "ridge_policy": args.material_ridge_policy,
                "material_scope": args.material_scope,
                "contract_e_reset_factorization": "cholesky-ridge-replayed-fixed-chart",
                "full_phase3_material_status": MATERIAL_FULL_BLOCKER_CODE,
                "initial_transition_seed_schedule": (
                    f"seed indices 9100..{9100 + int(args.seed_count) - 1}; "
                    "initial seeds [seed,17]; transition seeds [seed,29]"
                ),
                "contract_e_residual_seed_schedule": (
                    f"seed indices 9100..{9100 + int(args.seed_count) - 1}; "
                    f"residual seeds [seed,43+t] for t=0..{int(args.time_steps) - 1}"
                ),
                "rho": float(args.rho),
                "chol_ridge_rel": float(args.chol_ridge_rel),
                "chol_ridge_abs": float(args.chol_ridge_abs),
                "chol_ridge_escalation": float(args.chol_ridge_escalation),
                "chol_ridge_max_attempts": int(args.chol_ridge_max_attempts),
                "covariance_residual_limit": float(args.covariance_residual_limit),
                "nonclaims": [
                    (
                        "tiny material route gate only"
                        if args.material_scope == "tiny"
                        else "R9 Stage A route-scaling gate only"
                        if args.material_scope == "stage_a"
                        else "R9 Stage B CPU FP64 material statistical gate"
                    ),
                    "not SIR/SV correctness",
                    "not GPU/XLA/TF32 readiness",
                ],
            },
            "device": device,
            "material_manual_route": material,
            "material_tiny_manual_route": primary_fixture if args.material_scope == "tiny" else None,
            "gate": gate,
            "elapsed_seconds": time.perf_counter() - start,
        }
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if args.markdown_output:
            markdown_output = Path(args.markdown_output)
            markdown_output.parent.mkdir(parents=True, exist_ok=True)
            markdown_output.write_text(_render_markdown(payload), encoding="utf-8")
        print(json.dumps({"status": gate_status, "elapsed_seconds": payload["elapsed_seconds"]}, sort_keys=True))
        if gate_status != "passed":
            raise SystemExit(1)
        return
    records = []
    for state_dim in args.state_dims:
        for setting in args.settings:
            records.append(_run_fixture(harness, int(state_dim), setting, args))
    gate = _overall_gate(records, args, device)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "timestamp_utc": _dt.datetime.now(tz=_dt.timezone.utc).isoformat(),
        "host": platform.node(),
        "python_version": platform.python_version(),
        "tensorflow_version": harness.tf.__version__,
        "phase3_subplan": PHASE3_SUBPLAN,
        "manifest": {
            "gate_mode": args.gate_mode,
            "num_particles": int(args.num_particles),
            "seed_count": int(args.seed_count),
            "time_steps": int(args.time_steps),
            "state_dims": [int(x) for x in args.state_dims],
            "settings": args.settings,
            "theta": [float(x) for x in harness.THETA.numpy()],
            "fd_offsets": [int(x) for x in FD_OFFSETS],
            "fd_steps": [float(x) for x in args.fd_step_values],
            "fd_trim_rule": "drop highest and lowest objective values, regress remaining 11 points",
            "initial_transition_seed_schedule": (
                "seed indices 9100..9109; initial seeds [seed,17]; transition seeds [seed,29]"
            ),
            "contract_e_residual_seed_schedule": (
                "seed indices 9100..9109; residual seeds [seed,43+t] for t=0..9"
            ),
            "reverse_gradient_route": (
                "outer GradientTape diagnostic of summed per-seed Contract E scalars with "
                f"{args.reverse_transport_gradient_route}; transport VJP only, "
                "not a full manual likelihood reverse scan and not material evidence"
            ),
            "reverse_contract_e_gradient_probe": args.reverse_contract_e_gradient_probe,
            "forbidden_route_absent": "transport_ad_mode=full is not used",
            "contract_e_reset_factorization": args.contract_e_reset_factorization,
            "contract_e_diagnostic_labels": {
                "gap": (
                    "min residual Cholesky diagonal of sym(target_cov - plus_cov)+lambda I"
                    if args.contract_e_reset_factorization == "cholesky-ridge"
                    else "minimum eigenvalue of sym(target_cov - plus_cov)"
                ),
                "tilde_positive": (
                    "min Cholesky diagonal of tilde_cov+lambda I"
                    if args.contract_e_reset_factorization == "cholesky-ridge"
                    else "minimum retained positive eigenvalue of tilde_cov"
                ),
                "rank_margin": (
                    "legacy field: repeats min residual Cholesky diagonal under cholesky-ridge"
                    if args.contract_e_reset_factorization == "cholesky-ridge"
                    else "tilde rank minus target rank on the retained eigensupport"
                ),
            },
            "rho": float(args.rho),
            "tau": float(args.tau),
            "spectral_floor": float(args.spectral_floor),
            "chol_ridge_rel": float(args.chol_ridge_rel),
            "chol_ridge_abs": float(args.chol_ridge_abs),
            "chol_ridge_escalation": float(args.chol_ridge_escalation),
            "chol_ridge_max_attempts": int(args.chol_ridge_max_attempts),
            "covariance_residual_limit": float(args.covariance_residual_limit),
            "condition_limit": float(args.condition_limit),
        },
        "device": device,
        "records": records,
        "gate": gate,
        "elapsed_seconds": time.perf_counter() - start,
        "nonclaims": [
            "reverse gradients are diagnostics, not oracle",
            "not SIR/SV/nonlinear correctness",
            "not production readiness",
            "not HMC readiness",
            "not posterior correctness",
        ],
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.markdown_output:
        markdown_output = Path(args.markdown_output)
        markdown_output.parent.mkdir(parents=True, exist_ok=True)
        markdown_output.write_text(_render_markdown(payload), encoding="utf-8")
    print(json.dumps({"status": gate["status"], "elapsed_seconds": payload["elapsed_seconds"]}, sort_keys=True))
    if args.gate_mode == "material" and gate["status"] != "passed":
        raise SystemExit(1)
    if args.gate_mode == "smoke" and gate["status"] == "smoke_failed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
