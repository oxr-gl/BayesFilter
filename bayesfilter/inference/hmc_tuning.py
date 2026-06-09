"""Reviewed HMC tuning-policy contracts with diagnostic-only adaptation helpers."""

from __future__ import annotations

import time
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

import numpy as np

from bayesfilter.inference.hmc_diagnostics import (
    HMCFailureClassification,
    HMCScreenResult,
    classify_hmc_screen,
)


HMC_TUNING_POLICY_LABELS = (
    "fixed_kernel_screen",
    "dual_averaging_step_size",
    "fixed_mass_dual_averaging",
    "windowed_mass_adaptation_future",
    "manual_ladder_diagnostic",
)

_DUAL_AVERAGING_LABELS = frozenset(
    {"dual_averaging_step_size", "fixed_mass_dual_averaging"}
)


@dataclass(frozen=True)
class HMCTuningPolicy:
    """Bounded HMC tuning-policy metadata.

    A policy is executable only when it is explicitly implemented and reviewed.
    Raw strings remain fail-closed for adaptive behavior; callers must pass a
    policy object to opt into any adaptation. The labels are deliberately more
    specific than TFP kernel names so result artifacts can distinguish fixed
    diagnostic screens, fixed-mass step-size adaptation, and future mass
    adaptation that is named but not executable in this phase.
    """

    label: str
    adaptation_policy: str
    num_adaptation_steps: int = 0
    target_accept_prob: float | None = None
    source: str = "reviewed_stage_7_phase_3"
    enabled: bool = False
    implemented: bool = True
    diagnostic_role: str = "bounded HMC tuning diagnostic"
    nonclaims: tuple[str, ...] = (
        "tuning policy metadata only",
        "no posterior convergence claim",
        "no sampler superiority claim",
        "no default adaptation readiness claim",
    )

    def __post_init__(self) -> None:
        label = str(self.label)
        if label not in HMC_TUNING_POLICY_LABELS:
            raise ValueError(
                "HMC tuning policy label must be one of "
                + ", ".join(HMC_TUNING_POLICY_LABELS)
            )
        adaptation_policy = str(self.adaptation_policy)
        if not adaptation_policy:
            raise ValueError("adaptation_policy must be non-empty")
        steps = int(self.num_adaptation_steps)
        if steps < 0:
            raise ValueError("num_adaptation_steps must be non-negative")
        target_accept = (
            None
            if self.target_accept_prob is None
            else float(self.target_accept_prob)
        )
        if target_accept is not None:
            if not np.isfinite(target_accept) or not (0.0 < target_accept < 1.0):
                raise ValueError("target_accept_prob must be finite and in (0, 1)")
        source = str(self.source)
        if not source:
            raise ValueError("source must be non-empty")
        role = str(self.diagnostic_role)
        if not role:
            raise ValueError("diagnostic_role must be non-empty")
        nonclaims = tuple(str(item) for item in self.nonclaims)
        if not nonclaims:
            raise ValueError("nonclaims must be non-empty")
        object.__setattr__(self, "label", label)
        object.__setattr__(self, "adaptation_policy", adaptation_policy)
        object.__setattr__(self, "num_adaptation_steps", steps)
        object.__setattr__(self, "target_accept_prob", target_accept)
        object.__setattr__(self, "source", source)
        object.__setattr__(self, "enabled", bool(self.enabled))
        object.__setattr__(self, "implemented", bool(self.implemented))
        object.__setattr__(self, "diagnostic_role", role)
        object.__setattr__(self, "nonclaims", nonclaims)

    @classmethod
    def fixed_kernel_screen(cls) -> "HMCTuningPolicy":
        """Current fail-closed BayesFilter behavior: no adaptive kernel."""

        return cls(
            label="fixed_kernel_screen",
            adaptation_policy="fixed_kernel_no_adaptation",
            num_adaptation_steps=0,
            target_accept_prob=None,
            enabled=False,
            implemented=True,
            diagnostic_role="fixed-kernel bounded HMC screen",
            nonclaims=(
                "fixed-kernel screen only",
                "no posterior convergence claim",
                "no sampler superiority claim",
                "no default adaptation readiness claim",
            ),
        )

    @classmethod
    def dual_averaging_step_size(
        cls,
        *,
        num_adaptation_steps: int,
        target_accept_prob: float,
        source: str,
    ) -> "HMCTuningPolicy":
        """Reviewed diagnostic-only step-size adaptation with fixed mass."""

        return cls(
            label="dual_averaging_step_size",
            adaptation_policy="dual_averaging_step_size",
            num_adaptation_steps=num_adaptation_steps,
            target_accept_prob=target_accept_prob,
            source=source,
            enabled=True,
            implemented=True,
            diagnostic_role="dual-averaging step-size diagnostic only",
            nonclaims=(
                "dual-averaging step-size diagnostic only",
                "fixed mass matrix; no mass adaptation claim",
                "no posterior convergence claim",
                "no sampler superiority claim",
                "no default adaptation readiness claim",
            ),
        )

    @classmethod
    def fixed_mass_dual_averaging(
        cls,
        *,
        num_adaptation_steps: int,
        target_accept_prob: float,
        source: str,
    ) -> "HMCTuningPolicy":
        """Alias-like reviewed policy for fixed-mass step-size adaptation."""

        return cls(
            label="fixed_mass_dual_averaging",
            adaptation_policy="dual_averaging_step_size",
            num_adaptation_steps=num_adaptation_steps,
            target_accept_prob=target_accept_prob,
            source=source,
            enabled=True,
            implemented=True,
            diagnostic_role="fixed-mass dual-averaging diagnostic only",
            nonclaims=(
                "fixed-mass dual-averaging diagnostic only",
                "mass matrix is supplied/fixed; no windowed mass adaptation claim",
                "no posterior convergence claim",
                "no sampler superiority claim",
                "no default adaptation readiness claim",
            ),
        )

    @classmethod
    def windowed_mass_adaptation_future(cls) -> "HMCTuningPolicy":
        """Named future policy that is intentionally not executable."""

        return cls(
            label="windowed_mass_adaptation_future",
            adaptation_policy="windowed_mass_adaptation_future",
            num_adaptation_steps=0,
            target_accept_prob=None,
            enabled=True,
            implemented=False,
            diagnostic_role="future policy placeholder; not executable",
            nonclaims=(
                "future mass-adaptation label only",
                "not implemented or executable in Stage 7 / accepted Phase 3",
                "no posterior convergence claim",
                "no default adaptation readiness claim",
            ),
        )

    @classmethod
    def manual_ladder_diagnostic(cls) -> "HMCTuningPolicy":
        """Metadata for externally reviewed fixed-kernel ladders."""

        return cls(
            label="manual_ladder_diagnostic",
            adaptation_policy="fixed_kernel_manual_ladder",
            num_adaptation_steps=0,
            target_accept_prob=None,
            enabled=False,
            implemented=False,
            diagnostic_role="manual ladder metadata only; not an adaptive kernel",
            nonclaims=(
                "manual fixed-kernel ladder metadata only",
                "not executable by the BayesFilter HMC runner in this phase",
                "no posterior convergence claim",
                "no sampler superiority claim",
            ),
        )

    @property
    def uses_dual_averaging(self) -> bool:
        return self.label in _DUAL_AVERAGING_LABELS

    def payload(self) -> Mapping[str, Any]:
        return {
            "label": self.label,
            "adaptation_policy": self.adaptation_policy,
            "num_adaptation_steps": self.num_adaptation_steps,
            "target_accept_prob": self.target_accept_prob,
            "source": self.source,
            "enabled": self.enabled,
            "implemented": self.implemented,
            "diagnostic_role": self.diagnostic_role,
            "nonclaims": self.nonclaims,
        }


