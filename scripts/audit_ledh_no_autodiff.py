#!/usr/bin/env python
"""Manifest-driven no-autodiff audit for LEDH-PFPF-OT routes.

This tool is intentionally conservative.  A production route fails if scoped
production files contain forbidden autodiff patterns, if a production
``tf.custom_gradient`` boundary has a ``grad`` body that opens autodiff, if bad
route flags are selected, or if whitelist governance is too broad.
"""

from __future__ import annotations

import argparse
import contextlib
import json
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FORBIDDEN_PATTERNS = (
    "tf.GradientTape",
    "GradientTape(",
    ".gradient(",
    ".jacobian(",
    ".batch_jacobian(",
    "tf.gradients",
    "tf.autodiff.ForwardAccumulator",
    "ForwardAccumulator(",
    "tf.custom_gradient",
    "@tf.custom_gradient",
    "gradient_override_map",
    "RegisterGradient",
    "custom_gradient",
    "watch(",
)
BAD_ROUTE_FLAGS = {
    "transport_ad_mode": {"full"},
    "ad_evaluation_mode": {"reverse-gradient", "forward-jvp"},
    "transport_gradient_mode": {"filterflow_custom_op"},
}
GRAD_BODY_FORBIDDEN_PATTERNS = (
    "tf.GradientTape",
    "GradientTape(",
    "tf.autodiff.ForwardAccumulator",
    "ForwardAccumulator(",
    ".gradient(",
    ".jacobian(",
    ".batch_jacobian(",
    "tf.gradients",
)


class AuditError(RuntimeError):
    """Raised when audit inputs violate governance before scanning."""


class RuntimeAutodiffViolation(RuntimeError):
    """Raised by the runtime sentinel when production code opens autodiff."""


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    pattern: str
    text: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "line": self.line,
            "pattern": self.pattern,
            "text": self.text.strip(),
        }


def _repo_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def _rel_path(path: str | Path) -> str:
    candidate = Path(path)
    if candidate.is_absolute():
        try:
            return str(candidate.relative_to(ROOT))
        except ValueError:
            return str(candidate)
    return str(candidate)


def load_json(path: str | Path) -> dict[str, Any]:
    with _repo_path(path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise AuditError(f"{path} must contain a JSON object")
    return payload


def validate_whitelist(whitelist: dict[str, Any], production_files: list[str]) -> list[dict[str, Any]]:
    vetoes: list[dict[str, Any]] = []
    if whitelist.get("zero_default") is not True:
        vetoes.append({"reason": "zero_default_not_true"})
    production_set = {_rel_path(path) for path in production_files}
    for index, entry in enumerate(whitelist.get("entries", [])):
        if not isinstance(entry, dict):
            vetoes.append({"reason": "entry_not_object", "index": index})
            continue
        if "path_prefix" in entry or "directory" in entry:
            vetoes.append({"reason": "directory_wide_entry", "index": index, "entry": entry})
        path = entry.get("path")
        symbol = entry.get("symbol")
        if bool(path) == bool(symbol):
            vetoes.append({"reason": "entry_must_have_exactly_one_path_or_symbol", "index": index, "entry": entry})
        if path:
            rel = _rel_path(path)
            if rel.endswith("/"):
                vetoes.append({"reason": "directory_path_entry", "index": index, "path": rel})
            if rel in production_set:
                vetoes.append({"reason": "production_path_whitelisted", "index": index, "path": rel})
        if symbol:
            for production in production_set:
                if str(symbol).startswith(production):
                    vetoes.append(
                        {
                            "reason": "production_symbol_whitelisted",
                            "index": index,
                            "symbol": symbol,
                            "production_file": production,
                        }
                    )
    return vetoes


def scan_file(path: str | Path, patterns: tuple[str, ...] | list[str]) -> list[Finding]:
    rel = _rel_path(path)
    full = _repo_path(path)
    findings: list[Finding] = []
    with full.open("r", encoding="utf-8") as handle:
        for number, line in enumerate(handle, start=1):
            for pattern in patterns:
                if pattern in line:
                    findings.append(Finding(path=rel, line=number, pattern=pattern, text=line))
    return findings


def scan_files(paths: list[str], patterns: tuple[str, ...] | list[str]) -> list[Finding]:
    findings: list[Finding] = []
    for path in paths:
        findings.extend(scan_file(path, patterns))
    return findings


def _top_level_symbol_spans(path: str | Path) -> dict[str, tuple[int, int]]:
    full = _repo_path(path)
    lines = full.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[str, int]] = []
    pending_decorators: list[int] = []
    for index, line in enumerate(lines, start=1):
        stripped = line.lstrip(" ")
        if line.startswith("@"):
            pending_decorators.append(index)
            continue
        if line.startswith("def ") or line.startswith("class "):
            name = stripped.split("(", 1)[0].split(":", 1)[0].split()[1]
            start = pending_decorators[0] if pending_decorators else index
            starts.append((name, start))
            pending_decorators = []
            continue
        if line and not line.startswith((" ", "\t")):
            pending_decorators = []
    spans: dict[str, tuple[int, int]] = {}
    for position, (name, start) in enumerate(starts):
        end = starts[position + 1][1] - 1 if position + 1 < len(starts) else len(lines)
        spans[name] = (start, end)
    return spans


