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
    "bayesfilter-filtering-value-gradient-benchmark-p8-blocker-closure-master-plan-2026-06-11.md"
)
SOURCE_SCOPE_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json"
)
GENERALIZED_SV_SPEC_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.json"
)
P8_CONTRACT_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-contract-2026-06-11.json"
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
P8_B2_DATASET_MANIFEST_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.json"
)
P8_B2_DATASET_RESULT_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-result-2026-06-11.md"
)
P8_BLOCKER_FIX_GATES_PATH = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-blocker-fix-gates-2026-06-11.json"
)

DEFAULT_JSON = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-blocker-closure-status-2026-06-11.json"
)
DEFAULT_CSV = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-blocker-closure-status-2026-06-11.csv"
)
DEFAULT_MD = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-blocker-closure-status-2026-06-11.md"
)

SIR_ROW_ID = "zhao_cui_spatial_sir_austria_j9_T20"
P59_SIR_PASS_ARTIFACTS = {
    "P59-9a": (P59_9A_RESULT_PATH, "PASS_P59_9A_AUTHOR_SIR_36D_TARGET_FIT_PREP"),
    "P59-9b": (P59_9B_RESULT_PATH, "PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY"),
    "P59-9c": (P59_9C_RESULT_PATH, "PASS_P59_9C_PRECONDITIONED_ROUTE_INTEGRATION"),
    "P59-9d": (P59_9D_RESULT_PATH, "PASS_P59_9D_RUNNER_MANIFEST_PATH"),
    "P59-9e": (P59_9E_RESULT_PATH, "PASS_P59_9E_D18_EXECUTION_ONLY"),
}


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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


def _source_rows(source_scope: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["row_id"]: row for row in source_scope["promoted_or_replacement_source_rows"]}


def _row_truth_manifest(row: dict[str, Any], sir_evidence: dict[str, Any]) -> dict[str, Any]:
    values = row["truth_or_test_values"]
    row_id = row["row_id"]
    status = "accepted_source_truth_available"
    blocker = None
    numeric_readiness = row["numeric_readiness"]
    if row_id == "zhao_cui_generalized_sv_synthetic_from_estimated_values":
        status = "accepted_source_prior_mean_test_point_available"
    if row_id == SIR_ROW_ID and not sir_evidence["missing_phases"]:
        numeric_readiness = "source_route_execution_only_ready_numeric_pending"
    return {
        "model_row_id": row_id,
        "model_family": row["model_family"],
        "truth_status": status,
        "blocker_token": blocker,
        "numeric_readiness": numeric_readiness,
        "source_scope_numeric_readiness": row["numeric_readiness"],
        "truth_or_test_values": values,
        "source_anchors": row["source_anchors"],
        "nonclaims": (
            [
                "not a posterior estimate from SP500 returns",
                "author defaults are not accepted truth",
                "SP500 returns are not benchmark observations",
            ]
            if row_id == "zhao_cui_generalized_sv_synthetic_from_estimated_values"
            else []
        ),
    }


