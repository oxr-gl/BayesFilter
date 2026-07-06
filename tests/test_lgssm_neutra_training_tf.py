from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import json

import tensorflow as tf

from bayesfilter.inference import load_frozen_neutra_artifact
from bayesfilter.ssm import stable_ssm_target_signature
from bayesfilter.testing.lgssm_generic_target_adapter_tf import (
    make_lgssm_generic_target_fixture,
)
from bayesfilter.testing.lgssm_neutra_training_tf import (
    LGSSMAffineNeuTraTrainingConfig,
    LGSSM_NEUTRA_TRAINING_NONCLAIMS,
    train_and_validate_lgssm_affine_neutra,
)


def test_lgssm_affine_neutra_training_writes_reloadable_payload(tmp_path) -> None:
    artifact_dir = tmp_path / "artifacts"
    validation_path = tmp_path / "validation.json"

    result = train_and_validate_lgssm_affine_neutra(
        LGSSMAffineNeuTraTrainingConfig(
            seed=20260707,
            steps=4,
            batch_size=8,
            learning_rate=0.01,
            artifact_dir=artifact_dir,
            validation_path=validation_path,
        )
    )

    assert result.training_state_path.exists()
    assert result.payload_path.exists()
    assert result.validation_path.exists()
    assert result.training_state["schema"] == (
        "bayesfilter.lgssm_affine_neutra_training_state.v1"
    )
    assert result.frozen_payload["schema"] == "bayesfilter.neutra.frozen_affine_diag.v1"
    assert result.frozen_payload["dimension"] == 2
    assert result.frozen_payload["target_signature"] == result.target_signature
    assert result.validation["passed"] is True
    assert result.validation["training_summary"]["loss_is_explanatory_only"] is True
    assert result.training_state["nonclaims"] == LGSSM_NEUTRA_TRAINING_NONCLAIMS

    payload_from_disk = json.loads(result.payload_path.read_text(encoding="utf-8"))
    fixture = make_lgssm_generic_target_fixture()
    expected_signature = stable_ssm_target_signature(fixture.contract)
    artifact = load_frozen_neutra_artifact(
        payload_from_disk,
        expected_target_signature=expected_signature,
    )
    z = tf.constant([[0.0, 0.0], [0.10, -0.15]], dtype=tf.float64)
    theta = artifact.transport.forward_batch(z)

    assert artifact.manifest.target_signature == expected_signature
    assert theta.shape == (2, 2)
    assert bool(tf.reduce_all(tf.math.is_finite(theta)).numpy()) is True


def test_lgssm_affine_neutra_training_is_deterministic_for_fixed_seed(tmp_path) -> None:
    left = train_and_validate_lgssm_affine_neutra(
        LGSSMAffineNeuTraTrainingConfig(
            seed=20260707,
            steps=3,
            batch_size=6,
            learning_rate=0.01,
            artifact_dir=tmp_path / "left",
            validation_path=tmp_path / "left-validation.json",
        )
    )
    right = train_and_validate_lgssm_affine_neutra(
        LGSSMAffineNeuTraTrainingConfig(
            seed=20260707,
            steps=3,
            batch_size=6,
            learning_rate=0.01,
            artifact_dir=tmp_path / "right",
            validation_path=tmp_path / "right-validation.json",
        )
    )

    assert left.training_state["final_shift"] == right.training_state["final_shift"]
    assert left.training_state["final_raw_scale"] == right.training_state["final_raw_scale"]
    assert left.training_state["loss_history"] == right.training_state["loss_history"]
    assert left.frozen_payload["shift"] == right.frozen_payload["shift"]
    assert left.frozen_payload["raw_scale"] == right.frozen_payload["raw_scale"]


def test_lgssm_affine_neutra_training_preserves_reference_residuals(tmp_path) -> None:
    result = train_and_validate_lgssm_affine_neutra(
        LGSSMAffineNeuTraTrainingConfig(
            seed=20260707,
            steps=2,
            batch_size=4,
            learning_rate=0.01,
            artifact_dir=tmp_path / "artifacts",
            validation_path=tmp_path / "validation.json",
        )
    )

    residuals = result.validation["reference_residuals"]
    assert residuals["initial_batch_value_residual"] <= 1.0e-10
    assert residuals["initial_batch_score_residual"] <= 1.0e-8
    assert result.validation["finite_checks"] == {
        "base_values_finite": True,
        "base_scores_finite": True,
        "mechanics_value_finite": True,
        "mechanics_score_finite": True,
    }
