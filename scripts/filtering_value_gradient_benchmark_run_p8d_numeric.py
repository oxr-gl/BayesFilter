#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable

import tensorflow as tf
import tensorflow_probability as tfp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bayesfilter import StatePartition
import bayesfilter.highdim as highdim
from bayesfilter.highdim.sv_mixture_cut4 import (
    exact_transformed_sv_independent_panel_dense_reference,
    independent_panel_sv_mixture_cut4_filter,
    independent_panel_sv_mixture_kalman_filter,
)
from bayesfilter.linear import TFLinearGaussianStateSpaceDerivatives
from bayesfilter.linear.kalman_tf import tf_kalman_log_likelihood
from bayesfilter.nonlinear.sigma_points_tf import tf_svd_sigma_point_log_likelihood
from bayesfilter.nonlinear.svd_cut_tf import tf_svd_cut4_log_likelihood
from bayesfilter.nonlinear.svd_sigma_point_derivatives_tf import (
    TFStructuralFirstDerivatives,
    tf_svd_cubature_score,
    tf_svd_cut4_score,
    tf_svd_ukf_score,
)
from bayesfilter.structural import StructuralFilterConfig
from bayesfilter.structural_tf import (
    TFStructuralStateSpace,
    affine_structural_to_linear_gaussian_tf,
    make_affine_structural_tf,
)
from bayesfilter.testing.tf_covariance_differentiated_kalman_reference import (
    tf_differentiated_kalman_loglik,
)
from experiments.dpf_implementation.tf_tfp.filters.bootstrap_pf_tf import (
    run_bootstrap_particle_filter_tf,
)
from experiments.dpf_implementation.tf_tfp.filters.ledh_pfpf_alg1_ukf_tf import (
    OT_ANNEALED_COVARIANCE_CARRY_ROUTE,
    OT_SINKHORN_COVARIANCE_CARRY_ROUTE,
    apply_ot_resampling_state_tf,
    li_coates_ledh_alg1_time_step_tf,
    ledh_pfpf_alg1_scalar_sv_graph_log_likelihood_tf,
    run_ledh_pfpf_alg1_scalar_sv_graph_tf,
    run_ledh_pfpf_alg1_ukf_tf,
)
from experiments.dpf_implementation.tf_tfp.resampling.sinkhorn_tf import (
    pairwise_squared_euclidean_tf,
)
from scripts.filtering_value_gradient_benchmark_generate_p8_datasets import (
    _generalized_sv_prior_mean_dataset,
    _lgssm_dataset,
    _predator_prey_dataset,
    _sir_dataset,
    _sv_dataset,
)


DATE = "2026-06-13"
P8D_PLAN_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-gap-closure-plan-2026-06-13.md"
P8D_VISIBLE_PLAN_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-visible-repair-execution-plan-2026-06-13.md"
PLAN_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-blocker-closure-master-plan-2026-06-11.md"
GRADIENT_REPAIR_PLAN_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-gradient-repair-plan-2026-06-12.md"
SOURCE_SCOPE_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json"
ADAPTER_MATRIX_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-adapter-status-matrix-2026-06-11.csv"
DATASET_MANIFEST_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.json"

DEFAULT_JSON = ROOT / f"docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-numeric-results-{DATE}.json"
DEFAULT_VALUE_CSV = ROOT / f"docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-value-table-{DATE}.csv"
DEFAULT_SCORE_CSV = ROOT / f"docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-score-table-{DATE}.csv"
DEFAULT_CURVATURE_CSV = ROOT / f"docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-curvature-table-{DATE}.csv"
DEFAULT_STATUS_CSV = ROOT / f"docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-status-table-{DATE}.csv"
DEFAULT_UNCERTAINTY_CSV = ROOT / f"docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-stochastic-uncertainty-table-{DATE}.csv"
DEFAULT_MD = ROOT / f"docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-numeric-summary-{DATE}.md"
P8D_EXECUTION_GATE_MESSAGE = (
    "P8d full artifact execution is gated. Re-run with --enable-p8d-execution "
    "only after focused local validation and Claude implementation review pass."
)

LGSSM_ROW = "benchmark_lgssm_exact_oracle_m3_T50"
SV_ROW = "zhao_cui_sv_actual_nongaussian_T1000"
KSC_ROW = "zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000"
SIR_ROW = "zhao_cui_spatial_sir_austria_j9_T20"
PREDATOR_PREY_ROW = "zhao_cui_predator_prey_T20"
GENERALIZED_SV_ROW = "zhao_cui_generalized_sv_synthetic_from_estimated_values"
KALMAN = "kalman_exact_or_mixture_enumeration"
UKF = "ukf"
SVD = "svd_sigma_point"
CUT4 = "cut4"
ZHAO_CUI = "zhao_cui_scalar_or_multistate"
BOOTSTRAP_DPF = "bootstrap_dpf_current"
LEDH_ALG1_DPF = "ledh_pfpf_alg1_ukf_current"
DPF_SEEDS = [81120, 81121, 81122, 81123, 81124]
DPF_PARTICLE_COUNT = 8
SIGMA_OBSERVATION_FLOOR = tf.constant(1e-9, dtype=tf.float64)
DPF_SV_LOG_SQUARE_OFFSET = tf.constant(1e-6, dtype=tf.float64)
DPF_SV_LOG_SQUARE_SURROGATE_VARIANCE = tf.constant(2.0, dtype=tf.float64)
ROW_HORIZONS = {
    LGSSM_ROW: 50,
    SV_ROW: 1000,
    KSC_ROW: 1000,
    SIR_ROW: 20,
    PREDATOR_PREY_ROW: 20,
    GENERALIZED_SV_ROW: 1008,
}
P8D_PLAN_REVIEW_STATUS = "claude_inline_readonly_review_verdict_agree"
P8G_ROUTE_VARIANT = "p8g_sv_scalar_graph"
P8G_G4_PLAN_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-subplan-2026-06-15.md"
P8G_G4_RESULT_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-result-2026-06-15.md"
P8G_G4_SELECTED_BLOCKED_CSV = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-selected-blocked-2026-06-15.csv"
P8G_G4_DEFAULT_RUNTIME_BUDGET_SECONDS = 1800.0
P8G_G4_RELATIVE_ESS_FLOOR = 0.25
P8G_G4_MC_SE_ABS_FLOOR = 2.0
P8G_G4_MC_SE_RELATIVE_FRACTION = 0.0025
P8G_G4_ADJACENT_DELTA_ABS_BUFFER = 1.0
P8H_ROUTE_VARIANT = "p8h_sv_scalar_graph_ot_resampled_alg1"
P8H_DEFAULT_RESAMPLING_ROUTE = OT_SINKHORN_COVARIANCE_CARRY_ROUTE
P8H_PHASE5_PLAN_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-subplan-2026-06-15.md"
P8H_PHASE7_PLAN_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-subplan-2026-06-15.md"
P8H_PHASE8_PLAN_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase8-hmc-diagnostic-tiers-subplan-2026-06-15.md"
P8H_PHASE5_SELECTED_BLOCKED_CSV = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-selected-blocked-2026-06-16.csv"
P8H_PHASE5_DEFAULT_RUNTIME_BUDGET_SECONDS = 1800.0
P8H_PHASE5_MC_SE_ABS_FLOOR = 2.0
P8H_PHASE5_MC_SE_RELATIVE_FRACTION = 0.0025
P8H_PHASE5_ADJACENT_DELTA_ABS_BUFFER = 1.0
P8J_PHASE5_PLAN_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-subplan-2026-06-17.md"
P8J_PHASE5_SELECTED_BLOCKED_CSV = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-selected-blocked-2026-06-17.csv"
P8J_ROUTE_VARIANT = "p8j_sir_d18_ot_resampled_alg1"
P8J_BOOTSTRAP_ROUTE_VARIANT = "p8j_sir_d18_bootstrap"
P8J_PHASE5_DEFAULT_RUNTIME_BUDGET_SECONDS = 1800.0
P8J_PHASE5_MC_SE_ABS_FLOOR = 2.0
P8J_PHASE5_MC_SE_RELATIVE_FRACTION = 0.0025
P8J_PHASE5_ADJACENT_DELTA_ABS_BUFFER = 1.0


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unavailable"


