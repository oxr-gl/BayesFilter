from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim
from bayesfilter.highdim import stochastic_density_training as p77_metric
import scripts.p77_budgeted_corrected_metric_training as p77


def _config() -> p77_metric.P75TrainableTTConfig:
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
    return p77_metric.P75TrainableTTConfig(
        product_basis=basis,
        ranks=(1, 2, 1),
        tau=tf.constant(2.5, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-14, dtype=tf.float64),
        denominator_floor=tf.constant(1e-300, dtype=tf.float64),
        l2_weight=tf.constant(0.0, dtype=tf.float64),
        learning_rate=1e-3,
        gradient_clip_norm=10.0,
        seed=7703,
    )


def _cores() -> tuple[tf.Tensor, tf.Tensor]:
    return (
        tf.constant([[[0.4, -0.1], [0.2, 0.3]]], dtype=tf.float64),
        tf.constant([[[0.5], [0.1]], [[-0.2], [0.4]]], dtype=tf.float64),
    )


def _data(offset: float = 0.0) -> SimpleNamespace:
    return SimpleNamespace(
        local_fit_points=tf.constant(
            [
                [-0.75, -0.25, 0.25, 0.75],
                [-0.25, 0.50, -0.50, 0.25],
            ],
            dtype=tf.float64,
        ),
        target_values=tf.constant([0.25 + offset, 0.5, 1.0, 2.0], dtype=tf.float64),
        fit_weights=tf.constant([1.0, 2.0, 1.5, 0.5], dtype=tf.float64),
        manifest={
            "coordinate_frame_hash": f"unit-frame-{offset}",
            "local_clip_fraction": tf.constant(0.0, dtype=tf.float64),
        },
    )


class _Initializer:
    cores = _cores()
    manifest = {"unit_initializer": True}


def _context(
    *,
    degree: int,
    rank: int,
    batch_size: int,
    batches: int,
    seed: int,
    learning_rate: float,
):
    del degree, rank, batch_size, seed, learning_rate
    bridge = {
        "status": "pass",
        "frame_hash": "unit-frame",
        "blockers": (),
    }
    return {
        "target_dim": 2,
        "train_data_sequence": tuple(_data(0.1 + step * 0.01) for step in range(batches)),
        "audit_data_sequence": (_data(0.0), _data(0.2)),
        "trainer_config": _config(),
        "initializer": _Initializer(),
        "ukf_frame_bridge": bridge,
        "ukf_frame_manifest": {"frame_hash": "unit-frame", "target_dimension": 2},
        "training_seed_policy": {"fresh_training_batches": True},
        "training_clip_fraction_max": 0.0,
        "audit_clip_fraction_max": 0.0,
    }


def test_parameter_manifest_counts_current_degree2_rank4_d36_candidate() -> None:
    manifest = p77._parameter_manifest(dimension=36, degree=2, rank=4)

    assert manifest["P_theta"] == 1656
    assert manifest["parameter_count"] == 1656
    assert manifest["rank_tuple"][0] == 1
    assert manifest["rank_tuple"][-1] == 1
    assert len(manifest["term_counts"]) == 36
    assert manifest["recompute_if_rank_degree_dimension_basis_or_trainable_mask_changes"] is True


def test_budget_manifest_enforces_20x_gate_and_labels_smoke() -> None:
    params = p77._parameter_manifest(dimension=36, degree=2, rank=4)

    proper = p77._budget_manifest(
        parameter_manifest=params,
        batch_size=1024,
        batches=40,
        evidence_run=True,
    )
    smoke = p77._budget_manifest(
        parameter_manifest=params,
        batch_size=128,
        batches=1,
        evidence_run=False,
    )

    assert proper["minimum_training_samples"] == 33120
    assert proper["N_train"] == 40960
    assert proper["hard_budget_gate_passed"] is True
    assert proper["minimum_batches_for_batch_size"] == 33
    assert smoke["hard_budget_gate_passed"] is False
    assert smoke["non_evidence_mechanics_smoke"] is True


def test_under_budget_evidence_request_blocks_before_context(monkeypatch, tmp_path) -> None:
    def fail_context(**_kwargs):
        raise AssertionError("context must not be constructed for under-budget evidence")

    monkeypatch.setattr(p77, "_target_context", fail_context)

    payload = p77.budgeted_corrected_metric_training_payload(
        output=tmp_path / "blocked.json",
        degree=2,
        rank=4,
        batch_size=128,
        batches=1,
        learning_rate=1e-3,
        max_seconds=10.0,
        seed=7703,
        evidence_run=True,
    )

    assert payload["status"] == p77.STATUS_BUDGET_BLOCKED
    assert payload["training_started"] is False
    assert payload["optimizer_constructed"] is False
    assert payload["budget_manifest"]["hard_budget_gate_passed"] is False
    assert payload["gate_summary"]["blockers"] == ("under_budget_evidence_request",)


