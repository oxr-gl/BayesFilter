from __future__ import annotations

import json
import math
from pathlib import Path

import tensorflow as tf

from bayesfilter.inference import stable_adapter_signature, value_score_capability
from bayesfilter.nonlinear.ssl_lstm_zhaocui_hmc_minimal import (
    MINIMAL_SSL_LSTM_ZHAOCUI_HMC_NONCLAIMS,
    MINIMAL_SSL_LSTM_ZHAOCUI_HMC_TARGET_SCOPE,
    MinimalZhaoCuiHMCTargetAdapter,
    initial_minimal_ssl_lstm_hmc_state,
    minimal_ssl_lstm_config,
    minimal_ssl_lstm_fixture_payload,
    minimal_ssl_lstm_observations,
    minimal_ssl_lstm_theta,
    minimal_ssl_lstm_zhaocui_manifest,
)


ROOT = Path(__file__).resolve().parents[1]
PREDECESSOR_ARTIFACT = (
    ROOT / "docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_adapter_cpu_hidden_2026-07-06.json"
)
EXPECTED_PHASE1_LOG_PROB = -1.3985848756201187
EXPECTED_PHASE1_SCORE_NORM = 1.624779105977436
EXPECTED_PHASE1_SCORE_MIN = -1.3131200200244952
EXPECTED_PHASE1_SCORE_MAX = 0.04093624533430015
EXPECTED_PHASE1_ADAPTER_SIGNATURE = (
    "85095a36eaf605d1d84c539d5d912896b63c4028ae0aa8e63c5d63d183c85508"
)


def test_minimal_fixture_matches_predecessor_scalar_contract() -> None:
    config = minimal_ssl_lstm_config()
    theta = minimal_ssl_lstm_theta()
    observations = minimal_ssl_lstm_observations()
    manifest = minimal_ssl_lstm_zhaocui_manifest()
    payload = minimal_ssl_lstm_fixture_payload()

    assert config.horizon == 2
    assert config.latent_dim == 1
    assert config.hidden_dim == 1
    assert config.observation_dim == 1
    assert config.parameter_dim == 24
    assert theta.shape == (24,)
    assert observations.shape == (2, 1)
    assert manifest.reference_sample_count == 9
    assert manifest.initial_seed == (20260705, 41)
    assert manifest.process_seed == (20260705, 43)
    assert payload["theta"] == [
        0.09,
        -0.07,
        0.05,
        0.04,
        0.03,
        -0.02,
        0.06,
        -0.05,
        0.01,
        0.04,
        -0.03,
        0.02,
        0.35,
        -0.08,
        0.65,
        0.05,
        0.15,
        -0.1,
        0.2,
        -0.35,
        0.15,
        0.55,
        0.35,
        -0.15,
    ]


def test_internal_adapter_matches_frozen_predecessor_target_values() -> None:
    adapter = MinimalZhaoCuiHMCTargetAdapter(prior_scale=5.0)
    theta = initial_minimal_ssl_lstm_hmc_state(1.0e-3)
    batch = tf.stack([theta, theta], axis=0)

    value, score = adapter.log_prob_and_grad(theta)
    batch_values, batch_scores = adapter.log_prob_and_grad(batch)
    capability = value_score_capability(adapter)

    assert value.shape == ()
    assert score.shape == (24,)
    assert batch_values.shape == (2,)
    assert batch_scores.shape == (2, 24)
    assert bool(tf.reduce_all(tf.math.is_finite(value)).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(score)).numpy())
    assert math.isclose(float(value.numpy()), EXPECTED_PHASE1_LOG_PROB, abs_tol=1.0e-12)
    assert math.isclose(
        float(tf.linalg.norm(score).numpy()),
        EXPECTED_PHASE1_SCORE_NORM,
        abs_tol=1.0e-12,
    )
    assert math.isclose(
        float(tf.reduce_min(score).numpy()),
        EXPECTED_PHASE1_SCORE_MIN,
        abs_tol=1.0e-12,
    )
    assert math.isclose(
        float(tf.reduce_max(score).numpy()),
        EXPECTED_PHASE1_SCORE_MAX,
        abs_tol=1.0e-12,
    )
    assert stable_adapter_signature(adapter) == EXPECTED_PHASE1_ADAPTER_SIGNATURE
    assert adapter.target_scope == MINIMAL_SSL_LSTM_ZHAOCUI_HMC_TARGET_SCOPE
    assert capability.value_score_authority == "graph_native"
    assert capability.runtime_backend == "tensorflow"
    assert capability.full_chain_xla_diagnostic_ready is True
    assert tuple(MINIMAL_SSL_LSTM_ZHAOCUI_HMC_NONCLAIMS) == adapter.value_score_capability().nonclaims[-10:]


def test_internal_adapter_matches_saved_predecessor_artifact() -> None:
    artifact = json.loads(PREDECESSOR_ARTIFACT.read_text(encoding="utf-8"))
    adapter = MinimalZhaoCuiHMCTargetAdapter(prior_scale=5.0)
    theta = initial_minimal_ssl_lstm_hmc_state(1.0e-3)
    value, score = adapter.log_prob_and_grad(theta)
    batch_values, batch_scores = adapter.log_prob_and_grad(tf.stack([theta, theta], axis=0))
    capability = value_score_capability(adapter)

    assert artifact["schema_version"] == "minimal_ssl_lstm_zhaocui_hmc_ladder.phase1_adapter.v1"
    assert artifact["fixture"] == minimal_ssl_lstm_fixture_payload()
    assert artifact["target_diagnostics"]["score_shape"] == list(score.shape.as_list())
    assert artifact["target_diagnostics"]["batch_score_shape"] == list(
        batch_scores.shape.as_list()
    )
    assert artifact["target_diagnostics"]["batch_value_shape"] == list(
        batch_values.shape.as_list()
    )
    assert artifact["adapter_signature"] == stable_adapter_signature(adapter)
    assert math.isclose(
        artifact["target_diagnostics"]["log_prob"],
        float(value.numpy()),
        abs_tol=1.0e-12,
    )
    assert math.isclose(
        artifact["target_diagnostics"]["score_norm"],
        float(tf.linalg.norm(score).numpy()),
        abs_tol=1.0e-12,
    )
    assert math.isclose(
        artifact["target_diagnostics"]["score_min"],
        float(tf.reduce_min(score).numpy()),
        abs_tol=1.0e-12,
    )
    assert math.isclose(
        artifact["target_diagnostics"]["score_max"],
        float(tf.reduce_max(score).numpy()),
        abs_tol=1.0e-12,
    )
    assert artifact["capability"]["value_score_authority"] == capability.value_score_authority
    assert artifact["capability"]["runtime_backend"] == capability.runtime_backend
    assert artifact["capability"]["target_scope"] == capability.target_scope
    assert artifact["capability"]["nonclaims"] == list(capability.nonclaims)
    assert artifact["nonclaims"] == list(MINIMAL_SSL_LSTM_ZHAOCUI_HMC_NONCLAIMS)
