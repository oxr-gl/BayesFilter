#!/usr/bin/env python
"""P77 budget-gated corrected-metric training runner.

This is an opt-in P77 surface.  It is not a source-faithful Zhao--Cui route and
does not expose the failed random, calibrated-constant, or source-route prefit
ladders.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time
from typing import Any, Mapping, Sequence

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("MPLCONFIGDIR", "/tmp")

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import tensorflow as tf

from bayesfilter.highdim import stochastic_density_training as p77_metric
import scripts.p76_bounded_ukf_minibatch_pilot as phase6
import scripts.p76_generated_corrected_metric_diagnostic as phase10


RUN_START = time.monotonic()
SCRIPT_PATH = Path(__file__).resolve()
STATUS_COMPLETED = "P77_BUDGETED_CORRECTED_METRIC_TRAINING_COMPLETED"
STATUS_BRIDGE_BLOCKED = "P77_BLOCKED_UKF_FRAME_BRIDGE"
STATUS_BUDGET_BLOCKED = "P77_BLOCKED_UNDER_BUDGET_EVIDENCE_REQUEST"
STATUS_SEED_BLOCKED = "P77_BLOCKED_SEED_OVERLAP"
STATUS_TRAINING_BLOCKED = "P77_BLOCKED_TRAINING_VETO"
STATUS_METRIC_BLOCKED = "P77_BLOCKED_METRIC_EVALUATION"
SCHEMA_VERSION = "p77.budgeted_corrected_metric_training.v1"
MASTER_PROGRAM = (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md"
)
PHASE3_SUBPLAN = (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-subplan-2026-06-19.md"
)
DEFAULT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p77-budgeted-corrected-metric-training-2026-06-19.json"
)
P77_MIN_TRAINING_SAMPLES_PER_PARAMETER = 20
P77_PREFERRED_BATCH_SIZE = 1024
P77_PREFERRED_BATCHES = 40
P77_LEARNING_RATES = (1e-4, 3e-4, 1e-3)
NONCLAIMS = (
    "not source-faithful Zhao-Cui",
    "not lower-gate repair evidence",
    "not HMC readiness evidence",
    "not scaling evidence",
    "not default-policy evidence",
    "not final rank or sample policy",
)
FAILED_ROUTE_FENCE = {
    "random_initialization_live_route": False,
    "calibrated_constant_live_route": False,
    "source_route_prefit_live_route": False,
    "failed_historical_routes_only": True,
}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--degree", type=int, default=2)
    parser.add_argument("--rank", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=P77_PREFERRED_BATCH_SIZE)
    parser.add_argument("--batches", type=int, default=P77_PREFERRED_BATCHES)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--max-seconds", type=float, default=900.0)
    parser.add_argument("--seed", type=int, default=7703)
    parser.add_argument(
        "--evidence-run",
        action="store_true",
        help="Mark this command as a training-evidence request; requires the 20P gate.",
    )
    args = parser.parse_args(argv)

    payload = budgeted_corrected_metric_training_payload(
        output=args.output,
        degree=args.degree,
        rank=args.rank,
        batch_size=args.batch_size,
        batches=args.batches,
        learning_rate=args.learning_rate,
        max_seconds=args.max_seconds,
        seed=args.seed,
        evidence_run=bool(args.evidence_run),
    )
    _write_payload(args.output, payload)
    return 0


def budgeted_corrected_metric_training_payload(
    *,
    output: Path,
    degree: int,
    rank: int,
    batch_size: int,
    batches: int,
    learning_rate: float,
    max_seconds: float,
    seed: int,
    evidence_run: bool,
) -> Mapping[str, Any]:
    _validate_static_args(
        degree=degree,
        rank=rank,
        batch_size=batch_size,
        batches=batches,
        learning_rate=learning_rate,
        max_seconds=max_seconds,
    )
    if float(learning_rate) not in P77_LEARNING_RATES:
        raise ValueError("learning_rate must be one of the predeclared P77 candidates")

    output = Path(output)
    run_manifest = _initial_run_manifest(output=output)
    parameter_manifest = _parameter_manifest(
        dimension=36,
        degree=int(degree),
        rank=int(rank),
    )
    budget_manifest = _budget_manifest(
        parameter_manifest=parameter_manifest,
        batch_size=int(batch_size),
        batches=int(batches),
        evidence_run=bool(evidence_run),
    )
    base = _base_payload(
        output=output,
        run_manifest=run_manifest,
        degree=int(degree),
        rank=int(rank),
        batch_size=int(batch_size),
        batches=int(batches),
        learning_rate=float(learning_rate),
        max_seconds=float(max_seconds),
        seed=int(seed),
        evidence_run=bool(evidence_run),
        parameter_manifest=parameter_manifest,
        budget_manifest=budget_manifest,
    )
    if bool(evidence_run) and not budget_manifest["hard_budget_gate_passed"]:
        return _with_final_wall_time(
            {
                **base,
                "status": STATUS_BUDGET_BLOCKED,
                "completed_batches": 0,
                "requested_batches": int(batches),
                "training_started": False,
                "optimizer_constructed": False,
                "metric_batches": {},
                "gate_summary": {
                    "overall_status": "block",
                    "blockers": ("under_budget_evidence_request",),
                    "hard_budget_gate_passed": False,
                    "training_started": False,
                    "metric_evaluated": False,
                    "not lower-gate repair": True,
                    "not HMC readiness": True,
                },
            }
        )

    context = _target_context(
        degree=int(degree),
        rank=int(rank),
        batch_size=int(batch_size),
        batches=int(batches),
        seed=int(seed),
        learning_rate=float(learning_rate),
    )
    bridge = context["ukf_frame_bridge"]
    if bridge["status"] != "pass":
        return _with_final_wall_time(
            {
                **base,
                "status": STATUS_BRIDGE_BLOCKED,
                "completed_batches": 0,
                "requested_batches": int(batches),
                "training_started": False,
                "optimizer_constructed": False,
                "ukf_frame_manifest": context["ukf_frame_manifest"],
                "initializer_manifest": dict(context["initializer"].manifest),
                "ukf_frame_bridge": bridge,
                "metric_batches": {},
                "gate_summary": {
                    "overall_status": "block",
                    "blockers": tuple(bridge.get("blockers", ())),
                    "bridge_status": bridge["status"],
                    "training_started": False,
                    "metric_evaluated": False,
                },
            }
        )

    seed_manifest = _seed_manifest(
        batch_count=int(batches),
        validation_present=True,
        replay_present=True,
        audit_present=bool(evidence_run),
    )
    if not seed_manifest["pairwise_disjoint_roles"]:
        return _with_final_wall_time(
            {
                **base,
                "status": STATUS_SEED_BLOCKED,
                "completed_batches": 0,
                "requested_batches": int(batches),
                "training_started": False,
                "optimizer_constructed": False,
                "seed_manifest": seed_manifest,
                "ukf_frame_manifest": context["ukf_frame_manifest"],
                "initializer_manifest": dict(context["initializer"].manifest),
                "ukf_frame_bridge": bridge,
                "metric_batches": {},
                "gate_summary": {
                    "overall_status": "block",
                    "blockers": ("seed_overlap",),
                    "bridge_status": bridge["status"],
                    "training_started": False,
                    "metric_evaluated": False,
                },
            }
        )

    trainer_config = context["trainer_config"]
    trainer_config = _with_learning_rate(trainer_config, float(learning_rate))
    initializer = context["initializer"]
    baseline = p77_metric.TrainableFunctionalTT(
        trainer_config,
        initial_cores=initializer.cores,
    )
    trainer = p77_metric.TrainableFunctionalTT(
        trainer_config,
        initial_cores=initializer.cores,
    )
    runtime_parameter_count = _runtime_parameter_count(trainer)
    parameter_manifest_with_runtime = {
        **dict(parameter_manifest),
        "trainable_variable_count_runtime": runtime_parameter_count,
        "runtime_count_matches_formula": runtime_parameter_count
        == int(parameter_manifest["P_theta"]),
    }

    try:
        validation_data, replay_data = tuple(context["audit_data_sequence"])
        metric_batches = {
            "validation_baseline": _metric_payload(
                trainer=baseline,
                data=validation_data,
                label="p77_validation_baseline",
                role="heldout_metric",
            ),
            "replay_baseline": _metric_payload(
                trainer=baseline,
                data=replay_data,
                label="p77_replay_baseline",
                role="audit_metric",
            ),
        }
    except (tf.errors.InvalidArgumentError, ValueError, RuntimeError) as exc:
        return _metric_blocked_payload(
            base=base,
            context=context,
            seed_manifest=seed_manifest,
            blocker=f"baseline_metric_exception:{exc}",
        )

    optimizer = p77_metric.make_adam_optimizer(trainer_config)
    completed_batches = 0
    final_terms = None
    stop_reason = "max_batches_completed"
    trace = []
    for step, train_data in enumerate(context["train_data_sequence"]):
        elapsed = time.monotonic() - RUN_START
        if elapsed > float(max_seconds):
            stop_reason = "wall_clock_cap_reached_before_next_batch"
            break
        batch = phase6._target_batch_from_data(train_data, label=f"p77_train_batch_{step}")
        try:
            terms = trainer.train_step(batch, optimizer)
        except (tf.errors.InvalidArgumentError, ValueError) as exc:
            return _training_blocked_payload(
                base=base,
                context=context,
                seed_manifest=seed_manifest,
                completed_batches=completed_batches,
                requested_batches=int(batches),
                stop_reason="train_step_exception_veto",
                blocker=f"train_step_exception:{exc}",
                trace=trace,
            )
        if phase6._terms_have_nonfinite_veto(terms, trainer, batch):
            return _training_blocked_payload(
                base=base,
                context=context,
                seed_manifest=seed_manifest,
                completed_batches=completed_batches + 1,
                requested_batches=int(batches),
                stop_reason="nonfinite_training_quantity_veto",
                blocker="nonfinite_training_quantity",
                trace=trace,
                final_terms=terms,
            )
        final_terms = terms
        completed_batches += 1
        if step in {0, int(batches) - 1} or (step + 1) % 10 == 0:
            trace.append(
                {
                    "step": step + 1,
                    "terms": p77_metric.terms_payload(terms),
                    "elapsed_seconds": round(time.monotonic() - RUN_START, 3),
                }
            )

    if final_terms is None:
        return _training_blocked_payload(
            base=base,
            context=context,
            seed_manifest=seed_manifest,
            completed_batches=0,
            requested_batches=int(batches),
            stop_reason="no_training_step_completed",
            blocker="no_training_step_completed",
            trace=trace,
        )

    try:
        metric_batches.update(
            {
                "validation_trained": _metric_payload(
                    trainer=trainer,
                    data=validation_data,
                    label="p77_validation_trained",
                    role="heldout_metric",
                ),
                "replay_trained": _metric_payload(
                    trainer=trainer,
                    data=replay_data,
                    label="p77_replay_trained",
                    role="audit_metric",
                ),
            }
        )
    except (tf.errors.InvalidArgumentError, ValueError, RuntimeError) as exc:
        return _metric_blocked_payload(
            base=base,
            context=context,
            seed_manifest=seed_manifest,
            blocker=f"trained_metric_exception:{exc}",
        )

    fit_quality_claim_permitted = bool(
        evidence_run and budget_manifest["hard_budget_gate_passed"]
    )
    validation_summary = _validation_summary(
        metric_batches,
        fit_quality_claim_permitted=fit_quality_claim_permitted,
    )
    metric_vetoes = _metric_vetoes(metric_batches)
    blockers = []
    if completed_batches <= 0:
        blockers.append("no_completed_batches")
    if bool(evidence_run) and int(completed_batches) != int(batches):
        blockers.append("incomplete_batch_count")
    blockers.extend(metric_vetoes)
    if bool(evidence_run) and completed_batches * int(batch_size) < int(
        budget_manifest["minimum_training_samples"]
    ):
        blockers.append("completed_training_samples_below_20P")
    if fit_quality_claim_permitted and (
        validation_summary["validation_improved_for_selection"] is not True
    ):
        blockers.append("validation_not_improved_against_untrained_ukf_baseline")

    return _with_final_wall_time(
        {
            **base,
            "status": STATUS_COMPLETED,
            "completed_batches": int(completed_batches),
            "requested_batches": int(batches),
            "stop_reason": stop_reason,
            "training_started": True,
            "optimizer_constructed": True,
            "parameter_manifest": parameter_manifest_with_runtime,
            "seed_manifest": seed_manifest,
            "training_seed_policy": context["training_seed_policy"],
            "fresh_training_batches": True,
            "audit_data_used_for_tuning": False,
            "audit_used_for_selection": False,
            "audit_evaluated": False,
            "source_route_prefit_used": False,
            "default_behavior_changed": False,
            "ukf_frame_manifest": context["ukf_frame_manifest"],
            "initializer_manifest": dict(initializer.manifest),
            "ukf_frame_bridge": bridge,
            "training_clip_fraction_max": context["training_clip_fraction_max"],
            "audit_clip_fraction_max": context["audit_clip_fraction_max"],
            "step_trace": trace,
            "final_terms": p77_metric.terms_payload(final_terms),
            "metric_batches": metric_batches,
            "validation_summary": validation_summary,
            "gate_summary": {
                "overall_status": "pass" if not blockers else "block",
                "blockers": tuple(blockers),
                "bridge_status": bridge["status"],
                "hard_budget_gate_passed": bool(budget_manifest["hard_budget_gate_passed"]),
                "evidence_run": bool(evidence_run),
                "requested_batches": int(batches),
                "completed_batches": int(completed_batches),
                "all_requested_batches_completed": int(completed_batches)
                == int(batches),
                "completed_training_samples": int(completed_batches * int(batch_size)),
                "validation_improvement_observed_explanatory_only": validation_summary[
                    "validation_improvement_observed_explanatory_only"
                ],
                "fit_quality_claim_permitted": bool(fit_quality_claim_permitted),
                "validation_improved_for_selection": validation_summary[
                    "validation_improved_for_selection"
                ],
                "audit_final_only": True,
                "not lower-gate repair": True,
                "not HMC readiness": True,
                "not default policy": True,
            },
        }
    )


def _validate_static_args(
    *,
    degree: int,
    rank: int,
    batch_size: int,
    batches: int,
    learning_rate: float,
    max_seconds: float,
) -> None:
    if int(degree) != 2:
        raise ValueError("P77 reviewed surface requires degree == 2")
    if int(rank) != 4:
        raise ValueError("P77 reviewed surface requires rank == 4")
    if int(batch_size) < 2:
        raise ValueError("batch_size must be at least 2")
    if int(batches) < 1:
        raise ValueError("batches must be positive")
    if float(learning_rate) <= 0.0:
        raise ValueError("learning_rate must be positive")
    if float(max_seconds) <= 0.0:
        raise ValueError("max_seconds must be positive")


def _target_context(
    *,
    degree: int,
    rank: int,
    batch_size: int,
    batches: int,
    seed: int,
    learning_rate: float,
) -> Mapping[str, Any]:
    del learning_rate
    return phase6._target_context(
        degree=int(degree),
        rank=int(rank),
        batch_size=int(batch_size),
        batches=int(batches),
        seed=int(seed),
    )


def _with_learning_rate(config, learning_rate: float):
    return p77_metric.P75TrainableTTConfig(
        product_basis=config.product_basis,
        ranks=config.ranks,
        tau=config.tau,
        normalizer_floor=config.normalizer_floor,
        denominator_floor=config.denominator_floor,
        l2_weight=config.l2_weight,
        logz_anchor_weight=config.logz_anchor_weight,
        logz_reference=config.logz_reference,
        learning_rate=float(learning_rate),
        gradient_clip_norm=config.gradient_clip_norm,
        seed=config.seed,
        metadata=dict(config.metadata),
    )


def _parameter_manifest(*, dimension: int, degree: int, rank: int) -> Mapping[str, Any]:
    ranks = phase6._rank_tuple(int(dimension), int(rank))
    basis_counts = tuple([int(degree) + 1] * int(dimension))
    terms = tuple(
        int(ranks[axis] * basis_counts[axis] * ranks[axis + 1])
        for axis in range(int(dimension))
    )
    total = int(sum(terms))
    return {
        "P_theta": total,
        "parameter_count": total,
        "parameter_count_formula": "sum_k r_{k-1} b_k r_k",
        "dimension": int(dimension),
        "degree": int(degree),
        "rank": int(rank),
        "rank_tuple": ranks,
        "basis_counts": basis_counts,
        "trainable_mask": "all_tt_core_entries",
        "trainable_variable_count_runtime": None,
        "recompute_if_rank_degree_dimension_basis_or_trainable_mask_changes": True,
        "term_counts": terms,
    }


def _runtime_parameter_count(trainer: p77_metric.TrainableFunctionalTT) -> int:
    return int(
        sum(
            tf.size(tf.convert_to_tensor(variable), out_type=tf.int64).numpy()
            for variable in trainer.variables
        )
    )


def _budget_manifest(
    *,
    parameter_manifest: Mapping[str, Any],
    batch_size: int,
    batches: int,
    evidence_run: bool,
) -> Mapping[str, Any]:
    p_theta = int(parameter_manifest["P_theta"])
    n_train = int(batch_size) * int(batches)
    minimum = int(P77_MIN_TRAINING_SAMPLES_PER_PARAMETER * p_theta)
    min_batches = int(math.ceil(minimum / int(batch_size)))
    return {
        "P_theta": p_theta,
        "samples_per_parameter_rule": P77_MIN_TRAINING_SAMPLES_PER_PARAMETER,
        "minimum_training_samples": minimum,
        "batch_size": int(batch_size),
        "batches": int(batches),
        "N_train": n_train,
        "N_train_over_P_theta": float(n_train / p_theta),
        "minimum_batches_for_batch_size": min_batches,
        "preferred_first_proper_budget": {
            "batch_size": P77_PREFERRED_BATCH_SIZE,
            "batches": P77_PREFERRED_BATCHES,
            "N_train": P77_PREFERRED_BATCH_SIZE * P77_PREFERRED_BATCHES,
        },
        "hard_budget_gate_passed": bool(n_train >= minimum),
        "evidence_run": bool(evidence_run),
        "non_evidence_mechanics_smoke": not bool(evidence_run),
    }


def _seed_manifest(
    *,
    batch_count: int,
    validation_present: bool,
    replay_present: bool,
    audit_present: bool,
) -> Mapping[str, Any]:
    manifest = phase10._seed_manifest(bridge_training_present=batch_count > 0)
    role_seed_pairs = {
        key: dict(value) for key, value in manifest["role_seed_pairs"].items()
    }
    if batch_count > 0:
        role_seed_pairs["training_range"] = {
            "prior_seed_start": phase6.TARGET_TRAIN_PRIOR_SEED_BASE,
            "prior_seed_stop_inclusive": phase6.TARGET_TRAIN_PRIOR_SEED_BASE
            + int(batch_count)
            - 1,
            "process_noise_seed_start": phase6.TARGET_TRAIN_PROCESS_SEED_BASE,
            "process_noise_seed_stop_inclusive": phase6.TARGET_TRAIN_PROCESS_SEED_BASE
            + int(batch_count)
            - 1,
        }
    flat: dict[int, list[str]] = {}
    for role, values in role_seed_pairs.items():
        for name, value in values.items():
            if name.endswith("_start") or name.endswith("_stop_inclusive"):
                continue
            flat.setdefault(int(value), []).append(f"{role}.{name}")
    overlaps = {
        str(seed): labels for seed, labels in flat.items() if len(labels) > 1
    }
    return {
        "role_seed_pairs": role_seed_pairs,
        "validation_present": bool(validation_present),
        "replay_present": bool(replay_present),
        "audit_present": bool(audit_present),
        "pairwise_disjoint_roles": not overlaps and manifest["pairwise_disjoint_roles"],
        "overlapping_seed_values": overlaps,
        "audit_final_only": True,
        "validation_only_selection": True,
        "stop_on_overlap": True,
    }


def _metric_payload(
    *,
    trainer: p77_metric.TrainableFunctionalTT,
    data: Any,
    label: str,
    role: str,
) -> Mapping[str, Any]:
    payload = dict(
        phase10._metric_payload(
            trainer=trainer,
            data=data,
            label=label,
            role=role,
        )
    )
    payload["explanatory_only"] = role != "heldout_metric"
    payload["corrected_validation_CE_primary"] = role == "heldout_metric"
    return payload


def _metric_vetoes(metric_batches: Mapping[str, Mapping[str, Any]]) -> list[str]:
    blockers: list[str] = []
    for label, payload in metric_batches.items():
        if not payload.get("all_primary_values_finite", False):
            blockers.append(f"{label}_nonfinite_metric_quantity")
        if payload.get("heldout_cross_entropy_reconstruction_abs_error", math.inf) > 1e-10:
            blockers.append(f"{label}_ce_reconstruction_mismatch")
        if abs(float(payload.get("corrected_alpha_sum", math.inf)) - 1.0) > 1e-10:
            blockers.append(f"{label}_target_only_alpha_mass_not_one")
    return blockers


def _validation_summary(
    metric_batches: Mapping[str, Mapping[str, Any]],
    *,
    fit_quality_claim_permitted: bool,
) -> Mapping[str, Any]:
    baseline = float(metric_batches["validation_baseline"]["heldout_cross_entropy"])
    trained = float(metric_batches["validation_trained"]["heldout_cross_entropy"])
    absolute = trained - baseline
    denominator = max(abs(baseline), 1e-300)
    observed_improvement = bool(trained < baseline)
    return {
        "untrained_ukf_baseline_corrected_validation_CE": baseline,
        "trained_corrected_validation_CE": trained,
        "absolute_CE_change_trained_minus_baseline": absolute,
        "relative_CE_change": absolute / denominator,
        "validation_improvement_observed_explanatory_only": (
            observed_improvement if not fit_quality_claim_permitted else False
        ),
        "fit_quality_claim_permitted": bool(fit_quality_claim_permitted),
        "validation_improved_for_selection": (
            observed_improvement if fit_quality_claim_permitted else None
        ),
        "non_evidence_smoke_no_fit_quality_claim": not bool(
            fit_quality_claim_permitted
        ),
        "selection_protocol": "lowest_corrected_validation_CE_after_vetoes",
        "audit_used_for_selection": False,
    }


def _metric_blocked_payload(
    *,
    base: Mapping[str, Any],
    context: Mapping[str, Any],
    seed_manifest: Mapping[str, Any],
    blocker: str,
) -> Mapping[str, Any]:
    return _with_final_wall_time(
        {
            **dict(base),
            "status": STATUS_METRIC_BLOCKED,
            "completed_batches": 0,
            "requested_batches": int(base["requested_batches"]),
            "training_started": False,
            "optimizer_constructed": False,
            "seed_manifest": seed_manifest,
            "ukf_frame_manifest": context["ukf_frame_manifest"],
            "initializer_manifest": dict(context["initializer"].manifest),
            "ukf_frame_bridge": context["ukf_frame_bridge"],
            "metric_batches": {},
            "gate_summary": {
                "overall_status": "block",
                "blockers": (str(blocker),),
                "metric_evaluated": False,
            },
        }
    )


def _training_blocked_payload(
    *,
    base: Mapping[str, Any],
    context: Mapping[str, Any],
    seed_manifest: Mapping[str, Any],
    completed_batches: int,
    requested_batches: int,
    stop_reason: str,
    blocker: str,
    trace: Sequence[Mapping[str, Any]],
    final_terms=None,
) -> Mapping[str, Any]:
    blockers = [str(blocker)]
    if bool(base.get("evidence_run", False)) and int(completed_batches) != int(
        requested_batches
    ):
        blockers.append("incomplete_batch_count")
    if bool(base.get("evidence_run", False)) and int(
        completed_batches * int(base.get("batch_size", 0))
    ) < int(dict(base.get("budget_manifest", {})).get("minimum_training_samples", 0)):
        blockers.append("completed_training_samples_below_20P")
    payload = {
        **dict(base),
        "status": STATUS_TRAINING_BLOCKED,
        "completed_batches": int(completed_batches),
        "requested_batches": int(requested_batches),
        "stop_reason": str(stop_reason),
        "training_started": int(completed_batches) > 0,
        "optimizer_constructed": True,
        "seed_manifest": seed_manifest,
        "training_seed_policy": context["training_seed_policy"],
        "ukf_frame_manifest": context["ukf_frame_manifest"],
        "initializer_manifest": dict(context["initializer"].manifest),
        "ukf_frame_bridge": context["ukf_frame_bridge"],
        "step_trace": tuple(trace),
        "metric_batches": {},
        "gate_summary": {
            "overall_status": "block",
            "blockers": tuple(dict.fromkeys(blockers)),
            "evidence_run": bool(base.get("evidence_run", False)),
            "hard_budget_gate_passed": bool(
                dict(base.get("budget_manifest", {})).get(
                    "hard_budget_gate_passed", False
                )
            ),
            "completed_batches": int(completed_batches),
            "requested_batches": int(requested_batches),
            "all_requested_batches_completed": int(completed_batches)
            == int(requested_batches),
            "completed_training_samples": int(
                completed_batches * int(base.get("batch_size", 0))
            ),
            "stop_reason": str(stop_reason),
            "not lower-gate repair": True,
            "not HMC readiness": True,
        },
    }
    if final_terms is not None:
        payload["final_terms"] = p77_metric.terms_payload(final_terms)
    return _with_final_wall_time(payload)


def _base_payload(
    *,
    output: Path,
    run_manifest: Mapping[str, Any],
    degree: int,
    rank: int,
    batch_size: int,
    batches: int,
    learning_rate: float,
    max_seconds: float,
    seed: int,
    evidence_run: bool,
    parameter_manifest: Mapping[str, Any],
    budget_manifest: Mapping[str, Any],
) -> Mapping[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "metadata_date": "2026-06-19",
        "master_program": MASTER_PROGRAM,
        "subplan": PHASE3_SUBPLAN,
        "run_manifest": run_manifest,
        "diagnostic_scope": "p77_budget_gated_corrected_metric_training_surface",
        "degree": int(degree),
        "rank": int(rank),
        "batch_size": int(batch_size),
        "requested_batches": int(batches),
        "learning_rate": float(learning_rate),
        "learning_rate_candidates": P77_LEARNING_RATES,
        "max_seconds": float(max_seconds),
        "seed": int(seed),
        "evidence_run": bool(evidence_run),
        "parameter_manifest": dict(parameter_manifest),
        "budget_manifest": dict(budget_manifest),
        "validation_stopping_selection_protocol": {
            "selection_metric": "corrected_validation_CE",
            "selection_rule": "lowest_corrected_validation_CE_after_vetoes",
            "audit_exclusion": True,
            "replay_role": "veto_for_nonfinite_reconstruction_alpha_role_provenance_else_explanatory_until_phase5",
        },
        "failed_route_fence": dict(FAILED_ROUTE_FENCE),
        "source_route_prefit_used": False,
        "default_behavior_changed": False,
        "cpu_only": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "nonclaims": NONCLAIMS,
        "output": str(output),
    }


def _initial_run_manifest(*, output: Path) -> Mapping[str, Any]:
    env_keys = ("CUDA_VISIBLE_DEVICES", "MPLCONFIGDIR", "PWD")
    environment = {key: os.environ.get(key) for key in env_keys}
    python_argv = [sys.executable, *sys.argv]
    env_prefix = [
        f"{key}={value}"
        for key in ("CUDA_VISIBLE_DEVICES", "MPLCONFIGDIR")
        if (value := os.environ.get(key)) is not None
    ]
    replay_parts = [*env_prefix, *python_argv]
    return {
        "command": " ".join(shlex.quote(part) for part in replay_parts),
        "python_executable": sys.executable,
        "argv": list(sys.argv),
        "python_argv": python_argv,
        "environment": environment,
        "cpu_only": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "tensorflow_version": tf.__version__,
        "script": str(SCRIPT_PATH.relative_to(REPO_ROOT)),
        "output": str(output),
        "elapsed_seconds": round(time.monotonic() - RUN_START, 3),
        "git": _git_state_summary(),
    }


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


def _with_final_wall_time(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    updated = dict(payload)
    manifest = dict(updated.get("run_manifest", {}))
    manifest["elapsed_seconds"] = round(time.monotonic() - RUN_START, 3)
    updated["run_manifest"] = manifest
    updated["wall_time_seconds"] = manifest["elapsed_seconds"]
    return updated


def _write_payload(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    sys.exit(main())