def _manifest_symbol_spans(manifest: dict[str, Any], key: str) -> dict[str, list[dict[str, Any]]]:
    by_path: dict[str, list[dict[str, Any]]] = {}
    span_cache: dict[str, dict[str, tuple[int, int]]] = {}
    for entry in manifest.get(key, []):
        if not isinstance(entry, dict):
            continue
        path = _rel_path(str(entry.get("path", "")))
        symbol = str(entry.get("symbol", ""))
        if not path or not symbol:
            continue
        if path not in span_cache:
            span_cache[path] = _top_level_symbol_spans(path)
        if symbol not in span_cache[path]:
            raise AuditError(f"symbol {symbol!r} not found in {path}")
        start, end = span_cache[path][symbol]
        record = dict(entry)
        record["path"] = path
        record["symbol"] = symbol
        record["start_line"] = start
        record["end_line"] = end
        by_path.setdefault(path, []).append(record)
    return by_path


def _manifest_line_ranges(manifest: dict[str, Any], key: str) -> dict[str, list[dict[str, Any]]]:
    by_path: dict[str, list[dict[str, Any]]] = {}
    for entry in manifest.get(key, []):
        if not isinstance(entry, dict):
            continue
        path = _rel_path(str(entry.get("path", "")))
        if not path:
            continue
        start = int(entry.get("start_line", entry.get("line", -1)))
        end = int(entry.get("end_line", start))
        if start <= 0 or end < start:
            raise AuditError(f"invalid line range in {key}: {entry}")
        record = dict(entry)
        record["path"] = path
        record["start_line"] = start
        record["end_line"] = end
        by_path.setdefault(path, []).append(record)
    return by_path


def _span_record_for_line(
    spans_by_path: dict[str, list[dict[str, Any]]],
    path: str,
    line: int,
) -> dict[str, Any] | None:
    for span in spans_by_path.get(_rel_path(path), []):
        if int(span["start_line"]) <= line <= int(span["end_line"]):
            return span
    return None


def _allowed_custom_gradient_decorator_lines(manifest: dict[str, Any]) -> set[tuple[str, int]]:
    allowed: set[tuple[str, int]] = set()
    for entry in manifest.get("allowed_custom_gradient_boundaries", []):
        if not isinstance(entry, dict):
            continue
        path = _rel_path(str(entry.get("path", "")))
        decorator_line = int(entry.get("decorator_line", -1))
        if path and decorator_line > 0:
            allowed.add((path, decorator_line))
    return allowed


