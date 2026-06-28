from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

import numpy as np
import pytest
import tensorflow as tf

import bayesfilter
import bayesfilter.inference.hmc_budget_ladder as hmc_budget_ladder
from bayesfilter.inference import (
    FixedMassHMCTuningBudgetCallbackResult,
    FixedMassHMCTuningBudgetLadderConfig,
    FixedMassHMCTuningBudgetLadderResult,
    PrecomputedMassArtifact,
    ValueScoreCapability,
    run_fixed_mass_hmc_tuning_budget_ladder,
)


class _ToyGaussianAdapter:
    parameter_dim = 2

    def adapter_signature(self) -> str:
        return "budget-ladder-toy-gaussian-v1"

    def value_score_capability(self) -> ValueScoreCapability:
        return ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=False,
            runtime_backend="tensorflow",
            evidence_path="tests/test_hmc_budget_ladder.py",
            target_scope="budget_ladder_toy_gaussian",
            nonclaims=("tiny budget-ladder fixture only",),
        )

    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        value = tf.convert_to_tensor(theta, dtype=tf.float64)
        return -0.5 * tf.reduce_sum(tf.square(value), axis=-1), -value


class _ToyGaussianFullChainXLAAdapter(_ToyGaussianAdapter):
    def value_score_capability(self) -> ValueScoreCapability:
        return ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=True,
            full_chain_xla_diagnostic_ready=True,
            runtime_backend="tensorflow",
            evidence_path="tests/test_hmc_budget_ladder.py",
            target_scope="budget_ladder_toy_gaussian",
            nonclaims=("tiny budget-ladder full-chain XLA fixture only",),
        )


@dataclass(frozen=True)
class _FakeRunResult:
    samples: Any
    trace: Mapping[str, Any]
    diagnostics: Mapping[str, Any]
    metadata: Mapping[str, Any]


def _mass_artifact(
    adapter_signature: str = "budget-ladder-toy-gaussian-v1",
    *,
    position: np.ndarray | None = None,
    covariance: np.ndarray | None = None,
) -> PrecomputedMassArtifact:
    return PrecomputedMassArtifact.from_covariance(
        position=np.zeros(2) if position is None else position,
        covariance=np.eye(2) if covariance is None else covariance,
        adapter_signature=adapter_signature,
        position_role="map",
        covariance_source="unit_test_exact_covariance",
        source="unit_test_budget_ladder_mass",
        jitter=0.0,
    )


def _config(**overrides: Any) -> FixedMassHMCTuningBudgetLadderConfig:
    payload = {
        "budget_schedule": (4, 8, 16),
        "initial_step_size": 0.1,
        "num_leapfrog_steps": 2,
        "target_accept_prob": 0.70,
        "acceptance_band": (0.65, 0.75),
        "repair_band": (0.55, 0.85),
        "tune_num_results": 4,
        "screen_num_results": 4,
        "screen_num_burnin_steps": 2,
        "tune_seed_base": (20260619, 11),
        "screen_seed_base": (20260619, 21),
        "chain_execution_mode": "eager",
        "use_xla": False,
        "target_scope": "budget_ladder_toy_gaussian",
    }
    payload.update(overrides)
    return FixedMassHMCTuningBudgetLadderConfig(**payload)


def _initial_state_factory(
    seed: tuple[int, int],
    role: str,
    round_index: int,
    budget: int,
    step_size: float,
) -> tf.Tensor:
    del seed, role, round_index, budget, step_size
    return tf.zeros((2,), dtype=tf.float64)


