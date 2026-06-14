from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

import tensorflow as tf
import tensorflow_probability as tfp

import bayesfilter.highdim as highdim


DTYPE = tf.float64
MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m5-hmc-tier2-leapfrog-manifest-2026-06-09.json"
)
RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m5-hmc-tier2-leapfrog-result-2026-06-09.md"
)
P50_HMC_MANIFEST = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p50-hmc-readiness-tier-manifest-2026-06-09.json"
)
P50_SV_MANIFEST = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p50-m5-sv-generalized-sv-ladder-manifest-2026-06-09.json"
)

_STD_NORMAL = tfp.distributions.Normal(
    loc=tf.constant(0.0, dtype=DTYPE),
    scale=tf.constant(1.0, dtype=DTYPE),
)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _quadratic_value(theta: tf.Tensor) -> tf.Tensor:
    center = tf.constant([0.25, -0.75], dtype=DTYPE)
    residual = tf.convert_to_tensor(theta, dtype=DTYPE) - center
    return -0.5 * tf.reduce_sum(tf.square(residual))


def _sv_observations() -> tf.Tensor:
    return tf.constant([[0.12], [-0.07]], dtype=DTYPE)


def _sv_theta() -> tf.Tensor:
    gamma = tf.constant([0.60], dtype=DTYPE)
    beta = tf.constant([0.40], dtype=DTYPE)
    return tf.reshape(tf.stack([_STD_NORMAL.quantile(gamma), tf.math.log(beta)], axis=1), [-1])


def _sv_value(theta: tf.Tensor) -> tf.Tensor:
    theta_matrix = tf.reshape(tf.convert_to_tensor(theta, dtype=DTYPE), [-1, 2])
    gamma = _STD_NORMAL.cdf(theta_matrix[:, 0])
    beta = tf.exp(theta_matrix[:, 1])
    sigma = tf.constant([1.00], dtype=DTYPE)
    return highdim.exact_transformed_sv_independent_panel_dense_reference(
        _sv_observations(),
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        order=401,
        radius=8.0,
    ).log_likelihood


