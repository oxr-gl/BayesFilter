from __future__ import annotations

import tensorflow as tf

import bayesfilter.highdim as highdim


def _reference_convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def test_p85_domain_map_specs_payload_bounded_and_algebraic() -> None:
    bounded = highdim.DomainMapSpec.bounded_interval(
        -1.0,
        1.0,
        classification=highdim.P85_LEGACY_DIAGNOSTIC_CLASSIFICATION,
        classification_subtype=highdim.P85_LEGACY_DIAGNOSTIC_SUBTYPE,
        source_anchors=highdim.P85_LEGACY_DIAGNOSTIC_BASIS_DOMAIN_SOURCE_ANCHORS,
    )
    algebraic = highdim.DomainMapSpec.algebraic(
        1.0,
        classification=highdim.P85_AUTHOR_SIR_CLASSIFICATION,
        classification_subtype=highdim.P85_AUTHOR_SIR_SUBTYPE,
        source_anchors=highdim.P85_AUTHOR_SIR_BASIS_DOMAIN_SOURCE_ANCHORS,
    )

    assert bounded.manifest_payload()["family"] == "bounded_interval"
    assert bounded.manifest_payload()["classification_subtype"] == "diagnostic_legendre_route"
    assert algebraic.manifest_payload()["family"] == "algebraic"
    assert algebraic.manifest_payload()["classification"] == "source_faithful"
    assert algebraic.manifest_payload()["scale"] == 1.0


def test_p85_algebraic_map_formula_and_inverse() -> None:
    mapping = highdim.AlgebraicMap(1.0)
    points = tf.constant([-2.0, 0.0, 2.0], dtype=tf.float64)
    expected_reference = points / tf.sqrt(1.0 + tf.square(points))

    reference = mapping.to_reference(points)
    tf.debugging.assert_near(reference, expected_reference)
    tf.debugging.assert_near(mapping.from_reference(reference), points)

    log_density = mapping.domain_to_reference_log_density(points)
    expected_log_density = -1.5 * tf.math.log1p(tf.square(points))
    tf.debugging.assert_near(log_density, expected_log_density)


def test_p85_lagrangep_author_config_has_33_basis_functions() -> None:
    spec = highdim.p85_author_sir_lagrangep_algebraic_product_basis_spec(
        convention=_reference_convention()
    )
    payload = spec.manifest_payload()

    assert spec.dimension == 36
    assert spec.basis_dim_tuple() == (33,) * 36
    assert payload["classification"] == "source_faithful"
    assert payload["classification_subtype"] == "sir_config"
    assert payload["basis_family"] == ("lagrangep",) * 36
    assert payload["domain_map_family"] == ("algebraic",) * 36
    assert "basis_family" in payload["xla_static_fields"]
    assert "no fitting evidence" in payload["nonclaims"]


def test_p85_lagrangep_nondefault_degree_comparator_is_extension() -> None:
    spec = highdim.p85_author_sir_lagrangep_algebraic_product_basis_spec(
        convention=_reference_convention(),
        order=3,
        num_elems=8,
    )
    payload = spec.manifest_payload()

    assert spec.dimension == 36
    assert spec.basis_dim_tuple() == (25,) * 36
    assert payload["classification"] == (
        highdim.P85_AUTHOR_SIR_DEGREE_COMPARATOR_CLASSIFICATION
    )
    assert payload["classification_subtype"] == (
        highdim.P85_AUTHOR_SIR_DEGREE_COMPARATOR_SUBTYPE
    )
    assert payload["basis_family"] == ("lagrangep",) * 36
    assert payload["domain_map_family"] == ("algebraic",) * 36
    assert "basis_family" in payload["xla_static_fields"]


