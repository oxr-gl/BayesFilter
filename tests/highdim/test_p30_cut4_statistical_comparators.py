from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim
from bayesfilter import StatePartition
from bayesfilter.nonlinear.svd_cut_tf import tf_svd_cut4_filter
from bayesfilter.structural_tf import TFStructuralStateSpace, make_affine_structural_tf
from bayesfilter.structural import StructuralFilterConfig


@dataclass(frozen=True)
class _PairedEquivalence:
    mean_error: float
    ci_low: float
    ci_high: float
    max_abs_error: float


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _lgssm_highdim_model() -> highdim.LinearGaussianSSM:
    raw_initial_mean = tf.constant([0.05, -0.15], dtype=tf.float64)
    raw_initial_covariance = tf.constant([[0.8, 0.12], [0.12, 0.55]], dtype=tf.float64)
    transition_matrix = tf.constant([[0.72, 0.10], [-0.05, 0.58]], dtype=tf.float64)
    transition_covariance = tf.constant([[0.18, 0.03], [0.03, 0.11]], dtype=tf.float64)
    predictive_initial_mean = tf.linalg.matvec(transition_matrix, raw_initial_mean)
    predictive_initial_covariance = (
        transition_matrix
        @ raw_initial_covariance
        @ tf.transpose(transition_matrix)
        + transition_covariance
    )
    return highdim.LinearGaussianSSM(
        initial_mean=predictive_initial_mean,
        initial_covariance=predictive_initial_covariance,
        transition_matrix=transition_matrix,
        transition_covariance=transition_covariance,
        observation_matrix=tf.constant([[1.0, -0.35]], dtype=tf.float64),
        observation_covariance=tf.constant([[0.22]], dtype=tf.float64),
    )


def _lgssm_structural_model() -> TFStructuralStateSpace:
    raw_initial_mean = tf.constant([0.05, -0.15], dtype=tf.float64)
    raw_initial_covariance = tf.constant([[0.8, 0.12], [0.12, 0.55]], dtype=tf.float64)
    transition_matrix = tf.constant([[0.72, 0.10], [-0.05, 0.58]], dtype=tf.float64)
    transition_covariance = tf.constant([[0.18, 0.03], [0.03, 0.11]], dtype=tf.float64)
    model = _lgssm_highdim_model()
    partition = StatePartition(
        state_names=("x0", "x1"),
        stochastic_indices=(0, 1),
        deterministic_indices=(),
        innovation_dim=2,
    )
    return make_affine_structural_tf(
        partition=partition,
        initial_mean=raw_initial_mean,
        initial_covariance=raw_initial_covariance,
        transition_offset=model.transition_offset,
        transition_matrix=transition_matrix,
        innovation_matrix=tf.eye(2, dtype=tf.float64),
        innovation_covariance=transition_covariance,
        observation_offset=model.observation_offset,
        observation_matrix=model.observation_matrix,
        observation_covariance=model.observation_covariance,
    )


def _lgssm_filter_config() -> highdim.FixedBranchFilterConfig:
    return highdim.FixedBranchFilterConfig(
        fit_config=None,
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(highdim.IdentityCoordinateMap(2),),
        measure_convention=_convention(),
        deterministic_seed="p38-cut4-lgssm",
    )


def _paired_equivalence(errors: np.ndarray) -> _PairedEquivalence:
    values = np.asarray(errors, dtype=np.float64)
    mean = float(np.mean(values))
    if values.size <= 1:
        half_width = 0.0
    else:
        half_width = float(1.96 * np.std(values, ddof=1) / math.sqrt(values.size))
    return _PairedEquivalence(
        mean_error=mean,
        ci_low=mean - half_width,
        ci_high=mean + half_width,
        max_abs_error=float(np.max(np.abs(values))),
    )


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


