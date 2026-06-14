#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

PLAN_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-blocker-fix-execution-plan-2026-06-11.md"
)
SOURCE_SCOPE_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json"
)
DATASET_MANIFEST_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.json"
)
GENERALIZED_SV_SPEC_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.json"
)
P58_LEDGER_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p58-m9-source-route-pipeline-blocker-ledger-2026-06-11.md"
)
P59_9A_RESULT_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p59-9a-author-sir-36d-target-fit-result-2026-06-11.md"
)
P59_9B_RESULT_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p59-9b-source-route-step-spec-assembly-result-2026-06-11.md"
)
P59_9C_RESULT_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p59-9c-preconditioned-route-integration-result-2026-06-11.md"
)
P59_9D_RESULT_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p59-9d-runner-manifest-path-result-2026-06-11.md"
)
P59_9E_RESULT_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p59-9e-validation-ladder-result-2026-06-11.md"
)

DEFAULT_JSON = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-blocker-fix-gates-2026-06-11.json"
)
DEFAULT_CSV = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-adapter-status-matrix-2026-06-11.csv"
)
DEFAULT_MD = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-blocker-fix-gates-2026-06-11.md"
)

DPF_ALGORITHMS = {"bootstrap_dpf_current", "ledh_pfpf_alg1_ukf_current"}
KALMAN_OR_MIXTURE = "kalman_exact_or_mixture_enumeration"
ZHAO_CUI_ALGORITHM = "zhao_cui_scalar_or_multistate"
SIR_ROW_ID = "zhao_cui_spatial_sir_austria_j9_T20"

P59_SIR_PASS_ARTIFACTS = {
    "P59-9a": (P59_9A_RESULT_PATH, "PASS_P59_9A_AUTHOR_SIR_36D_TARGET_FIT_PREP"),
    "P59-9b": (P59_9B_RESULT_PATH, "PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY"),
    "P59-9c": (P59_9C_RESULT_PATH, "PASS_P59_9C_PRECONDITIONED_ROUTE_INTEGRATION"),
    "P59-9d": (P59_9D_RESULT_PATH, "PASS_P59_9D_RUNNER_MANIFEST_PATH"),
    "P59-9e": (P59_9E_RESULT_PATH, "PASS_P59_9E_D18_EXECUTION_ONLY"),
}

SOURCE_HORIZON_ROWS = {
    "benchmark_lgssm_exact_oracle_m3_T50",
    "zhao_cui_sv_actual_nongaussian_T1000",
    "zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000",
    "zhao_cui_spatial_sir_austria_j9_T20",
    "zhao_cui_predator_prey_T20",
}


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _source_rows(source_scope: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        row["row_id"]: row
        for row in source_scope["promoted_or_replacement_source_rows"]
    }


def _dataset_statuses(dataset_manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        row["model_row_id"]: row
        for row in dataset_manifest["dataset_records"]
    }


def _artifact_has_token(path: Path, token: str) -> bool:
    return path.exists() and token in path.read_text(encoding="utf-8")


def _sir_execution_only_evidence() -> dict[str, Any]:
    artifact_statuses = {}
    missing = []
    for phase, (path, token) in P59_SIR_PASS_ARTIFACTS.items():
        passed = _artifact_has_token(path, token)
        artifact_statuses[phase] = {
            "artifact": _rel(path),
            "required_token": token,
            "passed": passed,
        }
        if not passed:
            missing.append(phase)

    if missing:
        status = "BLOCK_P8_B6_SPATIAL_SIR_D18_SOURCE_ROUTE"
        readiness = "source_route_execution_only_evidence_missing"
    else:
        status = "PASS_P8_B6_SPATIAL_SIR_D18_EXECUTION_ONLY_RECOGNIZED"
        readiness = "source_route_execution_only_ready_numeric_pending"

    return {
        "status": status,
        "readiness": readiness,
        "artifact_statuses": artifact_statuses,
        "missing_phases": missing,
        "nonclaims": [
            "not d18 filtering accuracy evidence",
            "not same-route rank convergence evidence",
            "not same-target correctness evidence",
            "not d50 or d100 scaling evidence",
            "not HMC production readiness",
            "not adaptive Zhao-Cui parity",
            "not UKF correctness comparator evidence",
        ],
    }


