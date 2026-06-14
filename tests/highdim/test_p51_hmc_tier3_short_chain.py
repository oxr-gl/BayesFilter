from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Callable

import tensorflow as tf
import tensorflow_probability as tfp

import bayesfilter.highdim as highdim


DTYPE = tf.float64
MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m6-hmc-tier3-short-chain-manifest-2026-06-09.json"
)
RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m6-hmc-tier3-short-chain-result-2026-06-09.md"
)
M5_MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m5-hmc-tier2-leapfrog-manifest-2026-06-09.json"
)

_STD_NORMAL = tfp.distributions.Normal(
    loc=tf.constant(0.0, dtype=DTYPE),
    scale=tf.constant(1.0, dtype=DTYPE),
)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _observations() -> tf.Tensor:
    return tf.constant([[0.12], [-0.07]], dtype=DTYPE)


def _initial_theta() -> tf.Tensor:
    gamma = tf.constant([0.60], dtype=DTYPE)
    beta = tf.constant([0.40], dtype=DTYPE)
    return tf.reshape(tf.stack([_STD_NORMAL.quantile(gamma), tf.math.log(beta)], axis=1), [-1])


def _likelihood_value(theta: tf.Tensor) -> tf.Tensor:
    theta = tf.reshape(tf.convert_to_tensor(theta, dtype=DTYPE), [2])
    gamma = _STD_NORMAL.cdf(theta[0:1])
    beta = tf.exp(theta[1:2])
    sigma = tf.constant([1.00], dtype=DTYPE)
    return highdim.exact_transformed_sv_independent_panel_dense_reference(
        _observations(),
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        order=401,
        radius=8.0,
    ).log_likelihood


def _prior_log_prob(theta: tf.Tensor) -> tf.Tensor:
    theta = tf.reshape(tf.convert_to_tensor(theta, dtype=DTYPE), [2])
    prior_mean = _initial_theta()
    prior_scale = tf.constant([1.0, 1.0], dtype=DTYPE)
    residual = (theta - prior_mean) / prior_scale
    return -0.5 * tf.reduce_sum(tf.square(residual)) - tf.reduce_sum(
        tf.math.log(prior_scale) + 0.5 * tf.math.log(tf.constant(2.0 * math.pi, dtype=DTYPE))
    )


def _target_log_prob(theta: tf.Tensor) -> tf.Tensor:
    return _likelihood_value(theta) + _prior_log_prob(theta)


def _logsumexp_weighted(log_values: tf.Tensor, weights: tf.Tensor) -> tf.Tensor:
    max_log = tf.reduce_max(log_values)
    return tf.math.log(tf.reduce_sum(weights * tf.exp(log_values - max_log))) + max_log


def _grid_reference(order: int = 31, half_width: float = 0.5) -> dict[str, object]:
    center = _initial_theta()
    nodes, weights_1d = highdim.legendre_gauss_nodes_weights(order)
    theta0 = center[0] + half_width * nodes
    theta1 = center[1] + half_width * nodes
    scale_weights = half_width * weights_1d
    mesh0, mesh1 = tf.meshgrid(theta0, theta1, indexing="ij")
    w0, w1 = tf.meshgrid(scale_weights, scale_weights, indexing="ij")
    points = tf.stack([tf.reshape(mesh0, [-1]), tf.reshape(mesh1, [-1])], axis=1)
    weights = tf.reshape(w0 * w1, [-1])
    log_values = tf.stack([_target_log_prob(point) for point in tf.unstack(points)], axis=0)
    log_z = _logsumexp_weighted(log_values, weights)
    normalized = weights * tf.exp(log_values - log_z)
    mean = tf.reduce_sum(normalized[:, tf.newaxis] * points, axis=0)
    centered = points - mean
    covariance = tf.einsum("n,ni,nj->ij", normalized, centered, centered)
    tail_boundary_log_ratio = tf.reduce_max(
        tf.stack(
            [
                log_values[tf.abs(points[:, 0] - center[0]) > half_width * 0.98],
                log_values[tf.abs(points[:, 1] - center[1]) > half_width * 0.98],
            ],
            axis=0,
        )
    ) - tf.reduce_max(log_values)
    return {
        "mean": mean,
        "covariance": covariance,
        "log_normalizer": log_z,
        "tail_boundary_log_ratio": tail_boundary_log_ratio,
        "grid_points": int(points.shape[0]),
    }


def _run_hmc(seed: int = 20260609) -> dict[str, object]:
    kernel = tfp.mcmc.HamiltonianMonteCarlo(
        target_log_prob_fn=_target_log_prob,
        step_size=tf.constant(0.015, dtype=DTYPE),
        num_leapfrog_steps=4,
    )
    samples, trace = tfp.mcmc.sample_chain(
        num_results=80,
        num_burnin_steps=40,
        current_state=_initial_theta(),
        kernel=kernel,
        seed=tf.constant([seed, seed + 1], dtype=tf.int32),
        trace_fn=lambda _, kernel_results: {
            "is_accepted": kernel_results.is_accepted,
            "log_accept_ratio": kernel_results.log_accept_ratio,
        },
    )
    samples = tf.convert_to_tensor(samples, dtype=DTYPE)
    mean = tf.reduce_mean(samples, axis=0)
    centered = samples - mean
    covariance = tf.matmul(centered, centered, transpose_a=True) / tf.cast(tf.shape(samples)[0] - 1, DTYPE)
    return {
        "samples": samples,
        "mean": mean,
        "covariance": covariance,
        "acceptance_rate": tf.reduce_mean(tf.cast(trace["is_accepted"], DTYPE)),
        "max_abs_log_accept_ratio": tf.reduce_max(tf.abs(trace["log_accept_ratio"])),
        "nonfinite_sample_count": tf.reduce_sum(tf.cast(~tf.math.is_finite(samples), tf.int32)),
    }


