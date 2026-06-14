#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

REGISTRY_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json"
REFERENCE_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-reference-oracles-2026-06-10.json"
SEMANTICS_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-gradient-semantics-2026-06-10.json"
PREFLIGHT_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-preflight-matrix-2026-06-10.json"
METHODOLOGY_PATH = ROOT / "docs/plans/bayesfilter-synthetic-truth-filter-benchmark-methodology-proposal-2026-06-11.md"
SUBPLAN_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-synthetic-truth-runner-subplan-2026-06-11.md"
RESULT_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-synthetic-truth-runner-result-2026-06-11.md"

DEFAULT_OUT = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-contract-2026-06-11.json"
DEFAULT_CSV = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-capability-crosswalk-2026-06-11.csv"
DEFAULT_MD = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-capability-crosswalk-2026-06-11.md"


ALLOWED_SCORE_PROVENANCE = [
    "native_phi_autodiff",
    "native_phi_analytic",
    "physical_theta_chain_rule_converted_to_phi",
    "fixed_branch_diagnostic_only",
    "physical_theta_unconverted_diagnostic_only",
    "algorithm_gradient_not_exposed",
    "adapter_required_pending",
    "unsupported_by_target",
    "blocked_value_route",
    "no_theta_gradient_dim0",
    "not_available_transform_gap",
]

ALLOWED_HESSIAN_PROVENANCE = [
    "native_phi_hessian_autodiff",
    "native_phi_hessian_analytic",
    "full_chain_rule_hessian_transform",
    "partial_transform_diagnostic_only",
    "hessian_not_exposed",
    "adapter_required_pending",
    "unsupported_by_target",
    "blocked_value_route",
    "no_theta_gradient_dim0",
    "not_available_transform_gap",
]

CROSSWALK_COLUMNS = [
    "algorithm_id",
    "model_row_id",
    "capability_status",
    "score_coordinate_system",
    "score_derivative_provenance",
    "hessian_coordinate_system_or_reason",
    "hessian_derivative_provenance_or_gap",
    "diagnostic_only_reason",
    "not_available_reason",
    "current_performance_status",
]

