"""Fixed-mass HMC step-size budget ladder.

This module owns a generic BayesFilter orchestration pattern: for one frozen
mass artifact and one fixed leapfrog count, increase the dual-averaging budget
until a fresh fixed-kernel screen passes or a fail-closed veto fires.  The HMC
work is still delegated to :func:`run_full_chain_tfp_hmc`; conversions to Python
or NumPy happen only after TensorFlow/TFP returns, for artifacting and
classification.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

import numpy as np

from bayesfilter.inference.batched_value_score import LatentAffineBatchValueScoreAdapter
from bayesfilter.inference.hmc import (
    FullChainHMCConfig,
    FullChainHMCRunResult,
    PrecomputedMassArtifact,
    build_reusable_full_chain_tfp_hmc_runner,
    program_signature,
    run_full_chain_tfp_hmc,
    stable_adapter_signature,
)
from bayesfilter.inference.hmc_tuning import HMCTuningPolicy
from bayesfilter.inference.posterior_adapter import (
    ValueScoreCapability,
    value_score_capability,
)
from bayesfilter.runtime import stable_config_hash


BUDGET_LADDER_NONCLAIMS: tuple[str, ...] = (
    "fixed-mass HMC tuning-budget ladder only",
    "acceptance is a tuning-screen diagnostic only",
    "no posterior convergence claim",
    "no sampler superiority claim",
    "no default sampler readiness claim",
    "no empirical validity claim",
    "no GPU or XLA readiness claim",
)


RunFullChainFn = Callable[[Any, Any, FullChainHMCConfig], FullChainHMCRunResult]
InitialStateFactory = Callable[[tuple[int, int], str, int, int, float], Any]
ScreenCallback = Callable[[Mapping[str, Any], Any, Mapping[str, Any]], Any]
ProgressCallback = Callable[[str, Mapping[str, Any]], None]


@dataclass(frozen=True)
class FixedMassHMCTuningBudgetCallbackResult:
    """Role-separated client callback diagnostics for one screen round."""

    hard_vetoes: tuple[str, ...] = ()
    continuation_vetoes: tuple[str, ...] = ()
    promotion_vetoes: tuple[str, ...] = ()
    repair_triggers: tuple[str, ...] = ()
    diagnostics: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "hard_vetoes", _string_tuple(self.hard_vetoes))
        object.__setattr__(
            self,
            "continuation_vetoes",
            _string_tuple(self.continuation_vetoes),
        )
        object.__setattr__(
            self,
            "promotion_vetoes",
            _string_tuple(self.promotion_vetoes),
        )
        object.__setattr__(self, "repair_triggers", _string_tuple(self.repair_triggers))
        if not isinstance(self.diagnostics, Mapping):
            raise ValueError("callback diagnostics must be a mapping")
        object.__setattr__(self, "diagnostics", dict(self.diagnostics))

    @property
    def has_stop_veto(self) -> bool:
        return bool(self.hard_vetoes or self.continuation_vetoes)

    def payload(self) -> Mapping[str, Any]:
        return {
            "hard_vetoes": self.hard_vetoes,
            "continuation_vetoes": self.continuation_vetoes,
            "promotion_vetoes": self.promotion_vetoes,
            "repair_triggers": self.repair_triggers,
            "diagnostics": self.diagnostics,
        }


@dataclass(frozen=True)
class FixedMassHMCTuningBudgetLadderConfig:
    """Configuration for one fixed-mass, fixed-leapfrog budget ladder."""

    budget_schedule: tuple[int, ...]
    initial_step_size: float
    num_leapfrog_steps: int
    target_accept_prob: float = 0.70
    acceptance_band: tuple[float, float] = (0.65, 0.75)
    repair_band: tuple[float, float] = (0.55, 0.85)
    tune_num_results: int = 16
    screen_num_results: int = 32
    screen_num_burnin_steps: int = 8
    tune_seed_base: tuple[int, int] = (20260619, 100)
    screen_seed_base: tuple[int, int] = (20260619, 200)
    chain_execution_mode: str = "tf_function"
    use_xla: bool = False
    target_scope: str | None = None
    tuning_trace_policy: str = "standard"
    screen_trace_policy: str = "standard"
    target_status_trace_policy: str = "none"
    step_stability_rtol: float | None = None
    step_stability_is_hard_veto: bool = False
    source: str = "bayesfilter.inference.hmc_budget_ladder"

    def __post_init__(self) -> None:
        budgets = tuple(int(item) for item in self.budget_schedule)
        if not budgets:
            raise ValueError("budget_schedule must be non-empty")
        if any(item <= 0 for item in budgets):
            raise ValueError("budget_schedule values must be positive")
        object.__setattr__(self, "budget_schedule", budgets)
        initial_step = float(self.initial_step_size)
        if not np.isfinite(initial_step) or initial_step <= 0.0:
            raise ValueError("initial_step_size must be positive and finite")
        object.__setattr__(self, "initial_step_size", initial_step)
        leapfrog = int(self.num_leapfrog_steps)
        if leapfrog <= 0:
            raise ValueError("num_leapfrog_steps must be positive")
        object.__setattr__(self, "num_leapfrog_steps", leapfrog)
        target_accept = float(self.target_accept_prob)
        if not np.isfinite(target_accept) or not 0.0 < target_accept < 1.0:
            raise ValueError("target_accept_prob must be finite and in (0, 1)")
        object.__setattr__(self, "target_accept_prob", target_accept)
        acceptance_band = _validate_band(self.acceptance_band, name="acceptance_band")
        repair_band = _validate_band(self.repair_band, name="repair_band")
        if repair_band[0] > acceptance_band[0] or repair_band[1] < acceptance_band[1]:
            raise ValueError("repair_band must contain acceptance_band")
        object.__setattr__(self, "acceptance_band", acceptance_band)
        object.__setattr__(self, "repair_band", repair_band)
        for name in ("tune_num_results", "screen_num_results", "screen_num_burnin_steps"):
            value = int(getattr(self, name))
            if value <= 0:
                raise ValueError(f"{name} must be positive")
            object.__setattr__(self, name, value)
        object.__setattr__(self, "tune_seed_base", _validate_seed(self.tune_seed_base))
        screen_seed = _validate_seed(self.screen_seed_base)
        if screen_seed == self.tune_seed_base:
            raise ValueError("screen_seed_base must differ from tune_seed_base")
        object.__setattr__(self, "screen_seed_base", screen_seed)
        chain_execution_mode = str(self.chain_execution_mode)
        if chain_execution_mode not in {"tf_function", "eager"}:
            raise ValueError("chain_execution_mode must be 'tf_function' or 'eager'")
        object.__setattr__(self, "chain_execution_mode", chain_execution_mode)
        object.__setattr__(self, "use_xla", bool(self.use_xla))
        tuning_trace_policy = str(self.tuning_trace_policy)
        if tuning_trace_policy != "standard":
            raise ValueError("tuning_trace_policy must be 'standard'")
        object.__setattr__(self, "tuning_trace_policy", tuning_trace_policy)
        screen_trace_policy = str(self.screen_trace_policy)
        if screen_trace_policy != "standard":
            raise ValueError(
                "screen_trace_policy must be 'standard' so acceptance/log-accept "
                "diagnostics are available"
            )
        object.__setattr__(self, "screen_trace_policy", screen_trace_policy)
        target_status_policy = str(self.target_status_trace_policy)
        if target_status_policy not in {"none", "per_chain_step"}:
            raise ValueError(
                "target_status_trace_policy must be 'none' or 'per_chain_step'"
            )
        object.__setattr__(self, "target_status_trace_policy", target_status_policy)
        if self.target_scope is not None:
            object.__setattr__(self, "target_scope", str(self.target_scope))
        if self.step_stability_rtol is not None:
            rtol = float(self.step_stability_rtol)
            if not np.isfinite(rtol) or rtol < 0.0:
                raise ValueError("step_stability_rtol must be nonnegative and finite")
            object.__setattr__(self, "step_stability_rtol", rtol)
        object.__setattr__(
            self,
            "step_stability_is_hard_veto",
            bool(self.step_stability_is_hard_veto),
        )
        source = str(self.source)
        if not source:
            raise ValueError("source must be non-empty")
        object.__setattr__(self, "source", source)

    def payload(self) -> Mapping[str, Any]:
        return {
            "budget_schedule": self.budget_schedule,
            "initial_step_size": self.initial_step_size,
            "num_leapfrog_steps": self.num_leapfrog_steps,
            "target_accept_prob": self.target_accept_prob,
            "acceptance_band": self.acceptance_band,
            "repair_band": self.repair_band,
            "tune_num_results": self.tune_num_results,
            "screen_num_results": self.screen_num_results,
            "screen_num_burnin_steps": self.screen_num_burnin_steps,
            "tune_seed_base": self.tune_seed_base,
            "screen_seed_base": self.screen_seed_base,
            "chain_execution_mode": self.chain_execution_mode,
            "use_xla": self.use_xla,
            "target_scope": self.target_scope,
            "tuning_trace_policy": self.tuning_trace_policy,
            "screen_trace_policy": self.screen_trace_policy,
            "target_status_trace_policy": self.target_status_trace_policy,
            "step_stability_rtol": self.step_stability_rtol,
            "step_stability_is_hard_veto": self.step_stability_is_hard_veto,
            "source": self.source,
        }


@dataclass(frozen=True)
class FixedMassHMCTuningBudgetRound:
    """One tune/screen round in the budget ladder."""

    round_index: int
    budget: int
    tune_seed: tuple[int, int]
    screen_seed: tuple[int, int]
    initial_step_size: float
    tuned_step_size: float | None
    classification: str
    diagnostic_role: str
    tune_config_payload: Mapping[str, Any] | None
    screen_config_payload: Mapping[str, Any] | None
    tune_diagnostics: Mapping[str, Any]
    screen_diagnostics: Mapping[str, Any]
    callback_result: FixedMassHMCTuningBudgetCallbackResult
    hard_vetoes: tuple[str, ...] = ()
    continuation_vetoes: tuple[str, ...] = ()
    promotion_vetoes: tuple[str, ...] = ()
    repair_triggers: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "round_index", int(self.round_index))
        object.__setattr__(self, "budget", int(self.budget))
        object.__setattr__(self, "tune_seed", _validate_seed(self.tune_seed))
        object.__setattr__(self, "screen_seed", _validate_seed(self.screen_seed))
        initial_step = float(self.initial_step_size)
        if not np.isfinite(initial_step) or initial_step <= 0.0:
            raise ValueError("round initial_step_size must be positive and finite")
        object.__setattr__(self, "initial_step_size", initial_step)
        tuned_step = (
            None if self.tuned_step_size is None else float(self.tuned_step_size)
        )
        if tuned_step is not None and (
            not np.isfinite(tuned_step) or tuned_step <= 0.0
        ):
            raise ValueError("round tuned_step_size must be positive and finite")
        object.__setattr__(self, "tuned_step_size", tuned_step)
        object.__setattr__(self, "classification", str(self.classification))
        object.__setattr__(self, "diagnostic_role", str(self.diagnostic_role))
        object.__setattr__(
            self,
            "tune_config_payload",
            None if self.tune_config_payload is None else dict(self.tune_config_payload),
        )
        object.__setattr__(
            self,
            "screen_config_payload",
            None if self.screen_config_payload is None else dict(self.screen_config_payload),
        )
        object.__setattr__(self, "tune_diagnostics", dict(self.tune_diagnostics))
        object.__setattr__(self, "screen_diagnostics", dict(self.screen_diagnostics))
        object.__setattr__(self, "hard_vetoes", _string_tuple(self.hard_vetoes))
        object.__setattr__(
            self,
            "continuation_vetoes",
            _string_tuple(self.continuation_vetoes),
        )
        object.__setattr__(
            self,
            "promotion_vetoes",
            _string_tuple(self.promotion_vetoes),
        )
        object.__setattr__(self, "repair_triggers", _string_tuple(self.repair_triggers))

    @property
    def passed(self) -> bool:
        return self.classification == "passed"

    @property
    def repair_compatible(self) -> bool:
        return self.classification in {"acceptance_repair", "promotion_veto_repair"}

    def payload(self) -> Mapping[str, Any]:
        return {
            "round_index": self.round_index,
            "budget": self.budget,
            "tune_seed": self.tune_seed,
            "screen_seed": self.screen_seed,
            "initial_step_size": self.initial_step_size,
            "tuned_step_size": self.tuned_step_size,
            "classification": self.classification,
            "diagnostic_role": self.diagnostic_role,
            "tune_config_payload": self.tune_config_payload,
            "screen_config_payload": self.screen_config_payload,
            "tune_diagnostics": self.tune_diagnostics,
            "screen_diagnostics": self.screen_diagnostics,
            "callback_result": self.callback_result.payload(),
            "hard_vetoes": self.hard_vetoes,
            "continuation_vetoes": self.continuation_vetoes,
            "promotion_vetoes": self.promotion_vetoes,
            "repair_triggers": self.repair_triggers,
        }


@dataclass(frozen=True)
class FixedMassHMCTuningBudgetLadderResult:
    """Complete fixed-mass HMC tuning-budget ladder artifact."""

    config: FixedMassHMCTuningBudgetLadderConfig
    adapter_signature: str
    hmc_adapter_signature: str
    mass_artifact_payload: Mapping[str, Any]
    mass_artifact_signature: str
    target_dimension: int
    rounds: tuple[FixedMassHMCTuningBudgetRound, ...]
    selected_round_index: int | None
    final_status: str
    diagnostic_roles: Mapping[str, str]
    runner_route_summary: Mapping[str, Any] = field(default_factory=dict)
    nonclaims: tuple[str, ...] = BUDGET_LADDER_NONCLAIMS

    def __post_init__(self) -> None:
        signature = str(self.adapter_signature)
        if not signature:
            raise ValueError("adapter_signature must be non-empty")
        object.__setattr__(self, "adapter_signature", signature)
        hmc_signature = str(self.hmc_adapter_signature)
        if not hmc_signature:
            raise ValueError("hmc_adapter_signature must be non-empty")
        object.__setattr__(self, "hmc_adapter_signature", hmc_signature)
        mass_signature = str(self.mass_artifact_signature)
        if not mass_signature:
            raise ValueError("mass_artifact_signature must be non-empty")
        object.__setattr__(self, "mass_artifact_signature", mass_signature)
        object.__setattr__(self, "target_dimension", int(self.target_dimension))
        rounds = tuple(self.rounds)
        if not rounds:
            raise ValueError("budget ladder result requires at least one round")
        object.__setattr__(self, "rounds", rounds)
        selected = (
            None if self.selected_round_index is None else int(self.selected_round_index)
        )
        if selected is not None and selected not in range(len(rounds)):
            raise ValueError("selected_round_index must refer to a round")
        if selected is not None and not rounds[selected].passed:
            raise ValueError("selected round must have passed")
        object.__setattr__(self, "selected_round_index", selected)
        object.__setattr__(self, "final_status", str(self.final_status))
        object.__setattr__(self, "mass_artifact_payload", dict(self.mass_artifact_payload))
        object.__setattr__(self, "diagnostic_roles", dict(self.diagnostic_roles))
        object.__setattr__(self, "runner_route_summary", dict(self.runner_route_summary))
        nonclaims = tuple(str(item) for item in self.nonclaims)
        if not nonclaims:
            raise ValueError("nonclaims must be non-empty")
        object.__setattr__(self, "nonclaims", nonclaims)

    @property
    def passed(self) -> bool:
        return self.selected_round_index is not None

    @property
    def selected_round(self) -> FixedMassHMCTuningBudgetRound | None:
        if self.selected_round_index is None:
            return None
        return self.rounds[self.selected_round_index]

    @property
    def selected_config_hash(self) -> str | None:
        payload = self.selected_config_payload
        return None if payload is None else stable_config_hash(payload)

    @property
    def selected_config_payload(self) -> Mapping[str, Any] | None:
        selected = self.selected_round
        if selected is None or selected.tuned_step_size is None:
            return None
        return {
            "runtime": "bayesfilter.inference.run_fixed_mass_hmc_tuning_budget_ladder",
            "step_size": selected.tuned_step_size,
            "num_leapfrog_steps": self.config.num_leapfrog_steps,
            "selected_budget": selected.budget,
            "target_accept_prob": self.config.target_accept_prob,
            "acceptance_band": self.config.acceptance_band,
            "repair_band": self.config.repair_band,
            "adapter_signature": self.adapter_signature,
            "hmc_adapter_signature": self.hmc_adapter_signature,
            "target_scope": self._selected_target_scope(),
            "mass_artifact_signature": self.mass_artifact_signature,
            "target_status_trace_policy": self.config.target_status_trace_policy,
            "tune_seed": selected.tune_seed,
            "screen_seed": selected.screen_seed,
            "tune_config_payload": selected.tune_config_payload,
            "screen_config_payload": selected.screen_config_payload,
            "nonclaims": self.nonclaims,
        }

    @property
    def last_finite_tuned_round(self) -> FixedMassHMCTuningBudgetRound | None:
        for round_result in reversed(self.rounds):
            if round_result.tuned_step_size is not None:
                return round_result
        return None

    @property
    def last_repair_compatible_round(self) -> FixedMassHMCTuningBudgetRound | None:
        for round_result in reversed(self.rounds):
            if round_result.repair_compatible and round_result.tuned_step_size is not None:
                return round_result
        return None

    @property
    def repair_config_payload(self) -> Mapping[str, Any] | None:
        if self.passed:
            return None
        repair_round = self.last_repair_compatible_round
        if repair_round is None or repair_round.tuned_step_size is None:
            return None
        repair_step = _next_initial_step_after_screen_repair(
            self.config,
            tuned_step=repair_round.tuned_step_size,
            screen_diagnostics=repair_round.screen_diagnostics,
            classification=repair_round.classification,
        )
        return {
            "runtime": "bayesfilter.inference.run_fixed_mass_hmc_tuning_budget_ladder",
            "handoff_role": "private_repair_step_only",
            "step_size": repair_step,
            "num_leapfrog_steps": self.config.num_leapfrog_steps,
            "repair_round_index": repair_round.round_index,
            "repair_budget": repair_round.budget,
            "repair_classification": repair_round.classification,
            "repair_source": "screen_acceptance_directional_repair",
            "target_accept_prob": self.config.target_accept_prob,
            "acceptance_band": self.config.acceptance_band,
            "repair_band": self.config.repair_band,
            "adapter_signature": self.adapter_signature,
            "hmc_adapter_signature": self.hmc_adapter_signature,
            "target_scope": self._round_target_scope(repair_round),
            "mass_artifact_signature": self.mass_artifact_signature,
            "target_status_trace_policy": self.config.target_status_trace_policy,
            "tune_seed": repair_round.tune_seed,
            "screen_seed": repair_round.screen_seed,
            "nonclaims": (
                *self.nonclaims,
                "repair step is private retry state, not a selected kernel",
            ),
        }

    @property
    def repair_config_hash(self) -> str | None:
        payload = self.repair_config_payload
        return None if payload is None else stable_config_hash(payload)

    @property
    def artifact_hash(self) -> str:
        return stable_config_hash(self.payload())

    def payload(self) -> Mapping[str, Any]:
        selected_payload = self.selected_config_payload
        repair_payload = self.repair_config_payload
        return {
            "schema": "bayesfilter.fixed_mass_hmc_tuning_budget_ladder.v1",
            "config": self.config.payload(),
            "adapter_signature": self.adapter_signature,
            "hmc_adapter_signature": self.hmc_adapter_signature,
            "target_dimension": self.target_dimension,
            "mass_artifact_payload": self.mass_artifact_payload,
            "mass_artifact_signature": self.mass_artifact_signature,
            "rounds": tuple(round_result.payload() for round_result in self.rounds),
            "selected_round_index": self.selected_round_index,
            "selected_config_payload": selected_payload,
            "selected_config_hash": None
            if selected_payload is None
            else stable_config_hash(selected_payload),
            "repair_config_hash": None
            if repair_payload is None
            else stable_config_hash(repair_payload),
            "repair_config_available": repair_payload is not None,
            "repair_config_payload_exposed": False,
            "final_status": self.final_status,
            "diagnostic_roles": self.diagnostic_roles,
            "runner_route_summary": self.runner_route_summary,
            "passed": self.passed,
            "reports_posterior_convergence": False,
            "nonclaims": self.nonclaims,
            "artifact_hash_components": {
                "hash_function": "bayesfilter.runtime.stable_config_hash",
                "json_normalization": "sort_keys_compact_json",
            },
        }

    def _selected_target_scope(self) -> str | None:
        selected = self.selected_round
        if selected is None or selected.screen_config_payload is None:
            return self.config.target_scope
        return self._round_target_scope(selected)

    def _round_target_scope(
        self,
        round_result: FixedMassHMCTuningBudgetRound,
    ) -> str | None:
        if round_result.screen_config_payload is None:
            return self.config.target_scope
        target_scope = round_result.screen_config_payload.get("target_scope")
        return None if target_scope is None else str(target_scope)


def run_fixed_mass_hmc_tuning_budget_ladder(
    *,
    adapter: Any,
    mass_artifact: PrecomputedMassArtifact,
    initial_state_factory: InitialStateFactory,
    config: FixedMassHMCTuningBudgetLadderConfig,
    screen_callback: ScreenCallback | None = None,
    progress_callback: ProgressCallback | None = None,
    run_full_chain: RunFullChainFn = run_full_chain_tfp_hmc,
) -> FixedMassHMCTuningBudgetLadderResult:
    """Run a finite fixed-mass HMC tuning-budget ladder.

    The caller supplies the position-coordinate model target and a frozen mass
    artifact for that target.  BayesFilter builds the latent fixed-mass target
    used by TFP HMC, so the recorded mass artifact is operational geometry
    rather than only provenance.  Initial states returned by
    ``initial_state_factory`` are latent coordinates.
    """

    if not isinstance(config, FixedMassHMCTuningBudgetLadderConfig):
        raise TypeError("config must be FixedMassHMCTuningBudgetLadderConfig")
    if not isinstance(mass_artifact, PrecomputedMassArtifact):
        raise TypeError("mass_artifact must be PrecomputedMassArtifact")
    adapter_signature = stable_adapter_signature(adapter)
    _validate_mass_artifact_for_ladder(mass_artifact, adapter)
    mass_payload = mass_artifact.to_payload(include_arrays=True)
    mass_signature = _mass_artifact_signature(mass_artifact)
    target_scope = _resolve_target_scope(adapter, config)
    hmc_adapter = _build_fixed_mass_hmc_adapter(
        adapter=adapter,
        mass_artifact=mass_artifact,
        mass_signature=mass_signature,
        target_scope=target_scope,
    )
    hmc_adapter_signature = stable_adapter_signature(hmc_adapter)
    target_dimension = int(getattr(hmc_adapter, "parameter_dim", mass_artifact.dimension))
    rounds: list[FixedMassHMCTuningBudgetRound] = []
    current_step = float(config.initial_step_size)
    selected_index: int | None = None
    final_status = "budget_exhausted"
    use_reusable_route = (
        run_full_chain is run_full_chain_tfp_hmc
        and config.chain_execution_mode == "tf_function"
    )
    runner_cache: dict[str, Any] = {}
    runner_contract_payloads: dict[str, Mapping[str, Any]] = {}
    runner_route_events: list[Mapping[str, Any]] = []

    for round_index, budget in enumerate(config.budget_schedule):
        tune_seed = _round_seed(config.tune_seed_base, round_index)
        screen_seed = _round_seed(config.screen_seed_base, round_index)
        tune_config = _tune_config(
            config,
            budget=budget,
            seed=tune_seed,
            step=current_step,
            target_scope=target_scope,
        )
        tune_state = initial_state_factory(
            tune_seed,
            "tune",
            round_index,
            budget,
            current_step,
        )
        tune_result = None
        tune_error = None
        try:
            _emit_budget_ladder_boundary_progress(
                progress_callback,
                stage="fixed_mass_ladder_tune_call_start",
                role="tune",
                round_index=round_index,
                budget=budget,
                config=tune_config,
                route_category="reusable_runner" if use_reusable_route else "injected_runner",
                started=True,
                elapsed_s=0.0,
                started_perf_counter_s=time.perf_counter(),
            )
            tune_start = time.perf_counter()
            tune_result = _run_full_chain_with_optional_reusable_route(
                run_full_chain=run_full_chain,
                runner_cache=runner_cache,
                runner_contract_payloads=runner_contract_payloads,
                route_events=runner_route_events,
                adapter=hmc_adapter,
                initial_state=tune_state,
                config=tune_config,
                target_dimension=target_dimension,
                mass_signature=mass_signature,
                role="tune",
                round_index=round_index,
                budget=budget,
            )
            _emit_budget_ladder_boundary_progress(
                progress_callback,
                stage="fixed_mass_ladder_tune_call_complete",
                role="tune",
                round_index=round_index,
                budget=budget,
                config=tune_config,
                route_category="reusable_runner" if use_reusable_route else "injected_runner",
                completed=True,
                elapsed_s=time.perf_counter() - tune_start,
                runner_event=runner_route_events[-1] if runner_route_events else None,
            )
            tune_diagnostics = dict(_diagnostics_payload(tune_result))
        except Exception as exc:  # noqa: BLE001 - return a fail-closed artifact.
            tune_error = exc
            _emit_budget_ladder_boundary_progress(
                progress_callback,
                stage="fixed_mass_ladder_tune_call_error",
                role="tune",
                round_index=round_index,
                budget=budget,
                config=tune_config,
                route_category="reusable_runner" if use_reusable_route else "injected_runner",
                completed=True,
                error_type=type(exc).__name__,
            )
            tune_diagnostics = dict(_error_diagnostics(exc))
        tuned_step = _positive_finite_or_none(tune_diagnostics.get("final_step_size"))
        tune_diagnostics["step_stability"] = _step_stability_payload(
            previous_step=current_step,
            tuned_step=tuned_step,
            rtol=config.step_stability_rtol,
        )
        tune_vetoes = _tune_hard_vetoes(
            config,
            tune_diagnostics,
            budget=budget,
            tuned_step=tuned_step,
            tune_error=tune_error,
        )
        if tune_vetoes:
            round_result = FixedMassHMCTuningBudgetRound(
                round_index=round_index,
                budget=budget,
                tune_seed=tune_seed,
                screen_seed=screen_seed,
                initial_step_size=current_step,
                tuned_step_size=tuned_step,
                classification="hard_veto",
                diagnostic_role="hard_veto",
                tune_config_payload=tune_config.signature_payload(),
                screen_config_payload=None,
                tune_diagnostics=tune_diagnostics,
                screen_diagnostics={},
                callback_result=FixedMassHMCTuningBudgetCallbackResult(),
                hard_vetoes=tuple(tune_vetoes),
            )
            rounds.append(round_result)
            final_status = "hard_veto"
            break

        screen_config = _screen_config(
            config,
            seed=screen_seed,
            step=float(tuned_step),
            target_scope=target_scope,
        )
        screen_state = initial_state_factory(
            screen_seed,
            "screen",
            round_index,
            budget,
            float(tuned_step),
        )
        screen_result = None
        screen_error = None
        try:
            _emit_budget_ladder_boundary_progress(
                progress_callback,
                stage="fixed_mass_ladder_screen_call_start",
                role="screen",
                round_index=round_index,
                budget=budget,
                config=screen_config,
                route_category="reusable_runner" if use_reusable_route else "injected_runner",
                started=True,
                elapsed_s=0.0,
                started_perf_counter_s=time.perf_counter(),
            )
            screen_start = time.perf_counter()
            screen_result = _run_full_chain_with_optional_reusable_route(
                run_full_chain=run_full_chain,
                runner_cache=runner_cache,
                runner_contract_payloads=runner_contract_payloads,
                route_events=runner_route_events,
                adapter=hmc_adapter,
                initial_state=screen_state,
                config=screen_config,
                target_dimension=target_dimension,
                mass_signature=mass_signature,
                role="screen",
                round_index=round_index,
                budget=budget,
            )
            _emit_budget_ladder_boundary_progress(
                progress_callback,
                stage="fixed_mass_ladder_screen_call_complete",
                role="screen",
                round_index=round_index,
                budget=budget,
                config=screen_config,
                route_category="reusable_runner" if use_reusable_route else "injected_runner",
                completed=True,
                elapsed_s=time.perf_counter() - screen_start,
                runner_event=runner_route_events[-1] if runner_route_events else None,
            )
            screen_diagnostics = _diagnostics_payload(screen_result)
        except Exception as exc:  # noqa: BLE001 - return a fail-closed artifact.
            screen_error = exc
            _emit_budget_ladder_boundary_progress(
                progress_callback,
                stage="fixed_mass_ladder_screen_call_error",
                role="screen",
                round_index=round_index,
                budget=budget,
                config=screen_config,
                route_category="reusable_runner" if use_reusable_route else "injected_runner",
                completed=True,
                error_type=type(exc).__name__,
            )
            screen_diagnostics = _error_diagnostics(exc)
        round_payload = {
            "round_index": round_index,
            "budget": budget,
            "tune_seed": tune_seed,
            "screen_seed": screen_seed,
            "initial_step_size": current_step,
            "tuned_step_size": tuned_step,
            "tune_diagnostics": tune_diagnostics,
            "screen_diagnostics": screen_diagnostics,
            "config": config.payload(),
            "mass_artifact_signature": mass_signature,
            "adapter_signature": adapter_signature,
            "hmc_adapter_signature": hmc_adapter_signature,
            "sample_space": "position",
            "hmc_sample_space": "latent_fixed_mass",
        }
        callback_samples = None
        if screen_result is not None:
            callback_samples = hmc_adapter.latent_to_position(screen_result.samples)
        callback_result = _call_screen_callback(
            screen_callback,
            round_payload=round_payload,
            samples=callback_samples,
            diagnostics=screen_diagnostics,
        )
        (
            classification,
            diagnostic_role,
            hard_vetoes,
            continuation_vetoes,
            promotion_vetoes,
            repair_triggers,
        ) = (
            _classify_screen_round(
                config,
                screen_diagnostics=screen_diagnostics,
                screen_error=screen_error,
                callback_result=callback_result,
            )
        )
        round_result = FixedMassHMCTuningBudgetRound(
            round_index=round_index,
            budget=budget,
            tune_seed=tune_seed,
            screen_seed=screen_seed,
            initial_step_size=current_step,
            tuned_step_size=float(tuned_step),
            classification=classification,
            diagnostic_role=diagnostic_role,
            tune_config_payload=tune_config.signature_payload(),
            screen_config_payload=screen_config.signature_payload(),
            tune_diagnostics=tune_diagnostics,
            screen_diagnostics=screen_diagnostics,
            callback_result=callback_result,
            hard_vetoes=hard_vetoes,
            continuation_vetoes=continuation_vetoes,
            promotion_vetoes=promotion_vetoes,
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
        if classification == "continuation_veto":
            final_status = "continuation_veto"
            break
        current_step = _next_initial_step_after_screen_repair(
            config,
            tuned_step=float(tuned_step),
            screen_diagnostics=screen_diagnostics,
            classification=classification,
        )
    else:
        final_status = "budget_exhausted"

    return FixedMassHMCTuningBudgetLadderResult(
        config=config,
        adapter_signature=adapter_signature,
        hmc_adapter_signature=hmc_adapter_signature,
        mass_artifact_payload=mass_payload,
        mass_artifact_signature=mass_signature,
        target_dimension=target_dimension,
        rounds=tuple(rounds),
        selected_round_index=selected_index,
        final_status=final_status,
        diagnostic_roles={
            "acceptance_band": "tuning_screen_promotion_only",
            "repair_band": "acceptance_repair_trigger",
            "finite_samples": "hard_veto",
            "log_accept_ratio_finite": "hard_veto",
            "target_status_telemetry": "hard_veto_when_enabled",
            "step_stability": "explanatory_or_hard_veto_when_configured",
            "callback_hard_vetoes": "hard_veto",
            "callback_continuation_vetoes": "continuation_veto",
            "callback_promotion_vetoes": "promotion_veto_repair_trigger",
            "callback_repair_triggers": "promotion_veto_repair_trigger",
            "runtime": "explanatory_diagnostic",
        },
        runner_route_summary=_runner_route_summary(
            active_route=(
                "fixed_mass_scoped_reusable_runner"
                if use_reusable_route
                else "single_use_or_injected_runner"
            ),
            events=tuple(runner_route_events),
            contract_payloads=runner_contract_payloads,
        ),
    )


def _validate_mass_artifact_for_ladder(
    mass_artifact: PrecomputedMassArtifact,
    adapter: Any,
) -> None:
    mass_artifact.validate_for_adapter(adapter)


class _FixedMassLatentValueScoreAdapter(LatentAffineBatchValueScoreAdapter):
    """Latent fixed-mass target with a mass-bound stable adapter signature."""

    def __init__(
        self,
        *,
        base_adapter: Any,
        transform: Any,
        target_scope: str,
        adapter_signature: str,
    ) -> None:
        super().__init__(
            base_adapter=base_adapter,
            transform=transform,
            target_scope=target_scope,
            runtime_backend=(
                "bayesfilter.inference.hmc_budget_ladder."
                "_FixedMassLatentValueScoreAdapter"
            ),
            nonclaims=BUDGET_LADDER_NONCLAIMS,
        )
        self._adapter_signature = str(adapter_signature)
        if not self._adapter_signature:
            raise ValueError("fixed-mass latent adapter signature must be non-empty")

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
            "fixed-mass latent wrapper cannot promote fallback base authority",
            "fixed-mass latent wrapper preserves XLA authority only from accepted base authority",
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


def _resolve_target_scope(
    adapter: Any,
    config: FixedMassHMCTuningBudgetLadderConfig,
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
            "fixed-mass HMC budget ladder requires config.target_scope or an "
            "adapter value_score_capability target_scope"
        )
    return str(capability_scope)


def _build_fixed_mass_hmc_adapter(
    *,
    adapter: Any,
    mass_artifact: PrecomputedMassArtifact,
    mass_signature: str,
    target_scope: str,
) -> _FixedMassLatentValueScoreAdapter:
    transform = mass_artifact.build_latent_transform()
    latent_signature = program_signature(
        {
            "runtime": (
                "bayesfilter.inference.hmc_budget_ladder."
                "_FixedMassLatentValueScoreAdapter"
            ),
            "position_adapter_signature": stable_adapter_signature(adapter),
            "mass_artifact_signature": mass_signature,
            "target_scope": target_scope,
            "transform": transform.signature_payload(),
        }
    )
    return _FixedMassLatentValueScoreAdapter(
        base_adapter=adapter,
        transform=transform,
        target_scope=target_scope,
        adapter_signature=latent_signature,
    )


def _tune_config(
    config: FixedMassHMCTuningBudgetLadderConfig,
    *,
    budget: int,
    seed: tuple[int, int],
    step: float,
    target_scope: str,
) -> FullChainHMCConfig:
    policy = HMCTuningPolicy.fixed_mass_dual_averaging(
        num_adaptation_steps=int(budget),
        target_accept_prob=config.target_accept_prob,
        source=config.source,
    )
    return FullChainHMCConfig(
        num_results=config.tune_num_results,
        num_burnin_steps=int(budget),
        step_size=float(step),
        num_leapfrog_steps=config.num_leapfrog_steps,
        seed=seed,
        use_xla=config.use_xla,
        trace_policy=config.tuning_trace_policy,
        target_status_trace_policy=config.target_status_trace_policy,
        tuning_policy=policy,
        target_scope=target_scope,
        chain_execution_mode=config.chain_execution_mode,
    )


def _screen_config(
    config: FixedMassHMCTuningBudgetLadderConfig,
    *,
    seed: tuple[int, int],
    step: float,
    target_scope: str,
) -> FullChainHMCConfig:
    return FullChainHMCConfig(
        num_results=config.screen_num_results,
        num_burnin_steps=config.screen_num_burnin_steps,
        step_size=float(step),
        num_leapfrog_steps=config.num_leapfrog_steps,
        seed=seed,
        use_xla=config.use_xla,
        trace_policy=config.screen_trace_policy,
        target_status_trace_policy=config.target_status_trace_policy,
        target_scope=target_scope,
        chain_execution_mode=config.chain_execution_mode,
    )


def _diagnostics_payload(run_result: FullChainHMCRunResult) -> Mapping[str, Any]:
    diagnostics = dict(run_result.diagnostics)
    trace = dict(run_result.trace)
    payload = {
        "acceptance_rate": _scalar_or_none(diagnostics.get("acceptance_rate")),
        "finite_sample_count": _int_or_none(diagnostics.get("finite_sample_count")),
        "nonfinite_sample_count": _int_or_none(diagnostics.get("nonfinite_sample_count")),
        "final_step_size": _scalar_or_none(diagnostics.get("final_step_size")),
        "final_step_size_finite": _bool_or_none(
            diagnostics.get("final_step_size_finite")
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
        "raw_diagnostics": _json_ready(diagnostics),
        "runtime_metadata": _json_ready(run_result.metadata),
        "trace_summary": {
            "trace_keys": tuple(sorted(trace.keys())),
            "trace_unavailability": run_result.metadata.get("trace_unavailability"),
        },
    }
    if "log_accept_ratio" in trace:
        log_accept = np.asarray(_tensor_to_numpy(trace["log_accept_ratio"]), dtype=float)
        finite = np.isfinite(log_accept)
        payload["log_accept_ratio_finite"] = bool(np.all(finite))
        payload["max_abs_log_accept_ratio"] = (
            None if not np.any(finite) else float(np.max(np.abs(log_accept[finite])))
        )
    if "target_log_prob" in trace:
        target_log_prob = np.asarray(
            _tensor_to_numpy(trace["target_log_prob"]),
            dtype=float,
        )
        payload["target_log_prob_finite"] = bool(np.all(np.isfinite(target_log_prob)))
    samples = np.asarray(_tensor_to_numpy(run_result.samples), dtype=float)
    finite_by_sample = np.all(np.isfinite(samples), axis=-1)
    payload["samples_all_finite"] = bool(np.all(finite_by_sample))
    return payload


def _run_full_chain_with_optional_reusable_route(
    *,
    run_full_chain: RunFullChainFn,
    runner_cache: dict[str, Any],
    runner_contract_payloads: dict[str, Mapping[str, Any]],
    route_events: list[Mapping[str, Any]],
    adapter: Any,
    initial_state: Any,
    config: FullChainHMCConfig,
    target_dimension: int,
    mass_signature: str,
    role: str,
    round_index: int,
    budget: int,
) -> FullChainHMCRunResult:
    """Run HMC through a scoped reusable runner when the static contract matches.

    ``ReusableFullChainHMCRunner`` fixes TFP graph-shaping fields and accepts
    state, seed, and step size as runtime tensor arguments.  The selected HMC
    contract still comes from the supplied ``FullChainHMCConfig``; this wrapper
    only changes whether BayesFilter reuses an already-built callable.
    """

    if run_full_chain is not run_full_chain_tfp_hmc or config.chain_execution_mode != "tf_function":
        route_events.append(
            {
                "round_index": int(round_index),
                "budget": int(budget),
                "role": str(role),
                "route": "single_use_or_injected_runner",
                "static_contract_hash": None,
                "call_config_hash": stable_config_hash(config.signature_payload()),
                "runner_reused": False,
                "used_single_use_runner": run_full_chain is run_full_chain_tfp_hmc,
            }
        )
        return run_full_chain(adapter, initial_state, config)

    contract_payload = _reusable_static_contract_payload(
        config,
        hmc_adapter_signature=stable_adapter_signature(adapter),
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
        "round_index": int(round_index),
        "budget": int(budget),
        "role": str(role),
        "route": "fixed_mass_scoped_reusable_runner",
        "static_contract_hash": contract_hash,
        "call_config_hash": stable_config_hash(config.signature_payload()),
        "runner_reused": runner_reused,
        "used_single_use_runner": False,
    }
    route_events.append(route_event)
    return FullChainHMCRunResult(
        samples=result.samples,
        trace=result.trace,
        diagnostics=result.diagnostics,
        metadata={
            **dict(result.metadata),
            "fixed_mass_budget_ladder_route": route_event["route"],
            "fixed_mass_budget_ladder_role": route_event["role"],
            "fixed_mass_budget_ladder_static_contract_hash": contract_hash,
            "fixed_mass_budget_ladder_call_config_hash": route_event[
                "call_config_hash"
            ],
            "fixed_mass_budget_ladder_runner_reused": runner_reused,
            "fixed_mass_budget_ladder_static_contract_payload": contract_payload,
        },
    )


def _reusable_static_contract_payload(
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
    state_contract = _reusable_state_template_contract(initial_state)
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


def _reusable_state_template_contract(initial_state: Any) -> Mapping[str, Any]:
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


def _runner_route_summary(
    *,
    active_route: str,
    events: Sequence[Mapping[str, Any]],
    contract_payloads: Mapping[str, Mapping[str, Any]],
) -> Mapping[str, Any]:
    return {
        "active_route": active_route,
        "semantic_source": "run_fixed_mass_hmc_tuning_budget_ladder",
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
        and active_route == "fixed_mass_scoped_reusable_runner",
        "fallback_status": (
            "none"
            if active_route == "fixed_mass_scoped_reusable_runner"
            and not any(item.get("used_single_use_runner") is True for item in events)
            else "inactive_reusable_route"
        ),
        "route_nonclaims": (
            "route telemetry is engineering evidence only",
            "does not change selected step or HMC kernel semantics",
            "does not establish posterior convergence or sampler superiority",
        ),
    }


def _emit_budget_ladder_boundary_progress(
    callback: ProgressCallback | None,
    *,
    stage: str,
    role: str,
    round_index: int,
    budget: int,
    config: FullChainHMCConfig,
    route_category: str,
    started: bool = False,
    completed: bool = False,
    elapsed_s: float | None = None,
    started_perf_counter_s: float | None = None,
    runner_event: Mapping[str, Any] | None = None,
    error_type: str | None = None,
) -> None:
    if callback is None:
        return
    payload: dict[str, Any] = {
        "stage": str(stage),
        "round_index": int(round_index),
        "budget": int(budget),
        "role": str(role),
        "started": bool(started),
        "completed": bool(completed),
        "route_category": str(route_category),
        "call_config_hash": stable_config_hash(config.signature_payload()),
        "num_results": int(config.num_results),
        "num_burnin_steps": int(config.num_burnin_steps),
        "substage_budget_details_exposed": True,
        "uses_dual_averaging": bool(config.tuning_policy.uses_dual_averaging),
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
        "nonclaims": BUDGET_LADDER_NONCLAIMS,
    }
    if started_perf_counter_s is not None:
        payload["started_perf_counter_s"] = float(started_perf_counter_s)
        payload["timing_anchor_role"] = "process_local_monotonic_debug_only"
    if elapsed_s is not None:
        payload["elapsed_s"] = float(elapsed_s)
    if error_type is not None:
        payload["error_type"] = str(error_type)
    callback(str(stage), payload)


def _telemetry_payload(value: Any) -> Mapping[str, Any] | None:
    if value is None:
        return None
    payload = {key: _json_ready(item) for key, item in dict(value).items()}
    if "telemetry_failure_veto" in value:
        payload["telemetry_failure_veto_bool"] = bool(
            _bool_or_none(value["telemetry_failure_veto"])
        )
    return payload


def _tune_hard_vetoes(
    config: FixedMassHMCTuningBudgetLadderConfig,
    diagnostics: Mapping[str, Any],
    *,
    budget: int,
    tuned_step: float | None,
    tune_error: Exception | None,
) -> list[str]:
    vetoes: list[str] = []
    if tune_error is not None:
        vetoes.append("tune_hmc_error")
    if diagnostics.get("acceptance_rate") is None or not _finite_number(
        diagnostics.get("acceptance_rate")
    ):
        vetoes.append("tune_acceptance_missing_or_nonfinite")
    if tuned_step is None:
        vetoes.append("tune_final_step_missing_or_nonfinite")
    if diagnostics.get("log_accept_ratio_finite") is not True:
        vetoes.append("tune_log_accept_nonfinite_or_missing")
    if diagnostics.get("samples_all_finite") is not True:
        vetoes.append("tune_samples_nonfinite_or_missing")
    if diagnostics.get("num_adaptation_steps") is not None and int(
        diagnostics["num_adaptation_steps"]
    ) != int(budget):
        vetoes.append("tune_adaptation_steps_mismatch")
    telemetry = diagnostics.get("target_status_telemetry")
    if isinstance(telemetry, Mapping) and telemetry.get("telemetry_failure_veto_bool"):
        vetoes.append("tune_target_status_telemetry_failure")
    step_stability = diagnostics.get("step_stability")
    if (
        config.step_stability_is_hard_veto
        and isinstance(step_stability, Mapping)
        and step_stability.get("within_rtol") is False
    ):
        vetoes.append("tune_step_stability_outside_rtol")
    return vetoes


def _classify_screen_round(
    config: FixedMassHMCTuningBudgetLadderConfig,
    *,
    screen_diagnostics: Mapping[str, Any],
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
        hard_vetoes.append("screen_hmc_error")
    acceptance = screen_diagnostics.get("acceptance_rate")
    if acceptance is None or not _finite_number(acceptance):
        hard_vetoes.append("screen_acceptance_missing_or_nonfinite")
    if screen_diagnostics.get("log_accept_ratio_finite") is not True:
        hard_vetoes.append("screen_log_accept_nonfinite_or_missing")
    if screen_diagnostics.get("samples_all_finite") is not True:
        hard_vetoes.append("screen_samples_nonfinite_or_missing")
    if screen_diagnostics.get("target_log_prob_finite") is False:
        hard_vetoes.append("screen_target_log_prob_nonfinite")
    telemetry = screen_diagnostics.get("target_status_telemetry")
    if isinstance(telemetry, Mapping) and telemetry.get("telemetry_failure_veto_bool"):
        hard_vetoes.append("screen_target_status_telemetry_failure")
    hard_vetoes.extend(callback_result.hard_vetoes)
    if hard_vetoes:
        return (
            "hard_veto",
            "hard_veto",
            tuple(hard_vetoes),
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
    repair_triggers_list = list(callback_result.repair_triggers)
    if _finite_number(acceptance):
        acceptance_value = float(acceptance)
        if acceptance_value < config.repair_band[0]:
            repair_triggers_list.append("screen_acceptance_below_repair_band")
        elif acceptance_value > config.repair_band[1]:
            repair_triggers_list.append("screen_acceptance_above_repair_band")
    repair_triggers = tuple(dict.fromkeys(str(item) for item in repair_triggers_list))
    in_acceptance = (
        _finite_number(acceptance)
        and config.acceptance_band[0] <= float(acceptance) <= config.acceptance_band[1]
    )
    if promotion_vetoes or repair_triggers:
        if promotion_vetoes or callback_result.repair_triggers:
            return (
                "promotion_veto_repair",
                "promotion_veto_repair_trigger",
                (),
                (),
                promotion_vetoes,
                repair_triggers,
            )
        return (
            "acceptance_repair",
            "acceptance_repair_trigger",
            (),
            (),
            (),
            repair_triggers,
        )
    if in_acceptance:
        return "passed", "tuning_screen_promotion_only", (), (), (), ()
    return (
        "acceptance_repair",
        "acceptance_repair_trigger",
        (),
        (),
        (),
        ("acceptance_outside_pass_band_inside_repair_band",),
    )


def _next_initial_step_after_screen_repair(
    config: FixedMassHMCTuningBudgetLadderConfig,
    *,
    tuned_step: float,
    screen_diagnostics: Mapping[str, Any],
    classification: str,
) -> float:
    base_step = float(tuned_step)
    if not np.isfinite(base_step) or base_step <= 0.0:
        raise ValueError("finite positive tuned_step is required for repair handoff")
    if classification not in {"acceptance_repair", "promotion_veto_repair"}:
        return base_step
    acceptance = _scalar_or_none(screen_diagnostics.get("acceptance_rate"))
    if acceptance is None or not np.isfinite(acceptance):
        return base_step
    if acceptance < config.acceptance_band[0]:
        repaired = 0.5 * base_step
    elif acceptance > config.acceptance_band[1]:
        repaired = 2.0 * base_step
    else:
        return base_step
    if not np.isfinite(repaired) or repaired <= 0.0:
        raise ValueError("finite positive repaired step is required for repair handoff")
    return float(repaired)


def _call_screen_callback(
    callback: ScreenCallback | None,
    *,
    round_payload: Mapping[str, Any],
    samples: Any,
    diagnostics: Mapping[str, Any],
) -> FixedMassHMCTuningBudgetCallbackResult:
    if callback is None:
        return FixedMassHMCTuningBudgetCallbackResult()
    try:
        raw = callback(round_payload, samples, diagnostics)
        return _coerce_callback_result(raw)
    except Exception as exc:  # noqa: BLE001 - callback failures are fail-closed.
        return FixedMassHMCTuningBudgetCallbackResult(
            hard_vetoes=("callback_error",),
            diagnostics={
                "error_type": type(exc).__name__,
                "error_message": str(exc),
            },
        )


def _coerce_callback_result(raw: Any) -> FixedMassHMCTuningBudgetCallbackResult:
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


def _mass_artifact_signature(mass_artifact: PrecomputedMassArtifact) -> str:
    return program_signature(
        {
            "signature_payload": mass_artifact.signature_payload(),
            "position": np.asarray(mass_artifact.position, dtype=float),
            "covariance": np.asarray(mass_artifact.covariance, dtype=float),
            "factor": np.asarray(mass_artifact.factor, dtype=float),
        }
    )


def _error_diagnostics(exc: Exception) -> Mapping[str, Any]:
    return {
        "error_type": type(exc).__name__,
        "error_message": str(exc),
        "acceptance_rate": None,
        "samples_all_finite": False,
        "log_accept_ratio_finite": False,
        "target_log_prob_finite": False,
        "final_step_size": None,
        "final_step_size_finite": False,
    }


def _step_stability_payload(
    *,
    previous_step: float,
    tuned_step: float | None,
    rtol: float | None,
) -> Mapping[str, Any]:
    if tuned_step is None:
        return {
            "previous_step": float(previous_step),
            "tuned_step": None,
            "relative_change": None,
            "rtol": None if rtol is None else float(rtol),
            "within_rtol": None,
        }
    denominator = max(abs(float(previous_step)), np.finfo(float).tiny)
    relative_change = abs(float(tuned_step) - float(previous_step)) / denominator
    within_rtol = None if rtol is None else bool(relative_change <= float(rtol))
    return {
        "previous_step": float(previous_step),
        "tuned_step": float(tuned_step),
        "relative_change": float(relative_change),
        "rtol": None if rtol is None else float(rtol),
        "within_rtol": within_rtol,
    }


def _round_seed(base: tuple[int, int], index: int) -> tuple[int, int]:
    return int(base[0]), int(base[1]) + int(index)


def _validate_seed(seed: Sequence[int]) -> tuple[int, int]:
    values = tuple(int(item) for item in seed)
    if len(values) != 2:
        raise ValueError("seed must contain exactly two integers")
    return values


def _validate_band(values: Sequence[float], *, name: str) -> tuple[float, float]:
    if len(tuple(values)) != 2:
        raise ValueError(f"{name} must contain exactly two values")
    lower, upper = tuple(float(item) for item in values)
    if not np.isfinite(lower) or not np.isfinite(upper):
        raise ValueError(f"{name} values must be finite")
    if not 0.0 < lower <= upper < 1.0:
        raise ValueError(f"{name} must satisfy 0 < lower <= upper < 1")
    return lower, upper


def _string_tuple(values: Sequence[str] | str) -> tuple[str, ...]:
    if isinstance(values, str):
        raw = (values,)
    else:
        raw = tuple(values)
    return tuple(str(item) for item in raw if str(item))


def _positive_finite_or_none(value: Any) -> float | None:
    scalar = _scalar_or_none(value)
    if scalar is None or not np.isfinite(scalar) or scalar <= 0.0:
        return None
    return scalar


def _finite_number(value: Any) -> bool:
    scalar = _scalar_or_none(value)
    return scalar is not None and bool(np.isfinite(scalar))


def _tensor_to_numpy(value: Any) -> Any:
    if hasattr(value, "numpy"):
        return value.numpy()
    return value


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
