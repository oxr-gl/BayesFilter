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


def _filter_config(seed: str = "p50-m2-one-step") -> highdim.FixedBranchFilterConfig:
    return highdim.FixedBranchFilterConfig(
        fit_config=None,
        density_tau=0.0,
        normalizer_floor=1e-12,
        denominator_floor=1e-12,
        retained_storage_byte_budget=10_000_000,
        coordinate_maps=(highdim.IdentityCoordinateMap(1),),
        measure_convention=_convention(),
        deterministic_seed=seed,
    )


def _scalar_lgssm() -> highdim.LinearGaussianSSM:
    return highdim.LinearGaussianSSM(
        initial_mean=tf.constant([0.0], dtype=DTYPE),
        initial_covariance=tf.constant([[1.0]], dtype=DTYPE),
        transition_matrix=tf.constant([[0.7]], dtype=DTYPE),
        transition_covariance=tf.constant([[0.25]], dtype=DTYPE),
        observation_matrix=tf.constant([[1.0]], dtype=DTYPE),
        observation_covariance=tf.constant([[0.09]], dtype=DTYPE),
    )


def test_p50_one_step_lgssm_value_path_matches_exact_kalman_increment() -> None:
    result = highdim.FixedBranchSquaredTTFilter(_filter_config()).log_likelihood(
        _scalar_lgssm(),
        tf.zeros([0], dtype=DTYPE),
        tf.constant([0.2], dtype=DTYPE),
    )

    assert result.status is highdim.HighDimStatus.OK
    assert len(result.steps) == 1
    step = result.steps[0]
    tf.debugging.assert_near(
        result.log_likelihood,
        tf.constant(-0.980376005178410, dtype=DTYPE),
        atol=2e-10,
    )
    tf.debugging.assert_near(result.log_likelihood, step.log_normalizer)
    tf.debugging.assert_near(step.retained_filter.normalizer, tf.exp(step.log_normalizer))
    assert result.log_likelihood.dtype == DTYPE
    assert step.log_normalizer.shape.rank == 0
    assert result.branch_identity.manifest.payload["scope"] == "phase4_exact_small_model_value_path"
    assert "derivative_correctness" in result.branch_identity.manifest.payload["what_is_not_claimed"]


def test_p50_one_step_branch_identity_replays_without_hidden_randomness() -> None:
    runner = highdim.FixedBranchSquaredTTFilter(_filter_config(seed="p50-m2-replay"))
    observation = tf.constant([0.2], dtype=DTYPE)

    first = runner.log_likelihood(_scalar_lgssm(), tf.zeros([0], dtype=DTYPE), observation)
    second = runner.log_likelihood(_scalar_lgssm(), tf.zeros([0], dtype=DTYPE), observation)

    assert first.branch_identity.hash.value == second.branch_identity.hash.value
    assert first.steps[0].branch_identity.hash.value == second.steps[0].branch_identity.hash.value
    assert (
        first.retained_filter.branch_identity.hash.value
        == second.retained_filter.branch_identity.hash.value
    )
    tf.debugging.assert_equal(first.log_likelihood, second.log_likelihood)


def test_p50_one_step_accounting_contract_jacobian_shift_and_proposal_terms() -> None:
    frame = highdim.SourceRouteCoordinateFrame(
        mu=tf.constant([0.0], dtype=DTYPE),
        matrix=tf.constant([[2.0]], dtype=DTYPE),
        expansion_factor=1.0,
    )
    log_physical = tf.math.log(tf.constant([0.25, 0.75], dtype=DTYPE))
    log_reference = highdim.source_route_reference_log_density_from_physical(
        log_physical_density=log_physical,
        coordinate_frame=frame,
    )
    tf.debugging.assert_near(log_reference, log_physical + tf.math.log(tf.constant(2.0, dtype=DTYPE)))

    negative_log_target = -log_reference
    shift = tf.reduce_min(negative_log_target)
    shifted = highdim.source_route_shifted_negative_log_target(
        negative_log_target=negative_log_target,
        shift_constant=shift,
    )
    shifted_log_normalizer = tf.reduce_logsumexp(-shifted)
    tf.debugging.assert_near(
        highdim.source_route_log_normalizer_update(
            log_transport_normalizer=shifted_log_normalizer,
            shift_constant=shift,
        ),
        tf.reduce_logsumexp(log_reference),
    )

    log_proposal = tf.math.log(tf.constant([0.5, 0.5], dtype=DTYPE))
    correction = highdim.source_route_proposal_log_weights(
        log_target_density=log_reference,
        log_proposal_density=log_proposal,
    )
    tf.debugging.assert_near(correction, log_reference - log_proposal)
    tf.debugging.assert_near(
        highdim.source_route_discrete_log_normalizer_from_correction(
            log_proposal_density=log_proposal,
            correction_log_weights=correction,
        ),
        tf.reduce_logsumexp(log_reference),
    )
