from __future__ import annotations

import numpy as np
import pytest

from bayesfilter.inference.hmc import PrecomputedMassArtifact
from bayesfilter.inference.mass_matrix import (
    covariance_from_negative_hessian,
    covariance_from_precision,
    regularize_precision,
)


def test_hessian_mass_builder_preserves_positive_definite_precision():
    precision = np.array([[4.0, 1.0], [1.0, 3.0]])

    result = covariance_from_precision(
        precision,
        source="analytic_map_hessian",
        jitter=0.0,
    )

    np.testing.assert_allclose(result.covariance, np.linalg.inv(precision))
    np.testing.assert_allclose(result.regularized_precision, precision)
    assert result.matrix_kind == "dense"
    assert result.precision_eigen_summary["positive"] is True
    assert result.covariance_eigen_summary["positive"] is True
    assert result.regularization_report["clipped_eigenvalue_count"] == 0
    assert result.regularization_report["silent_eigenvalue_reflection"] is False


def test_hessian_mass_builder_regularizes_indefinite_precision_with_metadata():
    precision = np.array([[2.0, 0.0], [0.0, -0.5]])

    result = covariance_from_negative_hessian(
        precision,
        source="fd_psb_hessian",
        jitter=0.0,
        eigenvalue_floor=0.25,
    )

    assert result.precision_eigen_summary["positive"] is True
    assert result.covariance_eigen_summary["positive"] is True
    assert result.regularization_report["raw_nonpositive_eigenvalue_count"] == 1
    assert result.regularization_report["clipped_eigenvalue_count"] == 1
    assert result.regularization_report["effective_eigenvalue_floor"] == pytest.approx(
        0.25
    )
    np.testing.assert_allclose(
        result.regularized_precision,
        np.array([[2.0, 0.0], [0.0, 0.25]]),
    )


def test_hessian_mass_builder_records_symmetry_projection_metadata():
    precision = np.array([[2.0, 0.25], [0.0, 3.0]])

    result = covariance_from_precision(
        precision,
        source="finite_difference_hessian",
        jitter=0.0,
    )

    assert result.regularization_report["symmetry_projection"] == (
        "average_with_transpose"
    )
    assert result.regularization_report["input_asymmetric"] is True
    assert result.regularization_report["input_asymmetry_max_abs"] == pytest.approx(
        0.25
    )
    np.testing.assert_allclose(result.regularized_precision, result.regularized_precision.T)


def test_hessian_mass_builder_fails_closed_on_nonfinite_precision():
    with pytest.raises(ValueError, match="precision must be finite"):
        regularize_precision(np.array([[1.0, np.nan], [np.nan, 2.0]]))


def test_precomputed_mass_artifact_records_hessian_regularization_metadata():
    precision = np.array([[2.0, 0.0], [0.0, -0.5]])

    artifact = PrecomputedMassArtifact.from_negative_hessian(
        position=np.array([0.0, 0.0]),
        negative_hessian=precision,
        adapter_signature="test_hessian_mass_adapter_v1",
        covariance_source="fd_psb_hessian",
        jitter=0.0,
        eigenvalue_floor=0.25,
    )

    np.testing.assert_allclose(
        artifact.covariance,
        np.array([[0.5, 0.0], [0.0, 4.0]]),
    )
    np.testing.assert_allclose(artifact.factor @ artifact.factor.T, artifact.covariance)
    assert artifact.covariance_source == "fd_psb_hessian"
    assert artifact.eigen_summary["positive"] is True
    assert artifact.precision_eigen_summary["positive"] is True
    assert artifact.regularization_report["raw_nonpositive_eigenvalue_count"] == 1
    assert artifact.regularization_report["silent_eigenvalue_reflection"] is False
    assert "no posterior convergence claim" in artifact.nonclaims


def test_hessian_mass_builder_rejects_adapter_signature_mismatch():
    class Adapter:
        parameter_dim = 2

        def parameter_names(self):
            return ("a", "b")

    artifact = PrecomputedMassArtifact.from_negative_hessian(
        position=np.zeros(2),
        negative_hessian=np.eye(2),
        adapter_signature="not_the_adapter_signature",
        jitter=0.0,
    )

    with pytest.raises(ValueError, match="adapter signature mismatch"):
        artifact.validate_for_adapter(Adapter(), expected_dim=2)


def test_hessian_mass_builder_diagonal_fallback_records_provenance():
    result = covariance_from_precision(
        np.array([[4.0, 1.0], [1.0, 3.0]]),
        source="analytic_map_hessian",
        jitter=0.0,
        dense=False,
    )

    assert result.matrix_kind == "diagonal"
    np.testing.assert_allclose(result.covariance, np.diag([0.25, 1.0 / 3.0]))
    assert result.regularization_report["diagonal_fallback_used"] is True
    assert (
        result.regularization_report["diagonal_fallback_source"]
        == "regularized_precision_diagonal"
    )


def test_precomputed_mass_artifact_diagonal_fallback_records_provenance():
    artifact = PrecomputedMassArtifact.from_negative_hessian(
        position=np.zeros(2),
        negative_hessian=np.array([[4.0, 1.0], [1.0, 3.0]]),
        adapter_signature="test_diagonal_fallback_adapter_v1",
        jitter=0.0,
        dense=False,
    )

    assert artifact.regularization_report["diagonal_fallback_used"] is True
    assert (
        artifact.regularization_report["diagonal_fallback_source"]
        == "regularized_precision_diagonal"
    )
    payload = artifact.signature_payload()
    assert payload["regularization_report"]["diagonal_fallback_used"] is True