def _fake_result(
    *,
    acceptance: float,
    step_size: float | None,
    samples: Any | None = None,
    finite_log_accept: bool = True,
    finite_samples: bool = True,
    target_log_prob_finite: bool = True,
    num_adaptation_steps: int | None = None,
) -> _FakeRunResult:
    sample_value = 0.0 if finite_samples else np.nan
    samples = (
        tf.constant([[sample_value, sample_value]], dtype=tf.float64)
        if samples is None
        else tf.convert_to_tensor(samples, dtype=tf.float64)
    )
    trace: dict[str, Any] = {
        "is_accepted": tf.constant([acceptance >= 0.5, acceptance >= 0.25]),
        "log_accept_ratio": tf.constant(
            [0.0, 0.1 if finite_log_accept else np.nan],
            dtype=tf.float64,
        ),
        "target_log_prob": tf.constant(
            [0.0, -0.5 if target_log_prob_finite else np.nan],
            dtype=tf.float64,
        ),
    }
    if step_size is not None:
        trace["step_size"] = tf.constant([step_size], dtype=tf.float64)
    diagnostics: dict[str, Any] = {
        "acceptance_rate": tf.constant(float(acceptance), dtype=tf.float64),
        "finite_sample_count": tf.constant(2 if finite_samples else 0, dtype=tf.int32),
        "nonfinite_sample_count": tf.constant(0 if finite_samples else 2, dtype=tf.int32),
        "trace_policy": "standard",
    }
    if step_size is not None:
        diagnostics["final_step_size"] = tf.constant(step_size, dtype=tf.float64)
        diagnostics["final_step_size_finite"] = tf.constant(np.isfinite(step_size))
    if num_adaptation_steps is not None:
        diagnostics["num_adaptation_steps"] = tf.constant(num_adaptation_steps, dtype=tf.int32)
        trace["num_adaptation_steps"] = tf.constant([num_adaptation_steps], dtype=tf.int32)
    return _FakeRunResult(
        samples=samples,
        trace=trace,
        diagnostics=diagnostics,
        metadata={"trace_unavailability": {}, "nonclaims": ("fake runner only",)},
    )


def _scripted_runner(screen_acceptances: list[float]):
    calls: list[tuple[str, int, str]] = []

    def run(adapter: Any, _initial_state: Any, config: Any) -> _FakeRunResult:
        uses_tuning = bool(config.tuning_policy.uses_dual_averaging)
        calls.append(
            (
                "tune" if uses_tuning else "screen",
                int(config.num_burnin_steps),
                adapter.adapter_signature(),
            )
        )
        if uses_tuning:
            return _fake_result(
                acceptance=0.70,
                step_size=0.2 + 0.01 * len(calls),
                num_adaptation_steps=config.tuning_policy.num_adaptation_steps,
            )
        acceptance = screen_acceptances.pop(0)
        return _fake_result(acceptance=acceptance, step_size=None)

    return run, calls


def test_budget_ladder_config_validation_rejects_unbounded_or_missing_diagnostics() -> None:
    with pytest.raises(ValueError, match="budget_schedule"):
        _config(budget_schedule=())
    with pytest.raises(ValueError, match="screen_trace_policy"):
        _config(screen_trace_policy="reduced")
    with pytest.raises(ValueError, match="tuning_trace_policy"):
        _config(tuning_trace_policy="reduced")
    with pytest.raises(ValueError, match="repair_band"):
        _config(acceptance_band=(0.65, 0.75), repair_band=(0.66, 0.74))


def test_budget_ladder_acceptance_repair_advances_and_then_selects_stable_hash() -> None:
    run, calls = _scripted_runner([0.82, 0.70])

    result = run_fixed_mass_hmc_tuning_budget_ladder(
        adapter=_ToyGaussianAdapter(),
        mass_artifact=_mass_artifact(),
        initial_state_factory=_initial_state_factory,
        config=_config(budget_schedule=(4, 8)),
        run_full_chain=run,
    )

    assert isinstance(result, FixedMassHMCTuningBudgetLadderResult)
    assert result.passed is True
    assert [round_result.classification for round_result in result.rounds] == [
        "acceptance_repair",
        "passed",
    ]
    assert [(role, burnin) for role, burnin, _signature in calls] == [
        ("tune", 4),
        ("screen", 2),
        ("tune", 8),
        ("screen", 2),
    ]
    assert all(
        signature != "budget-ladder-toy-gaussian-v1"
        for _role, _burnin, signature in calls
    )
    assert result.selected_config_payload is not None
    assert result.selected_config_hash
    assert result.artifact_hash == run_fixed_mass_hmc_tuning_budget_ladder(
        adapter=_ToyGaussianAdapter(),
        mass_artifact=_mass_artifact(),
        initial_state_factory=_initial_state_factory,
        config=_config(budget_schedule=(4, 8)),
        run_full_chain=_scripted_runner([0.82, 0.70])[0],
    ).artifact_hash


