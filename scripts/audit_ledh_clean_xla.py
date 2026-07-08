#!/usr/bin/env python
"""Static clean-XLA guardrail for the LEDH-PFPF-OT score route.

This audit is intentionally narrow.  It checks the exact Phase 0 symbols and
pattern classes that currently make the corrected P8p SIR / streaming Sinkhorn
score path unclean for XLA compilation.  A current route with findings reports
``FAIL_CURRENT_ROUTE``; that is expected until later repair phases remove the
findings.
"""

from __future__ import annotations

import argparse
import ast
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SIR_PATH = ROOT / "docs" / "benchmarks" / "benchmark_p8p_parameterized_sir_gradient.py"
DEFAULT_TRANSPORT_PATH = (
    ROOT
    / "experiments"
    / "dpf_implementation"
    / "tf_tfp"
    / "resampling"
    / "annealed_transport_tf.py"
)


@dataclass(frozen=True)
class RequiredPattern:
    id: str
    file_key: str
    symbol: str
    patterns: tuple[str, ...]
    severity: str
    description: str


@dataclass(frozen=True)
class SymbolSpan:
    path: Path
    rel_path: str
    symbol: str
    node: ast.FunctionDef
    start_line: int
    end_line: int
    lines: list[str]


@dataclass(frozen=True)
class Finding:
    id: str
    path: str
    symbol: str
    line: int
    pattern: str
    severity: str
    text: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "path": self.path,
            "symbol": self.symbol,
            "line": self.line,
            "pattern": self.pattern,
            "severity": self.severity,
            "text": self.text.strip(),
        }


REQUIRED_PATTERNS: tuple[RequiredPattern, ...] = (
    RequiredPattern(
        id="SIR-RK4-FWD-LIST",
        file_key="sir",
        symbol="_sir_transition_mean_with_aux_tf",
        patterns=("aux: list[dict[str, tf.Tensor]] = []", "aux.append("),
        severity="current_veto",
        description="RK4 forward stores TensorFlow tensors in a Python aux list.",
    ),
    RequiredPattern(
        id="SIR-RK4-FWD-RANGE",
        file_key="sir",
        symbol="_sir_transition_mean_with_aux_tf",
        patterns=("for _ in range(int(substeps))",),
        severity="current_veto",
        description="RK4 forward substeps are Python-unrolled.",
    ),
    RequiredPattern(
        id="SIR-RK4-REV-REVERSED",
        file_key="sir",
        symbol="_sir_transition_mean_vjp_tf",
        patterns=("reversed(aux)",),
        severity="current_veto",
        description="RK4 reverse pass iterates over a Python aux list.",
    ),
    RequiredPattern(
        id="SIR-MANUAL-TIME-STATIC",
        file_key="sir",
        symbol="_manual_value_and_score_from_components",
        patterns=("time_steps = int(observations.shape[0])",),
        severity="current_veto",
        description="Manual route binds time length as a Python integer.",
    ),
    RequiredPattern(
        id="SIR-MANUAL-RECORD-LIST",
        file_key="sir",
        symbol="_manual_value_and_score_from_components",
        patterns=("records: list[", "records.append("),
        severity="current_veto",
        description="Manual route stores forward history in a Python records list.",
    ),
    RequiredPattern(
        id="SIR-MANUAL-FWD-RANGE",
        file_key="sir",
        symbol="_manual_value_and_score_from_components",
        patterns=("for time_index in range(time_steps)",),
        severity="current_veto",
        description="Manual route forward time scan is Python-unrolled.",
    ),
    RequiredPattern(
        id="SIR-MANUAL-SEED-LOOP",
        file_key="sir",
        symbol="_manual_value_and_score_from_components",
        patterns=("noise_rows = []", "for seed in args.batch_seeds", "noise_rows.append("),
        severity="current_veto",
        description="Fixed randomness is built with a Python seed loop in the route.",
    ),
    RequiredPattern(
        id="SIR-MANUAL-REV-REVERSED",
        file_key="sir",
        symbol="_manual_value_and_score_from_components",
        patterns=("reversed(records)",),
        severity="current_veto",
        description="Manual route reverse time scan iterates over Python records.",
    ),
    RequiredPattern(
        id="SINK-STOPPED-VALUE-KEY",
        file_key="transport",
        symbol="_filterflow_streaming_finite_sinkhorn_potentials_stopped_scale_keys",
        patterns=("key_x = tf.stop_gradient(x)",),
        severity="current_veto",
        description="Stopped-key value helper omits total derivative through the keys.",
    ),
    RequiredPattern(
        id="SINK-STOPPED-VALUE-RANGE",
        file_key="transport",
        symbol="_filterflow_streaming_finite_sinkhorn_potentials_stopped_scale_keys",
        patterns=("for _ in range(steps)",),
        severity="current_veto",
        description="Stopped-key value helper uses a Python Sinkhorn loop.",
    ),
    RequiredPattern(
        id="SINK-TOTAL-VALUE-RANGE",
        file_key="transport",
        symbol="_filterflow_streaming_finite_sinkhorn_potentials_total_vjp",
        patterns=("for _ in range(steps)",),
        severity="current_veto",
        description="Total value helper still uses a Python Sinkhorn loop.",
    ),
    RequiredPattern(
        id="SINK-STOPPED-VJP-KEY",
        file_key="transport",
        symbol="_filterflow_streaming_finite_sinkhorn_potentials_vjp_stopped_scale_keys",
        patterns=("key_x = tf.stop_gradient(x)",),
        severity="current_veto",
        description="Stopped-key VJP helper omits total derivative through the keys.",
    ),
    RequiredPattern(
        id="SINK-STOPPED-VJP-STATES",
        file_key="transport",
        symbol="_filterflow_streaming_finite_sinkhorn_potentials_vjp_stopped_scale_keys",
        patterns=("states = []", "states.append(", "for _ in range(steps)"),
        severity="current_veto",
        description="Stopped-key VJP helper stores Sinkhorn states in a Python list.",
    ),
    RequiredPattern(
        id="SINK-TOTAL-CUSTOM-TAPE",
        file_key="transport",
        symbol="_filterflow_manual_streaming_finite_transport_total_vjp",
        patterns=("tf.GradientTape", "tape.gradient("),
        severity="current_warning",
        description="Total streaming transport helper uses local autodiff.",
    ),
)


