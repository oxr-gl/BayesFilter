from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

from bayesfilter.inference import (
    FixedTransportValueScoreAdapter,
    InvalidNeuTraArtifact,
    ValueScoreCapability,
    load_frozen_neutra_artifact,
    stable_frozen_neutra_artifact_signature,
)
from bayesfilter.ssm import (
    BayesianSSMProblem,
    FilterProgram,
    ParameterChart,
    ParameterPrior,
    SSMDataSignature,
    SSMStaticShape,
    SSMTargetContract,
    stable_ssm_target_signature,
)


class BatchedQuadraticAdapter:
    parameter_dim = 3

    def value_score_capability(self) -> ValueScoreCapability:
        return ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=True,
            runtime_backend="tensorflow_batched_quadratic_fixture",
            evidence_path="tests/test_neutra_artifact_loader.py",
            target_scope="artifact_loader_quadratic_fixture",
            nonclaims=("target value/score fixture only",),
        )

    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        values = tf.convert_to_tensor(theta, dtype=tf.float64)
        return -0.5 * tf.reduce_sum(tf.square(values), axis=-1), -values


class FallbackBatchedQuadraticAdapter(BatchedQuadraticAdapter):
    def value_score_capability(self) -> ValueScoreCapability:
        return ValueScoreCapability(
            value_score_authority="gradient_tape_fallback",
            xla_hmc_ready=False,
            runtime_backend="fallback_fixture",
            target_scope="artifact_loader_fallback_fixture",
            nonclaims=("fallback fixture only",),
        )


def _target_signature() -> str:
    problem = BayesianSSMProblem(
        problem_id="toy-nonlinear-ssm",
        static_shape=SSMStaticShape(
            horizon=4,
            state_dim=2,
            observation_dim=1,
            innovation_dim=1,
            parameter_dim=3,
        ),
        data_signature=SSMDataSignature(
            dataset_id="toy-nonlinear-data",
            observation_shape=(4, 1),
            data_hash="sha256:data-v1",
        ),
        target_coordinate_convention="unconstrained",
        model_manifest={
            "model_id": "toy-nonlinear-model",
            "model_hash": "sha256:model-v1",
            "capabilities": ("transition_mean", "observation_mean"),
        },
    )
    chart = ParameterChart(
        parameter_names=("rho", "sigma", "beta"),
        unconstrained_dim=3,
        constrained_shape=(3,),
        transform_manifest={
            "transform_id": "identity-chart",
            "transform_hash": "sha256:chart-v1",
        },
        log_jacobian_convention="not_included",
    )
    prior = ParameterPrior(
        prior_manifest={
            "prior_id": "toy-gaussian-prior",
            "prior_hash": "sha256:prior-v1",
        },
        support_policy="unbounded",
        log_density_authority="graph_native",
    )
    filter_program = FilterProgram(
        filter_id="toy-deterministic-filter",
        required_model_capabilities=("transition_mean", "observation_mean"),
        deterministic_target_policy="deterministic",
        approximation_semantics="deterministic_approximation",
        filter_manifest={
            "filter_id": "toy-deterministic-filter",
            "filter_hash": "sha256:filter-v1",
        },
    )
    return stable_ssm_target_signature(
        SSMTargetContract(
            problem=problem,
            chart=chart,
            prior=prior,
            filter_program=filter_program,
        )
    )


def _payload(**overrides):
    values = {
        "schema": "bayesfilter.neutra.frozen_affine_diag.v1",
        "transport_id": "toy-neutra-transport",
        "dimension": 3,
        "target_signature": _target_signature(),
        "log_jacobian_available": True,
        "shift": (0.25, -0.5, 0.75),
        "raw_scale": (0.0, np.log(1.5), np.log(0.75)),
        "training_state_hash": "sha256:synthetic-training-state",
    }
    values.update(overrides)
    return values


