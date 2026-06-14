from __future__ import annotations

from pathlib import Path

import pytest
import tensorflow as tf

import bayesfilter
import bayesfilter.highdim as highdim


ROOT = Path(__file__).resolve().parents[2]


def _reference_convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _manifest_payload(scale: float = 1.0) -> dict[str, object]:
    return {
        "basis": {"family": "legendre", "degree": 2},
        "sample_points": tf.constant([[scale, 2.0]], dtype=tf.float64),
        "ranks": (1, 2, 1),
        "active": True,
        "none_field": None,
    }


def test_highdim_import_does_not_touch_top_level_all():
    assert hasattr(highdim, "MeasureConvention")
    assert "MeasureConvention" not in bayesfilter.__all__
    assert "BranchManifest" not in bayesfilter.__all__


def test_measure_convention_rejects_missing_density_measure():
    with pytest.raises(TypeError, match="density_measure"):
        highdim.MeasureConvention(
            density_measure="REFERENCE_MEASURE",
            mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
            reference_weight_name="omega",
        )


def test_measure_convention_rejects_density_mass_mismatch():
    convention = highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_LEBESGUE,
        reference_weight_name="omega",
    )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.MEASURE_MISMATCH.value):
        highdim.assert_density_matches_mass(convention)


def test_assert_finite_tensor_rejects_nan_and_inf():
    with pytest.raises(ValueError, match=highdim.HighDimStatus.NONFINITE_VALUE.value):
        highdim.assert_finite_tensor(
            "bad",
            tf.constant([1.0, float("nan"), float("inf")], dtype=tf.float64),
        )


def test_assert_shape_rejects_rank_mismatch():
    with pytest.raises(ValueError, match=highdim.HighDimStatus.INVALID_SHAPE.value):
        highdim.assert_shape(
            "bad_rank",
            tf.constant([[1.0, 2.0]], dtype=tf.float64),
            expected_rank=1,
        )


def test_branch_hash_is_identical_for_identical_manifest():
    left = highdim.BranchManifest("phase0.v1", _manifest_payload()).sha256()
    right = highdim.BranchManifest("phase0.v1", _manifest_payload()).sha256()

    assert left == right


def test_branch_hash_changes_for_each_manifest_field():
    base = highdim.BranchManifest("phase0.v1", _manifest_payload()).sha256()

    changed_version = highdim.BranchManifest("phase0.v2", _manifest_payload()).sha256()
    changed_payload = highdim.BranchManifest("phase0.v1", _manifest_payload(3.0)).sha256()
    changed_nested = highdim.BranchManifest(
        "phase0.v1",
        {**_manifest_payload(), "basis": {"family": "legendre", "degree": 3}},
    ).sha256()

    assert base != changed_version
    assert base != changed_payload
    assert base != changed_nested


def test_branch_hash_records_tensor_dtype_shape_and_values():
    base_payload = {"x": tf.constant([1.0, 2.0], dtype=tf.float64)}
    changed_shape_payload = {"x": tf.constant([[1.0, 2.0]], dtype=tf.float64)}
    changed_dtype_payload = {"x": tf.constant([1, 2], dtype=tf.int32)}

    base = highdim.BranchManifest("phase0.v1", base_payload).sha256()
    changed_shape = highdim.BranchManifest("phase0.v1", changed_shape_payload).sha256()
    changed_dtype = highdim.BranchManifest("phase0.v1", changed_dtype_payload).sha256()

    assert base != changed_shape
    assert base != changed_dtype


def test_selective_hash_cannot_construct_branch_identity():
    manifest = highdim.BranchManifest("phase0.v1", _manifest_payload())
    selective = highdim.BranchManifest("phase0.v1", {"basis": "only"}).sha256()

    with pytest.raises(
        ValueError,
        match=highdim.HighDimStatus.SELECTIVE_BRANCH_HASH_REJECTED.value,
    ):
        highdim.BranchIdentity(manifest=manifest, hash=selective)


def test_valid_branch_identity_accepts_full_manifest_hash():
    manifest = highdim.BranchManifest("phase0.v1", _manifest_payload())
    identity = highdim.BranchIdentity(manifest=manifest, hash=manifest.sha256())

    assert identity.hash == manifest.sha256()


def test_numpy_not_used_as_highdim_algorithmic_backend():
    module_paths = [
        ROOT / "bayesfilter" / "highdim" / "__init__.py",
        ROOT / "bayesfilter" / "highdim" / "derivatives.py",
        ROOT / "bayesfilter" / "highdim" / "diagnostics.py",
        ROOT / "bayesfilter" / "highdim" / "fixed_branch.py",
        ROOT / "bayesfilter" / "highdim" / "filtering.py",
        ROOT / "bayesfilter" / "highdim" / "fitting.py",
        ROOT / "bayesfilter" / "highdim" / "models.py",
        ROOT / "bayesfilter" / "highdim" / "source_route.py",
        ROOT / "bayesfilter" / "highdim" / "validation.py",
    ]

    for path in module_paths:
        text = path.read_text(encoding="utf-8")
        assert "import numpy" not in text
        assert "from numpy" not in text


def test_complexity_budget_returns_deterministic_status():
    result = highdim.ComplexityBudget(max_elements=10, max_bytes=80).validate(
        estimated_elements=11,
        dtype_size=8,
    )

    assert result.status is highdim.HighDimStatus.COMPLEXITY_GATE
    assert result.diagnostics["estimated_bytes"] == 88
