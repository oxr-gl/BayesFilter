#!/usr/bin/env python
"""P86 author Lagrangep algebraic route smoke runner.

The default and ``--schema-only`` modes do not fit or train.  ``--fit-smoke``
performs the single optimizer-step mechanics smoke only after exact human
approval of the command recorded in the P86 Phase 4 subplan.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Mapping

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("MPLCONFIGDIR", "/tmp")

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import tensorflow as tf

from bayesfilter.highdim.bases import (
    p85_author_sir_lagrangep_algebraic_product_basis_spec,
)
from bayesfilter.highdim.diagnostics import (
    DensityMeasure,
    MassMeasure,
    MeasureConvention,
)
from bayesfilter.highdim.stochastic_density_training import (
    P75ObjectiveBatch,
    P75TrainableTTConfig,
    TrainableFunctionalTT,
    make_adam_optimizer,
    terms_payload,
)


RUN_START = time.monotonic()
SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase4-tiny-author-route-fit-smoke-schema-2026-06-24.json"
)
FIT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase4-tiny-author-route-fit-smoke-2026-06-24.json"
)
PHASE4_SUBPLAN = (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase4-tiny-author-route-fit-smoke-subplan-2026-06-24.md"
)
PHASE4_RESULT = (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p86-phase4-tiny-author-route-fit-smoke-result-2026-06-24.md"
)
EXPECTED_FIT_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    "scripts/p86_author_lagrangep_fit_smoke.py --fit-smoke --dimension 2 "
    "--sample-count 8 --optimizer-steps 1 --seed 8604 --max-seconds 60 "
    "--output "
    "docs/plans/bayesfilter-highdim-zhao-cui-p86-phase4-tiny-author-route-fit-smoke-2026-06-24.json"
)
NONCLAIMS = (
    "tiny synthetic mechanics smoke only",
    "not an author SIR scientific fit",
    "not P84 budget-compliant fitting",
    "not fit-quality evidence",
    "not rank convergence evidence",
    "not posterior correctness evidence",
    "not KR closure evidence",
    "not HMC readiness evidence",
    "not LEDH comparison evidence",
    "not d50/d100 scale evidence",
    "not production readiness",
)


def _jsonable(value: Any) -> Any:
    if hasattr(value, "numpy"):
        return _jsonable(value.numpy())
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, float):
        if math.isnan(value):
            return "nan"
        if math.isinf(value):
            return "inf" if value > 0 else "-inf"
        return value
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    try:
        return float(value)
    except (TypeError, ValueError):
        return str(value)


def _write_payload(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n")


def _git_state_summary() -> Mapping[str, Any]:
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        porcelain = subprocess.check_output(
            ["git", "status", "--short"],
            cwd=REPO_ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).splitlines()
        return {
            "head": commit,
            "dirty": bool(porcelain),
            "status_short_count": len(porcelain),
        }
    except (OSError, subprocess.CalledProcessError) as exc:
        return {
            "head": "unknown",
            "dirty": "unknown",
            "status_error": str(exc),
        }


def _convention() -> MeasureConvention:
    return MeasureConvention(
        density_measure=DensityMeasure.REFERENCE_MEASURE,
        mass_measure=MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _route_spec(dimension: int):
    return p85_author_sir_lagrangep_algebraic_product_basis_spec(
        dimension=int(dimension),
        convention=_convention(),
    )


def _route_manifest(dimension: int) -> Mapping[str, Any]:
    spec = _route_spec(dimension)
    payload = spec.manifest_payload()
    return {
        "route_status": "hard_wired_author_lagrangep_algebraic",
        "basis_family": "lagrangep",
        "basis_order": 4,
        "basis_num_elems": 8,
        "basis_dim_tuple": payload["basis_dim_tuple"],
        "domain_map": "algebraic",
        "domain_scale": 1.0,
        "density_measure": DensityMeasure.REFERENCE_MEASURE.value,
        "mass_measure": MassMeasure.REFERENCE_MEASURE.value,
        "dtype": "float64",
        "dimension": int(dimension),
        "route_changing_cli": False,
        "source_anchors": payload["source_anchors"],
        "classification": payload["classification"],
        "classification_subtype": payload["classification_subtype"],
        "xla_static_fields": payload["xla_static_fields"],
        "nonclaims": payload["nonclaims"],
    }


def _config(*, dimension: int, seed: int) -> P75TrainableTTConfig:
    product_basis = _route_spec(dimension).build_product_basis()
    ranks = tuple([1] * (int(dimension) + 1))
    return P75TrainableTTConfig(
        product_basis=product_basis,
        ranks=ranks,
        tau=tf.constant(0.25, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        l2_weight=tf.constant(1e-8, dtype=tf.float64),
        learning_rate=1e-3,
        gradient_clip_norm=100.0,
        seed=int(seed),
        metadata={
            "fixture": "p86_author_lagrangep_tiny_synthetic_mechanics",
            "route": "hard_wired_lagrangep4x8_algebraic1",
            "smoke_only": True,
        },
    )


def _synthetic_batch(*, dimension: int, sample_count: int) -> P75ObjectiveBatch:
    count = int(sample_count)
    dim = int(dimension)
    if count < 2:
        raise ValueError("sample_count must be at least 2")
    reference = tf.linspace(
        tf.constant(-0.6, dtype=tf.float64),
        tf.constant(0.6, dtype=tf.float64),
        count,
    )
    columns = []
    for axis in range(dim):
        shift = tf.cast(axis, tf.float64) * tf.constant(0.07, dtype=tf.float64)
        clipped = tf.clip_by_value(
            reference + shift,
            tf.constant(-0.8, dtype=tf.float64),
            tf.constant(0.8, dtype=tf.float64),
        )
        physical = clipped * tf.math.rsqrt(1.0 - tf.square(clipped))
        columns.append(physical)
    points = tf.stack(columns, axis=1)
    target_values = tf.exp(
        -0.125 * tf.reduce_sum(tf.square(tf.stack(columns, axis=1)), axis=1)
    )
    weights = tf.ones([count], dtype=tf.float64)
    records = tuple(
        {
            "point_id": f"p86-phase4-synthetic-{index}",
            "cloud_hash": "p86-phase4-synthetic-training-only",
            "role": "fit",
        }
        for index in range(count)
    )
    return P75ObjectiveBatch(
        points=points,
        target_values=target_values,
        weights=weights,
        point_records=records,
        forbidden_audit_records=(
            {
                "point_id": "p86-phase4-forbidden-audit-marker",
                "cloud_hash": "p86-phase4-forbidden-audit",
                "role": "audit",
            },
        ),
        provenance_label="p86_phase4_synthetic_training_only",
    )


def _base_payload(output: Path, command: str, *, dimension: int, seed: int) -> Mapping[str, Any]:
    return {
        "schema_version": "p86_author_lagrangep_fit_smoke.v1",
        "script": str(SCRIPT_PATH.relative_to(REPO_ROOT)),
        "output": str(output),
        "command": command,
        "expected_fit_command": EXPECTED_FIT_COMMAND,
        "phase4_subplan": PHASE4_SUBPLAN,
        "phase4_result": PHASE4_RESULT,
        "git": _git_state_summary(),
        "environment": {
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "intentional_gpu_hiding": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
            "mplconfigdir": os.environ.get("MPLCONFIGDIR"),
            "python": sys.executable,
        },
        "route_manifest": _route_manifest(dimension),
        "seed": int(seed),
        "nonclaims": NONCLAIMS,
    }


def schema_payload(output: Path, command: str, *, dimension: int, seed: int) -> Mapping[str, Any]:
    config = _config(dimension=dimension, seed=seed)
    product_payload = config.product_basis.manifest_payload()
    return {
        **_base_payload(output, command, dimension=dimension, seed=seed),
        "status": "P86_PHASE4_SCHEMA_READY_NOT_FIT",
        "schema_only": True,
        "fit_smoke_executed": False,
        "optimizer_steps_completed": 0,
        "config": {
            "dimension": config.product_basis.dimension,
            "basis_dim_tuple": config.product_basis.basis_dim_tuple(),
            "ranks": config.ranks,
            "tau": float(config.tau.numpy()),
            "learning_rate": config.learning_rate,
            "gradient_clip_norm": config.gradient_clip_norm,
            "metadata": dict(config.metadata),
            "product_basis": product_payload,
        },
        "gate_summary": {
            "overall_status": "not_executed",
            "schema_only": True,
            "route_manifest_ok": _route_manifest_ok(product_payload),
            "fit_smoke_executed": False,
            "requires_exact_human_approval_before_fit": True,
        },
    }


def _route_manifest_ok(product_payload: Mapping[str, Any]) -> bool:
    bases = product_payload["bases"]
    return all(
        basis["family"] == "lagrangep"
        and basis["order"] == 4
        and basis["num_elems"] == 8
        and basis["basis_dim"] == 33
        and basis["domain_map"]["family"] == "algebraic"
        for basis in bases
    )


def fit_smoke_payload(
    output: Path,
    command: str,
    *,
    dimension: int,
    sample_count: int,
    optimizer_steps: int,
    seed: int,
    max_seconds: float,
) -> Mapping[str, Any]:
    if int(optimizer_steps) != 1:
        raise ValueError("P86 Phase 4 fit smoke is frozen to exactly one optimizer step")
    if Path(output) != FIT_OUTPUT:
        raise ValueError("P86 Phase 4 fit smoke output path is frozen by the approved command")
    if float(max_seconds) != 60.0:
        raise ValueError("P86 Phase 4 fit smoke max_seconds is frozen at 60")
    if int(dimension) != 2 or int(sample_count) != 8 or int(seed) != 8604:
        raise ValueError("P86 Phase 4 exact approval command is frozen to d=2, n=8, seed=8604")
    config = _config(dimension=dimension, seed=seed)
    batch = _synthetic_batch(dimension=dimension, sample_count=sample_count)
    trainer = TrainableFunctionalTT(config)
    optimizer = make_adam_optimizer(config)
    before = tuple(tf.identity(core) for core in trainer.variables)
    pre_terms = trainer.objective(batch)
    step_terms = None
    completed = 0
    stop_reason = "optimizer_steps_completed"
    for _ in range(int(optimizer_steps)):
        if time.monotonic() - RUN_START > float(max_seconds):
            stop_reason = "wall_clock_cap_reached_before_next_step"
            break
        step_terms = trainer.train_step(batch, optimizer)
        completed += 1
    if step_terms is None:
        raise RuntimeError("fit smoke produced no optimizer step")
    post_terms = trainer.objective(batch)
    deltas = [tf.norm(new - old) for old, new in zip(before, trainer.variables)]
    delta_stack = tf.stack(deltas)
    finite_deltas = bool(tf.reduce_all(tf.math.is_finite(delta_stack)).numpy())
    any_changed = bool(tf.reduce_any(delta_stack > 0.0).numpy())
    product_payload = config.product_basis.manifest_payload()
    route_ok = _route_manifest_ok(product_payload)
    status = (
        "P86_PHASE4_TINY_AUTHOR_ROUTE_FIT_SMOKE_COMPLETED"
        if completed == 1 and finite_deltas and any_changed and route_ok
        else "P86_PHASE4_TINY_AUTHOR_ROUTE_FIT_SMOKE_BLOCKED"
    )
    return {
        **_base_payload(output, command, dimension=dimension, seed=seed),
        "status": status,
        "schema_only": False,
        "fit_smoke_executed": True,
        "optimizer_steps_requested": int(optimizer_steps),
        "optimizer_steps_completed": int(completed),
        "max_seconds": float(max_seconds),
        "wall_time_seconds": round(time.monotonic() - RUN_START, 3),
        "stop_reason": stop_reason,
        "sample_count": int(sample_count),
        "batch": {
            "point_count": int(batch.points.shape[0]),
            "dimension": int(batch.points.shape[1]),
            "target_min": float(tf.reduce_min(batch.target_values).numpy()),
            "target_max": float(tf.reduce_max(batch.target_values).numpy()),
            "weight_sum": float(tf.reduce_sum(batch.weights).numpy()),
            "provenance_label": batch.provenance_label,
            "forbidden_audit_record_count": len(batch.forbidden_audit_records),
        },
        "config": {
            "dimension": config.product_basis.dimension,
            "basis_dim_tuple": config.product_basis.basis_dim_tuple(),
            "ranks": config.ranks,
            "tau": float(config.tau.numpy()),
            "learning_rate": config.learning_rate,
            "gradient_clip_norm": config.gradient_clip_norm,
            "metadata": dict(config.metadata),
            "product_basis": product_payload,
        },
        "terms": {
            "pre": terms_payload(pre_terms),
            "step": terms_payload(step_terms),
            "post": terms_payload(post_terms),
        },
        "parameter_delta_norms": deltas,
        "gate_summary": {
            "overall_status": "pass" if status.endswith("_COMPLETED") else "block",
            "route_manifest_ok": route_ok,
            "finite_parameter_deltas": finite_deltas,
            "any_core_changed": any_changed,
            "gradient_norm_finite": bool(
                tf.math.is_finite(tf.convert_to_tensor(step_terms.gradient_norm)).numpy()
            ),
            "optimizer_steps_completed": int(completed),
            "intentional_gpu_hiding": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
            "nonclaims": NONCLAIMS,
        },
    }


def _command_for_args(args: argparse.Namespace) -> str:
    output = args.output
    command = (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/p86_author_lagrangep_fit_smoke.py"
    )
    if args.fit_smoke:
        return EXPECTED_FIT_COMMAND
    else:
        command = f"{command} --schema-only"
    command = f"{command} --output {output}"
    return command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--schema-only", action="store_true")
    parser.add_argument("--fit-smoke", action="store_true")
    parser.add_argument("--dimension", type=int, default=2)
    parser.add_argument("--sample-count", type=int, default=8)
    parser.add_argument("--optimizer-steps", type=int, default=1)
    parser.add_argument("--seed", type=int, default=8604)
    parser.add_argument("--max-seconds", type=float, default=60.0)
    args = parser.parse_args(argv)
    if args.schema_only and args.fit_smoke:
        parser.error("--schema-only and --fit-smoke are mutually exclusive")
    command = _command_for_args(args)
    output = args.output
    payload = (
        fit_smoke_payload(
            output,
            command,
            dimension=args.dimension,
            sample_count=args.sample_count,
            optimizer_steps=args.optimizer_steps,
            seed=args.seed,
            max_seconds=args.max_seconds,
        )
        if args.fit_smoke
        else schema_payload(output, command, dimension=args.dimension, seed=args.seed)
    )
    _write_payload(output, payload)
    print(
        json.dumps(
            {
                "p86_status": payload["status"],
                "gate_summary": _jsonable(payload["gate_summary"]),
            },
            sort_keys=True,
        )
    )
    return 0 if payload["gate_summary"].get("overall_status") in {"pass", "not_executed"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
