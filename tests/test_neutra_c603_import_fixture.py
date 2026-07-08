from __future__ import annotations

import json
import os
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

from bayesfilter.inference import (
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
EXPECTED_TOPOLOGY_HASH = (
    "b898b910eb3367145f5260d124a3b5a8d48a1d6c2f9b050c2939990d5083e11f"
)
EXPECTED_TENSOR_HASH = (
    "add7f57aa0f2d4ba61456b2a259632ca35969edbe278ed1b8af563be29f88cfd"
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
        pytest.skip(
            f"c603 local handoff checkout is optional; set {HANDOFF_ROOT_ENV} or "
            f"restore {root}"
        )
    return root


def _proposal_path(root: Path) -> Path:
    return root / "docs/plans/bayesfilter-neutra-export-proposal-c603-rotemberg-second-order-svd-2026-07-05.json"


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


def _legacy_dense_iaf_masks(dim: int, hidden_layers: tuple[int, ...]) -> list[np.ndarray]:
    degrees: list[list[int]] = [list(range(1, dim + 1))]
    max_degree = max(1, dim - 1)
    for width in hidden_layers:
        degrees.append([1 + (index % max_degree) for index in range(width)])
    degrees.append(list(range(1, dim + 1)) + list(range(1, dim + 1)))
    masks = []
    for layer_index, (deg_in, deg_out) in enumerate(zip(degrees[:-1], degrees[1:])):
        is_output = layer_index == len(degrees) - 2
        masks.append(
            np.asarray(
                [
                    [
                        1.0
                        if ((source < target) if is_output else (source <= target))
                        else 0.0
                        for target in deg_out
                    ]
                    for source in deg_in
                ],
                dtype=np.float64,
            )
        )
    return masks


def _legacy_activation(name: str, values: np.ndarray) -> np.ndarray:
    if name == "elu":
        return np.where(values > 0.0, values, np.expm1(values))
    if name == "tanh":
        return np.tanh(values)
    if name == "relu":
        return np.maximum(values, 0.0)
    raise AssertionError(f"unsupported activation in fixture: {name}")


def _legacy_forward_and_logdet_from_transport_state(
    transport_state: dict[str, object],
    z: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(z, dtype=np.float64)
    output = values
    logdet = np.zeros(values.shape[0], dtype=np.float64)
    for component in transport_state["children"]:  # type: ignore[index]
        kind = component["type"]  # type: ignore[index]
        if kind == "dense_autoregressive_iaf":
            dim = int(component["dim"])  # type: ignore[index]
            hidden_layers = tuple(int(item) for item in component["hidden_layers"])  # type: ignore[index]
            activation = str(component["activation"])  # type: ignore[index]
            s_max = float(component["s_max"])  # type: ignore[index]
            weights = [np.asarray(item, dtype=np.float64) for item in component["weights"]]  # type: ignore[index]
            biases = [np.asarray(item, dtype=np.float64) for item in component["biases"]]  # type: ignore[index]
            masks = _legacy_dense_iaf_masks(dim, hidden_layers)
            h = output
            for weight, bias, mask in zip(weights[:-1], biases[:-1], masks[:-1]):
                h = _legacy_activation(activation, h @ (weight * mask) + bias)
            raw = h @ (weights[-1] * masks[-1]) + biases[-1]
            scale_logits = raw[:, :dim]
            shift = raw[:, dim:]
            scale_log = s_max * np.tanh(scale_logits / s_max)
            output = output * np.exp(scale_log) + shift
            logdet = logdet + np.sum(scale_log, axis=-1)
            continue
        if kind == "mixing_linear":
            W = np.asarray(component["W"], dtype=np.float64)  # type: ignore[index]
            output = output @ W.T
            logdet = logdet + np.linalg.slogdet(W)[1]
            continue
        if kind == "affine":
            offset = np.asarray(component["offset"], dtype=np.float64)  # type: ignore[index]
            if component.get("L_np") is not None:  # type: ignore[union-attr]
                L = np.asarray(component["L_np"], dtype=np.float64)  # type: ignore[index]
                output = output @ L.T + offset
                logdet = logdet + np.linalg.slogdet(L)[1]
            else:
                scale = np.asarray(component["scale"], dtype=np.float64)  # type: ignore[index]
                output = output * scale + offset
                logdet = logdet + np.sum(np.log(np.abs(scale)))
            continue
        raise AssertionError(f"unsupported legacy component in fixture: {kind}")
    return output, logdet


def test_c603_local_handoff_fixture_reproduces_validated_import() -> None:
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
    assert artifact.manifest.topology_hash == EXPECTED_TOPOLOGY_HASH
    assert artifact.manifest.tensor_hash == EXPECTED_TENSOR_HASH
    assert artifact.manifest.transport_hash == EXPECTED_TRANSPORT_HASH
    assert artifact.artifact_signature == EXPECTED_ARTIFACT_SIGNATURE
    assert tuple(payload["component_order"]) == (
        "c603_00_dense_autoregressive_iaf",
        "c603_01_mixing_linear",
        "c603_02_dense_autoregressive_iaf",
        "c603_03_mixing_linear",
        "c603_04_dense_autoregressive_iaf",
        "c603_05_affine",
    )

    z = np.asarray(
        [
            _theta_reference(root),
            [0.0] * 15,
            [0.1 * (index + 1) for index in range(15)],
            [-0.05 * (index + 1) for index in range(15)],
            [0.2 if index % 2 == 0 else -0.15 for index in range(15)],
        ],
        dtype=np.float64,
    )
    actual_forward = artifact.transport.forward_batch(tf.constant(z, dtype=tf.float64)).numpy()
    actual_logdet = artifact.transport.log_abs_det_jacobian_batch(
        tf.constant(z, dtype=tf.float64)
    ).numpy()
    expected_forward, expected_logdet = _legacy_forward_and_logdet_from_transport_state(
        training_state["transport_state"],  # type: ignore[index]
        z,
    )

    np.testing.assert_allclose(actual_forward, expected_forward, rtol=1e-12, atol=1e-12)
    np.testing.assert_allclose(actual_logdet, expected_logdet, rtol=1e-12, atol=1e-12)
    assert np.all(np.isfinite(actual_forward))
    assert np.all(np.isfinite(actual_logdet))
