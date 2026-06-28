from __future__ import annotations

import sys
import types

import numpy as np
import pytest

import bayesfilter.inference.hmc as hmc_runtime
from bayesfilter.inference import (
    FullChainHMCConfig,
    HMCTuningPolicy,
    PrecomputedMassArtifact,
    PriorSupportError,
    TargetFailurePolicy,
    bracket_initial_step_size,
    classify_hmc_tuning_diagnostic,
    evaluate_target_with_failure_policy,
    run_fixed_mass_step_tuning_diagnostic,
)


def _mass_artifact() -> PrecomputedMassArtifact:
    return PrecomputedMassArtifact.from_negative_hessian(
        position=np.zeros(2),
        negative_hessian=np.array([[4.0, 0.5], [0.5, 3.0]]),
        adapter_signature="phase3_fixed_mass_adapter_v1",
        covariance_source="phase2_regularized_hessian",
        jitter=0.0,
        eigenvalue_floor=1.0e-6,
    )


def _policy() -> HMCTuningPolicy:
    return HMCTuningPolicy.fixed_mass_dual_averaging(
        num_adaptation_steps=3,
        target_accept_prob=0.75,
        source="tests/test_hmc_fixed_mass_step_tuning.py",
    )


def test_initial_step_bracket_records_attempts_and_selects_finite_step():
    result = bracket_initial_step_size(
        target_probe_fn=lambda step: step <= 0.25,
        initial_step_size=1.0,
        max_attempts=4,
        contraction=0.5,
    )

    assert result.passed is True
    assert result.selected_step_size == pytest.approx(0.25)
    assert [attempt.finite for attempt in result.attempts] == [False, False, True]
    assert [attempt.step_size for attempt in result.attempts] == pytest.approx(
        [1.0, 0.5, 0.25]
    )
    assert "no posterior convergence claim" in result.nonclaims


def test_fixed_mass_step_tuning_records_frozen_mass_and_required_telemetry():
    artifact = _mass_artifact()
    target_policy = TargetFailurePolicy("phase3-fixed-mass-toy")

    def valid_target(theta):
        theta = np.asarray(theta, dtype=float)
        return -0.5 * float(theta @ theta), -theta

    evaluation = evaluate_target_with_failure_policy(
        valid_target,
        np.zeros(2),
        target_policy,
    )
    classification = classify_hmc_tuning_diagnostic(
        _policy(),
        target_evaluation=evaluation,
    )

    result = run_fixed_mass_step_tuning_diagnostic(
        _policy(),
        mass_artifact=artifact,
        initial_state=np.zeros(2),
        target_probe_fn=lambda step: np.isfinite(step),
        target_failure_classification=classification,
        num_results=4,
        num_burnin_steps=4,
        step_size=0.05,
        num_leapfrog_steps=2,
        seed=(20260613, 11),
    )
    payload = result.payload()

    assert result.frozen_mass_invariant["passed"] is True
    assert result.frozen_mass_invariant["mass_update_allowed"] is False
    assert result.frozen_mass_invariant["signature_includes_arrays"] is True
    assert artifact.covariance.flags.writeable is False
    assert artifact.factor.flags.writeable is False
    assert result.mass_artifact_signature == result.frozen_mass_invariant[
        "before_signature"
    ]
    assert result.mass_artifact_signature == result.frozen_mass_invariant[
        "after_signature"
    ]
    assert result.mass_artifact_payload["regularization_report"][
        "silent_eigenvalue_reflection"
    ] is False
    assert result.diagnostic.diagnostics["final_step_size_finite"] is True
    assert result.diagnostic.diagnostics["num_adaptation_steps"] == 3
    assert result.diagnostic.diagnostics["target_accept_prob"] == pytest.approx(0.75)
    assert "step_size" in result.diagnostic.trace
    assert "log_accept_ratio" in result.diagnostic.trace
    assert classification["classification"] == "tuning_diagnostic_passed_not_convergence"
    assert result.minimum_phase4_telemetry_present() == {
        "final_finite_step_size": True,
        "step_size_trace_or_bracket": True,
        "acceptance_log_accept_tuning_only": True,
        "adaptation_step_count": True,
        "target_accept_probability": True,
        "frozen_mass_artifact_signature": True,
        "frozen_mass_invariant": True,
        "target_invalidity_classification": True,
        "explicit_nonclaims": True,
    }
    assert payload["metadata"]["minimum_phase4_telemetry_present"][
        "frozen_mass_invariant"
    ] is True
    assert "no posterior convergence claim" in result.nonclaims


