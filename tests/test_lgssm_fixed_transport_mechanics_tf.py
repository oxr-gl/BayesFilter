from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

from bayesfilter.inference import (
    FixedTransportValueScoreAdapter,
    HMCTuningPolicy,
    InvalidNeuTraArtifact,
    bind_fixed_transport_hmc_mechanics,
    load_frozen_neutra_artifact,
    stable_fixed_transport_hmc_manifest_signature,
    stable_frozen_neutra_artifact_signature,
)
from bayesfilter.ssm import stable_ssm_target_signature
from bayesfilter.testing.lgssm_generic_target_adapter_tf import (
    make_lgssm_generic_target_fixture,
)


def _payload(target_signature: str, **overrides):
    values = {
        "schema": "bayesfilter.neutra.frozen_affine_diag.v1",
        "transport_id": "lgssm-fixed-affine-transport",
        "dimension": 2,
        "target_signature": target_signature,
        "log_jacobian_available": True,
        "shift": (0.20, -1.05),
        "raw_scale": (0.0, 0.0),
        "training_state_hash": "sha256:synthetic-lgssm-fixed-transport",
    }
    values.update(overrides)
    return values


def _fixture_and_artifact(**payload_overrides):
    fixture = make_lgssm_generic_target_fixture()
    target_signature = stable_ssm_target_signature(fixture.contract)
    artifact = load_frozen_neutra_artifact(
        _payload(target_signature, **payload_overrides),
        expected_target_signature=target_signature,
    )
    return fixture, artifact


def test_lgssm_identity_transport_matches_base_target_shifted_coordinates() -> None:
    fixture, artifact = _fixture_and_artifact()
    adapter = FixedTransportValueScoreAdapter(
        base_adapter=fixture.adapter,
        transport=artifact.transport,
        target_scope="lgssm-fixed-transport-mechanics-fixture",
        xla_hmc_ready=False,
    )
    z = tf.constant([[0.0, 0.0], [0.10, -0.05]], dtype=tf.float64)

    value, score = adapter.log_prob_and_grad(z)
    theta = artifact.transport.forward_batch(z)
    base_value, base_score = fixture.adapter.log_prob_and_grad(theta)

    tf.debugging.assert_near(value, base_value)
    tf.debugging.assert_near(score, base_score)
    assert adapter.value_score_capability().xla_hmc_ready is False
    assert "no NeuTra training claim" in artifact.manifest.nonclaims


def test_lgssm_affine_transport_matches_chain_rule_and_logdet() -> None:
    fixture, artifact = _fixture_and_artifact(
        shift=(0.05, -1.20),
        raw_scale=(np.log(1.25), np.log(0.70)),
        training_state_hash="sha256:synthetic-lgssm-affine-transport",
    )
    adapter = FixedTransportValueScoreAdapter(
        base_adapter=fixture.adapter,
        transport=artifact.transport,
        target_scope="lgssm-fixed-affine-transport-mechanics-fixture",
        xla_hmc_ready=False,
    )
    z = tf.constant([[0.20, -0.10], [-0.15, 0.05]], dtype=tf.float64)

    value, score = adapter.log_prob_and_grad(z)
    theta = artifact.transport.forward_batch(z)
    base_value, base_score = fixture.adapter.log_prob_and_grad(theta)
    scale = artifact.transport.scale
    expected_value = base_value + tf.reduce_sum(artifact.transport.raw_scale)
    expected_score = base_score * scale

    tf.debugging.assert_near(value, expected_value)
    tf.debugging.assert_near(score, expected_score)


def test_lgssm_fixed_transport_rejects_target_signature_mismatch() -> None:
    fixture = make_lgssm_generic_target_fixture()
    target_signature = stable_ssm_target_signature(fixture.contract)

    with pytest.raises(InvalidNeuTraArtifact, match="target_signature mismatch"):
        load_frozen_neutra_artifact(
            _payload("0" * 64),
            expected_target_signature=target_signature,
        )


def test_lgssm_fixed_transport_hmc_mechanics_manifest_is_stable_and_finite() -> None:
    fixture, artifact = _fixture_and_artifact(
        shift=(0.05, -1.20),
        raw_scale=(np.log(1.10), np.log(0.90)),
        training_state_hash="sha256:synthetic-lgssm-hmc-mechanics-transport",
    )
    initial = tf.constant([[0.10, -0.05]], dtype=tf.float64)

    result = bind_fixed_transport_hmc_mechanics(
        base_adapter=fixture.adapter,
        loaded_artifact=artifact,
        initial_position=initial,
        target_scope="lgssm-fixed-transport-hmc-mechanics-fixture",
        tuning_policy=HMCTuningPolicy.fixed_kernel_screen(),
        use_xla=False,
        seed=20260706,
        execution_device="cpu",
    )
    same = bind_fixed_transport_hmc_mechanics(
        base_adapter=fixture.adapter,
        loaded_artifact=artifact,
        initial_position=initial,
        target_scope="lgssm-fixed-transport-hmc-mechanics-fixture",
        tuning_policy=HMCTuningPolicy.fixed_kernel_screen(),
        use_xla=False,
        seed=20260706,
        execution_device="cpu",
    )

    assert result.value.shape == (1,)
    assert result.score.shape == (1, 2)
    assert bool(tf.reduce_all(tf.math.is_finite(result.value)).numpy()) is True
    assert bool(tf.reduce_all(tf.math.is_finite(result.score)).numpy()) is True
    assert result.manifest.target_signature == stable_ssm_target_signature(fixture.contract)
    assert result.manifest.mechanics_only is True
    assert result.manifest.execution_device == "cpu"
    assert result.manifest.use_xla is False
    assert stable_frozen_neutra_artifact_signature(artifact) == artifact.artifact_signature
    assert stable_fixed_transport_hmc_manifest_signature(result.manifest) == (
        stable_fixed_transport_hmc_manifest_signature(same.manifest)
    )