@dataclass(frozen=True)
class HMCTuningDiagnosticResult:
    """Tiny adaptation diagnostic result; not posterior evidence."""

    policy: HMCTuningPolicy
    diagnostics: Mapping[str, Any]
    trace: Mapping[str, Any]
    metadata: Mapping[str, Any]

    def payload(self) -> Mapping[str, Any]:
        return {
            "policy": self.policy.payload(),
            "diagnostics": self.diagnostics,
            "trace": self.trace,
            "metadata": self.metadata,
        }


def normalize_hmc_tuning_policy(
    tuning_policy: str | HMCTuningPolicy | None,
) -> HMCTuningPolicy:
    """Normalize reviewed tuning policies while keeping raw adaptation fail-closed."""

    if tuning_policy is None:
        return HMCTuningPolicy.fixed_kernel_screen()
    if isinstance(tuning_policy, HMCTuningPolicy):
        return tuning_policy
    label = str(tuning_policy)
    if label in {"fixed_kernel_no_adaptation", "fixed_kernel_screen"}:
        return HMCTuningPolicy.fixed_kernel_screen()
    raise ValueError(
        "HMC adaptation is fail-closed: use 'fixed_kernel_no_adaptation' "
        "or pass a reviewed HMCTuningPolicy object"
    )


def require_executable_tuning_policy(policy: HMCTuningPolicy) -> HMCTuningPolicy:
    if not policy.implemented:
        raise ValueError(f"HMC tuning policy {policy.label!r} is not implemented")
    if policy.label == "fixed_kernel_screen":
        return policy
    if policy.uses_dual_averaging:
        if not policy.enabled:
            raise ValueError("dual-averaging tuning policy must be enabled")
        if policy.num_adaptation_steps <= 0:
            raise ValueError("dual-averaging tuning policy requires adaptation steps")
        if policy.target_accept_prob is None:
            raise ValueError("dual-averaging tuning policy requires target_accept_prob")
        return policy
    raise ValueError(f"HMC tuning policy {policy.label!r} is not executable")


