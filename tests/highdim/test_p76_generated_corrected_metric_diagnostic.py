from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest
import tensorflow as tf

import scripts.p76_generated_corrected_metric_diagnostic as diagnostic
from bayesfilter.highdim import stochastic_density_training as p76_metric


def _config() -> p76_metric.P75TrainableTTConfig:
    import bayesfilter.highdim as highdim

    convention = highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )
    basis = highdim.ProductBasis(
        [
            highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 1),
            highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 1),
        ],
        convention,
    )
    return p76_metric.P75TrainableTTConfig(
        product_basis=basis,
        ranks=(1, 2, 1),
        tau=tf.constant(2.5, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-14, dtype=tf.float64),
        denominator_floor=tf.constant(1e-300, dtype=tf.float64),
        seed=7610,
    )


def _initial_cores() -> tuple[tf.Tensor, tf.Tensor]:
    return (
        tf.constant([[[0.4, -0.1], [0.2, 0.3]]], dtype=tf.float64),
        tf.constant([[[0.5], [0.1]], [[-0.2], [0.4]]], dtype=tf.float64),
    )


def _data() -> SimpleNamespace:
    return SimpleNamespace(
        local_fit_points=tf.constant(
            [
                [-0.75, -0.25, 0.25, 0.75],
                [-0.25, 0.50, -0.50, 0.25],
            ],
            dtype=tf.float64,
        ),
        target_values=tf.constant([0.0, 0.5, 1.0, 2.0], dtype=tf.float64),
        fit_weights=tf.constant([1.0, 2.0, 1.5, 0.5], dtype=tf.float64),
        manifest={
            "coordinate_frame_hash": "unit-frame",
            "local_clip_fraction": tf.constant(0.0, dtype=tf.float64),
        },
    )


def test_validate_bounds_enforces_reviewed_phase10_limits() -> None:
    diagnostic._validate_bounds(sample_count=32, degree=2, rank=4)
    with pytest.raises(ValueError, match="sample_count"):
        diagnostic._validate_bounds(sample_count=33, degree=2, rank=4)
    with pytest.raises(ValueError, match="degree"):
        diagnostic._validate_bounds(sample_count=32, degree=3, rank=4)
    with pytest.raises(ValueError, match="rank"):
        diagnostic._validate_bounds(sample_count=32, degree=2, rank=5)


def test_seed_manifest_records_pairwise_disjoint_roles_and_stop_policy() -> None:
    manifest = diagnostic._seed_manifest(bridge_training_present=True)

    assert manifest["bridge_training_present"] is True
    assert manifest["bridge_training_role_is_bookkeeping_only"] is True
    assert manifest["pairwise_disjoint_roles"] is True
    assert manifest["overlapping_seed_values"] == {}
    assert manifest["stop_on_overlap"] is True
    assert set(manifest["role_seed_pairs"]) == {
        "shift_calibration",
        "holdout_metric",
        "replay_metric",
        "bridge_training_bookkeeping_only",
    }


def test_metric_batch_from_data_preserves_metric_role_and_provenance() -> None:
    batch = diagnostic._metric_batch_from_data(
        data=_data(),
        label="unit",
        role="heldout_metric",
    )

    assert isinstance(batch, p76_metric.P76CorrectedHeldoutMetricBatch)
    assert batch.role == "heldout_metric"
    assert batch.provenance_label == "reviewed_target_bridge"
    assert batch.points.shape == (4, 2)
    assert not hasattr(batch, "target_values")
    assert not hasattr(batch, "weights")
    assert all(record["role"] == "heldout_metric" for record in batch.point_records)
    assert all(
        record["provenance_label"] == "reviewed_target_bridge"
        for record in batch.point_records
    )


