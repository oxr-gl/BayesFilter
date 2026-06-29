from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import tensorflow as tf

import bayesfilter.highdim as highdim


DTYPE = tf.float64
FINAL_TIME = 4
SEEDS = tuple(range(9101, 9111))
PARAMETER_NAMES = (
    "log_kappa_scale",
    "log_nu_scale",
    "log_obs_noise_scale",
)
REGIMES = (
    ("baseline_moderate", (0.0, 0.0, 0.0)),
    ("low_infection", (-0.35, 0.15, 0.0)),
    ("high_infection", (0.25, -0.15, 0.1)),
    ("near_boundary_stable", (0.45, -0.35, 0.2)),
)
MANIFEST_PATH = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-manifest-2026-06-29.json"
)


def _git_commit() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return "UNKNOWN"
    return completed.stdout.strip()


def _score_for_dataset(
    model: highdim.ParameterizedZhaoCuiSIRSSM,
    theta: tf.Tensor,
    states: tf.Tensor,
    observations: tf.Tensor,
) -> tuple[tf.Tensor, dict[str, tf.Tensor]]:
    initial = model.initial_log_density_parameter_score(theta, states[0:1])[0]
    transition_terms = []
    for time_index in range(1, FINAL_TIME + 1):
        transition_terms.append(
            model.transition_log_density_parameter_score(
                theta,
                states[time_index - 1 : time_index],
                states[time_index : time_index + 1],
                t=time_index,
            )[0]
        )
    observation_terms = []
    for time_index in range(FINAL_TIME + 1):
        observation_terms.append(
            model.observation_log_density_parameter_score(
                theta,
                states[time_index : time_index + 1],
                observations[time_index],
                t=time_index,
            )[0]
        )
    transition = tf.reduce_sum(tf.stack(transition_terms, axis=0), axis=0)
    observation = tf.reduce_sum(tf.stack(observation_terms, axis=0), axis=0)
    total = initial + transition + observation
    return total, {
        "initial": initial,
        "transition": transition,
        "observation": observation,
        "total": total,
    }


def _to_float_list(values: tf.Tensor) -> list[float]:
    return [float(value) for value in tf.reshape(values, [-1]).numpy()]


def _regime_result(
    model: highdim.ParameterizedZhaoCuiSIRSSM,
    name: str,
    theta_values: tuple[float, float, float],
) -> dict[str, object]:
    theta = tf.constant(theta_values, dtype=DTYPE)
    rows: list[dict[str, object]] = []
    total_scores = []
    for seed in SEEDS:
        states, observations = model.scaled_model(theta).simulate(
            final_time=FINAL_TIME,
            seed=int(seed),
        )
        score, components = _score_for_dataset(model, theta, states, observations)
        total_scores.append(score)
        rows.append(
            {
                "seed": int(seed),
                "score": _to_float_list(score),
                "component_scores": {
                    key: _to_float_list(value) for key, value in components.items()
                },
                "min_state": float(tf.reduce_min(states).numpy()),
                "max_state": float(tf.reduce_max(states).numpy()),
            }
        )
    score_matrix = tf.stack(total_scores, axis=0)
    mean = tf.reduce_mean(score_matrix, axis=0)
    centered = score_matrix - mean[tf.newaxis, :]
    sample_variance = tf.reduce_sum(tf.square(centered), axis=0) / tf.cast(
        len(SEEDS) - 1,
        DTYPE,
    )
    sample_sd = tf.sqrt(sample_variance)
    standard_error = sample_sd / tf.sqrt(tf.cast(len(SEEDS), DTYPE))
    abs_mean = tf.abs(mean)
    zero_sd = sample_sd <= tf.constant(1.0e-15, dtype=DTYPE)
    component_pass = tf.where(
        zero_sd,
        abs_mean <= tf.constant(1.0e-12, dtype=DTYPE),
        abs_mean <= tf.constant(2.0, dtype=DTYPE) * sample_sd,
    )
    advisory_z = tf.where(
        standard_error > tf.constant(0.0, dtype=DTYPE),
        abs_mean / standard_error,
        tf.fill(tf.shape(abs_mean), tf.constant(float("inf"), dtype=DTYPE)),
    )
    finite = bool(tf.reduce_all(tf.math.is_finite(score_matrix)).numpy())
    passed = bool(finite and tf.reduce_all(component_pass).numpy())
    return {
        "regime": name,
        "theta": tuple(float(value) for value in theta_values),
        "seed_count": len(SEEDS),
        "seeds": SEEDS,
        "path_final_time": FINAL_TIME,
        "parameter_names": PARAMETER_NAMES,
        "per_seed": rows,
        "mean_score": _to_float_list(mean),
        "sample_standard_deviation": _to_float_list(sample_sd),
        "standard_error": _to_float_list(standard_error),
        "advisory_abs_mean_over_se": _to_float_list(advisory_z),
        "component_pass": [bool(value) for value in component_pass.numpy()],
        "all_finite": finite,
        "passed": passed,
    }


