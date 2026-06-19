"""Tiny CPU-only smoke for the P76 UKF initializer."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shlex
import sys
from typing import Mapping, Sequence

import tensorflow as tf

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import bayesfilter.highdim as highdim
from bayesfilter.highdim import stochastic_density_training as p75
from bayesfilter.highdim import ukf_initializer as p76
from bayesfilter.highdim.ukf_scout import P52_UKF_SCOUT_CLAIM, UKFScoutResult


STATUS = "P76_PHASE4_TINY_SMOKE_COMPLETED"
NONCLAIMS = (
    "not lower-gate repair evidence",
    "not validation evidence",
    "not HMC readiness evidence",
    "not large-pilot evidence",
    "not scaling evidence",
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    output = Path(args.output)
    payload = run_smoke(run_manifest=_actual_run_manifest())
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return 0


def run_smoke(*, run_manifest: Mapping[str, object]) -> Mapping[str, object]:
    product_basis = _basis(dimension=4, degree=2)
    config = p76.P76UKFInitializerConfig(
        product_basis=product_basis,
        ranks=(1, 4, 4, 4, 1),
        time_index=1,
        quadrature_order=16,
    )
    initializer = p76.p76_build_ukf_initializer(_scout(), config)
    trainer_config = p75.P75TrainableTTConfig(
        product_basis=product_basis,
        ranks=config.ranks,
        tau=tf.constant(1e-6, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-14, dtype=tf.float64),
        denominator_floor=tf.constant(1e-300, dtype=tf.float64),
        l2_weight=tf.constant(1e-8, dtype=tf.float64),
        learning_rate=1e-3,
        gradient_clip_norm=10.0,
        seed=7604,
    )
    trainer = p75.TrainableFunctionalTT(trainer_config, initial_cores=initializer.cores)
    points = _tiny_training_points()
    target_values = tf.exp(-0.5 * tf.reduce_sum(tf.square(points), axis=1))
    batch = p75.P75ObjectiveBatch(
        points=points,
        target_values=target_values,
        weights=tf.ones([int(points.shape[0])], dtype=tf.float64),
        point_records=tuple(
            {
                "point_id": f"p76-phase4-fit-{index}",
                "cloud_hash": "p76-phase4-train-cloud",
                "role": "fit",
            }
            for index in range(int(points.shape[0]))
        ),
        forbidden_audit_records=(
            {
                "point_id": "p76-phase4-audit-sentinel",
                "cloud_hash": "p76-phase4-audit-cloud",
                "role": "audit",
            },
        ),
        provenance_label="p76_phase4_tiny_training_only",
    )
    optimizer = p75.make_adam_optimizer(trainer_config)
    terms = trainer.train_step(batch, optimizer)
    rho = trainer.rho_theta(points)
    normalizer = trainer.normalizer()
    log_density = trainer.log_density(points)
    finite_initializer_cores = all(
        bool(tf.reduce_all(tf.math.is_finite(core.values)).numpy())
        for core in initializer.cores
    )
    finite_total_loss = _finite_scalar(terms.total_loss)
    finite_gradient_norm = terms.gradient_norm is not None and _finite_scalar(terms.gradient_norm)
    finite_rho = bool(tf.reduce_all(tf.math.is_finite(rho)).numpy())
    finite_normalizer = _finite_scalar(normalizer)
    finite_log_density = bool(tf.reduce_all(tf.math.is_finite(log_density)).numpy())
    cpu_only = os.environ.get("CUDA_VISIBLE_DEVICES") == "-1"
    return {
        "schema_version": "p76.phase4.tiny_ukf_initializer_smoke.v1",
        "status": STATUS,
        "run_manifest": run_manifest,
        "cpu_only": cpu_only,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "initializer_rule": p76.P76_UKF_INITIALIZER_RULE,
        "source_route_prefit_used": False,
        "audit_data_used": False,
        "default_behavior_changed": False,
        "finite_initializer_cores": finite_initializer_cores,
        "finite_total_loss": finite_total_loss,
        "finite_gradient_norm": finite_gradient_norm,
        "finite_rho_theta": finite_rho,
        "finite_normalizer": finite_normalizer,
        "finite_log_density": finite_log_density,
        "total_loss": float(terms.total_loss.numpy()),
        "gradient_norm": float(tf.convert_to_tensor(terms.gradient_norm).numpy()),
        "normalizer": float(normalizer.numpy()),
        "rho_min": float(tf.reduce_min(rho).numpy()),
        "rho_max": float(tf.reduce_max(rho).numpy()),
        "log_density_min": float(tf.reduce_min(log_density).numpy()),
        "log_density_max": float(tf.reduce_max(log_density).numpy()),
        "train_step_count": 1,
        "initializer_manifest": dict(initializer.manifest),
        "nonclaims": NONCLAIMS,
    }


def _basis(*, dimension: int, degree: int) -> highdim.ProductBasis:
    convention = highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )
    return highdim.ProductBasis(
        [
            highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), degree)
            for _ in range(int(dimension))
        ],
        convention,
    )


def _scout() -> UKFScoutResult:
    mean_path = tf.constant([[1.0, 2.0], [3.0, 4.0]], dtype=tf.float64)
    covariance_path = tf.constant(
        [
            [[1.0, 0.1], [0.1, 2.0]],
            [[3.0, 0.2], [0.2, 4.0]],
        ],
        dtype=tf.float64,
    )
    return UKFScoutResult(
        dimension=2,
        compartments=1,
        horizon=1,
        sigma_point_count=5,
        mean_path=mean_path,
        covariance_path=covariance_path,
        scale_path=tf.sqrt(tf.linalg.diag_part(covariance_path)),
        covariance_eigenvalues=tf.linalg.eigvalsh(covariance_path),
        effective_dimension_path=tf.constant([2, 2], dtype=tf.int32),
        max_abs_correlation_path=tf.constant([0.1, 0.1], dtype=tf.float64),
        process_covariance_shape=(2, 2),
        process_covariance_diagonal_range=(1.0, 1.0),
        observation_covariance_shape=(1, 1),
        observation_covariance_diagonal_range=(1.0, 1.0),
        initial_covariance_shape=(2, 2),
        initial_covariance_diagonal_range=(1.0, 2.0),
        status="PASS_P52_UKF_SCOUT",
        claim_class=P52_UKF_SCOUT_CLAIM,
        nonclaims=(
            "scout_not_truth",
            "no filtering correctness",
            "no exact likelihood",
            "no HMC readiness",
        ),
    )


def _tiny_training_points() -> tf.Tensor:
    return tf.constant(
        [
            [0.0, 0.0, 0.0, 0.0],
            [0.25, -0.25, 0.50, -0.50],
            [-0.50, 0.25, -0.25, 0.50],
            [0.75, -0.50, 0.25, -0.25],
        ],
        dtype=tf.float64,
    )


def _finite_scalar(value: tf.Tensor) -> bool:
    tensor = tf.convert_to_tensor(value, dtype=tf.float64)
    return tensor.shape.rank == 0 and bool(tf.math.is_finite(tensor).numpy())


def _actual_run_manifest() -> Mapping[str, object]:
    env_keys = ("CUDA_VISIBLE_DEVICES", "MPLCONFIGDIR", "PWD")
    environment = {key: os.environ.get(key) for key in env_keys}
    python_argv = [sys.executable, *sys.argv]
    env_prefix = [
        f"{key}={value}"
        for key in ("CUDA_VISIBLE_DEVICES", "MPLCONFIGDIR")
        if (value := os.environ.get(key)) is not None
    ]
    replay_parts = [*env_prefix, *python_argv]
    return {
        "command": " ".join(shlex.quote(part) for part in replay_parts),
        "python_executable": sys.executable,
        "argv": list(sys.argv),
        "python_argv": python_argv,
        "environment": environment,
        "cpu_only": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "tensorflow_version": tf.__version__,
    }


if __name__ == "__main__":
    sys.exit(main())