def classify_fixed_kernel_screen_with_tuning_policy(
    policy: HMCTuningPolicy,
    screen: HMCScreenResult,
    *,
    acceptance_rate_by_chain: Any,
    step_size: float | None = None,
    num_leapfrog_steps: int | None = None,
    max_abs_log_accept_ratio: float | None = None,
) -> HMCFailureClassification:
    """Classify a fixed-kernel screen under the explicit Stage 7 policy label."""

    policy = require_executable_tuning_policy(policy)
    if policy.label != "fixed_kernel_screen":
        raise ValueError("fixed-kernel screen classification requires fixed_kernel_screen")
    return classify_hmc_screen(
        screen,
        acceptance_rate_by_chain=acceptance_rate_by_chain,
        fixed_kernel_used=True,
        num_adaptation_steps_zero=True,
        step_size=step_size,
        num_leapfrog_steps=num_leapfrog_steps,
        max_abs_log_accept_ratio=max_abs_log_accept_ratio,
    )


def classify_hmc_tuning_diagnostic(
    policy: HMCTuningPolicy,
    *,
    target_evaluation: Any | None = None,
    required_arrays_finite: bool = True,
    hmc_error: Mapping[str, Any] | None = None,
) -> Mapping[str, Any]:
    """Separate tuning telemetry from target validity and convergence claims."""

    require_executable_tuning_policy(policy)
    if hmc_error is not None:
        return {
            "passed": False,
            "classification": "hmc_execution_error",
            "diagnostic_role": "hard_veto",
            "nonclaims": policy.nonclaims,
        }
    if getattr(target_evaluation, "fallback_used", False):
        return {
            "passed": False,
            "classification": "target_invalidity_not_tuning_success",
            "diagnostic_role": "hard_veto",
            "failure_label": getattr(target_evaluation, "failure_label", None),
            "nonclaims": policy.nonclaims,
        }
    if not bool(required_arrays_finite):
        return {
            "passed": False,
            "classification": "nonfinite_tuning_diagnostic",
            "diagnostic_role": "hard_veto",
            "nonclaims": policy.nonclaims,
        }
    return {
        "passed": True,
        "classification": "tuning_diagnostic_passed_not_convergence",
        "diagnostic_role": "diagnostic_only",
        "reports_posterior_convergence": False,
        "nonclaims": policy.nonclaims,
    }


