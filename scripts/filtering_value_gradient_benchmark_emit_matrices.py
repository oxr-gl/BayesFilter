#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-matrices-2026-06-10.json"
DEFAULT_VALUE_CSV = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-value-error-matrix-2026-06-10.csv"
DEFAULT_GRAD_CSV = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-gradient-error-matrix-2026-06-10.csv"
DEFAULT_VALUE_MD = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-value-error-matrix-2026-06-10.md"
DEFAULT_GRAD_MD = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-gradient-error-matrix-2026-06-10.md"

REGISTRY_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json"
REFERENCE_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-reference-oracles-2026-06-10.json"
ADAPTER_SCHEMA_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-adapter-schema-2026-06-10.json"
SEMANTICS_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-gradient-semantics-2026-06-10.json"
PREFLIGHT_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-preflight-matrix-2026-06-10.json"
DET_SMOKE_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-smoke-payloads-2026-06-10.json"
DPF_SMOKE_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-filter-smoke-payloads-2026-06-10.json"
RESULT_PATH = ROOT / "docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-runner-matrices-result-2026-06-10.md"


COMPARATOR_LABELS = [
    "exact_LGSSM",
    "exact_or_dense_numerical",
    "transformed_actual_nongaussian",
    "gaussian_mixture_surrogate",
    "approximate_nongaussian",
    "no_reference",
    "invalid_gradient",
    "historical_only",
]


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _smoke_payloads() -> dict[tuple[str, str], dict[str, Any]]:
    payloads: dict[tuple[str, str], dict[str, Any]] = {}
    for path in (DET_SMOKE_PATH, DPF_SMOKE_PATH):
        for payload in _load(path)["payloads"]:
            if payload["evidence_role"] == "historical_only":
                continue
            payloads[(payload["algorithm_id"], payload["registry_row_id"])] = payload
    return payloads


def _comparator_labels(row: dict[str, Any], cell: dict[str, Any]) -> list[str]:
    labels: list[str] = []
    row_id = row["registry_row_id"]
    reference_type = row["reference_type"]
    row_class = row["registry_row_class"]
    normalized = cell["normalized_gradient_status"]

    if row_id == "lgssm_exact_kalman_dim_1_2_3":
        labels.append("exact_LGSSM")
    elif reference_type == "dense_numerical":
        labels.append("exact_or_dense_numerical")
        if row_class in {"lower_rung_reference", "production_candidate"}:
            labels.append("approximate_nongaussian")
    elif reference_type == "transformed_actual_nongaussian":
        labels.append("transformed_actual_nongaussian")
    elif reference_type == "gaussian_mixture_surrogate":
        labels.append("gaussian_mixture_surrogate")
    elif reference_type in {"blocked_only", "diagnostic"}:
        labels.append("no_reference")
    else:
        labels.append("approximate_nongaussian")

    if normalized == "resampling_gradient_not_valid":
        labels.append("invalid_gradient")
    return labels


def _cell_status(cell: dict[str, Any]) -> str:
    source_status = cell["source_status"]
    kind = cell["cell_kind"]
    if source_status == "ADAPTER_REQUIRED_WITH_REASON":
        return "NOT_RUN_ADAPTER_REQUIRED"
    if source_status == "UNSUPPORTED_WITH_REASON":
        return "UNSUPPORTED_BY_TARGET"
    if source_status == "BLOCKED_VALUE_ROUTE":
        return "BLOCKED_VALUE_ROUTE"
    if source_status == "SCOUT_ONLY_NOT_TRUTH":
        return "SCOUT_ONLY_NOT_TRUTH"
    if source_status == "READY_DIAGNOSTIC_ONLY":
        return "DIAGNOSTIC_ONLY_NOT_PROMOTION"
    if kind == "smoke_fixture_available":
        return "SMOKE_FIXTURE_NOT_BENCHMARK_RESULT"
    return "STATUS_ONLY_FROM_COVERAGE"