def _rel_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def _source_line(lines: list[str], line_number: int) -> str:
    if 1 <= line_number <= len(lines):
        return lines[line_number - 1]
    return ""


def _load_function_spans(path: Path) -> dict[str, SymbolSpan]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    lines = source.splitlines()
    spans: dict[str, SymbolSpan] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and isinstance(getattr(node, "parent", None), ast.Module):
            start_line = node.decorator_list[0].lineno if node.decorator_list else node.lineno
            if node.end_lineno is None:
                raise RuntimeError(f"missing end line for function {node.name} in {path}")
            spans[node.name] = SymbolSpan(
                path=path,
                rel_path=_rel_path(path),
                symbol=node.name,
                node=node,
                start_line=start_line,
                end_line=node.end_lineno,
                lines=lines,
            )
    return spans


def _with_parents(tree: ast.AST) -> ast.AST:
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            setattr(child, "parent", parent)
    return tree


def _load_function_spans_with_parent(path: Path) -> dict[str, SymbolSpan]:
    source = path.read_text(encoding="utf-8")
    tree = _with_parents(ast.parse(source))
    lines = source.splitlines()
    spans: dict[str, SymbolSpan] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and isinstance(getattr(node, "parent", None), ast.Module):
            start_line = node.decorator_list[0].lineno if node.decorator_list else node.lineno
            if node.end_lineno is None:
                raise RuntimeError(f"missing end line for function {node.name} in {path}")
            spans[node.name] = SymbolSpan(
                path=path,
                rel_path=_rel_path(path),
                symbol=node.name,
                node=node,
                start_line=start_line,
                end_line=node.end_lineno,
                lines=lines,
            )
    return spans


def _line_findings(pattern: RequiredPattern, span: SymbolSpan) -> list[Finding]:
    findings: list[Finding] = []
    for needle in pattern.patterns:
        for line_number in range(span.start_line, span.end_line + 1):
            text = _source_line(span.lines, line_number)
            if needle in text:
                findings.append(
                    Finding(
                        id=pattern.id,
                        path=span.rel_path,
                        symbol=span.symbol,
                        line=line_number,
                        pattern=needle,
                        severity=pattern.severity,
                        text=text,
                    )
                )
                break
    return findings