TUPLE_MANIFEST_FIELDS = [
    "model_row_id",
    "truth_draw_id",
    "algorithm_id",
    "truth_prior_lane",
    "accepted_draw_status",
    "truth_coordinate_system",
    "data_replicate_ids",
    "filter_seed_ids",
    "capability_status",
    "score_coordinate_system",
    "score_derivative_provenance",
    "hessian_coordinate_system_or_reason",
    "hessian_derivative_provenance_or_gap",
    "diagnostic_only_reason",
    "not_available_reason",
    "branch_veto_status",
    "failure_status",
    "performance_table_admission_status",
]


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _index_by(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {item[key]: item for item in items}


def _reason_text(reasons: list[str]) -> str:
    clean = [reason for reason in reasons if reason != "NONE"]
    return ";".join(clean)


def _capability_status(cell: dict[str, Any]) -> str:
    source_status = cell["source_status"]
    gradient_status = cell["normalized_gradient_status"]

    if source_status in {"BLOCKED_VALUE_ROUTE", "UNSUPPORTED_WITH_REASON", "ADAPTER_REQUIRED_WITH_REASON"}:
        return "not_available_with_reason"
    if source_status in {"READY_DIAGNOSTIC_ONLY", "READY_FIXED_BRANCH_DIAGNOSTIC", "SCOUT_ONLY_NOT_TRUTH"}:
        return "diagnostic_derivative_only"
    if gradient_status in {"valid_autodiff_gradient"}:
        return "value_plus_score"
    return "value_only"


def _score_provenance(cell: dict[str, Any], row: dict[str, Any]) -> str:
    raw = cell["raw_gradient_status"]
    normalized = cell["normalized_gradient_status"]
    coordinate_type = row["gradient_metadata"]["coordinate_type"]

    if raw == "NO_THETA_GRADIENT_DIM0":
        return "no_theta_gradient_dim0"
    if normalized == "blocked_value_route":
        return "blocked_value_route"
    if normalized == "unsupported_by_target":
        return "unsupported_by_target"
    if normalized == "adapter_required":
        return "adapter_required_pending"
    if normalized == "valid_autodiff_gradient":
        if coordinate_type == "unconstrained":
            return "native_phi_autodiff"
        if coordinate_type == "physical_box_constrained":
            return "physical_theta_unconverted_diagnostic_only"
        return "not_available_transform_gap"
    if normalized == "fixed_branch_gradient_diagnostic":
        return "fixed_branch_diagnostic_only"
    if normalized in {"diagnostic_only_not_promotion", "scout_only_not_truth"}:
        return "algorithm_gradient_not_exposed"
    if normalized == "resampling_gradient_not_valid":
        return "algorithm_gradient_not_exposed"
    return "algorithm_gradient_not_exposed"


def _score_coordinate(score_provenance: str) -> str:
    if score_provenance in {"native_phi_autodiff", "native_phi_analytic", "physical_theta_chain_rule_converted_to_phi"}:
        return "canonical_phi"
    if score_provenance == "physical_theta_unconverted_diagnostic_only":
        return "physical_theta_diagnostic_only_requires_chain_rule"
    if score_provenance == "no_theta_gradient_dim0":
        return "not_applicable_no_free_theta"
    if score_provenance in {"blocked_value_route", "unsupported_by_target", "adapter_required_pending"}:
        return "not_available"
    if score_provenance == "fixed_branch_diagnostic_only":
        return "fixed_branch_diagnostic_not_main_score"
    return "not_exposed"


def _hessian_provenance(
    cell: dict[str, Any],
    row: dict[str, Any],
    score_provenance: str,
) -> str:
    algorithm_id = cell["algorithm_id"]
    row_id = cell["registry_row_id"]
    coordinate_type = row["gradient_metadata"]["coordinate_type"]

    if score_provenance in {"blocked_value_route", "unsupported_by_target", "adapter_required_pending", "no_theta_gradient_dim0"}:
        return score_provenance
    if coordinate_type == "physical_box_constrained":
        return "not_available_transform_gap"
    if (
        algorithm_id == "kalman_exact_or_mixture_enumeration"
        and row_id == "lgssm_exact_kalman_dim_1_2_3"
    ):
        return "native_phi_hessian_autodiff"
    if score_provenance in {"fixed_branch_diagnostic_only", "physical_theta_unconverted_diagnostic_only"}:
        return "partial_transform_diagnostic_only"
    return "hessian_not_exposed"


def _hessian_coordinate(hessian_provenance: str) -> str:
    if hessian_provenance in {
        "native_phi_hessian_autodiff",
        "native_phi_hessian_analytic",
        "full_chain_rule_hessian_transform",
    }:
        return "canonical_phi"
    if hessian_provenance == "partial_transform_diagnostic_only":
        return "diagnostic_only_not_main_curvature"
    if hessian_provenance == "not_available_transform_gap":
        return "not_available_transform_gap"
    if hessian_provenance == "no_theta_gradient_dim0":
        return "not_applicable_no_free_theta"
    return "not_available"


def _diagnostic_reason(cell: dict[str, Any], score_provenance: str, hessian_provenance: str) -> str:
    reasons: list[str] = []
    if cell["source_status"] in {"READY_DIAGNOSTIC_ONLY", "READY_FIXED_BRANCH_DIAGNOSTIC", "SCOUT_ONLY_NOT_TRUTH"}:
        reasons.extend(reason for reason in cell["reason_codes"] if reason != "NONE")
        reasons.append(cell["source_status"])
    if score_provenance in {"fixed_branch_diagnostic_only", "physical_theta_unconverted_diagnostic_only"}:
        reasons.append(score_provenance)
    if hessian_provenance == "partial_transform_diagnostic_only":
        reasons.append("partial_hessian_transform_not_main_curvature")
    if cell["normalized_gradient_status"] == "resampling_gradient_not_valid":
        reasons.append("resampling_gradient_not_valid")
    return ";".join(sorted(set(reasons)))


def _not_available_reason(cell: dict[str, Any], score_provenance: str, hessian_provenance: str) -> str:
    reasons: list[str] = []
    if cell["source_status"] in {"BLOCKED_VALUE_ROUTE", "UNSUPPORTED_WITH_REASON", "ADAPTER_REQUIRED_WITH_REASON"}:
        reasons.extend(reason for reason in cell["reason_codes"] if reason != "NONE")
        reasons.append(cell["source_status"])
    if score_provenance in {
        "algorithm_gradient_not_exposed",
        "adapter_required_pending",
        "unsupported_by_target",
        "blocked_value_route",
        "no_theta_gradient_dim0",
        "not_available_transform_gap",
    }:
        reasons.append(score_provenance)
    if hessian_provenance in {
        "hessian_not_exposed",
        "adapter_required_pending",
        "unsupported_by_target",
        "blocked_value_route",
        "no_theta_gradient_dim0",
        "not_available_transform_gap",
    }:
        reasons.append(hessian_provenance)
    return ";".join(sorted(set(reasons)))


def _current_performance_status(cell: dict[str, Any]) -> str:
    if cell["source_status"] == "BLOCKED_VALUE_ROUTE":
        return "blocked_before_numeric_execution"
    if cell["source_status"] == "UNSUPPORTED_WITH_REASON":
        return "not_applicable_by_target"
    return "pending_numeric_execution"


def _crosswalk_row(cell: dict[str, Any], row: dict[str, Any]) -> dict[str, Any]:
    score_provenance = _score_provenance(cell, row)
    hessian_provenance = _hessian_provenance(cell, row, score_provenance)
    return {
        "algorithm_id": cell["algorithm_id"],
        "model_row_id": cell["registry_row_id"],
        "capability_status": _capability_status(cell),
        "score_coordinate_system": _score_coordinate(score_provenance),
        "score_derivative_provenance": score_provenance,
        "hessian_coordinate_system_or_reason": _hessian_coordinate(hessian_provenance),
        "hessian_derivative_provenance_or_gap": hessian_provenance,
        "diagnostic_only_reason": _diagnostic_reason(cell, score_provenance, hessian_provenance),
        "not_available_reason": _not_available_reason(cell, score_provenance, hessian_provenance),
        "current_performance_status": _current_performance_status(cell),
        "source_status": cell["source_status"],
        "raw_gradient_status": cell["raw_gradient_status"],
        "normalized_gradient_status": cell["normalized_gradient_status"],
        "reason_codes": [reason for reason in cell["reason_codes"] if reason != "NONE"],
    }


def _nested_crosswalk(rows: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, Any]]]:
    nested: dict[str, dict[str, dict[str, Any]]] = {}
    for row in rows:
        algorithm_id = row["algorithm_id"]
        model_row_id = row["model_row_id"]
        nested.setdefault(algorithm_id, {})[model_row_id] = row
    return nested


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CROSSWALK_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row[key] for key in CROSSWALK_COLUMNS})