def _metrics() -> dict[str, object]:
    reference = _grid_reference()
    chain = _run_hmc()
    mean_error_inf = tf.reduce_max(tf.abs(chain["mean"] - reference["mean"]))
    covariance_error_inf = tf.reduce_max(tf.abs(chain["covariance"] - reference["covariance"]))
    return {
        "reference_mean": [float(value) for value in reference["mean"].numpy()],
        "reference_covariance": reference["covariance"].numpy().tolist(),
        "reference_log_normalizer": float(reference["log_normalizer"].numpy()),
        "reference_tail_boundary_log_ratio": float(reference["tail_boundary_log_ratio"].numpy()),
        "reference_grid_points": reference["grid_points"],
        "sample_mean": [float(value) for value in chain["mean"].numpy()],
        "sample_covariance": chain["covariance"].numpy().tolist(),
        "acceptance_rate": float(chain["acceptance_rate"].numpy()),
        "max_abs_log_accept_ratio": float(chain["max_abs_log_accept_ratio"].numpy()),
        "nonfinite_sample_count": int(chain["nonfinite_sample_count"].numpy()),
        "mean_error_inf": float(mean_error_inf.numpy()),
        "covariance_error_inf": float(covariance_error_inf.numpy()),
    }


def test_p51_m6_manifest_uses_same_target_that_passed_m5_tier2() -> None:
    manifest = _manifest()
    m5 = json.loads(M5_MANIFEST_PATH.read_text(encoding="utf-8"))
    m5_targets = {row["target_id"]: row for row in m5["target_set"]}

    assert manifest["schema_version"] == "p51.hmc_tier3_short_chain.v1"
    assert manifest["status"] == "BLOCK_P51_M6_HMC_TIER3_SHORT_CHAIN"
    assert manifest["source_p51_tier2_phase"] == "P51-M5"
    assert manifest["target_id"] == "p51_m5_exact_transformed_sv_dim1_dense_reference"
    assert m5_targets[manifest["target_id"]]["decision"] == "PASS_TIER2_LEAPFROG_DIAGNOSTIC"
    assert manifest["posterior_reference"]["route"] == "deterministic two-dimensional quadrature"


def test_p51_m6_blocker_records_failed_posterior_reference_vetoes() -> None:
    manifest = _manifest()
    metrics = manifest["metrics"]
    tolerances = manifest["tolerances"]

    assert metrics["nonfinite_sample_count"] == 0
    assert metrics["acceptance_rate"] >= tolerances["acceptance_rate_between"][0]
    assert metrics["acceptance_rate"] <= tolerances["acceptance_rate_between"][1]
    assert metrics["mean_error_inf"] > tolerances["mean_error_inf_lt"]
    assert metrics["covariance_error_inf"] < tolerances["covariance_error_inf_lt"]
    assert metrics["reference_tail_boundary_log_ratio"] >= tolerances["reference_tail_boundary_log_ratio_lt"]
    assert manifest["decision"] == "BLOCK_TIER3_SHORT_CHAIN_DIAGNOSTIC"
    assert "mean_error_inf was 0.19210895764534353" in manifest["blocker_reason"]
    assert "reference_tail_boundary_log_ratio was 0.0" in manifest["blocker_reason"]
    disposition = manifest["predeclared_criteria_disposition"]
    assert disposition["finite_sample"] == "passed_nonfinite_sample_count_eq_0"
    assert disposition["acceptance"] == "passed_acceptance_rate_between_0p5_and_1p0"
    assert disposition["posterior_reference"] == "failed_mean_error_and_reference_tail_boundary_support"
    assert disposition["divergence"] == "not_assessed_after_posterior_reference_veto"
    assert disposition["reproducibility"] == "not_assessed_after_posterior_reference_veto"


def test_p51_m6_nonclaims_do_not_promote_production_or_gpu_hmc() -> None:
    manifest = _manifest()
    nonclaims = set(manifest["nonclaims"])

    assert manifest["promotion_boundary"]["short_chain_is_not_production_hmc_ready"] is True
    assert manifest["promotion_boundary"]["single_seed_short_chain_scope"] == "diagnostic_only"
    assert manifest["promotion_boundary"]["cpu_only_is_not_gpu_readiness"] is True
    assert "no production HMC readiness" in nonclaims
    assert "no GPU readiness" in nonclaims
    assert "no broad sampler convergence" in nonclaims
    assert "no model production readiness" in nonclaims
    assert "no source-faithful adaptive TT/SIRT filtering" in nonclaims
    assert "no S&P 500 reproduction" in nonclaims


def test_p51_m6_result_emits_token_once_and_records_reference_check() -> None:
    text = RESULT_PATH.read_text(encoding="utf-8")

    assert text.count("status: BLOCK_P51_M6_HMC_TIER3_SHORT_CHAIN") == 1
    assert "posterior/reference" in text
    assert "No production HMC readiness" in text