def _sir_closure_model() -> tuple[highdim.SpatialSIRSSM, TFStructuralStateSpace]:
    sir = highdim.p30_spatial_sir_fixture_model(1)
    partition = StatePartition(
        state_names=("S_1", "I_1"),
        stochastic_indices=(0, 1),
        deterministic_indices=(),
        innovation_dim=2,
    )
    config = StructuralFilterConfig(
        integration_space="innovation",
        deterministic_completion="none",
        approximation_label="p38_clean_room_sir_additive_gaussian_closure",
    )
    process_chol = tf.linalg.cholesky(sir.process_covariance)

    def transition(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        previous = tf.convert_to_tensor(previous_state, dtype=tf.float64)
        innov = tf.convert_to_tensor(innovation, dtype=tf.float64)
        return sir.transition_mean(previous) + innov @ tf.transpose(process_chol)

    def observe(state_points: tf.Tensor) -> tf.Tensor:
        return sir.infectious_components(state_points)

    structural = TFStructuralStateSpace(
        partition=partition,
        config=config,
        initial_mean=sir.initial_mean,
        initial_covariance=sir.initial_covariance,
        innovation_covariance=tf.eye(2, dtype=tf.float64),
        observation_covariance=sir.observation_covariance,
        transition_fn=transition,
        observation_fn=observe,
        name="p38_clean_room_sir_cut4_closure",
    )
    return sir, structural


def _predator_prey_closure_model() -> tuple[highdim.PredatorPreySSM, TFStructuralStateSpace]:
    predator_prey = highdim.p30_predator_prey_fixture_model()
    theta = predator_prey.true_parameters()
    partition = StatePartition(
        state_names=("prey", "predator"),
        stochastic_indices=(0, 1),
        deterministic_indices=(),
        innovation_dim=2,
    )
    config = StructuralFilterConfig(
        integration_space="innovation",
        deterministic_completion="none",
        approximation_label="p38_clean_room_predator_prey_additive_gaussian_closure",
    )
    process_chol = tf.linalg.cholesky(predator_prey.process_covariance)

    def transition(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        previous = tf.convert_to_tensor(previous_state, dtype=tf.float64)
        innov = tf.convert_to_tensor(innovation, dtype=tf.float64)
        return predator_prey.transition_mean(theta, previous) + innov @ tf.transpose(process_chol)

    def observe(state_points: tf.Tensor) -> tf.Tensor:
        return tf.convert_to_tensor(state_points, dtype=tf.float64)

    structural = TFStructuralStateSpace(
        partition=partition,
        config=config,
        initial_mean=predator_prey.initial_mean,
        initial_covariance=predator_prey.initial_covariance,
        innovation_covariance=tf.eye(2, dtype=tf.float64),
        observation_covariance=predator_prey.observation_covariance,
        transition_fn=transition,
        observation_fn=observe,
        name="p38_clean_room_predator_prey_cut4_closure",
    )
    return predator_prey, structural


def test_p38_lgssm_cut4_bridge_passes_paired_equivalence_manifest() -> None:
    observations = (
        tf.constant([[0.10], [-0.05], [0.18], [0.03]], dtype=tf.float64),
        tf.constant([[0.00], [0.07], [-0.02], [0.12]], dtype=tf.float64),
        tf.constant([[-0.12], [0.02], [0.06], [-0.01]], dtype=tf.float64),
        tf.constant([[0.21], [0.18], [0.10], [0.05]], dtype=tf.float64),
    )
    candidate_values = []
    cut4_values = []
    for obs in observations:
        candidate = highdim.FixedBranchSquaredTTFilter(_lgssm_filter_config()).log_likelihood(
            _lgssm_highdim_model(),
            tf.zeros([0], dtype=tf.float64),
            obs,
        )
        cut4 = tf_svd_cut4_filter(
            obs,
            _lgssm_structural_model(),
            innovation_floor=tf.constant(1e-12, dtype=tf.float64),
        )
        candidate_values.append(float(candidate.log_likelihood.numpy()))
        cut4_values.append(float(cut4.log_likelihood.numpy()))
        assert int(cut4.diagnostics.extra["point_count"].numpy()) == 24
        np.testing.assert_allclose(
            cut4.diagnostics.extra["deterministic_residual"].numpy(),
            0.0,
            atol=1e-12,
        )

    errors = np.asarray(candidate_values) - np.asarray(cut4_values)
    stats = _paired_equivalence(errors)
    manifest = highdim.P30Cut4StatisticalComparatorManifest(
        version="p38.cut4.lgssm.equivalence.v1",
        model_id=highdim.P30ModelSuiteModelID.LGSSM_EXACT,
        comparator_status=highdim.P30Cut4ComparatorStatus.EQUIVALENCE_PASSED,
        traceability_status=highdim.ModelSuiteTraceabilityStatus.SOURCE_MATCHED,
        comparator_description="CUT4 secondary comparator; exact Kalman remains primary exact reference",
        candidate_description="highdim exact linear Gaussian value path",
        audit_design={"fixture_count": len(observations), "augmented_dim": 4, "point_count": 24},
        equivalence_band=(-1e-8, 1e-8),
        ci_low=stats.ci_low,
        ci_high=stats.ci_high,
        max_abs_error=stats.max_abs_error,
        outlier_band=1e-7,
        finite_diagnostics={"all_finite": np.isfinite(errors).all(), "mean_error": stats.mean_error},
        veto_status="PASS_LOCAL",
        promotion_decision="RECORD_COMPARATOR_EQUIVALENCE_ONLY",
        non_claims=_non_claims("no derivative claim"),
    )

    assert manifest.comparator_status is highdim.P30Cut4ComparatorStatus.EQUIVALENCE_PASSED
    assert stats.max_abs_error <= 1e-7


def test_p38_sv_direct_cut4_boundary_is_manifested_as_not_applicable() -> None:
    manifest = highdim.P30Cut4StatisticalComparatorManifest(
        version="p38.cut4.sv.not-applicable.v1",
        model_id=highdim.P30ModelSuiteModelID.STOCHASTIC_VOLATILITY_SYNTHETIC,
        comparator_status=highdim.P30Cut4ComparatorStatus.COMPARATOR_NOT_APPLICABLE,
        traceability_status=highdim.ModelSuiteTraceabilityStatus.BAYESFILTER_EXTENSION,
        comparator_description="not applicable: native SV is heteroskedastic, not additive-Gaussian CUT4 observation closure",
        candidate_description="scalar dense/TT SV value lanes keep dense quadrature comparator",
        audit_design={"native_observation": "y_t|x_t ~ N(0, beta^2 exp(x_t))"},
        equivalence_band=None,
        ci_low=None,
        ci_high=None,
        max_abs_error=None,
        outlier_band=None,
        finite_diagnostics={"cut4_direct_native_sv": "not_run_semantic_mismatch"},
        veto_status="PASS_NOT_APPLICABLE_SEMANTIC_BOUNDARY",
        promotion_decision="RECORD_NOT_APPLICABLE_BOUNDARY",
        non_claims=_non_claims("no native SV CUT4 equivalence claim"),
    )

    assert manifest.comparator_status is highdim.P30Cut4ComparatorStatus.COMPARATOR_NOT_APPLICABLE


def test_p38_sir_clean_room_cut4_closure_is_diagnostic_only() -> None:
    sir, structural = _sir_closure_model()
    _states, observations = sir.simulate(final_time=1, seed=3802)
    cut4 = tf_svd_cut4_filter(observations, structural)

    assert np.isfinite(cut4.log_likelihood.numpy())
    assert int(cut4.diagnostics.extra["point_count"].numpy()) == 24
    assert cut4.metadata.approximation_label == "p38_clean_room_sir_additive_gaussian_closure"
    manifest = highdim.P30Cut4StatisticalComparatorManifest(
        version="p38.cut4.sir.diagnostic.v1",
        model_id=highdim.P30ModelSuiteModelID.SPATIAL_SIR,
        comparator_status=highdim.P30Cut4ComparatorStatus.DIAGNOSTIC_ONLY,
        traceability_status=highdim.ModelSuiteTraceabilityStatus.BAYESFILTER_EXTENSION,
        comparator_description="clean-room SIR-inspired additive-Gaussian CUT4 diagnostic closure",
        candidate_description="no highdim candidate equivalence; SIR remains model-contract first gate",
        audit_design={"compartments": 1, "augmented_dim": 4, "point_count": 24},
        equivalence_band=None,
        ci_low=None,
        ci_high=None,
        max_abs_error=None,
        outlier_band=None,
        finite_diagnostics={"cut4_log_likelihood_finite": True},
        veto_status="PASS_DIAGNOSTIC_ONLY",
        promotion_decision="RECORD_DIAGNOSTIC_ONLY",
        non_claims=_non_claims(
            "no production TT/SIRT SIR filtering",
            "no candidate-vs-CUT4 equivalence",
        ),
    )

    assert manifest.comparator_status is highdim.P30Cut4ComparatorStatus.DIAGNOSTIC_ONLY


def test_p38_predator_prey_clean_room_cut4_closure_is_diagnostic_only() -> None:
    predator_prey, structural = _predator_prey_closure_model()
    _states, observations = predator_prey.simulate(
        predator_prey.true_parameters(),
        final_time=1,
        seed=3803,
    )
    cut4 = tf_svd_cut4_filter(observations, structural)

    assert np.isfinite(cut4.log_likelihood.numpy())
    assert int(cut4.diagnostics.extra["point_count"].numpy()) == 24
    assert cut4.metadata.approximation_label == (
        "p38_clean_room_predator_prey_additive_gaussian_closure"
    )
    manifest = highdim.P30Cut4StatisticalComparatorManifest(
        version="p38.cut4.predator-prey.diagnostic.v1",
        model_id=highdim.P30ModelSuiteModelID.PREDATOR_PREY,
        comparator_status=highdim.P30Cut4ComparatorStatus.DIAGNOSTIC_ONLY,
        traceability_status=highdim.ModelSuiteTraceabilityStatus.BAYESFILTER_EXTENSION,
        comparator_description="clean-room predator-prey-inspired additive-Gaussian CUT4 diagnostic closure",
        candidate_description="no highdim candidate equivalence; predator-prey remains first-gate model contract",
        audit_design={"augmented_dim": 4, "point_count": 24},
        equivalence_band=None,
        ci_low=None,
        ci_high=None,
        max_abs_error=None,
        outlier_band=None,
        finite_diagnostics={"cut4_log_likelihood_finite": True},
        veto_status="PASS_DIAGNOSTIC_ONLY",
        promotion_decision="RECORD_DIAGNOSTIC_ONLY",
        non_claims=_non_claims(
            "no nonlinear preconditioning usefulness",
            "no candidate-vs-CUT4 equivalence",
        ),
    )

    assert manifest.traceability_status is highdim.ModelSuiteTraceabilityStatus.BAYESFILTER_EXTENSION


def test_p38_cut4_manifest_blocks_diagnostic_equivalence_metrics_and_overclaim() -> None:
    with pytest.raises(ValueError, match="non-equivalence rows"):
        highdim.P30Cut4StatisticalComparatorManifest(
            version="p38.cut4.bad-diagnostic.v1",
            model_id=highdim.P30ModelSuiteModelID.SPATIAL_SIR,
            comparator_status=highdim.P30Cut4ComparatorStatus.DIAGNOSTIC_ONLY,
            traceability_status=highdim.ModelSuiteTraceabilityStatus.BAYESFILTER_EXTENSION,
            comparator_description="diagnostic only",
            candidate_description="none",
            audit_design={"augmented_dim": 4},
            equivalence_band=(-1.0, 1.0),
            ci_low=0.0,
            ci_high=0.0,
            max_abs_error=0.0,
            outlier_band=1.0,
            finite_diagnostics={"finite": True},
            veto_status="PASS_DIAGNOSTIC_ONLY",
            promotion_decision="RECORD_DIAGNOSTIC_ONLY",
            non_claims=_non_claims(),
        )

    with pytest.raises(ValueError, match="cannot promote defaults"):
        highdim.P30Cut4StatisticalComparatorManifest(
            version="p38.cut4.bad-promote.v1",
            model_id=highdim.P30ModelSuiteModelID.LGSSM_EXACT,
            comparator_status=highdim.P30Cut4ComparatorStatus.EQUIVALENCE_PASSED,
            traceability_status=highdim.ModelSuiteTraceabilityStatus.SOURCE_MATCHED,
            comparator_description="CUT4 comparator",
            candidate_description="highdim exact value path",
            audit_design={"augmented_dim": 4},
            equivalence_band=(-1.0, 1.0),
            ci_low=0.0,
            ci_high=0.0,
            max_abs_error=0.0,
            outlier_band=1.0,
            finite_diagnostics={"finite": True},
            veto_status="PASS_LOCAL",
            promotion_decision="PROMOTE_DEFAULT_METHOD",
            non_claims=_non_claims(),
        )


def test_p38_cut4_manifest_requires_core_nonclaims() -> None:
    with pytest.raises(ValueError, match="ground truth"):
        highdim.P30Cut4StatisticalComparatorManifest(
            version="p38.cut4.missing-nonclaims.v1",
            model_id=highdim.P30ModelSuiteModelID.LGSSM_EXACT,
            comparator_status=highdim.P30Cut4ComparatorStatus.EQUIVALENCE_PASSED,
            traceability_status=highdim.ModelSuiteTraceabilityStatus.SOURCE_MATCHED,
            comparator_description="CUT4 comparator",
            candidate_description="highdim exact value path",
            audit_design={"augmented_dim": 4},
            equivalence_band=(-1.0, 1.0),
            ci_low=0.0,
            ci_high=0.0,
            max_abs_error=0.0,
            outlier_band=1.0,
            finite_diagnostics={"finite": True},
            veto_status="PASS_LOCAL",
            promotion_decision="RECORD_COMPARATOR_EQUIVALENCE_ONLY",
            non_claims=("no paper-scale validation",),
        )


def test_p38_cut4_manifest_symbols_are_subpackage_scoped() -> None:
    assert hasattr(highdim, "P30Cut4StatisticalComparatorManifest")
    assert hasattr(highdim, "P30Cut4ComparatorStatus")
    assert "P30Cut4StatisticalComparatorManifest" in highdim.__all__
    assert "P30Cut4ComparatorStatus" in highdim.__all__
