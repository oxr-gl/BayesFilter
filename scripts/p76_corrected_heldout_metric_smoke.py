#!/usr/bin/env python
"""Tiny CPU-only smoke for the P76 corrected heldout metric."""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import shlex
import sys
from typing import Any, Mapping, Sequence

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("MPLCONFIGDIR", "/tmp")

import tensorflow as tf

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import bayesfilter.highdim as highdim
from bayesfilter.highdim import stochastic_density_training as p76_metric


STATUS = "P76_PHASE9_CORRECTED_HELDOUT_METRIC_SMOKE_COMPLETED"
SCHEMA_VERSION = "p76.phase9.corrected_heldout_metric_smoke.v1"
DEFAULT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p76-phase9-corrected-heldout-metric-smoke-2026-06-19.json"
)
NONCLAIMS = (
    "metric-only smoke",
    "not training evidence",
    "not fit-quality evidence",
    "not lower-gate repair evidence",
    "not validation evidence",
    "not HMC readiness evidence",
    "not scaling evidence",
    "not source-faithful Zhao-Cui",
    "not final rank or sample policy",
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    payload = run_smoke(run_manifest=_actual_run_manifest(args.output))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n")
    return 0


def run_smoke(*, run_manifest: Mapping[str, object]) -> Mapping[str, object]:
    config = _config()
    trainer = p76_metric.TrainableFunctionalTT(config, initial_cores=_initial_cores())
    batch = _metric_batch()
    terms = trainer.corrected_heldout_density_metric(batch)
    corrected_alpha = trainer.corrected_heldout_metric_weights(batch)
    rho_theta = trainer.rho_theta(batch.points)
    normalizer = trainer.normalizer()
    historical_alpha = _historical_helper_boundary_alpha(trainer, batch)
    expected_corrected_alpha = tf.constant([0.0, 0.125, 0.375, 0.5], dtype=tf.float64)
    expected_historical_alpha = tf.constant(
        [2.5 / 16.5, 5.5 / 16.5, 5.25 / 16.5, 3.25 / 16.5],
        dtype=tf.float64,
    )
    reconstructed_ce = -tf.reduce_sum(
        corrected_alpha * tf.math.log(rho_theta)
    ) + tf.math.log(normalizer)
    alpha_l1_distance = tf.reduce_sum(tf.abs(corrected_alpha - historical_alpha))
    payload = p76_metric.corrected_heldout_metric_terms_payload(terms)
    finite_payload_flags = dict(payload["finite_flags"])
    return {
        "schema_version": SCHEMA_VERSION,
        "status": STATUS,
        "run_manifest": run_manifest,
        "cpu_only": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "default_behavior_changed": False,
        "train_step_count": 0,
        "optimizer_used": False,
        "generated_target_cloud_used": False,
        "source_route_prefit_used": False,
        "audit_data_used": False,
        "fixture": {
            "dimension": config.product_basis.dimension,
            "degree": 1,
            "ranks": config.ranks,
            "tau": float(config.tau.numpy()),
            "defensive_q0_values": [1.0, 1.0, 1.0, 1.0],
            "points": _tensor_list(batch.points),
            "target_sqrt_values": _tensor_list(batch.target_sqrt_values),
            "integration_weights": _tensor_list(batch.integration_weights),
            "role": batch.role,
            "provenance_label": batch.provenance_label,
        },
        "metric_payload": payload,
        "corrected_alpha": _tensor_list(corrected_alpha),
        "expected_corrected_alpha": _tensor_list(expected_corrected_alpha),
        "corrected_alpha_max_abs_error": float(
            tf.reduce_max(tf.abs(corrected_alpha - expected_corrected_alpha)).numpy()
        ),
        "historical_helper_boundary_only": {
            "label": "historical_helper_boundary_only",
            "alpha": _tensor_list(historical_alpha),
            "expected_alpha": _tensor_list(expected_historical_alpha),
            "alpha_max_abs_error": float(
                tf.reduce_max(tf.abs(historical_alpha - expected_historical_alpha)).numpy()
            ),
            "alpha_l1_distance_from_corrected": float(alpha_l1_distance.numpy()),
        },
        "rho_theta_values": _tensor_list(rho_theta),
        "normalizer": float(normalizer.numpy()),
        "reconstructed_heldout_cross_entropy": float(reconstructed_ce.numpy()),
        "heldout_cross_entropy_reconstruction_abs_error": float(
            tf.abs(reconstructed_ce - terms.heldout_cross_entropy).numpy()
        ),
        "finite_flags": {
            **finite_payload_flags,
            "rho_theta_values": bool(tf.reduce_all(tf.math.is_finite(rho_theta)).numpy()),
            "reconstructed_heldout_cross_entropy": bool(
                tf.math.is_finite(reconstructed_ce).numpy()
            ),
        },
        "manual_fixture_hand_checks": {
            "corrected_alpha_matches_expected": bool(
                tf.reduce_max(tf.abs(corrected_alpha - expected_corrected_alpha)).numpy()
                <= 1e-14
            ),
            "historical_alpha_matches_expected": bool(
                tf.reduce_max(tf.abs(historical_alpha - expected_historical_alpha)).numpy()
                <= 1e-14
            ),
            "ce_reconstruction_matches_metric": bool(
                tf.abs(reconstructed_ce - terms.heldout_cross_entropy).numpy() <= 1e-14
            ),
            "old_new_alpha_separated": bool(alpha_l1_distance.numpy() > 0.0),
        },
        "nonclaims": NONCLAIMS,
    }


def _config() -> p76_metric.P75TrainableTTConfig:
    return p76_metric.P75TrainableTTConfig(
        product_basis=_basis(),
        ranks=(1, 2, 1),
        tau=tf.constant(2.5, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-14, dtype=tf.float64),
        denominator_floor=tf.constant(1e-300, dtype=tf.float64),
        l2_weight=tf.constant(0.0, dtype=tf.float64),
        learning_rate=1e-3,
        gradient_clip_norm=10.0,
        seed=7609,
        metadata={
            "fixture": "p76_phase9_corrected_heldout_metric_smoke",
            "metric_only": True,
            "manual_metric_fixture": True,
        },
    )


def _basis() -> highdim.ProductBasis:
    convention = highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )
    return highdim.ProductBasis(
        [
            highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 1),
            highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 1),
        ],
        convention,
    )