def test_fixed_mass_signature_binds_array_payload():
    artifact_a = _mass_artifact()
    artifact_b = PrecomputedMassArtifact.from_negative_hessian(
        position=np.zeros(2),
        negative_hessian=np.array([[5.0, 0.5], [0.5, 3.0]]),
        adapter_signature="phase3_fixed_mass_adapter_v1",
        covariance_source="phase2_regularized_hessian",
        jitter=0.0,
        eigenvalue_floor=1.0e-6,
    )
    classification = {
        "classification": "tuning_diagnostic_passed_not_convergence",
        "diagnostic_role": "diagnostic_only",
        "nonclaims": ("no posterior convergence claim",),
    }

    result_a = run_fixed_mass_step_tuning_diagnostic(
        _policy(),
        mass_artifact=artifact_a,
        initial_state=np.zeros(2),
        target_probe_fn=lambda step: np.isfinite(step),
        target_failure_classification=classification,
        num_results=4,
        num_burnin_steps=4,
        step_size=0.05,
        num_leapfrog_steps=2,
        seed=(20260613, 13),
    )
    result_b = run_fixed_mass_step_tuning_diagnostic(
        _policy(),
        mass_artifact=artifact_b,
        initial_state=np.zeros(2),
        target_probe_fn=lambda step: np.isfinite(step),
        target_failure_classification=classification,
        num_results=4,
        num_burnin_steps=4,
        step_size=0.05,
        num_leapfrog_steps=2,
        seed=(20260613, 13),
    )

    assert result_a.mass_artifact_signature != result_b.mass_artifact_signature


def test_fixed_mass_step_tuning_preserves_bracketing_failure_artifact():
    artifact = _mass_artifact()
    classification = {
        "classification": "tuning_diagnostic_passed_not_convergence",
        "diagnostic_role": "diagnostic_only",
        "nonclaims": ("no posterior convergence claim",),
    }

    result = run_fixed_mass_step_tuning_diagnostic(
        _policy(),
        mass_artifact=artifact,
        initial_state=np.zeros(2),
        target_probe_fn=lambda step: False,
        target_failure_classification=classification,
        num_results=4,
        num_burnin_steps=4,
        step_size=0.05,
        num_leapfrog_steps=2,
    )

    assert result.passed is False
    assert result.initial_step_bracket.passed is False
    assert result.diagnostic.diagnostics["classification"] == (
        "initial_step_bracketing_failed"
    )
    assert result.diagnostic.metadata["diagnostic_role"] == "hard_veto"
    assert result.frozen_mass_invariant["passed"] is True
    assert result.initial_step_bracket.attempts[0].reason == "nonfinite_probe"


def test_fixed_mass_step_tuning_keeps_target_invalidity_separate_from_tuning():
    target_policy = TargetFailurePolicy("phase3-fixed-mass-invalid")

    def invalid_target(theta):
        raise PriorSupportError("outside support")

    evaluation = evaluate_target_with_failure_policy(
        invalid_target,
        np.zeros(2),
        target_policy,
    )
    classification = classify_hmc_tuning_diagnostic(
        _policy(),
        target_evaluation=evaluation,
    )

    assert classification["passed"] is False
    assert classification["classification"] == "target_invalidity_not_tuning_success"
    assert classification["diagnostic_role"] == "hard_veto"
    assert classification["failure_label"] == "prior_support"


def test_fixed_mass_step_tuning_requires_target_classification_schema():
    with pytest.raises(ValueError, match="target_failure_classification"):
        run_fixed_mass_step_tuning_diagnostic(
            _policy(),
            mass_artifact=_mass_artifact(),
            initial_state=np.zeros(2),
            target_probe_fn=lambda step: np.isfinite(step),
            target_failure_classification={"classification": "missing_role"},
            num_results=4,
            num_burnin_steps=4,
        )
    with pytest.raises(ValueError, match="unsupported classification"):
        run_fixed_mass_step_tuning_diagnostic(
            _policy(),
            mass_artifact=_mass_artifact(),
            initial_state=np.zeros(2),
            target_probe_fn=lambda step: np.isfinite(step),
            target_failure_classification={
                "classification": "locally_named_success",
                "diagnostic_role": "diagnostic_only",
                "nonclaims": ("no posterior convergence claim",),
            },
            num_results=4,
            num_burnin_steps=4,
        )
    with pytest.raises(ValueError, match="diagnostic_role"):
        run_fixed_mass_step_tuning_diagnostic(
            _policy(),
            mass_artifact=_mass_artifact(),
            initial_state=np.zeros(2),
            target_probe_fn=lambda step: np.isfinite(step),
            target_failure_classification={
                "classification": "tuning_diagnostic_passed_not_convergence",
                "diagnostic_role": "promotion",
                "nonclaims": ("no posterior convergence claim",),
            },
            num_results=4,
            num_burnin_steps=4,
        )
    with pytest.raises(ValueError, match="nonclaims"):
        run_fixed_mass_step_tuning_diagnostic(
            _policy(),
            mass_artifact=_mass_artifact(),
            initial_state=np.zeros(2),
            target_probe_fn=lambda step: np.isfinite(step),
            target_failure_classification={
                "classification": "tuning_diagnostic_passed_not_convergence",
                "diagnostic_role": "diagnostic_only",
                "nonclaims": (),
            },
            num_results=4,
            num_burnin_steps=4,
        )


