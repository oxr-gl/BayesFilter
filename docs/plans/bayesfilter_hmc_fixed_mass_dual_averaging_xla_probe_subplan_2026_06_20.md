# BayesFilter HMC Fixed-Mass Dual-Averaging XLA Probe Subplan

Date: 2026-06-20

Supervisor/executor: Codex

Read-only reviewer: Claude Code, path-only bounded review

Repository: `/home/ubuntu/python/BayesFilter`

## Phase Objective

Test and, if justified, narrow the BayesFilter HMC guard that currently blocks
all `tuning_policy.uses_dual_averaging and use_xla` configurations. The only
candidate for unblocking is the reviewed `fixed_mass_dual_averaging` policy on
the existing full-chain TFP HMC path with explicit full-chain XLA diagnostic
authority.

## Entry Conditions Inherited From Previous Phase

- MacroFinance active filtering/HMC runtime authority is BayesFilter.
- CCMA mixed-frequency HMC remains blocked from an XLA-first adaptive run until
  BayesFilter can demonstrate the exact wrapper path needed by CCMA.
- Prior status was conservative: BayesFilter rejected dual averaging with XLA at
  configuration construction time, before testing TFP/XLA execution.
- Existing fixed-kernel XLA Gaussian full-chain tests and non-XLA fixed-mass
  dual-averaging telemetry tests are the local reference checks.
- This phase is a small Host-XLA engineering probe, not a GPU readiness run and
  not a posterior validation run.

## Required Artifacts

- This subplan under `docs/plans/`.
- Claude path-only review record under `docs/plans/`.
- Focused BayesFilter patch, if the review and local audit permit it.
- Focused test output preserved in the result note.
- Phase result / close record under `docs/plans/`.
- If this phase passes, a refreshed next subplan for the CCMA exact target
  fixed-mass dual-averaging XLA canary in MacroFinance.

## Required Checks, Tests, And Reviews

- Skeptical pre-execution audit of this subplan.
- Claude read-only path review for consistency, feasibility, artifact coverage,
  and boundary safety.
- Local source audit that generic dual averaging remains fail-closed.
- Targeted Python syntax/import check with bytecode redirected outside the repo.
- Focused pytest checks, with repo cache/bytecode writes avoided:
  - fixed-kernel XLA Gaussian full-chain smoke remains passing;
  - non-XLA fixed-mass dual-averaging telemetry remains passing;
  - full-chain XLA authority-boundary tests remain passing, including
    unreviewed authority rejection and target-only XLA rejection;
  - raw-string `adaptation_policy="dual_averaging"` remains blocked;
  - reviewed-but-generic `HMCTuningPolicy.dual_averaging_step_size` remains
    blocked;
  - new fixed-mass dual-averaging XLA Gaussian exact-path test compiles/runs and
    records `jit_compile=True`, finite samples, finite final step size, adaptive
    trace fields (`step_size`, `target_accept_prob`, `num_adaptation_steps`),
    and explicit nonclaims.

## Evidence Contract

Scientific/engineering question:

Can BayesFilter's exact `run_full_chain_tfp_hmc` wrapper run TFP
`HamiltonianMonteCarlo` wrapped in `DualAveragingStepSizeAdaptation` under
`tf.function(jit_compile=True)` for the existing reviewed Gaussian
full-chain-XLA fixture?

Exact baseline/comparator:

- Current fixed-kernel XLA Gaussian full-chain test.
- Current non-XLA reviewed fixed-mass dual-averaging Gaussian telemetry test.
- Current fail-closed generic dual-averaging policy test.

Primary pass/fail criterion:

- The focused fixed-mass dual-averaging XLA Gaussian test passes on the exact
  BayesFilter full-chain wrapper, and the guard remains closed for generic
  dual-averaging policies.

Veto diagnostics:

- XLA compile/runtime failure in the exact wrapper path.
- Non-finite samples or non-finite final adapted step size in the tiny fixture.
- Missing adaptive trace fields required by the wrapper contract.
- Accidental admission of generic `dual_averaging_step_size` under XLA.
- Accidental admission of raw string `adaptation_policy="dual_averaging"`.
- Bypass of `ValueScoreCapability.full_chain_xla_diagnostic_ready`.
- Any active MacroFinance-local HMC/filtering use.

Explanatory-only diagnostics:

- Acceptance rate, log-accept-ratio values, timing, and exact adapted step-size
  value. These explain the smoke result but do not rank samplers or validate
  posterior inference.

What will not be concluded even if the run passes:

- No CCMA 314D readiness claim.
- No GPU readiness claim.
- No posterior convergence or posterior correctness claim.
- No performance superiority claim.
- No mass-adaptation claim.
- No claim that all TFP dual-averaging configurations are XLA-compatible.

Artifact preserving the result:

- Phase result note under `docs/plans/`, including command, environment, test
  outcome, decision table, inference-status table, and next handoff.

## Skeptical Pre-Execution Audit

- Wrong baseline risk: avoided by comparing against fixed-kernel XLA, non-XLA
  fixed-mass dual averaging, and generic-policy rejection.
- Proxy metric risk: finite tiny-chain output is only an engineering pass/fail
  screen, not a scientific promotion criterion.
- Missing stop condition risk: explicit stops are listed below.
- Unfair comparison risk: no speed or sampler ranking will be inferred.
- Hidden assumption risk: this phase assumes the reviewed Gaussian fixture is a
  sufficient wrapper-level exact-path probe, not evidence for CCMA target
  readiness.
- Stale context risk: local dirty diffs will be inspected before patching, and
  unrelated dirty work will not be reverted.
- Artifact mismatch risk: the result artifact must name the exact tests and
  preserve nonclaims; otherwise this phase cannot hand off.

Audit decision: pass for bounded execution after Claude review.

## Forbidden Claims And Actions

- Do not use MacroFinance-local `filters.*`, `inference.hmc*`,
  `inference.mass_matrix`, or `inference.posterior_adapter` as active runtime.
- Do not send whole files to Claude; use path-only bounded review.
- Do not claim GPU readiness from CPU-hidden Host-XLA tests.
- Do not claim CCMA readiness from the Gaussian fixture.
- Do not unblock raw string `adaptation_policy="dual_averaging"`.
- Do not unblock generic `HMCTuningPolicy.dual_averaging_step_size` for the
  full-chain XLA wrapper.
- Do not run an overnight or long CCMA HMC chain in this phase.

## Exact Next-Phase Handoff Conditions

If this phase passes:

- BayesFilter guard is narrowed only for reviewed `fixed_mass_dual_averaging`
  with normal full-chain XLA authority checks still active.
- Focused BayesFilter tests pass and the result note records the exact command.
- MacroFinance receives a refreshed CCMA exact-target fixed-mass dual-averaging
  XLA canary subplan, but no full HMC run is authorized yet.

If this phase fails:

- The all-dual-averaging XLA block remains in force or is restored.
- A blocker result records the failing exact path, failure mode, and smallest
  next repair option.

## Stop Conditions

- Claude identifies a material plan flaw that cannot be patched within five
  review rounds.
- BayesFilter write approval is unavailable.
- The exact TFP/XLA wrapper path fails to compile or run and the failure is not
  a trivial local coding defect.
- Generic dual averaging becomes accepted under XLA.
- Required result artifact or nonclaims cannot be written.

## End-Of-Phase Requirements

1. Run the required focused local checks.
2. Write a phase result / close record.
3. Draft or refresh the next subplan.
4. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