def test_p91_local_component_score_identity_at_true_theta() -> None:
    model = highdim.parameterized_zhao_cui_sir_austria_model()
    results = [
        _regime_result(model, name, theta_values)
        for name, theta_values in REGIMES
    ]
    status = (
        "PASS_P91_PHASE4_LOCAL_COMPONENT_SCORE_IDENTITY"
        if all(bool(result["passed"]) for result in results)
        else "BLOCK_P91_PHASE4_LOCAL_COMPONENT_SCORE_IDENTITY"
    )
    payload = {
        "schema_version": "p91.phase4.local_component_score_identity.v1",
        "status": status,
        "command": (
            "CUDA_VISIBLE_DEVICES=-1 python -m pytest "
            "tests/highdim/test_p81_analytical_sir_score.py::"
            "test_parameterized_sir_log_density_parameter_scores_match_diagnostic_tape "
            "tests/highdim/test_p91_score_identity.py -q"
        ),
        "git_commit": _git_commit(),
        "python_executable": sys.executable,
        "conda_environment": os.environ.get("CONDA_DEFAULT_ENV", "N/A"),
        "cpu_gpu_status": "CPU-only; CUDA_VISIBLE_DEVICES=-1 required by Phase 4",
        "data_generator": "model.scaled_model(theta_0).simulate(final_time=4, seed=seed)",
        "model_family": "ParameterizedZhaoCuiSIRSSM",
        "target_id": "zhao_cui_sir_austria_d18",
        "state_dimension": model.state_dim(),
        "observation_dimension": model.observation_dim(),
        "parameter_names": PARAMETER_NAMES,
        "score_scope": "local_complete_data_component_score",
        "regimes": results,
        "primary_criterion": (
            "for every regime and parameter component, "
            "abs(mean_score) <= 2 * sample_standard_deviation across 10 seeds"
        ),
        "advisory_diagnostics": (
            "standard_error",
            "advisory_abs_mean_over_se",
        ),
        "blocker_statuses_preserved": {
            "full_observed_data_filtering_score_identity": "NOT_CLAIMED",
            "previous_marginal_derivative": (
                "BLOCK_FIXED_TTSIRT_PREVIOUS_MARGINAL_DERIVATIVE_NOT_IMPLEMENTED"
            ),
            "fixed_ttsirt_transport_derivative": (
                "BLOCK_FIXED_TTSIRT_PROPOSAL_TRANSPORT_DERIVATIVE_NOT_IMPLEMENTED"
            ),
            "full_source_route_fd": "BLOCK_FULL_SOURCE_ROUTE_FD_NOT_CLAIMED",
        },
        "nonclaims": (
            "no exact likelihood proof",
            "no full observed-data filtering score identity",
            "no previous-marginal derivative readiness",
            "no fixed TTSIRT proposal/transport derivative readiness",
            "no GPU/XLA readiness",
            "no HMC readiness",
            "no benchmark result",
            "no package/release/CI readiness",
            "no default-policy authorization/change",
            "no production readiness",
        ),
    }
    MANIFEST_PATH.write_text(
        highdim.BranchManifest(
            version="p91.phase4.local_component_score_identity.manifest.v1",
            payload=payload,
        )
        .to_canonical_bytes()
        .decode("utf-8"),
        encoding="utf-8",
    )

    assert status == "PASS_P91_PHASE4_LOCAL_COMPONENT_SCORE_IDENTITY"
