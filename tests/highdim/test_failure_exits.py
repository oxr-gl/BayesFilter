from __future__ import annotations

import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _identity(
    ftt: highdim.FunctionalTT,
    defensive: highdim.TensorProductReferenceDensity,
    tau: float = 0.0,
    normalizer_floor: float = 1e-12,
    denominator_floor: float = 1e-12,
) -> highdim.BranchIdentity:
    return highdim.SquaredTTDensity.expected_branch_identity(
        sqrt_tt=ftt,
        defensive_density=defensive,
        tau=tf.constant(tau, dtype=tf.float64),
        normalizer_floor=tf.constant(normalizer_floor, dtype=tf.float64),
        denominator_floor=tf.constant(denominator_floor, dtype=tf.float64),
        measure_convention=_convention(),
    )


def test_squared_tt_normalizer_floor_is_veto_status():
    product = highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 0)],
        _convention(),
    )
    ftt = highdim.FunctionalTT(
        [highdim.TTCore(tf.constant([[[0.0]]], dtype=tf.float64))],
        product,
        _convention(),
    )
    defensive = highdim.TensorProductReferenceDensity(product, _convention())
    density = highdim.SquaredTTDensity(
        sqrt_tt=ftt,
        defensive_density=defensive,
        tau=tf.constant(0.0, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=_convention(),
        branch_identity=_identity(ftt, defensive),
    )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.NORMALIZER_FLOOR_EXCEEDED.value):
        density.normalizer()


def test_conditional_denominator_floor_is_veto_status():
    product = highdim.ProductBasis(
        [
            highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 1),
            highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 0),
        ],
        _convention(),
    )
    ftt = highdim.FunctionalTT(
        [
            highdim.TTCore(tf.constant([[[0.0], [1.0]]], dtype=tf.float64)),
            highdim.TTCore(tf.constant([[[1.0]]], dtype=tf.float64)),
        ],
        product,
        _convention(),
    )
    defensive = highdim.TensorProductReferenceDensity(product, _convention())
    density = highdim.SquaredTTDensity(
        sqrt_tt=ftt,
        defensive_density=defensive,
        tau=tf.constant(0.0, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=_convention(),
        branch_identity=_identity(
            ftt,
            defensive,
            normalizer_floor=1e-12,
            denominator_floor=1e-12,
        ),
    )
    grid = tf.linspace(tf.constant(-1.0, dtype=tf.float64), tf.constant(1.0, dtype=tf.float64), 5)

    with pytest.raises(ValueError, match=highdim.HighDimStatus.CONDITIONAL_DENOMINATOR_FLOOR_EXCEEDED.value):
        density.conditional_density(1, tf.constant([[0.0]], dtype=tf.float64), grid)


def test_density_constructor_rejects_nonfinite_floor():
    product = highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 0)],
        _convention(),
    )
    ftt = highdim.FunctionalTT(
        [highdim.TTCore(tf.constant([[[1.0]]], dtype=tf.float64))],
        product,
        _convention(),
    )
    defensive = highdim.TensorProductReferenceDensity(product, _convention())

    with pytest.raises(ValueError, match=highdim.HighDimStatus.NONFINITE_VALUE.value):
        highdim.SquaredTTDensity(
            sqrt_tt=ftt,
            defensive_density=defensive,
            tau=tf.constant(float("nan"), dtype=tf.float64),
            normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
            denominator_floor=tf.constant(1e-12, dtype=tf.float64),
            measure_convention=_convention(),
            branch_identity=_identity(ftt, defensive),
        )


def test_density_rejects_unrelated_branch_identity():
    product = highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 0)],
        _convention(),
    )
    ftt = highdim.FunctionalTT(
        [highdim.TTCore(tf.constant([[[1.0]]], dtype=tf.float64))],
        product,
        _convention(),
    )
    defensive = highdim.TensorProductReferenceDensity(product, _convention())
    wrong_manifest = ftt.manifest()

    with pytest.raises(ValueError, match=highdim.HighDimStatus.INVALID_BRANCH_MISMATCH.value):
        highdim.SquaredTTDensity(
            sqrt_tt=ftt,
            defensive_density=defensive,
            tau=tf.constant(0.0, dtype=tf.float64),
            normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
            denominator_floor=tf.constant(1e-12, dtype=tf.float64),
            measure_convention=_convention(),
            branch_identity=highdim.BranchIdentity(
                manifest=wrong_manifest,
                hash=wrong_manifest.sha256(),
            ),
        )


def _fit_config(
    ranks: tuple[int, ...],
    row_budget: int = 10_000,
    column_budget: int = 1_000,
    dense_matrix_byte_budget: int = 10_000_000,
    normal_matrix_byte_budget: int = 10_000_000,
    condition_number_veto: float = 1e14,
) -> highdim.FixedTTFitConfig:
    return highdim.FixedTTFitConfig(
        ranks=ranks,
        ridge=0.0,
        max_sweeps=1,
        sweep_order=tuple(range(len(ranks) - 1)),
        row_budget=row_budget,
        column_budget=column_budget,
        dense_matrix_byte_budget=dense_matrix_byte_budget,
        normal_matrix_byte_budget=normal_matrix_byte_budget,
        condition_number_warning=1e10,
        condition_number_veto=condition_number_veto,
        holdout_tolerance=1e-10,
    )


