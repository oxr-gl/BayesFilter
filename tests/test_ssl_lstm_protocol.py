from __future__ import annotations

import pytest

from bayesfilter.inference import ValueScoreCapability
from bayesfilter.nonlinear.ssl_lstm_protocol import (
    SSL_LSTM_VALUE_SCORE_SCHEMA_VERSION,
    InvalidSSLLSTMProtocol,
    SSLLSTMAdapterProtocol,
    SSLLSTMStaticConfig,
    build_expected_ssl_lstm_adapter_protocol,
    ssl_lstm_filter_protocol_spec,
    ssl_lstm_value_score_artifact_schema,
    validate_ssl_lstm_adapter_protocol,
    validate_ssl_lstm_value_score_artifact,
)


def test_ssl_lstm_static_config_builds_augmented_shape_and_parameter_names() -> None:
    config = SSLLSTMStaticConfig(
        horizon=5,
        latent_dim=2,
        hidden_dim=3,
        observation_dim=1,
    )

    names = config.parameter_names
    shape = config.static_shape()

    assert config.augmented_state_dim == 8
    assert config.innovation_dim == 2
    assert shape.horizon == 5
    assert shape.state_dim == 8
    assert shape.observation_dim == 1
    assert shape.innovation_dim == 2
    assert shape.parameter_dim == len(names)
    assert len(set(names)) == len(names)
    assert names[0] == "lstm_input.input.0.0"
    assert names[-1] == "observation_std_unconstrained.0"


def test_ssl_lstm_static_config_rejects_dense_covariance_until_reviewed() -> None:
    with pytest.raises(InvalidSSLLSTMProtocol, match="diagonal covariance"):
        SSLLSTMStaticConfig(
            horizon=5,
            latent_dim=2,
            hidden_dim=3,
            observation_dim=1,
            covariance_mode="dense",
        )


@pytest.mark.parametrize(
    ("filter_name", "gradient_path"),
    (
        ("fixed_sgqf", "analytic_first_order_fixed_sgqf"),
        ("svd_ukf", "analytic_first_order_svd_ukf"),
        ("zhaocui_fixed", "analytic_first_order_zhaocui_fixed"),
        ("ledh_streaming_ot", "manual_vjp_streaming_ot"),
    ),
)
def test_expected_ssl_lstm_protocol_accepts_declared_target_paths(
    filter_name: str,
    gradient_path: str,
) -> None:
    config = SSLLSTMStaticConfig(
        horizon=4,
        latent_dim=2,
        hidden_dim=2,
        observation_dim=1,
    )

    protocol = build_expected_ssl_lstm_adapter_protocol(
        config,
        filter_name=filter_name,  # type: ignore[arg-type]
        evidence_path="docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase2-value-score-protocol-result-2026-07-04.md",
    )
    spec = ssl_lstm_filter_protocol_spec(filter_name)

    assert protocol.gradient_path == gradient_path
    assert protocol.contract.filter_implementation == spec.filter_implementation
    assert protocol.contract.likelihood_term == spec.likelihood_term
    assert protocol.contract.seed_policy == spec.required_seed_policy
    assert protocol.contract.xla_hmc_ready is True
    assert len(protocol.stable_signature()) == 64


def test_ssl_lstm_protocol_rejects_gradient_tape_as_target_authority() -> None:
    config = SSLLSTMStaticConfig(
        horizon=4,
        latent_dim=2,
        hidden_dim=2,
        observation_dim=1,
    )

    with pytest.raises(InvalidSSLLSTMProtocol, match="gradient_tape_fallback"):
        build_expected_ssl_lstm_adapter_protocol(
            config,
            filter_name="fixed_sgqf",
            evidence_path="docs/plans/phase2.md",
            value_score_authority="gradient_tape_fallback",
            xla_hmc_ready=False,
        )


def test_ssl_lstm_protocol_rejects_wrong_gradient_path() -> None:
    config = SSLLSTMStaticConfig(
        horizon=4,
        latent_dim=2,
        hidden_dim=2,
        observation_dim=1,
    )

    with pytest.raises(InvalidSSLLSTMProtocol, match="requires gradient path"):
        build_expected_ssl_lstm_adapter_protocol(
            config,
            filter_name="ledh_streaming_ot",
            evidence_path="docs/plans/phase2.md",
            gradient_path="analytic_first_order_svd_ukf",  # type: ignore[arg-type]
        )