def _p8_reasons(cell: dict[str, Any]) -> list[str]:
    reasons = [reason for reason in cell["reason_codes"] if reason != "NONE"]
    status = _cell_status(cell)
    if status == "SMOKE_FIXTURE_NOT_BENCHMARK_RESULT":
        reasons.append("SMOKE_FIXTURE_NOT_BENCHMARK_RESULT")
        reasons.append("P8_NUMERIC_BENCHMARK_NOT_EXECUTED")
    elif status == "STATUS_ONLY_FROM_COVERAGE":
        reasons.append("P8_NUMERIC_BENCHMARK_NOT_EXECUTED")
    elif status == "DIAGNOSTIC_ONLY_NOT_PROMOTION":
        reasons.append("DIAGNOSTIC_ROW_NOT_PROMOTION")
    if not cell["p8_gradient_error_eligible"]:
        reasons.append("GRADIENT_STATUS_ONLY_BY_P6_SEMANTICS")
    return sorted(set(reasons))


def _display_value(cell: dict[str, Any]) -> str:
    if cell["value_error_abs"] is None:
        return f"{cell['cell_status']} ({'+'.join(cell['reason_codes'][:2])})"
    return f"{cell['value_error_abs']:.3g}"


def _display_gradient(cell: dict[str, Any]) -> str:
    if cell["gradient_error_abs"] is None:
        return f"{cell['gradient_status']} ({'+'.join(cell['reason_codes'][:2])})"
    return f"{cell['gradient_error_abs']:.3g}"


def _write_csv(path: Path, matrix: dict[str, dict[str, dict[str, Any]]], rows: list[str], mode: str) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["algorithm_id", *rows])
        for algorithm_id, row_cells in matrix.items():
            if mode == "value":
                writer.writerow([algorithm_id, *[_display_value(row_cells[row]) for row in rows]])
            else:
                writer.writerow([algorithm_id, *[_display_gradient(row_cells[row]) for row in rows]])


