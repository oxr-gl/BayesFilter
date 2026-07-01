"""Scoped HMC kernel tuning helpers.

This module intentionally implements only the early phases of the
BayesFilter-owned HMC kernel tuning program.  Phase 2 builds a validated
initial mass artifact and derives a formula-based initial step size and
leapfrog count.  Phase 3 runs a short fixed-kernel bootstrap screen and bounded
epsilon repair from that geometry.  Phase 4 captures retained fixed-kernel
diagnostic draws and feeds them to the reviewed windowed-mass diagnostic.  Phase
5 tunes a fixed-mass step size.  Phase 6 screens frozen-step trajectory
lengths.  Phase 7 runs the internal tune/verify/repair loop.  Phase 8 exposes a
one-call public wrapper while keeping raw HMC tuning mechanics internal to
BayesFilter policy.
"""

from __future__ import annotations

import json
import os
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

import numpy as np

from bayesfilter.inference.hmc import (
    FullChainHMCConfig,
    FullChainHMCRunResult,
    PrecomputedMassArtifact,
    SequentialRHatHMCVerificationConfig,
    build_reusable_full_chain_tfp_hmc_runner,
    build_sequential_rhat_hmc_verifier,
    program_signature,
    run_full_chain_tfp_hmc,
    stable_adapter_signature,
)
from bayesfilter.inference.hmc_diagnostics import screen_hmc_diagnostics
from bayesfilter.inference.hmc_budget_ladder import (
    FixedMassHMCTuningBudgetCallbackResult,
    FixedMassHMCTuningBudgetLadderConfig,
    FixedMassHMCTuningBudgetLadderResult,
    _build_fixed_mass_hmc_adapter,
    run_fixed_mass_hmc_tuning_budget_ladder,
)
from bayesfilter.inference.hmc_tuning import (
    HMCTuningPolicy,
    WindowedMassAdaptationConfig,
    WindowedMassAdaptationResult,
    run_windowed_mass_adaptation_diagnostic,
)
from bayesfilter.inference.posterior_adapter import (
    ValueScoreCapability,
    value_score_capability,
)
from bayesfilter.runtime import stable_config_hash


GEOMETRY_INITIALIZATION_NONCLAIMS = (
    "geometry initialization only",
    "no HMC runtime claim",
    "no tuning success claim",
    "no posterior convergence claim",
    "no sampler superiority claim",
    "no default-readiness claim",
)

BOOTSTRAP_SCREEN_NONCLAIMS = (
    "bootstrap fixed-kernel HMC screen only",
    "acceptance is a bootstrap repair diagnostic only",
    "no mass adaptation validity claim",
    "no trajectory tuning claim",
    "no posterior convergence claim",
    "no sampler superiority claim",
    "no default-readiness claim",
    "no GPU or XLA readiness claim",
)

WINDOWED_MASS_STAGE_NONCLAIMS = (
    "windowed mass-stage diagnostic only",
    "retained fixed-kernel samples are adaptation inputs only",
    "real acceptance telemetry required for step handoff",
    "no fixed-mass step tuning claim",
    "no trajectory tuning claim",
    "no posterior convergence claim",
    "no sampler superiority claim",
    "no default-readiness claim",
    "no GPU or XLA readiness claim",
)

FIXED_MASS_STEP_STAGE_NONCLAIMS = (
    "fixed-mass step-stage diagnostic only",
    "phase 4 adapted mass is frozen during step tuning",
    "fresh fixed-kernel screen required for step handoff",
    "no trajectory tuning claim",
    "no posterior convergence claim",
    "no sampler superiority claim",
    "no default-readiness claim",
    "no GPU or XLA readiness claim",
)

FROZEN_STEP_TRAJECTORY_STAGE_NONCLAIMS = (
    "frozen-step trajectory-stage diagnostic only",
    "phase 4 adapted mass is frozen during trajectory tuning",
    "phase 5 selected step is frozen during trajectory tuning",
    "candidate leapfrog mechanics are diagnostic telemetry only",
    "not fresh final verification",
    "no posterior convergence claim",
    "no sampler superiority claim",
    "no default-readiness claim",
    "no GPU or XLA readiness claim",
)

TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS = (
    "BayesFilter HMC tune-verify-repair loop only",
    "fresh fixed-kernel verification is a kernel handoff screen only",
    "no posterior convergence claim",
    "no sampler superiority claim",
    "no default-readiness claim",
    "no external-client scientific claim",
    "no GPU or XLA readiness claim",
)

HMC_KERNEL_TUNING_PUBLIC_NONCLAIMS = (
    "BayesFilter one-call HMC kernel tuning only",
    "final frozen kernel is a handoff artifact only",
    "tuning screens do not establish posterior convergence",
    "no posterior convergence claim",
    "no sampler superiority claim",
    "no default-readiness claim",
    "no external-client scientific claim",
    "no GPU readiness claim",
    "XLA execution, when requested, is runtime selection only",
)

RETAINED_FROZEN_KERNEL_REPLAY_NONCLAIMS = (
    "BayesFilter retained frozen-kernel adapter reconstruction only",
    "replays a previously verified adapter stack without running HMC",
    "no posterior convergence claim",
    "no sampler superiority claim",
    "no default-readiness claim",
    "no external-client scientific claim",
    "no GPU or XLA readiness claim",
)

_GEOMETRY_MIN_LEAPFROG = 3
_GEOMETRY_MAX_LEAPFROG = 25
_WINDOWED_STAGE_API_DISCARD_STEPS = 1
_FIXED_MASS_STAGE_TEST_BUDGET_SCHEDULE = (3, 6, 12)
_FIXED_MASS_STAGE_TUNE_NUM_RESULTS = 4
_FIXED_MASS_STAGE_SCREEN_NUM_RESULTS = 4
_FIXED_MASS_STAGE_SCREEN_BURNIN_STEPS = 1
_FROZEN_STEP_TRAJECTORY_CANDIDATE_OFFSETS = (-2, -1, 0, 1, 2)
_FROZEN_STEP_TRAJECTORY_CENTER_SLACK = 10
_FROZEN_STEP_TRAJECTORY_REPAIR_NEIGHBORHOOD_OFFSETS = (-4, -3, -2, -1, 0, 1, 2, 3, 4)
_FROZEN_STEP_TRAJECTORY_SOFT_DEADLINE_RESERVE_S = 60.0
_FROZEN_STEP_TRAJECTORY_SOFT_DEADLINE_SAFETY_MULTIPLIER = 1.25
_FROZEN_STEP_TRAJECTORY_SCREEN_NUM_RESULTS = 4
_FROZEN_STEP_TRAJECTORY_SCREEN_BURNIN_STEPS = 1
_SERIOUS_TUNING_MIN_RUN_BUDGET = 1000
_SERIOUS_TUNING_DIMENSION_FACTOR = 20
_SERIOUS_TUNING_MAX_INITIAL_BUDGET = 5000
_SERIOUS_TUNING_MAX_TUNE_BUDGET = 10000
_PUBLIC_TUNING_PROGRESS_FILENAME = "hmc_kernel_tuning_progress.json"
_PHASE7_VERIFICATION_ACCEPTANCE_BUDGET_BLOCKED = (
    "verification_acceptance_budget_blocked"
)
_PHASE6_TRAJECTORY_ACCEPTANCE_REPAIR_TRIGGER = (
    "phase6_trajectory_acceptance_outside_pass_band"
)
_PHASE7_VERIFICATION_ACCEPTANCE_REPAIR_TRIGGER = (
    "verification_acceptance_outside_pass_band"
)
_PHASE7_VERIFICATION_ACCEPTANCE_RETRY_PRE_PHASE6_MIN_RESERVES = 1.0

RunFullChainFn = Callable[[Any, Any, FullChainHMCConfig], FullChainHMCRunResult]
FixedMassScreenCallback = Callable[
    [Mapping[str, Any], Any, Mapping[str, Any]],
    Any,
]
TrajectoryScreenCallback = Callable[[Mapping[str, Any], Any, Mapping[str, Any]], Any]
VerificationCallback = Callable[[Mapping[str, Any], Any, Mapping[str, Any]], Any]
LoopProgressCallback = Callable[[str, Mapping[str, Any]], None]


def _bootstrap_selected_kernel_payload(
    *,
    config: "HMCBootstrapScreenConfig",
    selected: "HMCBootstrapRepairRound",
    adapter_signature: str,
    hmc_adapter_signature: str,
    mass_artifact_signature: str,
    geometry_artifact_hash: str,
    nonclaims: tuple[str, ...],
) -> Mapping[str, Any]:
    return {
        "runtime": "bayesfilter.inference.run_hmc_bootstrap_screen",
        "sample_space": "latent_fixed_mass",
        "step_size": selected.step_size,
        "num_leapfrog_steps": selected.num_leapfrog_steps,
        "target_trajectory_length": selected.target_trajectory_length,
        "target_accept_prob": config.target_accept_prob,
        "acceptance_band": config.acceptance_band,
        "repair_band": config.repair_band,
        "adapter_signature": adapter_signature,
        "hmc_adapter_signature": hmc_adapter_signature,
        "mass_artifact_signature": mass_artifact_signature,
        "geometry_artifact_hash": geometry_artifact_hash,
        "seed": selected.seed,
        "screen_config_payload": selected.screen_config_payload,
        "nonclaims": nonclaims,
    }


@dataclass(frozen=True)
class HMCGeometryInitializationConfig:
    """Configuration for geometry-derived initial HMC kernel parameters.

    The config deliberately does not ask the caller for a step size, leapfrog
    count, trajectory grid, mass-window schedule, or tuning budget schedule.
    Those belong to later internal BayesFilter tuning phases.
    """

    geometry_scaling_c: float = 0.5
    stability_guard: float = 0.8
    covariance_jitter: float = 1.0e-9
    eigenvalue_floor: float | None = 1.0e-9
    max_condition_number: float | None = None
    allow_geometry_fallback: bool = False
    seed: tuple[int, int] = (20260621, 2)
    source: str = "bayesfilter.inference.hmc_kernel_tuning"

    def __post_init__(self) -> None:
        scaling = float(self.geometry_scaling_c)
        guard = float(self.stability_guard)
        if not np.isfinite(scaling) or scaling <= 0.0:
            raise ValueError("geometry_scaling_c must be positive and finite")
        if not np.isfinite(guard) or guard <= 0.0:
            raise ValueError("stability_guard must be positive and finite")
        jitter = float(self.covariance_jitter)
        if not np.isfinite(jitter) or jitter < 0.0:
            raise ValueError("covariance_jitter must be finite and non-negative")
        floor = (
            None
            if self.eigenvalue_floor is None
            else float(self.eigenvalue_floor)
        )
        if floor is not None and (not np.isfinite(floor) or floor < 0.0):
            raise ValueError("eigenvalue_floor must be finite and non-negative")
        condition = (
            None
            if self.max_condition_number is None
            else float(self.max_condition_number)
        )
        if condition is not None and (
            not np.isfinite(condition) or condition <= 1.0
        ):
            raise ValueError("max_condition_number must be finite and greater than 1")
        seed = tuple(int(item) for item in self.seed)
        if len(seed) != 2:
            raise ValueError("seed must contain exactly two integers")
        source = str(self.source)
        if not source:
            raise ValueError("source must be non-empty")
        object.__setattr__(self, "geometry_scaling_c", scaling)
        object.__setattr__(self, "stability_guard", guard)
        object.__setattr__(self, "covariance_jitter", jitter)
        object.__setattr__(self, "eigenvalue_floor", floor)
        object.__setattr__(self, "max_condition_number", condition)
        object.__setattr__(self, "allow_geometry_fallback", bool(self.allow_geometry_fallback))
        object.__setattr__(self, "seed", seed)
        object.__setattr__(self, "source", source)

    def payload(self) -> Mapping[str, Any]:
        return {
            "geometry_scaling_c": self.geometry_scaling_c,
            "stability_guard": self.stability_guard,
            "covariance_jitter": self.covariance_jitter,
            "eigenvalue_floor": self.eigenvalue_floor,
            "max_condition_number": self.max_condition_number,
            "allow_geometry_fallback": self.allow_geometry_fallback,
            "seed": self.seed,
            "source": self.source,
        }


@dataclass(frozen=True)
class HMCGeometryInitializationResult:
    """Geometry-derived starting kernel, not HMC tuning evidence."""

    config: HMCGeometryInitializationConfig
    adapter_signature: str
    target_dimension: int
    mass_artifact: PrecomputedMassArtifact
    mass_artifact_signature: str
    initial_step_size: float
    initial_num_leapfrog_steps: int
    unclamped_num_leapfrog_steps: int
    target_trajectory_length: float
    hint_report: Mapping[str, Any]
    curvature_report: Mapping[str, Any]
    formula_report: Mapping[str, Any]
    seed_report: Mapping[str, Any]
    nonclaims: tuple[str, ...] = GEOMETRY_INITIALIZATION_NONCLAIMS

    def __post_init__(self) -> None:
        signature = str(self.adapter_signature)
        if not signature:
            raise ValueError("adapter_signature must be non-empty")
        dimension = int(self.target_dimension)
        if dimension <= 0:
            raise ValueError("target_dimension must be positive")
        if self.mass_artifact.adapter_signature != signature:
            raise ValueError("mass artifact adapter_signature mismatch")
        if self.mass_artifact.dimension != dimension:
            raise ValueError("mass artifact dimension mismatch")
        step = float(self.initial_step_size)
        if not np.isfinite(step) or step <= 0.0:
            raise ValueError("initial_step_size must be positive and finite")
        leapfrogs = int(self.initial_num_leapfrog_steps)
        raw_leapfrogs = int(self.unclamped_num_leapfrog_steps)
        if leapfrogs <= 0 or raw_leapfrogs <= 0:
            raise ValueError("leapfrog counts must be positive")
        trajectory = float(self.target_trajectory_length)
        if not np.isfinite(trajectory) or trajectory <= 0.0:
            raise ValueError("target_trajectory_length must be positive and finite")
        mass_signature = str(self.mass_artifact_signature)
        if not mass_signature:
            raise ValueError("mass_artifact_signature must be non-empty")
        nonclaims = tuple(str(item) for item in self.nonclaims)
        if not nonclaims:
            raise ValueError("nonclaims must be non-empty")
        object.__setattr__(self, "adapter_signature", signature)
        object.__setattr__(self, "target_dimension", dimension)
        object.__setattr__(self, "mass_artifact_signature", mass_signature)
        object.__setattr__(self, "initial_step_size", step)
        object.__setattr__(self, "initial_num_leapfrog_steps", leapfrogs)
        object.__setattr__(self, "unclamped_num_leapfrog_steps", raw_leapfrogs)
        object.__setattr__(self, "target_trajectory_length", trajectory)
        object.__setattr__(self, "hint_report", dict(self.hint_report))
        object.__setattr__(self, "curvature_report", dict(self.curvature_report))
        object.__setattr__(self, "formula_report", dict(self.formula_report))
        object.__setattr__(self, "seed_report", dict(self.seed_report))
        object.__setattr__(self, "nonclaims", nonclaims)

    def payload(self, *, include_mass_arrays: bool = False) -> Mapping[str, Any]:
        return {
            "artifact_type": "bayesfilter_hmc_geometry_initialization_result",
            "schema_version": 1,
            "config": self.config.payload(),
            "adapter_signature": self.adapter_signature,
            "target_dimension": self.target_dimension,
            "mass_artifact_payload": self.mass_artifact.to_payload(
                include_arrays=include_mass_arrays
            ),
            "mass_artifact_signature": self.mass_artifact_signature,
            "initial_step_size": self.initial_step_size,
            "initial_num_leapfrog_steps": self.initial_num_leapfrog_steps,
            "unclamped_num_leapfrog_steps": self.unclamped_num_leapfrog_steps,
            "target_trajectory_length": self.target_trajectory_length,
            "hint_report": self.hint_report,
            "curvature_report": self.curvature_report,
            "formula_report": self.formula_report,
            "seed_report": self.seed_report,
            "reports_hmc_runtime_readiness": False,
            "reports_tuning_success": False,
            "reports_posterior_convergence": False,
            "reports_sampler_superiority": False,
            "nonclaims": self.nonclaims,
        }

    @property
    def artifact_hash(self) -> str:
        return stable_config_hash(self.payload(include_mass_arrays=True))


@dataclass(frozen=True)
class HMCBootstrapScreenConfig:
    """Policy-level config for the Phase 3 bootstrap screen.

    Model clients do not supply HMC mechanics here.  Step size and leapfrog
    count are derived internally from the Phase 2 geometry artifact and the
    bounded bootstrap repair rule.
    """

    target_accept_prob: float = 0.70
    acceptance_band: tuple[float, float] = (0.65, 0.75)
    repair_band: tuple[float, float] = (0.55, 0.85)
    max_repairs: int = 5
    screen_num_results: int = 16
    screen_num_burnin_steps: int = 4
    seed: tuple[int, int] = (20260621, 3)
    chain_execution_mode: str = "tf_function"
    use_xla: bool = False
    target_scope: str | None = None
    target_status_trace_policy: str = "none"
    source: str = "bayesfilter.inference.hmc_kernel_tuning.bootstrap_screen"

    def __post_init__(self) -> None:
        target = float(self.target_accept_prob)
        if not np.isfinite(target) or not 0.0 < target < 1.0:
            raise ValueError("target_accept_prob must be finite and in (0, 1)")
        object.__setattr__(self, "target_accept_prob", target)
        acceptance_band = _validate_band(self.acceptance_band, name="acceptance_band")
        repair_band = _validate_band(self.repair_band, name="repair_band")
        if repair_band[0] > acceptance_band[0] or repair_band[1] < acceptance_band[1]:
            raise ValueError("repair_band must contain acceptance_band")
        object.__setattr__(self, "acceptance_band", acceptance_band)
        object.__setattr__(self, "repair_band", repair_band)
        max_repairs = int(self.max_repairs)
        if max_repairs < 0:
            raise ValueError("max_repairs must be non-negative")
        object.__setattr__(self, "max_repairs", max_repairs)
        for name in ("screen_num_results", "screen_num_burnin_steps"):
            value = int(getattr(self, name))
            if value <= 0:
                raise ValueError(f"{name} must be positive")
            object.__setattr__(self, name, value)
        object.__setattr__(self, "seed", _validate_seed(self.seed))
        mode = str(self.chain_execution_mode)
        if mode not in {"tf_function", "eager"}:
            raise ValueError("chain_execution_mode must be 'tf_function' or 'eager'")
        if self.use_xla and mode != "tf_function":
            raise ValueError("XLA HMC requires chain_execution_mode='tf_function'")
        object.__setattr__(self, "chain_execution_mode", mode)
        object.__setattr__(self, "use_xla", bool(self.use_xla))
        if self.target_scope is not None:
            scope = str(self.target_scope)
            if not scope:
                raise ValueError("target_scope must be non-empty when provided")
            object.__setattr__(self, "target_scope", scope)
        target_status_policy = str(self.target_status_trace_policy)
        if target_status_policy not in {"none", "per_chain_step"}:
            raise ValueError(
                "target_status_trace_policy must be 'none' or 'per_chain_step'"
            )
        object.__setattr__(self, "target_status_trace_policy", target_status_policy)
        source = str(self.source)
        if not source:
            raise ValueError("source must be non-empty")
        object.__setattr__(self, "source", source)

    def payload(self) -> Mapping[str, Any]:
        return {
            "target_accept_prob": self.target_accept_prob,
            "acceptance_band": self.acceptance_band,
            "repair_band": self.repair_band,
            "max_repairs": self.max_repairs,
            "screen_num_results": self.screen_num_results,
            "screen_num_burnin_steps": self.screen_num_burnin_steps,
            "seed": self.seed,
            "chain_execution_mode": self.chain_execution_mode,
            "use_xla": self.use_xla,
            "target_scope": self.target_scope,
            "target_status_trace_policy": self.target_status_trace_policy,
            "source": self.source,
        }


@dataclass(frozen=True)
class HMCBootstrapRepairRound:
    """One Phase 3 fixed-kernel screen attempt and repair decision."""

    round_index: int
    seed: tuple[int, int]
    step_size: float
    num_leapfrog_steps: int
    unclamped_num_leapfrog_steps: int
    target_trajectory_length: float
    leapfrog_clamped: bool
    clamp_direction: str | None
    classification: str
    diagnostic_role: str
    screen_config_payload: Mapping[str, Any] | None
    diagnostics: Mapping[str, Any]
    repair_action: str | None = None
    hard_vetoes: tuple[str, ...] = ()
    repair_triggers: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "round_index", int(self.round_index))
        object.__setattr__(self, "seed", _validate_seed(self.seed))
        step = float(self.step_size)
        if not np.isfinite(step) or step <= 0.0:
            raise ValueError("step_size must be positive and finite")
        object.__setattr__(self, "step_size", step)
        leapfrogs = int(self.num_leapfrog_steps)
        raw_leapfrogs = int(self.unclamped_num_leapfrog_steps)
        if leapfrogs <= 0 or raw_leapfrogs <= 0:
            raise ValueError("leapfrog counts must be positive")
        object.__setattr__(self, "num_leapfrog_steps", leapfrogs)
        object.__setattr__(self, "unclamped_num_leapfrog_steps", raw_leapfrogs)
        trajectory = float(self.target_trajectory_length)
        if not np.isfinite(trajectory) or trajectory <= 0.0:
            raise ValueError("target_trajectory_length must be positive and finite")
        object.__setattr__(self, "target_trajectory_length", trajectory)
        object.__setattr__(self, "leapfrog_clamped", bool(self.leapfrog_clamped))
        clamp = None if self.clamp_direction is None else str(self.clamp_direction)
        if clamp not in {None, "min", "max"}:
            raise ValueError("clamp_direction must be None, 'min', or 'max'")
        object.__setattr__(self, "clamp_direction", clamp)
        object.__setattr__(self, "classification", str(self.classification))
        object.__setattr__(self, "diagnostic_role", str(self.diagnostic_role))
        payload = (
            None
            if self.screen_config_payload is None
            else dict(self.screen_config_payload)
        )
        object.__setattr__(self, "screen_config_payload", payload)
        object.__setattr__(self, "diagnostics", dict(self.diagnostics))
        action = None if self.repair_action is None else str(self.repair_action)
        object.__setattr__(self, "repair_action", action)
        object.__setattr__(self, "hard_vetoes", _string_tuple(self.hard_vetoes))
        object.__setattr__(self, "repair_triggers", _string_tuple(self.repair_triggers))

    @property
    def passed(self) -> bool:
        return self.classification == "passed"

    def payload(self) -> Mapping[str, Any]:
        return {
            "round_index": self.round_index,
            "seed": self.seed,
            "step_size": self.step_size,
            "num_leapfrog_steps": self.num_leapfrog_steps,
            "unclamped_num_leapfrog_steps": self.unclamped_num_leapfrog_steps,
            "target_trajectory_length": self.target_trajectory_length,
            "leapfrog_clamped": self.leapfrog_clamped,
            "clamp_direction": self.clamp_direction,
            "classification": self.classification,
            "diagnostic_role": self.diagnostic_role,
            "screen_config_payload": self.screen_config_payload,
            "diagnostics": self.diagnostics,
            "repair_action": self.repair_action,
            "hard_vetoes": self.hard_vetoes,
            "repair_triggers": self.repair_triggers,
        }


@dataclass(frozen=True)
class HMCBootstrapScreenResult:
    """Phase 3 bootstrap artifact; not final HMC tuning evidence."""

    config: HMCBootstrapScreenConfig
    geometry_artifact_hash: str
    adapter_signature: str
    hmc_adapter_signature: str
    mass_artifact_signature: str
    target_dimension: int
    rounds: tuple[HMCBootstrapRepairRound, ...]
    selected_round_index: int | None
    final_status: str
    seed_report: Mapping[str, Any]
    diagnostic_roles: Mapping[str, str]
    bootstrap_runner_route: Mapping[str, Any] | None = None
    nonclaims: tuple[str, ...] = BOOTSTRAP_SCREEN_NONCLAIMS

    def __post_init__(self) -> None:
        for name in (
            "geometry_artifact_hash",
            "adapter_signature",
            "hmc_adapter_signature",
            "mass_artifact_signature",
            "final_status",
        ):
            value = str(getattr(self, name))
            if not value:
                raise ValueError(f"{name} must be non-empty")
            object.__setattr__(self, name, value)
        dimension = int(self.target_dimension)
        if dimension <= 0:
            raise ValueError("target_dimension must be positive")
        object.__setattr__(self, "target_dimension", dimension)
        rounds = tuple(self.rounds)
        if not rounds:
            raise ValueError("bootstrap result requires at least one round")
        object.__setattr__(self, "rounds", rounds)
        selected = (
            None if self.selected_round_index is None else int(self.selected_round_index)
        )
        if selected is not None and selected not in range(len(rounds)):
            raise ValueError("selected_round_index must refer to a round")
        if selected is not None and not rounds[selected].passed:
            raise ValueError("selected round must have passed")
        object.__setattr__(self, "selected_round_index", selected)
        object.__setattr__(self, "seed_report", dict(self.seed_report))
        object.__setattr__(self, "diagnostic_roles", dict(self.diagnostic_roles))
        route = (
            {}
            if self.bootstrap_runner_route is None
            else dict(self.bootstrap_runner_route)
        )
        object.__setattr__(self, "bootstrap_runner_route", route)
        nonclaims = tuple(str(item) for item in self.nonclaims)
        if not nonclaims:
            raise ValueError("nonclaims must be non-empty")
        object.__setattr__(self, "nonclaims", nonclaims)

    @property
    def passed(self) -> bool:
        return self.selected_round_index is not None

    @property
    def selected_round(self) -> HMCBootstrapRepairRound | None:
        if self.selected_round_index is None:
            return None
        return self.rounds[self.selected_round_index]

    @property
    def selected_kernel_payload(self) -> Mapping[str, Any] | None:
        selected = self.selected_round
        if selected is None:
            return None
        return _bootstrap_selected_kernel_payload(
            config=self.config,
            selected=selected,
            adapter_signature=self.adapter_signature,
            hmc_adapter_signature=self.hmc_adapter_signature,
            mass_artifact_signature=self.mass_artifact_signature,
            geometry_artifact_hash=self.geometry_artifact_hash,
            nonclaims=self.nonclaims,
        )

    @property
    def selected_kernel_hash(self) -> str | None:
        payload = self.selected_kernel_payload
        return None if payload is None else stable_config_hash(payload)

    @property
    def artifact_hash(self) -> str:
        return stable_config_hash(self.payload())

    def payload(self) -> Mapping[str, Any]:
        selected_payload = self.selected_kernel_payload
        return {
            "schema": "bayesfilter.hmc_bootstrap_screen.v1",
            "config": self.config.payload(),
            "geometry_artifact_hash": self.geometry_artifact_hash,
            "adapter_signature": self.adapter_signature,
            "hmc_adapter_signature": self.hmc_adapter_signature,
            "mass_artifact_signature": self.mass_artifact_signature,
            "target_dimension": self.target_dimension,
            "rounds": tuple(round_result.payload() for round_result in self.rounds),
            "selected_round_index": self.selected_round_index,
            "selected_kernel_payload": selected_payload,
            "selected_kernel_hash": None
            if selected_payload is None
            else stable_config_hash(selected_payload),
            "final_status": self.final_status,
            "seed_report": self.seed_report,
            "diagnostic_roles": self.diagnostic_roles,
            "bootstrap_runner_route": self.bootstrap_runner_route,
            "passed": self.passed,
            "reports_mass_adaptation_validity": False,
            "reports_trajectory_tuning": False,
            "reports_posterior_convergence": False,
            "reports_sampler_superiority": False,
            "reports_gpu_or_xla_readiness": False,
            "nonclaims": self.nonclaims,
            "artifact_hash_components": {
                "hash_function": "bayesfilter.runtime.stable_config_hash",
                "json_normalization": "sort_keys_compact_json",
            },
        }


@dataclass(frozen=True)
class HMCWindowedMassStageConfig:
    """Policy-level config for the Phase 4 windowed mass stage.

    The caller does not supply warmup windows, draw counts, step size, leapfrog
    counts, grids, mass schedules, or budget schedules.  Phase 4 owns those
    mechanics internally and records the chosen draw-capture policy in the
    result artifact.
    """

    target_accept_prob: float = 0.70
    seed: tuple[int, int] = (20260621, 4)
    chain_execution_mode: str = "tf_function"
    use_xla: bool = False
    target_scope: str | None = None
    target_status_trace_policy: str = "none"
    source: str = "bayesfilter.inference.hmc_kernel_tuning.windowed_mass_stage"

    def __post_init__(self) -> None:
        target = float(self.target_accept_prob)
        if not np.isfinite(target) or not 0.0 < target < 1.0:
            raise ValueError("target_accept_prob must be finite and in (0, 1)")
        object.__setattr__(self, "target_accept_prob", target)
        object.__setattr__(self, "seed", _validate_seed(self.seed))
        mode = str(self.chain_execution_mode)
        if mode not in {"tf_function", "eager"}:
            raise ValueError("chain_execution_mode must be 'tf_function' or 'eager'")
        if self.use_xla and mode != "tf_function":
            raise ValueError("XLA HMC requires chain_execution_mode='tf_function'")
        object.__setattr__(self, "chain_execution_mode", mode)
        object.__setattr__(self, "use_xla", bool(self.use_xla))
        if self.target_scope is not None:
            scope = str(self.target_scope)
            if not scope:
                raise ValueError("target_scope must be non-empty when provided")
            object.__setattr__(self, "target_scope", scope)
        target_status_policy = str(self.target_status_trace_policy)
        if target_status_policy not in {"none", "per_chain_step"}:
            raise ValueError(
                "target_status_trace_policy must be 'none' or 'per_chain_step'"
            )
        object.__setattr__(self, "target_status_trace_policy", target_status_policy)
        source = str(self.source)
        if not source:
            raise ValueError("source must be non-empty")
        object.__setattr__(self, "source", source)

    def payload(self) -> Mapping[str, Any]:
        return {
            "target_accept_prob": self.target_accept_prob,
            "seed": self.seed,
            "chain_execution_mode": self.chain_execution_mode,
            "use_xla": self.use_xla,
            "target_scope": self.target_scope,
            "target_status_trace_policy": self.target_status_trace_policy,
            "source": self.source,
        }


@dataclass(frozen=True)
class HMCWindowedMassStageResult:
    """Phase 4 adapted-mass handoff; not posterior or final tuning evidence."""

    config: HMCWindowedMassStageConfig
    geometry_artifact_hash: str
    bootstrap_artifact_hash: str
    selected_bootstrap_kernel_hash: str
    adapter_signature: str
    hmc_adapter_signature: str
    initial_mass_artifact_signature: str
    target_dimension: int
    final_status: str
    diagnostic_role: str
    hard_vetoes: tuple[str, ...]
    diagnostics: Mapping[str, Any]
    draw_capture_policy: Mapping[str, Any]
    warmup_draw_provenance: Mapping[str, Any]
    acceptance_telemetry_provenance: Mapping[str, Any]
    diagnostic_run_config_payload: Mapping[str, Any] | None
    windowed_config_payload: Mapping[str, Any]
    windowed_mass_result: WindowedMassAdaptationResult | None
    seed_report: Mapping[str, Any]
    diagnostic_roles: Mapping[str, str]
    nonclaims: tuple[str, ...] = WINDOWED_MASS_STAGE_NONCLAIMS

    def __post_init__(self) -> None:
        for name in (
            "geometry_artifact_hash",
            "bootstrap_artifact_hash",
            "selected_bootstrap_kernel_hash",
            "adapter_signature",
            "hmc_adapter_signature",
            "initial_mass_artifact_signature",
            "final_status",
            "diagnostic_role",
        ):
            value = str(getattr(self, name))
            if not value:
                raise ValueError(f"{name} must be non-empty")
            object.__setattr__(self, name, value)
        dimension = int(self.target_dimension)
        if dimension <= 0:
            raise ValueError("target_dimension must be positive")
        object.__setattr__(self, "target_dimension", dimension)
        hard_vetoes = _string_tuple(self.hard_vetoes)
        object.__setattr__(self, "hard_vetoes", hard_vetoes)
        object.__setattr__(self, "diagnostics", dict(self.diagnostics))
        object.__setattr__(self, "draw_capture_policy", dict(self.draw_capture_policy))
        object.__setattr__(
            self,
            "warmup_draw_provenance",
            dict(self.warmup_draw_provenance),
        )
        object.__setattr__(
            self,
            "acceptance_telemetry_provenance",
            dict(self.acceptance_telemetry_provenance),
        )
        payload = (
            None
            if self.diagnostic_run_config_payload is None
            else dict(self.diagnostic_run_config_payload)
        )
        object.__setattr__(self, "diagnostic_run_config_payload", payload)
        object.__setattr__(self, "windowed_config_payload", dict(self.windowed_config_payload))
        object.__setattr__(self, "seed_report", dict(self.seed_report))
        object.__setattr__(self, "diagnostic_roles", dict(self.diagnostic_roles))
        nonclaims = tuple(str(item) for item in self.nonclaims)
        if not nonclaims:
            raise ValueError("nonclaims must be non-empty")
        object.__setattr__(self, "nonclaims", nonclaims)
        if self.final_status == "passed":
            if hard_vetoes:
                raise ValueError("passed windowed mass stage cannot have hard vetoes")
            if self.windowed_mass_result is None or not self.windowed_mass_result.passed:
                raise ValueError("passed windowed mass stage requires passed windowed result")

    @property
    def passed(self) -> bool:
        return self.final_status == "passed"

    @property
    def adapted_mass_artifact_payload(self) -> Mapping[str, Any] | None:
        if self.windowed_mass_result is None:
            return None
        return self.windowed_mass_result.final_mass_artifact_payload

    @property
    def adapted_mass_artifact_signature(self) -> str | None:
        if self.windowed_mass_result is None:
            return None
        return self.windowed_mass_result.final_mass_artifact_signature

    @property
    def candidate_step_size(self) -> float | None:
        if self.windowed_mass_result is None:
            return None
        return self.windowed_mass_result.final_step_size

    @property
    def artifact_hash(self) -> str:
        return stable_config_hash(self.payload())

    def payload(self) -> Mapping[str, Any]:
        return {
            "schema": "bayesfilter.hmc_windowed_mass_stage.v1",
            "config": self.config.payload(),
            "geometry_artifact_hash": self.geometry_artifact_hash,
            "bootstrap_artifact_hash": self.bootstrap_artifact_hash,
            "selected_bootstrap_kernel_hash": self.selected_bootstrap_kernel_hash,
            "adapter_signature": self.adapter_signature,
            "hmc_adapter_signature": self.hmc_adapter_signature,
            "initial_mass_artifact_signature": self.initial_mass_artifact_signature,
            "target_dimension": self.target_dimension,
            "final_status": self.final_status,
            "diagnostic_role": self.diagnostic_role,
            "hard_vetoes": self.hard_vetoes,
            "diagnostics": self.diagnostics,
            "draw_capture_policy": self.draw_capture_policy,
            "warmup_draw_provenance": self.warmup_draw_provenance,
            "acceptance_telemetry_provenance": self.acceptance_telemetry_provenance,
            "diagnostic_run_config_payload": self.diagnostic_run_config_payload,
            "windowed_config_payload": self.windowed_config_payload,
            "windowed_mass_result": None
            if self.windowed_mass_result is None
            else self.windowed_mass_result.payload(),
            "adapted_mass_artifact_payload": self.adapted_mass_artifact_payload,
            "adapted_mass_artifact_signature": self.adapted_mass_artifact_signature,
            "candidate_step_size": self.candidate_step_size,
            "seed_report": self.seed_report,
            "diagnostic_roles": self.diagnostic_roles,
            "passed": self.passed,
            "reports_fixed_mass_step_tuning": False,
            "reports_trajectory_tuning": False,
            "reports_posterior_convergence": False,
            "reports_sampler_superiority": False,
            "reports_gpu_or_xla_readiness": False,
            "nonclaims": self.nonclaims,
        }


@dataclass(frozen=True)
class HMCFixedMassStepStageConfig:
    """Policy-level config for Phase 5 fixed-mass step tuning.

    The caller does not supply the budget schedule, tune/screen draw counts,
    burn-in counts, step size, leapfrog count, trajectory grid, or candidate
    grid. Phase 5 owns those mechanics and records them in the result.
    """

    target_accept_prob: float = 0.70
    acceptance_band: tuple[float, float] = (0.65, 0.75)
    repair_band: tuple[float, float] = (0.55, 0.85)
    seed: tuple[int, int] = (20260621, 5)
    chain_execution_mode: str = "tf_function"
    use_xla: bool = False
    target_scope: str | None = None
    target_status_trace_policy: str = "none"
    source: str = "bayesfilter.inference.hmc_kernel_tuning.fixed_mass_step_stage"

    def __post_init__(self) -> None:
        target = float(self.target_accept_prob)
        if not np.isfinite(target) or not 0.0 < target < 1.0:
            raise ValueError("target_accept_prob must be finite and in (0, 1)")
        object.__setattr__(self, "target_accept_prob", target)
        object.__setattr__(
            self,
            "acceptance_band",
            _validate_band(self.acceptance_band, name="acceptance_band"),
        )
        repair_band = _validate_band(self.repair_band, name="repair_band")
        if repair_band[0] > self.acceptance_band[0] or repair_band[1] < self.acceptance_band[1]:
            raise ValueError("repair_band must contain acceptance_band")
        object.__setattr__(self, "repair_band", repair_band)
        object.__setattr__(self, "seed", _validate_seed(self.seed))
        mode = str(self.chain_execution_mode)
        if mode not in {"tf_function", "eager"}:
            raise ValueError("chain_execution_mode must be 'tf_function' or 'eager'")
        if self.use_xla and mode != "tf_function":
            raise ValueError("XLA HMC requires chain_execution_mode='tf_function'")
        object.__setattr__(self, "chain_execution_mode", mode)
        object.__setattr__(self, "use_xla", bool(self.use_xla))
        if self.target_scope is not None:
            scope = str(self.target_scope)
            if not scope:
                raise ValueError("target_scope must be non-empty when provided")
            object.__setattr__(self, "target_scope", scope)
        target_status_policy = str(self.target_status_trace_policy)
        if target_status_policy not in {"none", "per_chain_step"}:
            raise ValueError(
                "target_status_trace_policy must be 'none' or 'per_chain_step'"
            )
        object.__setattr__(self, "target_status_trace_policy", target_status_policy)
        source = str(self.source)
        if not source:
            raise ValueError("source must be non-empty")
        object.__setattr__(self, "source", source)

    def payload(self) -> Mapping[str, Any]:
        return {
            "target_accept_prob": self.target_accept_prob,
            "acceptance_band": self.acceptance_band,
            "repair_band": self.repair_band,
            "seed": self.seed,
            "chain_execution_mode": self.chain_execution_mode,
            "use_xla": self.use_xla,
            "target_scope": self.target_scope,
            "target_status_trace_policy": self.target_status_trace_policy,
            "source": self.source,
        }


@dataclass(frozen=True)
class HMCFixedMassStepStageResult:
    """Phase 5 fixed-mass step handoff; not trajectory or posterior evidence."""

    config: HMCFixedMassStepStageConfig
    windowed_stage_artifact_hash: str
    selected_bootstrap_kernel_hash: str
    adapter_signature: str
    phase4_hmc_adapter_signature: str
    ladder_adapter_signature: str
    ladder_hmc_adapter_signature: str
    adapted_mass_artifact_payload: Mapping[str, Any]
    adapted_mass_artifact_signature: str
    initial_step_size: float
    fixed_num_leapfrog_steps: int
    target_dimension: int
    final_status: str
    diagnostic_role: str
    hard_vetoes: tuple[str, ...]
    repair_triggers: tuple[str, ...]
    diagnostics: Mapping[str, Any]
    budget_ladder_config_payload: Mapping[str, Any] | None
    budget_ladder_result: FixedMassHMCTuningBudgetLadderResult | None
    selected_step_payload: Mapping[str, Any] | None
    selected_step_hash: str | None
    repair_step_payload: Mapping[str, Any] | None
    repair_step_hash: str | None
    frozen_mass_invariant: Mapping[str, Any]
    seed_report: Mapping[str, Any]
    diagnostic_roles: Mapping[str, str]
    nonclaims: tuple[str, ...] = FIXED_MASS_STEP_STAGE_NONCLAIMS

    def __post_init__(self) -> None:
        for name in (
            "windowed_stage_artifact_hash",
            "selected_bootstrap_kernel_hash",
            "adapter_signature",
            "phase4_hmc_adapter_signature",
            "ladder_adapter_signature",
            "ladder_hmc_adapter_signature",
            "adapted_mass_artifact_signature",
            "final_status",
            "diagnostic_role",
        ):
            value = str(getattr(self, name))
            if not value:
                raise ValueError(f"{name} must be non-empty")
            object.__setattr__(self, name, value)
        initial_step = float(self.initial_step_size)
        if not np.isfinite(initial_step) or initial_step <= 0.0:
            raise ValueError("initial_step_size must be positive and finite")
        object.__setattr__(self, "initial_step_size", initial_step)
        leapfrog = int(self.fixed_num_leapfrog_steps)
        if leapfrog <= 0:
            raise ValueError("fixed_num_leapfrog_steps must be positive")
        object.__setattr__(self, "fixed_num_leapfrog_steps", leapfrog)
        dimension = int(self.target_dimension)
        if dimension <= 0:
            raise ValueError("target_dimension must be positive")
        object.__setattr__(self, "target_dimension", dimension)
        object.__setattr__(self, "hard_vetoes", _string_tuple(self.hard_vetoes))
        object.__setattr__(self, "repair_triggers", _string_tuple(self.repair_triggers))
        object.__setattr__(
            self,
            "adapted_mass_artifact_payload",
            dict(self.adapted_mass_artifact_payload),
        )
        object.__setattr__(self, "diagnostics", dict(self.diagnostics))
        config_payload = (
            None
            if self.budget_ladder_config_payload is None
            else dict(self.budget_ladder_config_payload)
        )
        object.__setattr__(self, "budget_ladder_config_payload", config_payload)
        selected_payload = (
            None if self.selected_step_payload is None else dict(self.selected_step_payload)
        )
        object.__setattr__(self, "selected_step_payload", selected_payload)
        selected_hash = None if self.selected_step_hash is None else str(self.selected_step_hash)
        object.__setattr__(self, "selected_step_hash", selected_hash)
        repair_payload = (
            None if self.repair_step_payload is None else dict(self.repair_step_payload)
        )
        object.__setattr__(self, "repair_step_payload", repair_payload)
        repair_hash = None if self.repair_step_hash is None else str(self.repair_step_hash)
        object.__setattr__(self, "repair_step_hash", repair_hash)
        object.__setattr__(self, "frozen_mass_invariant", dict(self.frozen_mass_invariant))
        object.__setattr__(self, "seed_report", dict(self.seed_report))
        object.__setattr__(self, "diagnostic_roles", dict(self.diagnostic_roles))
        nonclaims = tuple(str(item) for item in self.nonclaims)
        if not nonclaims:
            raise ValueError("nonclaims must be non-empty")
        object.__setattr__(self, "nonclaims", nonclaims)
        if self.final_status == "passed":
            if self.hard_vetoes:
                raise ValueError("passed fixed-mass step stage cannot have hard vetoes")
            if self.budget_ladder_result is None or not self.budget_ladder_result.passed:
                raise ValueError("passed fixed-mass step stage requires passed ladder")
            if self.selected_step_payload is None or self.selected_step_hash is None:
                raise ValueError("passed fixed-mass step stage requires selected step")
            if self.repair_step_payload is not None or self.repair_step_hash is not None:
                raise ValueError("passed fixed-mass step stage cannot have repair step")
        elif self.repair_step_payload is not None or self.repair_step_hash is not None:
            if self.repair_step_payload is None or self.repair_step_hash is None:
                raise ValueError("repair step payload/hash must be paired")
            if self.selected_step_payload is not None or self.selected_step_hash is not None:
                raise ValueError("repair step cannot also populate selected step")
            if stable_config_hash(self.repair_step_payload) != self.repair_step_hash:
                raise ValueError("repair step hash mismatch")

    @property
    def passed(self) -> bool:
        return self.final_status == "passed"

    @property
    def selected_step_size(self) -> float | None:
        if self.selected_step_payload is None:
            return None
        return float(self.selected_step_payload["step_size"])

    @property
    def repair_step_size(self) -> float | None:
        if self.repair_step_payload is None:
            return None
        return float(self.repair_step_payload["step_size"])

    @property
    def artifact_hash(self) -> str:
        return stable_config_hash(self.payload())

    def payload(self) -> Mapping[str, Any]:
        return {
            "schema": "bayesfilter.hmc_fixed_mass_step_stage.v1",
            "config": self.config.payload(),
            "windowed_stage_artifact_hash": self.windowed_stage_artifact_hash,
            "selected_bootstrap_kernel_hash": self.selected_bootstrap_kernel_hash,
            "adapter_signature": self.adapter_signature,
            "phase4_hmc_adapter_signature": self.phase4_hmc_adapter_signature,
            "ladder_adapter_signature": self.ladder_adapter_signature,
            "ladder_hmc_adapter_signature": self.ladder_hmc_adapter_signature,
            "adapted_mass_artifact_payload": self.adapted_mass_artifact_payload,
            "adapted_mass_artifact_signature": self.adapted_mass_artifact_signature,
            "initial_step_size": self.initial_step_size,
            "fixed_num_leapfrog_steps": self.fixed_num_leapfrog_steps,
            "target_dimension": self.target_dimension,
            "final_status": self.final_status,
            "diagnostic_role": self.diagnostic_role,
            "hard_vetoes": self.hard_vetoes,
            "repair_triggers": self.repair_triggers,
            "diagnostics": self.diagnostics,
            "budget_ladder_config_payload": self.budget_ladder_config_payload,
            "budget_ladder_result": None
            if self.budget_ladder_result is None
            else self.budget_ladder_result.payload(),
            "selected_step_payload": self.selected_step_payload,
            "selected_step_hash": self.selected_step_hash,
            "selected_step_size": self.selected_step_size,
            "repair_step_hash": self.repair_step_hash,
            "repair_step_available": self.repair_step_payload is not None,
            "repair_step_payload_exposed": False,
            "frozen_mass_invariant": self.frozen_mass_invariant,
            "seed_report": self.seed_report,
            "diagnostic_roles": self.diagnostic_roles,
            "passed": self.passed,
            "reports_trajectory_tuning": False,
            "reports_fresh_final_verification": False,
            "reports_posterior_convergence": False,
            "reports_sampler_superiority": False,
            "reports_gpu_or_xla_readiness": False,
            "nonclaims": self.nonclaims,
        }


@dataclass(frozen=True)
class HMCFrozenStepTrajectoryStageConfig:
    """Policy-level config for Phase 6 frozen-step trajectory tuning.

    The caller does not supply candidate leapfrog counts, leapfrog bounds,
    trajectory grids, target trajectory length, step size, mass windows, warmup
    budgets, or tuning budget schedules. Those mechanics are internal
    BayesFilter policy and are recorded only as diagnostic telemetry.
    """

    target_accept_prob: float = 0.70
    acceptance_band: tuple[float, float] = (0.65, 0.75)
    seed: tuple[int, int] = (20260621, 6)
    chain_execution_mode: str = "tf_function"
    use_xla: bool = False
    target_scope: str | None = None
    target_status_trace_policy: str = "none"
    public_timeout_budget_s: float | None = None
    public_timeout_started_perf_counter_s: float | None = None
    source: str = "bayesfilter.inference.hmc_kernel_tuning.frozen_step_trajectory_stage"

    def __post_init__(self) -> None:
        target = float(self.target_accept_prob)
        if not np.isfinite(target) or not 0.0 < target < 1.0:
            raise ValueError("target_accept_prob must be finite and in (0, 1)")
        object.__setattr__(self, "target_accept_prob", target)
        object.__setattr__(
            self,
            "acceptance_band",
            _validate_band(self.acceptance_band, name="acceptance_band"),
        )
        object.__setattr__(self, "seed", _validate_seed(self.seed))
        mode = str(self.chain_execution_mode)
        if mode not in {"tf_function", "eager"}:
            raise ValueError("chain_execution_mode must be 'tf_function' or 'eager'")
        if self.use_xla and mode != "tf_function":
            raise ValueError("XLA HMC requires chain_execution_mode='tf_function'")
        object.__setattr__(self, "chain_execution_mode", mode)
        object.__setattr__(self, "use_xla", bool(self.use_xla))
        if self.target_scope is not None:
            scope = str(self.target_scope)
            if not scope:
                raise ValueError("target_scope must be non-empty when provided")
            object.__setattr__(self, "target_scope", scope)
        target_status_policy = str(self.target_status_trace_policy)
        if target_status_policy not in {"none", "per_chain_step"}:
            raise ValueError(
                "target_status_trace_policy must be 'none' or 'per_chain_step'"
            )
        object.__setattr__(self, "target_status_trace_policy", target_status_policy)
        timeout_budget = (
            None
            if self.public_timeout_budget_s is None
            else float(self.public_timeout_budget_s)
        )
        if timeout_budget is not None and (
            not np.isfinite(timeout_budget) or timeout_budget <= 0.0
        ):
            raise ValueError("public_timeout_budget_s must be positive and finite")
        object.__setattr__(self, "public_timeout_budget_s", timeout_budget)
        timeout_started = (
            None
            if self.public_timeout_started_perf_counter_s is None
            else float(self.public_timeout_started_perf_counter_s)
        )
        if timeout_started is not None and (
            not np.isfinite(timeout_started) or timeout_started < 0.0
        ):
            raise ValueError(
                "public_timeout_started_perf_counter_s must be finite and non-negative"
            )
        object.__setattr__(
            self,
            "public_timeout_started_perf_counter_s",
            timeout_started,
        )
        source = str(self.source)
        if not source:
            raise ValueError("source must be non-empty")
        object.__setattr__(self, "source", source)

    def payload(self) -> Mapping[str, Any]:
        return {
            "target_accept_prob": self.target_accept_prob,
            "acceptance_band": self.acceptance_band,
            "seed": self.seed,
            "chain_execution_mode": self.chain_execution_mode,
            "use_xla": self.use_xla,
            "target_scope": self.target_scope,
            "target_status_trace_policy": self.target_status_trace_policy,
            "public_timeout_budget_s": self.public_timeout_budget_s,
            "public_timeout_started_perf_counter_s": self.public_timeout_started_perf_counter_s,
            "source": self.source,
        }


@dataclass(frozen=True)
class HMCFrozenStepTrajectoryStageResult:
    """Phase 6 frozen-step trajectory handoff; not final verification evidence."""

    config: HMCFrozenStepTrajectoryStageConfig
    geometry_artifact_hash: str
    bootstrap_artifact_hash: str
    windowed_stage_artifact_hash: str
    fixed_mass_step_stage_artifact_hash: str
    selected_bootstrap_kernel_hash: str
    selected_step_hash: str
    adapter_signature: str
    phase4_hmc_adapter_signature: str
    phase5_ladder_hmc_adapter_signature: str
    trajectory_hmc_adapter_signature: str
    adapted_mass_artifact_payload: Mapping[str, Any]
    adapted_mass_artifact_signature: str
    frozen_step_size: float
    fixed_bootstrap_num_leapfrog_steps: int
    target_dimension: int
    candidate_generation: Mapping[str, Any]
    candidate_results: tuple[Mapping[str, Any], ...]
    selected_candidate_index: int | None
    selected_trajectory_payload: Mapping[str, Any] | None
    selected_trajectory_hash: str | None
    final_status: str
    diagnostic_role: str
    hard_vetoes: tuple[str, ...]
    repair_triggers: tuple[str, ...]
    diagnostics: Mapping[str, Any]
    frozen_mass_invariant: Mapping[str, Any]
    frozen_step_invariant: Mapping[str, Any]
    seed_report: Mapping[str, Any]
    diagnostic_roles: Mapping[str, str]
    nonclaims: tuple[str, ...] = FROZEN_STEP_TRAJECTORY_STAGE_NONCLAIMS

    def __post_init__(self) -> None:
        for name in (
            "geometry_artifact_hash",
            "bootstrap_artifact_hash",
            "windowed_stage_artifact_hash",
            "fixed_mass_step_stage_artifact_hash",
            "selected_bootstrap_kernel_hash",
            "selected_step_hash",
            "adapter_signature",
            "phase4_hmc_adapter_signature",
            "phase5_ladder_hmc_adapter_signature",
            "trajectory_hmc_adapter_signature",
            "adapted_mass_artifact_signature",
            "final_status",
            "diagnostic_role",
        ):
            value = str(getattr(self, name))
            if not value:
                raise ValueError(f"{name} must be non-empty")
            object.__setattr__(self, name, value)
        step = float(self.frozen_step_size)
        if not np.isfinite(step) or step <= 0.0:
            raise ValueError("frozen_step_size must be positive and finite")
        object.__setattr__(self, "frozen_step_size", step)
        fixed_l = int(self.fixed_bootstrap_num_leapfrog_steps)
        if fixed_l <= 0:
            raise ValueError("fixed_bootstrap_num_leapfrog_steps must be positive")
        object.__setattr__(self, "fixed_bootstrap_num_leapfrog_steps", fixed_l)
        dimension = int(self.target_dimension)
        if dimension <= 0:
            raise ValueError("target_dimension must be positive")
        object.__setattr__(self, "target_dimension", dimension)
        object.__setattr__(
            self,
            "adapted_mass_artifact_payload",
            dict(self.adapted_mass_artifact_payload),
        )
        object.__setattr__(self, "candidate_generation", dict(self.candidate_generation))
        candidates = tuple(dict(item) for item in self.candidate_results)
        if not candidates and self.final_status != "hard_veto":
            raise ValueError(
                "frozen-step trajectory stage requires completed candidates "
                "unless returning a hard-veto closeout"
            )
        object.__setattr__(self, "candidate_results", candidates)
        selected = (
            None if self.selected_candidate_index is None else int(self.selected_candidate_index)
        )
        if selected is not None and selected not in range(len(candidates)):
            raise ValueError("selected_candidate_index must refer to a candidate")
        object.__setattr__(self, "selected_candidate_index", selected)
        selected_payload = (
            None
            if self.selected_trajectory_payload is None
            else dict(self.selected_trajectory_payload)
        )
        object.__setattr__(self, "selected_trajectory_payload", selected_payload)
        selected_hash = (
            None
            if self.selected_trajectory_hash is None
            else str(self.selected_trajectory_hash)
        )
        object.__setattr__(self, "selected_trajectory_hash", selected_hash)
        object.__setattr__(self, "hard_vetoes", _string_tuple(self.hard_vetoes))
        object.__setattr__(self, "repair_triggers", _string_tuple(self.repair_triggers))
        object.__setattr__(self, "diagnostics", dict(self.diagnostics))
        object.__setattr__(self, "frozen_mass_invariant", dict(self.frozen_mass_invariant))
        object.__setattr__(self, "frozen_step_invariant", dict(self.frozen_step_invariant))
        object.__setattr__(self, "seed_report", dict(self.seed_report))
        object.__setattr__(self, "diagnostic_roles", dict(self.diagnostic_roles))
        nonclaims = tuple(str(item) for item in self.nonclaims)
        if not nonclaims:
            raise ValueError("nonclaims must be non-empty")
        object.__setattr__(self, "nonclaims", nonclaims)
        if self.final_status == "passed":
            if self.hard_vetoes:
                raise ValueError("passed trajectory stage cannot have hard vetoes")
            if selected is None or selected_payload is None or selected_hash is None:
                raise ValueError("passed trajectory stage requires selected payload")
            if candidates[selected].get("classification") != "passed_screen":
                raise ValueError("selected trajectory candidate must have passed")

    @property
    def passed(self) -> bool:
        return self.final_status == "passed"

    @property
    def selected_candidate(self) -> Mapping[str, Any] | None:
        if self.selected_candidate_index is None:
            return None
        return self.candidate_results[self.selected_candidate_index]

    @property
    def selected_num_leapfrog_steps(self) -> int | None:
        candidate = self.selected_candidate
        return None if candidate is None else int(candidate["num_leapfrog_steps"])

    @property
    def selected_trajectory_length(self) -> float | None:
        candidate = self.selected_candidate
        return None if candidate is None else float(candidate["trajectory_length"])

    @property
    def artifact_hash(self) -> str:
        return stable_config_hash(self.payload())

    def payload(self) -> Mapping[str, Any]:
        return {
            "schema": "bayesfilter.hmc_frozen_step_trajectory_stage.v1",
            "config": self.config.payload(),
            "geometry_artifact_hash": self.geometry_artifact_hash,
            "bootstrap_artifact_hash": self.bootstrap_artifact_hash,
            "windowed_stage_artifact_hash": self.windowed_stage_artifact_hash,
            "fixed_mass_step_stage_artifact_hash": self.fixed_mass_step_stage_artifact_hash,
            "selected_bootstrap_kernel_hash": self.selected_bootstrap_kernel_hash,
            "selected_step_hash": self.selected_step_hash,
            "adapter_signature": self.adapter_signature,
            "phase4_hmc_adapter_signature": self.phase4_hmc_adapter_signature,
            "phase5_ladder_hmc_adapter_signature": self.phase5_ladder_hmc_adapter_signature,
            "trajectory_hmc_adapter_signature": self.trajectory_hmc_adapter_signature,
            "adapted_mass_artifact_payload": self.adapted_mass_artifact_payload,
            "adapted_mass_artifact_signature": self.adapted_mass_artifact_signature,
            "frozen_step_size": self.frozen_step_size,
            "fixed_bootstrap_num_leapfrog_steps": self.fixed_bootstrap_num_leapfrog_steps,
            "target_dimension": self.target_dimension,
            "candidate_generation": self.candidate_generation,
            "candidate_results": self.candidate_results,
            "selected_candidate_index": self.selected_candidate_index,
            "selected_candidate": self.selected_candidate,
            "selected_num_leapfrog_steps": self.selected_num_leapfrog_steps,
            "selected_trajectory_length": self.selected_trajectory_length,
            "selected_trajectory_payload": self.selected_trajectory_payload,
            "selected_trajectory_hash": self.selected_trajectory_hash,
            "final_status": self.final_status,
            "diagnostic_role": self.diagnostic_role,
            "hard_vetoes": self.hard_vetoes,
            "repair_triggers": self.repair_triggers,
            "diagnostics": self.diagnostics,
            "frozen_mass_invariant": self.frozen_mass_invariant,
            "frozen_step_invariant": self.frozen_step_invariant,
            "seed_report": self.seed_report,
            "diagnostic_roles": self.diagnostic_roles,
            "passed": self.passed,
            "reports_trajectory_tuning": self.passed,
            "reports_fresh_final_verification": False,
            "reports_posterior_convergence": False,
            "reports_sampler_superiority": False,
            "reports_gpu_or_xla_readiness": False,
            "candidate_mechanics_are_diagnostic_telemetry_only": True,
            "nonclaims": self.nonclaims,
        }


@dataclass(frozen=True)
class HMCTuneVerifyRepairLoopConfig:
    """Policy-level config for the Phase 7 outer tuning loop.

    The config intentionally hides raw HMC mechanics, stage budgets, candidate
    grids, and final verification draw counts from model clients. Those are
    derived from target dimension by BayesFilter-owned policy.
    """

    target_accept_prob: float = 0.70
    acceptance_band: tuple[float, float] = (0.65, 0.75)
    repair_band: tuple[float, float] = (0.55, 0.85)
    max_attempts: int = 5
    seed: tuple[int, int] = (20260621, 7)
    chain_execution_mode: str = "tf_function"
    use_xla: bool = False
    target_scope: str | None = None
    target_status_trace_policy: str = "none"
    public_timeout_budget_s: float | None = None
    public_timeout_started_perf_counter_s: float | None = None
    source: str = "bayesfilter.inference.hmc_kernel_tuning.tune_verify_repair_loop"

    def __post_init__(self) -> None:
        target = float(self.target_accept_prob)
        if not np.isfinite(target) or not 0.0 < target < 1.0:
            raise ValueError("target_accept_prob must be finite and in (0, 1)")
        object.__setattr__(self, "target_accept_prob", target)
        acceptance_band = _validate_band(self.acceptance_band, name="acceptance_band")
        repair_band = _validate_band(self.repair_band, name="repair_band")
        if repair_band[0] > acceptance_band[0] or repair_band[1] < acceptance_band[1]:
            raise ValueError("repair_band must contain acceptance_band")
        object.__setattr__(self, "acceptance_band", acceptance_band)
        object.__setattr__(self, "repair_band", repair_band)
        attempts = int(self.max_attempts)
        if attempts <= 0:
            raise ValueError("max_attempts must be positive")
        if attempts > 5:
            raise ValueError("Phase 7 max_attempts is hard-capped at 5")
        object.__setattr__(self, "max_attempts", attempts)
        object.__setattr__(self, "seed", _validate_seed(self.seed))
        mode = str(self.chain_execution_mode)
        if mode not in {"tf_function", "eager"}:
            raise ValueError("chain_execution_mode must be 'tf_function' or 'eager'")
        if self.use_xla and mode != "tf_function":
            raise ValueError("XLA HMC requires chain_execution_mode='tf_function'")
        object.__setattr__(self, "chain_execution_mode", mode)
        object.__setattr__(self, "use_xla", bool(self.use_xla))
        if self.target_scope is not None:
            scope = str(self.target_scope)
            if not scope:
                raise ValueError("target_scope must be non-empty when provided")
            object.__setattr__(self, "target_scope", scope)
        target_status_policy = str(self.target_status_trace_policy)
        if target_status_policy not in {"none", "per_chain_step"}:
            raise ValueError(
                "target_status_trace_policy must be 'none' or 'per_chain_step'"
            )
        object.__setattr__(self, "target_status_trace_policy", target_status_policy)
        timeout_budget = (
            None
            if self.public_timeout_budget_s is None
            else float(self.public_timeout_budget_s)
        )
        if timeout_budget is not None and (
            not np.isfinite(timeout_budget) or timeout_budget <= 0.0
        ):
            raise ValueError("public_timeout_budget_s must be positive and finite")
        object.__setattr__(self, "public_timeout_budget_s", timeout_budget)
        timeout_started = (
            None
            if self.public_timeout_started_perf_counter_s is None
            else float(self.public_timeout_started_perf_counter_s)
        )
        if timeout_started is not None and (
            not np.isfinite(timeout_started) or timeout_started < 0.0
        ):
            raise ValueError(
                "public_timeout_started_perf_counter_s must be finite and non-negative"
            )
        object.__setattr__(
            self,
            "public_timeout_started_perf_counter_s",
            timeout_started,
        )
        source = str(self.source)
        if not source:
            raise ValueError("source must be non-empty")
        object.__setattr__(self, "source", source)

    def payload(self) -> Mapping[str, Any]:
        return {
            "target_accept_prob": self.target_accept_prob,
            "acceptance_band": self.acceptance_band,
            "repair_band": self.repair_band,
            "max_attempts": self.max_attempts,
            "seed": self.seed,
            "chain_execution_mode": self.chain_execution_mode,
            "use_xla": self.use_xla,
            "target_scope": self.target_scope,
            "target_status_trace_policy": self.target_status_trace_policy,
            "public_timeout_budget_s": self.public_timeout_budget_s,
            "public_timeout_started_perf_counter_s": self.public_timeout_started_perf_counter_s,
            "source": self.source,
        }


@dataclass(frozen=True)
class HMCTuneVerifyRepairAttempt:
    """One Phase 7 tune-verify attempt and its private budget state."""

    attempt_index: int
    budget_policy_payload: Mapping[str, Any]
    incoming_state_payload: Mapping[str, Any] | None
    windowed_stage: HMCWindowedMassStageResult | None
    fixed_mass_step_stage: HMCFixedMassStepStageResult | None
    frozen_step_trajectory_stage: HMCFrozenStepTrajectoryStageResult | None
    verification_config_payload: Mapping[str, Any] | None
    verification_diagnostics: Mapping[str, Any]
    verification_callback_result: FixedMassHMCTuningBudgetCallbackResult
    final_status: str
    diagnostic_role: str
    hard_vetoes: tuple[str, ...]
    repair_triggers: tuple[str, ...]
    handoff_state_payload: Mapping[str, Any] | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "attempt_index", int(self.attempt_index))
        object.__setattr__(
            self,
            "budget_policy_payload",
            dict(self.budget_policy_payload),
        )
        incoming = (
            None
            if self.incoming_state_payload is None
            else dict(self.incoming_state_payload)
        )
        object.__setattr__(self, "incoming_state_payload", incoming)
        config_payload = (
            None
            if self.verification_config_payload is None
            else dict(self.verification_config_payload)
        )
        object.__setattr__(self, "verification_config_payload", config_payload)
        object.__setattr__(
            self,
            "verification_diagnostics",
            dict(self.verification_diagnostics),
        )
        object.__setattr__(self, "final_status", str(self.final_status))
        object.__setattr__(self, "diagnostic_role", str(self.diagnostic_role))
        object.__setattr__(self, "hard_vetoes", _string_tuple(self.hard_vetoes))
        object.__setattr__(self, "repair_triggers", _string_tuple(self.repair_triggers))
        handoff = (
            None
            if self.handoff_state_payload is None
            else dict(self.handoff_state_payload)
        )
        object.__setattr__(self, "handoff_state_payload", handoff)

    @property
    def passed(self) -> bool:
        return self.final_status == "passed"

    def payload(self) -> Mapping[str, Any]:
        return {
            "attempt_index": self.attempt_index,
            "budget_policy": self.budget_policy_payload,
            "incoming_state": self.incoming_state_payload,
            "windowed_stage": None
            if self.windowed_stage is None
            else self.windowed_stage.payload(),
            "fixed_mass_step_stage": None
            if self.fixed_mass_step_stage is None
            else self.fixed_mass_step_stage.payload(),
            "frozen_step_trajectory_stage": None
            if self.frozen_step_trajectory_stage is None
            else self.frozen_step_trajectory_stage.payload(),
            "verification_config_payload": self.verification_config_payload,
            "verification_diagnostics": self.verification_diagnostics,
            "verification_callback_result": self.verification_callback_result.payload(),
            "final_status": self.final_status,
            "diagnostic_role": self.diagnostic_role,
            "hard_vetoes": self.hard_vetoes,
            "repair_triggers": self.repair_triggers,
            "handoff_state": self.handoff_state_payload,
            "passed": self.passed,
        }


@dataclass(frozen=True)
class HMCTuneVerifyRepairLoopResult:
    """Phase 7 frozen-kernel handoff after tune/verify/repair."""

    config: HMCTuneVerifyRepairLoopConfig
    geometry_artifact_hash: str
    bootstrap_artifact_hash: str
    adapter_signature: str
    target_dimension: int
    attempts: tuple[HMCTuneVerifyRepairAttempt, ...]
    final_status: str
    diagnostic_role: str
    hard_vetoes: tuple[str, ...]
    repair_triggers: tuple[str, ...]
    final_kernel_payload: Mapping[str, Any] | None
    final_kernel_hash: str | None
    seed_report: Mapping[str, Any]
    diagnostic_roles: Mapping[str, str]
    terminal_budget_guard_payload: Mapping[str, Any] | None = None
    nonclaims: tuple[str, ...] = TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS

    def __post_init__(self) -> None:
        for name in (
            "geometry_artifact_hash",
            "bootstrap_artifact_hash",
            "adapter_signature",
            "final_status",
            "diagnostic_role",
        ):
            value = str(getattr(self, name))
            if not value:
                raise ValueError(f"{name} must be non-empty")
            object.__setattr__(self, name, value)
        dimension = int(self.target_dimension)
        if dimension <= 0:
            raise ValueError("target_dimension must be positive")
        object.__setattr__(self, "target_dimension", dimension)
        attempts = tuple(self.attempts)
        if not attempts:
            raise ValueError("Phase 7 loop requires at least one attempt")
        object.__setattr__(self, "attempts", attempts)
        object.__setattr__(self, "hard_vetoes", _string_tuple(self.hard_vetoes))
        object.__setattr__(self, "repair_triggers", _string_tuple(self.repair_triggers))
        final_payload = (
            None if self.final_kernel_payload is None else dict(self.final_kernel_payload)
        )
        object.__setattr__(self, "final_kernel_payload", final_payload)
        final_hash = None if self.final_kernel_hash is None else str(self.final_kernel_hash)
        object.__setattr__(self, "final_kernel_hash", final_hash)
        object.__setattr__(self, "seed_report", dict(self.seed_report))
        object.__setattr__(self, "diagnostic_roles", dict(self.diagnostic_roles))
        terminal_guard = (
            None
            if self.terminal_budget_guard_payload is None
            else dict(self.terminal_budget_guard_payload)
        )
        object.__setattr__(self, "terminal_budget_guard_payload", terminal_guard)
        nonclaims = tuple(str(item) for item in self.nonclaims)
        if not nonclaims:
            raise ValueError("nonclaims must be non-empty")
        object.__setattr__(self, "nonclaims", nonclaims)
        if self.final_status == "passed":
            if self.hard_vetoes:
                raise ValueError("passed Phase 7 loop cannot have hard vetoes")
            if final_payload is None or final_hash is None:
                raise ValueError("passed Phase 7 loop requires final kernel")
            if stable_config_hash(final_payload) != final_hash:
                raise ValueError("final kernel hash mismatch")
        if self.final_status in {
            "repair_or_retry",
            "budget_exhausted",
            "architecture_blocked",
            "hard_veto",
        }:
            if final_payload is not None or final_hash is not None:
                raise ValueError("non-passed Phase 7 loop cannot emit final kernel")

    @property
    def passed(self) -> bool:
        return self.final_status == "passed"

    @property
    def artifact_hash(self) -> str:
        return stable_config_hash(self.payload(include_final_mass_arrays=True))

    def payload(self, *, include_final_mass_arrays: bool = True) -> Mapping[str, Any]:
        del include_final_mass_arrays
        return {
            "schema": "bayesfilter.hmc_tune_verify_repair_loop.v1",
            "config": self.config.payload(),
            "geometry_artifact_hash": self.geometry_artifact_hash,
            "bootstrap_artifact_hash": self.bootstrap_artifact_hash,
            "adapter_signature": self.adapter_signature,
            "target_dimension": self.target_dimension,
            "attempts": tuple(attempt.payload() for attempt in self.attempts),
            "attempt_count": len(self.attempts),
            "budget_history": tuple(
                attempt.budget_policy_payload for attempt in self.attempts
            ),
            "final_status": self.final_status,
            "diagnostic_role": self.diagnostic_role,
            "hard_vetoes": self.hard_vetoes,
            "repair_triggers": self.repair_triggers,
            "final_kernel_payload": self.final_kernel_payload,
            "final_kernel_hash": self.final_kernel_hash,
            "seed_report": self.seed_report,
            "diagnostic_roles": self.diagnostic_roles,
            "terminal_budget_guard": self.terminal_budget_guard_payload,
            "passed": self.passed,
            "budget_exhausted_is_non_promoting": self.final_status == "budget_exhausted",
            "reports_posterior_convergence": False,
            "reports_sampler_superiority": False,
            "reports_default_readiness": False,
            "reports_external_client_scientific_claim": False,
            "reports_gpu_or_xla_readiness": False,
            "nonclaims": self.nonclaims,
        }


@dataclass(frozen=True)
class HMCKernelTuningConfig:
    """Public one-call HMC kernel tuning policy.

    This config is intentionally model-facing.  It exposes presets, acceptance
    policy, geometry policy, seeds, and target metadata; it does not expose
    caller-chosen step sizes, leapfrog counts, candidate grids, mass windows,
    warmup budgets, draw counts, or budget schedules.
    """

    preset: str = "standard"
    target_accept_prob: float = 0.70
    acceptance_band: tuple[float, float] = (0.65, 0.75)
    repair_band: tuple[float, float] = (0.55, 0.85)
    bootstrap_max_repairs: int = 5
    max_attempts: int = 5
    seed: tuple[int, int] = (20260621, 8)
    chain_execution_mode: str = "tf_function"
    use_xla: bool = False
    target_scope: str | None = None
    target_status_trace_policy: str = "none"
    geometry_scaling_c: float = 0.5
    stability_guard: float = 0.8
    covariance_jitter: float = 1.0e-9
    eigenvalue_floor: float | None = 1.0e-9
    max_condition_number: float | None = None
    allow_geometry_fallback: bool = False
    public_timeout_budget_s: float | None = None
    source: str = "bayesfilter.inference.tune_hmc_kernel"

    def __post_init__(self) -> None:
        preset = str(self.preset)
        if preset not in {"smoke", "diagnostic", "diagnostic_plus", "standard", "serious"}:
            raise ValueError(
                "preset must be 'smoke', 'diagnostic', 'diagnostic_plus', "
                "'standard', or 'serious'"
            )
        object.__setattr__(self, "preset", preset)
        target = float(self.target_accept_prob)
        if not np.isfinite(target) or not 0.0 < target < 1.0:
            raise ValueError("target_accept_prob must be finite and in (0, 1)")
        object.__setattr__(self, "target_accept_prob", target)
        acceptance_band = _validate_band(self.acceptance_band, name="acceptance_band")
        repair_band = _validate_band(self.repair_band, name="repair_band")
        if repair_band[0] > acceptance_band[0] or repair_band[1] < acceptance_band[1]:
            raise ValueError("repair_band must contain acceptance_band")
        object.__setattr__(self, "acceptance_band", acceptance_band)
        object.__setattr__(self, "repair_band", repair_band)
        repairs = int(self.bootstrap_max_repairs)
        if repairs < 0:
            raise ValueError("bootstrap_max_repairs must be non-negative")
        object.__setattr__(self, "bootstrap_max_repairs", repairs)
        attempts = int(self.max_attempts)
        if attempts <= 0:
            raise ValueError("max_attempts must be positive")
        if attempts > 5:
            raise ValueError("max_attempts is hard-capped at 5")
        object.__setattr__(self, "max_attempts", attempts)
        object.__setattr__(self, "seed", _validate_seed(self.seed))
        mode = str(self.chain_execution_mode)
        if mode not in {"tf_function", "eager"}:
            raise ValueError("chain_execution_mode must be 'tf_function' or 'eager'")
        if self.use_xla and mode != "tf_function":
            raise ValueError("XLA HMC requires chain_execution_mode='tf_function'")
        object.__setattr__(self, "chain_execution_mode", mode)
        object.__setattr__(self, "use_xla", bool(self.use_xla))
        if self.target_scope is not None:
            scope = str(self.target_scope)
            if not scope:
                raise ValueError("target_scope must be non-empty when provided")
            object.__setattr__(self, "target_scope", scope)
        target_status_policy = str(self.target_status_trace_policy)
        if target_status_policy not in {"none", "per_chain_step"}:
            raise ValueError(
                "target_status_trace_policy must be 'none' or 'per_chain_step'"
            )
        object.__setattr__(self, "target_status_trace_policy", target_status_policy)
        scaling = float(self.geometry_scaling_c)
        if not np.isfinite(scaling) or scaling <= 0.0:
            raise ValueError("geometry_scaling_c must be positive and finite")
        guard = float(self.stability_guard)
        if not np.isfinite(guard) or guard <= 0.0:
            raise ValueError("stability_guard must be positive and finite")
        jitter = float(self.covariance_jitter)
        if not np.isfinite(jitter) or jitter < 0.0:
            raise ValueError("covariance_jitter must be finite and non-negative")
        floor = (
            None
            if self.eigenvalue_floor is None
            else float(self.eigenvalue_floor)
        )
        if floor is not None and (not np.isfinite(floor) or floor < 0.0):
            raise ValueError("eigenvalue_floor must be finite and non-negative")
        condition = (
            None
            if self.max_condition_number is None
            else float(self.max_condition_number)
        )
        if condition is not None and (
            not np.isfinite(condition) or condition <= 1.0
        ):
            raise ValueError("max_condition_number must be finite and greater than 1")
        object.__setattr__(self, "geometry_scaling_c", scaling)
        object.__setattr__(self, "stability_guard", guard)
        object.__setattr__(self, "covariance_jitter", jitter)
        object.__setattr__(self, "eigenvalue_floor", floor)
        object.__setattr__(self, "max_condition_number", condition)
        object.__setattr__(self, "allow_geometry_fallback", bool(self.allow_geometry_fallback))
        timeout_budget = (
            None
            if self.public_timeout_budget_s is None
            else float(self.public_timeout_budget_s)
        )
        if timeout_budget is not None and (
            not np.isfinite(timeout_budget) or timeout_budget <= 0.0
        ):
            raise ValueError("public_timeout_budget_s must be positive and finite")
        object.__setattr__(self, "public_timeout_budget_s", timeout_budget)
        source = str(self.source)
        if not source:
            raise ValueError("source must be non-empty")
        object.__setattr__(self, "source", source)

    @classmethod
    def smoke(cls, **overrides: Any) -> "HMCKernelTuningConfig":
        payload: dict[str, Any] = {
            "preset": "smoke",
            "max_attempts": 1,
            "chain_execution_mode": "eager",
            "source": "bayesfilter.inference.tune_hmc_kernel.smoke",
        }
        payload.update(overrides)
        return cls(**payload)

    @classmethod
    def standard(cls, **overrides: Any) -> "HMCKernelTuningConfig":
        payload: dict[str, Any] = {
            "preset": "standard",
            "max_attempts": 3,
            "source": "bayesfilter.inference.tune_hmc_kernel.standard",
        }
        payload.update(overrides)
        return cls(**payload)

    @classmethod
    def diagnostic(cls, **overrides: Any) -> "HMCKernelTuningConfig":
        payload: dict[str, Any] = {
            "preset": "diagnostic",
            "max_attempts": 2,
            "source": "bayesfilter.inference.tune_hmc_kernel.diagnostic",
        }
        payload.update(overrides)
        return cls(**payload)

    @classmethod
    def diagnostic_plus(cls, **overrides: Any) -> "HMCKernelTuningConfig":
        payload: dict[str, Any] = {
            "preset": "diagnostic_plus",
            "max_attempts": 2,
            "source": "bayesfilter.inference.tune_hmc_kernel.diagnostic_plus",
        }
        payload.update(overrides)
        return cls(**payload)

    @classmethod
    def serious(cls, **overrides: Any) -> "HMCKernelTuningConfig":
        payload: dict[str, Any] = {
            "preset": "serious",
            "max_attempts": 5,
            "source": "bayesfilter.inference.tune_hmc_kernel.serious",
        }
        payload.update(overrides)
        return cls(**payload)

    @property
    def is_smoke(self) -> bool:
        return self.preset == "smoke"

    @property
    def uses_serious_budget_policy(self) -> bool:
        return self.preset == "serious"

    def payload(self) -> Mapping[str, Any]:
        return {
            "schema": "bayesfilter.hmc_kernel_tuning_config.v1",
            "preset": self.preset,
            "target_accept_prob": self.target_accept_prob,
            "acceptance_band": self.acceptance_band,
            "repair_band": self.repair_band,
            "bootstrap_max_repairs": self.bootstrap_max_repairs,
            "max_attempts": self.max_attempts,
            "seed": self.seed,
            "chain_execution_mode": self.chain_execution_mode,
            "use_xla": self.use_xla,
            "target_scope": self.target_scope,
            "target_status_trace_policy": self.target_status_trace_policy,
            "geometry_scaling_c": self.geometry_scaling_c,
            "stability_guard": self.stability_guard,
            "covariance_jitter": self.covariance_jitter,
            "eigenvalue_floor": self.eigenvalue_floor,
            "max_condition_number": self.max_condition_number,
            "allow_geometry_fallback": self.allow_geometry_fallback,
            "public_timeout_budget_s": self.public_timeout_budget_s,
            "source": self.source,
            "preset_role": _public_tuning_preset_role(self.preset),
            "hmc_mechanics_owned_by_bayesfilter": True,
            "forbidden_public_fields": _public_tuning_forbidden_fields(),
            "reports_posterior_convergence": False,
            "reports_sampler_superiority": False,
            "reports_default_readiness": False,
            "reports_gpu_or_xla_readiness": False,
        }


@dataclass(frozen=True)
class HMCKernelTuningResult:
    """Public one-call HMC kernel tuning result and frozen-kernel handoff gate."""

    config: HMCKernelTuningConfig
    adapter_signature: str
    target_dimension: int
    geometry: HMCGeometryInitializationResult | None
    bootstrap: HMCBootstrapScreenResult | None
    tune_verify_repair_loop: HMCTuneVerifyRepairLoopResult | None
    final_status: str
    diagnostic_role: str
    hard_vetoes: tuple[str, ...]
    repair_triggers: tuple[str, ...]
    final_kernel_payload: Mapping[str, Any] | None
    final_kernel_hash: str | None
    artifact_path: str | None
    diagnostic_roles: Mapping[str, str]
    nonclaims: tuple[str, ...] = HMC_KERNEL_TUNING_PUBLIC_NONCLAIMS

    def __post_init__(self) -> None:
        if not isinstance(self.config, HMCKernelTuningConfig):
            raise TypeError("config must be HMCKernelTuningConfig")
        signature = str(self.adapter_signature)
        if not signature:
            raise ValueError("adapter_signature must be non-empty")
        object.__setattr__(self, "adapter_signature", signature)
        dimension = int(self.target_dimension)
        if dimension <= 0:
            raise ValueError("target_dimension must be positive")
        object.__setattr__(self, "target_dimension", dimension)
        status = str(self.final_status)
        if not status:
            raise ValueError("final_status must be non-empty")
        role = str(self.diagnostic_role)
        if not role:
            raise ValueError("diagnostic_role must be non-empty")
        object.__setattr__(self, "final_status", status)
        object.__setattr__(self, "diagnostic_role", role)
        object.__setattr__(self, "hard_vetoes", _string_tuple(self.hard_vetoes))
        object.__setattr__(self, "repair_triggers", _string_tuple(self.repair_triggers))
        final_payload = (
            None if self.final_kernel_payload is None else dict(self.final_kernel_payload)
        )
        final_hash = None if self.final_kernel_hash is None else str(self.final_kernel_hash)
        object.__setattr__(self, "final_kernel_payload", final_payload)
        object.__setattr__(self, "final_kernel_hash", final_hash)
        artifact = None if self.artifact_path is None else str(self.artifact_path)
        object.__setattr__(self, "artifact_path", artifact)
        object.__setattr__(self, "diagnostic_roles", dict(self.diagnostic_roles))
        nonclaims = tuple(str(item) for item in self.nonclaims)
        if not nonclaims:
            raise ValueError("nonclaims must be non-empty")
        object.__setattr__(self, "nonclaims", nonclaims)
        if self.geometry is not None:
            if self.geometry.adapter_signature != signature:
                raise ValueError("geometry adapter signature mismatch")
            if self.geometry.target_dimension != dimension:
                raise ValueError("geometry target dimension mismatch")
        if self.bootstrap is not None:
            if self.geometry is None:
                raise ValueError("bootstrap result requires geometry result")
            if self.bootstrap.adapter_signature != signature:
                raise ValueError("bootstrap adapter signature mismatch")
            if self.bootstrap.target_dimension != dimension:
                raise ValueError("bootstrap target dimension mismatch")
            if self.bootstrap.geometry_artifact_hash != self.geometry.artifact_hash:
                raise ValueError("bootstrap geometry artifact mismatch")
        if self.tune_verify_repair_loop is not None:
            if self.bootstrap is None:
                raise ValueError("loop result requires bootstrap result")
            if self.tune_verify_repair_loop.adapter_signature != signature:
                raise ValueError("loop adapter signature mismatch")
            if self.tune_verify_repair_loop.target_dimension != dimension:
                raise ValueError("loop target dimension mismatch")
            if (
                self.tune_verify_repair_loop.bootstrap_artifact_hash
                != self.bootstrap.artifact_hash
            ):
                raise ValueError("loop bootstrap artifact mismatch")
        if status == "passed":
            if self.hard_vetoes:
                raise ValueError("passed public tuning result cannot have hard vetoes")
            if self.tune_verify_repair_loop is None or not self.tune_verify_repair_loop.passed:
                raise ValueError("passed public tuning result requires passed Phase 7 loop")
            if final_payload is None or final_hash is None:
                raise ValueError("passed public tuning result requires final kernel")
            if stable_config_hash(final_payload) != final_hash:
                raise ValueError("public final kernel hash mismatch")
        elif final_payload is not None or final_hash is not None:
            raise ValueError("non-passed public tuning result cannot emit final kernel")

    @property
    def passed(self) -> bool:
        return self.final_status == "passed"

    @property
    def final_frozen_kernel_handoff(self) -> Mapping[str, Any] | None:
        return self.final_kernel_payload

    @property
    def artifact_hash(self) -> str:
        return stable_config_hash(self.payload(include_internal_diagnostics=True))

    def payload(self, *, include_internal_diagnostics: bool = True) -> Mapping[str, Any]:
        return {
            "schema": "bayesfilter.hmc_kernel_tuning_result.v1",
            "config": self.config.payload(),
            "adapter_signature": self.adapter_signature,
            "target_dimension": self.target_dimension,
            "geometry_artifact_hash": None
            if self.geometry is None
            else self.geometry.artifact_hash,
            "bootstrap_artifact_hash": None
            if self.bootstrap is None
            else self.bootstrap.artifact_hash,
            "loop_artifact_hash": None
            if self.tune_verify_repair_loop is None
            else self.tune_verify_repair_loop.artifact_hash,
            "geometry": None
            if self.geometry is None or not include_internal_diagnostics
            else self.geometry.payload(include_mass_arrays=False),
            "bootstrap": None
            if self.bootstrap is None or not include_internal_diagnostics
            else self.bootstrap.payload(),
            "tune_verify_repair_loop": None
            if self.tune_verify_repair_loop is None or not include_internal_diagnostics
            else self.tune_verify_repair_loop.payload(include_final_mass_arrays=False),
            "final_status": self.final_status,
            "diagnostic_role": self.diagnostic_role,
            "hard_vetoes": self.hard_vetoes,
            "repair_triggers": self.repair_triggers,
            "final_kernel_payload": self.final_kernel_payload,
            "final_kernel_hash": self.final_kernel_hash,
            "artifact_path": self.artifact_path,
            "diagnostic_roles": self.diagnostic_roles,
            "passed": self.passed,
            "smoke_result_is_contract_only": self.config.is_smoke,
            "final_kernel_requires_phase7_pass": True,
            "reports_posterior_convergence": False,
            "reports_sampler_superiority": False,
            "reports_default_readiness": False,
            "reports_external_client_scientific_claim": False,
            "reports_gpu_or_xla_readiness": False,
            "nonclaims": self.nonclaims,
        }


@dataclass(frozen=True)
class RetainedFrozenKernelAdapterReplayResult:
    """BayesFilter-owned replay of a verified retained fixed-kernel adapter.

    The final adapted mass is defined in the latent coordinate system of the
    Phase 4/bootstrap fixed-mass adapter, not in the base model coordinates.
    This result preserves that two-transform lineage so model repositories do
    not have to reconstruct HMC/filtering mechanics locally.
    """

    adapter: Any
    adapted_mass_artifact: PrecomputedMassArtifact
    contract: Mapping[str, Any]
    final_kernel_payload: Mapping[str, Any]
    nonclaims: tuple[str, ...] = RETAINED_FROZEN_KERNEL_REPLAY_NONCLAIMS

    def __post_init__(self) -> None:
        if not isinstance(self.adapted_mass_artifact, PrecomputedMassArtifact):
            raise TypeError("adapted_mass_artifact must be PrecomputedMassArtifact")
        contract = dict(self.contract)
        final_payload = dict(self.final_kernel_payload)
        final_signature = str(contract.get("final_hmc_adapter_signature", ""))
        if not final_signature:
            raise ValueError("replay contract missing final_hmc_adapter_signature")
        if stable_adapter_signature(self.adapter) != final_signature:
            raise ValueError("replay adapter signature does not match contract")
        mass_signature = str(contract.get("adapted_mass_artifact_signature", ""))
        if not mass_signature:
            raise ValueError("replay contract missing adapted mass signature")
        if _mass_artifact_signature(self.adapted_mass_artifact) != mass_signature:
            raise ValueError("adapted mass signature does not match contract")
        nonclaims = tuple(str(item) for item in self.nonclaims)
        if not nonclaims:
            raise ValueError("nonclaims must be non-empty")
        object.__setattr__(self, "contract", contract)
        object.__setattr__(self, "final_kernel_payload", final_payload)
        object.__setattr__(self, "nonclaims", nonclaims)

    def payload(self) -> Mapping[str, Any]:
        return {
            "schema": "bayesfilter.retained_frozen_kernel_adapter_replay_result.v1",
            "contract": self.contract,
            "final_kernel_payload": {
                "public_handoff_schema": self.final_kernel_payload.get(
                    "public_handoff_schema"
                ),
                "target_scope": self.final_kernel_payload.get("target_scope"),
                "target_dimension": self.final_kernel_payload.get("target_dimension"),
                "fresh_fixed_kernel_verification_passed": self.final_kernel_payload.get(
                    "fresh_fixed_kernel_verification_passed"
                ),
                "adapted_mass_artifact_signature": self.final_kernel_payload.get(
                    "adapted_mass_artifact_signature"
                ),
                "phase7_final_kernel_hash": self.final_kernel_payload.get(
                    "phase7_final_kernel_hash"
                ),
            },
            "private_mass_arrays_publicized": False,
            "hmc_or_tuning_invoked": False,
            "reports_posterior_convergence": False,
            "reports_sampler_superiority": False,
            "reports_default_readiness": False,
            "reports_external_client_scientific_claim": False,
            "reports_gpu_or_xla_readiness": False,
            "nonclaims": self.nonclaims,
        }


def build_retained_frozen_kernel_hmc_adapter_from_tuning_payload(
    *,
    adapter: Any,
    tuning_payload: Mapping[str, Any],
    initial_position: Any,
    initial_covariance: Any | None = None,
    negative_hessian: Any | None = None,
    parameter_scales: Any | None = None,
    target_scope: str | None = None,
) -> RetainedFrozenKernelAdapterReplayResult:
    """Rebuild the BayesFilter adapter stack verified by one-call tuning.

    This helper performs no HMC execution.  It is the replay boundary for model
    repositories that need to launch a retained fixed-kernel run from a prior
    BayesFilter tuning result: callers supply their reviewed base adapter and
    the private tuning payload, and BayesFilter reconstructs the exact
    two-transform HMC adapter stack that the tuning verifier signed.
    """

    if not isinstance(tuning_payload, Mapping):
        raise TypeError("tuning_payload must be a mapping")
    if tuning_payload.get("schema") != "bayesfilter.hmc_kernel_tuning_result.v1":
        raise ValueError("tuning payload schema mismatch")
    if tuning_payload.get("passed") is not True or tuning_payload.get("final_status") != "passed":
        raise ValueError("retained frozen-kernel replay requires passed tuning payload")
    if tuning_payload.get("hard_vetoes"):
        raise ValueError("retained frozen-kernel replay rejects hard-vetoed tuning payload")
    adapter_signature = stable_adapter_signature(adapter)
    if str(tuning_payload.get("adapter_signature", "")) != adapter_signature:
        raise ValueError("tuning payload adapter signature mismatch")
    dimension = int(tuning_payload.get("target_dimension", 0))
    if dimension <= 0:
        raise ValueError("tuning payload target_dimension must be positive")
    if int(getattr(adapter, "parameter_dim", dimension)) != dimension:
        raise ValueError("adapter parameter_dim does not match tuning payload")

    config_payload = _required_mapping(tuning_payload, "config")
    final_kernel_payload = _replay_final_kernel_payload(tuning_payload)
    if final_kernel_payload.get("fresh_fixed_kernel_verification_passed") is not True:
        raise ValueError("final kernel verification did not pass")
    scope = _resolve_replay_target_scope(
        adapter=adapter,
        config_payload=config_payload,
        final_kernel_payload=final_kernel_payload,
        target_scope=target_scope,
    )
    geometry_payload = _required_mapping(tuning_payload, "geometry")
    geometry_config_payload = _required_mapping(geometry_payload, "config")
    geometry = initialize_hmc_kernel_geometry(
        adapter=adapter,
        initial_position=initial_position,
        config=_geometry_config_from_payload(geometry_config_payload),
        negative_hessian=negative_hessian,
        initial_covariance=initial_covariance,
        parameter_scales=parameter_scales,
    )
    if geometry.artifact_hash != str(tuning_payload.get("geometry_artifact_hash", "")):
        raise ValueError("reconstructed geometry artifact hash mismatch")
    if geometry.mass_artifact_signature != str(
        geometry_payload.get("mass_artifact_signature", "")
    ):
        raise ValueError("reconstructed geometry mass signature mismatch")

    bootstrap_payload = _required_mapping(tuning_payload, "bootstrap")
    phase4_adapter = _build_bootstrap_fixed_mass_adapter(
        adapter=adapter,
        mass_artifact=geometry.mass_artifact,
        mass_signature=geometry.mass_artifact_signature,
        target_scope=scope,
        nonclaims=FIXED_MASS_STEP_STAGE_NONCLAIMS,
    )
    phase4_signature = stable_adapter_signature(phase4_adapter)
    expected_phase4_signature = _expected_phase4_adapter_signature(
        bootstrap_payload=bootstrap_payload,
        tuning_payload=tuning_payload,
    )
    if phase4_signature != expected_phase4_signature:
        raise ValueError("reconstructed Phase 4 HMC adapter signature mismatch")

    adapted_mass_payload = _required_mapping(
        final_kernel_payload,
        "adapted_mass_artifact_payload",
    )
    adapted_mass = PrecomputedMassArtifact.from_payload(
        adapted_mass_payload,
        expected_adapter_signature=phase4_signature,
        expected_dim=dimension,
    )
    adapted_mass_signature = _mass_artifact_signature(adapted_mass)
    if adapted_mass_signature != str(
        final_kernel_payload.get("adapted_mass_artifact_signature", "")
    ):
        raise ValueError("reconstructed adapted mass signature mismatch")

    final_adapter = _build_fixed_mass_hmc_adapter(
        adapter=phase4_adapter,
        mass_artifact=adapted_mass,
        mass_signature=adapted_mass_signature,
        target_scope=scope,
    )
    final_signature = stable_adapter_signature(final_adapter)
    expected_final_signature = _expected_final_adapter_signature(tuning_payload)
    if final_signature != expected_final_signature:
        raise ValueError("reconstructed final HMC adapter signature mismatch")

    contract = {
        "schema": "bayesfilter.retained_frozen_kernel_adapter_replay_contract.v1",
        "base_adapter_signature": adapter_signature,
        "geometry_artifact_hash": geometry.artifact_hash,
        "geometry_mass_artifact_signature": geometry.mass_artifact_signature,
        "phase4_hmc_adapter_signature": phase4_signature,
        "adapted_mass_parent_adapter_signature": adapted_mass.adapter_signature,
        "adapted_mass_artifact_signature": adapted_mass_signature,
        "final_hmc_adapter_signature": final_signature,
        "target_scope": scope,
        "target_dimension": dimension,
        "final_kernel_hash": tuning_payload.get("final_kernel_hash"),
        "hmc_or_tuning_invoked": False,
        "replay_owned_by_bayesfilter": True,
        "reports_posterior_convergence": False,
        "reports_sampler_superiority": False,
        "reports_default_readiness": False,
        "reports_external_client_scientific_claim": False,
        "reports_gpu_or_xla_readiness": False,
    }
    return RetainedFrozenKernelAdapterReplayResult(
        adapter=final_adapter,
        adapted_mass_artifact=adapted_mass,
        contract=contract,
        final_kernel_payload=final_kernel_payload,
    )


def _required_mapping(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise ValueError(f"retained frozen-kernel replay missing mapping: {key}")
    return value


def _replay_final_kernel_payload(tuning_payload: Mapping[str, Any]) -> Mapping[str, Any]:
    loop = _required_mapping(tuning_payload, "tune_verify_repair_loop")
    loop_payload = loop.get("final_kernel_payload")
    if isinstance(loop_payload, Mapping):
        return loop_payload
    top_level_payload = _required_mapping(tuning_payload, "final_kernel_payload")
    if top_level_payload.get("public_handoff_schema") == (
        "bayesfilter.hmc_public_frozen_kernel_handoff.v1"
    ):
        raise ValueError(
            "retained frozen-kernel replay requires private final kernel payload; "
            "public handoff alone is not replayable"
        )
    return top_level_payload


def _geometry_config_from_payload(
    payload: Mapping[str, Any],
) -> HMCGeometryInitializationConfig:
    return HMCGeometryInitializationConfig(
        geometry_scaling_c=float(payload.get("geometry_scaling_c", 0.5)),
        stability_guard=float(payload.get("stability_guard", 0.8)),
        covariance_jitter=float(payload.get("covariance_jitter", 1.0e-9)),
        eigenvalue_floor=(
            None
            if payload.get("eigenvalue_floor") is None
            else float(payload.get("eigenvalue_floor"))
        ),
        max_condition_number=(
            None
            if payload.get("max_condition_number") is None
            else float(payload.get("max_condition_number"))
        ),
        allow_geometry_fallback=bool(payload.get("allow_geometry_fallback", False)),
        seed=tuple(int(item) for item in payload.get("seed", (20260621, 2))),
        source=str(payload.get("source", "bayesfilter.inference.hmc_kernel_tuning.geometry")),
    )


def _resolve_replay_target_scope(
    *,
    adapter: Any,
    config_payload: Mapping[str, Any],
    final_kernel_payload: Mapping[str, Any],
    target_scope: str | None,
) -> str:
    capability = value_score_capability(adapter)
    candidates = [
        target_scope,
        final_kernel_payload.get("target_scope"),
        config_payload.get("target_scope"),
        capability.target_scope,
    ]
    scope: str | None = None
    for candidate in candidates:
        if candidate is None:
            continue
        text = str(candidate)
        if not text:
            raise ValueError("retained frozen-kernel replay target_scope must be non-empty")
        if scope is None:
            scope = text
        elif scope != text:
            raise ValueError("retained frozen-kernel replay target_scope mismatch")
    if scope is None:
        raise ValueError("retained frozen-kernel replay requires target_scope")
    return scope


def _expected_phase4_adapter_signature(
    *,
    bootstrap_payload: Mapping[str, Any],
    tuning_payload: Mapping[str, Any],
) -> str:
    candidates: list[str] = []
    value = bootstrap_payload.get("hmc_adapter_signature")
    if value:
        candidates.append(str(value))
    for attempt in _replay_attempts(tuning_payload):
        for stage_name in (
            "windowed_stage",
            "fixed_mass_step_stage",
            "frozen_step_trajectory_stage",
        ):
            stage = attempt.get(stage_name)
            if not isinstance(stage, Mapping):
                continue
            for key in ("hmc_adapter_signature", "phase4_hmc_adapter_signature"):
                value = stage.get(key)
                if value:
                    candidates.append(str(value))
    return _single_replay_signature(
        candidates,
        label="Phase 4 HMC adapter signature",
    )


def _expected_final_adapter_signature(tuning_payload: Mapping[str, Any]) -> str:
    trajectory_candidates: list[str] = []
    fallback_candidates: list[str] = []
    for attempt in _replay_attempts(tuning_payload):
        trajectory = attempt.get("frozen_step_trajectory_stage")
        if isinstance(trajectory, Mapping) and trajectory.get("trajectory_hmc_adapter_signature"):
            trajectory_candidates.append(str(trajectory["trajectory_hmc_adapter_signature"]))
        fixed_mass = attempt.get("fixed_mass_step_stage")
        if isinstance(fixed_mass, Mapping) and fixed_mass.get("ladder_hmc_adapter_signature"):
            fallback_candidates.append(str(fixed_mass["ladder_hmc_adapter_signature"]))
        diagnostics = attempt.get("verification_diagnostics")
        if isinstance(diagnostics, Mapping):
            route = diagnostics.get("runner_route_summary")
            if isinstance(route, Mapping):
                for contract in route.get("distinct_static_runner_contracts", ()):
                    if not isinstance(contract, Mapping):
                        continue
                    static_payload = contract.get("static_contract_payload")
                    if isinstance(static_payload, Mapping) and static_payload.get(
                        "hmc_adapter_signature"
                    ):
                        fallback_candidates.append(str(static_payload["hmc_adapter_signature"]))
    return _single_replay_signature(
        trajectory_candidates or fallback_candidates,
        label="final HMC adapter signature",
    )


def _replay_attempts(tuning_payload: Mapping[str, Any]) -> tuple[Mapping[str, Any], ...]:
    loop = _required_mapping(tuning_payload, "tune_verify_repair_loop")
    attempts = loop.get("attempts")
    if not isinstance(attempts, Sequence) or isinstance(attempts, (str, bytes)):
        raise ValueError("retained frozen-kernel replay missing Phase 7 attempts")
    records = tuple(item for item in attempts if isinstance(item, Mapping))
    if not records:
        raise ValueError("retained frozen-kernel replay requires at least one attempt")
    passed = tuple(item for item in records if item.get("passed") is True)
    return passed if passed else records


def _single_replay_signature(candidates: Sequence[str], *, label: str) -> str:
    values = tuple(dict.fromkeys(str(item) for item in candidates if str(item)))
    if not values:
        raise ValueError(f"retained frozen-kernel replay missing {label}")
    if len(values) != 1:
        raise ValueError(f"retained frozen-kernel replay inconsistent {label}")
    return values[0]


def initialize_hmc_kernel_geometry(
    *,
    adapter: Any,
    initial_position: Any,
    config: HMCGeometryInitializationConfig | None = None,
    negative_hessian: Any | None = None,
    initial_covariance: Any | None = None,
    parameter_scales: Any | None = None,
) -> HMCGeometryInitializationResult:
    """Build an initial mass artifact and formula-derived epsilon/L.

    ``negative_hessian`` is interpreted as a local precision approximation
    ``-d2 log p(theta)`` in the same unconstrained coordinates as
    ``initial_position``.  This function is a geometry initializer only; it does
    not run HMC or adapt the kernel.
    """

    cfg = HMCGeometryInitializationConfig() if config is None else config
    if not isinstance(cfg, HMCGeometryInitializationConfig):
        raise TypeError("config must be HMCGeometryInitializationConfig")
    adapter_signature = stable_adapter_signature(adapter)
    position = _validate_position(initial_position)
    dimension = int(position.shape[0])
    hint = _select_geometry_hint(
        position=position,
        negative_hessian=negative_hessian,
        initial_covariance=initial_covariance,
        parameter_scales=parameter_scales,
        config=cfg,
    )
    mass_artifact = _build_mass_artifact(
        position=position,
        adapter_signature=adapter_signature,
        hint=hint,
        config=cfg,
    )
    omega = _curvature_frequencies(
        covariance=np.asarray(mass_artifact.covariance, dtype=float),
        precision=hint.precision_for_formula,
    )
    target_trajectory = _target_trajectory_length(omega)
    epsilon = _initial_step_size(omega, dimension=dimension, config=cfg)
    unclamped_l = int(np.ceil(target_trajectory / epsilon))
    leapfrogs = int(
        np.clip(unclamped_l, _GEOMETRY_MIN_LEAPFROG, _GEOMETRY_MAX_LEAPFROG)
    )
    mass_signature = _mass_artifact_signature(mass_artifact)
    return HMCGeometryInitializationResult(
        config=cfg,
        adapter_signature=adapter_signature,
        target_dimension=dimension,
        mass_artifact=mass_artifact,
        mass_artifact_signature=mass_signature,
        initial_step_size=epsilon,
        initial_num_leapfrog_steps=leapfrogs,
        unclamped_num_leapfrog_steps=unclamped_l,
        target_trajectory_length=target_trajectory,
        hint_report=hint.report,
        curvature_report=_curvature_report(omega),
        formula_report={
            "formula": "epsilon=min(c*d^(-1/4)/rms(omega), rho*2/max(omega)); L=ceil(tau/epsilon)",
            "geometry_scaling_c": cfg.geometry_scaling_c,
            "stability_guard": cfg.stability_guard,
            "target_trajectory_length": target_trajectory,
            "leapfrog_clamped": leapfrogs != unclamped_l,
            "internal_min_leapfrog": _GEOMETRY_MIN_LEAPFROG,
            "internal_max_leapfrog": _GEOMETRY_MAX_LEAPFROG,
        },
        seed_report={
            "root_seed": cfg.seed,
            "seed_owner": "BayesFilter",
            "geometry_seed": _derive_seed(cfg.seed, stage_index=0),
            "fresh_verification_seed_reserved": _derive_seed(cfg.seed, stage_index=5),
            "nonclaim": "geometry seed provenance only; no HMC run executed",
        },
    )


def run_hmc_bootstrap_screen(
    *,
    adapter: Any,
    geometry: HMCGeometryInitializationResult,
    config: HMCBootstrapScreenConfig | None = None,
    run_full_chain: RunFullChainFn = run_full_chain_tfp_hmc,
) -> HMCBootstrapScreenResult:
    """Run a short fixed-kernel screen and bounded epsilon repair.

    The caller supplies a model adapter and Phase 2 geometry artifact.  The
    screen itself runs in latent fixed-mass coordinates so the recorded mass
    artifact is the operational HMC geometry.  The returned artifact supports
    later tuning phases, but is not posterior convergence or sampler-readiness
    evidence.
    """

    cfg = HMCBootstrapScreenConfig() if config is None else config
    if not isinstance(cfg, HMCBootstrapScreenConfig):
        raise TypeError("config must be HMCBootstrapScreenConfig")
    if not isinstance(geometry, HMCGeometryInitializationResult):
        raise TypeError("geometry must be HMCGeometryInitializationResult")
    adapter_signature = stable_adapter_signature(adapter)
    if adapter_signature != geometry.adapter_signature:
        raise ValueError("bootstrap adapter signature must match geometry")
    geometry.mass_artifact.validate_for_adapter(
        adapter,
        expected_dim=geometry.target_dimension,
    )
    mass_signature = _mass_artifact_signature(geometry.mass_artifact)
    if mass_signature != geometry.mass_artifact_signature:
        raise ValueError("geometry mass artifact signature mismatch")
    target_scope = _resolve_bootstrap_target_scope(adapter, cfg)
    hmc_adapter = _build_bootstrap_fixed_mass_adapter(
        adapter=adapter,
        mass_artifact=geometry.mass_artifact,
        mass_signature=mass_signature,
        target_scope=target_scope,
    )
    hmc_adapter_signature = stable_adapter_signature(hmc_adapter)
    target_dimension = int(getattr(hmc_adapter, "parameter_dim", geometry.target_dimension))
    root_seed = cfg.seed
    geometry_seed = _seed_from_mapping(geometry.seed_report, "geometry_seed")
    rounds: list[HMCBootstrapRepairRound] = []
    step = float(geometry.initial_step_size)
    target_trajectory = float(geometry.target_trajectory_length)
    low_acceptance_step: float | None = None
    high_acceptance_step: float | None = None
    previous_clamp_direction: str | None = None
    final_status = "repair_budget_exhausted"
    selected_index: int | None = None
    runner_cache: dict[str, Any] = {}
    runner_contract_payloads: dict[str, Mapping[str, Any]] = {}
    runner_route_events: list[Mapping[str, Any]] = []
    single_use_build_count = 0
    injected_runner_call_count = 0
    reusable_runner_build_count = 0
    use_bootstrap_reusable_route = (
        run_full_chain is run_full_chain_tfp_hmc
        and cfg.chain_execution_mode == "tf_function"
    )

    for round_index in range(cfg.max_repairs + 1):
        leapfrog_payload = _bootstrap_leapfrog_payload(step, target_trajectory)
        screen_seed = _round_seed(root_seed, round_index)
        screen_config = _bootstrap_screen_config(
            cfg,
            seed=screen_seed,
            step=step,
            leapfrogs=leapfrog_payload["num_leapfrog_steps"],
            target_scope=target_scope,
        )
        diagnostics: Mapping[str, Any]
        screen_error: Exception | None = None
        route_event_recorded = False
        try:
            if use_bootstrap_reusable_route:
                contract_payload = _bootstrap_reusable_static_contract_payload(
                    screen_config,
                    hmc_adapter_signature=hmc_adapter_signature,
                    target_dimension=target_dimension,
                    mass_signature=mass_signature,
                )
                contract_hash = stable_config_hash(contract_payload)
                reusable_runner = runner_cache.get(contract_hash)
                runner_reused = reusable_runner is not None
                if reusable_runner is None:
                    reusable_runner = build_reusable_full_chain_tfp_hmc_runner(
                        hmc_adapter,
                        hmc_adapter.initial_position(),
                        screen_config,
                    )
                    runner_cache[contract_hash] = reusable_runner
                    runner_contract_payloads[contract_hash] = contract_payload
                    reusable_runner_build_count += 1
                run_result = reusable_runner.run(
                    current_state=hmc_adapter.initial_position(),
                    seed=screen_config.seed,
                    step_size=screen_config.step_size,
                )
                runner_route_events.append(
                    {
                        "round_index": round_index,
                        "route": "bootstrap_scoped_reusable_runner",
                        "static_contract_hash": contract_hash,
                        "runner_reused": runner_reused,
                        "used_single_use_runner": False,
                    }
                )
                route_event_recorded = True
            else:
                used_standard_single_use = run_full_chain is run_full_chain_tfp_hmc
                if used_standard_single_use:
                    single_use_build_count += 1
                else:
                    injected_runner_call_count += 1
                run_result = run_full_chain(
                    hmc_adapter,
                    hmc_adapter.initial_position(),
                    screen_config,
                )
                runner_route_events.append(
                    {
                        "round_index": round_index,
                        "route": "single_use_or_injected_runner",
                        "static_contract_hash": None,
                        "runner_reused": False,
                        "used_single_use_runner": used_standard_single_use,
                    }
                )
                route_event_recorded = True
            diagnostics = _bootstrap_diagnostics_payload(
                run_result,
                use_xla_requested=screen_config.use_xla,
                compile_chain_with_xla=screen_config.use_xla,
            )
        except Exception as exc:  # noqa: BLE001 - return fail-closed artifact.
            screen_error = exc
            if not route_event_recorded:
                runner_route_events.append(
                    {
                        "round_index": round_index,
                        "route": (
                            "bootstrap_scoped_reusable_runner"
                            if use_bootstrap_reusable_route
                            else "single_use_or_injected_runner"
                        ),
                        "static_contract_hash": None,
                        "runner_reused": False,
                        "used_single_use_runner": False,
                        "failed_before_route_completion": True,
                    }
                )
            diagnostics = _bootstrap_error_diagnostics(exc)
        (
            classification,
            diagnostic_role,
            hard_vetoes,
            repair_triggers,
        ) = _classify_bootstrap_screen(
            cfg,
            diagnostics=diagnostics,
            screen_error=screen_error,
        )
        repair_action: str | None = None
        if classification == "repair":
            acceptance = _scalar_or_none(diagnostics.get("acceptance_rate"))
            low_acceptance_step, high_acceptance_step = _bootstrap_update_repair_bracket(
                cfg,
                current_step=step,
                acceptance=acceptance,
                low_acceptance_step=low_acceptance_step,
                high_acceptance_step=high_acceptance_step,
            )
            repair_action = _bootstrap_repair_action(
                cfg,
                acceptance,
                low_acceptance_step=low_acceptance_step,
                high_acceptance_step=high_acceptance_step,
            )
            repair_triggers = repair_triggers + (repair_action,)
        round_result = HMCBootstrapRepairRound(
            round_index=round_index,
            seed=screen_seed,
            step_size=step,
            num_leapfrog_steps=int(leapfrog_payload["num_leapfrog_steps"]),
            unclamped_num_leapfrog_steps=int(
                leapfrog_payload["unclamped_num_leapfrog_steps"]
            ),
            target_trajectory_length=target_trajectory,
            leapfrog_clamped=bool(leapfrog_payload["leapfrog_clamped"]),
            clamp_direction=leapfrog_payload["clamp_direction"],
            classification=classification,
            diagnostic_role=diagnostic_role,
            screen_config_payload=screen_config.signature_payload(),
            diagnostics=diagnostics,
            repair_action=repair_action,
            hard_vetoes=hard_vetoes,
            repair_triggers=repair_triggers,
        )
        rounds.append(round_result)
        if classification == "passed":
            selected_index = round_index
            final_status = "passed"
            break
        if classification == "hard_veto":
            final_status = "hard_veto"
            break
        if classification != "repair":
            final_status = classification
            break
        current_clamp_direction = round_result.clamp_direction
        if (
            current_clamp_direction is not None
            and current_clamp_direction == previous_clamp_direction
        ):
            final_status = "blocked_repeated_leapfrog_cap_saturation"
            break
        previous_clamp_direction = current_clamp_direction
        if round_index >= cfg.max_repairs:
            final_status = "repair_budget_exhausted"
            break
        step = _repair_step_size(
            cfg,
            current_step=step,
            acceptance=acceptance,
            low_acceptance_step=low_acceptance_step,
            high_acceptance_step=high_acceptance_step,
        )

    selected_round = None if selected_index is None else rounds[selected_index]
    expected_selected_payload = (
        None
        if selected_round is None
        else _bootstrap_selected_kernel_payload(
            config=cfg,
            selected=selected_round,
            adapter_signature=adapter_signature,
            hmc_adapter_signature=hmc_adapter_signature,
            mass_artifact_signature=mass_signature,
            geometry_artifact_hash=geometry.artifact_hash,
            nonclaims=BOOTSTRAP_SCREEN_NONCLAIMS,
        )
    )
    expected_selected_hash = (
        None
        if expected_selected_payload is None
        else stable_config_hash(expected_selected_payload)
    )
    bootstrap_runner_route = {
        "active_route": (
            "bootstrap_scoped_reusable_runner"
            if use_bootstrap_reusable_route
            else "single_use_or_injected_runner"
        ),
        "semantic_source": "run_hmc_bootstrap_screen",
        "single_use_build_count_for_bootstrap_rounds": single_use_build_count,
        "injected_runner_call_count": injected_runner_call_count,
        "reusable_runner_build_count": reusable_runner_build_count,
        "distinct_static_runner_contract_count": len(runner_contract_payloads),
        "distinct_static_runner_contracts": tuple(
            {
                "static_contract_hash": contract_hash,
                "static_contract_payload": runner_contract_payloads[contract_hash],
            }
            for contract_hash in sorted(runner_contract_payloads)
        ),
        "bootstrap_round_count": len(rounds),
        "fallback_to_single_use_runner": (
            use_bootstrap_reusable_route and single_use_build_count > 0
        ),
        "fallback_status": (
            "none"
            if use_bootstrap_reusable_route and single_use_build_count == 0
            else "inactive_reusable_route"
        ),
        "round_route_events": tuple(runner_route_events),
        "selected_kernel_payload_hash": expected_selected_hash,
        "selected_kernel_preservation": {
            "checked": selected_round is not None,
            "semantic_source": "run_hmc_bootstrap_screen",
            "payload_hash": expected_selected_hash,
            "selected_round_index": selected_index,
            "preserved": selected_round is not None,
            "step_size": None if selected_round is None else selected_round.step_size,
            "num_leapfrog_steps": (
                None if selected_round is None else selected_round.num_leapfrog_steps
            ),
            "seed": None if selected_round is None else selected_round.seed,
            "screen_config_payload": (
                None if selected_round is None else selected_round.screen_config_payload
            ),
        },
        "dynamic_runner_inputs": ("current_state", "seed", "step_size"),
        "dynamic_inputs_preserve_round_semantics": True,
    }

    return HMCBootstrapScreenResult(
        config=cfg,
        geometry_artifact_hash=geometry.artifact_hash,
        adapter_signature=adapter_signature,
        hmc_adapter_signature=hmc_adapter_signature,
        mass_artifact_signature=mass_signature,
        target_dimension=target_dimension,
        rounds=tuple(rounds),
        selected_round_index=selected_index,
        final_status=final_status,
        seed_report={
            "geometry_root_seed": geometry.seed_report.get("root_seed"),
            "geometry_seed": geometry_seed,
            "bootstrap_root_seed": root_seed,
            "bootstrap_stage_seed": _derive_seed(root_seed, stage_index=0),
            "screen_round_seeds": tuple(round_result.seed for round_result in rounds),
            "seed_owner": "BayesFilter",
            "geometry_seed_distinct_from_bootstrap_seed": geometry_seed != root_seed,
        },
        diagnostic_roles={
            "acceptance_band": "bootstrap_promotion_only",
            "repair_band": "bootstrap_repair_trigger",
            "finite_samples": "hard_veto",
            "log_accept_ratio_finite": "hard_veto",
            "target_log_prob_finite": "hard_veto",
            "adapter_signature_match": "hard_veto",
            "mass_artifact_validity": "hard_veto",
            "repeated_leapfrog_cap_saturation": "phase_blocker_handoff",
            "runtime": "explanatory_diagnostic",
        },
        bootstrap_runner_route=bootstrap_runner_route,
    )


def run_hmc_windowed_mass_stage(
    *,
    adapter: Any,
    geometry: HMCGeometryInitializationResult,
    bootstrap: HMCBootstrapScreenResult,
    config: HMCWindowedMassStageConfig | None = None,
    run_full_chain: RunFullChainFn = run_full_chain_tfp_hmc,
    _attempt_budget_policy: "_HMCAttemptBudgetPolicy" | None = None,
    _attempt_state: "_HMCPhaseAttemptState" | None = None,
    _progress_callback: LoopProgressCallback | None = None,
    _attempt_index: int | None = None,
) -> HMCWindowedMassStageResult:
    """Capture retained diagnostic draws and run windowed mass adaptation.

    The retained samples from the fixed-kernel run are adaptation inputs only.
    They are not posterior samples and cannot establish convergence.
    """

    cfg = HMCWindowedMassStageConfig() if config is None else config
    if not isinstance(cfg, HMCWindowedMassStageConfig):
        raise TypeError("config must be HMCWindowedMassStageConfig")
    if not isinstance(geometry, HMCGeometryInitializationResult):
        raise TypeError("geometry must be HMCGeometryInitializationResult")
    if not isinstance(bootstrap, HMCBootstrapScreenResult):
        raise TypeError("bootstrap must be HMCBootstrapScreenResult")
    _validate_windowed_stage_inputs(adapter=adapter, geometry=geometry, bootstrap=bootstrap)
    target_scope = _resolve_windowed_stage_target_scope(adapter, cfg)
    mass_signature = _mass_artifact_signature(geometry.mass_artifact)
    hmc_adapter = _build_bootstrap_fixed_mass_adapter(
        adapter=adapter,
        mass_artifact=geometry.mass_artifact,
        mass_signature=mass_signature,
        target_scope=target_scope,
        nonclaims=WINDOWED_MASS_STAGE_NONCLAIMS,
    )
    hmc_adapter_signature = stable_adapter_signature(hmc_adapter)
    if hmc_adapter_signature != bootstrap.hmc_adapter_signature:
        raise ValueError("windowed stage HMC adapter signature must match bootstrap")
    stage_mass_artifact = _windowed_stage_initial_mass_artifact(
        adapter_signature=hmc_adapter_signature,
        target_dimension=geometry.target_dimension,
        attempt_state=_attempt_state,
    )
    stage_mass_signature = _mass_artifact_signature(stage_mass_artifact)
    selected = bootstrap.selected_kernel_payload
    if selected is None:
        raise ValueError("windowed stage requires selected bootstrap kernel payload")
    selected_hash = bootstrap.selected_kernel_hash
    if selected_hash is None:
        raise ValueError("windowed stage requires selected bootstrap kernel hash")

    windowed_config = _windowed_mass_stage_internal_config(_attempt_budget_policy)
    draw_capture_policy = _windowed_stage_draw_capture_policy(windowed_config)
    stage_seed = _derive_seed(cfg.seed, stage_index=0)
    diagnostic_config = _windowed_stage_diagnostic_run_config(
        cfg,
        windowed_config=windowed_config,
        selected_kernel=selected,
        seed=stage_seed,
        target_scope=target_scope,
    )
    progress_attempt_index = (
        int(_attempt_budget_policy.attempt_index)
        if _attempt_index is None and _attempt_budget_policy is not None
        else None if _attempt_index is None else int(_attempt_index)
    )
    use_reusable_runner = (
        run_full_chain is run_full_chain_tfp_hmc
        and cfg.chain_execution_mode == "tf_function"
    )
    route_category = "reusable_runner" if use_reusable_runner else "injected_runner"

    diagnostics: Mapping[str, Any]
    run_error: Exception | None = None
    diagnostic_run_config_payload: Mapping[str, Any] | None = diagnostic_config.signature_payload()
    windowed_result: WindowedMassAdaptationResult | None = None
    try:
        _emit_windowed_mass_progress(
            _progress_callback,
            "windowed_mass_runner_build_start",
            attempt_index=progress_attempt_index,
            route_category=route_category,
            started=True,
            elapsed_s=0.0,
            started_perf_counter_s=time.perf_counter(),
        )
        runner_build_start = time.perf_counter()
        runner_build_s = 0.0
        if use_reusable_runner:
            reusable_runner = build_reusable_full_chain_tfp_hmc_runner(
                hmc_adapter,
                hmc_adapter.initial_position(),
                diagnostic_config,
            )
        runner_build_s = time.perf_counter() - runner_build_start
        _emit_windowed_mass_progress(
            _progress_callback,
            "windowed_mass_runner_build_complete",
            attempt_index=progress_attempt_index,
            route_category=route_category,
            completed=True,
            elapsed_s=runner_build_s,
        )
        _emit_windowed_mass_progress(
            _progress_callback,
            "windowed_mass_runner_execute_start",
            attempt_index=progress_attempt_index,
            route_category=route_category,
            started=True,
            elapsed_s=0.0,
            started_perf_counter_s=time.perf_counter(),
        )
        runner_execute_start = time.perf_counter()
        if use_reusable_runner:
            run_result = reusable_runner.run(
                current_state=hmc_adapter.initial_position(),
                seed=diagnostic_config.seed,
                step_size=diagnostic_config.step_size,
            )
        else:
            run_result = run_full_chain(
                hmc_adapter,
                hmc_adapter.initial_position(),
                diagnostic_config,
            )
        runner_execute_s = time.perf_counter() - runner_execute_start
        _emit_windowed_mass_progress(
            _progress_callback,
            "windowed_mass_runner_execute_complete",
            attempt_index=progress_attempt_index,
            route_category=route_category,
            completed=True,
            elapsed_s=runner_execute_s,
        )
        _emit_windowed_mass_progress(
            _progress_callback,
            "windowed_mass_capture_start",
            attempt_index=progress_attempt_index,
            route_category=route_category,
            started=True,
            elapsed_s=0.0,
            started_perf_counter_s=time.perf_counter(),
        )
        capture_start = time.perf_counter()
        capture = _windowed_stage_capture_payload(
            run_result,
            expected_steps=windowed_config.warmup_steps,
            target_dimension=geometry.target_dimension,
        )
        capture_s = time.perf_counter() - capture_start
        capture = _with_windowed_stage_timing_metadata(
            capture,
            runner_build_s=runner_build_s,
            runner_execute_s=runner_execute_s,
            capture_s=capture_s,
            route_category=route_category,
        )
        _emit_windowed_mass_progress(
            _progress_callback,
            "windowed_mass_capture_complete",
            attempt_index=progress_attempt_index,
            route_category=route_category,
            completed=True,
            elapsed_s=capture_s,
        )
    except Exception as exc:  # noqa: BLE001 - return fail-closed artifact.
        run_error = exc
        capture = _windowed_stage_error_capture(exc)
    hard_vetoes = list(
        _classify_windowed_stage_capture(
            capture,
            run_error=run_error,
        )
    )
    if not hard_vetoes:
        _emit_windowed_mass_progress(
            _progress_callback,
            "windowed_mass_semantic_diagnostic_start",
            attempt_index=progress_attempt_index,
            route_category=route_category,
            started=True,
            elapsed_s=0.0,
            started_perf_counter_s=time.perf_counter(),
        )
        semantic_diagnostic_start = time.perf_counter()
        try:
            policy = HMCTuningPolicy.windowed_mass_adaptation(
                num_adaptation_steps=windowed_config.warmup_steps,
                target_accept_prob=cfg.target_accept_prob,
                source=cfg.source,
            )
            windowed_result = run_windowed_mass_adaptation_diagnostic(
                policy,
                config=windowed_config,
                initial_mass_artifact=stage_mass_artifact,
                warmup_draws=capture["warmup_draws"],
                initial_step_size=float(selected["step_size"]),
                acceptance_trace=capture["acceptance_trace"],
                expected_adapter_signature=hmc_adapter_signature,
                target_failure_classification={
                    "classification": "tuning_diagnostic_passed_not_convergence",
                    "diagnostic_role": "diagnostic_only",
                    "nonclaims": WINDOWED_MASS_STAGE_NONCLAIMS,
                },
            )
            if not windowed_result.passed:
                hard_vetoes.append("windowed_mass_diagnostic_hard_veto")
        except Exception as exc:  # noqa: BLE001 - return fail-closed artifact.
            hard_vetoes.append("windowed_mass_diagnostic_error")
            capture = {
                **dict(capture),
                "windowed_mass_error_type": type(exc).__name__,
                "windowed_mass_error_message": str(exc),
            }
        _emit_windowed_mass_progress(
            _progress_callback,
            "windowed_mass_semantic_diagnostic_complete",
            attempt_index=progress_attempt_index,
            route_category=route_category,
            completed=True,
            elapsed_s=time.perf_counter() - semantic_diagnostic_start,
        )
    final_status = "passed" if not hard_vetoes else "hard_veto"
    diagnostic_role = (
        "windowed_mass_stage_handoff_only" if final_status == "passed" else "hard_veto"
    )
    diagnostics = _windowed_stage_diagnostics(
        capture,
        windowed_result=windowed_result,
        hard_vetoes=tuple(hard_vetoes),
    )
    return HMCWindowedMassStageResult(
        config=cfg,
        geometry_artifact_hash=geometry.artifact_hash,
        bootstrap_artifact_hash=bootstrap.artifact_hash,
        selected_bootstrap_kernel_hash=selected_hash,
        adapter_signature=geometry.adapter_signature,
        hmc_adapter_signature=hmc_adapter_signature,
        initial_mass_artifact_signature=stage_mass_signature,
        target_dimension=geometry.target_dimension,
        final_status=final_status,
        diagnostic_role=diagnostic_role,
        hard_vetoes=tuple(hard_vetoes),
        diagnostics=diagnostics,
        draw_capture_policy=draw_capture_policy,
        warmup_draw_provenance=_warmup_draw_provenance(capture, draw_capture_policy),
        acceptance_telemetry_provenance=_acceptance_telemetry_provenance(capture),
        diagnostic_run_config_payload=diagnostic_run_config_payload,
        windowed_config_payload=windowed_config.payload(),
        windowed_mass_result=windowed_result,
        seed_report={
            "geometry_root_seed": geometry.seed_report.get("root_seed"),
            "bootstrap_root_seed": bootstrap.seed_report.get("bootstrap_root_seed"),
            "windowed_stage_root_seed": cfg.seed,
            "windowed_stage_seed": stage_seed,
            "seed_owner": "BayesFilter",
        },
        diagnostic_roles={
            "retained_samples": "adaptation_input_only",
            "acceptance_trace": "hard_veto_and_step_handoff_input",
            "log_accept_ratio": "hard_veto",
            "target_log_prob": "hard_veto",
            "runtime": "hard_veto",
            "windowed_mass_artifact": "phase5_handoff_only",
        },
    )


def run_hmc_fixed_mass_step_stage(
    *,
    adapter: Any,
    geometry: HMCGeometryInitializationResult,
    bootstrap: HMCBootstrapScreenResult,
    windowed_stage: HMCWindowedMassStageResult,
    config: HMCFixedMassStepStageConfig | None = None,
    screen_callback: FixedMassScreenCallback | None = None,
    run_full_chain: RunFullChainFn = run_full_chain_tfp_hmc,
    _attempt_budget_policy: "_HMCAttemptBudgetPolicy" | None = None,
    _attempt_state: "_HMCPhaseAttemptState" | None = None,
    _progress_callback: LoopProgressCallback | None = None,
    _attempt_index: int | None = None,
) -> HMCFixedMassStepStageResult:
    """Run Phase 5 fixed-mass step tuning from a passed Phase 4 handoff.

    Phase 5 freezes the Phase 4 adapted mass and tunes only step size through
    the existing BayesFilter fixed-mass budget ladder. The leapfrog count is
    held fixed until Phase 6 trajectory tuning.
    """

    cfg = HMCFixedMassStepStageConfig() if config is None else config
    if not isinstance(cfg, HMCFixedMassStepStageConfig):
        raise TypeError("config must be HMCFixedMassStepStageConfig")
    if not isinstance(geometry, HMCGeometryInitializationResult):
        raise TypeError("geometry must be HMCGeometryInitializationResult")
    if not isinstance(bootstrap, HMCBootstrapScreenResult):
        raise TypeError("bootstrap must be HMCBootstrapScreenResult")
    if not isinstance(windowed_stage, HMCWindowedMassStageResult):
        raise TypeError("windowed_stage must be HMCWindowedMassStageResult")
    _validate_fixed_mass_step_stage_inputs(
        adapter=adapter,
        geometry=geometry,
        bootstrap=bootstrap,
        windowed_stage=windowed_stage,
        config=cfg,
    )
    target_scope = _resolve_fixed_mass_step_stage_target_scope(adapter, cfg)
    selected_kernel = _selected_bootstrap_kernel_from_windowed_stage(
        windowed_stage,
        bootstrap=bootstrap,
    )
    adapted_mass = _phase4_adapted_mass_artifact(windowed_stage)
    initial_step = _fixed_mass_step_initial_step(
        windowed_stage,
        attempt_state=_attempt_state,
    )
    fixed_leapfrog = int(selected_kernel["num_leapfrog_steps"])
    budget_config = _fixed_mass_step_stage_ladder_config(
        cfg,
        initial_step=initial_step,
        num_leapfrog_steps=fixed_leapfrog,
        target_scope=target_scope,
        attempt_budget_policy=_attempt_budget_policy,
    )
    ladder_result: FixedMassHMCTuningBudgetLadderResult | None = None
    run_error: Exception | None = None
    hard_vetoes: list[str] = []
    before_signature = _mass_artifact_signature(adapted_mass)
    progress_attempt_index = (
        int(_attempt_budget_policy.attempt_index)
        if _attempt_index is None and _attempt_budget_policy is not None
        else None if _attempt_index is None else int(_attempt_index)
    )

    def forward_ladder_progress(stage: str, payload: Mapping[str, Any]) -> None:
        _emit_phase7_progress(
            _progress_callback,
            stage,
            attempt_index=0 if progress_attempt_index is None else progress_attempt_index,
            budget_policy=_attempt_budget_policy,
            started=bool(payload.get("started")),
            completed=bool(payload.get("completed")),
            extra=_budget_ladder_progress_extra(payload),
        )

    try:
        ladder_result = run_fixed_mass_hmc_tuning_budget_ladder(
            adapter=_phase4_latent_adapter_for_step_stage(
                adapter=adapter,
                geometry=geometry,
                windowed_stage=windowed_stage,
                target_scope=target_scope,
            ),
            mass_artifact=adapted_mass,
            initial_state_factory=_fixed_mass_step_initial_state_factory(
                adapted_mass.dimension
            ),
            config=budget_config,
            screen_callback=screen_callback,
            progress_callback=forward_ladder_progress,
            run_full_chain=run_full_chain,
        )
    except Exception as exc:  # noqa: BLE001 - return fail-closed artifact.
        run_error = exc
        hard_vetoes.append("fixed_mass_step_ladder_error")
    after_signature = _mass_artifact_signature(adapted_mass)
    frozen_mass_invariant = _fixed_mass_step_frozen_mass_invariant(
        before_signature,
        after_signature,
    )
    if not frozen_mass_invariant["passed"]:
        hard_vetoes.append("fixed_mass_step_mass_signature_mutated")
    diagnostics = _fixed_mass_step_stage_diagnostics(
        ladder_result,
        run_error=run_error,
        hard_vetoes=tuple(hard_vetoes),
    )
    hard_vetoes.extend(diagnostics.get("hard_vetoes_from_ladder", ()))
    hard_vetoes = list(dict.fromkeys(str(item) for item in hard_vetoes))
    continuation_vetoes = tuple(
        str(item) for item in diagnostics.get("continuation_vetoes_from_ladder", ())
    )
    repair_triggers = tuple(
        str(item) for item in diagnostics.get("repair_triggers_from_ladder", ())
    )
    if hard_vetoes:
        final_status = "hard_veto"
    elif continuation_vetoes:
        final_status = "hard_veto"
        hard_vetoes = list(
            dict.fromkeys([*hard_vetoes, "fixed_mass_step_continuation_veto"])
        )
    elif ladder_result is not None and ladder_result.passed:
        final_status = "passed"
    else:
        final_status = "repair_or_retry"
    diagnostic_role = (
        "fixed_mass_step_stage_handoff_only"
        if final_status == "passed"
        else ("repair_trigger" if final_status == "repair_or_retry" else "hard_veto")
    )
    selected_payload = None
    selected_hash = None
    repair_payload = None
    repair_hash = None
    if ladder_result is not None and ladder_result.passed:
        selected_payload = ladder_result.selected_config_payload
        selected_hash = ladder_result.selected_config_hash
    elif ladder_result is not None and final_status == "repair_or_retry":
        repair_payload = ladder_result.repair_config_payload
        repair_hash = ladder_result.repair_config_hash
    return HMCFixedMassStepStageResult(
        config=cfg,
        windowed_stage_artifact_hash=windowed_stage.artifact_hash,
        selected_bootstrap_kernel_hash=windowed_stage.selected_bootstrap_kernel_hash,
        adapter_signature=windowed_stage.adapter_signature,
        phase4_hmc_adapter_signature=windowed_stage.hmc_adapter_signature,
        ladder_adapter_signature=(
            "fixed_mass_step_ladder_unavailable"
            if ladder_result is None
            else ladder_result.adapter_signature
        ),
        ladder_hmc_adapter_signature=(
            "fixed_mass_step_ladder_hmc_unavailable"
            if ladder_result is None
            else ladder_result.hmc_adapter_signature
        ),
        adapted_mass_artifact_payload=adapted_mass.to_payload(include_arrays=True),
        adapted_mass_artifact_signature=before_signature,
        initial_step_size=initial_step,
        fixed_num_leapfrog_steps=fixed_leapfrog,
        target_dimension=windowed_stage.target_dimension,
        final_status=final_status,
        diagnostic_role=diagnostic_role,
        hard_vetoes=tuple(hard_vetoes),
        repair_triggers=repair_triggers,
        diagnostics={
            **diagnostics,
            "hard_vetoes": tuple(hard_vetoes),
            "continuation_vetoes": continuation_vetoes,
            "repair_triggers": repair_triggers,
        },
        budget_ladder_config_payload=budget_config.payload(),
        budget_ladder_result=ladder_result,
        selected_step_payload=selected_payload,
        selected_step_hash=selected_hash,
        repair_step_payload=repair_payload,
        repair_step_hash=repair_hash,
        frozen_mass_invariant=frozen_mass_invariant,
        seed_report={
            "windowed_stage_seed": windowed_stage.seed_report.get("windowed_stage_seed"),
            "fixed_mass_stage_root_seed": cfg.seed,
            "fixed_mass_tune_seed_base": _derive_seed(cfg.seed, stage_index=0),
            "fixed_mass_screen_seed_base": _derive_seed(cfg.seed, stage_index=1),
            "seed_owner": "BayesFilter",
        },
        diagnostic_roles={
            "frozen_mass_invariant": "hard_veto",
            "fresh_fixed_kernel_screen": "step_handoff_promotion_only",
            "tune_acceptance": "tuning_diagnostic_only",
            "screen_acceptance": "promotion_or_repair_or_hard_veto",
            "callback_hard_veto": "hard_veto",
            "callback_continuation_veto": "continuation_veto",
            "callback_promotion_veto": "repair_trigger",
            "runtime": "explanatory_or_hard_veto_when_missing",
        },
    )


def run_hmc_frozen_step_trajectory_stage(
    *,
    adapter: Any,
    geometry: HMCGeometryInitializationResult,
    bootstrap: HMCBootstrapScreenResult,
    windowed_stage: HMCWindowedMassStageResult,
    fixed_mass_step_stage: HMCFixedMassStepStageResult,
    config: HMCFrozenStepTrajectoryStageConfig | None = None,
    screen_callback: TrajectoryScreenCallback | None = None,
    run_full_chain: RunFullChainFn = run_full_chain_tfp_hmc,
    _attempt_budget_policy: "_HMCAttemptBudgetPolicy" | None = None,
    _attempt_state: "_HMCPhaseAttemptState" | None = None,
    _progress_callback: LoopProgressCallback | None = None,
    _attempt_index: int | None = None,
) -> HMCFrozenStepTrajectoryStageResult:
    """Run Phase 6 frozen-step trajectory tuning from a passed Phase 5 handoff.

    Phase 6 freezes the Phase 4 adapted mass and Phase 5 selected step, then
    screens internally generated candidate leapfrog counts with no adaptation.
    It is a trajectory handoff for the later tune-verify-repair loop, not final
    verification or posterior evidence.
    """

    cfg = HMCFrozenStepTrajectoryStageConfig() if config is None else config
    if not isinstance(cfg, HMCFrozenStepTrajectoryStageConfig):
        raise TypeError("config must be HMCFrozenStepTrajectoryStageConfig")
    if not isinstance(geometry, HMCGeometryInitializationResult):
        raise TypeError("geometry must be HMCGeometryInitializationResult")
    if not isinstance(bootstrap, HMCBootstrapScreenResult):
        raise TypeError("bootstrap must be HMCBootstrapScreenResult")
    if not isinstance(windowed_stage, HMCWindowedMassStageResult):
        raise TypeError("windowed_stage must be HMCWindowedMassStageResult")
    if not isinstance(fixed_mass_step_stage, HMCFixedMassStepStageResult):
        raise TypeError("fixed_mass_step_stage must be HMCFixedMassStepStageResult")
    _validate_frozen_step_trajectory_stage_inputs(
        adapter=adapter,
        geometry=geometry,
        bootstrap=bootstrap,
        windowed_stage=windowed_stage,
        fixed_mass_step_stage=fixed_mass_step_stage,
        config=cfg,
    )
    target_scope = _resolve_frozen_step_trajectory_stage_target_scope(adapter, cfg)
    adapted_mass = _phase4_adapted_mass_artifact(windowed_stage)
    frozen_step = _required_selected_step_size(fixed_mass_step_stage)
    fixed_bootstrap_l = int(fixed_mass_step_stage.fixed_num_leapfrog_steps)
    phase4_adapter = _phase4_latent_adapter_for_step_stage(
        adapter=adapter,
        geometry=geometry,
        windowed_stage=windowed_stage,
        target_scope=target_scope,
    )
    before_mass_signature = _mass_artifact_signature(adapted_mass)
    trajectory_adapter = _build_fixed_mass_hmc_adapter(
        adapter=phase4_adapter,
        mass_artifact=adapted_mass,
        mass_signature=before_mass_signature,
        target_scope=target_scope,
    )
    trajectory_hmc_signature = stable_adapter_signature(trajectory_adapter)
    if trajectory_hmc_signature != fixed_mass_step_stage.ladder_hmc_adapter_signature:
        raise ValueError("Phase 6 trajectory HMC adapter signature mismatch")
    candidate_generation = _frozen_step_trajectory_candidate_generation(
        geometry=geometry,
        selected_step_size=frozen_step,
        fixed_bootstrap_l=fixed_bootstrap_l,
        attempt_state=_attempt_state,
    )
    candidates = tuple(int(item) for item in candidate_generation["candidate_l_values"])
    candidate_results: list[Mapping[str, Any]] = []
    stage_hard_vetoes: list[str] = []
    stage_repair_triggers: list[str] = []
    run_error: Exception | None = None
    use_reusable_route = (
        run_full_chain is run_full_chain_tfp_hmc
        and cfg.chain_execution_mode == "tf_function"
    )
    runner_cache: dict[str, Any] = {}
    runner_contract_payloads: dict[str, Mapping[str, Any]] = {}
    runner_route_events: list[Mapping[str, Any]] = []
    candidate_elapsed_s: list[float] = []
    stage_start = time.perf_counter()
    soft_deadline_closeout: Mapping[str, Any] | None = None
    progress_attempt_index = (
        int(_attempt_budget_policy.attempt_index)
        if _attempt_index is None and _attempt_budget_policy is not None
        else None if _attempt_index is None else int(_attempt_index)
    )

    for candidate_index, leapfrog_count in enumerate(candidates):
        screen_seed = _round_seed(cfg.seed, candidate_index)
        screen_config = _frozen_step_trajectory_screen_config(
            cfg,
            seed=screen_seed,
            step=frozen_step,
            leapfrogs=leapfrog_count,
            target_scope=target_scope,
            attempt_budget_policy=_attempt_budget_policy,
        )
        soft_deadline_veto = _phase6_next_candidate_soft_deadline_veto(
            stage_start_perf_counter_s=stage_start,
            timeout_budget_s=cfg.public_timeout_budget_s,
            public_timeout_started_perf_counter_s=cfg.public_timeout_started_perf_counter_s,
            completed_elapsed_s=tuple(candidate_elapsed_s),
        )
        if soft_deadline_veto is not None:
            soft_deadline_closeout = {
                **soft_deadline_veto,
                "candidate_index": int(candidate_index),
                "candidate_count": len(candidates),
                "completed_candidate_count": len(candidate_results),
                "progress_only": True,
                "public_closeout_artifact_expected": True,
                "reason": "phase6_public_timeout_soft_deadline_before_next_candidate",
            }
            _emit_phase7_progress(
                _progress_callback,
                "trajectory_candidate_soft_deadline_closeout",
                attempt_index=0 if progress_attempt_index is None else progress_attempt_index,
                budget_policy=_attempt_budget_policy,
                completed=True,
                extra=_trajectory_candidate_progress_extra(
                    stage="trajectory_candidate_soft_deadline_closeout",
                    candidate_index=candidate_index,
                    candidate_count=len(candidates),
                    completed_candidate_count=len(candidate_results),
                    config=screen_config,
                    runner_event=runner_route_events[-1] if runner_route_events else None,
                    soft_deadline_payload=soft_deadline_closeout,
                ),
            )
            stage_hard_vetoes.append("phase6_public_timeout_soft_deadline")
            stage_repair_triggers.append(
                "phase6_public_timeout_soft_deadline_before_next_candidate"
            )
            break
        screen_result: FullChainHMCRunResult | None = None
        screen_error: Exception | None = None
        try:
            _emit_phase7_progress(
                _progress_callback,
                "trajectory_candidate_call_start",
                attempt_index=0 if progress_attempt_index is None else progress_attempt_index,
                budget_policy=_attempt_budget_policy,
                started=True,
                extra=_trajectory_candidate_progress_extra(
                    stage="trajectory_candidate_call_start",
                    candidate_index=candidate_index,
                    candidate_count=len(candidates),
                    completed_candidate_count=len(candidate_results),
                    config=screen_config,
                    runner_event=None,
                    elapsed_s=0.0,
                    started_perf_counter_s=time.perf_counter(),
                    soft_deadline_payload=_phase6_soft_deadline_state(
                        stage_start_perf_counter_s=stage_start,
                        timeout_budget_s=cfg.public_timeout_budget_s,
                        public_timeout_started_perf_counter_s=cfg.public_timeout_started_perf_counter_s,
                    ),
                ),
            )
            candidate_start = time.perf_counter()
            screen_result = _run_kernel_stage_with_optional_reusable_route(
                run_full_chain=run_full_chain,
                runner_cache=runner_cache,
                runner_contract_payloads=runner_contract_payloads,
                route_events=runner_route_events,
                route_name="frozen_step_trajectory_scoped_reusable_runner",
                route_scope="frozen_step_trajectory_candidate_screen",
                adapter=trajectory_adapter,
                initial_state=np.zeros(adapted_mass.dimension, dtype=float),
                config=screen_config,
                hmc_adapter_signature=trajectory_hmc_signature,
                target_dimension=windowed_stage.target_dimension,
                mass_signature=before_mass_signature,
                event_payload={
                    "candidate_index": candidate_index,
                    "num_leapfrog_steps": int(leapfrog_count),
                    "step_size": frozen_step,
                },
            )
            candidate_elapsed = time.perf_counter() - candidate_start
            candidate_elapsed_s.append(candidate_elapsed)
            _emit_phase7_progress(
                _progress_callback,
                "trajectory_candidate_call_complete",
                attempt_index=0 if progress_attempt_index is None else progress_attempt_index,
                budget_policy=_attempt_budget_policy,
                completed=True,
                extra=_trajectory_candidate_progress_extra(
                    stage="trajectory_candidate_call_complete",
                    candidate_index=candidate_index,
                    candidate_count=len(candidates),
                    completed_candidate_count=len(candidate_results) + 1,
                    config=screen_config,
                    runner_event=runner_route_events[-1] if runner_route_events else None,
                    elapsed_s=candidate_elapsed,
                    soft_deadline_payload=_phase6_soft_deadline_state(
                        stage_start_perf_counter_s=stage_start,
                        timeout_budget_s=cfg.public_timeout_budget_s,
                        public_timeout_started_perf_counter_s=cfg.public_timeout_started_perf_counter_s,
                    ),
                ),
            )
            diagnostics = _frozen_step_trajectory_diagnostics_payload(screen_result)
        except Exception as exc:  # noqa: BLE001 - return fail-closed artifact.
            screen_error = exc
            run_error = exc
            _emit_phase7_progress(
                _progress_callback,
                "trajectory_candidate_call_error",
                attempt_index=0 if progress_attempt_index is None else progress_attempt_index,
                budget_policy=_attempt_budget_policy,
                completed=True,
                extra=_trajectory_candidate_progress_extra(
                    stage="trajectory_candidate_call_error",
                    candidate_index=candidate_index,
                    candidate_count=len(candidates),
                    completed_candidate_count=len(candidate_results),
                    config=screen_config,
                    runner_event=runner_route_events[-1] if runner_route_events else None,
                    error_type=type(exc).__name__,
                    soft_deadline_payload=_phase6_soft_deadline_state(
                        stage_start_perf_counter_s=stage_start,
                        timeout_budget_s=cfg.public_timeout_budget_s,
                        public_timeout_started_perf_counter_s=cfg.public_timeout_started_perf_counter_s,
                    ),
                ),
            )
            diagnostics = _frozen_step_trajectory_error_diagnostics(exc)
        callback_result = _call_trajectory_screen_callback(
            screen_callback,
            round_payload={
                "candidate_index": candidate_index,
                "num_leapfrog_steps": int(leapfrog_count),
                "trajectory_length": float(frozen_step) * int(leapfrog_count),
                "step_size": frozen_step,
                "screen_seed": screen_seed,
                "screen_config_payload": screen_config.signature_payload(),
                "adapter_signature": stable_adapter_signature(phase4_adapter),
                "hmc_adapter_signature": trajectory_hmc_signature,
                "mass_artifact_signature": before_mass_signature,
                "sample_space": "phase4_latent_position",
                "hmc_sample_space": "adapted_mass_latent",
            },
            samples=None
            if screen_result is None
            else trajectory_adapter.latent_to_position(screen_result.samples),
            diagnostics=diagnostics,
        )
        (
            classification,
            diagnostic_role,
            hard_vetoes,
            continuation_vetoes,
            promotion_vetoes,
            repair_triggers,
        ) = _classify_frozen_step_trajectory_candidate(
            cfg,
            diagnostics=diagnostics,
            screen_error=screen_error,
            callback_result=callback_result,
        )
        candidate_payload = {
            "candidate_index": candidate_index,
            "seed": screen_seed,
            "step_size": frozen_step,
            "num_leapfrog_steps": int(leapfrog_count),
            "trajectory_length": float(frozen_step) * int(leapfrog_count),
            "target_trajectory_length": geometry.target_trajectory_length,
            "target_trajectory_distance": abs(
                float(frozen_step) * int(leapfrog_count)
                - float(geometry.target_trajectory_length)
            ),
            "classification": classification,
            "diagnostic_role": diagnostic_role,
            "screen_config_payload": screen_config.signature_payload(),
            "diagnostics": diagnostics,
            "callback_result": callback_result.payload(),
            "hard_vetoes": hard_vetoes,
            "continuation_vetoes": continuation_vetoes,
            "promotion_vetoes": promotion_vetoes,
            "repair_triggers": repair_triggers,
            "runtime_path": "run_full_chain_tfp_hmc_or_injected_run_full_chain_hook",
            "toy_fixed_trajectory_diagnostic_used": False,
            "no_adaptation": True,
            "candidate_elapsed_s": candidate_elapsed_s[-1]
            if candidate_elapsed_s
            else None,
        }
        if runner_route_events:
            candidate_payload["runner_route_event"] = runner_route_events[-1]
        candidate_results.append(candidate_payload)
        stage_hard_vetoes.extend(hard_vetoes)
        if continuation_vetoes:
            stage_hard_vetoes.append("frozen_step_trajectory_continuation_veto")
            stage_hard_vetoes.extend(continuation_vetoes)
        stage_repair_triggers.extend(repair_triggers)
        if hard_vetoes or continuation_vetoes:
            break

    stage_hard_vetoes = list(dict.fromkeys(str(item) for item in stage_hard_vetoes))
    stage_repair_triggers = list(
        dict.fromkeys(str(item) for item in stage_repair_triggers)
    )
    selected_index = None
    selected_payload = None
    selected_hash = None
    if stage_hard_vetoes:
        final_status = "hard_veto"
    else:
        selected_index = _select_frozen_step_trajectory_candidate(
            tuple(candidate_results),
            config=cfg,
            target_trajectory=geometry.target_trajectory_length,
        )
        if selected_index is None:
            final_status = "repair_or_retry"
            if not stage_repair_triggers:
                stage_repair_triggers.append("no_candidate_in_closed_acceptance_band")
        else:
            final_status = "passed"
            selected_payload = _frozen_step_trajectory_selected_payload(
                config=cfg,
                candidate=candidate_results[selected_index],
                selected_step_hash=str(fixed_mass_step_stage.selected_step_hash),
                selected_bootstrap_kernel_hash=fixed_mass_step_stage.selected_bootstrap_kernel_hash,
                fixed_mass_step_stage_artifact_hash=fixed_mass_step_stage.artifact_hash,
                adapted_mass_artifact_signature=before_mass_signature,
                phase4_hmc_adapter_signature=windowed_stage.hmc_adapter_signature,
                trajectory_hmc_adapter_signature=trajectory_hmc_signature,
                target_scope=target_scope,
            )
            selected_hash = stable_config_hash(selected_payload)
    after_mass_signature = _mass_artifact_signature(adapted_mass)
    frozen_mass_invariant = _frozen_step_trajectory_frozen_mass_invariant(
        before_mass_signature,
        after_mass_signature,
    )
    if not frozen_mass_invariant["passed"]:
        stage_hard_vetoes.append("frozen_step_trajectory_mass_signature_mutated")
        final_status = "hard_veto"
        selected_index = None
        selected_payload = None
        selected_hash = None
    frozen_step_invariant = _frozen_step_trajectory_frozen_step_invariant(
        before=frozen_step,
        after=_required_selected_step_size(fixed_mass_step_stage),
    )
    if not frozen_step_invariant["passed"]:
        stage_hard_vetoes.append("frozen_step_trajectory_step_mutated")
        final_status = "hard_veto"
        selected_index = None
        selected_payload = None
        selected_hash = None
    stage_hard_vetoes = list(dict.fromkeys(str(item) for item in stage_hard_vetoes))
    diagnostic_role = (
        "frozen_step_trajectory_handoff_only"
        if final_status == "passed"
        else ("repair_trigger" if final_status == "repair_or_retry" else "hard_veto")
    )
    return HMCFrozenStepTrajectoryStageResult(
        config=cfg,
        geometry_artifact_hash=geometry.artifact_hash,
        bootstrap_artifact_hash=bootstrap.artifact_hash,
        windowed_stage_artifact_hash=windowed_stage.artifact_hash,
        fixed_mass_step_stage_artifact_hash=fixed_mass_step_stage.artifact_hash,
        selected_bootstrap_kernel_hash=fixed_mass_step_stage.selected_bootstrap_kernel_hash,
        selected_step_hash=str(fixed_mass_step_stage.selected_step_hash),
        adapter_signature=fixed_mass_step_stage.adapter_signature,
        phase4_hmc_adapter_signature=windowed_stage.hmc_adapter_signature,
        phase5_ladder_hmc_adapter_signature=fixed_mass_step_stage.ladder_hmc_adapter_signature,
        trajectory_hmc_adapter_signature=trajectory_hmc_signature,
        adapted_mass_artifact_payload=adapted_mass.to_payload(include_arrays=True),
        adapted_mass_artifact_signature=before_mass_signature,
        frozen_step_size=frozen_step,
        fixed_bootstrap_num_leapfrog_steps=fixed_bootstrap_l,
        target_dimension=windowed_stage.target_dimension,
        candidate_generation=candidate_generation,
        candidate_results=tuple(candidate_results),
        selected_candidate_index=selected_index,
        selected_trajectory_payload=selected_payload,
        selected_trajectory_hash=selected_hash,
        final_status=final_status,
        diagnostic_role=diagnostic_role,
        hard_vetoes=tuple(stage_hard_vetoes),
        repair_triggers=tuple(stage_repair_triggers),
        diagnostics=_frozen_step_trajectory_stage_diagnostics(
            tuple(candidate_results),
            final_status=final_status,
            selected_candidate_index=selected_index,
            run_error=run_error,
            hard_vetoes=tuple(stage_hard_vetoes),
            repair_triggers=tuple(stage_repair_triggers),
            runner_route_summary=_kernel_stage_runner_route_summary(
                active_route=(
                    "frozen_step_trajectory_scoped_reusable_runner"
                    if use_reusable_route
                    else "single_use_or_injected_runner"
                ),
                events=tuple(runner_route_events),
                contract_payloads=runner_contract_payloads,
                semantic_source="run_hmc_frozen_step_trajectory_stage",
                reuse_nonclaim=(
                    "candidate L values often differ, so this stage may gain "
                    "uniform route telemetry more than warm-call reuse"
                ),
            ),
            soft_deadline_closeout=soft_deadline_closeout,
            expected_candidate_count=len(candidates),
        ),
        frozen_mass_invariant=frozen_mass_invariant,
        frozen_step_invariant=frozen_step_invariant,
        seed_report={
            "fixed_mass_step_stage_seed": fixed_mass_step_stage.seed_report.get(
                "fixed_mass_stage_root_seed"
            ),
            "frozen_step_trajectory_root_seed": cfg.seed,
            "candidate_screen_seeds": tuple(
                candidate["seed"] for candidate in candidate_results
            ),
            "seed_owner": "BayesFilter",
        },
        diagnostic_roles={
            "frozen_mass_invariant": "hard_veto",
            "frozen_step_invariant": "hard_veto",
            "candidate_acceptance": "trajectory_handoff_promotion_or_repair",
            "candidate_log_accept_ratio": "hard_veto",
            "candidate_target_log_prob": "hard_veto",
            "target_status_telemetry": "hard_veto_when_enabled",
            "callback_hard_veto": "hard_veto",
            "callback_continuation_veto": "continuation_veto",
            "callback_promotion_veto": "repair_trigger",
            "runtime": "explanatory_or_hard_veto_when_missing",
            "candidate_l_values": "diagnostic_telemetry_only",
        },
    )


def run_hmc_tune_verify_repair_loop(
    *,
    adapter: Any,
    geometry: HMCGeometryInitializationResult,
    bootstrap: HMCBootstrapScreenResult,
    config: HMCTuneVerifyRepairLoopConfig | None = None,
    fixed_mass_screen_callback: FixedMassScreenCallback | None = None,
    trajectory_screen_callback: TrajectoryScreenCallback | None = None,
    verification_callback: VerificationCallback | None = None,
    run_full_chain: RunFullChainFn = run_full_chain_tfp_hmc,
    _budget_policy_factory: Callable[[int, int], "_HMCAttemptBudgetPolicy"] | None = None,
    _windowed_stage_runner: Callable[..., HMCWindowedMassStageResult] = run_hmc_windowed_mass_stage,
    _fixed_mass_step_stage_runner: Callable[..., HMCFixedMassStepStageResult] = run_hmc_fixed_mass_step_stage,
    _frozen_step_trajectory_stage_runner: Callable[..., HMCFrozenStepTrajectoryStageResult] = run_hmc_frozen_step_trajectory_stage,
    _progress_callback: LoopProgressCallback | None = None,
) -> HMCTuneVerifyRepairLoopResult:
    """Run Phase 7 tune/verify/repair with private budget escalation.

    This is a scoped Phase 7 orchestration helper. It may be imported directly,
    but it is not the final one-call ``tune_hmc_kernel`` API.
    """

    cfg = HMCTuneVerifyRepairLoopConfig() if config is None else config
    if not isinstance(cfg, HMCTuneVerifyRepairLoopConfig):
        raise TypeError("config must be HMCTuneVerifyRepairLoopConfig")
    if not isinstance(geometry, HMCGeometryInitializationResult):
        raise TypeError("geometry must be HMCGeometryInitializationResult")
    if not isinstance(bootstrap, HMCBootstrapScreenResult):
        raise TypeError("bootstrap must be HMCBootstrapScreenResult")
    _validate_tune_verify_loop_inputs(adapter=adapter, geometry=geometry, bootstrap=bootstrap)
    target_scope = _resolve_tune_verify_loop_target_scope(adapter, cfg)
    if target_scope != _resolve_windowed_stage_target_scope(
        adapter,
        HMCWindowedMassStageConfig(
            target_accept_prob=cfg.target_accept_prob,
            seed=_derive_seed(cfg.seed, stage_index=10),
            chain_execution_mode=cfg.chain_execution_mode,
            target_scope=cfg.target_scope,
            target_status_trace_policy=cfg.target_status_trace_policy,
            source=cfg.source,
        ),
    ):
        raise ValueError("Phase 7 target scope resolution mismatch")
    policy_factory = (
        _default_attempt_budget_policy if _budget_policy_factory is None else _budget_policy_factory
    )
    attempts: list[HMCTuneVerifyRepairAttempt] = []
    hard_vetoes: list[str] = []
    repair_triggers: list[str] = []
    attempt_state: _HMCPhaseAttemptState | None = None
    final_kernel_payload: Mapping[str, Any] | None = None
    final_kernel_hash: str | None = None
    final_status = "budget_exhausted"
    diagnostic_role = "budget_exhausted_non_promoting"
    terminal_budget_guard_payload: Mapping[str, Any] | None = None

    for attempt_index in range(cfg.max_attempts):
        budget_policy = policy_factory(geometry.target_dimension, attempt_index)
        if not isinstance(budget_policy, _HMCAttemptBudgetPolicy):
            raise TypeError("private budget policy factory must return _HMCAttemptBudgetPolicy")
        verification_budget_blocker = _phase7_verification_acceptance_budget_blocker(
            config=cfg,
            attempt_state=attempt_state,
            next_attempt_policy=budget_policy,
        )
        if verification_budget_blocker is not None:
            final_status = "budget_exhausted"
            diagnostic_role = _PHASE7_VERIFICATION_ACCEPTANCE_BUDGET_BLOCKED
            terminal_budget_guard_payload = verification_budget_blocker
            repair_triggers.append(_PHASE7_VERIFICATION_ACCEPTANCE_BUDGET_BLOCKED)
            _emit_phase7_progress(
                _progress_callback,
                _PHASE7_VERIFICATION_ACCEPTANCE_BUDGET_BLOCKED,
                attempt_index=attempt_index,
                budget_policy=budget_policy,
                completed=True,
                extra=verification_budget_blocker,
            )
            break
        _emit_phase7_progress(
            _progress_callback,
            "loop_attempt_start",
            attempt_index=attempt_index,
            budget_policy=budget_policy,
            started=True,
            extra={"incoming_repair_handoff_available": attempt_state is not None},
        )
        incoming_payload = None if attempt_state is None else attempt_state.payload()
        windowed_stage: HMCWindowedMassStageResult | None = None
        fixed_stage: HMCFixedMassStepStageResult | None = None
        trajectory_stage: HMCFrozenStepTrajectoryStageResult | None = None
        verification_config_payload: Mapping[str, Any] | None = None
        verification_diagnostics: Mapping[str, Any] = {
            "attempt_index": attempt_index,
            "not_run": True,
            "reports_posterior_convergence": False,
        }
        verification_callback_result = FixedMassHMCTuningBudgetCallbackResult()
        attempt_hard_vetoes: list[str] = []
        attempt_repair_triggers: list[str] = []
        attempt_status = "repair_or_retry"
        attempt_role = "repair_trigger"
        handoff_state: _HMCPhaseAttemptState | None = None

        try:
            _emit_phase7_progress(
                _progress_callback,
                "windowed_mass_start",
                attempt_index=attempt_index,
                budget_policy=budget_policy,
                started=True,
            )

            def forward_windowed_mass_progress(
                stage: str,
                payload: Mapping[str, Any],
            ) -> None:
                _emit_phase7_progress(
                    _progress_callback,
                    stage,
                    attempt_index=attempt_index,
                    budget_policy=budget_policy,
                    started=bool(payload.get("started")),
                    completed=bool(payload.get("completed")),
                    extra=_windowed_mass_progress_extra(payload),
                )

            windowed_stage = _windowed_stage_runner(
                adapter=adapter,
                geometry=geometry,
                bootstrap=bootstrap,
                config=_phase7_windowed_stage_config(cfg, attempt_index=attempt_index),
                run_full_chain=run_full_chain,
                _attempt_budget_policy=budget_policy,
                _attempt_state=attempt_state,
                _progress_callback=forward_windowed_mass_progress,
                _attempt_index=attempt_index,
            )
            _emit_phase7_progress(
                _progress_callback,
                "windowed_mass_complete",
                attempt_index=attempt_index,
                budget_policy=budget_policy,
                completed=True,
                extra={
                    "final_status": windowed_stage.final_status,
                    "passed": windowed_stage.passed,
                    "artifact_hash": windowed_stage.artifact_hash,
                },
            )
            if windowed_stage.final_status == "hard_veto":
                attempt_hard_vetoes.extend(windowed_stage.hard_vetoes)
                attempt_status = "hard_veto"
                attempt_role = "hard_veto"
            elif not windowed_stage.passed:
                attempt_repair_triggers.append(
                    f"phase4_windowed_mass_status:{windowed_stage.final_status}"
                )
            else:
                _emit_phase7_progress(
                    _progress_callback,
                    "fixed_mass_step_start",
                    attempt_index=attempt_index,
                    budget_policy=budget_policy,
                    started=True,
                )
                fixed_stage = _fixed_mass_step_stage_runner(
                    adapter=adapter,
                    geometry=geometry,
                    bootstrap=bootstrap,
                    windowed_stage=windowed_stage,
                    config=_phase7_fixed_step_stage_config(cfg, attempt_index=attempt_index),
                    screen_callback=fixed_mass_screen_callback,
                    run_full_chain=run_full_chain,
                    _attempt_budget_policy=budget_policy,
                    _attempt_state=attempt_state,
                    _progress_callback=_progress_callback,
                    _attempt_index=attempt_index,
                )
                _emit_phase7_progress(
                    _progress_callback,
                    "fixed_mass_step_complete",
                    attempt_index=attempt_index,
                    budget_policy=budget_policy,
                    completed=True,
                    extra={
                        "final_status": fixed_stage.final_status,
                        "passed": fixed_stage.passed,
                        "artifact_hash": fixed_stage.artifact_hash,
                    },
                )
                if fixed_stage.final_status == "hard_veto":
                    attempt_hard_vetoes.extend(fixed_stage.hard_vetoes)
                    attempt_status = "hard_veto"
                    attempt_role = "hard_veto"
                elif not fixed_stage.passed:
                    attempt_repair_triggers.extend(fixed_stage.repair_triggers)
                    attempt_repair_triggers.append(
                        f"phase5_fixed_mass_step_status:{fixed_stage.final_status}"
                    )
                else:
                    _emit_phase7_progress(
                        _progress_callback,
                        "trajectory_start",
                        attempt_index=attempt_index,
                        budget_policy=budget_policy,
                        started=True,
                    )
                    trajectory_stage = _frozen_step_trajectory_stage_runner(
                        adapter=adapter,
                        geometry=geometry,
                        bootstrap=bootstrap,
                        windowed_stage=windowed_stage,
                        fixed_mass_step_stage=fixed_stage,
                        config=_phase7_trajectory_stage_config(
                            cfg,
                            attempt_index=attempt_index,
                        ),
                        screen_callback=trajectory_screen_callback,
                        run_full_chain=run_full_chain,
                        _attempt_budget_policy=budget_policy,
                        _attempt_state=attempt_state,
                        _progress_callback=_progress_callback,
                        _attempt_index=attempt_index,
                    )
                    _emit_phase7_progress(
                        _progress_callback,
                        "trajectory_complete",
                        attempt_index=attempt_index,
                        budget_policy=budget_policy,
                        completed=True,
                        extra={
                            "final_status": trajectory_stage.final_status,
                            "passed": trajectory_stage.passed,
                            "artifact_hash": trajectory_stage.artifact_hash,
                        },
                    )
                    if trajectory_stage.final_status == "hard_veto":
                        attempt_hard_vetoes.extend(trajectory_stage.hard_vetoes)
                        attempt_status = "hard_veto"
                        attempt_role = "hard_veto"
                    elif not trajectory_stage.passed:
                        attempt_repair_triggers.extend(trajectory_stage.repair_triggers)
                        attempt_repair_triggers.append(
                            f"phase6_trajectory_status:{trajectory_stage.final_status}"
                        )
                    else:
                        _emit_phase7_progress(
                            _progress_callback,
                            "verification_start",
                            attempt_index=attempt_index,
                            budget_policy=budget_policy,
                            started=True,
                        )
                        (
                            verification_config_payload,
                            verification_diagnostics,
                            verification_callback_result,
                            verify_status,
                            verify_role,
                            verify_hard_vetoes,
                            verify_repair_triggers,
                        ) = _run_phase7_final_verification(
                            adapter=adapter,
                            geometry=geometry,
                            windowed_stage=windowed_stage,
                            fixed_mass_step_stage=fixed_stage,
                            trajectory_stage=trajectory_stage,
                            config=cfg,
                            budget_policy=budget_policy,
                            attempt_index=attempt_index,
                            target_scope=target_scope,
                            verification_callback=verification_callback,
                            run_full_chain=run_full_chain,
                        )
                        _emit_phase7_progress(
                            _progress_callback,
                            "verification_complete",
                            attempt_index=attempt_index,
                            budget_policy=budget_policy,
                            completed=True,
                            extra={
                                "final_status": verify_status,
                                "diagnostic_role": verify_role,
                                "hard_veto_count": len(verify_hard_vetoes),
                                "repair_trigger_count": len(verify_repair_triggers),
                            },
                        )
                        attempt_status = verify_status
                        attempt_role = verify_role
                        attempt_hard_vetoes.extend(verify_hard_vetoes)
                        attempt_repair_triggers.extend(verify_repair_triggers)
                        if attempt_status == "passed":
                            final_kernel_payload = _phase7_final_kernel_payload(
                                config=cfg,
                                geometry=geometry,
                                bootstrap=bootstrap,
                                windowed_stage=windowed_stage,
                                fixed_mass_step_stage=fixed_stage,
                                trajectory_stage=trajectory_stage,
                                verification_config_payload=verification_config_payload,
                                verification_diagnostics=verification_diagnostics,
                                budget_policy=budget_policy,
                                attempt_index=attempt_index,
                                target_scope=target_scope,
                            )
                            final_kernel_hash = stable_config_hash(final_kernel_payload)
        except Exception as exc:  # noqa: BLE001 - Phase 7 must fail closed.
            attempt_status = "hard_veto"
            attempt_role = "hard_veto"
            attempt_hard_vetoes.append("phase7_runtime_error")
            verification_diagnostics = {
                "attempt_index": attempt_index,
                "error_type": type(exc).__name__,
                "error_message": str(exc),
                "reports_posterior_convergence": False,
                "nonclaims": TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS,
            }

        if windowed_stage is not None and windowed_stage.passed:
            handoff_state = _phase7_attempt_state_from_stages(
                config=cfg,
                windowed_stage=windowed_stage,
                fixed_mass_step_stage=fixed_stage,
                frozen_step_trajectory_stage=trajectory_stage,
                verification_config_payload=verification_config_payload,
                verification_diagnostics=verification_diagnostics,
                verification_final_status=attempt_status,
                verification_diagnostic_role=attempt_role,
                verification_repair_triggers=attempt_repair_triggers,
            )
        if attempt_status == "repair_or_retry" and (
            handoff_state is None or not handoff_state.has_stage_repair_handoff
        ):
            attempt_status = "architecture_blocked"
            attempt_role = "architecture_blocked"
            attempt_repair_triggers.append("phase7_required_private_handoff_missing")

        attempt_hard_vetoes = list(dict.fromkeys(str(item) for item in attempt_hard_vetoes))
        attempt_repair_triggers = list(
            dict.fromkeys(str(item) for item in attempt_repair_triggers)
        )
        attempt = HMCTuneVerifyRepairAttempt(
            attempt_index=attempt_index,
            budget_policy_payload=budget_policy.payload(),
            incoming_state_payload=incoming_payload,
            windowed_stage=windowed_stage,
            fixed_mass_step_stage=fixed_stage,
            frozen_step_trajectory_stage=trajectory_stage,
            verification_config_payload=verification_config_payload,
            verification_diagnostics=verification_diagnostics,
            verification_callback_result=verification_callback_result,
            final_status=attempt_status,
            diagnostic_role=attempt_role,
            hard_vetoes=tuple(attempt_hard_vetoes),
            repair_triggers=tuple(attempt_repair_triggers),
            handoff_state_payload=None if handoff_state is None else handoff_state.payload(),
        )
        _emit_phase7_progress(
            _progress_callback,
            "loop_attempt_complete",
            attempt_index=attempt_index,
            budget_policy=budget_policy,
            completed=True,
            extra={
                "final_status": attempt_status,
                "diagnostic_role": attempt_role,
                "hard_veto_count": len(attempt_hard_vetoes),
                "repair_trigger_count": len(attempt_repair_triggers),
            },
        )
        attempts.append(attempt)
        hard_vetoes.extend(attempt_hard_vetoes)
        repair_triggers.extend(attempt_repair_triggers)
        if attempt_status == "passed":
            final_status = "passed"
            diagnostic_role = "fresh_fixed_kernel_verification_passed"
            break
        if attempt_status == "hard_veto":
            final_status = "hard_veto"
            diagnostic_role = "hard_veto"
            final_kernel_payload = None
            final_kernel_hash = None
            break
        if attempt_status == "architecture_blocked":
            final_status = "architecture_blocked"
            diagnostic_role = "architecture_blocked"
            final_kernel_payload = None
            final_kernel_hash = None
            break
        attempt_state = handoff_state
    else:
        final_status = "budget_exhausted"
        diagnostic_role = "budget_exhausted_non_promoting"
        final_kernel_payload = None
        final_kernel_hash = None
        repair_triggers.append("phase7_budget_exhausted")

    hard_vetoes = list(dict.fromkeys(str(item) for item in hard_vetoes))
    repair_triggers = list(dict.fromkeys(str(item) for item in repair_triggers))
    result = HMCTuneVerifyRepairLoopResult(
        config=cfg,
        geometry_artifact_hash=geometry.artifact_hash,
        bootstrap_artifact_hash=bootstrap.artifact_hash,
        adapter_signature=geometry.adapter_signature,
        target_dimension=geometry.target_dimension,
        attempts=tuple(attempts),
        final_status=final_status,
        diagnostic_role=diagnostic_role,
        hard_vetoes=tuple(hard_vetoes),
        repair_triggers=tuple(repair_triggers),
        final_kernel_payload=final_kernel_payload,
        final_kernel_hash=final_kernel_hash,
        seed_report={
            "phase7_root_seed": cfg.seed,
            "attempt_seeds": tuple(_phase7_attempt_seed(cfg.seed, index) for index in range(len(attempts))),
            "verification_seeds": tuple(
                _derive_seed(_phase7_attempt_seed(cfg.seed, attempt.attempt_index), stage_index=4)
                for attempt in attempts
            ),
            "seed_owner": "BayesFilter",
            "verification_seed_independent_of_stage_seeds": True,
        },
        diagnostic_roles={
            "fresh_fixed_kernel_verification": "promotion_or_repair_or_hard_veto",
            "budget_exhausted": "terminal_non_promoting_repair_status",
            "verification_acceptance_budget_blocked": (
                "terminal_non_promoting_public_budget_guard"
            ),
            "architecture_blocked": "terminal_non_promoting_private_plumbing_blocker",
            "callback_hard_veto": "hard_veto",
            "callback_continuation_veto": "hard_veto",
            "callback_promotion_veto": "repair_or_retry",
            "callback_repair_trigger": "repair_or_retry",
            "mass_step_l_invariant": "hard_veto",
            "runtime": "hard_veto_when_error",
        },
        terminal_budget_guard_payload=terminal_budget_guard_payload,
    )
    _emit_phase7_progress(
        _progress_callback,
        "loop_complete",
        attempt_index=attempts[-1].attempt_index,
        budget_policy=None,
        completed=True,
        extra={
            "final_status": result.final_status,
            "diagnostic_role": result.diagnostic_role,
            "loop_artifact_hash": result.artifact_hash,
        },
    )
    return result


def tune_hmc_kernel(
    *,
    adapter: Any,
    initial_position: Any,
    config: HMCKernelTuningConfig | None = None,
    output_dir: str | Path | None = None,
    negative_hessian: Any | None = None,
    initial_covariance: Any | None = None,
    parameter_scales: Any | None = None,
    diagnostic_callback: FixedMassScreenCallback | None = None,
) -> HMCKernelTuningResult:
    """Tune a frozen HMC kernel from model-facing inputs.

    The caller supplies the model adapter, an initial position, optional
    geometry hints, an optional diagnostic callback, and an optional output
    directory.  BayesFilter owns the mass, step-size, leapfrog, screen,
    verification, and repair mechanics.  A final kernel is emitted only when
    the Phase 7 fresh fixed-kernel verification passes.
    """

    cfg = HMCKernelTuningConfig.standard() if config is None else config
    if not isinstance(cfg, HMCKernelTuningConfig):
        raise TypeError("config must be HMCKernelTuningConfig")
    public_timeout_started_perf_counter_s = (
        time.perf_counter() if cfg.public_timeout_budget_s is not None else None
    )
    position = _validate_position(initial_position)
    adapter_signature = stable_adapter_signature(adapter)
    target_dimension = int(position.shape[0])
    artifact_path = _public_tuning_artifact_path(output_dir)
    geometry: HMCGeometryInitializationResult | None = None
    bootstrap: HMCBootstrapScreenResult | None = None
    loop: HMCTuneVerifyRepairLoopResult | None = None
    final_status = "architecture_blocked"
    diagnostic_role = "not_reached"
    hard_vetoes: tuple[str, ...] = ()
    repair_triggers: tuple[str, ...] = ()
    final_kernel_payload: Mapping[str, Any] | None = None
    final_kernel_hash: str | None = None
    progress_path = _public_tuning_progress_path(output_dir)
    progress_state: dict[str, str | None] = {
        "last_started_stage": None,
        "last_completed_stage": None,
        "last_started_substage": None,
        "last_completed_substage": None,
        "last_started_artifact_stage": None,
        "last_completed_artifact_stage": None,
    }
    phase7_state: dict[str, Any] = {
        "last_attempt_index": None,
        "last_budget_payload": None,
    }

    def write_progress(
        stage: str,
        *,
        started: bool = False,
        completed: bool = False,
        phase7_substage: bool = False,
        artifact_stage: bool = False,
        extra: Mapping[str, Any] | None = None,
    ) -> None:
        if artifact_stage:
            if started:
                progress_state["last_started_artifact_stage"] = stage
            if completed:
                progress_state["last_completed_artifact_stage"] = stage
        else:
            if started:
                progress_state["last_started_stage"] = stage
            if completed:
                progress_state["last_completed_stage"] = stage
        if phase7_substage:
            if started:
                progress_state["last_started_substage"] = stage
            if completed:
                progress_state["last_completed_substage"] = stage
        _write_public_tuning_progress_if_requested(
            progress_path=progress_path,
            config=cfg,
            artifact_path=artifact_path,
            current_stage=stage,
            last_started_stage=progress_state["last_started_stage"],
            last_completed_stage=progress_state["last_completed_stage"],
            last_started_substage=progress_state["last_started_substage"],
            last_completed_substage=progress_state["last_completed_substage"],
            last_started_artifact_stage=progress_state["last_started_artifact_stage"],
            last_completed_artifact_stage=progress_state["last_completed_artifact_stage"],
            phase7_last_attempt_index=phase7_state["last_attempt_index"],
            phase7_last_budget_payload=phase7_state["last_budget_payload"],
            bootstrap_public_summary=_bootstrap_public_summary(
                bootstrap,
                xla_requested=cfg.use_xla,
            ),
            adapter_signature=adapter_signature,
            target_dimension=target_dimension,
            extra=extra,
        )

    def write_loop_progress(stage: str, payload: Mapping[str, Any]) -> None:
        event_payload = dict(payload)
        if "attempt_index" in event_payload:
            phase7_state["last_attempt_index"] = int(event_payload["attempt_index"])
        budget_payload = event_payload.get("bounded_public_budget_payload")
        if budget_payload is not None:
            phase7_state["last_budget_payload"] = dict(budget_payload)
        write_progress(
            stage,
            started=bool(event_payload.get("started")),
            completed=bool(event_payload.get("completed")),
            phase7_substage=True,
            extra={
                "phase7_loop_event": event_payload,
                "phase7_progress_contract": {
                    "progress_only": True,
                    "hmc_mechanics_exposed": False,
                    "reports_posterior_convergence": False,
                },
            },
        )

    def write_result_artifact(result: HMCKernelTuningResult) -> None:
        write_progress(
            "artifact_finalization_start",
            started=True,
            artifact_stage=True,
            extra={
                "final_status": result.final_status,
                "diagnostic_role": result.diagnostic_role,
            },
        )
        _write_public_tuning_artifact_if_requested(result, artifact_path)
        write_progress(
            "artifact_finalization_complete",
            completed=True,
            artifact_stage=True,
            extra={
                "artifact_path": None if artifact_path is None else str(artifact_path),
                "artifact_written": artifact_path is not None,
            },
        )

    try:
        write_progress("start", started=True)
        write_progress("geometry_start", started=True)
        geometry = initialize_hmc_kernel_geometry(
            adapter=adapter,
            initial_position=position,
            config=_public_geometry_config(cfg),
            negative_hessian=negative_hessian,
            initial_covariance=initial_covariance,
            parameter_scales=parameter_scales,
        )
        write_progress(
            "geometry_complete",
            completed=True,
            extra={"geometry_artifact_hash": geometry.artifact_hash},
        )
    except Exception as exc:  # noqa: BLE001 - public tuner returns fail-closed artifacts.
        final_status = "hard_veto"
        diagnostic_role = "geometry_initialization_hard_veto"
        hard_vetoes = ("geometry_initialization_error",)
        repair_triggers = (type(exc).__name__,)
        write_progress(
            "geometry_error",
            extra={"error_type": type(exc).__name__, "error_message": str(exc)},
        )
        result = HMCKernelTuningResult(
            config=cfg,
            adapter_signature=adapter_signature,
            target_dimension=target_dimension,
            geometry=None,
            bootstrap=None,
            tune_verify_repair_loop=None,
            final_status=final_status,
            diagnostic_role=diagnostic_role,
            hard_vetoes=hard_vetoes,
            repair_triggers=repair_triggers,
            final_kernel_payload=None,
            final_kernel_hash=None,
            artifact_path=None if artifact_path is None else str(artifact_path),
            diagnostic_roles=_public_tuning_diagnostic_roles(),
        )
        write_result_artifact(result)
        write_progress(
            "result_written",
            extra={
                "final_status": result.final_status,
                "diagnostic_role": result.diagnostic_role,
            },
        )
        return result

    try:
        write_progress("bootstrap_start", started=True)
        bootstrap = run_hmc_bootstrap_screen(
            adapter=adapter,
            geometry=geometry,
            config=_public_bootstrap_config(cfg),
        )
        write_progress(
            "bootstrap_complete",
            completed=True,
            extra={"bootstrap_artifact_hash": bootstrap.artifact_hash},
        )
    except Exception as exc:  # noqa: BLE001 - public tuner returns fail-closed artifacts.
        final_status = "hard_veto"
        diagnostic_role = "bootstrap_screen_hard_veto"
        hard_vetoes = ("bootstrap_screen_error",)
        repair_triggers = (type(exc).__name__,)
        write_progress(
            "bootstrap_error",
            extra={"error_type": type(exc).__name__, "error_message": str(exc)},
        )
        result = HMCKernelTuningResult(
            config=cfg,
            adapter_signature=adapter_signature,
            target_dimension=target_dimension,
            geometry=geometry,
            bootstrap=None,
            tune_verify_repair_loop=None,
            final_status=final_status,
            diagnostic_role=diagnostic_role,
            hard_vetoes=hard_vetoes,
            repair_triggers=repair_triggers,
            final_kernel_payload=None,
            final_kernel_hash=None,
            artifact_path=None if artifact_path is None else str(artifact_path),
            diagnostic_roles=_public_tuning_diagnostic_roles(),
        )
        write_result_artifact(result)
        write_progress(
            "result_written",
            extra={
                "final_status": result.final_status,
                "diagnostic_role": result.diagnostic_role,
            },
        )
        return result

    if not bootstrap.passed:
        final_status = bootstrap.final_status
        diagnostic_role = "bootstrap_screen_non_promoting"
        repair_triggers = tuple(
            dict.fromkeys(
                str(trigger)
                for round_result in bootstrap.rounds
                for trigger in round_result.repair_triggers
            )
        )
        hard_vetoes = tuple(
            dict.fromkeys(
                str(veto)
                for round_result in bootstrap.rounds
                for veto in round_result.hard_vetoes
            )
        )
        result = HMCKernelTuningResult(
            config=cfg,
            adapter_signature=adapter_signature,
            target_dimension=target_dimension,
            geometry=geometry,
            bootstrap=bootstrap,
            tune_verify_repair_loop=None,
            final_status=final_status,
            diagnostic_role=diagnostic_role,
            hard_vetoes=hard_vetoes,
            repair_triggers=repair_triggers,
            final_kernel_payload=None,
            final_kernel_hash=None,
            artifact_path=None if artifact_path is None else str(artifact_path),
            diagnostic_roles=_public_tuning_diagnostic_roles(),
        )
        write_result_artifact(result)
        write_progress(
            "result_written",
            extra={
                "final_status": result.final_status,
                "diagnostic_role": result.diagnostic_role,
            },
        )
        return result

    try:
        write_progress("loop_start", started=True)
        loop = run_hmc_tune_verify_repair_loop(
            adapter=adapter,
            geometry=geometry,
            bootstrap=bootstrap,
            config=_public_loop_config(
                cfg,
                public_timeout_started_perf_counter_s=public_timeout_started_perf_counter_s,
            ),
            fixed_mass_screen_callback=diagnostic_callback,
            trajectory_screen_callback=diagnostic_callback,
            verification_callback=diagnostic_callback,
            _budget_policy_factory=_public_budget_policy_factory(cfg),
            _progress_callback=write_loop_progress,
        )
        write_progress(
            "loop_complete",
            completed=True,
            extra={"loop_artifact_hash": loop.artifact_hash},
        )
    except Exception as exc:  # noqa: BLE001 - public tuner returns fail-closed artifacts.
        final_status = "hard_veto"
        diagnostic_role = "tune_verify_repair_loop_hard_veto"
        hard_vetoes = ("tune_verify_repair_loop_error",)
        repair_triggers = (type(exc).__name__,)
        write_progress(
            "loop_error",
            extra={"error_type": type(exc).__name__, "error_message": str(exc)},
        )
        result = HMCKernelTuningResult(
            config=cfg,
            adapter_signature=adapter_signature,
            target_dimension=target_dimension,
            geometry=geometry,
            bootstrap=bootstrap,
            tune_verify_repair_loop=None,
            final_status=final_status,
            diagnostic_role=diagnostic_role,
            hard_vetoes=hard_vetoes,
            repair_triggers=repair_triggers,
            final_kernel_payload=None,
            final_kernel_hash=None,
            artifact_path=None if artifact_path is None else str(artifact_path),
            diagnostic_roles=_public_tuning_diagnostic_roles(),
        )
        write_result_artifact(result)
        write_progress(
            "result_written",
            extra={
                "final_status": result.final_status,
                "diagnostic_role": result.diagnostic_role,
            },
        )
        return result

    final_status = loop.final_status
    diagnostic_role = loop.diagnostic_role
    hard_vetoes = loop.hard_vetoes
    repair_triggers = loop.repair_triggers
    if loop.passed:
        final_kernel_payload = _public_final_kernel_handoff_payload(loop)
        final_kernel_hash = stable_config_hash(final_kernel_payload)
    result = HMCKernelTuningResult(
        config=cfg,
        adapter_signature=adapter_signature,
        target_dimension=target_dimension,
        geometry=geometry,
        bootstrap=bootstrap,
        tune_verify_repair_loop=loop,
        final_status=final_status,
        diagnostic_role=diagnostic_role,
        hard_vetoes=hard_vetoes,
        repair_triggers=repair_triggers,
        final_kernel_payload=final_kernel_payload,
        final_kernel_hash=final_kernel_hash,
        artifact_path=None if artifact_path is None else str(artifact_path),
        diagnostic_roles=_public_tuning_diagnostic_roles(),
    )
    write_result_artifact(result)
    write_progress(
        "result_written",
        extra={
            "final_status": result.final_status,
            "diagnostic_role": result.diagnostic_role,
        },
    )
    return result


@dataclass(frozen=True)
class _GeometryHint:
    kind: str
    covariance: np.ndarray
    precision_for_formula: np.ndarray
    report: Mapping[str, Any]


def _validate_position(position: Any) -> np.ndarray:
    array = np.asarray(position, dtype=float)
    if array.ndim != 1:
        raise ValueError("initial_position must be a one-dimensional vector")
    if array.shape[0] <= 0:
        raise ValueError("initial_position must be non-empty")
    if not np.all(np.isfinite(array)):
        raise ValueError("initial_position must be finite")
    return array.copy()


def _select_geometry_hint(
    *,
    position: np.ndarray,
    negative_hessian: Any | None,
    initial_covariance: Any | None,
    parameter_scales: Any | None,
    config: HMCGeometryInitializationConfig,
) -> _GeometryHint:
    supplied = {
        "negative_hessian": negative_hessian is not None,
        "initial_covariance": initial_covariance is not None,
        "parameter_scales": parameter_scales is not None,
    }
    failures: list[Mapping[str, Any]] = []
    for kind, value in (
        ("negative_hessian", negative_hessian),
        ("initial_covariance", initial_covariance),
        ("parameter_scales", parameter_scales),
    ):
        if value is None:
            continue
        try:
            return _hint_from_value(
                kind=kind,
                value=value,
                position=position,
                config=config,
                supplied=supplied,
                failures=tuple(failures),
            )
        except Exception as exc:
            failures.append({"kind": kind, "error": str(exc)})
            if not config.allow_geometry_fallback:
                raise
    return _identity_hint(position=position, supplied=supplied, failures=tuple(failures))


def _hint_from_value(
    *,
    kind: str,
    value: Any,
    position: np.ndarray,
    config: HMCGeometryInitializationConfig,
    supplied: Mapping[str, bool],
    failures: tuple[Mapping[str, Any], ...],
) -> _GeometryHint:
    dimension = int(position.shape[0])
    if kind == "negative_hessian":
        precision = _validate_matrix(value, dimension=dimension, name=kind)
        artifact = PrecomputedMassArtifact.from_negative_hessian(
            position=position,
            negative_hessian=precision,
            adapter_signature="geometry_hint_validation_adapter",
            position_role="initial_position",
            covariance_source="negative_hessian",
            source="geometry_initialization_probe",
            jitter=config.covariance_jitter,
            eigenvalue_floor=config.eigenvalue_floor,
            max_condition_number=config.max_condition_number,
        )
        report = {
            "selected_hint": kind,
            "hint_precedence": (
                "negative_hessian",
                "initial_covariance",
                "parameter_scales",
                "identity",
            ),
            "supplied_hints": dict(supplied),
            "fallback_used": bool(failures),
            "fallback_failures": failures,
            "sign_convention": "-d2 log posterior in unconstrained coordinates",
            "parameterization": "same as initial_position",
            "regularization_report": artifact.regularization_report,
        }
        return _GeometryHint(
            kind=kind,
            covariance=np.asarray(artifact.covariance, dtype=float),
            precision_for_formula=np.linalg.pinv(np.asarray(artifact.covariance, dtype=float)),
            report=report,
        )
    if kind == "initial_covariance":
        covariance = _validate_matrix(value, dimension=dimension, name=kind)
        covariance = covariance + config.covariance_jitter * np.eye(dimension)
        _validate_spd(covariance, name=kind)
        return _GeometryHint(
            kind=kind,
            covariance=covariance,
            precision_for_formula=np.linalg.pinv(covariance),
            report={
                "selected_hint": kind,
                "hint_precedence": (
                    "negative_hessian",
                    "initial_covariance",
                    "parameter_scales",
                    "identity",
                ),
                "supplied_hints": dict(supplied),
                "fallback_used": bool(failures),
                "fallback_failures": failures,
                "parameterization": "same as initial_position",
                "regularization_report": {
                    "method": "covariance_jitter",
                    "covariance_jitter": config.covariance_jitter,
                },
            },
        )
    if kind == "parameter_scales":
        scales = np.asarray(value, dtype=float)
        if scales.shape != (dimension,):
            raise ValueError("parameter_scales shape must match initial_position")
        if not np.all(np.isfinite(scales)):
            raise ValueError("parameter_scales must be finite")
        if np.any(scales <= 0.0):
            raise ValueError("parameter_scales must be positive")
        covariance = np.diag(scales**2) + config.covariance_jitter * np.eye(dimension)
        return _GeometryHint(
            kind=kind,
            covariance=covariance,
            precision_for_formula=np.diag(1.0 / np.diag(covariance)),
            report={
                "selected_hint": kind,
                "hint_precedence": (
                    "negative_hessian",
                    "initial_covariance",
                    "parameter_scales",
                    "identity",
                ),
                "supplied_hints": dict(supplied),
                "fallback_used": bool(failures),
                "fallback_failures": failures,
                "parameterization": "same as initial_position",
                "regularization_report": {
                    "method": "diagonal_scales",
                    "covariance_jitter": config.covariance_jitter,
                },
            },
        )
    raise ValueError(f"unknown geometry hint kind: {kind}")


def _identity_hint(
    *,
    position: np.ndarray,
    supplied: Mapping[str, bool],
    failures: tuple[Mapping[str, Any], ...],
) -> _GeometryHint:
    dimension = int(position.shape[0])
    return _GeometryHint(
        kind="identity",
        covariance=np.eye(dimension),
        precision_for_formula=np.eye(dimension),
        report={
            "selected_hint": "identity",
            "hint_precedence": (
                "negative_hessian",
                "initial_covariance",
                "parameter_scales",
                "identity",
            ),
            "supplied_hints": dict(supplied),
            "fallback_used": bool(failures) or any(supplied.values()),
            "fallback_failures": failures,
            "parameterization": "same as initial_position",
            "regularization_report": {"method": "identity_fallback"},
        },
    )


def _validate_matrix(value: Any, *, dimension: int, name: str) -> np.ndarray:
    matrix = np.asarray(value, dtype=float)
    if matrix.shape != (dimension, dimension):
        raise ValueError(f"{name} shape must match initial_position dimension")
    if not np.all(np.isfinite(matrix)):
        raise ValueError(f"{name} must be finite")
    return 0.5 * (matrix + matrix.T)


def _validate_spd(matrix: np.ndarray, *, name: str) -> None:
    eigenvalues = np.linalg.eigvalsh(matrix)
    if not np.all(np.isfinite(eigenvalues)):
        raise ValueError(f"{name} eigenvalues must be finite")
    if np.any(eigenvalues <= 0.0):
        raise ValueError(f"{name} must be positive definite")


def _build_mass_artifact(
    *,
    position: np.ndarray,
    adapter_signature: str,
    hint: _GeometryHint,
    config: HMCGeometryInitializationConfig,
) -> PrecomputedMassArtifact:
    source = f"geometry_initialization_{hint.kind}"
    return PrecomputedMassArtifact.from_covariance(
        position=position,
        covariance=hint.covariance,
        adapter_signature=adapter_signature,
        position_role="initial_position",
        covariance_source=hint.kind,
        matrix_used_for_square_root="geometry_initialization_covariance",
        source=source,
        jitter=0.0,
        regularization_report={
            **dict(hint.report.get("regularization_report", {})),
            "geometry_initializer_source": config.source,
        },
        nonclaims=GEOMETRY_INITIALIZATION_NONCLAIMS,
    )


def _curvature_frequencies(
    *,
    covariance: np.ndarray,
    precision: np.ndarray,
) -> np.ndarray:
    eigenvalues_c, eigenvectors_c = np.linalg.eigh(0.5 * (covariance + covariance.T))
    if not np.all(np.isfinite(eigenvalues_c)) or np.any(eigenvalues_c <= 0.0):
        raise ValueError("covariance square-root eigenvalues must be finite and positive")
    factor = eigenvectors_c @ np.diag(np.sqrt(eigenvalues_c)) @ eigenvectors_c.T
    scaled = factor @ precision @ factor
    scaled = 0.5 * (scaled + scaled.T)
    eigenvalues = np.linalg.eigvalsh(scaled)
    if not np.all(np.isfinite(eigenvalues)):
        raise ValueError("mass-scaled curvature eigenvalues must be finite")
    eigenvalues = np.maximum(eigenvalues, 1.0e-16)
    return np.sqrt(eigenvalues)


def _target_trajectory_length(omega: np.ndarray) -> float:
    median = float(np.median(omega))
    if not np.isfinite(median) or median <= 0.0:
        raise ValueError("median curvature frequency must be positive and finite")
    return float(np.pi / (2.0 * median))


def _initial_step_size(
    omega: np.ndarray,
    *,
    dimension: int,
    config: HMCGeometryInitializationConfig,
) -> float:
    rms = float(np.sqrt(np.mean(np.square(omega))))
    max_omega = float(np.max(omega))
    if not np.isfinite(rms) or rms <= 0.0:
        raise ValueError("rms curvature frequency must be positive and finite")
    if not np.isfinite(max_omega) or max_omega <= 0.0:
        raise ValueError("max curvature frequency must be positive and finite")
    dimension_scale = float(dimension) ** (-0.25)
    scaled = config.geometry_scaling_c * dimension_scale / rms
    stable = config.stability_guard * 2.0 / max_omega
    step = float(min(scaled, stable))
    if not np.isfinite(step) or step <= 0.0:
        raise ValueError("formula-derived initial step size must be positive and finite")
    return step


def _curvature_report(omega: np.ndarray) -> Mapping[str, Any]:
    return {
        "omega_min": float(np.min(omega)),
        "omega_median": float(np.median(omega)),
        "omega_rms": float(np.sqrt(np.mean(np.square(omega)))),
        "omega_max": float(np.max(omega)),
        "omega_count": int(omega.shape[0]),
        "finite": bool(np.all(np.isfinite(omega))),
        "positive": bool(np.all(omega > 0.0)),
    }


def _derive_seed(root_seed: tuple[int, int], *, stage_index: int) -> tuple[int, int]:
    return (int(root_seed[0]) + 1009 * int(stage_index), int(root_seed[1]) + 9176)


def _mass_artifact_signature(mass_artifact: PrecomputedMassArtifact) -> str:
    return stable_config_hash(
        {
            "signature_payload": mass_artifact.signature_payload(),
            "position": np.asarray(mass_artifact.position, dtype=float),
            "covariance": np.asarray(mass_artifact.covariance, dtype=float),
            "factor": np.asarray(mass_artifact.factor, dtype=float),
        }
    )


class _BootstrapFixedMassLatentValueScoreAdapter:
    """Latent fixed-mass target with a mass-bound stable adapter signature."""

    def __init__(
        self,
        *,
        base_adapter: Any,
        transform: Any,
        target_scope: str,
        adapter_signature: str,
        nonclaims: Sequence[str] = BOOTSTRAP_SCREEN_NONCLAIMS,
    ) -> None:
        if not hasattr(base_adapter, "log_prob_and_grad"):
            raise TypeError("base_adapter must expose log_prob_and_grad")
        self.base_adapter = base_adapter
        self.transform = transform
        self.parameter_dim = int(transform.dimension)
        self.target_scope = str(target_scope)
        if not self.target_scope:
            raise ValueError("target_scope must be non-empty")
        self.runtime_backend = (
            "bayesfilter.inference.hmc_kernel_tuning."
            "_BootstrapFixedMassLatentValueScoreAdapter"
        )
        self.nonclaims = _string_tuple(nonclaims)
        self._adapter_signature = str(adapter_signature)
        if not self._adapter_signature:
            raise ValueError("bootstrap fixed-mass adapter signature must be non-empty")

    def adapter_signature(self) -> str:
        return self._adapter_signature

    def value_score_capability(self) -> ValueScoreCapability:
        base_capability = value_score_capability(self.base_adapter)
        base_scope = base_capability.target_scope
        scope_matches = base_scope is None or str(base_scope) == self.target_scope
        preserve_xla = (
            bool(base_capability.is_accepted_full_chain_xla_diagnostic_authority)
            and scope_matches
        )
        nonclaims = self.nonclaims + (
            f"base value/score authority: {base_capability.value_score_authority}",
            "bootstrap latent wrapper cannot promote fallback base authority",
            "bootstrap latent wrapper preserves XLA authority only from accepted base authority",
        )
        return ValueScoreCapability(
            value_score_authority=base_capability.value_score_authority,
            xla_hmc_ready=preserve_xla,
            full_chain_xla_diagnostic_ready=preserve_xla,
            runtime_backend=self.runtime_backend,
            evidence_path=base_capability.evidence_path if preserve_xla else None,
            target_scope=self.target_scope,
            nonclaims=nonclaims,
        )

    def initial_position(self) -> Any:
        import tensorflow as tf

        return tf.zeros((self.parameter_dim,), dtype=tf.float64)

    def latent_to_position(self, z: Any) -> Any:
        import tensorflow as tf

        z_tensor = self._validate_trailing_dimension(z, "latent coordinate")
        center = tf.convert_to_tensor(self.transform.center, dtype=z_tensor.dtype)
        factor = tf.convert_to_tensor(self.transform.factor, dtype=z_tensor.dtype)
        return center + tf.tensordot(z_tensor, factor, axes=[[-1], [1]])

    def theta_score_to_latent_score(self, theta_score: Any) -> Any:
        import tensorflow as tf

        score_tensor = self._validate_trailing_dimension(theta_score, "position/score")
        factor = tf.convert_to_tensor(self.transform.factor, dtype=score_tensor.dtype)
        return tf.tensordot(score_tensor, factor, axes=[[-1], [0]])

    def log_prob_and_grad(self, z: Any) -> tuple[Any, Any]:
        import tensorflow as tf

        z_tensor = self._validate_trailing_dimension(z, "latent coordinate")
        theta = self.latent_to_position(z_tensor)
        value, theta_score = self.base_adapter.log_prob_and_grad(theta)
        value_tensor = tf.convert_to_tensor(value, dtype=z_tensor.dtype)
        theta_score_tensor = tf.convert_to_tensor(theta_score, dtype=z_tensor.dtype)
        _validate_value_score_shapes(
            theta=theta,
            value=value_tensor,
            score=theta_score_tensor,
        )
        return value_tensor, self.theta_score_to_latent_score(theta_score_tensor)

    def target_status_telemetry(self, z: Any) -> Mapping[str, Any]:
        telemetry = getattr(self.base_adapter, "target_status_telemetry", None)
        if not callable(telemetry):
            raise TypeError("base_adapter must expose target_status_telemetry")
        theta = self.latent_to_position(z)
        payload = telemetry(theta)
        if not isinstance(payload, Mapping):
            raise TypeError("target_status_telemetry must return a mapping")
        return payload

    def _validate_trailing_dimension(self, value: Any, label: str) -> Any:
        import tensorflow as tf

        tensor = tf.convert_to_tensor(value, dtype=tf.float64)
        if tensor.shape.rank is None:
            raise ValueError(f"{label} tensor must have static rank")
        if tensor.shape.rank < 1:
            raise ValueError(
                f"{label} tensor must have rank at least 1 with trailing parameter dimension"
            )
        trailing = tensor.shape[-1]
        if trailing is None:
            raise ValueError(f"{label} tensor must have static trailing dimension")
        if int(trailing) != self.parameter_dim:
            raise ValueError(f"{label} trailing dimension must match transform dimension")
        return tensor


def _resolve_bootstrap_target_scope(
    adapter: Any,
    config: HMCBootstrapScreenConfig,
) -> str:
    capability = value_score_capability(adapter)
    capability_scope = capability.target_scope
    if config.target_scope is not None:
        target_scope = str(config.target_scope)
        if not target_scope:
            raise ValueError("target_scope must be non-empty when provided")
        if capability_scope is not None and target_scope != capability_scope:
            raise ValueError("value/score target_scope mismatch")
        return target_scope
    if capability_scope is None or not str(capability_scope):
        raise ValueError(
            "bootstrap screen requires config.target_scope or an adapter "
            "value_score_capability target_scope"
        )
    return str(capability_scope)


def _resolve_windowed_stage_target_scope(
    adapter: Any,
    config: HMCWindowedMassStageConfig,
) -> str:
    capability = value_score_capability(adapter)
    capability_scope = capability.target_scope
    if config.target_scope is not None:
        target_scope = str(config.target_scope)
        if not target_scope:
            raise ValueError("target_scope must be non-empty when provided")
        if capability_scope is not None and target_scope != capability_scope:
            raise ValueError("value/score target_scope mismatch")
        return target_scope
    if capability_scope is None or not str(capability_scope):
        raise ValueError(
            "windowed mass stage requires config.target_scope or an adapter "
            "value_score_capability target_scope"
        )
    return str(capability_scope)


def _resolve_fixed_mass_step_stage_target_scope(
    adapter: Any,
    config: HMCFixedMassStepStageConfig,
) -> str:
    capability = value_score_capability(adapter)
    capability_scope = capability.target_scope
    if config.target_scope is not None:
        target_scope = str(config.target_scope)
        if not target_scope:
            raise ValueError("target_scope must be non-empty when provided")
        if capability_scope is not None and target_scope != capability_scope:
            raise ValueError("value/score target_scope mismatch")
        return target_scope
    if capability_scope is None or not str(capability_scope):
        raise ValueError(
            "fixed-mass step stage requires config.target_scope or an adapter "
            "value_score_capability target_scope"
        )
    return str(capability_scope)


def _resolve_frozen_step_trajectory_stage_target_scope(
    adapter: Any,
    config: HMCFrozenStepTrajectoryStageConfig,
) -> str:
    capability = value_score_capability(adapter)
    capability_scope = capability.target_scope
    if config.target_scope is not None:
        target_scope = str(config.target_scope)
        if not target_scope:
            raise ValueError("target_scope must be non-empty when provided")
        if capability_scope is not None and target_scope != capability_scope:
            raise ValueError("value/score target_scope mismatch")
        return target_scope
    if capability_scope is None or not str(capability_scope):
        raise ValueError(
            "frozen-step trajectory stage requires config.target_scope or an "
            "adapter value_score_capability target_scope"
        )
    return str(capability_scope)


def _validate_windowed_stage_inputs(
    *,
    adapter: Any,
    geometry: HMCGeometryInitializationResult,
    bootstrap: HMCBootstrapScreenResult,
) -> None:
    adapter_signature = stable_adapter_signature(adapter)
    if adapter_signature != geometry.adapter_signature:
        raise ValueError("windowed stage adapter signature must match geometry")
    if adapter_signature != bootstrap.adapter_signature:
        raise ValueError("windowed stage adapter signature must match bootstrap")
    if not bootstrap.passed or bootstrap.selected_kernel_payload is None:
        raise ValueError("windowed stage requires passed bootstrap result")
    geometry.mass_artifact.validate_for_adapter(
        adapter,
        expected_dim=geometry.target_dimension,
    )
    mass_signature = _mass_artifact_signature(geometry.mass_artifact)
    if mass_signature != geometry.mass_artifact_signature:
        raise ValueError("geometry mass artifact signature mismatch")
    if mass_signature != bootstrap.mass_artifact_signature:
        raise ValueError("windowed stage mass artifact signature must match bootstrap")
    if bootstrap.geometry_artifact_hash != geometry.artifact_hash:
        raise ValueError("windowed stage bootstrap must match geometry artifact")
    if geometry.target_dimension != bootstrap.target_dimension:
        raise ValueError("windowed stage target dimension must match bootstrap")


def _validate_fixed_mass_step_stage_inputs(
    *,
    adapter: Any,
    geometry: HMCGeometryInitializationResult,
    bootstrap: HMCBootstrapScreenResult,
    windowed_stage: HMCWindowedMassStageResult,
    config: HMCFixedMassStepStageConfig,
) -> None:
    adapter_signature = stable_adapter_signature(adapter)
    if adapter_signature != windowed_stage.adapter_signature:
        raise ValueError("fixed-mass step stage adapter signature must match Phase 4")
    if geometry.adapter_signature != windowed_stage.adapter_signature:
        raise ValueError("fixed-mass step stage geometry must match Phase 4")
    if geometry.artifact_hash != windowed_stage.geometry_artifact_hash:
        raise ValueError("fixed-mass step stage geometry artifact must match Phase 4")
    if bootstrap.artifact_hash != windowed_stage.bootstrap_artifact_hash:
        raise ValueError("fixed-mass step stage bootstrap artifact must match Phase 4")
    if bootstrap.selected_kernel_hash != windowed_stage.selected_bootstrap_kernel_hash:
        raise ValueError("fixed-mass step stage selected bootstrap kernel mismatch")
    _validate_windowed_stage_inputs(adapter=adapter, geometry=geometry, bootstrap=bootstrap)
    if not windowed_stage.passed:
        raise ValueError("fixed-mass step stage requires passed Phase 4 result")
    if windowed_stage.adapted_mass_artifact_signature is None:
        raise ValueError("fixed-mass step stage requires adapted mass signature")
    if windowed_stage.candidate_step_size is None:
        raise ValueError("fixed-mass step stage requires candidate step size")
    if not np.isfinite(float(windowed_stage.candidate_step_size)):
        raise ValueError("fixed-mass step candidate step must be finite")
    if float(windowed_stage.candidate_step_size) <= 0.0:
        raise ValueError("fixed-mass step candidate step must be positive")
    selected = _selected_bootstrap_kernel_from_windowed_stage(
        windowed_stage,
        bootstrap=bootstrap,
    )
    if int(selected.get("num_leapfrog_steps", 0)) <= 0:
        raise ValueError("fixed-mass step stage requires positive bootstrap L")
    artifact = _phase4_adapted_mass_artifact(windowed_stage)
    if artifact.adapter_signature != windowed_stage.hmc_adapter_signature:
        raise ValueError("Phase 4 adapted mass adapter signature mismatch")
    signature = _mass_artifact_signature(artifact)
    if signature != windowed_stage.adapted_mass_artifact_signature:
        raise ValueError("Phase 4 adapted mass signature mismatch")
    artifact.validate_for_adapter(
        _phase4_latent_adapter_for_step_stage(
            adapter=adapter,
            geometry=geometry,
            windowed_stage=windowed_stage,
            target_scope=_resolve_fixed_mass_step_stage_target_scope(adapter, config),
        ),
        expected_dim=windowed_stage.target_dimension,
    )


def _validate_frozen_step_trajectory_stage_inputs(
    *,
    adapter: Any,
    geometry: HMCGeometryInitializationResult,
    bootstrap: HMCBootstrapScreenResult,
    windowed_stage: HMCWindowedMassStageResult,
    fixed_mass_step_stage: HMCFixedMassStepStageResult,
    config: HMCFrozenStepTrajectoryStageConfig,
) -> None:
    adapter_signature = stable_adapter_signature(adapter)
    if adapter_signature != fixed_mass_step_stage.adapter_signature:
        raise ValueError("frozen-step trajectory adapter signature mismatch")
    if adapter_signature != windowed_stage.adapter_signature:
        raise ValueError("frozen-step trajectory Phase 4 adapter signature mismatch")
    if geometry.adapter_signature != adapter_signature:
        raise ValueError("frozen-step trajectory geometry adapter signature mismatch")
    if bootstrap.adapter_signature != adapter_signature:
        raise ValueError("frozen-step trajectory bootstrap adapter signature mismatch")
    if geometry.artifact_hash != windowed_stage.geometry_artifact_hash:
        raise ValueError("frozen-step trajectory geometry artifact mismatch")
    if bootstrap.artifact_hash != windowed_stage.bootstrap_artifact_hash:
        raise ValueError("frozen-step trajectory bootstrap artifact mismatch")
    if fixed_mass_step_stage.windowed_stage_artifact_hash != windowed_stage.artifact_hash:
        raise ValueError("frozen-step trajectory Phase 5 windowed artifact mismatch")
    if fixed_mass_step_stage.selected_bootstrap_kernel_hash != bootstrap.selected_kernel_hash:
        raise ValueError("frozen-step trajectory selected bootstrap kernel hash mismatch")
    if fixed_mass_step_stage.selected_bootstrap_kernel_hash != windowed_stage.selected_bootstrap_kernel_hash:
        raise ValueError("frozen-step trajectory Phase 4 selected bootstrap hash mismatch")
    selected_bootstrap = bootstrap.selected_kernel_payload
    if selected_bootstrap is None or bootstrap.selected_kernel_hash is None:
        raise ValueError("frozen-step trajectory requires selected bootstrap kernel")
    if int(fixed_mass_step_stage.fixed_num_leapfrog_steps) != int(
        selected_bootstrap["num_leapfrog_steps"]
    ):
        raise ValueError("frozen-step trajectory fixed bootstrap L lineage mismatch")
    if not fixed_mass_step_stage.passed:
        raise ValueError("frozen-step trajectory requires passed Phase 5 result")
    if fixed_mass_step_stage.selected_step_payload is None:
        raise ValueError("frozen-step trajectory requires selected step payload")
    if fixed_mass_step_stage.selected_step_hash is None:
        raise ValueError("frozen-step trajectory requires selected step hash")
    if stable_config_hash(fixed_mass_step_stage.selected_step_payload) != fixed_mass_step_stage.selected_step_hash:
        raise ValueError("frozen-step trajectory selected step hash mismatch")
    selected_step = float(fixed_mass_step_stage.selected_step_payload.get("step_size"))
    if not np.isfinite(selected_step) or selected_step <= 0.0:
        raise ValueError("frozen-step trajectory selected step must be positive")
    if fixed_mass_step_stage.budget_ladder_result is None:
        raise ValueError("frozen-step trajectory requires Phase 5 budget ladder result")
    ladder = fixed_mass_step_stage.budget_ladder_result
    if not ladder.passed:
        raise ValueError("frozen-step trajectory requires passed Phase 5 ladder")
    if ladder.mass_artifact_signature != fixed_mass_step_stage.adapted_mass_artifact_signature:
        raise ValueError("frozen-step trajectory Phase 5 ladder mass signature mismatch")
    if ladder.selected_config_hash != fixed_mass_step_stage.selected_step_hash:
        raise ValueError("frozen-step trajectory ladder selected step hash mismatch")
    if ladder.adapter_signature != fixed_mass_step_stage.phase4_hmc_adapter_signature:
        raise ValueError("frozen-step trajectory ladder adapter signature mismatch")
    if ladder.hmc_adapter_signature != fixed_mass_step_stage.ladder_hmc_adapter_signature:
        raise ValueError("frozen-step trajectory ladder HMC adapter signature mismatch")
    if fixed_mass_step_stage.adapted_mass_artifact_signature != windowed_stage.adapted_mass_artifact_signature:
        raise ValueError("frozen-step trajectory Phase 4 adapted mass signature mismatch")
    if fixed_mass_step_stage.target_dimension != windowed_stage.target_dimension:
        raise ValueError("frozen-step trajectory target dimension mismatch")
    if geometry.target_dimension != fixed_mass_step_stage.target_dimension:
        raise ValueError("frozen-step trajectory geometry dimension mismatch")
    _validate_fixed_mass_step_stage_inputs(
        adapter=adapter,
        geometry=geometry,
        bootstrap=bootstrap,
        windowed_stage=windowed_stage,
        config=HMCFixedMassStepStageConfig(
            target_accept_prob=fixed_mass_step_stage.config.target_accept_prob,
            acceptance_band=fixed_mass_step_stage.config.acceptance_band,
            repair_band=fixed_mass_step_stage.config.repair_band,
            seed=fixed_mass_step_stage.config.seed,
            chain_execution_mode=fixed_mass_step_stage.config.chain_execution_mode,
            target_scope=config.target_scope
            if config.target_scope is not None
            else fixed_mass_step_stage.config.target_scope,
            target_status_trace_policy=fixed_mass_step_stage.config.target_status_trace_policy,
            source=fixed_mass_step_stage.config.source,
        ),
    )
    target_scope = _resolve_frozen_step_trajectory_stage_target_scope(adapter, config)
    selected_payload_scope = fixed_mass_step_stage.selected_step_payload.get("target_scope")
    if selected_payload_scope is not None and str(selected_payload_scope) != target_scope:
        raise ValueError("frozen-step trajectory selected step target_scope mismatch")


def _validate_tune_verify_loop_inputs(
    *,
    adapter: Any,
    geometry: HMCGeometryInitializationResult,
    bootstrap: HMCBootstrapScreenResult,
) -> None:
    adapter_signature = stable_adapter_signature(adapter)
    if adapter_signature != geometry.adapter_signature:
        raise ValueError("Phase 7 adapter signature must match geometry")
    if adapter_signature != bootstrap.adapter_signature:
        raise ValueError("Phase 7 adapter signature must match bootstrap")
    if bootstrap.geometry_artifact_hash != geometry.artifact_hash:
        raise ValueError("Phase 7 bootstrap must match geometry artifact")
    if not bootstrap.passed:
        raise ValueError("Phase 7 requires passed bootstrap result")
    if geometry.target_dimension != bootstrap.target_dimension:
        raise ValueError("Phase 7 geometry and bootstrap dimensions must match")
    geometry.mass_artifact.validate_for_adapter(
        adapter,
        expected_dim=geometry.target_dimension,
    )


def _public_tuning_forbidden_fields() -> tuple[str, ...]:
    return (
        "step_size",
        "initial_step_size",
        "num_leapfrog_steps",
        "leapfrog_count",
        "min_leapfrog",
        "max_leapfrog",
        "candidate_l_grid",
        "trajectory_grid",
        "mass_window_schedule",
        "warmup_budget_schedule",
        "tuning_budget_schedule",
        "tune_num_results",
        "screen_num_results",
        "verification_num_results",
        "verification_num_burnin_steps",
    )


def _public_tuning_preset_role(preset: str) -> str:
    if preset == "smoke":
        return "contract_scale_only"
    if preset == "diagnostic":
        return "bounded_public_timeout_diagnostic_only"
    if preset == "diagnostic_plus":
        return "bounded_public_verification_diagnostic_only"
    if preset == "standard":
        return "moderate_local_diagnostic_only"
    if preset == "serious":
        return "dimension_scaled_tuning_policy_only"
    raise ValueError("unknown HMC kernel tuning preset")


def _public_geometry_config(config: HMCKernelTuningConfig) -> HMCGeometryInitializationConfig:
    return HMCGeometryInitializationConfig(
        geometry_scaling_c=config.geometry_scaling_c,
        stability_guard=config.stability_guard,
        covariance_jitter=config.covariance_jitter,
        eigenvalue_floor=config.eigenvalue_floor,
        max_condition_number=config.max_condition_number,
        allow_geometry_fallback=config.allow_geometry_fallback,
        seed=_derive_seed(config.seed, stage_index=2),
        source=f"{config.source}.geometry",
    )


def _public_bootstrap_config(config: HMCKernelTuningConfig) -> HMCBootstrapScreenConfig:
    if config.preset == "smoke":
        screen_num_results = 4
        screen_num_burnin_steps = 1
    elif config.preset == "standard":
        screen_num_results = 16
        screen_num_burnin_steps = 4
    else:
        screen_num_results = 32
        screen_num_burnin_steps = 8
    return HMCBootstrapScreenConfig(
        target_accept_prob=config.target_accept_prob,
        acceptance_band=config.acceptance_band,
        repair_band=config.repair_band,
        max_repairs=config.bootstrap_max_repairs,
        screen_num_results=screen_num_results,
        screen_num_burnin_steps=screen_num_burnin_steps,
        seed=_derive_seed(config.seed, stage_index=3),
        chain_execution_mode=config.chain_execution_mode,
        use_xla=config.use_xla,
        target_scope=config.target_scope,
        target_status_trace_policy=config.target_status_trace_policy,
        source=f"{config.source}.bootstrap",
    )


def _public_loop_config(
    config: HMCKernelTuningConfig,
    *,
    public_timeout_started_perf_counter_s: float | None = None,
) -> HMCTuneVerifyRepairLoopConfig:
    return HMCTuneVerifyRepairLoopConfig(
        target_accept_prob=config.target_accept_prob,
        acceptance_band=config.acceptance_band,
        repair_band=config.repair_band,
        max_attempts=config.max_attempts,
        seed=_derive_seed(config.seed, stage_index=7),
        chain_execution_mode=config.chain_execution_mode,
        use_xla=config.use_xla,
        target_scope=config.target_scope,
        target_status_trace_policy=config.target_status_trace_policy,
        public_timeout_budget_s=config.public_timeout_budget_s,
        public_timeout_started_perf_counter_s=public_timeout_started_perf_counter_s,
        source=f"{config.source}.tune_verify_repair_loop",
    )


def _public_budget_policy_factory(
    config: HMCKernelTuningConfig,
) -> Callable[[int, int], _HMCAttemptBudgetPolicy] | None:
    if config.preset == "serious":
        return None

    def factory(target_dimension: int, attempt_index: int) -> _HMCAttemptBudgetPolicy:
        dimension = int(target_dimension)
        if dimension <= 0:
            raise ValueError("target_dimension must be positive")
        index = int(attempt_index)
        if index < 0:
            raise ValueError("attempt_index must be non-negative")
        if config.preset == "smoke":
            base = min(max(8, 4 * dimension), 64)
            warmup = max(12, base)
            screen_floor = 4
            verification_floor = 4
            burnin_floor = 1
            budget_class = "smoke_contract"
            budget_cap = 64
        elif config.preset == "diagnostic":
            budget_cap = 64
            base = min(max(16, 8 * dimension), 32)
            warmup = max(16, base)
            screen_floor = 8
            verification_floor = 8
            burnin_floor = 2
            budget_class = "bounded_public_diagnostic"
        elif config.preset == "diagnostic_plus":
            budget_cap = 256
            base = min(max(64, 32 * dimension), 128)
            warmup = max(64, base)
            screen_floor = 16
            verification_floor = 32
            burnin_floor = 4
            budget_class = "bounded_public_diagnostic_plus"
        else:
            base = max(128, 25 * dimension)
            warmup = base
            screen_floor = 16
            verification_floor = 32
            burnin_floor = 4
            budget_class = "standard_public_diagnostic"
            budget_cap = None
        budget = int(base * (2 ** index))
        if budget_cap is not None:
            budget = min(budget, budget_cap)
        phase5_screen = max(screen_floor, _ceil_div(budget, 4))
        phase6_screen = max(screen_floor, _ceil_div(budget, 4))
        verification_results = max(verification_floor, _ceil_div(budget, 2))
        return _HMCAttemptBudgetPolicy(
            target_dimension=dimension,
            attempt_index=index,
            budget=budget,
            phase4_warmup_steps=warmup,
            phase5_tune_budgets=(
                max(2, _ceil_div(budget, 4)),
                max(4, _ceil_div(budget, 2)),
                max(8, budget),
            ),
            phase5_screen_num_results=phase5_screen,
            phase5_screen_burnin_steps=max(burnin_floor, _ceil_div(phase5_screen, 4)),
            phase6_screen_num_results=phase6_screen,
            phase6_screen_burnin_steps=max(burnin_floor, _ceil_div(phase6_screen, 4)),
            verification_num_results=verification_results,
            verification_num_burnin_steps=max(
                burnin_floor,
                _ceil_div(verification_results, 4),
            ),
            serious_policy=False,
            public_budget_class=budget_class,
            public_budget_cap=budget_cap,
            public_max_attempts=config.max_attempts,
            public_diagnostic_preset=config.preset,
        )

    return factory


def _public_final_kernel_handoff_payload(
    loop: HMCTuneVerifyRepairLoopResult,
) -> Mapping[str, Any]:
    if not loop.passed or loop.final_kernel_payload is None:
        raise ValueError("public handoff requires passed Phase 7 final kernel")
    private_payload = loop.final_kernel_payload
    required_keys = (
        "schema",
        "target_scope",
        "target_dimension",
        "adapted_mass_artifact_payload",
        "adapted_mass_artifact_signature",
        "step_size",
        "num_leapfrog_steps",
        "trajectory_length",
        "target_accept_prob",
        "acceptance_band",
        "verification_acceptance_rate",
        "geometry_artifact_hash",
        "bootstrap_artifact_hash",
        "windowed_stage_artifact_hash",
        "fixed_mass_step_stage_artifact_hash",
        "frozen_step_trajectory_stage_artifact_hash",
        "selected_step_hash",
        "selected_trajectory_hash",
        "fresh_fixed_kernel_verification_passed",
        "reports_posterior_convergence",
        "reports_sampler_superiority",
        "reports_default_readiness",
        "reports_external_client_scientific_claim",
        "reports_gpu_or_xla_readiness",
        "nonclaims",
    )
    return {
        "runtime": "bayesfilter.inference.tune_hmc_kernel",
        "public_handoff_schema": "bayesfilter.hmc_public_frozen_kernel_handoff.v1",
        **{key: private_payload[key] for key in required_keys if key in private_payload},
        "phase7_final_kernel_hash": loop.final_kernel_hash,
        "internal_tuning_controls_exposed": False,
    }


def _public_tuning_artifact_path(output_dir: str | Path | None) -> Path | None:
    if output_dir is None:
        return None
    path = Path(output_dir)
    if path.suffix:
        return path
    return path / "hmc_kernel_tuning_result.json"


def _public_tuning_progress_path(output_dir: str | Path | None) -> Path | None:
    if output_dir is None:
        return None
    path = Path(output_dir)
    if path.suffix:
        return path.with_name(_PUBLIC_TUNING_PROGRESS_FILENAME)
    return path / _PUBLIC_TUNING_PROGRESS_FILENAME


def _utc_now_isoformat() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _write_public_tuning_progress_if_requested(
    *,
    progress_path: Path | None,
    config: HMCKernelTuningConfig,
    artifact_path: Path | None,
    current_stage: str,
    last_started_stage: str | None,
    last_completed_stage: str | None,
    adapter_signature: str | None,
    target_dimension: int | None,
    last_started_substage: str | None = None,
    last_completed_substage: str | None = None,
    last_started_artifact_stage: str | None = None,
    last_completed_artifact_stage: str | None = None,
    phase7_last_attempt_index: int | None = None,
    phase7_last_budget_payload: Mapping[str, Any] | None = None,
    bootstrap_public_summary: Mapping[str, Any] | None = None,
    extra: Mapping[str, Any] | None = None,
) -> None:
    if progress_path is None:
        return
    progress_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "bayesfilter.hmc_kernel_tuning_progress.v1",
        "preset": config.preset,
        "current_stage": str(current_stage),
        "last_started_stage": last_started_stage,
        "last_completed_stage": last_completed_stage,
        "last_started_substage": last_started_substage,
        "last_completed_substage": last_completed_substage,
        "last_started_artifact_stage": last_started_artifact_stage,
        "last_completed_artifact_stage": last_completed_artifact_stage,
        "phase7_last_attempt_index": phase7_last_attempt_index,
        "phase7_last_budget_payload": None
        if phase7_last_budget_payload is None
        else dict(phase7_last_budget_payload),
        "bootstrap_public_summary": _bootstrap_public_summary(
            None,
            xla_requested=config.use_xla,
        )
        if bootstrap_public_summary is None
        else dict(bootstrap_public_summary),
        "timestamp_utc": _utc_now_isoformat(),
        "process_id": os.getpid(),
        "output_directory": str(progress_path.parent),
        "artifact_path": None if artifact_path is None else str(artifact_path),
        "progress_artifact_path": str(progress_path),
        "adapter_signature": adapter_signature,
        "target_dimension": None if target_dimension is None else int(target_dimension),
        "reports_posterior_convergence": False,
        "reports_sampler_superiority": False,
        "reports_default_readiness": False,
        "reports_external_client_scientific_claim": False,
        "reports_gpu_or_xla_readiness": False,
        "nonclaims": HMC_KERNEL_TUNING_PUBLIC_NONCLAIMS,
    }
    if extra is not None:
        payload["extra"] = dict(extra)
    with progress_path.open("w", encoding="utf-8") as handle:
        handle.write(json.dumps(_json_ready(payload), indent=2, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def _write_public_tuning_artifact_if_requested(
    result: HMCKernelTuningResult,
    artifact_path: Path | None,
) -> None:
    if artifact_path is None:
        return
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact = _public_tuning_artifact_payload(result)
    artifact_path.write_text(
        json.dumps(_json_ready(artifact), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _public_tuning_artifact_payload(
    result: HMCKernelTuningResult,
) -> Mapping[str, Any]:
    active_repair_triggers = () if result.final_status == "passed" else result.repair_triggers
    historical_repair_triggers = result.repair_triggers if result.final_status == "passed" else ()
    phase7_public_summary = _phase7_public_summary(result.tune_verify_repair_loop)
    return {
        "schema": "bayesfilter.hmc_kernel_tuning_public_artifact.v1",
        "result_hash": result.artifact_hash,
        "config": result.config.payload(),
        "adapter_signature": result.adapter_signature,
        "target_dimension": result.target_dimension,
        "stage_hashes": {
            "geometry": None if result.geometry is None else result.geometry.artifact_hash,
            "bootstrap": None if result.bootstrap is None else result.bootstrap.artifact_hash,
            "tune_verify_repair_loop": None
            if result.tune_verify_repair_loop is None
            else result.tune_verify_repair_loop.artifact_hash,
        },
        "status": result.final_status,
        "diagnostic_role": result.diagnostic_role,
        "hard_vetoes": result.hard_vetoes,
        "repair_triggers": active_repair_triggers,
        "active_repair_triggers": active_repair_triggers,
        "historical_repair_triggers": historical_repair_triggers,
        "bootstrap_public_summary": _bootstrap_public_summary(
            result.bootstrap,
            xla_requested=result.config.use_xla,
        ),
        "final_kernel_payload": result.final_kernel_payload,
        "final_kernel_hash": result.final_kernel_hash,
        "final_kernel_requires_phase7_pass": True,
        "attempt_count": None
        if result.tune_verify_repair_loop is None
        else len(result.tune_verify_repair_loop.attempts),
        "phase7_public_summary": phase7_public_summary,
        "diagnostic_roles": result.diagnostic_roles,
        "artifact_policy": {
            "posterior_samples_written": False,
            "internal_tuning_controls_exposed": False,
            "private_budget_schedule_exposed": False,
            "mass_window_schedule_exposed": False,
            "candidate_grid_exposed": False,
            "phase7_public_summary_exposed": phase7_public_summary is not None,
            "raw_draw_counts_exposed": False,
            "private_state_exposed": False,
            "public_reconstruction_api": False,
        },
        "reports_posterior_convergence": False,
        "reports_sampler_superiority": False,
        "reports_default_readiness": False,
        "reports_external_client_scientific_claim": False,
        "reports_gpu_or_xla_readiness": False,
        "nonclaims": result.nonclaims,
    }


def _phase7_public_summary(
    loop: HMCTuneVerifyRepairLoopResult | None,
) -> Mapping[str, Any] | None:
    if loop is None:
        return None
    last_attempt = loop.attempts[-1] if loop.attempts else None
    last_phase6_summary = (
        None
        if last_attempt is None
        else _frozen_step_trajectory_public_summary(last_attempt.frozen_step_trajectory_stage)
    )
    attempt_summaries = tuple(
        _phase7_attempt_public_summary(attempt) for attempt in loop.attempts
    )
    return {
        "schema": "bayesfilter.hmc_tune_verify_repair_public_summary.v1",
        "final_status": loop.final_status,
        "diagnostic_role": loop.diagnostic_role,
        "attempt_count": len(loop.attempts),
        "attempt_summaries": attempt_summaries,
        "latest_attempt_index": None if last_attempt is None else last_attempt.attempt_index,
        "latest_attempt_status": None if last_attempt is None else last_attempt.final_status,
        "latest_attempt_diagnostic_role": None
        if last_attempt is None
        else last_attempt.diagnostic_role,
        "latest_attempt_repair_triggers": ()
        if last_attempt is None
        else last_attempt.repair_triggers,
        "latest_phase6_public_summary": last_phase6_summary,
        "terminal_budget_guard": _phase7_terminal_budget_guard_public_summary(
            loop.terminal_budget_guard_payload
        ),
        "repair_triggers": loop.repair_triggers,
        "hard_vetoes": loop.hard_vetoes,
        "candidate_grid_exposed": False,
        "hmc_mechanics_exposed": False,
        "reports_posterior_convergence": False,
        "reports_sampler_superiority": False,
        "reports_default_readiness": False,
        "reports_gpu_or_xla_readiness": False,
        "nonclaims": TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS,
    }


def _phase7_terminal_budget_guard_public_summary(
    payload: Mapping[str, Any] | None,
) -> Mapping[str, Any] | None:
    if not isinstance(payload, Mapping):
        return None
    allowed_keys = {
        "schema",
        "classification",
        "previous_verification_acceptance_relation",
        "verification_repair_trigger",
        "verification_repair_applied",
        "next_attempt_index",
        "next_attempt_public_budget_class",
        "next_attempt_public_budget_cap",
        "next_attempt_budget_is_public_policy",
        "timeout_budget_s",
        "elapsed_s",
        "remaining_s",
        "reserve_s",
        "estimated_next_candidate_s",
        "estimated_pre_phase6_retry_overhead_s",
        "estimated_pre_phase6_retry_overhead_reserve_multiplier",
        "estimated_minimum_next_attempt_s",
        "deadline_clock_scope",
        "closeout_required_before_next_attempt",
        "diagnostic_role",
        "progress_only",
        "hmc_mechanics_exposed",
        "reports_posterior_convergence",
        "reports_sampler_superiority",
        "reports_default_readiness",
        "reports_external_client_scientific_claim",
        "reports_gpu_or_xla_readiness",
        "nonclaims",
    }
    return {key: payload[key] for key in allowed_keys if key in payload}


def _phase7_attempt_public_summary(
    attempt: HMCTuneVerifyRepairAttempt,
) -> Mapping[str, Any]:
    """Summarize a Phase 7 attempt without exposing HMC mechanics."""

    return {
        "schema": "bayesfilter.hmc_tune_verify_repair_attempt_public_summary.v1",
        "attempt_index": attempt.attempt_index,
        "final_status": attempt.final_status,
        "diagnostic_role": attempt.diagnostic_role,
        "hard_vetoes": attempt.hard_vetoes,
        "repair_triggers": attempt.repair_triggers,
        "budget_public_summary": _phase7_attempt_budget_public_summary(
            attempt.budget_policy_payload
        ),
        "stage_statuses": {
            "windowed_mass": _stage_status_public_summary(attempt.windowed_stage),
            "fixed_mass_step": _stage_status_public_summary(attempt.fixed_mass_step_stage),
            "frozen_step_trajectory": _stage_status_public_summary(
                attempt.frozen_step_trajectory_stage
            ),
            "verification": _phase7_verification_public_summary(attempt),
        },
        "phase6_public_summary": _frozen_step_trajectory_public_summary(
            attempt.frozen_step_trajectory_stage
        ),
        "private_handoff_payload_exposed": False,
        "hmc_mechanics_exposed": False,
        "reports_posterior_convergence": False,
        "reports_sampler_superiority": False,
        "reports_default_readiness": False,
        "reports_gpu_or_xla_readiness": False,
        "nonclaims": TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS,
    }


def _stage_status_public_summary(stage: Any) -> Mapping[str, Any] | None:
    if stage is None:
        return None
    return {
        "final_status": getattr(stage, "final_status", None),
        "diagnostic_role": getattr(stage, "diagnostic_role", None),
        "passed": bool(getattr(stage, "passed", False)),
        "hard_vetoes": tuple(getattr(stage, "hard_vetoes", ())),
        "repair_triggers": tuple(getattr(stage, "repair_triggers", ())),
        "artifact_hash": getattr(stage, "artifact_hash", None),
        "hmc_mechanics_exposed": False,
        "reports_posterior_convergence": False,
    }


def _phase7_attempt_budget_public_summary(
    budget_payload: Mapping[str, Any] | None,
) -> Mapping[str, Any] | None:
    if not isinstance(budget_payload, Mapping):
        return None
    allowed_keys = {
        "target_dimension",
        "attempt_index",
        "budget",
        "serious_policy",
        "public_budget_class",
        "public_budget_cap",
        "public_max_attempts",
        "public_diagnostic_preset",
        "diagnostic_role",
        "internal_policy_only",
    }
    summary = {key: budget_payload[key] for key in allowed_keys if key in budget_payload}
    summary["substage_budget_details_exposed"] = False
    summary["hmc_mechanics_exposed"] = False
    summary["reports_posterior_convergence"] = False
    return summary


def _phase7_verification_public_summary(
    attempt: HMCTuneVerifyRepairAttempt,
) -> Mapping[str, Any]:
    diagnostics = (
        attempt.verification_diagnostics
        if isinstance(attempt.verification_diagnostics, Mapping)
        else {}
    )
    config_payload = (
        attempt.verification_config_payload
        if isinstance(attempt.verification_config_payload, Mapping)
        else {}
    )
    budget_payload = (
        attempt.budget_policy_payload
        if isinstance(attempt.budget_policy_payload, Mapping)
        else {}
    )
    # HMCTuneVerifyRepairAttempt intentionally does not retain the loop config,
    # so the verifier payload must carry the acceptance band used by the final
    # promotion classifier.  The fallback is exposed as a provenance flag rather
    # than silently pretending the payload was complete.
    raw_band = config_payload.get("acceptance_band")
    acceptance_band_from_payload = (
        isinstance(raw_band, Sequence)
        and not isinstance(raw_band, (str, bytes))
        and len(raw_band) == 2
    )
    acceptance_band = (
        tuple(float(item) for item in raw_band)
        if acceptance_band_from_payload
        else (0.55, 0.85)
    )
    relation = _acceptance_relation_to_band(diagnostics.get("acceptance_rate"), acceptance_band)
    sequential_policy = diagnostics.get("sequential_rhat_policy")
    runner_route = diagnostics.get("runner_route_summary")
    route_summary = None
    if isinstance(runner_route, Mapping):
        route_summary = {
            "active_route": runner_route.get("active_route"),
            "single_use_build_count": runner_route.get("single_use_build_count"),
            "fallback_status": runner_route.get("fallback_status"),
            "semantic_source": runner_route.get("semantic_source"),
        }
    summary = {
        "schema": "bayesfilter.hmc_phase7_verification_public_summary.v1",
        "attempt_index": attempt.attempt_index,
        "verification_ran": bool(
            attempt.verification_config_payload is not None
            and not diagnostics.get("not_run")
        ),
        "final_status": attempt.final_status,
        "diagnostic_role": attempt.diagnostic_role,
        "hard_vetoes": attempt.hard_vetoes,
        "repair_triggers": attempt.repair_triggers,
        "verification_policy": config_payload.get(
            "verification_policy",
            "sequential_rhat" if diagnostics.get("sequential_rhat_verification") else None,
        ),
        "sequential_rhat_verification": bool(
            diagnostics.get("sequential_rhat_verification")
        ),
        "rhat_threshold": diagnostics.get("rhat_threshold"),
        "check_interval": diagnostics.get("check_interval"),
        "max_results": diagnostics.get("max_results")
        or config_payload.get("max_results")
        or budget_payload.get("verification_num_results"),
        "num_burnin_steps": config_payload.get("num_burnin_steps"),
        "chain_count": config_payload.get("chain_count"),
        "all_finite_rhat_at_or_below_threshold": diagnostics.get(
            "all_finite_rhat_at_or_below_threshold"
        ),
        "cap_hit": diagnostics.get("cap_hit"),
        "acceptance_relation": relation,
        "acceptance_band_from_payload": acceptance_band_from_payload,
        "acceptance_band_fallback_used": not acceptance_band_from_payload,
        "runtime_finite": diagnostics.get("runtime_finite"),
        "log_accept_ratio_finite": diagnostics.get("log_accept_ratio_finite"),
        "draw_values_finite": diagnostics.get("samples_all_finite"),
        "target_values_finite": diagnostics.get("target_log_prob_finite"),
        "runner_route_public_summary": route_summary,
        "hmc_mechanics_exposed": False,
        "reports_posterior_convergence": False,
        "reports_sampler_superiority": False,
        "reports_default_readiness": False,
        "reports_gpu_or_xla_readiness": False,
        "nonclaims": TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS,
    }
    return summary


def _public_tuning_diagnostic_roles() -> Mapping[str, str]:
    return {
        "geometry_initialization": "hard_veto_when_invalid",
        "bootstrap_screen": "promotion_or_repair_or_hard_veto",
        "tune_verify_repair_loop": "promotion_or_repair_or_hard_veto",
        "fresh_fixed_kernel_verification": "kernel_handoff_screen_only",
        "output_artifact": "audit_evidence_only_not_public_reconstruction_api",
    }


def _bootstrap_public_summary(
    bootstrap: HMCBootstrapScreenResult | None,
    *,
    xla_requested: bool,
) -> Mapping[str, Any]:
    """Summarize Phase 3 routing evidence without raw HMC mechanics."""

    if bootstrap is None:
        return {
            "round_count": None,
            "final_status": None,
            "last_round_index": None,
            "last_classification": None,
            "last_diagnostic_role": None,
            "last_acceptance_relation_to_band": None,
            "observed_acceptance_relations": (),
            "oscillatory_acceptance_repair_observed": False,
            "hard_veto_present": False,
            "hard_veto_categories": (),
            "leapfrog_cap_saturation_observed": False,
            "leapfrog_cap_saturation_direction": "none",
            "xla_requested": bool(xla_requested),
            "jit_compile_metadata": "missing",
            "round_timing_available": False,
            "max_round_runtime_s": None,
            "timing_scope": "missing",
            "metadata_limitations": ("bootstrap_not_started",),
        }
    rounds = tuple(bootstrap.rounds)
    last_round = rounds[-1] if rounds else None
    relations = tuple(
        _bootstrap_acceptance_relation(
            round_result.diagnostics.get("acceptance_rate"),
            bootstrap.config.acceptance_band,
        )
        for round_result in rounds
    )
    hard_veto_categories = tuple(
        dict.fromkeys(
            _public_bootstrap_hard_veto_category(veto)
            for round_result in rounds
            for veto in round_result.hard_vetoes
        )
    )
    clamp_directions = tuple(
        str(round_result.clamp_direction)
        for round_result in rounds
        if round_result.leapfrog_clamped and round_result.clamp_direction is not None
    )
    finite_runtimes = tuple(
        runtime
        for runtime in (
            _scalar_or_none(round_result.diagnostics.get("runtime_s"))
            for round_result in rounds
        )
        if runtime is not None and bool(np.isfinite(runtime))
    )
    timing_scopes = tuple(
        str(scope)
        for scope in (
            _bootstrap_round_timing_scope(round_result.diagnostics)
            for round_result in rounds
        )
        if scope is not None
    )
    metadata_limitations: list[str] = []
    jit_states = tuple(
        _bootstrap_round_jit_metadata(round_result.diagnostics)
        for round_result in rounds
    )
    if not jit_states or any(state == "missing" for state in jit_states):
        metadata_limitations.append("jit_compile_metadata_missing")
    if not finite_runtimes:
        metadata_limitations.append("round_runtime_missing")
    if not timing_scopes:
        metadata_limitations.append("timing_scope_missing")
    if any(
        _bootstrap_round_uses_fixture_or_synthetic(round_result.diagnostics)
        for round_result in rounds
    ):
        metadata_limitations.append("fixture_or_synthetic_metadata_present")
    if any(relation == "missing_or_nonfinite" for relation in relations):
        metadata_limitations.append("acceptance_relation_missing_or_nonfinite")
    return {
        "round_count": len(rounds),
        "final_status": bootstrap.final_status,
        "last_round_index": None if last_round is None else last_round.round_index,
        "last_classification": None if last_round is None else last_round.classification,
        "last_diagnostic_role": None
        if last_round is None
        else last_round.diagnostic_role,
        "last_acceptance_relation_to_band": None
        if last_round is None
        else relations[-1],
        "observed_acceptance_relations": tuple(dict.fromkeys(relations)),
        "oscillatory_acceptance_repair_observed": (
            "below" in relations and "above" in relations
        ),
        "hard_veto_present": bool(hard_veto_categories),
        "hard_veto_categories": hard_veto_categories,
        "leapfrog_cap_saturation_observed": bool(clamp_directions),
        "leapfrog_cap_saturation_direction": _bootstrap_cap_saturation_direction(
            clamp_directions
        ),
        "xla_requested": bool(xla_requested),
        "jit_compile_metadata": _summarize_bootstrap_jit_metadata(jit_states),
        "round_timing_available": bool(finite_runtimes),
        "max_round_runtime_s": None if not finite_runtimes else max(finite_runtimes),
        "timing_scope": _summarize_bootstrap_timing_scope(timing_scopes),
        "metadata_limitations": tuple(dict.fromkeys(metadata_limitations)),
    }


def _bootstrap_acceptance_relation(
    value: Any,
    acceptance_band: tuple[float, float],
) -> str:
    acceptance = _scalar_or_none(value)
    if acceptance is None or not np.isfinite(acceptance):
        return "missing_or_nonfinite"
    lower, upper = acceptance_band
    if acceptance < lower:
        return "below"
    if acceptance > upper:
        return "above"
    return "inside"


def _public_bootstrap_hard_veto_category(veto: str) -> str:
    mapping = {
        "screen_hmc_error": "screen_hmc_error",
        "screen_acceptance_missing_or_nonfinite": "nonfinite_acceptance",
        "screen_runtime_missing_or_nonfinite": "screen_hmc_error",
        "screen_log_accept_nonfinite_or_missing": "nonfinite_log_accept",
        "screen_samples_nonfinite_or_missing": "nonfinite_samples",
        "screen_target_log_prob_nonfinite_or_missing": "nonfinite_target_log_prob",
        "screen_target_status_telemetry_failure": "target_status_telemetry_failure",
    }
    return mapping.get(str(veto), "screen_hmc_error")


def _bootstrap_cap_saturation_direction(directions: tuple[str, ...]) -> str:
    if not directions:
        return "none"
    unique = tuple(dict.fromkeys(directions))
    if len(unique) == 1 and unique[0] in {"min", "max"}:
        return unique[0]
    if any(direction not in {"min", "max"} for direction in unique):
        return "unknown"
    return "mixed"


def _bootstrap_round_metadata(diagnostics: Mapping[str, Any]) -> Mapping[str, Any]:
    metadata = diagnostics.get("runtime_metadata")
    return metadata if isinstance(metadata, Mapping) else {}


def _bootstrap_round_jit_metadata(diagnostics: Mapping[str, Any]) -> str:
    metadata = _bootstrap_round_metadata(diagnostics)
    value = _bool_or_none(metadata.get("jit_compile"))
    if value is None:
        return "missing"
    return "true" if value else "false"


def _summarize_bootstrap_jit_metadata(states: tuple[str, ...]) -> str:
    if not states or any(state == "missing" for state in states):
        return "missing"
    if all(state == "true" for state in states):
        return "true"
    if all(state == "false" for state in states):
        return "false"
    return "missing"


def _bootstrap_round_timing_scope(diagnostics: Mapping[str, Any]) -> str | None:
    metadata = _bootstrap_round_metadata(diagnostics)
    scope = metadata.get("sample_chain_timing_scope")
    if scope is None:
        return None
    value = str(scope)
    return value if value else None


def _summarize_bootstrap_timing_scope(scopes: tuple[str, ...]) -> str:
    if not scopes:
        return "missing"
    unique = tuple(dict.fromkeys(scopes))
    return unique[0] if len(unique) == 1 else "mixed"


def _bootstrap_round_uses_fixture_or_synthetic(
    diagnostics: Mapping[str, Any],
) -> bool:
    metadata = _bootstrap_round_metadata(diagnostics)
    return _metadata_marks_fixture_or_synthetic(metadata)


def _resolve_tune_verify_loop_target_scope(
    adapter: Any,
    config: HMCTuneVerifyRepairLoopConfig,
) -> str:
    capability = value_score_capability(adapter)
    capability_scope = capability.target_scope
    if config.target_scope is not None:
        target_scope = str(config.target_scope)
        if not target_scope:
            raise ValueError("target_scope must be non-empty when provided")
        if capability_scope is not None and target_scope != capability_scope:
            raise ValueError("value/score target_scope mismatch")
        return target_scope
    if capability_scope is None or not str(capability_scope):
        raise ValueError(
            "Phase 7 requires config.target_scope or an adapter "
            "value_score_capability target_scope"
        )
    return str(capability_scope)


@dataclass(frozen=True)
class _HMCAttemptBudgetPolicy:
    target_dimension: int
    attempt_index: int
    budget: int
    phase4_warmup_steps: int
    phase5_tune_budgets: tuple[int, int, int]
    phase5_screen_num_results: int
    phase5_screen_burnin_steps: int
    phase6_screen_num_results: int
    phase6_screen_burnin_steps: int
    verification_num_results: int
    verification_num_burnin_steps: int
    serious_policy: bool = True
    public_budget_class: str | None = None
    public_budget_cap: int | None = None
    public_max_attempts: int | None = None
    public_diagnostic_preset: str | None = None

    def __post_init__(self) -> None:
        for name in (
            "target_dimension",
            "attempt_index",
            "budget",
            "phase4_warmup_steps",
            "phase5_screen_num_results",
            "phase5_screen_burnin_steps",
            "phase6_screen_num_results",
            "phase6_screen_burnin_steps",
            "verification_num_results",
            "verification_num_burnin_steps",
        ):
            value = int(getattr(self, name))
            if name == "attempt_index":
                if value < 0:
                    raise ValueError("attempt_index must be non-negative")
            elif value <= 0:
                raise ValueError(f"{name} must be positive")
            object.__setattr__(self, name, value)
        budgets = tuple(int(item) for item in self.phase5_tune_budgets)
        if len(budgets) != 3 or any(item <= 0 for item in budgets):
            raise ValueError("phase5_tune_budgets must contain three positive values")
        object.__setattr__(self, "phase5_tune_budgets", budgets)
        object.__setattr__(self, "serious_policy", bool(self.serious_policy))
        budget_class = (
            None
            if self.public_budget_class is None
            else str(self.public_budget_class)
        )
        object.__setattr__(self, "public_budget_class", budget_class)
        budget_cap = (
            None
            if self.public_budget_cap is None
            else int(self.public_budget_cap)
        )
        if budget_cap is not None and budget_cap <= 0:
            raise ValueError("public_budget_cap must be positive when provided")
        object.__setattr__(self, "public_budget_cap", budget_cap)
        max_attempts = (
            None
            if self.public_max_attempts is None
            else int(self.public_max_attempts)
        )
        if max_attempts is not None and max_attempts <= 0:
            raise ValueError("public_max_attempts must be positive when provided")
        object.__setattr__(self, "public_max_attempts", max_attempts)
        preset = (
            None
            if self.public_diagnostic_preset is None
            else str(self.public_diagnostic_preset)
        )
        object.__setattr__(self, "public_diagnostic_preset", preset)

    def payload(self) -> Mapping[str, Any]:
        return {
            "target_dimension": self.target_dimension,
            "attempt_index": self.attempt_index,
            "budget": self.budget,
            "phase4_warmup_steps": self.phase4_warmup_steps,
            "phase5_tune_budgets": self.phase5_tune_budgets,
            "phase5_screen_num_results": self.phase5_screen_num_results,
            "phase5_screen_burnin_steps": self.phase5_screen_burnin_steps,
            "phase6_screen_num_results": self.phase6_screen_num_results,
            "phase6_screen_burnin_steps": self.phase6_screen_burnin_steps,
            "verification_num_results": self.verification_num_results,
            "verification_num_burnin_steps": self.verification_num_burnin_steps,
            "budget_formula": (
                "budget0=min(max_budget, max(min_run, 20*dimension)); "
                "budget_k=min(max_tune, budget0*2**k)"
            ),
            "budget_formula_parameters": {
                "min_run": _SERIOUS_TUNING_MIN_RUN_BUDGET,
                "dimension_factor": _SERIOUS_TUNING_DIMENSION_FACTOR,
                "max_budget": _SERIOUS_TUNING_MAX_INITIAL_BUDGET,
                "max_tune": _SERIOUS_TUNING_MAX_TUNE_BUDGET,
            },
            "subbudget_formula": {
                "phase4_warmup_steps": "budget_k",
                "phase5_tune_budgets": "(ceil(budget_k/4), ceil(budget_k/2), budget_k)",
                "phase5_screen": "results=max(32, ceil(budget_k/4)); burnin=max(8, ceil(results/4))",
                "phase6_screen": "results=max(32, ceil(budget_k/4)); burnin=max(8, ceil(results/4))",
                "verification": "results=max(64, ceil(budget_k/2)); burnin=max(16, ceil(results/4))",
            },
            "serious_policy": self.serious_policy,
            "public_budget_class": self.public_budget_class,
            "public_budget_cap": self.public_budget_cap,
            "public_max_attempts": self.public_max_attempts,
            "public_diagnostic_preset": self.public_diagnostic_preset,
            "diagnostic_role": (
                "public_bounded_timeout_diagnostic"
                if self.public_diagnostic_preset == "diagnostic"
                else (
                    "public_bounded_verification_diagnostic_plus"
                    if self.public_diagnostic_preset == "diagnostic_plus"
                    else "public_kernel_tuning_budget"
                )
            ),
            "nonclaims": TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS,
            "internal_policy_only": True,
        }


def _phase7_progress_budget_payload(
    budget_policy: _HMCAttemptBudgetPolicy | None,
) -> Mapping[str, Any] | None:
    if budget_policy is None:
        return None
    return {
        "target_dimension": budget_policy.target_dimension,
        "attempt_index": budget_policy.attempt_index,
        "budget": budget_policy.budget,
        "serious_policy": budget_policy.serious_policy,
        "public_budget_class": budget_policy.public_budget_class,
        "public_budget_cap": budget_policy.public_budget_cap,
        "public_max_attempts": budget_policy.public_max_attempts,
        "public_diagnostic_preset": budget_policy.public_diagnostic_preset,
        "diagnostic_role": (
            "public_bounded_timeout_diagnostic"
            if budget_policy.public_diagnostic_preset == "diagnostic"
            else (
                "public_bounded_verification_diagnostic_plus"
                if budget_policy.public_diagnostic_preset == "diagnostic_plus"
                else "public_kernel_tuning_budget"
            )
        ),
        "nonclaims": TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS,
        "internal_policy_only": True,
        "substage_budget_details_exposed": False,
        "hmc_mechanics_exposed": False,
        "reports_posterior_convergence": False,
    }


def _emit_windowed_mass_progress(
    callback: LoopProgressCallback | None,
    stage: str,
    *,
    attempt_index: int | None,
    route_category: str,
    started: bool = False,
    completed: bool = False,
    elapsed_s: float | None = None,
    started_perf_counter_s: float | None = None,
) -> None:
    if callback is None:
        return
    payload: dict[str, Any] = {
        "stage": str(stage),
        "started": bool(started),
        "completed": bool(completed),
        "progress_only": True,
        "hmc_mechanics_exposed": False,
        "route_category": str(route_category),
        "reports_posterior_convergence": False,
        "reports_sampler_superiority": False,
        "reports_default_readiness": False,
        "reports_external_client_scientific_claim": False,
        "reports_gpu_or_xla_readiness": False,
        "nonclaims": WINDOWED_MASS_STAGE_NONCLAIMS,
    }
    if attempt_index is not None:
        payload["attempt_index"] = int(attempt_index)
    if started_perf_counter_s is not None:
        payload["started_perf_counter_s"] = float(started_perf_counter_s)
        payload["timing_anchor_role"] = "process_local_monotonic_debug_only"
    if elapsed_s is not None:
        payload["elapsed_s"] = float(elapsed_s)
    callback(str(stage), payload)


def _windowed_mass_progress_extra(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    allowed_keys = {
        "stage",
        "attempt_index",
        "started",
        "completed",
        "progress_only",
        "hmc_mechanics_exposed",
        "route_category",
        "elapsed_s",
        "started_perf_counter_s",
        "timing_anchor_role",
        "reports_posterior_convergence",
        "reports_sampler_superiority",
        "reports_default_readiness",
        "reports_external_client_scientific_claim",
        "reports_gpu_or_xla_readiness",
        "nonclaims",
    }
    return {key: payload[key] for key in allowed_keys if key in payload}


def _budget_ladder_progress_extra(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    allowed_keys = {
        "stage",
        "round_index",
        "budget",
        "role",
        "started",
        "completed",
        "route_category",
        "call_config_hash",
        "num_results",
        "num_burnin_steps",
        "substage_budget_details_exposed",
        "uses_dual_averaging",
        "runner_reused",
        "static_contract_hash",
        "elapsed_s",
        "started_perf_counter_s",
        "timing_anchor_role",
        "error_type",
        "progress_only",
        "hmc_mechanics_exposed",
        "reports_posterior_convergence",
        "reports_sampler_superiority",
        "reports_default_readiness",
        "reports_external_client_scientific_claim",
        "reports_gpu_or_xla_readiness",
        "nonclaims",
    }
    return {key: payload[key] for key in allowed_keys if key in payload}


def _trajectory_candidate_progress_extra(
    *,
    stage: str,
    candidate_index: int,
    candidate_count: int,
    config: FullChainHMCConfig,
    runner_event: Mapping[str, Any] | None,
    completed_candidate_count: int | None = None,
    soft_deadline_payload: Mapping[str, Any] | None = None,
    elapsed_s: float | None = None,
    started_perf_counter_s: float | None = None,
    error_type: str | None = None,
) -> Mapping[str, Any]:
    payload: dict[str, Any] = {
        "stage": str(stage),
        "candidate_index": int(candidate_index),
        "candidate_count": int(candidate_count),
        "completed_candidate_count": (
            int(completed_candidate_count)
            if completed_candidate_count is not None
            else int(candidate_index)
        ),
        "num_results": int(config.num_results),
        "num_burnin_steps": int(config.num_burnin_steps),
        "substage_budget_details_exposed": True,
        "call_config_hash": stable_config_hash(config.signature_payload()),
        "route_category": (
            "injected_runner"
            if config.chain_execution_mode != "tf_function"
            else "reusable_runner"
        ),
        "runner_reused": None
        if runner_event is None
        else bool(runner_event.get("runner_reused", False)),
        "static_contract_hash": None
        if runner_event is None
        else runner_event.get("static_contract_hash"),
        "progress_only": True,
        "hmc_mechanics_exposed": False,
        "reports_posterior_convergence": False,
        "reports_sampler_superiority": False,
        "reports_default_readiness": False,
        "reports_external_client_scientific_claim": False,
        "reports_gpu_or_xla_readiness": False,
        "nonclaims": FROZEN_STEP_TRAJECTORY_STAGE_NONCLAIMS,
    }
    if elapsed_s is not None:
        payload["elapsed_s"] = float(elapsed_s)
    if started_perf_counter_s is not None:
        payload["started_perf_counter_s"] = float(started_perf_counter_s)
        payload["timing_anchor_role"] = "process_local_monotonic_debug_only"
    if soft_deadline_payload is not None:
        payload["soft_deadline"] = dict(soft_deadline_payload)
    if error_type is not None:
        payload["error_type"] = str(error_type)
    return payload


def _phase6_soft_deadline_state(
    *,
    stage_start_perf_counter_s: float,
    timeout_budget_s: float | None,
    public_timeout_started_perf_counter_s: float | None = None,
    reserve_s: float = _FROZEN_STEP_TRAJECTORY_SOFT_DEADLINE_RESERVE_S,
) -> Mapping[str, Any]:
    if timeout_budget_s is None:
        return {
            "enabled": False,
            "hmc_mechanics_exposed": False,
            "reports_posterior_convergence": False,
        }
    budget = float(timeout_budget_s)
    reserve = max(0.0, min(float(reserve_s), budget * 0.5))
    now = time.perf_counter()
    stage_elapsed = max(0.0, now - float(stage_start_perf_counter_s))
    anchor = (
        float(stage_start_perf_counter_s)
        if public_timeout_started_perf_counter_s is None
        else float(public_timeout_started_perf_counter_s)
    )
    elapsed = max(0.0, now - anchor)
    remaining = budget - elapsed
    return {
        "enabled": True,
        "timeout_budget_s": budget,
        "reserve_s": reserve,
        "elapsed_s": elapsed,
        "remaining_s": remaining,
        "within_closeout_window": remaining <= reserve,
        "deadline_clock_scope": (
            "phase6_stage_local"
            if public_timeout_started_perf_counter_s is None
            else "public_one_call_global"
        ),
        "stage_elapsed_s": stage_elapsed,
        "stage_remaining_s": budget - stage_elapsed,
        "hmc_mechanics_exposed": False,
        "reports_posterior_convergence": False,
    }


def _phase6_next_candidate_soft_deadline_veto(
    *,
    stage_start_perf_counter_s: float,
    timeout_budget_s: float | None,
    public_timeout_started_perf_counter_s: float | None = None,
    completed_elapsed_s: Sequence[float],
) -> Mapping[str, Any] | None:
    if timeout_budget_s is None:
        return None
    state = dict(
        _phase6_soft_deadline_state(
            stage_start_perf_counter_s=stage_start_perf_counter_s,
            timeout_budget_s=timeout_budget_s,
            public_timeout_started_perf_counter_s=public_timeout_started_perf_counter_s,
        )
    )
    completed = tuple(float(value) for value in completed_elapsed_s)
    if not completed:
        estimated_next_s = _FROZEN_STEP_TRAJECTORY_SOFT_DEADLINE_RESERVE_S
    else:
        estimated_next_s = max(completed) * _FROZEN_STEP_TRAJECTORY_SOFT_DEADLINE_SAFETY_MULTIPLIER
    closeout_required = bool(
        state["within_closeout_window"]
        or float(state["remaining_s"]) <= estimated_next_s + float(state["reserve_s"])
    )
    if not closeout_required:
        return None
    return {
        **state,
        "estimated_next_candidate_s": float(estimated_next_s),
        "completed_candidate_elapsed_count": len(completed),
        "closeout_required_before_next_candidate": True,
        "diagnostic_role": "public_timeout_closeout_hard_veto",
        "hmc_mechanics_exposed": False,
        "reports_posterior_convergence": False,
        "reports_sampler_superiority": False,
        "reports_default_readiness": False,
        "reports_gpu_or_xla_readiness": False,
    }


def _phase7_verification_acceptance_budget_blocker(
    *,
    config: HMCTuneVerifyRepairLoopConfig,
    attempt_state: "_HMCPhaseAttemptState | None",
    next_attempt_policy: "_HMCAttemptBudgetPolicy",
) -> Mapping[str, Any] | None:
    if config.public_timeout_budget_s is None or attempt_state is None:
        return None
    budget_guard_repair_triggers = {
        _PHASE7_VERIFICATION_ACCEPTANCE_REPAIR_TRIGGER,
        _PHASE6_TRAJECTORY_ACCEPTANCE_REPAIR_TRIGGER,
    }
    if (
        attempt_state.verification_repair_trigger
        not in budget_guard_repair_triggers
        or not attempt_state.verification_repair_applied
        or attempt_state.verification_acceptance_relation
        not in {"below_acceptance_band", "above_acceptance_band"}
    ):
        return None
    budget = float(config.public_timeout_budget_s)
    anchor = (
        time.perf_counter()
        if config.public_timeout_started_perf_counter_s is None
        else float(config.public_timeout_started_perf_counter_s)
    )
    elapsed = max(0.0, time.perf_counter() - anchor)
    remaining = budget - elapsed
    reserve = max(0.0, min(_FROZEN_STEP_TRAJECTORY_SOFT_DEADLINE_RESERVE_S, budget * 0.5))
    # The next attempt must at least survive the public work before Phase 6 and
    # the first Phase 6 candidate preflight.  Phase 6 uses one reserve as the
    # no-candidate timing estimate; add a public lower-bound reserve for the
    # retry's Phase 4/5 overhead so the outer loop does not spend work whose
    # likely outcome is an immediate Phase 6 timeout closeout.
    estimated_next_candidate_s = reserve
    estimated_pre_phase6_retry_overhead_s = (
        reserve * _PHASE7_VERIFICATION_ACCEPTANCE_RETRY_PRE_PHASE6_MIN_RESERVES
    )
    estimated_minimum_next_attempt_s = (
        estimated_pre_phase6_retry_overhead_s + estimated_next_candidate_s
    )
    closeout_required = remaining <= reserve + estimated_minimum_next_attempt_s
    if not closeout_required:
        return None
    return {
        "schema": "bayesfilter.hmc_phase7_verification_acceptance_budget_blocker.v1",
        "classification": _PHASE7_VERIFICATION_ACCEPTANCE_BUDGET_BLOCKED,
        "previous_verification_acceptance_relation": (
            attempt_state.verification_acceptance_relation
        ),
        "verification_repair_trigger": attempt_state.verification_repair_trigger,
        "verification_repair_applied": True,
        "next_attempt_index": int(next_attempt_policy.attempt_index),
        "next_attempt_public_budget_class": next_attempt_policy.public_budget_class,
        "next_attempt_public_budget_cap": next_attempt_policy.public_budget_cap,
        "next_attempt_budget_is_public_policy": (
            next_attempt_policy.public_budget_class is not None
        ),
        "timeout_budget_s": budget,
        "elapsed_s": elapsed,
        "remaining_s": remaining,
        "reserve_s": reserve,
        "estimated_next_candidate_s": estimated_next_candidate_s,
        "estimated_pre_phase6_retry_overhead_s": estimated_pre_phase6_retry_overhead_s,
        "estimated_pre_phase6_retry_overhead_reserve_multiplier": (
            _PHASE7_VERIFICATION_ACCEPTANCE_RETRY_PRE_PHASE6_MIN_RESERVES
        ),
        "estimated_minimum_next_attempt_s": estimated_minimum_next_attempt_s,
        "deadline_clock_scope": (
            "phase7_loop_local"
            if config.public_timeout_started_perf_counter_s is None
            else "public_one_call_global"
        ),
        "closeout_required_before_next_attempt": True,
        "diagnostic_role": _PHASE7_VERIFICATION_ACCEPTANCE_BUDGET_BLOCKED,
        "progress_only": True,
        "hmc_mechanics_exposed": False,
        "reports_posterior_convergence": False,
        "reports_sampler_superiority": False,
        "reports_default_readiness": False,
        "reports_external_client_scientific_claim": False,
        "reports_gpu_or_xla_readiness": False,
        "nonclaims": TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS,
    }


def _emit_phase7_progress(
    callback: LoopProgressCallback | None,
    stage: str,
    *,
    attempt_index: int,
    budget_policy: _HMCAttemptBudgetPolicy | None,
    started: bool = False,
    completed: bool = False,
    extra: Mapping[str, Any] | None = None,
) -> None:
    if callback is None:
        return
    payload: dict[str, Any] = {
        "stage": str(stage),
        "attempt_index": int(attempt_index),
        "started": bool(started),
        "completed": bool(completed),
        "bounded_public_budget_payload": _phase7_progress_budget_payload(
            budget_policy
        ),
        "progress_only": True,
        "hmc_mechanics_exposed": False,
        "reports_posterior_convergence": False,
        "reports_sampler_superiority": False,
        "reports_default_readiness": False,
        "reports_external_client_scientific_claim": False,
        "reports_gpu_or_xla_readiness": False,
        "nonclaims": TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS,
    }
    if extra is not None:
        payload["extra"] = dict(extra)
        if (
            extra.get("substage_budget_details_exposed") is True
            and payload["bounded_public_budget_payload"] is not None
        ):
            bounded = dict(payload["bounded_public_budget_payload"])
            bounded["substage_budget_details_exposed"] = True
            payload["bounded_public_budget_payload"] = bounded
    callback(str(stage), payload)


@dataclass(frozen=True)
class _HMCPhaseAttemptState:
    mass_artifact_payload: Mapping[str, Any] | None = None
    mass_artifact_signature: str | None = None
    selected_step_size: float | None = None
    selected_step_hash: str | None = None
    selected_num_leapfrog_steps: int | None = None
    selected_trajectory_hash: str | None = None
    verification_acceptance_rate: float | None = None
    verification_acceptance_relation: str = "unavailable"
    verification_repair_trigger: str | None = None
    verification_repair_source: str | None = None
    verification_repair_step_size: float | None = None
    verification_repair_step_hash: str | None = None
    verification_repair_applied: bool = False
    handoff_stage: str = "initial"

    def __post_init__(self) -> None:
        payload = (
            None if self.mass_artifact_payload is None else dict(self.mass_artifact_payload)
        )
        object.__setattr__(self, "mass_artifact_payload", payload)
        mass_signature = (
            None
            if self.mass_artifact_signature is None
            else str(self.mass_artifact_signature)
        )
        object.__setattr__(self, "mass_artifact_signature", mass_signature)
        step = None if self.selected_step_size is None else float(self.selected_step_size)
        if step is not None and (not np.isfinite(step) or step <= 0.0):
            raise ValueError("attempt handoff selected_step_size must be positive")
        object.__setattr__(self, "selected_step_size", step)
        step_hash = None if self.selected_step_hash is None else str(self.selected_step_hash)
        object.__setattr__(self, "selected_step_hash", step_hash)
        leapfrog = (
            None
            if self.selected_num_leapfrog_steps is None
            else int(self.selected_num_leapfrog_steps)
        )
        if leapfrog is not None and leapfrog <= 0:
            raise ValueError("attempt handoff selected_num_leapfrog_steps must be positive")
        object.__setattr__(self, "selected_num_leapfrog_steps", leapfrog)
        trajectory_hash = (
            None
            if self.selected_trajectory_hash is None
            else str(self.selected_trajectory_hash)
        )
        object.__setattr__(self, "selected_trajectory_hash", trajectory_hash)
        stage = str(self.handoff_stage)
        if stage not in {"initial", "phase4", "phase5_repair", "phase5_selected", "phase6"}:
            raise ValueError("attempt handoff_stage is invalid")
        object.__setattr__(self, "handoff_stage", stage)
        acceptance = (
            None
            if self.verification_acceptance_rate is None
            else float(self.verification_acceptance_rate)
        )
        if acceptance is not None and not np.isfinite(acceptance):
            raise ValueError("verification_acceptance_rate must be finite when provided")
        object.__setattr__(self, "verification_acceptance_rate", acceptance)
        relation = str(self.verification_acceptance_relation)
        if relation not in {
            "below_acceptance_band",
            "inside_acceptance_band",
            "above_acceptance_band",
            "unavailable",
        }:
            raise ValueError("verification_acceptance_relation is invalid")
        object.__setattr__(self, "verification_acceptance_relation", relation)
        trigger = (
            None
            if self.verification_repair_trigger is None
            else str(self.verification_repair_trigger)
        )
        if trigger is not None and trigger not in {
            _PHASE6_TRAJECTORY_ACCEPTANCE_REPAIR_TRIGGER,
            _PHASE7_VERIFICATION_ACCEPTANCE_REPAIR_TRIGGER,
        }:
            raise ValueError("verification_repair_trigger is invalid")
        object.__setattr__(self, "verification_repair_trigger", trigger)
        source = (
            None
            if self.verification_repair_source is None
            else str(self.verification_repair_source)
        )
        if source is not None and not source:
            raise ValueError("verification_repair_source must be non-empty when provided")
        object.__setattr__(self, "verification_repair_source", source)
        repair_step = (
            None
            if self.verification_repair_step_size is None
            else float(self.verification_repair_step_size)
        )
        if repair_step is not None and (not np.isfinite(repair_step) or repair_step <= 0.0):
            raise ValueError("verification_repair_step_size must be positive and finite")
        repair_hash = (
            None
            if self.verification_repair_step_hash is None
            else str(self.verification_repair_step_hash)
        )
        if (repair_step is None) != (repair_hash is None):
            raise ValueError("verification repair step size/hash must be paired")
        object.__setattr__(self, "verification_repair_step_size", repair_step)
        object.__setattr__(self, "verification_repair_step_hash", repair_hash)
        repair_applied = bool(self.verification_repair_applied)
        if repair_applied and (
            trigger is None
            or relation not in {"below_acceptance_band", "above_acceptance_band"}
            or repair_step is None
            or repair_hash is None
        ):
            raise ValueError("verification repair handoff is incomplete")
        object.__setattr__(self, "verification_repair_applied", repair_applied)

    @property
    def has_mass_handoff(self) -> bool:
        return (
            self.mass_artifact_payload is not None
            and self.mass_artifact_signature is not None
        )

    @property
    def has_step_handoff(self) -> bool:
        return (
            self.has_mass_handoff
            and self.selected_step_size is not None
            and self.selected_step_hash is not None
        )

    @property
    def has_required_repair_handoff(self) -> bool:
        return self.has_stage_repair_handoff

    @property
    def has_stage_repair_handoff(self) -> bool:
        if self.handoff_stage == "phase4":
            return self.has_mass_handoff
        if self.handoff_stage in {"phase5_repair", "phase5_selected"}:
            return self.has_step_handoff
        if self.handoff_stage != "phase6":
            return False
        return (
            self.mass_artifact_payload is not None
            and self.mass_artifact_signature is not None
            and self.selected_step_size is not None
            and self.selected_step_hash is not None
            and self.selected_num_leapfrog_steps is not None
            and self.selected_trajectory_hash is not None
        )

    @property
    def has_final_kernel_handoff(self) -> bool:
        return (
            self.mass_artifact_payload is not None
            and self.mass_artifact_signature is not None
            and self.selected_step_size is not None
            and self.selected_step_hash is not None
            and self.selected_num_leapfrog_steps is not None
            and self.selected_trajectory_hash is not None
        )

    def payload(self) -> Mapping[str, Any]:
        return {
            "handoff_stage": self.handoff_stage,
            "mass_artifact_payload": self.mass_artifact_payload,
            "mass_artifact_signature": self.mass_artifact_signature,
            "selected_step_size": self.selected_step_size,
            "selected_step_hash": self.selected_step_hash,
            "selected_num_leapfrog_steps": self.selected_num_leapfrog_steps,
            "selected_trajectory_hash": self.selected_trajectory_hash,
            "verification_acceptance_rate": self.verification_acceptance_rate,
            "verification_acceptance_relation": self.verification_acceptance_relation,
            "verification_repair_trigger": self.verification_repair_trigger,
            "verification_repair_source": self.verification_repair_source,
            "verification_repair_step_size": self.verification_repair_step_size,
            "verification_repair_step_hash": self.verification_repair_step_hash,
            "verification_repair_applied": self.verification_repair_applied,
            "mass_handoff_complete": self.has_mass_handoff,
            "step_handoff_complete": self.has_step_handoff,
            "stage_repair_handoff_complete": self.has_stage_repair_handoff,
            "required_private_handoff_complete": self.has_required_repair_handoff,
            "final_kernel_handoff_complete": self.has_final_kernel_handoff,
        }


def _default_attempt_budget_policy(
    target_dimension: int,
    attempt_index: int,
) -> _HMCAttemptBudgetPolicy:
    dimension = int(target_dimension)
    if dimension <= 0:
        raise ValueError("target_dimension must be positive")
    index = int(attempt_index)
    if index < 0:
        raise ValueError("attempt_index must be non-negative")
    budget0 = min(
        _SERIOUS_TUNING_MAX_INITIAL_BUDGET,
        max(
            _SERIOUS_TUNING_MIN_RUN_BUDGET,
            _SERIOUS_TUNING_DIMENSION_FACTOR * dimension,
        ),
    )
    budget = min(_SERIOUS_TUNING_MAX_TUNE_BUDGET, int(budget0 * (2 ** index)))
    phase5_screen = max(32, _ceil_div(budget, 4))
    phase6_screen = max(32, _ceil_div(budget, 4))
    verification_results = max(64, _ceil_div(budget, 2))
    return _HMCAttemptBudgetPolicy(
        target_dimension=dimension,
        attempt_index=index,
        budget=budget,
        phase4_warmup_steps=budget,
        phase5_tune_budgets=(
            _ceil_div(budget, 4),
            _ceil_div(budget, 2),
            budget,
        ),
        phase5_screen_num_results=phase5_screen,
        phase5_screen_burnin_steps=max(8, _ceil_div(phase5_screen, 4)),
        phase6_screen_num_results=phase6_screen,
        phase6_screen_burnin_steps=max(8, _ceil_div(phase6_screen, 4)),
        verification_num_results=verification_results,
        verification_num_burnin_steps=max(16, _ceil_div(verification_results, 4)),
    )


def _phase7_attempt_seed(root_seed: tuple[int, int], attempt_index: int) -> tuple[int, int]:
    return _derive_seed(root_seed, stage_index=10 + int(attempt_index))


def _phase7_windowed_stage_config(
    config: HMCTuneVerifyRepairLoopConfig,
    *,
    attempt_index: int,
) -> HMCWindowedMassStageConfig:
    return HMCWindowedMassStageConfig(
        target_accept_prob=config.target_accept_prob,
        seed=_derive_seed(_phase7_attempt_seed(config.seed, attempt_index), stage_index=0),
        chain_execution_mode=config.chain_execution_mode,
        use_xla=config.use_xla,
        target_scope=config.target_scope,
        target_status_trace_policy=config.target_status_trace_policy,
        source=config.source,
    )


def _phase7_fixed_step_stage_config(
    config: HMCTuneVerifyRepairLoopConfig,
    *,
    attempt_index: int,
) -> HMCFixedMassStepStageConfig:
    return HMCFixedMassStepStageConfig(
        target_accept_prob=config.target_accept_prob,
        acceptance_band=config.acceptance_band,
        repair_band=config.repair_band,
        seed=_derive_seed(_phase7_attempt_seed(config.seed, attempt_index), stage_index=1),
        chain_execution_mode=config.chain_execution_mode,
        use_xla=config.use_xla,
        target_scope=config.target_scope,
        target_status_trace_policy=config.target_status_trace_policy,
        source=config.source,
    )


def _phase7_trajectory_stage_config(
    config: HMCTuneVerifyRepairLoopConfig,
    *,
    attempt_index: int,
) -> HMCFrozenStepTrajectoryStageConfig:
    return HMCFrozenStepTrajectoryStageConfig(
        target_accept_prob=config.target_accept_prob,
        acceptance_band=config.acceptance_band,
        seed=_derive_seed(_phase7_attempt_seed(config.seed, attempt_index), stage_index=2),
        chain_execution_mode=config.chain_execution_mode,
        use_xla=config.use_xla,
        target_scope=config.target_scope,
        target_status_trace_policy=config.target_status_trace_policy,
        public_timeout_budget_s=config.public_timeout_budget_s,
        public_timeout_started_perf_counter_s=config.public_timeout_started_perf_counter_s,
        source=config.source,
    )


def _build_bootstrap_fixed_mass_adapter(
    *,
    adapter: Any,
    mass_artifact: PrecomputedMassArtifact,
    mass_signature: str,
    target_scope: str,
    nonclaims: Sequence[str] = BOOTSTRAP_SCREEN_NONCLAIMS,
) -> _BootstrapFixedMassLatentValueScoreAdapter:
    transform = mass_artifact.build_latent_transform()
    latent_signature = program_signature(
        {
            "runtime": (
                "bayesfilter.inference.hmc_kernel_tuning."
                "_BootstrapFixedMassLatentValueScoreAdapter"
            ),
            "position_adapter_signature": stable_adapter_signature(adapter),
            "mass_artifact_signature": mass_signature,
            "target_scope": target_scope,
            "transform": transform.signature_payload(),
        }
    )
    return _BootstrapFixedMassLatentValueScoreAdapter(
        base_adapter=adapter,
        transform=transform,
        target_scope=target_scope,
        adapter_signature=latent_signature,
        nonclaims=nonclaims,
    )


def _phase4_latent_adapter_for_step_stage(
    *,
    adapter: Any,
    geometry: HMCGeometryInitializationResult,
    windowed_stage: HMCWindowedMassStageResult,
    target_scope: str,
) -> _BootstrapFixedMassLatentValueScoreAdapter:
    mass_signature = _mass_artifact_signature(geometry.mass_artifact)
    if mass_signature != geometry.mass_artifact_signature:
        raise ValueError("geometry mass artifact signature mismatch")
    if windowed_stage.windowed_mass_result is None:
        raise ValueError("Phase 4 result missing windowed mass artifact")
    phase4_initial_mass = windowed_stage.windowed_mass_result.final_mass_artifact
    if not isinstance(phase4_initial_mass, PrecomputedMassArtifact):
        raise TypeError("Phase 4 final mass artifact must be PrecomputedMassArtifact")
    if phase4_initial_mass.adapter_signature != windowed_stage.hmc_adapter_signature:
        raise ValueError("Phase 4 initial latent mass signature mismatch")
    hmc_adapter = _build_bootstrap_fixed_mass_adapter(
        adapter=adapter,
        mass_artifact=geometry.mass_artifact,
        mass_signature=mass_signature,
        target_scope=target_scope,
        nonclaims=FIXED_MASS_STEP_STAGE_NONCLAIMS,
    )
    if stable_adapter_signature(hmc_adapter) != windowed_stage.hmc_adapter_signature:
        raise ValueError("rebuilt Phase 4 HMC adapter signature mismatch")
    return hmc_adapter


def _phase4_adapted_mass_artifact(
    windowed_stage: HMCWindowedMassStageResult,
) -> PrecomputedMassArtifact:
    windowed_result = windowed_stage.windowed_mass_result
    if windowed_result is None or windowed_result.final_mass_artifact is None:
        raise ValueError("Phase 4 result does not carry final mass artifact")
    artifact = windowed_result.final_mass_artifact
    if not isinstance(artifact, PrecomputedMassArtifact):
        raise TypeError("Phase 4 final mass artifact must be PrecomputedMassArtifact")
    return artifact


def _selected_bootstrap_kernel_from_windowed_stage(
    windowed_stage: HMCWindowedMassStageResult,
    *,
    bootstrap: HMCBootstrapScreenResult,
) -> Mapping[str, Any]:
    selected = bootstrap.selected_kernel_payload
    if selected is None:
        raise ValueError("Phase 5 requires selected bootstrap kernel payload")
    selected_hash = bootstrap.selected_kernel_hash
    if selected_hash != windowed_stage.selected_bootstrap_kernel_hash:
        raise ValueError("Phase 5 selected bootstrap kernel hash mismatch")
    payload = None
    if windowed_stage.diagnostic_run_config_payload is not None:
        payload = windowed_stage.diagnostic_run_config_payload
    if payload is None:
        raise ValueError("Phase 4 result missing diagnostic run config payload")
    step_size = payload.get("step_size")
    leapfrog = payload.get("num_leapfrog_steps")
    if step_size is None or leapfrog is None:
        raise ValueError("Phase 4 diagnostic config missing selected kernel fields")
    if float(step_size) != float(selected["step_size"]):
        raise ValueError("Phase 4 diagnostic step does not match bootstrap selection")
    if int(leapfrog) != int(selected["num_leapfrog_steps"]):
        raise ValueError("Phase 4 diagnostic L does not match bootstrap selection")
    return {"step_size": float(step_size), "num_leapfrog_steps": int(leapfrog)}


def _fixed_mass_step_stage_ladder_config(
    config: HMCFixedMassStepStageConfig,
    *,
    initial_step: float,
    num_leapfrog_steps: int,
    target_scope: str,
    attempt_budget_policy: _HMCAttemptBudgetPolicy | None = None,
) -> FixedMassHMCTuningBudgetLadderConfig:
    if attempt_budget_policy is None:
        budget_schedule = _FIXED_MASS_STAGE_TEST_BUDGET_SCHEDULE
        tune_num_results = _FIXED_MASS_STAGE_TUNE_NUM_RESULTS
        screen_num_results = _FIXED_MASS_STAGE_SCREEN_NUM_RESULTS
        screen_num_burnin_steps = _FIXED_MASS_STAGE_SCREEN_BURNIN_STEPS
    else:
        budget_schedule = attempt_budget_policy.phase5_tune_budgets
        tune_num_results = _FIXED_MASS_STAGE_TUNE_NUM_RESULTS
        screen_num_results = attempt_budget_policy.phase5_screen_num_results
        screen_num_burnin_steps = attempt_budget_policy.phase5_screen_burnin_steps
    return FixedMassHMCTuningBudgetLadderConfig(
        budget_schedule=budget_schedule,
        initial_step_size=float(initial_step),
        num_leapfrog_steps=int(num_leapfrog_steps),
        target_accept_prob=config.target_accept_prob,
        acceptance_band=config.acceptance_band,
        repair_band=config.repair_band,
        tune_num_results=tune_num_results,
        screen_num_results=screen_num_results,
        screen_num_burnin_steps=screen_num_burnin_steps,
        tune_seed_base=_derive_seed(config.seed, stage_index=0),
        screen_seed_base=_derive_seed(config.seed, stage_index=1),
        chain_execution_mode=config.chain_execution_mode,
        use_xla=config.use_xla,
        target_scope=target_scope,
        target_status_trace_policy=config.target_status_trace_policy,
        source=config.source,
    )


def _fixed_mass_step_initial_step(
    windowed_stage: HMCWindowedMassStageResult,
    *,
    attempt_state: _HMCPhaseAttemptState | None,
) -> float:
    if (
        attempt_state is not None
        and attempt_state.verification_repair_applied
        and attempt_state.verification_repair_step_size is not None
    ):
        return float(attempt_state.verification_repair_step_size)
    if attempt_state is not None and attempt_state.selected_step_size is not None:
        return float(attempt_state.selected_step_size)
    if windowed_stage.candidate_step_size is None:
        raise ValueError("fixed-mass step stage requires candidate step size")
    return float(windowed_stage.candidate_step_size)


def _fixed_mass_step_initial_state_factory(
    dimension: int,
) -> Callable[[tuple[int, int], str, int, int, float], np.ndarray]:
    dim = int(dimension)
    if dim <= 0:
        raise ValueError("initial state dimension must be positive")

    def factory(
        _seed: tuple[int, int],
        _stage: str,
        _round_index: int,
        _budget: int,
        _step: float,
    ) -> np.ndarray:
        return np.zeros(dim, dtype=float)

    return factory


def _fixed_mass_step_frozen_mass_invariant(
    before: str,
    after: str,
) -> Mapping[str, Any]:
    return {
        "passed": before == after,
        "before_signature": before,
        "after_signature": after,
        "signature_includes_arrays": True,
        "mass_update_allowed": False,
        "role": "hard_veto",
    }


def _fixed_mass_step_stage_diagnostics(
    ladder_result: FixedMassHMCTuningBudgetLadderResult | None,
    *,
    run_error: Exception | None,
    hard_vetoes: tuple[str, ...],
) -> Mapping[str, Any]:
    if ladder_result is None:
        return {
            "passed": False,
            "ladder_final_status": None,
            "ladder_round_count": 0,
            "selected_round_index": None,
            "selected_step_size": None,
            "hard_vetoes_from_ladder": (),
            "repair_triggers_from_ladder": (),
            "run_error_type": None if run_error is None else type(run_error).__name__,
            "run_error_message": None if run_error is None else str(run_error),
            "reports_posterior_convergence": False,
            "nonclaims": FIXED_MASS_STEP_STAGE_NONCLAIMS,
        }
    hard_from_ladder: list[str] = []
    continuation_from_ladder: list[str] = []
    repair_from_ladder: list[str] = []
    for round_result in ladder_result.rounds:
        hard_from_ladder.extend(round_result.hard_vetoes)
        continuation_from_ladder.extend(round_result.continuation_vetoes)
        if round_result.classification in {
            "acceptance_repair",
            "promotion_veto_repair",
        }:
            repair_from_ladder.extend(round_result.repair_triggers)
    selected = ladder_result.selected_round
    return {
        "passed": ladder_result.passed,
        "ladder_final_status": ladder_result.final_status,
        "ladder_round_count": len(ladder_result.rounds),
        "selected_round_index": ladder_result.selected_round_index,
        "selected_step_size": None if selected is None else selected.tuned_step_size,
        "selected_budget": None if selected is None else selected.budget,
        "hard_vetoes_from_ladder": tuple(dict.fromkeys(hard_from_ladder)),
        "continuation_vetoes_from_ladder": tuple(
            dict.fromkeys(continuation_from_ladder)
        ),
        "repair_triggers_from_ladder": tuple(dict.fromkeys(repair_from_ladder)),
        "stage_hard_vetoes_before_ladder": hard_vetoes,
        "reports_posterior_convergence": False,
        "nonclaims": FIXED_MASS_STEP_STAGE_NONCLAIMS,
    }


def _required_selected_step_size(
    fixed_mass_step_stage: HMCFixedMassStepStageResult,
) -> float:
    step = fixed_mass_step_stage.selected_step_size
    if step is None:
        raise ValueError("frozen-step trajectory requires selected step size")
    value = float(step)
    if not np.isfinite(value) or value <= 0.0:
        raise ValueError("frozen-step trajectory selected step must be positive")
    return value


def _frozen_step_trajectory_candidate_generation(
    *,
    geometry: HMCGeometryInitializationResult,
    selected_step_size: float,
    fixed_bootstrap_l: int,
    attempt_state: _HMCPhaseAttemptState | None = None,
) -> Mapping[str, Any]:
    step = float(selected_step_size)
    if not np.isfinite(step) or step <= 0.0:
        raise ValueError("selected_step_size must be positive and finite")
    target = float(geometry.target_trajectory_length)
    if not np.isfinite(target) or target <= 0.0:
        raise ValueError("target trajectory length must be positive and finite")
    center = int(np.ceil(target / step))
    if center <= 0:
        raise ValueError("formula-derived trajectory center L must be positive")
    raw_candidates_list = [
        center + int(offset) for offset in _FROZEN_STEP_TRAJECTORY_CANDIDATE_OFFSETS
    ]
    raw_candidates_list.append(int(fixed_bootstrap_l))
    previous_l = (
        None if attempt_state is None else attempt_state.selected_num_leapfrog_steps
    )
    if previous_l is not None:
        raw_candidates_list.append(int(previous_l))
    verification_repair_applied = bool(
        attempt_state is not None
        and attempt_state.verification_repair_applied
        and attempt_state.verification_repair_trigger
        in {
            _PHASE6_TRAJECTORY_ACCEPTANCE_REPAIR_TRIGGER,
            _PHASE7_VERIFICATION_ACCEPTANCE_REPAIR_TRIGGER,
        }
    )
    if verification_repair_applied and previous_l is not None:
        raw_candidates_list.extend(
            int(previous_l) + int(offset)
            for offset in _FROZEN_STEP_TRAJECTORY_REPAIR_NEIGHBORHOOD_OFFSETS
        )
    raw_candidates = tuple(raw_candidates_list)
    local_max = max(
        _GEOMETRY_MIN_LEAPFROG,
        min(_GEOMETRY_MAX_LEAPFROG, center + _FROZEN_STEP_TRAJECTORY_CENTER_SLACK),
    )
    clamped = tuple(
        int(np.clip(item, _GEOMETRY_MIN_LEAPFROG, local_max))
        for item in raw_candidates
    )
    candidates = tuple(sorted(dict.fromkeys(clamped)))
    return {
        "formula": "L*=ceil(geometry.target_trajectory_length / selected_step_size)",
        "center_candidate_l": center,
        "selected_step_size": step,
        "target_trajectory_length": target,
        "fixed_bootstrap_num_leapfrog_steps": int(fixed_bootstrap_l),
        "previous_attempt_center_l": previous_l,
        "neighborhood_offsets": _FROZEN_STEP_TRAJECTORY_CANDIDATE_OFFSETS,
        "verification_repair_neighborhood_applied": verification_repair_applied,
        "verification_repair_neighborhood_offsets": (
            _FROZEN_STEP_TRAJECTORY_REPAIR_NEIGHBORHOOD_OFFSETS
            if verification_repair_applied
            else ()
        ),
        "raw_candidate_l_values": raw_candidates,
        "internal_min_leapfrog": _GEOMETRY_MIN_LEAPFROG,
        "internal_max_leapfrog": _GEOMETRY_MAX_LEAPFROG,
        "local_max_leapfrog": local_max,
        "local_max_leapfrog_formula": "min(internal_max_leapfrog, center_candidate_l + 10)",
        "candidate_l_values": candidates,
        "candidate_order": "ascending_clamped_l",
        "candidate_mechanics_are_diagnostic_telemetry_only": True,
    }


def _frozen_step_trajectory_screen_config(
    config: HMCFrozenStepTrajectoryStageConfig,
    *,
    seed: tuple[int, int],
    step: float,
    leapfrogs: int,
    target_scope: str,
    attempt_budget_policy: _HMCAttemptBudgetPolicy | None = None,
) -> FullChainHMCConfig:
    if attempt_budget_policy is None:
        num_results = _FROZEN_STEP_TRAJECTORY_SCREEN_NUM_RESULTS
        burnin_steps = _FROZEN_STEP_TRAJECTORY_SCREEN_BURNIN_STEPS
    else:
        num_results = attempt_budget_policy.phase6_screen_num_results
        burnin_steps = attempt_budget_policy.phase6_screen_burnin_steps
    return FullChainHMCConfig(
        num_results=num_results,
        num_burnin_steps=burnin_steps,
        step_size=float(step),
        num_leapfrog_steps=int(leapfrogs),
        seed=seed,
        use_xla=config.use_xla,
        trace_policy="standard",
        target_status_trace_policy=config.target_status_trace_policy,
        target_scope=target_scope,
        chain_execution_mode=config.chain_execution_mode,
    )


def _frozen_step_trajectory_diagnostics_payload(
    run_result: FullChainHMCRunResult,
) -> Mapping[str, Any]:
    payload = dict(_bootstrap_diagnostics_payload(run_result))
    screen = dict(payload.get("screen_diagnostic", {}))
    roles = dict(screen.get("diagnostic_roles", {}))
    roles["screen"] = "frozen-step trajectory fixed-kernel screen only"
    screen["diagnostic_roles"] = roles
    screen["nonclaims"] = FROZEN_STEP_TRAJECTORY_STAGE_NONCLAIMS
    payload["screen_diagnostic"] = screen
    payload["diagnostic_context"] = "frozen_step_trajectory_candidate_screen"
    payload["nonclaims"] = FROZEN_STEP_TRAJECTORY_STAGE_NONCLAIMS
    return payload


def _run_kernel_stage_with_optional_reusable_route(
    *,
    run_full_chain: RunFullChainFn,
    runner_cache: dict[str, Any],
    runner_contract_payloads: dict[str, Mapping[str, Any]],
    route_events: list[Mapping[str, Any]],
    route_name: str,
    route_scope: str,
    adapter: Any,
    initial_state: Any,
    config: FullChainHMCConfig,
    hmc_adapter_signature: str,
    target_dimension: int,
    mass_signature: str,
    event_payload: Mapping[str, Any],
) -> FullChainHMCRunResult:
    if run_full_chain is not run_full_chain_tfp_hmc or config.chain_execution_mode != "tf_function":
        route_event = {
            **dict(event_payload),
            "route_scope": str(route_scope),
            "route": "single_use_or_injected_runner",
            "static_contract_hash": None,
            "call_config_hash": stable_config_hash(config.signature_payload()),
            "runner_reused": False,
            "used_single_use_runner": run_full_chain is run_full_chain_tfp_hmc,
        }
        route_events.append(route_event)
        return run_full_chain(adapter, initial_state, config)

    contract_payload = _kernel_stage_reusable_static_contract_payload(
        config,
        hmc_adapter_signature=hmc_adapter_signature,
        target_dimension=target_dimension,
        mass_signature=mass_signature,
        initial_state=initial_state,
    )
    contract_hash = stable_config_hash(contract_payload)
    runner = runner_cache.get(contract_hash)
    runner_reused = runner is not None
    if runner is None:
        runner = build_reusable_full_chain_tfp_hmc_runner(
            adapter,
            initial_state,
            config,
        )
        runner_cache[contract_hash] = runner
        runner_contract_payloads[contract_hash] = contract_payload
    result = runner.run(
        current_state=initial_state,
        seed=config.seed,
        step_size=config.step_size,
    )
    route_event = {
        **dict(event_payload),
        "route_scope": str(route_scope),
        "route": str(route_name),
        "static_contract_hash": contract_hash,
        "call_config_hash": stable_config_hash(config.signature_payload()),
        "runner_reused": runner_reused,
        "used_single_use_runner": False,
    }
    route_events.append(route_event)
    metadata = {
        **dict(result.metadata),
        "kernel_stage_route": str(route_name),
        "kernel_stage_route_scope": str(route_scope),
        "kernel_stage_static_contract_hash": contract_hash,
        "kernel_stage_call_config_hash": route_event["call_config_hash"],
        "kernel_stage_runner_reused": runner_reused,
        "kernel_stage_static_contract_payload": contract_payload,
    }
    return FullChainHMCRunResult(
        samples=result.samples,
        trace=result.trace,
        diagnostics=result.diagnostics,
        metadata=metadata,
    )


def _kernel_stage_reusable_static_contract_payload(
    config: FullChainHMCConfig,
    *,
    hmc_adapter_signature: str,
    target_dimension: int,
    mass_signature: str,
    initial_state: Any,
) -> Mapping[str, Any]:
    payload = dict(config.signature_payload())
    payload.pop("seed", None)
    payload.pop("step_size", None)
    state_contract = _kernel_stage_reusable_state_template_contract(initial_state)
    return {
        "runner": "build_reusable_full_chain_tfp_hmc_runner",
        "hmc_adapter_signature": str(hmc_adapter_signature),
        "target_dimension": int(target_dimension),
        "mass_artifact_signature": str(mass_signature),
        "initial_state_shape": state_contract["initial_state_shape"],
        "initial_state_dtype": state_contract["initial_state_dtype"],
        "initial_state_dtype_source": state_contract["initial_state_dtype_source"],
        "static_config": payload,
        "dynamic_inputs": ("current_state", "seed", "step_size"),
    }


def _kernel_stage_reusable_state_template_contract(initial_state: Any) -> Mapping[str, Any]:
    import tensorflow as tf

    template = tf.cast(tf.convert_to_tensor(initial_state), tf.float64)
    if template.shape.rank is None:
        raise ValueError("reusable HMC runner requires static state rank")
    shape = template.shape.as_list()
    if any(dim is None for dim in shape):
        raise ValueError("reusable HMC runner requires fully static state shape")
    return {
        "initial_state_shape": tuple(int(dim) for dim in shape),
        "initial_state_dtype": template.dtype.name,
        "initial_state_dtype_source": "tf.cast(tf.convert_to_tensor(initial_state), tf.float64)",
    }


def _kernel_stage_runner_route_summary(
    *,
    active_route: str,
    events: Sequence[Mapping[str, Any]],
    contract_payloads: Mapping[str, Mapping[str, Any]],
    semantic_source: str,
    reuse_nonclaim: str,
) -> Mapping[str, Any]:
    return {
        "active_route": str(active_route),
        "semantic_source": str(semantic_source),
        "reusable_runner_build_count": len(contract_payloads),
        "distinct_static_runner_contract_count": len(contract_payloads),
        "single_use_build_count": sum(
            1 for item in events if item.get("used_single_use_runner") is True
        ),
        "injected_runner_call_count": sum(
            1
            for item in events
            if item.get("route") == "single_use_or_injected_runner"
            and item.get("used_single_use_runner") is False
        ),
        "round_route_events": tuple(dict(item) for item in events),
        "distinct_static_runner_contracts": tuple(
            {
                "static_contract_hash": contract_hash,
                "static_contract_payload": contract_payloads[contract_hash],
            }
            for contract_hash in sorted(contract_payloads)
        ),
        "fallback_to_single_use_runner": any(
            item.get("used_single_use_runner") is True for item in events
        )
        and active_route != "single_use_or_injected_runner",
        "fallback_status": (
            "none"
            if active_route != "single_use_or_injected_runner"
            and not any(item.get("used_single_use_runner") is True for item in events)
            else "inactive_reusable_route"
        ),
        "route_nonclaims": (
            "route telemetry is engineering evidence only",
            str(reuse_nonclaim),
            "does not establish posterior convergence or sampler superiority",
        ),
    }


def _frozen_step_trajectory_error_diagnostics(exc: Exception) -> Mapping[str, Any]:
    payload = dict(_bootstrap_error_diagnostics(exc))
    payload["screen_diagnostic"] = {
        **dict(payload.get("screen_diagnostic", {})),
        "diagnostic_roles": {"screen": "frozen-step trajectory runtime hard veto"},
        "nonclaims": FROZEN_STEP_TRAJECTORY_STAGE_NONCLAIMS,
    }
    payload["diagnostic_context"] = "frozen_step_trajectory_candidate_screen"
    payload["nonclaims"] = FROZEN_STEP_TRAJECTORY_STAGE_NONCLAIMS
    return payload


def _call_trajectory_screen_callback(
    callback: TrajectoryScreenCallback | None,
    *,
    round_payload: Mapping[str, Any],
    samples: Any,
    diagnostics: Mapping[str, Any],
) -> FixedMassHMCTuningBudgetCallbackResult:
    if callback is None:
        return FixedMassHMCTuningBudgetCallbackResult()
    try:
        raw = callback(round_payload, samples, diagnostics)
        return _coerce_trajectory_callback_result(raw)
    except Exception as exc:  # noqa: BLE001 - callback failures are fail-closed.
        return FixedMassHMCTuningBudgetCallbackResult(
            hard_vetoes=("callback_error",),
            diagnostics={
                "error_type": type(exc).__name__,
                "error_message": str(exc),
            },
        )


def _coerce_trajectory_callback_result(
    raw: Any,
) -> FixedMassHMCTuningBudgetCallbackResult:
    if raw is None:
        return FixedMassHMCTuningBudgetCallbackResult()
    if isinstance(raw, FixedMassHMCTuningBudgetCallbackResult):
        return raw
    if not isinstance(raw, Mapping):
        raise ValueError("screen_callback must return a mapping or callback result")
    return FixedMassHMCTuningBudgetCallbackResult(
        hard_vetoes=tuple(raw.get("hard_vetoes", ())),
        continuation_vetoes=tuple(raw.get("continuation_vetoes", ())),
        promotion_vetoes=tuple(raw.get("promotion_vetoes", ())),
        repair_triggers=tuple(raw.get("repair_triggers", ())),
        diagnostics=dict(raw.get("diagnostics", {})),
    )


def _classify_frozen_step_trajectory_candidate(
    config: HMCFrozenStepTrajectoryStageConfig,
    *,
    diagnostics: Mapping[str, Any],
    screen_error: Exception | None,
    callback_result: FixedMassHMCTuningBudgetCallbackResult,
) -> tuple[
    str,
    str,
    tuple[str, ...],
    tuple[str, ...],
    tuple[str, ...],
    tuple[str, ...],
]:
    hard_vetoes: list[str] = []
    if screen_error is not None:
        hard_vetoes.append("trajectory_screen_hmc_error")
    acceptance = diagnostics.get("acceptance_rate")
    if acceptance is None or not _finite_number(acceptance):
        hard_vetoes.append("trajectory_acceptance_missing_or_nonfinite")
    if diagnostics.get("runtime_finite") is not True:
        hard_vetoes.append("trajectory_runtime_missing_or_nonfinite")
    if diagnostics.get("log_accept_ratio_finite") is not True:
        hard_vetoes.append("trajectory_log_accept_nonfinite_or_missing")
    if diagnostics.get("samples_all_finite") is not True:
        hard_vetoes.append("trajectory_samples_nonfinite_or_missing")
    if diagnostics.get("target_log_prob_finite") is not True:
        hard_vetoes.append("trajectory_target_log_prob_nonfinite_or_missing")
    telemetry = diagnostics.get("target_status_telemetry")
    if isinstance(telemetry, Mapping) and telemetry.get("telemetry_failure_veto_bool"):
        hard_vetoes.append("trajectory_target_status_telemetry_failure")
    hard_vetoes.extend(callback_result.hard_vetoes)
    if hard_vetoes:
        return (
            "hard_veto",
            "hard_veto",
            tuple(dict.fromkeys(hard_vetoes)),
            callback_result.continuation_vetoes,
            callback_result.promotion_vetoes,
            callback_result.repair_triggers,
        )
    if callback_result.continuation_vetoes:
        return (
            "continuation_veto",
            "continuation_veto",
            (),
            callback_result.continuation_vetoes,
            callback_result.promotion_vetoes,
            callback_result.repair_triggers,
        )
    promotion_vetoes = tuple(callback_result.promotion_vetoes)
    repair_triggers = tuple(callback_result.repair_triggers)
    if promotion_vetoes or repair_triggers:
        return (
            "repair_or_retry",
            "promotion_veto_repair_trigger",
            (),
            (),
            promotion_vetoes,
            repair_triggers,
        )
    acceptance_value = float(acceptance)
    if config.acceptance_band[0] <= acceptance_value <= config.acceptance_band[1]:
        return "passed_screen", "trajectory_handoff_promotion_only", (), (), (), ()
    return (
        "repair_or_retry",
        "trajectory_acceptance_repair_trigger",
        (),
        (),
        (),
        ("acceptance_outside_pass_band",),
    )


def _select_frozen_step_trajectory_candidate(
    candidates: tuple[Mapping[str, Any], ...],
    *,
    config: HMCFrozenStepTrajectoryStageConfig,
    target_trajectory: float,
) -> int | None:
    passed = [
        (index, candidate)
        for index, candidate in enumerate(candidates)
        if candidate.get("classification") == "passed_screen"
    ]
    if not passed:
        return None
    lower, upper = config.acceptance_band
    midpoint = 0.5 * (lower + upper)
    selected_index, _selected = min(
        passed,
        key=lambda item: (
            abs(float(item[1]["diagnostics"]["acceptance_rate"]) - midpoint),
            abs(float(item[1]["trajectory_length"]) - float(target_trajectory)),
            float(item[1]["trajectory_length"]),
            int(item[1]["candidate_index"]),
        ),
    )
    return int(selected_index)


def _frozen_step_trajectory_selected_payload(
    *,
    config: HMCFrozenStepTrajectoryStageConfig,
    candidate: Mapping[str, Any],
    selected_step_hash: str,
    selected_bootstrap_kernel_hash: str,
    fixed_mass_step_stage_artifact_hash: str,
    adapted_mass_artifact_signature: str,
    phase4_hmc_adapter_signature: str,
    trajectory_hmc_adapter_signature: str,
    target_scope: str,
) -> Mapping[str, Any]:
    return {
        "runtime": "bayesfilter.inference.run_hmc_frozen_step_trajectory_stage",
        "step_size": float(candidate["step_size"]),
        "num_leapfrog_steps": int(candidate["num_leapfrog_steps"]),
        "trajectory_length": float(candidate["trajectory_length"]),
        "target_trajectory_length": float(candidate["target_trajectory_length"]),
        "target_trajectory_distance": float(candidate["target_trajectory_distance"]),
        "target_accept_prob": config.target_accept_prob,
        "acceptance_band": config.acceptance_band,
        "target_scope": target_scope,
        "selected_step_hash": str(selected_step_hash),
        "selected_bootstrap_kernel_hash": str(selected_bootstrap_kernel_hash),
        "fixed_mass_step_stage_artifact_hash": str(fixed_mass_step_stage_artifact_hash),
        "adapted_mass_artifact_signature": str(adapted_mass_artifact_signature),
        "phase4_hmc_adapter_signature": str(phase4_hmc_adapter_signature),
        "trajectory_hmc_adapter_signature": str(trajectory_hmc_adapter_signature),
        "screen_seed": candidate["seed"],
        "screen_config_payload": candidate["screen_config_payload"],
        "candidate_index": int(candidate["candidate_index"]),
        "candidate_mechanics_are_diagnostic_telemetry_only": True,
        "not_fresh_final_verification": True,
        "nonclaims": FROZEN_STEP_TRAJECTORY_STAGE_NONCLAIMS,
    }


def _frozen_step_trajectory_frozen_mass_invariant(
    before: str,
    after: str,
) -> Mapping[str, Any]:
    return {
        "passed": before == after,
        "before_signature": before,
        "after_signature": after,
        "signature_includes_arrays": True,
        "mass_update_allowed": False,
        "role": "hard_veto",
    }


def _frozen_step_trajectory_frozen_step_invariant(
    *,
    before: float,
    after: float,
) -> Mapping[str, Any]:
    return {
        "passed": float(before) == float(after),
        "before_step_size": float(before),
        "after_step_size": float(after),
        "step_update_allowed": False,
        "role": "hard_veto",
    }


def _frozen_step_trajectory_stage_diagnostics(
    candidates: tuple[Mapping[str, Any], ...],
    *,
    final_status: str,
    selected_candidate_index: int | None,
    run_error: Exception | None,
    hard_vetoes: tuple[str, ...],
    repair_triggers: tuple[str, ...],
    runner_route_summary: Mapping[str, Any],
    soft_deadline_closeout: Mapping[str, Any] | None = None,
    expected_candidate_count: int | None = None,
) -> Mapping[str, Any]:
    candidate_count = len(candidates)
    expected_count = (
        candidate_count
        if expected_candidate_count is None
        else int(expected_candidate_count)
    )
    skipped_count = max(0, expected_count - candidate_count)
    return {
        "passed": final_status == "passed",
        "final_status": final_status,
        "candidate_count": candidate_count,
        "expected_candidate_count": expected_count,
        "completed_candidate_count": candidate_count,
        "skipped_candidate_count": skipped_count,
        "passed_candidate_count": sum(
            candidate.get("classification") == "passed_screen"
            for candidate in candidates
        ),
        "selected_candidate_index": selected_candidate_index,
        "selected_acceptance_rate": None
        if selected_candidate_index is None
        else candidates[selected_candidate_index]["diagnostics"].get("acceptance_rate"),
        "hard_vetoes": hard_vetoes,
        "repair_triggers": repair_triggers,
        "run_error_type": None if run_error is None else type(run_error).__name__,
        "run_error_message": None if run_error is None else str(run_error),
        "reports_fresh_final_verification": False,
        "reports_posterior_convergence": False,
        "candidate_mechanics_are_diagnostic_telemetry_only": True,
        "public_timeout_closeout": None
        if soft_deadline_closeout is None
        else dict(soft_deadline_closeout),
        "runner_route_summary": runner_route_summary,
        "nonclaims": FROZEN_STEP_TRAJECTORY_STAGE_NONCLAIMS,
    }


def _acceptance_relation_to_band(
    acceptance: Any,
    band: tuple[float, float],
) -> str:
    value = _scalar_or_none(acceptance)
    if value is None:
        return "unavailable"
    lower, upper = (float(band[0]), float(band[1]))
    if value < lower:
        return "below_acceptance_band"
    if value > upper:
        return "above_acceptance_band"
    return "inside_acceptance_band"


def _frozen_step_trajectory_public_summary(
    stage: HMCFrozenStepTrajectoryStageResult | None,
) -> Mapping[str, Any] | None:
    """Summarize Phase 6 without exposing candidate grids or HMC mechanics."""

    if stage is None:
        return None
    candidate_results = tuple(stage.candidate_results)
    relation_counts = {
        "below_acceptance_band": 0,
        "inside_acceptance_band": 0,
        "above_acceptance_band": 0,
        "unavailable": 0,
    }
    for candidate in candidate_results:
        diagnostics = candidate.get("diagnostics")
        acceptance = (
            diagnostics.get("acceptance_rate") if isinstance(diagnostics, Mapping) else None
        )
        relation = _acceptance_relation_to_band(acceptance, stage.config.acceptance_band)
        relation_counts[relation] += 1
    selected_relation = "unavailable"
    if stage.selected_candidate_index is not None:
        selected = candidate_results[int(stage.selected_candidate_index)]
        diagnostics = selected.get("diagnostics")
        selected_relation = _acceptance_relation_to_band(
            diagnostics.get("acceptance_rate") if isinstance(diagnostics, Mapping) else None,
            stage.config.acceptance_band,
        )
    runner_route = stage.diagnostics.get("runner_route_summary")
    route_summary = None
    if isinstance(runner_route, Mapping):
        route_summary = {
            "active_route": runner_route.get("active_route"),
            "reusable_runner_build_count": runner_route.get("reusable_runner_build_count"),
            "distinct_static_runner_contract_count": runner_route.get(
                "distinct_static_runner_contract_count"
            ),
            "single_use_build_count": runner_route.get("single_use_build_count"),
            "injected_runner_call_count": runner_route.get("injected_runner_call_count"),
            "fallback_status": runner_route.get("fallback_status"),
        }
    timeout_closeout = stage.diagnostics.get("public_timeout_closeout")
    public_timeout_closeout = None
    if isinstance(timeout_closeout, Mapping):
        allowed_timeout_keys = {
            "enabled",
            "timeout_budget_s",
            "reserve_s",
            "elapsed_s",
            "remaining_s",
            "within_closeout_window",
            "deadline_clock_scope",
            "stage_elapsed_s",
            "stage_remaining_s",
            "estimated_next_candidate_s",
            "completed_candidate_elapsed_count",
            "closeout_required_before_next_candidate",
            "diagnostic_role",
            "candidate_index",
            "candidate_count",
            "completed_candidate_count",
            "progress_only",
            "public_closeout_artifact_expected",
            "reason",
            "hmc_mechanics_exposed",
            "reports_posterior_convergence",
            "reports_sampler_superiority",
            "reports_default_readiness",
            "reports_gpu_or_xla_readiness",
        }
        public_timeout_closeout = {
            key: timeout_closeout[key]
            for key in allowed_timeout_keys
            if key in timeout_closeout
        }
    return {
        "schema": "bayesfilter.hmc_frozen_step_trajectory_public_summary.v1",
        "final_status": stage.final_status,
        "diagnostic_role": stage.diagnostic_role,
        "candidate_count": int(
            stage.diagnostics.get("expected_candidate_count", len(candidate_results))
        ),
        "completed_candidate_count": int(
            stage.diagnostics.get("completed_candidate_count", len(candidate_results))
        ),
        "skipped_candidate_count": int(
            stage.diagnostics.get("skipped_candidate_count", 0)
        ),
        "passed_candidate_count": int(stage.diagnostics.get("passed_candidate_count", 0)),
        "selected_candidate_index": stage.selected_candidate_index,
        "selected_acceptance_relation": selected_relation,
        "candidate_acceptance_relation_counts": relation_counts,
        "verification_repair_neighborhood_applied": bool(
            stage.candidate_generation.get("verification_repair_neighborhood_applied", False)
        ),
        "hard_vetoes": stage.hard_vetoes,
        "repair_triggers": stage.repair_triggers,
        "public_timeout_closeout": public_timeout_closeout,
        "runner_route_public_summary": route_summary,
        "candidate_grid_exposed": False,
        "hmc_mechanics_exposed": False,
        "reports_fresh_final_verification": False,
        "reports_posterior_convergence": False,
        "reports_sampler_superiority": False,
        "reports_default_readiness": False,
        "reports_gpu_or_xla_readiness": False,
        "nonclaims": FROZEN_STEP_TRAJECTORY_STAGE_NONCLAIMS,
    }


def _run_phase7_final_verification(
    *,
    adapter: Any,
    geometry: HMCGeometryInitializationResult,
    windowed_stage: HMCWindowedMassStageResult,
    fixed_mass_step_stage: HMCFixedMassStepStageResult,
    trajectory_stage: HMCFrozenStepTrajectoryStageResult,
    config: HMCTuneVerifyRepairLoopConfig,
    budget_policy: _HMCAttemptBudgetPolicy,
    attempt_index: int,
    target_scope: str,
    verification_callback: VerificationCallback | None,
    run_full_chain: RunFullChainFn,
) -> tuple[
    Mapping[str, Any] | None,
    Mapping[str, Any],
    FixedMassHMCTuningBudgetCallbackResult,
    str,
    str,
    tuple[str, ...],
    tuple[str, ...],
]:
    adapted_mass = _phase4_adapted_mass_artifact(windowed_stage)
    mass_signature = _mass_artifact_signature(adapted_mass)
    step = _required_selected_step_size(fixed_mass_step_stage)
    leapfrog = trajectory_stage.selected_num_leapfrog_steps
    if leapfrog is None:
        raise ValueError("Phase 7 final verification requires selected L")
    phase4_adapter = _phase4_latent_adapter_for_step_stage(
        adapter=adapter,
        geometry=geometry,
        windowed_stage=windowed_stage,
        target_scope=target_scope,
    )
    verification_adapter = _build_fixed_mass_hmc_adapter(
        adapter=phase4_adapter,
        mass_artifact=adapted_mass,
        mass_signature=mass_signature,
        target_scope=target_scope,
    )
    verification_hmc_signature = stable_adapter_signature(verification_adapter)
    if verification_hmc_signature != trajectory_stage.trajectory_hmc_adapter_signature:
        raise ValueError("Phase 7 verification HMC adapter signature mismatch")
    before_mass_signature = mass_signature
    before_step = step
    before_l = int(leapfrog)
    verification_seed = _derive_seed(
        _phase7_attempt_seed(config.seed, attempt_index),
        stage_index=4,
    )
    if run_full_chain is run_full_chain_tfp_hmc:
        return _run_phase7_sequential_rhat_final_verification(
            adapted_mass=adapted_mass,
            mass_signature=mass_signature,
            step=step,
            leapfrog=int(leapfrog),
            verification_adapter=verification_adapter,
            verification_hmc_signature=verification_hmc_signature,
            phase4_adapter=phase4_adapter,
            fixed_mass_step_stage=fixed_mass_step_stage,
            trajectory_stage=trajectory_stage,
            config=config,
            budget_policy=budget_policy,
            attempt_index=attempt_index,
            verification_seed=verification_seed,
            verification_callback=verification_callback,
            before_mass_signature=before_mass_signature,
            before_step=before_step,
            before_l=before_l,
        )
    verification_config = FullChainHMCConfig(
        num_results=budget_policy.verification_num_results,
        num_burnin_steps=budget_policy.verification_num_burnin_steps,
        step_size=step,
        num_leapfrog_steps=int(leapfrog),
        seed=verification_seed,
        use_xla=config.use_xla,
        trace_policy="standard",
        target_status_trace_policy=config.target_status_trace_policy,
        target_scope=target_scope,
        chain_execution_mode=config.chain_execution_mode,
    )
    runner_cache: dict[str, Any] = {}
    runner_contract_payloads: dict[str, Mapping[str, Any]] = {}
    runner_route_events: list[Mapping[str, Any]] = []
    run_result: FullChainHMCRunResult | None = None
    run_error: Exception | None = None
    try:
        run_result = _run_kernel_stage_with_optional_reusable_route(
            run_full_chain=run_full_chain,
            runner_cache=runner_cache,
            runner_contract_payloads=runner_contract_payloads,
            route_events=runner_route_events,
            route_name="phase7_final_verification_scoped_reusable_runner",
            route_scope="phase7_fresh_fixed_kernel_verification",
            adapter=verification_adapter,
            initial_state=np.zeros(adapted_mass.dimension, dtype=float),
            config=verification_config,
            hmc_adapter_signature=verification_hmc_signature,
            target_dimension=windowed_stage.target_dimension,
            mass_signature=mass_signature,
            event_payload={
                "attempt_index": int(attempt_index),
                "num_leapfrog_steps": int(leapfrog),
                "step_size": step,
                "verification_num_results": int(
                    budget_policy.verification_num_results
                ),
                "verification_num_burnin_steps": int(
                    budget_policy.verification_num_burnin_steps
                ),
            },
        )
        diagnostics = dict(_bootstrap_diagnostics_payload(run_result))
    except Exception as exc:  # noqa: BLE001 - final verification is fail-closed.
        run_error = exc
        diagnostics = dict(_bootstrap_error_diagnostics(exc))
    diagnostics["diagnostic_context"] = "phase7_fresh_fixed_kernel_verification"
    diagnostics["nonclaims"] = TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS
    diagnostics["verification_budget"] = budget_policy.payload()
    diagnostics["runner_route_summary"] = _kernel_stage_runner_route_summary(
        active_route=(
            "phase7_final_verification_scoped_reusable_runner"
            if run_full_chain is run_full_chain_tfp_hmc
            and config.chain_execution_mode == "tf_function"
            else "single_use_or_injected_runner"
        ),
        events=tuple(runner_route_events),
        contract_payloads=runner_contract_payloads,
        semantic_source="_run_phase7_final_verification",
        reuse_nonclaim=(
            "fresh final verification is one call per attempt, so this route is "
            "primarily consistency and regression protection rather than warm-call reuse"
        ),
    )
    callback_result = _call_trajectory_screen_callback(
        verification_callback,
        round_payload={
            "attempt_index": attempt_index,
            "seed": verification_seed,
            "step_size": step,
            "num_leapfrog_steps": int(leapfrog),
            "trajectory_length": float(step) * int(leapfrog),
            "verification_config_payload": {
                **verification_config.signature_payload(),
                "acceptance_band": tuple(float(item) for item in config.acceptance_band),
            },
            "adapter_signature": stable_adapter_signature(phase4_adapter),
            "hmc_adapter_signature": verification_hmc_signature,
            "mass_artifact_signature": mass_signature,
            "sample_space": "phase4_latent_position",
            "hmc_sample_space": "adapted_mass_latent",
            "diagnostic_role": "fresh_fixed_kernel_verification",
        },
        samples=None
        if run_result is None
        else verification_adapter.latent_to_position(run_result.samples),
        diagnostics=diagnostics,
    )
    (
        final_status,
        diagnostic_role,
        hard_vetoes,
        repair_triggers,
    ) = _classify_phase7_final_verification(
        config,
        diagnostics=diagnostics,
        screen_error=run_error,
        callback_result=callback_result,
    )
    after_mass_signature = _mass_artifact_signature(adapted_mass)
    mass_signature_unchanged = before_mass_signature == after_mass_signature
    step_size_unchanged = before_step == _required_selected_step_size(fixed_mass_step_stage)
    num_leapfrog_steps_unchanged = before_l == trajectory_stage.selected_num_leapfrog_steps
    invariant = {
        "mass_signature_unchanged": mass_signature_unchanged,
        "kernel_scale_unchanged": step_size_unchanged,
        "trajectory_count_unchanged": num_leapfrog_steps_unchanged,
        "kernel_mechanics_publicized": False,
        "role": "hard_veto",
    }
    diagnostics["frozen_kernel_invariant"] = invariant
    invariant_vetoes: list[str] = []
    if not mass_signature_unchanged:
        invariant_vetoes.append("verification_mass_signature_mutated")
    if not step_size_unchanged:
        invariant_vetoes.append("verification_step_size_mutated")
    if not num_leapfrog_steps_unchanged:
        invariant_vetoes.append("verification_leapfrog_count_mutated")
    if invariant_vetoes:
        final_status = "hard_veto"
        diagnostic_role = "hard_veto"
        hard_vetoes = tuple(dict.fromkeys([*hard_vetoes, *invariant_vetoes]))
    return (
        {
            **verification_config.signature_payload(),
            "acceptance_band": tuple(float(item) for item in config.acceptance_band),
        },
        diagnostics,
        callback_result,
        final_status,
        diagnostic_role,
        hard_vetoes,
        repair_triggers,
    )


def _run_phase7_sequential_rhat_final_verification(
    *,
    adapted_mass: PrecomputedMassArtifact,
    mass_signature: str,
    step: float,
    leapfrog: int,
    verification_adapter: Any,
    verification_hmc_signature: str,
    phase4_adapter: Any,
    fixed_mass_step_stage: HMCFixedMassStepStageResult,
    trajectory_stage: HMCFrozenStepTrajectoryStageResult,
    config: HMCTuneVerifyRepairLoopConfig,
    budget_policy: _HMCAttemptBudgetPolicy,
    attempt_index: int,
    verification_seed: tuple[int, int],
    verification_callback: VerificationCallback | None,
    before_mass_signature: str,
    before_step: float,
    before_l: int,
) -> tuple[
    Mapping[str, Any] | None,
    Mapping[str, Any],
    FixedMassHMCTuningBudgetCallbackResult,
    str,
    str,
    tuple[str, ...],
    tuple[str, ...],
]:
    max_results = int(budget_policy.verification_num_results)
    check_interval = min(500, max_results)
    sequential_config = SequentialRHatHMCVerificationConfig(
        check_interval=check_interval,
        max_results=max_results,
        num_burnin_steps=budget_policy.verification_num_burnin_steps,
        step_size=step,
        num_leapfrog_steps=int(leapfrog),
        seed=verification_seed,
        chain_count=4,
        rhat_threshold=1.01,
        use_xla=config.use_xla,
        target_scope=config.target_scope,
        chain_execution_mode=config.chain_execution_mode,
    )
    verifier = build_sequential_rhat_hmc_verifier(
        verification_adapter,
        np.zeros(adapted_mass.dimension, dtype=float),
        sequential_config,
    )
    run_error: Exception | None = None
    try:
        result = verifier.run()
        diagnostics = dict(result.diagnostics)
    except Exception as exc:  # noqa: BLE001 - final verification is fail-closed.
        run_error = exc
        diagnostics = dict(_bootstrap_error_diagnostics(exc))
        diagnostics["sequential_rhat_verification"] = True
        diagnostics["rhat_threshold"] = 1.01
        diagnostics["check_interval"] = check_interval
        diagnostics["max_results"] = max_results
    diagnostics["diagnostic_context"] = "phase7_sequential_rhat_fixed_kernel_verification"
    diagnostics["nonclaims"] = TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS
    diagnostics["verification_budget"] = budget_policy.payload()
    diagnostics["sequential_rhat_policy"] = {
        "check_interval": check_interval,
        "rhat_threshold": 1.01,
        "max_results": max_results,
        "stopping_rule": "stop_when_all_finite_parameter_rhat_at_or_below_threshold",
        "cap_rule": "stop_at_budget_policy_verification_num_results_without_promotion",
        "mechanics_publicized": False,
    }
    diagnostics["runner_route_summary"] = {
        "active_route": "phase7_sequential_rhat_fixed_size_chunk_verifier",
        "single_use_build_count": 0,
        "fallback_status": "none",
        "semantic_source": "_run_phase7_sequential_rhat_final_verification",
        "route_nonclaims": (
            "sequential R-hat final verification uses fixed-size TF/TFP chunks",
            "R-hat is a tuning-verification stop rule, not posterior convergence proof",
        ),
    }
    verification_payload = {
        "verification_policy": "sequential_rhat",
        "check_interval": check_interval,
        "max_results": max_results,
        "num_burnin_steps": sequential_config.num_burnin_steps,
        "chain_count": sequential_config.chain_count,
        "rhat_threshold": sequential_config.rhat_threshold,
        "acceptance_band": tuple(float(item) for item in config.acceptance_band),
        "use_xla": sequential_config.use_xla,
        "chain_execution_mode": sequential_config.chain_execution_mode,
        "target_scope": sequential_config.target_scope,
        "trace_policy": "reduced_public_safe_aggregate",
        "adaptation_policy": "fixed_kernel_no_adaptation",
        "hmc_mechanics_publicized": False,
        "internal_policy_only": True,
    }
    callback_result = _call_trajectory_screen_callback(
        verification_callback,
        round_payload={
            "attempt_index": attempt_index,
            "verification_config_payload": verification_payload,
            "adapter_signature": stable_adapter_signature(phase4_adapter),
            "hmc_adapter_signature": verification_hmc_signature,
            "mass_artifact_signature": mass_signature,
            "sample_space": "phase4_latent_position",
            "hmc_sample_space": "adapted_mass_latent",
            "diagnostic_role": "sequential_rhat_fixed_kernel_verification",
            "kernel_mechanics_publicized": False,
        },
        samples=None,
        diagnostics=diagnostics,
    )
    (
        final_status,
        diagnostic_role,
        hard_vetoes,
        repair_triggers,
    ) = _classify_phase7_final_verification(
        config,
        diagnostics=diagnostics,
        screen_error=run_error,
        callback_result=callback_result,
    )
    after_mass_signature = _mass_artifact_signature(adapted_mass)
    mass_signature_unchanged = before_mass_signature == after_mass_signature
    step_size_unchanged = before_step == _required_selected_step_size(fixed_mass_step_stage)
    num_leapfrog_steps_unchanged = before_l == trajectory_stage.selected_num_leapfrog_steps
    invariant = {
        "mass_signature_unchanged": mass_signature_unchanged,
        "kernel_scale_unchanged": step_size_unchanged,
        "trajectory_count_unchanged": num_leapfrog_steps_unchanged,
        "kernel_mechanics_publicized": False,
        "role": "hard_veto",
    }
    diagnostics["frozen_kernel_invariant"] = invariant
    invariant_vetoes: list[str] = []
    if not mass_signature_unchanged:
        invariant_vetoes.append("verification_mass_signature_mutated")
    if not step_size_unchanged:
        invariant_vetoes.append("verification_step_size_mutated")
    if not num_leapfrog_steps_unchanged:
        invariant_vetoes.append("verification_leapfrog_count_mutated")
    if invariant_vetoes:
        final_status = "hard_veto"
        diagnostic_role = "hard_veto"
        hard_vetoes = tuple(dict.fromkeys([*hard_vetoes, *invariant_vetoes]))
    return (
        verification_payload,
        diagnostics,
        callback_result,
        final_status,
        diagnostic_role,
        hard_vetoes,
        repair_triggers,
    )


def _classify_phase7_final_verification(
    config: HMCTuneVerifyRepairLoopConfig,
    *,
    diagnostics: Mapping[str, Any],
    screen_error: Exception | None,
    callback_result: FixedMassHMCTuningBudgetCallbackResult,
) -> tuple[str, str, tuple[str, ...], tuple[str, ...]]:
    hard_vetoes: list[str] = []
    if screen_error is not None:
        hard_vetoes.append("verification_hmc_error")
    acceptance = diagnostics.get("acceptance_rate")
    if acceptance is None or not _finite_number(acceptance):
        hard_vetoes.append("verification_acceptance_missing_or_nonfinite")
    if diagnostics.get("runtime_finite") is not True:
        hard_vetoes.append("verification_runtime_missing_or_nonfinite")
    if diagnostics.get("log_accept_ratio_finite") is not True:
        hard_vetoes.append("verification_log_accept_nonfinite_or_missing")
    if diagnostics.get("samples_all_finite") is not True:
        hard_vetoes.append("verification_samples_nonfinite_or_missing")
    if diagnostics.get("target_log_prob_finite") is not True:
        hard_vetoes.append("verification_target_log_prob_nonfinite_or_missing")
    telemetry = diagnostics.get("target_status_telemetry")
    if isinstance(telemetry, Mapping) and telemetry.get("telemetry_failure_veto_bool"):
        hard_vetoes.append("verification_target_status_telemetry_failure")
    hard_vetoes.extend(callback_result.hard_vetoes)
    if hard_vetoes:
        return "hard_veto", "hard_veto", tuple(dict.fromkeys(hard_vetoes)), ()
    if callback_result.continuation_vetoes:
        return (
            "hard_veto",
            "hard_veto",
            tuple(
                dict.fromkeys(
                    ["verification_callback_continuation_veto", *callback_result.continuation_vetoes]
                )
            ),
            (),
        )
    repair_triggers: list[str] = []
    if callback_result.promotion_vetoes:
        repair_triggers.extend(callback_result.promotion_vetoes)
    if callback_result.repair_triggers:
        repair_triggers.extend(callback_result.repair_triggers)
    if repair_triggers:
        return (
            "repair_or_retry",
            "repair_trigger",
            (),
            tuple(dict.fromkeys(repair_triggers)),
        )
    if diagnostics.get("sequential_rhat_verification") is True:
        if diagnostics.get("all_finite_rhat_at_or_below_threshold") is True:
            acceptance_value = float(acceptance)
            if config.acceptance_band[0] <= acceptance_value <= config.acceptance_band[1]:
                return "passed", "sequential_rhat_fixed_kernel_verification_passed", (), ()
            return (
                "repair_or_retry",
                "verification_acceptance_repair_trigger",
                (),
                ("verification_acceptance_outside_pass_band",),
            )
        triggers = ["verification_rhat_above_threshold_or_cap_hit"]
        if diagnostics.get("cap_hit") is True:
            triggers.append("verification_rhat_cap_hit")
        return (
            "repair_or_retry",
            "verification_rhat_repair_trigger",
            (),
            tuple(triggers),
        )
    acceptance_value = float(acceptance)
    if config.acceptance_band[0] <= acceptance_value <= config.acceptance_band[1]:
        return "passed", "fresh_fixed_kernel_verification_passed", (), ()
    return (
        "repair_or_retry",
        "verification_acceptance_repair_trigger",
        (),
        ("verification_acceptance_outside_pass_band",),
    )


def _phase7_attempt_state_from_stages(
    *,
    config: HMCTuneVerifyRepairLoopConfig,
    windowed_stage: HMCWindowedMassStageResult,
    fixed_mass_step_stage: HMCFixedMassStepStageResult | None,
    frozen_step_trajectory_stage: HMCFrozenStepTrajectoryStageResult | None,
    verification_config_payload: Mapping[str, Any] | None = None,
    verification_diagnostics: Mapping[str, Any] | None = None,
    verification_final_status: str | None = None,
    verification_diagnostic_role: str | None = None,
    verification_repair_triggers: Sequence[str] = (),
) -> _HMCPhaseAttemptState:
    mass_artifact = _phase4_adapted_mass_artifact(windowed_stage)
    step_size = None
    step_hash = None
    handoff_stage = "phase4"
    if fixed_mass_step_stage is not None:
        if fixed_mass_step_stage.passed:
            step_size = fixed_mass_step_stage.selected_step_size
            step_hash = fixed_mass_step_stage.selected_step_hash
            handoff_stage = "phase5_selected"
        else:
            step_size = fixed_mass_step_stage.repair_step_size
            step_hash = fixed_mass_step_stage.repair_step_hash
            handoff_stage = "phase5_repair"
    leapfrog = None
    trajectory_hash = None
    if frozen_step_trajectory_stage is not None:
        leapfrog = frozen_step_trajectory_stage.selected_num_leapfrog_steps
        trajectory_hash = frozen_step_trajectory_stage.selected_trajectory_hash
        if frozen_step_trajectory_stage.passed:
            handoff_stage = "phase6"
    verification_repair = _phase7_verification_repair_handoff_payload(
        config=config,
        selected_step_size=step_size,
        selected_step_hash=step_hash,
        verification_config_payload=verification_config_payload,
        verification_diagnostics=verification_diagnostics,
        verification_final_status=verification_final_status,
        verification_diagnostic_role=verification_diagnostic_role,
        verification_repair_triggers=verification_repair_triggers,
    )
    if (
        not verification_repair["verification_repair_applied"]
        and frozen_step_trajectory_stage is not None
    ):
        verification_repair = _phase6_trajectory_repair_handoff_payload(
            config=config,
            selected_step_size=step_size,
            selected_step_hash=step_hash,
            frozen_step_trajectory_stage=frozen_step_trajectory_stage,
        )
    return _HMCPhaseAttemptState(
        mass_artifact_payload=mass_artifact.to_payload(include_arrays=True),
        mass_artifact_signature=_mass_artifact_signature(mass_artifact),
        selected_step_size=step_size,
        selected_step_hash=step_hash,
        selected_num_leapfrog_steps=leapfrog,
        selected_trajectory_hash=trajectory_hash,
        verification_acceptance_rate=verification_repair["verification_acceptance_rate"],
        verification_acceptance_relation=verification_repair["verification_acceptance_relation"],
        verification_repair_trigger=verification_repair["verification_repair_trigger"],
        verification_repair_source=verification_repair["verification_repair_source"],
        verification_repair_step_size=verification_repair["verification_repair_step_size"],
        verification_repair_step_hash=verification_repair["verification_repair_step_hash"],
        verification_repair_applied=verification_repair["verification_repair_applied"],
        handoff_stage=handoff_stage,
    )


def _phase7_verification_repair_handoff_payload(
    *,
    config: HMCTuneVerifyRepairLoopConfig,
    selected_step_size: float | None,
    selected_step_hash: str | None,
    verification_config_payload: Mapping[str, Any] | None,
    verification_diagnostics: Mapping[str, Any] | None,
    verification_final_status: str | None,
    verification_diagnostic_role: str | None,
    verification_repair_triggers: Sequence[str],
) -> Mapping[str, Any]:
    diagnostics = {} if verification_diagnostics is None else dict(verification_diagnostics)
    acceptance = _scalar_or_none(diagnostics.get("acceptance_rate"))
    relation = "unavailable"
    if acceptance is not None:
        if acceptance < float(config.acceptance_band[0]):
            relation = "below_acceptance_band"
        elif acceptance > float(config.acceptance_band[1]):
            relation = "above_acceptance_band"
        else:
            relation = "inside_acceptance_band"
    triggers = tuple(str(item) for item in verification_repair_triggers)
    trigger = (
        _PHASE7_VERIFICATION_ACCEPTANCE_REPAIR_TRIGGER
        if _PHASE7_VERIFICATION_ACCEPTANCE_REPAIR_TRIGGER in triggers
        else None
    )
    repair_step_size = None
    repair_step_hash = None
    repair_source = None
    repair_applied = False
    if (
        trigger is not None
        and relation in {"below_acceptance_band", "above_acceptance_band"}
        and selected_step_size is not None
    ):
        factor = 0.5 if relation == "below_acceptance_band" else 2.0
        repair_step_size = float(selected_step_size) * factor
        if not np.isfinite(repair_step_size) or repair_step_size <= 0.0:
            raise ValueError("verification repair step size must be positive and finite")
        repair_payload = {
            "runtime": "bayesfilter.inference.hmc_kernel_tuning.phase7_verification_repair",
            "repair_source": "phase7_final_verification_acceptance",
            "verification_final_status": verification_final_status,
            "verification_diagnostic_role": verification_diagnostic_role,
            "verification_repair_trigger": trigger,
            "verification_acceptance_rate": acceptance,
            "verification_acceptance_relation": relation,
            "acceptance_band": tuple(float(item) for item in config.acceptance_band),
            "base_step_size": float(selected_step_size),
            "base_step_hash": selected_step_hash,
            "repair_factor": factor,
            "step_size": repair_step_size,
            "verification_config_payload": (
                None
                if verification_config_payload is None
                else dict(verification_config_payload)
            ),
            "private_handoff_only": True,
            "public_progress_exposes_step": False,
        }
        repair_step_hash = stable_config_hash(repair_payload)
        repair_source = "phase7_final_verification_acceptance"
        repair_applied = True
    return {
        "verification_acceptance_rate": acceptance,
        "verification_acceptance_relation": relation,
        "verification_repair_trigger": trigger,
        "verification_repair_source": repair_source,
        "verification_repair_step_size": repair_step_size,
        "verification_repair_step_hash": repair_step_hash,
        "verification_repair_applied": repair_applied,
    }


def _phase6_trajectory_repair_handoff_payload(
    *,
    config: HMCTuneVerifyRepairLoopConfig,
    selected_step_size: float | None,
    selected_step_hash: str | None,
    frozen_step_trajectory_stage: HMCFrozenStepTrajectoryStageResult,
) -> Mapping[str, Any]:
    """Build a private step repair when Phase 6 fails directionally.

    If every completed frozen-step trajectory candidate is on the same side of
    the acceptance pass band, changing only ``L`` cannot repair the observed
    acceptance regime.  The retry therefore adjusts the next Phase 5 initial
    step privately while leaving the public Phase 6 artifact redacted.
    """

    if (
        frozen_step_trajectory_stage.final_status != "repair_or_retry"
        or selected_step_size is None
        or not frozen_step_trajectory_stage.candidate_results
    ):
        return {
            "verification_acceptance_rate": None,
            "verification_acceptance_relation": "unavailable",
            "verification_repair_trigger": None,
            "verification_repair_source": None,
            "verification_repair_step_size": None,
            "verification_repair_step_hash": None,
            "verification_repair_applied": False,
        }
    relations = [
        _acceptance_relation_to_band(
            candidate.get("diagnostics", {}).get("acceptance_rate")
            if isinstance(candidate.get("diagnostics"), Mapping)
            else None,
            config.acceptance_band,
        )
        for candidate in frozen_step_trajectory_stage.candidate_results
        if candidate.get("classification") == "repair_or_retry"
    ]
    unique_relations = set(relations)
    if len(relations) != len(frozen_step_trajectory_stage.candidate_results) or unique_relations not in (
        {"below_acceptance_band"},
        {"above_acceptance_band"},
    ):
        return {
            "verification_acceptance_rate": None,
            "verification_acceptance_relation": "unavailable",
            "verification_repair_trigger": None,
            "verification_repair_source": None,
            "verification_repair_step_size": None,
            "verification_repair_step_hash": None,
            "verification_repair_applied": False,
        }
    relation = next(iter(unique_relations))
    factor = 0.5 if relation == "below_acceptance_band" else 2.0
    repair_step_size = float(selected_step_size) * factor
    if not np.isfinite(repair_step_size) or repair_step_size <= 0.0:
        raise ValueError("Phase 6 trajectory repair step size must be positive and finite")
    acceptance_values = tuple(
        float(candidate["diagnostics"]["acceptance_rate"])
        for candidate in frozen_step_trajectory_stage.candidate_results
        if isinstance(candidate.get("diagnostics"), Mapping)
        and _finite_number(candidate["diagnostics"].get("acceptance_rate"))
    )
    acceptance_summary = None
    if acceptance_values:
        acceptance_summary = {
            "count": len(acceptance_values),
            "min": min(acceptance_values),
            "max": max(acceptance_values),
        }
    repair_payload = {
        "runtime": "bayesfilter.inference.hmc_kernel_tuning.phase6_trajectory_repair",
        "repair_source": "phase6_frozen_step_trajectory_acceptance",
        "trajectory_final_status": frozen_step_trajectory_stage.final_status,
        "trajectory_diagnostic_role": frozen_step_trajectory_stage.diagnostic_role,
        "verification_repair_trigger": _PHASE6_TRAJECTORY_ACCEPTANCE_REPAIR_TRIGGER,
        "verification_acceptance_relation": relation,
        "trajectory_candidate_count": len(frozen_step_trajectory_stage.candidate_results),
        "trajectory_acceptance_summary": acceptance_summary,
        "acceptance_band": tuple(float(item) for item in config.acceptance_band),
        "base_step_size": float(selected_step_size),
        "base_step_hash": selected_step_hash,
        "repair_factor": factor,
        "step_size": repair_step_size,
        "trajectory_stage_artifact_hash": frozen_step_trajectory_stage.artifact_hash,
        "private_handoff_only": True,
        "public_progress_exposes_step": False,
        "public_progress_exposes_candidate_grid": False,
    }
    return {
        "verification_acceptance_rate": None,
        "verification_acceptance_relation": relation,
        "verification_repair_trigger": _PHASE6_TRAJECTORY_ACCEPTANCE_REPAIR_TRIGGER,
        "verification_repair_source": "phase6_frozen_step_trajectory_acceptance",
        "verification_repair_step_size": repair_step_size,
        "verification_repair_step_hash": stable_config_hash(repair_payload),
        "verification_repair_applied": True,
    }


def _phase7_final_kernel_payload(
    *,
    config: HMCTuneVerifyRepairLoopConfig,
    geometry: HMCGeometryInitializationResult,
    bootstrap: HMCBootstrapScreenResult,
    windowed_stage: HMCWindowedMassStageResult,
    fixed_mass_step_stage: HMCFixedMassStepStageResult,
    trajectory_stage: HMCFrozenStepTrajectoryStageResult,
    verification_config_payload: Mapping[str, Any] | None,
    verification_diagnostics: Mapping[str, Any],
    budget_policy: _HMCAttemptBudgetPolicy,
    attempt_index: int,
    target_scope: str,
) -> Mapping[str, Any]:
    adapted_mass = _phase4_adapted_mass_artifact(windowed_stage)
    step = _required_selected_step_size(fixed_mass_step_stage)
    leapfrog = trajectory_stage.selected_num_leapfrog_steps
    if leapfrog is None:
        raise ValueError("final kernel payload requires selected L")
    return {
        "runtime": "bayesfilter.inference.run_hmc_tune_verify_repair_loop",
        "schema": "bayesfilter.hmc_frozen_kernel_handoff.v1",
        "attempt_index": int(attempt_index),
        "target_scope": target_scope,
        "target_dimension": geometry.target_dimension,
        "adapted_mass_artifact_payload": adapted_mass.to_payload(include_arrays=True),
        "adapted_mass_artifact_signature": _mass_artifact_signature(adapted_mass),
        "step_size": float(step),
        "num_leapfrog_steps": int(leapfrog),
        "trajectory_length": float(step) * int(leapfrog),
        "target_accept_prob": config.target_accept_prob,
        "acceptance_band": config.acceptance_band,
        "geometry_artifact_hash": geometry.artifact_hash,
        "bootstrap_artifact_hash": bootstrap.artifact_hash,
        "windowed_stage_artifact_hash": windowed_stage.artifact_hash,
        "fixed_mass_step_stage_artifact_hash": fixed_mass_step_stage.artifact_hash,
        "frozen_step_trajectory_stage_artifact_hash": trajectory_stage.artifact_hash,
        "selected_step_hash": fixed_mass_step_stage.selected_step_hash,
        "selected_trajectory_hash": trajectory_stage.selected_trajectory_hash,
        "verification_config_payload": verification_config_payload,
        "verification_acceptance_rate": verification_diagnostics.get("acceptance_rate"),
        "budget_policy": budget_policy.payload(),
        "fresh_fixed_kernel_verification_passed": True,
        "reports_posterior_convergence": False,
        "reports_sampler_superiority": False,
        "reports_default_readiness": False,
        "reports_external_client_scientific_claim": False,
        "reports_gpu_or_xla_readiness": False,
        "nonclaims": TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS,
    }


def _windowed_mass_stage_internal_config(
    attempt_budget_policy: _HMCAttemptBudgetPolicy | None = None,
) -> WindowedMassAdaptationConfig:
    if attempt_budget_policy is None:
        warmup_steps = 12
        initial_buffer = 2
        final_buffer = 2
        first_window_size = 3
    else:
        warmup_steps = int(attempt_budget_policy.phase4_warmup_steps)
        initial_buffer = max(2, min(warmup_steps // 10, warmup_steps // 4))
        final_buffer = max(2, min(warmup_steps // 10, warmup_steps // 4))
        if initial_buffer + final_buffer >= warmup_steps:
            initial_buffer = max(1, warmup_steps // 4)
            final_buffer = max(1, warmup_steps // 4)
        slow_steps = warmup_steps - initial_buffer - final_buffer
        first_window_size = max(2, min(max(2, slow_steps // 4), slow_steps))
    return WindowedMassAdaptationConfig(
        warmup_steps=warmup_steps,
        initial_buffer=initial_buffer,
        final_buffer=final_buffer,
        first_window_size=first_window_size,
        min_window_samples=2,
        mass_shrinkage=0.25,
        covariance_jitter=1.0e-6,
        eigenvalue_floor=1.0e-9,
        step_adaptation_rate=0.03,
    )


def _windowed_stage_initial_mass_artifact(
    *,
    adapter_signature: str,
    target_dimension: int,
    attempt_state: _HMCPhaseAttemptState | None = None,
) -> PrecomputedMassArtifact:
    dimension = int(target_dimension)
    if dimension <= 0:
        raise ValueError("target_dimension must be positive")
    if attempt_state is not None and attempt_state.mass_artifact_payload is not None:
        artifact = PrecomputedMassArtifact.from_payload(
            attempt_state.mass_artifact_payload,
            expected_adapter_signature=str(adapter_signature),
            expected_dim=dimension,
        )
        if attempt_state.mass_artifact_signature is not None:
            observed = _mass_artifact_signature(artifact)
            if observed != attempt_state.mass_artifact_signature:
                raise ValueError("Phase 7 carried mass artifact signature mismatch")
        return artifact
    return PrecomputedMassArtifact.from_covariance(
        position=np.zeros(dimension),
        covariance=np.eye(dimension),
        adapter_signature=str(adapter_signature),
        position_role="latent_fixed_mass_origin",
        covariance_source="latent_identity_initial_mass",
        matrix_used_for_square_root="latent_identity",
        source="windowed_mass_stage_initial_latent_mass",
        jitter=0.0,
        regularization_report={
            "method": "latent_identity",
            "coordinate_system": "latent_fixed_mass",
            "source": "run_hmc_windowed_mass_stage",
        },
        nonclaims=WINDOWED_MASS_STAGE_NONCLAIMS,
    )


def _windowed_stage_draw_capture_policy(
    config: WindowedMassAdaptationConfig,
) -> Mapping[str, Any]:
    return {
        "route": "retained_fixed_kernel_samples",
        "num_results": config.warmup_steps,
        "warmup_steps": config.warmup_steps,
        "num_burnin_steps": _WINDOWED_STAGE_API_DISCARD_STEPS,
        "api_discarded_burnin_count": _WINDOWED_STAGE_API_DISCARD_STEPS,
        "api_discarded_burnin_counted_as_adaptation_input": False,
        "retained_samples_are_adaptation_inputs_only": True,
        "assumes_discarded_burnin_state_capture": False,
        "sample_space": "latent_fixed_mass",
        "nonclaims": WINDOWED_MASS_STAGE_NONCLAIMS,
    }


def _windowed_stage_diagnostic_run_config(
    config: HMCWindowedMassStageConfig,
    *,
    windowed_config: WindowedMassAdaptationConfig,
    selected_kernel: Mapping[str, Any],
    seed: tuple[int, int],
    target_scope: str,
) -> FullChainHMCConfig:
    return FullChainHMCConfig(
        num_results=windowed_config.warmup_steps,
        num_burnin_steps=_WINDOWED_STAGE_API_DISCARD_STEPS,
        step_size=float(selected_kernel["step_size"]),
        num_leapfrog_steps=int(selected_kernel["num_leapfrog_steps"]),
        seed=seed,
        use_xla=config.use_xla,
        trace_policy="standard",
        target_status_trace_policy=config.target_status_trace_policy,
        target_scope=target_scope,
        chain_execution_mode=config.chain_execution_mode,
    )


def _windowed_stage_capture_payload(
    run_result: FullChainHMCRunResult,
    *,
    expected_steps: int,
    target_dimension: int,
) -> Mapping[str, Any]:
    diagnostics = dict(run_result.diagnostics)
    trace = dict(run_result.trace)
    metadata = dict(run_result.metadata)
    samples = np.asarray(_tensor_to_numpy(run_result.samples), dtype=float)
    acceptance = _trace_array_or_none(trace, "is_accepted")
    log_accept = _trace_array_or_none(trace, "log_accept_ratio")
    target_log_prob = _trace_array_or_none(trace, "target_log_prob")
    runtime_s = _runtime_seconds_or_none(metadata)
    finite_acceptance = _valid_trace_vector(
        acceptance,
        expected_steps,
        bounds=(0.0, 1.0),
    )
    policy_filled_or_default = (
        not finite_acceptance or _acceptance_trace_is_default_like(acceptance)
    )
    runtime_evidence = _windowed_stage_runtime_evidence(metadata)
    fixture_or_synthetic = _metadata_marks_fixture_or_synthetic(metadata)
    payload = {
        "warmup_draws": samples,
        "acceptance_trace": acceptance,
        "log_accept_ratio": log_accept,
        "target_log_prob": target_log_prob,
        "runtime_s": runtime_s,
        "runtime_finite": runtime_s is not None and bool(np.isfinite(runtime_s)),
        "samples_shape": tuple(int(dim) for dim in samples.shape),
        "acceptance_shape": None
        if acceptance is None
        else tuple(int(dim) for dim in acceptance.shape),
        "log_accept_shape": None
        if log_accept is None
        else tuple(int(dim) for dim in log_accept.shape),
        "target_log_prob_shape": None
        if target_log_prob is None
        else tuple(int(dim) for dim in target_log_prob.shape),
        "expected_steps": int(expected_steps),
        "target_dimension": int(target_dimension),
        "finite_sample_count": _int_or_none(diagnostics.get("finite_sample_count")),
        "nonfinite_sample_count": _int_or_none(
            diagnostics.get("nonfinite_sample_count")
        ),
        "raw_diagnostics": _json_ready(diagnostics),
        "runtime_metadata": _json_ready(metadata),
        "runtime_evidence": runtime_evidence,
        "fixture_or_synthetic": fixture_or_synthetic,
        "acceptance_trace_key_present": "is_accepted" in trace,
        "acceptance_policy_filled_or_default": policy_filled_or_default,
        "trace_summary": {
            "trace_keys": tuple(sorted(trace.keys())),
            "trace_unavailability": metadata.get("trace_unavailability"),
        },
    }
    return payload


def _with_windowed_stage_timing_metadata(
    capture: Mapping[str, Any],
    *,
    runner_build_s: float,
    runner_execute_s: float,
    capture_s: float,
    route_category: str,
) -> Mapping[str, Any]:
    payload = dict(capture)
    metadata = dict(payload.get("runtime_metadata", {}))
    timing_buckets = dict(metadata.get("timing_buckets", {}))
    timing_buckets.update(
        {
            "windowed_stage_runner_build_s": (
                "explanatory_only_windowed_stage_runner_build"
            ),
            "windowed_stage_runner_execute_s": (
                "explanatory_only_windowed_stage_sample_chain_call"
            ),
            "windowed_stage_capture_s": (
                "explanatory_only_windowed_stage_public_safe_capture"
            ),
        }
    )
    metadata.update(
        {
            "windowed_stage_route_category": str(route_category),
            "windowed_stage_runner_build_s": float(runner_build_s),
            "windowed_stage_runner_execute_s": float(runner_execute_s),
            "windowed_stage_capture_s": float(capture_s),
            "windowed_stage_timing_scope": (
                "public_safe_runner_build_execute_and_capture_timing"
            ),
            "timing_buckets": timing_buckets,
        }
    )
    payload["runtime_metadata"] = metadata
    return payload


def _windowed_stage_error_capture(exc: Exception) -> Mapping[str, Any]:
    return {
        "error_type": type(exc).__name__,
        "error_message": str(exc),
        "warmup_draws": None,
        "acceptance_trace": None,
        "log_accept_ratio": None,
        "target_log_prob": None,
        "runtime_s": None,
        "runtime_finite": False,
        "samples_shape": None,
        "acceptance_shape": None,
        "log_accept_shape": None,
        "target_log_prob_shape": None,
        "expected_steps": None,
        "target_dimension": None,
        "finite_sample_count": None,
        "nonfinite_sample_count": None,
        "raw_diagnostics": {},
        "runtime_metadata": {},
        "runtime_evidence": "error",
        "fixture_or_synthetic": False,
        "acceptance_trace_key_present": False,
        "acceptance_policy_filled_or_default": True,
        "trace_summary": {"trace_keys": (), "trace_unavailability": {}},
    }


def _classify_windowed_stage_capture(
    capture: Mapping[str, Any],
    *,
    run_error: Exception | None,
) -> tuple[str, ...]:
    hard_vetoes: list[str] = []
    if run_error is not None:
        hard_vetoes.append("windowed_stage_hmc_error")
    expected_steps = capture.get("expected_steps")
    target_dimension = capture.get("target_dimension")
    draws = capture.get("warmup_draws")
    acceptance = capture.get("acceptance_trace")
    log_accept = capture.get("log_accept_ratio")
    target_log_prob = capture.get("target_log_prob")
    if capture.get("runtime_finite") is not True:
        hard_vetoes.append("windowed_stage_runtime_missing_or_nonfinite")
    if capture.get("runtime_evidence") != "tfp_hmc_runtime":
        hard_vetoes.append("windowed_stage_fixture_or_nonruntime_telemetry")
    if capture.get("fixture_or_synthetic") is True:
        hard_vetoes.append("windowed_stage_fixture_or_nonruntime_telemetry")
    if not _valid_draw_matrix(draws, expected_steps, target_dimension):
        hard_vetoes.append("windowed_stage_warmup_draws_invalid")
    if (
        not _valid_trace_vector(acceptance, expected_steps, bounds=(0.0, 1.0))
        or capture.get("acceptance_policy_filled_or_default") is True
    ):
        hard_vetoes.append("windowed_stage_acceptance_telemetry_invalid_or_default")
    if not _valid_trace_vector(log_accept, expected_steps):
        hard_vetoes.append("windowed_stage_log_accept_invalid")
    if not _valid_trace_vector(target_log_prob, expected_steps):
        hard_vetoes.append("windowed_stage_target_log_prob_invalid")
    return tuple(dict.fromkeys(hard_vetoes))


def _valid_draw_matrix(value: Any, expected_steps: Any, target_dimension: Any) -> bool:
    if value is None or expected_steps is None or target_dimension is None:
        return False
    array = np.asarray(value, dtype=float)
    if array.shape != (int(expected_steps), int(target_dimension)):
        return False
    return bool(np.all(np.isfinite(array)))


def _valid_trace_vector(
    value: Any,
    expected_steps: Any,
    *,
    bounds: tuple[float, float] | None = None,
) -> bool:
    if value is None or expected_steps is None:
        return False
    array = np.asarray(value, dtype=float)
    if array.shape != (int(expected_steps),):
        return False
    if not np.all(np.isfinite(array)):
        return False
    if bounds is not None:
        lower, upper = bounds
        if np.any((array < lower) | (array > upper)):
            return False
    return True


def _acceptance_trace_is_default_like(value: Any) -> bool:
    if value is None:
        return True
    array = np.asarray(value, dtype=float)
    if array.size == 0:
        return True
    return bool(np.allclose(array, array.reshape(-1)[0]))


def _windowed_stage_runtime_evidence(metadata: Mapping[str, Any]) -> str:
    if _metadata_marks_fixture_or_synthetic(metadata):
        return "fixture_or_synthetic"
    if metadata.get("runtime") != "tfp.mcmc.sample_chain":
        return "missing_or_unknown_runtime"
    invocation_count = _int_or_none(metadata.get("sample_chain_invocation_count"))
    if invocation_count is None or invocation_count <= 0:
        return "missing_or_unknown_runtime"
    return "tfp_hmc_runtime"


def _metadata_marks_fixture_or_synthetic(metadata: Mapping[str, Any]) -> bool:
    for key in ("fixture_or_synthetic", "test_fixture", "synthetic"):
        if metadata.get(key) is True:
            return True
    nonclaims = metadata.get("nonclaims", ())
    if isinstance(nonclaims, str):
        candidates = (nonclaims,)
    else:
        try:
            candidates = tuple(nonclaims)
        except TypeError:
            candidates = ()
    markers = ("fake", "fixture", "synthetic", "test-only", "unit test")
    return any(
        any(marker in str(item).lower() for marker in markers)
        for item in candidates
    )


def _windowed_stage_diagnostics(
    capture: Mapping[str, Any],
    *,
    windowed_result: WindowedMassAdaptationResult | None,
    hard_vetoes: tuple[str, ...],
) -> Mapping[str, Any]:
    return {
        "passed": not hard_vetoes,
        "hard_vetoes": hard_vetoes,
        "runtime_s": capture.get("runtime_s"),
        "runtime_finite": capture.get("runtime_finite"),
        "samples_shape": capture.get("samples_shape"),
        "acceptance_shape": capture.get("acceptance_shape"),
        "log_accept_shape": capture.get("log_accept_shape"),
        "target_log_prob_shape": capture.get("target_log_prob_shape"),
        "finite_sample_count": capture.get("finite_sample_count"),
        "nonfinite_sample_count": capture.get("nonfinite_sample_count"),
        "windowed_mass_passed": None
        if windowed_result is None
        else bool(windowed_result.passed),
        "adapted_mass_artifact_signature": None
        if windowed_result is None
        else windowed_result.final_mass_artifact_signature,
        "candidate_step_size": None
        if windowed_result is None
        else windowed_result.final_step_size,
        "reports_posterior_convergence": False,
        "raw_diagnostics": capture.get("raw_diagnostics", {}),
        "runtime_metadata": capture.get("runtime_metadata", {}),
        "trace_summary": capture.get("trace_summary", {}),
        "windowed_mass_error_type": capture.get("windowed_mass_error_type"),
        "windowed_mass_error_message": capture.get("windowed_mass_error_message"),
        "nonclaims": WINDOWED_MASS_STAGE_NONCLAIMS,
    }


def _warmup_draw_provenance(
    capture: Mapping[str, Any],
    draw_capture_policy: Mapping[str, Any],
) -> Mapping[str, Any]:
    return {
        "source": "run_full_chain_tfp_hmc_retained_samples",
        "sample_space": "latent_fixed_mass",
        "samples_shape": capture.get("samples_shape"),
        "expected_steps": capture.get("expected_steps"),
        "target_dimension": capture.get("target_dimension"),
        "draw_capture_policy_hash": stable_config_hash(draw_capture_policy),
        "fixture_or_synthetic": bool(capture.get("fixture_or_synthetic")),
        "runtime_evidence": capture.get("runtime_evidence"),
        "adaptation_input_only": True,
        "posterior_samples": False,
    }


def _acceptance_telemetry_provenance(
    capture: Mapping[str, Any],
) -> Mapping[str, Any]:
    acceptance = capture.get("acceptance_trace")
    return {
        "source": "run_full_chain_tfp_hmc_trace.is_accepted",
        "shape": capture.get("acceptance_shape"),
        "expected_steps": capture.get("expected_steps"),
        "trace_key_present": bool(capture.get("acceptance_trace_key_present")),
        "fixture_or_synthetic": bool(capture.get("fixture_or_synthetic")),
        "policy_filled_or_default": bool(
            capture.get("acceptance_policy_filled_or_default")
        ),
        "runtime_evidence": capture.get("runtime_evidence"),
        "finite_and_aligned": _valid_trace_vector(
            acceptance,
            capture.get("expected_steps"),
            bounds=(0.0, 1.0),
        ),
    }


def _validate_value_score_shapes(*, theta: Any, value: Any, score: Any) -> None:
    theta_shape = theta.shape
    value_shape = value.shape
    score_shape = score.shape
    if theta_shape.rank == 1:
        parameter_dim = theta_shape[-1]
        if parameter_dim is None:
            raise ValueError("scalar theta must have static parameter dimension")
        if value_shape.rank not in (0, None):
            raise ValueError("scalar target value must be rank 0")
        if score_shape.rank != 1:
            raise ValueError("scalar target score must have rank 1")
        if score_shape[-1] is not None and int(score_shape[-1]) != int(parameter_dim):
            raise ValueError("scalar target score parameter dimension mismatch")
        return
    if theta_shape.rank == 2:
        batch_size = theta_shape[0]
        parameter_dim = theta_shape[1]
        if batch_size is None or parameter_dim is None:
            raise ValueError("batched theta must have static batch and parameter dimensions")
        if value_shape.rank != 1:
            raise ValueError("batched target value must be rank 1")
        if score_shape.rank != 2:
            raise ValueError("batched target score must be rank 2")
        if value_shape[0] is not None and int(value_shape[0]) != int(batch_size):
            raise ValueError("batched target value leading dimension mismatch")
        if score_shape[0] is not None and int(score_shape[0]) != int(batch_size):
            raise ValueError("batched target score leading dimension mismatch")
        if score_shape[1] is not None and int(score_shape[1]) != int(parameter_dim):
            raise ValueError("batched target score parameter dimension mismatch")
        return
    raise ValueError("theta must have rank 1 [parameter] or rank 2 [batch, parameter]")


def _bootstrap_screen_config(
    config: HMCBootstrapScreenConfig,
    *,
    seed: tuple[int, int],
    step: float,
    leapfrogs: int,
    target_scope: str,
) -> FullChainHMCConfig:
    return FullChainHMCConfig(
        num_results=config.screen_num_results,
        num_burnin_steps=config.screen_num_burnin_steps,
        step_size=float(step),
        num_leapfrog_steps=int(leapfrogs),
        seed=seed,
        use_xla=config.use_xla,
        trace_policy="standard",
        target_status_trace_policy=config.target_status_trace_policy,
        target_scope=target_scope,
        chain_execution_mode=config.chain_execution_mode,
    )


def _bootstrap_leapfrog_payload(
    step: float,
    target_trajectory: float,
) -> Mapping[str, Any]:
    raw = int(np.ceil(float(target_trajectory) / float(step)))
    if raw <= 0:
        raise ValueError("formula-derived bootstrap leapfrog count must be positive")
    leapfrogs = int(np.clip(raw, _GEOMETRY_MIN_LEAPFROG, _GEOMETRY_MAX_LEAPFROG))
    if leapfrogs == raw:
        clamp_direction = None
    elif raw < _GEOMETRY_MIN_LEAPFROG:
        clamp_direction = "min"
    else:
        clamp_direction = "max"
    return {
        "num_leapfrog_steps": leapfrogs,
        "unclamped_num_leapfrog_steps": raw,
        "leapfrog_clamped": leapfrogs != raw,
        "clamp_direction": clamp_direction,
        "internal_min_leapfrog": _GEOMETRY_MIN_LEAPFROG,
        "internal_max_leapfrog": _GEOMETRY_MAX_LEAPFROG,
    }


def _bootstrap_reusable_static_contract_payload(
    config: FullChainHMCConfig,
    *,
    hmc_adapter_signature: str,
    target_dimension: int,
    mass_signature: str,
) -> Mapping[str, Any]:
    """Return the bootstrap fields that fix the reusable runner graph.

    ``ReusableFullChainHMCRunner`` accepts seed, current state, and step size as
    runtime tensors.  They are preserved in every round's
    ``screen_config_payload`` and selected-kernel payload, so they must not be
    part of the reusable static contract key.
    """

    tuning_payload = config.tuning_policy.payload()
    return {
        "semantic_source": "run_hmc_bootstrap_screen",
        "runner": "build_reusable_full_chain_tfp_hmc_runner",
        "hmc_adapter_signature": hmc_adapter_signature,
        "mass_artifact_signature": mass_signature,
        "target_dimension": int(target_dimension),
        "num_results": config.num_results,
        "num_burnin_steps": config.num_burnin_steps,
        "num_leapfrog_steps": config.num_leapfrog_steps,
        "use_xla": config.use_xla,
        "chain_execution_mode": config.chain_execution_mode,
        "trace_policy": config.trace_policy,
        "target_status_trace_policy": config.target_status_trace_policy,
        "adaptation_policy": config.adaptation_policy,
        "tuning_policy": tuning_payload,
        "target_scope": config.target_scope,
        "dynamic_inputs": ("current_state", "seed", "step_size"),
        "excluded_dynamic_fields": ("seed", "step_size"),
    }


def _bootstrap_diagnostics_payload(
    run_result: FullChainHMCRunResult,
    *,
    use_xla_requested: bool | None = None,
    compile_chain_with_xla: bool | None = None,
) -> Mapping[str, Any]:
    diagnostics = dict(run_result.diagnostics)
    trace = dict(run_result.trace)
    metadata = dict(run_result.metadata)
    acceptance = _scalar_or_none(diagnostics.get("acceptance_rate"))
    runtime_s = _runtime_seconds_or_none(metadata)
    use_xla_metadata = _bool_or_none(metadata.get("use_xla"))
    jit_compile_metadata = _bool_or_none(metadata.get("jit_compile"))
    use_xla = (
        bool(use_xla_requested)
        if use_xla_requested is not None
        else bool(use_xla_metadata)
    )
    jit_compile = (
        bool(compile_chain_with_xla)
        if compile_chain_with_xla is not None
        else bool(jit_compile_metadata)
    )
    payload: dict[str, Any] = {
        "acceptance_rate": acceptance,
        "runtime_s": runtime_s,
        "runtime_finite": runtime_s is not None and bool(np.isfinite(runtime_s)),
        "use_xla": use_xla,
        "xla_requested": use_xla,
        "compile_chain_with_xla": jit_compile,
        "jit_compile_metadata": "true" if jit_compile else "false",
        "finite_sample_count": _int_or_none(diagnostics.get("finite_sample_count")),
        "nonfinite_sample_count": _int_or_none(
            diagnostics.get("nonfinite_sample_count")
        ),
        "target_accept_prob": _scalar_or_none(diagnostics.get("target_accept_prob")),
        "num_adaptation_steps": _int_or_none(diagnostics.get("num_adaptation_steps")),
        "trace_policy": diagnostics.get("trace_policy"),
        "divergence_status": diagnostics.get("divergence_status"),
        "divergence_count": _int_or_none(diagnostics.get("divergence_count")),
        "target_status_telemetry": _telemetry_payload(
            diagnostics.get("target_status_telemetry")
        ),
        "log_accept_ratio_finite": None,
        "max_abs_log_accept_ratio": None,
        "target_log_prob_finite": None,
        "samples_all_finite": None,
        "screen_diagnostic": None,
        "raw_diagnostics": _json_ready(diagnostics),
        "runtime_metadata": _json_ready(metadata),
        "trace_summary": {
            "trace_keys": tuple(sorted(trace.keys())),
            "trace_unavailability": metadata.get("trace_unavailability"),
        },
    }
    log_accept = None
    if "log_accept_ratio" in trace:
        log_accept = np.asarray(_tensor_to_numpy(trace["log_accept_ratio"]), dtype=float)
        finite = np.isfinite(log_accept)
        payload["log_accept_ratio_finite"] = bool(np.all(finite))
        payload["max_abs_log_accept_ratio"] = (
            None if not np.any(finite) else float(np.max(np.abs(log_accept[finite])))
        )
    target_log_prob = None
    if "target_log_prob" in trace:
        target_log_prob = np.asarray(
            _tensor_to_numpy(trace["target_log_prob"]),
            dtype=float,
        )
        payload["target_log_prob_finite"] = bool(
            np.all(np.isfinite(target_log_prob))
        )
    samples = np.asarray(_tensor_to_numpy(run_result.samples), dtype=float)
    finite_by_sample = np.all(np.isfinite(samples), axis=-1)
    samples_all_finite = bool(np.all(finite_by_sample))
    payload["samples_all_finite"] = samples_all_finite
    required_arrays_finite = bool(
        samples_all_finite and payload["target_log_prob_finite"] is not False
    )
    screen = screen_hmc_diagnostics(
        sample_chain_returned=True,
        hmc_error_absent=True,
        required_arrays_finite=required_arrays_finite,
        log_accept_ratio=log_accept,
        divergences=trace.get("divergence"),
        acceptance_rate_by_chain=None if acceptance is None else (acceptance,),
        fixed_kernel_used=True,
        num_adaptation_steps_zero=True,
        latent_initial_scale_zero=True,
        use_xla_false=None if use_xla else True,
        compile_chain_with_xla_false=None if jit_compile else True,
        diagnostic_role="bootstrap fixed-kernel screen only",
    )
    payload["screen_diagnostic"] = {
        "passed": screen.passed,
        "checks": dict(screen.checks),
        "diagnostic_roles": dict(screen.diagnostic_roles),
        "unavailable_diagnostics": screen.unavailable_diagnostics,
        "nonclaims": screen.nonclaims,
    }
    if target_log_prob is not None:
        finite = target_log_prob[np.isfinite(target_log_prob)]
        payload["target_log_prob_min"] = (
            None if finite.size == 0 else float(np.min(finite))
        )
        payload["target_log_prob_max"] = (
            None if finite.size == 0 else float(np.max(finite))
        )
    return payload


def _telemetry_payload(value: Any) -> Mapping[str, Any] | None:
    if value is None:
        return None
    payload = {key: _json_ready(item) for key, item in dict(value).items()}
    if "telemetry_failure_veto" in value:
        payload["telemetry_failure_veto_bool"] = bool(
            _bool_or_none(value["telemetry_failure_veto"])
        )
    return payload


def _runtime_seconds_or_none(metadata: Mapping[str, Any]) -> float | None:
    for key in ("sample_chain_call_s", "first_call_s", "warm_call_s"):
        scalar = _scalar_or_none(metadata.get(key))
        if scalar is not None:
            return scalar
    return None


def _bootstrap_error_diagnostics(exc: Exception) -> Mapping[str, Any]:
    return {
        "error_type": type(exc).__name__,
        "error_message": str(exc),
        "acceptance_rate": None,
        "runtime_s": None,
        "runtime_finite": False,
        "samples_all_finite": False,
        "log_accept_ratio_finite": False,
        "target_log_prob_finite": False,
        "screen_diagnostic": {
            "passed": False,
            "checks": {
                "sample_chain_returned": False,
                "hmc_error_absent": False,
            },
            "diagnostic_roles": {"screen": "bootstrap runtime hard veto"},
            "unavailable_diagnostics": (),
            "nonclaims": BOOTSTRAP_SCREEN_NONCLAIMS,
        },
    }


def _classify_bootstrap_screen(
    config: HMCBootstrapScreenConfig,
    *,
    diagnostics: Mapping[str, Any],
    screen_error: Exception | None,
) -> tuple[str, str, tuple[str, ...], tuple[str, ...]]:
    hard_vetoes: list[str] = []
    if screen_error is not None:
        hard_vetoes.append("screen_hmc_error")
    acceptance = diagnostics.get("acceptance_rate")
    if acceptance is None or not _finite_number(acceptance):
        hard_vetoes.append("screen_acceptance_missing_or_nonfinite")
    if diagnostics.get("runtime_finite") is not True:
        hard_vetoes.append("screen_runtime_missing_or_nonfinite")
    if diagnostics.get("log_accept_ratio_finite") is not True:
        hard_vetoes.append("screen_log_accept_nonfinite_or_missing")
    if diagnostics.get("samples_all_finite") is not True:
        hard_vetoes.append("screen_samples_nonfinite_or_missing")
    if diagnostics.get("target_log_prob_finite") is not True:
        hard_vetoes.append("screen_target_log_prob_nonfinite_or_missing")
    telemetry = diagnostics.get("target_status_telemetry")
    if isinstance(telemetry, Mapping) and telemetry.get("telemetry_failure_veto_bool"):
        hard_vetoes.append("screen_target_status_telemetry_failure")
    if hard_vetoes:
        return "hard_veto", "hard_veto", tuple(hard_vetoes), ()
    acceptance_value = float(acceptance)
    if config.acceptance_band[0] <= acceptance_value <= config.acceptance_band[1]:
        return "passed", "bootstrap_screen_promotion_only", (), ()
    if acceptance_value < config.acceptance_band[0]:
        trigger = (
            "acceptance_below_repair_band"
            if acceptance_value < config.repair_band[0]
            else "acceptance_below_acceptance_band_inside_repair_band"
        )
        return (
            "repair",
            "bootstrap_acceptance_repair_trigger",
            (),
            (trigger,),
        )
    trigger = (
        "acceptance_above_repair_band"
        if acceptance_value > config.repair_band[1]
        else "acceptance_above_acceptance_band_inside_repair_band"
    )
    return (
        "repair",
        "bootstrap_acceptance_repair_trigger",
        (),
        (trigger,),
    )


def _bootstrap_repair_action(
    config: HMCBootstrapScreenConfig,
    acceptance: float | None,
    *,
    low_acceptance_step: float | None = None,
    high_acceptance_step: float | None = None,
) -> str:
    if acceptance is None or not np.isfinite(float(acceptance)):
        return "no_repair_nonfinite_acceptance"
    if low_acceptance_step is not None and high_acceptance_step is not None:
        _validate_bootstrap_repair_bracket(
            low_acceptance_step=low_acceptance_step,
            high_acceptance_step=high_acceptance_step,
        )
        return "bracketed_log_step_midpoint_recompute_l"
    if float(acceptance) < config.acceptance_band[0]:
        return "reduce_epsilon_recompute_l"
    return "increase_epsilon_recompute_l"


def _bootstrap_update_repair_bracket(
    config: HMCBootstrapScreenConfig,
    *,
    current_step: float,
    acceptance: float | None,
    low_acceptance_step: float | None,
    high_acceptance_step: float | None,
) -> tuple[float | None, float | None]:
    if acceptance is None or not np.isfinite(float(acceptance)):
        return low_acceptance_step, high_acceptance_step
    step = float(current_step)
    if not np.isfinite(step) or step <= 0.0:
        raise ValueError("bootstrap repair bracket step must be positive and finite")
    if float(acceptance) < config.acceptance_band[0]:
        low_acceptance_step = step
    else:
        high_acceptance_step = step
    if low_acceptance_step is not None and high_acceptance_step is not None:
        _validate_bootstrap_repair_bracket(
            low_acceptance_step=low_acceptance_step,
            high_acceptance_step=high_acceptance_step,
        )
    return low_acceptance_step, high_acceptance_step


def _validate_bootstrap_repair_bracket(
    *,
    low_acceptance_step: float,
    high_acceptance_step: float,
) -> None:
    low_step = float(low_acceptance_step)
    high_step = float(high_acceptance_step)
    if (
        not np.isfinite(low_step)
        or low_step <= 0.0
        or not np.isfinite(high_step)
        or high_step <= 0.0
    ):
        raise ValueError("bootstrap repair bracket endpoints must be positive and finite")
    if not np.log(high_step) < np.log(low_step):
        raise ValueError("bootstrap repair bracket endpoints must be ordered in log-step space")


def _repair_step_size(
    config: HMCBootstrapScreenConfig,
    *,
    current_step: float,
    acceptance: float | None,
    low_acceptance_step: float | None = None,
    high_acceptance_step: float | None = None,
) -> float:
    if acceptance is None or not np.isfinite(float(acceptance)):
        raise ValueError("finite acceptance is required for epsilon repair")
    if low_acceptance_step is not None and high_acceptance_step is not None:
        _validate_bootstrap_repair_bracket(
            low_acceptance_step=low_acceptance_step,
            high_acceptance_step=high_acceptance_step,
        )
        repaired = float(np.exp(
            0.5 * (np.log(float(low_acceptance_step)) + np.log(float(high_acceptance_step)))
        ))
    else:
        factor = 0.5 if float(acceptance) < config.acceptance_band[0] else 2.0
        repaired = float(current_step) * factor
    if not np.isfinite(repaired) or repaired <= 0.0:
        raise ValueError("repaired bootstrap step size must be positive and finite")
    return repaired


def _round_seed(base: tuple[int, int], index: int) -> tuple[int, int]:
    return int(base[0]), int(base[1]) + int(index)


def _validate_seed(seed: Sequence[int]) -> tuple[int, int]:
    values = tuple(int(item) for item in seed)
    if len(values) != 2:
        raise ValueError("seed must contain exactly two integers")
    return values


def _seed_from_mapping(mapping: Mapping[str, Any], key: str) -> tuple[int, int] | None:
    value = mapping.get(key)
    if value is None:
        return None
    return _validate_seed(value)


def _validate_band(values: Sequence[float], *, name: str) -> tuple[float, float]:
    values = tuple(values)
    if len(values) != 2:
        raise ValueError(f"{name} must contain exactly two values")
    lower, upper = tuple(float(item) for item in values)
    if not np.isfinite(lower) or not np.isfinite(upper):
        raise ValueError(f"{name} values must be finite")
    if not 0.0 < lower <= upper < 1.0:
        raise ValueError(f"{name} must satisfy 0 < lower <= upper < 1")
    return lower, upper


def _ceil_div(numerator: int, denominator: int) -> int:
    numerator = int(numerator)
    denominator = int(denominator)
    if denominator <= 0:
        raise ValueError("denominator must be positive")
    return -(-numerator // denominator)


def _string_tuple(values: Sequence[str] | str) -> tuple[str, ...]:
    if isinstance(values, str):
        raw = (values,)
    else:
        raw = tuple(values)
    return tuple(str(item) for item in raw if str(item))


def _finite_number(value: Any) -> bool:
    scalar = _scalar_or_none(value)
    return scalar is not None and bool(np.isfinite(scalar))


def _tensor_to_numpy(value: Any) -> Any:
    if hasattr(value, "numpy"):
        return value.numpy()
    return value


def _trace_array_or_none(trace: Mapping[str, Any], key: str) -> np.ndarray | None:
    if key not in trace:
        return None
    return np.asarray(_tensor_to_numpy(trace[key]))


def _scalar_or_none(value: Any) -> float | None:
    if value is None:
        return None
    array = np.asarray(_tensor_to_numpy(value))
    if array.size == 0:
        return None
    try:
        return float(array.reshape(-1)[-1])
    except (TypeError, ValueError):
        return None


def _int_or_none(value: Any) -> int | None:
    scalar = _scalar_or_none(value)
    return None if scalar is None else int(scalar)


def _bool_or_none(value: Any) -> bool | None:
    if value is None:
        return None
    array = np.asarray(_tensor_to_numpy(value))
    if array.size == 0:
        return None
    return bool(array.reshape(-1)[-1])


def _json_ready(value: Any) -> Any:
    if hasattr(value, "numpy"):
        return _json_ready(value.numpy())
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, Mapping):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_ready(item) for item in value]
    return value