def _value_and_score(value_fn: Callable[[tf.Tensor], tf.Tensor], theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
    theta = tf.convert_to_tensor(theta, dtype=DTYPE)
    with tf.GradientTape() as tape:
        tape.watch(theta)
        value = value_fn(theta)
    score = tape.gradient(value, theta)
    if score is None:
        raise AssertionError("score gradient is None")
    return tf.convert_to_tensor(value, dtype=DTYPE), tf.convert_to_tensor(score, dtype=DTYPE)


def _potential_and_grad(value_fn: Callable[[tf.Tensor], tf.Tensor], theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
    value, score = _value_and_score(value_fn, theta)
    return -value, -score


def _hamiltonian(value_fn: Callable[[tf.Tensor], tf.Tensor], theta: tf.Tensor, momentum: tf.Tensor) -> tf.Tensor:
    potential, _ = _potential_and_grad(value_fn, theta)
    return potential + 0.5 * tf.reduce_sum(tf.square(tf.convert_to_tensor(momentum, dtype=DTYPE)))


def _leapfrog(
    value_fn: Callable[[tf.Tensor], tf.Tensor],
    theta: tf.Tensor,
    momentum: tf.Tensor,
    *,
    step_size: float,
    num_steps: int,
) -> tuple[tf.Tensor, tf.Tensor]:
    q = tf.convert_to_tensor(theta, dtype=DTYPE)
    p = tf.convert_to_tensor(momentum, dtype=DTYPE)
    epsilon = tf.constant(step_size, dtype=DTYPE)
    _, grad = _potential_and_grad(value_fn, q)
    p = p - 0.5 * epsilon * grad
    for step_index in range(int(num_steps)):
        q = q + epsilon * p
        _, grad = _potential_and_grad(value_fn, q)
        if step_index == int(num_steps) - 1:
            p = p - 0.5 * epsilon * grad
        else:
            p = p - epsilon * grad
    return q, p


def _tier2_metrics(
    value_fn: Callable[[tf.Tensor], tf.Tensor],
    theta: tf.Tensor,
    momentum: tf.Tensor,
    *,
    step_size: float,
    num_steps: int,
) -> dict[str, float]:
    initial_hamiltonian = _hamiltonian(value_fn, theta, momentum)
    next_theta, next_momentum = _leapfrog(
        value_fn,
        theta,
        momentum,
        step_size=step_size,
        num_steps=num_steps,
    )
    final_hamiltonian = _hamiltonian(value_fn, next_theta, next_momentum)
    reverse_theta, reverse_momentum = _leapfrog(
        value_fn,
        next_theta,
        -next_momentum,
        step_size=step_size,
        num_steps=num_steps,
    )
    _, score = _value_and_score(value_fn, theta)
    return {
        "step_size": float(step_size),
        "num_steps": int(num_steps),
        "energy_error_abs": abs(float((final_hamiltonian - initial_hamiltonian).numpy())),
        "reversibility_position_inf": float(tf.reduce_max(tf.abs(reverse_theta - theta)).numpy()),
        "reversibility_momentum_inf": float(tf.reduce_max(tf.abs(reverse_momentum + momentum)).numpy()),
        "score_norm": float(tf.linalg.norm(score).numpy()),
    }


def test_p51_m5_manifest_tracks_p50_tier2_and_strict_sv_baseline() -> None:
    manifest = _manifest()
    p50_hmc = json.loads(P50_HMC_MANIFEST.read_text(encoding="utf-8"))
    p50_sv = json.loads(P50_SV_MANIFEST.read_text(encoding="utf-8"))
    p50_tiers = {row["tier"]: row for row in p50_hmc["tiers"]}
    sv_rows = {row["row_id"]: row for row in p50_sv["rows"]}

    assert manifest["schema_version"] == "p51.hmc_tier2_leapfrog.v1"
    assert manifest["status"] == "PASS_P51_M5_HMC_TIER2_LEAPFROG"
    assert manifest["source_p50_tier"] == "TIER_2_HAMILTONIAN_LEAPFROG"
    assert p50_tiers["TIER_2_HAMILTONIAN_LEAPFROG"]["pass_status"] == "not_run"
    assert manifest["strict_sv_baseline_row"] == "exact_transformed_sv_zhaocui_vs_dense_dim_1_2_3"
    assert sv_rows[manifest["strict_sv_baseline_row"]]["m4_class"] == "PASS_SAME_TARGET_VALUE_AND_GRADIENT"
    assert manifest["target_set"][1]["target_id"] == "p51_m5_exact_transformed_sv_dim1_dense_reference"


def test_p51_m5_recomputed_tier2_metrics_match_manifest_and_pass() -> None:
    manifest_targets = {row["target_id"]: row for row in _manifest()["target_set"]}
    cases = {
        "p51_m5_quadratic_harness_fixture": (
            _quadratic_value,
            tf.constant([0.10, -0.20], dtype=DTYPE),
            tf.constant([0.03, -0.04], dtype=DTYPE),
        ),
        "p51_m5_exact_transformed_sv_dim1_dense_reference": (
            _sv_value,
            _sv_theta(),
            tf.constant([0.02, -0.015], dtype=DTYPE),
        ),
    }

    for target_id, (value_fn, theta, momentum) in cases.items():
        target = manifest_targets[target_id]
        tolerances = target["tolerances"]
        for recorded, step_size in zip(target["metrics"], target["step_sizes"], strict=True):
            metrics = _tier2_metrics(
                value_fn,
                theta,
                momentum,
                step_size=step_size,
                num_steps=target["num_steps"],
            )
            assert metrics["energy_error_abs"] < tolerances["energy_error_abs_lt"]
            assert metrics["reversibility_position_inf"] < tolerances["reversibility_position_inf_lt"]
            assert metrics["reversibility_momentum_inf"] < tolerances["reversibility_momentum_inf_lt"]
            tf.debugging.assert_near(
                tf.constant(metrics["energy_error_abs"], dtype=DTYPE),
                tf.constant(recorded["energy_error_abs"], dtype=DTYPE),
                atol=1e-12,
                rtol=1e-12,
            )
            tf.debugging.assert_near(
                tf.constant(metrics["reversibility_position_inf"], dtype=DTYPE),
                tf.constant(recorded["reversibility_position_inf"], dtype=DTYPE),
                atol=1e-12,
                rtol=1e-12,
            )
            tf.debugging.assert_near(
                tf.constant(metrics["reversibility_momentum_inf"], dtype=DTYPE),
                tf.constant(recorded["reversibility_momentum_inf"], dtype=DTYPE),
                atol=1e-12,
                rtol=1e-12,
            )
        assert target["decision"] == "PASS_TIER2_LEAPFROG_DIAGNOSTIC"


def test_p51_m5_nonclaims_do_not_promote_sampler_or_production_hmc() -> None:
    manifest = _manifest()
    nonclaims = set(manifest["nonclaims"])

    assert manifest["promotion_boundary"]["finite_gradient_is_not_tier2"] is True
    assert manifest["promotion_boundary"]["quadratic_harness_is_not_model_evidence"] is True
    assert manifest["promotion_boundary"]["tier2_is_not_hmc_ready_without_tier3"] is True
    assert "no short-chain sampler health" in nonclaims
    assert "no production HMC readiness" in nonclaims
    assert "no GPU readiness" in nonclaims
    assert "no model production readiness" in nonclaims
    assert "no source-faithful adaptive TT/SIRT filtering" in nonclaims
    assert "no S&P 500 reproduction" in nonclaims


def test_p51_m5_result_emits_token_once_and_records_cpu_only_validation() -> None:
    text = RESULT_PATH.read_text(encoding="utf-8")

    assert text.count("status: PASS_P51_M5_HMC_TIER2_LEAPFROG") == 1
    assert "exact transformed SV dim-1 dense reference" in text
    assert "No short-chain sampler health" in text
    assert "CPU-only" in text