def test_budget_ladder_fixed_mass_wrapper_preserves_full_chain_xla_authority() -> None:
    seen_capabilities: list[ValueScoreCapability] = []

    def run(adapter: Any, _initial_state: Any, config: Any) -> _FakeRunResult:
        del config
        seen_capabilities.append(adapter.value_score_capability())
        return _fake_result(
            acceptance=0.70,
            step_size=0.2 if len(seen_capabilities) == 1 else None,
            num_adaptation_steps=4 if len(seen_capabilities) == 1 else None,
        )

    result = run_fixed_mass_hmc_tuning_budget_ladder(
        adapter=_ToyGaussianFullChainXLAAdapter(),
        mass_artifact=_mass_artifact(),
        initial_state_factory=_initial_state_factory,
        config=_config(
            budget_schedule=(4,),
            chain_execution_mode="tf_function",
            use_xla=True,
        ),
        run_full_chain=run,
    )

    assert result.passed is True
    assert len(seen_capabilities) == 2
    for capability in seen_capabilities:
        assert capability.xla_hmc_ready is True
        assert capability.full_chain_xla_diagnostic_ready is True
        assert capability.is_accepted_full_chain_xla_diagnostic_authority is True
        assert any(
            "preserves XLA authority only from accepted base authority" in claim
            for claim in capability.nonclaims
        )


def test_budget_ladder_finite_acceptance_outside_repair_band_repairs() -> None:
    run, calls = _scripted_runner([0.90, 0.70])

    result = run_fixed_mass_hmc_tuning_budget_ladder(
        adapter=_ToyGaussianAdapter(),
        mass_artifact=_mass_artifact(),
        initial_state_factory=_initial_state_factory,
        config=_config(budget_schedule=(4, 8)),
        run_full_chain=run,
    )

    assert result.passed is True
    assert result.final_status == "passed"
    assert [round_result.classification for round_result in result.rounds] == [
        "acceptance_repair",
        "passed",
    ]
    assert result.rounds[0].hard_vetoes == ()
    assert result.rounds[0].repair_triggers == ("screen_acceptance_above_repair_band",)
    assert [(role, burnin) for role, burnin, _signature in calls] == [
        ("tune", 4),
        ("screen", 2),
        ("tune", 8),
        ("screen", 2),
    ]


def test_budget_ladder_nonfinite_screen_diagnostics_still_hard_veto() -> None:
    calls: list[str] = []

    def run(_adapter: Any, _initial_state: Any, config: Any) -> _FakeRunResult:
        uses_tuning = bool(config.tuning_policy.uses_dual_averaging)
        calls.append("tune" if uses_tuning else "screen")
        if uses_tuning:
            return _fake_result(
                acceptance=0.70,
                step_size=0.2,
                num_adaptation_steps=config.tuning_policy.num_adaptation_steps,
            )
        return _fake_result(
            acceptance=0.70,
            step_size=None,
            finite_samples=False,
        )

    result = run_fixed_mass_hmc_tuning_budget_ladder(
        adapter=_ToyGaussianAdapter(),
        mass_artifact=_mass_artifact(),
        initial_state_factory=_initial_state_factory,
        config=_config(budget_schedule=(4, 8)),
        run_full_chain=run,
    )

    assert result.passed is False
    assert result.final_status == "hard_veto"
    assert result.rounds[0].classification == "hard_veto"
    assert result.rounds[0].hard_vetoes == ("screen_samples_nonfinite_or_missing",)
    assert calls == ["tune", "screen"]


def test_budget_ladder_callback_roles_are_preserved() -> None:
    run, _calls = _scripted_runner([0.70, 0.70])

    def callback(_round_payload: Mapping[str, Any], _samples: Any, _diagnostics: Mapping[str, Any]) -> Mapping[str, Any]:
        return {
            "promotion_vetoes": ("domain_boundary_needs_more_budget",),
            "repair_triggers": ("domain_repair",),
            "diagnostics": {"source": "unit_test"},
        }

    result = run_fixed_mass_hmc_tuning_budget_ladder(
        adapter=_ToyGaussianAdapter(),
        mass_artifact=_mass_artifact(),
        initial_state_factory=_initial_state_factory,
        config=_config(budget_schedule=(4,)),
        screen_callback=callback,
        run_full_chain=run,
    )

    assert result.passed is False
    assert result.final_status == "budget_exhausted"
    assert result.rounds[0].classification == "promotion_veto_repair"
    assert result.rounds[0].promotion_vetoes == ("domain_boundary_needs_more_budget",)
    assert result.rounds[0].repair_triggers == ("domain_repair",)


