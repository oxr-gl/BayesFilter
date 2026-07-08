from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
import tensorflow as tf

from bayesfilter.nonlinear.ssl_lstm_protocol import SSLLSTMStaticConfig
from bayesfilter.nonlinear.ssl_lstm_zhaocui_fixed_adapter import (
    SSLLSTMZhaoCuiFixedManifest,
    build_ssl_lstm_zhaocui_fixed_value_score_artifact,
    make_ssl_lstm_zhaocui_fixed_components,
    tf_ssl_lstm_zhaocui_fixed_score,
)


EVIDENCE_PATH = (
    "docs/plans/"
    "bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase2-"
    "zhaocui-fixed-adapter-implementation-result-2026-07-05.md"
)


def _config() -> SSLLSTMStaticConfig:
    return SSLLSTMStaticConfig(
        horizon=2,
        latent_dim=1,
        hidden_dim=1,
        observation_dim=1,
    )


def _theta() -> tf.Tensor:
    config = _config()
    values = np.zeros(config.parameter_dim, dtype=np.float64)
    values[0:4] = np.array([0.09, -0.07, 0.05, 0.04])
    values[4:8] = np.array([0.03, -0.02, 0.06, -0.05])
    values[8:12] = np.array([0.01, 0.04, -0.03, 0.02])
    values[12] = 0.35
    values[13] = -0.08
    values[14] = 0.65
    values[15] = 0.05
    values[16:19] = np.array([0.15, -0.10, 0.20])
    values[19:22] = np.array([-0.35, 0.15, 0.55])
    values[22] = 0.35
    values[-1] = -0.15
    return tf.constant(values, dtype=tf.float64)


def _observations() -> tf.Tensor:
    return tf.constant([[0.12], [-0.03]], dtype=tf.float64)


def _manifest() -> SSLLSTMZhaoCuiFixedManifest:
    return SSLLSTMZhaoCuiFixedManifest(
        reference_sample_count=9,
        initial_seed=(20260705, 41),
        process_seed=(20260705, 43),
    )


def _finite_difference(
    theta: tf.Tensor,
    value_fn,
    *,
    indices: tuple[int, ...],
    step: float = 1.0e-5,
) -> np.ndarray:
    base = np.asarray(theta.numpy(), dtype=np.float64)
    values = np.zeros([len(indices)], dtype=np.float64)
    for offset, index in enumerate(indices):
        plus = base.copy()
        minus = base.copy()
        plus[index] += step
        minus[index] -= step
        values[offset] = (
            float(value_fn(tf.constant(plus, dtype=tf.float64)).numpy())
            - float(value_fn(tf.constant(minus, dtype=tf.float64)).numpy())
        ) / (2.0 * step)
    return values


def test_zhaocui_fixed_manifest_records_honest_route_classification() -> None:
    manifest = _manifest()
    payload = manifest.as_dict()

    assert payload["source_route_classification"] == "fixed_hmc_adaptation_with_extension_likelihood"
    assert payload["reference_seed_policy"] == "stateless_required"
    assert payload["resampling_policy"] == "not_used_fixed_logmeanexp_replay"
    assert payload["score_path"] == "manual_first_order_tensorflow_chain_rule"
    assert any("full_sol.m" in item for item in payload["source_anchor_summary"])
    assert any("computeL.m" in item for item in payload["source_anchor_summary"])
    assert "no source-faithful SSL-LSTM Zhao-Cui parity claim" in payload["nonclaims"]