def _write_markdown(path: Path, rows: list[dict[str, Any]]) -> None:
    columns = [
        "algorithm_id",
        "model_row_id",
        "capability_status",
        "score_derivative_provenance",
        "hessian_derivative_provenance_or_gap",
        "current_performance_status",
    ]
    lines = ["| " + " | ".join(columns) + " |"]
    lines.append("| " + " | ".join(["---"] * len(columns)) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _algorithm_specific_contracts(algorithm_ids: list[str]) -> dict[str, Any]:
    contracts: dict[str, Any] = {}
    for algorithm_id in algorithm_ids:
        if algorithm_id in {"bootstrap_dpf_current", "ledh_pfpf_alg1_ukf_current"}:
            contracts[algorithm_id] = {
                "stochastic_filter": True,
                "filter_seed_ladder_required": True,
                "mc_uncertainty_required_before_ranking": True,
                "required_diagnostics": [
                    "data_se",
                    "particle_mc_se",
                    "seed_ladder_status",
                    "effective_sample_size",
                    "resampling_count",
                    "degeneracy_flags",
                ],
                "gradient_policy": "not_certified_for_main_score_without_separate_review",
            }
        else:
            contracts[algorithm_id] = {
                "stochastic_filter": False,
                "filter_seed_ladder_required": False,
                "mc_uncertainty_required_before_ranking": False,
                "required_diagnostics": ["failure_rate", "nan_rate", "branch_veto_rate"],
                "gradient_policy": "use_crosswalk_score_provenance",
            }
    return contracts


def build_artifact() -> dict[str, Any]:
    registry = _load(REGISTRY_PATH)
    references = _index_by(_load(REFERENCE_PATH)["rows"], "registry_row_id")
    semantics = _load(SEMANTICS_PATH)
    preflight = _load(PREFLIGHT_PATH)
    registry_rows = _index_by(registry["rows"], "row_id")

    crosswalk_rows = [
        _crosswalk_row(cell, registry_rows[cell["registry_row_id"]])
        for cell in preflight["preflight_cells"]
    ]
    crosswalk = _nested_crosswalk(crosswalk_rows)

    value_table_schema = {
        "rows": "algorithm_id",
        "columns": "model_row_id",
        "cell_fields": [
            "mean_average_log_likelihood",
            "standard_error",
            "confidence_interval",
            "failure_rate",
            "nan_rate",
            "current_performance_status",
        ],
        "numeric_status": "pending_accepted_truth_draws_and_reviewed_evaluators",
    }
    score_table_schema = {
        "rows": "algorithm_id",
        "columns": "model_row_id",
        "cell_fields": [
            "mean_score_norm",
            "max_score_component",
            "min_score_component",
            "max_standardized_component",
            "score_coordinate_system",
            "score_derivative_provenance",
            "failure_rate",
        ],
        "numeric_status": "pending_accepted_truth_draws_and_reviewed_evaluators",
    }
    componentwise_score_schema = {
        "rows": "algorithm_id x model_row_id x truth_draw_id x parameter_coordinate",
        "fields": [
            "algorithm_id",
            "model_row_id",
            "truth_draw_id",
            "parameter_coordinate",
            "signed_mean_score",
            "standard_error",
            "confidence_interval_low",
            "confidence_interval_high",
            "standardized_mean",
            "score_coordinate_system",
            "score_derivative_provenance",
            "performance_table_admission_status",
        ],
        "mandatory": True,
        "numeric_status": "schema_frozen_numeric_pending",
    }
    curvature_table_schema = {
        "rows": "algorithm_id",
        "columns": "model_row_id",
        "cell_fields": [
            "replicate_level_lambda_min_negative_hessian_mean",
            "replicate_level_lambda_min_negative_hessian_median",
            "replicate_level_lambda_min_negative_hessian_quantiles",
            "positive_definite_fraction",
            "sign_convention",
            "hessian_derivative_provenance_or_gap",
        ],
        "primary_curvature_object": "replicate_level_lambda_min(-H)",
        "numeric_status": "pending_full_hessian_coordinate_contract",
    }
    stochastic_table_schema = {
        "rows": "dpf_algorithm_id",
        "columns": "model_row_id",
        "cell_fields": [
            "data_standard_error",
            "particle_mc_standard_error",
            "mc_se_to_data_se_ratio",
            "seed_ladder_status",
            "particle_count",
            "effective_sample_size",
            "resampling_count",
            "degeneracy_flags",
        ],
        "ranking_rule": "do_not_rank_small_differences_when_mc_noise_dominant",
        "numeric_status": "pending_stochastic_seed_calibration",
    }
    lgssm_exact_schema = {
        "rows": "algorithm_id",
        "columns": "lgssm_exact_kalman_dim_1_2_3",
        "cell_fields": [
            "exact_average_loglik_error",
            "exact_score_error_norm",
            "exact_hessian_error_norm",
            "reference_route",
        ],
        "numeric_status": "pending_reviewed_evaluator_outputs",
    }

    return {
        "schema_version": "filter_bench.synthetic_truth_p8.v1",
        "metadata_date": "2026-06-11",
        "phase": "FILTER_BENCH_P8",
        "status": "PASS_FILTER_BENCH_P8_SYNTHETIC_TRUTH_CONTRACT",
        "numeric_benchmark_status": "BLOCK_FILTER_BENCH_P8_SYNTHETIC_TRUTH_NUMERIC_RUN_PENDING",
        "purpose": "Synthetic-truth likelihood-geometry benchmark contract for the frozen filtering value/gradient roster.  This artifact freezes schemas and provenance before numeric execution.",
        "supersedes": {
            "old_p8_status_runner": "docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-runner-matrices-result-2026-06-10.md",
            "reason": "The old P8 oracle-error matrix criterion was impossible for nonlinear models without exact references.  This P8 uses the reviewed synthetic-truth methodology.",
        },
        "source_artifacts": {
            "methodology_proposal": _rel(METHODOLOGY_PATH),
            "subplan": _rel(SUBPLAN_PATH),
            "target_registry": _rel(REGISTRY_PATH),
            "reference_oracles": _rel(REFERENCE_PATH),
            "gradient_semantics": _rel(SEMANTICS_PATH),
            "preflight_matrix": _rel(PREFLIGHT_PATH),
        },
        "frozen_roster": preflight["frozen_roster"],
        "benchmark_scope": {
            "contract_emission_complete": True,
            "numeric_benchmark_execution_complete": False,
            "performance_answer_complete": False,
            "accepted_truth_draws_generated": False,
            "synthetic_datasets_generated": False,
            "horizon_calibration_complete": False,
            "stochastic_seed_calibration_complete": False,
            "p7_preflight_used_as_performance_evidence": False,
            "smoke_fixtures_used_as_performance_evidence": False,
            "old_ledh_pfpf_ot_current_evidence": False,
        },
        "coordinate_contract": {
            "canonical_coordinate_system": "phi_unconstrained_benchmark_coordinates",
            "physical_parameter_transform": "theta = tau(phi)",
            "score_chain_rule": "g_phi = J_tau(phi)^T g_theta",
            "hessian_chain_rule": "H_phi = J_tau^T H_theta J_tau + sum_k g_theta,k Hessian_phi tau_k",
            "partial_hessian_transform_policy": "partial transforms are diagnostic_only; missing full transform is not_available_transform_gap",
            "allowed_score_derivative_provenance": ALLOWED_SCORE_PROVENANCE,
            "allowed_hessian_derivative_provenance_or_gap": ALLOWED_HESSIAN_PROVENANCE,
            "loglik_sign_convention": "average log likelihood; curvature reports lambda_min(-H)",
        },
        "truth_design_contract": {
            "truth_prior_lanes": ["core_prior", "stress_prior"],
            "truth_draw_manifest_status": "pending_calibration",
            "accepted_draw_manifest_schema": [
                "model_row_id",
                "truth_draw_id",
                "truth_prior_lane",
                "phi_value",
                "theta_value",
                "transform_tau",
                "acceptance_status",
                "rejection_reason",
                "stationarity_check",
                "finite_simulation_check",
                "seed",
            ],
            "data_generation_schema": [
                "model_row_id",
                "truth_draw_id",
                "data_replicate_id",
                "horizon",
                "observations_artifact",
                "data_seed",
            ],
            "horizon_calibration_ladder": {
                "T": [512, 1024, 2048, 4096, 8192],
                "R": [16, 32],
                "long_run_variance_estimators": ["HAC_Newey_West", "batch_means"],
                "status": "pending",
            },
            "stochastic_seed_ladder": {
                "S": [4, 8, 16, 32],
                "mc_se_rule": "MC_SE <= 0.25 * data_SE before ranking small differences",
                "status": "pending",
            },
        },
        "tuple_level_crosswalk_contract": {
            "status": "pending_accepted_truth_draws",
            "required_fields": TUPLE_MANIFEST_FIELDS,
            "performance_interpretation": "not_performance_evidence_until_tuple_rows_exist_and_numeric_evaluators_run",
        },
        "capability_crosswalk_columns": CROSSWALK_COLUMNS,
        "capability_crosswalk_rows": crosswalk_rows,
        "capability_crosswalk": crosswalk,
        "benchmark_table_schemas": {
            "value": value_table_schema,
            "score": score_table_schema,
            "componentwise_score": componentwise_score_schema,
            "curvature": curvature_table_schema,
            "stochastic_filter_uncertainty": stochastic_table_schema,
            "lgssm_exact_reference": lgssm_exact_schema,
        },
        "algorithm_specific_contracts": _algorithm_specific_contracts(
            preflight["frozen_roster"]["algorithm_ids"]
        ),
        "row_reference_summary": {
            row_id: {
                "reference_type": references[row_id]["reference_type"],
                "benchmark_class": references[row_id]["benchmark_class"],
                "reference_value_policy": references[row_id]["reference_value_policy"],
                "reference_gradient_policy": references[row_id]["reference_gradient_policy"],
                "theta_dimension_policy": references[row_id]["theta_dimension_policy"],
            }
            for row_id in preflight["frozen_roster"]["model_columns"]
        },
        "historical_only_records": [
            {
                "algorithm_id": "ledh_pfpf_ot_historical",
                "current_evidence": False,
                "reason_codes": ["HISTORICAL_LEDHPFPF_OT_SUPERSEDED"],
                "admission_policy": "excluded_from_current_performance_tables",
            }
        ],
        "decision_table": [
            {
                "decision": "pass_revised_p8_contract_gate",
                "primary_criterion": "synthetic-truth contract emitted for all frozen cells with provenance and no proxy performance claims",
                "veto_diagnostics": "no veto fired for contract emission",
                "main_uncertainty": "numeric benchmark execution remains pending",
                "next_justified_action": "generate accepted truth draws, calibrate horizons/seeds, then run reviewed evaluators",
                "not_concluded": "filter ranking, full numeric value/score/curvature performance, DPF gradient certification, Bayesian-estimation readiness",
            },
            {
                "decision": "block_full_numeric_p8_performance_closeout",
                "primary_criterion": "accepted truth draws and reviewed numeric evaluator outputs are absent",
                "veto_diagnostics": "numeric-run-pending block active",
                "main_uncertainty": "which evaluator cells will become numeric after calibration and adapter repair",
                "next_justified_action": "write the next execution plan for truth-draw generation and numeric evaluator implementation",
                "not_concluded": "that any algorithm is better or worse on the benchmark ladder",
            },
        ],
        "run_manifest": {
            "git_commit": "dirty worktree; P8 synthetic-truth contract artifacts uncommitted",
            "dirty_state_summary": "dirty worktree preserved; unrelated changes not reverted",
            "command": "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_synthetic_truth.py",
            "environment": "local Python environment",
            "conda_env": "N/A",
            "cpu_gpu_status": "CPU-only metadata/schema emission; no GPU conclusion",
            "dtype": "manifest-level only; per-row dtype lives in P1 registry",
            "seeds": "No new random draws generated in this contract phase",
            "plan_file": _rel(SUBPLAN_PATH),
            "result_file": _rel(RESULT_PATH),
            "output_json": _rel(DEFAULT_OUT),
            "capability_crosswalk_csv": _rel(DEFAULT_CSV),
            "capability_crosswalk_markdown": _rel(DEFAULT_MD),
        },
        "post_run_red_team_note": {
            "strongest_alternative_explanation": "A contract artifact can look like progress while still leaving the numeric benchmark unrun.",
            "what_would_overturn_numeric_block": "Accepted truth draws, synthetic datasets, horizon and seed calibration, and reviewed evaluator outputs for reportable cells.",
            "weakest_part_of_evidence": "No likelihood, score, curvature, or stochastic uncertainty measurements are produced in this phase.",
        },
        "semantics_source_summary": {
            "schema_version": semantics["schema_version"],
            "status": semantics["status"],
            "matrix_emission_rules": semantics["matrix_emission_rules"],
        },
        "nonclaims": [
            "not a filter ranking",
            "not a full numeric benchmark result",
            "not evidence that nonlinear approximate likelihoods are exact",
            "not a DPF gradient certification",
            "not HMC, GPU, or Bayesian-estimation readiness",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--crosswalk-csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--crosswalk-markdown", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    artifact = build_artifact()
    crosswalk_rows = artifact["capability_crosswalk_rows"]
    args.output_json.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    _write_csv(args.crosswalk_csv, crosswalk_rows)
    _write_markdown(args.crosswalk_markdown, crosswalk_rows)
    print(f"wrote {args.output_json}")
    print(f"status {artifact['status']}")
    print(f"numeric_benchmark_status {artifact['numeric_benchmark_status']}")


if __name__ == "__main__":
    main()