def run_gaussian_dual_averaging_diagnostic(
    policy: HMCTuningPolicy,
    *,
    initial_state: Any,
    num_results: int = 4,
    num_burnin_steps: int = 4,
    step_size: float = 0.05,
    num_leapfrog_steps: int = 2,
    seed: tuple[int, int] = (20260609, 3),
) -> HMCTuningDiagnosticResult:
    """Run a tiny Gaussian TFP diagnostic for reviewed dual averaging.

    This helper exists to prove telemetry extraction and policy gating. It is
    not a posterior validation run and intentionally uses only a standard
    Gaussian target.
    """

    policy = require_executable_tuning_policy(policy)
    if not policy.uses_dual_averaging:
        raise ValueError("Gaussian dual-averaging diagnostic requires a dual policy")
    for name, value in {
        "num_results": num_results,
        "num_burnin_steps": num_burnin_steps,
        "num_leapfrog_steps": num_leapfrog_steps,
    }.items():
        if int(value) <= 0:
            raise ValueError(f"{name} must be positive")
    if policy.num_adaptation_steps > int(num_burnin_steps):
        raise ValueError("num_adaptation_steps must not exceed num_burnin_steps")
    step = float(step_size)
    if not np.isfinite(step) or step <= 0.0:
        raise ValueError("step_size must be positive and finite")

    import tensorflow as tf
    import tensorflow_probability as tfp

    state = tf.convert_to_tensor(initial_state, dtype=tf.float64)
    tfm = tfp.mcmc

    def target_log_prob(x: Any) -> Any:
        values = tf.convert_to_tensor(x, dtype=tf.float64)
        return -0.5 * tf.reduce_sum(tf.square(values), axis=-1)

    base_kernel = tfm.HamiltonianMonteCarlo(
        target_log_prob_fn=target_log_prob,
        step_size=tf.constant(step, dtype=tf.float64),
        num_leapfrog_steps=int(num_leapfrog_steps),
    )
    kernel = tfm.DualAveragingStepSizeAdaptation(
        inner_kernel=base_kernel,
        num_adaptation_steps=policy.num_adaptation_steps,
        target_accept_prob=tf.constant(policy.target_accept_prob, dtype=tf.float64),
    )

    def trace_fn(_state: Any, kernel_results: Any) -> Mapping[str, Any]:
        return {
            "is_accepted": kernel_results.inner_results.is_accepted,
            "log_accept_ratio": kernel_results.inner_results.log_accept_ratio,
            "step_size": kernel_results.new_step_size,
            "target_accept_prob": kernel_results.target_accept_prob,
            "num_adaptation_steps": kernel_results.num_adaptation_steps,
        }

    start = time.perf_counter()
    samples, trace = tfm.sample_chain(
        num_results=int(num_results),
        num_burnin_steps=int(num_burnin_steps),
        current_state=state,
        kernel=kernel,
        trace_fn=trace_fn,
        seed=tf.constant(tuple(int(item) for item in seed), dtype=tf.int32),
    )
    elapsed = time.perf_counter() - start

    sample_array = np.asarray(samples.numpy(), dtype=float)
    step_sizes = np.asarray(trace["step_size"].numpy(), dtype=float)
    accepted = np.asarray(trace["is_accepted"].numpy(), dtype=bool)
    log_accept_ratio = np.asarray(trace["log_accept_ratio"].numpy(), dtype=float)
    target_accept = float(np.asarray(trace["target_accept_prob"].numpy()).ravel()[-1])
    adaptation_steps = int(
        np.asarray(trace["num_adaptation_steps"].numpy()).ravel()[-1]
    )
    diagnostics = {
        "policy_label": policy.label,
        "adaptation_policy": policy.adaptation_policy,
        "num_adaptation_steps": adaptation_steps,
        "target_accept_prob": target_accept,
        "initial_step_size": step,
        "final_step_size": float(np.asarray(step_sizes).ravel()[-1]),
        "final_step_size_finite": bool(np.all(np.isfinite(step_sizes))),
        "acceptance_rate": float(np.mean(accepted)) if accepted.size else float("nan"),
        "log_accept_ratio_finite": bool(np.all(np.isfinite(log_accept_ratio))),
        "finite_sample_count": int(np.sum(np.all(np.isfinite(sample_array), axis=-1))),
        "nonfinite_sample_count": int(
            np.sum(~np.all(np.isfinite(sample_array), axis=-1))
        ),
        "reports_posterior_convergence": False,
    }
    metadata = {
        "runtime": "tfp.mcmc.DualAveragingStepSizeAdaptation",
        "diagnostic_role": policy.diagnostic_role,
        "elapsed_s": elapsed,
        "nonclaims": policy.nonclaims,
    }
    trace_payload = {
        "is_accepted": accepted.tolist(),
        "log_accept_ratio": log_accept_ratio.tolist(),
        "step_size": step_sizes.tolist(),
    }
    return HMCTuningDiagnosticResult(
        policy=policy,
        diagnostics=diagnostics,
        trace=trace_payload,
        metadata=metadata,
    )