def test_p85_lagrangep_nodes_use_author_jacobi11_interior_points() -> None:
    basis = highdim.LagrangePiecewiseBasis1D(highdim.AlgebraicMap(1.0), 4, 8)
    local_interior = tf.constant(
        [
            0.5 * (1.0 - (3.0 / 7.0) ** 0.5),
            0.5,
            0.5 * (1.0 + (3.0 / 7.0) ** 0.5),
        ],
        dtype=tf.float64,
    )
    expected_first_element = tf.concat(
        [
            tf.constant([-1.0], dtype=tf.float64),
            -1.0 + local_interior * 0.25,
            tf.constant([-0.75], dtype=tf.float64),
        ],
        axis=0,
    )

    tf.debugging.assert_near(basis.reference_nodes[:5], expected_first_element)


def test_p85_lagrangep_basis_interpolates_own_nodes() -> None:
    basis = highdim.LagrangePiecewiseBasis1D(highdim.AlgebraicMap(1.0), 4, 8)
    reference_nodes = basis.reference_nodes
    physical_nodes = basis.domain.from_reference(reference_nodes)
    values = basis.evaluate(physical_nodes)

    assert basis.basis_dim == 33
    tf.debugging.assert_near(values, tf.eye(33, dtype=tf.float64), atol=1e-8)


def test_p85_lagrangep_basis_has_piecewise_local_support() -> None:
    basis = highdim.LagrangePiecewiseBasis1D(highdim.AlgebraicMap(1.0), 4, 8)
    physical_point = basis.domain.from_reference(tf.constant([-0.9], dtype=tf.float64))
    values = basis.evaluate(physical_point)[0]

    tf.debugging.assert_near(values[5:], tf.zeros([28], dtype=tf.float64), atol=1e-12)
    assert float(tf.reduce_sum(tf.abs(values[:5])).numpy()) > 0.0


def test_p86_lagrangep_mass_and_integral_are_available_without_fit_claim() -> None:
    basis = highdim.LagrangePiecewiseBasis1D(highdim.AlgebraicMap(1.0), 4, 8)
    mass = basis.mass_matrix(highdim.MassMeasure.REFERENCE_MEASURE)
    integral = basis.integral_vector(highdim.MassMeasure.REFERENCE_MEASURE)

    assert mass.shape == (33, 33)
    assert integral.shape == (33,)
    tf.debugging.assert_near(mass, tf.transpose(mass), atol=1e-12)
    tf.debugging.assert_near(tf.reduce_sum(integral), tf.constant(1.0, dtype=tf.float64))


def test_p85_legacy_legendre_config_remains_local_gap() -> None:
    spec = highdim.p85_legacy_legendre_product_basis_spec(
        dimension=36,
        fit_degree=1,
        convention=_reference_convention(),
    )
    payload = spec.manifest_payload()

    assert payload["classification"] == "local_gap"
    assert payload["classification_subtype"] == "diagnostic_legendre_route"
    assert payload["basis_dim_tuple"] == (2,) * 36
    assert payload["basis_family"] == ("legendre",) * 36
    assert payload["domain_map_family"] == ("bounded_interval",) * 36


def test_p85_p59_manifest_distinguishes_legacy_and_author_configs() -> None:
    result = highdim.p59_author_sir_36d_target_fit_prep(sample_count=5)
    manifest = result.manifest

    legacy = manifest["basis_domain_config"]
    author = manifest["author_basis_domain_config_available"]

    assert result.status == highdim.P59_9A_PASS_STATUS
    assert legacy["classification"] == "local_gap"
    assert legacy["classification_subtype"] == "diagnostic_legendre_route"
    assert author["classification"] == "source_faithful"
    assert author["classification_subtype"] == "sir_config"
    assert author["basis_dim_tuple"] == (33,) * 36
    assert manifest["author_basis_domain_config_status"] == (
        highdim.P85_AUTHOR_SIR_BASIS_DOMAIN_CONFIG_STATUS
    )
    assert manifest["author_basis_domain_full_fit_status"] == (
        highdim.P85_AUTHOR_SIR_BASIS_DOMAIN_FULL_FIT_BLOCK_STATUS
    )
    assert "author Lagrangep(4,8) AlgebraicMapping(1) config is not fitted in P85" in manifest[
        "nonclaims"
    ]
    assert "no AlgebraicMapping(1) parity claim" in manifest["fit_data_manifest"]["nonclaims"]
