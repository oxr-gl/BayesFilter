from __future__ import annotations

import json
from pathlib import Path

import pytest
import tensorflow as tf

import bayesfilter
import bayesfilter.highdim as highdim


DTYPE = tf.float64
MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m1-stable-score-api-manifest-2026-06-09.json"
)
RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m1-stable-score-api-result-2026-06-09.md"
)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _quadratic_value(theta: tf.Tensor) -> tf.Tensor:
    center = tf.constant([0.25, -0.75], dtype=DTYPE)
    residual = tf.convert_to_tensor(theta, dtype=DTYPE) - center
    return -0.5 * tf.reduce_sum(tf.square(residual))


def test_p51_m1_manifest_preserves_original_gap_split() -> None:
    manifest = _manifest()
    original = manifest["original_p50_gap"]
    split = manifest["gap_resolution"]["split"]

    assert manifest["schema_version"] == "p51.stable_score_api.v1"
    assert manifest["status"] == "PASS_P51_M1_STABLE_SCORE_API"
    assert original["id"] == "stable_top_level_score_api"
    assert original["classification"] == "partially_closed"
    assert split["subpackage_contract_lane"]["status"] == "passed_stable_highdim_contract"
    assert split["subpackage_contract_lane"]["api_scope"] == "bayesfilter.highdim"
    assert split["root_public_export_lane"]["status"] == "BLOCKED_PUBLIC_API_DECISION"
    assert split["root_public_export_lane"]["requires_separate_policy_approval"] is True
    assert split["root_public_export_lane"]["api_scope"] == "root-level bayesfilter public API"


def test_p51_m1_stable_highdim_score_api_exports_are_subpackage_only() -> None:
    stable_symbols = {"HighDimScoreAPIResult", "evaluate_highdim_score_api"}
    legacy_experimental_symbols = {
        "ExperimentalScoreAPIResult",
        "evaluate_experimental_score_api",
    }

    assert stable_symbols.issubset(set(highdim.__all__))
    assert all(hasattr(highdim, name) for name in stable_symbols)
    assert stable_symbols.isdisjoint(set(bayesfilter.__all__))
    assert all(not hasattr(bayesfilter, name) for name in stable_symbols)
    assert legacy_experimental_symbols.isdisjoint(set(bayesfilter.__all__))
    assert all(not hasattr(bayesfilter, name) for name in legacy_experimental_symbols)


def test_p51_m1_evaluate_highdim_score_api_returns_scalar_value_and_score() -> None:
    theta = tf.constant([1.0, -2.0], dtype=DTYPE)
    result = highdim.evaluate_highdim_score_api(
        target_id="p51_m1_quadratic_contract_fixture",
        evidence_class="lower_rung",
        route_label="hmc_compatible_deterministic_filtering",
        parameterization="theta=(theta_0, theta_1)",
        theta=theta,
        value_fn=_quadratic_value,
        diagnostics={"fixture": "deterministic_quadratic"},
    )

    expected_score = -(theta - tf.constant([0.25, -0.75], dtype=DTYPE))

    assert result.status is highdim.HighDimStatus.OK
    assert isinstance(result, highdim.HighDimScoreAPIResult)
    assert result.log_likelihood.shape.rank == 0
    assert result.score.shape == theta.shape
    assert result.theta.dtype == DTYPE
    assert result.score.dtype == DTYPE
    assert result.branch_identity.hash.value
    tf.debugging.assert_near(result.score, expected_score)
    assert result.diagnostics["api_scope"] == "bayesfilter.highdim"
    assert result.diagnostics["stable_subpackage_api"] is True
    assert result.diagnostics["stable_top_level_api"] is False
    assert result.diagnostics["hmc_readiness"] == "not_claimed"


def test_p51_m1_score_api_rejects_bad_shapes_routes_and_disconnected_values() -> None:
    with pytest.raises(ValueError, match="INVALID_SHAPE"):
        highdim.evaluate_highdim_score_api(
            target_id="bad_shape",
            evidence_class="lower_rung",
            route_label="hmc_compatible_deterministic_filtering",
            parameterization="theta matrix",
            theta=tf.zeros([1, 2], dtype=DTYPE),
            value_fn=lambda current_theta: tf.reduce_sum(current_theta),
        )

    with pytest.raises(ValueError, match="invalid stable score route label"):
        highdim.evaluate_highdim_score_api(
            target_id="bad_route",
            evidence_class="lower_rung",
            route_label="adaptive source-faithful filtering",
            parameterization="theta",
            theta=tf.zeros([2], dtype=DTYPE),
            value_fn=_quadratic_value,
        )

    with pytest.raises(ValueError, match="score gradient is None"):
        highdim.evaluate_highdim_score_api(
            target_id="disconnected",
            evidence_class="lower_rung",
            route_label="hmc_compatible_deterministic_filtering",
            parameterization="theta",
            theta=tf.zeros([2], dtype=DTYPE),
            value_fn=lambda _current_theta: tf.constant(1.0, dtype=DTYPE),
        )


def test_p51_m1_result_emits_token_once_and_nonclaims_are_visible() -> None:
    text = RESULT_PATH.read_text(encoding="utf-8")

    assert text.count("status: PASS_P51_M1_STABLE_SCORE_API") == 1
    assert "Root-level `bayesfilter` public score API remains blocked" in text
    assert "No HMC readiness" in text
    assert "No production HMC readiness" in text
    assert "No production model readiness" in text
