#!/usr/bin/env python
"""Validate frozen-contract fields for the P71 Phase 4d ladder artifact."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import p67_author_sir_adjacent_ladder_diagnostics as p67

ROW_EXECUTION_PASS_STATUS = "PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY"


EXPECTED_ROW_SPECS = {
    label: {"degree": degree, "rank": rank, "fit_sample_count": fit_count}
    for label, degree, rank, fit_count in p67.ROW_SPECS
}
EXPECTED_FIT_BUDGETS = {
    "base_candidate": 16,
    "rank_pair": 36,
    "degree_pair": 24,
}


def validate_payload(payload: Mapping[str, Any]) -> tuple[str, ...]:
    blockers: list[str] = []
    rows = payload.get("rows")
    if not isinstance(rows, Mapping):
        return ("missing_rows_mapping",)
    observed_labels = set(rows)
    expected_labels = set(EXPECTED_ROW_SPECS)
    if observed_labels != expected_labels:
        blockers.append(
            "row_label_mismatch:"
            f"expected={sorted(expected_labels)} observed={sorted(observed_labels)}"
        )
    for label, expected in EXPECTED_ROW_SPECS.items():
        row = rows.get(label)
        if not isinstance(row, Mapping):
            blockers.append(f"{label}_missing_row_mapping")
            continue
        for field, expected_value in expected.items():
            if row.get(field) != expected_value:
                blockers.append(
                    f"{label}_{field}_mismatch:"
                    f"expected={expected_value} observed={row.get(field)}"
                )
    if payload.get("thresholds") != p67.THRESHOLDS:
        blockers.append("top_level_thresholds_mismatch")
    for ladder_name in ("rank_ladder", "degree_ladder"):
        ladder = payload.get(ladder_name)
        if not isinstance(ladder, Mapping):
            blockers.append(f"{ladder_name}_missing_mapping")
            continue
        if ladder.get("thresholds") != p67.THRESHOLDS:
            blockers.append(f"{ladder_name}_thresholds_mismatch")
    run_manifest = payload.get("run_manifest")
    if not isinstance(run_manifest, Mapping):
        blockers.append("missing_run_manifest_mapping")
    else:
        if run_manifest.get("cpu_only_intent") != "CUDA_VISIBLE_DEVICES=-1":
            blockers.append("cpu_only_intent_mismatch")
        if run_manifest.get("fit_budgets") != EXPECTED_FIT_BUDGETS:
            blockers.append("fit_budgets_mismatch")
        if run_manifest.get("sample_count") != 1:
            blockers.append("sample_count_mismatch")
        if run_manifest.get("bounded_screen_only") is not True:
            blockers.append("bounded_screen_only_missing")
    admitted = _admitted_rows(rows)
    if len(admitted) != 1:
        blockers.append(f"admitted_configuration_count_mismatch:{len(admitted)}")
    return tuple(blockers)


def _admitted_rows(rows: Mapping[str, Any]) -> tuple[str, ...]:
    admitted = []
    for label, row in rows.items():
        if not isinstance(row, Mapping):
            continue
        if (
            row.get("status") == ROW_EXECUTION_PASS_STATUS
            and row.get("budget_limited") is False
            and row.get("source_invariants", {}).get("passed") is True
        ):
            admitted.append(str(label))
    return tuple(admitted)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", required=True)
    args = parser.parse_args()
    payload = json.loads(Path(args.artifact).read_text())
    blockers = validate_payload(payload)
    if blockers:
        print(
            json.dumps(
                {
                    "phase4d_artifact_contract": "FAIL",
                    "blockers": blockers,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 2
    print(
        json.dumps(
            {
                "phase4d_artifact_contract": "PASS",
                "admitted_configuration_count": 1,
                "admitted_rows": _admitted_rows(payload["rows"]),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