def test_ssl_lstm_protocol_rejects_unscoped_or_missing_evidence_metadata() -> None:
    config = SSLLSTMStaticConfig(
        horizon=4,
        latent_dim=2,
        hidden_dim=2,
        observation_dim=1,
    )
    protocol = build_expected_ssl_lstm_adapter_protocol(
        config,
        filter_name="svd_ukf",
        evidence_path="docs/plans/phase2.md",
    )
    contract = protocol.contract
    capability = ValueScoreCapability(
        value_score_authority="graph_native",
        xla_hmc_ready=True,
        runtime_backend="tensorflow",
        target_scope=contract.value_score.target_scope,
        nonclaims=("missing evidence path fixture",),
    )
    replacement = SSLLSTMAdapterProtocol(
        filter_name=protocol.filter_name,
        gradient_path=protocol.gradient_path,
        contract=contract.__class__(
            parameter_names=contract.parameter_names,
            static_shape=contract.static_shape,
            transform=contract.transform,
            observation_semantics=contract.observation_semantics,
            regularization=contract.regularization,
            value_score=capability,
            prior_term=contract.prior_term,
            likelihood_term=contract.likelihood_term,
            dtype=contract.dtype,
            backend=contract.backend,
            filter_implementation=contract.filter_implementation,
            compile_mode=contract.compile_mode,
            trace_policy=contract.trace_policy,
            return_filtered=contract.return_filtered,
            seed_policy=contract.seed_policy,
            map_source=contract.map_source,
            mass_matrix_source=contract.mass_matrix_source,
            hessian_source=contract.hessian_source,
        ),
        branch_or_randomness_policy=protocol.branch_or_randomness_policy,
    )

    with pytest.raises(InvalidSSLLSTMProtocol, match="evidence_path"):
        validate_ssl_lstm_adapter_protocol(replacement)


def _artifact(protocol):
    return {
        "schema_version": SSL_LSTM_VALUE_SCORE_SCHEMA_VERSION,
        "artifact_role": "target",
        "target_scope": protocol.contract.value_score.target_scope,
        "filter_name": protocol.filter_name,
        "gradient_path": protocol.gradient_path,
        "value_score_authority": protocol.contract.value_score.value_score_authority,
        "compile_mode": protocol.contract.compile_mode,
        "jit_compile": True,
        "device": "GPU:0",
        "tf32_enabled": True,
        "seed_policy": protocol.contract.seed_policy,
        "branch_or_randomness_policy": protocol.branch_or_randomness_policy,
        "log_likelihood": -1.25,
        "score": [0.0, 1.0],
        "score_finite": True,
        "finite_difference_check": {"max_abs_error": 1e-6},
        "diagnostic_roles": {
            "finite_difference_check": "promotion_veto_for_adapter_admission",
            "runtime": "explanatory",
        },
        "nonclaims": (
            "tiny fixture only",
            "no HMC convergence claim",
        ),
    }


def test_ssl_lstm_value_score_artifact_schema_and_validator() -> None:
    config = SSLLSTMStaticConfig(
        horizon=4,
        latent_dim=2,
        hidden_dim=2,
        observation_dim=1,
    )
    protocol = build_expected_ssl_lstm_adapter_protocol(
        config,
        filter_name="zhaocui_fixed",
        evidence_path="docs/plans/phase2.md",
    )
    schema = ssl_lstm_value_score_artifact_schema()
    artifact = _artifact(protocol)

    assert "finite_difference_check" in schema["required_fields"]
    assert schema["diagnostic_roles"]["finite_difference_check"] == (
        "promotion_veto_for_adapter_admission"
    )
    assert validate_ssl_lstm_value_score_artifact(
        artifact,
        protocol=protocol,
    )["filter_name"] == "zhaocui_fixed"


def test_ssl_lstm_value_score_artifact_rejects_missing_jit_or_nonfinite_score() -> None:
    config = SSLLSTMStaticConfig(
        horizon=4,
        latent_dim=2,
        hidden_dim=2,
        observation_dim=1,
    )
    protocol = build_expected_ssl_lstm_adapter_protocol(
        config,
        filter_name="fixed_sgqf",
        evidence_path="docs/plans/phase2.md",
    )

    no_jit = _artifact(protocol)
    no_jit["jit_compile"] = False
    with pytest.raises(InvalidSSLLSTMProtocol, match="jit_compile true"):
        validate_ssl_lstm_value_score_artifact(no_jit, protocol=protocol)

    nonfinite = _artifact(protocol)
    nonfinite["score_finite"] = False
    with pytest.raises(InvalidSSLLSTMProtocol, match="hard veto"):
        validate_ssl_lstm_value_score_artifact(nonfinite, protocol=protocol)
