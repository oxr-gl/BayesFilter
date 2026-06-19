from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import tensorflow as tf

import scripts.p76_bounded_ukf_minibatch_pilot as pilot
from bayesfilter.highdim import source_route
from bayesfilter.highdim import ukf_initializer as p76
from bayesfilter.highdim.ukf_scout import P52_UKF_SCOUT_CLAIM, UKFScoutResult


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


def test_rank_tuple_matches_tt_boundary_ranks() -> None:
    assert pilot._rank_tuple(4, 3) == (1, 3, 3, 3, 1)


def test_bridge_blocker_payload_is_fail_closed() -> None:
    product_basis = pilot._product_basis(dimension=4, degree=2)
    config = p76.P76UKFInitializerConfig(
        product_basis=product_basis,
        ranks=pilot._rank_tuple(4, 2),
        quadrature_order=16,
    )
    initializer = p76.p76_build_ukf_initializer(_scout(), config)
    frame = source_route.SourceRouteCoordinateFrame(
        mu=initializer.center,
        matrix=initializer.linear_map,
        expansion_factor=config.gamma,
    )

    bridge = pilot._ukf_frame_bridge_from_blocker(
        frame=frame,
        product_basis=product_basis,
        initializer=initializer,
        bridge_blocker="fresh_batch_or_audit_data_error:test",
    )

    assert bridge["status"] == "block"
    assert bridge["dimension_match"] is True
    assert bridge["training_clip_fraction_max"] == 1.0
    assert bridge["audit_clip_fraction_max"] == 1.0
    assert "fresh_batch_or_audit_data_error:test" in bridge["blockers"]
    assert bridge["target_tieout_source"] == "not_evaluated_bridge_blocker"


def test_bridge_tieout_source_records_actual_batch_target_path() -> None:
    assert (
        "actual_batch_target_values_vs_independent_direct_physical_density"
        in Path(
            __file__
        ).resolve().parents[2].joinpath(
            "scripts/p76_bounded_ukf_minibatch_pilot.py"
        ).read_text()
    )


def test_training_blocked_payload_records_fail_closed_status_and_blocker() -> None:
    product_basis = pilot._product_basis(dimension=4, degree=2)
    config = p76.P76UKFInitializerConfig(
        product_basis=product_basis,
        ranks=pilot._rank_tuple(4, 2),
        quadrature_order=16,
    )
    initializer = p76.p76_build_ukf_initializer(_scout(), config)
    frame = source_route.SourceRouteCoordinateFrame(
        mu=initializer.center,
        matrix=initializer.linear_map,
        expansion_factor=config.gamma,
    )
    frame_hash = source_route._p69_frame_hash(frame)
    context = {
        "training_seed_policy": {"fresh_training_batches": True},
        "ukf_frame_manifest": {"frame_hash": frame_hash},
        "initializer": initializer,
        "ukf_frame_bridge": {
            "status": "pass",
            "frame_hash": frame_hash,
            "blockers": (),
        },
        "training_clip_fraction_max": 0.0,
        "audit_clip_fraction_max": 0.0,
    }
    base = {
        "schema_version": pilot.SCHEMA_VERSION,
        "run_manifest": {"elapsed_seconds": 0.0},
    }

    payload = pilot._training_blocked_payload(
        base=base,
        context=context,
        completed_batches=1,
        requested_batches=3,
        stop_reason="nonfinite_training_quantity_veto",
        blocker="nonfinite_training_quantity",
        trace=({"step": 1, "veto": "nonfinite_training_quantity"},),
    )

    assert payload["status"] == pilot.STATUS_TRAINING_BLOCKED
    assert payload["gate_summary"]["overall_status"] == "block"
    assert payload["gate_summary"]["blockers"] == ("nonfinite_training_quantity",)
    assert payload["gate_summary"]["stop_reason"] == "nonfinite_training_quantity_veto"
    assert payload["completed_batches"] == 1
    assert payload["wall_time_seconds"] == payload["run_manifest"]["elapsed_seconds"]


def test_terms_have_nonfinite_veto_detects_nonfinite_loss() -> None:
    terms = SimpleNamespace(
        total_loss=tf.constant(float("nan"), dtype=tf.float64),
        weighted_empirical_cross_entropy=tf.constant(0.0, dtype=tf.float64),
        log_normalizer=tf.constant(0.0, dtype=tf.float64),
        regularization=tf.constant(0.0, dtype=tf.float64),
        normalizer=tf.constant(1.0, dtype=tf.float64),
        alpha_min=tf.constant(0.0, dtype=tf.float64),
        alpha_max=tf.constant(1.0, dtype=tf.float64),
        alpha_sum=tf.constant(1.0, dtype=tf.float64),
        rho_min=tf.constant(1.0, dtype=tf.float64),
        rho_max=tf.constant(2.0, dtype=tf.float64),
        gradient_norm=tf.constant(1.0, dtype=tf.float64),
    )
    trainer = SimpleNamespace()
    batch = SimpleNamespace(points=tf.zeros([1, 1], dtype=tf.float64))

    assert pilot._terms_have_nonfinite_veto(terms, trainer, batch) is True


def test_final_wall_time_rewrites_manifest_elapsed_seconds() -> None:
    payload = {
        "run_manifest": {"elapsed_seconds": 0.0, "command": "unit-test"},
        "status": "unit",
    }

    updated = pilot._with_final_wall_time(payload)

    assert updated["run_manifest"]["command"] == "unit-test"
    assert updated["run_manifest"]["elapsed_seconds"] > 0.0
    assert updated["wall_time_seconds"] == updated["run_manifest"]["elapsed_seconds"]


def test_pilot_script_does_not_expose_failed_p75_init_ladder_names() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "scripts/p76_bounded_ukf_minibatch_pilot.py"
    ).read_text()
    forbidden = (
        "_".join(["calibrated", "constant"]),
        "_".join(["source", "guided", "prefit"]),
        '"random"',
        "P75_INIT_MODES",
        "compare_init_modes",
    )
    for text in forbidden:
        assert text not in source
