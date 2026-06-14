#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import tensorflow as tf


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bayesfilter.highdim.models import (
    LinearGaussianSSM,
    StochasticVolatilitySSM,
    p30_predator_prey_fixture_model,
    zhao_cui_sir_austria_model,
)
from bayesfilter.highdim.sv_mixture_cut4 import transformed_sv_observations


STATUS_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-blocker-closure-status-2026-06-11.json"
)
SOURCE_SCOPE_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json"
)
DEFAULT_JSON = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.json"
)
DEFAULT_CSV = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.csv"
)
DEFAULT_MD = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.md"
)


DATASET_ROWS = [
    {
        "model_row_id": "benchmark_lgssm_exact_oracle_m3_T50",
        "status": "generate",
        "seed": 81100,
    },
    {
        "model_row_id": "zhao_cui_sv_actual_nongaussian_T1000",
        "status": "generate",
        "seed": 81101,
    },
    {
        "model_row_id": "zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000",
        "status": "derive_from_actual_sv",
        "source_model_row_id": "zhao_cui_sv_actual_nongaussian_T1000",
        "transform_offset": 1e-8,
    },
    {
        "model_row_id": "zhao_cui_spatial_sir_austria_j9_T20",
        "status": "generate",
        "seed": 81103,
    },
    {
        "model_row_id": "zhao_cui_predator_prey_T20",
        "status": "generate",
        "seed": 81104,
    },
    {
        "model_row_id": "zhao_cui_generalized_sv_synthetic_from_estimated_values",
        "status": "generate",
        "seed": 81105,
    },
]


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _tensor_summary(tensor: tf.Tensor) -> dict[str, Any]:
    value = tf.convert_to_tensor(tensor, dtype=tf.float64)
    raw = tf.io.serialize_tensor(value).numpy()
    return {
        "shape": [int(dim) for dim in value.shape],
        "dtype": value.dtype.name,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "mean": float(tf.reduce_mean(value).numpy()),
        "stddev": float(tf.math.reduce_std(value).numpy()),
        "min": float(tf.reduce_min(value).numpy()),
        "max": float(tf.reduce_max(value).numpy()),
        "all_finite": bool(tf.reduce_all(tf.math.is_finite(value)).numpy()),
    }


def _lgssm_benchmark_model() -> LinearGaussianSSM:
    phi = tf.constant([0.72, 0.55, 0.35], dtype=tf.float64)
    q_scale = tf.constant(0.35, dtype=tf.float64)
    r_scale = tf.constant(0.45, dtype=tf.float64)
    initial_variance = tf.square(q_scale) / (1.0 - tf.square(phi))
    return LinearGaussianSSM(
        initial_mean=tf.zeros([3], dtype=tf.float64),
        initial_covariance=tf.linalg.diag(initial_variance),
        transition_matrix=tf.linalg.diag(phi),
        transition_covariance=tf.square(q_scale) * tf.eye(3, dtype=tf.float64),
        observation_matrix=tf.constant(
            [
                [1.0, 0.25, -0.15],
                [0.2, 1.1, 0.3],
                [-0.1, 0.35, 0.9],
            ],
            dtype=tf.float64,
        ),
        observation_covariance=tf.square(r_scale) * tf.eye(3, dtype=tf.float64),
    )


def _lgssm_dataset(seed: int) -> dict[str, Any]:
    model = _lgssm_benchmark_model()
    generator = tf.random.Generator.from_seed(int(seed))
    initial_chol = tf.linalg.cholesky(model.initial_covariance)
    process_chol = tf.linalg.cholesky(model.transition_covariance)
    observation_chol = tf.linalg.cholesky(model.observation_covariance)
    state = model.initial_mean + tf.linalg.matvec(
        initial_chol,
        generator.normal([model.state_dim()], dtype=tf.float64),
    )
    states = [state]
    observations = [
        model.observation_offset
        + tf.linalg.matvec(model.observation_matrix, state)
        + tf.linalg.matvec(
            observation_chol,
            generator.normal([model.observation_dim()], dtype=tf.float64),
        )
    ]
    for _time_index in range(1, 50):
        state = (
            model.transition_offset
            + tf.linalg.matvec(model.transition_matrix, state)
            + tf.linalg.matvec(
                process_chol,
                generator.normal([model.state_dim()], dtype=tf.float64),
            )
        )
        states.append(state)
        observations.append(
            model.observation_offset
            + tf.linalg.matvec(model.observation_matrix, state)
            + tf.linalg.matvec(
                observation_chol,
                generator.normal([model.observation_dim()], dtype=tf.float64),
            )
        )
    return {
        "truth_theta_coordinate": "physical_benchmark_exact_oracle",
        "truth_physical": {
            "phi": [0.72, 0.55, 0.35],
            "q_scale": 0.35,
            "r_scale": 0.45,
        },
        "truth_theta": [0.72, 0.55, 0.35, 0.35, 0.45],
        "states": tf.stack(states),
        "observations": tf.stack(observations),
        "model_manifest": model.manifest_payload()
        | {
            "benchmark_policy": (
                "explicit identifiable exact-oracle LGSSM; not a Zhao-Cui "
                "MATLAB rng(0) reproduction"
            ),
            "identifiability_diagnostics": {
                "observation_matrix_rank": int(
                    tf.linalg.matrix_rank(model.observation_matrix).numpy()
                ),
                "transition_spectral_radius": 0.72,
            },
        },
    }