def test_payload_with_stubbed_context_records_budget_and_corrected_metrics(
    monkeypatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        p77,
        "_target_context",
        lambda **kwargs: _context(**kwargs),
    )

    payload = p77.budgeted_corrected_metric_training_payload(
        output=tmp_path / "smoke.json",
        degree=2,
        rank=4,
        batch_size=4,
        batches=2,
        learning_rate=1e-3,
        max_seconds=10.0,
        seed=7703,
        evidence_run=False,
    )

    assert payload["status"] == p77.STATUS_COMPLETED
    assert payload["evidence_run"] is False
    assert payload["budget_manifest"]["non_evidence_mechanics_smoke"] is True
    assert payload["parameter_manifest"]["P_theta"] == 1656
    assert payload["completed_batches"] == 2
    assert payload["optimizer_constructed"] is True
    assert payload["audit_used_for_selection"] is False
    assert payload["audit_evaluated"] is False
    assert payload["failed_route_fence"]["failed_historical_routes_only"] is True
    assert set(payload["metric_batches"]) == {
        "validation_baseline",
        "validation_trained",
        "replay_baseline",
        "replay_trained",
    }
    assert payload["metric_batches"]["validation_baseline"]["corrected_validation_CE_primary"] is True
    assert payload["metric_batches"]["replay_baseline"]["corrected_validation_CE_primary"] is False
    assert "untrained_ukf_baseline_corrected_validation_CE" in payload["validation_summary"]
    assert payload["gate_summary"]["evidence_run"] is False
    assert (
        payload["validation_summary"]["validation_improvement_observed_explanatory_only"]
        in {True, False}
    )
    assert payload["validation_summary"]["fit_quality_claim_permitted"] is False
    assert payload["validation_summary"]["validation_improved_for_selection"] is None
    assert payload["validation_summary"]["non_evidence_smoke_no_fit_quality_claim"] is True
    assert payload["gate_summary"]["fit_quality_claim_permitted"] is False


def test_learning_rate_candidates_are_predeclared() -> None:
    assert p77.P77_LEARNING_RATES == (1e-4, 3e-4, 1e-3)
    with pytest.raises(ValueError, match="learning_rate"):
        p77.budgeted_corrected_metric_training_payload(
            output=Path("unused.json"),
            degree=2,
            rank=4,
            batch_size=128,
            batches=1,
            learning_rate=2e-3,
            max_seconds=10.0,
            seed=7703,
            evidence_run=False,
        )


def test_evidence_run_vetoes_validation_non_improvement(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(
        p77,
        "_target_context",
        lambda **kwargs: _context(**kwargs),
    )

    def fake_metric_payload(*, trainer, data, label, role):
        del trainer, data
        ce_by_label = {
            "p77_validation_baseline": 1.0,
            "p77_validation_trained": 2.0,
            "p77_replay_baseline": 1.0,
            "p77_replay_trained": 1.0,
        }
        return {
            "label": label,
            "role": role,
            "heldout_cross_entropy": ce_by_label[label],
            "all_primary_values_finite": True,
            "heldout_cross_entropy_reconstruction_abs_error": 0.0,
            "corrected_alpha_sum": 1.0,
            "corrected_validation_CE_primary": role == "heldout_metric",
            "explanatory_only": role != "heldout_metric",
        }

    monkeypatch.setattr(p77, "_metric_payload", fake_metric_payload)

    payload = p77.budgeted_corrected_metric_training_payload(
        output=tmp_path / "evidence.json",
        degree=2,
        rank=4,
        batch_size=33120,
        batches=1,
        learning_rate=1e-3,
        max_seconds=10.0,
        seed=7703,
        evidence_run=True,
    )

    assert payload["budget_manifest"]["hard_budget_gate_passed"] is True
    assert payload["validation_summary"]["fit_quality_claim_permitted"] is True
    assert payload["validation_summary"]["validation_improved_for_selection"] is False
    assert payload["gate_summary"]["overall_status"] == "block"
    assert "validation_not_improved_against_untrained_ukf_baseline" in payload[
        "gate_summary"
    ]["blockers"]


def test_runner_source_does_not_expose_failed_live_routes() -> None:
    source = Path("scripts/p77_budgeted_corrected_metric_training.py").read_text()
    forbidden = (
        "P75" + "_" + "INIT" + "_" + "MODES",
        "_".join(("compare", "init", "modes")),
        "_".join(("source", "guided", "prefit")),
        "-".join(("source", "guided", "prefit")),
        '"' + "ran" + "dom" + '"',
    )
    for text in forbidden:
        assert text not in source


def test_runtime_parameter_count_matches_trainable_variables() -> None:
    trainer = p77_metric.TrainableFunctionalTT(_config(), initial_cores=_cores())

    assert p77._runtime_parameter_count(trainer) == 8
