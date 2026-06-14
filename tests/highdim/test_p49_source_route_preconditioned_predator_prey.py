from __future__ import annotations

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64


def test_p49_preconditioner_contract_records_source_route_components() -> None:
    contract = highdim.SourceRoutePreconditionerContract(
        variant="preconditioner",
        coefficient=tf.constant(0.8, dtype=DTYPE),
        reference_density_label="predator_prey_local_gaussian_reference",
        forward_map_label="Tu2x",
        inverse_map_label="Tx2u",
    )

    payload = contract.manifest_payload()
    assert payload["variant"] == "preconditioner"
    assert payload["route_label"] == highdim.SOURCE_FAITHFUL_ROUTE_LABEL
    assert payload["forward_map_label"] == "Tu2x"
    assert payload["inverse_map_label"] == "Tx2u"


def test_p49_preconditioned_residual_target_identity_is_exact_on_fixture() -> None:
    points = tf.constant(
        [
            [48.0, 4.0],
            [52.0, 5.0],
            [60.0, 7.0],
            [70.0, 3.5],
        ],
        dtype=DTYPE,
    )
    center = tf.constant([55.0, 5.0], dtype=DTYPE)
    full_negative_log = (
        0.01 * tf.square(points[:, 0] - center[0])
        + 0.08 * tf.square(points[:, 1] - center[1])
        + 0.0002 * tf.square((points[:, 0] - center[0]) * (points[:, 1] - center[1]))
    )
    preconditioner_negative_log = (
        0.01 * tf.square(points[:, 0] - center[0])
        + 0.08 * tf.square(points[:, 1] - center[1])
    )

    residual = highdim.source_route_residual_negative_log_target(
        full_negative_log_target=full_negative_log,
        preconditioner_negative_log_target=preconditioner_negative_log,
    )
    error = highdim.source_route_preconditioned_target_identity_error(
        full_negative_log_target=full_negative_log,
        preconditioner_negative_log_target=preconditioner_negative_log,
        residual_negative_log_target=residual,
    )

    tf.debugging.assert_near(error, tf.constant(0.0, dtype=DTYPE))
    tf.debugging.assert_near(
        preconditioner_negative_log + residual,
        full_negative_log,
    )


def test_p49_predator_prey_ladder_separates_fixed_design_blocker_from_source_route() -> None:
    fixed_row = highdim.SourceRoutePredatorPreyLadderRow(
        row_id="p47-m5b-fixed-design-blocker",
        route_label=highdim.GRADIENT_ADAPTATION_ROUTE_LABEL,
        horizon=25,
        baseline="P47 M5b fixed-design result",
        primary_check="deterministic replay passes but production accuracy tolerances fail",
        decision_status="BLOCKED_FIXED_DESIGN_ACCURACY_TUNING",
        non_claims=(
            "fixed-design failure is not source-route failure",
            "no nonlinear preconditioning usefulness claim",
        ),
    )
    source_identity_row = highdim.SourceRoutePredatorPreyLadderRow(
        row_id="p49-m5-source-preconditioner-identity",
        route_label=highdim.SOURCE_FAITHFUL_ROUTE_LABEL,
        horizon=2,
        baseline="exact full = preconditioner + residual target identity",
        primary_check="target-decomposition identity error is zero on fixture",
        decision_status="PASS_TARGET_IDENTITY_ONLY",
        non_claims=(
            "no predator-prey production token",
            "no adaptive TT/SIRT fit claim",
        ),
    )
    manifest = highdim.SourceRoutePredatorPreyLadderManifest(
        rows=(fixed_row, source_identity_row),
        fixed_design_failure_interpretation="P47 M5b is a fixed-design tuning blocker, not evidence against source Zhao-Cui preconditioning.",
        source_route_claim_status="target identity only; full preconditioned route remains unimplemented",
        production_token_emitted=False,
    )

    payload = manifest.manifest_payload()
    assert payload["production_token_emitted"] is False
    assert payload["rows"][0]["route_label"] == highdim.GRADIENT_ADAPTATION_ROUTE_LABEL
    assert payload["rows"][1]["route_label"] == highdim.SOURCE_FAITHFUL_ROUTE_LABEL
    assert "fixed-design tuning blocker" in payload["fixed_design_failure_interpretation"]


def test_p49_predator_prey_manifest_rejects_unearned_production_token() -> None:
    blocked_source_row = highdim.SourceRoutePredatorPreyLadderRow(
        row_id="p49-m5-source-preconditioner-blocked",
        route_label=highdim.SOURCE_FAITHFUL_ROUTE_LABEL,
        horizon=25,
        baseline="short-horizon source preconditioner ladder",
        primary_check="full route not implemented",
        decision_status="BLOCKED_SOURCE_ROUTE_NOT_IMPLEMENTED",
        non_claims=("no predator-prey production token",),
    )

    with pytest.raises(ValueError, match="PASS_SOURCE_PRECONDITIONED_FILTERING"):
        highdim.SourceRoutePredatorPreyLadderManifest(
            rows=(blocked_source_row,),
            fixed_design_failure_interpretation="P47 fixed branch is not source route evidence.",
            source_route_claim_status="blocked",
            production_token_emitted=True,
        )


def test_p49_predator_prey_manifest_rejects_identity_only_production_token() -> None:
    identity_only_row = highdim.SourceRoutePredatorPreyLadderRow(
        row_id="p49-m5-source-preconditioner-identity",
        route_label=highdim.SOURCE_FAITHFUL_ROUTE_LABEL,
        horizon=2,
        baseline="exact target identity",
        primary_check="full equals preconditioner plus residual",
        decision_status="PASS_TARGET_IDENTITY_ONLY",
        non_claims=("no predator-prey production token",),
    )

    with pytest.raises(ValueError, match="PASS_SOURCE_PRECONDITIONED_FILTERING"):
        highdim.SourceRoutePredatorPreyLadderManifest(
            rows=(identity_only_row,),
            fixed_design_failure_interpretation="P47 fixed branch is not source route evidence.",
            source_route_claim_status="identity only",
            production_token_emitted=True,
        )


def test_p49_preconditioner_helpers_reject_bad_shapes_and_metadata() -> None:
    with pytest.raises(ValueError, match="variant"):
        highdim.SourceRoutePreconditionerContract(
            variant="ad_hoc",
            coefficient=tf.constant(1.0, dtype=DTYPE),
            reference_density_label="ref",
            forward_map_label="f",
            inverse_map_label="g",
        )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.INVALID_SHAPE.value):
        highdim.source_route_residual_negative_log_target(
            full_negative_log_target=tf.zeros([2], dtype=DTYPE),
            preconditioner_negative_log_target=tf.zeros([3], dtype=DTYPE),
        )
