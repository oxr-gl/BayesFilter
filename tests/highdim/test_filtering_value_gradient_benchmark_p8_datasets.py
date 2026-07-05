from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


DATASET_JSON = Path(
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.json"
)
DATASET_CSV = Path(
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.csv"
)
DATASET_MD = Path(
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.md"
)


def _artifact() -> dict[str, Any]:
    return json.loads(DATASET_JSON.read_text(encoding="utf-8"))


def _rows_by_id() -> dict[str, dict[str, Any]]:
    artifact = _artifact()
    return {row["model_row_id"]: row for row in artifact["dataset_records"]}


def _assert_finite_summary(summary: dict[str, Any], shape: list[int]) -> None:
    assert summary["shape"] == shape
    assert summary["dtype"] == "float64"
    assert len(summary["sha256"]) == 64
    assert summary["all_finite"] is True
    for key in ("mean", "stddev", "min", "max"):
        assert isinstance(summary[key], float)


def test_p8_dataset_manifest_status_and_scope_boundary() -> None:
    artifact = _artifact()

    assert artifact["schema_version"] == "filter_bench.p8_synthetic_datasets.v1"
    assert artifact["phase"] == "FILTER_BENCH_P8_B2_SYNTHETIC_DATASETS"
    assert artifact["status"] == (
        "PASS_P8_B2_SYNTHETIC_DATASET_MANIFEST_READY_WITH_NUMERIC_EVALUATORS_PENDING"
    )
    assert artifact["numeric_benchmark_status"] == "BLOCK_P8_NUMERIC_BENCHMARK_NOT_YET_RUN"
    assert artifact["ready_for_numeric_benchmark"] is False
    assert artifact["dataset_status_counts"] == {"generated": 7}
    assert "not a numeric benchmark result" in artifact["nonclaims"]
    assert "not SIR d=18 source-route validation success" in artifact["nonclaims"]

    p44_rows = [row_id for row_id in artifact["source_scope_row_ids"] if row_id.startswith("p44_")]
    assert p44_rows == []


def test_p8_dataset_manifest_generates_lgssm_exact_oracle_row() -> None:
    row = _rows_by_id()["benchmark_lgssm_exact_oracle_m3_T50"]

    assert row["dataset_status"] == "generated"
    assert row["blocker_token"] is None
    assert row["horizon"] == 50
    assert row["seed"] == 81100
    assert row["truth_theta_coordinate"] == "physical_benchmark_exact_oracle"
    assert row["truth_physical"] == {
        "phi": [0.72, 0.55, 0.35],
        "q_scale": 0.35,
        "r_scale": 0.45,
    }
    _assert_finite_summary(row["observation_summary"], [50, 3])
    _assert_finite_summary(row["state_summary"], [50, 3])
    assert row["model_manifest"]["family"] == "LinearGaussianSSM"
    assert row["model_manifest"]["identifiability_diagnostics"]["observation_matrix_rank"] == 3
    assert "not a Zhao-Cui MATLAB C reproduction" in row["nonclaims"]


def test_p8_dataset_manifest_generates_sv_actual_and_ksc_surrogate_rows() -> None:
    rows = _rows_by_id()
    actual = rows["zhao_cui_sv_actual_nongaussian_T1000"]
    ksc = rows["zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000"]

    assert actual["dataset_status"] == "generated"
    assert actual["horizon"] == 1000
    assert actual["seed"] == 81101
    assert actual["truth_physical"] == {"gamma": 0.6, "beta": 0.4, "sigma": 1.0}
    assert actual["truth_theta_coordinate"] == "synthetic_unconstrained"
    _assert_finite_summary(actual["observation_summary"], [1000, 1])
    _assert_finite_summary(actual["state_summary"], [1000, 1])
    assert actual["model_manifest"]["family"] == "StochasticVolatilitySSM"

    assert ksc["dataset_status"] == "generated"
    assert ksc["source_model_row_id"] == actual["model_row_id"]
    assert ksc["transform"] == "log(y_t^2 + offset)"
    assert ksc["transform_offset"] == 1e-8
    assert ksc["seed"] == actual["seed"]
    assert ksc["state_summary"]["sha256"] == actual["state_summary"]["sha256"]
    assert ksc["observation_summary"]["sha256"] != actual["observation_summary"]["sha256"]
    assert "not exact native SV likelihood" in ksc["nonclaims"]


