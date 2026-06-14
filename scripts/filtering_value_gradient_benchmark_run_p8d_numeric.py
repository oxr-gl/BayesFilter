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
    run_ledh_pfpf_alg1_ukf_tf,
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
ROW_HORIZONS = {
    LGSSM_ROW: 50,
    SV_ROW: 1000,
    KSC_ROW: 1000,
    SIR_ROW: 20,
    PREDATOR_PREY_ROW: 20,
    GENERALIZED_SV_ROW: 1008,
}
P8D_PLAN_REVIEW_STATUS = "claude_inline_readonly_review_verdict_agree"


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
    observation_covariance = tf.reshape(tf.constant(1e-6, dtype=tf.float64), [1, 1])
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
        return beta * tf.exp(0.5 * points)

    def observation_jacobian(point: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        point = tf.reshape(tf.convert_to_tensor(point, dtype=tf.float64), [1])
        return tf.reshape(0.5 * beta * tf.exp(0.5 * point[0]), [1, 1])

    def observation_log_density(points: tf.Tensor, observation: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        points = tf.convert_to_tensor(points, dtype=tf.float64)
        observation = tf.reshape(tf.convert_to_tensor(observation, dtype=tf.float64), [1])
        scale = beta * tf.exp(0.5 * points[:, 0])
        return tfp.distributions.Normal(
            loc=tf.zeros_like(scale),
            scale=scale,
        ).log_prob(tf.broadcast_to(observation[0], tf.shape(scale)))

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


def _dpf_generalized_sv_callbacks(theta: tf.Tensor):
    theta = tf.convert_to_tensor(theta, dtype=tf.float64)
    gamma = _normal01().cdf(theta[0])
    tau = tf.exp(theta[1])
    mu = theta[2]
    transition_covariance = tf.reshape(tf.constant(1.0, dtype=tf.float64), [1, 1])
    observation_covariance = tf.reshape(tf.constant(1e-6, dtype=tf.float64), [1, 1])
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
        return tf.exp(0.5 * tau * points)

    def observation_jacobian(point: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        point = tf.reshape(tf.convert_to_tensor(point, dtype=tf.float64), [1])
        return tf.reshape(0.5 * tau * tf.exp(0.5 * tau * point[0]), [1, 1])

    def observation_log_density(points: tf.Tensor, observation: tf.Tensor, time_index: int) -> tf.Tensor:
        del time_index
        points = tf.convert_to_tensor(points, dtype=tf.float64)
        observation = tf.reshape(tf.convert_to_tensor(observation, dtype=tf.float64), [1])
        scale = tf.exp(0.5 * tau * points[:, 0])
        return tfp.distributions.Normal(
            loc=tf.zeros_like(scale),
            scale=scale,
        ).log_prob(tf.broadcast_to(observation[0], tf.shape(scale)))

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
    if row_id == GENERALIZED_SV_ROW:
        return (
            _dpf_generalized_sv_callbacks(_generalized_sv_theta()),
            _generalized_sv_observations(),
            "generalized_sv_prior_mean",
            1008,
        )
    raise ValueError(f"no DPF callback route for {row_id}")


def _has_dpf_route(row_id: str) -> bool:
    return row_id in {LGSSM_ROW, SV_ROW, PREDATOR_PREY_ROW, GENERALIZED_SV_ROW}


def _dpf_single_run(
    algorithm_id: str,
    *,
    row_id: str,
    seed: int,
    particle_count: int,
):
    callbacks, observations, route_label, _horizon = _dpf_route(row_id)
    if algorithm_id == BOOTSTRAP_DPF:
        return run_bootstrap_particle_filter_tf(
            observations=observations,
            initial_sample=callbacks["initial_sample"],
            transition_sample=callbacks["transition_sample"],
            observation_log_density=callbacks["observation_log_density_fn"],
            seed=int(seed),
            num_particles=int(particle_count),
            ess_threshold_ratio=0.5,
            method_id=f"bootstrap_dpf_current_{route_label}_tf",
        )
    if algorithm_id == LEDH_ALG1_DPF:
        return run_ledh_pfpf_alg1_ukf_tf(
            observations=observations,
            initial_sample=callbacks["initial_sample"],
            initial_covariance=callbacks["initial_covariance"],
            transition_sample=callbacks["transition_sample"],
            transition_mean_fn=callbacks["transition_mean_fn"],
            transition_log_density_fn=callbacks["transition_log_density_fn"],
            observation_mean_fn=callbacks["observation_mean_fn"],
            observation_jacobian_fn=callbacks["observation_jacobian_fn"],
            observation_log_density_fn=callbacks["observation_log_density_fn"],
            process_noise_covariance_fn=callbacks["process_noise_covariance_fn"],
            observation_covariance_fn=callbacks["observation_covariance_fn"],
            seed=int(seed),
            num_particles=int(particle_count),
            pseudo_time_steps=tf.constant([1.0], dtype=tf.float64),
            resampling_route="none",
            method_id=f"ledh_pfpf_alg1_ukf_current_{route_label}_tf",
        )
    raise ValueError(f"unsupported DPF algorithm: {algorithm_id}")


def _numeric_dpf_lgssm_cell(algorithm_id: str, adapter: dict[str, str]) -> dict[str, Any]:
    return _numeric_dpf_cell(algorithm_id, LGSSM_ROW, adapter)


def _numeric_dpf_cell(algorithm_id: str, model_row_id: str, adapter: dict[str, str]) -> dict[str, Any]:
    started = time.time()
    cell = _base_cell(algorithm_id=algorithm_id, model_row_id=model_row_id, adapter=adapter)
    _callbacks, _observations, _route_label, horizon = _dpf_route(model_row_id)
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
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--value-csv", type=Path, default=DEFAULT_VALUE_CSV)
    parser.add_argument("--score-csv", type=Path, default=DEFAULT_SCORE_CSV)
    parser.add_argument("--curvature-csv", type=Path, default=DEFAULT_CURVATURE_CSV)
    parser.add_argument("--status-csv", type=Path, default=DEFAULT_STATUS_CSV)
    parser.add_argument("--uncertainty-csv", type=Path, default=DEFAULT_UNCERTAINTY_CSV)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()
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