def test_metric_payload_reconstructs_corrected_ce_without_training() -> None:
    trainer = p76_metric.TrainableFunctionalTT(_config(), initial_cores=_initial_cores())

    payload = diagnostic._metric_payload(
        trainer=trainer,
        data=_data(),
        label="unit",
        role="heldout_metric",
    )

    expected_ce = -sum(
        alpha * diagnostic.math.log(rho)
        for alpha, rho in zip(payload["corrected_alpha"], payload["rho_theta_values"])
    ) + diagnostic.math.log(payload["normalizer"])
    assert payload["role"] == "heldout_metric"
    assert payload["provenance_label"] == "reviewed_target_bridge"
    assert payload["heldout_cross_entropy"] == pytest.approx(expected_ce)
    assert payload["reconstructed_heldout_cross_entropy"] == pytest.approx(expected_ce)
    assert payload["heldout_cross_entropy_reconstruction_abs_error"] == pytest.approx(0.0)
    assert payload["corrected_alpha_sum"] == pytest.approx(1.0)
    assert payload["all_primary_values_finite"] is True
    assert payload["not_training_or_selection"] is True


def test_payload_uses_stubbed_context_and_keeps_no_training_contract(monkeypatch, tmp_path) -> None:
    class Initializer:
        cores = _initial_cores()
        manifest = {"unit_initializer": True}

    def fake_context(*, degree: int, rank: int, sample_count: int, seed: int):
        del degree, rank, sample_count, seed
        bridge = {
            "status": "pass",
            "target_dimension": 2,
            "frame_dimension": 2,
            "product_basis_dimension": 2,
            "initializer_dimension": 2,
            "dimension_match": True,
            "frame_hash": "unit-frame",
            "training_frame_hashes": ("unit-frame",),
            "audit_frame_hashes": ("unit-frame", "unit-frame"),
            "reconstruction_max_abs_error": 0.0,
            "target_tieout_max_abs_error": 0.0,
            "target_tieout_source": (
                "actual_batch_target_values_vs_independent_direct_physical_density"
            ),
            "training_clip_fraction_max": 0.0,
            "audit_clip_fraction_max": 0.0,
            "bridge_target_values_finite": True,
            "training_target_values_finite": True,
            "audit_target_values_finite": True,
            "nonfinite_target_value_count": 0,
            "thresholds": {
                "reconstruction_max_abs_error": 1e-10,
                "target_tieout_max_abs_error": 1e-10,
                "training_clip_fraction_max": 0.25,
                "audit_clip_fraction_max": 0.25,
            },
            "blockers": (),
        }
        return {
            "target_dim": 2,
            "shift_constant": tf.constant(0.0, dtype=tf.float64),
            "shift_calibration_data": _data(),
            "train_data_sequence": (_data(),),
            "audit_data_sequence": (_data(), _data()),
            "trainer_config": _config(),
            "initializer": Initializer(),
            "ukf_frame_bridge": bridge,
            "ukf_frame_manifest": {"frame_hash": "unit-frame"},
        }

    monkeypatch.setattr(diagnostic, "_build_context", fake_context)

    payload = diagnostic.generated_corrected_metric_diagnostic_payload(
        output=tmp_path / "phase10.json",
        sample_count=32,
        degree=2,
        rank=4,
        seed=7610,
    )

    assert payload["status"] == diagnostic.STATUS_COMPLETED
    assert payload["train_step_count"] == 0
    assert payload["optimizer_used"] is False
    assert payload["optimizer_constructed"] is False
    assert payload["generated_sample_metric_only"] is True
    assert payload["fit_quality_claimed"] is False
    assert payload["default_behavior_changed"] is False
    assert payload["bridge_training_cloud_policy"]["bookkeeping_only"] is True
    assert payload["seed_manifest"]["pairwise_disjoint_roles"] is True
    assert payload["gate_summary"]["overall_status"] == "pass"
    assert set(payload["metric_batches"]) == {"holdout", "replay"}
    assert payload["metric_batches"]["holdout"]["role"] == "heldout_metric"
    assert payload["metric_batches"]["replay"]["role"] == "audit_metric"
    assert "not fit-quality evidence" in payload["nonclaims"]
    assert Path(payload["output"]).name == "phase10.json"