def _initial_cores() -> tuple[tf.Tensor, tf.Tensor]:
    return (
        tf.constant([[[0.4, -0.1], [0.2, 0.3]]], dtype=tf.float64),
        tf.constant([[[0.5], [0.1]], [[-0.2], [0.4]]], dtype=tf.float64),
    )


def _metric_batch() -> p76_metric.P76CorrectedHeldoutMetricBatch:
    points = tf.constant(
        [
            [-0.75, -0.25],
            [-0.25, 0.50],
            [0.25, -0.50],
            [0.75, 0.25],
        ],
        dtype=tf.float64,
    )
    records = tuple(
        {
            "point_id": f"p76-phase9-metric-{index}",
            "role": "heldout_metric",
            "provenance_label": "manual_metric_fixture",
        }
        for index in range(4)
    )
    return p76_metric.P76CorrectedHeldoutMetricBatch(
        points=points,
        target_sqrt_values=tf.constant([0.0, 0.5, 1.0, 2.0], dtype=tf.float64),
        integration_weights=tf.constant([1.0, 2.0, 1.5, 0.5], dtype=tf.float64),
        role="heldout_metric",
        provenance_label="manual_metric_fixture",
        point_records=records,
    )


def _historical_helper_boundary_alpha(
    trainer: p76_metric.TrainableFunctionalTT,
    batch: p76_metric.P76CorrectedHeldoutMetricBatch,
) -> tf.Tensor:
    q0 = tf.exp(trainer.defensive_density.log_density(batch.points))
    raw = batch.integration_weights * (tf.square(batch.target_sqrt_values) + trainer.config.tau * q0)
    return raw / tf.reduce_sum(raw)


def _actual_run_manifest(output: Path) -> Mapping[str, object]:
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
        "output": str(output),
        "environment": environment,
        "cpu_only": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "tensorflow_version": tf.__version__,
    }


def _tensor_list(value: tf.Tensor) -> Any:
    return _jsonable(tf.convert_to_tensor(value, dtype=tf.float64).numpy().tolist())


def _jsonable(value: Any) -> Any:
    if hasattr(value, "numpy"):
        return _jsonable(value.numpy())
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, float):
        if math.isnan(value):
            return "nan"
        if math.isinf(value):
            return "inf" if value > 0 else "-inf"
        return value
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    try:
        return float(value)
    except (TypeError, ValueError):
        return str(value)


if __name__ == "__main__":
    sys.exit(main())
