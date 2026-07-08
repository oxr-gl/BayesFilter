"""Scalar SSL-LSTM filtering-likelihood geometry diagnostic.

This benchmark checks whether the scalar SVD-UKF filtering likelihood can
provide finite value/score telemetry and an accepted local SPD geometry
candidate for four inherited free parameters. It is not an HMC run and does
not claim posterior correctness, convergence, or default readiness.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")

import numpy as np
import tensorflow as tf


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bayesfilter.inference import (  # noqa: E402
    LOW_RANK_SPD_QUADRATIC_GEOMETRY_NONCLAIMS,
    LowRankSPDQuadraticGeometryConfig,
    fit_low_rank_spd_quadratic_geometry,
)
from bayesfilter.nonlinear.ssl_lstm_protocol import SSLLSTMStaticConfig  # noqa: E402
from bayesfilter.nonlinear.ssl_lstm_sgqf_ukf_adapters import (  # noqa: E402
    ssl_lstm_observation,
    ssl_lstm_parameter_slices,
    ssl_lstm_transition,
    tf_ssl_lstm_svd_ukf_score,
    unpack_ssl_lstm_parameters,
)
from bayesfilter.nonlinear.ssl_lstm_zhaocui_hmc_minimal import (  # noqa: E402
    minimal_ssl_lstm_theta,
)


SCRIPT_NAME = "benchmark_scalar_ssl_lstm_filtering_geometry_2026_07_08.py"
SCHEMA_VERSION = "scalar_ssl_lstm.filtering_geometry.v1"
PLAN_PATH = (
    "docs/plans/"
    "bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md"
)
SUBPLAN_PATH = (
    "docs/plans/"
    "bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-filtering-geometry-subplan-2026-07-08.md"
)
RESULT_PATH = (
    "docs/plans/"
    "bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-filtering-geometry-result-2026-07-08.md"
)
DEFAULT_JSON_PATH = (
    ROOT / "docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json"
)
DEFAULT_MARKDOWN_PATH = (
    ROOT / "docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.md"
)
FREE_PARAMETER_NAMES = (
    "latent_mean_weight.0.0",
    "latent_mean_bias.0",
    "observation_weight.0.0",
    "observation_bias.0",
)
NONCLAIMS = (
    "scalar filtering-likelihood geometry diagnostic only",
    "not complete-data oracle evidence",
    "not HMC readiness evidence",
    "not an HMC run",
    "not HMC convergence evidence",
    "not posterior correctness evidence",
    "not sampler superiority evidence",
    "not statistical ranking evidence",
    "not Zhao-Cui source-faithfulness evidence",
    "not GPU/XLA production-readiness evidence",
    "not default-readiness evidence",
)


@dataclass(frozen=True)
class ScalarFilteringGeometrySettings:
    """Configuration for the scalar filtering-likelihood geometry diagnostic."""

    horizon: int = 30
    seed: tuple[int, int] = (20260708, 2301)
    simulation_noise_scale: float = 1.0
    filter_name: str = "svd_ukf"
    free_parameter_names: tuple[str, ...] = FREE_PARAMETER_NAMES
    free_parameter_scale: tuple[float, ...] = (0.35, 0.35, 0.35, 0.35)
    prior_scale: float = 4.0
    spectral_gap_tolerance: float = 1.0e-10
    low_rank_rank: int = 4
    low_rank_sample_count: int = 72
    low_rank_min_samples_per_parameter: int = 5
    low_rank_trust_radius: float = 0.30
    low_rank_pilot_radius: float = 0.08
    low_rank_pilot_direction_count: int = 64
    low_rank_eigenvalue_floor: float = 1.0e-4
    low_rank_max_condition_number: float = 1.0e5
    low_rank_holdout_rmse_abs_tolerance: float = 5.0e-2
    low_rank_holdout_rmse_rel_tolerance: float = 5.0e-3
    low_rank_fit_max_iterations: int = 300
    compute_finite_difference_curvature: bool = True
    finite_difference_step_scale: float = 1.0e-3
    use_compiled_value_score: bool = True
    jit_compile_value_score: bool = False

    def __post_init__(self) -> None:
        for name in (
            "horizon",
            "low_rank_rank",
            "low_rank_sample_count",
            "low_rank_min_samples_per_parameter",
            "low_rank_pilot_direction_count",
            "low_rank_fit_max_iterations",
        ):
            value = int(getattr(self, name))
            if value <= 0:
                raise ValueError(f"{name} must be positive")
            object.__setattr__(self, name, value)
        if int(self.horizon) <= 1:
            raise ValueError("horizon must be greater than one")
        seed = tuple(int(item) for item in self.seed)
        if len(seed) != 2:
            raise ValueError("seed must contain exactly two integers")
        object.__setattr__(self, "seed", seed)
        if str(self.filter_name) != "svd_ukf":
            raise ValueError("Phase 1 is scoped to the svd_ukf filtering branch")
        names = tuple(str(item) for item in self.free_parameter_names)
        if len(names) != 4:
            raise ValueError("Phase 1 is scoped to exactly four free parameters")
        object.__setattr__(self, "free_parameter_names", names)
        scale = tuple(float(item) for item in self.free_parameter_scale)
        if len(scale) != len(names):
            raise ValueError("free_parameter_scale must match free_parameter_names")
        if any(not np.isfinite(item) or item <= 0.0 for item in scale):
            raise ValueError("free_parameter_scale entries must be positive finite")
        object.__setattr__(self, "free_parameter_scale", scale)
        for name in (
            "simulation_noise_scale",
            "prior_scale",
            "spectral_gap_tolerance",
            "low_rank_trust_radius",
            "low_rank_pilot_radius",
            "low_rank_eigenvalue_floor",
            "low_rank_max_condition_number",
            "low_rank_holdout_rmse_abs_tolerance",
            "low_rank_holdout_rmse_rel_tolerance",
            "finite_difference_step_scale",
        ):
            value = float(getattr(self, name))
            if not np.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be positive finite")
            object.__setattr__(self, name, value)
        object.__setattr__(
            self,
            "compute_finite_difference_curvature",
            bool(self.compute_finite_difference_curvature),
        )
        object.__setattr__(self, "use_compiled_value_score", bool(self.use_compiled_value_score))
        object.__setattr__(self, "jit_compile_value_score", bool(self.jit_compile_value_score))
        if self.jit_compile_value_score:
            raise ValueError("Phase 1 compiled-score repair is CPU-hidden non-XLA only")

    @property
    def dimension(self) -> int:
        return len(self.free_parameter_names)

    @property
    def effective_low_rank_rank(self) -> int:
        return min(self.low_rank_rank, max(self.dimension - 1, 0))

    @property
    def regression_parameter_count(self) -> int:
        return 1 + self.dimension + 1 + self.effective_low_rank_rank

    @property
    def required_finite_samples(self) -> int:
        return self.low_rank_min_samples_per_parameter * self.regression_parameter_count

    def payload(self) -> Mapping[str, Any]:
        return {
            "horizon": self.horizon,
            "seed": self.seed,
            "simulation_noise_scale": self.simulation_noise_scale,
            "filter_name": self.filter_name,
            "free_parameter_names": self.free_parameter_names,
            "free_parameter_scale": self.free_parameter_scale,
            "prior_scale": self.prior_scale,
            "spectral_gap_tolerance": self.spectral_gap_tolerance,
            "low_rank_rank": self.low_rank_rank,
            "effective_low_rank_rank": self.effective_low_rank_rank,
            "low_rank_sample_count": self.low_rank_sample_count,
            "low_rank_min_samples_per_parameter": self.low_rank_min_samples_per_parameter,
            "low_rank_trust_radius": self.low_rank_trust_radius,
            "low_rank_pilot_radius": self.low_rank_pilot_radius,
            "low_rank_pilot_direction_count": self.low_rank_pilot_direction_count,
            "low_rank_eigenvalue_floor": self.low_rank_eigenvalue_floor,
            "low_rank_max_condition_number": self.low_rank_max_condition_number,
            "low_rank_holdout_rmse_abs_tolerance": self.low_rank_holdout_rmse_abs_tolerance,
            "low_rank_holdout_rmse_rel_tolerance": self.low_rank_holdout_rmse_rel_tolerance,
            "low_rank_fit_max_iterations": self.low_rank_fit_max_iterations,
            "compute_finite_difference_curvature": self.compute_finite_difference_curvature,
            "finite_difference_step_scale": self.finite_difference_step_scale,
            "use_compiled_value_score": self.use_compiled_value_score,
            "jit_compile_value_score": self.jit_compile_value_score,
            "regression_parameter_count": self.regression_parameter_count,
            "required_finite_samples": self.required_finite_samples,
        }


@dataclass(frozen=True)
class ScalarFilteringGeometryTarget:
    """Four-parameter scalar SSL-LSTM filtering-likelihood target."""

    config: SSLLSTMStaticConfig
    base_theta: tf.Tensor
    free_indices: tuple[int, ...]
    free_parameter_names: tuple[str, ...]
    truth_free: tf.Tensor
    scale: tf.Tensor
    observations: tf.Tensor
    settings: ScalarFilteringGeometrySettings

    def __post_init__(self) -> None:
        if self.settings.use_compiled_value_score:
            compiled = tf.function(
                self._value_and_score_impl,
                jit_compile=bool(self.settings.jit_compile_value_score),
                reduce_retracing=True,
            )
        else:
            compiled = None
        object.__setattr__(self, "_compiled_value_and_score", compiled)

    def full_theta(self, free_values: tf.Tensor) -> tf.Tensor:
        free = tf.reshape(tf.convert_to_tensor(free_values, dtype=tf.float64), [-1])
        if int(free.shape[0]) != len(self.free_indices):
            raise ValueError("free_values must match Phase 1 free-parameter dimension")
        return tf.tensor_scatter_nd_update(
            tf.convert_to_tensor(self.base_theta, dtype=tf.float64),
            tf.constant([[index] for index in self.free_indices], dtype=tf.int32),
            free,
        )

    def value_and_score(self, free_values: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        free = tf.reshape(tf.convert_to_tensor(free_values, dtype=tf.float64), [-1])
        compiled = getattr(self, "_compiled_value_and_score", None)
        if compiled is not None:
            return compiled(free)
        return self._value_and_score_impl(free)

    def eager_value_and_score(self, free_values: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        free = tf.reshape(tf.convert_to_tensor(free_values, dtype=tf.float64), [-1])
        return self._value_and_score_impl(free)

    def _value_and_score_impl(self, free: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        full = self.full_theta(free)
        result, _components = tf_ssl_lstm_svd_ukf_score(
            self.observations,
            full,
            self.config,
            evidence_path=SUBPLAN_PATH,
            spectral_gap_tolerance=tf.constant(
                self.settings.spectral_gap_tolerance,
                dtype=tf.float64,
            ),
        )
        full_score = tf.reshape(tf.convert_to_tensor(result.score, dtype=tf.float64), [-1])
        if int(full_score.shape[0]) != int(self.config.parameter_dim):
            raise ValueError("filtering score has wrong parameter dimension")
        delta = free - self.truth_free
        variance = tf.constant(self.settings.prior_scale**2, dtype=tf.float64)
        prior_value = -0.5 * tf.reduce_sum(tf.square(delta) / variance)
        prior_score = -delta / variance
        score = tf.gather(full_score, list(self.free_indices)) + prior_score
        value = tf.convert_to_tensor(result.log_likelihood, dtype=tf.float64) + prior_value
        return tf.convert_to_tensor(value, dtype=tf.float64), tf.convert_to_tensor(score, dtype=tf.float64)

    def compiled_eager_parity(self, free_values: tf.Tensor) -> Mapping[str, Any]:
        if not self.settings.use_compiled_value_score:
            return {
                "checked": False,
                "reason": "compiled_value_score_disabled",
                "passed": None,
            }
        compiled_value, compiled_score = self.value_and_score(free_values)
        eager_value, eager_score = self.eager_value_and_score(free_values)
        compiled_value_np = float(tf.convert_to_tensor(compiled_value, dtype=tf.float64).numpy())
        eager_value_np = float(tf.convert_to_tensor(eager_value, dtype=tf.float64).numpy())
        compiled_score_np = np.asarray(tf.reshape(compiled_score, [-1]).numpy(), dtype=float)
        eager_score_np = np.asarray(tf.reshape(eager_score, [-1]).numpy(), dtype=float)
        value_abs_error = abs(compiled_value_np - eager_value_np)
        score_max_abs_error = float(
            np.max(np.abs(compiled_score_np - eager_score_np))
            if compiled_score_np.size
            else np.inf
        )
        passed = bool(value_abs_error <= 1.0e-10 and score_max_abs_error <= 1.0e-10)
        return {
            "checked": True,
            "passed": passed,
            "value_abs_error": value_abs_error,
            "score_max_abs_error": score_max_abs_error,
            "jit_compile": bool(self.settings.jit_compile_value_score),
            "execution_role": "cpu_hidden_non_xla_debug_optimization",
        }


def default_settings() -> ScalarFilteringGeometrySettings:
    return ScalarFilteringGeometrySettings()


def scalar_ssl_lstm_config(horizon: int) -> SSLLSTMStaticConfig:
    return SSLLSTMStaticConfig(
        horizon=int(horizon),
        latent_dim=1,
        hidden_dim=1,
        observation_dim=1,
    )


def free_parameter_indices(
    config: SSLLSTMStaticConfig,
    names: Sequence[str] = FREE_PARAMETER_NAMES,
) -> tuple[int, ...]:
    by_name = {name: index for index, name in enumerate(config.parameter_names)}
    missing = [name for name in names if name not in by_name]
    if missing:
        raise ValueError(f"unknown SSL-LSTM parameter names: {missing}")
    return tuple(int(by_name[name]) for name in names)


def build_filtering_geometry_target(
    settings: ScalarFilteringGeometrySettings | None = None,
) -> ScalarFilteringGeometryTarget:
    cfg = default_settings() if settings is None else settings
    config = scalar_ssl_lstm_config(cfg.horizon)
    base_theta = tf.reshape(tf.convert_to_tensor(minimal_ssl_lstm_theta(), dtype=tf.float64), [-1])
    if int(base_theta.shape[0]) != config.parameter_dim:
        raise ValueError("minimal scalar theta does not match scalar SSL-LSTM config")
    free_indices = free_parameter_indices(config, cfg.free_parameter_names)
    truth_free = tf.gather(base_theta, list(free_indices))
    observations = simulate_observation_path(config, base_theta, cfg)
    return ScalarFilteringGeometryTarget(
        config=config,
        base_theta=base_theta,
        free_indices=free_indices,
        free_parameter_names=cfg.free_parameter_names,
        truth_free=tf.convert_to_tensor(truth_free, dtype=tf.float64),
        scale=tf.constant(cfg.free_parameter_scale, dtype=tf.float64),
        observations=observations,
        settings=cfg,
    )


def simulate_observation_path(
    config: SSLLSTMStaticConfig,
    theta: tf.Tensor,
    settings: ScalarFilteringGeometrySettings,
) -> tf.Tensor:
    """Simulate scalar observations from the SSL-LSTM fixture."""

    params = unpack_ssl_lstm_parameters(theta, config)
    noise = tf.random.stateless_normal(
        [int(settings.horizon), 2],
        seed=tf.constant(settings.seed, dtype=tf.int32),
        dtype=tf.float64,
    )
    state = tf.reshape(params.initial_mean, [1, config.augmented_state_dim])
    states = [tf.reshape(state[0], [config.augmented_state_dim])]
    scale = tf.constant(settings.simulation_noise_scale, dtype=tf.float64)
    for time_index in range(1, int(settings.horizon)):
        transition_mean = ssl_lstm_transition(params, state)
        latent = (
            transition_mean[:, :1]
            + scale * params.process_std[tf.newaxis, :] * noise[time_index : time_index + 1, :1]
        )
        state = tf.concat([latent, transition_mean[:, 1:]], axis=1)
        states.append(tf.reshape(state[0], [config.augmented_state_dim]))
    state_tensor = tf.stack(states, axis=0)
    observation_mean = ssl_lstm_observation(params, state_tensor)
    observations = observation_mean + scale * params.observation_std[tf.newaxis, :] * noise[:, 1:2]
    return tf.convert_to_tensor(observations, dtype=tf.float64)


def run_filtering_geometry_diagnostic(
    settings: ScalarFilteringGeometrySettings | None = None,
) -> Mapping[str, Any]:
    cfg = default_settings() if settings is None else settings
    start = time.perf_counter()
    target = build_filtering_geometry_target(cfg)
    center = tf.convert_to_tensor(target.truth_free, dtype=tf.float64)
    parity = target.compiled_eager_parity(center)
    initial_value, initial_score, initial_status = safe_value_and_score(target, center)
    finite_difference = (
        finite_difference_negative_score_jacobian(target, center)
        if cfg.compute_finite_difference_curvature
        else {"computed": False, "reason": "disabled_by_settings"}
    )

    low_rank_config = LowRankSPDQuadraticGeometryConfig(
        rank=cfg.low_rank_rank,
        sample_count=cfg.low_rank_sample_count,
        min_samples_per_parameter=cfg.low_rank_min_samples_per_parameter,
        trust_radius=cfg.low_rank_trust_radius,
        pilot_radius=cfg.low_rank_pilot_radius,
        pilot_direction_count=cfg.low_rank_pilot_direction_count,
        eigenvalue_floor=cfg.low_rank_eigenvalue_floor,
        max_condition_number=cfg.low_rank_max_condition_number,
        holdout_rmse_abs_tolerance=cfg.low_rank_holdout_rmse_abs_tolerance,
        holdout_rmse_rel_tolerance=cfg.low_rank_holdout_rmse_rel_tolerance,
        fit_max_iterations=cfg.low_rank_fit_max_iterations,
        seed=cfg.seed,
    )
    geometry = fit_low_rank_spd_quadratic_geometry(
        target.value_and_score,
        center,
        scale=target.scale,
        config=low_rank_config,
    )
    geometry_payload = geometry.payload(include_arrays=True)
    geometry_diagnostics = geometry_payload["diagnostics"]
    sample_ratio_passed = bool(
        geometry_diagnostics.get("finite_sample_count", 0)
        >= cfg.required_finite_samples
    )
    precision_summary = geometry_payload.get("precision_eigen_summary")
    precision_spd_passed = bool(precision_summary and precision_summary.get("positive"))
    condition_passed = bool(
        precision_summary
        and precision_summary.get("condition_number") is not None
        and float(precision_summary["condition_number"]) <= cfg.low_rank_max_condition_number * (1.0 + 1.0e-8)
    )
    initial_finite_passed = initial_status == "finite"
    geometry_sanity_passed = bool(
        initial_finite_passed
        and geometry.accepted
        and sample_ratio_passed
        and precision_spd_passed
        and condition_passed
        and parity.get("passed", True) is not False
    )
    vetoes = []
    if parity.get("passed") is False:
        vetoes.append("compiled_eager_value_score_mismatch")
    if not initial_finite_passed:
        vetoes.append(f"initial_filtering_value_score_{initial_status}")
    if not geometry.accepted:
        vetoes.append(f"low_rank_geometry_{geometry.status}")
    if not sample_ratio_passed:
        vetoes.append("finite_sample_ratio_failed")
    if geometry.accepted and not precision_spd_passed:
        vetoes.append("precision_not_spd")
    if geometry.accepted and not condition_passed:
        vetoes.append("precision_condition_above_cap")

    payload = {
        "schema_version": SCHEMA_VERSION,
        "artifact_role": "cpu_hidden_scalar_filtering_likelihood_geometry_diagnostic",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "script": f"docs/benchmarks/{SCRIPT_NAME}",
        "plan_path": PLAN_PATH,
        "subplan_path": SUBPLAN_PATH,
        "result_path": RESULT_PATH,
        "classification": "extension_or_invention",
        "target_scope": "scalar_ssl_lstm:svd_ukf_filtering_geometry:phase1",
        "settings": cfg.payload(),
        "environment": environment_payload(),
        "git": git_payload(),
        "target": target_payload(target),
        "center": {
            "position_role": "truth_free_initial_center",
            "coordinate_system": "free_parameters_center_plus_scale_times_z",
            "free_parameter_values": center,
            "log_prob": initial_value,
            "score": initial_score,
            "score_norm": None if initial_status != "finite" else float(np.linalg.norm(initial_score * np.asarray(target.scale.numpy(), dtype=float))),
            "status": initial_status,
            "reports_map_quality": False,
        },
        "compiled_value_score": parity,
        "finite_difference_curvature": finite_difference,
        "low_rank_geometry": geometry_payload,
        "artifact_array_policy": {
            "low_rank_geometry_arrays_included": True,
            "array_scope": "private_local_four_dimensional_diagnostic_artifact",
            "reason": "Phase 2 mass handoff requires auditable precision and covariance matrices",
        },
        "decision": {
            "geometry_sanity_passed": geometry_sanity_passed,
            "initial_finite_passed": initial_finite_passed,
            "low_rank_geometry_accepted": bool(geometry.accepted),
            "sample_ratio_passed": sample_ratio_passed,
            "precision_spd_passed": precision_spd_passed,
            "condition_passed": condition_passed,
            "compiled_eager_parity_passed": parity.get("passed"),
            "vetoes": tuple(vetoes),
            "viable_for_phase2_mass_handoff": geometry_sanity_passed,
            "next_justified_action": (
                "draft geometry-to-mass handoff subplan"
                if geometry_sanity_passed
                else "write Phase 1 repair-trigger result before any mass or HMC step"
            ),
        },
        "metric_roles": {
            "geometry_sanity_passed": "primary_phase1_pass_fail",
            "initial_value_score_finiteness": "promotion_veto",
            "low_rank_geometry_accepted": "promotion_veto",
            "finite_sample_count": "promotion_veto",
            "precision_spd": "promotion_veto",
            "precision_condition_number": "promotion_veto",
            "center_score_norm": "explanatory_only",
            "finite_difference_curvature": "explanatory_only",
            "holdout_rmse": "geometry_fit_gate_only_not_hmc_evidence",
            "compiled_eager_parity": "implementation_veto",
        },
        "inference_status": {
            "hard_veto_screen": "passed" if not vetoes else "failed",
            "statistically_supported_ranking": "none; single diagnostic target",
            "descriptive_only_differences": (
                "score norm, finite-difference curvature, residuals, condition number, and runtime"
            ),
            "default_readiness": "not assessed",
            "hmc_readiness": "not assessed; Phase 1 does not run HMC",
            "next_evidence_needed": "geometry-to-mass handoff only if geometry_sanity_passed is true",
        },
        "run_manifest": {
            "command": (
                "timeout 300 env CUDA_VISIBLE_DEVICES=-1 python "
                "docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_geometry_2026_07_08.py"
            ),
            "conda_env": os.environ.get("CONDA_DEFAULT_ENV", "N/A"),
            "cpu_gpu_status": "CPU-hidden debug/reference exception",
            "compiled_value_score_status": (
                "tf.function_jit_compile_false_cpu_hidden_debug"
                if cfg.use_compiled_value_score
                else "eager"
            ),
            "data_version": "stateless_simulated_scalar_ssl_lstm_filtering_path_v1",
            "random_seeds": cfg.seed,
            "wall_time_seconds": float(time.perf_counter() - start),
            "output_artifacts": (
                str(DEFAULT_JSON_PATH.relative_to(ROOT)),
                str(DEFAULT_MARKDOWN_PATH.relative_to(ROOT)),
            ),
            "plan_file": PLAN_PATH,
            "subplan_file": SUBPLAN_PATH,
            "result_file": RESULT_PATH,
        },
        "nonclaims": NONCLAIMS + tuple(LOW_RANK_SPD_QUADRATIC_GEOMETRY_NONCLAIMS),
    }
    return json_ready(payload)


def safe_value_and_score(
    target: ScalarFilteringGeometryTarget,
    free_values: tf.Tensor,
) -> tuple[float | None, list[float] | None, str]:
    try:
        value, score = target.value_and_score(free_values)
        value_np = float(tf.convert_to_tensor(value, dtype=tf.float64).numpy())
        score_np = np.asarray(tf.reshape(tf.convert_to_tensor(score, dtype=tf.float64), [-1]).numpy(), dtype=float)
    except Exception:  # noqa: BLE001 - diagnostic fail-closed path.
        return None, None, "exception"
    if score_np.shape != (len(target.free_indices),):
        return value_np, score_np.tolist(), "score_shape_mismatch"
    if not np.isfinite(value_np) or not np.all(np.isfinite(score_np)):
        return value_np, score_np.tolist(), "nonfinite"
    return value_np, score_np.tolist(), "finite"


def finite_difference_negative_score_jacobian(
    target: ScalarFilteringGeometryTarget,
    center: tf.Tensor,
) -> Mapping[str, Any]:
    center_np = np.asarray(tf.reshape(center, [-1]).numpy(), dtype=float)
    scale_np = np.asarray(target.scale.numpy(), dtype=float)
    dim = int(center_np.size)
    step_scale = float(target.settings.finite_difference_step_scale)
    columns = []
    failures = []
    for index in range(dim):
        step = step_scale * scale_np[index]
        plus = center_np.copy()
        minus = center_np.copy()
        plus[index] += step
        minus[index] -= step
        _value_plus, score_plus, status_plus = safe_value_and_score(
            target,
            tf.constant(plus, dtype=tf.float64),
        )
        _value_minus, score_minus, status_minus = safe_value_and_score(
            target,
            tf.constant(minus, dtype=tf.float64),
        )
        if status_plus != "finite" or status_minus != "finite":
            failures.append(
                {
                    "index": index,
                    "plus_status": status_plus,
                    "minus_status": status_minus,
                }
            )
            columns.append(np.full(dim, np.nan, dtype=float))
            continue
        columns.append(
            (
                np.asarray(score_plus, dtype=float)
                - np.asarray(score_minus, dtype=float)
            )
            / (2.0 * step)
        )
    jacobian = np.column_stack(columns)
    negative = -0.5 * (jacobian + jacobian.T)
    whitened = scale_np[:, np.newaxis] * negative * scale_np[np.newaxis, :]
    finite = bool(np.all(np.isfinite(whitened)))
    return {
        "computed": True,
        "finite": finite,
        "failures": failures,
        "coordinate_system": "whitened_center_plus_scale_times_z",
        "step_scale": step_scale,
        "negative_score_jacobian_eigen_summary": (
            eigen_summary(whitened) if finite else None
        ),
        "role": "explanatory_only_not_phase1_promotion",
    }


def target_payload(target: ScalarFilteringGeometryTarget) -> Mapping[str, Any]:
    slices = ssl_lstm_parameter_slices(target.config)
    return {
        "model": "scalar_ssl_lstm_filtering_likelihood",
        "filter_name": target.settings.filter_name,
        "filter_score_helper": "tf_ssl_lstm_svd_ukf_score",
        "horizon": int(target.config.horizon),
        "latent_dim": int(target.config.latent_dim),
        "hidden_dim": int(target.config.hidden_dim),
        "observation_dim": int(target.config.observation_dim),
        "augmented_state_dim": int(target.config.augmented_state_dim),
        "full_parameter_dim": int(target.config.parameter_dim),
        "free_parameter_dim": len(target.free_indices),
        "free_parameter_names": target.free_parameter_names,
        "free_parameter_indices": target.free_indices,
        "fixed_parameter_count": int(target.config.parameter_dim - len(target.free_indices)),
        "truth_free_parameters": target.truth_free,
        "observation_shape": tuple(int(item) for item in target.observations.shape),
        "parameter_slice_starts": {
            "latent_weight_start": int(slices.latent_weight_start),
            "latent_bias_start": int(slices.latent_bias_start),
            "observation_weight_start": int(slices.observation_weight_start),
            "observation_bias_start": int(slices.observation_bias_start),
        },
        "likelihood_terms": (
            "svd_ukf_filtering_log_likelihood",
            "weak_gaussian_prior_on_four_free_parameters",
        ),
    }


def eigen_summary(matrix: Any) -> Mapping[str, Any]:
    values = np.linalg.eigvalsh(np.asarray(matrix, dtype=float))
    finite = bool(np.all(np.isfinite(values)))
    positive = bool(finite and np.all(values > 0.0))
    return {
        "finite": finite,
        "positive": positive,
        "min": float(np.min(values)) if finite else None,
        "max": float(np.max(values)) if finite else None,
        "condition_number": (
            float(np.max(values) / np.min(values)) if positive else None
        ),
        "values": tuple(float(value) for value in values) if finite else None,
    }


def environment_payload() -> Mapping[str, Any]:
    return {
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", "<unset>"),
        "cpu_hidden": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
        "tf_version": tf.__version__,
        "tf_physical_gpus": [device.name for device in tf.config.list_physical_devices("GPU")],
        "trust_basis": "cpu_hidden_debug_reference_exception",
    }


def git_payload() -> Mapping[str, Any]:
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:  # noqa: BLE001 - provenance best effort.
        commit = "unavailable"
    return {"commit": commit}


def write_artifacts(
    payload: Mapping[str, Any],
    *,
    json_path: Path = DEFAULT_JSON_PATH,
    markdown_path: Path = DEFAULT_MARKDOWN_PATH,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, indent=2, sort_keys=True)
        handle.write("\n")
    markdown_path.write_text(render_markdown(payload), encoding="utf-8")


def render_markdown(payload: Mapping[str, Any]) -> str:
    decision = payload["decision"]
    low_rank = payload["low_rank_geometry"]
    precision = low_rank.get("precision_eigen_summary")
    lines = [
        "# Scalar SSL-LSTM Filtering Geometry Diagnostic - 2026-07-08",
        "",
        "## Decision",
        "",
        f"- geometry_sanity_passed: `{decision['geometry_sanity_passed']}`",
        f"- vetoes: `{decision['vetoes']}`",
        f"- next_justified_action: {decision['next_justified_action']}",
        "",
        "## Geometry",
        "",
        f"- low-rank accepted/status: `{low_rank['accepted']}` / `{low_rank['status']}`",
        f"- finite sample count: `{low_rank['diagnostics'].get('finite_sample_count')}`",
        f"- required finite samples: `{low_rank['diagnostics'].get('required_finite_samples')}`",
        f"- precision eigen summary: `{precision}`",
        "",
        "## Nonclaims",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["nonclaims"])
    lines.append("")
    return "\n".join(lines)


def json_ready(value: Any) -> Any:
    if isinstance(value, tf.Tensor):
        return json_ready(value.numpy())
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--json-path", type=Path, default=DEFAULT_JSON_PATH)
    parser.add_argument("--markdown-path", type=Path, default=DEFAULT_MARKDOWN_PATH)
    parser.add_argument("--horizon", type=int, default=default_settings().horizon)
    parser.add_argument(
        "--sample-count",
        type=int,
        default=default_settings().low_rank_sample_count,
    )
    parser.add_argument(
        "--pilot-direction-count",
        type=int,
        default=default_settings().low_rank_pilot_direction_count,
    )
    parser.add_argument(
        "--trust-radius",
        type=float,
        default=default_settings().low_rank_trust_radius,
    )
    parser.add_argument(
        "--no-finite-difference-curvature",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--eager-value-score",
        action="store_true",
        default=False,
        help="Disable the CPU-hidden non-XLA compiled value/score wrapper.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    settings = replace(
        default_settings(),
        horizon=int(args.horizon),
        low_rank_sample_count=int(args.sample_count),
        low_rank_pilot_direction_count=int(args.pilot_direction_count),
        low_rank_trust_radius=float(args.trust_radius),
        compute_finite_difference_curvature=not bool(args.no_finite_difference_curvature),
        use_compiled_value_score=not bool(args.eager_value_score),
    )
    payload = run_filtering_geometry_diagnostic(settings)
    write_artifacts(
        payload,
        json_path=Path(args.json_path),
        markdown_path=Path(args.markdown_path),
    )
    print(json.dumps(payload["decision"], sort_keys=True))
    return 0 if payload["decision"]["geometry_sanity_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
