from __future__ import annotations

import copy
import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

from bayesfilter.inference import (
    finalize_dense_iaf_neutra_artifact_payload,
    load_frozen_neutra_artifact,
)
from bayesfilter.inference.legacy_neutra_import import (
    InvalidLegacyNeuTraImport,
    build_dense_iaf_payload_from_legacy_training_state,
    build_dense_iaf_payload_from_legacy_transport_state,
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


def _target_signature() -> str:
    problem = BayesianSSMProblem(
        problem_id="legacy-neutra-import-toy-ssm",
        static_shape=SSMStaticShape(
            horizon=3,
            state_dim=1,
            observation_dim=1,
            innovation_dim=1,
            parameter_dim=2,
        ),
        data_signature=SSMDataSignature(
            dataset_id="legacy-neutra-import-toy-data",
            observation_shape=(3, 1),
            data_hash="sha256:legacy-neutra-import-data",
        ),
        target_coordinate_convention="unconstrained",
        model_manifest={
            "model_id": "legacy-neutra-import-toy-model",
            "model_hash": "sha256:legacy-neutra-import-model",
            "capabilities": ("transition_mean", "observation_mean"),
        },
    )
    chart = ParameterChart(
        parameter_names=("alpha", "beta"),
        unconstrained_dim=2,
        constrained_shape=(2,),
        transform_manifest={
            "transform_id": "identity-chart",
            "transform_hash": "sha256:legacy-neutra-import-chart",
        },
        log_jacobian_convention="not_included",
    )
    prior = ParameterPrior(
        prior_manifest={
            "prior_id": "legacy-neutra-import-prior",
            "prior_hash": "sha256:legacy-neutra-import-prior",
        },
        support_policy="unbounded",
        log_density_authority="graph_native",
    )
    filter_program = FilterProgram(
        filter_id="legacy-neutra-import-filter",
        required_model_capabilities=("transition_mean", "observation_mean"),
        deterministic_target_policy="deterministic",
        approximation_semantics="deterministic_approximation",
        filter_manifest={
            "filter_id": "legacy-neutra-import-filter",
            "filter_hash": "sha256:legacy-neutra-import-filter",
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


def _legacy_transport_state():
    return {
        "type": "composed",
        "metadata": {"dim": 2, "type": "composed"},
        "children": [
            {
                "type": "dense_autoregressive_iaf",
                "dim": 2,
                "hidden_layers": [2],
                "activation": "tanh",
                "s_max": 1.0,
                "weights": [
                    [[0.5, -0.25], [0.75, 0.1]],
                    [[0.2, -0.4, 0.3, -0.2], [0.1, 0.6, -0.5, 0.7]],
                ],
                "biases": [
                    [0.05, -0.1],
                    [0.02, -0.03, 0.04, -0.05],
                ],
                "metadata": {"dim": 2, "type": "dense_autoregressive_iaf"},
            },
            {
                "type": "mixing_linear",
                "W": [[0.0, 1.0], [1.0, 0.0]],
                "metadata": {"dim": 2, "type": "mixing_linear"},
            },
            {
                "type": "affine",
                "offset": [0.1, -0.2],
                "L_np": [[1.0, 0.0], [0.0, 2.0]],
                "metadata": {"dim": 2, "type": "affine_dense"},
            },
        ],
    }


def _legacy_training_state():
    return {
        "kind": "legacy_neutra_training_fixture",
        "transport_state": _legacy_transport_state(),
        "seed": 123,
    }


def _legacy_forward_and_logdet(z):
    z = np.asarray(z, dtype=np.float64)
    out = z
    logdet = np.zeros(z.shape[0], dtype=np.float64)

    # dense_autoregressive_iaf
    w0 = np.array([[0.5, -0.25], [0.75, 0.1]], dtype=np.float64)
    b0 = np.array([0.05, -0.1], dtype=np.float64)
    w1 = np.array(
        [[0.2, -0.4, 0.3, -0.2], [0.1, 0.6, -0.5, 0.7]],
        dtype=np.float64,
    )
    b1 = np.array([0.02, -0.03, 0.04, -0.05], dtype=np.float64)
    mask0 = np.array([[1.0, 1.0], [0.0, 0.0]], dtype=np.float64)
    mask1 = np.array([[0.0, 1.0, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0]], dtype=np.float64)
    h = np.tanh(out @ (w0 * mask0) + b0)
    raw = h @ (w1 * mask1) + b1
    scale_log = np.tanh(raw[:, :2])
    shift = raw[:, 2:]
    out = out * np.exp(scale_log) + shift
    logdet = logdet + np.sum(scale_log, axis=-1)

    # mixing_linear uses z @ W.T in legacy
    W = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.float64)
    out = out @ W.T
    logdet = logdet + np.linalg.slogdet(W)[1]

    # affine uses z @ L.T + offset in legacy batch form
    L = np.array([[1.0, 0.0], [0.0, 2.0]], dtype=np.float64)
    offset = np.array([0.1, -0.2], dtype=np.float64)
    out = out @ L.T + offset
    logdet = logdet + np.linalg.slogdet(L)[1]
    return out, logdet


def test_legacy_transport_state_import_builds_payload_and_matches_legacy() -> None:
    payload = build_dense_iaf_payload_from_legacy_transport_state(
        _legacy_transport_state(),
        transport_id="legacy-synthetic-transport",
        target_signature=_target_signature(),
        training_state_hash="sha256:legacy-training-state",
        expected_dimension=2,
        component_id_prefix="legacy",
        legacy_payload_references={"training_state_path": "docs/plans/legacy.json"},
    )
    finalized = finalize_dense_iaf_neutra_artifact_payload(payload)
    artifact = load_frozen_neutra_artifact(
        finalized,
        expected_target_signature=_target_signature(),
    )
    z = tf.constant([[0.2, -0.4], [0.1, 0.3], [0.0, 0.0]], dtype=tf.float64)
    actual_u = artifact.transport.forward_batch(z).numpy()
    actual_logdet = artifact.transport.log_abs_det_jacobian_batch(z).numpy()
    expected_u, expected_logdet = _legacy_forward_and_logdet(z.numpy())

    np.testing.assert_allclose(actual_u, expected_u, rtol=1e-12, atol=1e-12)
    np.testing.assert_allclose(actual_logdet, expected_logdet, rtol=1e-12, atol=1e-12)
    assert tuple(payload["component_order"]) == (
        "legacy_00_dense_autoregressive_iaf",
        "legacy_01_mixing_linear",
        "legacy_02_affine",
    )
    assert payload["components"][1]["matrix"] == ((0.0, 1.0), (1.0, 0.0))


def test_legacy_training_state_import_uses_transport_state_field() -> None:
    payload = build_dense_iaf_payload_from_legacy_training_state(
        _legacy_training_state(),
        transport_id="legacy-synthetic-transport",
        target_signature=_target_signature(),
        training_state_hash="sha256:legacy-training-state",
        expected_dimension=2,
    )
    assert payload["transport_id"] == "legacy-synthetic-transport"
    assert payload["training_state_hash"] == "sha256:legacy-training-state"
    assert payload["dimension"] == 2


def test_legacy_import_rejects_noncomposed_root_unknown_component_and_smax() -> None:
    bad_root = copy.deepcopy(_legacy_transport_state())
    bad_root["type"] = "affine"
    with pytest.raises(InvalidLegacyNeuTraImport, match="must be composed"):
        build_dense_iaf_payload_from_legacy_transport_state(
            bad_root,
            transport_id="x",
            target_signature=_target_signature(),
        )

    bad_kind = copy.deepcopy(_legacy_transport_state())
    bad_kind["children"][1]["type"] = "real_nvp"
    with pytest.raises(InvalidLegacyNeuTraImport, match="unsupported legacy component kind"):
        build_dense_iaf_payload_from_legacy_transport_state(
            bad_kind,
            transport_id="x",
            target_signature=_target_signature(),
        )

    bad_smax = copy.deepcopy(_legacy_transport_state())
    bad_smax["children"][0]["s_max"] = 0.5
    with pytest.raises(InvalidLegacyNeuTraImport, match=r"s_max == 1.0"):
        build_dense_iaf_payload_from_legacy_transport_state(
            bad_smax,
            transport_id="x",
            target_signature=_target_signature(),
        )


def test_legacy_import_rejects_nonfinite_and_dimension_mismatch() -> None:
    bad_nonfinite = copy.deepcopy(_legacy_transport_state())
    bad_nonfinite["children"][0]["weights"][0][0][0] = float("nan")
    with pytest.raises(InvalidLegacyNeuTraImport, match="must be finite"):
        build_dense_iaf_payload_from_legacy_transport_state(
            bad_nonfinite,
            transport_id="x",
            target_signature=_target_signature(),
        )

    bad_dim = copy.deepcopy(_legacy_transport_state())
    bad_dim["children"][1]["W"] = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    with pytest.raises(InvalidLegacyNeuTraImport, match="row count mismatch|col count mismatch"):
        build_dense_iaf_payload_from_legacy_transport_state(
            bad_dim,
            transport_id="x",
            target_signature=_target_signature(),
        )

    with pytest.raises(InvalidLegacyNeuTraImport, match="missing transport_state"):
        build_dense_iaf_payload_from_legacy_training_state(
            {"kind": "broken"},
            transport_id="x",
            target_signature=_target_signature(),
        )