def _sv_dataset(seed: int) -> dict[str, Any]:
    model = StochasticVolatilitySSM(sigma=1.0)
    theta = model.unconstrained_from_physical(gamma=0.6, beta=0.4)
    states, observations = model.simulate(theta=theta, final_time=999, seed=seed)
    return {
        "truth_theta_coordinate": "synthetic_unconstrained",
        "truth_physical": {"gamma": 0.6, "beta": 0.4, "sigma": 1.0},
        "truth_theta": [float(x) for x in theta.numpy().tolist()],
        "states": states,
        "observations": observations,
        "model_manifest": model.manifest_payload(),
    }


def _sir_dataset(seed: int) -> dict[str, Any]:
    model = zhao_cui_sir_austria_model()
    states, observations = model.simulate(final_time=19, seed=seed)
    return {
        "truth_theta_coordinate": "no_free_theta",
        "truth_physical": {"kappa": [0.1] * 9, "nu": [18.0] * 9},
        "truth_theta": [],
        "states": states,
        "observations": observations,
        "model_manifest": model.manifest_payload(),
        "domain_diagnostics": model.domain_diagnostics(states),
    }


def _predator_prey_dataset(seed: int) -> dict[str, Any]:
    model = p30_predator_prey_fixture_model()
    theta = model.true_parameters()
    states, observations = model.simulate(theta=theta, final_time=19, seed=seed)
    return {
        "truth_theta_coordinate": "physical",
        "truth_physical": {
            "r": 0.6,
            "K": 114.0,
            "a": 25.0,
            "s": 0.3,
            "u": 0.5,
            "v": 0.5,
        },
        "truth_theta": [float(x) for x in theta.numpy().tolist()],
        "states": states,
        "observations": observations,
        "model_manifest": model.manifest_payload(),
        "domain_diagnostics": model.domain_diagnostics(states),
    }


def _standard_normal_quantile(probability: float) -> float:
    p = tf.constant(float(probability), dtype=tf.float64)
    value = tf.sqrt(tf.constant(2.0, dtype=tf.float64)) * tf.math.erfinv(2.0 * p - 1.0)
    return float(value.numpy())


def _generalized_sv_prior_mean_dataset(seed: int) -> dict[str, Any]:
    gamma = tf.constant(2.0 * 20.0 / 21.5 - 1.0, dtype=tf.float64)
    tau = tf.constant(math.sqrt(0.005 * math.pi), dtype=tf.float64)
    mu = tf.constant(0.0, dtype=tf.float64)
    horizon = 1008
    generator = tf.random.Generator.from_seed(int(seed))
    stationary_scale = tf.math.rsqrt(1.0 - tf.square(gamma))
    state = mu + stationary_scale * generator.normal([], dtype=tf.float64)
    states = []
    observations = []
    for _time_index in range(horizon):
        state = (
            mu
            + gamma * (state - mu)
            + generator.normal([], dtype=tf.float64)
        )
        variance = tf.exp(tau * state)
        observation = tf.sqrt(variance) * generator.normal([], dtype=tf.float64)
        states.append(state)
        observations.append(tf.reshape(observation, [1]))
    states_tensor = tf.reshape(tf.stack(states), [horizon, 1])
    observations_tensor = tf.stack(observations)
    z_gamma = _standard_normal_quantile(float(gamma.numpy()))
    log_tau = float(tf.math.log(tau).numpy())
    return {
        "truth_theta_coordinate": "source_route_active_transformed_prior_mean",
        "truth_physical": {
            "gamma": float(gamma.numpy()),
            "tau_or_sigma": float(tau.numpy()),
            "mu_or_log_beta_center_coordinate": 0.0,
            "phi": 0.0,
            "a": 0.0,
            "delta": 0.0,
            "nu1": "inf",
            "nu2": "inf",
        },
        "truth_theta": [z_gamma, log_tau, 0.0],
        "states": states_tensor,
        "observations": observations_tensor,
        "model_manifest": {
            "family": "ZhaoCuiSVModelsGeneralizedSVPriorMeanSynthetic",
            "source_route": "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels",
            "paper_anchor": "Zhao-Cui Section 6.2 S&P 500 prior distribution",
            "state_dimension": 1,
            "observation_dimension": 1,
            "horizon": horizon,
            "active_estimated_parameters": ["gamma", "tau", "mu"],
            "fixed_context": {"phi": 0.0, "a": 0.0, "delta": 0.0, "nu1": "inf", "nu2": "inf"},
            "prior_mean_convention": (
                "finite-coordinate prior center: E[(gamma+1)/2], E[sigma], "
                "and zero center for log(beta)/sigma or source mu/tau coordinate"
            ),
            "paper_priors": {
                "(gamma+1)/2": "Beta(20, 1.5)",
                "sigma_squared": "IG(1, 0.005)",
                "log_beta_given_sigma": "Normal(0, sigma^2 / 0.8)",
            },
            "simulation_equations": {
                "initial_state": "x0 ~ Normal(0, 1 / (1 - gamma^2)) in source-route scaled coordinates",
                "transition": "x_t = mu + gamma * (x_{t-1} - mu) + Normal(0, 1)",
                "variance": "v_t = exp(tau * x_t) because delta=0",
                "observation": "y_t = sqrt(v_t) * Normal(0, 1) because nu2=inf",
            },
            "coordinate_caveat": (
                "The paper writes log(beta)/sigma as the third transformed "
                "coordinate; the mirrored svmodels code names the third active "
                "coordinate mu. The prior-center value is zero under both labels."
            ),
            "what_is_not_claimed": [
                "not a posterior estimate from SP500 returns",
                "not a direct SP500 benchmark-data row",
                "not a claim that E[sigma^2] or ordinary E[beta] is finite",
                "not evaluator correctness evidence",
                "not filter performance evidence",
            ],
        },
    }