def audit_paths(
    *,
    sir_path: str | Path = DEFAULT_SIR_PATH,
    transport_path: str | Path = DEFAULT_TRANSPORT_PATH,
) -> dict[str, Any]:
    paths = {
        "sir": Path(sir_path),
        "transport": Path(transport_path),
    }
    spans_by_key = {key: _load_function_spans_with_parent(path) for key, path in paths.items()}
    required_results: list[dict[str, Any]] = []
    findings: list[Finding] = []
    warning_findings: list[Finding] = []
    missing_required_patterns: list[dict[str, Any]] = []
    absent_current_veto_patterns: list[dict[str, Any]] = []
    missing_warning_symbols: list[dict[str, Any]] = []

    for pattern in REQUIRED_PATTERNS:
        spans = spans_by_key[pattern.file_key]
        span = spans.get(pattern.symbol)
        if span is None:
            status = "MISSING_SYMBOL" if pattern.severity == "current_veto" else "MISSING_WARNING_SYMBOL"
            record = {
                "id": pattern.id,
                "path": _rel_path(paths[pattern.file_key]),
                "symbol": pattern.symbol,
                "severity": pattern.severity,
                "status": status,
                "description": pattern.description,
                "findings": [],
            }
            required_results.append(record)
            if status == "MISSING_SYMBOL":
                missing_required_patterns.append(record)
            else:
                missing_warning_symbols.append(record)
            continue

        pattern_findings = _line_findings(pattern, span)
        if pattern_findings:
            status = "FOUND_CURRENT_VETO" if pattern.severity == "current_veto" else "FOUND_WARNING"
            findings.extend(pattern_findings)
            if pattern.severity != "current_veto":
                warning_findings.extend(pattern_findings)
        else:
            status = "ABSENT_CLEAN_OR_MOVED" if pattern.severity == "current_veto" else "ABSENT_WARNING"
            if pattern.severity == "current_veto":
                absent_current_veto_patterns.append(
                    {
                        "id": pattern.id,
                        "path": span.rel_path,
                        "symbol": span.symbol,
                        "severity": pattern.severity,
                        "status": status,
                        "description": pattern.description,
                    }
                )
        required_results.append(
            {
                "id": pattern.id,
                "path": span.rel_path,
                "symbol": span.symbol,
                "start_line": span.start_line,
                "end_line": span.end_line,
                "severity": pattern.severity,
                "status": status,
                "description": pattern.description,
                "findings": [finding.as_dict() for finding in pattern_findings],
            }
        )

    current_veto_findings = [finding for finding in findings if finding.severity == "current_veto"]
    if missing_required_patterns:
        decision = "FAIL_AUDIT_CONFIGURATION"
    elif current_veto_findings:
        decision = "FAIL_CURRENT_ROUTE"
    else:
        decision = "PASS_STATIC_CLEAN_XLA_GUARDRAIL"

    summary_by_file: dict[str, dict[str, int]] = {}
    for finding in findings:
        summary = summary_by_file.setdefault(
            finding.path,
            {"current_veto": 0, "current_warning": 0},
        )
        summary[finding.severity] = summary.get(finding.severity, 0) + 1

    return {
        "schema_version": "ledh_clean_xla_static_audit.v1",
        "decision": decision,
        "required_pattern_results": required_results,
        "findings": [finding.as_dict() for finding in findings],
        "current_veto_findings": [finding.as_dict() for finding in current_veto_findings],
        "warning_findings": [finding.as_dict() for finding in warning_findings],
        "missing_required_patterns": missing_required_patterns,
        "missing_warning_symbols": missing_warning_symbols,
        "absent_current_veto_patterns": absent_current_veto_patterns,
        "summary_by_file": summary_by_file,
        "nonclaims": [
            "static guardrail result only",
            "not GPU/XLA runtime evidence",
            "not HLO evidence",
            "not numerical correctness evidence",
            "not HMC readiness evidence",
            "stopped partial derivatives are not scores",
        ],
    }


def audit_default() -> dict[str, Any]:
    return audit_paths()


def _format_text(result: dict[str, Any]) -> str:
    lines = [f"decision: {result['decision']}"]
    for finding in result["findings"]:
        lines.append(
            f"{finding['severity']} {finding['id']} "
            f"{finding['path']}:{finding['line']} {finding['pattern']}"
        )
    return "\n".join(lines)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sir-path", default=str(DEFAULT_SIR_PATH))
    parser.add_argument("--transport-path", default=str(DEFAULT_TRANSPORT_PATH))
    parser.add_argument("--format", choices=("json", "text"), default="text")
    parser.add_argument("--output", help="Optional path for writing the audit output.")
    args = parser.parse_args(list(argv) if argv is not None else None)

    result = audit_paths(sir_path=args.sir_path, transport_path=args.transport_path)
    if args.format == "json":
        output = json.dumps(result, indent=2, sort_keys=True)
    else:
        output = _format_text(result)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