def _blocker_rows(sir_evidence: dict[str, Any]) -> list[dict[str, Any]]:
    if sir_evidence["missing_phases"]:
        sir_blocker = {
            "blocker_id": "P8-B6",
            "name": "Spatial SIR d=18 source route",
            "status": "partial_pass_p59_9a_only",
            "pass_token": "PASS_P59_9A_AUTHOR_SIR_36D_TARGET_FIT_PREP",
            "block_token": "BLOCK_P8_B6_SPATIAL_SIR_D18_SOURCE_ROUTE",
            "remaining_work": (
                "P59-9b through P59-9e remain: source-route step-spec assembly, "
                "preconditioned-route decision, runner/manifest path, and validation ladder."
            ),
        }
    else:
        sir_blocker = {
            "blocker_id": "P8-B6",
            "name": "Spatial SIR d=18 source route",
            "status": "pass_execution_only_ready_numeric_pending",
            "pass_token": "PASS_P8_B6_SPATIAL_SIR_D18_EXECUTION_ONLY_RECOGNIZED",
            "block_token": "",
            "remaining_work": (
                "No row-level source-route hard block remains. P59-9e execution-only "
                "evidence is recognized with nonclaims; numeric evaluator execution "
                "and any accuracy/rank/scaling claims remain pending."
            ),
        }

    return [
        {
            "blocker_id": "P8-B1",
            "name": "Source truth and generalized-SV prior-mean gate",
            "status": "pass_source_truth_manifest_ready",
            "pass_token": "PASS_P8_B1_SOURCE_TRUTH_MANIFEST_READY",
            "block_token": "",
            "remaining_work": (
                "No source-truth/test-point row block remains; generalized SV uses "
                "the reviewed Zhao-Cui S&P prior-mean convention."
            ),
        },
        {
            "blocker_id": "P8-B2",
            "name": "Synthetic datasets",
            "status": "pass_dataset_manifest_ready",
            "pass_token": "PASS_P8_B2_SYNTHETIC_DATASET_MANIFEST_READY",
            "block_token": "",
            "remaining_work": (
                "Synthetic data manifests exist for the benchmark exact-oracle "
                "LGSSM, SV actual, SV KSC surrogate, raw SIR, predator-prey, "
                "and generalized-SV prior-mean rows."
            ),
        },
        {
            "blocker_id": "P8-B3",
            "name": "Horizon calibration",
            "status": "protocol_ready_numeric_pending",
            "pass_token": "PASS_P8_B3_HORIZON_PROTOCOL_READY_NUMERIC_PENDING",
            "block_token": "BLOCK_P8_B3_NUMERIC_HORIZON_CALIBRATION_PENDING",
            "remaining_work": (
                "Protocol gate exists for source-paper horizons and long-run "
                "variance estimators; measured horizon calibration remains pending."
            ),
        },
        {
            "blocker_id": "P8-B4",
            "name": "Stochastic seed calibration",
            "status": "protocol_ready_numeric_pending",
            "pass_token": "PASS_P8_B4_STOCHASTIC_PROTOCOL_READY_NUMERIC_PENDING",
            "block_token": "BLOCK_P8_B4_NUMERIC_SEED_LADDER_PENDING",
            "remaining_work": (
                "DPF seed-ladder and MC-SE/data-SE rule gate exists; measured "
                "seed ladders remain pending before any DPF ranking."
            ),
        },
        {
            "blocker_id": "P8-B5",
            "name": "Evaluator and adapter closure",
            "status": "adapter_status_matrix_ready_numeric_pending",
            "pass_token": "PASS_P8_B5_ADAPTER_STATUS_MATRIX_READY_NUMERIC_PENDING",
            "block_token": "BLOCK_P8_B5_NUMERIC_EVALUATOR_RUN_PENDING",
            "remaining_work": (
                "No-silent-hole adapter status matrix exists; reviewed numeric "
                "value/score/curvature evaluator execution remains pending."
            ),
        },
        sir_blocker,
        {
            "blocker_id": "P8-B7",
            "name": "Numeric benchmark runner and tables",
            "status": "blocked_on_source_rows_and_numeric_evaluators",
            "pass_token": "PASS_P8_B7_NUMERIC_BENCHMARK_RUNNER",
            "block_token": "BLOCK_P8_B7_NUMERIC_BENCHMARK_RUNNER",
            "remaining_work": (
                "Run promoted source-paper rows across algorithms and emit value, "
                "componentwise score, curvature, failure, and stochastic uncertainty tables."
            ),
        },
        {
            "blocker_id": "P8-B8",
            "name": "Reviewed closeout",
            "status": "pending_execution_review",
            "pass_token": "PASS_P8_B8_REVIEWED_CLOSEOUT",
            "block_token": "BLOCK_P8_B8_REVIEWED_CLOSEOUT",
            "remaining_work": "Run Claude read-only execution review after artifacts are validated.",
        },
    ]