def test_budget_ladder_repair_trigger_without_promotion_veto_blocks_selection() -> None:
    run, _calls = _scripted_runner([0.70])

    def callback(
        _round_payload: Mapping[str, Any],
        _samples: Any,
        _diagnostics: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        return {"repair_triggers": ("domain_needs_more_tuning_budget",)}

    result = run_fixed_mass_hmc_tuning_budget_ladder(
        adapter=_ToyGaussianAdapter(),
        mass_artifact=_mass_artifact(),
        initial_state_factory=_initial_state_factory,
        config=_config(budget_schedule=(4,)),
        screen_callback=callback,
        run_full_chain=run,
    )

    assert result.passed is False
    assert result.final_status == "budget_exhausted"
    assert result.rounds[0].classification == "promotion_veto_repair"
    assert result.rounds[0].promotion_vetoes == ()
    assert result.rounds[0].repair_triggers == ("domain_needs_more_tuning_budget",)


def test_budget_ladder_callback_hard_veto_stops_and_records_callback_result() -> None:
    run, _calls = _scripted_runner([0.70])

    def callback(
        _round_payload: Mapping[str, Any],
        _samples: Any,
        _diagnostics: Mapping[str, Any],
    ) -> FixedMassHMCTuningBudgetCallbackResult:
        return FixedMassHMCTuningBudgetCallbackResult(
            hard_vetoes=("domain_hard_veto",),
            diagnostics={"source": "unit_test"},
        )

    result = run_fixed_mass_hmc_tuning_budget_ladder(
        adapter=_ToyGaussianAdapter(),
        mass_artifact=_mass_artifact(),
        initial_state_factory=_initial_state_factory,
        config=_config(budget_schedule=(4, 8)),
        screen_callback=callback,
        run_full_chain=run,
    )

    assert result.final_status == "hard_veto"
    assert result.rounds[0].hard_vetoes == ("domain_hard_veto",)
    assert result.rounds[0].callback_result.diagnostics["source"] == "unit_test"


def test_budget_ladder_callback_continuation_veto_is_distinct_from_hard_veto() -> None:
    run, _calls = _scripted_runner([0.70])

    def callback(
        _round_payload: Mapping[str, Any],
        _samples: Any,
        _diagnostics: Mapping[str, Any],
    ) -> FixedMassHMCTuningBudgetCallbackResult:
        return FixedMassHMCTuningBudgetCallbackResult(
            continuation_vetoes=("artifact_cannot_answer_question",),
        )

    result = run_fixed_mass_hmc_tuning_budget_ladder(
        adapter=_ToyGaussianAdapter(),
        mass_artifact=_mass_artifact(),
        initial_state_factory=_initial_state_factory,
        config=_config(budget_schedule=(4, 8)),
        screen_callback=callback,
        run_full_chain=run,
    )

    assert result.final_status == "continuation_veto"
    assert result.rounds[0].classification == "continuation_veto"
    assert result.rounds[0].hard_vetoes == ()
    assert result.rounds[0].continuation_vetoes == ("artifact_cannot_answer_question",)


def test_budget_ladder_injected_tf_function_run_bypasses_reusable_runner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_if_built(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("injected run_full_chain must bypass reusable runner")

    run, calls = _scripted_runner([0.70])
    monkeypatch.setattr(
        hmc_budget_ladder,
        "build_reusable_full_chain_tfp_hmc_runner",
        fail_if_built,
    )

    result = run_fixed_mass_hmc_tuning_budget_ladder(
        adapter=_ToyGaussianAdapter(),
        mass_artifact=_mass_artifact(),
        initial_state_factory=_initial_state_factory,
        config=_config(budget_schedule=(4,), chain_execution_mode="tf_function"),
        run_full_chain=run,
    )

    assert result.passed is True
    assert [(role, burnin) for role, burnin, _signature in calls] == [
        ("tune", 4),
        ("screen", 2),
    ]
    route = result.runner_route_summary
    assert route["active_route"] == "single_use_or_injected_runner"
    assert route["reusable_runner_build_count"] == 0
    assert route["injected_runner_call_count"] == 2


def test_budget_ladder_default_tf_function_route_uses_reusable_runner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[Mapping[str, Any]] = []

    class _FakeReusableRunner:
        def __init__(self, config: Any) -> None:
            self.config = config

        def run(self, *, current_state: Any, seed: Any, step_size: Any) -> _FakeRunResult:
            role = "tune" if self.config.tuning_policy.uses_dual_averaging else "screen"
            calls.append(
                {
                    "role": role,
                    "seed": tuple(int(item) for item in seed),
                    "step_size": float(step_size),
                    "num_burnin_steps": int(self.config.num_burnin_steps),
                    "initial_state": np.asarray(current_state, dtype=float),
                }
            )
            if role == "tune":
                return _fake_result(
                    acceptance=0.70,
                    step_size=0.2,
                    num_adaptation_steps=self.config.tuning_policy.num_adaptation_steps,
                )
            return _fake_result(acceptance=0.70, step_size=None)

    def fake_builder(adapter: Any, initial_state_template: Any, config: Any) -> _FakeReusableRunner:
        calls.append(
            {
                "builder": True,
                "adapter_signature": adapter.adapter_signature(),
                "num_results": int(config.num_results),
                "num_burnin_steps": int(config.num_burnin_steps),
                "uses_dual_averaging": bool(config.tuning_policy.uses_dual_averaging),
                "initial_state_template": np.asarray(initial_state_template, dtype=float),
            }
        )
        return _FakeReusableRunner(config)

    monkeypatch.setattr(
        hmc_budget_ladder,
        "build_reusable_full_chain_tfp_hmc_runner",
        fake_builder,
    )

    result = run_fixed_mass_hmc_tuning_budget_ladder(
        adapter=_ToyGaussianAdapter(),
        mass_artifact=_mass_artifact(),
        initial_state_factory=_initial_state_factory,
        config=_config(budget_schedule=(4,), chain_execution_mode="tf_function"),
    )

    assert result.passed is True
    builder_calls = [call for call in calls if call.get("builder")]
    run_calls = [call for call in calls if call.get("role")]
    assert len(builder_calls) == 2
    assert [call["uses_dual_averaging"] for call in builder_calls] == [True, False]
    assert [call["role"] for call in run_calls] == ["tune", "screen"]
    assert all(
        call["adapter_signature"] != _ToyGaussianAdapter().adapter_signature()
        for call in builder_calls
    )
    route = result.runner_route_summary
    assert route["active_route"] == "fixed_mass_scoped_reusable_runner"
    assert route["reusable_runner_build_count"] == 2
    assert route["distinct_static_runner_contract_count"] == 2
    assert route["single_use_build_count"] == 0
    assert route["fallback_status"] == "none"
    assert result.rounds[0].tune_diagnostics["runtime_metadata"][
        "fixed_mass_budget_ladder_route"
    ] == "fixed_mass_scoped_reusable_runner"
    assert result.rounds[0].screen_diagnostics["runtime_metadata"][
        "fixed_mass_budget_ladder_static_contract_hash"
    ] == route["round_route_events"][1]["static_contract_hash"]


def test_budget_ladder_default_reusable_route_reuses_repeated_screen_contract(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    screen_acceptances = [0.82, 0.70]
    runner_builds: list[Mapping[str, Any]] = []

    class _FakeReusableRunner:
        def __init__(self, config: Any) -> None:
            self.config = config

        def run(self, *, current_state: Any, seed: Any, step_size: Any) -> _FakeRunResult:
            del current_state, seed, step_size
            if self.config.tuning_policy.uses_dual_averaging:
                return _fake_result(
                    acceptance=0.70,
                    step_size=0.2,
                    num_adaptation_steps=self.config.tuning_policy.num_adaptation_steps,
                )
            return _fake_result(
                acceptance=screen_acceptances.pop(0),
                step_size=None,
            )

    def fake_builder(_adapter: Any, _initial_state_template: Any, config: Any) -> _FakeReusableRunner:
        runner_builds.append(
            {
                "uses_dual_averaging": bool(config.tuning_policy.uses_dual_averaging),
                "num_burnin_steps": int(config.num_burnin_steps),
                "step_size": float(config.step_size),
                "seed": tuple(config.seed),
            }
        )
        return _FakeReusableRunner(config)

    monkeypatch.setattr(
        hmc_budget_ladder,
        "build_reusable_full_chain_tfp_hmc_runner",
        fake_builder,
    )

    result = run_fixed_mass_hmc_tuning_budget_ladder(
        adapter=_ToyGaussianAdapter(),
        mass_artifact=_mass_artifact(),
        initial_state_factory=_initial_state_factory,
        config=_config(budget_schedule=(4, 8), chain_execution_mode="tf_function"),
    )

    assert result.passed is True
    assert [round_result.classification for round_result in result.rounds] == [
        "acceptance_repair",
        "passed",
    ]
    route = result.runner_route_summary
    assert route["reusable_runner_build_count"] == 3
    assert route["distinct_static_runner_contract_count"] == 3
    screen_events = [
        event for event in route["round_route_events"] if event["role"] == "screen"
    ]
    assert [event["runner_reused"] for event in screen_events] == [False, True]
    assert sum(not build["uses_dual_averaging"] for build in runner_builds) == 1


def test_budget_ladder_reusable_route_preserves_xla_authority_failure() -> None:
    result = run_fixed_mass_hmc_tuning_budget_ladder(
        adapter=_ToyGaussianAdapter(),
        mass_artifact=_mass_artifact(),
        initial_state_factory=_initial_state_factory,
        config=_config(
            budget_schedule=(4,),
            chain_execution_mode="tf_function",
            use_xla=True,
        ),
    )

    assert result.passed is False
    assert result.final_status == "hard_veto"
    assert "tune_hmc_error" in result.rounds[0].hard_vetoes
    assert result.rounds[0].tune_diagnostics["error_type"] == "ValueError"
    assert "full-chain-XLA diagnostic authority" in result.rounds[0].tune_diagnostics[
        "error_message"
    ]


def test_budget_ladder_budget_exhaustion_is_distinct_from_hard_veto() -> None:
    run, _calls = _scripted_runner([0.82, 0.83])

    result = run_fixed_mass_hmc_tuning_budget_ladder(
        adapter=_ToyGaussianAdapter(),
        mass_artifact=_mass_artifact(),
        initial_state_factory=_initial_state_factory,
        config=_config(budget_schedule=(4, 8)),
        run_full_chain=run,
    )

    assert result.passed is False
    assert result.final_status == "budget_exhausted"
    assert [round_result.classification for round_result in result.rounds] == [
        "acceptance_repair",
        "acceptance_repair",
    ]
    assert result.selected_config_hash is None
    assert result.repair_config_hash
    assert result.repair_config_payload is not None
    payload = result.payload()
    assert payload["repair_config_available"] is True
    assert payload["repair_config_payload_exposed"] is False
    assert "repair_config_payload" not in payload


def test_budget_ladder_builds_latent_fixed_mass_adapter_and_position_callback_samples() -> None:
    callbacks: list[tuple[str, np.ndarray]] = []

    def run(adapter: Any, _initial_state: Any, config: Any) -> _FakeRunResult:
        assert adapter.adapter_signature() != "budget-ladder-toy-gaussian-v1"
        uses_tuning = bool(config.tuning_policy.uses_dual_averaging)
        sample = [[0.0, 0.0]] if uses_tuning else [[1.0, -1.0]]
        return _fake_result(
            acceptance=0.70,
            step_size=0.2 if uses_tuning else None,
            samples=sample,
            num_adaptation_steps=(
                config.tuning_policy.num_adaptation_steps if uses_tuning else None
            ),
        )

    def callback(
        round_payload: Mapping[str, Any],
        samples: Any,
        _diagnostics: Mapping[str, Any],
    ) -> None:
        callbacks.append(
            (
                str(round_payload["sample_space"]),
                np.asarray(samples, dtype=float),
            )
        )

    mass_artifact = _mass_artifact(
        position=np.array([10.0, 20.0]),
        covariance=np.diag([4.0, 9.0]),
    )
    result = run_fixed_mass_hmc_tuning_budget_ladder(
        adapter=_ToyGaussianAdapter(),
        mass_artifact=mass_artifact,
        initial_state_factory=_initial_state_factory,
        config=_config(budget_schedule=(4,)),
        screen_callback=callback,
        run_full_chain=run,
    )

    assert result.passed is True
    assert result.adapter_signature == "budget-ladder-toy-gaussian-v1"
    assert result.hmc_adapter_signature != result.adapter_signature
    assert callbacks[0][0] == "position"
    np.testing.assert_allclose(callbacks[0][1], [[12.0, 17.0]])


def test_budget_ladder_callback_position_samples_preserve_sample_and_chain_axes() -> None:
    callbacks: list[np.ndarray] = []
    latent_screen_samples = np.array(
        [
            [[1.0, -1.0], [0.5, 0.25]],
            [[-0.25, 0.75], [0.0, 0.0]],
            [[0.1, 0.2], [0.3, 0.4]],
        ],
        dtype=float,
    )

    def run(adapter: Any, _initial_state: Any, config: Any) -> _FakeRunResult:
        assert adapter.adapter_signature() != "budget-ladder-toy-gaussian-v1"
        uses_tuning = bool(config.tuning_policy.uses_dual_averaging)
        return _fake_result(
            acceptance=0.70,
            step_size=0.2 if uses_tuning else None,
            samples=np.zeros((3, 2, 2)) if uses_tuning else latent_screen_samples,
            num_adaptation_steps=(
                config.tuning_policy.num_adaptation_steps if uses_tuning else None
            ),
        )

    def callback(
        _round_payload: Mapping[str, Any],
        samples: Any,
        _diagnostics: Mapping[str, Any],
    ) -> None:
        callbacks.append(np.asarray(samples, dtype=float))

    mass_artifact = _mass_artifact(
        position=np.array([10.0, 20.0]),
        covariance=np.diag([4.0, 9.0]),
    )
    result = run_fixed_mass_hmc_tuning_budget_ladder(
        adapter=_ToyGaussianAdapter(),
        mass_artifact=mass_artifact,
        initial_state_factory=_initial_state_factory,
        config=_config(budget_schedule=(4,)),
        screen_callback=callback,
        run_full_chain=run,
    )

    assert result.passed is True
    assert callbacks[0].shape == latent_screen_samples.shape
    np.testing.assert_allclose(
        callbacks[0],
        np.array([10.0, 20.0]) + latent_screen_samples @ np.diag([2.0, 3.0]),
    )


def test_budget_ladder_step_stability_can_be_hard_veto() -> None:
    run, _calls = _scripted_runner([0.70])

    result = run_fixed_mass_hmc_tuning_budget_ladder(
        adapter=_ToyGaussianAdapter(),
        mass_artifact=_mass_artifact(),
        initial_state_factory=_initial_state_factory,
        config=_config(
            budget_schedule=(4, 8),
            initial_step_size=0.1,
            step_stability_rtol=0.01,
            step_stability_is_hard_veto=True,
        ),
        run_full_chain=run,
    )

    assert result.final_status == "hard_veto"
    assert result.rounds[0].classification == "hard_veto"
    assert result.rounds[0].hard_vetoes == ("tune_step_stability_outside_rtol",)
    assert result.rounds[0].tune_diagnostics["step_stability"]["within_rtol"] is False


def test_budget_ladder_public_exports_are_additive() -> None:
    assert bayesfilter.FixedMassHMCTuningBudgetLadderConfig is (
        FixedMassHMCTuningBudgetLadderConfig
    )
    assert bayesfilter.run_fixed_mass_hmc_tuning_budget_ladder is (
        run_fixed_mass_hmc_tuning_budget_ladder
    )
    assert run_fixed_mass_hmc_tuning_budget_ladder.__module__ == (
        "bayesfilter.inference.hmc_budget_ladder"
    )


def test_budget_ladder_tiny_gaussian_real_tfp_round_runs() -> None:
    result = run_fixed_mass_hmc_tuning_budget_ladder(
        adapter=_ToyGaussianAdapter(),
        mass_artifact=_mass_artifact(),
        initial_state_factory=_initial_state_factory,
        config=_config(
            budget_schedule=(3,),
            initial_step_size=0.1,
            tune_num_results=3,
            screen_num_results=3,
            screen_num_burnin_steps=1,
        ),
    )

    assert len(result.rounds) == 1
    assert result.rounds[0].tune_diagnostics["final_step_size"] is not None
    assert result.rounds[0].tune_diagnostics["samples_all_finite"] is True
    assert result.rounds[0].screen_diagnostics["samples_all_finite"] is True
    assert "no posterior convergence claim" in result.nonclaims
