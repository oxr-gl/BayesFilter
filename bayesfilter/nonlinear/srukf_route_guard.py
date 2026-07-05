"""Static route guard for admitted factor-propagating SR-UKF code."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


FORBIDDEN_SRUKF_ROUTE_PATTERNS: tuple[str, ...] = (
    "GradientTape",
    "tf_svd_sigma_point_filter",
    "eigenderivative",
    "strict_spd_principal_sqrt",
    "strict-SPD principal-root",
    "principal_sqrt_frechet_derivative",
)


@dataclass(frozen=True)
class SRUKFRouteGuardViolation:
    """One forbidden route occurrence found by the static guard."""

    pattern: str
    line_number: int
    line: str


def find_forbidden_srukf_routes(text: str) -> tuple[SRUKFRouteGuardViolation, ...]:
    """Return forbidden route occurrences in admitted SR-UKF implementation text."""

    violations: list[SRUKFRouteGuardViolation] = []
    for line_number, line in enumerate(str(text).splitlines(), start=1):
        for pattern in FORBIDDEN_SRUKF_ROUTE_PATTERNS:
            if pattern in line:
                violations.append(
                    SRUKFRouteGuardViolation(
                        pattern=pattern,
                        line_number=line_number,
                        line=line.strip(),
                    )
                )
    return tuple(violations)


def assert_no_forbidden_srukf_routes(
    paths: Iterable[str | Path],
) -> tuple[SRUKFRouteGuardViolation, ...]:
    """Raise if any admitted SR-UKF source path contains a forbidden route."""

    all_violations: list[SRUKFRouteGuardViolation] = []
    for path_like in paths:
        path = Path(path_like)
        violations = find_forbidden_srukf_routes(path.read_text(encoding="utf-8"))
        all_violations.extend(violations)
    if all_violations:
        formatted = "; ".join(
            f"{violation.pattern}@{violation.line_number}: {violation.line}"
            for violation in all_violations
        )
        raise ValueError(f"forbidden_srukf_route_detected: {formatted}")
    return tuple()
