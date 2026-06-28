# BayesFilter HMC Kernel Tuning XLA Parameter Repair Plan

Date: 2026-06-22

Status: `in_progress`

## Objective

Repair the generic BayesFilter one-call HMC kernel tuning path so HMC runtime
stages can run either non-XLA or XLA according to an explicit config parameter.

## Runtime Classification

Accepted TF/TFP runtime. This changes only BayesFilter-owned HMC tuning
configuration and capability propagation around `tfp.mcmc.sample_chain`.

## Evidence Contract

Question: Can the generic HMC kernel tuning stages propagate an explicit
`use_xla` request without demoting already-reviewed full-chain XLA adapter
authority?

Baseline: current generic path hard-codes `use_xla=False` in bootstrap,
windowed-mass, fixed-mass step, frozen-step trajectory, and final verification
configs, and the latent fixed-mass wrapper reports `xla_hmc_ready=False`.

Primary pass criterion: focused tests show default configs remain non-XLA while
`use_xla=True` propagates into stage `FullChainHMCConfig` payloads and the
latent wrapper preserves XLA authority only from a base adapter with accepted
full-chain XLA authority.

Veto diagnostics: unauthorized adapters must not become XLA-ready; eager chain
execution with `use_xla=True` must continue to fail through existing
`FullChainHMCConfig` validation; no MacroFinance-local HMC runtime may be used.

Explanatory diagnostics: config payloads, wrapper capability payloads, focused
unit-test metadata.

Nonclaims: no posterior convergence, sampler superiority, performance
improvement, GPU readiness, or scientific validity is concluded from this
repair.

## Skeptical Plan Audit

Wrong-baseline risk: the issue is not only a stage config hard-code; the latent
fixed-mass wrapper also strips XLA authority. The repair must address both.

Proxy-metric risk: no runtime speedup claim will be made from unit tests.

Hidden-assumption risk: `use_xla=True` must not authorize XLA by itself.
BayesFilter's existing full-chain XLA authority validation remains the gate.

Environment risk: focused tests can run CPU-only and need not initialize GPU.

Artifact-answer risk: config/capability tests directly answer whether XLA can
be selected by policy and propagated through wrappers.

Audit decision: proceed with a scoped implementation.

## Required Changes

- Add `use_xla: bool = False` to public and stage tuning configs.
- Include `use_xla` in config payloads and Phase 7 subconfig handoffs.
- Pass `use_xla=config.use_xla` into all generic `FullChainHMCConfig` builders.
- Preserve latent wrapper XLA/full-chain authority only when the base adapter is
  already accepted for XLA and the target scope is bound to the wrapper scope.
- Add focused tests for default non-XLA behavior, opt-in propagation, and
  fail-closed wrapper behavior.

## Stop Conditions

Stop if the repair requires changing the semantics of full-chain XLA authority,
if focused tests show unauthorized adapters can reach XLA, or if config changes
would expose step size, leapfrog count, budget schedules, or posterior claims to
model clients.
