from __future__ import annotations

import copy
import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

from bayesfilter.inference import (
    FrozenDenseIAFTransport,
    InvalidNeuTraArtifact,
    finalize_dense_iaf_neutra_artifact_payload,
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


SCHEMA = "bayesfilter.neutra.dense_iaf_frozen_transport.v1"


def _target_signature() -> str:
    problem = BayesianSSMProblem(
        problem_id="dense-iaf-toy-ssm",
        static_shape=SSMStaticShape(
            horizon=3,
            state_dim=1,
            observation_dim=1,
            innovation_dim=1,
            parameter_dim=2,
        ),
        data_signature=SSMDataSignature(
            dataset_id="dense-iaf-toy-data",
            observation_shape=(3, 1),
            data_hash="sha256:dense-iaf-data",
        ),
        target_coordinate_convention="unconstrained",
        model_manifest={
            "model_id": "dense-iaf-toy-model",
            "model_hash": "sha256:dense-iaf-model",
            "capabilities": ("transition_mean", "observation_mean"),
        },
    )
    chart = ParameterChart(
        parameter_names=("alpha", "beta"),
        unconstrained_dim=2,
        constrained_shape=(2,),
        transform_manifest={
            "transform_id": "identity-chart",
            "transform_hash": "sha256:dense-iaf-chart",
        },
        log_jacobian_convention="not_included",
    )
    prior = ParameterPrior(
        prior_manifest={
            "prior_id": "toy-gaussian-prior",
            "prior_hash": "sha256:dense-iaf-prior",
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
            "filter_hash": "sha256:dense-iaf-filter",
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


def _raw_payload(**overrides):
    values = {
        "schema": SCHEMA,
        "transport_id": "dense-iaf-synthetic-transport",
        "dimension": 2,
        "target_signature": _target_signature(),
        "log_jacobian_available": True,
        "component_order": ("dense",),
        "components": (
            {
                "component_id": "dense",
                "kind": "dense_autoregressive_iaf",
                "dim": 2,
                "hidden_layers": (2,),
                "activation": "tanh",
                "s_max": 1.0,
                "masks_policy": "legacy_degree_masks_v1",
                "dtype": "float64",
                "weights": (
                    ((0.5, -0.25), (0.75, 0.1)),
                    ((0.2, -0.4, 0.3, -0.2), (0.1, 0.6, -0.5, 0.7)),
                ),
                "biases": (
                    (0.05, -0.1),
                    (0.02, -0.03, 0.04, -0.05),
                ),
            },
        ),
        "training_state_hash": "sha256:dense-iaf-synthetic-training",
        "nonclaims": (
            "frozen dense-IAF transport artifact loader only",
            "no NeuTra training claim",
            "no HMC tuning or sampling claim",
            "no posterior convergence claim",
            "no scientific validity claim",
            "no default policy change",
        ),
    }
    values.update(overrides)
    return values


def _payload(**overrides):
    return finalize_dense_iaf_neutra_artifact_payload(_raw_payload(**overrides))


def _load(payload=None):
    return load_frozen_neutra_artifact(
        _payload() if payload is None else payload,
        expected_target_signature=_target_signature(),
    )


def _expected_forward_and_logdet(z):
    z = np.asarray(z, dtype=np.float64)
    w0 = np.array([[0.5, -0.25], [0.75, 0.1]], dtype=np.float64)
    b0 = np.array([0.05, -0.1], dtype=np.float64)
    w1 = np.array(
        [[0.2, -0.4, 0.3, -0.2], [0.1, 0.6, -0.5, 0.7]],
        dtype=np.float64,
    )
    b1 = np.array([0.02, -0.03, 0.04, -0.05], dtype=np.float64)
    mask0 = np.array([[1.0, 1.0], [0.0, 0.0]], dtype=np.float64)
    mask1 = np.array([[0.0, 1.0, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0]], dtype=np.float64)
    h = np.tanh(z @ (w0 * mask0) + b0)
    raw = h @ (w1 * mask1) + b1
    scale_log = np.tanh(raw[:, :2])
    shift = raw[:, 2:]
    return z * np.exp(scale_log) + shift, np.sum(scale_log, axis=-1)


def test_dense_iaf_loader_accepts_synthetic_payload_and_manifest() -> None:
    artifact = _load()

    assert isinstance(artifact.transport, FrozenDenseIAFTransport)
    assert artifact.manifest.schema == SCHEMA
    assert artifact.manifest.dimension == 2
    assert artifact.binding.target_signature == _target_signature()
    assert artifact.binding.transport_manifest["topology_hash"] == artifact.manifest.topology_hash
    assert artifact.binding.transport_manifest["tensor_hash"] == artifact.manifest.tensor_hash
    assert stable_frozen_neutra_artifact_signature(artifact) == artifact.artifact_signature
    assert "no HMC tuning or sampling claim" in artifact.manifest.nonclaims


def test_dense_iaf_loader_forward_and_logdet_match_fixture() -> None:
    artifact = _load()
    z = tf.constant([[0.2, -0.4], [0.1, 0.3]], dtype=tf.float64)

    actual = artifact.transport.forward_batch(z)
    actual_logdet = artifact.transport.log_abs_det_jacobian_batch(z)
    expected, expected_logdet = _expected_forward_and_logdet(z.numpy())

    np.testing.assert_allclose(actual.numpy(), expected, rtol=1e-12, atol=1e-12)
    np.testing.assert_allclose(
        actual_logdet.numpy(),
        expected_logdet,
        rtol=1e-12,
        atol=1e-12,
    )


def test_dense_iaf_loader_rejects_target_signature_mismatch_and_legacy_identity() -> None:
    with pytest.raises(InvalidNeuTraArtifact, match="target_signature mismatch"):
        load_frozen_neutra_artifact(
            _payload(),
            expected_target_signature="0" * 64,
        )

    historical_style = _payload(target_signature="legacy-rotemberg-target-name")
    with pytest.raises(InvalidNeuTraArtifact, match="sha256"):
        load_frozen_neutra_artifact(
            historical_style,
            expected_target_signature=_target_signature(),
        )


def test_dense_iaf_loader_rejects_individual_hash_tampering() -> None:
    for field in ("topology_hash", "tensor_hash", "transport_hash"):
        tampered = dict(_payload())
        tampered[field] = "0" * 64
        with pytest.raises(InvalidNeuTraArtifact, match=f"{field} mismatch"):
            load_frozen_neutra_artifact(
                tampered,
                expected_target_signature=_target_signature(),
            )


def test_dense_iaf_loader_rejects_nonfinite_and_shape_mismatch() -> None:
    nonfinite = _raw_payload()
    component = dict(nonfinite["components"][0])
    weights = [list(row_group) for row_group in component["weights"]]
    weights[0] = [list(row) for row in weights[0]]
    weights[0][0] = (float("nan"), -0.25)
    component["weights"] = tuple(tuple(tuple(row) for row in group) for group in weights)
    nonfinite["components"] = (component,)
    with pytest.raises(InvalidNeuTraArtifact, match="finite"):
        finalize_dense_iaf_neutra_artifact_payload(nonfinite)

    bad_shape = copy.deepcopy(_payload())
    bad_shape["components"][0]["weights"][0] = ((0.5,), (0.75,))
    bad_shape = finalize_dense_iaf_neutra_artifact_payload(bad_shape)
    with pytest.raises(InvalidNeuTraArtifact, match="shape mismatch"):
        load_frozen_neutra_artifact(
            bad_shape,
            expected_target_signature=_target_signature(),
        )


def test_dense_iaf_loader_rejects_process_local_identity_and_component_semantics() -> None:
    with pytest.raises(InvalidNeuTraArtifact, match="process-local"):
        finalize_dense_iaf_neutra_artifact_payload(
            _raw_payload(transport_id=f"object at 0x{id(object()):x}")
        )

    unsupported = copy.deepcopy(_payload())
    unsupported["components"][0]["kind"] = "real_nvp"
    unsupported = finalize_dense_iaf_neutra_artifact_payload(unsupported)
    with pytest.raises(InvalidNeuTraArtifact, match="unsupported component kind"):
        load_frozen_neutra_artifact(
            unsupported,
            expected_target_signature=_target_signature(),
        )

    bad_policy = copy.deepcopy(_payload())
    bad_policy["components"][0]["masks_policy"] = "legacy_runtime_mask_object"
    bad_policy = finalize_dense_iaf_neutra_artifact_payload(bad_policy)
    with pytest.raises(InvalidNeuTraArtifact, match="masks_policy"):
        load_frozen_neutra_artifact(
            bad_policy,
            expected_target_signature=_target_signature(),
        )


def test_dense_iaf_loader_rejects_summary_only_historical_artifacts() -> None:
    with pytest.raises(InvalidNeuTraArtifact, match="schema"):
        load_frozen_neutra_artifact(
            {
                "schema_version": 1,
                "kind": "neutra_paper_style_at_baseline",
                "replay_state_path": "docs/plans/artifacts/legacy/paper_dense_iaf_replay.json",
                "row": {"candidate_arm": "paper_dense_iaf"},
            },
            expected_target_signature=_target_signature(),
        )
