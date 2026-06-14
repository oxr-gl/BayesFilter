from __future__ import annotations

import json
from pathlib import Path

import pytest
import tensorflow as tf

from bayesfilter import highdim


MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p52-m3-ukf-scouting-manifest-2026-06-10.json"
)
SUBPLAN_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p52-m3-ukf-scouting-subplan-2026-06-10.md"
)
P30_PATH = Path(
    "docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex"
)


def test_p52_ukf_scout_rejects_truth_or_hmc_claims() -> None:
    with pytest.raises(ValueError, match="stronger claims"):
        highdim.UKFScoutConfig(claim_class="correctness oracle")


def test_p52_ukf_scout_shapes_and_sigma_point_count_for_d18() -> None:
    model = highdim.p30_spatial_sir_fixture_model(9)
    result = highdim.spatial_sir_ukf_scout(
        model,
        config=highdim.UKFScoutConfig(horizon=1),
    )

    assert result.status == "PASS_P52_UKF_SCOUT"
    assert result.claim_class == highdim.P52_UKF_SCOUT_CLAIM
    assert result.dimension == 18
    assert result.compartments == 9
    assert result.sigma_point_count == 2 * 18 + 1
    assert result.mean_path.shape == (2, 18)
    assert result.covariance_path.shape == (2, 18, 18)
    assert result.scale_path.shape == (2, 18)
    assert result.covariance_eigenvalues.shape == (2, 18)
    assert result.effective_dimension_path.shape == (2,)
    assert bool(tf.reduce_all(tf.math.is_finite(result.mean_path)).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(result.covariance_path)).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(result.scale_path)).numpy())
    assert "scout_not_truth" in result.nonclaims
    assert "no filtering correctness" in result.nonclaims
    assert "no HMC readiness" in result.nonclaims


def test_p52_ukf_scout_uses_observation_path_when_supplied() -> None:
    model = highdim.p30_spatial_sir_fixture_model(1)
    config = highdim.UKFScoutConfig(horizon=1)
    nominal = highdim.spatial_sir_ukf_scout(model, config=config)
    shifted = highdim.spatial_sir_ukf_scout(
        model,
        config=config,
        observations=tf.constant([[99.0], [77.0]], dtype=tf.float64),
    )

    assert shifted.mean_path.shape == nominal.mean_path.shape
    assert not bool(tf.reduce_all(tf.equal(shifted.mean_path, nominal.mean_path)).numpy())


def test_p52_ukf_scout_manifest_for_dimensions_and_nonclaims() -> None:
    manifest = highdim.p52_spatial_sir_ukf_scout_manifest(horizon=1)
    rows = {int(row["dimension"]): row for row in manifest["rows"]}
    subplan = SUBPLAN_PATH.read_text(encoding="utf-8")
    p30 = P30_PATH.read_text(encoding="utf-8")

    assert manifest["schema_version"] == "p52.ukf_scout.v1"
    assert manifest["status"] == "PASS_P52_M3_UKF_SCOUTING"
    assert manifest["claim_class"] == "scout_not_truth"
    assert set(rows) == {18, 50, 100}
    assert rows[18]["sigma_point_count"] == 37
    assert rows[50]["sigma_point_count"] == 101
    assert rows[100]["sigma_point_count"] == 201
    assert rows[100]["claim_class"] == "scout_not_truth"
    assert rows[100]["final_center_dimension"] == 100
    assert rows[100]["final_scale_dimension"] == 100
    assert rows[100]["final_covariance_spectrum_dimension"] == 100
    assert len(rows[100]["final_center_head"]) == 4
    assert len(rows[100]["final_center_tail"]) == 4
    assert rows[100]["final_scale_range"][0] > 0.0
    assert rows[100]["final_covariance_eigenvalue_range"][0] > 0.0
    assert list(rows[18]["covariance_choices"]["process_covariance_shape"]) == [18, 18]
    assert list(rows[18]["covariance_choices"]["observation_covariance_shape"]) == [9, 9]
    assert rows[18]["lower_rung_sanity_comparator"]["status"] == (
        "recorded_sanity_only_not_promotion"
    )
    assert rows[18]["lower_rung_sanity_comparator"]["source_dimension"] == 2
    assert "not a d=18 dense reference" in rows[18]["lower_rung_sanity_comparator"]["nonclaims"]
    assert all(row["finite"] is True for row in rows.values())
    assert "no exact likelihood" in manifest["nonclaims"]
    assert "no d=100 filtering correctness" in manifest["nonclaims"]
    assert "UKF scout produces finite means/covariances" in subplan
    assert "not a correctness oracle" in p30


def test_p52_m3_persisted_manifest_matches_protocol_summary() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    expected = highdim.p52_spatial_sir_ukf_scout_manifest(horizon=1)

    assert manifest["schema_version"] == expected["schema_version"]
    assert manifest["status"] == "PASS_P52_M3_UKF_SCOUTING"
    assert manifest["claim_class"] == "scout_not_truth"
    assert manifest["dimensions"] == [18, 50, 100]
    expected_rows = {
        int(row["dimension"]): row
        for row in expected["rows"]
    }
    for row in manifest["rows"]:
        expected_row = expected_rows[int(row["dimension"])]
        assert row["sigma_point_count"] == expected_row["sigma_point_count"]
        assert row["status"] == "PASS_P52_UKF_SCOUT"
        assert row["claim_class"] == "scout_not_truth"
        assert row["finite"] is True
        assert row["final_center_dimension"] == int(row["dimension"])
        assert row["final_scale_dimension"] == int(row["dimension"])
        assert row["final_covariance_spectrum_dimension"] == int(row["dimension"])
        assert "covariance_choices" in row
        assert "lower_rung_sanity_comparator" in row
        assert row["effective_dimension_path"] == expected_row["effective_dimension_path"]
        assert "no filtering correctness" in row["nonclaims"]
    assert "no production spatial SIR readiness" in manifest["nonclaims"]