def _convert_for_json(value: Any) -> Any:
    if isinstance(value, tf.Tensor):
        tensor = tf.convert_to_tensor(value)
        if tensor.shape.rank == 0:
            item = tensor.numpy().item()
            if isinstance(item, bytes):
                return item.decode("utf-8")
            return item
        return tensor.numpy().tolist()
    if isinstance(value, dict):
        return {str(key): _convert_for_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_convert_for_json(item) for item in value]
    return value


def _dataset_record(row: dict[str, Any], generated: dict[str, dict[str, Any]]) -> dict[str, Any]:
    row_id = row["model_row_id"]
    status = row["status"]
    if status == "derive_from_actual_sv":
        source = generated[row["source_model_row_id"]]
        transformed = transformed_sv_observations(
            source["observations"],
            offset=float(row["transform_offset"]),
        )
        return {
            "model_row_id": row_id,
            "dataset_status": "generated",
            "blocker_token": None,
            "reason": None,
            "source_model_row_id": row["source_model_row_id"],
            "transform": "log(y_t^2 + offset)",
            "transform_offset": float(row["transform_offset"]),
            "horizon": int(transformed.shape[0]),
            "seed": source["seed"],
            "observation_summary": _tensor_summary(transformed),
            "state_summary": _tensor_summary(source["states"]),
            "truth_physical": source["truth_physical"],
            "truth_theta_coordinate": source["truth_theta_coordinate"],
            "truth_theta": source["truth_theta"],
            "nonclaims": ["not exact native SV likelihood", "surrogate observation target"],
        }

    seed = int(row["seed"])
    if row_id == "benchmark_lgssm_exact_oracle_m3_T50":
        payload = _lgssm_dataset(seed)
    elif row_id == "zhao_cui_sv_actual_nongaussian_T1000":
        payload = _sv_dataset(seed)
    elif row_id == "zhao_cui_spatial_sir_austria_j9_T20":
        payload = _sir_dataset(seed)
    elif row_id == "zhao_cui_predator_prey_T20":
        payload = _predator_prey_dataset(seed)
    elif row_id == "zhao_cui_generalized_sv_synthetic_from_estimated_values":
        payload = _generalized_sv_prior_mean_dataset(seed)
    else:
        raise ValueError(f"unknown generated dataset row: {row_id}")
    payload["seed"] = seed
    generated[row_id] = payload
    record = {
        "model_row_id": row_id,
        "dataset_status": "generated",
        "blocker_token": None,
        "reason": None,
        "horizon": int(payload["observations"].shape[0]),
        "seed": seed,
        "observation_summary": _tensor_summary(payload["observations"]),
        "state_summary": _tensor_summary(payload["states"]),
        "truth_physical": payload["truth_physical"],
        "truth_theta_coordinate": payload["truth_theta_coordinate"],
        "truth_theta": payload["truth_theta"],
        "model_manifest": _convert_for_json(payload["model_manifest"]),
        "nonclaims": ["not a filter performance result", "not a ranking"],
    }
    if row_id == "benchmark_lgssm_exact_oracle_m3_T50":
        record["nonclaims"].append("not a Zhao-Cui MATLAB C reproduction")
    if row_id == "zhao_cui_generalized_sv_synthetic_from_estimated_values":
        record["nonclaims"].extend(
            [
                "not a posterior estimate from SP500 returns",
                "not a direct SP500 benchmark-data row",
                "not an ordinary finite-mean claim for sigma_squared_or_beta",
            ]
        )
    if "domain_diagnostics" in payload:
        record["domain_diagnostics"] = _convert_for_json(payload["domain_diagnostics"])
    return record


