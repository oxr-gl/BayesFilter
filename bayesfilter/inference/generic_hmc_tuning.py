"""Generic BayesFilter-owned HMC tuning orchestration.

This module is an additive client-facing orchestration layer.  It composes the
existing BayesFilter HMC tuning and runtime primitives into a stable artifact
without changing the behavior of the lower-level diagnostic helpers.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

import numpy as np

from bayesfilter.inference.hmc import PrecomputedMassArtifact, stable_adapter_signature
from bayesfilter.inference.hmc_tuning import (
    FixedTrajectoryTuningConfig,
    HMCTuningPolicy,
    production_leapfrog_count,
    require_executable_tuning_policy,
)
from bayesfilter.runtime import CandidateResult, select_first_tie_candidate, stable_config_hash


GENERIC_HMC_TUNING_NONCLAIMS = (
    "generic HMC tuning orchestration artifact only",
    "acceptance is a tuning promotion screen only",
    "no posterior convergence claim",
    "no sampler superiority claim",
    "no default sampler readiness claim",
    "no client scientific validity claim",
)


@dataclass(frozen=True)
class GenericHMCTuningConfig:
    """Client-facing fixed-kernel tuning orchestration settings."""

    step_size_candidates: tuple[float, ...]
    num_leapfrog_step_candidates: tuple[int, ...]
    acceptance_band: tuple[float, float] = (0.65, 0.75)
    tuning_seed: tuple[int, int] = (20260614, 21)
    heldout_seed: tuple[int, int] = (20260614, 22)
    target_trajectory_length: float = float(np.pi)
    policy_source: str = "bayesfilter.inference.generic_hmc_tuning"

    def __post_init__(self) -> None:
        steps = tuple(float(item) for item in self.step_size_candidates)
        if not steps:
            raise ValueError("step_size_candidates must be non-empty")
        if any((not np.isfinite(item)) or item <= 0.0 for item in steps):
            raise ValueError("step_size_candidates must be positive and finite")
        leapfrogs = tuple(int(item) for item in self.num_leapfrog_step_candidates)
        if not leapfrogs:
            raise ValueError("num_leapfrog_step_candidates must be non-empty")
        if any(item <= 0 for item in leapfrogs):
            raise ValueError("num_leapfrog_step_candidates must be positive")
        lower, upper = (float(self.acceptance_band[0]), float(self.acceptance_band[1]))
        if not (np.isfinite(lower) and np.isfinite(upper) and 0.0 < lower <= upper < 1.0):
            raise ValueError("acceptance_band must satisfy 0 < lower <= upper < 1")
        tuning_seed = tuple(int(item) for item in self.tuning_seed)
        heldout_seed = tuple(int(item) for item in self.heldout_seed)
        if len(tuning_seed) != 2 or len(heldout_seed) != 2:
            raise ValueError("seeds must contain exactly two integers")
        if tuning_seed == heldout_seed:
            raise ValueError("heldout_seed must differ from tuning_seed")
        target = float(self.target_trajectory_length)
        if not np.isfinite(target) or target <= 0.0:
            raise ValueError("target_trajectory_length must be positive and finite")
        source = str(self.policy_source)
        if not source:
            raise ValueError("policy_source must be non-empty")
        object.__setattr__(self, "step_size_candidates", steps)
        object.__setattr__(self, "num_leapfrog_step_candidates", leapfrogs)
        object.__setattr__(self, "acceptance_band", (lower, upper))
        object.__setattr__(self, "tuning_seed", tuning_seed)
        object.__setattr__(self, "heldout_seed", heldout_seed)
        object.__setattr__(self, "target_trajectory_length", target)
        object.__setattr__(self, "policy_source", source)

    def payload(self) -> Mapping[str, Any]:
        return {
            "step_size_candidates": self.step_size_candidates,
            "num_leapfrog_step_candidates": self.num_leapfrog_step_candidates,
            "acceptance_band": self.acceptance_band,
            "tuning_seed": self.tuning_seed,
            "heldout_seed": self.heldout_seed,
            "target_trajectory_length": self.target_trajectory_length,
            "policy_source": self.policy_source,
        }


@dataclass(frozen=True)
class GenericHMCCandidateResult:
    """One client-target candidate row with checkpoint-ready payload."""

    candidate_index: int
    step_size: float
    num_leapfrog_steps: int
    trajectory_length: float
    seed: tuple[int, int]
    acceptance_rate: float | None
    finite_sample_count: int
    nonfinite_sample_count: int
    log_accept_ratio_finite: bool
    outcome: str
    diagnostic_role: str
    vetoes: tuple[str, ...] = ()
    checkpoint_path: str | None = None

    def __post_init__(self) -> None:
        index = int(self.candidate_index)
        if index < 0:
            raise ValueError("candidate_index must be non-negative")
        step = float(self.step_size)
        if not np.isfinite(step) or step <= 0.0:
            raise ValueError("candidate step_size must be positive and finite")
        leapfrogs = int(self.num_leapfrog_steps)
        if leapfrogs <= 0:
            raise ValueError("candidate num_leapfrog_steps must be positive")
        trajectory = float(self.trajectory_length)
        if not np.isfinite(trajectory) or trajectory <= 0.0:
            raise ValueError("candidate trajectory_length must be positive and finite")
        seed = tuple(int(item) for item in self.seed)
        if len(seed) != 2:
            raise ValueError("candidate seed must contain exactly two integers")
        acceptance = None if self.acceptance_rate is None else float(self.acceptance_rate)
        if acceptance is not None and (
            not np.isfinite(acceptance) or acceptance < 0.0 or acceptance > 1.0
        ):
            raise ValueError("candidate acceptance_rate must be in [0, 1]")
        outcome = str(self.outcome)
        role = str(self.diagnostic_role)
        if not outcome or not role:
            raise ValueError("candidate outcome and diagnostic_role must be non-empty")
        checkpoint = None if self.checkpoint_path is None else str(self.checkpoint_path)
        object.__setattr__(self, "candidate_index", index)
        object.__setattr__(self, "step_size", step)
        object.__setattr__(self, "num_leapfrog_steps", leapfrogs)
        object.__setattr__(self, "trajectory_length", trajectory)
        object.__setattr__(self, "seed", seed)
        object.__setattr__(self, "acceptance_rate", acceptance)
        object.__setattr__(self, "finite_sample_count", int(self.finite_sample_count))
        object.__setattr__(self, "nonfinite_sample_count", int(self.nonfinite_sample_count))
        object.__setattr__(self, "log_accept_ratio_finite", bool(self.log_accept_ratio_finite))
        object.__setattr__(self, "outcome", outcome)
        object.__setattr__(self, "diagnostic_role", role)
        object.__setattr__(self, "vetoes", tuple(str(item) for item in self.vetoes))
        object.__setattr__(self, "checkpoint_path", checkpoint)

    @property
    def passed_screen(self) -> bool:
        return self.outcome == "passed_screen" and not self.vetoes

    def payload(self) -> Mapping[str, Any]:
        return {
            "candidate_index": self.candidate_index,
            "step_size": self.step_size,
            "num_leapfrog_steps": self.num_leapfrog_steps,
            "trajectory_length": self.trajectory_length,
            "seed": self.seed,
            "acceptance_rate": self.acceptance_rate,
            "finite_sample_count": self.finite_sample_count,
            "nonfinite_sample_count": self.nonfinite_sample_count,
            "log_accept_ratio_finite": self.log_accept_ratio_finite,
            "outcome": self.outcome,
            "diagnostic_role": self.diagnostic_role,
            "vetoes": self.vetoes,
            "checkpoint_path": self.checkpoint_path,
            "checkpoint_payload_hash": stable_config_hash(
                {
                    "candidate_index": self.candidate_index,
                    "step_size": self.step_size,
                    "num_leapfrog_steps": self.num_leapfrog_steps,
                    "seed": self.seed,
                    "acceptance_rate": self.acceptance_rate,
                    "outcome": self.outcome,
                    "vetoes": self.vetoes,
                }
            ),
        }


@dataclass(frozen=True)
class GenericHMCTuningResult:
    """Stable generic HMC tuning result for downstream clients."""

    policy: HMCTuningPolicy
    config: GenericHMCTuningConfig
    adapter_signature: str
    target_dimension: int
    mass_artifact_payload: Mapping[str, Any]
    mass_artifact_signature: str
    candidate_results: tuple[GenericHMCCandidateResult, ...]
    selected_candidate_index: int | None
    heldout_candidate: GenericHMCCandidateResult | None
    diagnostic_roles: Mapping[str, str]
    vetoes: tuple[str, ...]
    nonclaims: tuple[str, ...] = GENERIC_HMC_TUNING_NONCLAIMS

    def __post_init__(self) -> None:
        signature = str(self.adapter_signature)
        mass_signature = str(self.mass_artifact_signature)
        if not signature or not mass_signature:
            raise ValueError("adapter and mass artifact signatures must be non-empty")
        dimension = int(self.target_dimension)
        if dimension <= 0:
            raise ValueError("target_dimension must be positive")
        candidates = tuple(self.candidate_results)
        if not candidates:
            raise ValueError("candidate_results must be non-empty")
        selected = (
            None if self.selected_candidate_index is None else int(self.selected_candidate_index)
        )
        if selected is not None and all(item.candidate_index != selected for item in candidates):
            raise ValueError("selected_candidate_index must refer to a candidate")
        roles = {str(key): str(value) for key, value in self.diagnostic_roles.items()}
        if not roles:
            raise ValueError("diagnostic_roles must be non-empty")
        nonclaims = tuple(str(item) for item in self.nonclaims)
        if not nonclaims:
            raise ValueError("nonclaims must be non-empty")
        object.__setattr__(self, "adapter_signature", signature)
        object.__setattr__(self, "target_dimension", dimension)
        object.__setattr__(self, "mass_artifact_payload", dict(self.mass_artifact_payload))
        object.__setattr__(self, "mass_artifact_signature", mass_signature)
        object.__setattr__(self, "candidate_results", candidates)
        object.__setattr__(self, "selected_candidate_index", selected)
        object.__setattr__(self, "diagnostic_roles", roles)
        object.__setattr__(self, "vetoes", tuple(str(item) for item in self.vetoes))
        object.__setattr__(self, "nonclaims", nonclaims)

    @property
    def selected_candidate(self) -> GenericHMCCandidateResult | None:
        if self.selected_candidate_index is None:
            return None
        for candidate in self.candidate_results:
            if candidate.candidate_index == self.selected_candidate_index:
                return candidate
        return None

    @property
    def passed(self) -> bool:
        return (
            self.selected_candidate is not None
            and self.heldout_candidate is not None
            and self.heldout_candidate.passed_screen
            and not self.vetoes
        )

    def payload(self) -> Mapping[str, Any]:
        selected_candidate = self.selected_candidate
        checkpoint_paths = {
            "selected_candidate": (
                None
                if selected_candidate is None
                else selected_candidate.checkpoint_path
            ),
            "heldout_candidate": (
                None
                if self.heldout_candidate is None
                else self.heldout_candidate.checkpoint_path
            ),
        }
        heldout_confirmation = {
            "status": (
                "passed"
                if self.heldout_candidate is not None
                and self.heldout_candidate.passed_screen
                else "failed_or_not_run"
            ),
            "semantics": (
                "heldout candidate is a promotion veto/repair trigger only; "
                "it is not a posterior convergence or sampler superiority claim"
            ),
            "candidate": (
                None
                if self.heldout_candidate is None
                else self.heldout_candidate.payload()
            ),
        }
        checkpoint_payload = {
            "artifact_type": "bayesfilter_generic_hmc_tuning_checkpoint",
            "adapter_signature": self.adapter_signature,
            "target_dimension": self.target_dimension,
            "mass_artifact_signature": self.mass_artifact_signature,
            "selected_candidate_index": self.selected_candidate_index,
            "selected_step_size": (
                None if selected_candidate is None else selected_candidate.step_size
            ),
            "selected_num_leapfrog_steps": (
                None
                if selected_candidate is None
                else selected_candidate.num_leapfrog_steps
            ),
            "selected_trajectory_length": (
                None
                if selected_candidate is None
                else selected_candidate.trajectory_length
            ),
            "selected_seed": (
                None if selected_candidate is None else selected_candidate.seed
            ),
            "candidate_payload_hash": stable_config_hash(
                tuple(item.payload() for item in self.candidate_results)
            ),
        }
        payload = {
            "artifact_type": "bayesfilter_generic_hmc_tuning_result",
            "policy": self.policy.payload(),
            "config": self.config.payload(),
            "adapter_signature": self.adapter_signature,
            "target_dimension": self.target_dimension,
            "map_provenance": {
                "position_role": self.mass_artifact_payload.get("position_role"),
                "source": self.mass_artifact_payload.get("source"),
                "adapter_signature": self.adapter_signature,
                "semantics": "MAP/center provenance from PrecomputedMassArtifact",
            },
            "mass_provenance": {
                "mass_artifact_signature": self.mass_artifact_signature,
                "covariance_source": self.mass_artifact_payload.get("covariance_source"),
                "matrix_used_for_square_root": self.mass_artifact_payload.get(
                    "matrix_used_for_square_root"
                ),
                "factor_orientation": self.mass_artifact_payload.get("factor_orientation"),
            },
            "mass_artifact_payload": self.mass_artifact_payload,
            "mass_artifact_signature": self.mass_artifact_signature,
            "selected_mass": self.mass_artifact_payload,
            "candidate_results": tuple(item.payload() for item in self.candidate_results),
            "selected_candidate": (
                None if selected_candidate is None else selected_candidate.payload()
            ),
            "selected_step_size": (
                None if selected_candidate is None else selected_candidate.step_size
            ),
            "selected_num_leapfrog_steps": (
                None
                if selected_candidate is None
                else selected_candidate.num_leapfrog_steps
            ),
            "selected_trajectory_length": (
                None
                if selected_candidate is None
                else selected_candidate.trajectory_length
            ),
            "selected_seed": (
                None if selected_candidate is None else selected_candidate.seed
            ),
            "heldout_candidate": (
                None if self.heldout_candidate is None else self.heldout_candidate.payload()
            ),
            "heldout_confirmation": heldout_confirmation,
            "checkpoint_paths": checkpoint_paths,
            "checkpoint_payload": checkpoint_payload,
            "diagnostic_roles": self.diagnostic_roles,
            "vetoes": self.vetoes,
            "passed": self.passed,
            "reports_posterior_convergence": False,
            "reports_sampler_superiority": False,
            "reports_default_readiness": False,
            "nonclaims": self.nonclaims,
        }
        return payload

    @property
    def artifact_hash(self) -> str:
        return stable_config_hash(self.payload())


def run_generic_hmc_tuning_orchestration(
    adapter: Any,
    mass_artifact: PrecomputedMassArtifact,
    config: GenericHMCTuningConfig,
    *,
    candidate_acceptance_rates: Sequence[float] | None = None,
    heldout_acceptance_rate: float | None = None,
    checkpoint_root: str | None = None,
) -> GenericHMCTuningResult:
    """Run a small generic HMC tuning orchestration on supplied diagnostics.

    This first generic layer validates ownership, schema, mass provenance,
    candidate selection, checkpoint-ready payloads, heldout seed discipline, and
    nonclaim semantics.  It intentionally does not replace the lower-level HMC
    diagnostic functions; client-specific execution can fill the candidate
    acceptance rows from actual BayesFilter-owned workers.
    """

    adapter_signature = stable_adapter_signature(adapter)
    position, _covariance, _factor = mass_artifact.validate_for_adapter(adapter)
    target_dimension = int(position.shape[0])
    policy = HMCTuningPolicy.fixed_trajectory_tuning(
        target_accept_prob=0.5 * sum(config.acceptance_band),
        source=config.policy_source,
    )
    require_executable_tuning_policy(policy)

    candidate_grid = [
        (step, leapfrog)
        for step in config.step_size_candidates
        for leapfrog in config.num_leapfrog_step_candidates
    ]
    if candidate_acceptance_rates is not None and len(candidate_acceptance_rates) != len(candidate_grid):
        raise ValueError("candidate_acceptance_rates length must match candidate grid")
    lower, upper = config.acceptance_band
    midpoint = 0.5 * (lower + upper)
    candidates = tuple(
        _build_candidate_result(
            candidate_index=index,
            step_size=step,
            leapfrog_count=leapfrog,
            seed=config.tuning_seed,
            acceptance_rate=(
                None if candidate_acceptance_rates is None else candidate_acceptance_rates[index]
            ),
            acceptance_band=config.acceptance_band,
            checkpoint_root=checkpoint_root,
            stage="tuning",
        )
        for index, (step, leapfrog) in enumerate(candidate_grid)
    )
    selected = _select_generic_candidate(candidates, midpoint=midpoint)
    heldout = None
    vetoes: list[str] = []
    if selected is None:
        vetoes.append("no_candidate_in_closed_acceptance_promotion_band")
    else:
        heldout_acceptance = selected.acceptance_rate if heldout_acceptance_rate is None else heldout_acceptance_rate
        heldout = _build_candidate_result(
            candidate_index=selected.candidate_index,
            step_size=selected.step_size,
            leapfrog_count=selected.num_leapfrog_steps,
            seed=config.heldout_seed,
            acceptance_rate=heldout_acceptance,
            acceptance_band=config.acceptance_band,
            checkpoint_root=checkpoint_root,
            stage="heldout",
        )
        if not heldout.passed_screen:
            vetoes.append("heldout_confirmation_failed")
    mass_payload = mass_artifact.signature_payload()
    mass_signature = stable_config_hash(
        {
            "signature_payload": mass_payload,
            "position": np.asarray(mass_artifact.position, dtype=float).tolist(),
            "covariance": np.asarray(mass_artifact.covariance, dtype=float).tolist(),
            "factor": np.asarray(mass_artifact.factor, dtype=float).tolist(),
        }
    )
    _ = FixedTrajectoryTuningConfig(
        num_leapfrog_step_candidates=config.num_leapfrog_step_candidates,
        acceptance_band=config.acceptance_band,
        seed=config.tuning_seed,
        target_trajectory_length=config.target_trajectory_length,
    )
    if selected is not None:
        production_l, theory_l = production_leapfrog_count(
            selected.step_size,
            max(config.num_leapfrog_step_candidates),
            min(config.num_leapfrog_step_candidates),
            target_traj=config.target_trajectory_length,
        )
    else:
        production_l = None
        theory_l = None
    roles = {
        "acceptance_band": "tuning_promotion_screen_only",
        "finite_samples": "hard_veto",
        "log_accept_ratio_finite": "hard_veto",
        "heldout_confirmation": "promotion_veto_repair_trigger",
        "candidate_runtime": "explanatory_diagnostic",
        "production_leapfrog_count": "explanatory_diagnostic",
        "production_leapfrog_count_value": str(production_l),
        "theory_leapfrog_count_value": str(theory_l),
    }
    return GenericHMCTuningResult(
        policy=policy,
        config=config,
        adapter_signature=adapter_signature,
        target_dimension=target_dimension,
        mass_artifact_payload=mass_payload,
        mass_artifact_signature=mass_signature,
        candidate_results=candidates,
        selected_candidate_index=None if selected is None else selected.candidate_index,
        heldout_candidate=heldout,
        diagnostic_roles=roles,
        vetoes=tuple(vetoes),
    )


def _build_candidate_result(
    *,
    candidate_index: int,
    step_size: float,
    leapfrog_count: int,
    seed: tuple[int, int],
    acceptance_rate: float | None,
    acceptance_band: tuple[float, float],
    checkpoint_root: str | None,
    stage: str,
) -> GenericHMCCandidateResult:
    lower, upper = acceptance_band
    if acceptance_rate is None:
        outcome = "blocked_missing_acceptance_diagnostic"
        vetoes = ("acceptance_rate_missing",)
        role = "hard_veto"
        finite_count = 0
        nonfinite_count = 0
        log_accept_finite = False
    else:
        acceptance = float(acceptance_rate)
        if not np.isfinite(acceptance):
            outcome = "blocked_missing_acceptance_diagnostic"
            vetoes = ("acceptance_rate_nonfinite",)
            role = "hard_veto"
            finite_count = 0
            nonfinite_count = 0
            log_accept_finite = False
        elif acceptance < lower:
            outcome = "rejected_accept_low"
            vetoes = ("acceptance_below_closed_promotion_band",)
            role = "promotion_veto_repair_trigger"
            finite_count = 1
            nonfinite_count = 0
            log_accept_finite = True
        elif acceptance > upper:
            outcome = "rejected_accept_high"
            vetoes = ("acceptance_above_closed_promotion_band",)
            role = "promotion_veto_repair_trigger"
            finite_count = 1
            nonfinite_count = 0
            log_accept_finite = True
        else:
            outcome = "passed_screen"
            vetoes = ()
            role = "tuning_promotion_screen_only"
            finite_count = 1
            nonfinite_count = 0
            log_accept_finite = True
    checkpoint = None
    if checkpoint_root is not None:
        checkpoint = (
            f"{checkpoint_root.rstrip('/')}/{stage}_candidate_{int(candidate_index):04d}.json"
        )
    return GenericHMCCandidateResult(
        candidate_index=candidate_index,
        step_size=step_size,
        num_leapfrog_steps=leapfrog_count,
        trajectory_length=float(step_size) * int(leapfrog_count),
        seed=seed,
        acceptance_rate=acceptance_rate,
        finite_sample_count=finite_count,
        nonfinite_sample_count=nonfinite_count,
        log_accept_ratio_finite=log_accept_finite,
        outcome=outcome,
        diagnostic_role=role,
        vetoes=vetoes,
        checkpoint_path=checkpoint,
    )


def _select_generic_candidate(
    candidates: Sequence[GenericHMCCandidateResult],
    *,
    midpoint: float,
) -> GenericHMCCandidateResult | None:
    viable = [
        CandidateResult(
            candidate_index=candidate.candidate_index,
            step_size=candidate.step_size,
            leapfrog_steps=candidate.num_leapfrog_steps,
            score=(
                abs(float(candidate.acceptance_rate) - float(midpoint))
                if candidate.acceptance_rate is not None
                else float("inf")
            ),
            status="ok" if candidate.passed_screen else "rejected",
            payload=candidate,
        )
        for candidate in candidates
    ]
    try:
        selected = select_first_tie_candidate(viable)
    except ValueError:
        return None
    return selected.payload


@dataclass(frozen=True)
class GenericHMCCandidateEvaluation:
    """One generic candidate evaluation supplied by a BayesFilter worker.

    This public row type is deliberately broader than the toy diagnostic rows:
    client projects may attach target-specific telemetry under ``payload``,
    while BayesFilter still owns candidate identity, acceptance role, and stable
    serialization semantics.
    """

    candidate_index: int
    step_size: float
    num_leapfrog_steps: int
    acceptance_rate: float | None
    diagnostic_roles: Mapping[str, str]
    payload: Mapping[str, Any] | None = None
    status: str = "ok"
    vetoes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        index = int(self.candidate_index)
        if index < 0:
            raise ValueError("candidate_index must be non-negative")
        step = float(self.step_size)
        if not np.isfinite(step) or step <= 0.0:
            raise ValueError("step_size must be positive and finite")
        leapfrogs = int(self.num_leapfrog_steps)
        if leapfrogs <= 0:
            raise ValueError("num_leapfrog_steps must be positive")
        acceptance = None if self.acceptance_rate is None else float(self.acceptance_rate)
        if acceptance is not None and (
            not np.isfinite(acceptance) or acceptance < 0.0 or acceptance > 1.0
        ):
            raise ValueError("acceptance_rate must be in [0, 1]")
        roles = {str(key): str(value) for key, value in self.diagnostic_roles.items()}
        if not roles:
            raise ValueError("diagnostic_roles must be non-empty")
        status = str(self.status)
        if not status:
            raise ValueError("status must be non-empty")
        object.__setattr__(self, "candidate_index", index)
        object.__setattr__(self, "step_size", step)
        object.__setattr__(self, "num_leapfrog_steps", leapfrogs)
        object.__setattr__(self, "acceptance_rate", acceptance)
        object.__setattr__(self, "diagnostic_roles", roles)
        object.__setattr__(self, "payload", {} if self.payload is None else dict(self.payload))
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "vetoes", tuple(str(item) for item in self.vetoes))

    @property
    def trajectory_length(self) -> float:
        return float(self.step_size * self.num_leapfrog_steps)

    def stable_payload(self) -> Mapping[str, Any]:
        return {
            "candidate_index": self.candidate_index,
            "step_size": self.step_size,
            "num_leapfrog_steps": self.num_leapfrog_steps,
            "trajectory_length": self.trajectory_length,
            "acceptance_rate": self.acceptance_rate,
            "diagnostic_roles": self.diagnostic_roles,
            "payload": self.payload,
            "status": self.status,
            "vetoes": self.vetoes,
        }


@dataclass(frozen=True)
class GenericHMCTuningArtifact:
    """Stable exported artifact returned by generic HMC tuning orchestration."""

    policy: HMCTuningPolicy
    adapter_signature: str
    target_dimension: int
    mass_artifact: PrecomputedMassArtifact
    candidate_evaluations: tuple[GenericHMCCandidateEvaluation, ...]
    selected_candidate_index: int | None
    seed: tuple[int, int]
    map_provenance: Mapping[str, Any]
    heldout_confirmation: Mapping[str, Any]
    checkpoint_paths: Mapping[str, str]
    diagnostic_roles: Mapping[str, str]
    vetoes: tuple[str, ...] = ()
    nonclaims: tuple[str, ...] = GENERIC_HMC_TUNING_NONCLAIMS

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
        candidates = tuple(self.candidate_evaluations)
        if not candidates:
            raise ValueError("candidate_evaluations must be non-empty")
        selected = None if self.selected_candidate_index is None else int(self.selected_candidate_index)
        if selected is not None and all(item.candidate_index != selected for item in candidates):
            raise ValueError("selected_candidate_index must refer to a candidate")
        seed = tuple(int(item) for item in self.seed)
        if len(seed) != 2:
            raise ValueError("seed must contain exactly two integers")
        roles = {str(key): str(value) for key, value in self.diagnostic_roles.items()}
        if not roles:
            raise ValueError("diagnostic_roles must be non-empty")
        paths = {str(key): str(value) for key, value in self.checkpoint_paths.items()}
        object.__setattr__(self, "adapter_signature", signature)
        object.__setattr__(self, "target_dimension", dimension)
        object.__setattr__(self, "candidate_evaluations", candidates)
        object.__setattr__(self, "selected_candidate_index", selected)
        object.__setattr__(self, "seed", seed)
        object.__setattr__(self, "map_provenance", dict(self.map_provenance))
        object.__setattr__(self, "heldout_confirmation", dict(self.heldout_confirmation))
        object.__setattr__(self, "checkpoint_paths", paths)
        object.__setattr__(self, "diagnostic_roles", roles)
        object.__setattr__(self, "vetoes", tuple(str(item) for item in self.vetoes))
        object.__setattr__(self, "nonclaims", tuple(str(item) for item in self.nonclaims))

    @property
    def selected_candidate(self) -> GenericHMCCandidateEvaluation | None:
        if self.selected_candidate_index is None:
            return None
        for candidate in self.candidate_evaluations:
            if candidate.candidate_index == self.selected_candidate_index:
                return candidate
        return None

    @property
    def passed(self) -> bool:
        return self.selected_candidate is not None and not self.vetoes

    @property
    def stable_json(self) -> str:
        return json.dumps(self.payload(), sort_keys=True, separators=(",", ":"))

    @property
    def artifact_hash(self) -> str:
        return stable_config_hash(self.payload())

    def payload(self) -> Mapping[str, Any]:
        selected = self.selected_candidate
        mass_payload = self.mass_artifact.signature_payload()
        candidate_payloads = tuple(item.stable_payload() for item in self.candidate_evaluations)
        return {
            "artifact_type": "bayesfilter_generic_hmc_tuning_artifact",
            "policy": self.policy.payload(),
            "adapter_signature": self.adapter_signature,
            "target_dimension": self.target_dimension,
            "selected_mass": mass_payload,
            "mass_provenance": {
                "mass_artifact_signature": stable_config_hash(
                    {
                        "signature_payload": mass_payload,
                        "position": np.asarray(self.mass_artifact.position, dtype=float).tolist(),
                        "covariance": np.asarray(self.mass_artifact.covariance, dtype=float).tolist(),
                        "factor": np.asarray(self.mass_artifact.factor, dtype=float).tolist(),
                    }
                ),
                "covariance_source": self.mass_artifact.covariance_source,
                "source": self.mass_artifact.source,
                "regularization_report": self.mass_artifact.regularization_report,
            },
            "map_provenance": self.map_provenance,
            "candidate_evaluations": candidate_payloads,
            "selected_candidate": None if selected is None else selected.stable_payload(),
            "selected_step_size": None if selected is None else selected.step_size,
            "selected_num_leapfrog_steps": None if selected is None else selected.num_leapfrog_steps,
            "selected_trajectory_length": None if selected is None else selected.trajectory_length,
            "selected_seed": self.seed,
            "heldout_confirmation": self.heldout_confirmation,
            "checkpoint_paths": self.checkpoint_paths,
            "checkpoint_payload": {
                "candidate_evaluation_hash": stable_config_hash(candidate_payloads),
                "selected_candidate_index": self.selected_candidate_index,
                "seed": self.seed,
            },
            "diagnostics": {
                "passed": self.passed,
                "diagnostic_roles": self.diagnostic_roles,
                "vetoes": self.vetoes,
                "reports_posterior_convergence": False,
                "reports_sampler_superiority": False,
                "reports_default_readiness": False,
            },
            "vetoes": self.vetoes,
            "nonclaims": self.nonclaims,
        }


def orchestrate_generic_hmc_tuning(
    *,
    policy: HMCTuningPolicy,
    adapter_signature: str,
    target_dimension: int,
    mass_artifact: PrecomputedMassArtifact,
    candidate_evaluations: Sequence[GenericHMCCandidateEvaluation],
    seed: tuple[int, int],
    map_provenance: Mapping[str, Any],
    heldout_confirmation: Mapping[str, Any],
    checkpoint_paths: Mapping[str, str],
) -> GenericHMCTuningArtifact:
    """Select a generic HMC candidate and return a stable client artifact.

    This orchestration layer intentionally consumes candidate rows supplied by a
    BayesFilter-owned worker/runtime path.  It does not call the private tiny
    Gaussian fixture and does not replace existing diagnostic functions.
    """

    policy = require_executable_tuning_policy(policy)
    if not policy.uses_fixed_trajectory_tuning:
        raise ValueError("generic HMC orchestration currently requires fixed_trajectory_tuning")
    candidates = tuple(candidate_evaluations)
    if not candidates:
        raise ValueError("candidate_evaluations must be non-empty")
    target_accept = (
        0.70 if policy.target_accept_prob is None else float(policy.target_accept_prob)
    )
    worker_rows = tuple(
        CandidateResult(
            candidate_index=candidate.candidate_index,
            step_size=candidate.step_size,
            leapfrog_steps=candidate.num_leapfrog_steps,
            score=(
                abs(float(candidate.acceptance_rate) - target_accept)
                if candidate.acceptance_rate is not None
                else float("inf")
            ),
            status="ok" if candidate.status == "ok" and not candidate.vetoes else "rejected",
            payload=candidate,
        )
        for candidate in candidates
    )
    try:
        selected = select_first_tie_candidate(worker_rows).payload
    except ValueError:
        selected = None
    vetoes = () if selected is not None else ("no_candidate_selected",)
    return GenericHMCTuningArtifact(
        policy=policy,
        adapter_signature=adapter_signature,
        target_dimension=target_dimension,
        mass_artifact=mass_artifact,
        candidate_evaluations=candidates,
        selected_candidate_index=None if selected is None else selected.candidate_index,
        seed=seed,
        map_provenance=map_provenance,
        heldout_confirmation=heldout_confirmation,
        checkpoint_paths=checkpoint_paths,
        diagnostic_roles={
            "candidate_screen": "promotion_veto",
            "mass_artifact_signature": "hard_veto",
            "heldout_confirmation": "promotion_veto_when_required",
            "artifact_hash": "explanatory_diagnostic",
        },
        vetoes=vetoes,
    )
