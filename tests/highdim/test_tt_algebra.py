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


def _product_basis(degrees: tuple[int, ...]) -> highdim.ProductBasis:
    return highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), degree) for degree in degrees],
        _convention(),
    )


def _product_basis_on_interval(
    degrees: tuple[int, ...],
    left: float,
    right: float,
) -> highdim.ProductBasis:
    return highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(left, right), degree) for degree in degrees],
        _convention(),
    )


def test_rank_one_tt_product_evaluates_exactly():
    product = _product_basis((1, 1))
    core0 = highdim.TTCore(tf.constant([[[1.0], [2.0]]], dtype=tf.float64))
    core1 = highdim.TTCore(tf.constant([[[3.0], [4.0]]], dtype=tf.float64))
    ftt = highdim.FunctionalTT([core0, core1], product, _convention())
    points = tf.constant([[0.0, 0.0], [0.5, -0.25]], dtype=tf.float64)

    values = ftt.evaluate(points)
    psi0 = product.evaluate_axis(0, points[:, 0])
    psi1 = product.evaluate_axis(1, points[:, 1])
    expected = (psi0[:, 0] + 2.0 * psi0[:, 1]) * (
        3.0 * psi1[:, 0] + 4.0 * psi1[:, 1]
    )

    tf.debugging.assert_near(values, expected, atol=1e-12)


def test_low_rank_bivariate_polynomial_evaluates_exactly():
    product = _product_basis((1, 1))
    core0 = highdim.TTCore(
        tf.constant(
            [
                [[1.0, 0.0], [0.0, 1.0]],
            ],
            dtype=tf.float64,
        )
    )
    core1 = highdim.TTCore(
        tf.constant(
            [
                [[1.0], [1.0]],
                [[2.0], [3.0]],
            ],
            dtype=tf.float64,
        )
    )
    ftt = highdim.FunctionalTT([core0, core1], product, _convention())
    points = tf.constant([[0.1, -0.2], [0.3, 0.4]], dtype=tf.float64)

    psi0 = product.evaluate_axis(0, points[:, 0])
    psi1 = product.evaluate_axis(1, points[:, 1])
    expected = psi0[:, 0] * (psi1[:, 0] + psi1[:, 1]) + psi0[:, 1] * (
        2.0 * psi1[:, 0] + 3.0 * psi1[:, 1]
    )

    tf.debugging.assert_near(ftt.evaluate(points), expected, atol=1e-12)


def test_trivariate_coupled_function_has_expected_rank_shape_and_integral():
    product = _product_basis((1, 1, 1))
    core0 = highdim.TTCore(tf.constant([[[1.0, 0.0], [0.0, 1.0]]], dtype=tf.float64))
    core1 = highdim.TTCore(
        tf.constant(
            [
                [[1.0, 0.0], [0.0, 1.0]],
                [[0.0, 1.0], [1.0, 0.0]],
            ],
            dtype=tf.float64,
        )
    )
    core2 = highdim.TTCore(tf.constant([[[1.0], [0.0]], [[0.0], [1.0]]], dtype=tf.float64))
    ftt = highdim.FunctionalTT([core0, core1, core2], product, _convention())

    assert ftt.rank_tuple() == (1, 2, 2, 1)
    assert ftt.basis_dim_tuple() == (2, 2, 2)
    tf.debugging.assert_near(ftt.integrate_all(), tf.constant(1.0, dtype=tf.float64), atol=1e-12)


def test_integrate_all_uses_declared_mass_measure():
    product = _product_basis((0,))
    core = highdim.TTCore(tf.constant([[[2.0]]], dtype=tf.float64))
    ftt = highdim.FunctionalTT([core], product, _convention())

    tf.debugging.assert_near(ftt.integrate_all(), tf.constant(2.0, dtype=tf.float64), atol=0.0)


def test_functional_tt_rejects_product_basis_measure_mismatch():
    product = _product_basis((0,))
    mismatched = highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_LEBESGUE,
        mass_measure=highdim.MassMeasure.REFERENCE_LEBESGUE,
        reference_weight_name="omega",
    )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.MEASURE_MISMATCH.value):
        highdim.FunctionalTT(
            [highdim.TTCore(tf.constant([[[1.0]]], dtype=tf.float64))],
            product,
            mismatched,
        )


def test_marginalization_records_integrated_and_kept_axes():
    product = _product_basis((1, 1))
    ftt = highdim.FunctionalTT(
        [
            highdim.TTCore(tf.constant([[[1.0, 2.0], [0.0, 3.0]]], dtype=tf.float64)),
            highdim.TTCore(tf.constant([[[5.0], [7.0]], [[11.0], [13.0]]], dtype=tf.float64)),
        ],
        product,
        _convention(),
    )

    contracted = ftt.contract_axes([1])

    assert contracted.kept_axes == (0,)
    assert contracted.integrated_axes == (1,)
    assert contracted.diagnostics["status"] == highdim.HighDimStatus.OK.value
    assert contracted.branch_identity is not None
    expected_core = tf.constant([[[27.0], [33.0]]], dtype=tf.float64)
    tf.debugging.assert_near(contracted.cores[0].values, expected_core, atol=1e-12)


