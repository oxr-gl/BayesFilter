from __future__ import annotations

import tensorflow as tf

import bayesfilter.highdim as highdim
from bayesfilter.highdim import stochastic_density_training as p75


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _author_product_basis(dimension: int = 2) -> highdim.ProductBasis:
    spec = highdim.p85_author_sir_lagrangep_algebraic_product_basis_spec(
        dimension=dimension,
        convention=_convention(),
    )
    return spec.build_product_basis()


def _rank_one_functional_tt(product: highdim.ProductBasis, values: tuple[float, ...]) -> highdim.FunctionalTT:
    cores = []
    for axis, value in enumerate(values):
        updates = tf.ones([product.bases[axis].basis_dim], dtype=tf.float64) * value
        cores.append(highdim.TTCore(tf.reshape(updates, [1, -1, 1])))
    return highdim.FunctionalTT(cores, product, _convention())


def _branch_identity(
    ftt: highdim.FunctionalTT,
    defensive: highdim.TensorProductReferenceDensity,
    tau: float,
) -> highdim.BranchIdentity:
    return highdim.SquaredTTDensity.expected_branch_identity(
        sqrt_tt=ftt,
        defensive_density=defensive,
        tau=tf.constant(tau, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=_convention(),
    )


def _density(product: highdim.ProductBasis) -> highdim.SquaredTTDensity:
    ftt = _rank_one_functional_tt(product, (2.0, 3.0))
    defensive = highdim.TensorProductReferenceDensity(product, _convention())
    tau = 0.25
    return highdim.SquaredTTDensity(
        sqrt_tt=ftt,
        defensive_density=defensive,
        tau=tf.constant(tau, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=_convention(),
        branch_identity=_branch_identity(ftt, defensive, tau),
    )


def test_p86_functional_tt_integrate_all_consumes_author_lagrangep_basis() -> None:
    product = _author_product_basis(2)
    ftt = _rank_one_functional_tt(product, (2.0, 3.0))

    tf.debugging.assert_near(
        ftt.integrate_all(),
        tf.constant(6.0, dtype=tf.float64),
        atol=tf.constant(1e-12, dtype=tf.float64),
    )
    assert ftt.basis_dim_tuple() == (33, 33)


def test_p86_functional_tt_manifest_serializes_author_lagrangep_algebraic_route() -> None:
    product = _author_product_basis(2)
    ftt = _rank_one_functional_tt(product, (2.0, 3.0))

    basis_payloads = ftt.manifest_payload()["bases"]

    assert tuple(basis["family"] for basis in basis_payloads) == ("lagrangep", "lagrangep")
    assert tuple(basis["domain_map"]["family"] for basis in basis_payloads) == ("algebraic", "algebraic")
    assert tuple(basis["basis_dim"] for basis in basis_payloads) == (33, 33)
    assert tuple(basis["order"] for basis in basis_payloads) == (4, 4)
    assert tuple(basis["num_elems"] for basis in basis_payloads) == (8, 8)


def test_p86_trainable_snapshot_manifest_serializes_author_lagrangep_algebraic_route() -> None:
    product = _author_product_basis(2)
    config = p75.P75TrainableTTConfig(
        product_basis=product,
        ranks=(1, 1, 1),
        tau=tf.constant(0.25, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
    )
    initial_cores = tuple(core.values for core in _rank_one_functional_tt(product, (1.0, 1.0)).cores)
    trainable = p75.TrainableFunctionalTT(config, initial_cores=initial_cores)
    density = trainable.snapshot_density()

    basis_payloads = density.branch_identity.manifest.payload["sqrt_tt"]["bases"]

    assert tuple(basis["family"] for basis in basis_payloads) == ("lagrangep", "lagrangep")
    assert tuple(basis["domain_map"]["family"] for basis in basis_payloads) == ("algebraic", "algebraic")
    assert tuple(basis["basis_dim"] for basis in basis_payloads) == (33, 33)


def test_p86_squared_tt_normalizer_and_marginal_consume_author_lagrangep_basis() -> None:
    product = _author_product_basis(2)
    density = _density(product)
    points = tf.constant([[-0.5], [0.0], [0.5]], dtype=tf.float64)

    tf.debugging.assert_near(
        density.sqrt_square_normalizer(),
        tf.constant(36.0, dtype=tf.float64),
        atol=tf.constant(1e-12, dtype=tf.float64),
    )
    tf.debugging.assert_near(
        density.normalizer(),
        tf.constant(36.25, dtype=tf.float64),
        atol=tf.constant(1e-12, dtype=tf.float64),
    )
    marginal_values = density.normalized_marginal_density_values([0], points)

    assert marginal_values.shape == (3,)
    assert bool(tf.reduce_all(tf.math.is_finite(marginal_values)).numpy())


def test_p86_trainable_tt_normalizer_consumes_author_lagrangep_basis_without_training() -> None:
    product = _author_product_basis(2)
    config = p75.P75TrainableTTConfig(
        product_basis=product,
        ranks=(1, 1, 1),
        tau=tf.constant(0.25, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
    )
    initial_cores = tuple(core.values for core in _rank_one_functional_tt(product, (2.0, 3.0)).cores)
    trainable = p75.TrainableFunctionalTT(config, initial_cores=initial_cores)

    tf.debugging.assert_near(
        trainable.sqrt_square_normalizer(),
        tf.constant(36.0, dtype=tf.float64),
        atol=tf.constant(1e-12, dtype=tf.float64),
    )
    tf.debugging.assert_near(
        trainable.normalizer(),
        tf.constant(36.25, dtype=tf.float64),
        atol=tf.constant(1e-12, dtype=tf.float64),
    )


def test_p86_squared_tt_normalizer_derivative_consumes_author_lagrangep_basis() -> None:
    product = _author_product_basis(2)
    ftt = _rank_one_functional_tt(product, (2.0, 3.0))
    dot_cores = (
        highdim.TTCore(tf.ones_like(ftt.cores[0].values)),
        highdim.TTCore(tf.zeros_like(ftt.cores[1].values)),
    )

    derivative = highdim.squared_tt_normalizer_derivative(ftt, dot_cores)

    assert derivative.shape == ()
    assert bool(tf.math.is_finite(derivative).numpy())