def _classify_production_findings(
    findings: list[Finding],
    manifest: dict[str, Any],
) -> tuple[list[Finding], list[dict[str, Any]]]:
    if manifest.get("route_scope") != "selected_route_exact":
        return findings, []
    excluded_symbol_spans = _manifest_symbol_spans(manifest, "excluded_symbols")
    excluded_line_ranges = _manifest_line_ranges(manifest, "excluded_line_ranges")
    allowed_decorator_lines = _allowed_custom_gradient_decorator_lines(manifest)
    active: list[Finding] = []
    excluded: list[dict[str, Any]] = []
    for finding in findings:
        line_key = (finding.path, finding.line)
        if (
            line_key in allowed_decorator_lines
            and finding.pattern in {"tf.custom_gradient", "@tf.custom_gradient", "custom_gradient"}
        ):
            excluded.append(
                {
                    **finding.as_dict(),
                    "classification": "allowed_manual_custom_gradient_boundary",
                    "reason": "decorator line is listed in allowed_custom_gradient_boundaries; grad body is audited separately",
                }
            )
            continue
        span = _span_record_for_line(excluded_symbol_spans, finding.path, finding.line)
        if span is not None:
            excluded.append(
                {
                    **finding.as_dict(),
                    "classification": span.get("classification", "excluded_symbol"),
                    "symbol": span.get("symbol"),
                    "reason": span.get("reason", ""),
                }
            )
            continue
        line_range = _span_record_for_line(excluded_line_ranges, finding.path, finding.line)
        if line_range is not None:
            excluded.append(
                {
                    **finding.as_dict(),
                    "classification": line_range.get("classification", "excluded_line_range"),
                    "reason": line_range.get("reason", ""),
                }
            )
            continue
        active.append(finding)
    return active, excluded