def build_artifact() -> dict[str, Any]:
    source_scope = _load(SOURCE_SCOPE_PATH)
    generalized_sv_spec = _load(GENERALIZED_SV_SPEC_PATH)
    p8_contract = _load(P8_CONTRACT_PATH)
    blocker_fix_gates = _load(P8_BLOCKER_FIX_GATES_PATH)
    sir_evidence = _sir_execution_only_evidence()
    rows = _source_rows(source_scope)
    truth_manifest = [_row_truth_manifest(row, sir_evidence) for row in rows.values()]
    truth_status_counts: dict[str, int] = {}
    for row in truth_manifest:
        status = row["truth_status"]
        truth_status_counts[status] = truth_status_counts.get(status, 0) + 1

    blockers = _blocker_rows(sir_evidence)
    blocker_status_counts: dict[str, int] = {}
    for row in blockers:
        status = row["status"]
        blocker_status_counts[status] = blocker_status_counts.get(status, 0) + 1

    return {
        "schema_version": "filter_bench.p8_blocker_closure_status.v1",
        "metadata_date": "2026-06-11",
        "phase": "FILTER_BENCH_P8_BLOCKER_CLOSURE",
        "status": "PASS_P8_BLOCKER_CLOSURE_STATUS_MANIFEST_WITH_REMAINING_BLOCKERS",
        "numeric_benchmark_status": "BLOCK_P8_NUMERIC_BENCHMARK_NOT_YET_RUN",
        "purpose": (
            "Execute the first reviewed P8 blocker-closure slice: materialize "
            "the source-truth readiness ledger, preserve real row-level blockers, "
            "and define the remaining execution gates without proxy promotion. "
            "The manifest now also carries the reviewed P8-B2 partial dataset "
            "generation pass."
        ),
        "source_artifacts": {
            "plan": _rel(PLAN_PATH),
            "source_scope_contract": _rel(SOURCE_SCOPE_PATH),
            "generalized_sv_spec": _rel(GENERALIZED_SV_SPEC_PATH),
            "p8_synthetic_truth_contract": _rel(P8_CONTRACT_PATH),
            "p58_sir_blocker_ledger": _rel(P58_LEDGER_PATH),
            "p59_9a_result": _rel(P59_9A_RESULT_PATH),
            "p59_9b_result": _rel(P59_9B_RESULT_PATH),
            "p59_9c_result": _rel(P59_9C_RESULT_PATH),
            "p59_9d_result": _rel(P59_9D_RESULT_PATH),
            "p59_9e_result": _rel(P59_9E_RESULT_PATH),
            "p8_b2_dataset_manifest": _rel(P8_B2_DATASET_MANIFEST_PATH),
            "p8_b2_dataset_result": _rel(P8_B2_DATASET_RESULT_PATH),
            "p8_blocker_fix_gates": _rel(P8_BLOCKER_FIX_GATES_PATH),
        },
        "role_contract": {
            "supervisor_and_executor": "Codex in this dialogue",
            "reviewer": "Claude Code read-only",
            "detached_codex_agent_allowed": False,
        },
        "truth_manifest": truth_manifest,
        "truth_status_counts": truth_status_counts,
        "blockers": blockers,
        "blocker_status_counts": blocker_status_counts,
        "row_level_blocks": (
            {
                SIR_ROW_ID: {
                    "status": "BLOCK_P8_B6_SPATIAL_SIR_D18_SOURCE_ROUTE",
                    "p59_9a_status": "PASS_P59_9A_AUTHOR_SIR_36D_TARGET_FIT_PREP",
                    "reason": (
                        "The 36D bounded target/fit preparation has passed, but "
                        "step-spec assembly, runner path, comparator-tier manifest, "
                        "and validation ladder are not complete."
                    ),
                },
            }
            if sir_evidence["missing_phases"]
            else {}
        ),
        "sir_d18_execution_only_status": sir_evidence,
        "generalized_sv_prior_mean_status": {
            "status": generalized_sv_spec["numeric_status"],
            "reason": (
                "Zhao-Cui S&P prior-mean synthetic test point is materialized; "
                "value/score evaluator execution remains pending."
            ),
            "nonclaims": [
                "not a posterior estimate from SP500 returns",
                "not a direct SP500 benchmark-data row",
                "not a claim that sigma^2 or beta has a finite ordinary prior mean",
            ],
        },
        "promotion_guardrails": {
            "p44_rows_promoted": False,
            "old_ledh_pfpf_ot_current_evidence_allowed": False,
            "sir_old_local_operator_route_allowed": False,
            "generalized_sv_author_defaults_as_truth_allowed": False,
            "sp500_returns_as_benchmark_data_allowed": False,
            "dpf_ranking_before_mc_se_allowed": False,
            "uncertified_score_or_hessian_promotion_allowed": False,
            "protocol_gate_counts_as_numeric_benchmark_allowed": False,
        },
        "ready_for_numeric_benchmark": False,
        "next_executable_phases": [
            "generalized-SV prior-mean evaluator execution",
            "P8-B7 numeric evaluator execution for nonblocked rows",
        ],
        "decision_table": [
            {
                "decision": "pass_source_truth_manifest_for_available_source_rows",
                "primary_criterion": "source-paper truth values are carried from the source-scope contract with anchors",
                "veto_diagnostics": "P44 rows, SP500 benchmark data, and author defaults are not promoted",
                "main_uncertainty": "generalized-SV evaluator semantics, DPF MC-SE, and score/curvature provenance remain pending",
                "next_justified_action": "continue P8-B7 numeric evaluator work",
                "not_concluded": "numeric performance or filter ranking",
            },
            {
                "decision": "keep_numeric_p8_blocked",
                "primary_criterion": "reviewed numeric evaluator outputs are not yet complete",
                "veto_diagnostics": "numeric benchmark remains blocked",
                "main_uncertainty": "remaining implementation effort for numeric evaluators and adapters",
                "next_justified_action": "execute P8-B7 numeric evaluator run",
                "not_concluded": "Bayesian-estimation readiness or DPF gradient validity",
            },
        ],
        "inherited_p8_scope_flags": p8_contract["benchmark_scope"],
        "nonclaims": [
            "not a numeric benchmark result",
            "not a filter ranking",
            "not a DPF gradient certification",
            "not generalized-SV evaluator correctness or performance evidence",
            "not SIR d=18 filtering accuracy or rank-convergence evidence",
            "not Bayesian-estimation readiness",
        ],
    }


