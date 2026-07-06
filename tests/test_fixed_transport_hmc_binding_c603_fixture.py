from __future__ import annotations

import json
import os
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import tensorflow as tf

from bayesfilter.inference import (
    HMCTuningPolicy,
    ValueScoreCapability,
    bind_fixed_transport_hmc_mechanics,
    finalize_dense_iaf_neutra_artifact_payload,
    load_frozen_neutra_artifact,
)
from bayesfilter.inference.legacy_neutra_import import (
    build_dense_iaf_payload_from_legacy_training_state,
)


HANDOFF_ROOT_ENV = "BAYESFILTER_DSGE_HMC_HANDOFF_ROOT"
DEFAULT_HANDOFF_ROOT = Path("/tmp/dsge_hmc-neutra-handoff-20260705")
TARGET_SIGNATURE = (
    "8f5caae87797898bd8d4f0c795246f5103e3535e247a49e5ebf01217ece20d07"
)
EXPECTED_TRANSPORT_HASH = (
    "5d4b43cf2e0da2c35d5a0000a390110364f2d7d7fd205e8b0cabb72d0cf87dcc"
)
EXPECTED_ARTIFACT_SIGNATURE = (
    "4df1eeb2f9e6a094fbf2dfe07fd899de7a1e6576fc8a8a2268b8020228f283be"
)


def _handoff_root() -> Path:
    raw = os.environ.get(HANDOFF_ROOT_ENV)
    root = DEFAULT_HANDOFF_ROOT if not raw else Path(raw).expanduser()
    if not root.exists():
        raise AssertionError(
            f"c603 local handoff checkout is required for this mechanics test: {root}"
        )
    return root


def _proposal_path(root: Path) -> Path:
    return root / (
        "docs/plans/"
        "bayesfilter-neutra-export-proposal-c603-rotemberg-second-order-svd-2026-07-05.json"
    )


def _training_state_path(root: Path) -> Path:
    return root / (
        "docs/plans/artifacts/"
        "rotemberg-second-order-svd-4d-minimal-principal-sqrt-baseline-2026-07-01/"
        "phase6/serious_baseline_launch/paper_dense_iaf_seed20260622.training_state.json"
    )


def _replay_state_path(root: Path) -> Path:
    return root / (
        "docs/plans/artifacts/"
        "rotemberg-second-order-svd-4d-minimal-principal-sqrt-baseline-2026-07-01/"
        "phase6/serious_baseline_launch/paper_dense_iaf_seed20260622_replay_state.json"
    )


def _config_path(root: Path) -> Path:
    return root / (
        "docs/plans/artifacts/"
        "rotemberg-second-order-svd-4d-minimal-principal-sqrt-baseline-2026-07-01/"
        "phase6/serious_baseline_launch/hmc_workers/fixed_hmc_grid/"
        "0603_fixed_hmc_grid_candidate_index-603_leapfrog-2_step_size-0.729166666666_config.json"
    )


def _preflight_path(root: Path) -> Path:
    return root / (
        "docs/plans/artifacts/"
        "rotemberg-second-order-svd-4d-minimal-principal-sqrt-baseline-2026-07-01/"
        "phase1/preflight/rotemberg_second_order_svd_target_preflight.json"
    )


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assert_expected_hashes(root: Path, proposal: dict[str, object]) -> None:
    frozen = proposal["frozen_transport"]["transport_manifest"]  # type: ignore[index]
    expected_training = frozen["state_reference"]["sha256"]  # type: ignore[index]
    expected_replay = frozen["replay_reference"]["sha256"]  # type: ignore[index]
    expected_config = frozen["hmc_config_reference"]["sha256"]  # type: ignore[index]

    training_path = _training_state_path(root)
    replay_path = _replay_state_path(root)
    config_path = _config_path(root)

    assert _sha256(training_path) == expected_training
    assert _sha256(replay_path) == expected_replay
    assert _sha256(config_path) == expected_config


def _theta_reference(root: Path) -> list[float]:
    preflight = _load_json(_preflight_path(root))
    values = preflight.get("theta_reference")
    if not isinstance(values, list) or len(values) != 15:
        raise AssertionError("c603 preflight theta_reference must be a length-15 list")
    return [float(item) for item in values]


class BatchedQuadraticAdapter:
    parameter_dim = 15

    def value_score_capability(self) -> ValueScoreCapability:
        return ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=True,
            runtime_backend="tensorflow_batched_quadratic_fixture",
            evidence_path="tests/test_fixed_transport_hmc_binding_c603_fixture.py",
            target_scope="c603_fixed_transport_hmc_fixture",
            nonclaims=("mechanics smoke only",),
        )

    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        values = tf.convert_to_tensor(theta, dtype=tf.float64)
        return -0.5 * tf.reduce_sum(tf.square(values), axis=-1), -values