def _classify_custom_gradient_results(
    results: list[dict[str, Any]],
    manifest: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    if manifest.get("route_scope") != "selected_route_exact":
        return results, [], []
    excluded_symbol_spans = _manifest_symbol_spans(manifest, "excluded_symbols")
    excluded_line_ranges = _manifest_line_ranges(manifest, "excluded_line_ranges")
    allowed_decorator_lines = _allowed_custom_gradient_decorator_lines(manifest)
    selected: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    unapproved: list[dict[str, Any]] = []
    for result in results:
        path = _rel_path(str(result.get("path", "")))
        decorator_line = int(result.get("decorator_line", -1))
        if (path, decorator_line) in allowed_decorator_lines:
            selected.append(result)
            continue
        span = _span_record_for_line(excluded_symbol_spans, path, decorator_line)
        line_range = _span_record_for_line(excluded_line_ranges, path, decorator_line)
        if span is not None or line_range is not None:
            record = dict(result)
            if span is not None:
                record["classification"] = span.get("classification", "excluded_symbol")
                record["symbol"] = span.get("symbol")
                record["reason"] = span.get("reason", "")
            else:
                record["classification"] = line_range.get("classification", "excluded_line_range")
                record["reason"] = line_range.get("reason", "")
            excluded.append(record)
            continue
        unapproved.append(result)
    return selected, excluded, unapproved


def _indent_width(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def custom_gradient_grad_body_results(paths: list[str]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for path in paths:
        rel = _rel_path(path)
        full = _repo_path(path)
        lines = full.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            if "@tf.custom_gradient" not in line:
                continue
            decorator_line = index + 1
            def_line = None
            def_indent = None
            for cursor in range(index + 1, len(lines)):
                stripped = lines[cursor].lstrip(" ")
                if stripped.startswith("def "):
                    def_line = cursor + 1
                    def_indent = _indent_width(lines[cursor])
                    break
            grad_line = None
            end_index = len(lines)
            if def_line is not None and def_indent is not None:
                for cursor in range(def_line, len(lines)):
                    stripped = lines[cursor].lstrip(" ")
                    indent = _indent_width(lines[cursor])
                    if cursor > def_line and indent <= def_indent and stripped.startswith("def "):
                        end_index = cursor
                        break
                    if stripped.startswith("def grad"):
                        grad_line = cursor + 1
            body_findings: list[Finding] = []
            if grad_line is not None:
                for cursor in range(grad_line - 1, end_index):
                    for pattern in GRAD_BODY_FORBIDDEN_PATTERNS:
                        if pattern in lines[cursor]:
                            body_findings.append(
                                Finding(
                                    path=rel,
                                    line=cursor + 1,
                                    pattern=pattern,
                                    text=lines[cursor],
                                )
                            )
            results.append(
                {
                    "path": rel,
                    "decorator_line": decorator_line,
                    "def_line": def_line,
                    "grad_line": grad_line,
                    "status": "FAIL_GRAD_BODY_AUTODIFF" if body_findings else "PASS_GRAD_BODY_SCAN",
                    "findings": [finding.as_dict() for finding in body_findings],
                }
            )
    return results


def bad_route_flag_vetoes(route_flags: dict[str, Any]) -> list[dict[str, Any]]:
    vetoes: list[dict[str, Any]] = []
    for key, bad_values in BAD_ROUTE_FLAGS.items():
        value = route_flags.get(key)
        if value in bad_values:
            vetoes.append({"flag": key, "value": value, "reason": "bad_production_route_flag"})
    return vetoes


def _finding_matches_p1(finding: Finding, p1: dict[str, Any]) -> bool:
    return (
        finding.path == _rel_path(str(p1.get("path", "")))
        and int(p1.get("line", -1)) == finding.line
        and str(p1.get("pattern", "")) in finding.text
    )


def failed_expected_p1_ids(
    findings: list[Finding],
    grad_results: list[dict[str, Any]],
    manifest: dict[str, Any],
) -> list[str]:
    expected = set(manifest.get("expected_negative_control_failures", []))
    p1_entries = {
        str(entry.get("id")): entry for entry in manifest.get("p1_findings", [])
        if str(entry.get("id")) in expected
    }
    failed: set[str] = set()
    for p1_id, entry in p1_entries.items():
        if any(_finding_matches_p1(finding, entry) for finding in findings):
            failed.add(p1_id)
            continue
        for result in grad_results:
            for grad_finding in result.get("findings", []):
                if (
                    _rel_path(str(entry.get("path", ""))) == grad_finding.get("path")
                    and int(entry.get("line", -1)) == int(grad_finding.get("line", -2))
                ):
                    failed.add(p1_id)
    return sorted(failed)


def audit_manifest(manifest: dict[str, Any], whitelist: dict[str, Any]) -> dict[str, Any]:
    production_files = [_rel_path(path) for path in manifest.get("production_files", [])]
    diagnostic_files = [_rel_path(path) for path in manifest.get("diagnostic_or_test_files", [])]
    patterns = tuple(manifest.get("forbidden_patterns", DEFAULT_FORBIDDEN_PATTERNS))
    raw_production_findings = scan_files(production_files, patterns)
    production_findings, excluded_production_findings = _classify_production_findings(
        raw_production_findings,
        manifest,
    )
    diagnostic_findings = scan_files(diagnostic_files, patterns) if diagnostic_files else []
    raw_grad_results = custom_gradient_grad_body_results(production_files)
    selected_grad_results, excluded_grad_results, unapproved_grad_results = (
        _classify_custom_gradient_results(raw_grad_results, manifest)
    )
    grad_results = selected_grad_results if manifest.get("route_scope") == "selected_route_exact" else raw_grad_results
    whitelist_vetoes = validate_whitelist(whitelist, production_files)
    route_vetoes = bad_route_flag_vetoes(dict(manifest.get("route_flags", {})))
    failed_ids = failed_expected_p1_ids(production_findings, grad_results, manifest)
    expected = sorted(str(item) for item in manifest.get("expected_negative_control_failures", []))
    missing_expected = [item for item in expected if item not in set(failed_ids)]
    grad_body_failures = [
        result for result in grad_results
        if result.get("status") == "FAIL_GRAD_BODY_AUTODIFF"
    ]
    current_route_failed = bool(
        production_findings
        or route_vetoes
        or whitelist_vetoes
        or missing_expected
        or grad_body_failures
        or unapproved_grad_results
    )
    decision = "FAIL_CURRENT_ROUTE" if current_route_failed else "PASS_NO_AUTODIFF_AUDIT"
    nonclaims = [
        "audit tooling result only",
        "not GPU feasibility",
        "not FD agreement",
    ]
    if decision == "FAIL_CURRENT_ROUTE":
        nonclaims.append("not no-autodiff certification")
        nonclaims.append("current route failed the selected audit contract")
    else:
        nonclaims.append("no-autodiff certification for the exact manifest route only")
        nonclaims.append("not transferable to a different route manifest")
    return {
        "schema_version": "ledh_no_autodiff_audit_result.v1",
        "route_id": manifest.get("route_id"),
        "decision": decision,
        "failed_p1_ids": failed_ids,
        "missing_expected_negative_control_failures": missing_expected,
        "production_findings": [finding.as_dict() for finding in production_findings],
        "excluded_production_findings": excluded_production_findings,
        "raw_production_findings_count": len(raw_production_findings),
        "diagnostic_whitelist_hits": [finding.as_dict() for finding in diagnostic_findings],
        "production_whitelist_vetoes": whitelist_vetoes,
        "bad_route_flag_vetoes": route_vetoes,
        "custom_gradient_boundary_results": grad_results,
        "excluded_custom_gradient_boundary_results": excluded_grad_results,
        "unapproved_custom_gradient_boundary_results": unapproved_grad_results,
        "runtime_sentinel_result": {
            "sentinel_available": True,
            "full_route_runtime_not_executed": True,
            "reason": "P2 static negative-control audit; focused sentinel behavior is covered by tests",
        },
        "nonclaims": nonclaims,
    }


class AutodiffRuntimeSentinel(contextlib.AbstractContextManager["AutodiffRuntimeSentinel"]):
    """Audit-only context that blocks TensorFlow autodiff entrypoints."""

    def __init__(self, tf_module: Any, *, route_id: str, allow_diagnostic: bool = False) -> None:
        self.tf_module = tf_module
        self.route_id = route_id
        self.allow_diagnostic = allow_diagnostic
        self._original_gradient_tape: Any = None
        self._original_forward_accumulator: Any = None

    def __enter__(self) -> "AutodiffRuntimeSentinel":
        self._original_gradient_tape = getattr(self.tf_module, "GradientTape")
        autodiff = getattr(self.tf_module, "autodiff", None)
        if autodiff is not None and hasattr(autodiff, "ForwardAccumulator"):
            self._original_forward_accumulator = getattr(autodiff, "ForwardAccumulator")

        def _blocked_gradient_tape(*_args: Any, **_kwargs: Any) -> Any:
            raise RuntimeAutodiffViolation(
                f"production route {self.route_id} attempted to open tf.GradientTape"
            )

        def _blocked_forward_accumulator(*_args: Any, **_kwargs: Any) -> Any:
            raise RuntimeAutodiffViolation(
                f"production route {self.route_id} attempted to open tf.autodiff.ForwardAccumulator"
            )

        setattr(self.tf_module, "GradientTape", _blocked_gradient_tape)
        if autodiff is not None and self._original_forward_accumulator is not None:
            setattr(autodiff, "ForwardAccumulator", _blocked_forward_accumulator)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        del exc_type, exc_value, traceback
        if self._original_gradient_tape is not None:
            setattr(self.tf_module, "GradientTape", self._original_gradient_tape)
        autodiff = getattr(self.tf_module, "autodiff", None)
        if autodiff is not None and self._original_forward_accumulator is not None:
            setattr(autodiff, "ForwardAccumulator", self._original_forward_accumulator)
        return None


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--whitelist", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--expect-decision", choices=("FAIL_CURRENT_ROUTE", "PASS_NO_AUTODIFF_AUDIT"))
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    manifest = load_json(args.manifest)
    whitelist = load_json(args.whitelist)
    result = audit_manifest(manifest, whitelist)
    output = _repo_path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.expect_decision and result["decision"] != args.expect_decision:
        return 2
    if not args.expect_decision and result["decision"] != "PASS_NO_AUTODIFF_AUDIT":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
