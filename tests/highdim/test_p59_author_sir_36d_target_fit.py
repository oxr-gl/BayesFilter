from __future__ import annotations

import tensorflow as tf

import bayesfilter.highdim as highdim


def test_p59_9a_author_sir_bounded_fit_uses_36d_source_target() -> None:
    result = highdim.p59_author_sir_36d_target_fit_prep(sample_count=6)

    assert result.status == highdim.P59_9A_PASS_STATUS
    assert result.target_dimension == highdim.P59_9A_AUTHOR_SIR_TARGET_DIMENSION
    assert result.target_dimension == result.parameter_dimension + 2 * result.state_dimension
    assert result.parameter_dimension == 0
    assert result.state_dimension == 18
    assert result.sample_count == 6
    assert result.fit_status == highdim.HighDimStatus.OK.value
    assert result.fit_branch_hash is not None
    assert result.density_branch_hash is not None
    tf.debugging.assert_equal(
        tf.reduce_all(tf.math.is_finite(result.negative_log_values)),
        True,
    )


def test_p59_9a_manifest_marks_bounded_prep_not_validation() -> None:
    result = highdim.p59_author_sir_36d_target_fit_prep(sample_count=5)
    payload = result.manifest_payload()
    manifest = payload["manifest"]

    assert manifest["target_id"] == highdim.P58_M9_AUTHOR_SIR_TARGET_ID
    assert manifest["pipeline_phase"] == "P59-9a"
    assert manifest["artifact_role"] == "bounded_preparation_evidence_only"
    assert manifest["source_target_order"] == "[theta, x_t, x_{t-1}]"
    assert manifest["fit_data_mode"] == highdim.P63_AUTHOR_SIR_SOURCE_FIT_DATA_MODE
    assert (
        manifest["fit_data_manifest"]["coordinate_frame_source"]
        == "source_computeL_weighted_augmented_samples"
    )
    assert (
        manifest["fit_data_manifest"]["fixed_variant_resampling"]
        == highdim.P63_AUTHOR_SIR_FIXED_VARIANT_RESAMPLING
    )
    assert manifest["author_sir_d_plus_2m_dimension_check"] is True
    assert manifest["transport_dimension"] == 36
    assert "no AlgebraicMapping(1) parity claim" in manifest["fit_data_manifest"]["nonclaims"]
    assert "no d18 filtering accuracy claim" in manifest["nonclaims"]
    assert "no Phase-9 validation launch" in manifest["nonclaims"]


def test_p59_9a_transport_manifest_is_fixed_ttsirt_not_contract_double() -> None:
    result = highdim.p59_author_sir_36d_target_fit_prep(sample_count=4)
    transport = result.transport_manifest

    assert transport is not None
    assert transport["family"] == "FixedTTSIRTTransport"
    assert transport["source_contract_level"] == "fixed_ttsirt"
    assert transport["tt_cores_declared"] is True
    assert transport["defensive_density_declared"] is True
    assert transport["defensive_mass_positive"] is True
    assert transport["defensive_tau"] == highdim.P62_AUTHOR_TTSIRT_EXECUTABLE_DEFAULT_TAU
    assert transport["defensive_tau_source"] == "author_executable_ttsirt_default"
    assert result.manifest["source_declared_tau_unwired"] == 10.0
    assert (
        result.manifest["source_executable_ttsirt_default_tau"]
        == highdim.P62_AUTHOR_TTSIRT_EXECUTABLE_DEFAULT_TAU
    )


def test_p59_9a_blocks_invalid_sample_count_without_launching_validation() -> None:
    result = highdim.p59_author_sir_36d_target_fit_prep(sample_count=1)

    assert result.status == highdim.P59_9A_BLOCK_STATUS
    assert "sample_count_must_be_at_least_2" in result.blockers
    assert result.fit_status == "not_attempted"
    assert result.transport_manifest is None
    assert "no Phase-9 validation launch" in result.manifest["nonclaims"]