def test_full_axis_contraction_records_scalar_without_fake_core():
    product = _product_basis((0, 0))
    ftt = highdim.FunctionalTT(
        [
            highdim.TTCore(tf.constant([[[2.0]]], dtype=tf.float64)),
            highdim.TTCore(tf.constant([[[3.0]]], dtype=tf.float64)),
        ],
        product,
        _convention(),
    )

    contracted = ftt.contract_axes([0, 1])

    assert contracted.kept_axes == ()
    assert contracted.integrated_axes == (0, 1)
    assert contracted.cores == ()
    assert contracted.diagnostics["representation"] == "scalar"
    tf.debugging.assert_near(
        contracted.scalar_value,
        tf.constant(6.0, dtype=tf.float64),
        atol=0.0,
    )


def test_contracted_branch_identity_hashes_contracted_payload():
    product = _product_basis((0, 0))
    ftt = highdim.FunctionalTT(
        [
            highdim.TTCore(tf.constant([[[2.0]]], dtype=tf.float64)),
            highdim.TTCore(tf.constant([[[3.0]]], dtype=tf.float64)),
        ],
        product,
        _convention(),
    )

    contracted = ftt.contract_axes([1])

    assert contracted.branch_identity.hash == contracted.manifest().sha256()
    assert contracted.branch_identity.hash != ftt.manifest().sha256()


def test_contracted_branch_hash_changes_with_retained_basis_domain():
    cores = [
        highdim.TTCore(tf.constant([[[2.0]]], dtype=tf.float64)),
        highdim.TTCore(tf.constant([[[3.0]]], dtype=tf.float64)),
    ]
    reference = highdim.FunctionalTT(cores, _product_basis_on_interval((0, 0), -1.0, 1.0), _convention())
    changed_basis = highdim.FunctionalTT(cores, _product_basis_on_interval((0, 0), 0.0, 1.0), _convention())

    reference_contracted = reference.contract_axes([1])
    changed_contracted = changed_basis.contract_axes([1])

    assert reference_contracted.retained_bases != changed_contracted.retained_bases
    assert reference_contracted.branch_identity.hash != changed_contracted.branch_identity.hash


def test_branch_manifest_hash_changes_when_core_or_basis_field_changes():
    product = _product_basis((0,))
    ftt = highdim.FunctionalTT(
        [highdim.TTCore(tf.constant([[[1.0]]], dtype=tf.float64))],
        product,
        _convention(),
    )
    changed = highdim.FunctionalTT(
        [highdim.TTCore(tf.constant([[[2.0]]], dtype=tf.float64))],
        product,
        _convention(),
    )

    assert ftt.manifest().sha256() != changed.manifest().sha256()

    changed_basis = highdim.ProductBasis(
        [highdim.LegendreBasis1D(highdim.BoundedInterval(0.0, 1.0), 0)],
        _convention(),
    )
    changed_basis_ftt = highdim.FunctionalTT(
        [highdim.TTCore(tf.constant([[[1.0]]], dtype=tf.float64))],
        changed_basis,
        _convention(),
    )

    assert ftt.manifest().sha256() != changed_basis_ftt.manifest().sha256()


def test_complexity_gate_fires_before_large_allocation():
    product = _product_basis((0,))
    ftt = highdim.FunctionalTT(
        [highdim.TTCore(tf.constant([[[1.0]]], dtype=tf.float64))],
        product,
        _convention(),
    )
    result = ftt.validate_complexity(
        budget=highdim.ComplexityBudget(max_elements=4, max_bytes=32),
        estimated_elements=5,
    )

    assert result.status is highdim.HighDimStatus.COMPLEXITY_GATE


def test_evaluate_and_contraction_enforce_complexity_budget_before_work():
    product = _product_basis((1,))
    ftt = highdim.FunctionalTT(
        [highdim.TTCore(tf.constant([[[1.0], [2.0]]], dtype=tf.float64))],
        product,
        _convention(),
        complexity_budget=highdim.ComplexityBudget(max_elements=1, max_bytes=8),
    )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.COMPLEXITY_GATE.value):
        ftt.evaluate(tf.constant([[0.0]], dtype=tf.float64))

    with pytest.raises(ValueError, match=highdim.HighDimStatus.COMPLEXITY_GATE.value):
        ftt.integrate_all()

    with pytest.raises(ValueError, match=highdim.HighDimStatus.COMPLEXITY_GATE.value):
        ftt.contract_axes([0])


def test_contract_axes_complexity_accounts_for_retained_rank_growth():
    product = _product_basis((0, 0, 0, 0))
    ftt = highdim.FunctionalTT(
        [
            highdim.TTCore(tf.ones([1, 1, 100], dtype=tf.float64)),
            highdim.TTCore(tf.ones([100, 1, 100], dtype=tf.float64)),
            highdim.TTCore(tf.ones([100, 1, 100], dtype=tf.float64)),
            highdim.TTCore(tf.ones([100, 1, 1], dtype=tf.float64)),
        ],
        product,
        _convention(),
        complexity_budget=highdim.ComplexityBudget(max_elements=100_000, max_bytes=800_000),
    )

    with pytest.raises(ValueError, match=highdim.HighDimStatus.COMPLEXITY_GATE.value):
        ftt.contract_axes([1])
