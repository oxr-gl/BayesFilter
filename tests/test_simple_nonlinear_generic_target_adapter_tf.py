from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

from bayesfilter.inference import evaluate_batch_native_value_score
from bayesfilter.ssm import (
    stable_ssm_posterior_adapter_signature,
    stable_ssm_target_signature,
)
from bayesfilter.testing.simple_nonlinear_generic_target_adapter_tf import (
    MODEL_B_INITIAL_BATCH,
    SIMPLE_NONLINEAR_GENERIC_TARGET_NONCLAIMS,
    make_simple_nonlinear_generic_target_contract,
    make_simple_nonlinear_generic_target_fixture,
    simple_nonlinear_filter_diagnostics,
    simple_nonlinear_gaussian_prior_log_prob_and_grad,
    simple_nonlinear_svd_ukf_log_likelihood_and_grad,
)


def _theta_batch() -> tf.Tensor:
    return tf.constant(
        [
            [0.68, 0.24, 0.78],
            [0.70, 0.25, 0.80],
        ],
        dtype=tf.float64,
    )


def test_simple_nonlinear_contract_is_stable_deterministic_and_untransported() -> None:
    left = make_simple_nonlinear_generic_target_contract()
    right = make_simple_nonlinear_generic_target_contract()
    changed = make_simple_nonlinear_generic_target_contract(
        filter_hash="sha256:changed-filter",
    )

    assert left.problem.static_shape.manifest_payload() == {
        "horizon": 3,
        "state_dim": 2,
        "observation_dim": 1,
        "innovation_dim": 1,
        "parameter_dim": 3,
    }
    assert left.problem.problem_id == "model-b-nonlinear-accumulation-generic-target-fixture"
    assert left.filter_program.approximation_semantics == "deterministic_approximation"
    assert left.filter_program.deterministic_target_policy == "deterministic"
    assert left.frozen_transport is None
    assert stable_ssm_target_signature(left) == stable_ssm_target_signature(right)
    assert stable_ssm_target_signature(left) != stable_ssm_target_signature(changed)


def test_simple_nonlinear_adapter_emits_finite_batch_values_scores() -> None:
    fixture = make_simple_nonlinear_generic_target_fixture()
    theta = _theta_batch()

    value, score = fixture.adapter.log_prob_and_grad(theta)
    result = evaluate_batch_native_value_score(fixture.adapter, theta, dtype=tf.float64)

    assert value.shape == (2,)
    assert score.shape == (2, 3)
    assert result.metadata.rank == "batch"
    assert result.metadata.parameter_dim == 3
    assert tf.reduce_all(tf.math.is_finite(value))
    assert tf.reduce_all(tf.math.is_finite(score))
    assert fixture.adapter.metadata().batch_rank_policy == "rank2_required"
    assert fixture.adapter.metadata().nonclaims == SIMPLE_NONLINEAR_GENERIC_TARGET_NONCLAIMS
    assert fixture.adapter.value_score_capability().xla_hmc_ready is False


def test_simple_nonlinear_adapter_matches_prior_plus_svd_ukf_likelihood() -> None:
    fixture = make_simple_nonlinear_generic_target_fixture()
    theta = _theta_batch()

    value, score = fixture.adapter.log_prob_and_grad(theta)
    prior_value, prior_score = simple_nonlinear_gaussian_prior_log_prob_and_grad(theta)
    likelihood_value, likelihood_score = simple_nonlinear_svd_ukf_log_likelihood_and_grad(theta)

    tf.debugging.assert_near(value, prior_value + likelihood_value)
    tf.debugging.assert_near(score, prior_score + likelihood_score)


def test_simple_nonlinear_initial_batch_is_finite_and_residual_free() -> None:
    fixture = make_simple_nonlinear_generic_target_fixture()

    value, score = fixture.adapter.log_prob_and_grad(MODEL_B_INITIAL_BATCH)
    diagnostics = simple_nonlinear_filter_diagnostics(MODEL_B_INITIAL_BATCH)

    assert value.shape == (1,)
    assert score.shape == (1, 3)
    assert np.isfinite(value.numpy()).all()
    assert np.isfinite(score.numpy()).all()
    np.testing.assert_allclose(
        diagnostics["deterministic_residual"].numpy(),
        np.zeros([1]),
        atol=1.0e-12,
    )


def test_simple_nonlinear_adapter_rejects_rank1_position() -> None:
    fixture = make_simple_nonlinear_generic_target_fixture()

    with pytest.raises(ValueError, match="rank 2 theta"):
        fixture.adapter.log_prob_and_grad(
            tf.constant([0.70, 0.25, 0.80], dtype=tf.float64)
        )


def test_simple_nonlinear_adapter_signature_and_manifest_are_stable() -> None:
    fixture = make_simple_nonlinear_generic_target_fixture()
    same = make_simple_nonlinear_generic_target_fixture()
    changed_contract = make_simple_nonlinear_generic_target_contract(
        prior_hash="sha256:changed-prior",
    )
    changed_fixture = type(fixture.adapter)(
        contract=changed_contract,
        prior_log_prob_and_grad=simple_nonlinear_gaussian_prior_log_prob_and_grad,
        filter_log_likelihood_and_grad=simple_nonlinear_svd_ukf_log_likelihood_and_grad,
        dtype=tf.float64,
        target_scope="model-b-nonlinear-accumulation-generic-target-fixture",
        evidence_path="bayesfilter/testing/simple_nonlinear_generic_target_adapter_tf.py",
        nonclaims=SIMPLE_NONLINEAR_GENERIC_TARGET_NONCLAIMS,
    )

    assert fixture.adapter.manifest_payload()["target_signature"] == stable_ssm_target_signature(
        fixture.contract
    )
    assert stable_ssm_posterior_adapter_signature(
        fixture.adapter
    ) == stable_ssm_posterior_adapter_signature(same.adapter)
    assert stable_ssm_posterior_adapter_signature(
        fixture.adapter
    ) != stable_ssm_posterior_adapter_signature(changed_fixture)


def test_simple_nonlinear_score_matches_finite_difference_reference() -> None:
    fixture = make_simple_nonlinear_generic_target_fixture()
    theta = MODEL_B_INITIAL_BATCH
    _value, score = fixture.adapter.log_prob_and_grad(theta)
    eps = tf.constant(1.0e-5, dtype=tf.float64)
    columns = []
    for dim in range(3):
        basis = tf.one_hot(dim, 3, dtype=tf.float64)[tf.newaxis, :]
        plus = fixture.adapter.log_prob(theta + eps * basis)[0]
        minus = fixture.adapter.log_prob(theta - eps * basis)[0]
        columns.append((plus - minus) / (2.0 * eps))
    finite_difference = tf.stack(columns, axis=0)[tf.newaxis, :]

    tf.debugging.assert_near(score, finite_difference, rtol=1.0e-4, atol=1.0e-4)


def test_simple_nonlinear_generic_target_cpu_only_hides_gpu() -> None:
    assert os.environ.get("CUDA_VISIBLE_DEVICES") == "-1"
    assert tf.config.list_physical_devices("GPU") == []
