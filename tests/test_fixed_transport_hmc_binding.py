from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

from bayesfilter.inference import (
    FIXED_TRANSPORT_HMC_BINDING_NONCLAIMS,
    HMCTuningPolicy,
    InvalidFixedTransportHMCBinding,
    ValueScoreCapability,
    bind_fixed_transport_hmc_mechanics,
    load_frozen_neutra_artifact,
    stable_fixed_transport_hmc_manifest_signature,
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
            evidence_path="tests/test_fixed_transport_hmc_binding.py",
            target_scope="fixed_transport_hmc_fixture",
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
            target_scope="fixed_transport_hmc_fixture",
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


def _artifact():
    return load_frozen_neutra_artifact(
        _payload(),
        expected_target_signature=_target_signature(),
    )


def test_fixed_transport_hmc_mechanics_manifest_and_value_score() -> None:
    artifact = _artifact()
    initial = tf.constant([[0.1, -0.2, 0.3]], dtype=tf.float64)

    result = bind_fixed_transport_hmc_mechanics(
        base_adapter=BatchedQuadraticAdapter(),
        loaded_artifact=artifact,
        initial_position=initial,
        target_scope="fixed_transport_hmc_fixture",
        tuning_policy=HMCTuningPolicy.fixed_kernel_screen(),
        use_xla=False,
        seed=123,
        execution_device="cpu",
    )

    assert result.value.shape == (1,)
    assert result.score.shape == (1, 3)
    assert bool(tf.reduce_all(tf.math.is_finite(result.value)).numpy()) is True
    assert bool(tf.reduce_all(tf.math.is_finite(result.score)).numpy()) is True
    assert result.manifest.target_signature == _target_signature()
    assert result.manifest.transport_hash == artifact.binding.transport_manifest["transport_hash"]
    assert result.manifest.hmc_policy_label == "fixed_kernel_screen"
    assert result.manifest.hmc_policy_hash
    assert result.manifest.execution_device == "cpu"
    assert result.manifest.mechanics_only is True
    assert result.manifest.seed == 123
    assert result.diagnostics["mechanics_only"] is True
    assert "no serious HMC convergence claim" in result.manifest.nonclaims
    assert "no default HMC policy change" in FIXED_TRANSPORT_HMC_BINDING_NONCLAIMS


def test_fixed_transport_hmc_manifest_signature_is_stable_and_changes_with_policy() -> None:
    artifact = _artifact()
    initial = tf.constant([[0.1, -0.2, 0.3]], dtype=tf.float64)
    first = bind_fixed_transport_hmc_mechanics(
        base_adapter=BatchedQuadraticAdapter(),
        loaded_artifact=artifact,
        initial_position=initial,
        target_scope="fixed_transport_hmc_fixture",
        tuning_policy=HMCTuningPolicy.fixed_kernel_screen(),
        use_xla=False,
    )
    same = bind_fixed_transport_hmc_mechanics(
        base_adapter=BatchedQuadraticAdapter(),
        loaded_artifact=artifact,
        initial_position=initial,
        target_scope="fixed_transport_hmc_fixture",
        tuning_policy=HMCTuningPolicy.fixed_kernel_screen(),
        use_xla=False,
    )
    changed = bind_fixed_transport_hmc_mechanics(
        base_adapter=BatchedQuadraticAdapter(),
        loaded_artifact=artifact,
        initial_position=initial,
        target_scope="fixed_transport_hmc_fixture",
        tuning_policy=HMCTuningPolicy.dual_averaging_step_size(
            num_adaptation_steps=2,
            target_accept_prob=0.75,
            source="tests/test_fixed_transport_hmc_binding.py",
        ),
        use_xla=False,
    )

    assert stable_fixed_transport_hmc_manifest_signature(first.manifest) == (
        stable_fixed_transport_hmc_manifest_signature(same.manifest)
    )
    assert stable_fixed_transport_hmc_manifest_signature(first.manifest) != (
        stable_fixed_transport_hmc_manifest_signature(changed.manifest)
    )


def test_fixed_transport_hmc_binding_rejects_fallback_authority_for_xla() -> None:
    with pytest.raises(InvalidFixedTransportHMCBinding, match="accepted value/score"):
        bind_fixed_transport_hmc_mechanics(
            base_adapter=FallbackBatchedQuadraticAdapter(),
            loaded_artifact=_artifact(),
            initial_position=tf.constant([[0.1, -0.2, 0.3]], dtype=tf.float64),
            target_scope="fixed_transport_hmc_fixture",
            use_xla=True,
        )


def test_fixed_transport_hmc_binding_allows_fallback_authority_for_non_xla_mechanics_only() -> None:
    result = bind_fixed_transport_hmc_mechanics(
        base_adapter=FallbackBatchedQuadraticAdapter(),
        loaded_artifact=_artifact(),
        initial_position=tf.constant([[0.1, -0.2, 0.3]], dtype=tf.float64),
        target_scope="fixed_transport_hmc_fixture",
        use_xla=False,
    )

    assert result.manifest.use_xla is False
    assert result.manifest.xla_hmc_ready is False
    assert result.manifest.mechanics_only is True


def test_fixed_transport_hmc_binding_rejects_scalar_initial_position_and_bad_seed() -> None:
    with pytest.raises(ValueError, match=r"\[B, D\]"):
        bind_fixed_transport_hmc_mechanics(
            base_adapter=BatchedQuadraticAdapter(),
            loaded_artifact=_artifact(),
            initial_position=tf.constant([0.1, -0.2, 0.3], dtype=tf.float64),
            target_scope="fixed_transport_hmc_fixture",
        )

    with pytest.raises(InvalidFixedTransportHMCBinding, match="seed"):
        bind_fixed_transport_hmc_mechanics(
            base_adapter=BatchedQuadraticAdapter(),
            loaded_artifact=_artifact(),
            initial_position=tf.constant([[0.1, -0.2, 0.3]], dtype=tf.float64),
            target_scope="fixed_transport_hmc_fixture",
            seed=-1,
        )


def test_fixed_transport_hmc_mechanics_matches_fixed_transport_chain_rule() -> None:
    artifact = _artifact()
    initial = tf.constant([[0.1, -0.2, 0.3]], dtype=tf.float64)
    result = bind_fixed_transport_hmc_mechanics(
        base_adapter=BatchedQuadraticAdapter(),
        loaded_artifact=artifact,
        initial_position=initial,
        target_scope="fixed_transport_hmc_fixture",
    )
    u = artifact.transport.forward_batch(initial).numpy()
    scale = artifact.transport.scale.numpy()
    expected_value = -0.5 * np.sum(u * u, axis=-1) + np.sum(
        artifact.transport.raw_scale.numpy()
    )
    expected_score = (-u) * scale

    np.testing.assert_allclose(result.value.numpy(), expected_value)
    np.testing.assert_allclose(result.score.numpy(), expected_score)
