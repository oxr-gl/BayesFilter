#!/usr/bin/env python
"""Emit the bounded P59-9d author-SIR M9 runner/readiness manifest."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import bayesfilter.highdim as highdim


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Emit the P59-9d author-SIR M9 runner/readiness manifest."
    )
    parser.add_argument(
        "--output",
        default=highdim.P59_9D_DEFAULT_MANIFEST_PATH,
        help="Manifest JSON output path.",
    )
    parser.add_argument(
        "--sample-count",
        type=int,
        default=1,
        help="Bounded retained reference sample count for the manifest smoke.",
    )
    parser.add_argument(
        "--fit-sample-count",
        type=int,
        default=highdim.P59_D18_EXECUTION_ONLY_FIT_SAMPLE_COUNT,
        help="Bounded fit probe count for the manifest smoke.",
    )
    parser.add_argument(
        "--comparator-tier",
        default="d18_execution_only",
        choices=highdim.P58_M9_ALLOWED_COMPARATOR_TIERS,
        help="Declared P59-9e comparator tier.",
    )
    args = parser.parse_args(argv)

    result = highdim.p59_author_sir_runner_manifest_path(
        manifest_path=Path(args.output),
        comparator_tier=args.comparator_tier,
        sample_count=args.sample_count,
        fit_sample_count=args.fit_sample_count,
        write_manifest=True,
    )
    print(result.status)
    print(result.manifest_path)
    if result.blockers:
        for blocker in result.blockers:
            print(blocker, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