def test_p8_dataset_manifest_generates_sir_raw_synthetic_but_not_source_route_success() -> None:
    row = _rows_by_id()["zhao_cui_spatial_sir_austria_j9_T20"]

    assert row["dataset_status"] == "generated"
    assert row["horizon"] == 20
    assert row["seed"] == 81103
    assert row["truth_theta_coordinate"] == "no_free_theta"
    assert row["truth_theta"] == []
    assert row["truth_physical"]["kappa"] == [0.1] * 9
    assert row["truth_physical"]["nu"] == [18.0] * 9
    _assert_finite_summary(row["observation_summary"], [20, 9])
    _assert_finite_summary(row["state_summary"], [20, 18])
    assert row["domain_diagnostics"]["has_negative_state"] is False
    assert row["model_manifest"]["state_dimension"] == 18
    assert "production_tt_sirt_sir_filtering" in row["model_manifest"]["what_is_not_claimed"]


def test_p8_dataset_manifest_generates_parameterized_sir_without_mutating_fixed_row() -> None:
    rows = _rows_by_id()
    fixed = rows["zhao_cui_spatial_sir_austria_j9_T20"]
    row = rows["zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale"]

    assert fixed["truth_theta_coordinate"] == "no_free_theta"
    assert fixed["truth_theta"] == []

    assert row["dataset_status"] == "generated"
    assert row["horizon"] == 20
    assert row["seed"] == fixed["seed"] == 81103
    assert row["fixed_base_model_row_id"] == fixed["model_row_id"]
    assert row["truth_theta_coordinate"] == "sir_log_scale_theta"
    assert row["truth_theta"] == [0.0, 0.0, 0.0]
    assert row["truth_theta_semantics"] == (
        "log-scale origin reproducing fixed source SIR base parameters"
    )
    assert row["parameter_order"] == [
        "log_kappa_scale",
        "log_nu_scale",
        "log_obs_noise_scale",
    ]
    assert row["theta_domain"] == {
        "log_kappa_scale": [-0.5, 0.5],
        "log_nu_scale": [-0.5, 0.5],
        "log_obs_noise_scale": [-0.5, 0.5],
    }
    assert row["truth_physical"]["kappa"] == [0.1] * 9
    assert row["truth_physical"]["nu"] == [18.0] * 9
    assert row["truth_physical"]["observation_standard_deviation"] == 10.0
    _assert_finite_summary(row["observation_summary"], [20, 9])
    _assert_finite_summary(row["state_summary"], [20, 18])
    assert row["observation_summary"]["sha256"] == fixed["observation_summary"]["sha256"]
    assert row["state_summary"]["sha256"] == fixed["state_summary"]["sha256"]
    assert row["domain_diagnostics"]["has_negative_state"] is False
    assert row["model_manifest"]["family"] == "ParameterizedZhaoCuiSIRSSM"
    assert row["model_manifest"]["parameter_order"] == [
        "log_kappa_scale",
        "log_nu_scale",
        "log_obs_noise_scale",
    ]
    assert row["model_manifest"]["fixed_base_model_row_id"] == fixed["model_row_id"]
    assert (
        row["model_manifest"]["leaderboard_score_provenance_requirement"]
        == "analytical_manual_only"
    )
    assert "not score admission evidence" in row["nonclaims"]
    assert (
        "not a replacement for the fixed no-free-theta source-parity row"
        in row["nonclaims"]
    )


def test_p8_dataset_manifest_generates_predator_prey_with_domain_diagnostic_visible() -> None:
    row = _rows_by_id()["zhao_cui_predator_prey_T20"]

    assert row["dataset_status"] == "generated"
    assert row["horizon"] == 20
    assert row["seed"] == 81104
    assert row["truth_theta_coordinate"] == "physical"
    assert row["truth_physical"] == {
        "r": 0.6,
        "K": 114.0,
        "a": 25.0,
        "s": 0.3,
        "u": 0.5,
        "v": 0.5,
    }
    _assert_finite_summary(row["observation_summary"], [20, 2])
    _assert_finite_summary(row["state_summary"], [20, 2])
    assert row["domain_diagnostics"]["has_negative_state"] is True
    assert row["domain_diagnostics"]["min_state"] < 0.0
    assert "paper_scale_predator_prey_result" in row["model_manifest"]["what_is_not_claimed"]