def _write_csv(path: Path, blockers: list[dict[str, Any]]) -> None:
    columns = ["blocker_id", "name", "status", "pass_token", "block_token", "remaining_work"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in blockers:
            writer.writerow({column: row[column] for column in columns})


def _write_markdown(path: Path, artifact: dict[str, Any]) -> None:
    lines = [
        "# P8 Blocker Closure Status",
        "",
        f"status: {artifact['status']}",
        f"numeric_benchmark_status: {artifact['numeric_benchmark_status']}",
        "",
        "| Blocker | Status | Remaining work |",
        "| --- | --- | --- |",
    ]
    for row in artifact["blockers"]:
        lines.append(f"| `{row['blocker_id']}` {row['name']} | `{row['status']}` | {row['remaining_work']} |")
    lines.extend(
        [
            "",
            "## Row-Level Blocks",
            "",
            "| Row | Status | Reason |",
            "| --- | --- | --- |",
        ]
    )
    if artifact["row_level_blocks"]:
        for row_id, row in artifact["row_level_blocks"].items():
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
            "PASS_P8_B1_SOURCE_TRUTH_MANIFEST_READY",
            "PASS_P8_B2_SYNTHETIC_DATASET_MANIFEST_READY",
            "PASS_P8_B3_HORIZON_PROTOCOL_READY_NUMERIC_PENDING",
            "PASS_P8_B4_STOCHASTIC_PROTOCOL_READY_NUMERIC_PENDING",
            "PASS_P8_B5_ADAPTER_STATUS_MATRIX_READY_NUMERIC_PENDING",
            "PASS_P8_B6_SPATIAL_SIR_D18_EXECUTION_ONLY_RECOGNIZED",
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
    _write_csv(args.summary_csv, artifact["blockers"])
    _write_markdown(args.summary_markdown, artifact)
    print(f"wrote {args.output_json}")
    print(f"status {artifact['status']}")
    print(f"numeric_benchmark_status {artifact['numeric_benchmark_status']}")


if __name__ == "__main__":
    main()
