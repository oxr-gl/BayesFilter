from __future__ import annotations

import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64


def _convention() -> highdim.MeasureConvention:
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _product_basis(dimension: int) -> highdim.ProductBasis:
    return highdim.ProductBasis(
        [
            highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 0)
            for _ in range(dimension)
        ],
        _convention(),
    )


def _density(dimension: int) -> highdim.SquaredTTDensity:
    product = _product_basis(dimension)
    ftt = highdim.FunctionalTT(
        [highdim.TTCore(tf.constant([[[1.0]]], dtype=DTYPE)) for _ in range(dimension)],
        product,
        _convention(),
    )
    defensive = highdim.TensorProductReferenceDensity(product, _convention())
    branch_identity = highdim.SquaredTTDensity.expected_branch_identity(
        sqrt_tt=ftt,
        defensive_density=defensive,
        tau=tf.constant(0.0, dtype=DTYPE),
        normalizer_floor=tf.constant(1e-12, dtype=DTYPE),
        denominator_floor=tf.constant(1e-12, dtype=DTYPE),
        measure_convention=_convention(),
    )
    return highdim.SquaredTTDensity(
        sqrt_tt=ftt,
        defensive_density=defensive,
        tau=tf.constant(0.0, dtype=DTYPE),
        normalizer_floor=tf.constant(1e-12, dtype=DTYPE),
        denominator_floor=tf.constant(1e-12, dtype=DTYPE),
        measure_convention=_convention(),
        branch_identity=branch_identity,
    )


def _transport(dimension: int = 2) -> highdim.SourceRouteTransportProtocol:
    fixed = highdim.FixedTTSIRTTransport(
        density=_density(dimension),
        cdf_config=highdim.KRCDFConfig(
            grid_size=129,
            bisection_steps=28,
            monotonicity_tolerance=1e-12,
            bracket_tolerance=1e-12,
            denominator_floor=1e-12,
            max_floor_count=0,
        ),
    )
    return highdim.SourceRouteTransportProtocol(fixed)


def _target() -> highdim.SourceRouteTarget:
    frame = highdim.SourceRouteCoordinateFrame(
        mu=tf.constant([1.0, -0.25], dtype=DTYPE),
        matrix=tf.constant([[1.5, 0.0], [0.25, 1.25]], dtype=DTYPE),
        expansion_factor=1.0,
    )

    def negative_log_physical(points: tf.Tensor) -> tf.Tensor:
        centered = points - tf.constant([[0.5], [0.25]], dtype=DTYPE)
        return 0.5 * tf.reduce_sum(tf.square(centered), axis=0) + 0.1

    return highdim.build_source_route_target(
        negative_log_physical_density_fn=negative_log_physical,
        coordinate_frame=frame,
        shift_constant=tf.constant(0.2, dtype=DTYPE),
        time_index=1,
    )


def test_p57_m5_retained_weights_match_author_fun_post_over_eval_pdf_identity() -> None:
    target = _target()
    transport = _transport()
    reference = tf.constant([[0.2, 0.5, 0.8], [0.1, 0.75, 0.4]], dtype=DTYPE)

    result = highdim.source_route_generate_retained_samples(
        target=target,
        transport=transport,
        reference_samples=reference,
        time_index=1,
    )

    local = transport.inverse_transport(reference)
    physical = target.physical_points_from_reference(local)
    negative_log_physical = target.negative_log_physical_density_fn(physical)
    author_fun_post = (
        negative_log_physical
        - target.coordinate_frame.log_abs_det()
        - target.shift_constant
    )
    expected_proposal = tf.math.log(transport.eval_pdf(local))
    expected_correction = -author_fun_post - expected_proposal

    tf.debugging.assert_near(result.retained_batch.samples, physical)
    tf.debugging.assert_near(result.proposal_log_density, expected_proposal)
    tf.debugging.assert_near(result.target_log_density, -author_fun_post)
    tf.debugging.assert_near(result.correction_log_weights, expected_correction)
    tf.debugging.assert_near(
        result.retained_batch.log_weights,
        highdim.normalize_log_weights(expected_correction),
    )


def test_p57_m5_proposal_denominator_is_not_base_uniform_density() -> None:
    target = _target()
    transport = _transport()
    reference = tf.constant([[0.2, 0.8], [0.25, 0.75]], dtype=DTYPE)
    local = transport.inverse_transport(reference)

    result = highdim.source_route_generate_retained_samples(
        target=target,
        transport=transport,
        reference_samples=reference,
        time_index=1,
    )

    base_uniform_log_density = tf.zeros([2], dtype=DTYPE)
    source_eval_pdf_log_density = tf.math.log(transport.eval_pdf(local))

    tf.debugging.assert_near(result.proposal_log_density, source_eval_pdf_log_density)
    assert bool(tf.reduce_any(tf.abs(result.proposal_log_density - base_uniform_log_density) > 1e-6).numpy())


def test_p57_m5_retained_manifest_records_source_route_and_ess() -> None:
    result = highdim.source_route_generate_retained_samples(
        target=_target(),
        transport=_transport(),
        reference_samples=tf.constant([[0.3, 0.6, 0.9], [0.2, 0.4, 0.8]], dtype=DTYPE),
        time_index=1,
    )
    payload = result.manifest_payload()

    assert payload["retained_batch"]["route_label"] == highdim.SOURCE_FAITHFUL_ROUTE_LABEL
    assert payload["retained_batch"]["sample_origin"] == "retained_from_transport"
    assert result.diagnostics.sample_count == 3
    assert bool((result.diagnostics.effective_sample_size > 0.0).numpy())