def _fit_product(degrees: tuple[int, ...]) -> highdim.ProductBasis:
    return highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), degree) for degree in degrees],
        _convention(),
    )


class _NoDesignAllocationFitter(highdim.FixedTTFitter):
    def _build_design_matrix(self, *args, **kwargs):  # pragma: no cover - fail-fast guard
        raise AssertionError("design matrix should not be allocated after a complexity gate")


def test_row_column_and_normal_matrix_budgets_fail_before_allocation():
    product = _fit_product((1, 1))
    points = tf.constant([[-0.5, -0.5], [0.5, 0.5]], dtype=tf.float64)
    samples = highdim.FixedTTFitSampleBatch(
        points=points,
        target_values=tf.ones([2], dtype=tf.float64),
        weights=tf.ones([2], dtype=tf.float64),
    )
    cores = [
        highdim.TTCore(tf.ones([1, 2, 2], dtype=tf.float64)),
        highdim.TTCore(tf.ones([2, 2, 1], dtype=tf.float64)),
    ]

    row = _NoDesignAllocationFitter().fit(
        product,
        samples,
        _fit_config((1, 2, 1), row_budget=1),
        cores,
        branch_seed="row",
        measure_convention=_convention(),
    )
    column = _NoDesignAllocationFitter().fit(
        product,
        samples,
        _fit_config((1, 2, 1), column_budget=3),
        cores,
        branch_seed="column",
        measure_convention=_convention(),
    )
    normal = _NoDesignAllocationFitter().fit(
        product,
        samples,
        _fit_config((1, 2, 1), normal_matrix_byte_budget=8),
        cores,
        branch_seed="normal",
        measure_convention=_convention(),
    )

    assert row.status is highdim.HighDimStatus.COMPLEXITY_GATE
    assert row.core_update_statuses[0]["gate"] == "row_budget"
    assert column.status is highdim.HighDimStatus.COMPLEXITY_GATE
    assert column.core_update_statuses[0]["gate"] == "column_budget"
    assert normal.status is highdim.HighDimStatus.COMPLEXITY_GATE
    assert normal.core_update_statuses[0]["gate"] == "normal_matrix_byte_budget"


def test_dense_matrix_budget_fails_before_allocation():
    product = _fit_product((1, 1))
    points = tf.constant([[-0.5, -0.5], [0.5, 0.5]], dtype=tf.float64)
    samples = highdim.FixedTTFitSampleBatch(
        points=points,
        target_values=tf.ones([2], dtype=tf.float64),
        weights=tf.ones([2], dtype=tf.float64),
    )
    cores = [
        highdim.TTCore(tf.ones([1, 2, 2], dtype=tf.float64)),
        highdim.TTCore(tf.ones([2, 2, 1], dtype=tf.float64)),
    ]

    result = _NoDesignAllocationFitter().fit(
        product,
        samples,
        _fit_config((1, 2, 1), dense_matrix_byte_budget=8),
        cores,
        branch_seed="dense",
        measure_convention=_convention(),
    )

    assert result.status is highdim.HighDimStatus.COMPLEXITY_GATE
    assert result.core_update_statuses[0]["gate"] == "dense_matrix_byte_budget"


def test_condition_number_veto_status_is_deterministic():
    product = _fit_product((1,))
    points = tf.constant([[0.0], [0.0]], dtype=tf.float64)
    samples = highdim.FixedTTFitSampleBatch(
        points=points,
        target_values=tf.ones([2], dtype=tf.float64),
        weights=tf.ones([2], dtype=tf.float64),
    )
    cores = [highdim.TTCore(tf.ones([1, 2, 1], dtype=tf.float64))]

    first = highdim.FixedTTFitter().fit(
        product,
        samples,
        _fit_config((1, 1), condition_number_veto=10.0),
        cores,
        branch_seed="condition",
        measure_convention=_convention(),
    )
    second = highdim.FixedTTFitter().fit(
        product,
        samples,
        _fit_config((1, 1), condition_number_veto=10.0),
        cores,
        branch_seed="condition",
        measure_convention=_convention(),
    )

    assert first.status is highdim.HighDimStatus.CONDITION_NUMBER_VETO
    assert second.status is highdim.HighDimStatus.CONDITION_NUMBER_VETO
    assert first.branch_hash == second.branch_hash


def test_fixed_fit_missing_measure_convention_fails():
    product = _fit_product((0,))
    mismatched = highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_LEBESGUE,
        mass_measure=highdim.MassMeasure.REFERENCE_LEBESGUE,
        reference_weight_name="omega",
    )
    samples = highdim.FixedTTFitSampleBatch(
        points=tf.constant([[0.0]], dtype=tf.float64),
        target_values=tf.ones([1], dtype=tf.float64),
        weights=tf.ones([1], dtype=tf.float64),
    )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.MEASURE_MISMATCH.value):
        highdim.FixedTTFitter().fit(
            product,
            samples,
            _fit_config((1, 1), condition_number_veto=1e14),
            [highdim.TTCore(tf.ones([1, 1, 1], dtype=tf.float64))],
            branch_seed="measure",
            measure_convention=mismatched,
        )
