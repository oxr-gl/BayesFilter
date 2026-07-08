"""Phase 7 CPU ladder for the actual-SV analytical SR-UKF score."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import tensorflow as tf

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bayesfilter.highdim.actual_sv_srukf_tf import (
    actual_transformed_sv_independent_panel_augmented_noise_srukf_score,
)


DEFAULT_JSON = Path(
    "docs/plans/bayesfilter-srukf-actual-sv-score-phase7-score-true-consistency-2026-07-01.json"
)
DEFAULT_MARKDOWN = Path(
    "docs/plans/bayesfilter-srukf-actual-sv-score-phase7-score-true-consistency-2026-07-01.md"
)


def _git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _simulate_actual_sv(
    *,
    seed: int,
    time_count: int,
    gamma: float,
    beta: float,
    sigma: float,
) -> tf.Tensor:
    rng = np.random.default_rng(int(seed))
    stationary_sd = sigma / np.sqrt(1.0 - gamma**2)
    previous_h = rng.normal(0.0, stationary_sd)
    observations = []
    for _ in range(int(time_count)):
        h_t = gamma * previous_h + sigma * rng.normal()
        y_t = beta * np.exp(0.5 * h_t) * rng.normal()
        observations.append(y_t)
        previous_h = h_t
    return tf.reshape(tf.constant(observations, dtype=tf.float64), [-1, 1])


def _score_case(case: dict[str, Any]) -> dict[str, Any]:
    scores = []
    values = []
    diagnostics = []
    for seed in case["seeds"]:
        observations = _simulate_actual_sv(
            seed=int(seed),
            time_count=int(case["time_count"]),
            gamma=float(case["gamma"]),
            beta=float(case["beta"]),
            sigma=float(case["sigma"]),
        )
        result = actual_transformed_sv_independent_panel_augmented_noise_srukf_score(
            observations,
            gamma=float(case["gamma"]),
            beta=float(case["beta"]),
            sigma=float(case["sigma"]),
        )
        scores.append(result.score.numpy())
        values.append(float(result.log_likelihood.numpy()))
        diagnostics.append(
            {
                "max_factor_reconstruction_residual": result.diagnostics[
                    "max_factor_reconstruction_residual"
                ],
                "max_factor_derivative_residual": result.diagnostics[
                    "max_factor_derivative_residual"
                ],
                "max_innovation_solve_residual": result.diagnostics[
                    "max_innovation_solve_residual"
                ],
            }
        )

    score_array = np.asarray(scores, dtype=float)
    mean = score_array.mean(axis=0)
    sample_sd = score_array.std(axis=0, ddof=1)
    standard_error = sample_sd / np.sqrt(score_array.shape[0])
    z_score = np.divide(
        mean,
        standard_error,
        out=np.zeros_like(mean),
        where=standard_error > 0.0,
    )
    pass_by_coordinate = np.abs(mean) <= 2.0 * standard_error
    tiny_se = standard_error <= 1e-12
    pass_by_coordinate = np.where(tiny_se, np.abs(mean) <= 1e-10, pass_by_coordinate)
    return {
        "case_id": case["case_id"],
        "gamma": float(case["gamma"]),
        "beta": float(case["beta"]),
        "sigma": float(case["sigma"]),
        "time_count": int(case["time_count"]),
        "seeds": list(case["seeds"]),
        "score_parameterization": ["theta_gamma", "theta_beta"],
        "score_mean": mean.tolist(),
        "score_sample_sd": sample_sd.tolist(),
        "score_standard_error": standard_error.tolist(),
        "score_z": z_score.tolist(),
        "pass_by_coordinate": [bool(value) for value in pass_by_coordinate],
        "passed": bool(np.all(pass_by_coordinate)),
        "average_log_likelihood": float(np.mean(values)),
        "max_factor_reconstruction_residual": float(
            max(entry["max_factor_reconstruction_residual"] for entry in diagnostics)
        ),
        "max_factor_derivative_residual": float(
            max(entry["max_factor_derivative_residual"] for entry in diagnostics)
        ),
        "max_innovation_solve_residual": float(
            max(entry["max_innovation_solve_residual"] for entry in diagnostics)
        ),
    }


def _default_cases() -> list[dict[str, Any]]:
    seeds = tuple(range(10))
    return [
        {
            "case_id": "actual_sv_moderate_persistence",
            "gamma": 0.55,
            "beta": 0.90,
            "sigma": 0.22,
            "time_count": 25,
            "seeds": seeds,
        },
        {
            "case_id": "actual_sv_higher_persistence",
            "gamma": 0.75,
            "beta": 1.10,
            "sigma": 0.35,
            "time_count": 25,
            "seeds": seeds,
        },
    ]


def _write_markdown(payload: dict[str, Any], path: Path) -> None:
    lines = [
        "# Phase 7 Actual-SV SR-UKF Score-At-True Consistency",
        "",
        f"Status: {'PASSED' if payload['passed'] else 'FAILED'}",
        "",
        "## Evidence Contract",
        "",
        "- Question: is the average analytical SR-UKF score at the true parameter",
        "  compatible with zero across 10 independently simulated datasets?",
        "- Primary criterion: every coordinate mean lies within two standard errors",
        "  of zero, with a tiny-standard-error absolute fallback of `1e-10`.",
        "- Not concluded: exact likelihood correctness, HMC readiness, GPU/XLA",
        "  readiness, or leaderboard admission.",
        "- Warning: the cubature SR-UKF actual-SV route can make the gamma score",
        "  nearly zero structurally; this passes the consistency gate but is weak",
        "  evidence about gamma information in the surrogate.",
        "",
        "## Manifest",
        "",
        f"- Git commit: `{payload['git_commit']}`",
        f"- CPU/GPU status: `{payload['cpu_gpu_status']}`",
        f"- Command: `{payload['command']}`",
        "",
        "## Results",
        "",
        "| Case | Param | Mean | SE | z | Pass |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for case in payload["cases"]:
        for index, parameter in enumerate(case["score_parameterization"]):
            lines.append(
                "| {case_id} | {parameter} | {mean:.6g} | {se:.6g} | {z:.6g} | {passed} |".format(
                    case_id=case["case_id"],
                    parameter=parameter,
                    mean=case["score_mean"][index],
                    se=case["score_standard_error"][index],
                    z=case["score_z"][index],
                    passed=case["pass_by_coordinate"][index],
                )
            )
    lines.extend(
        [
            "",
            "## Route Boundary",
            "",
            "- Admitted score route: `factor_propagating_srukf_manual_score`.",
            "- Forbidden families remain excluded: `GradientTape`,",
            "  `tf_svd_sigma_point_filter`, historical SVD/eigenderivative",
            "  derivatives, and strict-SPD principal-root derivative helpers.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    start = time.perf_counter()
    cases = [_score_case(case) for case in _default_cases()]
    payload = {
        "schema_version": "actual_sv_srukf_phase7_score_true.v1",
        "git_commit": _git_commit(),
        "command": "CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_actual_sv_srukf_phase7_ladder.py",
        "cpu_gpu_status": "CPU-only; CUDA_VISIBLE_DEVICES=-1 set before TensorFlow import by caller",
        "cases": cases,
        "passed": bool(all(case["passed"] for case in cases)),
        "wall_time_seconds": time.perf_counter() - start,
        "nonclaims": [
            "not exact actual-SV likelihood",
            "not same-target transformed likelihood",
            "not leaderboard admission",
            "not HMC readiness",
            "not GPU/XLA readiness",
        ],
    }
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_markdown(payload, args.markdown_output)
    if not payload["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