def build_artifact() -> dict[str, Any]:
    source_scope = _load(SOURCE_SCOPE_PATH)
    generated: dict[str, dict[str, Any]] = {}
    records = [_dataset_record(row, generated) for row in DATASET_ROWS]
    status_counts: dict[str, int] = {}
    for record in records:
        key = str(record["dataset_status"])
        status_counts[key] = status_counts.get(key, 0) + 1
    return {
        "schema_version": "filter_bench.p8_synthetic_datasets.v1",
        "metadata_date": "2026-06-11",
        "phase": "FILTER_BENCH_P8_B2_SYNTHETIC_DATASETS",
        "status": "PASS_P8_B2_SYNTHETIC_DATASET_MANIFEST_READY_WITH_NUMERIC_EVALUATORS_PENDING",
        "numeric_benchmark_status": "BLOCK_P8_NUMERIC_BENCHMARK_NOT_YET_RUN",
        "purpose": (
            "Generate reproducible synthetic dataset manifests for P8 source-paper "
            "rows whose truth/test point and source generator are available."
        ),
        "source_artifacts": {
            "blocker_status": _rel(STATUS_PATH),
            "source_scope_contract": _rel(SOURCE_SCOPE_PATH),
        },
        "source_scope_row_ids": source_scope["source_scope_row_ids"],
        "dataset_records": records,
        "dataset_status_counts": status_counts,
        "ready_for_numeric_benchmark": False,
        "reason_not_ready": (
            "Evaluator/adapter, horizon, seed, and reviewed numeric table phases "
            "remain incomplete."
        ),
        "benchmark_guardrails": {
            "p44_rows_promoted": False,
            "author_defaults_as_generalized_sv_truth_allowed": False,
            "sp500_returns_as_benchmark_observations_allowed": False,
            "zhao_cui_lgssm_matlab_C_claim_allowed": False,
            "old_ledh_pfpf_ot_current_evidence_allowed": False,
            "old_sir_local_operator_route_allowed": False,
            "dpf_ranking_before_mc_se_allowed": False,
            "protocol_gate_counts_as_numeric_benchmark_allowed": False,
        },
        "nonclaims": [
            "not a numeric benchmark result",
            "not a filter ranking",
            "not evaluator correctness evidence",
            "not generalized-SV evaluator correctness evidence",
            "not SIR d=18 source-route validation success",
        ],
    }


def _write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    columns = [
        "model_row_id",
        "dataset_status",
        "blocker_token",
        "horizon",
        "seed",
        "observation_sha256",
        "state_sha256",
        "reason",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for record in records:
            obs = record.get("observation_summary") or {}
            state = record.get("state_summary") or {}
            writer.writerow(
                {
                    "model_row_id": record["model_row_id"],
                    "dataset_status": record["dataset_status"],
                    "blocker_token": record.get("blocker_token"),
                    "horizon": record.get("horizon"),
                    "seed": record.get("seed"),
                    "observation_sha256": obs.get("sha256"),
                    "state_sha256": state.get("sha256"),
                    "reason": record.get("reason"),
                }
            )


def _write_markdown(path: Path, artifact: dict[str, Any]) -> None:
    lines = [
        "# P8 Synthetic Dataset Manifest",
        "",
        f"status: {artifact['status']}",
        f"numeric_benchmark_status: {artifact['numeric_benchmark_status']}",
        "",
        "| Row | Dataset status | Horizon | Seed | Blocker |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for record in artifact["dataset_records"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{record['model_row_id']}`",
                    f"`{record['dataset_status']}`",
                    "" if record.get("horizon") is None else str(record["horizon"]),
                    "" if record.get("seed") is None else str(record["seed"]),
                    "" if record.get("blocker_token") is None else f"`{record['blocker_token']}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Required Tokens",
            "",
            "```text",
            artifact["status"],
            artifact["numeric_benchmark_status"],
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--summary-csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--summary-markdown", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    artifact = build_artifact()
    args.output_json.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    _write_csv(args.summary_csv, artifact["dataset_records"])
    _write_markdown(args.summary_markdown, artifact)
    print(f"wrote {args.output_json}")
    print(f"status {artifact['status']}")
    print(f"numeric_benchmark_status {artifact['numeric_benchmark_status']}")


if __name__ == "__main__":
    main()