def _write_md(path: Path, matrix: dict[str, dict[str, dict[str, Any]]], rows: list[str], mode: str) -> None:
    lines = []
    lines.append("| algorithm | " + " | ".join(rows) + " |")
    lines.append("| --- | " + " | ".join(["---"] * len(rows)) + " |")
    for algorithm_id, row_cells in matrix.items():
        if mode == "value":
            cells = [_display_value(row_cells[row]) for row in rows]
        else:
            cells = [_display_gradient(row_cells[row]) for row in rows]
        lines.append("| " + algorithm_id + " | " + " | ".join(cells) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_artifact() -> dict[str, Any]:
    registry = _load(REGISTRY_PATH)
    references = {row["registry_row_id"]: row for row in _load(REFERENCE_PATH)["rows"]}
    semantics = _load(SEMANTICS_PATH)
    preflight = _load(PREFLIGHT_PATH)
    smoke_payloads = _smoke_payloads()

    algorithm_ids = preflight["frozen_roster"]["algorithm_ids"]
    rows = preflight["frozen_roster"]["model_columns"]
    value_matrix: dict[str, dict[str, dict[str, Any]]] = {algorithm_id: {} for algorithm_id in algorithm_ids}
    gradient_matrix: dict[str, dict[str, dict[str, Any]]] = {algorithm_id: {} for algorithm_id in algorithm_ids}
    status_matrix: dict[str, dict[str, dict[str, Any]]] = {algorithm_id: {} for algorithm_id in algorithm_ids}
    diagnostics_matrix: dict[str, dict[str, dict[str, Any]]] = {algorithm_id: {} for algorithm_id in algorithm_ids}
    seed_level_raw_rows: list[dict[str, Any]] = []

    for cell in preflight["preflight_cells"]:
        algorithm_id = cell["algorithm_id"]
        row_id = cell["registry_row_id"]
        row = references[row_id]
        smoke = smoke_payloads.get((algorithm_id, row_id))
        labels = _comparator_labels(row, cell)
        reason_codes = _p8_reasons(cell)
        cell_status = _cell_status(cell)
        diagnostics: dict[str, Any] = {
            "source_kind": cell["source_kind"],
            "source_status": cell["source_status"],
            "cell_kind": cell["cell_kind"],
            "reference_type": row["reference_type"],
            "benchmark_class": row["benchmark_class"],
            "reference_gradient_policy": row["reference_gradient_policy"],
            "performance_interpretation": "not_performance_evidence",
        }
        if smoke is not None:
            diagnostics.update(
                {
                    "smoke_fixture_artifact": smoke["artifact_path"],
                    "smoke_runtime_seconds": smoke["runtime_seconds"],
                    "smoke_random_seed": smoke["random_seed"],
                    "algorithm_value_fixture": smoke["value"],
                    "algorithm_gradient_fixture": smoke["gradient"],
                    "mc_standard_error": smoke["diagnostics"].get("mc_standard_error"),
                    "particle_count": smoke["diagnostics"].get("particle_count"),
                    "effective_sample_size_min": smoke["diagnostics"].get(
                        "effective_sample_size_min"
                    ),
                    "resampling_policy": smoke["diagnostics"].get("resampling_policy"),
                    "seed_list": smoke["diagnostics"].get("seed_list"),
                }
            )
            for seed in smoke["diagnostics"].get("seed_list", []):
                seed_level_raw_rows.append(
                    {
                        "algorithm_id": algorithm_id,
                        "registry_row_id": row_id,
                        "seed": seed,
                        "aggregate_fixture_value": smoke["value"],
                        "seed_level_value": None,
                        "mc_standard_error": smoke["diagnostics"].get("mc_standard_error"),
                        "reason_codes": ["SMOKE_FIXTURE_NOT_BENCHMARK_RESULT"],
                        "performance_interpretation": "not_performance_evidence",
                    }
                )

        value_matrix[algorithm_id][row_id] = {
            "value_error_abs": None,
            "value_error_rel": None,
            "value_status": cell["value_status"],
            "cell_status": cell_status,
            "comparator_labels": labels,
            "reason_codes": reason_codes,
            "mc_standard_error": diagnostics.get("mc_standard_error"),
            "performance_interpretation": "not_performance_evidence",
        }
        gradient_matrix[algorithm_id][row_id] = {
            "gradient_error_abs": None,
            "gradient_error_rel": None,
            "gradient_status": cell["normalized_gradient_status"],
            "raw_gradient_status": cell["raw_gradient_status"],
            "p8_gradient_error_eligible": cell["p8_gradient_error_eligible"],
            "cell_status": cell_status,
            "comparator_labels": labels,
            "reason_codes": reason_codes,
            "performance_interpretation": "not_performance_evidence",
        }
        status_matrix[algorithm_id][row_id] = {
            "cell_status": cell_status,
            "value_status": cell["value_status"],
            "raw_gradient_status": cell["raw_gradient_status"],
            "normalized_gradient_status": cell["normalized_gradient_status"],
            "comparator_labels": labels,
            "reason_codes": reason_codes,
        }
        diagnostics_matrix[algorithm_id][row_id] = diagnostics

    return {
        "schema_version": "filter_bench.runner_matrices.v1",
        "metadata_date": "2026-06-10",
        "phase": "FILTER_BENCH_P8",
        "status": "BLOCK_FILTER_BENCH_P8_RUNNER_MATRICES",
        "blocker": {
            "blocked_token": "BLOCK_FILTER_BENCH_P8_RUNNER_MATRICES",
            "reason": "No reviewed full numeric benchmark runner exists for the frozen 7x12 roster; emitting complete status matrices is possible, but promoting smoke/preflight values to value or gradient errors would violate the evidence contract.",
            "required_repair": "Implement actual per-cell numeric benchmark adapters for the frozen roster or explicitly revise the P8 criterion before claiming benchmark performance.",
        },
        "source_artifacts": {
            "target_registry": _rel(REGISTRY_PATH),
            "adapter_schema": _rel(ADAPTER_SCHEMA_PATH),
            "reference_oracles": _rel(REFERENCE_PATH),
            "gradient_semantics": _rel(SEMANTICS_PATH),
            "preflight_matrix": _rel(PREFLIGHT_PATH),
            "deterministic_smoke_payloads": _rel(DET_SMOKE_PATH),
            "dpf_smoke_payloads": _rel(DPF_SMOKE_PATH),
        },
        "frozen_roster": preflight["frozen_roster"],
        "comparator_label_vocabulary": COMPARATOR_LABELS,
        "benchmark_scope": {
            "matrix_emission_complete": True,
            "numeric_benchmark_execution_complete": False,
            "performance_answer_complete": False,
            "p7_preflight_used_as_performance_evidence": False,
            "smoke_fixtures_used_as_performance_evidence": False,
            "old_ledh_pfpf_ot_current_evidence": False,
        },
        "run_manifest": {
            "git_commit": "dirty worktree; P8 artifacts uncommitted",
            "dirty_state_summary": "dirty worktree preserved; unrelated changes not reverted",
            "command": "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_matrices.py",
            "environment": "local Python environment",
            "conda_env": "N/A",
            "cpu_gpu_status": "CPU-only; CUDA_VISIBLE_DEVICES=-1 for validation; no GPU conclusion",
            "dtype": "manifest-level only; per-row dtype lives in P1 registry",
            "seeds": "Smoke payload seeds retained only as non-performance diagnostics",
            "plan_file": "docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-runner-matrices-subplan-2026-06-10.md",
            "result_file": _rel(RESULT_PATH),
            "output_json": _rel(DEFAULT_OUT),
            "value_csv": _rel(DEFAULT_VALUE_CSV),
            "gradient_csv": _rel(DEFAULT_GRAD_CSV),
            "value_markdown": _rel(DEFAULT_VALUE_MD),
            "gradient_markdown": _rel(DEFAULT_GRAD_MD),
            "registry_artifact": _rel(REGISTRY_PATH),
            "adapter_schema_artifact": _rel(ADAPTER_SCHEMA_PATH),
            "reference_oracle_artifact": _rel(REFERENCE_PATH),
        },
        "value_error_matrix": value_matrix,
        "gradient_error_matrix": gradient_matrix,
        "status_matrix": status_matrix,
        "diagnostics_matrix": diagnostics_matrix,
        "seed_level_raw_rows": seed_level_raw_rows,
        "historical_only_records": [
            {
                "algorithm_id": "ledh_pfpf_ot_historical",
                "comparator_labels": ["historical_only"],
                "current_evidence": False,
                "reason_codes": ["HISTORICAL_LEDHPFPF_OT_SUPERSEDED"],
            }
        ],
        "post_run_red_team_note": {
            "strongest_alternative_explanation": "The complete-looking matrices may be mistaken for performance matrices even though all numeric errors are null.",
            "would_overturn_blocker": "A reviewed command that computes actual value and eligible gradient errors for the frozen roster, with MC uncertainty for stochastic DPF rows and no proxy promotion.",
            "weakest_part_of_evidence": "P8 currently emits matrix structure and statuses, not full benchmark numerical results.",
        },
        "nonclaims": [
            "P8 output is not a filter ranking",
            "P8 output does not contain full numeric benchmark errors",
            "P7 preflight is not benchmark evidence",
            "smoke fixtures are not benchmark performance evidence",
            "no DPF gradient certification",
            "no HMC, GPU, or Bayesian-estimation readiness",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--value-csv", type=Path, default=DEFAULT_VALUE_CSV)
    parser.add_argument("--gradient-csv", type=Path, default=DEFAULT_GRAD_CSV)
    parser.add_argument("--value-markdown", type=Path, default=DEFAULT_VALUE_MD)
    parser.add_argument("--gradient-markdown", type=Path, default=DEFAULT_GRAD_MD)
    args = parser.parse_args()

    artifact = build_artifact()
    rows = artifact["frozen_roster"]["model_columns"]
    args.output_json.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    _write_csv(args.value_csv, artifact["value_error_matrix"], rows, "value")
    _write_csv(args.gradient_csv, artifact["gradient_error_matrix"], rows, "gradient")
    _write_md(args.value_markdown, artifact["value_error_matrix"], rows, "value")
    _write_md(args.gradient_markdown, artifact["gradient_error_matrix"], rows, "gradient")
    print(f"wrote {args.output_json}")
    print(f"status {artifact['status']}")


if __name__ == "__main__":
    main()