def _artifact():
    root = _handoff_root()
    proposal = _load_json(_proposal_path(root))
    _assert_expected_hashes(root, proposal)
    training_state = _load_json(_training_state_path(root))

    payload = build_dense_iaf_payload_from_legacy_training_state(
        training_state,
        transport_id=proposal["frozen_transport"]["transport_id"],  # type: ignore[index]
        target_signature=TARGET_SIGNATURE,
        training_state_hash=(
            "sha256:"
            + proposal["frozen_transport"]["transport_manifest"]["state_reference"]["sha256"]  # type: ignore[index]
        ),
        expected_dimension=proposal["frozen_transport"]["dimension"],  # type: ignore[index]
        component_id_prefix="c603",
        legacy_payload_references={
            "proposal_path": str(_proposal_path(root)),
            "training_state_path": str(_training_state_path(root)),
            "training_state_sha256": proposal["frozen_transport"]["transport_manifest"]["state_reference"]["sha256"],  # type: ignore[index]
            "replay_state_path": str(_replay_state_path(root)),
            "replay_state_sha256": proposal["frozen_transport"]["transport_manifest"]["replay_reference"]["sha256"],  # type: ignore[index]
            "hmc_config_path": str(_config_path(root)),
            "hmc_config_sha256": proposal["frozen_transport"]["transport_manifest"]["hmc_config_reference"]["sha256"],  # type: ignore[index]
        },
    )
    finalized = finalize_dense_iaf_neutra_artifact_payload(payload)
    artifact = load_frozen_neutra_artifact(
        finalized,
        expected_target_signature=TARGET_SIGNATURE,
    )
    assert artifact.binding.target_signature == TARGET_SIGNATURE
    assert artifact.manifest.transport_hash == EXPECTED_TRANSPORT_HASH
    assert artifact.artifact_signature == EXPECTED_ARTIFACT_SIGNATURE
    return artifact


def _reference_value_and_score(transport: object, z: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
    with tf.GradientTape(persistent=True) as tape:
        tape.watch(z)
        u = transport.forward_batch(z)  # type: ignore[attr-defined]
        logdet = transport.log_abs_det_jacobian_batch(z)  # type: ignore[attr-defined]
    jacobian = tape.batch_jacobian(u, z)
    logdet_score = tape.batch_jacobian(logdet[:, tf.newaxis], z)[:, 0, :]
    del tape
    value = -0.5 * tf.reduce_sum(tf.square(u), axis=-1) + logdet
    score = tf.einsum("bui,bu->bi", jacobian, -u) + logdet_score
    return value, score


def test_c603_fixed_transport_hmc_mechanics_smoke_preserves_loaded_artifact_identity() -> None:
    artifact = _artifact()
    z = tf.constant(
        [
            _theta_reference(_handoff_root()),
            [0.0] * 15,
            [0.1 * (index + 1) for index in range(15)],
            [-0.05 * (index + 1) for index in range(15)],
            [0.2 if index % 2 == 0 else -0.15 for index in range(15)],
        ],
        dtype=tf.float64,
    )

    result = bind_fixed_transport_hmc_mechanics(
        base_adapter=BatchedQuadraticAdapter(),
        loaded_artifact=artifact,
        initial_position=z,
        target_scope="c603_fixed_transport_hmc_fixture",
        tuning_policy=HMCTuningPolicy.fixed_kernel_screen(),
        use_xla=False,
        seed=17,
        execution_device="cpu",
    )

    expected_value, expected_score = _reference_value_and_score(artifact.transport, z)

    assert result.manifest.target_signature == TARGET_SIGNATURE
    assert result.manifest.transport_hash == EXPECTED_TRANSPORT_HASH
    assert result.manifest.execution_device == "cpu"
    assert result.manifest.mechanics_only is True
    assert result.manifest.hmc_policy_label == "fixed_kernel_screen"
    assert result.diagnostics["mechanics_only"] is True
    assert "no serious HMC convergence claim" in result.manifest.nonclaims
    assert bool(tf.reduce_all(tf.math.is_finite(result.value)).numpy()) is True
    assert bool(tf.reduce_all(tf.math.is_finite(result.score)).numpy()) is True

    np.testing.assert_allclose(result.value.numpy(), expected_value.numpy(), rtol=1e-12, atol=1e-12)
    np.testing.assert_allclose(result.score.numpy(), expected_score.numpy(), rtol=1e-12, atol=1e-12)
