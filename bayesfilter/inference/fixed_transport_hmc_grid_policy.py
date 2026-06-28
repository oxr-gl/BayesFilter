"""Generic fixed-transport HMC candidate-grid policy contracts.

This module owns the BayesFilter side of fixed-NeuTra HMC candidate generation.
Model-specific repositories should consume the policy-spec payload and execute
the candidates; they should not rebuild generic HMC step/leapfrog grids.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from bayesfilter.runtime import stable_config_hash


FIXED_TRANSPORT_HMC_GRID_POLICY_NONCLAIMS: tuple[str, ...] = (
    "generic fixed-transport HMC candidate-grid policy only",
    "does not run HMC",
    "does not adapt a trained transport",
    "does not claim posterior convergence",
    "does not claim sampler superiority",
    "does not claim model-specific scientific validity",
)


def _finite_positive(value: float, *, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be positive and finite")
    return number


def _finite_probability(value: float | None) -> float | None:
    if value is None:
        return None
    number = float(value)
    if not math.isfinite(number) or number < 0.0 or number > 1.0:
        return None
    return number


def _rounded(value: float) -> float:
    return round(float(value), 12)


@dataclass(frozen=True)
class FixedTransportHMCGridPolicyConfig:
    """Configuration for a generic fixed-transport HMC candidate policy."""

    base_step_size_candidates: tuple[float, ...] = (
        0.05, 0.075, 0.1, 0.15, 0.2, 0.3, 0.5)
    num_leapfrog_step_candidates: tuple[int, ...] = (1, 2, 3, 4, 8, 16, 25)
    acceptance_band: tuple[float, float] = (0.65, 0.75)
    high_acceptance_refinement_max: float = 0.85
    max_num_leapfrog_steps: int = 25
    refinement_leapfrog_step: int = 2
    refinement_lower_leapfrog_margin: int = 4
    refinement_step_size_increment: float = 0.05
    refinement_step_size_count: int = 5
    policy_source: str = "bayesfilter.inference.fixed_transport_hmc_grid_policy"
    schema_version: int = 1

    def __post_init__(self) -> None:
        base_steps = tuple(
            _finite_positive(item, name="base_step_size_candidates")
            for item in self.base_step_size_candidates
        )
        if not base_steps:
            raise ValueError("base_step_size_candidates must be non-empty")
        leapfrogs = tuple(int(item) for item in self.num_leapfrog_step_candidates)
        if not leapfrogs or any(item <= 0 for item in leapfrogs):
            raise ValueError("num_leapfrog_step_candidates must be positive")
        lower, upper = (float(self.acceptance_band[0]), float(self.acceptance_band[1]))
        if not (math.isfinite(lower) and math.isfinite(upper) and 0.0 < lower <= upper < 1.0):
            raise ValueError("acceptance_band must satisfy 0 < lower <= upper < 1")
        high_max = float(self.high_acceptance_refinement_max)
        if not (math.isfinite(high_max) and upper <= high_max < 1.0):
            raise ValueError("high_acceptance_refinement_max must be in [upper, 1)")
        max_l = int(self.max_num_leapfrog_steps)
        if max_l <= 0:
            raise ValueError("max_num_leapfrog_steps must be positive")
        step = int(self.refinement_leapfrog_step)
        margin = int(self.refinement_lower_leapfrog_margin)
        count = int(self.refinement_step_size_count)
        if step <= 0 or margin < 0 or count <= 0:
            raise ValueError("refinement step, margin, and count must be valid")
        increment = _finite_positive(
            self.refinement_step_size_increment,
            name="refinement_step_size_increment",
        )
        source = str(self.policy_source)
        if not source:
            raise ValueError("policy_source must be non-empty")
        schema = int(self.schema_version)
        if schema <= 0:
            raise ValueError("schema_version must be positive")
        object.__setattr__(self, "base_step_size_candidates", base_steps)
        object.__setattr__(self, "num_leapfrog_step_candidates", tuple(dict.fromkeys(leapfrogs)))
        object.__setattr__(self, "acceptance_band", (lower, upper))
        object.__setattr__(self, "high_acceptance_refinement_max", high_max)
        object.__setattr__(self, "max_num_leapfrog_steps", max_l)
        object.__setattr__(self, "refinement_leapfrog_step", step)
        object.__setattr__(self, "refinement_lower_leapfrog_margin", margin)
        object.__setattr__(self, "refinement_step_size_increment", increment)
        object.__setattr__(self, "refinement_step_size_count", count)
        object.__setattr__(self, "policy_source", source)
        object.__setattr__(self, "schema_version", schema)

    def payload(self) -> Mapping[str, Any]:
        return {
            "schema_version": self.schema_version,
            "base_step_size_candidates": self.base_step_size_candidates,
            "num_leapfrog_step_candidates": self.num_leapfrog_step_candidates,
            "acceptance_band": self.acceptance_band,
            "high_acceptance_refinement_max": self.high_acceptance_refinement_max,
            "max_num_leapfrog_steps": self.max_num_leapfrog_steps,
            "refinement_leapfrog_step": self.refinement_leapfrog_step,
            "refinement_lower_leapfrog_margin": self.refinement_lower_leapfrog_margin,
            "refinement_step_size_increment": self.refinement_step_size_increment,
            "refinement_step_size_count": self.refinement_step_size_count,
            "policy_source": self.policy_source,
        }


@dataclass(frozen=True)
class FixedTransportHMCGridCandidateSpec:
    """One executable HMC candidate emitted by a policy spec."""

    candidate_index: int
    step_size: float
    num_leapfrog_steps: int
    grid_stage: str
    base_step_size: float | None = None
    step_size_scale: float | None = None
    refinement_reason: str | None = None

    def __post_init__(self) -> None:
        index = int(self.candidate_index)
        if index < 0:
            raise ValueError("candidate_index must be non-negative")
        step = _finite_positive(self.step_size, name="step_size")
        leapfrog = int(self.num_leapfrog_steps)
        if leapfrog <= 0:
            raise ValueError("num_leapfrog_steps must be positive")
        stage = str(self.grid_stage)
        if not stage:
            raise ValueError("grid_stage must be non-empty")
        base = (
            None if self.base_step_size is None
            else _finite_positive(self.base_step_size, name="base_step_size")
        )
        scale = (
            None if self.step_size_scale is None
            else _finite_positive(self.step_size_scale, name="step_size_scale")
        )
        reason = None if self.refinement_reason is None else str(self.refinement_reason)
        object.__setattr__(self, "candidate_index", index)
        object.__setattr__(self, "step_size", _rounded(step))
        object.__setattr__(self, "num_leapfrog_steps", leapfrog)
        object.__setattr__(self, "grid_stage", stage)
        object.__setattr__(self, "base_step_size", None if base is None else _rounded(base))
        object.__setattr__(self, "step_size_scale", None if scale is None else _rounded(scale))
        object.__setattr__(self, "refinement_reason", reason)

    def identity(self) -> tuple[float, int]:
        return (self.step_size, self.num_leapfrog_steps)

    def payload(self) -> Mapping[str, Any]:
        return {
            "candidate_index": self.candidate_index,
            "step_size": self.step_size,
            "num_leapfrog_steps": self.num_leapfrog_steps,
            "trajectory_time": _rounded(self.step_size * self.num_leapfrog_steps),
            "grid_stage": self.grid_stage,
            "base_step_size": self.base_step_size,
            "step_size_scale": self.step_size_scale,
            "refinement_reason": self.refinement_reason,
        }


@dataclass(frozen=True)
class FixedTransportHMCGridPolicySpec:
    """Stable BayesFilter-owned policy artifact for model-specific executors."""

    config: FixedTransportHMCGridPolicyConfig
    candidate_specs: tuple[FixedTransportHMCGridCandidateSpec, ...]
    status: str
    refinement_reasons: tuple[str, ...] = ()
    selection_rule: str = "shortest_leapfrog_acceptance_in_band_then_diagnostics"
    nonclaims: tuple[str, ...] = FIXED_TRANSPORT_HMC_GRID_POLICY_NONCLAIMS

    def __post_init__(self) -> None:
        candidates = tuple(self.candidate_specs)
        if not candidates:
            raise ValueError("candidate_specs must be non-empty")
        identities = [candidate.identity() for candidate in candidates]
        if len(set(identities)) != len(identities):
            raise ValueError("candidate_specs must be unique by step_size and L")
        status = str(self.status)
        if not status:
            raise ValueError("status must be non-empty")
        selection = str(self.selection_rule)
        if not selection:
            raise ValueError("selection_rule must be non-empty")
        object.__setattr__(self, "candidate_specs", candidates)
        object.__setattr__(self, "status", status)
        object.__setattr__(
            self,
            "refinement_reasons",
            tuple(str(item) for item in self.refinement_reasons),
        )
        object.__setattr__(self, "selection_rule", selection)
        object.__setattr__(self, "nonclaims", tuple(str(item) for item in self.nonclaims))

    def payload(self) -> Mapping[str, Any]:
        payload = {
            "artifact_type": "bayesfilter_fixed_transport_hmc_grid_policy_spec",
            "schema_version": self.config.schema_version,
            "policy_source": self.config.policy_source,
            "config": self.config.payload(),
            "candidate_specs": tuple(candidate.payload() for candidate in self.candidate_specs),
            "candidate_count": len(self.candidate_specs),
            "status": self.status,
            "refinement_reasons": self.refinement_reasons,
            "selection_rule": self.selection_rule,
            "nonclaims": self.nonclaims,
        }
        return {
            **payload,
            "policy_hash": stable_config_hash(payload),
            "hash_function": "bayesfilter.runtime.stable_config_hash",
        }

    @property
    def policy_hash(self) -> str:
        return str(self.payload()["policy_hash"])


def build_fixed_transport_hmc_grid_policy_spec(
    *,
    step_size_scale: float,
    config: FixedTransportHMCGridPolicyConfig | None = None,
    observed_candidate_rows: Sequence[Mapping[str, Any]] = (),
) -> FixedTransportHMCGridPolicySpec:
    """Build a candidate-grid policy spec with optional boundary refinement."""

    policy = FixedTransportHMCGridPolicyConfig() if config is None else config
    scale = _finite_positive(step_size_scale, name="step_size_scale")
    candidates: list[FixedTransportHMCGridCandidateSpec] = []
    seen: set[tuple[float, int]] = set()

    def add_candidate(
        *,
        step_size: float,
        leapfrog: int,
        stage: str,
        base_step_size: float | None = None,
        reason: str | None = None,
    ) -> None:
        if int(leapfrog) > policy.max_num_leapfrog_steps:
            return
        candidate = FixedTransportHMCGridCandidateSpec(
            candidate_index=len(candidates),
            step_size=step_size,
            num_leapfrog_steps=int(leapfrog),
            grid_stage=stage,
            base_step_size=base_step_size,
            step_size_scale=scale,
            refinement_reason=reason,
        )
        identity = candidate.identity()
        if identity in seen:
            return
        seen.add(identity)
        candidates.append(candidate)

    for base_step in policy.base_step_size_candidates:
        for leapfrog in policy.num_leapfrog_step_candidates:
            add_candidate(
                step_size=base_step * scale,
                leapfrog=leapfrog,
                stage="coarse_grid",
                base_step_size=base_step,
            )

    reasons = []
    boundary = _boundary_refinement_request(policy, observed_candidate_rows)
    if boundary is not None:
        step_size, start_l, stop_l = boundary
        reason = "high_acceptance_shorter_L_and_in_band_longer_L_boundary"
        reasons.append(reason)
        for refined_step in _refined_step_sizes(policy, step_size):
            for leapfrog in _refined_leapfrogs(policy, start_l, stop_l):
                add_candidate(
                    step_size=refined_step,
                    leapfrog=leapfrog,
                    stage="local_refinement_grid",
                    reason=reason,
                )

    return FixedTransportHMCGridPolicySpec(
        config=policy,
        candidate_specs=tuple(
            FixedTransportHMCGridCandidateSpec(
                candidate_index=index,
                step_size=candidate.step_size,
                num_leapfrog_steps=candidate.num_leapfrog_steps,
                grid_stage=candidate.grid_stage,
                base_step_size=candidate.base_step_size,
                step_size_scale=candidate.step_size_scale,
                refinement_reason=candidate.refinement_reason,
            )
            for index, candidate in enumerate(candidates)
        ),
        status="refinement_added" if reasons else "coarse_grid_only",
        refinement_reasons=tuple(reasons),
    )


def _boundary_refinement_request(
    config: FixedTransportHMCGridPolicyConfig,
    rows: Sequence[Mapping[str, Any]],
) -> tuple[float, int, int] | None:
    lower, upper = config.acceptance_band
    del lower
    by_step: dict[float, list[tuple[int, float]]] = {}
    for row in rows:
        step = row.get("step_size")
        leapfrog = row.get("num_leapfrog_steps", row.get("leapfrog"))
        acceptance = _finite_probability(row.get("acceptance_rate"))
        if step is None or leapfrog is None or acceptance is None:
            continue
        step_value = _rounded(float(step))
        leapfrog_value = int(leapfrog)
        by_step.setdefault(step_value, []).append((leapfrog_value, acceptance))

    for step_value, diagnostics in sorted(by_step.items()):
        high = [
            (leapfrog, acceptance)
            for leapfrog, acceptance in diagnostics
            if upper < acceptance <= config.high_acceptance_refinement_max
        ]
        in_band = [
            (leapfrog, acceptance)
            for leapfrog, acceptance in diagnostics
            if config.acceptance_band[0] <= acceptance <= upper
        ]
        if not high or not in_band:
            continue
        shorter_high = min(high, key=lambda item: item[0])
        longer_in_band = min(
            (item for item in in_band if item[0] > shorter_high[0]),
            key=lambda item: item[0],
            default=None,
        )
        if longer_in_band is None:
            continue
        start = max(1, shorter_high[0] - config.refinement_lower_leapfrog_margin)
        stop = min(config.max_num_leapfrog_steps, longer_in_band[0])
        return (step_value, start, stop)
    return None


def _refined_step_sizes(
    config: FixedTransportHMCGridPolicyConfig,
    boundary_step_size: float,
) -> tuple[float, ...]:
    return tuple(
        _rounded(boundary_step_size + index * config.refinement_step_size_increment)
        for index in range(config.refinement_step_size_count)
    )


def _refined_leapfrogs(
    config: FixedTransportHMCGridPolicyConfig,
    start_l: int,
    stop_l: int,
) -> tuple[int, ...]:
    values = list(range(int(start_l), int(stop_l), config.refinement_leapfrog_step))
    values.append(int(stop_l))
    return tuple(dict.fromkeys(item for item in values if item <= config.max_num_leapfrog_steps))
