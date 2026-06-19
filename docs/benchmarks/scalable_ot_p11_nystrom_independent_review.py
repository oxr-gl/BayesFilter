"""Independent Agent B review for Phase 11 Nystrom artifacts.

This script inspects existing Agent A JSON/result artifacts only.  It does not
run Agent A diagnostics, mutate Agent A files, fetch packages, use GPU evidence,
or establish speedup/default/posterior/HMC readiness claims.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import json
from pathlib import Path
import platform
import re
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from docs.benchmarks.scalable_ot_candidate_result_schema import (
    SchemaValidationError,
    validate_candidate_result,
)


REQUIRED_FIXTURE_RANKS = {
    "tiny_manual": {"1", "2", "3", "full"},
    "small_parity": {"2", "4", "8", "full"},
    "high_dim_low_rank": {"2", "4", "8", "16", "full"},
    "high_dim_locality": {"2", "4", "8", "16", "full"},
    "ledh_specific_smoke": {"2", "4", "8", "16", "full"},
}

PROMOTION_FIXTURES = {
    "tiny_manual",
    "small_parity",
    "high_dim_low_rank",
    "ledh_specific_smoke",
}

REQUIRED_TOP_KEYS = {
    "candidate_records",
    "fixture_summaries",
    "fixtures",
    "hard_vetoes",
    "manifest",
    "nonclaims",
    "phase11_status",
    "settings",
    "source_anchors",
    "source_route_components",
    "status",
    "summary",
    "thresholds",
}

REQUIRED_DENSE_FIELDS = {
    "dense_reference_max_abs_particle_error",
    "dense_reference_rms_particle_error",
}

REQUIRED_TOP_NONCLAIMS = {
    "no speedup claim",
    "no ranking claim",
    "no production default change",
    "no posterior correctness claim",
    "no HMC readiness claim",
    "no public API readiness claim",
    "no production readiness claim",
    "no statistically supported ranking",
}

FORBIDDEN_POSITIVE_PATTERNS = {
    "speedup proven",
    "establishes speedup",
    "production-ready",
    "production ready",
    "default-ready",
    "default ready",
    "posterior-correct",
    "posterior correct",
    "posterior correctness established",
    "hmc-ready",
    "hmc ready",
    "public api ready",
    "fastest",
    "best algorithm",
    "statistically supported ranking",
}

NEGATION_MARKERS = {
    "no ",
    "not ",
    "does not",
    "do not",
    "cannot",
    "| none",
    "not established",
    "not concluded",
}


@dataclass(frozen=True)
class Finding:
    severity: str
    finding_id: str
    path: str
    message: str
    recommendation: str
    field: str | None = None
    line: int | None = None
    evidence: Any = None
    blocks_agree: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "finding_id": self.finding_id,
            "path": self.path,
            "field": self.field,
            "line": self.line,
            "message": self.message,
            "evidence": self.evidence,
            "recommendation": self.recommendation,
            "blocks_agree": self.blocks_agree,
        }


def _finding(
    findings: list[Finding],
    severity: str,
    finding_id: str,
    path: Path,
    message: str,
    recommendation: str,
    *,
    field: str | None = None,
    line: int | None = None,
    evidence: Any = None,
    blocks_agree: bool | None = None,
) -> None:
    if blocks_agree is None:
        blocks_agree = severity in {"BLOCKER", "HIGH"}
    findings.append(
        Finding(
            severity=severity,
            finding_id=finding_id,
            path=str(path),
            field=field,
            line=line,
            message=message,
            evidence=evidence,
            recommendation=recommendation,
            blocks_agree=blocks_agree,
        )
    )


def _line_hits(text: str, phrase: str) -> list[tuple[int, str]]:
    hits: list[tuple[int, str]] = []
    needle = phrase.lower()
    for lineno, line in enumerate(text.splitlines(), start=1):
        if needle in line.lower():
            hits.append((lineno, line.strip()))
    return hits


def _positive_claim_lines(text: str) -> list[tuple[int, str, str]]:
    hits: list[tuple[int, str, str]] = []
    lines = text.splitlines()
    paragraph_lines: list[tuple[int, str]] = []
    for index, line in enumerate(lines, start=1):
        if line.strip():
            paragraph_lines.append((index, line.strip()))
            continue
        hits.extend(_positive_claim_paragraph_hits(paragraph_lines))
        paragraph_lines = []
    hits.extend(_positive_claim_paragraph_hits(paragraph_lines))
    return hits


def _positive_claim_paragraph_hits(paragraph_lines: list[tuple[int, str]]) -> list[tuple[int, str, str]]:
    if not paragraph_lines:
        return []
    paragraph = " ".join(line for _, line in paragraph_lines)
    sentence_starts = [m.start() for m in re.finditer(r"(?<!\d)[.!?](?:\s+|$)", paragraph)]
    sentences: list[str] = []
    start = 0
    for end_marker in sentence_starts:
        sentences.append(paragraph[start : end_marker + 1].strip())
        start = end_marker + 1
    tail = paragraph[start:].strip()
    if tail:
        sentences.append(tail)

    hits: list[tuple[int, str, str]] = []
    first_line = paragraph_lines[0][0]
    for sentence in sentences:
        lowered = sentence.lower()
        for pattern in FORBIDDEN_POSITIVE_PATTERNS:
            if pattern in lowered and not any(marker in lowered for marker in NEGATION_MARKERS):
                hits.append((first_line, pattern, sentence))
    return hits


def _severity_counts(findings: list[Finding]) -> dict[str, int]:
    counts = Counter(f.severity for f in findings)
    return {severity: counts.get(severity, 0) for severity in ("BLOCKER", "HIGH", "MEDIUM", "LOW")}


def _decision(findings: list[Finding]) -> str:
    severities = {f.severity for f in findings if f.blocks_agree}
    if "BLOCKER" in severities:
        return "BLOCKED"
    if "HIGH" in severities:
        return "REVISE_AGENT_A"
    if findings:
        return "AGREE_WITH_NONBLOCKING_FINDINGS"
    return "AGREE"


def _record_identity(record: dict[str, Any]) -> tuple[str | None, str | None]:
    diagnostics = record.get("diagnostics", {})
    if not isinstance(diagnostics, dict):
        return None, None
    fixture = diagnostics.get("fixture")
    rank_label = diagnostics.get("rank_label")
    return str(fixture) if fixture is not None else None, str(rank_label) if rank_label is not None else None


def review(agent_a_json: Path, agent_a_result: Path) -> dict[str, Any]:
    findings: list[Finding] = []
    data = json.loads(agent_a_json.read_text(encoding="utf-8"))
    result_text = agent_a_result.read_text(encoding="utf-8")

    if not isinstance(data, dict):
        _finding(
            findings,
            "BLOCKER",
            "json_not_mapping",
            agent_a_json,
            "Agent A JSON root is not a mapping.",
            "Regenerate the Agent A diagnostic JSON with the declared manifest shape.",
            blocks_agree=True,
        )
        return _build_review(agent_a_json, agent_a_result, data, result_text, findings, {})

    missing_top = sorted(REQUIRED_TOP_KEYS.difference(data))
    if missing_top:
        _finding(
            findings,
            "BLOCKER",
            "missing_top_level_manifest_keys",
            agent_a_json,
            "Agent A JSON is missing required top-level manifest keys.",
            "Regenerate or amend the diagnostic JSON so the manifest can be reviewed.",
            field="top_level",
            evidence=missing_top,
        )

    records = data.get("candidate_records")
    if not isinstance(records, list) or not records:
        _finding(
            findings,
            "BLOCKER",
            "candidate_records_missing_or_empty",
            agent_a_json,
            "Top-level candidate_records is missing, not a list, or empty.",
            "Write direct Phase 3 candidate records under top-level candidate_records.",
            field="candidate_records",
        )
        records = []

    schema_warnings: list[dict[str, Any]] = []
    by_fixture_rank: dict[tuple[str | None, str | None], list[int]] = defaultdict(list)
    reduced_viable: dict[str, list[str]] = defaultdict(list)
    dense_roles: dict[str, set[str]] = defaultdict(set)

    for index, record in enumerate(records):
        field_prefix = f"candidate_records[{index}]"
        if not isinstance(record, dict):
            _finding(
                findings,
                "BLOCKER",
                "candidate_record_not_mapping",
                agent_a_json,
                "A candidate_records entry is not a direct mapping.",
                "Emit direct Phase 3 record mappings under candidate_records.",
                field=field_prefix,
                evidence=type(record).__name__,
            )
            continue
        if "candidate_record" in record:
            _finding(
                findings,
                "HIGH",
                "nested_candidate_record_shape",
                agent_a_json,
                "A candidate_records entry contains a nested candidate_record wrapper.",
                "Use direct top-level Phase 3 records, one per fixture/rank pair.",
                field=field_prefix,
            )
        try:
            warnings = validate_candidate_result(record)
        except SchemaValidationError as exc:
            _finding(
                findings,
                "BLOCKER",
                "schema_validation_failed",
                agent_a_json,
                "A direct candidate record failed Phase 3 schema validation.",
                "Repair Agent A diagnostic record fields before interpreting the artifact.",
                field=field_prefix,
                evidence=str(exc),
            )
            continue
        for warning in warnings:
            schema_warnings.append({"index": index, "warning": warning})

        fixture, rank_label = _record_identity(record)
        by_fixture_rank[(fixture, rank_label)].append(index)
        diagnostics = record.get("diagnostics", {})
        diagnostic_roles = record.get("diagnostic_roles", {})

        if not str(record.get("baseline_comparator", "")).startswith("phase1_dense_streaming"):
            _finding(
                findings,
                "BLOCKER",
                "bad_baseline_prefix",
                agent_a_json,
                "Candidate record baseline_comparator does not begin phase1_dense_streaming.",
                "Recompute or amend Agent A diagnostics against the Phase 1 dense/streaming comparator.",
                field=f"{field_prefix}.baseline_comparator",
                evidence=record.get("baseline_comparator"),
            )

        if record.get("source_route") == "source_faithful":
            _finding(
                findings,
                "HIGH",
                "whole_route_source_faithful_overclaim",
                agent_a_json,
                "Candidate record marks the whole route source_faithful.",
                "Keep the whole route fixed_hmc_adaptation and classify only anchored sub-operations as source_faithful.",
                field=f"{field_prefix}.source_route",
                evidence=record.get("source_route"),
            )

        if record.get("source_route") != "fixed_hmc_adaptation":
            _finding(
                findings,
                "HIGH",
                "unexpected_source_route",
                agent_a_json,
                "Candidate record source_route is not fixed_hmc_adaptation.",
                "Use fixed_hmc_adaptation for the whole local prototype route unless a reviewed exception expands the target.",
                field=f"{field_prefix}.source_route",
                evidence=record.get("source_route"),
            )

        if not isinstance(diagnostics, dict):
            _finding(
                findings,
                "BLOCKER",
                "diagnostics_not_mapping",
                agent_a_json,
                "Candidate diagnostics is not a mapping.",
                "Emit diagnostic fields needed for fixture/rank artifact review.",
                field=f"{field_prefix}.diagnostics",
            )
            continue

        missing_dense = sorted(REQUIRED_DENSE_FIELDS.difference(diagnostics))
        if missing_dense:
            _finding(
                findings,
                "BLOCKER",
                "missing_dense_reference_fields",
                agent_a_json,
                "Candidate record is missing dense-reference max/RMS fields.",
                "Emit dense_reference_max_abs_particle_error and dense_reference_rms_particle_error for every fixture/rank.",
                field=f"{field_prefix}.diagnostics",
                evidence=missing_dense,
            )

        if diagnostics.get("is_full_rank") is False and diagnostics.get("reduced_rank_viability_pass") is True:
            if fixture is not None and rank_label is not None:
                reduced_viable[str(fixture)].append(str(rank_label))

        for name in REQUIRED_DENSE_FIELDS:
            role = diagnostic_roles.get(name)
            if role is not None and fixture is not None:
                dense_roles[str(fixture)].add(str(role))

        if diagnostic_roles.get("runtime_proxy_seconds") != "explanatory":
            _finding(
                findings,
                "HIGH",
                "runtime_proxy_not_explanatory",
                agent_a_json,
                "Runtime proxy is not classified as explanatory.",
                "Keep runtime proxy fields explanatory until a reviewed runtime evidence contract exists.",
                field=f"{field_prefix}.diagnostic_roles.runtime_proxy_seconds",
                evidence=diagnostic_roles.get("runtime_proxy_seconds"),
            )
        if diagnostic_roles.get("memory_proxy") != "explanatory":
            _finding(
                findings,
                "HIGH",
                "memory_proxy_not_explanatory",
                agent_a_json,
                "Memory proxy is not classified as explanatory.",
                "Keep memory proxy fields explanatory until a reviewed memory evidence contract exists.",
                field=f"{field_prefix}.diagnostic_roles.memory_proxy",
                evidence=diagnostic_roles.get("memory_proxy"),
            )
        if diagnostics.get("runtime_proxy_role") != "explanatory_only_until_validity_gates_pass":
            _finding(
                findings,
                "MEDIUM",
                "runtime_proxy_role_missing_or_changed",
                agent_a_json,
                "Runtime proxy role text is missing or changed.",
                "Record that runtime is explanatory only until validity gates pass.",
                field=f"{field_prefix}.diagnostics.runtime_proxy_role",
                evidence=diagnostics.get("runtime_proxy_role"),
                blocks_agree=False,
            )

    if schema_warnings:
        _finding(
            findings,
            "MEDIUM",
            "schema_validation_warnings",
            agent_a_json,
            "Phase 3 schema validation returned warnings.",
            "Inspect and repair warning sources before comparative synthesis.",
            field="candidate_records",
            evidence=schema_warnings,
            blocks_agree=False,
        )

    duplicates = {
        f"{fixture}:{rank}": indices
        for (fixture, rank), indices in by_fixture_rank.items()
        if fixture is not None and rank is not None and len(indices) != 1
    }
    if duplicates:
        _finding(
            findings,
            "BLOCKER",
            "duplicate_fixture_rank_records",
            agent_a_json,
            "Candidate records are not exactly one direct record per fixture/rank pair.",
            "Deduplicate direct records so every planned fixture/rank has exactly one record.",
            field="candidate_records",
            evidence=duplicates,
        )

    observed_by_fixture: dict[str, set[str]] = defaultdict(set)
    for fixture, rank_label in by_fixture_rank:
        if fixture is not None and rank_label is not None:
            observed_by_fixture[str(fixture)].add(str(rank_label))

    missing_fixtures = sorted(set(REQUIRED_FIXTURE_RANKS).difference(observed_by_fixture))
    if missing_fixtures:
        _finding(
            findings,
            "BLOCKER",
            "missing_required_fixtures",
            agent_a_json,
            "Required fixtures are missing from candidate_records.",
            "Rerun or amend diagnostics to include all required fixtures.",
            field="candidate_records",
            evidence=missing_fixtures,
        )
    for fixture, required_ranks in REQUIRED_FIXTURE_RANKS.items():
        missing_ranks = sorted(required_ranks.difference(observed_by_fixture.get(fixture, set())))
        extra_ranks = sorted(observed_by_fixture.get(fixture, set()).difference(required_ranks))
        if missing_ranks:
            _finding(
                findings,
                "BLOCKER",
                "missing_required_ranks",
                agent_a_json,
                "Required rank labels are missing for a fixture.",
                "Rerun or amend diagnostics with the predeclared rank grid.",
                field=f"candidate_records.{fixture}",
                evidence=missing_ranks,
            )
        if extra_ranks:
            _finding(
                findings,
                "LOW",
                "extra_rank_labels",
                agent_a_json,
                "Unexpected extra rank labels are present for a fixture.",
                "Confirm these extra records are intentional before comparative synthesis.",
                field=f"candidate_records.{fixture}",
                evidence=extra_ranks,
                blocks_agree=False,
            )

    summary = data.get("summary", {})
    if isinstance(summary, dict):
        if summary.get("candidate_record_count") != len(records):
            _finding(
                findings,
                "MEDIUM",
                "candidate_record_count_mismatch",
                agent_a_json,
                "Summary candidate_record_count does not match actual record count.",
                "Refresh summary counts so readers can audit coverage.",
                field="summary.candidate_record_count",
                evidence={"summary": summary.get("candidate_record_count"), "actual": len(records)},
                blocks_agree=False,
            )
        viability_by_fixture = summary.get("viability_by_fixture", {})
        if isinstance(viability_by_fixture, dict):
            if viability_by_fixture.get("high_dim_locality") is not None:
                _finding(
                    findings,
                    "HIGH",
                    "high_dim_locality_promoted",
                    agent_a_json,
                    "high_dim_locality is not marked explanatory-only in summary viability.",
                    "Keep high_dim_locality explanatory and out of promotion viability.",
                    field="summary.viability_by_fixture.high_dim_locality",
                    evidence=viability_by_fixture.get("high_dim_locality"),
                )
            for fixture in sorted(PROMOTION_FIXTURES):
                if viability_by_fixture.get(fixture) is not True:
                    _finding(
                        findings,
                        "HIGH",
                        "promotion_fixture_not_viable",
                        agent_a_json,
                        "A promotion fixture does not have a viable reduced rank in summary.",
                        "Do not promote Phase 11 diagnostic continuation until every promotion fixture has a viable reduced rank.",
                        field=f"summary.viability_by_fixture.{fixture}",
                        evidence=viability_by_fixture.get(fixture),
                    )
        else:
            _finding(
                findings,
                "BLOCKER",
                "summary_viability_not_mapping",
                agent_a_json,
                "summary.viability_by_fixture is not a mapping.",
                "Emit fixture-level viability summary for artifact review.",
                field="summary.viability_by_fixture",
            )
    else:
        _finding(
            findings,
            "BLOCKER",
            "summary_not_mapping",
            agent_a_json,
            "JSON summary is missing or not a mapping.",
            "Emit summary section needed for artifact review.",
            field="summary",
        )

    for fixture in sorted(PROMOTION_FIXTURES):
        if not reduced_viable.get(fixture):
            _finding(
                findings,
                "HIGH",
                "no_viable_reduced_rank_record",
                agent_a_json,
                "No non-full record has reduced_rank_viability_pass=True for a promotion fixture.",
                "Treat Phase 11 as not promoted until a genuine reduced rank passes or record a repair-trigger rationale.",
                field=f"candidate_records.{fixture}",
            )

    if dense_roles.get("high_dim_locality") and dense_roles["high_dim_locality"] != {"explanatory"}:
        _finding(
            findings,
            "HIGH",
            "high_dim_locality_dense_role_not_explanatory",
            agent_a_json,
            "high_dim_locality dense-reference diagnostics are not all explanatory.",
            "Keep high_dim_locality dense-reference behavior explanatory by plan.",
            field="candidate_records.high_dim_locality.diagnostic_roles",
            evidence=sorted(dense_roles["high_dim_locality"]),
        )

    top_nonclaims = set(data.get("nonclaims", [])) if isinstance(data.get("nonclaims"), list) else set()
    missing_nonclaims = sorted(REQUIRED_TOP_NONCLAIMS.difference(top_nonclaims))
    if missing_nonclaims:
        _finding(
            findings,
            "HIGH",
            "missing_json_nonclaims",
            agent_a_json,
            "Top-level JSON nonclaims are missing required non-claims.",
            "Add explicit nonclaims before using the artifact in comparative synthesis.",
            field="nonclaims",
            evidence=missing_nonclaims,
        )

    if data.get("source_route_components", {}).get("filterflow_cost_scaling_adapter") != "fixed_hmc_adaptation":
        _finding(
            findings,
            "HIGH",
            "filterflow_adapter_not_fixed_hmc_adaptation",
            agent_a_json,
            "FilterFlow cost scaling adapter is not classified as fixed_hmc_adaptation.",
            "Classify local FilterFlow adapters as fixed_hmc_adaptation, not source_faithful.",
            field="source_route_components.filterflow_cost_scaling_adapter",
            evidence=data.get("source_route_components", {}).get("filterflow_cost_scaling_adapter"),
        )

    for lineno, line in _line_hits(result_text, "nested candidate record"):
        _finding(
            findings,
            "LOW",
            "result_nested_candidate_wording",
            agent_a_result,
            "Result note uses stale nested-candidate wording while JSON uses direct top-level candidate_records.",
            "Refresh result prose to say direct top-level candidate_records, without changing Agent B review evidence.",
            line=lineno,
            evidence=line,
            blocks_agree=False,
        )
    for lineno, line in _line_hits(result_text, "nested `candidate_records`"):
        _finding(
            findings,
            "LOW",
            "result_nested_candidate_records_wording",
            agent_a_result,
            "Result note uses stale nested candidate_records wording while JSON uses direct top-level records.",
            "Refresh result prose to say direct top-level candidate_records.",
            line=lineno,
            evidence=line,
            blocks_agree=False,
        )

    for lineno, pattern, line in _positive_claim_lines(result_text):
        _finding(
            findings,
            "HIGH",
            "forbidden_positive_claim_text",
            agent_a_result,
            "Result text appears to contain an unsupported positive readiness/performance claim.",
            "Replace with explicit non-claim wording unless a reviewed evidence contract supports the claim.",
            line=lineno,
            evidence={"pattern": pattern, "line": line},
        )

    required_result_phrases = {
        "No speedup": "no speedup",
        "No default readiness": "no production/default readiness",
        "No posterior correctness": "no posterior correctness",
        "No HMC readiness": "no HMC readiness",
        "No ranking": "no statistically supported ranking",
        "Whole route fixed_hmc_adaptation": "whole implementation route remains `fixed_hmc_adaptation`",
    }
    lowered_result = result_text.lower()
    for label, phrase in required_result_phrases.items():
        if phrase.lower() not in lowered_result:
            _finding(
                findings,
                "MEDIUM",
                "missing_result_nonclaim_or_route_phrase",
                agent_a_result,
                f"Result text is missing expected non-claim/source-route phrase: {label}.",
                "Refresh result text so non-claims and whole-route classification are auditable.",
                evidence=phrase,
                blocks_agree=False,
            )

    metrics = {
        "record_count": len(records),
        "fixtures": {fixture: sorted(ranks) for fixture, ranks in sorted(observed_by_fixture.items())},
        "schema_warning_count": len(schema_warnings),
        "reduced_viable_ranks": {fixture: sorted(ranks) for fixture, ranks in sorted(reduced_viable.items())},
        "high_dim_locality_dense_roles": sorted(dense_roles.get("high_dim_locality", set())),
    }
    return _build_review(agent_a_json, agent_a_result, data, result_text, findings, metrics)


def _build_review(
    agent_a_json: Path,
    agent_a_result: Path,
    data: Any,
    result_text: str,
    findings: list[Finding],
    metrics: dict[str, Any],
) -> dict[str, Any]:
    counts = _severity_counts(findings)
    decision = _decision(findings)
    return {
        "review_status": "COMPLETED",
        "agent_b_recommended_decision": decision,
        "finding_counts_by_severity": counts,
        "blocks_agree": any(f.blocks_agree for f in findings),
        "findings": [f.to_dict() for f in sorted(findings, key=_finding_sort_key)],
        "metrics": metrics,
        "artifact_paths": {
            "agent_a_json": str(agent_a_json),
            "agent_a_result": str(agent_a_result),
        },
        "manifest": {
            "python": sys.version,
            "platform": platform.platform(),
            "review_script": "docs/benchmarks/scalable_ot_p11_nystrom_independent_review.py",
            "agent_b_boundary": "read_only_review_of_agent_a_artifacts",
            "not_concluded": [
                "no speedup claim",
                "no ranking claim",
                "no production/default readiness",
                "no posterior correctness",
                "no HMC readiness",
                "no public API readiness",
            ],
        },
    }


def _finding_sort_key(finding: Finding) -> tuple[int, str]:
    order = {"BLOCKER": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    return order.get(finding.severity, 99), finding.finding_id


def write_markdown(review_data: dict[str, Any], path: Path) -> None:
    lines = [
        "# Agent B Independent Review: Phase 11 Nystrom",
        "",
        f"- Review status: `{review_data['review_status']}`",
        f"- Recommended decision: `{review_data['agent_b_recommended_decision']}`",
        f"- Blocks AGREE: `{review_data['blocks_agree']}`",
        "",
        "## Finding Counts",
        "",
        "| Severity | Count |",
        "| --- | ---: |",
    ]
    for severity, count in review_data["finding_counts_by_severity"].items():
        lines.append(f"| `{severity}` | `{count}` |")

    metrics = review_data.get("metrics", {})
    lines.extend(
        [
            "",
            "## Metrics",
            "",
            f"- Candidate records: `{metrics.get('record_count', 'N/A')}`",
            f"- Schema warnings: `{metrics.get('schema_warning_count', 'N/A')}`",
            f"- High-dim-locality dense roles: `{metrics.get('high_dim_locality_dense_roles', 'N/A')}`",
            "",
            "## Fixture Coverage",
            "",
            "| Fixture | Rank labels |",
            "| --- | --- |",
        ]
    )
    for fixture, ranks in metrics.get("fixtures", {}).items():
        lines.append(f"| `{fixture}` | `{ranks}` |")

    lines.extend(
        [
            "",
            "## Findings",
            "",
            "| Severity | ID | Blocks AGREE | Location | Message |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for finding in review_data["findings"]:
        location = finding["path"]
        if finding.get("line") is not None:
            location += f":{finding['line']}"
        elif finding.get("field"):
            location += f" `{finding['field']}`"
        message = str(finding["message"]).replace("|", "\\|")
        lines.append(
            f"| `{finding['severity']}` | `{finding['finding_id']}` | "
            f"`{finding['blocks_agree']}` | `{location}` | {message} |"
        )

    lines.extend(
        [
            "",
            "## Non-Claims",
            "",
            "- No speedup claim.",
            "- No ranking claim.",
            "- No production/default readiness.",
            "- No posterior correctness.",
            "- No HMC readiness.",
            "- No public API readiness.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent-a-json", type=Path, required=True)
    parser.add_argument("--agent-a-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--markdown-output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    review_data = review(args.agent_a_json, args.agent_a_result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(review_data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(review_data, args.markdown_output)
    print(json.dumps({
        "review_status": review_data["review_status"],
        "agent_b_recommended_decision": review_data["agent_b_recommended_decision"],
        "finding_counts_by_severity": review_data["finding_counts_by_severity"],
        "blocks_agree": review_data["blocks_agree"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