def _source_horizon(row: dict[str, Any], generalized_sv_spec: dict[str, Any]) -> int:
    row_id = row["row_id"]
    values = row["truth_or_test_values"]
    if row_id == "zhao_cui_generalized_sv_synthetic_from_estimated_values":
        return int(generalized_sv_spec["synthetic_generation_contract"]["core_horizon"])
    return int(values["horizon"])


def _horizon_gate_rows(
    rows: dict[str, dict[str, Any]],
    datasets: dict[str, dict[str, Any]],
    generalized_sv_spec: dict[str, Any],
    sir_evidence: dict[str, Any],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for row_id, row in rows.items():
        dataset = datasets.get(row_id, {})
        dataset_status = dataset.get("dataset_status", "not_generated")
        blocker = dataset.get("blocker_token")
        if row_id == "benchmark_lgssm_exact_oracle_m3_T50":
            status = "exact_oracle_horizon_locked_numeric_calibration_pending"
        elif row_id == "zhao_cui_generalized_sv_synthetic_from_estimated_values":
            status = "source_prior_mean_horizon_locked_numeric_calibration_pending"
        elif row_id == SIR_ROW_ID:
            if not sir_evidence["missing_phases"]:
                status = "source_horizon_locked_source_route_execution_only_ready_numeric_pending"
                blocker = None
            else:
                status = "source_horizon_locked_source_route_validation_pending"
                blocker = "BLOCK_P8_B6_SPATIAL_SIR_D18_SOURCE_ROUTE"
        else:
            status = "source_horizon_locked_numeric_calibration_pending"
        result.append(
            {
                "model_row_id": row_id,
                "source_horizon": _source_horizon(row, generalized_sv_spec),
                "dataset_status": dataset_status,
                "horizon_gate_status": status,
                "blocker_token": blocker,
                "long_run_variance_estimators": ["HAC_Newey_West", "batch_means"],
                "numeric_horizon_calibration_run": False,
                "interpretation": (
                    "protocol_gate_only_not_numeric_horizon_calibration"
                ),
            }
        )
    return result


def _stochastic_gate_rows(
    rows: dict[str, dict[str, Any]],
    algorithms: list[str],
    datasets: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for algorithm_id in algorithms:
        if algorithm_id not in DPF_ALGORITHMS:
            continue
        for row_id in rows:
            dataset = datasets.get(row_id, {})
            dataset_status = dataset.get("dataset_status", "not_generated")
            blocker = dataset.get("blocker_token")
            if dataset_status == "generated":
                status = "seed_protocol_ready_numeric_pending"
            else:
                status = "seed_protocol_ready_row_precondition_pending"
            result.append(
                {
                    "algorithm_id": algorithm_id,
                    "model_row_id": row_id,
                    "dataset_status": dataset_status,
                    "stochastic_gate_status": status,
                    "blocker_token": blocker,
                    "seed_ladder": [4, 8, 16, 32],
                    "required_diagnostics": [
                        "data_standard_error",
                        "particle_mc_standard_error",
                        "mc_se_to_data_se_ratio",
                        "effective_sample_size",
                        "resampling_count",
                        "degeneracy_flags",
                    ],
                    "ranking_enabled": False,
                    "ranking_rule": "ranking_enabled_only_after_MC_SE_le_0p25_data_SE",
                    "numeric_seed_ladder_run": False,
                }
            )
    return result


def _kalman_or_mixture_status(row_id: str) -> tuple[str, str, str, str, str]:
    if row_id == "benchmark_lgssm_exact_oracle_m3_T50":
        return (
            "exact_lgssm_protocol_ready_numeric_pending",
            "exact_lgssm_score_protocol_ready_numeric_pending",
            "exact_lgssm_hessian_protocol_ready_numeric_pending",
            "exact_lgssm_only",
            "",
        )
    if row_id == "zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000":
        return (
            "mixture_enumeration_protocol_ready_numeric_pending",
            "score_protocol_pending_mixture_surrogate",
            "hessian_not_exposed_numeric_pending",
            "declared_gaussian_mixture_surrogate_only",
            "",
        )
    return (
        "not_applicable_outside_lgssm_or_declared_mixture_surrogate",
        "not_applicable_outside_lgssm_or_declared_mixture_surrogate",
        "not_applicable_outside_lgssm_or_declared_mixture_surrogate",
        "structured_not_applicable",
        "KALMAN_REMOVED_OUTSIDE_LGSSM_OR_DECLARED_MIXTURE",
    )


def _adapter_status(
    *,
    algorithm_id: str,
    row_id: str,
    dataset_status: str,
    dataset_blocker: str | None,
    sir_evidence: dict[str, Any],
) -> dict[str, str]:
    if algorithm_id == KALMAN_OR_MIXTURE:
        value, score, hessian, target, reason = _kalman_or_mixture_status(row_id)
        return {
            "target_contract_status": target,
            "value_adapter_status": value,
            "score_adapter_status": score,
            "hessian_adapter_status": hessian,
            "not_available_reason": reason,
        }

    if row_id == SIR_ROW_ID:
        if algorithm_id == ZHAO_CUI_ALGORITHM:
            if not sir_evidence["missing_phases"]:
                return {
                    "target_contract_status": "source_route_target_compatible_execution_only_ready",
                    "value_adapter_status": "source_route_execution_only_ready_numeric_evaluator_pending",
                    "score_adapter_status": "not_applicable_no_free_theta",
                    "hessian_adapter_status": "not_applicable_no_free_theta",
                    "not_available_reason": "",
                }
            return {
                "target_contract_status": "source_route_target_compatible",
                "value_adapter_status": "blocked_on_p59_9b_to_9e_source_route",
                "score_adapter_status": "not_applicable_no_free_theta",
                "hessian_adapter_status": "not_applicable_no_free_theta",
                "not_available_reason": "BLOCK_P8_B6_SPATIAL_SIR_D18_SOURCE_ROUTE",
            }
        return {
            "target_contract_status": "target_compatible",
            "value_adapter_status": "protocol_ready_numeric_evaluator_pending",
            "score_adapter_status": "not_applicable_no_free_theta",
            "hessian_adapter_status": "not_applicable_no_free_theta",
            "not_available_reason": "",
        }

    if dataset_status != "generated":
        return {
            "target_contract_status": "target_compatible",
            "value_adapter_status": "blocked_on_dataset_precondition",
            "score_adapter_status": "blocked_on_dataset_precondition",
            "hessian_adapter_status": "blocked_on_dataset_precondition",
            "not_available_reason": dataset_blocker or "DATASET_PRECONDITION_PENDING",
        }

    score_status = (
        "not_certified_for_main_score_without_mc_and_fixed_branch_review"
        if algorithm_id in DPF_ALGORITHMS
        else "score_protocol_ready_numeric_evaluator_pending"
    )
    return {
        "target_contract_status": "target_compatible",
        "value_adapter_status": "protocol_ready_numeric_evaluator_pending",
        "score_adapter_status": score_status,
        "hessian_adapter_status": "hessian_not_exposed_numeric_pending",
        "not_available_reason": "",
    }


def _adapter_matrix_rows(
    rows: dict[str, dict[str, Any]],
    algorithms: list[str],
    datasets: dict[str, dict[str, Any]],
    sir_evidence: dict[str, Any],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for algorithm_id in algorithms:
        for row_id in rows:
            dataset = datasets.get(row_id, {})
            dataset_status = dataset.get("dataset_status", "not_generated")
            dataset_blocker = dataset.get("blocker_token")
            status = _adapter_status(
                algorithm_id=algorithm_id,
                row_id=row_id,
                dataset_status=dataset_status,
                dataset_blocker=dataset_blocker,
                sir_evidence=sir_evidence,
            )
            numeric_status = (
                "pending_numeric_execution"
                if not status["not_available_reason"]
                else "blocked_or_not_applicable_with_reason"
            )
            result.append(
                {
                    "algorithm_id": algorithm_id,
                    "model_row_id": row_id,
                    "dataset_status": dataset_status,
                    "numeric_execution_status": numeric_status,
                    **status,
                }
            )
    return result


def build_artifact() -> dict[str, Any]:
    source_scope = _load(SOURCE_SCOPE_PATH)
    dataset_manifest = _load(DATASET_MANIFEST_PATH)
    generalized_sv_spec = _load(GENERALIZED_SV_SPEC_PATH)
    sir_evidence = _sir_execution_only_evidence()
    rows = _source_rows(source_scope)
    datasets = _dataset_statuses(dataset_manifest)
    algorithms = list(source_scope["algorithm_ids"])

    horizon_rows = _horizon_gate_rows(rows, datasets, generalized_sv_spec, sir_evidence)
    stochastic_rows = _stochastic_gate_rows(rows, algorithms, datasets)
    adapter_rows = _adapter_matrix_rows(rows, algorithms, datasets, sir_evidence)
    expected_adapter_cells = len(rows) * len(algorithms)

    row_blocks = {}
    if sir_evidence["missing_phases"]:
        row_blocks[SIR_ROW_ID] = {
            "status": "BLOCK_P8_B6_SPATIAL_SIR_D18_SOURCE_ROUTE",
            "reason": "P59-9a passed, but P59-9b through P59-9e remain.",
            "remaining_phases": [
                "P59-9b_source_route_step_spec_assembly",
                "P59-9c_preconditioned_route_decision",
                "P59-9d_runner_manifest_path",
                "P59-9e_validation_ladder",
            ],
        }

    return {
        "schema_version": "filter_bench.p8_blocker_fix_gates.v1",
        "metadata_date": "2026-06-11",
        "phase": "FILTER_BENCH_P8_BLOCKER_FIX_GATES",
        "status": "PASS_P8_BLOCKER_FIX_GATES_SOURCE_ROWS_READY_NUMERIC_PENDING",
        "numeric_benchmark_status": "BLOCK_P8_NUMERIC_BENCHMARK_NOT_YET_RUN",
        "purpose": (
            "Close the local status/protocol gaps for P8-B3, P8-B4, and P8-B5 "
            "without promoting protocol artifacts to numeric benchmark results."
        ),
        "source_artifacts": {
            "execution_plan": _rel(PLAN_PATH),
            "source_scope_contract": _rel(SOURCE_SCOPE_PATH),
            "p8_dataset_manifest": _rel(DATASET_MANIFEST_PATH),
            "generalized_sv_spec": _rel(GENERALIZED_SV_SPEC_PATH),
            "p58_sir_blocker_ledger": _rel(P58_LEDGER_PATH),
            "p59_9a_result": _rel(P59_9A_RESULT_PATH),
            "p59_9b_result": _rel(P59_9B_RESULT_PATH),
            "p59_9c_result": _rel(P59_9C_RESULT_PATH),
            "p59_9d_result": _rel(P59_9D_RESULT_PATH),
            "p59_9e_result": _rel(P59_9E_RESULT_PATH),
        },
        "role_contract": {
            "supervisor_and_executor": "Codex in this dialogue",
            "reviewer": "Claude Code read-only",
            "detached_codex_agent_allowed": False,
        },
        "phase_gate_statuses": {
            "P8-B3": {
                "status": "protocol_ready_numeric_pending",
                "token": "PASS_P8_B3_HORIZON_PROTOCOL_READY_NUMERIC_PENDING",
                "numeric_horizon_calibration_run": False,
            },
            "P8-B4": {
                "status": "protocol_ready_numeric_pending",
                "token": "PASS_P8_B4_STOCHASTIC_PROTOCOL_READY_NUMERIC_PENDING",
                "numeric_seed_ladder_run": False,
            },
            "P8-B5": {
                "status": "adapter_status_matrix_ready_numeric_pending",
                "token": "PASS_P8_B5_ADAPTER_STATUS_MATRIX_READY_NUMERIC_PENDING",
                "numeric_evaluator_run": False,
                "expected_adapter_cells": expected_adapter_cells,
                "actual_adapter_cells": len(adapter_rows),
            },
            "hard_source_blocks": {
                "status": "source_rows_ready_execution_only_sir_generalized_sv_prior_mean_ready",
                "token": "PASS_P8_SOURCE_BLOCKS_REFRESHED_NO_ROW_LEVEL_HARD_BLOCKS",
            },
        },
        "horizon_protocol": {
            "status": "PASS_P8_B3_HORIZON_PROTOCOL_READY_NUMERIC_PENDING",
            "rows": horizon_rows,
            "long_run_variance_estimators": ["HAC_Newey_West", "batch_means"],
            "numeric_calibration_required_before_benchmark_closeout": True,
            "nonclaim": "source horizons and variance-estimator policy are not measured horizon adequacy",
        },
        "stochastic_seed_protocol": {
            "status": "PASS_P8_B4_STOCHASTIC_PROTOCOL_READY_NUMERIC_PENDING",
            "rows": stochastic_rows,
            "seed_ladder": [4, 8, 16, 32],
            "promotion_rule": "MC_SE <= 0.25 * data_SE before ranking small differences",
            "ranking_enabled": False,
            "numeric_seed_ladder_required_before_dpf_ranking": True,
        },
        "adapter_status_matrix": {
            "status": "PASS_P8_B5_ADAPTER_STATUS_MATRIX_READY_NUMERIC_PENDING",
            "rows": adapter_rows,
            "expected_cell_count": expected_adapter_cells,
            "actual_cell_count": len(adapter_rows),
            "numeric_evaluator_required_before_value_or_score_tables": True,
        },
        "row_level_hard_blocks": row_blocks,
        "sir_d18_execution_only_status": sir_evidence,
        "generalized_sv_prior_mean_status": {
            "status": generalized_sv_spec["numeric_status"],
            "reason": (
                "The Zhao-Cui S&P prior-mean synthetic test point is materialized; "
                "numeric evaluator execution remains pending."
            ),
            "forbidden_substitutes": generalized_sv_spec[
                "estimate_materialization_contract"
            ]["forbidden_substitutes"],
        },
        "promotion_guardrails": {
            "p44_rows_promoted": False,
            "author_defaults_as_generalized_sv_truth_allowed": False,
            "sp500_returns_as_benchmark_observations_allowed": False,
            "zhao_cui_lgssm_matlab_C_claim_allowed": False,
            "old_ledh_pfpf_ot_current_evidence_allowed": False,
            "old_sir_local_operator_route_allowed": False,
            "dpf_ranking_before_mc_se_allowed": False,
            "protocol_gate_counts_as_numeric_benchmark_allowed": False,
        },
        "ready_for_numeric_benchmark": False,
        "numeric_benchmark_blockers": [
            "P8_B7_NUMERIC_EVALUATOR_RUN_NOT_EXECUTED",
        ],
        "decision_table": [
            {
                "decision": "pass_B3_B4_B5_protocol_and_status_gates",
                "primary_criterion": "no silent holes in horizon, stochastic, and adapter gate artifacts",
                "veto_diagnostics": "no source substitution or proxy numeric promotion",
                "main_uncertainty": "actual numeric evaluator and MC-SE results are still absent",
                "next_justified_action": "materialize hard source rows or execute numeric evaluators for nonblocked rows",
                "not_concluded": "filter ranking or numeric performance",
            },
            {
                "decision": "keep_full_p8_numeric_benchmark_blocked",
                "primary_criterion": "numeric evaluator outputs remain incomplete",
                "veto_diagnostics": "numeric_benchmark_status remains blocked",
                "main_uncertainty": "generalized-SV evaluator execution, DPF MC-SE, and score/curvature provenance",
                "next_justified_action": "P8-B7 numeric evaluator execution",
                "not_concluded": "Bayesian-estimation readiness",
            },
        ],
        "nonclaims": [
            "not a numeric benchmark result",
            "not a filter ranking",
            "not DPF gradient certification",
            "not generalized-SV evaluator correctness or performance evidence",
            "not Zhao-Cui MATLAB LGSSM reproduction",
            "not SIR d18 filtering accuracy or rank-convergence evidence",
        ],
    }


ADAPTER_CSV_COLUMNS = [
    "algorithm_id",
    "model_row_id",
    "dataset_status",
    "target_contract_status",
    "value_adapter_status",
    "score_adapter_status",
    "hessian_adapter_status",
    "numeric_execution_status",
    "not_available_reason",
]


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=ADAPTER_CSV_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row[column] for column in ADAPTER_CSV_COLUMNS})


def _write_markdown(path: Path, artifact: dict[str, Any]) -> None:
    lines = [
        "# P8 Blocker Fix Gates",
        "",
        f"status: {artifact['status']}",
        f"numeric_benchmark_status: {artifact['numeric_benchmark_status']}",
        "",
        "## Phase Gates",
        "",
        "| Gate | Status | Token |",
        "| --- | --- | --- |",
    ]
    for gate, row in artifact["phase_gate_statuses"].items():
        lines.append(f"| `{gate}` | `{row['status']}` | `{row['token']}` |")
    lines.extend(
        [
            "",
            "## Hard Source Blocks",
            "",
            "| Row | Status | Reason |",
            "| --- | --- | --- |",
        ]
    )
    if artifact["row_level_hard_blocks"]:
        for row_id, row in artifact["row_level_hard_blocks"].items():
            lines.append(f"| `{row_id}` | `{row['status']}` | {row['reason']} |")
    else:
        lines.append("| None | `no_row_level_hard_blocks_after_source_refresh` | P59-9e execution-only SIR evidence and generalized-SV prior-mean readiness are recognized; numeric benchmark remains pending. |")
    lines.extend(
        [
            "",
            "## Required Tokens",
            "",
            "```text",
            artifact["status"],
            artifact["numeric_benchmark_status"],
            "PASS_P8_B3_HORIZON_PROTOCOL_READY_NUMERIC_PENDING",
            "PASS_P8_B4_STOCHASTIC_PROTOCOL_READY_NUMERIC_PENDING",
            "PASS_P8_B5_ADAPTER_STATUS_MATRIX_READY_NUMERIC_PENDING",
            "PASS_P8_SOURCE_BLOCKS_REFRESHED_NO_ROW_LEVEL_HARD_BLOCKS",
            "PASS_P8_B6_SPATIAL_SIR_D18_EXECUTION_ONLY_RECOGNIZED",
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--adapter-csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--summary-markdown", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    artifact = build_artifact()
    args.output_json.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    _write_csv(args.adapter_csv, artifact["adapter_status_matrix"]["rows"])
    _write_markdown(args.summary_markdown, artifact)
    print(f"wrote {args.output_json}")
    print(f"status {artifact['status']}")
    print(f"numeric_benchmark_status {artifact['numeric_benchmark_status']}")


if __name__ == "__main__":
    main()