def test_p8_dataset_manifest_generates_generalized_sv_prior_mean_row() -> None:
    row = _rows_by_id()["zhao_cui_generalized_sv_synthetic_from_estimated_values"]

    assert row["dataset_status"] == "generated"
    assert row["blocker_token"] is None
    assert row["reason"] is None
    assert row["horizon"] == 1008
    assert row["seed"] == 81105
    assert row["truth_theta_coordinate"] == "source_route_active_transformed_prior_mean"
    assert row["truth_physical"] == {
        "gamma": 0.8604651162790697,
        "tau_or_sigma": 0.12533141373155002,
        "mu_or_log_beta_center_coordinate": 0.0,
        "phi": 0.0,
        "a": 0.0,
        "delta": 0.0,
        "nu1": "inf",
        "nu2": "inf",
    }
    assert row["truth_theta"] == [1.0824113944610982, -2.076793740349318, 0.0]
    _assert_finite_summary(row["observation_summary"], [1008, 1])
    _assert_finite_summary(row["state_summary"], [1008, 1])
    assert row["model_manifest"]["family"] == "ZhaoCuiSVModelsGeneralizedSVPriorMeanSynthetic"
    assert "not a posterior estimate from SP500 returns" in row["nonclaims"]
    assert "not a direct SP500 benchmark-data row" in row["nonclaims"]
    assert "not an ordinary finite-mean claim for sigma_squared_or_beta" in row["nonclaims"]


def test_p8_dataset_summary_artifacts_match_manifest() -> None:
    artifact = _artifact()
    with DATASET_CSV.open(newline="", encoding="utf-8") as handle:
        csv_rows = list(csv.DictReader(handle))
    md = DATASET_MD.read_text(encoding="utf-8")

    assert len(csv_rows) == len(artifact["dataset_records"])
    assert {row["model_row_id"] for row in csv_rows} == set(_rows_by_id())
    assert md.startswith("# P8 Synthetic Dataset Manifest")
    assert "PASS_P8_B2_SYNTHETIC_DATASET_MANIFEST_READY_WITH_NUMERIC_EVALUATORS_PENDING" in md
    assert "BLOCK_P8_NUMERIC_BENCHMARK_NOT_YET_RUN" in md
    assert "BLOCK_P8_B2_LGSSM_AUTHOR_C_MATRIX_PENDING" not in md
    assert "BLOCK_GENERALIZED_SV_NUMERIC_RUN_ESTIMATED_VALUES_PENDING" not in md


def test_p8_dataset_emitter_regenerates_manifest_artifacts(tmp_path: Path) -> None:
    output_json = tmp_path / "datasets.json"
    output_csv = tmp_path / "datasets.csv"
    output_md = tmp_path / "datasets.md"
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "-1"
    env["MPLCONFIGDIR"] = "/tmp"

    subprocess.run(
        [
            sys.executable,
            "scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py",
            "--output-json",
            str(output_json),
            "--summary-csv",
            str(output_csv),
            "--summary-markdown",
            str(output_md),
        ],
        check=True,
        env=env,
    )

    regenerated = json.loads(output_json.read_text(encoding="utf-8"))
    committed = _artifact()
    with output_csv.open(newline="", encoding="utf-8") as handle:
        csv_rows = list(csv.DictReader(handle))
    md = output_md.read_text(encoding="utf-8")

    assert regenerated["status"] == committed["status"]
    assert regenerated["numeric_benchmark_status"] == committed["numeric_benchmark_status"]
    assert regenerated["dataset_status_counts"] == committed["dataset_status_counts"]
    assert regenerated["dataset_records"] == committed["dataset_records"]
    assert len(csv_rows) == len(regenerated["dataset_records"])
    assert md.startswith("# P8 Synthetic Dataset Manifest")
