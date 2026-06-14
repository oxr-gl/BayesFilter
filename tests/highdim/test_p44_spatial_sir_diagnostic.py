from __future__ import annotations

import tensorflow as tf

import bayesfilter.highdim as highdim
from bayesfilter.nonlinear.svd_cut_tf import tf_svd_cut4_filter
from bayesfilter.structural import StatePartition, StructuralFilterConfig
from bayesfilter.structural_tf import TFStructuralStateSpace


DTYPE = tf.float64


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _theta0() -> tf.Tensor:
    return tf.constant([0.05, -0.03, 0.04, -0.02], dtype=DTYPE)


def _observations() -> tf.Tensor:
    return tf.constant([[14.10], [11.85]], dtype=DTYPE)


def _sir_model() -> highdim.SpatialSIRSSM:
    return highdim.p30_spatial_sir_fixture_model(1)


def _structural_closure(theta: tf.Tensor) -> TFStructuralStateSpace:
    theta = tf.convert_to_tensor(theta, dtype=DTYPE)
    sir = _sir_model()
    initial_shift = tf.stack([theta[0], theta[1]])
    process_scale = tf.exp(theta[2])
    observation_scale = tf.exp(theta[3])
    process_chol = tf.linalg.cholesky(process_scale * sir.process_covariance)

    def transition_fn(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        previous = tf.convert_to_tensor(previous_state, dtype=DTYPE)
        innov = tf.convert_to_tensor(innovation, dtype=DTYPE)
        mean = sir.transition_mean(previous)
        return mean + innov @ tf.transpose(process_chol)

    def observation_fn(state_points: tf.Tensor) -> tf.Tensor:
        return sir.infectious_components(state_points)

    return TFStructuralStateSpace(
        partition=StatePartition(
            state_names=("S_1", "I_1"),
            stochastic_indices=(0, 1),
            deterministic_indices=(),
            innovation_dim=2,
        ),
        config=StructuralFilterConfig(
            integration_space="innovation",
            deterministic_completion="none",
            approximation_label="p44_m5_sir_additive_gaussian_diagnostic_closure",
        ),
        initial_mean=sir.initial_mean + initial_shift,
        initial_covariance=process_scale * sir.initial_covariance,
        innovation_covariance=tf.eye(2, dtype=DTYPE),
        observation_covariance=observation_scale * sir.observation_covariance,
        transition_fn=transition_fn,
        observation_fn=observation_fn,
        name="p44_m5_sir_cut4_diagnostic_closure",
    )


def _cut4_value(theta: tf.Tensor):
    return tf_svd_cut4_filter(
        _observations(),
        _structural_closure(theta),
        innovation_floor=tf.constant(1e-12, dtype=DTYPE),
        return_filtered=True,
    )


def _value_and_score(theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
    theta = tf.convert_to_tensor(theta, dtype=DTYPE)
    with tf.GradientTape() as tape:
        tape.watch(theta)
        result = _cut4_value(theta)
        value = result.log_likelihood
    score = tape.gradient(value, theta)
    if score is None:
        raise AssertionError("GradientTape returned None")
    return value, score


def _non_claims(*extra: str) -> tuple[str, ...]:
    return (
        "CUT4 is not nonlinear ground truth",
        "no paper-scale validation",
        "no adaptive MATLAB behavior",
        "no GPU readiness",
        "no HMC readiness",
        "no DSGE readiness",
        "no stable public API readiness",
        "no end-to-end score API readiness",
        *extra,
    )


def test_p44_m5_sir_model_contract_anchor_and_negative_domain_policy() -> None:
    sir = _sir_model()
    payload = sir.manifest_payload()

    assert sir.state_dim() == 2
    assert sir.observation_dim() == 1
    assert payload["dimension_convention"] == "state is (S_1,I_1,...,S_J,I_J) in R^{2J}; R is eliminated"
    assert payload["observation_convention"] == "infectious coordinates only"
    assert payload["domain_policy"] == "diagnose_negative_after_noise"
    assert "eq:p27-sir6" in payload["source_equations"]
    assert "production_tt_sirt_sir_filtering" in payload["what_is_not_claimed"]

    diagnostics = sir.domain_diagnostics(tf.constant([[486.0, 14.0], [-0.5, 12.0]], dtype=DTYPE))
    assert diagnostics["domain_policy"] == "diagnose_negative_after_noise"
    assert diagnostics["has_negative_state"] is True
    assert float(diagnostics["min_state"].numpy()) < 0.0


def test_p44_m5_cut4_closure_has_finite_value_and_diagnostic_score() -> None:
    value, score = _value_and_score(_theta0())

    print(
        "P44_M5_SIR_CUT4_DIAGNOSTIC "
        f"value={float(value.numpy()):.6e} "
        f"score_norm={float(tf.linalg.norm(score).numpy()):.6e}"
    )
    assert bool(tf.math.is_finite(value).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(score)).numpy())
    assert float(tf.linalg.norm(score).numpy()) > 0.0


def test_p44_m5_cut4_metadata_preserves_diagnostic_closure_boundary() -> None:
    result = _cut4_value(_theta0())

    assert result.metadata.approximation_label == "p44_m5_sir_additive_gaussian_diagnostic_closure"
    assert result.metadata.differentiability_status == "value_only"
    assert int(result.diagnostics.extra["augmented_dim"].numpy()) == 4
    assert int(result.diagnostics.extra["point_count"].numpy()) == 24
    assert int(result.diagnostics.extra["polynomial_degree"].numpy()) == 5
    assert int(result.diagnostics.extra["innovation_floor_count"].numpy()) == 0
    reason = result.diagnostics.extra["derivative_status_reason"]
    if hasattr(reason, "numpy"):
        reason = reason.numpy().decode()
    assert "derivatives are not certified" in str(reason)


def test_p44_m5_no_matched_zhaocui_equality_route_for_sir_closure() -> None:
    config = highdim.FixedBranchFilterConfig(
        fit_config=None,
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(highdim.IdentityCoordinateMap(2),),
        measure_convention=_convention(),
        deterministic_seed="p44-m5-sir-no-zhaocui-equality-route",
    )

    try:
        highdim.FixedBranchSquaredTTFilter(config).log_likelihood(
            _sir_model(),
            tf.zeros([0], dtype=DTYPE),
            _observations(),
        )
    except TypeError as exc:
        assert "scalar nonlinear dense value path requires state_dim == 1" in str(exc)
    else:
        raise AssertionError("SIR closure unexpectedly found a matched Zhao-Cui equality route")


def test_p44_m5_diagnostic_manifest_blocks_equality_claims() -> None:
    manifest = highdim.P30Cut4StatisticalComparatorManifest(
        version="p44.m5.sir.diagnostic.v1",
        model_id=highdim.P30ModelSuiteModelID.SPATIAL_SIR,
        comparator_status=highdim.P30Cut4ComparatorStatus.DIAGNOSTIC_ONLY,
        traceability_status=highdim.ModelSuiteTraceabilityStatus.BAYESFILTER_EXTENSION,
        comparator_description="P44 M5 clean-room SIR-inspired additive-Gaussian CUT4 diagnostic closure",
        candidate_description="no matched Zhao-Cui equality target; current highdim fixed-branch route rejects non-scalar nonlinear SIR",
        audit_design={
            "compartments": 1,
            "state_dim": 2,
            "observation_dim": 1,
            "horizon": 2,
            "augmented_dim": 4,
            "point_count": 24,
        },
        equivalence_band=None,
        ci_low=None,
        ci_high=None,
        max_abs_error=None,
        outlier_band=None,
        finite_diagnostics={
            "cut4_value_finite": True,
            "cut4_diagnostic_score_finite": True,
            "zhaocui_equality_route": "blocked_no_matched_non_scalar_target",
        },
        veto_status="PASS_DIAGNOSTIC_ONLY",
        promotion_decision="RECORD_DIAGNOSTIC_ONLY_NO_EQUALITY_CLAIM",
        non_claims=_non_claims(
            "no native SIR filtering correctness",
            "no production TT/SIRT SIR filtering",
            "no candidate-vs-CUT4 equivalence",
            "no Zhao-Cui SIR equality target",
        ),
    )

    assert manifest.comparator_status is highdim.P30Cut4ComparatorStatus.DIAGNOSTIC_ONLY
    assert manifest.equivalence_band is None