def test_zhaocui_fixed_score_is_finite_deterministic_and_matches_fd_subset() -> None:
    config = _config()
    theta = _theta()
    manifest = _manifest()
    result, components = tf_ssl_lstm_zhaocui_fixed_score(
        _observations(),
        theta,
        config,
        evidence_path=EVIDENCE_PATH,
        manifest=manifest,
    )
    repeated, repeated_components = tf_ssl_lstm_zhaocui_fixed_score(
        _observations(),
        theta,
        config,
        evidence_path=EVIDENCE_PATH,
        manifest=manifest,
    )

    assert result.failure is None
    assert components.protocol.filter_name == "zhaocui_fixed"
    assert components.protocol.gradient_path == "analytic_first_order_zhaocui_fixed"
    assert repeated_components.manifest.as_dict() == components.manifest.as_dict()
    assert np.isfinite(float(result.log_likelihood.numpy()))
    assert np.all(np.isfinite(result.score.numpy()))
    np.testing.assert_allclose(result.log_likelihood.numpy(), repeated.log_likelihood.numpy(), atol=1e-12)
    np.testing.assert_allclose(result.score.numpy(), repeated.score.numpy(), atol=1e-12)
    assert result.diagnostics["derivative_method"] == "analytic_first_order_fixed_replay"

    def value_fn(theta_value: tf.Tensor) -> tf.Tensor:
        local, _components = tf_ssl_lstm_zhaocui_fixed_score(
            _observations(),
            theta_value,
            config,
            evidence_path=EVIDENCE_PATH,
            manifest=manifest,
        )
        return local.log_likelihood

    indices = (0, 4, 8, 12, 13, 14, 15, 16, 19, 22)
    finite_difference = _finite_difference(theta, value_fn, indices=indices)
    residual = np.max(np.abs(result.score.numpy()[list(indices)] - finite_difference))
    np.testing.assert_allclose(
        result.score.numpy()[list(indices)],
        finite_difference,
        rtol=4e-3,
        atol=7e-4,
    )
    artifact = build_ssl_lstm_zhaocui_fixed_value_score_artifact(
        protocol=components.protocol,
        manifest=manifest,
        log_likelihood=result.log_likelihood,
        score=result.score,
        finite_difference_max_abs_error=float(residual),
    )
    assert artifact["filter_name"] == "zhaocui_fixed"
    assert artifact["artifact_role"] == "debug_reference"
    assert artifact["seed_policy"] == "stateless_required"
    assert artifact["branch_or_randomness_policy"] == "fixed_hmc_adaptation_manifest"
    assert artifact["finite_difference_check"]["role"] == "promotion_veto_for_adapter_admission"


def test_zhaocui_fixed_recenter_diagnostic_is_stable() -> None:
    config = _config()
    theta = _theta()
    result, _components = tf_ssl_lstm_zhaocui_fixed_score(
        _observations(),
        theta,
        config,
        evidence_path=EVIDENCE_PATH,
        manifest=_manifest(),
    )
    frame = result.diagnostics["recenter_frame"]

    assert tuple(frame["weighted_mean"].shape) == (config.augmented_state_dim,)
    assert tuple(frame["cholesky_diagonal"].shape) == (config.augmented_state_dim,)
    assert float(frame["effective_sample_size"].numpy()) > 1.0
    assert np.all(frame["cholesky_diagonal"].numpy() > 0.0)


def test_zhaocui_fixed_value_score_artifact_can_be_serialized(tmp_path: Path) -> None:
    config = _config()
    theta = _theta()
    result, components = tf_ssl_lstm_zhaocui_fixed_score(
        _observations(),
        theta,
        config,
        evidence_path=EVIDENCE_PATH,
        manifest=_manifest(),
    )
    artifact = build_ssl_lstm_zhaocui_fixed_value_score_artifact(
        protocol=components.protocol,
        manifest=components.manifest,
        log_likelihood=result.log_likelihood,
        score=result.score,
        finite_difference_max_abs_error=0.0,
    )
    output = tmp_path / "zhaocui_fixed_artifact.json"
    output.write_text(json.dumps(artifact, sort_keys=True), encoding="utf-8")

    restored = json.loads(output.read_text(encoding="utf-8"))
    assert restored["zhaocui_fixed_manifest"]["score_path"] == "manual_first_order_tensorflow_chain_rule"
    assert "no HMC convergence claim" in restored["nonclaims"]


def test_zhaocui_fixed_protocol_metadata_is_stable() -> None:
    config = _config()
    theta = _theta()
    components = make_ssl_lstm_zhaocui_fixed_components(
        theta,
        config,
        evidence_path=EVIDENCE_PATH,
        manifest=_manifest(),
    )
    repeated = make_ssl_lstm_zhaocui_fixed_components(
        theta,
        config,
        evidence_path=EVIDENCE_PATH,
        manifest=_manifest(),
    )

    assert components.protocol.stable_signature() == repeated.protocol.stable_signature()
    assert components.protocol.contract.filter_implementation == "ssl_lstm_zhaocui_fixed"
    assert components.protocol.contract.likelihood_term == "zhaocui_fixed_analytic_score"


def test_zhaocui_fixed_source_avoids_target_autodiff_and_numpy() -> None:
    source = Path("bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py").read_text(
        encoding="utf-8"
    )
    forbidden = ("GradientTape", "tf.py_function", "np.", "numpy")
    hits = [item for item in forbidden if item in source]

    assert hits == []


def test_zhaocui_fixed_rejects_invalid_manifest() -> None:
    with pytest.raises(ValueError, match="reference_sample_count"):
        SSLLSTMZhaoCuiFixedManifest(reference_sample_count=0)
    with pytest.raises(ValueError, match="stateless seeds"):
        SSLLSTMZhaoCuiFixedManifest(initial_seed=(1, 2, 3))
    with pytest.raises(ValueError, match="recenter_ridge"):
        SSLLSTMZhaoCuiFixedManifest(recenter_ridge=0.0)