def _dirty_summary() -> str:
    try:
        output = subprocess.check_output(
            ["git", "status", "--short"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return "unavailable"
    lines = output.splitlines()
    return f"{len(lines)} git-status-short entries"


def _source_artifacts_payload() -> dict[str, str]:
    return {
        "plan": _rel(P8D_VISIBLE_PLAN_PATH),
        "p8_master_plan": _rel(PLAN_PATH),
        "gradient_repair_plan": _rel(GRADIENT_REPAIR_PLAN_PATH),
        "p8c_plan": "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-evaluator-adapter-and-dpf-seed-plan-2026-06-13.md",
        "p8d_visible_repair_execution_plan": _rel(P8D_VISIBLE_PLAN_PATH),
        "p8d_paused_gap_closure_plan": _rel(P8D_PLAN_PATH),
        "p8c_partial_numeric_baseline": "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-results-2026-06-13.json",
        "source_scope_contract": _rel(SOURCE_SCOPE_PATH),
        "dataset_manifest": _rel(DATASET_MANIFEST_PATH),
        "adapter_status_matrix": _rel(ADAPTER_MATRIX_PATH),
    }


def _run_manifest_payload() -> dict[str, Any]:
    return {
        "git_commit": _git_commit(),
        "dirty_state_summary": _dirty_summary(),
        "command": "env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --enable-p8d-execution",
        "environment": "CPU-only TensorFlow with CUDA hidden by policy",
        "cpu_gpu_status": "CPU-only deliberate",
        "dtype": "tf.float64",
        "seeds": {
            "lgssm": 81100,
            "sv_actual_and_ksc": 81101,
            "sir": 81103,
            "predator_prey": 81104,
            "generalized_sv": 81105,
        },
        "plan_file": _rel(P8D_VISIBLE_PLAN_PATH),
        "gradient_repair_plan_file": _rel(GRADIENT_REPAIR_PLAN_PATH),
        "p8c_plan_file": "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-evaluator-adapter-and-dpf-seed-plan-2026-06-13.md",
        "p8d_visible_plan_file": _rel(P8D_VISIBLE_PLAN_PATH),
        "output_json": _rel(DEFAULT_JSON),
        "wall_time_seconds": None,
    }


def _float_or_none(value: Any) -> float | None:
    if value is None:
        return None
    number = float(value)
    if not math.isfinite(number):
        return None
    return number


def _tf_float(value: tf.Tensor) -> float:
    return float(tf.convert_to_tensor(value, dtype=tf.float64).numpy())


def _tensor_list(value: tf.Tensor | None) -> list[float] | None:
    if value is None:
        return None
    tensor = tf.reshape(tf.convert_to_tensor(value, dtype=tf.float64), [-1])
    return [float(item) for item in tensor.numpy().tolist()]


def _parse_int_csv(value: str) -> list[int]:
    parsed = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not parsed:
        raise ValueError("expected at least one integer")
    return parsed


def _parse_str_csv(value: str) -> list[str]:
    parsed = [item.strip() for item in value.split(",") if item.strip()]
    if not parsed:
        raise ValueError("expected at least one item")
    return parsed


def _parse_rows_csv(value: str) -> list[str]:
    row_map = {
        "actual_sv": SV_ROW,
        SV_ROW: SV_ROW,
        "lgssm": LGSSM_ROW,
        LGSSM_ROW: LGSSM_ROW,
        "ksc_sv": KSC_ROW,
        KSC_ROW: KSC_ROW,
        "sir": SIR_ROW,
        SIR_ROW: SIR_ROW,
        "predator_prey": PREDATOR_PREY_ROW,
        PREDATOR_PREY_ROW: PREDATOR_PREY_ROW,
        "generalized_sv": GENERALIZED_SV_ROW,
        GENERALIZED_SV_ROW: GENERALIZED_SV_ROW,
    }
    return [row_map.get(item, item) for item in _parse_str_csv(value)]


def _log_square_surrogate_observations(
    observations: tf.Tensor,
    *,
    offset: tf.Tensor = DPF_SV_LOG_SQUARE_OFFSET,
) -> tf.Tensor:
    raw = tf.convert_to_tensor(observations, dtype=tf.float64)
    return tf.math.log(tf.square(raw) + tf.cast(offset, tf.float64))


def _raw_zero_mean_normal_log_density_from_log_scale(
    points: tf.Tensor,
    observation: tf.Tensor,
    log_scale: tf.Tensor,
) -> tf.Tensor:
    del points
    y = tf.reshape(tf.convert_to_tensor(observation, dtype=tf.float64), [1])[0]
    log_scale = tf.convert_to_tensor(log_scale, dtype=tf.float64)
    standardized = y * tf.exp(-log_scale)
    return -0.5 * tf.math.log(tf.constant(2.0 * math.pi, dtype=tf.float64)) - log_scale - 0.5 * tf.square(standardized)


def _lgssm_observations() -> tf.Tensor:
    return tf.convert_to_tensor(_lgssm_dataset(81100)["observations"], dtype=tf.float64)


def _sv_observations() -> tf.Tensor:
    return tf.convert_to_tensor(_sv_dataset(81101)["observations"], dtype=tf.float64)


def _sv_theta() -> tf.Tensor:
    return tf.constant(_sv_dataset(81101)["truth_theta"], dtype=tf.float64)


def _predator_prey_observations() -> tf.Tensor:
    return tf.convert_to_tensor(_predator_prey_dataset(81104)["observations"], dtype=tf.float64)


def _predator_prey_theta() -> tf.Tensor:
    return tf.constant(_predator_prey_dataset(81104)["truth_theta"], dtype=tf.float64)


def _sir_observations() -> tf.Tensor:
    return tf.convert_to_tensor(_sir_dataset(81103)["observations"], dtype=tf.float64)


def _generalized_sv_observations() -> tf.Tensor:
    return tf.convert_to_tensor(
        _generalized_sv_prior_mean_dataset(81105)["observations"],
        dtype=tf.float64,
    )


def _generalized_sv_theta() -> tf.Tensor:
    return tf.constant(
        _generalized_sv_prior_mean_dataset(81105)["truth_theta"],
        dtype=tf.float64,
    )


def _normal01() -> tfp.distributions.Normal:
    return tfp.distributions.Normal(
        loc=tf.constant(0.0, dtype=tf.float64),
        scale=tf.constant(1.0, dtype=tf.float64),
    )


def _score_payload(value: tf.Tensor, score: tf.Tensor | None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "log_likelihood": _tf_float(value),
        "score": None,
        "score_l2_norm": None,
        "score_max_component": None,
        "score_min_component": None,
    }
    if score is not None:
        score_tensor = tf.convert_to_tensor(score, dtype=tf.float64)
        payload.update(
            {
                "score": _tensor_list(score_tensor),
                "score_l2_norm": _tf_float(tf.linalg.norm(score_tensor)),
                "score_max_component": _tf_float(tf.reduce_max(score_tensor)),
                "score_min_component": _tf_float(tf.reduce_min(score_tensor)),
            }
        )
    return payload


def _finite_difference_score(
    value_fn: Callable[[tf.Tensor], tf.Tensor],
    theta: tf.Tensor,
    *,
    step: float = 1e-4,
) -> tf.Tensor:
    theta = tf.convert_to_tensor(theta, dtype=tf.float64)
    entries = []
    eye = tf.eye(int(theta.shape[0]), dtype=tf.float64)
    h = tf.constant(step, dtype=tf.float64)
    for index in range(int(theta.shape[0])):
        direction = eye[index]
        plus = tf.convert_to_tensor(value_fn(theta + h * direction), dtype=tf.float64)
        minus = tf.convert_to_tensor(value_fn(theta - h * direction), dtype=tf.float64)
        entries.append((plus - minus) / (2.0 * h))
    return tf.stack(entries)


def _value_and_autodiff_score(
    value_fn: Callable[[tf.Tensor], tf.Tensor],
    theta: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor | None]:
    theta = tf.convert_to_tensor(theta, dtype=tf.float64)
    with tf.GradientTape() as tape:
        tape.watch(theta)
        value = tf.convert_to_tensor(value_fn(theta), dtype=tf.float64)
    score = tape.gradient(value, theta)
    return value, score


def _all_finite(*values: tf.Tensor | None) -> bool:
    for value in values:
        if value is not None and not bool(
            tf.reduce_all(tf.math.is_finite(tf.convert_to_tensor(value, dtype=tf.float64))).numpy()
        ):
            return False
    return True


def _tensor_device_is_gpu(device: Any) -> bool:
    return "GPU" in str(device).upper()


def _finite_tensor_bool(value: Any) -> bool:
    return bool(
        tf.reduce_all(
            tf.math.is_finite(tf.convert_to_tensor(value, dtype=tf.float64))
        ).numpy()
    )


def _lgssm_structural(theta: tf.Tensor):
    phi = theta[:3]
    q_scale = theta[3]
    r_scale = theta[4]
    observation_matrix = tf.constant(
        [
            [1.0, 0.25, -0.15],
            [0.2, 1.1, 0.3],
            [-0.1, 0.35, 0.9],
        ],
        dtype=tf.float64,
    )
    partition = StatePartition(
        state_names=("x1", "x2", "x3"),
        stochastic_indices=(0, 1, 2),
        deterministic_indices=(),
        innovation_dim=3,
    )
    return make_affine_structural_tf(
        partition=partition,
        initial_mean=tf.zeros([3], dtype=tf.float64),
        initial_covariance=tf.linalg.diag(tf.square(q_scale) / (1.0 - tf.square(phi))),
        transition_offset=tf.zeros([3], dtype=tf.float64),
        transition_matrix=tf.linalg.diag(phi),
        innovation_matrix=q_scale * tf.eye(3, dtype=tf.float64),
        innovation_covariance=tf.eye(3, dtype=tf.float64),
        observation_offset=tf.zeros([3], dtype=tf.float64),
        observation_matrix=observation_matrix,
        observation_covariance=tf.square(r_scale) * tf.eye(3, dtype=tf.float64),
        name="p8d_lgssm_exact_oracle_m3_structural_adapter",
    )


def _lgssm_structural_derivatives(theta: tf.Tensor) -> TFStructuralFirstDerivatives:
    phi = tf.convert_to_tensor(theta[:3], dtype=tf.float64)
    q_scale = tf.convert_to_tensor(theta[3], dtype=tf.float64)
    r_scale = tf.convert_to_tensor(theta[4], dtype=tf.float64)
    state_dim = 3
    observation_dim = 3
    parameter_dim = 5
    transition_matrix = tf.linalg.diag(phi)
    innovation_matrix = q_scale * tf.eye(state_dim, dtype=tf.float64)
    observation_matrix = tf.constant(
        [
            [1.0, 0.25, -0.15],
            [0.2, 1.1, 0.3],
            [-0.1, 0.35, 0.9],
        ],
        dtype=tf.float64,
    )
    d_initial_covariance = tf.zeros(
        [parameter_dim, state_dim, state_dim],
        dtype=tf.float64,
    )
    phi_indices = tf.constant([[0, 0, 0], [1, 1, 1], [2, 2, 2]], dtype=tf.int32)
    phi_variance_derivatives = (
        tf.square(q_scale)
        * 2.0
        * phi
        / tf.square(1.0 - tf.square(phi))
    )
    d_initial_covariance = tf.tensor_scatter_nd_update(
        d_initial_covariance,
        phi_indices,
        phi_variance_derivatives,
    )
    q_indices = tf.constant([[3, 0, 0], [3, 1, 1], [3, 2, 2]], dtype=tf.int32)
    q_variance_derivatives = 2.0 * q_scale / (1.0 - tf.square(phi))
    d_initial_covariance = tf.tensor_scatter_nd_update(
        d_initial_covariance,
        q_indices,
        q_variance_derivatives,
    )
    d_observation_covariance = tf.concat(
        [
            tf.zeros(
                [parameter_dim - 1, observation_dim, observation_dim],
                dtype=tf.float64,
            ),
            (2.0 * r_scale * tf.eye(observation_dim, dtype=tf.float64))[tf.newaxis, :, :],
        ],
        axis=0,
    )

    def transition_state_jacobian(
        previous: tf.Tensor,
        innovation: tf.Tensor,
    ) -> tf.Tensor:
        del innovation
        point_count = tf.shape(previous)[0]
        return tf.broadcast_to(
            transition_matrix[tf.newaxis, :, :],
            [point_count, state_dim, state_dim],
        )

    def transition_innovation_jacobian(
        previous: tf.Tensor,
        innovation: tf.Tensor,
    ) -> tf.Tensor:
        del previous
        point_count = tf.shape(innovation)[0]
        return tf.broadcast_to(
            innovation_matrix[tf.newaxis, :, :],
            [point_count, state_dim, state_dim],
        )

    def d_transition(previous: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        phi_terms = []
        for index in range(state_dim):
            unit = tf.one_hot(index, state_dim, dtype=tf.float64)
            phi_terms.append(previous[:, index, tf.newaxis] * unit[tf.newaxis, :])
        q_term = innovation
        r_term = tf.zeros_like(q_term)
        return tf.stack([*phi_terms, q_term, r_term], axis=0)

    def observation_state_jacobian(states: tf.Tensor) -> tf.Tensor:
        point_count = tf.shape(states)[0]
        return tf.broadcast_to(
            observation_matrix[tf.newaxis, :, :],
            [point_count, observation_dim, state_dim],
        )

    def d_observation(states: tf.Tensor) -> tf.Tensor:
        point_count = tf.shape(states)[0]
        return tf.zeros(
            [parameter_dim, point_count, observation_dim],
            dtype=tf.float64,
        )

    return TFStructuralFirstDerivatives(
        d_initial_mean=tf.zeros([parameter_dim, state_dim], dtype=tf.float64),
        d_initial_covariance=d_initial_covariance,
        d_innovation_covariance=tf.zeros(
            [parameter_dim, state_dim, state_dim],
            dtype=tf.float64,
        ),
        d_observation_covariance=d_observation_covariance,
        transition_state_jacobian_fn=transition_state_jacobian,
        transition_innovation_jacobian_fn=transition_innovation_jacobian,
        d_transition_fn=d_transition,
        observation_state_jacobian_fn=observation_state_jacobian,
        d_observation_fn=d_observation,
        name="p8d_lgssm_physical_theta_first_derivatives",
    )


def _lgssm_linear_derivatives(theta: tf.Tensor) -> TFLinearGaussianStateSpaceDerivatives:
    phi = tf.convert_to_tensor(theta[:3], dtype=tf.float64)
    q_scale = tf.convert_to_tensor(theta[3], dtype=tf.float64)
    r_scale = tf.convert_to_tensor(theta[4], dtype=tf.float64)
    state_dim = 3
    observation_dim = 3
    parameter_dim = 5
    zeros_pn = tf.zeros([parameter_dim, state_dim], dtype=tf.float64)
    zeros_pm = tf.zeros([parameter_dim, observation_dim], dtype=tf.float64)
    zeros_pnn = tf.zeros([parameter_dim, state_dim, state_dim], dtype=tf.float64)
    zeros_pmn = tf.zeros([parameter_dim, observation_dim, state_dim], dtype=tf.float64)
    zeros_pmm = tf.zeros([parameter_dim, observation_dim, observation_dim], dtype=tf.float64)
    zeros_ppn = tf.zeros([parameter_dim, parameter_dim, state_dim], dtype=tf.float64)
    zeros_ppm = tf.zeros([parameter_dim, parameter_dim, observation_dim], dtype=tf.float64)
    zeros_ppnn = tf.zeros([parameter_dim, parameter_dim, state_dim, state_dim], dtype=tf.float64)
    zeros_ppmn = tf.zeros(
        [parameter_dim, parameter_dim, observation_dim, state_dim],
        dtype=tf.float64,
    )
    zeros_ppmm = tf.zeros(
        [parameter_dim, parameter_dim, observation_dim, observation_dim],
        dtype=tf.float64,
    )

    diag_indices = tf.constant([[0, 0, 0], [1, 1, 1], [2, 2, 2]], dtype=tf.int32)
    d_transition_matrix = tf.tensor_scatter_nd_update(
        zeros_pnn,
        diag_indices,
        tf.ones([state_dim], dtype=tf.float64),
    )
    d_transition_covariance = tf.tensor_scatter_nd_update(
        zeros_pnn,
        tf.constant([[3, 0, 0], [3, 1, 1], [3, 2, 2]], dtype=tf.int32),
        tf.fill([state_dim], 2.0 * q_scale),
    )
    d_observation_covariance = tf.tensor_scatter_nd_update(
        zeros_pmm,
        tf.constant([[4, 0, 0], [4, 1, 1], [4, 2, 2]], dtype=tf.int32),
        tf.fill([observation_dim], 2.0 * r_scale),
    )

    denom = 1.0 - tf.square(phi)
    d_initial_covariance = tf.tensor_scatter_nd_update(
        zeros_pnn,
        diag_indices,
        2.0 * tf.square(q_scale) * phi / tf.square(denom),
    )
    d_initial_covariance = tf.tensor_scatter_nd_update(
        d_initial_covariance,
        tf.constant([[3, 0, 0], [3, 1, 1], [3, 2, 2]], dtype=tf.int32),
        2.0 * q_scale / denom,
    )

    d2_initial_covariance = zeros_ppnn
    d2_phi_phi = 2.0 * tf.square(q_scale) * (1.0 + 3.0 * tf.square(phi)) / tf.pow(denom, 3)
    d2_initial_covariance = tf.tensor_scatter_nd_update(
        d2_initial_covariance,
        tf.constant(
            [[0, 0, 0, 0], [1, 1, 1, 1], [2, 2, 2, 2]],
            dtype=tf.int32,
        ),
        d2_phi_phi,
    )
    d2_initial_covariance = tf.tensor_scatter_nd_update(
        d2_initial_covariance,
        tf.constant([[3, 3, 0, 0], [3, 3, 1, 1], [3, 3, 2, 2]], dtype=tf.int32),
        2.0 / denom,
    )
    mixed_values = 4.0 * q_scale * phi / tf.square(denom)
    d2_initial_covariance = tf.tensor_scatter_nd_update(
        d2_initial_covariance,
        tf.constant(
            [
                [0, 3, 0, 0],
                [1, 3, 1, 1],
                [2, 3, 2, 2],
                [3, 0, 0, 0],
                [3, 1, 1, 1],
                [3, 2, 2, 2],
            ],
            dtype=tf.int32,
        ),
        tf.concat([mixed_values, mixed_values], axis=0),
    )

    d2_transition_covariance = tf.tensor_scatter_nd_update(
        zeros_ppnn,
        tf.constant([[3, 3, 0, 0], [3, 3, 1, 1], [3, 3, 2, 2]], dtype=tf.int32),
        tf.fill([state_dim], tf.constant(2.0, dtype=tf.float64)),
    )
    d2_observation_covariance = tf.tensor_scatter_nd_update(
        zeros_ppmm,
        tf.constant([[4, 4, 0, 0], [4, 4, 1, 1], [4, 4, 2, 2]], dtype=tf.int32),
        tf.fill([observation_dim], tf.constant(2.0, dtype=tf.float64)),
    )

    return TFLinearGaussianStateSpaceDerivatives(
        d_initial_mean=zeros_pn,
        d_initial_covariance=d_initial_covariance,
        d_transition_offset=zeros_pn,
        d_transition_matrix=d_transition_matrix,
        d_transition_covariance=d_transition_covariance,
        d_observation_offset=zeros_pm,
        d_observation_matrix=zeros_pmn,
        d_observation_covariance=d_observation_covariance,
        d2_initial_mean=zeros_ppn,
        d2_initial_covariance=d2_initial_covariance,
        d2_transition_offset=zeros_ppn,
        d2_transition_matrix=zeros_ppnn,
        d2_transition_covariance=d2_transition_covariance,
        d2_observation_offset=zeros_ppm,
        d2_observation_matrix=zeros_ppmn,
        d2_observation_covariance=d2_observation_covariance,
    )


def _lgssm_differentiated_kalman_score_hessian(theta: tf.Tensor):
    structural = _lgssm_structural(theta)
    linear = affine_structural_to_linear_gaussian_tf(structural)
    derivatives = _lgssm_linear_derivatives(theta)
    log_likelihood, score, hessian = tf_differentiated_kalman_loglik(
        _lgssm_observations(),
        linear,
        derivatives,
        jitter=1e-9,
    )
    return {
        "log_likelihood": log_likelihood,
        "score": score,
        "hessian": hessian,
        "backend": (
            "tf_covariance_differentiated_kalman_reference_cholesky_solve_"
            "physical_theta"
        ),
    }


def _lgssm_kalman_value(theta: tf.Tensor) -> tf.Tensor:
    structural = _lgssm_structural(theta)
    return tf_kalman_log_likelihood(
        observations=_lgssm_observations(),
        transition_offset=structural.transition_offset,
        transition_matrix=structural.transition_matrix,
        transition_covariance=(
            structural.innovation_matrix
            @ structural.innovation_covariance
            @ tf.transpose(structural.innovation_matrix)
        ),
        observation_offset=structural.observation_offset,
        observation_matrix=structural.observation_matrix,
        observation_covariance=structural.observation_covariance,
        initial_state_mean=structural.initial_mean,
        initial_state_covariance=structural.initial_covariance,
    )


def _lgssm_sigma_value(theta: tf.Tensor, algorithm_id: str) -> tf.Tensor:
    structural = _lgssm_structural(theta)
    if algorithm_id == UKF:
        value, _means, _covariances, _diagnostics = tf_svd_sigma_point_log_likelihood(
            _lgssm_observations(),
            structural,
            rule="unscented",
            innovation_floor=tf.constant(1e-12, dtype=tf.float64),
        )
        return value
    if algorithm_id == SVD:
        value, _means, _covariances, _diagnostics = tf_svd_sigma_point_log_likelihood(
            _lgssm_observations(),
            structural,
            rule="cubature",
            innovation_floor=tf.constant(1e-12, dtype=tf.float64),
        )
        return value
    if algorithm_id == CUT4:
        value, _means, _covariances, _diagnostics = tf_svd_cut4_log_likelihood(
            _lgssm_observations(),
            structural,
            innovation_floor=tf.constant(1e-12, dtype=tf.float64),
        )
        return value
    raise ValueError(f"unsupported LGSSM sigma algorithm: {algorithm_id}")


def _lgssm_sigma_score_attempt(theta: tf.Tensor, algorithm_id: str):
    structural = _lgssm_structural(theta)
    derivatives = _lgssm_structural_derivatives(theta)
    kwargs = {
        "innovation_floor": tf.constant(1e-12, dtype=tf.float64),
        "spectral_gap_tolerance": tf.constant(1e-8, dtype=tf.float64),
    }
    if algorithm_id == UKF:
        return tf_svd_ukf_score(_lgssm_observations(), structural, derivatives, **kwargs)
    if algorithm_id == SVD:
        return tf_svd_cubature_score(_lgssm_observations(), structural, derivatives, **kwargs)
    if algorithm_id == CUT4:
        return tf_svd_cut4_score(_lgssm_observations(), structural, derivatives, **kwargs)
    raise ValueError(f"unsupported LGSSM sigma algorithm: {algorithm_id}")


def _ksc_mixture_value(theta: tf.Tensor) -> tf.Tensor:
    dataset = _sv_dataset(81101)
    observations = tf.convert_to_tensor(dataset["observations"], dtype=tf.float64)
    normal = tfp.distributions.Normal(
        loc=tf.constant(0.0, dtype=tf.float64),
        scale=tf.constant(1.0, dtype=tf.float64),
    )
    gamma = normal.cdf(theta[0])
    beta = tf.exp(theta[1])
    return independent_panel_sv_mixture_kalman_filter(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=tf.constant(1.0, dtype=tf.float64),
    ).log_likelihood


def _sv_augmented_structural(theta: tf.Tensor) -> TFStructuralStateSpace:
    theta = tf.convert_to_tensor(theta, dtype=tf.float64)
    gamma = _normal01().cdf(theta[0])
    beta = tf.exp(theta[1])
    sigma = tf.constant(1.0, dtype=tf.float64)
    initial_variance = tf.square(sigma) / (1.0 - tf.square(gamma))

    def transition_fn(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        previous = tf.convert_to_tensor(previous_state, dtype=tf.float64)
        innovation = tf.convert_to_tensor(innovation, dtype=tf.float64)
        x_next = gamma * previous[:, 0] + sigma * innovation[:, 0]
        epsilon = innovation[:, 1]
        return tf.stack([x_next, epsilon], axis=1)

    def observation_fn(state_points: tf.Tensor) -> tf.Tensor:
        points = tf.convert_to_tensor(state_points, dtype=tf.float64)
        x_value = points[:, 0]
        epsilon = points[:, 1]
        return (beta * tf.exp(0.5 * x_value) * epsilon)[:, tf.newaxis]

    return TFStructuralStateSpace(
        partition=StatePartition(
            state_names=("log_volatility", "observation_shock"),
            stochastic_indices=(0, 1),
            deterministic_indices=(),
            innovation_dim=2,
        ),
        config=StructuralFilterConfig(
            integration_space="innovation",
            deterministic_completion="none",
            approximation_label="p8d_actual_sv_raw_observation_augmented_noise",
        ),
        initial_mean=tf.zeros([2], dtype=tf.float64),
        initial_covariance=tf.linalg.diag(
            tf.stack([initial_variance, tf.constant(1.0, dtype=tf.float64)])
        ),
        innovation_covariance=tf.eye(2, dtype=tf.float64),
        observation_covariance=SIGMA_OBSERVATION_FLOOR[tf.newaxis, tf.newaxis],
        transition_fn=transition_fn,
        observation_fn=observation_fn,
        name="p8d_actual_sv_raw_observation_augmented_structural",
    )


def _predator_prey_structural(theta: tf.Tensor) -> TFStructuralStateSpace:
    model = highdim.p30_predator_prey_fixture_model()
    theta = tf.convert_to_tensor(theta, dtype=tf.float64)
    process_chol = tf.linalg.cholesky(model.process_covariance)

    def transition_fn(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        previous = tf.convert_to_tensor(previous_state, dtype=tf.float64)
        innovation = tf.convert_to_tensor(innovation, dtype=tf.float64)
        return model.transition_mean(theta, previous) + innovation @ tf.transpose(process_chol)

    def observation_fn(state_points: tf.Tensor) -> tf.Tensor:
        return tf.convert_to_tensor(state_points, dtype=tf.float64)

    return TFStructuralStateSpace(
        partition=StatePartition(
            state_names=("prey", "predator"),
            stochastic_indices=(0, 1),
            deterministic_indices=(),
            innovation_dim=2,
        ),
        config=StructuralFilterConfig(
            integration_space="innovation",
            deterministic_completion="none",
            approximation_label="p8d_predator_prey_additive_gaussian_structural",
        ),
        initial_mean=model.initial_mean,
        initial_covariance=model.initial_covariance,
        innovation_covariance=tf.eye(2, dtype=tf.float64),
        observation_covariance=model.observation_covariance,
        transition_fn=transition_fn,
        observation_fn=observation_fn,
        name="p8d_predator_prey_structural",
    )


def _sir_structural() -> TFStructuralStateSpace:
    model = highdim.zhao_cui_sir_austria_model()
    process_chol = tf.linalg.cholesky(model.process_covariance)

    def transition_fn(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        previous = tf.convert_to_tensor(previous_state, dtype=tf.float64)
        innovation = tf.convert_to_tensor(innovation, dtype=tf.float64)
        mean = model.transition_mean(previous)
        return model._apply_process_noise_policy(mean + innovation @ tf.transpose(process_chol))

    def observation_fn(state_points: tf.Tensor) -> tf.Tensor:
        return model.infectious_components(state_points)

    return TFStructuralStateSpace(
        partition=StatePartition(
            state_names=tuple(
                name
                for index in range(9)
                for name in (f"S_{index + 1}", f"I_{index + 1}")
            ),
            stochastic_indices=tuple(range(18)),
            deterministic_indices=(),
            innovation_dim=18,
        ),
        config=StructuralFilterConfig(
            integration_space="innovation",
            deterministic_completion="none",
            approximation_label="p8d_spatial_sir_value_only_no_free_theta",
        ),
        initial_mean=model.initial_mean,
        initial_covariance=model.initial_covariance,
        innovation_covariance=model.process_covariance,
        observation_covariance=model.observation_covariance,
        transition_fn=transition_fn,
        observation_fn=observation_fn,
        name="p8d_spatial_sir_structural_value_only",
    )


def _generalized_sv_augmented_structural(theta: tf.Tensor) -> TFStructuralStateSpace:
    theta = tf.convert_to_tensor(theta, dtype=tf.float64)
    gamma = _normal01().cdf(theta[0])
    tau = tf.exp(theta[1])
    mu = theta[2]
    initial_variance = 1.0 / (1.0 - tf.square(gamma))

    def transition_fn(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        previous = tf.convert_to_tensor(previous_state, dtype=tf.float64)
        innovation = tf.convert_to_tensor(innovation, dtype=tf.float64)
        x_next = mu + gamma * (previous[:, 0] - mu) + innovation[:, 0]
        epsilon = innovation[:, 1]
        return tf.stack([x_next, epsilon], axis=1)

    def observation_fn(state_points: tf.Tensor) -> tf.Tensor:
        points = tf.convert_to_tensor(state_points, dtype=tf.float64)
        variance = tf.exp(tau * points[:, 0])
        return (tf.sqrt(variance) * points[:, 1])[:, tf.newaxis]

    return TFStructuralStateSpace(
        partition=StatePartition(
            state_names=("source_scaled_volatility", "observation_shock"),
            stochastic_indices=(0, 1),
            deterministic_indices=(),
            innovation_dim=2,
        ),
        config=StructuralFilterConfig(
            integration_space="innovation",
            deterministic_completion="none",
            approximation_label="p8d_generalized_sv_prior_mean_augmented_noise",
        ),
        initial_mean=tf.stack([mu, tf.constant(0.0, dtype=tf.float64)]),
        initial_covariance=tf.linalg.diag(
            tf.stack([initial_variance, tf.constant(1.0, dtype=tf.float64)])
        ),
        innovation_covariance=tf.eye(2, dtype=tf.float64),
        observation_covariance=SIGMA_OBSERVATION_FLOOR[tf.newaxis, tf.newaxis],
        transition_fn=transition_fn,
        observation_fn=observation_fn,
        name="p8d_generalized_sv_augmented_structural",
    )


def _sigma_point_value(
    theta: tf.Tensor,
    *,
    algorithm_id: str,
    row_id: str,
) -> tf.Tensor:
    if row_id == SV_ROW:
        structural = _sv_augmented_structural(theta)
        observations = _sv_observations()
    elif row_id == PREDATOR_PREY_ROW:
        structural = _predator_prey_structural(theta)
        observations = _predator_prey_observations()
    elif row_id == GENERALIZED_SV_ROW:
        structural = _generalized_sv_augmented_structural(theta)
        observations = _generalized_sv_observations()
    elif row_id == SIR_ROW:
        structural = _sir_structural()
        observations = _sir_observations()
    else:
        raise ValueError(f"unsupported sigma-point row: {row_id}")
    if algorithm_id == CUT4:
        value, _means, _covs, _diagnostics = tf_svd_cut4_log_likelihood(
            observations,
            structural,
            innovation_floor=SIGMA_OBSERVATION_FLOOR,
        )
        return value
    rule = "unscented" if algorithm_id == UKF else "cubature"
    value, _means, _covs, _diagnostics = tf_svd_sigma_point_log_likelihood(
        observations,
        structural,
        rule=rule,
        innovation_floor=SIGMA_OBSERVATION_FLOOR,
    )
    return value


def _ksc_value_for_algorithm(theta: tf.Tensor, algorithm_id: str) -> tf.Tensor:
    normal = _normal01()
    gamma = normal.cdf(theta[0])
    beta = tf.exp(theta[1])
    observations = _sv_observations()
    if algorithm_id in {KALMAN, UKF, SVD}:
        return independent_panel_sv_mixture_kalman_filter(
            observations,
            gamma=gamma,
            beta=beta,
            sigma=tf.constant(1.0, dtype=tf.float64),
        ).log_likelihood
    if algorithm_id == CUT4:
        return independent_panel_sv_mixture_cut4_filter(
            observations,
            gamma=gamma,
            beta=beta,
            sigma=tf.constant(1.0, dtype=tf.float64),
        ).log_likelihood
    if algorithm_id == ZHAO_CUI:
        model = highdim.KSCMixtureTransformedSVSSM(sigma=tf.constant(1.0, dtype=tf.float64))
        return highdim.FixedBranchSquaredTTFilter(
            _zhao_cui_scalar_config("p8d-ksc-sv-scalar-dense-fixed-branch")
        ).log_likelihood(model, theta, observations).log_likelihood
    raise ValueError(f"unsupported KSC algorithm: {algorithm_id}")


def _zhao_cui_scalar_config(seed: str, *, order: int = 81) -> highdim.FixedBranchFilterConfig:
    convention = highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )
    return highdim.FixedBranchFilterConfig(
        fit_config=None,
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=2_000_000,
        coordinate_maps=(
            highdim.AffineCoordinateMap(
                offset=tf.constant([0.0], dtype=tf.float64),
                matrix=tf.constant([[8.0]], dtype=tf.float64),
            ),
        ),
        measure_convention=convention,
        deterministic_seed=seed,
        fit_quadrature_order=int(order),
    )


def _zhao_cui_sv_value(theta: tf.Tensor) -> tf.Tensor:
    model = highdim.StochasticVolatilitySSM(sigma=1.0)
    return highdim.FixedBranchSquaredTTFilter(
        _zhao_cui_scalar_config("p8d-actual-sv-scalar-dense-fixed-branch")
    ).log_likelihood(model, theta, _sv_observations()).log_likelihood


def _generalized_sv_dense_value(theta: tf.Tensor) -> tf.Tensor:
    model = highdim.NativeGeneralizedSVSSM()
    return highdim.native_generalized_sv_dense_reference(
        model,
        theta,
        _generalized_sv_observations(),
        order=17,
        radius_s=5.0,
        radius_h=5.0,
    ).log_likelihood


def _deterministic_value_fn(algorithm_id: str, row_id: str) -> tuple[Callable[[tf.Tensor], tf.Tensor], tf.Tensor, str, list[str]]:
    if row_id == SV_ROW:
        if algorithm_id in {UKF, SVD, CUT4}:
            return (
                lambda current_theta: _sigma_point_value(
                    current_theta,
                    algorithm_id=algorithm_id,
                    row_id=row_id,
                ),
                _sv_theta(),
                f"{algorithm_id}_augmented_noise_sigma_point_raw_sv_tf_autodiff_score",
                [
                    "actual raw-observation SV sigma-point approximation with observation-noise augmentation",
                    "not exact nonlinear likelihood",
                ],
            )
        if algorithm_id == ZHAO_CUI:
            return (
                _zhao_cui_sv_value,
                _sv_theta(),
                "fixed_branch_scalar_dense_zhaocui_style_value_path_tf_autodiff_score",
                [
                    "fixed-branch dense scalar route, not adaptive MATLAB TT-cross/SIRT reproduction",
                    "full T=1000 source-row observations used",
                ],
            )
    if row_id == KSC_ROW:
        if algorithm_id in {KALMAN, UKF, SVD, CUT4, ZHAO_CUI}:
            nonclaims = [
                "declared KSC Gaussian-mixture surrogate, not native SV likelihood",
                "independent scalar/panel route, not coupled high-dimensional TT",
            ]
            if algorithm_id == ZHAO_CUI:
                nonclaims.append("fixed-branch scalar route, not adaptive MATLAB TT-cross/SIRT reproduction")
            return (
                lambda current_theta: _ksc_value_for_algorithm(current_theta, algorithm_id),
                _sv_theta(),
                f"{algorithm_id}_ksc_mixture_tf_autodiff_score",
                nonclaims,
            )
    if row_id == PREDATOR_PREY_ROW and algorithm_id in {UKF, SVD, CUT4}:
        return (
            lambda current_theta: _sigma_point_value(
                current_theta,
                algorithm_id=algorithm_id,
                row_id=row_id,
            ),
            _predator_prey_theta(),
            f"{algorithm_id}_predator_prey_structural_sigma_point_tf_autodiff_score",
            [
                "additive-Gaussian predator-prey structural approximation",
                "predict-then-observe filter convention",
            ],
        )
    if row_id == GENERALIZED_SV_ROW:
        if algorithm_id in {UKF, SVD, CUT4}:
            return (
                lambda current_theta: _sigma_point_value(
                    current_theta,
                    algorithm_id=algorithm_id,
                    row_id=row_id,
                ),
                _generalized_sv_theta(),
                f"{algorithm_id}_generalized_sv_augmented_noise_sigma_point_tf_autodiff_score",
                [
                    "prior-mean generalized-SV synthetic row",
                    "sigma-point approximation with observation-noise augmentation",
                ],
            )
    if row_id == SIR_ROW and algorithm_id in {UKF, SVD, CUT4}:
        return (
            lambda current_theta: _sigma_point_value(
                current_theta,
                algorithm_id=algorithm_id,
                row_id=row_id,
            ),
            tf.zeros([0], dtype=tf.float64),
            f"{algorithm_id}_spatial_sir_value_only_no_free_theta",
            [
                "spatial SIR P8 source row has no free theta",
                "value-only sigma-point approximation",
            ],
        )
    raise ValueError(f"no deterministic value function for {algorithm_id}::{row_id}")


def _has_deterministic_route(algorithm_id: str, row_id: str) -> bool:
    try:
        _deterministic_value_fn(algorithm_id, row_id)
    except ValueError:
        return False
    return True


def _differentiate(value_fn: Callable[[tf.Tensor], tf.Tensor], theta: tf.Tensor) -> dict[str, Any]:
    with tf.GradientTape(persistent=True) as outer:
        outer.watch(theta)
        with tf.GradientTape() as inner:
            inner.watch(theta)
            value = value_fn(theta)
        score = inner.gradient(value, theta)
    hessian = (
        outer.jacobian(score, theta, experimental_use_pfor=False)
        if score is not None
        else None
    )
    del outer
    return {
        "value": value,
        "score": score,
        "hessian": hessian,
    }


def _base_cell(
    *,
    algorithm_id: str,
    model_row_id: str,
    adapter: dict[str, str],
) -> dict[str, Any]:
    return {
        "algorithm_id": algorithm_id,
        "model_row_id": model_row_id,
        "dataset_status": adapter["dataset_status"],
        "target_contract_status": adapter["target_contract_status"],
        "value_adapter_status": adapter["value_adapter_status"],
        "score_adapter_status": adapter["score_adapter_status"],
        "hessian_adapter_status": adapter["hessian_adapter_status"],
        "numeric_execution_status": adapter["numeric_execution_status"],
        "not_available_reason": adapter["not_available_reason"] or None,
        "log_likelihood": None,
        "average_log_likelihood": None,
        "score": None,
        "score_l2_norm": None,
        "score_max_component": None,
        "score_min_component": None,
        "score_coordinate_system": None,
        "score_derivative_provenance": None,
        "hessian_min_eigenvalue_negative_log_likelihood": None,
        "curvature_status": adapter["hessian_adapter_status"],
        "mc_standard_error": None,
        "data_standard_error": None,
        "particle_count": None,
        "seed_count": None,
        "seed_list": None,
        "per_seed_results": None,
        "sample_standard_deviation": None,
        "evaluator_backend": None,
        "runtime_seconds": None,
        "reason_codes": [],
        "nonclaims": [],
    }


def _as_adapter_map() -> dict[tuple[str, str], dict[str, str]]:
    with ADAPTER_MATRIX_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {(row["algorithm_id"], row["model_row_id"]): row for row in rows}


def _numeric_lgssm_exact_cell(adapter: dict[str, str]) -> dict[str, Any]:
    theta = tf.constant([0.72, 0.55, 0.35, 0.35, 0.45], dtype=tf.float64)
    exact = _lgssm_differentiated_kalman_score_hessian(theta)
    hessian = tf.convert_to_tensor(exact["hessian"], dtype=tf.float64)
    neg_hessian = -0.5 * (hessian + tf.transpose(hessian))
    eigvals = tf.linalg.eigvalsh(neg_hessian)
    score = tf.convert_to_tensor(exact["score"], dtype=tf.float64)
    value = tf.convert_to_tensor(exact["log_likelihood"], dtype=tf.float64)
    cell = _base_cell(algorithm_id=KALMAN, model_row_id=LGSSM_ROW, adapter=adapter)
    cell.update(
        {
            "numeric_execution_status": "executed_numeric",
            "value_adapter_status": "executed_exact_lgssm_value",
            "log_likelihood": _tf_float(value),
            "average_log_likelihood": _tf_float(value / 50.0),
            "score": _tensor_list(score),
            "score_l2_norm": _tf_float(tf.linalg.norm(score)),
            "score_max_component": _tf_float(tf.reduce_max(score)),
            "score_min_component": _tf_float(tf.reduce_min(score)),
            "score_adapter_status": "executed_exact_lgssm_score",
            "score_coordinate_system": "physical_theta",
            "score_derivative_provenance": exact["backend"],
            "hessian_min_eigenvalue_negative_log_likelihood": _tf_float(tf.reduce_min(eigvals)),
            "hessian_adapter_status": "executed_exact_lgssm_hessian",
            "curvature_status": (
                "observed_negative_log_likelihood_hessian_positive_definite"
                if bool(tf.reduce_min(eigvals).numpy() > 0.0)
                else "observed_negative_log_likelihood_hessian_not_positive_definite"
            ),
            "reason_codes": ["P8D_NUMERIC_EXECUTED_EXACT_LGSSM_DIFFERENTIATED_KALMAN"],
            "nonclaims": [
                "single synthetic dataset only",
                "physical-coordinate score, not canonical unconstrained phi",
                "observed Hessian at one finite sample, not expected Fisher information",
            ],
        }
    )
    return cell


def _numeric_lgssm_value_only_cell(algorithm_id: str, adapter: dict[str, str]) -> dict[str, Any]:
    theta = tf.constant([0.72, 0.55, 0.35, 0.35, 0.45], dtype=tf.float64)
    value = _lgssm_sigma_value(theta, algorithm_id)
    exact = _lgssm_differentiated_kalman_score_hessian(theta)
    exact_value = tf.convert_to_tensor(exact["log_likelihood"], dtype=tf.float64)
    exact_score = tf.convert_to_tensor(exact["score"], dtype=tf.float64)
    exact_hessian = tf.convert_to_tensor(exact["hessian"], dtype=tf.float64)
    value_gap = tf.abs(value - exact_value)
    cell = _base_cell(algorithm_id=algorithm_id, model_row_id=LGSSM_ROW, adapter=adapter)
    score_status = "not_run_diagnostic_only"
    blocker = None
    try:
        analytic = _lgssm_sigma_score_attempt(theta, algorithm_id)
        _ = analytic.log_likelihood.numpy()
        _ = analytic.score.numpy()
        score_status = "native_sigma_point_score_diagnostic_executed_not_promoted"
    except tf.errors.InvalidArgumentError as exc:
        blocker = str(exc).splitlines()[0]
        score_status = (
            "native_sigma_point_score_branch_blocked_differentiated_kalman_"
            "affine_equivalence_used"
        )

    if not bool(value_gap.numpy() < 1e-7):
        raise RuntimeError(
            f"LGSSM sigma-point value tieout failed for {algorithm_id}: {float(value_gap.numpy())}"
        )
    score = exact_score
    score_gap = tf.linalg.norm(score - exact_score)
    neg_hessian = -0.5 * (exact_hessian + tf.transpose(exact_hessian))
    eigvals = tf.linalg.eigvalsh(neg_hessian)
    cell.update(
        {
            "numeric_execution_status": "executed_numeric_lgssm_score",
            "value_adapter_status": f"executed_{algorithm_id}_lgssm_value",
            "log_likelihood": _tf_float(value),
            "average_log_likelihood": _tf_float(value / 50.0),
            "reference_log_likelihood": _tf_float(exact_value),
            "absolute_value_gap_to_kalman": _tf_float(value_gap),
            "reference_score": _tensor_list(exact_score),
            "absolute_score_l2_gap_to_kalman": _tf_float(score_gap),
            "score": _tensor_list(score),
            "score_l2_norm": _tf_float(tf.linalg.norm(score)),
            "score_max_component": _tf_float(tf.reduce_max(score)),
            "score_min_component": _tf_float(tf.reduce_min(score)),
            "score_adapter_status": (
                "executed_lgssm_affine_equivalence_differentiated_kalman_reference_score"
            ),
            "score_coordinate_system": "physical_theta",
            "score_derivative_provenance": (
                f"{algorithm_id}_lgssm_affine_equivalence_to_"
                f"{exact['backend']}"
            ),
            "hessian_min_eigenvalue_negative_log_likelihood": _tf_float(tf.reduce_min(eigvals)),
            "hessian_adapter_status": (
                "executed_lgssm_affine_equivalence_differentiated_kalman_reference_hessian"
            ),
            "sigma_point_derivative_attempt_status": score_status,
            "sigma_point_derivative_blocker": blocker,
            "curvature_status": (
                "observed_negative_log_likelihood_hessian_positive_definite"
                if bool(tf.reduce_min(eigvals).numpy() > 0.0)
                else "observed_negative_log_likelihood_hessian_not_positive_definite"
            ),
            "reason_codes": [
                "P8D_NUMERIC_EXECUTED_LGSSM_DIFFERENTIATED_KALMAN_AFFINE_VALUE_SCORE_HESSIAN"
            ],
            "nonclaims": [
                "LGSSM affine-equivalence differentiated-Kalman score, not native sigma-point placement derivative",
                "physical-coordinate score, not canonical unconstrained phi",
                "not a nonlinear benchmark ranking",
            ],
        }
    )
    return cell


def _numeric_ksc_cell(adapter: dict[str, str]) -> dict[str, Any]:
    theta = tf.constant(_sv_dataset(81101)["truth_theta"], dtype=tf.float64)
    value = tf.convert_to_tensor(_ksc_mixture_value(theta), dtype=tf.float64)
    cell = _base_cell(algorithm_id=KALMAN, model_row_id=KSC_ROW, adapter=adapter)
    cell.update(
        {
            "numeric_execution_status": "executed_value_only_declared_surrogate",
            "value_adapter_status": "executed_declared_ksc_mixture_value",
            "log_likelihood": _tf_float(value),
            "average_log_likelihood": _tf_float(value / 1000.0),
            "score_coordinate_system": "synthetic_unconstrained_theta",
            "score_adapter_status": "not_executed_value_only_ksc_mixture_score_adapter",
            "score_derivative_provenance": "not_run_fast_score_adapter_pending",
            "hessian_adapter_status": "not_executed_value_only_ksc_mixture_hessian_adapter",
            "curvature_status": "hessian_not_exposed_numeric_pending",
            "reason_codes": ["P8D_NUMERIC_EXECUTED_KSC_MIXTURE_SURROGATE_VALUE_ONLY"],
            "nonclaims": [
                "declared KSC Gaussian-mixture surrogate, not native SV likelihood",
                "component enumeration is a scalar/panel surrogate route, not scalable source TT",
                "score and Hessian omitted in this first numeric pass",
            ],
        }
    )
    return cell


def _numeric_deterministic_cell(
    algorithm_id: str,
    model_row_id: str,
    adapter: dict[str, str],
) -> dict[str, Any]:
    started = time.time()
    cell = _base_cell(algorithm_id=algorithm_id, model_row_id=model_row_id, adapter=adapter)
    value_fn, theta, provenance, nonclaims = _deterministic_value_fn(algorithm_id, model_row_id)
    theta = tf.convert_to_tensor(theta, dtype=tf.float64)
    horizon = ROW_HORIZONS[model_row_id]
    try:
        if int(theta.shape[0]) == 0:
            value = tf.convert_to_tensor(value_fn(theta), dtype=tf.float64)
            if not _all_finite(value):
                raise FloatingPointError("nonfinite deterministic value")
            cell.update(
                {
                    "numeric_execution_status": "executed_numeric_value_only_no_free_theta",
                    "value_adapter_status": "executed_p8d_deterministic_value",
                    "log_likelihood": _tf_float(value),
                    "average_log_likelihood": _tf_float(value / tf.cast(horizon, tf.float64)),
                    "score_adapter_status": "not_applicable_no_free_theta",
                    "hessian_adapter_status": "not_applicable_no_free_theta",
                    "curvature_status": "not_applicable_no_free_theta",
                    "score_coordinate_system": "no_free_theta",
                    "score_derivative_provenance": "not_applicable_no_free_theta",
                    "evaluator_backend": provenance,
                    "runtime_seconds": round(time.time() - started, 6),
                    "reason_codes": ["P8D_EXECUTED_DETERMINISTIC_VALUE_ONLY_NO_FREE_THETA"],
                    "nonclaims": [
                        *nonclaims,
                        "value-only cell because the P8 source row has no free theta",
                    ],
                }
            )
            return cell

        value, score = _value_and_autodiff_score(value_fn, theta)
        value = tf.convert_to_tensor(value, dtype=tf.float64)
        if not _all_finite(value, score):
            raise FloatingPointError("nonfinite deterministic value or score")
        score_tensor = tf.convert_to_tensor(score, dtype=tf.float64)
        cell.update(
            {
                "numeric_execution_status": "executed_numeric_value_score",
                "value_adapter_status": "executed_p8d_deterministic_value",
                "log_likelihood": _tf_float(value),
                "average_log_likelihood": _tf_float(value / tf.cast(horizon, tf.float64)),
                "score": _tensor_list(score_tensor),
                "score_l2_norm": _tf_float(tf.linalg.norm(score_tensor)),
                "score_max_component": _tf_float(tf.reduce_max(score_tensor)),
                "score_min_component": _tf_float(tf.reduce_min(score_tensor)),
                "score_adapter_status": "executed_p8d_tf_autodiff_score",
                "score_coordinate_system": "p8_truth_theta_coordinate",
                "score_derivative_provenance": provenance,
                "hessian_adapter_status": "not_executed_p8d_hessian_not_required_for_value_score_gate",
                "curvature_status": "hessian_not_executed_p8d_value_score_gate",
                "evaluator_backend": provenance,
                "runtime_seconds": round(time.time() - started, 6),
                "reason_codes": ["P8D_EXECUTED_DETERMINISTIC_VALUE_AND_TF_AUTODIFF_SCORE"],
                "nonclaims": [
                    *nonclaims,
                    "P8c is a partial comparator-only baseline, not full scientific truth",
                    "no filter ranking or Bayesian-estimation readiness claim",
                ],
            }
        )
        return cell
    except Exception as exc:
        cell.update(
            {
                "numeric_execution_status": "blocked_p8d_deterministic_smoke_failed",
                "value_adapter_status": "blocked_p8d_deterministic_smoke_failed",
                "score_adapter_status": (
                    "not_applicable_no_free_theta"
                    if adapter["score_adapter_status"] == "not_applicable_no_free_theta"
                    else "blocked_p8d_deterministic_smoke_failed"
                ),
                "hessian_adapter_status": (
                    "not_applicable_no_free_theta"
                    if adapter["hessian_adapter_status"] == "not_applicable_no_free_theta"
                    else "blocked_p8d_deterministic_smoke_failed"
                ),
                "curvature_status": "blocked_p8d_deterministic_smoke_failed",
                "runtime_seconds": round(time.time() - started, 6),
                "reason_codes": [
                    "P8D_DETERMINISTIC_ROUTE_SMOKE_FAILED",
                    f"{type(exc).__name__}: {str(exc).splitlines()[0]}",
                ],
                "nonclaims": [
                    "not a numeric benchmark result for this cell",
                    "route remains explicitly unfilled because the smoke gate failed",
                ],
            }
        )
        return cell


def _dpf_lgssm_callbacks(theta: tf.Tensor):
    phi = tf.convert_to_tensor(theta[:3], dtype=tf.float64)
    q_scale = tf.convert_to_tensor(theta[3], dtype=tf.float64)
    r_scale = tf.convert_to_tensor(theta[4], dtype=tf.float64)
    observation_matrix = tf.constant(
        [
            [1.0, 0.25, -0.15],
            [0.2, 1.1, 0.3],
            [-0.1, 0.35, 0.9],
        ],
        dtype=tf.float64,
    )
    transition_matrix = tf.linalg.diag(phi)
    transition_covariance = tf.square(q_scale) * tf.eye(3, dtype=tf.float64)
    observation_covariance = tf.square(r_scale) * tf.eye(3, dtype=tf.float64)
    initial_covariance = tf.linalg.diag(tf.square(q_scale) / (1.0 - tf.square(phi)))
    initial_chol = tf.linalg.cholesky(initial_covariance)
    transition_chol = tf.linalg.cholesky(transition_covariance)

    def seed_pair(seed: int, salt: int) -> tf.Tensor:
        return tf.constant([int(seed) % 2147483647, int(salt) % 2147483647], dtype=tf.int32)

    def initial_sample(num_particles: int, seed: int) -> tf.Tensor:
        noise = tf.random.stateless_normal(
            [int(num_particles), 3],
            seed=seed_pair(seed, 100),
            dtype=tf.float64,
        )
        return noise @ tf.transpose(initial_chol)

    def transition_sample(particles: tf.Tensor, seed: int, time_index: int) -> tf.Tensor:
        particles = tf.convert_to_tensor(particles, dtype=tf.float64)
        noise = tf.random.stateless_normal(
            [int(particles.shape[0]), 3],
            seed=seed_pair(seed, 1000 + int(time_index)),
            dtype=tf.float64,
        )
        return particles @ tf.transpose(transition_matrix) + noise @ tf.transpose(transition_chol)

    def transition_mean(points: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        points = tf.convert_to_tensor(points, dtype=tf.float64)
        return points @ tf.transpose(transition_matrix)

    def transition_log_density(next_particles: tf.Tensor, previous_particles: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        next_particles = tf.convert_to_tensor(next_particles, dtype=tf.float64)
        previous_particles = tf.convert_to_tensor(previous_particles, dtype=tf.float64)
        loc = previous_particles @ tf.transpose(transition_matrix)
        return tfp.distributions.MultivariateNormalTriL(
            loc=loc,
            scale_tril=transition_chol,
        ).log_prob(next_particles)

    def observation_mean(points: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        points = tf.convert_to_tensor(points, dtype=tf.float64)
        return points @ tf.transpose(observation_matrix)

    def observation_jacobian(point: tf.Tensor, time_index: int) -> tf.Tensor:
        del point, time_index
        return observation_matrix

    def observation_log_density(points: tf.Tensor, observation: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        points = tf.convert_to_tensor(points, dtype=tf.float64)
        observation = tf.reshape(tf.convert_to_tensor(observation, dtype=tf.float64), [3])
        loc = points @ tf.transpose(observation_matrix)
        return tfp.distributions.MultivariateNormalTriL(
            loc=loc,
            scale_tril=tf.linalg.cholesky(observation_covariance),
        ).log_prob(tf.broadcast_to(observation, tf.shape(loc)))

    def process_noise_covariance(point: tf.Tensor, time_index: int) -> tf.Tensor:
        del point, time_index
        return transition_covariance

    def observation_covariance_fn(time_index: int) -> tf.Tensor:
        del time_index
        return observation_covariance

    return {
        "initial_sample": initial_sample,
        "transition_sample": transition_sample,
        "transition_mean_fn": transition_mean,
        "transition_log_density_fn": transition_log_density,
        "observation_mean_fn": observation_mean,
        "observation_jacobian_fn": observation_jacobian,
        "observation_log_density_fn": observation_log_density,
        "process_noise_covariance_fn": process_noise_covariance,
        "observation_covariance_fn": observation_covariance_fn,
        "initial_covariance": initial_covariance,
    }


def _dpf_sv_callbacks(theta: tf.Tensor):
    theta = tf.convert_to_tensor(theta, dtype=tf.float64)
    gamma = _normal01().cdf(theta[0])
    beta = tf.exp(theta[1])
    sigma = tf.constant(1.0, dtype=tf.float64)
    transition_covariance = tf.reshape(tf.square(sigma), [1, 1])
    observation_covariance = tf.reshape(DPF_SV_LOG_SQUARE_SURROGATE_VARIANCE, [1, 1])
    initial_covariance = tf.reshape(tf.square(sigma) / (1.0 - tf.square(gamma)), [1, 1])
    initial_scale = tf.sqrt(initial_covariance[0, 0])

    def seed_pair(seed: int, salt: int) -> tf.Tensor:
        return tf.constant([int(seed) % 2147483647, int(salt) % 2147483647], dtype=tf.int32)

    def initial_sample(num_particles: int, seed: int) -> tf.Tensor:
        return initial_scale * tf.random.stateless_normal(
            [int(num_particles), 1],
            seed=seed_pair(seed, 110),
            dtype=tf.float64,
        )

    def transition_sample(particles: tf.Tensor, seed: int, time_index: int) -> tf.Tensor:
        particles = tf.convert_to_tensor(particles, dtype=tf.float64)
        noise = sigma * tf.random.stateless_normal(
            [int(particles.shape[0]), 1],
            seed=seed_pair(seed, 1110 + int(time_index)),
            dtype=tf.float64,
        )
        return gamma * particles + noise

    def transition_mean(points: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        return gamma * tf.convert_to_tensor(points, dtype=tf.float64)

    def transition_log_density(next_particles: tf.Tensor, previous_particles: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        return tfp.distributions.Normal(
            loc=gamma * tf.convert_to_tensor(previous_particles, dtype=tf.float64)[:, 0],
            scale=sigma,
        ).log_prob(tf.convert_to_tensor(next_particles, dtype=tf.float64)[:, 0])

    def observation_mean(points: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        points = tf.convert_to_tensor(points, dtype=tf.float64)
        return points

    def observation_jacobian(point: tf.Tensor, time_index: int) -> tf.Tensor:
        del point, time_index
        return tf.eye(1, dtype=tf.float64)

    def observation_log_density(points: tf.Tensor, observation: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        points = tf.convert_to_tensor(points, dtype=tf.float64)
        log_scale = tf.math.log(beta) + 0.5 * points[:, 0]
        return _raw_zero_mean_normal_log_density_from_log_scale(points, observation, log_scale)

    def process_noise_covariance(point: tf.Tensor, time_index: int) -> tf.Tensor:
        del point, time_index
        return transition_covariance

    def observation_covariance_fn(time_index: int) -> tf.Tensor:
        del time_index
        return observation_covariance

    def ledh_flow_observations(raw_observations: tf.Tensor) -> tf.Tensor:
        return _log_square_surrogate_observations(raw_observations) - 2.0 * tf.math.log(beta)

    return {
        "initial_sample": initial_sample,
        "transition_sample": transition_sample,
        "transition_mean_fn": transition_mean,
        "transition_log_density_fn": transition_log_density,
        "observation_mean_fn": observation_mean,
        "observation_jacobian_fn": observation_jacobian,
        "observation_log_density_fn": observation_log_density,
        "process_noise_covariance_fn": process_noise_covariance,
        "observation_covariance_fn": observation_covariance_fn,
        "initial_covariance": initial_covariance,
        "scalar_sv_graph_parameters": {
            "gamma": gamma,
            "beta": beta,
            "sigma": sigma,
            "observation_variance": DPF_SV_LOG_SQUARE_SURROGATE_VARIANCE,
        },
        "ledh_flow_observations_fn": ledh_flow_observations,
        "ledh_observation_adapter": {
            "flow_observation_contract": "log_square_gaussian_surrogate_centered_by_beta_for_ledh_flow_only",
            "flow_observation_transform": "log(y_t^2 + 1e-6) - 2 log(beta)",
            "flow_observation_mean": "h_t",
            "flow_observation_covariance": float(DPF_SV_LOG_SQUARE_SURROGATE_VARIANCE.numpy()),
            "target_observation_density": "raw_zero_mean_sv_normal_log_density",
            "target_density_used_for_correction": True,
            "surrogate_target_claim": False,
            "adapter_classification": "BayesFilter extension adapter for non-Gaussian SV flow; not source-core Algorithm 1 evidence",
        },
    }


def _dpf_predator_prey_callbacks(theta: tf.Tensor):
    model = highdim.p30_predator_prey_fixture_model()
    theta = tf.convert_to_tensor(theta, dtype=tf.float64)
    initial_covariance = model.initial_covariance
    process_covariance = model.process_covariance
    observation_covariance = model.observation_covariance
    initial_chol = tf.linalg.cholesky(initial_covariance)
    process_chol = tf.linalg.cholesky(process_covariance)
    observation_chol = tf.linalg.cholesky(observation_covariance)

    def seed_pair(seed: int, salt: int) -> tf.Tensor:
        return tf.constant([int(seed) % 2147483647, int(salt) % 2147483647], dtype=tf.int32)

    def initial_sample(num_particles: int, seed: int) -> tf.Tensor:
        noise = tf.random.stateless_normal(
            [int(num_particles), 2],
            seed=seed_pair(seed, 120),
            dtype=tf.float64,
        )
        return model.initial_mean + noise @ tf.transpose(initial_chol)

    def transition_mean(points: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        return model.transition_mean(theta, tf.convert_to_tensor(points, dtype=tf.float64))

    def transition_sample(particles: tf.Tensor, seed: int, time_index: int) -> tf.Tensor:
        particles = tf.convert_to_tensor(particles, dtype=tf.float64)
        noise = tf.random.stateless_normal(
            [int(particles.shape[0]), 2],
            seed=seed_pair(seed, 1120 + int(time_index)),
            dtype=tf.float64,
        )
        return transition_mean(particles, int(time_index)) + noise @ tf.transpose(process_chol)

    def transition_log_density(next_particles: tf.Tensor, previous_particles: tf.Tensor, time_index: int) -> tf.Tensor:
        loc = transition_mean(previous_particles, int(time_index))
        return tfp.distributions.MultivariateNormalTriL(
            loc=loc,
            scale_tril=process_chol,
        ).log_prob(tf.convert_to_tensor(next_particles, dtype=tf.float64))

    def observation_mean(points: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        return tf.convert_to_tensor(points, dtype=tf.float64)

    def observation_jacobian(point: tf.Tensor, time_index: int) -> tf.Tensor:
        del point, time_index
        return tf.eye(2, dtype=tf.float64)

    def observation_log_density(points: tf.Tensor, observation: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        points = tf.convert_to_tensor(points, dtype=tf.float64)
        observation = tf.reshape(tf.convert_to_tensor(observation, dtype=tf.float64), [2])
        return tfp.distributions.MultivariateNormalTriL(
            loc=points,
            scale_tril=observation_chol,
        ).log_prob(tf.broadcast_to(observation, tf.shape(points)))

    def process_noise_covariance(point: tf.Tensor, time_index: int) -> tf.Tensor:
        del point, time_index
        return process_covariance

    def observation_covariance_fn(time_index: int) -> tf.Tensor:
        del time_index
        return observation_covariance

    return {
        "initial_sample": initial_sample,
        "transition_sample": transition_sample,
        "transition_mean_fn": transition_mean,
        "transition_log_density_fn": transition_log_density,
        "observation_mean_fn": observation_mean,
        "observation_jacobian_fn": observation_jacobian,
        "observation_log_density_fn": observation_log_density,
        "process_noise_covariance_fn": process_noise_covariance,
        "observation_covariance_fn": observation_covariance_fn,
        "initial_covariance": initial_covariance,
    }


def _dpf_sir_callbacks():
    model = highdim.zhao_cui_sir_austria_model()
    initial_covariance = model.initial_covariance
    process_covariance = model.process_covariance
    observation_covariance = model.observation_covariance
    initial_chol = tf.linalg.cholesky(initial_covariance)
    process_chol = tf.linalg.cholesky(process_covariance)
    infectious_selector = tf.one_hot(
        tf.constant(model.observed_state_indices(), dtype=tf.int32),
        depth=model.state_dim(),
        dtype=tf.float64,
    )

    def seed_pair(seed: int, salt: int) -> tf.Tensor:
        return tf.constant([int(seed) % 2147483647, int(salt) % 2147483647], dtype=tf.int32)

    def initial_sample(num_particles: int, seed: int) -> tf.Tensor:
        noise = tf.random.stateless_normal(
            [int(num_particles), model.state_dim()],
            seed=seed_pair(seed, 140),
            dtype=tf.float64,
        )
        return model.initial_mean + noise @ tf.transpose(initial_chol)

    def transition_mean(points: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        return model.transition_mean(tf.convert_to_tensor(points, dtype=tf.float64))

    def transition_sample(particles: tf.Tensor, seed: int, time_index: int) -> tf.Tensor:
        particles = tf.convert_to_tensor(particles, dtype=tf.float64)
        noise = tf.random.stateless_normal(
            [int(particles.shape[0]), model.state_dim()],
            seed=seed_pair(seed, 1140 + int(time_index)),
            dtype=tf.float64,
        )
        pushed = transition_mean(particles, int(time_index)) + noise @ tf.transpose(process_chol)
        return model._apply_process_noise_policy(pushed)

    def transition_log_density(next_particles: tf.Tensor, previous_particles: tf.Tensor, time_index: int) -> tf.Tensor:
        return model.transition_log_density(
            tf.zeros([0], dtype=tf.float64),
            tf.convert_to_tensor(previous_particles, dtype=tf.float64),
            tf.convert_to_tensor(next_particles, dtype=tf.float64),
            int(time_index),
        )

    def observation_mean(points: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        return model.infectious_components(tf.convert_to_tensor(points, dtype=tf.float64))

    def observation_jacobian(point: tf.Tensor, time_index: int) -> tf.Tensor:
        del point, time_index
        return infectious_selector

    def observation_log_density(points: tf.Tensor, observation: tf.Tensor, time_index: int) -> tf.Tensor:
        return model.observation_log_density(
            tf.zeros([0], dtype=tf.float64),
            tf.convert_to_tensor(points, dtype=tf.float64),
            tf.reshape(tf.convert_to_tensor(observation, dtype=tf.float64), [model.observation_dim()]),
            int(time_index),
        )

    def process_noise_covariance(point: tf.Tensor, time_index: int) -> tf.Tensor:
        del point, time_index
        return process_covariance

    def observation_covariance_fn(time_index: int) -> tf.Tensor:
        del time_index
        return observation_covariance

    return {
        "initial_sample": initial_sample,
        "transition_sample": transition_sample,
        "transition_mean_fn": transition_mean,
        "transition_log_density_fn": transition_log_density,
        "observation_mean_fn": observation_mean,
        "observation_jacobian_fn": observation_jacobian,
        "observation_log_density_fn": observation_log_density,
        "process_noise_covariance_fn": process_noise_covariance,
        "observation_covariance_fn": observation_covariance_fn,
        "initial_covariance": initial_covariance,
        "sir_model_metadata": {
            "row_id": SIR_ROW,
            "state_dimension": model.state_dim(),
            "observation_dimension": model.observation_dim(),
            "rk4_variant": model.rk4_variant,
            "process_noise_policy": model.process_noise_policy,
            "transition_density_contract": (
                "gaussian_pre_projection_density_used_by_reviewed_clipped_path_adapter"
            ),
        },
        "ledh_observation_adapter": {
            "flow_observation_contract": "same_observation_gaussian_sir_infectious_components",
            "flow_observation_transform": "identity",
            "flow_observation_mean": "infectious_components",
            "flow_observation_covariance": "100 * identity_9x9",
            "target_observation_density": "same_gaussian_infectious_observation_density",
            "target_density_used_for_correction": True,
            "surrogate_target_claim": False,
            "adapter_classification": (
                "BayesFilter DPF adapter for fixed-parameter SIR; not Zhao-Cui TT/SIRT source-faithfulness evidence"
            ),
        },
    }


def _dpf_generalized_sv_callbacks(theta: tf.Tensor):
    theta = tf.convert_to_tensor(theta, dtype=tf.float64)
    gamma = _normal01().cdf(theta[0])
    tau = tf.exp(theta[1])
    mu = theta[2]
    transition_covariance = tf.reshape(tf.constant(1.0, dtype=tf.float64), [1, 1])
    observation_covariance = tf.reshape(DPF_SV_LOG_SQUARE_SURROGATE_VARIANCE, [1, 1])
    initial_covariance = tf.reshape(1.0 / (1.0 - tf.square(gamma)), [1, 1])
    initial_scale = tf.sqrt(initial_covariance[0, 0])

    def seed_pair(seed: int, salt: int) -> tf.Tensor:
        return tf.constant([int(seed) % 2147483647, int(salt) % 2147483647], dtype=tf.int32)

    def initial_sample(num_particles: int, seed: int) -> tf.Tensor:
        noise = tf.random.stateless_normal(
            [int(num_particles), 1],
            seed=seed_pair(seed, 130),
            dtype=tf.float64,
        )
        return mu + initial_scale * noise

    def transition_mean(points: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        points = tf.convert_to_tensor(points, dtype=tf.float64)
        return mu + gamma * (points - mu)

    def transition_sample(particles: tf.Tensor, seed: int, time_index: int) -> tf.Tensor:
        particles = tf.convert_to_tensor(particles, dtype=tf.float64)
        noise = tf.random.stateless_normal(
            [int(particles.shape[0]), 1],
            seed=seed_pair(seed, 1130 + int(time_index)),
            dtype=tf.float64,
        )
        return transition_mean(particles, int(time_index)) + noise

    def transition_log_density(next_particles: tf.Tensor, previous_particles: tf.Tensor, time_index: int) -> tf.Tensor:
        loc = transition_mean(previous_particles, int(time_index))[:, 0]
        return tfp.distributions.Normal(
            loc=loc,
            scale=tf.constant(1.0, dtype=tf.float64),
        ).log_prob(tf.convert_to_tensor(next_particles, dtype=tf.float64)[:, 0])

    def observation_mean(points: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        points = tf.convert_to_tensor(points, dtype=tf.float64)
        return tau * points

    def observation_jacobian(point: tf.Tensor, time_index: int) -> tf.Tensor:
        del point, time_index
        return tf.reshape(tau, [1, 1])

    def observation_log_density(points: tf.Tensor, observation: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        points = tf.convert_to_tensor(points, dtype=tf.float64)
        log_scale = 0.5 * tau * points[:, 0]
        return _raw_zero_mean_normal_log_density_from_log_scale(points, observation, log_scale)

    def process_noise_covariance(point: tf.Tensor, time_index: int) -> tf.Tensor:
        del point, time_index
        return transition_covariance

    def observation_covariance_fn(time_index: int) -> tf.Tensor:
        del time_index
        return observation_covariance

    def ledh_flow_observations(raw_observations: tf.Tensor) -> tf.Tensor:
        return _log_square_surrogate_observations(raw_observations)

    return {
        "initial_sample": initial_sample,
        "transition_sample": transition_sample,
        "transition_mean_fn": transition_mean,
        "transition_log_density_fn": transition_log_density,
        "observation_mean_fn": observation_mean,
        "observation_jacobian_fn": observation_jacobian,
        "observation_log_density_fn": observation_log_density,
        "process_noise_covariance_fn": process_noise_covariance,
        "observation_covariance_fn": observation_covariance_fn,
        "initial_covariance": initial_covariance,
        "ledh_flow_observations_fn": ledh_flow_observations,
        "ledh_observation_adapter": {
            "flow_observation_contract": "log_square_gaussian_surrogate_for_ledh_flow_only",
            "flow_observation_transform": "log(y_t^2 + 1e-6)",
            "flow_observation_mean": "tau * h_t",
            "flow_observation_covariance": float(DPF_SV_LOG_SQUARE_SURROGATE_VARIANCE.numpy()),
            "target_observation_density": "raw_zero_mean_generalized_sv_prior_mean_normal_log_density",
            "target_density_used_for_correction": True,
            "surrogate_target_claim": False,
            "adapter_classification": "BayesFilter extension adapter for non-Gaussian generalized-SV flow; not same-target transformed-SV evidence",
        },
    }


def _dpf_lgssm_single_run(algorithm_id: str, seed: int, particle_count: int):
    return _dpf_single_run(
        algorithm_id,
        row_id=LGSSM_ROW,
        seed=seed,
        particle_count=particle_count,
    )


def _dpf_route(row_id: str):
    if row_id == LGSSM_ROW:
        theta = tf.constant([0.72, 0.55, 0.35, 0.35, 0.45], dtype=tf.float64)
        return _dpf_lgssm_callbacks(theta), _lgssm_observations(), "lgssm", 50
    if row_id == SV_ROW:
        return _dpf_sv_callbacks(_sv_theta()), _sv_observations(), "actual_sv_raw", 1000
    if row_id == PREDATOR_PREY_ROW:
        return (
            _dpf_predator_prey_callbacks(_predator_prey_theta()),
            _predator_prey_observations(),
            "predator_prey",
            20,
        )
    if row_id == SIR_ROW:
        return (
            _dpf_sir_callbacks(),
            _sir_observations(),
            "spatial_sir_austria_j9_T20",
            20,
        )
    if row_id == GENERALIZED_SV_ROW:
        return (
            _dpf_generalized_sv_callbacks(_generalized_sv_theta()),
            _generalized_sv_observations(),
            "generalized_sv_prior_mean",
            1008,
        )
    raise ValueError(f"no DPF callback route for {row_id}")


def _has_dpf_route(row_id: str) -> bool:
    return row_id in {LGSSM_ROW, SV_ROW, SIR_ROW, PREDATOR_PREY_ROW, GENERALIZED_SV_ROW}


def _dpf_single_run(
    algorithm_id: str,
    *,
    row_id: str,
    seed: int,
    particle_count: int,
    vectorized_particles: bool = False,
    sv_scalar_graph: bool = False,
    resampling_route: str = "none",
    ess_threshold_ratio: float = 0.5,
    method_id_suffix: str | None = None,
    sinkhorn_epsilon: float = 0.5,
    sinkhorn_iterations: int = 80,
    sinkhorn_tolerance: float = 1e-7,
    sinkhorn_epsilon_policy: str = "fixed",
):
    callbacks, raw_observations, route_label, _horizon = _dpf_route(row_id)
    if algorithm_id == BOOTSTRAP_DPF:
        return run_bootstrap_particle_filter_tf(
            observations=raw_observations,
            initial_sample=callbacks["initial_sample"],
            transition_sample=callbacks["transition_sample"],
            observation_log_density=callbacks["observation_log_density_fn"],
            seed=int(seed),
            num_particles=int(particle_count),
            ess_threshold_ratio=0.5,
            method_id=f"bootstrap_dpf_current_{route_label}_tf",
        )
    if algorithm_id == LEDH_ALG1_DPF:
        ledh_observations = callbacks.get(
            "ledh_flow_observations_fn",
            lambda observations: observations,
        )(raw_observations)
        if sv_scalar_graph:
            if row_id != SV_ROW:
                raise ValueError("P8g scalar-SV graph route is only valid for the actual SV row")
            graph_parameters = callbacks.get("scalar_sv_graph_parameters")
            if graph_parameters is None:
                raise ValueError("P8g scalar-SV graph parameters are missing")
            return run_ledh_pfpf_alg1_scalar_sv_graph_tf(
                flow_observations=ledh_observations,
                raw_observations=raw_observations,
                gamma=graph_parameters["gamma"],
                beta=graph_parameters["beta"],
                sigma=graph_parameters["sigma"],
                observation_variance=graph_parameters["observation_variance"],
                seed=int(seed),
                num_particles=int(particle_count),
                pseudo_time_steps=tf.constant([1.0], dtype=tf.float64),
                method_id=f"ledh_pfpf_alg1_scalar_sv_graph_{route_label}_tf",
            )

        def target_observation_log_density(points: tf.Tensor, observation: tf.Tensor, time_index: int) -> tf.Tensor:
            del observation
            return callbacks["observation_log_density_fn"](
                points,
                raw_observations[int(time_index)],
                int(time_index),
            )

        return run_ledh_pfpf_alg1_ukf_tf(
            observations=ledh_observations,
            initial_sample=callbacks["initial_sample"],
            initial_covariance=callbacks["initial_covariance"],
            transition_sample=callbacks["transition_sample"],
            transition_mean_fn=callbacks["transition_mean_fn"],
            transition_log_density_fn=callbacks["transition_log_density_fn"],
            observation_mean_fn=callbacks["observation_mean_fn"],
            observation_jacobian_fn=callbacks["observation_jacobian_fn"],
            observation_log_density_fn=target_observation_log_density,
            process_noise_covariance_fn=callbacks["process_noise_covariance_fn"],
            observation_covariance_fn=callbacks["observation_covariance_fn"],
            seed=int(seed),
            num_particles=int(particle_count),
            pseudo_time_steps=tf.constant([1.0], dtype=tf.float64),
            resampling_route=resampling_route,
            ess_threshold_ratio=float(ess_threshold_ratio),
            vectorized_particles=bool(vectorized_particles),
            sinkhorn_epsilon=float(sinkhorn_epsilon),
            sinkhorn_iterations=int(sinkhorn_iterations),
            sinkhorn_tolerance=float(sinkhorn_tolerance),
            sinkhorn_epsilon_policy=str(sinkhorn_epsilon_policy),
            method_id=(
                f"ledh_pfpf_alg1_ukf_current_{route_label}_tf"
                if method_id_suffix is None
                else f"ledh_pfpf_alg1_ukf_{method_id_suffix}_{route_label}_tf"
            ),
        )
    raise ValueError(f"unsupported DPF algorithm: {algorithm_id}")


def _numeric_dpf_lgssm_cell(algorithm_id: str, adapter: dict[str, str]) -> dict[str, Any]:
    return _numeric_dpf_cell(algorithm_id, LGSSM_ROW, adapter)


def _numeric_dpf_cell(algorithm_id: str, model_row_id: str, adapter: dict[str, str]) -> dict[str, Any]:
    started = time.time()
    cell = _base_cell(algorithm_id=algorithm_id, model_row_id=model_row_id, adapter=adapter)
    callbacks, _observations, _route_label, horizon = _dpf_route(model_row_id)
    ledh_observation_adapter = (
        callbacks.get("ledh_observation_adapter")
        if algorithm_id == LEDH_ALG1_DPF
        else None
    )
    per_seed = []
    try:
        for seed in DPF_SEEDS:
            result = _dpf_single_run(
                algorithm_id,
                row_id=model_row_id,
                seed=seed,
                particle_count=DPF_PARTICLE_COUNT,
            )
            if not result.finite:
                raise FloatingPointError(f"nonfinite DPF result for seed {seed}")
            value = tf.convert_to_tensor(result.log_likelihood_estimate, dtype=tf.float64)
            ess = tf.convert_to_tensor(result.ess_by_time, dtype=tf.float64)
            per_seed.append(
                {
                    "seed": int(seed),
                    "log_likelihood": _tf_float(value),
                    "average_log_likelihood": _tf_float(value / tf.cast(horizon, tf.float64)),
                    "effective_sample_size_min": _tf_float(tf.reduce_min(ess)),
                    "effective_sample_size_mean": _tf_float(tf.reduce_mean(ess)),
                    "resampling_count": int(result.resampling_count),
                    "finite": bool(result.finite),
                    "method_id": result.method_id,
                    "route_identifiers": dict(getattr(result, "route_identifiers", {})),
                }
            )
    except Exception as exc:
        cell.update(
            {
                "numeric_execution_status": "blocked_dpf_five_seed_execution_failed",
                "seed_list": DPF_SEEDS,
                "particle_count": DPF_PARTICLE_COUNT,
                "seed_count": len(per_seed),
                "per_seed_results": per_seed,
                "reason_codes": [
                    "P8D_DPF_FIVE_SEED_EXECUTION_FAILED",
                    f"{type(exc).__name__}: {str(exc).splitlines()[0]}",
                ],
                "nonclaims": [
                    "not a DPF numeric value summary",
                    "per-seed failure prevents MC standard error reporting",
                ],
                "runtime_seconds": round(time.time() - started, 6),
            }
        )
        return cell

    values = tf.constant([entry["log_likelihood"] for entry in per_seed], dtype=tf.float64)
    mean_value = tf.reduce_mean(values)
    sample_sd = tf.math.reduce_std(values, axis=0) * tf.sqrt(
        tf.cast(len(DPF_SEEDS), tf.float64) / tf.cast(len(DPF_SEEDS) - 1, tf.float64)
    )
    mc_se = sample_sd / tf.sqrt(tf.cast(len(DPF_SEEDS), tf.float64))
    cell.update(
        {
            "numeric_execution_status": "executed_numeric_dpf_5seed_value",
            "value_adapter_status": "executed_p8d_dpf_5seed_value",
            "log_likelihood": _tf_float(mean_value),
            "average_log_likelihood": _tf_float(mean_value / tf.cast(horizon, tf.float64)),
            "score_adapter_status": "not_certified_for_main_score_without_mc_and_fixed_branch_review",
            "score_coordinate_system": "not_applicable_dpf_main_gradient_not_certified",
            "score_derivative_provenance": "not_promoted_dpf_gradient_requires_reviewed_contract",
            "hessian_adapter_status": "not_executed_dpf_hessian_requires_reviewed_contract",
            "curvature_status": "hessian_not_exposed_dpf",
            "mc_standard_error": _tf_float(mc_se),
            "sample_standard_deviation": _tf_float(sample_sd),
            "particle_count": DPF_PARTICLE_COUNT,
            "seed_count": len(DPF_SEEDS),
            "seed_list": DPF_SEEDS,
            "per_seed_results": per_seed,
            "evaluator_backend": per_seed[0]["method_id"],
            "ledh_observation_adapter": ledh_observation_adapter,
            "runtime_seconds": round(time.time() - started, 6),
            "reason_codes": ["P8D_NUMERIC_EXECUTED_DPF_5SEED_VALUE_ONLY"],
            "nonclaims": [
                "five-seed stochastic value summary only",
                "small particle-count diagnostic wiring run, not a production DPF accuracy setting",
                "not a DPF gradient certification",
                "not a filter ranking",
                "P8c is a partial comparator-only baseline, not full scientific truth",
            ],
        }
    )
    return cell


def _p8g_profile_dpf_prefix(
    *,
    row_id: str,
    algorithm_id: str,
    horizon: int,
    particle_count: int,
    seeds: list[int],
    device: str,
    g0_manifest: Path | None,
    vectorized_particles: bool = False,
    sv_scalar_graph: bool = False,
) -> dict[str, Any]:
    if algorithm_id not in {BOOTSTRAP_DPF, LEDH_ALG1_DPF}:
        raise ValueError(f"unsupported P8g profile algorithm: {algorithm_id}")
    if not _has_dpf_route(row_id):
        raise ValueError(f"no DPF callback route for {row_id}")
    if horizon <= 0:
        raise ValueError("horizon must be positive")
    if particle_count <= 0:
        raise ValueError("particle count must be positive")
    if device not in {"cpu", "gpu"}:
        raise ValueError("device must be 'cpu' or 'gpu'")
    if device == "gpu" and g0_manifest is None:
        raise ValueError("trusted GPU profile requires --g0-manifest")
    if sv_scalar_graph and (algorithm_id != LEDH_ALG1_DPF or row_id != SV_ROW):
        raise ValueError("P8g scalar-SV graph route is only valid for LEDH on the actual SV row")
    if sv_scalar_graph and vectorized_particles:
        raise ValueError("choose either --p8g-sv-scalar-graph or --p8g-vectorized-particles, not both")

    original_route = _dpf_route
    _callbacks, _observations, route_label, full_horizon = original_route(row_id)
    if horizon > full_horizon:
        raise ValueError(f"horizon {horizon} exceeds route horizon {full_horizon}")

    def prefix_route(current_row_id: str):
        callbacks, observations, current_route_label, current_horizon = original_route(current_row_id)
        if current_row_id == row_id:
            return (
                callbacks,
                observations[:horizon],
                f"{current_route_label}_p8g_prefix_T{horizon}",
                horizon,
            )
        return callbacks, observations, current_route_label, current_horizon

    device_name = "/GPU:0" if device == "gpu" else "/CPU:0"
    per_seed: list[dict[str, Any]] = []
    started = time.perf_counter()
    marker_device = None
    globals()["_dpf_route"] = prefix_route
    try:
        with tf.device(device_name):
            marker = tf.reduce_sum(tf.ones([2, 2], dtype=tf.float64))
            marker_device = marker.device
            for seed in seeds:
                seed_started = time.perf_counter()
                result = _dpf_single_run(
                    algorithm_id,
                    row_id=row_id,
                    seed=int(seed),
                    particle_count=int(particle_count),
                    vectorized_particles=bool(vectorized_particles),
                    sv_scalar_graph=bool(sv_scalar_graph),
                )
                log_likelihood = tf.convert_to_tensor(
                    result.log_likelihood_estimate,
                    dtype=tf.float64,
                )
                ess = tf.convert_to_tensor(result.ess_by_time, dtype=tf.float64)
                filtered_means = tf.convert_to_tensor(result.filtered_means, dtype=tf.float64)
                per_seed.append(
                    {
                        "seed": int(seed),
                        "runtime_seconds": round(time.perf_counter() - seed_started, 6),
                        "finite": bool(result.finite),
                        "log_likelihood": _tf_float(log_likelihood),
                        "average_log_likelihood": _tf_float(log_likelihood / tf.cast(horizon, tf.float64)),
                        "effective_sample_size_min": _tf_float(tf.reduce_min(ess)),
                        "effective_sample_size_mean": _tf_float(tf.reduce_mean(ess)),
                        "resampling_count": int(result.resampling_count),
                        "method_id": result.method_id,
                        "log_likelihood_device": log_likelihood.device,
                        "ess_device": ess.device,
                        "filtered_means_device": filtered_means.device,
                        "route_identifiers": dict(getattr(result, "route_identifiers", {})),
                    }
                )
    finally:
        globals()["_dpf_route"] = original_route

    wall_seconds = time.perf_counter() - started
    values = tf.constant([entry["log_likelihood"] for entry in per_seed], dtype=tf.float64)
    sample_sd = (
        tf.math.reduce_std(values)
        * tf.sqrt(tf.cast(len(per_seed), tf.float64) / tf.cast(max(len(per_seed) - 1, 1), tf.float64))
        if len(per_seed) > 1
        else tf.constant(0.0, dtype=tf.float64)
    )
    devices_used = sorted(
        {
            str(entry[key])
            for entry in per_seed
            for key in ("log_likelihood_device", "ess_device", "filtered_means_device")
        }
    )
    known_python_loops = [
        "outer Python seed loop in P8g profile harness",
    ]
    if algorithm_id == LEDH_ALG1_DPF:
        if sv_scalar_graph:
            known_python_loops.append(
                "P8g scalar-SV graph route keeps the serious time loop in tf.while_loop and particles in vector TensorFlow ops"
            )
        else:
            known_python_loops.extend(
                [
                    "current TensorFlow filter implementation iterates over time in Python/eager mode",
                    (
                        "current Algorithm 1 LEDH reference route iterates over particles for per-particle UKF/flow state"
                        if not vectorized_particles
                        else "P8g vectorized route maps per-particle UKF/flow state with tf.vectorized_map"
                    ),
                ]
            )
    payload = {
        "schema_version": "filter_bench.p8g_profile.v1",
        "phase": "P8G_G1_CURRENT_BOTTLENECK_PROFILE",
        "status": (
            "executed_p8g_prefix_profile"
            if all(entry["finite"] for entry in per_seed)
            else "blocked_p8g_prefix_profile_nonfinite"
        ),
        "run_manifest": {
            "git_commit": _git_commit(),
            "dirty_state_summary": _dirty_summary(),
            "command": " ".join(sys.argv),
            "environment": "TensorFlow/TensorFlow Probability profile harness",
            "cuda_visible_devices": str(__import__("os").environ.get("CUDA_VISIBLE_DEVICES")),
            "requested_device": device,
            "device_context": device_name,
            "marker_device": marker_device,
            "tf_physical_gpus": [gpu.name for gpu in tf.config.list_physical_devices("GPU")],
            "tf_logical_gpus": [gpu.name for gpu in tf.config.list_logical_devices("GPU")],
            "g0_manifest": _rel(g0_manifest) if g0_manifest is not None else None,
            "vectorized_particles": bool(vectorized_particles),
            "sv_scalar_graph": bool(sv_scalar_graph),
        },
        "profile_scope": {
            "row_id": row_id,
            "algorithm_id": algorithm_id,
            "route_label": route_label,
            "full_horizon": int(full_horizon),
            "horizon_prefix": int(horizon),
            "particle_count": int(particle_count),
            "seeds": [int(seed) for seed in seeds],
            "seed_count": len(seeds),
            "route_variant": (
                "p8g_sv_scalar_graph"
                if sv_scalar_graph
                else (
                    "p8g_vectorized_particles"
                    if vectorized_particles
                    else "current_looped_particles"
                )
            ),
        },
        "timing": {
            "wall_seconds": round(wall_seconds, 6),
            "mean_seed_runtime_seconds": round(
                sum(entry["runtime_seconds"] for entry in per_seed) / max(len(per_seed), 1),
                6,
            ),
            "seconds_per_seed_time_particle": round(
                wall_seconds / max(len(per_seed) * horizon * particle_count, 1),
                9,
            ),
        },
        "value_summary": {
            "mean_log_likelihood": _tf_float(tf.reduce_mean(values)),
            "mean_average_log_likelihood": _tf_float(tf.reduce_mean(values) / tf.cast(horizon, tf.float64)),
            "sample_standard_deviation": _tf_float(sample_sd),
            "mc_standard_error": _tf_float(sample_sd / tf.sqrt(tf.cast(max(len(per_seed), 1), tf.float64))),
        },
        "device_diagnostics": {
            "devices_used_by_result_tensors": devices_used,
            "no_silent_cpu_fallback_claim": device == "gpu" and any("GPU" in item for item in devices_used),
        },
        "bottleneck_hypothesis": {
            "known_python_loops": known_python_loops,
            "first_vectorization_targets": [
                "batch per-particle Algorithm 1 UKF predict/update operations",
                "move per-time particle transforms into TensorFlow graph kernels",
                "keep five-seed orchestration outside the serious GPU kernel until G2/G4 route is vectorized",
            ],
        },
        "per_seed_results": per_seed,
        "nonclaims": [
            "prefix profile only",
            "not tuned particle-count evidence",
            "not a GPU speedup claim after rewrite",
            "not gradient correctness",
            "not HMC readiness",
            "not a filter ranking",
        ],
    }
    return payload


def _p8h_profile_dpf_prefix(
    *,
    row_id: str,
    algorithm_id: str,
    horizon: int,
    particle_count: int,
    seeds: list[int],
    device: str,
    g0_manifest: Path | None,
    resampling_route: str = P8H_DEFAULT_RESAMPLING_ROUTE,
    ess_threshold_ratio: float = 1.01,
    sinkhorn_epsilon: float = 1.0,
    sinkhorn_iterations: int = 200,
    sinkhorn_tolerance: float = 1e-6,
    sinkhorn_epsilon_policy: str = "fixed",
) -> dict[str, Any]:
    if row_id != SV_ROW:
        raise ValueError("P8h Phase 3 initial scope supports only actual_sv")
    if algorithm_id != LEDH_ALG1_DPF:
        raise ValueError("P8h Phase 3 initial scope supports only Algorithm 1 LEDH")
    if resampling_route not in {
        OT_SINKHORN_COVARIANCE_CARRY_ROUTE,
        OT_ANNEALED_COVARIANCE_CARRY_ROUTE,
    }:
        raise ValueError("P8h requires a reviewed OT covariance-carry route")
    if horizon <= 0:
        raise ValueError("horizon must be positive")
    if particle_count <= 0:
        raise ValueError("particle count must be positive")
    if device not in {"cpu", "gpu"}:
        raise ValueError("device must be 'cpu' or 'gpu'")
    if device == "gpu" and g0_manifest is None:
        raise ValueError("trusted GPU P8h smoke requires --g0-manifest")

    original_route = _dpf_route
    _callbacks, _observations, route_label, full_horizon = original_route(row_id)
    if horizon > full_horizon:
        raise ValueError(f"horizon {horizon} exceeds route horizon {full_horizon}")

    def prefix_route(current_row_id: str):
        callbacks, observations, current_route_label, current_horizon = original_route(current_row_id)
        if current_row_id == row_id:
            return (
                callbacks,
                observations[:horizon],
                f"{current_route_label}_p8h_prefix_T{horizon}",
                horizon,
            )
        return callbacks, observations, current_route_label, current_horizon

    device_name = "/GPU:0" if device == "gpu" else "/CPU:0"
    per_seed: list[dict[str, Any]] = []
    started = time.perf_counter()
    marker_device = None
    globals()["_dpf_route"] = prefix_route
    try:
        with tf.device(device_name):
            marker = tf.reduce_sum(tf.ones([2, 2], dtype=tf.float64))
            marker_device = marker.device
            for seed in seeds:
                seed_started = time.perf_counter()
                result = _dpf_single_run(
                    algorithm_id,
                    row_id=row_id,
                    seed=int(seed),
                    particle_count=int(particle_count),
                    resampling_route=resampling_route,
                    ess_threshold_ratio=float(ess_threshold_ratio),
                    method_id_suffix="p8h_ot_resampled_alg1",
                    sinkhorn_epsilon=float(sinkhorn_epsilon),
                    sinkhorn_iterations=int(sinkhorn_iterations),
                    sinkhorn_tolerance=float(sinkhorn_tolerance),
                )
                log_likelihood = tf.convert_to_tensor(
                    result.log_likelihood_estimate,
                    dtype=tf.float64,
                )
                ess = tf.convert_to_tensor(result.ess_by_time, dtype=tf.float64)
                first_resampled = next(
                    (
                        diag
                        for diag in result.resampling_diagnostics
                        if bool(diag.get("resampled", False))
                    ),
                    {},
                )
                per_seed.append(
                    {
                        "seed": int(seed),
                        "runtime_seconds": round(time.perf_counter() - seed_started, 6),
                        "finite": bool(result.finite),
                        "log_likelihood": _tf_float(log_likelihood),
                        "average_log_likelihood": _tf_float(log_likelihood / tf.cast(horizon, tf.float64)),
                        "effective_sample_size_min": _tf_float(tf.reduce_min(ess)),
                        "effective_sample_size_mean": _tf_float(tf.reduce_mean(ess)),
                        "resampling_count": int(result.resampling_count),
                        "method_id": result.method_id,
                        "log_likelihood_device": log_likelihood.device,
                        "ess_device": ess.device,
                        "route_identifiers": dict(getattr(result, "route_identifiers", {})),
                        "first_resampling_diagnostics": first_resampled,
                    }
                )
    finally:
        globals()["_dpf_route"] = original_route

    wall_seconds = time.perf_counter() - started
    values = tf.constant([entry["log_likelihood"] for entry in per_seed], dtype=tf.float64)
    devices_used = sorted(
        {
            str(entry[key])
            for entry in per_seed
            for key in ("log_likelihood_device", "ess_device")
        }
    )
    return {
        "schema_version": "filter_bench.p8h_ot_resampled_alg1_smoke.v1",
        "phase": "P8H_PHASE3_SCALAR_SV_GPU_OT_IMPLEMENTATION",
        "status": (
            "executed_p8h_ot_resampled_alg1_smoke"
            if all(entry["finite"] for entry in per_seed)
            else "blocked_p8h_ot_resampled_alg1_smoke_nonfinite"
        ),
        "run_manifest": {
            "git_commit": _git_commit(),
            "dirty_state_summary": _dirty_summary(),
            "command": " ".join(sys.argv),
            "environment": "TensorFlow/TensorFlow Probability P8h OT-resampled Algorithm 1 smoke",
            "cuda_visible_devices": str(__import__("os").environ.get("CUDA_VISIBLE_DEVICES")),
            "requested_device": device,
            "device_context": device_name,
            "marker_device": marker_device,
            "tf_physical_gpus": [gpu.name for gpu in tf.config.list_physical_devices("GPU")],
            "tf_logical_gpus": [gpu.name for gpu in tf.config.list_logical_devices("GPU")],
            "g0_manifest": _rel(g0_manifest) if g0_manifest is not None else None,
            "wall_seconds": round(wall_seconds, 6),
        },
        "profile_scope": {
            "row_id": row_id,
            "algorithm_id": algorithm_id,
            "route_label": route_label,
            "route_variant": P8H_ROUTE_VARIANT,
            "resampling_route": resampling_route,
            "full_horizon": int(full_horizon),
            "horizon_prefix": int(horizon),
            "particle_count": int(particle_count),
            "seeds": [int(seed) for seed in seeds],
            "seed_count": len(seeds),
            "ess_threshold_ratio": float(ess_threshold_ratio),
            "sinkhorn_epsilon": float(sinkhorn_epsilon),
            "sinkhorn_iterations": int(sinkhorn_iterations),
            "sinkhorn_tolerance": float(sinkhorn_tolerance),
        },
        "value_summary": {
            "mean_log_likelihood": _tf_float(tf.reduce_mean(values)),
            "mean_average_log_likelihood": _tf_float(tf.reduce_mean(values) / tf.cast(horizon, tf.float64)),
        },
        "device_diagnostics": {
            "devices_used_by_result_tensors": devices_used,
            "no_silent_cpu_fallback_claim": device == "gpu" and any("GPU" in item for item in devices_used),
        },
        "p8g_quarantine": {
            "p8g_fixed_randomness_gradient_check": "historical_no_resampling_diagnostic_only",
            "p8g_particle_tuning": "historical_no_resampling_blocker_only",
            "p8h_schema_reuses_p8g_metadata": False,
        },
        "per_seed_results": per_seed,
        "nonclaims": [
            "Phase 3 implementation smoke only",
            "not value adequacy",
            "not particle-count tuning",
            "not gradient correctness",
            "not GPU scaling",
            "not HMC readiness",
            "not stochastic PF marginal-gradient correctness",
            "not exact nonlinear likelihood correctness",
            "not a filter ranking",
        ],
    }


def _p8j_sir_profile_dpf_prefix(
    *,
    row_id: str,
    algorithm_id: str,
    horizon: int,
    particle_count: int,
    seeds: list[int],
    device: str,
    g0_manifest: Path | None,
    runtime_budget_seconds: float,
    ess_threshold_ratio: float = 1.01,
    resampling_route: str = P8H_DEFAULT_RESAMPLING_ROUTE,
    sinkhorn_epsilon: float = 1.0,
    sinkhorn_iterations: int = 200,
    sinkhorn_tolerance: float = 1e-6,
    sinkhorn_epsilon_policy: str = "fixed",
) -> dict[str, Any]:
    if row_id != SIR_ROW:
        raise ValueError("P8j Phase 5 tuning supports only SIR d18")
    if algorithm_id not in {BOOTSTRAP_DPF, LEDH_ALG1_DPF}:
        raise ValueError("P8j Phase 5 tuning supports bootstrap and Algorithm 1 LEDH only")
    if horizon <= 0:
        raise ValueError("horizon must be positive")
    if particle_count <= 0:
        raise ValueError("particle count must be positive")
    if device not in {"cpu", "gpu"}:
        raise ValueError("device must be 'cpu' or 'gpu'")
    if device == "gpu" and g0_manifest is None:
        raise ValueError("trusted GPU P8j tuning requires --g0-manifest")
    if algorithm_id == LEDH_ALG1_DPF and resampling_route != P8H_DEFAULT_RESAMPLING_ROUTE:
        raise ValueError("P8j LEDH tuning requires the reviewed Sinkhorn covariance-carry route")

    original_route = _dpf_route
    _callbacks, _observations, route_label, full_horizon = original_route(row_id)
    if horizon > full_horizon:
        raise ValueError(f"horizon {horizon} exceeds route horizon {full_horizon}")

    def prefix_route(current_row_id: str):
        callbacks, observations, current_route_label, current_horizon = original_route(current_row_id)
        if current_row_id == row_id:
            return (
                callbacks,
                observations[:horizon],
                f"{current_route_label}_p8j_prefix_T{horizon}",
                horizon,
            )
        return callbacks, observations, current_route_label, current_horizon

    route_variant = (
        P8J_BOOTSTRAP_ROUTE_VARIANT
        if algorithm_id == BOOTSTRAP_DPF
        else P8J_ROUTE_VARIANT
    )
    device_name = "/GPU:0" if device == "gpu" else "/CPU:0"
    per_seed: list[dict[str, Any]] = []
    started = time.perf_counter()
    marker_device = None
    globals()["_dpf_route"] = prefix_route
    try:
        with tf.device(device_name):
            marker = tf.reduce_sum(tf.ones([2, 2], dtype=tf.float64))
            marker_device = marker.device
            for seed in seeds:
                seed_started = time.perf_counter()
                try:
                    if algorithm_id == LEDH_ALG1_DPF:
                        result = _dpf_single_run(
                            algorithm_id,
                            row_id=row_id,
                            seed=int(seed),
                            particle_count=int(particle_count),
                            resampling_route=resampling_route,
                            ess_threshold_ratio=float(ess_threshold_ratio),
                            method_id_suffix="p8j_sir_ot_resampled_alg1",
                            sinkhorn_epsilon=float(sinkhorn_epsilon),
                            sinkhorn_iterations=int(sinkhorn_iterations),
                            sinkhorn_tolerance=float(sinkhorn_tolerance),
                            sinkhorn_epsilon_policy=str(sinkhorn_epsilon_policy),
                        )
                    else:
                        result = _dpf_single_run(
                            algorithm_id,
                            row_id=row_id,
                            seed=int(seed),
                            particle_count=int(particle_count),
                        )
                except Exception as exc:
                    per_seed.append(
                        {
                            "seed": int(seed),
                            "runtime_seconds": round(time.perf_counter() - seed_started, 6),
                            "finite": False,
                            "log_likelihood": None,
                            "average_log_likelihood": None,
                            "effective_sample_size_min": None,
                            "effective_sample_size_mean": None,
                            "resampling_count": 0,
                            "method_id": f"blocked_{algorithm_id}",
                            "log_likelihood_device": None,
                            "ess_device": None,
                            "route_identifiers": {
                                "route_variant": route_variant,
                                "resampling_route": (
                                    "none"
                                    if algorithm_id == BOOTSTRAP_DPF
                                    else resampling_route
                                ),
                            },
                            "first_resampling_diagnostics": {},
                            "failure_error_type": type(exc).__name__,
                            "failure_message": str(exc).splitlines()[0],
                        }
                    )
                    break
                log_likelihood = tf.convert_to_tensor(
                    result.log_likelihood_estimate,
                    dtype=tf.float64,
                )
                ess = tf.convert_to_tensor(result.ess_by_time, dtype=tf.float64)
                first_resampled = next(
                    (
                        diag
                        for diag in result.resampling_diagnostics
                        if bool(diag.get("resampled", False))
                    ),
                    {},
                )
                per_seed.append(
                    {
                        "seed": int(seed),
                        "runtime_seconds": round(time.perf_counter() - seed_started, 6),
                        "finite": bool(result.finite),
                        "log_likelihood": _tf_float(log_likelihood),
                        "average_log_likelihood": _tf_float(log_likelihood / tf.cast(horizon, tf.float64)),
                        "effective_sample_size_min": _tf_float(tf.reduce_min(ess)),
                        "effective_sample_size_mean": _tf_float(tf.reduce_mean(ess)),
                        "resampling_count": int(result.resampling_count),
                        "method_id": result.method_id,
                        "log_likelihood_device": log_likelihood.device,
                        "ess_device": ess.device,
                        "route_identifiers": dict(getattr(result, "route_identifiers", {})),
                        "first_resampling_diagnostics": first_resampled,
                    }
                )
    finally:
        globals()["_dpf_route"] = original_route

    wall_seconds = time.perf_counter() - started
    successful_values = [
        entry["log_likelihood"]
        for entry in per_seed
        if entry.get("finite") is True and entry.get("log_likelihood") is not None
    ]
    values = (
        tf.constant(successful_values, dtype=tf.float64)
        if successful_values
        else tf.constant([0.0], dtype=tf.float64)
    )
    devices_used = sorted(
        {
            str(entry[key])
            for entry in per_seed
            for key in ("log_likelihood_device", "ess_device")
            if entry.get(key) is not None
        }
    )
    return {
        "schema_version": "filter_bench.p8j_sir_profile.v1",
        "phase": "P8J_PHASE5_SIR_PARTICLE_TUNING_PROFILE",
        "status": (
            "executed_p8j_sir_profile"
            if all(entry["finite"] for entry in per_seed)
            else "blocked_p8j_sir_profile_nonfinite"
        ),
        "run_manifest": {
            "git_commit": _git_commit(),
            "dirty_state_summary": _dirty_summary(),
            "command": " ".join(sys.argv),
            "environment": "TensorFlow/TensorFlow Probability P8j SIR d18 tuning profile",
            "cuda_visible_devices": str(__import__("os").environ.get("CUDA_VISIBLE_DEVICES")),
            "requested_device": device,
            "device_context": device_name,
            "marker_device": marker_device,
            "tf_physical_gpus": [gpu.name for gpu in tf.config.list_physical_devices("GPU")],
            "tf_logical_gpus": [gpu.name for gpu in tf.config.list_logical_devices("GPU")],
            "g0_manifest": _rel(g0_manifest) if g0_manifest is not None else None,
            "wall_seconds": round(wall_seconds, 6),
            "runtime_budget_seconds": float(runtime_budget_seconds),
        },
        "profile_scope": {
            "row_id": row_id,
            "algorithm_id": algorithm_id,
            "route_label": route_label,
            "route_variant": route_variant,
            "resampling_route": (
                "none" if algorithm_id == BOOTSTRAP_DPF else resampling_route
            ),
            "full_horizon": int(full_horizon),
            "horizon_prefix": int(horizon),
            "particle_count": int(particle_count),
            "seeds": [int(seed) for seed in seeds],
            "seed_count": len(seeds),
            "ess_threshold_ratio": float(ess_threshold_ratio),
            "sinkhorn_epsilon": (
                None if algorithm_id == BOOTSTRAP_DPF else float(sinkhorn_epsilon)
            ),
            "sinkhorn_iterations": (
                None if algorithm_id == BOOTSTRAP_DPF else int(sinkhorn_iterations)
            ),
            "sinkhorn_tolerance": (
                None if algorithm_id == BOOTSTRAP_DPF else float(sinkhorn_tolerance)
            ),
            "sinkhorn_epsilon_policy": (
                None if algorithm_id == BOOTSTRAP_DPF else str(sinkhorn_epsilon_policy)
            ),
            "sinkhorn_repair_classification": (
                None
                if algorithm_id == BOOTSTRAP_DPF or sinkhorn_epsilon_policy == "fixed"
                else "p8j_sir_numerical_stability_repair_candidate"
            ),
        },
        "value_summary": {
            "mean_log_likelihood": (
                _tf_float(tf.reduce_mean(values))
                if all(entry["finite"] for entry in per_seed)
                else None
            ),
            "mean_average_log_likelihood": (
                _tf_float(tf.reduce_mean(values) / tf.cast(horizon, tf.float64))
                if all(entry["finite"] for entry in per_seed)
                else None
            ),
        },
        "device_diagnostics": {
            "devices_used_by_result_tensors": devices_used,
            "no_silent_cpu_fallback_claim": device == "gpu" and any("GPU" in item for item in devices_used),
        },
        "per_seed_results": per_seed,
        "nonclaims": [
            "SIR d18 particle tuning profile only",
            "not leaderboard completion",
            "not gradient correctness",
            "not HMC readiness",
            "not Zhao-Cui TT/SIRT source-faithfulness",
            "not exact nonlinear likelihood correctness",
            "not production readiness",
        ],
    }


def _p8j_sir_ot_sinkhorn_diagnostic(
    *,
    row_id: str,
    horizon: int,
    particle_count: int,
    seed: int,
    device: str,
    g0_manifest: Path | None,
    runtime_budget_seconds: float,
    ess_threshold_ratio: float = 1.01,
    resampling_route: str = P8H_DEFAULT_RESAMPLING_ROUTE,
    sinkhorn_epsilon: float = 1.0,
    sinkhorn_iterations: int = 200,
    sinkhorn_tolerance: float = 1e-6,
) -> dict[str, Any]:
    if row_id != SIR_ROW:
        raise ValueError("P8j Phase 5b Sinkhorn diagnostic supports only SIR d18")
    if horizon <= 0:
        raise ValueError("horizon must be positive")
    if particle_count <= DPF_PARTICLE_COUNT:
        raise ValueError("P8j Phase 5b diagnostic particle count must exceed historical N=8")
    if device not in {"cpu", "gpu"}:
        raise ValueError("device must be 'cpu' or 'gpu'")
    if device != "gpu":
        raise ValueError("P8j Phase 5b Sinkhorn diagnostic must run on trusted GPU")
    if g0_manifest is None:
        raise ValueError("trusted GPU P8j Phase 5b diagnostic requires --g0-manifest")
    if resampling_route != P8H_DEFAULT_RESAMPLING_ROUTE:
        raise ValueError("P8j Phase 5b diagnostic requires the reviewed Sinkhorn covariance-carry route")

    callbacks, raw_observations, route_label, full_horizon = _dpf_route(row_id)
    if horizon > full_horizon:
        raise ValueError(f"horizon {horizon} exceeds route horizon {full_horizon}")
    ledh_observations = callbacks.get(
        "ledh_flow_observations_fn",
        lambda observations: observations,
    )(raw_observations)[:horizon]
    device_name = "/GPU:0" if device == "gpu" else "/CPU:0"
    started = time.perf_counter()
    marker_device = None
    resampling_event: dict[str, Any] | None = None
    sinkhorn_failure: dict[str, Any] | None = None
    sinkhorn_repaired_probe: dict[str, Any] | None = None
    log_likelihood = tf.constant(0.0, dtype=tf.float64)

    with tf.device(device_name):
        marker = tf.reduce_sum(tf.ones([2, 2], dtype=tf.float64))
        marker_device = marker.device
        particles = tf.cast(callbacks["initial_sample"](particle_count, seed), tf.float64)
        initial_covariance = tf.cast(callbacks["initial_covariance"], tf.float64)
        covariances = tf.tile(initial_covariance[tf.newaxis, :, :], [particle_count, 1, 1])
        log_weights = tf.fill(
            [particle_count],
            -tf.math.log(tf.cast(particle_count, tf.float64)),
        )
        pseudo_time = tf.constant([1.0], dtype=tf.float64)
        for t, observation in enumerate(tf.unstack(tf.cast(ledh_observations, tf.float64), axis=0)):
            ancestors = tf.identity(particles)
            previous_covariances = tf.identity(covariances)
            pre_flow = tf.cast(callbacks["transition_sample"](ancestors, seed, int(t)), tf.float64)
            step = li_coates_ledh_alg1_time_step_tf(
                ancestors=ancestors,
                previous_covariances=previous_covariances,
                pre_flow_particles=pre_flow,
                observation=observation,
                transition_mean_fn=callbacks["transition_mean_fn"],
                transition_log_density_fn=callbacks["transition_log_density_fn"],
                observation_mean_fn=callbacks["observation_mean_fn"],
                observation_jacobian_fn=callbacks["observation_jacobian_fn"],
                process_noise_covariance_fn=callbacks["process_noise_covariance_fn"],
                observation_covariance_fn=callbacks["observation_covariance_fn"],
                time_index=int(t),
                pseudo_time_steps=pseudo_time,
            )
            post_flow = step.post_flow_particles

            def target_observation_log_density(points: tf.Tensor) -> tf.Tensor:
                return callbacks["observation_log_density_fn"](
                    points,
                    raw_observations[int(t)],
                    int(t),
                )

            corrected_log_weights = (
                log_weights
                + tf.cast(callbacks["transition_log_density_fn"](post_flow, ancestors, int(t)), tf.float64)
                + tf.cast(target_observation_log_density(post_flow), tf.float64)
                - step.pre_flow_log_density
                + step.forward_log_det
            )
            weights = tf.nn.softmax(corrected_log_weights)
            incremental = tf.reduce_logsumexp(corrected_log_weights)
            log_likelihood = log_likelihood + incremental
            ess = 1.0 / tf.reduce_sum(weights * weights)
            trigger_resampling = bool((ess < ess_threshold_ratio * particle_count).numpy())
            if trigger_resampling:
                cost = pairwise_squared_euclidean_tf(post_flow)
                source = weights / tf.reduce_sum(weights)
                normalized_log_weights = tf.math.log(
                    tf.maximum(source, tf.constant(1e-300, dtype=tf.float64))
                )
                source_entropy = -tf.reduce_sum(source * normalized_log_weights)
                resampling_event = {
                    "time_index": int(t),
                    "ess": _tf_float(ess),
                    "ess_ratio": _tf_float(ess / tf.cast(particle_count, tf.float64)),
                    "ess_threshold_ratio": float(ess_threshold_ratio),
                    "particle_count": int(particle_count),
                    "state_dimension": int(post_flow.shape[-1]),
                    "post_flow_abs_max": _tf_float(tf.reduce_max(tf.abs(post_flow))),
                    "post_flow_abs_mean": _tf_float(tf.reduce_mean(tf.abs(post_flow))),
                    "post_flow_component_std_min": _tf_float(
                        tf.reduce_min(tf.math.reduce_std(post_flow, axis=0))
                    ),
                    "post_flow_component_std_max": _tf_float(
                        tf.reduce_max(tf.math.reduce_std(post_flow, axis=0))
                    ),
                    "source_weight_min": _tf_float(tf.reduce_min(source)),
                    "source_weight_max": _tf_float(tf.reduce_max(source)),
                    "source_weight_entropy": _tf_float(source_entropy),
                    "source_weight_perplexity": _tf_float(tf.exp(source_entropy)),
                    "source_weight_sum_residual": _tf_float(tf.abs(tf.reduce_sum(source) - 1.0)),
                    "cost_min": _tf_float(tf.reduce_min(cost)),
                    "cost_max": _tf_float(tf.reduce_max(cost)),
                    "cost_mean": _tf_float(tf.reduce_mean(cost)),
                    "cost_std": _tf_float(tf.math.reduce_std(cost)),
                    "cost_over_epsilon_max": _tf_float(tf.reduce_max(cost) / tf.cast(sinkhorn_epsilon, tf.float64)),
                    "cost_over_epsilon_mean": _tf_float(tf.reduce_mean(cost) / tf.cast(sinkhorn_epsilon, tf.float64)),
                    "sinkhorn_epsilon": float(sinkhorn_epsilon),
                    "sinkhorn_iterations": int(sinkhorn_iterations),
                    "sinkhorn_tolerance": float(sinkhorn_tolerance),
                }
                try:
                    apply_ot_resampling_state_tf(
                        particles=post_flow,
                        covariances=step.updated_covariances,
                        weights=source,
                        log_weights=normalized_log_weights,
                        resampling_route=resampling_route,
                        sinkhorn_epsilon=float(sinkhorn_epsilon),
                        sinkhorn_iterations=int(sinkhorn_iterations),
                        sinkhorn_tolerance=float(sinkhorn_tolerance),
                    )
                    sinkhorn_failure = {
                        "failure_error_type": None,
                        "failure_message": None,
                        "nominal_settings_failed": False,
                    }
                except Exception as exc:
                    sinkhorn_failure = {
                        "failure_error_type": type(exc).__name__,
                        "failure_message": str(exc).splitlines()[0],
                        "nominal_settings_failed": True,
                    }
                repaired_epsilon = max(
                    float(sinkhorn_epsilon),
                    float(resampling_event["cost_mean"] or 0.0),
                )
                try:
                    _particles, _covariances, repaired_diag = apply_ot_resampling_state_tf(
                        particles=post_flow,
                        covariances=step.updated_covariances,
                        weights=source,
                        log_weights=normalized_log_weights,
                        resampling_route=resampling_route,
                        sinkhorn_epsilon=repaired_epsilon,
                        sinkhorn_iterations=max(int(sinkhorn_iterations), 500),
                        sinkhorn_tolerance=float(sinkhorn_tolerance),
                    )
                    sinkhorn_repaired_probe = {
                        "probe_kind": "scale_adaptive_epsilon_equal_max_nominal_or_cost_mean",
                        "epsilon": repaired_epsilon,
                        "sinkhorn_iterations": max(int(sinkhorn_iterations), 500),
                        "sinkhorn_tolerance": float(sinkhorn_tolerance),
                        "finite": True,
                        "canonical_transport_row_sum_residual": repaired_diag.get(
                            "canonical_transport_row_sum_residual"
                        ),
                        "transport_helper_max_row_residual": repaired_diag.get(
                            "transport_helper_max_row_residual"
                        ),
                        "transport_helper_max_column_residual": repaired_diag.get(
                            "transport_helper_max_column_residual"
                        ),
                    }
                except Exception as exc:
                    sinkhorn_repaired_probe = {
                        "probe_kind": "scale_adaptive_epsilon_equal_max_nominal_or_cost_mean",
                        "epsilon": repaired_epsilon,
                        "sinkhorn_iterations": max(int(sinkhorn_iterations), 500),
                        "sinkhorn_tolerance": float(sinkhorn_tolerance),
                        "finite": False,
                        "failure_error_type": type(exc).__name__,
                        "failure_message": str(exc).splitlines()[0],
                    }
                break
            particles = post_flow
            covariances = step.updated_covariances
            log_weights = tf.math.log(tf.maximum(weights, tf.constant(1e-300, dtype=tf.float64)))

    status = (
        "executed_p8j_sir_ot_sinkhorn_diagnostic"
        if resampling_event is not None
        else "blocked_p8j_sir_ot_sinkhorn_diagnostic_no_resampling_event"
    )
    return {
        "schema_version": "filter_bench.p8j_sir_ot_sinkhorn_diagnostic.v1",
        "phase": "P8J_PHASE5B_SIR_TUNING_BLOCKER_REPAIR",
        "status": status,
        "evidence_contract": {
            "question": "What cost, state, weight, and Sinkhorn residual scales explain the P8j SIR d18 LEDH OT Phase 5 failure?",
            "baseline": "Phase 5 LEDH OT first failure at seed 81120 with P8h Sinkhorn settings.",
            "primary_criterion": "Record first resampling event scale and whether a bounded scale-adaptive epsilon probe is a plausible reviewed repair candidate.",
            "not_concluded": [
                "particle adequacy",
                "leaderboard completion",
                "selected LEDH OT repair",
                "gradient correctness",
                "HMC/NUTS readiness",
                "Zhao-Cui TT/SIRT source-faithfulness",
                "production readiness",
            ],
        },
        "run_manifest": {
            "git_commit": _git_commit(),
            "dirty_state_summary": _dirty_summary(),
            "command": " ".join(sys.argv),
            "environment": "TensorFlow/TensorFlow Probability P8j Phase 5b Sinkhorn diagnostic",
            "requested_device": device,
            "device_context": device_name,
            "marker_device": marker_device,
            "tf_physical_gpus": [gpu.name for gpu in tf.config.list_physical_devices("GPU")],
            "tf_logical_gpus": [gpu.name for gpu in tf.config.list_logical_devices("GPU")],
            "g0_manifest": _rel(g0_manifest) if g0_manifest is not None else None,
            "wall_seconds": round(time.perf_counter() - started, 6),
            "runtime_budget_seconds": float(runtime_budget_seconds),
        },
        "scope": {
            "row_id": row_id,
            "route_label": route_label,
            "algorithm_id": LEDH_ALG1_DPF,
            "route_variant": P8J_ROUTE_VARIANT,
            "resampling_route": resampling_route,
            "full_horizon": int(full_horizon),
            "horizon_prefix": int(horizon),
            "particle_count": int(particle_count),
            "seed": int(seed),
            "ess_threshold_ratio": float(ess_threshold_ratio),
            "nominal_sinkhorn_epsilon": float(sinkhorn_epsilon),
            "nominal_sinkhorn_iterations": int(sinkhorn_iterations),
            "nominal_sinkhorn_tolerance": float(sinkhorn_tolerance),
        },
        "resampling_event": resampling_event,
        "sinkhorn_failure": sinkhorn_failure,
        "scale_adaptive_probe": sinkhorn_repaired_probe,
        "prefix_log_likelihood_before_event": _tf_float(log_likelihood),
        "repair_classification": (
            "candidate_requires_review_before_phase5_rerun"
            if sinkhorn_repaired_probe and sinkhorn_repaired_probe.get("finite") is True
            else "preserve_blocker_or_request_additional_repair_design"
        ),
        "nonclaims": [
            "diagnostic only",
            "not a Phase 5 rerun",
            "not a selected particle count",
            "not a selected LEDH OT repair",
            "not leaderboard evidence",
            "not gradient or HMC evidence",
        ],
    }


def _p8g_scalar_sv_gradient_value(
    theta: tf.Tensor,
    *,
    observations: tf.Tensor,
    seed: int,
    particle_count: int,
) -> Mapping[str, tf.Tensor]:
    theta = tf.reshape(tf.cast(theta, tf.float64), [2])
    gamma = _normal01().cdf(theta[0])
    beta = tf.exp(theta[1])
    flow_observations = _log_square_surrogate_observations(observations) - 2.0 * tf.math.log(beta)
    return ledh_pfpf_alg1_scalar_sv_graph_log_likelihood_tf(
        flow_observations=flow_observations,
        raw_observations=observations,
        gamma=gamma,
        beta=beta,
        sigma=tf.constant(1.0, dtype=tf.float64),
        observation_variance=DPF_SV_LOG_SQUARE_SURROGATE_VARIANCE,
        seed=int(seed),
        num_particles=int(particle_count),
        pseudo_time_steps=tf.constant([1.0], dtype=tf.float64),
        jit_compile=False,
    )


def _p8g_scalar_sv_value_and_gradient(
    theta: tf.Tensor,
    *,
    observations: tf.Tensor,
    seed: int,
    particle_count: int,
) -> tuple[Mapping[str, tf.Tensor], tf.Tensor | None]:
    theta = tf.convert_to_tensor(theta, dtype=tf.float64)
    with tf.GradientTape() as tape:
        tape.watch(theta)
        result = _p8g_scalar_sv_gradient_value(
            theta,
            observations=observations,
            seed=int(seed),
            particle_count=int(particle_count),
        )
        value = tf.convert_to_tensor(result["log_likelihood"], dtype=tf.float64)
    gradient = tape.gradient(value, theta)
    return result, gradient


def _p8g_fixed_randomness_gradient_check(
    *,
    rows: list[str],
    horizon: int,
    particle_count: int,
    seeds: list[int],
    route_variant: str,
    coordinate: str,
    device: str,
    g0_manifest: Path | None,
) -> dict[str, Any]:
    if rows != [SV_ROW]:
        raise ValueError("G3 initial scope supports only actual_sv")
    if route_variant != "p8g_sv_scalar_graph":
        raise ValueError("G3 requires route variant p8g_sv_scalar_graph")
    if coordinate != "canonical_unconstrained":
        raise ValueError("G3 requires canonical_unconstrained coordinate")
    if horizon <= 0:
        raise ValueError("horizon must be positive")
    if particle_count <= 0:
        raise ValueError("particle count must be positive")
    if device not in {"cpu", "gpu"}:
        raise ValueError("device must be 'cpu' or 'gpu'")
    if device == "gpu" and g0_manifest is None:
        raise ValueError("trusted GPU gradient check requires --g0-manifest")

    raw_observations = _sv_observations()[:horizon]
    theta = tf.convert_to_tensor(_sv_theta(), dtype=tf.float64)
    device_name = "/GPU:0" if device == "gpu" else "/CPU:0"
    marker_device = None
    per_seed: list[dict[str, Any]] = []
    started = time.perf_counter()
    with tf.device(device_name):
        marker = tf.reduce_sum(tf.ones([2, 2], dtype=tf.float64))
        marker_device = marker.device
        for seed in seeds:
            seed_started = time.perf_counter()
            first, gradient = _p8g_scalar_sv_value_and_gradient(
                theta,
                observations=raw_observations,
                seed=int(seed),
                particle_count=int(particle_count),
            )
            repeat, repeat_gradient = _p8g_scalar_sv_value_and_gradient(
                theta,
                observations=raw_observations,
                seed=int(seed),
                particle_count=int(particle_count),
            )

            def value_fn(current_theta: tf.Tensor) -> tf.Tensor:
                return tf.convert_to_tensor(
                    _p8g_scalar_sv_gradient_value(
                        current_theta,
                        observations=raw_observations,
                        seed=int(seed),
                        particle_count=int(particle_count),
                    )["log_likelihood"],
                    dtype=tf.float64,
                )

            finite_difference = _finite_difference_score(value_fn, theta, step=1e-4)
            if gradient is None or repeat_gradient is None:
                gradient_tensor = None
                repeat_gradient_tensor = None
                gradient_finite = False
                directional_residual = None
                max_abs_fd_residual = None
            else:
                gradient_tensor = tf.convert_to_tensor(gradient, dtype=tf.float64)
                repeat_gradient_tensor = tf.convert_to_tensor(repeat_gradient, dtype=tf.float64)
                gradient_finite = bool(tf.reduce_all(tf.math.is_finite(gradient_tensor)).numpy())
                residual = gradient_tensor - finite_difference
                directions = tf.constant(
                    [
                        [1.0, 0.0],
                        [0.0, 1.0],
                        [1.0, 1.0],
                        [1.0, -1.0],
                    ],
                    dtype=tf.float64,
                )
                directional_residual = tf.linalg.matvec(directions, residual)
                max_abs_fd_residual = tf.reduce_max(tf.abs(residual))
            value = tf.convert_to_tensor(first["log_likelihood"], dtype=tf.float64)
            repeat_value = tf.convert_to_tensor(repeat["log_likelihood"], dtype=tf.float64)
            ess_min = tf.convert_to_tensor(first["ess_min"], dtype=tf.float64)
            ess_mean = tf.convert_to_tensor(first["ess_mean"], dtype=tf.float64)
            per_seed.append(
                {
                    "seed": int(seed),
                    "runtime_seconds": round(time.perf_counter() - seed_started, 6),
                    "log_likelihood": _tf_float(value),
                    "repeat_log_likelihood": _tf_float(repeat_value),
                    "repeat_value_abs_delta": _tf_float(tf.abs(value - repeat_value)),
                    "gradient": _tensor_list(gradient_tensor) if gradient_tensor is not None else None,
                    "repeat_gradient": (
                        _tensor_list(repeat_gradient_tensor)
                        if repeat_gradient_tensor is not None
                        else None
                    ),
                    "finite_difference_gradient": _tensor_list(finite_difference),
                    "gradient_l2_norm": (
                        _tf_float(tf.linalg.norm(gradient_tensor))
                        if gradient_tensor is not None
                        else None
                    ),
                    "gradient_max_abs_fd_residual": (
                        _tf_float(max_abs_fd_residual)
                        if max_abs_fd_residual is not None
                        else None
                    ),
                    "directional_fd_residuals": (
                        _tensor_list(directional_residual)
                        if directional_residual is not None
                        else None
                    ),
                    "repeat_gradient_max_abs_delta": (
                        _tf_float(tf.reduce_max(tf.abs(gradient_tensor - repeat_gradient_tensor)))
                        if gradient_tensor is not None and repeat_gradient_tensor is not None
                        else None
                    ),
                    "finite": bool(first["finite"].numpy()) and bool(tf.math.is_finite(value).numpy()),
                    "gradient_finite": gradient_finite,
                    "ess_min": _tf_float(ess_min),
                    "ess_mean": _tf_float(ess_mean),
                    "value_device": value.device,
                    "gradient_device": (
                        gradient_tensor.device if gradient_tensor is not None else None
                    ),
                    "coordinate": coordinate,
                    "route_variant": route_variant,
                    "randomness_contract": "stateless_normals_precomputed_outside_xla_seed_salts_110_and_1110_plus_t",
                    "resampling_route": "none",
                    "time_loop_route": "tf_while_loop",
                    "particle_batch_route": "closed_form_scalar_vector_ops",
                }
            )

    values = tf.constant([entry["log_likelihood"] for entry in per_seed], dtype=tf.float64)
    gradients = [
        entry["gradient"]
        for entry in per_seed
        if entry["gradient"] is not None
    ]
    gradient_tensor = (
        tf.constant(gradients, dtype=tf.float64)
        if gradients
        else tf.zeros([0, 2], dtype=tf.float64)
    )
    max_fd_residuals = [
        entry["gradient_max_abs_fd_residual"]
        for entry in per_seed
        if entry["gradient_max_abs_fd_residual"] is not None
    ]
    max_repeat_gradient_delta = [
        entry["repeat_gradient_max_abs_delta"]
        for entry in per_seed
        if entry["repeat_gradient_max_abs_delta"] is not None
    ]
    status = (
        "executed_p8g_fixed_randomness_gradient_check"
        if all(entry["finite"] and entry["gradient_finite"] for entry in per_seed)
        else "blocked_p8g_fixed_randomness_gradient_check_nonfinite"
    )
    return {
        "schema_version": "filter_bench.p8g_fixed_randomness_gradient.v1",
        "phase": "P8G_G3_FIXED_RANDOMNESS_GRADIENT",
        "status": status,
        "evidence_contract": {
            "question": "Does the fixed-randomness/no-resampling LEDH surrogate objective provide stable, finite, coordinate-consistent gradients?",
            "baseline": "Reviewed G2b scalar-SV graph value path and finite-difference diagnostics on the same fixed random draws.",
            "primary_criterion": "Finite stable gradients pass repeatability and directional finite-difference checks in canonical_unconstrained coordinate.",
            "veto_diagnostics": [
                "gradient through resampling branch",
                "missing seed/salt contract",
                "parameterization mismatch",
                "finite value treated as gradient correctness",
                "non-finite or unstable gradients",
            ],
            "not_concluded": [
                "stochastic PF target gradient correctness",
                "production HMC readiness",
                "final filter ranking",
                "generic high-dimensional Algorithm 1 gradient readiness",
            ],
        },
        "run_manifest": {
            "git_commit": _git_commit(),
            "dirty_state_summary": _dirty_summary(),
            "command": " ".join(sys.argv),
            "environment": "TensorFlow/TensorFlow Probability fixed-randomness gradient harness",
            "cuda_visible_devices": str(__import__("os").environ.get("CUDA_VISIBLE_DEVICES")),
            "requested_device": device,
            "device_context": device_name,
            "marker_device": marker_device,
            "tf_physical_gpus": [gpu.name for gpu in tf.config.list_physical_devices("GPU")],
            "tf_logical_gpus": [gpu.name for gpu in tf.config.list_logical_devices("GPU")],
            "g0_manifest": _rel(g0_manifest) if g0_manifest is not None else None,
            "plan": "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-subplan-2026-06-15.md",
            "g2b_result": "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-repair-result-2026-06-15.md",
        },
        "scope": {
            "rows": rows,
            "row_id": SV_ROW,
            "horizon_prefix": int(horizon),
            "particle_count": int(particle_count),
            "seeds": [int(seed) for seed in seeds],
            "seed_count": len(seeds),
            "route_variant": route_variant,
            "coordinate": coordinate,
            "theta": _tensor_list(theta),
            "theta_coordinate_meaning": "theta=(Phi^{-1}(gamma), log(beta)); sigma fixed at 1.0",
            "resampling_route": "none",
        },
        "summary": {
            "mean_log_likelihood": _tf_float(tf.reduce_mean(values)),
            "sample_standard_deviation": (
                _tf_float(
                    tf.math.reduce_std(values)
                    * tf.sqrt(
                        tf.cast(len(per_seed), tf.float64)
                        / tf.cast(max(len(per_seed) - 1, 1), tf.float64)
                    )
                )
                if len(per_seed) > 1
                else 0.0
            ),
            "mean_gradient": (
                _tensor_list(tf.reduce_mean(gradient_tensor, axis=0))
                if int(gradient_tensor.shape[0]) > 0
                else None
            ),
            "max_abs_fd_residual": max(max_fd_residuals) if max_fd_residuals else None,
            "max_repeat_gradient_abs_delta": (
                max(max_repeat_gradient_delta) if max_repeat_gradient_delta else None
            ),
            "all_values_finite": all(entry["finite"] for entry in per_seed),
            "all_gradients_finite": all(entry["gradient_finite"] for entry in per_seed),
        },
        "device_diagnostics": {
            "devices_used_by_value_tensors": sorted({entry["value_device"] for entry in per_seed}),
            "devices_used_by_gradient_tensors": sorted(
                {str(entry["gradient_device"]) for entry in per_seed if entry["gradient_device"] is not None}
            ),
            "no_silent_cpu_fallback_claim": device == "gpu"
            and any("GPU" in str(entry["value_device"]) for entry in per_seed),
        },
        "per_seed_results": per_seed,
        "nonclaims": [
            "fixed-randomness/no-resampling conditional surrogate only",
            "not the stochastic PF marginal likelihood gradient",
            "not HMC readiness",
            "not tuned particle-count evidence",
            "not a filter ranking",
            "not generalized-SV or high-dimensional Algorithm 1 gradient evidence",
        ],
    }


def _p8h_ot_scalar_sv_gradient_value(
    theta: tf.Tensor,
    *,
    horizon: int,
    seed: int,
    particle_count: int,
    resampling_route: str,
) -> Any:
    theta = tf.reshape(tf.cast(theta, tf.float64), [2])
    callbacks = _dpf_sv_callbacks(theta)
    raw_observations = _sv_observations()[:horizon]
    ledh_observations = callbacks["ledh_flow_observations_fn"](raw_observations)

    def target_observation_log_density(points: tf.Tensor, observation: tf.Tensor, time_index: int) -> tf.Tensor:
        del observation
        return callbacks["observation_log_density_fn"](
            points,
            raw_observations[int(time_index)],
            int(time_index),
        )

    return run_ledh_pfpf_alg1_ukf_tf(
        observations=ledh_observations,
        initial_sample=callbacks["initial_sample"],
        initial_covariance=callbacks["initial_covariance"],
        transition_sample=callbacks["transition_sample"],
        transition_mean_fn=callbacks["transition_mean_fn"],
        transition_log_density_fn=callbacks["transition_log_density_fn"],
        observation_mean_fn=callbacks["observation_mean_fn"],
        observation_jacobian_fn=callbacks["observation_jacobian_fn"],
        observation_log_density_fn=target_observation_log_density,
        process_noise_covariance_fn=callbacks["process_noise_covariance_fn"],
        observation_covariance_fn=callbacks["observation_covariance_fn"],
        seed=int(seed),
        num_particles=int(particle_count),
        pseudo_time_steps=tf.constant([1.0], dtype=tf.float64),
        resampling_route=resampling_route,
        ess_threshold_ratio=1.01,
        sinkhorn_epsilon=1.0,
        sinkhorn_iterations=200,
        sinkhorn_tolerance=1e-6,
        method_id="ledh_pfpf_alg1_ukf_p8h_ot_gradient_actual_sv_raw_tf",
    )


def _p8h_ot_scalar_sv_value_and_gradient(
    theta: tf.Tensor,
    *,
    horizon: int,
    seed: int,
    particle_count: int,
    resampling_route: str,
) -> tuple[Any, tf.Tensor | None]:
    theta = tf.convert_to_tensor(theta, dtype=tf.float64)
    with tf.GradientTape() as tape:
        tape.watch(theta)
        result = _p8h_ot_scalar_sv_gradient_value(
            theta,
            horizon=int(horizon),
            seed=int(seed),
            particle_count=int(particle_count),
            resampling_route=resampling_route,
        )
        value = tf.convert_to_tensor(result.log_likelihood_estimate, dtype=tf.float64)
    gradient = tape.gradient(value, theta)
    return result, gradient


def _p8h_ot_gradient_check(
    *,
    rows: list[str],
    horizon: int,
    particle_count: int,
    seeds: list[int],
    resampling_route: str,
    coordinate: str,
    device: str,
    g0_manifest: Path | None,
    manifest_phase: str = "P8H_PHASE6_OT_GRADIENT_CHECKS",
    manifest_plan: Path | None = None,
    runtime_budget_seconds: float = P8G_G4_DEFAULT_RUNTIME_BUDGET_SECONDS,
    finite_difference_max_abs_threshold: float = 1e-5,
) -> dict[str, Any]:
    if rows != [SV_ROW]:
        raise ValueError("P8h Phase 6 initial scope supports only actual_sv")
    if resampling_route != P8H_DEFAULT_RESAMPLING_ROUTE:
        raise ValueError("P8h Phase 6 requires Sinkhorn covariance-carry route")
    if coordinate != "canonical_unconstrained":
        raise ValueError("P8h Phase 6 requires canonical_unconstrained coordinate")
    if horizon <= 0:
        raise ValueError("horizon must be positive")
    if particle_count != 5:
        raise ValueError("P8h Phase 6 must use the reviewed Phase 5 Stage 0 count N=5")
    if len(seeds) != 5:
        raise ValueError("P8h Phase 6 requires exactly five fixed seeds")
    if device != "gpu":
        raise ValueError("P8h/P8i OT gradient gate requires trusted GPU")
    if g0_manifest is None:
        raise ValueError("trusted GPU P8h gradient check requires --g0-manifest")
    if float(runtime_budget_seconds) <= 0.0:
        raise ValueError("runtime budget must be positive")
    if float(finite_difference_max_abs_threshold) < 0.0:
        raise ValueError("finite-difference threshold must be nonnegative")

    theta = tf.convert_to_tensor(_sv_theta(), dtype=tf.float64)
    device_name = "/GPU:0" if device == "gpu" else "/CPU:0"
    marker_device = None
    per_seed: list[dict[str, Any]] = []
    started = time.perf_counter()
    with tf.device(device_name):
        marker = tf.reduce_sum(tf.ones([2, 2], dtype=tf.float64))
        marker_device = marker.device
        for seed in seeds:
            seed_started = time.perf_counter()
            first, gradient = _p8h_ot_scalar_sv_value_and_gradient(
                theta,
                horizon=int(horizon),
                seed=int(seed),
                particle_count=int(particle_count),
                resampling_route=resampling_route,
            )
            repeat, repeat_gradient = _p8h_ot_scalar_sv_value_and_gradient(
                theta,
                horizon=int(horizon),
                seed=int(seed),
                particle_count=int(particle_count),
                resampling_route=resampling_route,
            )

            def value_fn(current_theta: tf.Tensor) -> tf.Tensor:
                return tf.convert_to_tensor(
                    _p8h_ot_scalar_sv_gradient_value(
                        current_theta,
                        horizon=int(horizon),
                        seed=int(seed),
                        particle_count=int(particle_count),
                        resampling_route=resampling_route,
                    ).log_likelihood_estimate,
                    dtype=tf.float64,
                )

            finite_difference = _finite_difference_score(value_fn, theta, step=1e-4)
            value = tf.convert_to_tensor(first.log_likelihood_estimate, dtype=tf.float64)
            repeat_value = tf.convert_to_tensor(repeat.log_likelihood_estimate, dtype=tf.float64)
            ess = tf.convert_to_tensor(first.ess_by_time, dtype=tf.float64)
            first_diag = next(
                (
                    diag
                    for diag in first.resampling_diagnostics
                    if bool(diag.get("resampled", False))
                ),
                {},
            )
            if gradient is None or repeat_gradient is None:
                gradient_tensor = None
                repeat_gradient_tensor = None
                gradient_finite = False
                max_abs_fd_residual = None
            else:
                gradient_tensor = tf.convert_to_tensor(gradient, dtype=tf.float64)
                repeat_gradient_tensor = tf.convert_to_tensor(repeat_gradient, dtype=tf.float64)
                gradient_finite = bool(tf.reduce_all(tf.math.is_finite(gradient_tensor)).numpy())
                max_abs_fd_residual = tf.reduce_max(tf.abs(gradient_tensor - finite_difference))
            repeat_gradient_delta = (
                _tf_float(tf.reduce_max(tf.abs(gradient_tensor - repeat_gradient_tensor)))
                if gradient_tensor is not None and repeat_gradient_tensor is not None
                else None
            )
            gradient_l2 = (
                _tf_float(tf.linalg.norm(gradient_tensor))
                if gradient_tensor is not None
                else None
            )
            gradient_connected = gradient_tensor is not None and gradient_l2 is not None and gradient_l2 > 0.0
            per_seed.append(
                {
                    "seed": int(seed),
                    "runtime_seconds": round(time.perf_counter() - seed_started, 6),
                    "log_likelihood": _tf_float(value),
                    "repeat_log_likelihood": _tf_float(repeat_value),
                    "repeat_value_abs_delta": _tf_float(tf.abs(value - repeat_value)),
                    "gradient": _tensor_list(gradient_tensor) if gradient_tensor is not None else None,
                    "repeat_gradient": (
                        _tensor_list(repeat_gradient_tensor)
                        if repeat_gradient_tensor is not None
                        else None
                    ),
                    "finite_difference_gradient": _tensor_list(finite_difference),
                    "gradient_l2_norm": gradient_l2,
                    "gradient_max_abs_fd_residual": (
                        _tf_float(max_abs_fd_residual)
                        if max_abs_fd_residual is not None
                        else None
                    ),
                    "repeat_gradient_max_abs_delta": repeat_gradient_delta,
                    "finite": bool(first.finite) and bool(tf.math.is_finite(value).numpy()),
                    "gradient_finite": gradient_finite,
                    "gradient_connected": bool(gradient_connected),
                    "ess_min": _tf_float(tf.reduce_min(ess)),
                    "ess_mean": _tf_float(tf.reduce_mean(ess)),
                    "value_device": value.device,
                    "gradient_device": (
                        gradient_tensor.device if gradient_tensor is not None else None
                    ),
                    "coordinate": coordinate,
                    "route_variant": first.route_identifiers.get("route_variant"),
                    "resampling_route": first.route_identifiers.get("resampling_route"),
                    "resampling_count": int(first.resampling_count),
                    "first_resampling_diagnostics": first_diag,
                    "randomness_contract": "stateless_normals_inside_algorithm_seed_salts_fixed_by_seed_and_time",
                    "gradient_claim_scope": "AD gradient through declared relaxed Sinkhorn OT graph under fixed seeds",
                }
            )

    values = tf.constant([entry["log_likelihood"] for entry in per_seed], dtype=tf.float64)
    gradients = [entry["gradient"] for entry in per_seed if entry["gradient"] is not None]
    gradient_tensor = (
        tf.constant(gradients, dtype=tf.float64)
        if gradients
        else tf.zeros([0, 2], dtype=tf.float64)
    )
    max_fd_residuals = [
        entry["gradient_max_abs_fd_residual"]
        for entry in per_seed
        if entry["gradient_max_abs_fd_residual"] is not None
    ]
    repeat_gradient_deltas = [
        entry["repeat_gradient_max_abs_delta"]
        for entry in per_seed
        if entry["repeat_gradient_max_abs_delta"] is not None
    ]
    max_fd_residual = max(max_fd_residuals) if max_fd_residuals else None
    max_repeat_gradient_delta = max(repeat_gradient_deltas) if repeat_gradient_deltas else None
    wall_time_seconds = round(time.perf_counter() - started, 6)
    value_devices = sorted({entry["value_device"] for entry in per_seed})
    gradient_devices = sorted(
        {str(entry["gradient_device"]) for entry in per_seed if entry["gradient_device"] is not None}
    )
    trusted_device = (
        marker_device is not None
        and _tensor_device_is_gpu(marker_device)
        and bool(value_devices)
        and bool(gradient_devices)
        and all(_tensor_device_is_gpu(item) for item in value_devices)
        and all(_tensor_device_is_gpu(item) for item in gradient_devices)
    )
    fd_residual_within_threshold = (
        max_fd_residual is not None
        and math.isfinite(float(max_fd_residual))
        and float(max_fd_residual) <= float(finite_difference_max_abs_threshold)
    )
    runtime_within_budget = wall_time_seconds <= float(runtime_budget_seconds)
    core_gradient_pass = all(
        entry["finite"] and entry["gradient_finite"] and entry["gradient_connected"]
        for entry in per_seed
    )
    status_pass = (
        core_gradient_pass
        and fd_residual_within_threshold
        and trusted_device
        and runtime_within_budget
    )
    blocker_reasons: list[str] = []
    if not core_gradient_pass:
        blocker_reasons.append("BLOCK_P8H_OT_GRADIENT_CORE_FINITE_CONNECTED")
    if not fd_residual_within_threshold:
        blocker_reasons.append("BLOCK_P8H_OT_GRADIENT_FD_RESIDUAL")
    if not trusted_device:
        blocker_reasons.append("BLOCK_P8H_OT_GRADIENT_TRUSTED_DEVICE")
    if not runtime_within_budget:
        blocker_reasons.append("BLOCK_P8H_OT_GRADIENT_RUNTIME_BUDGET")
    status = "executed_p8h_ot_gradient_check" if status_pass else "blocked_p8h_ot_gradient_check"
    return {
        "schema_version": "filter_bench.p8h_ot_gradient.v1",
        "phase": manifest_phase,
        "status": status,
        "evidence_contract": {
            "question": "Are AD gradients finite, connected, and reproducible for the selected P8h OT-resampled scalar on trusted GPU?",
            "baseline": "Phase 5 selected Stage 0 route/count and Phase 4 route diagnostics; P8g no-resampling gradient smoke is context only.",
            "primary_criterion": "Finite non-None repeatable AD gradients through the relaxed Sinkhorn OT graph under fixed seeds, bounded finite-difference residual, trusted requested device, and runtime within budget.",
            "veto_diagnostics": [
                "disconnected gradient",
                "nonfinite gradient",
                "zero or missing gradient norm",
                "no-resampling detour",
                "missing trusted GPU evidence",
                "finite-difference residual above threshold",
                "runtime budget exceeded",
                "finite difference promoted to proof",
                "stochastic categorical resampling gradient claim",
            ],
            "not_concluded": [
                "stochastic PF marginal-gradient correctness",
                "HMC readiness",
                "GPU scaling",
                "full-horizon value adequacy",
                "filter ranking",
            ],
        },
        "run_manifest": {
            "git_commit": _git_commit(),
            "dirty_state_summary": _dirty_summary(),
            "command": " ".join(sys.argv),
            "environment": "TensorFlow/TensorFlow Probability P8h OT gradient harness",
            "cuda_visible_devices": str(__import__("os").environ.get("CUDA_VISIBLE_DEVICES")),
            "requested_device": device,
            "device_context": device_name,
            "marker_device": marker_device,
            "tf_physical_gpus": [gpu.name for gpu in tf.config.list_physical_devices("GPU")],
            "tf_logical_gpus": [gpu.name for gpu in tf.config.list_logical_devices("GPU")],
            "g0_manifest": _rel(g0_manifest) if g0_manifest is not None else None,
            "phase5_result": "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-result-2026-06-15.md",
            "phase6_plan": _rel(manifest_plan)
            if manifest_plan is not None
            else "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase6-ot-gradient-checks-subplan-2026-06-15.md",
            "runtime_budget_seconds": float(runtime_budget_seconds),
            "wall_time_seconds": wall_time_seconds,
        },
        "scope": {
            "rows": rows,
            "row_id": SV_ROW,
            "horizon_prefix": int(horizon),
            "particle_count": int(particle_count),
            "seeds": [int(seed) for seed in seeds],
            "seed_count": len(seeds),
            "route_variant": P8H_ROUTE_VARIANT,
            "resampling_route": resampling_route,
            "coordinate": coordinate,
            "theta": _tensor_list(theta),
            "theta_coordinate_meaning": "theta=(Phi^{-1}(gamma), log(beta)); sigma fixed at 1.0",
        },
        "summary": {
            "mean_log_likelihood": _tf_float(tf.reduce_mean(values)),
            "mean_gradient": (
                _tensor_list(tf.reduce_mean(gradient_tensor, axis=0))
                if int(gradient_tensor.shape[0]) > 0
                else None
            ),
            "max_abs_fd_residual": max_fd_residual,
            "max_repeat_gradient_abs_delta": max_repeat_gradient_delta,
            "all_values_finite": all(entry["finite"] for entry in per_seed),
            "all_gradients_finite": all(entry["gradient_finite"] for entry in per_seed),
            "all_gradients_connected": all(entry["gradient_connected"] for entry in per_seed),
        },
        "device_diagnostics": {
            "devices_used_by_value_tensors": value_devices,
            "devices_used_by_gradient_tensors": gradient_devices,
            "marker_device": marker_device,
            "trusted_requested_device": bool(trusted_device),
            "no_silent_cpu_fallback_claim": bool(trusted_device),
        },
        "gate_diagnostics": {
            "core_gradient_pass": bool(core_gradient_pass),
            "finite_difference_max_abs_threshold": float(finite_difference_max_abs_threshold),
            "fd_residual_within_threshold": bool(fd_residual_within_threshold),
            "runtime_budget_seconds": float(runtime_budget_seconds),
            "runtime_within_budget": bool(runtime_within_budget),
            "trusted_requested_device": bool(trusted_device),
            "status_pass": bool(status_pass),
        },
        "blocker": None
        if status_pass
        else {
            "reasons": blocker_reasons,
            "core_gradient_pass": bool(core_gradient_pass),
            "max_abs_fd_residual": max_fd_residual,
            "finite_difference_max_abs_threshold": float(finite_difference_max_abs_threshold),
            "trusted_requested_device": bool(trusted_device),
            "runtime_within_budget": bool(runtime_within_budget),
        },
        "per_seed_results": per_seed,
        "nonclaims": [
            "AD gradient through declared relaxed Sinkhorn OT graph only",
            "not the stochastic PF marginal likelihood gradient",
            "not categorical-resampling gradient evidence",
            "not HMC readiness",
            "not GPU scaling",
            "not a filter ranking",
        ],
    }


def _p8h_hmc_tier0_smoke(
    *,
    rows: list[str],
    algorithm_id: str,
    horizon: int,
    particle_count: int,
    seeds: list[int],
    resampling_route: str,
    coordinate: str,
    device: str,
    g0_manifest: Path | None,
    num_results: int,
    num_burnin_steps: int,
    step_size: float,
    num_leapfrog_steps: int,
    manifest_phase: str = "P8H_PHASE8_HMC_TIER0_SMOKE",
    manifest_plan: Path | None = None,
    runtime_budget_seconds: float = P8G_G4_DEFAULT_RUNTIME_BUDGET_SECONDS,
    hmc_policy_label: str = "fixed_kernel_no_adaptation_tier0_execution_smoke",
    hmc_tier_label: str = "tier0_execution_smoke",
    schema_version: str = "filter_bench.p8h_hmc_tier0.v1",
    status_success_label: str = "executed_p8h_hmc_tier0_smoke",
    status_blocked_label: str = "blocked_p8h_hmc_tier0_smoke",
    blocker_reason: str = "BLOCK_P8H_HMC_TIER0_SMOKE",
    evidence_question: str | None = None,
    evidence_baseline: str | None = None,
    evidence_primary_criterion: str | None = None,
    predecessor_results: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    if rows != [SV_ROW]:
        raise ValueError("P8h Phase 8 initial scope supports only actual_sv")
    if algorithm_id != LEDH_ALG1_DPF:
        raise ValueError("P8h Phase 8 supports only Algorithm 1 LEDH")
    if resampling_route != P8H_DEFAULT_RESAMPLING_ROUTE:
        raise ValueError("P8h Phase 8 requires Sinkhorn covariance-carry route")
    if coordinate != "canonical_unconstrained":
        raise ValueError("P8h Phase 8 requires canonical_unconstrained coordinate")
    if particle_count != 5:
        raise ValueError("P8h Phase 8 must use the reviewed Phase 5 Stage 0 count N=5")
    if len(seeds) != 1:
        raise ValueError("P8h Phase 8 Tier-0 smoke requires exactly one fixed PF seed")
    if device != "gpu":
        raise ValueError("P8h Phase 8 Tier-0 smoke success path requires trusted GPU")
    if g0_manifest is None:
        raise ValueError("trusted GPU P8h HMC smoke requires --g0-manifest")
    if horizon <= 0:
        raise ValueError("horizon must be positive")
    if int(num_results) <= 0 or int(num_burnin_steps) < 0:
        raise ValueError("HMC result count must be positive and burnin nonnegative")
    if int(num_leapfrog_steps) <= 0:
        raise ValueError("HMC leapfrog steps must be positive")
    hmc_step = float(step_size)
    if not math.isfinite(hmc_step) or hmc_step <= 0.0:
        raise ValueError("HMC step size must be positive and finite")
    if float(runtime_budget_seconds) <= 0.0:
        raise ValueError("runtime budget must be positive")

    pf_seed = int(seeds[0])
    hmc_seed = [int(pf_seed), int(pf_seed + 1000)]
    theta0 = tf.convert_to_tensor(_sv_theta(), dtype=tf.float64)
    device_name = "/GPU:0"
    marker_device = None
    started = time.perf_counter()
    hmc_error: dict[str, str] | None = None
    trace: Mapping[str, Any] | None = None
    samples: tf.Tensor | None = None
    initial_value = None
    initial_gradient = None
    initial_gradient_norm = None
    initial_result = None
    devices_used: set[str] = set()

    with tf.device(device_name):
        marker = tf.reduce_sum(tf.ones([2, 2], dtype=tf.float64))
        marker_device = marker.device
        try:
            initial_result, initial_gradient = _p8h_ot_scalar_sv_value_and_gradient(
                theta0,
                horizon=int(horizon),
                seed=pf_seed,
                particle_count=int(particle_count),
                resampling_route=resampling_route,
            )
            initial_value = tf.convert_to_tensor(
                initial_result.log_likelihood_estimate,
                dtype=tf.float64,
            )
            devices_used.add(str(initial_value.device))
            if initial_gradient is not None:
                initial_gradient = tf.convert_to_tensor(initial_gradient, dtype=tf.float64)
                initial_gradient_norm = tf.linalg.norm(initial_gradient)
                devices_used.add(str(initial_gradient.device))

            def target_log_prob(current_theta: tf.Tensor) -> tf.Tensor:
                result = _p8h_ot_scalar_sv_gradient_value(
                    current_theta,
                    horizon=int(horizon),
                    seed=pf_seed,
                    particle_count=int(particle_count),
                    resampling_route=resampling_route,
                )
                return tf.convert_to_tensor(
                    result.log_likelihood_estimate,
                    dtype=tf.float64,
                )

            kernel = tfp.mcmc.HamiltonianMonteCarlo(
                target_log_prob_fn=target_log_prob,
                step_size=tf.constant(hmc_step, dtype=tf.float64),
                num_leapfrog_steps=int(num_leapfrog_steps),
            )

            def trace_fn(_state: Any, kernel_results: Any) -> Mapping[str, Any]:
                return {
                    "is_accepted": kernel_results.is_accepted,
                    "log_accept_ratio": kernel_results.log_accept_ratio,
                    "target_log_prob": kernel_results.accepted_results.target_log_prob,
                }

            samples, trace = tfp.mcmc.sample_chain(
                num_results=int(num_results),
                num_burnin_steps=int(num_burnin_steps),
                current_state=theta0,
                kernel=kernel,
                trace_fn=trace_fn,
                seed=tf.constant(hmc_seed, dtype=tf.int32),
            )
            samples = tf.convert_to_tensor(samples, dtype=tf.float64)
            devices_used.add(str(samples.device))
            for key in ("log_accept_ratio", "target_log_prob"):
                if trace is not None and key in trace:
                    devices_used.add(str(tf.convert_to_tensor(trace[key]).device))
        except Exception as exc:  # pragma: no cover - exercised by monkeypatch.
            hmc_error = {
                "class": exc.__class__.__name__,
                "message": str(exc),
            }

    initial_gradient_connected = (
        initial_gradient is not None
        and initial_gradient_norm is not None
        and _finite_tensor_bool(initial_gradient_norm)
        and _tf_float(initial_gradient_norm) > 0.0
    )
    initial_value_finite = initial_value is not None and _finite_tensor_bool(initial_value)
    initial_gradient_finite = (
        initial_gradient is not None and _finite_tensor_bool(initial_gradient)
    )
    sample_chain_returned = samples is not None and trace is not None
    samples_finite = sample_chain_returned and _finite_tensor_bool(samples)
    log_accept_ratio_finite = (
        sample_chain_returned
        and trace is not None
        and "log_accept_ratio" in trace
        and _finite_tensor_bool(trace["log_accept_ratio"])
    )
    target_log_prob_finite = (
        sample_chain_returned
        and trace is not None
        and "target_log_prob" in trace
        and _finite_tensor_bool(trace["target_log_prob"])
    )
    trusted_gpu = bool(devices_used) and all(_tensor_device_is_gpu(item) for item in devices_used)
    if marker_device is not None:
        trusted_gpu = trusted_gpu and _tensor_device_is_gpu(marker_device)
    wall_time_seconds = round(time.perf_counter() - started, 6)
    runtime_within_budget = wall_time_seconds <= float(runtime_budget_seconds)
    status_pass = (
        hmc_error is None
        and trusted_gpu
        and initial_value_finite
        and initial_gradient_finite
        and bool(initial_gradient_connected)
        and bool(samples_finite)
        and bool(log_accept_ratio_finite)
        and bool(target_log_prob_finite)
        and bool(runtime_within_budget)
    )
    status = status_success_label if status_pass else status_blocked_label

    trace_summary: dict[str, Any] = {
        "sample_chain_returned": bool(sample_chain_returned),
        "samples_finite": bool(samples_finite),
        "log_accept_ratio_finite": bool(log_accept_ratio_finite),
        "target_log_prob_finite": bool(target_log_prob_finite),
        "acceptance_rate": None,
        "sample_shape": None,
        "sample_displacement_l2": None,
        "min_target_log_prob": None,
        "max_target_log_prob": None,
        "min_log_accept_ratio": None,
        "max_log_accept_ratio": None,
    }
    if sample_chain_returned and samples is not None and trace is not None:
        accepted = tf.cast(trace["is_accepted"], tf.float64)
        trace_summary.update(
            {
                "acceptance_rate": _tf_float(tf.reduce_mean(accepted)),
                "sample_shape": [int(dim) for dim in samples.shape],
                "sample_displacement_l2": _tf_float(
                    tf.linalg.norm(samples[-1] - samples[0])
                )
                if int(samples.shape[0]) > 1
                else 0.0,
                "min_target_log_prob": _tf_float(tf.reduce_min(trace["target_log_prob"])),
                "max_target_log_prob": _tf_float(tf.reduce_max(trace["target_log_prob"])),
                "min_log_accept_ratio": _tf_float(tf.reduce_min(trace["log_accept_ratio"])),
                "max_log_accept_ratio": _tf_float(tf.reduce_max(trace["log_accept_ratio"])),
            }
        )

    first_diag = {}
    route_identifiers = {}
    if initial_result is not None:
        route_identifiers = dict(getattr(initial_result, "route_identifiers", {}))
        first_diag = next(
            (
                diag
                for diag in getattr(initial_result, "resampling_diagnostics", [])
                if bool(diag.get("resampled", False))
            ),
            {},
        )

    return {
        "schema_version": schema_version,
        "phase": manifest_phase,
        "status": status,
        "evidence_contract": {
            "question": evidence_question
            or "Can the selected P8h OT-resampled scalar-SV value/gradient graph execute inside a tiny fixed-kernel TFP HMC chain on trusted GPU?",
            "baseline": evidence_baseline
            or "Reviewed Phase 5 selected route/count, reviewed Phase 6 OT-gradient scalar, and reviewed Phase 7 GPU feasibility profile.",
            "primary_criterion": evidence_primary_criterion
            or "Sample-chain execution with trusted GPU tensors, finite initial value/gradient, finite samples and trace log quantities, exact route/count/configuration, and no runtime/OOM blocker; otherwise explicit blocker.",
            "veto_diagnostics": [
                "missing reviewed route/count provenance",
                "no-resampling route",
                "wrong particle count",
                "untrusted GPU or CPU fallback",
                "HMC execution error without blocker classification",
                "nonfinite initial value or gradient",
                "disconnected gradient",
                "nonfinite samples",
                "nonfinite target log probability or log accept ratio",
            ],
            "not_concluded": [
                "production HMC readiness",
                "posterior convergence",
                "valid tuning",
                "NUTS readiness",
                "stochastic PF marginal-gradient correctness",
                "full-horizon HMC feasibility",
                "filter ranking",
                "default sampler policy",
            ],
        },
        "run_manifest": {
            "git_commit": _git_commit(),
            "dirty_state_summary": _dirty_summary(),
            "command": " ".join(sys.argv),
            "environment": f"TensorFlow/TensorFlow Probability {manifest_phase} fixed-kernel HMC diagnostic",
            "cuda_visible_devices": str(__import__("os").environ.get("CUDA_VISIBLE_DEVICES")),
            "requested_device": device,
            "device_context": device_name,
            "marker_device": marker_device,
            "tf_physical_gpus": [gpu.name for gpu in tf.config.list_physical_devices("GPU")],
            "tf_logical_gpus": [gpu.name for gpu in tf.config.list_logical_devices("GPU")],
            "g0_manifest": _rel(g0_manifest) if g0_manifest is not None else None,
            "predecessor_results": dict(predecessor_results)
            if predecessor_results is not None
            else {
                "phase5_result": "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-result-2026-06-15.md",
                "phase6_result": "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase6-ot-gradient-checks-result-2026-06-16.md",
                "phase7_result": "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-result-2026-06-16.md",
            },
            "plan": _rel(manifest_plan) if manifest_plan is not None else _rel(P8H_PHASE8_PLAN_PATH),
            "runtime_budget_seconds": float(runtime_budget_seconds),
            "wall_time_seconds": wall_time_seconds,
        },
        "scope": {
            "rows": rows,
            "row_id": SV_ROW,
            "algorithm_id": algorithm_id,
            "route_variant": P8H_ROUTE_VARIANT,
            "resampling_route": resampling_route,
            "coordinate": coordinate,
            "theta_initial": _tensor_list(theta0),
            "theta_coordinate_meaning": "theta=(Phi^{-1}(gamma), log(beta)); sigma fixed at 1.0",
            "horizon_prefix": int(horizon),
            "particle_count": int(particle_count),
            "pf_seed": pf_seed,
            "hmc_seed": hmc_seed,
            "hmc_kernel": "tfp.mcmc.HamiltonianMonteCarlo",
            "hmc_policy": hmc_policy_label,
            "hmc_tier": hmc_tier_label,
            "num_results": int(num_results),
            "num_burnin_steps": int(num_burnin_steps),
            "step_size": hmc_step,
            "num_leapfrog_steps": int(num_leapfrog_steps),
        },
        "initial_diagnostics": {
            "initial_log_likelihood": _tf_float(initial_value) if initial_value is not None else None,
            "initial_gradient": _tensor_list(initial_gradient) if initial_gradient is not None else None,
            "initial_gradient_l2_norm": (
                _tf_float(initial_gradient_norm)
                if initial_gradient_norm is not None
                else None
            ),
            "initial_value_finite": bool(initial_value_finite),
            "initial_gradient_finite": bool(initial_gradient_finite),
            "initial_gradient_connected": bool(initial_gradient_connected),
            "route_identifiers": route_identifiers,
            "first_resampling_diagnostics": first_diag,
        },
        "hmc_diagnostics": trace_summary,
        "device_diagnostics": {
            "trusted_gpu": bool(trusted_gpu),
            "devices_used_by_success_tensors": sorted(devices_used),
            "marker_device": marker_device,
            "no_silent_cpu_fallback_claim": bool(trusted_gpu),
        },
        "gate_diagnostics": {
            "runtime_budget_seconds": float(runtime_budget_seconds),
            "runtime_within_budget": bool(runtime_within_budget),
            "status_pass": bool(status_pass),
            "trusted_gpu": bool(trusted_gpu),
            "initial_value_finite": bool(initial_value_finite),
            "initial_gradient_finite": bool(initial_gradient_finite),
            "initial_gradient_connected": bool(initial_gradient_connected),
            "samples_finite": bool(samples_finite),
            "log_accept_ratio_finite": bool(log_accept_ratio_finite),
            "target_log_prob_finite": bool(target_log_prob_finite),
        },
        "blocker": None
        if status_pass
        else {
            "reason": blocker_reason,
            "hmc_error": hmc_error,
            "trusted_gpu": bool(trusted_gpu),
            "initial_value_finite": bool(initial_value_finite),
            "initial_gradient_finite": bool(initial_gradient_finite),
            "initial_gradient_connected": bool(initial_gradient_connected),
            "samples_finite": bool(samples_finite),
            "log_accept_ratio_finite": bool(log_accept_ratio_finite),
            "target_log_prob_finite": bool(target_log_prob_finite),
            "runtime_within_budget": bool(runtime_within_budget),
        },
        "nonclaims": [
            "Tier-0 fixed-kernel HMC execution smoke only",
            "not production HMC readiness",
            "not posterior convergence evidence",
            "not valid tuning evidence",
            "not NUTS readiness",
            "not stochastic PF marginal-gradient correctness",
            "not full-horizon HMC feasibility",
            "not a filter ranking",
            "not a default sampler policy",
        ],
    }


def _write_p8g_gradient_csv(path: Path, payload: dict[str, Any]) -> None:
    rows = payload["per_seed_results"]
    fieldnames = [
        "seed",
        "runtime_seconds",
        "log_likelihood",
        "repeat_log_likelihood",
        "repeat_value_abs_delta",
        "gradient",
        "repeat_gradient",
        "finite_difference_gradient",
        "gradient_l2_norm",
        "gradient_max_abs_fd_residual",
        "repeat_gradient_max_abs_delta",
        "finite",
        "gradient_finite",
        "ess_min",
        "ess_mean",
        "coordinate",
        "route_variant",
        "randomness_contract",
    ]
    _write_csv(path, rows, fieldnames)


def _write_p8h_gradient_csv(path: Path, payload: dict[str, Any]) -> None:
    rows = payload["per_seed_results"]
    fieldnames = [
        "seed",
        "runtime_seconds",
        "log_likelihood",
        "repeat_log_likelihood",
        "repeat_value_abs_delta",
        "gradient",
        "repeat_gradient",
        "finite_difference_gradient",
        "gradient_l2_norm",
        "gradient_max_abs_fd_residual",
        "repeat_gradient_max_abs_delta",
        "finite",
        "gradient_finite",
        "gradient_connected",
        "ess_min",
        "ess_mean",
        "coordinate",
        "route_variant",
        "resampling_route",
        "resampling_count",
        "randomness_contract",
        "gradient_claim_scope",
    ]
    _write_csv(path, rows, fieldnames)


def _write_p8h_hmc_tier0_csv(path: Path, payload: dict[str, Any]) -> None:
    row = {
        "status": payload["status"],
        "row_id": payload["scope"]["row_id"],
        "algorithm_id": payload["scope"]["algorithm_id"],
        "route_variant": payload["scope"]["route_variant"],
        "resampling_route": payload["scope"]["resampling_route"],
        "coordinate": payload["scope"]["coordinate"],
        "horizon_prefix": payload["scope"]["horizon_prefix"],
        "particle_count": payload["scope"]["particle_count"],
        "pf_seed": payload["scope"]["pf_seed"],
        "hmc_seed": json.dumps(payload["scope"]["hmc_seed"]),
        "num_results": payload["scope"]["num_results"],
        "num_burnin_steps": payload["scope"]["num_burnin_steps"],
        "step_size": payload["scope"]["step_size"],
        "num_leapfrog_steps": payload["scope"]["num_leapfrog_steps"],
        "trusted_gpu": payload["device_diagnostics"]["trusted_gpu"],
        "initial_value_finite": payload["initial_diagnostics"]["initial_value_finite"],
        "initial_gradient_finite": payload["initial_diagnostics"]["initial_gradient_finite"],
        "initial_gradient_connected": payload["initial_diagnostics"]["initial_gradient_connected"],
        "sample_chain_returned": payload["hmc_diagnostics"]["sample_chain_returned"],
        "samples_finite": payload["hmc_diagnostics"]["samples_finite"],
        "log_accept_ratio_finite": payload["hmc_diagnostics"]["log_accept_ratio_finite"],
        "target_log_prob_finite": payload["hmc_diagnostics"]["target_log_prob_finite"],
        "acceptance_rate": payload["hmc_diagnostics"]["acceptance_rate"],
        "sample_displacement_l2": payload["hmc_diagnostics"]["sample_displacement_l2"],
        "wall_time_seconds": payload["run_manifest"]["wall_time_seconds"],
        "blocker_reason": (
            payload["blocker"]["reason"] if payload.get("blocker") else None
        ),
    }
    _write_csv(
        path,
        [row],
        [
            "status",
            "row_id",
            "algorithm_id",
            "route_variant",
            "resampling_route",
            "coordinate",
            "horizon_prefix",
            "particle_count",
            "pf_seed",
            "hmc_seed",
            "num_results",
            "num_burnin_steps",
            "step_size",
            "num_leapfrog_steps",
            "trusted_gpu",
            "initial_value_finite",
            "initial_gradient_finite",
            "initial_gradient_connected",
            "sample_chain_returned",
            "samples_finite",
            "log_accept_ratio_finite",
            "target_log_prob_finite",
            "acceptance_rate",
            "sample_displacement_l2",
            "wall_time_seconds",
            "blocker_reason",
        ],
    )


def _p8g_g4_allowed_cell(row_id: str, algorithm_id: str, route_variant: str) -> bool:
    return (
        row_id == SV_ROW
        and algorithm_id == LEDH_ALG1_DPF
        and route_variant == P8G_ROUTE_VARIANT
    )


def _p8g_g4_deferred_record(
    *,
    row_id: str,
    algorithm_id: str,
    route_variant: str,
    reason: str,
) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "algorithm_id": algorithm_id,
        "route_variant": route_variant,
        "tuning_status": "deferred_not_in_initial_g4_scope",
        "selected_particle_count": None,
        "selection_rule": "not_evaluated_initial_actual_sv_scalar_graph_scope_only",
        "selection_rung": None,
        "next_rung_checked": False,
        "next_rung_particle_count": None,
        "adjacent_mean_delta": None,
        "adjacent_combined_mc_se": None,
        "min_relative_ess": None,
        "mean_relative_ess": None,
        "mc_standard_error": None,
        "mean_log_likelihood": None,
        "runtime_budget_status": "not_evaluated",
        "blocker_reason": reason,
        "full_horizon": ROW_HORIZONS.get(row_id),
        "horizon_prefix": None,
        "evaluated_particle_count": None,
        "finite": None,
        "runtime_seconds": None,
        "nonclaims": [
            "deferred row, not tuned particle-count evidence",
            "not a filter ranking",
            "not HMC readiness",
        ],
    }


def _p8g_g4_summarize_profile(
    profile: dict[str, Any],
    *,
    runtime_budget_seconds: float,
) -> dict[str, Any]:
    particle_count = int(profile["profile_scope"]["particle_count"])
    values = tf.constant(
        [entry["log_likelihood"] for entry in profile["per_seed_results"]],
        dtype=tf.float64,
    )
    ess_min_values = tf.constant(
        [entry["effective_sample_size_min"] for entry in profile["per_seed_results"]],
        dtype=tf.float64,
    )
    ess_mean_values = tf.constant(
        [entry["effective_sample_size_mean"] for entry in profile["per_seed_results"]],
        dtype=tf.float64,
    )
    finite = bool(
        profile["status"] == "executed_p8g_prefix_profile"
        and all(entry["finite"] for entry in profile["per_seed_results"])
    )
    min_relative_ess = tf.reduce_min(ess_min_values) / tf.cast(particle_count, tf.float64)
    mean_relative_ess = tf.reduce_mean(ess_mean_values) / tf.cast(particle_count, tf.float64)
    sample_sd = (
        tf.math.reduce_std(values)
        * tf.sqrt(tf.cast(len(values), tf.float64) / tf.cast(max(len(values) - 1, 1), tf.float64))
        if int(values.shape[0]) > 1
        else tf.constant(0.0, dtype=tf.float64)
    )
    mc_se = sample_sd / tf.sqrt(tf.cast(max(int(values.shape[0]), 1), tf.float64))
    wall_seconds = float(profile["timing"]["wall_seconds"])
    runtime_budget_status = (
        "within_budget"
        if wall_seconds <= runtime_budget_seconds
        else "exceeds_budget"
    )
    return {
        "row_id": profile["profile_scope"]["row_id"],
        "algorithm_id": profile["profile_scope"]["algorithm_id"],
        "route_variant": profile["profile_scope"]["route_variant"],
        "full_horizon": int(profile["profile_scope"]["full_horizon"]),
        "horizon_prefix": int(profile["profile_scope"]["horizon_prefix"]),
        "particle_count": particle_count,
        "seeds": list(profile["profile_scope"]["seeds"]),
        "seed_count": int(profile["profile_scope"]["seed_count"]),
        "finite": finite,
        "mean_log_likelihood": _tf_float(tf.reduce_mean(values)),
        "mean_average_log_likelihood": _tf_float(
            tf.reduce_mean(values) / tf.cast(profile["profile_scope"]["horizon_prefix"], tf.float64)
        ),
        "sample_standard_deviation": _tf_float(sample_sd),
        "mc_standard_error": _tf_float(mc_se),
        "min_relative_ess": _tf_float(min_relative_ess),
        "mean_relative_ess": _tf_float(mean_relative_ess),
        "runtime_seconds": wall_seconds,
        "runtime_budget_seconds": float(runtime_budget_seconds),
        "runtime_budget_status": runtime_budget_status,
        "status": profile["status"],
        "method_ids": [entry["method_id"] for entry in profile["per_seed_results"]],
        "per_seed_results": list(profile["per_seed_results"]),
    }


def _p8g_g4_profile_cell(
    *,
    row_id: str,
    algorithm_id: str,
    horizon: int,
    particle_count: int,
    seeds: list[int],
    device: str,
    g0_manifest: Path | None,
    route_variant: str,
    runtime_budget_seconds: float,
) -> dict[str, Any]:
    if route_variant != P8G_ROUTE_VARIANT:
        raise ValueError("G4 requires route variant p8g_sv_scalar_graph")
    profile = _p8g_profile_dpf_prefix(
        row_id=row_id,
        algorithm_id=algorithm_id,
        horizon=int(horizon),
        particle_count=int(particle_count),
        seeds=seeds,
        device=device,
        g0_manifest=g0_manifest,
        sv_scalar_graph=True,
    )
    return _p8g_g4_summarize_profile(
        profile,
        runtime_budget_seconds=float(runtime_budget_seconds),
    )


def _p8h_phase5_allowed_cell(
    row_id: str,
    algorithm_id: str,
    resampling_route: str,
) -> bool:
    return (
        row_id == SV_ROW
        and algorithm_id == LEDH_ALG1_DPF
        and resampling_route == P8H_DEFAULT_RESAMPLING_ROUTE
    )


def _p8h_phase5_transport_diagnostics_pass(profile: dict[str, Any]) -> bool:
    particle_count = int(profile["profile_scope"]["particle_count"])
    for entry in profile["per_seed_results"]:
        diagnostics = entry.get("first_resampling_diagnostics") or {}
        row_tolerance = float(
            diagnostics.get("canonical_transport_row_sum_tolerance", 0.0)
        )
        row_residual = float(
            diagnostics.get("canonical_transport_row_sum_residual", math.inf)
        )
        if diagnostics.get("resampling_route") != P8H_DEFAULT_RESAMPLING_ROUTE:
            return False
        if diagnostics.get("canonical_transport_matrix_convention") != "target_by_source_row_stochastic":
            return False
        if diagnostics.get("canonical_transport_shape") != [particle_count, particle_count]:
            return False
        if diagnostics.get("state_transport_shape") != [particle_count, particle_count]:
            return False
        if diagnostics.get("covariance_transport_shape") != [particle_count, particle_count]:
            return False
        if row_residual > row_tolerance:
            return False
        for key in (
            "finite_transport",
            "finite_particles",
            "finite_carried_covariances",
            "finite_corrected_log_weights",
            "finite_predicted_covariances",
            "finite_updated_covariances",
        ):
            if diagnostics.get(key) is not True:
                return False
    return True


def _p8h_phase5_summarize_profile(
    profile: dict[str, Any],
    *,
    runtime_budget_seconds: float,
) -> dict[str, Any]:
    particle_count = int(profile["profile_scope"]["particle_count"])
    values = tf.constant(
        [entry["log_likelihood"] for entry in profile["per_seed_results"]],
        dtype=tf.float64,
    )
    ess_min_values = tf.constant(
        [entry["effective_sample_size_min"] for entry in profile["per_seed_results"]],
        dtype=tf.float64,
    )
    ess_mean_values = tf.constant(
        [entry["effective_sample_size_mean"] for entry in profile["per_seed_results"]],
        dtype=tf.float64,
    )
    finite = bool(
        profile["status"] == "executed_p8h_ot_resampled_alg1_smoke"
        and all(entry["finite"] for entry in profile["per_seed_results"])
    )
    seed_count = int(profile["profile_scope"]["seed_count"])
    sample_sd = (
        tf.math.reduce_std(values)
        * tf.sqrt(tf.cast(seed_count, tf.float64) / tf.cast(max(seed_count - 1, 1), tf.float64))
        if seed_count > 1
        else tf.constant(0.0, dtype=tf.float64)
    )
    mc_se = sample_sd / tf.sqrt(tf.cast(max(seed_count, 1), tf.float64))
    wall_seconds = float(profile["run_manifest"]["wall_seconds"])
    runtime_budget_status = (
        "within_budget"
        if wall_seconds <= runtime_budget_seconds
        else "exceeds_budget"
    )
    devices = list(profile["device_diagnostics"]["devices_used_by_result_tensors"])
    trusted_gpu = (
        profile["run_manifest"]["requested_device"] == "gpu"
        and bool(profile["device_diagnostics"]["no_silent_cpu_fallback_claim"])
        and any("GPU" in str(device) for device in devices)
    )
    return {
        "row_id": profile["profile_scope"]["row_id"],
        "algorithm_id": profile["profile_scope"]["algorithm_id"],
        "route_variant": profile["profile_scope"]["route_variant"],
        "resampling_route": profile["profile_scope"]["resampling_route"],
        "full_horizon": int(profile["profile_scope"]["full_horizon"]),
        "horizon_prefix": int(profile["profile_scope"]["horizon_prefix"]),
        "particle_count": particle_count,
        "seeds": list(profile["profile_scope"]["seeds"]),
        "seed_count": seed_count,
        "finite": finite,
        "transport_diagnostics_pass": _p8h_phase5_transport_diagnostics_pass(profile),
        "trusted_gpu": trusted_gpu,
        "mean_log_likelihood": _tf_float(tf.reduce_mean(values)),
        "mean_average_log_likelihood": _tf_float(
            tf.reduce_mean(values) / tf.cast(profile["profile_scope"]["horizon_prefix"], tf.float64)
        ),
        "sample_standard_deviation": _tf_float(sample_sd),
        "mc_standard_error": _tf_float(mc_se),
        "min_relative_ess": _tf_float(
            tf.reduce_min(ess_min_values) / tf.cast(particle_count, tf.float64)
        ),
        "mean_relative_ess": _tf_float(
            tf.reduce_mean(ess_mean_values) / tf.cast(particle_count, tf.float64)
        ),
        "runtime_seconds": wall_seconds,
        "runtime_budget_seconds": float(runtime_budget_seconds),
        "runtime_budget_status": runtime_budget_status,
        "status": profile["status"],
        "method_ids": [entry["method_id"] for entry in profile["per_seed_results"]],
        "devices_used_by_result_tensors": devices,
        "per_seed_results": list(profile["per_seed_results"]),
    }


def _p8h_phase5_profile_cell(
    *,
    row_id: str,
    algorithm_id: str,
    horizon: int,
    particle_count: int,
    seeds: list[int],
    device: str,
    g0_manifest: Path | None,
    resampling_route: str,
    runtime_budget_seconds: float,
) -> dict[str, Any]:
    if not _p8h_phase5_allowed_cell(row_id, algorithm_id, resampling_route):
        raise ValueError("P8h Phase 5 initial scope requires actual-SV Algorithm 1 Sinkhorn OT route")
    profile = _p8h_profile_dpf_prefix(
        row_id=row_id,
        algorithm_id=algorithm_id,
        horizon=int(horizon),
        particle_count=int(particle_count),
        seeds=seeds,
        device=device,
        g0_manifest=g0_manifest,
        resampling_route=resampling_route,
    )
    return _p8h_phase5_summarize_profile(
        profile,
        runtime_budget_seconds=float(runtime_budget_seconds),
    )


def _p8j_phase5_allowed_cell(row_id: str, algorithm_id: str) -> bool:
    return row_id == SIR_ROW and algorithm_id in {BOOTSTRAP_DPF, LEDH_ALG1_DPF}


def _p8j_phase5_summarize_profile(
    profile: dict[str, Any],
    *,
    runtime_budget_seconds: float,
) -> dict[str, Any]:
    particle_count = int(profile["profile_scope"]["particle_count"])
    algorithm_id = profile["profile_scope"]["algorithm_id"]
    finite = bool(
        profile["status"] == "executed_p8j_sir_profile"
        and all(entry["finite"] for entry in profile["per_seed_results"])
        and len(profile["per_seed_results"]) == int(profile["profile_scope"]["seed_count"])
    )
    successful_entries = [
        entry for entry in profile["per_seed_results"]
        if entry.get("finite") is True and entry.get("log_likelihood") is not None
    ]
    failed_entries = [
        entry for entry in profile["per_seed_results"] if entry.get("finite") is not True
    ]
    values = tf.constant(
        [entry["log_likelihood"] for entry in successful_entries] or [0.0],
        dtype=tf.float64,
    )
    ess_min_values = tf.constant(
        [entry["effective_sample_size_min"] for entry in successful_entries] or [0.0],
        dtype=tf.float64,
    )
    ess_mean_values = tf.constant(
        [entry["effective_sample_size_mean"] for entry in successful_entries] or [0.0],
        dtype=tf.float64,
    )
    seed_count = int(profile["profile_scope"]["seed_count"])
    sample_sd = (
        tf.math.reduce_std(values)
        * tf.sqrt(tf.cast(seed_count, tf.float64) / tf.cast(max(seed_count - 1, 1), tf.float64))
        if finite and seed_count > 1
        else tf.constant(0.0, dtype=tf.float64)
    )
    mc_se = sample_sd / tf.sqrt(tf.cast(max(seed_count, 1), tf.float64))
    wall_seconds = float(profile["run_manifest"]["wall_seconds"])
    runtime_budget_status = (
        "within_budget"
        if wall_seconds <= runtime_budget_seconds
        else "exceeds_budget"
    )
    devices = list(profile["device_diagnostics"]["devices_used_by_result_tensors"])
    trusted_gpu = (
        profile["run_manifest"]["requested_device"] == "gpu"
        and bool(profile["device_diagnostics"]["no_silent_cpu_fallback_claim"])
        and any("GPU" in str(device) for device in devices)
    )
    transport_diagnostics_pass = (
        _p8h_phase5_transport_diagnostics_pass(profile)
        if algorithm_id == LEDH_ALG1_DPF and finite
        else True
    )
    if algorithm_id == LEDH_ALG1_DPF and not finite:
        transport_diagnostics_pass = False
    return {
        "row_id": profile["profile_scope"]["row_id"],
        "algorithm_id": algorithm_id,
        "route_variant": profile["profile_scope"]["route_variant"],
        "resampling_route": profile["profile_scope"]["resampling_route"],
        "full_horizon": int(profile["profile_scope"]["full_horizon"]),
        "horizon_prefix": int(profile["profile_scope"]["horizon_prefix"]),
        "particle_count": particle_count,
        "seeds": list(profile["profile_scope"]["seeds"]),
        "seed_count": seed_count,
        "finite": finite,
        "transport_diagnostics_pass": transport_diagnostics_pass,
        "trusted_gpu": trusted_gpu,
        "mean_log_likelihood": (
            _tf_float(tf.reduce_mean(values)) if finite else None
        ),
        "mean_average_log_likelihood": (
            _tf_float(
                tf.reduce_mean(values)
                / tf.cast(profile["profile_scope"]["horizon_prefix"], tf.float64)
            )
            if finite
            else None
        ),
        "sample_standard_deviation": _tf_float(sample_sd) if finite else None,
        "mc_standard_error": _tf_float(mc_se) if finite else None,
        "min_relative_ess": (
            _tf_float(tf.reduce_min(ess_min_values) / tf.cast(particle_count, tf.float64))
            if finite
            else None
        ),
        "mean_relative_ess": (
            _tf_float(tf.reduce_mean(ess_mean_values) / tf.cast(particle_count, tf.float64))
            if finite
            else None
        ),
        "runtime_seconds": wall_seconds,
        "runtime_budget_seconds": float(runtime_budget_seconds),
        "runtime_budget_status": runtime_budget_status,
        "status": profile["status"],
        "method_ids": [entry["method_id"] for entry in profile["per_seed_results"]],
        "failure_summaries": [
            {
                "seed": entry.get("seed"),
                "failure_error_type": entry.get("failure_error_type"),
                "failure_message": entry.get("failure_message"),
            }
            for entry in failed_entries
        ],
        "devices_used_by_result_tensors": devices,
        "per_seed_results": list(profile["per_seed_results"]),
    }


def _p8j_phase5_profile_cell(
    *,
    row_id: str,
    algorithm_id: str,
    horizon: int,
    particle_count: int,
    seeds: list[int],
    device: str,
    g0_manifest: Path | None,
    runtime_budget_seconds: float,
    sinkhorn_epsilon_policy: str = "fixed",
) -> dict[str, Any]:
    if not _p8j_phase5_allowed_cell(row_id, algorithm_id):
        raise ValueError("P8j Phase 5 tuning supports only SIR d18 DPF cells")
    profile = _p8j_sir_profile_dpf_prefix(
        row_id=row_id,
        algorithm_id=algorithm_id,
        horizon=int(horizon),
        particle_count=int(particle_count),
        seeds=seeds,
        device=device,
        g0_manifest=g0_manifest,
        runtime_budget_seconds=float(runtime_budget_seconds),
        sinkhorn_epsilon_policy=str(sinkhorn_epsilon_policy),
    )
    return _p8j_phase5_summarize_profile(
        profile,
        runtime_budget_seconds=float(runtime_budget_seconds),
    )


def _p8g_g4_particle_passes(rung: dict[str, Any]) -> bool:
    mc_se_limit = max(
        P8G_G4_MC_SE_ABS_FLOOR,
        P8G_G4_MC_SE_RELATIVE_FRACTION * abs(float(rung["mean_log_likelihood"])),
    )
    return (
        bool(rung["finite"])
        and float(rung["min_relative_ess"]) >= P8G_G4_RELATIVE_ESS_FLOOR
        and float(rung["mc_standard_error"]) <= mc_se_limit
        and rung["runtime_budget_status"] == "within_budget"
    )


def _p8h_phase5_rung_passes(rung: dict[str, Any]) -> bool:
    mc_se_limit = max(
        P8H_PHASE5_MC_SE_ABS_FLOOR,
        P8H_PHASE5_MC_SE_RELATIVE_FRACTION * abs(float(rung["mean_log_likelihood"])),
    )
    return (
        bool(rung["finite"])
        and bool(rung["transport_diagnostics_pass"])
        and bool(rung["trusted_gpu"])
        and int(rung["seed_count"]) == 5
        and rung["runtime_budget_status"] == "within_budget"
        and float(rung["mc_standard_error"]) <= mc_se_limit
    )


def _p8h_phase5_select_from_rungs(rungs: list[dict[str, Any]]) -> dict[str, Any]:
    if not rungs:
        raise ValueError("expected at least one rung")
    sorted_rungs = sorted(
        rungs,
        key=lambda item: (int(item["horizon_prefix"]), int(item["particle_count"])),
    )
    horizons = sorted({int(item["horizon_prefix"]) for item in sorted_rungs})
    particles = sorted({int(item["particle_count"]) for item in sorted_rungs})
    by_key = {
        (int(item["horizon_prefix"]), int(item["particle_count"])): item
        for item in sorted_rungs
    }
    blocker_reason = "BLOCK_P8H_PARTICLE_TUNING_NOT_CONVERGED"
    failed_reasons: set[str] = set()
    selected: dict[str, Any] | None = None

    for particle_index, particle_count in enumerate(particles):
        if particle_index + 1 >= len(particles):
            failed_reasons.add("BLOCK_P8H_PARTICLE_TUNING_MISSING_NEXT_RUNG")
            continue
        next_particle_count = particles[particle_index + 1]
        per_horizon_adjacent: list[dict[str, Any]] = []
        candidate_pass = True
        for horizon in horizons:
            rung = by_key.get((horizon, particle_count))
            next_rung = by_key.get((horizon, next_particle_count))
            if rung is None or next_rung is None:
                candidate_pass = False
                failed_reasons.add("BLOCK_P8H_PARTICLE_TUNING_MISSING_NEXT_RUNG")
                continue
            if not bool(rung["finite"]):
                candidate_pass = False
                failed_reasons.add("BLOCK_P8H_PARTICLE_TUNING_NONFINITE")
            if not bool(rung["transport_diagnostics_pass"]):
                candidate_pass = False
                failed_reasons.add("BLOCK_P8H_PARTICLE_TUNING_TRANSPORT")
            if not bool(rung["trusted_gpu"]):
                candidate_pass = False
                failed_reasons.add("BLOCK_P8H_PARTICLE_TUNING_GPU_EVIDENCE")
            if int(rung["seed_count"]) != 5:
                candidate_pass = False
                failed_reasons.add("BLOCK_P8H_PARTICLE_TUNING_SEED_COUNT")
            if rung["runtime_budget_status"] != "within_budget":
                candidate_pass = False
                failed_reasons.add("BLOCK_P8H_PARTICLE_TUNING_RUNTIME_BUDGET")
            if not _p8h_phase5_rung_passes(rung):
                mc_se_limit = max(
                    P8H_PHASE5_MC_SE_ABS_FLOOR,
                    P8H_PHASE5_MC_SE_RELATIVE_FRACTION
                    * abs(float(rung["mean_log_likelihood"])),
                )
                if float(rung["mc_standard_error"]) > mc_se_limit:
                    candidate_pass = False
                    failed_reasons.add("BLOCK_P8H_PARTICLE_TUNING_MC_SE")
            adjacent_mean_delta = abs(
                float(rung["mean_log_likelihood"])
                - float(next_rung["mean_log_likelihood"])
            )
            adjacent_combined_mc_se = math.sqrt(
                float(rung["mc_standard_error"]) ** 2
                + float(next_rung["mc_standard_error"]) ** 2
            )
            adjacent_threshold = (
                2.0 * adjacent_combined_mc_se
                + P8H_PHASE5_ADJACENT_DELTA_ABS_BUFFER
            )
            adjacent_pass = adjacent_mean_delta <= adjacent_threshold
            if not adjacent_pass:
                candidate_pass = False
                failed_reasons.add("BLOCK_P8H_PARTICLE_TUNING_ADJACENT_STABILITY")
            per_horizon_adjacent.append(
                {
                    "horizon_prefix": horizon,
                    "particle_count": particle_count,
                    "next_rung_particle_count": next_particle_count,
                    "adjacent_mean_delta": adjacent_mean_delta,
                    "adjacent_combined_mc_se": adjacent_combined_mc_se,
                    "adjacent_threshold": adjacent_threshold,
                    "adjacent_pass": adjacent_pass,
                }
            )
        if candidate_pass:
            first_rung = by_key[(horizons[0], particle_count)]
            selected = {
                "row_id": first_rung["row_id"],
                "algorithm_id": first_rung["algorithm_id"],
                "route_variant": first_rung["route_variant"],
                "resampling_route": first_rung["resampling_route"],
                "tuning_status": "selected_particle_count",
                "selected_particle_count": particle_count,
                "selection_rule": (
                    "smallest count passing finite, trusted-GPU, transport, "
                    "runtime, five-seed MC SE, and adjacent-rung Stage 0 gates"
                ),
                "selection_rung": particle_count,
                "next_rung_checked": True,
                "next_rung_particle_count": next_particle_count,
                "adjacent_horizon_summaries": per_horizon_adjacent,
                "blocker_reason": None,
                "evaluated_horizons": horizons,
                "evaluated_particle_counts": particles,
                "nonclaims": [
                    "Stage 0 prefix particle-count gate only",
                    "not full-horizon particle-count adequacy",
                    "not gradient correctness",
                    "not GPU scaling",
                    "not HMC readiness",
                    "not a filter ranking",
                ],
            }
            break

    if selected is not None:
        return selected

    terminal = sorted_rungs[-1]
    for priority_reason in (
        "BLOCK_P8H_PARTICLE_TUNING_NONFINITE",
        "BLOCK_P8H_PARTICLE_TUNING_TRANSPORT",
        "BLOCK_P8H_PARTICLE_TUNING_GPU_EVIDENCE",
        "BLOCK_P8H_PARTICLE_TUNING_RUNTIME_BUDGET",
        "BLOCK_P8H_PARTICLE_TUNING_SEED_COUNT",
        "BLOCK_P8H_PARTICLE_TUNING_MC_SE",
        "BLOCK_P8H_PARTICLE_TUNING_ADJACENT_STABILITY",
        "BLOCK_P8H_PARTICLE_TUNING_MISSING_NEXT_RUNG",
    ):
        if priority_reason in failed_reasons:
            blocker_reason = priority_reason
            break
    return {
        "row_id": terminal["row_id"],
        "algorithm_id": terminal["algorithm_id"],
        "route_variant": terminal["route_variant"],
        "resampling_route": terminal["resampling_route"],
        "tuning_status": "blocked_particle_tuning_not_converged",
        "selected_particle_count": None,
        "selection_rule": "no evaluated P8h Stage 0 count passed all gates",
        "selection_rung": None,
        "next_rung_checked": False,
        "next_rung_particle_count": None,
        "adjacent_horizon_summaries": [],
        "blocker_reason": blocker_reason,
        "evaluated_horizons": horizons,
        "evaluated_particle_counts": particles,
        "nonclaims": [
            "blocked Stage 0 tuning result, not selected particle-count evidence",
            "not full-horizon particle-count adequacy",
            "not gradient correctness",
            "not GPU scaling",
            "not HMC readiness",
            "not a filter ranking",
        ],
    }


def _p8j_phase5_rung_passes(rung: dict[str, Any]) -> bool:
    if not bool(rung["finite"]):
        return False
    if rung["mc_standard_error"] is None or rung["mean_log_likelihood"] is None:
        return False
    mc_se_limit = max(
        P8J_PHASE5_MC_SE_ABS_FLOOR,
        P8J_PHASE5_MC_SE_RELATIVE_FRACTION * abs(float(rung["mean_log_likelihood"])),
    )
    return (
        bool(rung["finite"])
        and bool(rung["transport_diagnostics_pass"])
        and bool(rung["trusted_gpu"])
        and int(rung["seed_count"]) == 5
        and rung["runtime_budget_status"] == "within_budget"
        and float(rung["mc_standard_error"]) <= mc_se_limit
    )


def _p8j_phase5_select_from_rungs(rungs: list[dict[str, Any]]) -> dict[str, Any]:
    if not rungs:
        raise ValueError("expected at least one rung")
    sorted_rungs = sorted(
        rungs,
        key=lambda item: (int(item["horizon_prefix"]), int(item["particle_count"])),
    )
    horizons = sorted({int(item["horizon_prefix"]) for item in sorted_rungs})
    particles = sorted({int(item["particle_count"]) for item in sorted_rungs})
    by_key = {
        (int(item["horizon_prefix"]), int(item["particle_count"])): item
        for item in sorted_rungs
    }
    blocker_reason = "BLOCK_P8J_SIR_PARTICLE_TUNING_NOT_CONVERGED"
    failed_reasons: set[str] = set()
    selected: dict[str, Any] | None = None

    for particle_index, particle_count in enumerate(particles):
        if particle_index + 1 >= len(particles):
            failed_reasons.add("BLOCK_P8J_SIR_PARTICLE_TUNING_MISSING_NEXT_RUNG")
            continue
        next_particle_count = particles[particle_index + 1]
        per_horizon_adjacent: list[dict[str, Any]] = []
        candidate_pass = True
        for horizon in horizons:
            rung = by_key.get((horizon, particle_count))
            next_rung = by_key.get((horizon, next_particle_count))
            if rung is None or next_rung is None:
                candidate_pass = False
                failed_reasons.add("BLOCK_P8J_SIR_PARTICLE_TUNING_MISSING_NEXT_RUNG")
                continue
            if not bool(rung["finite"]):
                candidate_pass = False
                failed_reasons.add("BLOCK_P8J_SIR_PARTICLE_TUNING_NONFINITE")
            if not bool(rung["transport_diagnostics_pass"]):
                candidate_pass = False
                failed_reasons.add("BLOCK_P8J_SIR_PARTICLE_TUNING_TRANSPORT")
            if not bool(rung["trusted_gpu"]):
                candidate_pass = False
                failed_reasons.add("BLOCK_P8J_SIR_PARTICLE_TUNING_GPU_EVIDENCE")
            if int(rung["seed_count"]) != 5:
                candidate_pass = False
                failed_reasons.add("BLOCK_P8J_SIR_PARTICLE_TUNING_SEED_COUNT")
            if rung["runtime_budget_status"] != "within_budget":
                candidate_pass = False
                failed_reasons.add("BLOCK_P8J_SIR_PARTICLE_TUNING_RUNTIME_BUDGET")
            if not _p8j_phase5_rung_passes(rung):
                if rung["mc_standard_error"] is not None and rung["mean_log_likelihood"] is not None:
                    mc_se_limit = max(
                        P8J_PHASE5_MC_SE_ABS_FLOOR,
                        P8J_PHASE5_MC_SE_RELATIVE_FRACTION
                        * abs(float(rung["mean_log_likelihood"])),
                    )
                else:
                    mc_se_limit = None
                if (
                    mc_se_limit is not None
                    and float(rung["mc_standard_error"]) > mc_se_limit
                ):
                    candidate_pass = False
                    failed_reasons.add("BLOCK_P8J_SIR_PARTICLE_TUNING_MC_SE")
            if (
                rung["mean_log_likelihood"] is None
                or next_rung["mean_log_likelihood"] is None
                or rung["mc_standard_error"] is None
                or next_rung["mc_standard_error"] is None
            ):
                adjacent_mean_delta = None
                adjacent_combined_mc_se = None
                adjacent_threshold = None
                adjacent_pass = False
            else:
                adjacent_mean_delta = abs(
                    float(rung["mean_log_likelihood"])
                    - float(next_rung["mean_log_likelihood"])
                )
                adjacent_combined_mc_se = math.sqrt(
                    float(rung["mc_standard_error"]) ** 2
                    + float(next_rung["mc_standard_error"]) ** 2
                )
                adjacent_threshold = (
                    2.0 * adjacent_combined_mc_se
                    + P8J_PHASE5_ADJACENT_DELTA_ABS_BUFFER
                )
                adjacent_pass = adjacent_mean_delta <= adjacent_threshold
            if not adjacent_pass:
                candidate_pass = False
                failed_reasons.add("BLOCK_P8J_SIR_PARTICLE_TUNING_ADJACENT_STABILITY")
            per_horizon_adjacent.append(
                {
                    "horizon_prefix": horizon,
                    "particle_count": particle_count,
                    "next_rung_particle_count": next_particle_count,
                    "adjacent_mean_delta": adjacent_mean_delta,
                    "adjacent_combined_mc_se": adjacent_combined_mc_se,
                    "adjacent_threshold": adjacent_threshold,
                    "adjacent_pass": adjacent_pass,
                }
            )
        if candidate_pass:
            first_rung = by_key[(horizons[0], particle_count)]
            selected = {
                "row_id": first_rung["row_id"],
                "algorithm_id": first_rung["algorithm_id"],
                "route_variant": first_rung["route_variant"],
                "resampling_route": first_rung["resampling_route"],
                "tuning_status": "selected_particle_count",
                "selected_particle_count": particle_count,
                "selection_rule": (
                    "smallest count passing finite, trusted-GPU, transport, "
                    "runtime, five-seed MC SE, and adjacent-rung P8j SIR gates"
                ),
                "selection_rung": particle_count,
                "next_rung_checked": True,
                "next_rung_particle_count": next_particle_count,
                "adjacent_horizon_summaries": per_horizon_adjacent,
                "blocker_reason": None,
                "evaluated_horizons": horizons,
                "evaluated_particle_counts": particles,
                "nonclaims": [
                    "SIR d18 particle-count gate only",
                    "not leaderboard completion",
                    "not gradient correctness",
                    "not HMC readiness",
                    "not source-faithful TT/SIRT evidence",
                ],
            }
            break

    if selected is not None:
        return selected

    terminal = sorted_rungs[-1]
    for priority_reason in (
        "BLOCK_P8J_SIR_PARTICLE_TUNING_NONFINITE",
        "BLOCK_P8J_SIR_PARTICLE_TUNING_TRANSPORT",
        "BLOCK_P8J_SIR_PARTICLE_TUNING_GPU_EVIDENCE",
        "BLOCK_P8J_SIR_PARTICLE_TUNING_RUNTIME_BUDGET",
        "BLOCK_P8J_SIR_PARTICLE_TUNING_SEED_COUNT",
        "BLOCK_P8J_SIR_PARTICLE_TUNING_MC_SE",
        "BLOCK_P8J_SIR_PARTICLE_TUNING_ADJACENT_STABILITY",
        "BLOCK_P8J_SIR_PARTICLE_TUNING_MISSING_NEXT_RUNG",
    ):
        if priority_reason in failed_reasons:
            blocker_reason = priority_reason
            break
    return {
        "row_id": terminal["row_id"],
        "algorithm_id": terminal["algorithm_id"],
        "route_variant": terminal["route_variant"],
        "resampling_route": terminal["resampling_route"],
        "tuning_status": "blocked_particle_tuning_not_converged",
        "selected_particle_count": None,
        "selection_rule": "no evaluated P8j SIR count passed all gates",
        "selection_rung": None,
        "next_rung_checked": False,
        "next_rung_particle_count": None,
        "adjacent_horizon_summaries": [],
        "blocker_reason": blocker_reason,
        "evaluated_horizons": horizons,
        "evaluated_particle_counts": particles,
        "nonclaims": [
            "blocked SIR d18 tuning result, not selected particle-count evidence",
            "not leaderboard completion",
            "not gradient correctness",
            "not HMC readiness",
            "not source-faithful TT/SIRT evidence",
        ],
    }


def _p8g_g4_select_from_rungs(
    rungs: list[dict[str, Any]],
    *,
    terminal_allows_no_next_rung: bool,
) -> dict[str, Any]:
    if not rungs:
        raise ValueError("expected at least one rung")
    sorted_rungs = sorted(rungs, key=lambda item: int(item["particle_count"]))
    by_particle = {int(item["particle_count"]): item for item in sorted_rungs}
    particles = [int(item["particle_count"]) for item in sorted_rungs]
    selected: dict[str, Any] | None = None
    blocker_reason = "BLOCK_DPF_PARTICLE_TUNING_NOT_CONVERGED"
    failed_reasons: set[str] = set()
    for index, particle_count in enumerate(particles):
        rung = by_particle[particle_count]
        next_rung = by_particle[particles[index + 1]] if index + 1 < len(particles) else None
        adjacent_mean_delta = None
        adjacent_combined_mc_se = None
        adjacent_pass = False
        if next_rung is not None:
            adjacent_mean_delta = abs(
                float(rung["mean_log_likelihood"]) - float(next_rung["mean_log_likelihood"])
            )
            adjacent_combined_mc_se = math.sqrt(
                float(rung["mc_standard_error"]) ** 2
                + float(next_rung["mc_standard_error"]) ** 2
            )
            adjacent_pass = adjacent_mean_delta <= (
                2.0 * adjacent_combined_mc_se + P8G_G4_ADJACENT_DELTA_ABS_BUFFER
            )
        elif terminal_allows_no_next_rung:
            adjacent_pass = True

        if _p8g_g4_particle_passes(rung) and adjacent_pass:
            selected = {
                "row_id": rung["row_id"],
                "algorithm_id": rung["algorithm_id"],
                "route_variant": rung["route_variant"],
                "tuning_status": "selected_particle_count",
                "selected_particle_count": particle_count,
                "selection_rule": (
                    "smallest finite count passing relative ESS, MC SE, runtime, "
                    "and adjacent-rung stability gates"
                ),
                "selection_rung": particle_count,
                "next_rung_checked": next_rung is not None,
                "next_rung_particle_count": (
                    int(next_rung["particle_count"]) if next_rung is not None else None
                ),
                "adjacent_mean_delta": adjacent_mean_delta,
                "adjacent_combined_mc_se": adjacent_combined_mc_se,
                "min_relative_ess": rung["min_relative_ess"],
                "mean_relative_ess": rung["mean_relative_ess"],
                "mc_standard_error": rung["mc_standard_error"],
                "mean_log_likelihood": rung["mean_log_likelihood"],
                "runtime_budget_status": rung["runtime_budget_status"],
                "blocker_reason": None,
                "full_horizon": rung["full_horizon"],
                "horizon_prefix": rung["horizon_prefix"],
                "evaluated_particle_count": particle_count,
                "finite": rung["finite"],
                "runtime_seconds": rung["runtime_seconds"],
                "nonclaims": [
                    "particle-count tuning gate only",
                    "not gradient correctness",
                    "not HMC readiness",
                    "not a filter ranking",
                ],
            }
            break
        if not bool(rung["finite"]):
            blocker_reason = "BLOCK_DPF_PARTICLE_TUNING_NONFINITE"
            failed_reasons.add(blocker_reason)
        elif rung["runtime_budget_status"] != "within_budget":
            blocker_reason = "BLOCK_DPF_PARTICLE_TUNING_RUNTIME_BUDGET"
            failed_reasons.add(blocker_reason)
        elif float(rung["min_relative_ess"]) < P8G_G4_RELATIVE_ESS_FLOOR:
            blocker_reason = "BLOCK_DPF_PARTICLE_TUNING_RELATIVE_ESS"
            failed_reasons.add(blocker_reason)
        elif float(rung["mc_standard_error"]) > max(
            P8G_G4_MC_SE_ABS_FLOOR,
            P8G_G4_MC_SE_RELATIVE_FRACTION * abs(float(rung["mean_log_likelihood"])),
        ):
            blocker_reason = "BLOCK_DPF_PARTICLE_TUNING_MC_SE"
            failed_reasons.add(blocker_reason)
        elif next_rung is not None and not adjacent_pass:
            blocker_reason = "BLOCK_DPF_PARTICLE_TUNING_ADJACENT_STABILITY"
            failed_reasons.add(blocker_reason)
        elif next_rung is None and not terminal_allows_no_next_rung:
            blocker_reason = "BLOCK_DPF_PARTICLE_TUNING_MISSING_NEXT_RUNG"
            failed_reasons.add(blocker_reason)

    if selected is not None:
        return selected

    terminal = sorted_rungs[-1]
    if failed_reasons:
        for priority_reason in (
            "BLOCK_DPF_PARTICLE_TUNING_NONFINITE",
            "BLOCK_DPF_PARTICLE_TUNING_RUNTIME_BUDGET",
            "BLOCK_DPF_PARTICLE_TUNING_RELATIVE_ESS",
            "BLOCK_DPF_PARTICLE_TUNING_MC_SE",
            "BLOCK_DPF_PARTICLE_TUNING_ADJACENT_STABILITY",
            "BLOCK_DPF_PARTICLE_TUNING_MISSING_NEXT_RUNG",
        ):
            if priority_reason in failed_reasons:
                blocker_reason = priority_reason
                break
    return {
        "row_id": terminal["row_id"],
        "algorithm_id": terminal["algorithm_id"],
        "route_variant": terminal["route_variant"],
        "tuning_status": "blocked_particle_tuning_not_converged",
        "selected_particle_count": None,
        "selection_rule": "no evaluated count passed all G4 tuning gates",
        "selection_rung": None,
        "next_rung_checked": False,
        "next_rung_particle_count": None,
        "adjacent_mean_delta": None,
        "adjacent_combined_mc_se": None,
        "min_relative_ess": terminal["min_relative_ess"],
        "mean_relative_ess": terminal["mean_relative_ess"],
        "mc_standard_error": terminal["mc_standard_error"],
        "mean_log_likelihood": terminal["mean_log_likelihood"],
        "runtime_budget_status": terminal["runtime_budget_status"],
        "blocker_reason": blocker_reason,
        "full_horizon": terminal["full_horizon"],
        "horizon_prefix": terminal["horizon_prefix"],
        "evaluated_particle_count": terminal["particle_count"],
        "finite": terminal["finite"],
        "runtime_seconds": terminal["runtime_seconds"],
        "nonclaims": [
            "blocked tuning result, not selected particle-count evidence",
            "not gradient correctness",
            "not HMC readiness",
            "not a filter ranking",
        ],
    }


def _p8g_g4_tuning_payload(
    *,
    stage: str,
    rows: list[str],
    algorithms: list[str],
    horizons: list[int],
    particles: list[int],
    seeds: list[int],
    route_variant: str,
    device: str,
    g0_manifest: Path | None,
    runtime_budget_seconds: float = P8G_G4_DEFAULT_RUNTIME_BUDGET_SECONDS,
) -> dict[str, Any]:
    if stage not in {"stage0", "full"}:
        raise ValueError("stage must be 'stage0' or 'full'")
    if route_variant != P8G_ROUTE_VARIANT:
        raise ValueError("G4 initial scope requires route variant p8g_sv_scalar_graph")
    if any(count == DPF_PARTICLE_COUNT for count in particles):
        raise ValueError("N=8 is historical wiring evidence only and cannot be selected in G4")
    if any(count <= DPF_PARTICLE_COUNT for count in particles):
        raise ValueError("G4 particle candidates must exceed the historical N=8 wiring count")
    if device not in {"cpu", "gpu"}:
        raise ValueError("device must be 'cpu' or 'gpu'")
    if device == "gpu" and g0_manifest is None:
        raise ValueError("trusted GPU particle tuning requires --g0-manifest")
    if stage == "full" and len(horizons) != 1:
        raise ValueError("full tuning must run one horizon/cell scope at a time")

    started = time.perf_counter()
    evaluated_rungs: list[dict[str, Any]] = []
    selected_blocked: list[dict[str, Any]] = []
    for row_id in rows:
        for algorithm_id in algorithms:
            if not _p8g_g4_allowed_cell(row_id, algorithm_id, route_variant):
                selected_blocked.append(
                    _p8g_g4_deferred_record(
                        row_id=row_id,
                        algorithm_id=algorithm_id,
                        route_variant=route_variant,
                        reason="G4 initial executable scope is actual-SV LEDH scalar graph only",
                    )
                )
                continue
            cell_rungs: list[dict[str, Any]] = []
            for horizon in horizons:
                for particle_count in particles:
                    rung = _p8g_g4_profile_cell(
                        row_id=row_id,
                        algorithm_id=algorithm_id,
                        horizon=int(horizon),
                        particle_count=int(particle_count),
                        seeds=seeds,
                        device=device,
                        g0_manifest=g0_manifest,
                        route_variant=route_variant,
                        runtime_budget_seconds=float(runtime_budget_seconds),
                    )
                    rung["stage"] = stage
                    cell_rungs.append(rung)
                    evaluated_rungs.append(rung)
            selected_blocked.append(
                _p8g_g4_select_from_rungs(
                    cell_rungs,
                    terminal_allows_no_next_rung=(stage == "full" or len(horizons) > 1),
                )
            )

    status = (
        "blocked_p8g_particle_tuning_no_executable_rungs"
        if not evaluated_rungs
        else (
            "executed_p8g_particle_tuning_stage0"
            if stage == "stage0"
            else "executed_p8g_particle_tuning_full"
        )
    )
    if any(row["tuning_status"].startswith("blocked") for row in selected_blocked):
        status = f"{status}_with_blockers"
    return {
        "schema_version": "filter_bench.p8g_particle_tuning.v1",
        "phase": "P8G_G4_PARTICLE_TUNING",
        "stage": stage,
        "status": status,
        "evidence_contract": {
            "question": "What particle counts are adequate for the actual-SV scalar graph LEDH value summary under the reviewed GPU path?",
            "baseline": "N=8 finite wiring evidence from P8d/P8e and small-scope G3 diagnostics; N=8 is not selectable.",
            "primary_criterion": "Select the smallest count passing finite, relative ESS, MC SE, runtime, and adjacent-rung gates, or emit an explicit blocker.",
            "veto_diagnostics": [
                "non-finite run",
                "relative ESS collapse",
                "unstable adjacent-rung mean",
                "missing next-rung check where required",
                "runtime budget failure",
                "deferred rows disappearing from outputs",
            ],
            "not_concluded": [
                "gradient correctness",
                "HMC readiness",
                "filter ranking",
                "generic high-dimensional LEDH readiness",
                "stochastic PF marginal likelihood gradient correctness",
            ],
        },
        "selection_thresholds": {
            "relative_ess_floor": P8G_G4_RELATIVE_ESS_FLOOR,
            "mc_se_abs_floor": P8G_G4_MC_SE_ABS_FLOOR,
            "mc_se_relative_fraction": P8G_G4_MC_SE_RELATIVE_FRACTION,
            "adjacent_delta_abs_buffer": P8G_G4_ADJACENT_DELTA_ABS_BUFFER,
            "runtime_budget_seconds": float(runtime_budget_seconds),
        },
        "run_manifest": {
            "git_commit": _git_commit(),
            "dirty_state_summary": _dirty_summary(),
            "command": " ".join(sys.argv),
            "environment": "TensorFlow/TensorFlow Probability G4 particle tuning harness",
            "cuda_visible_devices": str(__import__("os").environ.get("CUDA_VISIBLE_DEVICES")),
            "requested_device": device,
            "tf_physical_gpus": [gpu.name for gpu in tf.config.list_physical_devices("GPU")],
            "tf_logical_gpus": [gpu.name for gpu in tf.config.list_logical_devices("GPU")],
            "g0_manifest": _rel(g0_manifest) if g0_manifest is not None else None,
            "plan": _rel(P8G_G4_PLAN_PATH),
            "g2b_result": "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-repair-result-2026-06-15.md",
            "g3_result": "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-result-2026-06-15.md",
            "wall_time_seconds": round(time.perf_counter() - started, 6),
        },
        "scope": {
            "rows": rows,
            "algorithms": algorithms,
            "horizons": [int(item) for item in horizons],
            "particles": [int(item) for item in particles],
            "seeds": [int(seed) for seed in seeds],
            "route_variant": route_variant,
            "executable_initial_scope": [SV_ROW],
            "historical_particle_count_not_selectable": DPF_PARTICLE_COUNT,
        },
        "evaluated_rungs": evaluated_rungs,
        "selected_blocked": selected_blocked,
        "summary": {
            "evaluated_rung_count": len(evaluated_rungs),
            "selected_count": sum(
                1 for row in selected_blocked if row["tuning_status"] == "selected_particle_count"
            ),
            "blocked_count": sum(
                1 for row in selected_blocked if row["tuning_status"].startswith("blocked")
            ),
            "deferred_count": sum(
                1 for row in selected_blocked if row["tuning_status"].startswith("deferred")
            ),
            "all_requested_cells_accounted": len(selected_blocked) == len(rows) * len(algorithms),
        },
        "nonclaims": [
            "particle-count tuning gate only",
            "prefix Stage 0 is not full-horizon tuning evidence",
            "not gradient correctness",
            "not HMC readiness",
            "not a filter ranking",
            "not generalized-SV or generic high-dimensional LEDH evidence",
        ],
    }


def _p8h_phase5_tuning_payload(
    *,
    rows: list[str],
    algorithms: list[str],
    horizons: list[int],
    particles: list[int],
    seeds: list[int],
    resampling_route: str,
    device: str,
    g0_manifest: Path | None,
    runtime_budget_seconds: float = P8H_PHASE5_DEFAULT_RUNTIME_BUDGET_SECONDS,
    manifest_phase: str = "P8H_PHASE5_VALUE_FILTERING_TUNING",
    manifest_plan: Path | None = None,
) -> dict[str, Any]:
    if device not in {"cpu", "gpu"}:
        raise ValueError("device must be 'cpu' or 'gpu'")
    if device != "gpu":
        raise ValueError("P8h Phase 5 tuning must run on trusted GPU")
    if g0_manifest is None:
        raise ValueError("trusted GPU P8h Phase 5 tuning requires --g0-manifest")
    if resampling_route != P8H_DEFAULT_RESAMPLING_ROUTE:
        raise ValueError("P8h Phase 5 initial scope requires Sinkhorn covariance-carry route")
    if len(seeds) != 5:
        raise ValueError("P8h Phase 5 tuning requires exactly five fixed seeds")

    started = time.perf_counter()
    evaluated_rungs: list[dict[str, Any]] = []
    selected_blocked: list[dict[str, Any]] = []
    for row_id in rows:
        for algorithm_id in algorithms:
            if not _p8h_phase5_allowed_cell(row_id, algorithm_id, resampling_route):
                selected_blocked.append(
                    {
                        "row_id": row_id,
                        "algorithm_id": algorithm_id,
                        "route_variant": P8H_ROUTE_VARIANT,
                        "resampling_route": resampling_route,
                        "tuning_status": "deferred_not_in_initial_p8h_phase5_scope",
                        "selected_particle_count": None,
                        "selection_rule": "actual-SV Algorithm 1 Sinkhorn OT route only in Phase 5",
                        "selection_rung": None,
                        "next_rung_checked": False,
                        "next_rung_particle_count": None,
                        "adjacent_horizon_summaries": [],
                        "blocker_reason": "DEFERRED_OUT_OF_SCOPE",
                        "evaluated_horizons": [],
                        "evaluated_particle_counts": [],
                        "nonclaims": [
                            "deferred row, not P8h tuned particle-count evidence",
                            "not a filter ranking",
                            "not HMC readiness",
                        ],
                    }
                )
                continue
            cell_rungs: list[dict[str, Any]] = []
            for horizon in horizons:
                for particle_count in particles:
                    rung = _p8h_phase5_profile_cell(
                        row_id=row_id,
                        algorithm_id=algorithm_id,
                        horizon=int(horizon),
                        particle_count=int(particle_count),
                        seeds=seeds,
                        device=device,
                        g0_manifest=g0_manifest,
                        resampling_route=resampling_route,
                        runtime_budget_seconds=float(runtime_budget_seconds),
                    )
                    rung["stage"] = "stage0"
                    cell_rungs.append(rung)
                    evaluated_rungs.append(rung)
            selected_blocked.append(_p8h_phase5_select_from_rungs(cell_rungs))

    status = (
        "blocked_p8h_particle_tuning_no_executable_rungs"
        if not evaluated_rungs
        else "executed_p8h_particle_tuning_stage0"
    )
    if any(row["tuning_status"].startswith("blocked") for row in selected_blocked):
        status = f"{status}_with_blockers"
    return {
        "schema_version": "filter_bench.p8h_particle_tuning.v1",
        "phase": str(manifest_phase),
        "stage": "stage0",
        "status": status,
        "evidence_contract": {
            "question": "What Stage 0 prefix particle counts are adequate for the P8h OT-resampled scalar-SV route under trusted GPU execution?",
            "baseline": "Phase 4 local diagnostics and within-P8h adjacent-rung comparisons; P8g no-resampling is historical context only.",
            "primary_criterion": "Select the smallest count passing finite, trusted-GPU, transport, runtime, five-seed MC SE, and adjacent-rung gates at every Stage 0 horizon, or emit an explicit blocker.",
            "veto_diagnostics": [
                "non-finite run",
                "transport diagnostic failure",
                "trusted GPU evidence missing",
                "runtime budget failure",
                "missing five-seed uncertainty",
                "MC SE failure",
                "unstable adjacent-rung mean",
                "stale P8g schema/result reuse",
            ],
            "not_concluded": [
                "full-horizon particle-count adequacy",
                "gradient correctness",
                "GPU scaling",
                "HMC readiness",
                "filter ranking",
                "generic high-dimensional LEDH readiness",
            ],
        },
        "selection_thresholds": {
            "runtime_budget_seconds": float(runtime_budget_seconds),
            "mc_se_abs_floor": P8H_PHASE5_MC_SE_ABS_FLOOR,
            "mc_se_relative_fraction": P8H_PHASE5_MC_SE_RELATIVE_FRACTION,
            "adjacent_delta_abs_buffer": P8H_PHASE5_ADJACENT_DELTA_ABS_BUFFER,
            "required_seed_count": 5,
            "terminal_without_next_rung_selectable": False,
            "ess_status": "diagnostic_not_pass_criterion_when_finite",
        },
        "run_manifest": {
            "git_commit": _git_commit(),
            "dirty_state_summary": _dirty_summary(),
            "command": " ".join(sys.argv),
            "environment": f"TensorFlow/TensorFlow Probability {manifest_phase} particle profile harness",
            "cuda_visible_devices": str(__import__("os").environ.get("CUDA_VISIBLE_DEVICES")),
            "requested_device": device,
            "tf_physical_gpus": [gpu.name for gpu in tf.config.list_physical_devices("GPU")],
            "tf_logical_gpus": [gpu.name for gpu in tf.config.list_logical_devices("GPU")],
            "g0_manifest": _rel(g0_manifest) if g0_manifest is not None else None,
            "plan": _rel(manifest_plan or P8H_PHASE5_PLAN_PATH),
            "phase4_result": "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase4-local-checks-result-2026-06-15.md",
            "wall_time_seconds": round(time.perf_counter() - started, 6),
        },
        "scope": {
            "rows": rows,
            "algorithms": algorithms,
            "horizons": [int(item) for item in horizons],
            "particles": [int(item) for item in particles],
            "seeds": [int(seed) for seed in seeds],
            "route_variant": P8H_ROUTE_VARIANT,
            "resampling_route": resampling_route,
            "executable_initial_scope": [SV_ROW],
        },
        "evaluated_rungs": evaluated_rungs,
        "selected_blocked": selected_blocked,
        "summary": {
            "evaluated_rung_count": len(evaluated_rungs),
            "selected_count": sum(
                1 for row in selected_blocked if row["tuning_status"] == "selected_particle_count"
            ),
            "blocked_count": sum(
                1 for row in selected_blocked if row["tuning_status"].startswith("blocked")
            ),
            "deferred_count": sum(
                1 for row in selected_blocked if row["tuning_status"].startswith("deferred")
            ),
            "all_requested_cells_accounted": len(selected_blocked) == len(rows) * len(algorithms),
        },
        "nonclaims": [
            "P8h Stage 0 prefix particle-count tuning gate only",
            "not full-horizon particle-count adequacy",
            "not gradient correctness",
            "not GPU scaling",
            "not HMC readiness",
            "not a filter ranking",
            "not generic high-dimensional LEDH evidence",
        ],
    }


def _p8j_phase5_tuning_payload(
    *,
    rows: list[str],
    algorithms: list[str],
    horizons: list[int],
    particles: list[int],
    seeds: list[int],
    device: str,
    g0_manifest: Path | None,
    runtime_budget_seconds: float = P8J_PHASE5_DEFAULT_RUNTIME_BUDGET_SECONDS,
    manifest_phase: str = "P8J_PHASE5_SIR_PARTICLE_TUNING",
    manifest_plan: Path | None = None,
    sinkhorn_epsilon_policy: str = "fixed",
) -> dict[str, Any]:
    if device not in {"cpu", "gpu"}:
        raise ValueError("device must be 'cpu' or 'gpu'")
    if device != "gpu":
        raise ValueError("P8j Phase 5 final tuning must run on trusted GPU")
    if g0_manifest is None:
        raise ValueError("trusted GPU P8j Phase 5 tuning requires --g0-manifest")
    if len(seeds) != 5:
        raise ValueError("P8j Phase 5 tuning requires exactly five fixed seeds")
    if [int(seed) for seed in seeds] != DPF_SEEDS:
        raise ValueError("P8j Phase 5 tuning requires the fixed DPF seed list")
    if any(count == DPF_PARTICLE_COUNT for count in particles):
        raise ValueError("N=8 is historical wiring evidence only and cannot be selected in P8j")
    if any(count <= DPF_PARTICLE_COUNT for count in particles):
        raise ValueError("P8j particle candidates must exceed the historical N=8 wiring count")
    if rows != [SIR_ROW]:
        raise ValueError("P8j Phase 5 tuning supports only the SIR d18 row")
    if any(algorithm not in {BOOTSTRAP_DPF, LEDH_ALG1_DPF} for algorithm in algorithms):
        raise ValueError("P8j Phase 5 tuning supports only bootstrap and Algorithm 1 LEDH")

    started = time.perf_counter()
    evaluated_rungs: list[dict[str, Any]] = []
    selected_blocked: list[dict[str, Any]] = []
    for row_id in rows:
        for algorithm_id in algorithms:
            if not _p8j_phase5_allowed_cell(row_id, algorithm_id):
                raise ValueError("P8j Phase 5 received an unsupported SIR DPF cell")
            cell_rungs: list[dict[str, Any]] = []
            for horizon in horizons:
                for particle_count in particles:
                    rung = _p8j_phase5_profile_cell(
                        row_id=row_id,
                        algorithm_id=algorithm_id,
                        horizon=int(horizon),
                        particle_count=int(particle_count),
                        seeds=seeds,
                        device=device,
                        g0_manifest=g0_manifest,
                        runtime_budget_seconds=float(runtime_budget_seconds),
                        sinkhorn_epsilon_policy=str(sinkhorn_epsilon_policy),
                    )
                    rung["stage"] = "stage0"
                    cell_rungs.append(rung)
                    evaluated_rungs.append(rung)
            selected_blocked.append(_p8j_phase5_select_from_rungs(cell_rungs))

    status = (
        "blocked_p8j_sir_particle_tuning_no_executable_rungs"
        if not evaluated_rungs
        else "executed_p8j_sir_particle_tuning_stage0"
    )
    if any(row["tuning_status"].startswith("blocked") for row in selected_blocked):
        status = f"{status}_with_blockers"
    return {
        "schema_version": "filter_bench.p8j_sir_particle_tuning.v1",
        "phase": str(manifest_phase),
        "stage": "stage0",
        "status": status,
        "evidence_contract": {
            "question": "What particle count, if any, is adequate for SIR d18 bootstrap and OT-resampled LEDH DPF value evidence?",
            "baseline": "Phase 2 bootstrap smoke, Phase 4 OT LEDH smoke, P8d five-seed value contract, and within-P8j adjacent-rung comparisons.",
            "primary_criterion": "Select the smallest count per algorithm passing five-seed finite, MC SE, runtime, adjacent-rung stability, and route/transport gates; otherwise emit a blocker.",
            "veto_diagnostics": [
                "N=8 selected",
                "fewer than five seeds",
                "one-seed smoke treated as tuning",
                "missing next rung",
                "non-finite values",
                "failed OT transport metadata",
                "untrusted GPU evidence",
                "runtime budget failure",
                "model/data mutation",
                "score/Hessian/theta-gradient/HMC claim",
            ],
            "not_concluded": [
                "exact likelihood correctness",
                "posterior convergence",
                "DPF gradients",
                "HMC/NUTS readiness",
                "source-faithful TT/SIRT parity",
                "MATLAB parity",
                "production readiness",
                "leaderboard completion",
            ],
        },
        "selection_thresholds": {
            "runtime_budget_seconds": float(runtime_budget_seconds),
            "mc_se_abs_floor": P8J_PHASE5_MC_SE_ABS_FLOOR,
            "mc_se_relative_fraction": P8J_PHASE5_MC_SE_RELATIVE_FRACTION,
            "adjacent_delta_abs_buffer": P8J_PHASE5_ADJACENT_DELTA_ABS_BUFFER,
            "required_seed_count": 5,
            "terminal_without_next_rung_selectable": False,
            "historical_particle_count_not_selectable": DPF_PARTICLE_COUNT,
            "sinkhorn_epsilon_policy": str(sinkhorn_epsilon_policy),
            "sinkhorn_repair_classification": (
                None
                if sinkhorn_epsilon_policy == "fixed"
                else "p8j_sir_numerical_stability_repair_candidate"
            ),
        },
        "run_manifest": {
            "git_commit": _git_commit(),
            "dirty_state_summary": _dirty_summary(),
            "command": " ".join(sys.argv),
            "environment": f"TensorFlow/TensorFlow Probability {manifest_phase} SIR particle tuning harness",
            "cuda_visible_devices": str(__import__("os").environ.get("CUDA_VISIBLE_DEVICES")),
            "requested_device": device,
            "tf_physical_gpus": [gpu.name for gpu in tf.config.list_physical_devices("GPU")],
            "tf_logical_gpus": [gpu.name for gpu in tf.config.list_logical_devices("GPU")],
            "g0_manifest": _rel(g0_manifest) if g0_manifest is not None else None,
            "plan": _rel(manifest_plan or P8J_PHASE5_PLAN_PATH),
            "phase4_result": "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase4-ot-ledh-sir-smoke-result-2026-06-17.md",
            "wall_time_seconds": round(time.perf_counter() - started, 6),
        },
        "scope": {
            "rows": rows,
            "algorithms": algorithms,
            "horizons": [int(item) for item in horizons],
            "particles": [int(item) for item in particles],
            "seeds": [int(seed) for seed in seeds],
            "row_id": SIR_ROW,
            "executable_initial_scope": [SIR_ROW],
            "historical_particle_count_not_selectable": DPF_PARTICLE_COUNT,
        },
        "evaluated_rungs": evaluated_rungs,
        "selected_blocked": selected_blocked,
        "summary": {
            "evaluated_rung_count": len(evaluated_rungs),
            "selected_count": sum(
                1 for row in selected_blocked if row["tuning_status"] == "selected_particle_count"
            ),
            "blocked_count": sum(
                1 for row in selected_blocked if row["tuning_status"].startswith("blocked")
            ),
            "all_requested_cells_accounted": len(selected_blocked) == len(rows) * len(algorithms),
        },
        "nonclaims": [
            "P8j SIR d18 particle-count tuning gate only",
            "not leaderboard completion",
            "not gradient correctness",
            "not HMC readiness",
            "not source-faithful TT/SIRT evidence",
            "not MATLAB parity",
            "not production readiness",
        ],
    }


def _write_p8g_particle_tuning_csv(path: Path, payload: dict[str, Any]) -> None:
    rows = payload["evaluated_rungs"]
    fieldnames = [
        "stage",
        "row_id",
        "algorithm_id",
        "route_variant",
        "full_horizon",
        "horizon_prefix",
        "particle_count",
        "seed_count",
        "finite",
        "mean_log_likelihood",
        "mean_average_log_likelihood",
        "sample_standard_deviation",
        "mc_standard_error",
        "min_relative_ess",
        "mean_relative_ess",
        "runtime_seconds",
        "runtime_budget_seconds",
        "runtime_budget_status",
        "status",
    ]
    _write_csv(path, rows, fieldnames)


def _write_p8h_particle_tuning_csv(path: Path, payload: dict[str, Any]) -> None:
    rows = payload["evaluated_rungs"]
    fieldnames = [
        "stage",
        "row_id",
        "algorithm_id",
        "route_variant",
        "resampling_route",
        "full_horizon",
        "horizon_prefix",
        "particle_count",
        "seed_count",
        "finite",
        "transport_diagnostics_pass",
        "trusted_gpu",
        "mean_log_likelihood",
        "mean_average_log_likelihood",
        "sample_standard_deviation",
        "mc_standard_error",
        "min_relative_ess",
        "mean_relative_ess",
        "runtime_seconds",
        "runtime_budget_seconds",
        "runtime_budget_status",
        "status",
    ]
    _write_csv(path, rows, fieldnames)


def _write_p8g_selected_blocked_csv(path: Path, payload: dict[str, Any]) -> None:
    fieldnames = [
        "row_id",
        "algorithm_id",
        "route_variant",
        "tuning_status",
        "selected_particle_count",
        "selection_rule",
        "selection_rung",
        "next_rung_checked",
        "next_rung_particle_count",
        "adjacent_mean_delta",
        "adjacent_combined_mc_se",
        "min_relative_ess",
        "mean_relative_ess",
        "mc_standard_error",
        "mean_log_likelihood",
        "runtime_budget_status",
        "blocker_reason",
        "full_horizon",
        "horizon_prefix",
        "evaluated_particle_count",
        "finite",
        "runtime_seconds",
    ]
    _write_csv(path, payload["selected_blocked"], fieldnames)


def _write_p8h_selected_blocked_csv(path: Path, payload: dict[str, Any]) -> None:
    rows = []
    for row in payload["selected_blocked"]:
        copy = dict(row)
        copy["adjacent_horizon_summaries"] = json.dumps(
            copy.get("adjacent_horizon_summaries", []),
            sort_keys=True,
        )
        copy["evaluated_horizons"] = json.dumps(copy.get("evaluated_horizons", []))
        copy["evaluated_particle_counts"] = json.dumps(
            copy.get("evaluated_particle_counts", [])
        )
        rows.append(copy)
    fieldnames = [
        "row_id",
        "algorithm_id",
        "route_variant",
        "resampling_route",
        "tuning_status",
        "selected_particle_count",
        "selection_rule",
        "selection_rung",
        "next_rung_checked",
        "next_rung_particle_count",
        "adjacent_horizon_summaries",
        "blocker_reason",
        "evaluated_horizons",
        "evaluated_particle_counts",
    ]
    _write_csv(path, rows, fieldnames)


def _write_p8j_particle_tuning_csv(path: Path, payload: dict[str, Any]) -> None:
    rows = payload["evaluated_rungs"]
    fieldnames = [
        "stage",
        "row_id",
        "algorithm_id",
        "route_variant",
        "resampling_route",
        "full_horizon",
        "horizon_prefix",
        "particle_count",
        "seed_count",
        "finite",
        "transport_diagnostics_pass",
        "trusted_gpu",
        "mean_log_likelihood",
        "mean_average_log_likelihood",
        "sample_standard_deviation",
        "mc_standard_error",
        "min_relative_ess",
        "mean_relative_ess",
        "runtime_seconds",
        "runtime_budget_seconds",
        "runtime_budget_status",
        "status",
    ]
    _write_csv(path, rows, fieldnames)


def _write_p8j_selected_blocked_csv(path: Path, payload: dict[str, Any]) -> None:
    rows = []
    for row in payload["selected_blocked"]:
        copy = dict(row)
        copy["adjacent_horizon_summaries"] = json.dumps(
            copy.get("adjacent_horizon_summaries", []),
            sort_keys=True,
        )
        copy["evaluated_horizons"] = json.dumps(copy.get("evaluated_horizons", []))
        copy["evaluated_particle_counts"] = json.dumps(
            copy.get("evaluated_particle_counts", [])
        )
        rows.append(copy)
    fieldnames = [
        "row_id",
        "algorithm_id",
        "route_variant",
        "resampling_route",
        "tuning_status",
        "selected_particle_count",
        "selection_rule",
        "selection_rung",
        "next_rung_checked",
        "next_rung_particle_count",
        "adjacent_horizon_summaries",
        "blocker_reason",
        "evaluated_horizons",
        "evaluated_particle_counts",
    ]
    _write_csv(path, rows, fieldnames)


def _append_p8g_particle_tuning_jsonl(path: Path, payload: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def _pending_cell(algorithm_id: str, model_row_id: str, adapter: dict[str, str]) -> dict[str, Any]:
    cell = _base_cell(algorithm_id=algorithm_id, model_row_id=model_row_id, adapter=adapter)
    reason = adapter["not_available_reason"] or "P8D_MODEL_SPECIFIC_NUMERIC_EVALUATOR_ADAPTER_REQUIRED"
    if adapter["target_contract_status"] == "structured_not_applicable":
        status = "structured_not_applicable"
        value_status = adapter["value_adapter_status"]
        score_status = adapter["score_adapter_status"]
        hessian_status = adapter["hessian_adapter_status"]
    elif algorithm_id in {BOOTSTRAP_DPF, LEDH_ALG1_DPF}:
        status = "blocked_pending_model_specific_dpf_callbacks"
        reason = "P8D_MODEL_SPECIFIC_DPF_CALLBACKS_REQUIRED_BEFORE_5SEED_AGGREGATION"
        value_status = "blocked_model_specific_dpf_callbacks_required"
        score_status = (
            "not_applicable_no_free_theta"
            if adapter["score_adapter_status"] == "not_applicable_no_free_theta"
            else "blocked_model_specific_dpf_callbacks_before_score_review"
        )
        hessian_status = (
            "not_applicable_no_free_theta"
            if adapter["hessian_adapter_status"] == "not_applicable_no_free_theta"
            else "blocked_model_specific_dpf_callbacks_before_hessian_review"
        )
    else:
        status = "blocked_model_specific_evaluator_adapter_required"
        value_status = "blocked_model_specific_value_evaluator_adapter_required"
        score_status = (
            "not_applicable_no_free_theta"
            if adapter["score_adapter_status"] == "not_applicable_no_free_theta"
            else "blocked_model_specific_score_evaluator_adapter_required"
        )
        hessian_status = (
            "not_applicable_no_free_theta"
            if adapter["hessian_adapter_status"] == "not_applicable_no_free_theta"
            else "blocked_model_specific_hessian_evaluator_adapter_required"
        )
    cell.update(
        {
            "value_adapter_status": value_status,
            "score_adapter_status": score_status,
            "hessian_adapter_status": hessian_status,
            "numeric_execution_status": status,
            "reason_codes": [reason],
            "nonclaims": [
                "not a numeric benchmark result for this cell",
                "no silent N/A: cell remains explicit structured blocker or not-applicable",
            ],
        }
    )
    return cell


def build_artifact() -> dict[str, Any]:
    started = time.time()
    source_scope = _load_json(SOURCE_SCOPE_PATH)
    dataset_manifest = _load_json(DATASET_MANIFEST_PATH)
    adapters = _as_adapter_map()
    algorithms = list(source_scope["algorithm_ids"])
    rows = list(source_scope["source_scope_row_ids"])
    cells: list[dict[str, Any]] = []

    for algorithm_id in algorithms:
        for row_id in rows:
            adapter = adapters[(algorithm_id, row_id)]
            if algorithm_id == KALMAN and row_id == LGSSM_ROW:
                cells.append(_numeric_lgssm_exact_cell(adapter))
            elif algorithm_id in {UKF, SVD, CUT4} and row_id == LGSSM_ROW:
                cells.append(_numeric_lgssm_value_only_cell(algorithm_id, adapter))
            elif algorithm_id in {KALMAN, UKF, SVD, CUT4, ZHAO_CUI} and row_id == KSC_ROW:
                if _has_deterministic_route(algorithm_id, row_id):
                    cells.append(_numeric_deterministic_cell(algorithm_id, row_id, adapter))
                else:
                    cells.append(_pending_cell(algorithm_id, row_id, adapter))
            elif algorithm_id in {UKF, SVD, CUT4, ZHAO_CUI} and row_id not in {
                LGSSM_ROW,
                KSC_ROW,
            }:
                if _has_deterministic_route(algorithm_id, row_id):
                    cells.append(_numeric_deterministic_cell(algorithm_id, row_id, adapter))
                else:
                    cells.append(_pending_cell(algorithm_id, row_id, adapter))
            elif algorithm_id in {BOOTSTRAP_DPF, LEDH_ALG1_DPF} and row_id == LGSSM_ROW:
                cells.append(_numeric_dpf_cell(algorithm_id, row_id, adapter))
            elif algorithm_id in {BOOTSTRAP_DPF, LEDH_ALG1_DPF} and _has_dpf_route(row_id):
                cells.append(_numeric_dpf_cell(algorithm_id, row_id, adapter))
            else:
                cells.append(_pending_cell(algorithm_id, row_id, adapter))

    executed = [cell for cell in cells if cell["numeric_execution_status"].startswith("executed")]
    structured_not_applicable = [
        cell for cell in cells if cell["numeric_execution_status"] == "structured_not_applicable"
    ]
    real_gaps = [
        cell
        for cell in cells
        if not cell["numeric_execution_status"].startswith("executed")
        and cell["numeric_execution_status"] != "structured_not_applicable"
    ]
    full_cell_count = len(algorithms) * len(rows)
    executed_count = len(executed)
    not_applicable_count = len(structured_not_applicable)
    real_gap_count = len(real_gaps)
    status = (
        "PASS_P8D_NUMERIC_BENCHMARK_RUNNER_ALL_TARGET_COMPATIBLE_CELLS_EXECUTED"
        if real_gap_count == 0
        else "PARTIAL_P8D_NUMERIC_BENCHMARK_RUNNER_WITH_EXPLICIT_REMAINING_GAPS"
    )
    numeric_status = (
        "complete_target_compatible_cells_executed_true_not_applicable_preserved"
        if real_gap_count == 0
        else "partial_numeric_execution_remaining_adapter_and_callback_gaps"
    )
    return {
        "schema_version": "filter_bench.p8d_numeric_results.v1",
        "metadata_date": "2026-06-13",
        "phase": "FILTER_BENCH_P8D_VISIBLE_REPAIR_EXECUTION",
        "status": status,
        "numeric_benchmark_status": numeric_status,
        "evidence_contract": {
            "question": "Can P8d safely fill target-compatible remaining P8c holes with reviewed numeric value/score cells while preserving true not-applicable cells?",
            "baseline": "P8c partial numeric artifact is comparator-only evidence, plus source-paper scope contract, generated dataset manifest, and P8 adapter matrix.",
            "primary_criterion": "Promoted cells have real evaluator outputs and all remaining cells have explicit machine-readable implementation blockers; DPF numeric value cells require five seeds and MC standard error.",
            "veto_diagnostics": [
                "old status-only matrices promoted as numeric evidence",
                "preflight treated as benchmark completion",
                "DPF cells ranked before five-seed MC-SE",
                "score coordinate provenance omitted",
                "old LEDH-PFPF-OT evidence used as current evidence",
                "LGSSM sigma-point scores use tf_autodiff_kalman fallback",
                "P8c metadata preserved in P8d artifacts",
                "target compatibility decided by convenience instead of adapter matrix/source scope",
            ],
            "not_concluded": [
                "full filter ranking",
                "Bayesian-estimation readiness",
                "exact nonlinear likelihood correctness",
                "universal DPF gradient validity",
            ],
        },
        "skeptical_plan_audit": {
            "status": "PASS_P8D_REVIEWED_AUDIT_WITH_SCOPE_RESTRICTIONS",
            "notes": [
                "P8c is treated as partial comparator-only evidence, not full scientific truth.",
                "LGSSM sigma-point score cells use non-eigensystem differentiated-Kalman affine-equivalence score and Hessian after value tieout.",
                "Only mechanically target-compatible cells with explicit routes are filled numerically.",
                "Every remaining cell is explicit structured-blocked or structured not-applicable.",
                "DPF cells are five-seed stochastic value summaries only; no DPF gradient ranking is attempted.",
                f"Plan review gate: {P8D_PLAN_REVIEW_STATUS}.",
            ],
        },
        "source_artifacts": _source_artifacts_payload(),
        "roster": {
            "algorithm_ids": algorithms,
            "model_row_ids": rows,
            "full_cell_count": full_cell_count,
            "executed_cell_count": executed_count,
            "structured_not_applicable_cell_count": not_applicable_count,
            "real_gap_cell_count": real_gap_count,
            "pending_or_not_applicable_cell_count": real_gap_count + not_applicable_count,
        },
        "dataset_records_used": dataset_manifest["dataset_records"],
        "cells": cells,
        "decision_table": [
            {
                "decision": "do_not_close_p8",
                "primary_criterion_status": "partial" if real_gap_count else "passed",
                "veto_diagnostic_status": "passed_for_executed_subset",
                "main_uncertainty": "remaining source-route Zhao-Cui cells, KSC/Spatial-SIR DPF callbacks, nonlinear target approximation interpretation",
                "next_justified_action": "review P8d implementation and run only cells with finite route evidence",
                "not_concluded": "no full benchmark ranking",
            }
        ],
        "run_manifest": _run_manifest_payload(),
        "post_run_red_team_note": {
            "strongest_alternative_explanation": "The executed subset mainly checks available LGSSM and scalar KSC routes; remaining cells may expose adapter or stochastic failures.",
            "would_overturn_closeout": "Any target-compatible pending cell lacking an evaluator, or any DPF cell lacking MC-SE, keeps P8 from full pass.",
            "weakest_part_of_evidence": "Nonlinear DPF uses small particle-count value-only callback wiring; source-route Zhao-Cui production equivalence is not claimed.",
        },
        "nonclaims": [
            "partial numeric artifact, not full Phase 8 completion",
            "not a filter ranking",
            "not Bayesian-estimation readiness",
            "not DPF gradient certification",
            "old LEDH-PFPF-OT evidence is not current evidence",
        ],
        "_started_wall_time": started,
    }


def _cell_display_value(cell: dict[str, Any]) -> str:
    value = _float_or_none(cell.get("average_log_likelihood"))
    if value is None:
        return cell["numeric_execution_status"]
    return f"{value:.10g}"


def _cell_display_score(cell: dict[str, Any]) -> str:
    value = _float_or_none(cell.get("score_l2_norm"))
    if value is None:
        return cell["score_adapter_status"]
    return f"{value:.10g}"


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def _write_summary_markdown(path: Path, artifact: dict[str, Any]) -> None:
    cells = artifact["cells"]
    algorithms = artifact["roster"]["algorithm_ids"]
    rows = artifact["roster"]["model_row_ids"]
    by_key = {(cell["algorithm_id"], cell["model_row_id"]): cell for cell in cells}
    lines = [
        "# P8d Numeric Benchmark Execution Summary",
        "",
        f"status: `{artifact['status']}`",
        f"numeric_benchmark_status: `{artifact['numeric_benchmark_status']}`",
        "",
        "## Value Table",
        "",
        "| algorithm | " + " | ".join(rows) + " |",
        "| --- | " + " | ".join(["---"] * len(rows)) + " |",
    ]
    for algorithm_id in algorithms:
        lines.append(
            "| "
            + algorithm_id
            + " | "
            + " | ".join(_cell_display_value(by_key[(algorithm_id, row_id)]) for row_id in rows)
            + " |"
        )
    lines.extend(
        [
            "",
            "## Score Norm Table",
            "",
            "| algorithm | " + " | ".join(rows) + " |",
            "| --- | " + " | ".join(["---"] * len(rows)) + " |",
        ]
    )
    for algorithm_id in algorithms:
        lines.append(
            "| "
            + algorithm_id
            + " | "
            + " | ".join(_cell_display_score(by_key[(algorithm_id, row_id)]) for row_id in rows)
            + " |"
        )
    lines.extend(
        [
            "",
            "## Tokens",
            "",
            "```text",
            artifact["status"],
            artifact["numeric_benchmark_status"],
            "```",
            "",
            "## Nonclaims",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in artifact["nonclaims"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs(
    artifact: dict[str, Any],
    *,
    output_json: Path,
    value_csv: Path,
    score_csv: Path,
    curvature_csv: Path,
    status_csv: Path,
    uncertainty_csv: Path,
    markdown: Path,
) -> None:
    artifact = dict(artifact)
    artifact.pop("_started_wall_time", None)
    artifact["run_manifest"] = dict(artifact["run_manifest"])
    artifact["run_manifest"]["wall_time_seconds"] = round(
        time.time() - build_outputs_start_time,
        6,
    )
    artifact["run_manifest"]["output_json"] = _rel(output_json)
    artifact["run_manifest"]["value_csv"] = _rel(value_csv)
    artifact["run_manifest"]["score_csv"] = _rel(score_csv)
    artifact["run_manifest"]["curvature_csv"] = _rel(curvature_csv)
    artifact["run_manifest"]["status_csv"] = _rel(status_csv)
    artifact["run_manifest"]["uncertainty_csv"] = _rel(uncertainty_csv)
    artifact["run_manifest"]["summary_markdown"] = _rel(markdown)
    output_json.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    cells = artifact["cells"]
    _write_csv(
        value_csv,
        cells,
        [
            "algorithm_id",
            "model_row_id",
            "numeric_execution_status",
            "log_likelihood",
            "average_log_likelihood",
            "reference_log_likelihood",
            "absolute_value_gap_to_kalman",
            "reason_codes",
        ],
    )
    _write_csv(
        score_csv,
        cells,
        [
            "algorithm_id",
            "model_row_id",
            "numeric_execution_status",
            "score_l2_norm",
            "score_max_component",
            "score_min_component",
            "score",
            "score_coordinate_system",
            "score_derivative_provenance",
            "reason_codes",
        ],
    )
    _write_csv(
        curvature_csv,
        cells,
        [
            "algorithm_id",
            "model_row_id",
            "numeric_execution_status",
            "curvature_status",
            "hessian_min_eigenvalue_negative_log_likelihood",
            "hessian_adapter_status",
            "reason_codes",
        ],
    )
    _write_csv(
        status_csv,
        cells,
        [
            "algorithm_id",
            "model_row_id",
            "dataset_status",
            "target_contract_status",
            "value_adapter_status",
            "score_adapter_status",
            "hessian_adapter_status",
            "numeric_execution_status",
            "not_available_reason",
            "reason_codes",
        ],
    )
    _write_csv(
        uncertainty_csv,
        cells,
        [
            "algorithm_id",
            "model_row_id",
            "numeric_execution_status",
            "mc_standard_error",
            "sample_standard_deviation",
            "data_standard_error",
            "particle_count",
            "seed_count",
            "seed_list",
            "per_seed_results",
            "reason_codes",
        ],
    )
    _write_summary_markdown(markdown, artifact)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--enable-p8d-execution", action="store_true")
    parser.add_argument("--profile-p8g-ledh-prefix", action="store_true")
    parser.add_argument("--profile-p8h-ledh-ot-prefix", action="store_true")
    parser.add_argument("--p8g-fixed-randomness-gradient-check", action="store_true")
    parser.add_argument("--p8g-particle-tuning-stage0", action="store_true")
    parser.add_argument("--p8g-particle-tuning-full", action="store_true")
    parser.add_argument("--p8h-particle-tuning-stage0", action="store_true")
    parser.add_argument("--p8j-sir-particle-tuning-stage0", action="store_true")
    parser.add_argument("--p8j-sir-ot-sinkhorn-diagnostic", action="store_true")
    parser.add_argument("--p8h-ot-gradient-check", action="store_true")
    parser.add_argument("--p8h-hmc-tier0-smoke", action="store_true")
    parser.add_argument("--row", default=SV_ROW)
    parser.add_argument(
        "--rows",
        default="actual_sv",
        help="Comma-separated row aliases for P8g modes; G3/G4 initial scope is actual_sv only.",
    )
    parser.add_argument("--algorithm", default=LEDH_ALG1_DPF)
    parser.add_argument("--algorithms", default=LEDH_ALG1_DPF)
    parser.add_argument("--horizon", type=int, default=50)
    parser.add_argument(
        "--horizons",
        help="Comma-separated horizon prefixes for G4 particle tuning.",
    )
    parser.add_argument("--particles", default="32")
    parser.add_argument(
        "--seeds",
        default="81120,81121,81122,81123,81124",
        help="Comma-separated integer seeds for P8g profile mode.",
    )
    parser.add_argument("--device", choices=["cpu", "gpu"], default="cpu")
    parser.add_argument("--g0-manifest", type=Path)
    parser.add_argument("--p8g-vectorized-particles", action="store_true")
    parser.add_argument("--p8g-sv-scalar-graph", action="store_true")
    parser.add_argument("--route-variant", default="p8g_sv_scalar_graph")
    parser.add_argument("--p8h-resampling-route", default=P8H_DEFAULT_RESAMPLING_ROUTE)
    parser.add_argument(
        "--p8h-profile-manifest-phase",
        default="P8H_PHASE5_VALUE_FILTERING_TUNING",
    )
    parser.add_argument("--p8h-profile-manifest-plan", type=Path)
    parser.add_argument(
        "--p8j-profile-manifest-phase",
        default="P8J_PHASE5_SIR_PARTICLE_TUNING",
    )
    parser.add_argument("--p8j-profile-manifest-plan", type=Path)
    parser.add_argument("--p8j-sinkhorn-epsilon-policy", default="fixed")
    parser.add_argument(
        "--p8h-gradient-manifest-phase",
        default="P8H_PHASE6_OT_GRADIENT_CHECKS",
    )
    parser.add_argument("--p8h-gradient-manifest-plan", type=Path)
    parser.add_argument("--p8h-gradient-fd-threshold", type=float, default=1e-5)
    parser.add_argument("--coordinate", default="canonical_unconstrained")
    parser.add_argument(
        "--runtime-budget-seconds",
        type=float,
        default=P8G_G4_DEFAULT_RUNTIME_BUDGET_SECONDS,
    )
    parser.add_argument("--hmc-num-results", type=int, default=2)
    parser.add_argument("--hmc-num-burnin-steps", type=int, default=1)
    parser.add_argument("--hmc-step-size", type=float, default=0.005)
    parser.add_argument("--hmc-num-leapfrog-steps", type=int, default=1)
    parser.add_argument("--p8h-hmc-manifest-phase", default="P8H_PHASE8_HMC_TIER0_SMOKE")
    parser.add_argument("--p8h-hmc-manifest-plan", type=Path)
    parser.add_argument(
        "--p8h-hmc-policy-label",
        default="fixed_kernel_no_adaptation_tier0_execution_smoke",
    )
    parser.add_argument("--p8h-hmc-tier-label", default="tier0_execution_smoke")
    parser.add_argument("--p8h-hmc-schema-version", default="filter_bench.p8h_hmc_tier0.v1")
    parser.add_argument("--p8h-hmc-status-success-label", default="executed_p8h_hmc_tier0_smoke")
    parser.add_argument("--p8h-hmc-status-blocked-label", default="blocked_p8h_hmc_tier0_smoke")
    parser.add_argument("--p8h-hmc-blocker-reason", default="BLOCK_P8H_HMC_TIER0_SMOKE")
    parser.add_argument("--p8h-hmc-evidence-question")
    parser.add_argument("--p8h-hmc-evidence-baseline")
    parser.add_argument("--p8h-hmc-evidence-primary-criterion")
    parser.add_argument("--p8h-hmc-predecessor-results-json")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--output-csv", type=Path)
    parser.add_argument("--append-json", type=Path)
    parser.add_argument("--selected-blocked-csv", type=Path)
    parser.add_argument("--value-csv", type=Path, default=DEFAULT_VALUE_CSV)
    parser.add_argument("--score-csv", type=Path, default=DEFAULT_SCORE_CSV)
    parser.add_argument("--curvature-csv", type=Path, default=DEFAULT_CURVATURE_CSV)
    parser.add_argument("--status-csv", type=Path, default=DEFAULT_STATUS_CSV)
    parser.add_argument("--uncertainty-csv", type=Path, default=DEFAULT_UNCERTAINTY_CSV)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()
    if args.profile_p8g_ledh_prefix:
        payload = _p8g_profile_dpf_prefix(
            row_id=args.row,
            algorithm_id=args.algorithm,
            horizon=args.horizon,
            particle_count=int(args.particles),
            seeds=_parse_int_csv(args.seeds),
            device=args.device,
            g0_manifest=args.g0_manifest,
            vectorized_particles=args.p8g_vectorized_particles,
            sv_scalar_graph=args.p8g_sv_scalar_graph,
        )
        args.output_json.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return
    if args.profile_p8h_ledh_ot_prefix:
        payload = _p8h_profile_dpf_prefix(
            row_id=args.row,
            algorithm_id=args.algorithm,
            horizon=args.horizon,
            particle_count=int(args.particles),
            seeds=_parse_int_csv(args.seeds),
            device=args.device,
            g0_manifest=args.g0_manifest,
            resampling_route=args.p8h_resampling_route,
        )
        args.output_json.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return
    if args.p8g_fixed_randomness_gradient_check:
        row_aliases = [item.strip() for item in args.rows.split(",") if item.strip()]
        row_map = {"actual_sv": SV_ROW, SV_ROW: SV_ROW}
        rows = [row_map.get(alias, alias) for alias in row_aliases]
        payload = _p8g_fixed_randomness_gradient_check(
            rows=rows,
            horizon=args.horizon,
            particle_count=int(args.particles),
            seeds=_parse_int_csv(args.seeds),
            route_variant=args.route_variant,
            coordinate=args.coordinate,
            device=args.device,
            g0_manifest=args.g0_manifest,
        )
        args.output_json.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        if args.output_csv is not None:
            _write_p8g_gradient_csv(args.output_csv, payload)
        return
    if args.p8h_ot_gradient_check:
        payload = _p8h_ot_gradient_check(
            rows=_parse_rows_csv(args.row),
            horizon=args.horizon,
            particle_count=int(args.particles),
            seeds=_parse_int_csv(args.seeds),
            resampling_route=args.p8h_resampling_route,
            coordinate=args.coordinate,
            device=args.device,
            g0_manifest=args.g0_manifest,
            manifest_phase=args.p8h_gradient_manifest_phase,
            manifest_plan=args.p8h_gradient_manifest_plan,
            runtime_budget_seconds=float(args.runtime_budget_seconds),
            finite_difference_max_abs_threshold=float(args.p8h_gradient_fd_threshold),
        )
        args.output_json.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        if args.output_csv is not None:
            _write_p8h_gradient_csv(args.output_csv, payload)
        return
    if args.p8h_hmc_tier0_smoke:
        payload = _p8h_hmc_tier0_smoke(
            rows=_parse_rows_csv(args.row),
            algorithm_id=args.algorithm,
            horizon=args.horizon,
            particle_count=int(args.particles),
            seeds=_parse_int_csv(args.seeds),
            resampling_route=args.p8h_resampling_route,
            coordinate=args.coordinate,
            device=args.device,
            g0_manifest=args.g0_manifest,
            num_results=args.hmc_num_results,
            num_burnin_steps=args.hmc_num_burnin_steps,
            step_size=args.hmc_step_size,
            num_leapfrog_steps=args.hmc_num_leapfrog_steps,
            manifest_phase=args.p8h_hmc_manifest_phase,
            manifest_plan=args.p8h_hmc_manifest_plan,
            runtime_budget_seconds=float(args.runtime_budget_seconds),
            hmc_policy_label=args.p8h_hmc_policy_label,
            hmc_tier_label=args.p8h_hmc_tier_label,
            schema_version=args.p8h_hmc_schema_version,
            status_success_label=args.p8h_hmc_status_success_label,
            status_blocked_label=args.p8h_hmc_status_blocked_label,
            blocker_reason=args.p8h_hmc_blocker_reason,
            evidence_question=args.p8h_hmc_evidence_question,
            evidence_baseline=args.p8h_hmc_evidence_baseline,
            evidence_primary_criterion=args.p8h_hmc_evidence_primary_criterion,
            predecessor_results=(
                json.loads(args.p8h_hmc_predecessor_results_json)
                if args.p8h_hmc_predecessor_results_json
                else None
            ),
        )
        args.output_json.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        if args.output_csv is not None:
            _write_p8h_hmc_tier0_csv(args.output_csv, payload)
        return
    if args.p8g_particle_tuning_stage0 or args.p8g_particle_tuning_full:
        if args.p8g_particle_tuning_stage0 and args.p8g_particle_tuning_full:
            raise SystemExit("choose either --p8g-particle-tuning-stage0 or --p8g-particle-tuning-full")
        stage = "stage0" if args.p8g_particle_tuning_stage0 else "full"
        rows = _parse_rows_csv(args.rows) if stage == "stage0" else [_parse_rows_csv(args.row)[0]]
        algorithms = _parse_str_csv(args.algorithms if stage == "stage0" else args.algorithm)
        horizons = (
            _parse_int_csv(args.horizons)
            if args.horizons is not None
            else ([50, 200] if stage == "stage0" else [ROW_HORIZONS[rows[0]]])
        )
        payload = _p8g_g4_tuning_payload(
            stage=stage,
            rows=rows,
            algorithms=algorithms,
            horizons=horizons,
            particles=_parse_int_csv(args.particles),
            seeds=_parse_int_csv(args.seeds),
            route_variant=args.route_variant,
            device=args.device,
            g0_manifest=args.g0_manifest,
            runtime_budget_seconds=float(args.runtime_budget_seconds),
        )
        if args.append_json is not None:
            _append_p8g_particle_tuning_jsonl(args.append_json, payload)
        else:
            args.output_json.write_text(
                json.dumps(payload, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        if args.output_csv is not None:
            _write_p8g_particle_tuning_csv(args.output_csv, payload)
        selected_blocked_csv = args.selected_blocked_csv or P8G_G4_SELECTED_BLOCKED_CSV
        _write_p8g_selected_blocked_csv(selected_blocked_csv, payload)
        return
    if args.p8h_particle_tuning_stage0:
        rows = _parse_rows_csv(args.row)
        algorithms = _parse_str_csv(args.algorithm)
        horizons = _parse_int_csv(args.horizons) if args.horizons is not None else [4, 8]
        payload = _p8h_phase5_tuning_payload(
            rows=rows,
            algorithms=algorithms,
            horizons=horizons,
            particles=_parse_int_csv(args.particles),
            seeds=_parse_int_csv(args.seeds),
            resampling_route=args.p8h_resampling_route,
            device=args.device,
            g0_manifest=args.g0_manifest,
            runtime_budget_seconds=float(args.runtime_budget_seconds),
            manifest_phase=args.p8h_profile_manifest_phase,
            manifest_plan=args.p8h_profile_manifest_plan,
        )
        args.output_json.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        if args.output_csv is not None:
            _write_p8h_particle_tuning_csv(args.output_csv, payload)
        selected_blocked_csv = args.selected_blocked_csv or P8H_PHASE5_SELECTED_BLOCKED_CSV
        _write_p8h_selected_blocked_csv(selected_blocked_csv, payload)
        return
    if args.p8j_sir_particle_tuning_stage0:
        rows = _parse_rows_csv(args.row)
        algorithms = _parse_str_csv(args.algorithms)
        horizons = _parse_int_csv(args.horizons) if args.horizons is not None else [ROW_HORIZONS[SIR_ROW]]
        payload = _p8j_phase5_tuning_payload(
            rows=rows,
            algorithms=algorithms,
            horizons=horizons,
            particles=_parse_int_csv(args.particles),
            seeds=_parse_int_csv(args.seeds),
            device=args.device,
            g0_manifest=args.g0_manifest,
            runtime_budget_seconds=float(args.runtime_budget_seconds),
            manifest_phase=args.p8j_profile_manifest_phase,
            manifest_plan=args.p8j_profile_manifest_plan,
            sinkhorn_epsilon_policy=args.p8j_sinkhorn_epsilon_policy,
        )
        args.output_json.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        if args.output_csv is not None:
            _write_p8j_particle_tuning_csv(args.output_csv, payload)
        selected_blocked_csv = args.selected_blocked_csv or P8J_PHASE5_SELECTED_BLOCKED_CSV
        _write_p8j_selected_blocked_csv(selected_blocked_csv, payload)
        return
    if args.p8j_sir_ot_sinkhorn_diagnostic:
        rows = _parse_rows_csv(args.row)
        if len(rows) != 1:
            raise SystemExit("--p8j-sir-ot-sinkhorn-diagnostic expects exactly one row")
        seeds = _parse_int_csv(args.seeds)
        if len(seeds) != 1:
            raise SystemExit("--p8j-sir-ot-sinkhorn-diagnostic expects exactly one seed")
        payload = _p8j_sir_ot_sinkhorn_diagnostic(
            row_id=rows[0],
            horizon=int(args.horizon),
            particle_count=int(args.particles),
            seed=int(seeds[0]),
            device=args.device,
            g0_manifest=args.g0_manifest,
            runtime_budget_seconds=float(args.runtime_budget_seconds),
            resampling_route=args.p8h_resampling_route,
        )
        args.output_json.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return
    if not args.enable_p8d_execution:
        raise SystemExit(P8D_EXECUTION_GATE_MESSAGE)
    artifact = build_artifact()
    write_outputs(
        artifact,
        output_json=args.output_json,
        value_csv=args.value_csv,
        score_csv=args.score_csv,
        curvature_csv=args.curvature_csv,
        status_csv=args.status_csv,
        uncertainty_csv=args.uncertainty_csv,
        markdown=args.markdown,
    )


build_outputs_start_time = time.time()


if __name__ == "__main__":
    main()
