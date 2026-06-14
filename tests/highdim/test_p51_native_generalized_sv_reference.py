from __future__ import annotations

import json
from pathlib import Path

import tensorflow as tf

import bayesfilter
import bayesfilter.highdim as highdim


DTYPE = tf.float64
MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-manifest-2026-06-09.json"
)
RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-result-2026-06-09.md"
)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _fixture() -> tuple[highdim.NativeGeneralizedSVSSM, tf.Tensor, tf.Tensor]:
    model = highdim.NativeGeneralizedSVSSM()
    theta = model.unconstrained_from_physical(
        rho_s=tf.constant(0.25, dtype=DTYPE),
        rho_h=tf.constant(0.55, dtype=DTYPE),
        sigma_s=tf.constant(0.70, dtype=DTYPE),
        sigma_h=tf.constant(0.45, dtype=DTYPE),
        beta=tf.constant(0.35, dtype=DTYPE),
    )
    observations = tf.constant([[0.18], [-0.08]], dtype=DTYPE)
    return model, theta, observations


def _value_and_score(order: int) -> tuple[tf.Tensor, tf.Tensor, object]:
    model, theta, observations = _fixture()
    result = highdim.evaluate_highdim_score_api(
        target_id="native_generalized_sv_raw_observation_dense_reference",
        evidence_class="lower_rung",
        route_label="hmc_compatible_deterministic_filtering",
        parameterization=model.parameterization,
        theta=theta,
        value_fn=lambda current_theta: highdim.native_generalized_sv_dense_reference(
            model,
            current_theta,
            observations,
            order=order,
            radius_s=3.5,
            radius_h=3.5,
        ).log_likelihood,
        diagnostics={
            "reference_route": "dense_native_generalized_sv_raw_observation",
            "grid_order": order,
        },
    )
    return result.log_likelihood, result.score, result


def test_p51_m2_manifest_reclassifies_native_generalized_sv_reference_gap() -> None:
    manifest = _manifest()
    row = manifest["native_generalized_sv_same_target_reference"]

    assert manifest["schema_version"] == "p51.native_generalized_sv_reference.v1"
    assert manifest["status"] == "PASS_P51_M2_NATIVE_GENERALIZED_SV_REFERENCE"
    assert row["source_gap"] == "native_generalized_sv_same_target_reference"
    assert row["p50_status"] == "BLOCKED_REFERENCE_MISSING"
    assert row["p51_status"] == "passed_low_dimensional_native_dense_reference"
    assert row["target_identity"] == "y_t = beta s_t + exp(h_t/2) epsilon_t"
    assert row["state"] == "(s_t, h_t)"
    assert row["candidate_algorithm_status"]["cut4"] == "not_evaluated_for_native_same_target"
    assert row["candidate_algorithm_status"]["zhao_cui"] == "not_evaluated_for_native_same_target"


def test_p51_m2_native_generalized_sv_exports_are_subpackage_only() -> None:
    symbols = {
        "NativeGeneralizedSVDenseReferenceResult",
        "NativeGeneralizedSVSSM",
        "native_generalized_sv_dense_reference",
    }

    assert symbols.issubset(set(highdim.__all__))
    assert all(hasattr(highdim, name) for name in symbols)
    assert symbols.isdisjoint(set(bayesfilter.__all__))
    assert all(not hasattr(bayesfilter, name) for name in symbols)


def test_p51_m2_native_dense_reference_has_raw_observation_identity_and_moments() -> None:
    model, theta, observations = _fixture()
    result = highdim.native_generalized_sv_dense_reference(
        model,
        theta,
        observations,
        order=21,
        radius_s=3.5,
        radius_h=3.5,
    )

    assert isinstance(result, highdim.NativeGeneralizedSVDenseReferenceResult)
    assert result.log_likelihood.shape.rank == 0
    assert result.log_normalizers.shape == (2,)
    assert result.mean_path.shape == (2, 2)
    assert result.covariance_path.shape == (2, 2, 2)
    assert result.diagnostics["target"] == "native raw-y generalized SV"
    assert result.diagnostics["backend"] == "dense_native_generalized_sv_raw_observation"
    assert "not transformed-residual diagnostic" in result.diagnostics["non_claims"]
    assert "no CUT4 same-target equality" in result.diagnostics["non_claims"]
    assert "no Zhao-Cui same-target equality" in result.diagnostics["non_claims"]
    tf.debugging.assert_equal(
        model.observation_log_density(theta, tf.constant([[0.4, -0.2]], dtype=DTYPE), observations[0], t=0),
        model.observation_log_density(theta, tf.constant([[0.4, -0.2]], dtype=DTYPE), observations[0], t=7),
    )


def test_p51_m2_native_dense_reference_value_and_gradient_refine() -> None:
    coarse_value, coarse_score, coarse_result = _value_and_score(order=19)
    fine_value, fine_score, fine_result = _value_and_score(order=25)
    score_gap = tf.linalg.norm(coarse_score - fine_score)
    relative_score_gap = score_gap / tf.maximum(tf.constant(1.0, dtype=DTYPE), tf.linalg.norm(fine_score))

    tf.debugging.assert_near(coarse_value, fine_value, atol=2e-3, rtol=2e-3)
    tf.debugging.assert_near(coarse_score, fine_score, atol=8e-3, rtol=8e-3)
    tf.debugging.assert_less(relative_score_gap, tf.constant(8e-3, dtype=DTYPE))
    assert coarse_result.diagnostics["stable_subpackage_api"] is True
    assert fine_result.diagnostics["hmc_readiness"] == "not_claimed"


def test_p51_m2_result_emits_token_once_and_nonclaims_are_visible() -> None:
    text = RESULT_PATH.read_text(encoding="utf-8")

    assert text.count("status: PASS_P51_M2_NATIVE_GENERALIZED_SV_REFERENCE") == 1
    assert "No CUT4 same-target equality" in text
    assert "No Zhao-Cui same-target equality" in text
    assert "No HMC readiness" in text
    assert "No production generalized SV readiness" in text