def test_frozen_neutra_loader_accepts_synthetic_artifact_and_binding() -> None:
    artifact = load_frozen_neutra_artifact(
        _payload(),
        expected_target_signature=_target_signature(),
    )

    assert artifact.manifest.dimension == 3
    assert artifact.binding.target_signature == _target_signature()
    assert artifact.binding.log_jacobian_available is True
    assert artifact.transport.parameter_dim == 3
    assert stable_frozen_neutra_artifact_signature(artifact) == artifact.artifact_signature
    assert "no NeuTra training claim" in artifact.manifest.nonclaims


def test_frozen_neutra_loader_forward_and_logdet_roundtrip() -> None:
    artifact = load_frozen_neutra_artifact(
        _payload(),
        expected_target_signature=_target_signature(),
    )
    z = tf.constant([[0.1, -0.2, 0.3], [0.4, 0.0, -0.1]], dtype=tf.float64)
    u = artifact.transport.forward_batch(z)
    logdet = artifact.transport.log_abs_det_jacobian_batch(z)
    expected_scale = np.exp(np.array([0.0, np.log(1.5), np.log(0.75)]))
    expected_u = np.array([0.25, -0.5, 0.75]) + z.numpy() * expected_scale

    np.testing.assert_allclose(u.numpy(), expected_u)
    np.testing.assert_allclose(
        logdet.numpy(),
        np.repeat(np.sum(np.log(expected_scale)), 2),
    )


def test_frozen_neutra_loader_rejects_schema_dimension_target_and_logdet_failures() -> None:
    cases = [
        ({"schema": "unsupported"}, "unsupported"),
        ({"dimension": 0}, "dimension"),
        ({"target_signature": "wrong"}, "target_signature mismatch"),
        ({"log_jacobian_available": False}, "log_jacobian_available"),
        ({"shift": (1.0, 2.0)}, "shift length"),
        ({"raw_scale": (1.0, 2.0)}, "raw_scale length"),
    ]

    for override, pattern in cases:
        with pytest.raises(InvalidNeuTraArtifact, match=pattern):
            load_frozen_neutra_artifact(
                _payload(**override),
                expected_target_signature=_target_signature(),
            )


def test_frozen_neutra_loader_rejects_process_local_identity() -> None:
    with pytest.raises(InvalidNeuTraArtifact, match="process-local"):
        load_frozen_neutra_artifact(
            _payload(transport_id=f"object at 0x{id(object()):x}"),
            expected_target_signature=_target_signature(),
        )


def test_frozen_neutra_loader_is_compatible_with_fixed_transport_adapter() -> None:
    artifact = load_frozen_neutra_artifact(
        _payload(),
        expected_target_signature=_target_signature(),
    )
    adapter = FixedTransportValueScoreAdapter(
        base_adapter=BatchedQuadraticAdapter(),
        transport=artifact.transport,
        target_scope="artifact_loader_fixed_transport_fixture",
        xla_hmc_ready=True,
    )
    z = tf.constant([[0.1, -0.2, 0.3], [0.4, 0.0, -0.1]], dtype=tf.float64)
    value, score = adapter.log_prob_and_grad(z)

    assert value.shape == (2,)
    assert score.shape == (2, 3)
    assert adapter.value_score_capability().value_score_authority == "graph_native"
    assert adapter.value_score_capability().xla_hmc_ready is True


def test_frozen_neutra_loader_does_not_promote_fallback_base_authority() -> None:
    artifact = load_frozen_neutra_artifact(
        _payload(),
        expected_target_signature=_target_signature(),
    )
    adapter = FixedTransportValueScoreAdapter(
        base_adapter=FallbackBatchedQuadraticAdapter(),
        transport=artifact.transport,
        target_scope="artifact_loader_fixed_transport_fallback_fixture",
        xla_hmc_ready=True,
        full_chain_xla_diagnostic_ready=True,
    )
    capability = adapter.value_score_capability()

    assert capability.value_score_authority == "gradient_tape_fallback"
    assert capability.xla_hmc_ready is False
    assert capability.full_chain_xla_diagnostic_ready is False
    assert any(
        "fixed transport wrapper cannot promote fallback base authority" in claim
        for claim in capability.nonclaims
    )