def test_fixed_mass_step_tuning_rejects_non_fixed_mass_policy():
    artifact = _mass_artifact()
    policy = HMCTuningPolicy.dual_averaging_step_size(
        num_adaptation_steps=3,
        target_accept_prob=0.75,
        source="tests/test_hmc_fixed_mass_step_tuning.py",
    )

    with pytest.raises(ValueError, match="fixed_mass_dual_averaging"):
        run_fixed_mass_step_tuning_diagnostic(
            policy,
            mass_artifact=artifact,
            initial_state=np.zeros(2),
            target_probe_fn=lambda step: np.isfinite(step),
            target_failure_classification={
                "classification": "not_used",
                "diagnostic_role": "diagnostic_only",
                "nonclaims": ("no posterior convergence claim",),
            },
            num_results=4,
            num_burnin_steps=4,
        )


def test_xla_generic_dual_averaging_remains_blocked_for_phase3():
    generic_policy = HMCTuningPolicy.dual_averaging_step_size(
        num_adaptation_steps=3,
        target_accept_prob=0.75,
        source="tests/test_hmc_fixed_mass_step_tuning.py",
    )

    with pytest.raises(ValueError, match="fixed_mass_dual_averaging"):
        FullChainHMCConfig(
            num_results=4,
            num_burnin_steps=4,
            step_size=0.05,
            num_leapfrog_steps=2,
            seed=(20260613, 12),
            use_xla=True,
            tuning_policy=generic_policy,
        )


def test_sample_chain_runner_selects_eager_nonjit_and_xla_paths(monkeypatch):
    function_calls: list[dict[str, object]] = []
    sample_chain_calls: list[dict[str, object]] = []

    class FakeFunction:
        def __init__(self, fn, kwargs):
            self.fn = fn
            self.kwargs = dict(kwargs)

        def __call__(self):
            return self.fn()

    def fake_function(fn, **kwargs):
        function_calls.append(dict(kwargs))
        return FakeFunction(fn, kwargs)

    def fake_sample_chain(**kwargs):
        sample_chain_calls.append(dict(kwargs))
        return "samples", {"trace": "ok"}

    fake_tf = types.SimpleNamespace(
        int32="int32",
        constant=lambda value, dtype=None: ("constant", value, dtype),
        function=fake_function,
    )
    fake_tfp = types.SimpleNamespace(
        mcmc=types.SimpleNamespace(sample_chain=fake_sample_chain)
    )
    monkeypatch.setitem(sys.modules, "tensorflow", fake_tf)
    monkeypatch.setitem(sys.modules, "tensorflow_probability", fake_tfp)

    def config(**overrides):
        payload = {
            "num_results": 4,
            "num_burnin_steps": 1,
            "step_size": 0.05,
            "num_leapfrog_steps": 2,
            "seed": (20260613, 15),
        }
        payload.update(overrides)
        return FullChainHMCConfig(**payload)

    eager_runner = hmc_runtime._build_sample_chain_runner(
        config(chain_execution_mode="eager"),
        kernel="kernel",
        trace_fn=lambda _state, _results: {},
        initial_state="state",
    )
    assert not isinstance(eager_runner, FakeFunction)
    assert eager_runner() == ("samples", {"trace": "ok"})
    assert function_calls == []

    tf_runner = hmc_runtime._build_sample_chain_runner(
        config(chain_execution_mode="tf_function"),
        kernel="kernel",
        trace_fn=lambda _state, _results: {},
        initial_state="state",
    )
    assert isinstance(tf_runner, FakeFunction)
    assert tf_runner.kwargs["reduce_retracing"] is True
    assert "jit_compile" not in tf_runner.kwargs

    xla_runner = hmc_runtime._build_sample_chain_runner(
        config(chain_execution_mode="tf_function", use_xla=True),
        kernel="kernel",
        trace_fn=lambda _state, _results: {},
        initial_state="state",
    )
    assert isinstance(xla_runner, FakeFunction)
    assert xla_runner.kwargs["jit_compile"] is True
    assert xla_runner.kwargs["reduce_retracing"] is True
    assert len(sample_chain_calls) == 1


def test_full_chain_hmc_rejects_generic_dual_averaging_policy_in_phase3():
    generic_policy = HMCTuningPolicy.dual_averaging_step_size(
        num_adaptation_steps=3,
        target_accept_prob=0.75,
        source="tests/test_hmc_fixed_mass_step_tuning.py",
    )

    with pytest.raises(ValueError, match="fixed_mass_dual_averaging"):
        FullChainHMCConfig(
            num_results=4,
            num_burnin_steps=4,
            step_size=0.05,
            num_leapfrog_steps=2,
            seed=(20260613, 14),
            tuning_policy=generic_policy,
        )
